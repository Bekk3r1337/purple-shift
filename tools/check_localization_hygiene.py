#!/usr/bin/env python3
from pathlib import Path
import ast
import re
import sys

GAME = Path("game")
CYRILLIC = re.compile(r"[А-Яа-яЁё]")
LONG_DASHES = ("—", "–")

problems = []
english_old_strings = {}

SOURCE_STRING_CALL = re.compile(r'_\(\s*("(?:\\.|[^"])*")\s*\)')
RUNTIME_CATALOG_ASSIGNMENT = re.compile(
    r'(?m)^\s*(ps[A-Za-z0-9_]*(?:catalog|messages|cgs|documents|achievements|events|hypotheses|items|profiles))\s*=\s*([\[\{])'
)
STRING_LITERAL = re.compile(r'"(?:\\.|[^"])*"|\'(?:\\.|[^\'])*\'')


def extract_balanced_assignment(text, start_index, opening):
    closing = "]" if opening == "[" else "}"
    index = start_index
    depth = 0
    quote = None
    escaped = False

    while index < len(text):
        char = text[index]

        if quote is not None:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
        else:
            if char in ('"', "\'"):
                quote = char
            elif char == opening:
                depth += 1
            elif char == closing:
                depth -= 1
                if depth == 0:
                    return text[start_index:index + 1]

        index += 1

    return text[start_index:]

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
            if not stripped or stripped.startswith("#"):
                continue

            if stripped.startswith("old "):
                literal = stripped[4:].strip()
                try:
                    source_text = ast.literal_eval(literal)
                except (SyntaxError, ValueError):
                    source_text = None

                if isinstance(source_text, str):
                    previous = english_old_strings.get(source_text)
                    if previous is not None:
                        prev_path, prev_line = previous
                        problems.append(
                            f"{path}:{lineno}: duplicate English string translation for "
                            f"{source_text!r}; first defined at {prev_path}:{prev_line}"
                        )
                    else:
                        english_old_strings[source_text] = (path, lineno)
                continue

            if CYRILLIC.search(stripped):
                problems.append(
                    f"{path}:{lineno}: Cyrillic remains in active English localization: {stripped}"
                )


# Anything explicitly passed through _() needs a string-table entry.
for path in sorted(GAME.rglob("*.rpy")):
    if path.as_posix().startswith("game/tl/"):
        continue

    text = path.read_text(encoding="utf-8-sig")

    for match in SOURCE_STRING_CALL.finditer(text):
        try:
            source_text = ast.literal_eval(match.group(1))
        except (SyntaxError, ValueError):
            continue

        if CYRILLIC.search(source_text) and source_text not in english_old_strings:
            lineno = text.count("\n", 0, match.start()) + 1
            problems.append(
                f"{path}:{lineno}: _() string has no English string translation: {source_text!r}"
            )

    # Runtime data catalogs are rendered dynamically, so Ren'Py cannot create
    # translation blocks for them automatically. Every Cyrillic literal in
    # these user-facing catalogs must have an explicit English string entry.
    for assignment in RUNTIME_CATALOG_ASSIGNMENT.finditer(text):
        variable_name = assignment.group(1)
        opening = assignment.group(2)
        block = extract_balanced_assignment(text, assignment.start(2), opening)

        for literal_match in STRING_LITERAL.finditer(block):
            try:
                source_text = ast.literal_eval(literal_match.group(0))
            except (SyntaxError, ValueError):
                continue

            if not isinstance(source_text, str) or not CYRILLIC.search(source_text):
                continue

            if source_text not in english_old_strings:
                absolute_index = assignment.start(2) + literal_match.start()
                lineno = text.count("\n", 0, absolute_index) + 1
                problems.append(
                    f"{path}:{lineno}: dynamic catalog {variable_name} has no English "
                    f"string translation for {source_text!r}"
                )


if problems:
    print("Localization hygiene check failed:")
    for problem in problems:
        print(f" - {problem}")
    sys.exit(1)

print("Localization hygiene check passed: no long dashes, no active Cyrillic in English, no duplicate translations, and dynamic runtime strings have English coverage.")
