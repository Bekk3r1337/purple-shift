#!/usr/bin/env python3
"""Merge needless click-by-click Ren'Py dialogue runs.

The tool only joins directly adjacent say statements made by the same speaker.
It deliberately preserves a small set of dramatic beats, sound cues, ellipses,
interpolated lines, and long passages that are easier to review separately.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


SAY_RE = re.compile(
    r'^(?P<indent>\s*)(?P<speaker>n|p|sv|vet|mem|newb|cur) '
    r'"(?P<text>(?:[^"\\]|\\.)*)"\s*$'
)

PRESERVE = {
    "...",
    "…",
    "Пиип.",
    "Щелчок.",
    "Секунда.",
    "Тишина.",
    "Стой.",
    "Нет.",
    "Да.",
    "Пока.",
}


def can_join(left: re.Match[str], right: re.Match[str], count: int) -> bool:
    if left["indent"] != right["indent"] or left["speaker"] != right["speaker"]:
        return False

    if count >= 3:
        return False

    left_text = left["text"].strip()
    right_text = right["text"].strip()
    if left_text in PRESERVE or right_text in PRESERVE:
        return False
    if left_text.endswith(":"):
        return False
    if "[" in left_text or "[" in right_text:
        return False
    if len(left_text) + len(right_text) > 245:
        return False

    return True


def merge_file(path: Path) -> int:
    original = path.read_text(encoding="utf-8")
    lines = original.splitlines()
    merged: list[str] = []
    joins = 0
    index = 0

    while index < len(lines):
        match = SAY_RE.match(lines[index])
        if not match:
            merged.append(lines[index])
            index += 1
            continue

        text = match["text"]
        count = 1
        cursor = index + 1
        current = match

        while cursor < len(lines):
            following = SAY_RE.match(lines[cursor])
            if not following or not can_join(current, following, count):
                break

            text = "{} {}".format(text.rstrip(), following["text"].lstrip())
            current = re.match(
                SAY_RE,
                '{}{} "{}"'.format(
                    match["indent"],
                    match["speaker"],
                    text,
                ),
            )
            if current is None:
                break

            count += 1
            cursor += 1
            joins += 1

        merged.append(
            '{}{} "{}"'.format(
                match["indent"],
                match["speaker"],
                text,
            )
        )
        index = cursor

    result = "\n".join(merged) + ("\n" if original.endswith("\n") else "")
    path.write_text(result, encoding="utf-8")
    return joins


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("usage: merge_dialogue_runs.py FILE [FILE ...]")

    total = 0
    for argument in sys.argv[1:]:
        path = Path(argument)
        joins = merge_file(path)
        total += joins
        print("{}: {} joins".format(path, joins))

    print("total: {} joins".format(total))


if __name__ == "__main__":
    main()
