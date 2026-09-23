#!/usr/bin/env python3
from pathlib import Path
import re
import sys

GAME = Path("game")
CYRILLIC = re.compile(r"[А-Яа-яЁё]")
LONG_DASHES = ("—", "–")

problems = []

for path in sorted(GAME.rglob("*.rpy")):
    try:
        text = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as exc:
        problems.append(f"{path}: unable to decode as UTF-8: {exc}")
        continue

    is_english = path.as_posix().startswith("game/tl/english/")

    for lineno, line in enumerate(text.splitlines(), 1):
        if any(ch in line for ch in LONG_DASHES):
            problems.append(
                f"{path}:{lineno}: long dash found; use '-' instead"
            )

        if is_english:
            stripped = line.strip()
            # Ren'Py string translations intentionally keep the Russian source
            # in old "...". Comments also contain the original source line.
            if not stripped or stripped.startswith("#") or stripped.startswith("old "):
                continue
            if CYRILLIC.search(stripped):
                problems.append(
                    f"{path}:{lineno}: Cyrillic remains in active English localization: {stripped}"
                )

if problems:
    print("Localization hygiene check failed:")
    for problem in problems:
        print(f" - {problem}")
    sys.exit(1)

print("Localization hygiene check passed: no long dashes and no active Cyrillic in English.")
