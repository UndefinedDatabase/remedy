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
# doctor core (Step 2665)
# ---------------------------------------------------------------------------


def _cmd_doctor_core(ns: argparse.Namespace) -> None:
    from pathlib import Path

    checks: list[dict[str, str | bool]] = []

    def _check(name: str, ok: bool, detail: str = "") -> None:
        checks.append({"check": name, "ok": ok, "detail": detail})

    import importlib

    def _safe_err(exc: Exception) -> str:
        import re
        msg = str(exc)
        if len(msg) > 120:
            msg = msg[:120] + "..."
        msg = re.sub(r"/home/[^/]+/", "~/", msg)
        msg = re.sub(r"/Users/[^/]+/", "~/", msg)
        msg = msg.replace("/root/", "~/")
        msg = msg.replace("/mnt/", "~/")
        msg = msg.replace("/tmp/", "~/")
        msg = re.sub(r"(?i)(key|token|secret|password|api_key)=[^\s,;)\"']+", r"\1=***", msg)
        return msg

    def _try_import(name: str, module: str, attr: str) -> None:
        try:
            mod = importlib.import_module(module)
            val = getattr(mod, attr, None)
            if val is None:
                _check(name, False, f"{attr} not found in {module}")
            else:
                _check(name, True, f"{attr} available")
        except Exception as exc:
            _check(name, False, _safe_err(exc))

    _try_import("worker_facade", "apps.cli.commands.worker_facade_cmd", "COMMAND_HANDLERS")

    try:
        cat = importlib.import_module("apps.cli.command_catalog")
        _check("command_catalog", True,
               f"{len(cat.CATALOG)} commands, {len(cat.GROUPS)} groups")
    except Exception as exc:
        _check("command_catalog", False, _safe_err(exc))

    _try_import("run_contract", "packages.orchestration.run_contract", "ContractAction")
    _try_import("mission_facade", "packages.orchestration.dogfood_run", "run_mission_loop")
    _try_import("self_repair_proposal", "packages.orchestration.self_repair_proposal",
                "list_self_repair_proposals")
    _try_import("review_bundle", "packages.orchestration.review_bundle", "build_review_bundle")
    _try_import("config", "packages.orchestration.config", "get_config")
    _try_import("approval_policy", "packages.orchestration.execution_approval_policy",
                "evaluate_execution_approval_policy")

    fast_lane = Path("scripts/remedy_test_fast.sh")
    _check("fast_test_lane", fast_lane.exists(), str(fast_lane))

    full_lane = Path("scripts/remedy_test_full.sh")
    _check("full_test_lane", full_lane.exists(), str(full_lane))

    blockers: list[str] = [str(c["check"]) for c in checks if not c["ok"]]
    ready = len(blockers) == 0

    result: dict[str, Any] = {
        "ready": ready,
        "checks": checks,
        "blockers": blockers,
    }

    if getattr(ns, "json", False):
        print(json.dumps(result, indent=2))
        return
    print(f"Core Product Spine: {'READY' if ready else 'NOT READY'}")
    for c in checks:
        ok = "OK" if c["ok"] else "FAIL"
        print(f"  [{ok}] {c['check']}: {c['detail']}")
    if blockers:
        print(f"  blockers: {', '.join(blockers)}")


# ---------------------------------------------------------------------------
# approval policy-list (Step 2753)
# ---------------------------------------------------------------------------


def _cmd_approval_policy_list(ns: argparse.Namespace) -> None:
    from packages.orchestration.execution_approval_policy import (
        list_execution_approval_policies,
    )
    policies = list_execution_approval_policies()
    if getattr(ns, "json", False):
        print(json.dumps({"policies": policies, "count": len(policies)}, indent=2))
        return
    print(f"Approval policies: {len(policies)}")
    for p in policies:
        status = "ENABLED" if p.get("enabled") else "disabled"
        print(f"  [{status}] {p.get('policy_id', '?')}: {p.get('label', '')}")


# ---------------------------------------------------------------------------
# approval policy-show (Step 2754)
# ---------------------------------------------------------------------------


def _cmd_approval_policy_show(ns: argparse.Namespace) -> None:
    from packages.orchestration.execution_approval_policy import (
        load_execution_approval_policy,
    )
    policy_id = getattr(ns, "policy_id", "")
    if not policy_id:
        _err("policy_id required")
    policy = load_execution_approval_policy(policy_id)
    if not policy:
        _err(f"policy not found: {policy_id}")
    if getattr(ns, "json", False):
        print(json.dumps(policy.to_dict(), indent=2))
        return
    d = policy.to_dict()
    print(f"Policy: {d['policy_id']}")
    print(f"  label: {d['label']}")
    print(f"  enabled: {d['enabled']}")
    print(f"  adapter: {d['adapter_id']} ({d['adapter_kind']})")
    print(f"  template: {d['template_id']} ({d['template_kind']})")
    print(f"  uses: {d['uses_consumed']}/{d['max_uses']}")


# ---------------------------------------------------------------------------
# approval policy-enable (Step 2755)
# ---------------------------------------------------------------------------


