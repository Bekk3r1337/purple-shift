from __future__ import annotations

import argparse
import base64
import getpass
import json
import mimetypes
import os
import shutil
import threading
import time
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
MASTER_ROOT = OUTPUT_ROOT / "master"
GAME_READY_ROOT = OUTPUT_ROOT / "game_ready"
BACKUP_ROOT = ROOT / "art_backup"
LOG_PATH = OUTPUT_ROOT / "generation_log.jsonl"

SUPPORTED_IMAGES = {".png", ".jpg", ".jpeg", ".webp"}

GENAPI_BASE = "https://api.gen-api.ru/api/v1"
GENAPI_NETWORK = "gpt-image-2-5"
MODEL = "sunburst"

# OVERDRIVE SETTINGS
QUALITY = "max"
POLL_SECONDS = 5
POLL_TIMEOUT_SECONDS = 20 * 60

CHAR_WORKERS = 5
SCENE_WORKERS = 3

# GenAPI-safe request sizes
REQUEST_SIZE_CH = "1024x1536"
REQUEST_SIZE_BG_CG = "1920x1080"

# Master sizes
MASTER_SIZE_CH = (2048, 3072)
MASTER_SIZE_BG_CG = (3840, 2160)

LOG_LOCK = threading.Lock()

CATEGORY_DIRS = {
    "ch": ROOT / "game" / "images" / "ch",
    "bg": ROOT / "game" / "images" / "bg",
    "cg": ROOT / "game" / "images" / "cg",
}

CURATED_PROMOTION = [
    ("ch", "nov_neutral.png"),
    ("ch", "nov_angry.png"),
    ("ch", "nov_scared.png"),
    ("ch", "vet_tired.png"),
    ("ch", "vet_warm.png"),
    ("ch", "mem_nervous.png"),
    ("ch", "mem_angry.png"),
    ("ch", "super_tired.png"),
    ("ch", "super_soft.png"),
    ("ch", "curator_stern.png"),
    ("ch", "curator_smile.png"),
    ("bg", "warehouse_storm.jpg"),
    ("bg", "control_room_storm.jpg"),
    ("cg", "team_break_cinematic.jpg"),
    ("cg", "v13_false_memory.jpg"),
    ("cg", "zero_shift_v2.jpg"),
    ("cg", "storm_first_contact.jpg"),
]

VISUAL_PASS_2_BATCHES = ("ui", "bg_variants", "consistency", "extra_cg", "vfx")
VISUAL_PASS_2_LABELS = {
    "ui": "UI / меню",
    "bg_variants": "Уникальные варианты фонов",
    "consistency": "Consistency-pass персонажей",
    "extra_cg": "Дополнительные сюжетные CG",
    "vfx": "VFX / Storm overlays",
}

CHARACTER_CANONICAL = {
    "nov": "game/images/ch/nov_relief.png",
    "vet": "game/images/ch/vet1.png",
    "mem": "game/images/ch/mem_serious.png",
    "super": "game/images/ch/super_stern.png",
    "curator": "game/images/ch/curator.png",
}

