from __future__ import annotations

import argparse
import base64
import getpass
import json
import mimetypes
import os
import shutil
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None

try:
    from PIL import Image
except ImportError:
    Image = None


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
MANIFEST_PATH = HERE / "tasks.json"
STYLE_PATH = HERE / "style_bible.txt"
ENV_PATH = HERE / ".env"
OUTPUT_ROOT = ROOT / "art_output"
BACKUP_ROOT = ROOT / "art_backup"
LOG_PATH = OUTPUT_ROOT / "generation_log.jsonl"

SUPPORTED_IMAGES = {".png", ".jpg", ".jpeg", ".webp"}

GENAPI_BASE = "https://api.gen-api.ru/api/v1"
GENAPI_NETWORK = "gpt-image-2-5"
DEFAULT_MODEL = "sunburst"
FAST_MODEL = "flare"
POLL_SECONDS = 5
POLL_TIMEOUT_SECONDS = 15 * 60
DEFAULT_WORKERS = 5
LOG_LOCK = threading.Lock()

CHARACTER_CANONICAL = {
    "nov": "game/images/ch/nov_relief.png",
    "vet": "game/images/ch/vet1.png",
    "mem": "game/images/ch/mem_serious.png",
    "super": "game/images/ch/super_stern.png",
    "curator": "game/images/ch/curator.png",
}

CATEGORY_DIRS = {
    "ch": ROOT / "game" / "images" / "ch",
    "bg": ROOT / "game" / "images" / "bg",
    "cg": ROOT / "game" / "images" / "cg",
}

