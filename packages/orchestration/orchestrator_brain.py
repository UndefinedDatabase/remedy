"""
Main Orchestrator Brain v0 — the reader of its persisted decision traces.

The situation builder, option scorer, anti-loop guard, model routing plan, decision selector
and idea intake went with the orchestrator CLI group (F261 T003). What stays is the one
reader the cockpit's orchestrator section calls.

Public API::

    list_decisions(scope, data_dir=None) -> list[dict]
"""

from __future__ import annotations

import json
from pathlib import Path


def _decisions_root(scope_key: str, data_dir: Path) -> Path:
    safe = scope_key.replace(":", "_").replace("/", "_")
    return data_dir / "workspaces" / "orchestrator" / "decisions" / safe


def list_decisions(scope_key: str, data_dir: Path | None = None) -> list[dict]:
    from packages.orchestration.data_paths import resolve_data_root
    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    base = _decisions_root(scope_key, ddir)
    if not base.is_dir():
        return []
    out: list[dict] = []
    try:
        files = sorted(base.glob("*/decision.json"))
        for p in files:
            try:
                out.append(json.loads(p.read_bytes()))
            except (OSError, json.JSONDecodeError):
                continue
    except OSError:
        return []
    out.sort(key=lambda d: d.get("generated_at", ""))
    return out

