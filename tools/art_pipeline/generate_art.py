from __future__ import annotations

import argparse
import base64
import getpass
import json
import os
import shutil
import time
from contextlib import ExitStack
from datetime import datetime
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    Image = None

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
MANIFEST_PATH = HERE / "tasks.json"
STYLE_PATH = HERE / "style_bible.txt"
ENV_PATH = HERE / ".env"
OUTPUT_ROOT = ROOT / "art_output"
BACKUP_ROOT = ROOT / "art_backup"
LOG_PATH = OUTPUT_ROOT / "generation_log.jsonl"

SUPPORTED_IMAGES = {".png", ".jpg", ".jpeg", ".webp"}
DEFAULT_MODEL = "gpt-image-2.5-sunburst"
FAST_MODEL = "gpt-image-2.5-flare"

CATEGORY_DIRS = {
    "ch": ROOT / "game" / "images" / "ch",
    "bg": ROOT / "game" / "images" / "bg",
    "cg": ROOT / "game" / "images" / "cg",
}

CATEGORY_PROMPTS = {
    "ch": (
        "Create a production-quality remaster of this exact visual-novel character sprite. "
        "Preserve identity, face shape, hair, clothing, body proportions, pose intent and emotion. "
        "Improve anatomy, line confidence, material rendering, facial detail and lighting consistency. "
        "Full-body sprite, clean silhouette, transparent background. Do not redesign the character."
    ),
    "bg": (
        "Create a production-quality cinematic remaster of this exact visual-novel background. "
        "Preserve the same location, camera angle, architecture, layout and story-readable landmarks. "
        "Improve perspective, materials, industrial detail, lighting and atmosphere. No people, no text, no logos."
    ),
    "cg": (
        "Create a production-quality cinematic remaster of this exact visual-novel CG. "
        "Preserve the scene, characters, story beat, composition and emotional meaning. "
        "Improve anatomy, facial consistency, environment detail, lighting, depth and cinematic polish. "
        "Do not add text, captions or watermarks."
    ),
}


def load_env() -> None:
    if not ENV_PATH.exists():
        return
    for raw in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def ensure_api_key() -> str:
    load_env()
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if key:
        return key

    print("\nДля генерации нужен OpenAI API key.")
    print("Ключ будет сохранён только локально в tools/art_pipeline/.env и игнорируется Git.")
    key = getpass.getpass("OPENAI_API_KEY: ").strip()
    if not key:
        raise SystemExit("Ключ не введён.")

    ENV_PATH.write_text(f"OPENAI_API_KEY={key}\n", encoding="utf-8")
    os.environ["OPENAI_API_KEY"] = key
    return key


def load_style() -> str:
    return STYLE_PATH.read_text(encoding="utf-8").strip()


def load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def image_files(folder: Path) -> list[Path]:
    if not folder.exists():
        return []
    return sorted(
        p for p in folder.iterdir()
        if p.is_file() and p.suffix.lower() in SUPPORTED_IMAGES
    )


def output_format_for(path: Path, category: str) -> str:
    if category == "ch":
        return "png"
    if path.suffix.lower() in {".jpg", ".jpeg"}:
        return "jpeg"
    if path.suffix.lower() == ".webp":
        return "webp"
    return "png"


def api_size_for(category: str) -> str:
    return "1024x1536" if category == "ch" else "2048x1152"


def auto_remaster_tasks(category: str) -> list[dict]:
    source_dir = CATEGORY_DIRS[category]
    tasks = []
    for source in image_files(source_dir):
        rel = source.relative_to(ROOT).as_posix()
        target = (OUTPUT_ROOT / "remaster" / category / source.name).relative_to(ROOT).as_posix()
        tasks.append({
            "id": f"remaster-{category}-{source.stem}",
            "category": category,
            "mode": "edit",
            "refs": [rel],
            "target": target,
            "apply_to": rel,
            "prompt": CATEGORY_PROMPTS[category],
            "size": api_size_for(category),
            "quality": "high",
            "background": "transparent" if category == "ch" else "opaque",
            "output_format": output_format_for(source, category),
            "preserve_reference_size": True,
        })
    return tasks


def curated_tasks(category: str | None = None) -> list[dict]:
    manifest = load_manifest()
    tasks = [t for t in manifest.get("tasks", []) if t.get("enabled", True)]
    if category:
        tasks = [t for t in tasks if t.get("category") == category]
    return tasks


def compose_prompt(task: dict) -> str:
    style = load_style()
    specific = task.get("prompt", "").strip()
    return f"{style}\n\nTASK:\n{specific}".strip()


