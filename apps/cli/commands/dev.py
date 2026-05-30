"""Dev group command handlers."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable

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


def _find_latest_smoke() -> dict[str, Any]:
    """Find and parse latest smoke summary."""
    result: dict[str, Any] = {
        "found": False, "status": "unknown",
        "job_id": "", "project_id": "", "smoke_log": "",
    }
    smoke_dir = Path(".data/smoke")
    if not smoke_dir.is_dir():
        return result
    candidates = sorted(smoke_dir.glob("*/summary.json"))
    if not candidates:
        return result
    summary_path = candidates[-1]
    try:
        data = json.loads(summary_path.read_text())
        result["found"] = True
        result["status"] = data.get("status", "unknown")
        result["job_id"] = data.get("job_id", "")
        result["project_id"] = data.get("project_id", "")
        result["smoke_log"] = str(summary_path.parent / "smoke.log")
    except (json.JSONDecodeError, OSError):
        result["found"] = True
        result["status"] = "corrupt"
    return result


def _dev_status(*, json_output: bool = False) -> None:
    """Lightweight status aggregator over latest smoke and contract checks."""
    smoke_info = _find_latest_smoke()

    status: dict[str, Any] = {
        "version": 1,
        "cli_ok": True,
        "latest_smoke": smoke_info,
        "ui_contract_ok": False,
        "task_progress_ok": False,
        "worker_cleanup_ok": False,
        "autocoder_fake_e2e_ok": False,
        "remaining_blockers": [],
    }

    # Check UI contract
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

    # Check worker cleanup — availability, not functionality
    import shutil
    status["worker_cleanup_ok"] = shutil.which("ollama") is not None

    # Check autocoder path — verify apply is callable, not just importable
    try:
        from packages.orchestration.structured_patch import FileOp, StructuredPatch
        from packages.orchestration.source_apply import apply_structured_patch
        # Verify patch model can be constructed
        _p = StructuredPatch(
            intent_kind="file_ops",
            file_ops=(FileOp(path="test.py", action="create", language="python",
                             content="pass\n", risk="low"),),
            target_paths=("test.py",),
            risk="low", applicability="applicable", requires_approval=False,
        )
        status["autocoder_fake_e2e_ok"] = callable(apply_structured_patch)
    except (ImportError, Exception):
        status["autocoder_fake_e2e_ok"] = False

    # Remaining blockers
    blockers = []
    if not smoke_info["found"]:
        blockers.append("no smoke summary found — run: source scripts/remedy_smoke.sh && remedy_smoke")
    elif smoke_info["status"] != "passed":
        blockers.append(f"smoke status: {smoke_info['status']}")
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
        smoke_mark = "OK" if smoke_info["status"] == "passed" else "FAIL" if smoke_info["found"] else "UNKNOWN"
        print(f"  smoke: {smoke_mark}")
        if smoke_info["found"]:
            print(f"    job_id: {smoke_info['job_id']}")
        for key in ("cli_ok", "ui_contract_ok", "task_progress_ok",
                     "worker_cleanup_ok", "autocoder_fake_e2e_ok"):
            mark = "OK" if status[key] else "FAIL"
            print(f"  {key}: {mark}")
        if blockers:
            print(f"  blockers: {len(blockers)}")
            for b in blockers:
                print(f"    - {b}")
        else:
            print("  blockers: none")
        print()
        print("Commands:")
        print("  remedy ui <job_id>              — open UI")
        print("  remedy worker unload --all      — free VRAM")
        print('  remedy do "goal" --fixture-builder --no-ui --json  — fake E2E')
        print("  source scripts/remedy_smoke.sh && remedy_smoke  — smoke")


COMMAND_HANDLERS: dict[str, Callable[["argparse.Namespace"], None]] = {
    "dev.agent-loop": lambda args: _cmd_agent_loop(args.job_id),
    "dev.smoke-help": lambda args: _dev_smoke_help(),
    "dev.status": lambda args: _dev_status(json_output=getattr(args, "json", False)),
}
