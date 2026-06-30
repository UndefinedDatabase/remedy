"""Scratch file guard — deterministic, read-only workspace hygiene check.

Inspects the *root* of a job workspace for forbidden scratch files (ad-hoc
``_*.py`` helpers that a builder may have left behind). Pure orchestration
logic: no provider calls, no target-repo mutation, no job state mutation.
Same inputs always yield the same guard, so the result is reproducible
across runs.

A file matching a forbidden pattern is *allowed* (not flagged) when it appears
in ``allowed_files`` or in a review scope packet's ``changed_files`` — i.e. it
is a legitimate, reviewed deliverable rather than scratch.

Public API:
    build_scratch_file_guard(workspace, allowed_files) -> dict
    write_scratch_file_guard(workspace, evidence_dir, task_id, allowed_files, written) -> None
"""
from __future__ import annotations

import fnmatch
import json
import re
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.0.0"

_SAFE_TASK_ID_RE = re.compile(r"^T\d{3,}$")

FORBIDDEN_PATTERNS: tuple[str, ...] = (
    "_[!_]*.py",
)


def _allowed_names(allowed_files: list[str] | None) -> set[str]:
    """Return the set of allowed match keys: full entries plus their basenames."""
    names: set[str] = set()
    for entry in allowed_files or []:
        text = str(entry).strip()
        if not text:
            continue
        names.add(text)
        names.add(Path(text).name)
    return names


def _matches_forbidden(name: str) -> bool:
    return any(fnmatch.fnmatch(name, pat) for pat in FORBIDDEN_PATTERNS)


def build_scratch_file_guard(
    workspace: str,
    allowed_files: list[str] | None = None,
) -> dict[str, Any]:
    """Check workspace root for forbidden scratch files.

    Scans only the top-level entries of ``workspace`` (non-recursive). A file
    whose name matches a forbidden pattern is reported. It is recorded under
    ``allowed_files_found`` when its name (or full relative path) is in
    ``allowed_files``; otherwise it is a ``forbidden_files`` entry.
    """
    allowed = _allowed_names(allowed_files)

    files_found: list[str] = []
    forbidden_files: list[str] = []
    allowed_files_found: list[str] = []

    ws = Path(workspace) if workspace else None
    if ws and ws.is_dir():
        for child in sorted(ws.iterdir()):
            if not child.is_file():
                continue
            name = child.name
            if not _matches_forbidden(name):
                continue
            files_found.append(name)
            if name in allowed:
                allowed_files_found.append(name)
            else:
                forbidden_files.append(name)

    guard_status = "BLOCKED" if forbidden_files else "PASS"
    suggested_cleanup = [f"rm {path}" for path in forbidden_files]

    return {
        "schema_version": SCHEMA_VERSION,
        "task_id": "",
        "guard_status": guard_status,
        "checked_patterns": list(FORBIDDEN_PATTERNS),
        "files_found": files_found,
        "forbidden_files": forbidden_files,
        "allowed_files_found": allowed_files_found,
        "suggested_cleanup": suggested_cleanup,
    }


def _collect_scope_changed_files(evidence_dir: str) -> list[str]:
    """Collect ``changed_files`` from every review scope packet under evidence_dir."""
    base = Path(evidence_dir) / "task_runs"
    if not base.is_dir():
        return []
    collected: list[str] = []
    for packet in base.glob("*/review_scope_packet.json"):
        try:
            data = json.loads(packet.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if isinstance(data, dict):
            for f in data.get("changed_files", []) or []:
                collected.append(str(f))
    return collected


def write_scratch_file_guard(
    workspace: str,
    evidence_dir: str,
    task_id: str,
    allowed_files: list[str] | None,
    written: dict[str, str],
) -> None:
    """Build and write ``scratch_file_guard.json`` to task or job evidence.

    When ``task_id`` is a safe task ID (``T001`` ...), the guard is written to
    ``task_runs/<task_id>/scratch_file_guard.json``; otherwise it is written at
    job level as ``scratch_file_guard.json``. No-op without an evidence dir.

    Files named in any review scope packet's ``changed_files`` are merged into
    the allowed set, so reviewed deliverables are never flagged as scratch.
    """
    if not evidence_dir:
        return

    merged_allowed = list(allowed_files or [])
    merged_allowed.extend(_collect_scope_changed_files(evidence_dir))

    guard = build_scratch_file_guard(workspace, merged_allowed)

    ev = Path(evidence_dir)
    task_id = str(task_id or "")
    if task_id and _SAFE_TASK_ID_RE.fullmatch(task_id):
        guard["task_id"] = task_id
        rel = f"task_runs/{task_id}/scratch_file_guard.json"
        out_dir = ev / "task_runs" / task_id
    else:
        rel = "scratch_file_guard.json"
        out_dir = ev

    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "scratch_file_guard.json"
    json_path.write_text(json.dumps(guard, indent=2) + "\n", encoding="utf-8")
    written[rel] = str(json_path)