def source_reference_size(task: dict) -> tuple[int, int] | None:
    if Image is None or not task.get("preserve_reference_size"):
        return None
    refs = task.get("refs") or []
    if not refs:
        return None
    ref = ROOT / refs[0]
    if not ref.exists():
        return None
    try:
        with Image.open(ref) as im:
            return im.size
    except Exception:
        return None


def final_size_for(task: dict) -> tuple[int, int] | None:
    explicit = task.get("final_size")
    if explicit and isinstance(explicit, list) and len(explicit) == 2:
        return int(explicit[0]), int(explicit[1])
    ref_size = source_reference_size(task)
    if ref_size:
        return ref_size
    if task.get("category") in {"bg", "cg"}:
        return 1920, 1080
    return None


def normalize_image(path: Path, task: dict) -> None:
    if Image is None:
        return
    final_size = final_size_for(task)
    if not final_size:
        return
    with Image.open(path) as im:
        if im.size == final_size:
            return
        if im.mode not in {"RGB", "RGBA"}:
            im = im.convert("RGBA" if task.get("background") == "transparent" else "RGB")
        resized = im.resize(final_size, Image.Resampling.LANCZOS)
        fmt = task.get("output_format", "png")
        save_format = {"jpeg": "JPEG", "jpg": "JPEG", "webp": "WEBP"}.get(fmt, "PNG")
        kwargs = {"quality": 95} if save_format in {"JPEG", "WEBP"} else {}
        if save_format == "JPEG" and resized.mode == "RGBA":
            resized = resized.convert("RGB")
        resized.save(path, format=save_format, **kwargs)


def save_result(result, target: Path, task: dict) -> None:
    if not getattr(result, "data", None):
        raise RuntimeError("API не вернул изображение")
    encoded = result.data[0].b64_json
    if not encoded:
        raise RuntimeError("API вернул пустой b64_json")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(base64.b64decode(encoded))
    normalize_image(target, task)


def call_api(client: OpenAI, task: dict, model: str, quality_override: str | None = None):
    prompt = compose_prompt(task)
    quality = quality_override or task.get("quality", "high")
    kwargs = {
        "model": model,
        "prompt": prompt,
        "size": task.get("size", "auto"),
        "quality": quality,
        "background": task.get("background", "auto"),
        "output_format": task.get("output_format", "png"),
    }

    mode = task.get("mode", "generate")
    refs = [ROOT / p for p in task.get("refs", [])]

    if mode == "edit":
        missing = [str(p) for p in refs if not p.exists()]
        if missing:
            raise FileNotFoundError("Не найдены референсы: " + ", ".join(missing))
        with ExitStack() as stack:
            opened = [stack.enter_context(open(p, "rb")) for p in refs]
            image_arg = opened[0] if len(opened) == 1 else opened
            return client.images.edit(image=image_arg, **kwargs)

    return client.images.generate(**kwargs)


def append_log(record: dict) -> None:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def run_tasks(tasks: list[dict], model: str, quality_override: str | None, force: bool, dry_run: bool) -> None:
    if not tasks:
        print("Нет задач.")
        return

    print(f"\nЗадач: {len(tasks)}")
    print(f"Модель: {model}")
    if quality_override:
        print(f"Качество override: {quality_override}")

    if dry_run:
        for i, task in enumerate(tasks, 1):
            print(f"\n[{i}/{len(tasks)}] {task['id']}")
            print(f"  mode={task.get('mode', 'generate')} target={task.get('target')}")
            print(f"  refs={task.get('refs', [])}")
            print(f"  size={task.get('size')} quality={task.get('quality')} background={task.get('background')}")
            print("  prompt:", compose_prompt(task)[:700].replace("\n", " "), "...")
        return

    if OpenAI is None:
        raise SystemExit("Пакет openai не установлен. Запусти GENERATE_ART.bat ещё раз.")

    api_key = ensure_api_key()
    client = OpenAI(api_key=api_key)

    for i, task in enumerate(tasks, 1):
        target = ROOT / task["target"]
        print(f"\n[{i}/{len(tasks)}] {task['id']}")
        if target.exists() and not force:
            print(f"  SKIP: уже существует {target.relative_to(ROOT)}")
            continue

        started = time.time()
        status = "ok"
        error = None
        try:
            result = call_api(client, task, model=model, quality_override=quality_override)
            save_result(result, target, task)
            print(f"  OK -> {target.relative_to(ROOT)}")
        except Exception as exc:
            status = "error"
            error = repr(exc)
            print(f"  ERROR: {exc}")

        append_log({
            "time": datetime.now().isoformat(timespec="seconds"),
            "task": task.get("id"),
            "status": status,
            "target": task.get("target"),
            "model": model,
            "seconds": round(time.time() - started, 2),
            "error": error,
        })


