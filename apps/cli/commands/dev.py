"""Dev group command handlers."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    import argparse

# Re-use brain module's agent_loop handler for dev.agent-loop
from apps.cli.commands.brain import _cmd_agent_loop


def _dev_smoke_help() -> None:
    print("Smoke test:")
    print("  source scripts/remedy_smoke.sh && remedy_smoke")
    print("")
    print("Or run directly:")
    print("  bash scripts/remedy_smoke.sh")


def _dev_status(*, json_output: bool = False) -> None:
    """Lightweight status aggregator over latest smoke and contract checks."""
    status: dict = {
        "version": 1,
        "cli_ok": True,
        "smoke_ok": False,
        "ui_contract_ok": False,
        "task_progress_ok": False,
        "worker_cleanup_ok": False,
        "autocoder_fake_e2e_ok": False,
        "remaining_blockers": [],
    }

    # Check latest smoke summary
    smoke_summary = Path(".data/smoke/latest/summary.json")
    if not smoke_summary.exists():
        # Try alternative path
        for p in sorted(Path(".data/smoke").glob("*/summary.json")):
            smoke_summary = p
    if smoke_summary.exists():
        try:
            data = json.loads(smoke_summary.read_text())
            status["smoke_ok"] = data.get("status") == "passed"
        except (json.JSONDecodeError, OSError):
            pass

    # Check UI contract files
    try:
        from packages.orchestration.ui_view_model import build_brain_view_model
        from packages.core.models import Job
        job = Job(name="status-check")
        vm = build_brain_view_model(job, [])
        origins = [n for n in vm["nodes"] if n["is_origin"]]
        status["ui_contract_ok"] = (
            vm["version"] == 4
            and len(origins) == 1
            and vm["visible_counts_by_zoom"][0] == 1
        )
    except Exception:
        pass

    # Check task progress
    try:
        from packages.orchestration.ui_view_model import build_task_progress
        from packages.core.models import Job
        job = Job(name="tp-check")
        tp = build_task_progress(job, [])
        status["task_progress_ok"] = tp["version"] == 1
    except Exception:
        pass

    # Check worker cleanup availability
    import shutil
    status["worker_cleanup_ok"] = shutil.which("ollama") is not None

    # Check autocoder fixture path
    try:
        from packages.orchestration.structured_patch import StructuredPatch
        from packages.orchestration.source_apply import apply_structured_patch
        status["autocoder_fake_e2e_ok"] = True
    except ImportError:
        status["autocoder_fake_e2e_ok"] = False

    # Remaining blockers
    blockers = []
    if not status["smoke_ok"]:
        blockers.append("smoke not passed or summary not found")
    if not status["ui_contract_ok"]:
        blockers.append("UI contract check failed")
    if not status["task_progress_ok"]:
        blockers.append("task-progress version mismatch")
    status["remaining_blockers"] = blockers

    if json_output:
        print(json.dumps(status, indent=2))
    else:
        print("Remedy Developer Status")
        print("=" * 40)
        for key, val in status.items():
            if key == "remaining_blockers":
                if val:
                    print(f"  blockers: {len(val)}")
                    for b in val:
                        print(f"    - {b}")
                else:
                    print("  blockers: none")
            elif key == "version":
                continue
            else:
                mark = "OK" if val else "FAIL"
                print(f"  {key}: {mark}")
        print()
        print("Commands:")
        print("  remedy ui <job_id>              — open UI")
        print("  remedy worker unload --all      — free VRAM")
        print("  remedy do \"goal\" --fixture-builder --no-ui --json  — fake E2E")
        print("  source scripts/remedy_smoke.sh && remedy_smoke  — smoke")


COMMAND_HANDLERS: dict[str, Callable[["argparse.Namespace"], None]] = {
    "dev.agent-loop": lambda args: _cmd_agent_loop(args.job_id),
    "dev.smoke-help": lambda args: _dev_smoke_help(),
    "dev.status": lambda args: _dev_status(json_output=getattr(args, "json", False)),
}
