"""CLI handlers for worker onboarding facade + mission command facade.

Simple operator-facing commands that call existing safe low-level rails.
No provider execution. No auto-approval. No secret storage.
"""

from __future__ import annotations

import json
import sys
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, NoReturn

if TYPE_CHECKING:
    import argparse

# ---------------------------------------------------------------------------
# Worker alias registry (Step 2619)
# ---------------------------------------------------------------------------

_WORKER_ALIASES: dict[str, dict[str, str]] = {
    "claude": {
        "adapter_id": "claude-code-v0",
        "template_id": "claude-code-repair-v0",
        "kind": "claude_code",
        "label": "Claude Code",
    },
    "claude-code": {
        "adapter_id": "claude-code-v0",
        "template_id": "claude-code-repair-v0",
        "kind": "claude_code",
        "label": "Claude Code",
    },
    "fixture": {
        "adapter_id": "fixture-v0",
        "template_id": "fixture-echo-v0",
        "kind": "fixture_builder",
        "label": "Fixture (test only)",
    },
    "generic": {
        "adapter_id": "generic-cli-v0",
        "template_id": "generic-cli-v0",
        "kind": "generic_external_cli_builder",
        "label": "Generic CLI",
    },
}


def _resolve_alias(worker: str) -> dict[str, str] | None:
    return _WORKER_ALIASES.get(worker.lower().strip())