CATEGORY_PROMPTS = {
    "ch": (
        "IDENTITY-LOCKED sprite remaster. REFERENCE 1 is the canonical identity anchor for this exact character. "
        "If REFERENCE 2 is present, use it ONLY for the target pose/expression/variant; do not borrow a new face from it. "
        "The output must unmistakably be the same person as REFERENCE 1: same face geometry, eyes, nose, jaw, hair, "
        "apparent age, body proportions, work uniform design and silhouette. Preserve the target sprite's pose and emotion. "
        "Do not beautify, age up/down, masculinize/feminize, photorealize, redesign or change hairstyle/clothes. "
        "Only improve drawing cleanliness, anatomy, hands, fabric rendering, line confidence and subtle lighting. "
        "Full-body 2D visual-novel sprite, transparent background."
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

    key = os.environ.get("GENAPI_API_KEY", "").strip()
    if key:
        return key

    # Migration for the first version of the art pipeline:
    # the user may already have stored a GenAPI key under OPENAI_API_KEY.
    legacy = os.environ.get("OPENAI_API_KEY", "").strip()
    if legacy:
        ENV_PATH.write_text(f"GENAPI_API_KEY={legacy}\n", encoding="utf-8")
        os.environ["GENAPI_API_KEY"] = legacy
        print("Найден сохранённый ключ. Переключил локальный .env на GenAPI.")
        return legacy

    print("\nДля генерации нужен API-ключ GenAPI.")
    print("Ключ сохранится только локально в tools/art_pipeline/.env и игнорируется Git.")
    key = getpass.getpass("GENAPI_API_KEY: ").strip()
    if not key:
        raise SystemExit("Ключ не введён.")

    ENV_PATH.write_text(f"GENAPI_API_KEY={key}\n", encoding="utf-8")
    os.environ["GENAPI_API_KEY"] = key
    return key


def headers_for(api_key: str, *, json_content: bool = True) -> dict[str, str]:
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    if json_content:
        headers["Content-Type"] = "application/json"
    return headers


def validate_key(api_key: str) -> None:
    response = requests.get(
        f"{GENAPI_BASE}/user",
        headers=headers_for(api_key),
        timeout=30,
    )
    if response.status_code == 401:
        raise RuntimeError("GenAPI отклонил API-ключ (401). Проверь ключ в личном кабинете GenAPI.")
    response.raise_for_status()

    data = response.json()
    balance = data.get("balance")
    if balance is not None:
        print(f"GenAPI подключён. Баланс: {balance} ₽")
    else:
        print("GenAPI подключён.")


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
    return "1024x1536" if category == "ch" else "1920x1080"


def character_identity_refs(source: Path, rel: str) -> list[str]:
    stem = source.stem.lower()
    if stem.startswith("nov"):
        key = "nov"
    elif stem.startswith("vet"):
        key = "vet"
    elif stem.startswith("mem"):
        key = "mem"
    elif stem.startswith("super"):
        key = "super"
    elif stem.startswith("curator"):
        key = "curator"
    else:
        return [rel]

    anchor = CHARACTER_CANONICAL[key]
    if anchor == rel:
        return [anchor]
    return [anchor, rel]


def auto_remaster_tasks(category: str) -> list[dict]:
    source_dir = CATEGORY_DIRS[category]
    tasks = []
    for source in image_files(source_dir):
        rel = source.relative_to(ROOT).as_posix()

        if category == "ch":
            # Keep the failed first-pass remasters untouched for comparison.
            # The locked pass goes to a new folder and always uses one canonical
            # face anchor for every expression of the same character.
            target = (OUTPUT_ROOT / "remaster_locked" / category / source.name).relative_to(ROOT).as_posix()
            refs = character_identity_refs(source, rel)
        else:
            target = (OUTPUT_ROOT / "remaster" / category / source.name).relative_to(ROOT).as_posix()
            refs = [rel]

        tasks.append({
            "id": f"remaster-{category}-{source.stem}",
            "category": category,
            "mode": "edit",
            "refs": refs,
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


def path_to_data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def extract_result_items(data: dict) -> list:
    result = data.get("result")
    if isinstance(result, list) and result:
        return result

    output = data.get("output")
    if isinstance(output, list) and output:
        return output
    if isinstance(output, str) and output:
        return [output]

    full = data.get("full_response")
    if isinstance(full, list) and full:
        return full

    return []


def resolve_result_bytes(item, api_key: str) -> bytes:
    if isinstance(item, dict):
        for key in ("url", "image_url", "output", "result"):
            if item.get(key):
                return resolve_result_bytes(item[key], api_key)
        for key in ("b64_json", "base64", "data"):
            value = item.get(key)
            if isinstance(value, str) and value:
                try:
                    return base64.b64decode(value)
                except Exception:
                    pass

    if not isinstance(item, str):
        raise RuntimeError(f"Неизвестный формат результата GenAPI: {type(item).__name__}")

    if item.startswith("data:") and ";base64," in item:
        return base64.b64decode(item.split(";base64,", 1)[1])

    if item.startswith("http://") or item.startswith("https://"):
        response = requests.get(item, timeout=120)
        response.raise_for_status()
        return response.content

    try:
        return base64.b64decode(item, validate=True)
    except Exception as exc:
        raise RuntimeError("GenAPI вернул результат в неизвестном формате") from exc


def wait_for_result(request_id: str | int, api_key: str, label: str = "") -> dict:
    deadline = time.time() + POLL_TIMEOUT_SECONDS
    url = f"{GENAPI_BASE}/request/get/{request_id}"

    while time.time() < deadline:
        response = requests.get(url, headers=headers_for(api_key), timeout=30)
        response.raise_for_status()
        data = response.json()
        status = str(data.get("status", "")).lower()

        if status == "success":
            return data
        if status in {"error", "failed", "failure", "cancelled", "canceled"}:
            raise RuntimeError(f"GenAPI завершил задачу со статусом {status}: {data}")

        progress = data.get("progress")
        if progress is not None:
            print(f"  [{label}] GenAPI: {status or 'processing'}, {progress}%")
        else:
            print(f"  [{label}] GenAPI: {status or 'processing'}")
        time.sleep(POLL_SECONDS)

    raise TimeoutError("GenAPI не завершил генерацию за 15 минут.")


def call_genapi(api_key: str, task: dict, model: str, quality_override: str | None = None) -> dict:
    prompt = compose_prompt(task)
    quality = quality_override or task.get("quality", "high")

    # callback_url intentionally omitted: we use GenAPI long-polling by request_id.
    # Passing null is rejected by the network validator.
    payload = {
        "is_sync": False,
        "prompt": prompt,
        "model": model,
        "quality": quality,
        "image_size": task.get("size", "1024x1024"),
        "background": task.get("background", "auto"),
        "num_images": 1,
        "output_format": task.get("output_format", "png"),
    }

    refs = [ROOT / p for p in task.get("refs", [])]
    missing = [str(p) for p in refs if not p.exists()]
    if missing:
        raise FileNotFoundError("Не найдены референсы: " + ", ".join(missing))

    endpoint = f"{GENAPI_BASE}/networks/{GENAPI_NETWORK}"

    if refs:
        # GenAPI documents files_array inputs as multipart/form-data.
        # image_urls[] makes the field arrive as a real array instead of a JSON
        # string/data-URI value, which the GPT Image 2.5 validator rejects.
        files = []
        handles = []
        try:
            for ref in refs:
                handle = open(ref, "rb")
                handles.append(handle)
                mime = mimetypes.guess_type(ref.name)[0] or "application/octet-stream"
                files.append(("image_urls[]", (ref.name, handle, mime)))

            form = {
                "is_sync": "false",
                "prompt": prompt,
                "model": model,
                "quality": quality,
                "image_size": task.get("size", "1024x1024"),
                "background": task.get("background", "auto"),
                "num_images": "1",
                "output_format": task.get("output_format", "png"),
            }
            response = requests.post(
                endpoint,
                data=form,
                files=files,
                headers=headers_for(api_key, json_content=False),
                timeout=180,
            )
        finally:
            for handle in handles:
                handle.close()
    else:
        response = requests.post(
            endpoint,
            json=payload,
            headers=headers_for(api_key),
            timeout=120,
        )

    if response.status_code == 401:
        raise RuntimeError("GenAPI отклонил API-ключ (401).")
    if response.status_code == 422:
        raise RuntimeError(f"GenAPI не принял параметры задачи: {response.text}")
    response.raise_for_status()

    data = response.json()
    status = str(data.get("status", "")).lower()

    if status == "success" and extract_result_items(data):
        return data

    request_id = data.get("request_id") or data.get("id")
    if not request_id:
        raise RuntimeError(f"GenAPI не вернул request_id: {data}")

    print(f"  [{task.get('id', 'task')}] GenAPI request_id: {request_id}")
    return wait_for_result(request_id, api_key, task.get("id", "task"))


def save_genapi_result(data: dict, target: Path, task: dict, api_key: str) -> None:
    items = extract_result_items(data)
    if not items:
        raise RuntimeError(f"GenAPI не вернул изображение: {data}")

    image_bytes = resolve_result_bytes(items[0], api_key)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(image_bytes)
    normalize_image(target, task)


def append_log(record: dict) -> None:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    with LOG_LOCK:
        with LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def run_one_task(task: dict, api_key: str, model: str, quality_override: str | None, force: bool) -> dict:
    target = ROOT / task["target"]
    task_id = task.get("id", "task")

    if target.exists() and not force:
        return {"task": task_id, "status": "skip", "target": str(target.relative_to(ROOT)), "seconds": 0.0, "error": None}

    started = time.time()
    status = "ok"
    error = None
    try:
        print(f"  START [{task_id}]")
        result = call_genapi(api_key, task, model=model, quality_override=quality_override)
        save_genapi_result(result, target, task, api_key)
        print(f"  OK    [{task_id}] -> {target.relative_to(ROOT)}")
    except Exception as exc:
        status = "error"
        error = repr(exc)
        print(f"  ERROR [{task_id}]: {exc}")

    record = {
        "time": datetime.now().isoformat(timespec="seconds"),
        "task": task_id,
        "status": status,
        "target": task.get("target"),
        "provider": "genapi",
        "model": f"{GENAPI_NETWORK}:{model}",
        "seconds": round(time.time() - started, 2),
        "error": error,
    }
    append_log(record)
    return record


def run_tasks(
    tasks: list[dict],
    model: str,
    quality_override: str | None,
    force: bool,
    dry_run: bool,
    workers: int = DEFAULT_WORKERS,
) -> None:
    if not tasks:
        print("Нет задач.")
        return

    workers = max(1, min(int(workers), 10))

    print(f"\nЗадач: {len(tasks)}")
    print("Провайдер: GenAPI")
    print(f"Модель: GPT Image 2.5 / {model}")
    print(f"Параллельно: до {workers} генераций")
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

    if requests is None:
        raise SystemExit("Пакет requests не установлен. Запусти GENERATE_ART.bat ещё раз.")

    api_key = ensure_api_key()
    validate_key(api_key)

    runnable = []
    for task in tasks:
        target = ROOT / task["target"]
        if target.exists() and not force:
            print(f"  SKIP  [{task['id']}] уже существует {target.relative_to(ROOT)}")
        else:
            runnable.append(task)

    if not runnable:
        print("Все результаты уже существуют.")
        return

    ok = 0
    errors = 0
    with ThreadPoolExecutor(max_workers=min(workers, len(runnable))) as pool:
        future_map = {
            pool.submit(run_one_task, task, api_key, model, quality_override, force): task
            for task in runnable
        }
        for future in as_completed(future_map):
            try:
                record = future.result()
                if record["status"] == "ok":
                    ok += 1
                elif record["status"] == "error":
                    errors += 1
            except Exception as exc:
                errors += 1
                task = future_map[future]
                print(f"  ERROR [{task.get('id', 'task')}]: {exc}")

    print(f"\nГотово. Успешно: {ok}, ошибок: {errors}.")


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
    raw = input("Модель GenAPI: [1] Sunburst quality  [2] Flare faster  (Enter=1): ").strip()
    return FAST_MODEL if raw == "2" else DEFAULT_MODEL


def confirm_generation(tasks: list[dict]) -> bool:
    print(f"Подготовлено задач: {len(tasks)}")
    print("Генерация использует платный GenAPI. Уже существующие результаты будут пропущены.")
    answer = input("Запустить? [y/N]: ").strip().lower()
    return answer in {"y", "yes", "д", "да"}


def menu() -> None:
    while True:
        print("\n" + "=" * 72)
        print(" PURPLE SHIFT - GPT IMAGE 2.5 / GenAPI ART PIPELINE")
        print("=" * 72)
        print("1. Показать план curated-артов без генерации")
        print("2. Ремастер персонажей с жёсткой фиксацией лиц (5 параллельно)")
        print("3. Ремастер всех фонов")
        print("4. Ремастер всех CG")
        print("5. Сгенерировать новые curated-арты")
        print("6. ПОЛНЫЙ ПРОГОН: персонажи + фоны + CG + curated")
        print("7. Применить готовые ремастеры в игру (с backup)")
        print("8. Выйти")
        choice = input("\nВыбор: ").strip()

        if choice == "1":
            run_tasks(curated_tasks(), DEFAULT_MODEL, None, False, True, DEFAULT_WORKERS)
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
            run_tasks(tasks, choose_model(), None, False, False, DEFAULT_WORKERS)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Purple Shift GPT Image 2.5 art pipeline via GenAPI")
    p.add_argument("--menu", action="store_true")
    p.add_argument("--category", choices=["ch", "bg", "cg", "curated", "all"])
    p.add_argument("--model", default=DEFAULT_MODEL, choices=[DEFAULT_MODEL, FAST_MODEL])
    p.add_argument("--quality", choices=["low", "medium", "high", "xhigh", "max"])
    p.add_argument("--force", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--task", help="Запустить одну curated-задачу по id")
    p.add_argument("--apply", choices=["ch", "bg", "cg", "all"])
    p.add_argument("--workers", type=int, default=DEFAULT_WORKERS, help="Одновременных генераций (1-10, по умолчанию 5)")
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

    run_tasks(tasks, args.model, args.quality, args.force, args.dry_run, args.workers)


if __name__ == "__main__":
    main()
