"""How many model turns the Pi harness took, read from its own call records (amend1014c, R3).

One Pi process runs an agent loop of several model turns. The token ledger counts PROCESSES (one
row per harness invocation), so the honest second figure comes from the authoritative event
stream: each Pi call record under `<run dir>/pi/<role>.jsonl` carries the `model_turns` that
`pi_events.summarize_pi_events` counted from the completed assistant `message_end` events.
Remedy deliberately does NOT split a ledger row per turn: budgets and the ledger key their rows by
provider attempt, and a turn is not an attempt. A zero-turn failed invocation counts 0 turns.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from packages.orchestration import data_paths


def pi_turns_in_run(run_id: str) -> dict[str, dict[str, int]]:
    """``{role: {"invocations": n, "model_turns": n}}`` for one run; {} when Pi made no record."""
    found: dict[str, dict[str, int]] = {}
    pi_dir = Path(data_paths.run_dir(run_id)) / "pi"
    try:
        files = sorted(pi_dir.glob("*.jsonl"))
    except OSError:
        return found
    for path in files:
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        for line in lines:
            try:
                record: Any = json.loads(line)
            except ValueError:
                continue
            turns = record.get("model_turns") if isinstance(record, dict) else None
            if not isinstance(turns, int) or isinstance(turns, bool) or turns < 0:
                continue
            slot = found.setdefault(str(record.get("role") or path.stem), {"invocations": 0, "model_turns": 0})
            slot["invocations"] += 1
            slot["model_turns"] += turns
    return found


def pi_turns_for_job(run_ids: list[str]) -> dict[str, dict[str, int]]:
    """The per-role Pi totals over a job's runs, each run counted once."""
    total: dict[str, dict[str, int]] = {}
    for run_id in dict.fromkeys(run_ids):
        for role, figures in pi_turns_in_run(run_id).items():
            slot = total.setdefault(role, {"invocations": 0, "model_turns": 0})
            slot["invocations"] += figures["invocations"]
            slot["model_turns"] += figures["model_turns"]
    return total
