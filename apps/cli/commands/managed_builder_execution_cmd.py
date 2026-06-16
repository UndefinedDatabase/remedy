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


def _cmd_template_list(ns: "argparse.Namespace") -> None:
    from packages.orchestration.managed_builder_execution import list_command_templates
    templates = list_command_templates()
    print(json.dumps(templates, indent=2))


def _cmd_template_show(ns: "argparse.Namespace") -> None:
    from packages.orchestration.managed_builder_execution import get_command_template
    tid = getattr(ns, "template_id", "")
    if not tid:
        _err("template_id required")
    tmpl = get_command_template(tid)
    if not tmpl:
        _err(f"template not found: {tid}")
    print(json.dumps(tmpl, indent=2))


def _cmd_template_create(ns: "argparse.Namespace") -> None:
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


def _cmd_approve(ns: "argparse.Namespace") -> None:
    from packages.orchestration.managed_builder_execution import approve_managed_execution
    sid = getattr(ns, "session_id", "")
    tid = getattr(ns, "template", "") or getattr(ns, "template_id", "")
    if not sid:
        _err("session_id required")
    if not tid:
        _err("--template required")
    approval = approve_managed_execution(sid, tid)
    if not approval:
        _err("approval failed (template not found or disabled)")
    print(json.dumps(approval.to_dict(), indent=2))


def _cmd_run(ns: "argparse.Namespace") -> None:
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


def _cmd_show(ns: "argparse.Namespace") -> None:
    from packages.orchestration.managed_builder_execution import get_execution_result
    eid = getattr(ns, "execution_id", "")
    if not eid:
        _err("execution_id required")
    result = get_execution_result(eid)
    if not result:
        _err(f"execution not found: {eid}")
    print(json.dumps(result, indent=2))


def _cmd_list(ns: "argparse.Namespace") -> None:
    from packages.orchestration.managed_builder_execution import list_execution_results
    job_id = getattr(ns, "job_id", "") or ""
    results = list_execution_results(job_id)
    print(json.dumps(results, indent=2))


def _cmd_debug_bundle(ns: "argparse.Namespace") -> None:
    from packages.orchestration.managed_builder_execution import build_debug_bundle
    eid = getattr(ns, "execution_id", "")
    if not eid:
        _err("execution_id required")
    bundle = build_debug_bundle(eid)
    if not bundle:
        _err(f"execution not found: {eid}")
    print(json.dumps(bundle, indent=2))


def _cmd_integrity(ns: "argparse.Namespace") -> None:
    from packages.orchestration.managed_builder_execution import managed_execution_integrity
    result = managed_execution_integrity()
    print(json.dumps(result, indent=2))


COMMAND_HANDLERS = {
    "execution.template-list": _cmd_template_list,
    "execution.template-show": _cmd_template_show,
    "execution.template-create": _cmd_template_create,
    "execution.approve": _cmd_approve,
    "execution.run": _cmd_run,
    "execution.show": _cmd_show,
    "execution.list": _cmd_list,
    "execution.debug-bundle": _cmd_debug_bundle,
    "execution.integrity": _cmd_integrity,
}