def apply_outputs(tasks: list[dict]) -> None:
    candidates = []
    for task in tasks:
        apply_to = task.get("apply_to")
        if not apply_to:
            continue
        src = ROOT / task["target"]
        dst = ROOT / apply_to
        if src.exists():
            candidates.append((task, src, dst))

    if not candidates:
        print("Нет готовых файлов для применения.")
        return

    print(f"\nБудут заменены {len(candidates)} файлов в game/images.")
    answer = input("Продолжить? Будет создан backup. [y/N]: ").strip().lower()
    if answer not in {"y", "yes", "д", "да"}:
        print("Отменено.")
        return

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_dir = BACKUP_ROOT / stamp

    for task, src, dst in candidates:
        if dst.exists():
            backup = backup_dir / dst.relative_to(ROOT)
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(dst, backup)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"  APPLY {task['id']} -> {dst.relative_to(ROOT)}")

    print(f"Backup: {backup_dir.relative_to(ROOT)}")


def choose_model() -> str:
    raw = input("Модель: [1] Sunburst quality  [2] Flare faster  (Enter=1): ").strip()
    return FAST_MODEL if raw == "2" else DEFAULT_MODEL


def confirm_generation(tasks: list[dict]) -> bool:
    print(f"Подготовлено задач: {len(tasks)}")
    print("Генерация использует платный OpenAI API. Уже существующие результаты будут пропущены.")
    answer = input("Запустить? [y/N]: ").strip().lower()
    return answer in {"y", "yes", "д", "да"}


def menu() -> None:
    while True:
        print("\n" + "=" * 72)
        print(" PURPLE SHIFT - GPT IMAGE 2.5 ART PIPELINE")
        print("=" * 72)
        print("1. Показать план curated-артов без генерации")
        print("2. Ремастер всех персонажей")
        print("3. Ремастер всех фонов")
        print("4. Ремастер всех CG")
        print("5. Сгенерировать новые curated-арты")
        print("6. ПОЛНЫЙ ПРОГОН: персонажи + фоны + CG + curated")
        print("7. Применить готовые ремастеры в игру (с backup)")
        print("8. Выйти")
        choice = input("\nВыбор: ").strip()

        if choice == "1":
            run_tasks(curated_tasks(), DEFAULT_MODEL, None, False, True)
            continue
        if choice == "8":
            return

        if choice == "2":
            tasks = auto_remaster_tasks("ch")
        elif choice == "3":
            tasks = auto_remaster_tasks("bg")
        elif choice == "4":
            tasks = auto_remaster_tasks("cg")
        elif choice == "5":
            tasks = curated_tasks()
        elif choice == "6":
            tasks = (
                auto_remaster_tasks("ch")
                + auto_remaster_tasks("bg")
                + auto_remaster_tasks("cg")
                + curated_tasks()
            )
        elif choice == "7":
            all_tasks = auto_remaster_tasks("ch") + auto_remaster_tasks("bg") + auto_remaster_tasks("cg")
            apply_outputs(all_tasks)
            continue
        else:
            print("Неизвестный пункт.")
            continue

        if confirm_generation(tasks):
            run_tasks(tasks, choose_model(), None, False, False)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Purple Shift GPT Image 2.5 art pipeline")
    p.add_argument("--menu", action="store_true")
    p.add_argument("--category", choices=["ch", "bg", "cg", "curated", "all"])
    p.add_argument("--model", default=DEFAULT_MODEL, choices=[DEFAULT_MODEL, FAST_MODEL])
    p.add_argument("--quality", choices=["low", "medium", "high", "xhigh", "max", "auto"])
    p.add_argument("--force", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--task", help="Запустить одну curated-задачу по id")
    p.add_argument("--apply", choices=["ch", "bg", "cg", "all"])
    return p.parse_args()


def main() -> None:
    args = parse_args()
    if args.menu or (not args.category and not args.task and not args.apply):
        menu()
        return

    if args.apply:
        cats = ["ch", "bg", "cg"] if args.apply == "all" else [args.apply]
        tasks = []
        for cat in cats:
            tasks.extend(auto_remaster_tasks(cat))
        apply_outputs(tasks)
        return

    if args.task:
        tasks = [t for t in curated_tasks() if t.get("id") == args.task]
        if not tasks:
            raise SystemExit(f"Не найдена задача: {args.task}")
    elif args.category == "curated":
        tasks = curated_tasks()
    elif args.category == "all":
        tasks = auto_remaster_tasks("ch") + auto_remaster_tasks("bg") + auto_remaster_tasks("cg") + curated_tasks()
    else:
        tasks = auto_remaster_tasks(args.category)

    run_tasks(tasks, args.model, args.quality, args.force, args.dry_run)


if __name__ == "__main__":
    main()
