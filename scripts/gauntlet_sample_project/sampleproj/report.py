"""Render a report over imported records.

The path normalisation here is the same three lines as in
:mod:`sampleproj.importer` — the duplication g05 asks to be removed.
"""
from __future__ import annotations

from pathlib import Path

from .config import DEFAULTS


def report_dir(target_dir: Path | str) -> Path:
    """Normalise a directory the same way the importer does."""
    # --- path normalisation (duplicated in importer.py) ---
    target = Path(target_dir).expanduser()
    target = target if target.is_absolute() else Path.cwd() / target
    target = Path(str(target).rstrip("/")) if str(target) != "/" else target
    # --- end duplication ---
    return target


def build_report(target_dir: Path | str, *, width: int | None = None) -> str:
    """A fixed-width listing of what is in the target directory."""
    columns = width or DEFAULTS["report_width"]
    directory = report_dir(target_dir)
    names = sorted(p.name for p in directory.glob("*.txt")) if directory.is_dir() else []
    lines = [f"records: {len(names)}".ljust(columns).rstrip()]
    lines += [f"  - {name}" for name in names]
    return "\n".join(lines) + "\n"
