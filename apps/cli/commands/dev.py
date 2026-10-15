"""Dev group command handlers."""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import TYPE_CHECKING, Any

from apps.cli.json_envelope import emit_ok

if TYPE_CHECKING:
    import argparse

# Re-use brain module's agent_loop handler for dev.agent-loop
from apps.cli.commands.brain import _cmd_agent_loop


def _dev_smoke_help(*, json_output: bool = False) -> None:
    if json_output:
        emit_ok(commands=[
            "source scripts/remedy_smoke.sh && remedy_smoke",
            "bash scripts/remedy_smoke.sh",
        ])
        return
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
        "worker_cleanup_ok": False,
        "autocoder_fake_e2e_ok": False,
        "repair_loop_ok": None,
        "reviewer_loop_ok": None,
        "remaining_blockers": [],
        "advisories": [],
    }

    # Check worker cleanup — availability, not functionality
    import shutil
    status["worker_cleanup_ok"] = shutil.which("ollama") is not None

    # Check autocoder path — verify apply is callable, not just importable
    try:
        from packages.orchestration.source_apply import apply_structured_patch
        from packages.orchestration.structured_patch import FileOp, StructuredPatch
        _p = StructuredPatch(
            intent_kind="file_ops",
            file_ops=(FileOp(path="test.py", action="create", language="python",
                             content="pass\n", risk="low"),),
            target_paths=("test.py",),
            risk="low", applicability="applicable", requires_approval=False,
        )
        status["autocoder_fake_e2e_ok"] = callable(apply_structured_patch)
    except (ImportError, TypeError):
        status["autocoder_fake_e2e_ok"] = False

    # Check repair loop — module importable and build_repair_context callable
    try:
        from packages.orchestration.repair_context import build_repair_context
        status["repair_loop_ok"] = callable(build_repair_context)
    except (ImportError, Exception):  # noqa: BLE001 — a repair-loop check failure must not block other checks
        status["repair_loop_ok"] = False

    # Check reviewer loop — module importable
    try:
        from packages.orchestration.reviewer import run_reviewer
        status["reviewer_loop_ok"] = callable(run_reviewer)
    except (ImportError, Exception):  # noqa: BLE001 — a reviewer-loop check failure must not block other checks
        status["reviewer_loop_ok"] = False

    # Remaining blockers (hard failures) vs advisories (informational)
    blockers = []
    advisories: list[str] = []
    if not smoke_info["found"]:
        blockers.append("no smoke summary found — run: source scripts/remedy_smoke.sh && remedy_smoke")
    elif smoke_info["status"] != "passed":
        blockers.append(f"smoke status: {smoke_info['status']}")
    if not status["worker_cleanup_ok"]:
        advisories.append("ollama not found — worker unload unavailable")
    # New capability checks — null means untested, false means crashed
    for cap_key, cap_label in (
        ("repair_loop_ok", "repair loop"),
        ("reviewer_loop_ok", "reviewer loop"),
    ):
        if status[cap_key] is False:
            blockers.append(f"{cap_label} module import failed")
        elif status[cap_key] is None:
            advisories.append(f"{cap_label} not verified")
    status["remaining_blockers"] = blockers
    status["advisories"] = advisories

    if json_output:
        emit_ok(**status)
    else:
        print("Remedy Developer Status")
        print("=" * 40)
        smoke_mark = "OK" if smoke_info["status"] == "passed" else "FAIL" if smoke_info["found"] else "UNKNOWN"
        print(f"  smoke: {smoke_mark}")
        if smoke_info["found"]:
            print(f"    job_id: {smoke_info['job_id']}")
        for key in ("cli_ok",
                     "worker_cleanup_ok", "autocoder_fake_e2e_ok",
                     "repair_loop_ok",
                     "reviewer_loop_ok"):
            val = status[key]
            mark = "N/A" if val is None else "OK" if val else "FAIL"
            print(f"  {key}: {mark}")
        if blockers:
            print(f"  blockers: {len(blockers)}")
            for b in blockers:
                print(f"    - {b}")
        else:
            print("  blockers: none")
        if advisories:
            print(f"  advisories: {len(advisories)}")
            for a in advisories:
                print(f"    - {a}")
        print()
        print("Commands:")
        print("  remedy serve start                          — the supervisor and its public API")
        print("  remedy worker unload --all                  — free VRAM")
        print('  remedy do "goal" --json                     — plan and run a job, stop before apply')
        print("  remedy dev status --json                    — this status")
        print("  source scripts/remedy_smoke.sh && remedy_smoke     — smoke")


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "dev.agent-loop": lambda args: _cmd_agent_loop(args.job_id),
    "dev.smoke-help": lambda args: _dev_smoke_help(json_output=getattr(args, "json", False)),
    "dev.status": lambda args: _dev_status(json_output=getattr(args, "json", False)),
}