def _err(msg: str) -> NoReturn:
    print(json.dumps({"error": msg}), file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# worker doctor (Step 2620)
# ---------------------------------------------------------------------------


def _cmd_worker_doctor(ns: argparse.Namespace) -> None:
    import shutil

    from packages.orchestration.main_builder_adapter import get_builder_adapter_spec
    from packages.orchestration.managed_builder_execution import get_command_template

    worker = getattr(ns, "worker", "")
    if not worker:
        _err("worker name required (e.g. claude)")
    alias = _resolve_alias(worker)
    if not alias:
        _err(f"unknown worker: {worker}. Known: {', '.join(sorted(_WORKER_ALIASES))}")

    adapter_id = alias["adapter_id"]
    template_id = alias["template_id"]

    adapter = get_builder_adapter_spec(adapter_id)
    template = get_command_template(template_id)

    checks: list[dict[str, str | bool]] = []
    blockers: list[str] = []

    binary = shutil.which(worker.split("-")[0]) if alias["kind"] == "claude_code" else None
    if alias["kind"] == "claude_code":
        checks.append({"check": "binary_on_path", "ok": binary is not None,
                        "detail": str(binary or "not found")})
        if not binary:
            blockers.append(f"{alias['label']} binary not found on PATH.")

    checks.append({"check": "adapter_exists", "ok": adapter is not None,
                    "detail": adapter_id})
    if adapter:
        enabled = adapter.get("enabled", False)
        checks.append({"check": "adapter_enabled", "ok": enabled,
                        "detail": adapter.get("mode", "disabled")})
        if not enabled:
            blockers.append(f"Adapter disabled. Fix: remedy worker add {worker} --json")
    else:
        blockers.append(f"Adapter {adapter_id} not found.")

    checks.append({"check": "template_exists", "ok": template is not None,
                    "detail": template_id})
    if template:
        enabled = template.get("enabled", False)
        checks.append({"check": "template_enabled", "ok": enabled,
                        "detail": str(enabled)})
        if not enabled:
            blockers.append(f"Template disabled. Fix: remedy worker add {worker} --json")
    else:
        blockers.append(f"Template {template_id} not found.")

    ready = len(blockers) == 0
    next_cmd = "" if ready else f"remedy worker add {worker} --json"

    report: dict[str, Any] = {
        "worker": worker,
        "adapter_id": adapter_id,
        "template_id": template_id,
        "ready": ready,
        "checks": checks,
        "blockers": blockers,
    }
    if next_cmd:
        report["next_recommended_command"] = next_cmd

    if getattr(ns, "json", False):
        print(json.dumps(report, indent=2))
        return
    print(f"Worker: {alias['label']} ({worker})")
    print(f"  ready: {ready}")
    for c in checks:
        ok = "OK" if c["ok"] else "FAIL"
        print(f"  [{ok}] {c['check']}: {c['detail']}")
    if blockers:
        print("  blockers:")
        for b in blockers:
            print(f"    - {b}")
    if next_cmd:
        print(f"  next: {next_cmd}")


# ---------------------------------------------------------------------------
# worker add (Step 2621)
# ---------------------------------------------------------------------------


def _cmd_worker_add(ns: argparse.Namespace) -> None:
    from packages.orchestration.main_builder_adapter import (
        BuilderAdapterMode,
        BuilderAdapterSpec,
        get_builder_adapter_spec,
        save_builder_adapter_spec,
    )
    from packages.orchestration.managed_builder_execution import (
        enable_command_template,
        get_command_template,
    )

    worker = getattr(ns, "worker", "")
    if not worker:
        _err("worker name required (e.g. claude)")
    alias = _resolve_alias(worker)
    if not alias:
        _err(f"unknown worker: {worker}. Known: {', '.join(sorted(_WORKER_ALIASES))}")

    adapter_id = alias["adapter_id"]
    template_id = alias["template_id"]
    results: dict[str, Any] = {"worker": worker, "adapter_id": adapter_id, "template_id": template_id}
    warnings: list[str] = []

    adapter_d = get_builder_adapter_spec(adapter_id)
    if adapter_d:
        if not adapter_d.get("enabled", False):
            spec = BuilderAdapterSpec.from_dict(adapter_d)
            spec.enabled = True
            spec.mode = BuilderAdapterMode.OPERATOR_LAUNCHED
            ok = save_builder_adapter_spec(spec)
            results["adapter_enabled"] = bool(ok)
            if not ok:
                warnings.append(f"Failed to enable adapter {adapter_id}")
        else:
            results["adapter_enabled"] = True
    else:
        results["adapter_enabled"] = False
        warnings.append(f"Adapter {adapter_id} not found in default specs.")

    template = get_command_template(template_id)
    if template:
        if not template.get("enabled", False):
            tmpl = enable_command_template(template_id)
            results["template_enabled"] = tmpl is not None
            if not tmpl:
                warnings.append(f"Template {template_id} failed safety validation.")
        else:
            results["template_enabled"] = True
    else:
        results["template_enabled"] = False
        warnings.append(f"Template {template_id} not found in default templates.")

    results["ready"] = results.get("adapter_enabled", False) and results.get("template_enabled", False)
    results["warnings"] = warnings
    results["note"] = "Execution still requires explicit approval per session."

    quickstart = [
        f"1. Check readiness: remedy worker doctor {worker} --json",
        "2. Create or choose a mission run: remedy dogfood create <job_id> --json",
        "3. Run mission loop: remedy mission run <run_id> --job-id <job_id> --json",
        "4. Approve execution when prompted: remedy execution approve <session_id> --template <template_id> --json",
        "5. Read morning report: remedy mission report <run_id> --job-id <job_id> --json",
    ]
    results["quickstart"] = quickstart

    results["advanced"] = {
        "adapter_id": adapter_id,
        "template_id": template_id,
        "low_level_commands": [
            f"remedy builder adapter-show {adapter_id} --json",
            f"remedy execution template-show {template_id} --json",
            f"remedy execution approve <session_id> --template {template_id} --json",
        ],
    }

    if getattr(ns, "json", False):
        print(json.dumps(results, indent=2))
        return
    status = "READY" if results["ready"] else "NOT READY"
    print(f"Worker added: {alias['label']} ({worker}) — {status}")
    if warnings:
        for w in warnings:
            print(f"  warning: {w}")
    print(f"  note: {results['note']}")
    print("  quickstart:")
    for step in quickstart:
        print(f"    {step}")


# ---------------------------------------------------------------------------
# worker disable (Step 2622)
# ---------------------------------------------------------------------------


def _cmd_worker_disable(ns: argparse.Namespace) -> None:
    from packages.orchestration.main_builder_adapter import (
        BuilderAdapterMode,
        BuilderAdapterSpec,
        get_builder_adapter_spec,
        save_builder_adapter_spec,
    )
    from packages.orchestration.managed_builder_execution import (
        disable_command_template,
    )

    worker = getattr(ns, "worker", "")
    if not worker:
        _err("worker name required (e.g. claude)")
    alias = _resolve_alias(worker)
    if not alias:
        _err(f"unknown worker: {worker}. Known: {', '.join(sorted(_WORKER_ALIASES))}")

    adapter_id = alias["adapter_id"]
    template_id = alias["template_id"]

    adapter_disabled = False
    adapter_d = get_builder_adapter_spec(adapter_id)
    if adapter_d:
        spec = BuilderAdapterSpec.from_dict(adapter_d)
        spec.enabled = False
        spec.mode = BuilderAdapterMode.DISABLED
        adapter_disabled = bool(save_builder_adapter_spec(spec))

    template_ok = disable_command_template(template_id)

    result: dict[str, Any] = {
        "worker": worker,
        "adapter_disabled": adapter_disabled,
        "template_disabled": template_ok is not None,
        "adapter_id": adapter_id,
        "template_id": template_id,
    }

    if getattr(ns, "json", False):
        print(json.dumps(result, indent=2))
        return
    print(f"Worker disabled: {alias['label']} ({worker})")


# ---------------------------------------------------------------------------
# mission run facade (Step 2624)
# ---------------------------------------------------------------------------


def _cmd_mission_run(ns: argparse.Namespace) -> None:
    from packages.orchestration.dogfood_run import run_mission_loop
    run_id = getattr(ns, "run_id", "")
    if not run_id:
        _err("run_id required")
    job_id = getattr(ns, "job_id", "") or ""
    max_steps = int(getattr(ns, "max_steps", None) or 10)
    max_seconds = int(getattr(ns, "max_seconds", None) or 300)
    result = run_mission_loop(
        run_id, job_id=job_id,
        max_steps=max_steps, max_seconds=max_seconds,
    )
    data = result.to_dict()
    if getattr(ns, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Mission run: {result.run_id}")
    print(f"  steps: {result.steps_attempted}  status: {result.final_status}")
    print(f"  stop: {result.stop_reason}")
    if result.next_safe_action:
        print(f"  next: {result.next_safe_action}")
    if result.blocking_reasons:
        print(f"  blockers: {', '.join(result.blocking_reasons)}")


# ---------------------------------------------------------------------------
# mission report facade (Step 2625)
# ---------------------------------------------------------------------------


def _cmd_mission_report(ns: argparse.Namespace) -> None:
    from packages.orchestration.dogfood_run import build_mission_morning_report
    run_id = getattr(ns, "run_id", "")
    if not run_id:
        _err("run_id required")
    job_id = getattr(ns, "job_id", "") or ""
    report = build_mission_morning_report(run_id, job_id=job_id)
    data = report.to_dict()
    if getattr(ns, "json", False):
        print(json.dumps(data, indent=2))
        return
    print(f"Mission Report: {report.run_id}")
    print(f"  mission: {report.mission_status}  status: {report.final_status}")
    if report.stopped_because:
        print(f"  stopped: {report.stopped_because}")
    print(f"  steps: {report.steps_completed}")
    if report.next_safe_action:
        print(f"  next: {report.next_safe_action}")
    print(f"  summary: {report.operator_summary}")


# ---------------------------------------------------------------------------
# Handler registry
# ---------------------------------------------------------------------------


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "worker.doctor": _cmd_worker_doctor,
    "worker.add": _cmd_worker_add,
    "worker.disable": _cmd_worker_disable,
    "mission.run": _cmd_mission_run,
    "mission.report": _cmd_mission_report,
}
