"""Import records into a target directory.

Note the path normalisation below: the same three lines appear in
:mod:`sampleproj.report`. g05 asks for exactly that duplication to be
extracted into one helper.
"""
from __future__ import annotations

from pathlib import Path

from .parsing import parse_records


def import_records(lines: list[str], target_dir: Path | str) -> list[Path]:
    """Write one file per record; returns the files written, in order."""
    # --- path normalisation (duplicated in report.py) ---
    target = Path(target_dir).expanduser()
    target = target if target.is_absolute() else Path.cwd() / target
    target = Path(str(target).rstrip("/")) if str(target) != "/" else target
    # --- end duplication ---

    target.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for record in parse_records(lines):
        path = target / f"{record['name']}.txt"
        path.write_text(record["value"] + "\n", encoding="utf-8")
        written.append(path)
    return written


def plan_import(lines: list[str], target_dir: Path | str) -> list[str]:
    """What an import WOULD write, without writing it."""
    target = Path(target_dir)
    return [str(target / f"{r['name']}.txt") for r in parse_records(lines)]