def _cmd_approval_policy_enable(ns: argparse.Namespace) -> None:
    from packages.orchestration.execution_approval_policy import (
        load_execution_approval_policy,
        save_execution_approval_policy,
    )
    policy_id = getattr(ns, "policy_id", "")
    if not policy_id:
        _err("policy_id required")
    policy = load_execution_approval_policy(policy_id)
    if not policy:
        from packages.orchestration.execution_approval_policy import default_policies
        for dp in default_policies():
            if dp.policy_id == policy_id:
                policy = dp
                break
    if not policy:
        _err(f"policy not found: {policy_id}")

    if not policy.requires_fixture_only and not policy.allow_real_provider:
        confirm = getattr(ns, "confirm_real_provider", False)
        if not confirm:
            _err(
                f"Policy {policy_id} is for a real provider. "
                "Pass --confirm-real-provider to enable."
            )
        policy.allow_real_provider = True

    policy.enabled = True
    policy.updated_at = json.loads(json.dumps(
        {"t": __import__("datetime").datetime.now(
            __import__("datetime").timezone.utc,
        ).isoformat()},
    ))["t"]

    ok = save_execution_approval_policy(policy)
    result: dict[str, Any] = {
        "policy_id": policy_id,
        "enabled": ok,
        "allow_real_provider": policy.allow_real_provider,
    }
    if getattr(ns, "json", False):
        print(json.dumps(result, indent=2))
        return
    print(f"Policy {policy_id}: {'ENABLED' if ok else 'FAILED'}")


# ---------------------------------------------------------------------------
# approval policy-disable (Step 2756)
# ---------------------------------------------------------------------------


def _cmd_approval_policy_disable(ns: argparse.Namespace) -> None:
    from packages.orchestration.execution_approval_policy import (
        load_execution_approval_policy,
        save_execution_approval_policy,
    )
    policy_id = getattr(ns, "policy_id", "")
    if not policy_id:
        _err("policy_id required")
    policy = load_execution_approval_policy(policy_id)
    if not policy:
        _err(f"policy not found: {policy_id}")
    policy.enabled = False
    policy.updated_at = json.loads(json.dumps(
        {"t": __import__("datetime").datetime.now(
            __import__("datetime").timezone.utc,
        ).isoformat()},
    ))["t"]
    ok = save_execution_approval_policy(policy)
    if getattr(ns, "json", False):
        print(json.dumps({"policy_id": policy_id, "disabled": ok}, indent=2))
        return
    print(f"Policy {policy_id}: {'DISABLED' if ok else 'FAILED'}")


# ---------------------------------------------------------------------------
# approval policy-evaluate (Step 2757)
# ---------------------------------------------------------------------------


def _cmd_approval_policy_evaluate(ns: argparse.Namespace) -> None:
    from packages.orchestration.execution_approval_policy import (
        evaluate_execution_approval_policy,
    )
    session_id = getattr(ns, "session_id", "")
    template_id = getattr(ns, "template_id", "")
    if not session_id:
        _err("session_id required")
    if not template_id:
        _err("template_id required (--template)")
    decision = evaluate_execution_approval_policy(session_id, template_id)
    if getattr(ns, "json", False):
        print(json.dumps(decision.to_dict(), indent=2))
        return
    print(f"Policy evaluation: {decision.decision_code}")
    print(f"  allowed: {decision.allowed}")
    print(f"  reason: {decision.reason}")


# ---------------------------------------------------------------------------
# approval policy-grant (Step 2758)
# ---------------------------------------------------------------------------


def _cmd_approval_policy_grant(ns: argparse.Namespace) -> None:
    from packages.orchestration.execution_approval_policy import (
        create_policy_granted_execution_approval,
    )
    session_id = getattr(ns, "session_id", "")
    template_id = getattr(ns, "template_id", "")
    if not session_id:
        _err("session_id required")
    if not template_id:
        _err("template_id required (--template)")
    result = create_policy_granted_execution_approval(session_id, template_id)
    if getattr(ns, "json", False):
        print(json.dumps(result, indent=2))
        return
    if result["granted"]:
        print(f"Approval granted: {result['approval_id']}")
    else:
        print(f"Denied: {result['decision'].get('decision_code', 'unknown')}")
        print(f"  reason: {result['decision'].get('reason', '')}")


# ---------------------------------------------------------------------------
# Handler registry
# ---------------------------------------------------------------------------


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "worker.doctor": _cmd_worker_doctor,
    "worker.add": _cmd_worker_add,
    "worker.disable": _cmd_worker_disable,
    "mission.run": _cmd_mission_run,
    "mission.report": _cmd_mission_report,
    "doctor.core": _cmd_doctor_core,
    "approval.policy-list": _cmd_approval_policy_list,
    "approval.policy-show": _cmd_approval_policy_show,
    "approval.policy-enable": _cmd_approval_policy_enable,
    "approval.policy-disable": _cmd_approval_policy_disable,
    "approval.policy-evaluate": _cmd_approval_policy_evaluate,
    "approval.policy-grant": _cmd_approval_policy_grant,
}