CATEGORY_PROMPTS = {
    "ch": (
        "IDENTITY-LOCKED visual novel sprite remaster. "
        "REFERENCE 1 is the canonical identity anchor and must define the exact character identity. "
        "If REFERENCE 2 is present, use it only for the target pose, gesture, clothing folds and emotion. "
        "The output must unmistakably be the same person as REFERENCE 1: same face geometry, eye shape, nose, jaw, "
        "hairline, hairstyle, apparent age, body proportions, uniform design and silhouette. "
        "Do not redesign, beautify, age up/down, photorealize, change ethnicity, change hairstyle, or change clothing. "
        "Preserve the intended emotion and pose. Improve only drawing polish, anatomy, hands, rendering quality, "
        "fabric detail, line confidence and subtle lighting. "
        "Create a clean 2D semi-realistic anime / visual novel full-body sprite on a transparent background."
    ),
    "bg": (
        "Create a premium master-quality remaster of this exact visual-novel background. "
        "Preserve the same location, camera angle, architecture, industrial layout and story-important landmarks. "
        "Keep it as polished 2D semi-realistic anime / cinematic VN background art, not photorealistic and not 3D. "
        "Improve perspective, materials, atmosphere, lighting and environmental storytelling. "
        "No people, no text, no logos."
    ),
    "cg": (
        "Create a premium master-quality remaster of this exact visual-novel CG. "
        "Preserve the scene, composition, emotional meaning, characters and story beat. "
        "Keep it as polished 2D semi-realistic anime / cinematic VN illustration, not photorealistic and not 3D. "
        "Improve anatomy, faces, hands, lighting, scene coherence, atmosphere and cinematic polish. "
        "No subtitles, no text, no watermarks."
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


def request_size_for(category: str) -> str:
    return REQUEST_SIZE_CH if category == "ch" else REQUEST_SIZE_BG_CG


def master_size_for_category(category: str) -> tuple[int, int]:
    return MASTER_SIZE_CH if category == "ch" else MASTER_SIZE_BG_CG


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


def source_reference_size(task: dict) -> tuple[int, int] | None:
    if Image is None or not task.get("preserve_reference_size"):
        return None
    refs = task.get("refs") or []
    if not refs:
        return None
    ref = ROOT / refs[-1]
    if not ref.exists():
        return None
    try:
        with Image.open(ref) as im:
            return im.size
    except Exception:
        return None


def game_ready_size_for(task: dict) -> tuple[int, int] | None:
    explicit = task.get("game_ready_size")
    if explicit and isinstance(explicit, list) and len(explicit) == 2:
        return int(explicit[0]), int(explicit[1])

    ref_size = source_reference_size(task)
    if ref_size:
        return ref_size

    if task.get("category") in {"bg", "cg"}:
        return 1920, 1080

    return None


def compose_prompt(task: dict) -> str:
    style = load_style()
    specific = task.get("prompt", "").strip()
    return f"{style}\n\nTASK:\n{specific}".strip()


def make_output_paths(task: dict) -> tuple[Path, Path]:
    category = task["category"]
    filename = Path(task.get("apply_to") or task["target"]).name

    output_group = str(task.get("output_group") or "").strip()
    if output_group:
        group_root = OUTPUT_ROOT / output_group
        master_root = group_root / "master"
        game_ready_root = group_root / "game_ready"
    else:
        master_root = MASTER_ROOT
        game_ready_root = GAME_READY_ROOT

    return master_root / category / filename, game_ready_root / category / filename


def normalize_and_save_versions(raw_path: Path, task: dict, master_path: Path, game_ready_path: Path) -> None:
    if Image is None:
        master_path.parent.mkdir(parents=True, exist_ok=True)
        game_ready_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(raw_path, master_path)
        shutil.copy2(raw_path, game_ready_path)
        return

    category = task["category"]
    output_format = task.get("output_format", "png")
    save_format = {"jpeg": "JPEG", "jpg": "JPEG", "webp": "WEBP"}.get(output_format, "PNG")
    save_kwargs = {"quality": 95} if save_format in {"JPEG", "WEBP"} else {}

    explicit_master = task.get("master_size")
    if isinstance(explicit_master, list) and len(explicit_master) == 2:
        master_size = (int(explicit_master[0]), int(explicit_master[1]))
    else:
        master_size = master_size_for_category(category)

    ready_size = game_ready_size_for(task)

    with Image.open(raw_path) as im:
        wants_alpha = category == "ch" or task.get("background") == "transparent"
        target_mode = "RGBA" if wants_alpha else "RGB"

        if im.mode != target_mode:
            im = im.convert(target_mode)

        # MASTER
        master_img = im.resize(master_size, Image.Resampling.LANCZOS)
        master_path.parent.mkdir(parents=True, exist_ok=True)
        if save_format == "JPEG" and master_img.mode == "RGBA":
            master_img = master_img.convert("RGB")
        master_img.save(master_path, format=save_format, **save_kwargs)

        # GAME READY
        game_ready_path.parent.mkdir(parents=True, exist_ok=True)
        if ready_size:
            ready_img = im.resize(ready_size, Image.Resampling.LANCZOS)
        else:
            ready_img = im.copy()

        if save_format == "JPEG" and ready_img.mode == "RGBA":
            ready_img = ready_img.convert("RGB")
        ready_img.save(game_ready_path, format=save_format, **save_kwargs)


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


def resolve_result_bytes(item) -> bytes:
    if isinstance(item, dict):
        for key in ("url", "image_url", "output", "result"):
            if item.get(key):
                return resolve_result_bytes(item[key])
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

    raise TimeoutError("GenAPI не завершил генерацию за 20 минут.")


def call_genapi(api_key: str, task: dict) -> dict:
    prompt = compose_prompt(task)
    refs = [ROOT / p for p in task.get("refs", [])]
    missing = [str(p) for p in refs if not p.exists()]
    if missing:
        raise FileNotFoundError("Не найдены референсы: " + ", ".join(missing))

    endpoint = f"{GENAPI_BASE}/networks/{GENAPI_NETWORK}"

    if refs:
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
                "model": MODEL,
                "quality": QUALITY,
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
        payload = {
            "is_sync": False,
            "prompt": prompt,
            "model": MODEL,
            "quality": QUALITY,
            "image_size": task.get("size", "1024x1024"),
            "background": task.get("background", "auto"),
            "num_images": 1,
            "output_format": task.get("output_format", "png"),
        }
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


def save_genapi_result(data: dict, task: dict) -> tuple[Path, Path]:
    items = extract_result_items(data)
    if not items:
        raise RuntimeError(f"GenAPI не вернул изображение: {data}")

    image_bytes = resolve_result_bytes(items[0])

    tmp_dir = OUTPUT_ROOT / "_tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    tmp_path = tmp_dir / f"{task['id']}.{task.get('output_format', 'png')}"

    tmp_path.write_bytes(image_bytes)

    master_path, game_ready_path = make_output_paths(task)
    normalize_and_save_versions(tmp_path, task, master_path, game_ready_path)

    try:
        tmp_path.unlink(missing_ok=True)
    except Exception:
        pass

    return master_path, game_ready_path


def append_log(record: dict) -> None:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    with LOG_LOCK:
        with LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def auto_remaster_tasks(category: str) -> list[dict]:
    source_dir = CATEGORY_DIRS[category]
    tasks = []

    for source in image_files(source_dir):
        rel = source.relative_to(ROOT).as_posix()
        if category == "ch":
            refs = character_identity_refs(source, rel)
        else:
            refs = [rel]

        task = {
            "id": f"remaster-{category}-{source.stem}",
            "category": category,
            "mode": "edit",
            "refs": refs,
            "target": rel,
            "apply_to": rel,
            "prompt": CATEGORY_PROMPTS[category],
            "size": request_size_for(category),
            "quality": QUALITY,
            "background": "transparent" if category == "ch" else "opaque",
            "output_format": output_format_for(source, category),
            "preserve_reference_size": True,
        }

        if category == "ch" and source.stem.lower() == "vet_injured":
            task["safe_refs"] = [
                "game/images/ch/vet1.png",
                "game/images/ch/vet_concerned.png",
            ]
            task["safe_prompt"] = (
                CATEGORY_PROMPTS["ch"]
                + " Create a non-graphic fatigued variant with subtle wrist or hand discomfort only. "
                  "No blood, no wounds, no bruises, no exposed injury, no medical trauma."
            )

        tasks.append(task)

    return tasks


def manifest_tasks(category: str | None = None, batch: str | None = None) -> list[dict]:
    manifest = load_manifest()
    tasks = [t for t in manifest.get("tasks", []) if t.get("enabled", True)]

    prepared = []
    for t in tasks:
        if category and t.get("category") != category:
            continue
        if batch and t.get("batch") != batch:
            continue

        task = dict(t)
        cat = task["category"]
        task["size"] = request_size_for(cat)
        task["quality"] = QUALITY
        prepared.append(task)

    return prepared


def curated_tasks(category: str | None = None) -> list[dict]:
    return manifest_tasks(category=category)


def visual_pass_2_tasks(batch: str | None = None) -> list[dict]:
    tasks = manifest_tasks(batch=batch)
    return [t for t in tasks if t.get("output_group") == "visual_pass_2"]


def run_one_task(task: dict, api_key: str) -> dict:
    task_id = task.get("id", "task")
    master_path, game_ready_path = make_output_paths(task)

    if game_ready_path.exists():
        return {
            "task": task_id,
            "status": "skip",
            "master_path": str(master_path.relative_to(ROOT)),
            "game_ready_path": str(game_ready_path.relative_to(ROOT)),
            "seconds": 0.0,
            "error": None,
        }

    started = time.time()
    status = "ok"
    error = None

    try:
        print(f"  START [{task_id}]")
        try:
            result = call_genapi(api_key, task)
        except Exception as first_exc:
            message = str(first_exc).lower()
            safe_refs = task.get("safe_refs")
            if safe_refs and ("модера" in message or "moderation" in message):
                print(f"  RETRY [{task_id}] moderation-safe reference set")
                safe_task = dict(task)
                safe_task["refs"] = safe_refs
                safe_task["prompt"] = task.get("safe_prompt", task.get("prompt", ""))
                result = call_genapi(api_key, safe_task)
                task = safe_task
            else:
                raise

        master_path, game_ready_path = save_genapi_result(result, task)
        print(f"  OK    [{task_id}]")
        print(f"        master:     {master_path.relative_to(ROOT)}")
        print(f"        game_ready: {game_ready_path.relative_to(ROOT)}")

    except Exception as exc:
        status = "error"
        error = repr(exc)
        print(f"  ERROR [{task_id}]: {exc}")

    record = {
        "time": datetime.now().isoformat(timespec="seconds"),
        "task": task_id,
        "status": status,
        "master_path": str(master_path.relative_to(ROOT)),
        "game_ready_path": str(game_ready_path.relative_to(ROOT)),
        "provider": "genapi",
        "model": f"{GENAPI_NETWORK}:{MODEL}",
        "quality": QUALITY,
        "seconds": round(time.time() - started, 2),
        "error": error,
    }
    append_log(record)
    return record


def workers_for_category(category: str) -> int:
    return CHAR_WORKERS if category == "ch" else SCENE_WORKERS


def run_tasks(tasks: list[dict], category: str, dry_run: bool = False, workers: int | None = None) -> None:
    if not tasks:
        print("Нет задач.")
        return

    if workers is None:
        workers = workers_for_category(category)
    workers = max(1, min(int(workers), 10))

    print(f"\nЗадач: {len(tasks)}")
    print("Режим: OVERDRIVE")
    print("Провайдер: GenAPI")
    print(f"Модель: {MODEL}")
    print(f"Качество: {QUALITY}")
    print(f"Параллельно: до {workers} генераций")

    categories = sorted({task.get("category", "?") for task in tasks})
    print("Категории:", ", ".join(categories))
    print("Request size: определяется для каждой задачи")
    print("Master: до 3840x2160 для сцен/UI/VFX и 2048x3072 для спрайтов")

    if dry_run:
        for i, task in enumerate(tasks, 1):
            master_path, game_ready_path = make_output_paths(task)
            print(f"\n[{i}/{len(tasks)}] {task['id']}")
            print(f"  refs={task.get('refs', [])}")
            print(f"  request_size={task.get('size')}")
            print(f"  master={master_path.relative_to(ROOT)}")
            print(f"  game_ready={game_ready_path.relative_to(ROOT)}")
            print("  prompt:", compose_prompt(task)[:700].replace("\n", " "), "...")
        return

    if requests is None:
        raise SystemExit("Пакет requests не установлен. Запусти GENERATE_ART.bat ещё раз.")

    api_key = ensure_api_key()
    validate_key(api_key)

    runnable = []
    for task in tasks:
        _, game_ready_path = make_output_paths(task)
        if game_ready_path.exists():
            print(f"  SKIP  [{task['id']}] уже существует {game_ready_path.relative_to(ROOT)}")
        else:
            runnable.append(task)

    if not runnable:
        print("Все результаты уже существуют.")
        return

    ok = 0
    errors = 0

    with ThreadPoolExecutor(max_workers=min(workers, len(runnable))) as pool:
        future_map = {
            pool.submit(run_one_task, task, api_key): task
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

        _, src = make_output_paths(task)
        dst = ROOT / apply_to

        if src.exists():
            candidates.append((task, src, dst))

    if not candidates:
        print("Нет готовых game_ready файлов для применения.")
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


def promote_curated_outputs() -> None:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_dir = BACKUP_ROOT / stamp / "curated"
    promoted = 0
    missing = []

    print("\nПроверяю 17 curated-артов...")

    for category, filename in CURATED_PROMOTION:
        candidates = [
            GAME_READY_ROOT / category / filename,
            OUTPUT_ROOT / "curated" / category / filename,
            MASTER_ROOT / category / filename,
        ]
        src = next((p for p in candidates if p.exists()), None)
        dst = ROOT / "game" / "images" / category / filename

        if src is None:
            missing.append(f"{category}/{filename}")
            print(f"  MISSING {category}/{filename}")
            continue

        if dst.exists():
            backup = backup_dir / dst.relative_to(ROOT)
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(dst, backup)

        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        promoted += 1
        print(f"  INSTALL {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")

    print(f"\nУстановлено curated-артов: {promoted}/17.")
    if missing:
        print("Не найдены:")
        for item in missing:
            print(f"  - {item}")
        print("Их можно догенерировать пунктом 5, затем снова запустить установку.")
    else:
        print("Все 17 curated-артов установлены в game/images и готовы к коммиту.")
    if promoted and backup_dir.exists():
        print(f"Backup: {backup_dir.relative_to(ROOT)}")


def visual_pass_2_destination(task: dict) -> Path:
    batch = task.get("batch")
    filename = Path(task["target"]).name

    if batch == "ui":
        return ROOT / "game" / "images" / "ui" / "v2" / filename
    if batch == "bg_variants":
        return ROOT / "game" / "images" / "bg" / filename
    if batch == "consistency":
        return ROOT / "game" / "images" / "ch" / filename
    if batch == "extra_cg":
        return ROOT / "game" / "images" / "cg" / filename
    if batch == "vfx":
        return ROOT / "game" / "images" / "vfx" / filename

    raise ValueError(f"Неизвестный batch Visual Pass 2: {batch}")


def promote_visual_pass_2_outputs() -> None:
    tasks = visual_pass_2_tasks()
    if not tasks:
        print("В tasks.json нет задач Visual Pass 2.")
        return

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_dir = BACKUP_ROOT / stamp / "visual_pass_2"
    promoted = 0
    missing = []

    print(f"\nУстановка Visual Pass 2: {len(tasks)} файлов...")

    for task in tasks:
        _, src = make_output_paths(task)
        dst = visual_pass_2_destination(task)

        if not src.exists():
            missing.append(task["id"])
            print(f"  MISSING [{task['id']}] {src.relative_to(ROOT)}")
            continue

        if dst.exists():
            backup = backup_dir / dst.relative_to(ROOT)
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(dst, backup)

        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        promoted += 1
        print(f"  INSTALL [{task['id']}] -> {dst.relative_to(ROOT)}")

    print(f"\nУстановлено Visual Pass 2: {promoted}/{len(tasks)}.")
    if missing:
        print("Не найдены результаты:")
        for task_id in missing:
            print(f"  - {task_id}")
        print("Догенерируй отсутствующий пакет и снова запусти установку.")
    else:
        print("Все файлы Visual Pass 2 перенесены в game/images и готовы к коммиту.")

    if promoted and backup_dir.exists():
        print(f"Backup: {backup_dir.relative_to(ROOT)}")


def run_visual_pass_2_batch(batch: str, dry_run: bool = False) -> None:
    tasks = visual_pass_2_tasks(batch)
    if not tasks:
        print(f"Нет задач пакета {batch}.")
        return
    workers = CHAR_WORKERS if batch == "consistency" else SCENE_WORKERS
    run_tasks(tasks, "ch" if batch == "consistency" else "cg", dry_run=dry_run, workers=workers)


def confirm_generation(tasks: list[dict]) -> bool:
    print(f"Подготовлено задач: {len(tasks)}")
    print("Режим OVERDRIVE - Sunburst + MAX quality + high-resolution master files.")
    print("Это дорогой режим. Уже существующие результаты будут пропущены.")
    answer = input("Запустить? [y/N]: ").strip().lower()
    return answer in {"y", "yes", "д", "да"}


def menu() -> None:
    while True:
        print("\n" + "=" * 78)
        print(" PURPLE SHIFT - GPT IMAGE 2.5 / GenAPI OVERDRIVE")
        print("=" * 78)
        print("1. VISUAL PASS 2 - СГЕНЕРИРОВАТЬ ВСЁ (46 задач)")
        print("2. Visual Pass 2 - UI / меню (8)")
        print("3. Visual Pass 2 - уникальные фоны (3)")
        print("4. Visual Pass 2 - consistency персонажей (20)")
        print("5. Visual Pass 2 - дополнительные CG (10)")
        print("6. Visual Pass 2 - VFX / Storm overlays (5)")
        print("7. Показать план Visual Pass 2 без генерации")
        print("8. Установить готовый Visual Pass 2 в game/images")
        print("9. Выйти")
        print("")
        print("10. Legacy - ремастер персонажей")
        print("11. Legacy - ремастер фонов")
        print("12. Legacy - ремастер CG")
        print("13. Legacy - установить старые 17 curated-артов")
        choice = input("\nВыбор: ").strip()

        if choice == "9":
            return

        if choice == "1":
            tasks = visual_pass_2_tasks()
            if confirm_generation(tasks):
                for batch in VISUAL_PASS_2_BATCHES:
                    print(f"\n=== {VISUAL_PASS_2_LABELS[batch]} ===")
                    run_visual_pass_2_batch(batch)
            continue

        if choice == "2":
            batch = "ui"
        elif choice == "3":
            batch = "bg_variants"
        elif choice == "4":
            batch = "consistency"
        elif choice == "5":
            batch = "extra_cg"
        elif choice == "6":
            batch = "vfx"
        elif choice == "7":
            tasks = visual_pass_2_tasks()
            run_tasks(tasks, "cg", dry_run=True, workers=SCENE_WORKERS)
            continue
        elif choice == "8":
            promote_visual_pass_2_outputs()
            continue
        elif choice == "10":
            tasks = auto_remaster_tasks("ch")
            if confirm_generation(tasks):
                run_tasks(tasks, "ch", workers=CHAR_WORKERS)
            continue
        elif choice == "11":
            tasks = auto_remaster_tasks("bg")
            if confirm_generation(tasks):
                run_tasks(tasks, "bg", workers=SCENE_WORKERS)
            continue
        elif choice == "12":
            tasks = auto_remaster_tasks("cg")
            if confirm_generation(tasks):
                run_tasks(tasks, "cg", workers=SCENE_WORKERS)
            continue
        elif choice == "13":
            promote_curated_outputs()
            continue
        else:
            print("Неизвестный пункт.")
            continue

        tasks = visual_pass_2_tasks(batch)
        if confirm_generation(tasks):
            run_visual_pass_2_batch(batch)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Purple Shift GPT Image 2.5 OVERDRIVE art pipeline via GenAPI")
    p.add_argument("--menu", action="store_true")
    p.add_argument("--category", choices=["ch", "bg", "cg", "curated", "all"])
    p.add_argument("--visual-batch", choices=[*VISUAL_PASS_2_BATCHES, "all"])
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--apply", choices=["ch", "bg", "cg", "all"])
    p.add_argument("--promote-curated", action="store_true", help="Установить старые 17 curated-артов")
    p.add_argument("--promote-vp2", action="store_true", help="Установить Visual Pass 2 в game/images")
    p.add_argument("--workers", type=int, default=None, help="Одновременных генераций")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    if args.menu or (
        not args.category
        and not args.visual_batch
        and not args.apply
        and not args.promote_curated
        and not args.promote_vp2
    ):
        menu()
        return

    if args.promote_vp2:
        promote_visual_pass_2_outputs()
        return

    if args.promote_curated:
        promote_curated_outputs()
        return

    if args.visual_batch:
        if args.visual_batch == "all":
            for batch in VISUAL_PASS_2_BATCHES:
                run_visual_pass_2_batch(batch, dry_run=args.dry_run)
        else:
            tasks = visual_pass_2_tasks(args.visual_batch)
            workers = args.workers or (CHAR_WORKERS if args.visual_batch == "consistency" else SCENE_WORKERS)
            run_tasks(tasks, "ch" if args.visual_batch == "consistency" else "cg", dry_run=args.dry_run, workers=workers)
        return

    if args.apply:
        cats = ["ch", "bg", "cg"] if args.apply == "all" else [args.apply]
        tasks = []
        for cat in cats:
            tasks.extend(auto_remaster_tasks(cat))
        apply_outputs(tasks)
        return

    if args.category == "ch":
        run_tasks(auto_remaster_tasks("ch"), "ch", dry_run=args.dry_run, workers=args.workers)
    elif args.category == "bg":
        run_tasks(auto_remaster_tasks("bg"), "bg", dry_run=args.dry_run, workers=args.workers)
    elif args.category == "cg":
        run_tasks(auto_remaster_tasks("cg"), "cg", dry_run=args.dry_run, workers=args.workers)
    elif args.category == "curated":
        run_tasks(curated_tasks(), "cg", dry_run=args.dry_run, workers=args.workers)
    elif args.category == "all":
        print("=== CHARACTERS ===")
        run_tasks(auto_remaster_tasks("ch"), "ch", dry_run=args.dry_run, workers=args.workers or CHAR_WORKERS)
        print("\n=== BACKGROUNDS ===")
        run_tasks(auto_remaster_tasks("bg"), "bg", dry_run=args.dry_run, workers=args.workers or SCENE_WORKERS)
        print("\n=== CG ===")
        run_tasks(auto_remaster_tasks("cg"), "cg", dry_run=args.dry_run, workers=args.workers or SCENE_WORKERS)
        print("\n=== CURATED ===")
        run_tasks(curated_tasks(), "cg", dry_run=args.dry_run, workers=args.workers or SCENE_WORKERS)


if __name__ == "__main__":
    main()