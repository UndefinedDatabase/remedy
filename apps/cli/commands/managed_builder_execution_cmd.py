"""CLI handlers for Managed Builder Execution v1 commands.

Stdlib-only. JSON-safe. Invalid IDs → _err() with sys.exit(1).
"""

from __future__ import annotations

import json
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import argparse


def _err(msg: str) -> None:
    print(json.dumps({"error": msg}), file=sys.stderr)
    sys.exit(1)


def _cmd_template_list(ns: argparse.Namespace) -> None:
    from packages.orchestration.managed_builder_execution import list_command_templates
    templates = list_command_templates()
    print(json.dumps(templates, indent=2))


def _cmd_template_show(ns: argparse.Namespace) -> None:
    from packages.orchestration.managed_builder_execution import get_command_template
    tid = getattr(ns, "template_id", "")
    if not tid:
        _err("template_id required")
    tmpl = get_command_template(tid)
    if not tmpl:
        _err(f"template not found: {tid}")
    print(json.dumps(tmpl, indent=2))


def _cmd_template_create(ns: argparse.Namespace) -> None:
    from packages.orchestration.managed_builder_execution import CommandTemplate, save_command_template
    tid = getattr(ns, "template_id", "")
    if not tid:
        _err("template_id required")
    adapter_kind = getattr(ns, "adapter_kind", "") or ""
    argv_raw = getattr(ns, "argv", "") or ""
    if not argv_raw:
        _err("--argv required (space-separated tokens)")
    argv_tokens = argv_raw.split()
    tmpl = CommandTemplate(
        template_id=tid,
        adapter_kind=adapter_kind,
        label=getattr(ns, "label", "") or tid,
        argv_template=argv_tokens,
        allowed_placeholders=[],
        requires_approval=True,
        enabled=False,
    )
    ok = save_command_template(tmpl)
    if not ok:
        _err("template rejected by safety validation")
    print(json.dumps({"saved": True, "template_id": tid}))


def _cmd_approve(ns: argparse.Namespace) -> None:
    from packages.orchestration.managed_builder_execution import approve_managed_execution
    sid = getattr(ns, "session_id", "")
    tid = getattr(ns, "template", "") or getattr(ns, "template_id", "")
    if not sid:
        _err("session_id required")
    if not tid:
        _err("--template required")
    # v1.1: pass binding fields from CLI args.
    approval = approve_managed_execution(
        sid, tid,
        package_id=getattr(ns, "package_id", "") or "",
        adapter_id=getattr(ns, "adapter_id", "") or "",
        adapter_kind=getattr(ns, "adapter_kind", "") or "",
        max_runs=int(getattr(ns, "max_runs", 1) or 1),
        approval_scope=getattr(ns, "approval_scope", "") or "",
    )
    if not approval:
        _err("approval failed (template not found or disabled)")
    print(json.dumps(approval.to_dict(), indent=2))


def _cmd_run(ns: argparse.Namespace) -> None:
    from packages.orchestration.managed_builder_execution import run_managed_builder
    sid = getattr(ns, "session_id", "")
    tid = getattr(ns, "template", "") or getattr(ns, "template_id", "")
    if not sid:
        _err("session_id required")
    if not tid:
        _err("--template required")
    repo_path = getattr(ns, "repo_path", "") or ""
    job_id = getattr(ns, "job_id", "") or ""
    result = run_managed_builder(
        sid, template_id=tid, repo_path=repo_path, job_id=job_id,
    )
    print(json.dumps(result.to_dict(), indent=2))


def _cmd_show(ns: argparse.Namespace) -> None:
    from packages.orchestration.managed_builder_execution import get_execution_result
    eid = getattr(ns, "execution_id", "")
    if not eid:
        _err("execution_id required")
    result = get_execution_result(eid)
    if not result:
        _err(f"execution not found: {eid}")
    print(json.dumps(result, indent=2))


def _cmd_list(ns: argparse.Namespace) -> None:
    from packages.orchestration.list_options import ListOptionError, apply_list_options
    from packages.orchestration.managed_builder_execution import list_execution_results
    job_id = getattr(ns, "job_id", "") or ""
    results = list_execution_results(job_id)
    try:
        results = apply_list_options(
            results,
            sort=getattr(ns, "sort", None),
            desc=getattr(ns, "desc", False),
            since=getattr(ns, "since", None),
            until=getattr(ns, "until", None),
            limit=getattr(ns, "limit", None),
            sort_fields={
                "started_at": lambda r: r.get("started_at") or "",
                "ended_at": lambda r: r.get("ended_at") or "",
                "status": lambda r: r.get("status") or "",
                "duration_ms": lambda r: r.get("duration_ms") or 0,
            },
            default_sort_field="started_at",
            date_getter=lambda r: r.get("started_at") or None,
        )
    except ListOptionError as exc:
        _err(str(exc))
    print(json.dumps(results, indent=2))


