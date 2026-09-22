# Purple Shift - GPT Image 2.5 Art Pipeline

One-click local art generation/remaster pipeline for the Ren'Py project.

## Start

Double-click `GENERATE_ART.bat` in the repository root.

On the first real generation the launcher asks for `OPENAI_API_KEY`. The key is saved only in `tools/art_pipeline/.env`, which is ignored by Git.

## What it can do

- remaster every existing character sprite using the sprite itself as the identity reference;
- remaster every background while preserving location/camera/layout;
- remaster every existing CG while preserving the scene and composition;
- generate curated new expressions, Storm variants and new cinematic CGs from `tasks.json`;
- use GPT Image 2.5 Sunburst by default or Flare for a faster pass;
- skip outputs that already exist, so a stopped batch can be resumed;
- write generated candidates to `art_output/` instead of overwriting the game;
- apply remasters from the menu only after review, with automatic originals backup in `art_backup/`.

## Safety workflow

1. Generate to `art_output/`.
2. Review the images.
3. Delete bad candidates and rerun them with `--force`, or adjust their prompt in `tasks.json`.
4. Apply only approved remasters to `game/images`.
5. Run Ren'Py lint/test and review the game visually before committing binary changes.

## Command line

```bat
python tools\art_pipeline\generate_art.py --category ch
python tools\art_pipeline\generate_art.py --category bg
python tools\art_pipeline\generate_art.py --category cg
python tools\art_pipeline\generate_art.py --category curated
python tools\art_pipeline\generate_art.py --category all
python tools\art_pipeline\generate_art.py --task cg-zero-shift-remake --force
python tools\art_pipeline\generate_art.py --category curated --dry-run
python tools\art_pipeline\generate_art.py --apply all
```

Model override:

```bat
python tools\art_pipeline\generate_art.py --category cg --model gpt-image-2.5-flare
```

Quality override:

```bat
python tools\art_pipeline\generate_art.py --category cg --quality xhigh
```
