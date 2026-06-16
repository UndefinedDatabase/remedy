"""Runtime CLI handlers for the Main Builder Adapter v0 (Step 1981).

Metadata-only handlers. No provider/model execution. No secrets. No raw output. JSON-safe.
"""
from __future__ import annotations

import json
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import argparse


def _out(data: dict, ns: argparse.Namespace) -> None:
    if getattr(ns, "json", False):
        json.dump(data, sys.stdout, indent=2, default=str)
        sys.stdout.write("\n")
    else:
        for k, v in data.items():
            print(f"  {k}: {v}")


def _err(msg: str) -> None:
    print(msg, file=sys.stderr)
    sys.exit(1)


def _cmd_adapter_list(ns: argparse.Namespace) -> None:
    from packages.orchestration.main_builder_adapter import list_builder_adapter_specs
    specs = list_builder_adapter_specs()
    _out({"adapters": specs, "count": len(specs)}, ns)


def _cmd_adapter_show(ns: argparse.Namespace) -> None:
    from packages.orchestration.main_builder_adapter import get_builder_adapter_spec
    adapter_id = getattr(ns, "adapter_id", "")
    spec = get_builder_adapter_spec(adapter_id)
    if not spec:
        _err(f"Adapter not found: {adapter_id}")
    _out(spec, ns)


def _cmd_adapter_enable(ns: argparse.Namespace) -> None:
    from packages.orchestration.main_builder_adapter import (
        _ALL_MODES,
        BuilderAdapterMode,
        BuilderAdapterSpec,
        get_builder_adapter_spec,
        save_builder_adapter_spec,
    )
    adapter_id = getattr(ns, "adapter_id", "")
    mode = getattr(ns, "mode", "")
    if mode not in _ALL_MODES:
        _err(f"Invalid mode: {mode}. Valid: {sorted(_ALL_MODES)}")
    spec_d = get_builder_adapter_spec(adapter_id)
    if not spec_d:
        _err(f"Adapter not found: {adapter_id}")
    spec = BuilderAdapterSpec.from_dict(spec_d)
    spec.enabled = mode != BuilderAdapterMode.DISABLED
    spec.mode = mode
    ok = save_builder_adapter_spec(spec)
    if not ok:
        _err("Failed to save adapter spec (possible secret/raw content detected).")
    _out(spec.to_dict(), ns)


def _cmd_package_create(ns: argparse.Namespace) -> None:
    from packages.orchestration.main_builder_adapter import build_builder_request_package
    job_id = getattr(ns, "job_id", "")
    repair_id = getattr(ns, "repair_id", "") or ""
    adapter_id = getattr(ns, "adapter_id", "") or ""
    if not job_id:
        _err("job_id is required.")
    pkg = build_builder_request_package(job_id, repair_id=repair_id, adapter_id=adapter_id)
    _out(pkg.to_dict(), ns)


def _cmd_session_create(ns: argparse.Namespace) -> None:
    from packages.orchestration.main_builder_adapter import create_builder_session
    package_id = getattr(ns, "package_id", "")
    adapter_id = getattr(ns, "adapter_id", "")
    job_id = getattr(ns, "job_id", "") or ""
    repair_id = getattr(ns, "repair_id", "") or ""
    if not package_id or not adapter_id:
        _err("package_id and --adapter-id are required.")
    session = create_builder_session(package_id, adapter_id, job_id=job_id, repair_id=repair_id)
    _out(session.to_dict(), ns)


def _cmd_session_show(ns: argparse.Namespace) -> None:
    from packages.orchestration.main_builder_adapter import load_builder_session
    session_id = getattr(ns, "session_id", "")
    session = load_builder_session(session_id)
    if not session:
        _err(f"Session not found: {session_id}")
    _out(session.to_dict(), ns)


def _cmd_session_list(ns: argparse.Namespace) -> None:
    from packages.orchestration.main_builder_adapter import list_builder_sessions
    job_id = getattr(ns, "job_id", "")
    sessions = list_builder_sessions(job_id)
    _out({"sessions": sessions, "count": len(sessions)}, ns)


def _cmd_session_record_output(ns: argparse.Namespace) -> None:
    from packages.orchestration.main_builder_adapter import record_builder_session_output
    session_id = getattr(ns, "session_id", "")
    artifact_ref = getattr(ns, "artifact_ref", "") or ""
    session = record_builder_session_output(session_id, candidate_artifact_ref=artifact_ref)
    if not session:
        _err(f"Session not found: {session_id}")
    _out(session.to_dict(), ns)


def _cmd_session_intake(ns: argparse.Namespace) -> None:
    from packages.orchestration.main_builder_adapter import record_builder_session_intake_complete
    session_id = getattr(ns, "session_id", "")
    session = record_builder_session_intake_complete(session_id, sandbox_submission_id="pending")
    if not session:
        _err(f"Session not found: {session_id}")
    _out(session.to_dict(), ns)


def _cmd_integrity(ns: argparse.Namespace) -> None:
    from packages.orchestration.main_builder_adapter import builder_adapter_integrity
    result = builder_adapter_integrity()
    _out(result, ns)


COMMAND_HANDLERS: dict[str, object] = {
    "builder.adapter-list": _cmd_adapter_list,
    "builder.adapter-show": _cmd_adapter_show,
    "builder.adapter-enable": _cmd_adapter_enable,
    "builder.package-create": _cmd_package_create,
    "builder.session-create": _cmd_session_create,
    "builder.session-show": _cmd_session_show,
    "builder.session-list": _cmd_session_list,
    "builder.session-record-output": _cmd_session_record_output,
    "builder.session-intake": _cmd_session_intake,
    "builder.integrity": _cmd_integrity,
}