def _cmd_debug_bundle(ns: argparse.Namespace) -> None:
    from packages.orchestration.managed_builder_execution import build_debug_bundle
    eid = getattr(ns, "execution_id", "")
    if not eid:
        _err("execution_id required")
    bundle = build_debug_bundle(eid)
    if not bundle:
        _err(f"execution not found: {eid}")
    print(json.dumps(bundle, indent=2))


def _cmd_integrity(ns: argparse.Namespace) -> None:
    from packages.orchestration.managed_builder_execution import managed_execution_integrity
    result = managed_execution_integrity()
    print(json.dumps(result, indent=2))


def _cmd_approval_show(ns: argparse.Namespace) -> None:
    from packages.orchestration.managed_builder_execution import get_execution_approval
    sid = getattr(ns, "session_id", "")
    if not sid:
        _err("session_id required")
    approval = get_execution_approval(sid)
    if not approval:
        _err(f"approval not found for session: {sid}")
    print(json.dumps(approval, indent=2))


def _cmd_approval_validate(ns: argparse.Namespace) -> None:
    from packages.orchestration.managed_builder_execution import validate_execution_approval
    sid = getattr(ns, "session_id", "")
    tid = getattr(ns, "template", "") or getattr(ns, "template_id", "")
    if not sid:
        _err("session_id required")
    if not tid:
        _err("--template required")
    codes = validate_execution_approval(sid, tid)
    print(json.dumps({"valid": len(codes) == 0, "codes": codes}, indent=2))


def _cmd_approval_list(ns: argparse.Namespace) -> None:
    from packages.orchestration.managed_builder_execution import list_execution_approvals
    approvals = list_execution_approvals()
    print(json.dumps(approvals, indent=2))


def _cmd_template_enable(ns: argparse.Namespace) -> None:
    from packages.orchestration.managed_builder_execution import enable_command_template
    tid = getattr(ns, "template_id", "")
    if not tid:
        _err("template_id required")
    tmpl = enable_command_template(tid)
    if not tmpl:
        _err(f"template not found or failed safety validation: {tid}")
    print(json.dumps(tmpl.to_dict(), indent=2))


def _cmd_template_disable(ns: argparse.Namespace) -> None:
    from packages.orchestration.managed_builder_execution import disable_command_template
    tid = getattr(ns, "template_id", "")
    if not tid:
        _err("template_id required")
    tmpl = disable_command_template(tid)
    if not tmpl:
        _err(f"template not found: {tid}")
    print(json.dumps(tmpl.to_dict(), indent=2))


def _cmd_template_update(ns: argparse.Namespace) -> None:
    from packages.orchestration.managed_builder_execution import update_command_template
    tid = getattr(ns, "template_id", "")
    if not tid:
        _err("template_id required")
    timeout = getattr(ns, "timeout_seconds", None)
    max_output = getattr(ns, "max_output_bytes", None)
    label = getattr(ns, "label", None)
    tmpl = update_command_template(
        tid,
        timeout_seconds=int(timeout) if timeout else None,
        max_output_bytes=int(max_output) if max_output else None,
        label=label,
    )
    if not tmpl:
        _err(f"template not found or update rejected: {tid}")
    print(json.dumps(tmpl.to_dict(), indent=2))


