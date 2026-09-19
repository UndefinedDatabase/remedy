"""Data group command handlers (F276): the data root's footprint, per class."""

from __future__ import annotations

import json as _json
from collections.abc import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import argparse


def format_data_bytes(n: int) -> str:
    """A byte count for a person: 1023 B, 1.0 KB, 652.0 GB (powers of 1024)."""
    value = float(n)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if value < 1024 or unit == "TB":
            return f"{int(value)} {unit}" if unit == "B" else f"{value:.1f} {unit}"
        value /= 1024
    raise AssertionError("unreachable")


def _cmd_data_usage(*, json_output: bool = False) -> None:
    from packages.orchestration.data_footprint import (
        FOOTPRINT_CLASSES,
        export_footprint_json,
        footprint,
    )
    from packages.orchestration.data_paths import resolve_data_root

    fp = footprint(resolve_data_root())
    if json_output:
        print(_json.dumps(export_footprint_json(fp), sort_keys=True))
        return
    print(f"Data root: {fp.root}")
    if not fp.exists:
        print("  (does not exist — nothing stored yet)")
        return
    totals = fp.class_totals()
    for data_class in FOOTPRINT_CLASSES:
        size, files = totals[data_class]
        print(f"  {data_class:<13} {format_data_bytes(size):>10}  {files} files")
        for child in fp.children:
            if child.data_class == data_class:
                print(f"    {child.name:<22} {format_data_bytes(child.bytes):>10}  {child.files} files")
    print(f"  {'total':<13} {format_data_bytes(fp.total_bytes):>10}  {fp.total_files} files")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "data.usage": lambda args: _cmd_data_usage(json_output=getattr(args, "json", False)),
}