def _cmd_operator_runbook(ns: argparse.Namespace) -> None:
    from packages.orchestration.main_builder_adapter import (
        get_builder_adapter_spec,
        load_builder_session,
    )
    from packages.orchestration.managed_builder_execution import get_command_template

    sid = getattr(ns, "session_id", "")
    tid = getattr(ns, "template", "") or getattr(ns, "template_id", "")
    if not sid:
        _err("session_id required")
    if not tid:
        _err("--template required")

    session = load_builder_session(sid)
    if not session:
        _err(f"session not found: {sid}")

    tmpl = get_command_template(tid)
    spec = get_builder_adapter_spec(session.adapter_id) if session.adapter_id else None

    steps: list[dict[str, str]] = []
    blockers: list[str] = []

    if spec:
        steps.append({"step": "1", "action": f"remedy builder adapter-show {session.adapter_id} --json", "label": "Show adapter"})
        if not spec.get("enabled", False):
            blockers.append(f"Adapter {session.adapter_id} is disabled. Enable with: remedy builder adapter-enable {session.adapter_id} --mode operator_launched --json")
    else:
        blockers.append(f"Adapter {session.adapter_id} not found.")

    steps.append({"step": "2", "action": f"remedy builder session-show {sid} --json", "label": "Show session"})

    if tmpl:
        steps.append({"step": "3", "action": f"remedy execution template-show {tid} --json", "label": "Show template"})
        if not tmpl.get("enabled", False):
            blockers.append(f"Template {tid} is disabled. Enable with: remedy execution template-enable {tid} --json")
    else:
        blockers.append(f"Template {tid} not found.")

    steps.append({"step": "4", "action": f"remedy execution approve {sid} --template {tid} --json", "label": "Approve execution"})
    steps.append({"step": "5", "action": f"remedy execution run {sid} --template {tid} --json", "label": "Run execution"})
    steps.append({"step": "6", "action": "remedy execution show <execution_id> --json", "label": "Show result"})
    steps.append({"step": "7", "action": "remedy execution debug-bundle <execution_id> --json", "label": "Debug bundle"})
    steps.append({"step": "8", "action": f"remedy builder session-record-output {sid} --artifact-ref <ref> --json", "label": "Record output ref"})
    steps.append({"step": "9", "action": f"remedy builder session-intake {sid} --json", "label": "Sandbox intake"})

    runbook = {
        "session_id": sid,
        "template_id": tid,
        "adapter_id": session.adapter_id if session else "",
        "ready": len(blockers) == 0,
        "blockers": blockers,
        "steps": steps,
    }
    print(json.dumps(runbook, indent=2))


def _cmd_claude_doctor(ns: argparse.Namespace) -> None:
    import shutil

    from packages.orchestration.main_builder_adapter import get_builder_adapter_spec
    from packages.orchestration.managed_builder_execution import get_command_template

    claude_binary = shutil.which("claude")
    adapter = get_builder_adapter_spec("claude-code-v0")
    template = get_command_template("claude-code-repair-v0")

    checks: list[dict[str, str | bool]] = []
    blockers: list[str] = []

    checks.append({"check": "claude_binary_on_path", "ok": claude_binary is not None,
                    "detail": str(claude_binary or "not found")})
    if not claude_binary:
        blockers.append("Claude Code binary not found on PATH.")

    checks.append({"check": "claude_adapter_exists", "ok": adapter is not None,
                    "detail": "claude-code-v0"})
    if adapter:
        enabled = adapter.get("enabled", False)
        checks.append({"check": "claude_adapter_enabled", "ok": enabled,
                        "detail": adapter.get("mode", "disabled")})
        if not enabled:
            blockers.append("Claude Code adapter is disabled. Enable with: remedy builder adapter-enable claude-code-v0 --mode operator_launched --json")
    else:
        blockers.append("Claude Code adapter not found.")

    checks.append({"check": "claude_template_exists", "ok": template is not None,
                    "detail": "claude-code-repair-v0"})
    if template:
        enabled = template.get("enabled", False)
        checks.append({"check": "claude_template_enabled", "ok": enabled,
                        "detail": str(enabled)})
        if not enabled:
            blockers.append("Claude Code template is disabled. Enable with: remedy execution template-enable claude-code-repair-v0 --json")
    else:
        blockers.append("Claude Code template not found.")

    report = {
        "ready": len(blockers) == 0,
        "checks": checks,
        "blockers": blockers,
    }
    print(json.dumps(report, indent=2))


COMMAND_HANDLERS = {
    "execution.template-list": _cmd_template_list,
    "execution.template-show": _cmd_template_show,
    "execution.template-create": _cmd_template_create,
    "execution.template-enable": _cmd_template_enable,
    "execution.template-disable": _cmd_template_disable,
    "execution.template-update": _cmd_template_update,
    "execution.approve": _cmd_approve,
    "execution.run": _cmd_run,
    "execution.show": _cmd_show,
    "execution.list": _cmd_list,
    "execution.debug-bundle": _cmd_debug_bundle,
    "execution.integrity": _cmd_integrity,
    "execution.approval-show": _cmd_approval_show,
    "execution.approval-validate": _cmd_approval_validate,
    "execution.approval-list": _cmd_approval_list,
    "execution.operator-runbook": _cmd_operator_runbook,
    "execution.claude-doctor": _cmd_claude_doctor,
}
