"""
Managed External Builder Execution v1 + Dogfood Observability (Steps 2026-2075).

The first managed execution seam for external builder adapters. Remedy can launch a builder session
via a bounded subprocess — but ONLY through a pre-approved command template, with a sanitized
environment, hard timeout, output byte cap, and mandatory sandbox intake.

  Workers execute. Remedy governs. Subprocess ONLY through bounded command templates.

This module is the ONLY place in the codebase that may invoke subprocess for builder execution.
It enforces:
  - shell=False ALWAYS (argv list only, never a shell string).
  - Sanitized env: only allowlisted keys passed to subprocess (PATH, HOME, LANG, TERM; NO secrets/
    tokens/API keys/proxy vars).
  - Hard timeout: max 600s (killed on timeout).
  - Output byte cap: max 256KB stdout+stderr (truncated, not streamed).
  - Command template: every argv token validated at save time against shell metacharacters,
    forbidden/destructive programs, and raw markers.
  - Operator approval required by default before any execution.
  - Managed runner disabled by default: requires explicit operator enable.
  - Output is UNTRUSTED: raw bytes go to a private file (0o600); public surfaces carry safe
    redacted refs and summaries only.
  - No auto-apply / auto-approve / auto-PR / auto-git. Builder output enters the External Builder
    Sandbox intake path → Trust Gate → Verification → human Approval → do continue.

Hard rules:
  - NO shell=True. NO arbitrary command execution. NO unconstrained subprocess.
  - NO provider SDK calls. NO secrets/tokens in subprocess env. NO network passthrough.
  - NO auto-apply/approve/test/git/PR/MemPalace/memory/embeddings/MCP.
  - NO raw output in public surfaces (scrubbed refs only).

Public API::

    # Command templates
    default_command_templates() -> list[CommandTemplate]
    save_command_template(template, data_dir=None) -> bool
    list_command_templates(data_dir=None) -> list[dict]
    get_command_template(template_id, data_dir=None) -> dict | None

    # Approval gate
    approve_managed_execution(session_id, template_id, *, operator_id="", data_dir=None) -> ExecutionApproval | None
    get_execution_approval(session_id, data_dir=None) -> dict | None

    # Managed runner
    run_managed_builder(session_id, *, template_id="", placeholder_values=None,
        repo_path="", data_dir=None) -> ManagedExecutionResult

    # Event ledger + debug bundle
    list_execution_events(session_id, data_dir=None) -> list[dict]
    get_execution_result(execution_id, data_dir=None) -> dict | None
    list_execution_results(job_id="", data_dir=None) -> list[dict]
    build_debug_bundle(execution_id, data_dir=None) -> dict | None

    # Integration
    managed_execution_mission_signal(job_id, data_dir=None) -> dict
    managed_execution_integrity(data_dir=None) -> dict
"""

from __future__ import annotations

import json
import logging
import os
import re
import signal
import subprocess
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from packages.orchestration.exec_guard import ExecGuardPolicy, run_guarded
from packages.orchestration.provider_trust import _safe_path_label, _scrub_public

_log = logging.getLogger("remedy.managed_execution")


# ---------------------------------------------------------------------------
# Constants / safety
# ---------------------------------------------------------------------------

SCHEMA_VERSION = "managed-builder-execution-v1"
_MBE_DIRNAME = "managed_builder_execution"

_RAW_MARKERS = ("diff --git", "-----BEGIN", "Traceback (most recent call last)", "sk-",
                "api_key", "apikey", "password", "secret_key")

_SK_PATTERN = re.compile(r"\bsk-[A-Za-z0-9_-]{6,}\b")

# Shell metacharacters — must never appear in template argv tokens.
_SHELL_METACHARS = (";", "|", "&", "$", "`", ">", "<", "\n", "&&", "||", "$(")

# Destructive / forbidden programs.
_FORBIDDEN_PROGRAMS = frozenset({
    "rm", "rmdir", "mkfs", "dd", "sudo", "shutdown", "reboot",
    "curl", "wget", "ssh", "scp", "chmod", "chown", "kill", "killall",
})

# Env keys that may be passed to subprocess (everything else stripped).
_ALLOWED_ENV_KEYS = frozenset({
    "PATH", "HOME", "LANG", "LC_ALL", "TERM", "USER", "LOGNAME",
    "TMPDIR", "TMP", "TEMP", "SHELL", "XDG_RUNTIME_DIR",
})

# Env keys that must NEVER pass through (secrets, tokens, proxies).
_FORBIDDEN_ENV_KEYS = frozenset({
    "ANTHROPIC_API_KEY", "OPENAI_API_KEY", "CLAUDE_API_KEY",
    "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY",
    "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN",
    "GITHUB_TOKEN", "GH_TOKEN", "GITLAB_TOKEN",
    "DATABASE_URL", "REDIS_URL",
})

MAX_TIMEOUT_SECONDS = 600
DEFAULT_TIMEOUT_SECONDS = 300
MAX_OUTPUT_BYTES = 256 * 1024  # 256 KB
DEFAULT_APPROVAL_EXPIRY_SECONDS = 1800  # 30 minutes

# Allowed placeholder keys in command templates.
_ALLOWED_PLACEHOLDER_KEYS = frozenset({
    "repo_path", "output_dir", "goal_summary", "task_type",
    "session_id", "job_id", "repair_id", "context_file",
})


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe(text: str, limit: int = 300) -> str:
    """Truncate + scrub a string for public surfaces."""
    t = str(text or "")[:limit]
    t = _scrub_public(t)
    t = _SK_PATTERN.sub("[redacted-secret]", t)
    return t


def _resolve_ddir(data_dir: Path | None) -> Path:
    if data_dir is not None:
        return Path(data_dir)
    from packages.orchestration.data_paths import resolve_data_root
    return resolve_data_root()


def _mbe_dir(job_id: str, ddir: Path) -> Path:
    return ddir / "workspaces" / job_id / _MBE_DIRNAME


def _global_mbe_dir(ddir: Path) -> Path:
    return ddir / _MBE_DIRNAME


def _atomic_write(p: Path, data: dict[str, Any]) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.parent.exists():
        os.chmod(p.parent, 0o700)
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
    os.chmod(tmp, 0o600)
    os.replace(tmp, p)


def _load_json(p: Path) -> dict[str, Any] | None:
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def _load_json_dir(d: Path) -> list[dict[str, Any]]:
    if not d.is_dir():
        return []
    out = []
    for f in sorted(d.iterdir()):
        if f.suffix == ".json":
            blob = _load_json(f)
            if blob:
                out.append(blob)
    return out


# ---------------------------------------------------------------------------
# Command template model
# ---------------------------------------------------------------------------


@dataclass
class CommandTemplate:
    template_id: str = ""
    adapter_kind: str = ""
    label: str = ""
    argv_template: list[str] = field(default_factory=list)
    allowed_placeholders: list[str] = field(default_factory=list)
    sanitized_env_keys: list[str] = field(default_factory=lambda: sorted(_ALLOWED_ENV_KEYS))
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS
    max_output_bytes: int = MAX_OUTPUT_BYTES
    requires_approval: bool = True
    enabled: bool = False
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "template_id": self.template_id,
            "adapter_kind": self.adapter_kind,
            "label": _safe(self.label),
            "argv_template": list(self.argv_template),
            "allowed_placeholders": list(self.allowed_placeholders),
            "sanitized_env_keys": list(self.sanitized_env_keys),
            "timeout_seconds": min(int(self.timeout_seconds), MAX_TIMEOUT_SECONDS),
            "max_output_bytes": min(int(self.max_output_bytes), MAX_OUTPUT_BYTES),
            "requires_approval": bool(self.requires_approval),
            "enabled": bool(self.enabled),
            "notes": _safe(self.notes),
            "schema_version": SCHEMA_VERSION,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> CommandTemplate:
        return cls(
            template_id=str(d.get("template_id", "")),
            adapter_kind=str(d.get("adapter_kind", "")),
            label=str(d.get("label", "")),
            argv_template=list(d.get("argv_template") or []),
            allowed_placeholders=list(d.get("allowed_placeholders") or []),
            sanitized_env_keys=list(d.get("sanitized_env_keys") or sorted(_ALLOWED_ENV_KEYS)),
            timeout_seconds=min(int(d.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS)), MAX_TIMEOUT_SECONDS),
            max_output_bytes=min(int(d.get("max_output_bytes", MAX_OUTPUT_BYTES)), MAX_OUTPUT_BYTES),
            requires_approval=bool(d.get("requires_approval", True)),
            enabled=bool(d.get("enabled", False)),
            notes=str(d.get("notes", "")),
        )


# ---------------------------------------------------------------------------
# Execution approval model
# ---------------------------------------------------------------------------


class ApprovalScope:
    SINGLE_RUN = "single_run"
    SESSION_LIFETIME = "session_lifetime"
    TIME_BOUNDED = "time_bounded"


_ALL_APPROVAL_SCOPES = frozenset({
    ApprovalScope.SINGLE_RUN,
    ApprovalScope.SESSION_LIFETIME,
    ApprovalScope.TIME_BOUNDED,
})


@dataclass
class ExecutionApproval:
    approval_id: str = ""
    session_id: str = ""
    template_id: str = ""
    operator_id: str = ""
    approved_at: str = ""
    notes: str = ""
    # v1.1 hardening fields
    package_id: str = ""
    adapter_id: str = ""
    adapter_kind: str = ""
    expires_at: str = ""
    max_runs: int = 0  # 0 = unlimited
    used_count: int = 0
    max_runtime_seconds: int = MAX_TIMEOUT_SECONDS
    max_output_bytes: int = MAX_OUTPUT_BYTES
    approval_scope: str = ApprovalScope.SINGLE_RUN

    def to_dict(self) -> dict[str, Any]:
        return {
            "approval_id": self.approval_id,
            "session_id": self.session_id,
            "template_id": self.template_id,
            "operator_id": _safe(self.operator_id, 100),
            "approved_at": self.approved_at,
            "notes": _safe(self.notes),
            "package_id": self.package_id,
            "adapter_id": self.adapter_id,
            "adapter_kind": self.adapter_kind,
            "expires_at": self.expires_at,
            "max_runs": self.max_runs,
            "used_count": self.used_count,
            "max_runtime_seconds": min(int(self.max_runtime_seconds), MAX_TIMEOUT_SECONDS),
            "max_output_bytes": min(int(self.max_output_bytes), MAX_OUTPUT_BYTES),
            "approval_scope": self.approval_scope if self.approval_scope in _ALL_APPROVAL_SCOPES else ApprovalScope.SINGLE_RUN,
            "schema_version": SCHEMA_VERSION,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> ExecutionApproval:
        return cls(
            approval_id=str(d.get("approval_id", "")),
            session_id=str(d.get("session_id", "")),
            template_id=str(d.get("template_id", "")),
            operator_id=str(d.get("operator_id", "")),
            approved_at=str(d.get("approved_at", "")),
            notes=str(d.get("notes", "")),
            package_id=str(d.get("package_id", "")),
            adapter_id=str(d.get("adapter_id", "")),
            adapter_kind=str(d.get("adapter_kind", "")),
            expires_at=str(d.get("expires_at", "")),
            max_runs=int(d.get("max_runs", 0)),
            used_count=int(d.get("used_count", 0)),
            max_runtime_seconds=min(int(d.get("max_runtime_seconds", MAX_TIMEOUT_SECONDS)), MAX_TIMEOUT_SECONDS),
            max_output_bytes=min(int(d.get("max_output_bytes", MAX_OUTPUT_BYTES)), MAX_OUTPUT_BYTES),
            approval_scope=str(d.get("approval_scope", ApprovalScope.SINGLE_RUN)),
        )


# ---------------------------------------------------------------------------
# Execution event model
# ---------------------------------------------------------------------------


class ExecutionEventKind:
    REQUESTED = "execution_requested"
    APPROVED = "execution_approved"
    STARTED = "execution_started"
    COMPLETED = "execution_completed"
    FAILED = "execution_failed"
    TIMEOUT = "execution_timeout"
    INTAKE_STARTED = "intake_started"
    INTAKE_COMPLETED = "intake_completed"
    # v1.1 hardening events
    APPROVAL_EXPIRED = "approval_expired"
    APPROVAL_EXHAUSTED = "approval_exhausted"
    APPROVAL_VALIDATED = "approval_validated"
    BINDING_MISMATCH = "binding_mismatch"
    APPROVAL_CONSUMED = "approval_consumed"
    RUNTIME_CAP_APPLIED = "runtime_cap_applied"
    OUTPUT_CAP_APPLIED = "output_cap_applied"
    OUTPUT_REF_CREATED = "output_ref_created"


_ALL_EVENT_KINDS = frozenset({
    ExecutionEventKind.REQUESTED, ExecutionEventKind.APPROVED,
    ExecutionEventKind.STARTED, ExecutionEventKind.COMPLETED,
    ExecutionEventKind.FAILED, ExecutionEventKind.TIMEOUT,
    ExecutionEventKind.INTAKE_STARTED, ExecutionEventKind.INTAKE_COMPLETED,
    ExecutionEventKind.APPROVAL_EXPIRED, ExecutionEventKind.APPROVAL_EXHAUSTED,
    ExecutionEventKind.APPROVAL_VALIDATED, ExecutionEventKind.BINDING_MISMATCH,
    ExecutionEventKind.APPROVAL_CONSUMED, ExecutionEventKind.RUNTIME_CAP_APPLIED,
    ExecutionEventKind.OUTPUT_CAP_APPLIED, ExecutionEventKind.OUTPUT_REF_CREATED,
})


@dataclass
class ExecutionEvent:
    event_id: str = ""
    execution_id: str = ""
    session_id: str = ""
    kind: str = ""
    timestamp: str = ""
    safe_summary: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "execution_id": self.execution_id,
            "session_id": self.session_id,
            "kind": self.kind,
            "timestamp": self.timestamp,
            "safe_summary": _safe(self.safe_summary, 500),
            "metadata": {k: _safe(str(v)) for k, v in list(self.metadata.items())[:20]},
            "schema_version": SCHEMA_VERSION,
        }


# ---------------------------------------------------------------------------
# Managed execution result model
# ---------------------------------------------------------------------------


class ManagedExecutionStatus:
    NOT_STARTED = "not_started"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    BLOCKED = "blocked"
    APPROVAL_REQUIRED = "approval_required"


_ALL_EXECUTION_STATUSES = frozenset({
    ManagedExecutionStatus.NOT_STARTED, ManagedExecutionStatus.RUNNING,
    ManagedExecutionStatus.COMPLETED, ManagedExecutionStatus.FAILED,
    ManagedExecutionStatus.TIMEOUT, ManagedExecutionStatus.BLOCKED,
    ManagedExecutionStatus.APPROVAL_REQUIRED,
})


@dataclass
class ManagedExecutionResult:
    execution_id: str = ""
    session_id: str = ""
    template_id: str = ""
    job_id: str = ""
    status: str = ManagedExecutionStatus.NOT_STARTED
    exit_code: int | None = None
    duration_ms: int = 0
    output_ref: str = ""
    safe_summary: str = ""
    blocking_reasons: list[str] = field(default_factory=list)
    next_safe_action: str = ""
    started_at: str = ""
    ended_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "session_id": self.session_id,
            "template_id": self.template_id,
            "job_id": self.job_id,
            "status": self.status,
            "exit_code": self.exit_code,
            "duration_ms": self.duration_ms,
            "output_ref": _safe(self.output_ref, 200),
            "safe_summary": _safe(self.safe_summary, 500),
            "blocking_reasons": [_safe(r) for r in self.blocking_reasons[:10]],
            "next_safe_action": _safe(self.next_safe_action, 500),
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "schema_version": SCHEMA_VERSION,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> ManagedExecutionResult:
        return cls(
            execution_id=str(d.get("execution_id", "")),
            session_id=str(d.get("session_id", "")),
            template_id=str(d.get("template_id", "")),
            job_id=str(d.get("job_id", "")),
            status=str(d.get("status", ManagedExecutionStatus.NOT_STARTED)),
            exit_code=d.get("exit_code"),
            duration_ms=int(d.get("duration_ms", 0)),
            output_ref=str(d.get("output_ref", "")),
            safe_summary=str(d.get("safe_summary", "")),
            blocking_reasons=list(d.get("blocking_reasons") or []),
            next_safe_action=str(d.get("next_safe_action", "")),
            started_at=str(d.get("started_at", "")),
            ended_at=str(d.get("ended_at", "")),
        )


# ---------------------------------------------------------------------------
# Command template registry
# ---------------------------------------------------------------------------


def default_command_templates() -> list[CommandTemplate]:
    """Default command templates — all disabled by default."""
    return [
        CommandTemplate(
            template_id="claude-code-repair-v0",
            adapter_kind="claude_code",
            label="Claude Code — repair task",
            argv_template=["claude", "--print", "--output-format", "json",
                           "--max-turns", "5", "{goal_summary}"],
            allowed_placeholders=["goal_summary"],
            requires_approval=True, enabled=False,
        ),
        CommandTemplate(
            template_id="generic-cli-repair-v0",
            adapter_kind="generic_external_cli_builder",
            label="Generic CLI builder — repair task",
            argv_template=["{repo_path}/.remedy/builder.sh", "--session", "{session_id}",
                           "--output", "{output_dir}"],
            allowed_placeholders=["repo_path", "output_dir", "session_id"],
            requires_approval=True, enabled=False,
        ),
    ]


def _templates_dir(ddir: Path) -> Path:
    return ddir / _MBE_DIRNAME / "templates"


def _validate_argv_template(argv: list[str]) -> tuple[bool, str]:
    """Validate argv tokens for shell safety."""
    if not argv:
        return False, "empty argv template"
    for i, tok in enumerate(argv):
        for meta in _SHELL_METACHARS:
            if meta in tok:
                return False, f"shell metacharacter '{meta}' in argv[{i}]"
    # First token (program) must not be forbidden.
    prog = os.path.basename(str(argv[0]).strip("{}"))
    if prog in _FORBIDDEN_PROGRAMS:
        return False, f"forbidden program: {prog}"
    return True, "ok"


def save_command_template(template: CommandTemplate, data_dir: Path | None = None) -> bool:
    """Save a command template. Validates safety. Returns False on rejection."""
    ddir = _resolve_ddir(data_dir)
    # Validate argv.
    ok, reason = _validate_argv_template(template.argv_template)
    if not ok:
        return False
    # Validate placeholders.
    for ph in template.allowed_placeholders:
        if ph not in _ALLOWED_PLACEHOLDER_KEYS:
            return False
    # Clamp timeout/output.
    template.timeout_seconds = min(template.timeout_seconds, MAX_TIMEOUT_SECONDS)
    template.max_output_bytes = min(template.max_output_bytes, MAX_OUTPUT_BYTES)
    d = template.to_dict()
    # Reject raw markers in serialized form.
    blob = json.dumps(d).lower()
    for marker in _RAW_MARKERS:
        if marker.lower() in blob:
            return False
    _atomic_write(_templates_dir(ddir) / f"{template.template_id}.json", d)
    return True


def list_command_templates(data_dir: Path | None = None) -> list[dict[str, Any]]:
    ddir = _resolve_ddir(data_dir)
    stored = _load_json_dir(_templates_dir(ddir))
    if stored:
        return stored
    return [t.to_dict() for t in default_command_templates()]


def get_command_template(template_id: str, data_dir: Path | None = None) -> dict[str, Any] | None:
    for t in list_command_templates(data_dir):
        if t.get("template_id") == template_id:
            return t
    return None


def enable_command_template(template_id: str, data_dir: Path | None = None) -> CommandTemplate | None:
    """Enable a command template. Validates safety before enabling. Returns None if not found or unsafe."""
    ddir = _resolve_ddir(data_dir)
    tmpl_d = get_command_template(template_id, ddir)
    if not tmpl_d:
        return None
    tmpl = CommandTemplate.from_dict(tmpl_d)
    ok, reason = _validate_argv_template(tmpl.argv_template)
    if not ok:
        return None
    tmpl.enabled = True
    if not save_command_template(tmpl, ddir):
        return None
    return tmpl


def disable_command_template(template_id: str, data_dir: Path | None = None) -> CommandTemplate | None:
    """Disable a command template. Returns None if not found."""
    ddir = _resolve_ddir(data_dir)
    tmpl_d = get_command_template(template_id, ddir)
    if not tmpl_d:
        return None
    tmpl = CommandTemplate.from_dict(tmpl_d)
    tmpl.enabled = False
    if not save_command_template(tmpl, ddir):
        return None
    return tmpl


def update_command_template(
    template_id: str, *,
    timeout_seconds: int | None = None,
    max_output_bytes: int | None = None,
    label: str | None = None,
    data_dir: Path | None = None,
) -> CommandTemplate | None:
    """Update mutable fields of a command template. Returns None if not found or rejected."""
    ddir = _resolve_ddir(data_dir)
    tmpl_d = get_command_template(template_id, ddir)
    if not tmpl_d:
        return None
    tmpl = CommandTemplate.from_dict(tmpl_d)
    if timeout_seconds is not None:
        tmpl.timeout_seconds = min(int(timeout_seconds), MAX_TIMEOUT_SECONDS)
    if max_output_bytes is not None:
        tmpl.max_output_bytes = min(int(max_output_bytes), MAX_OUTPUT_BYTES)
    if label is not None:
        tmpl.label = label
    if not save_command_template(tmpl, ddir):
        return None
    return tmpl


# ---------------------------------------------------------------------------
# Operator approval gate
# ---------------------------------------------------------------------------


def approve_managed_execution(
    session_id: str, template_id: str, *, operator_id: str = "",
    package_id: str = "", adapter_id: str = "", adapter_kind: str = "",
    expires_at: str = "", max_runs: int = 1,
    max_runtime_seconds: int = 0, max_output_bytes: int = 0,
    approval_scope: str = "",
    data_dir: Path | None = None,
) -> ExecutionApproval | None:
    """Record operator approval for a managed execution. No auto-approval.

    v1.1: approval is scoped, expiring, bounded, and bound to session/package/adapter/template.
    Default scope is single_run (one execution only). max_runs defaults to 1.
    """
    ddir = _resolve_ddir(data_dir)
    tmpl = get_command_template(template_id, ddir)
    if not tmpl:
        return None
    if not tmpl.get("enabled", False):
        return None

    # Default expiry: now + 30 minutes if not specified.
    if not expires_at:
        from datetime import timedelta
        expires_at = (datetime.now(timezone.utc) + timedelta(seconds=DEFAULT_APPROVAL_EXPIRY_SECONDS)).isoformat()

    # R-0113: auto-bind package_id, adapter_id, adapter_kind from real session when omitted.
    try:
        from packages.orchestration.main_builder_adapter import (
            get_builder_adapter_spec,
            load_builder_session,
        )
        session = load_builder_session(session_id, ddir)
        if session:
            if not package_id and session.package_id:
                package_id = session.package_id
            if not adapter_id and session.adapter_id:
                adapter_id = session.adapter_id
            if not adapter_kind and session.adapter_id:
                spec = get_builder_adapter_spec(session.adapter_id, ddir)
                if spec:
                    spec_dict = spec if isinstance(spec, dict) else spec.to_dict()
                    adapter_kind = spec_dict.get("kind", "")
    except ImportError:
        pass  # graceful degradation

    # Derive adapter_kind from template if still not specified.
    ak = adapter_kind or tmpl.get("adapter_kind", "")
    scope = approval_scope if approval_scope in _ALL_APPROVAL_SCOPES else ApprovalScope.SINGLE_RUN

    # For single_run, force max_runs=1.
    if scope == ApprovalScope.SINGLE_RUN:
        max_runs = 1

    # Clamp caps.
    runtime_cap = min(max_runtime_seconds, MAX_TIMEOUT_SECONDS) if max_runtime_seconds > 0 else MAX_TIMEOUT_SECONDS
    output_cap = min(max_output_bytes, MAX_OUTPUT_BYTES) if max_output_bytes > 0 else MAX_OUTPUT_BYTES

    approval = ExecutionApproval(
        approval_id=uuid4().hex[:16],
        session_id=session_id,
        template_id=template_id,
        operator_id=operator_id or "operator",
        approved_at=_now(),
        package_id=package_id,
        adapter_id=adapter_id,
        adapter_kind=ak,
        expires_at=expires_at,
        max_runs=max(0, max_runs),
        used_count=0,
        max_runtime_seconds=runtime_cap,
        max_output_bytes=output_cap,
        approval_scope=scope,
    )
    _atomic_write(
        _global_mbe_dir(ddir) / "approvals" / f"{session_id}.json",
        approval.to_dict(),
    )
    return approval


def get_execution_approval(session_id: str, data_dir: Path | None = None) -> dict[str, Any] | None:
    ddir = _resolve_ddir(data_dir)
    return _load_json(_global_mbe_dir(ddir) / "approvals" / f"{session_id}.json")


def list_execution_approvals(data_dir: Path | None = None) -> list[dict[str, Any]]:
    """List all execution approvals."""
    ddir = _resolve_ddir(data_dir)
    return _load_json_dir(_global_mbe_dir(ddir) / "approvals")


def validate_execution_approval(
    session_id: str, template_id: str, *,
    package_id: str = "", adapter_id: str = "",
    data_dir: Path | None = None,
) -> list[str]:
    """Validate an execution approval against 11 safety codes.

    Returns a list of violation codes (empty = valid).
    Codes: approval_not_found, approval_expired, approval_exhausted,
    template_mismatch, adapter_kind_mismatch, session_mismatch,
    package_mismatch, adapter_mismatch, runtime_exceeds_cap,
    output_exceeds_cap, scope_violation.
    """
    ddir = _resolve_ddir(data_dir)
    codes: list[str] = []

    approval = get_execution_approval(session_id, ddir)
    if not approval:
        return ["approval_not_found"]

    # 1. Session mismatch.
    if approval.get("session_id", "") != session_id:
        codes.append("session_mismatch")

    # 2. Template mismatch.
    if approval.get("template_id", "") != template_id:
        codes.append("template_mismatch")

    # 3. Expiry check — missing/empty expires_at is treated as expired.
    expires_at = approval.get("expires_at", "")
    if not expires_at:
        codes.append("approval_expired")
    else:
        try:
            exp_dt = datetime.fromisoformat(expires_at)
            if datetime.now(timezone.utc) > exp_dt:
                codes.append("approval_expired")
        except (ValueError, TypeError):
            codes.append("approval_expired")

    # 4. Exhaustion check.
    max_runs = int(approval.get("max_runs", 0))
    used_count = int(approval.get("used_count", 0))
    if max_runs > 0 and used_count >= max_runs:
        codes.append("approval_exhausted")

    # 5. Scope violation (single_run already used).
    scope = approval.get("approval_scope", ApprovalScope.SINGLE_RUN)
    if scope == ApprovalScope.SINGLE_RUN and used_count >= 1:
        if "approval_exhausted" not in codes:
            codes.append("scope_violation")

    # 6. Adapter kind mismatch.
    tmpl = get_command_template(template_id, ddir)
    approval_ak = approval.get("adapter_kind", "")
    if tmpl and approval_ak:
        template_ak = tmpl.get("adapter_kind", "")
        if template_ak and approval_ak != template_ak:
            codes.append("adapter_kind_mismatch")

    # 7. Package binding.
    approval_pkg = approval.get("package_id", "")
    if approval_pkg and package_id and approval_pkg != package_id:
        codes.append("package_mismatch")

    # 8. Adapter binding.
    approval_adapter = approval.get("adapter_id", "")
    if approval_adapter and adapter_id and approval_adapter != adapter_id:
        codes.append("adapter_mismatch")

    # 9. Runtime cap.
    if tmpl:
        tmpl_timeout = tmpl.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS)
        approval_runtime = int(approval.get("max_runtime_seconds", MAX_TIMEOUT_SECONDS))
        if approval_runtime > 0 and tmpl_timeout > approval_runtime:
            codes.append("runtime_exceeds_cap")

    # 10. Output cap.
    if tmpl:
        tmpl_output = tmpl.get("max_output_bytes", MAX_OUTPUT_BYTES)
        approval_output = int(approval.get("max_output_bytes", MAX_OUTPUT_BYTES))
        if approval_output > 0 and tmpl_output > approval_output:
            codes.append("output_exceeds_cap")

    # 11+. Session/adapter/template binding validation (R-0107).
    codes.extend(_validate_session_binding(
        session_id, template_id, approval, tmpl, ddir,
    ))

    return codes


def _validate_session_binding(
    session_id: str, template_id: str,
    approval: dict[str, Any], tmpl: dict[str, Any] | None,
    ddir: Path,
) -> list[str]:
    """Validate approval against real session, adapter, and template bindings (R-0107)."""
    codes: list[str] = []
    try:
        from packages.orchestration.main_builder_adapter import (
            get_builder_adapter_spec,
            load_builder_session,
        )
    except ImportError:
        return codes  # graceful degradation if module not available

    # Load real session — if not found, return session_not_found code.
    session = load_builder_session(session_id, ddir)
    if not session:
        codes.append("session_not_found")
        return codes

    # Session must be in an executable state (not completed/intake-only).
    non_executable = {"completed_intake_only"}
    if session.status in non_executable:
        codes.append("session_not_executable")

    # Approval package_id must match session.package_id (auto-check, not caller-dependent).
    approval_pkg = approval.get("package_id", "")
    if approval_pkg and session.package_id and approval_pkg != session.package_id:
        codes.append("approval_package_mismatch")

    # Approval adapter_id must match session.adapter_id.
    approval_adp = approval.get("adapter_id", "")
    if approval_adp and session.adapter_id and approval_adp != session.adapter_id:
        codes.append("approval_adapter_mismatch")

    # Template adapter_kind must match adapter spec kind.
    if session.adapter_id and tmpl:
        spec = get_builder_adapter_spec(session.adapter_id, ddir)
        if spec:
            # spec is dict (get_builder_adapter_spec returns dict | None).
            spec_dict = spec if isinstance(spec, dict) else spec.to_dict()
            tmpl_ak = tmpl.get("adapter_kind", "")
            spec_kind = spec_dict.get("kind", "")
            if tmpl_ak and spec_kind and tmpl_ak != spec_kind:
                codes.append("template_adapter_kind_mismatch")
            if not spec_dict.get("enabled", False):
                codes.append("adapter_disabled")
        elif approval_adp:
            # Adapter specified in approval but not found.
            codes.append("adapter_not_found")

    return codes


def _increment_approval_used_count(session_id: str, ddir: Path) -> None:
    """Atomically increment the used_count on an approval after successful run."""
    p = _global_mbe_dir(ddir) / "approvals" / f"{session_id}.json"
    data = _load_json(p)
    if not data:
        return
    data["used_count"] = int(data.get("used_count", 0)) + 1
    _atomic_write(p, data)


# ---------------------------------------------------------------------------
# Event ledger
# ---------------------------------------------------------------------------


def _append_event(
    execution_id: str, session_id: str, job_id: str,
    kind: str, summary: str, metadata: dict[str, Any] | None = None,
    *, ddir: Path,
) -> ExecutionEvent:
    ev = ExecutionEvent(
        event_id=uuid4().hex[:12],
        execution_id=execution_id,
        session_id=session_id,
        kind=kind,
        timestamp=_now(),
        safe_summary=summary,
        metadata=metadata or {},
    )
    jid = job_id or "_global"
    events_dir = _mbe_dir(jid, ddir) / "events"
    _atomic_write(events_dir / f"{ev.event_id}.json", ev.to_dict())
    # v1.1: structured logging bridge — operators get events via standard Python logging.
    _log.info("mbe_event kind=%s exec=%s session=%s summary=%s",
              kind, execution_id[:8], session_id[:8] if session_id else "-",
              _safe(summary, 100))
    return ev


def list_execution_events(session_id: str = "", job_id: str = "",
                           data_dir: Path | None = None) -> list[dict[str, Any]]:
    ddir = _resolve_ddir(data_dir)
    if job_id:
        all_events = _load_json_dir(_mbe_dir(job_id, ddir) / "events")
    else:
        # Scan all workspaces.
        all_events = []
        ws = ddir / "workspaces"
        if ws.is_dir():
            for child in sorted(ws.iterdir()):
                all_events.extend(_load_json_dir(child / _MBE_DIRNAME / "events"))
    if session_id:
        return [e for e in all_events if e.get("session_id") == session_id]
    return all_events


# ---------------------------------------------------------------------------
# Resolve argv from template + placeholders
# ---------------------------------------------------------------------------


def _resolve_argv(template: dict[str, Any], placeholder_values: dict[str, str]) -> tuple[bool, list[str], str]:
    """Resolve a command template argv with placeholder substitution.

    Returns (ok, resolved_argv, reason). Rejects shell metacharacters, forbidden programs,
    and unknown placeholders."""
    argv_template = template.get("argv_template", [])
    allowed_ph = set(template.get("allowed_placeholders", []))
    resolved: list[str] = []
    for tok in argv_template:
        # Substitute {placeholder} patterns.
        out = tok
        for key in _ALLOWED_PLACEHOLDER_KEYS:
            pattern = "{" + key + "}"
            if pattern in out:
                if key not in allowed_ph:
                    return False, [], f"placeholder '{key}' not in allowed_placeholders"
                val = str(placeholder_values.get(key, ""))
                if not val:
                    return False, [], f"placeholder '{key}' has no value"
                # Validate value: no shell metacharacters.
                for meta in _SHELL_METACHARS:
                    if meta in val:
                        return False, [], f"shell metacharacter in placeholder value '{key}'"
                out = out.replace(pattern, val)
        resolved.append(out)
    # Final safety check on resolved argv.
    if not resolved:
        return False, [], "empty resolved argv"
    prog = os.path.basename(resolved[0])
    if prog in _FORBIDDEN_PROGRAMS:
        return False, [], f"forbidden program: {prog}"
    for i, tok in enumerate(resolved):
        for meta in _SHELL_METACHARS:
            if meta in tok:
                return False, [], f"shell metacharacter in resolved argv[{i}]"
    return True, resolved, "ok"


# ---------------------------------------------------------------------------
# Sanitized env builder
# ---------------------------------------------------------------------------


def _build_sanitized_env(template: dict[str, Any]) -> dict[str, str]:
    """Build a sanitized subprocess environment from current env, filtered to allowed keys only."""
    allowed = set(template.get("sanitized_env_keys", sorted(_ALLOWED_ENV_KEYS)))
    # Never pass forbidden keys regardless of template config.
    allowed -= _FORBIDDEN_ENV_KEYS
    # Only pass keys that are in the global allowed set.
    allowed &= _ALLOWED_ENV_KEYS
    env: dict[str, str] = {}
    for key in sorted(allowed):
        val = os.environ.get(key)
        if val is not None:
            env[key] = val
    return env


def _builder_exec_policy(timeout: int, max_bytes: int, cwd: str | None,
                         env: dict[str, str]) -> ExecGuardPolicy:
    """Stage-1 builder policy (F085 T002a) — only the limits this seam can prove.

    `cpu_seconds`, `address_space_bytes` and `open_files` are deliberately None: a
    value picked without measuring real builder workloads would kill legitimate builds
    (a multi-threaded build burns CPU-seconds far faster than wall-clock), and T2_F085
    makes the per-class rlimit VALUES config with per-project overrides. RLIMIT_AS also
    cannot be classified from what `wait4` reports, so a build it killed would surface
    as a plain failure. What IS enforced is real: the guard's own wall deadline, a
    per-stream output cap applied WHILE reading, the cwd pin, a zero core dump, and
    `FORBIDDEN_ENV_KEYS` as a floor beneath the template's allowlist. `env` is already
    the product of `_build_sanitized_env`, so allowlisting its keys reproduces it.
    """
    return ExecGuardPolicy(
        wall_timeout_seconds=float(timeout),
        output_cap_bytes=max_bytes,
        cwd=cwd,
        env=env,
        env_allowlist=tuple(sorted(env)),
        core_file_bytes=0,
    )


def _guarded_exit_code(guarded) -> int:
    """Translate a guard result into the integer `exit_code` this module publishes.

    `subprocess.run` reported a signal death as -SIGNUM; the guard reports
    `returncode=None` plus the signal NAME, so the negative form is rebuilt here.
    """
    if guarded.returncode is not None:
        return guarded.returncode
    try:
        return -int(signal.Signals[guarded.term_signal].value)
    except (KeyError, ValueError, TypeError):
        return -1


# ---------------------------------------------------------------------------
# Managed runner (the ONLY subprocess execution point for builders)
# ---------------------------------------------------------------------------


def _load_package(package_id: str, job_id: str, ddir: Path) -> dict[str, Any] | None:
    """Load a BuilderRequestPackage by ID. Searches job workspace then global."""
    if job_id:
        p = ddir / "workspaces" / job_id / "main_builder_adapter" / "packages" / f"{package_id}.json"
        d = _load_json(p)
        if d:
            return d
    ws = ddir / "workspaces"
    if ws.is_dir():
        for child in sorted(ws.iterdir()):
            p = child / "main_builder_adapter" / "packages" / f"{package_id}.json"
            d = _load_json(p)
            if d:
                return d
    return None


def run_managed_builder(
    session_id: str, *, template_id: str = "",
    placeholder_values: dict[str, str] | None = None,
    repo_path: str = "", job_id: str = "",
    data_dir: Path | None = None,
) -> ManagedExecutionResult:
    """Run a managed builder execution via bounded subprocess.

    This is the ONLY function that executes a subprocess for builder adapters.
    shell=False ALWAYS. Sanitized env. Hard timeout. Output byte cap.
    Output is UNTRUSTED and stored privately; public surfaces get redacted refs only.

    Returns a ManagedExecutionResult with status, exit code, duration, and output ref.
    The caller is responsible for feeding output into the External Builder Sandbox intake path.
    """
    ddir = _resolve_ddir(data_dir)
    result = ManagedExecutionResult(
        execution_id=uuid4().hex[:16],
        session_id=session_id,
        template_id=template_id,
        job_id=job_id,
        started_at=_now(),
    )
    ph = placeholder_values or {}
    if repo_path:
        ph.setdefault("repo_path", repo_path)

    # 1. Resolve template.
    tmpl = get_command_template(template_id, ddir)
    if not tmpl:
        result.status = ManagedExecutionStatus.BLOCKED
        result.blocking_reasons.append("template_not_found")
        result.next_safe_action = "remedy execution template-list --json"
        result.ended_at = _now()
        _save_execution_result(result, ddir)
        _append_event(result.execution_id, session_id, job_id,
                       ExecutionEventKind.FAILED, "Template not found", ddir=ddir)
        return result

    if not tmpl.get("enabled", False):
        result.status = ManagedExecutionStatus.BLOCKED
        result.blocking_reasons.append("template_disabled")
        result.next_safe_action = f"remedy execution template-show {template_id} --json"
        result.ended_at = _now()
        _save_execution_result(result, ddir)
        _append_event(result.execution_id, session_id, job_id,
                       ExecutionEventKind.FAILED, "Template disabled", ddir=ddir)
        return result

    # 1b. R-0111: require real BuilderSession for managed execution.
    # Also auto-source placeholder values from session + package (Phase 3).
    try:
        from packages.orchestration.main_builder_adapter import load_builder_session
        _session = load_builder_session(session_id, ddir)
        if not _session:
            result.status = ManagedExecutionStatus.BLOCKED
            result.blocking_reasons.append("session_not_found")
            result.next_safe_action = f"remedy builder session-show {session_id} --json"
            result.ended_at = _now()
            _save_execution_result(result, ddir)
            _append_event(result.execution_id, session_id, job_id,
                           ExecutionEventKind.FAILED, "BuilderSession not found", ddir=ddir)
            return result
        # Auto-source placeholder values from session + package.
        ph.setdefault("session_id", _session.session_id)
        if _session.job_id:
            ph.setdefault("job_id", _session.job_id)
            if not job_id:
                job_id = _session.job_id
                result.job_id = job_id
        if _session.repair_id:
            ph.setdefault("repair_id", _session.repair_id)
        if _session.package_id:
            _pkg = _load_package(_session.package_id, _session.job_id, ddir)
            if _pkg:
                ph.setdefault("goal_summary", _safe(str(_pkg.get("goal_summary", "")), 200))
                ph.setdefault("task_type", str(_pkg.get("task_type", "")))
    except ImportError:
        pass  # graceful degradation if module unavailable

    # 2. Check approval (v1.1: full validation with 11 codes).
    if tmpl.get("requires_approval", True):
        validation_codes = validate_execution_approval(
            session_id, template_id,
            package_id=ph.get("package_id", ""),
            adapter_id=ph.get("adapter_id", ""),
            data_dir=ddir,
        )
        if validation_codes:
            # Map specific codes to specific event kinds.
            if "approval_not_found" in validation_codes:
                result.status = ManagedExecutionStatus.APPROVAL_REQUIRED
                result.blocking_reasons.append("approval_required")
                ev_kind = ExecutionEventKind.REQUESTED
            elif "approval_expired" in validation_codes:
                result.status = ManagedExecutionStatus.BLOCKED
                result.blocking_reasons.extend(validation_codes)
                ev_kind = ExecutionEventKind.APPROVAL_EXPIRED
            elif "approval_exhausted" in validation_codes or "scope_violation" in validation_codes:
                result.status = ManagedExecutionStatus.BLOCKED
                result.blocking_reasons.extend(validation_codes)
                ev_kind = ExecutionEventKind.APPROVAL_EXHAUSTED
            elif any(c.endswith("_mismatch") for c in validation_codes):
                result.status = ManagedExecutionStatus.BLOCKED
                result.blocking_reasons.extend(validation_codes)
                ev_kind = ExecutionEventKind.BINDING_MISMATCH
            else:
                result.status = ManagedExecutionStatus.BLOCKED
                result.blocking_reasons.extend(validation_codes)
                ev_kind = ExecutionEventKind.FAILED

            result.next_safe_action = f"remedy execution approve {session_id} --template {template_id} --json"
            result.ended_at = _now()
            _save_execution_result(result, ddir)
            _append_event(result.execution_id, session_id, job_id,
                           ev_kind,
                           f"Approval validation failed: {', '.join(validation_codes)}",
                           {"validation_codes": ", ".join(validation_codes)},
                           ddir=ddir)
            return result

        # Approval valid — emit validated event.
        _append_event(result.execution_id, session_id, job_id,
                       ExecutionEventKind.APPROVAL_VALIDATED,
                       "Approval passed all validation checks", ddir=ddir)

        # Apply approval caps (tighter-wins).
        approval_data = get_execution_approval(session_id, ddir)
        if approval_data:
            approval_runtime = int(approval_data.get("max_runtime_seconds", MAX_TIMEOUT_SECONDS))
            approval_output = int(approval_data.get("max_output_bytes", MAX_OUTPUT_BYTES))
            tmpl_timeout = tmpl.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS)
            tmpl_output = tmpl.get("max_output_bytes", MAX_OUTPUT_BYTES)
            if 0 < approval_runtime < tmpl_timeout:
                tmpl["timeout_seconds"] = approval_runtime
                _append_event(result.execution_id, session_id, job_id,
                               ExecutionEventKind.RUNTIME_CAP_APPLIED,
                               f"Approval runtime cap {approval_runtime}s applied",
                               ddir=ddir)
            if 0 < approval_output < tmpl_output:
                tmpl["max_output_bytes"] = approval_output
                _append_event(result.execution_id, session_id, job_id,
                               ExecutionEventKind.OUTPUT_CAP_APPLIED,
                               f"Approval output cap {approval_output}B applied",
                               ddir=ddir)

    # 3. Resolve argv.
    ok, argv, reason = _resolve_argv(tmpl, ph)
    if not ok:
        result.status = ManagedExecutionStatus.BLOCKED
        result.blocking_reasons.append(f"argv_resolution_failed: {reason}")
        result.next_safe_action = f"remedy execution show {result.execution_id} --json"
        result.ended_at = _now()
        _save_execution_result(result, ddir)
        _append_event(result.execution_id, session_id, job_id,
                       ExecutionEventKind.FAILED, f"Argv resolution failed: {reason}", ddir=ddir)
        return result

    # 4. Build sanitized env.
    env = _build_sanitized_env(tmpl)

    timeout = min(tmpl.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS), MAX_TIMEOUT_SECONDS)
    max_bytes = min(tmpl.get("max_output_bytes", MAX_OUTPUT_BYTES), MAX_OUTPUT_BYTES)

    # 4b. Consume approval BEFORE subprocess start (R-0108).
    # Counts allowed starts, not successful exits. Failed/timeout runs still consume.
    if tmpl.get("requires_approval", True):
        _increment_approval_used_count(session_id, ddir)
        _append_event(result.execution_id, session_id, job_id,
                       ExecutionEventKind.APPROVAL_CONSUMED,
                       "Approval used_count incremented before execution", ddir=ddir)

    # 5. Record start event.
    _append_event(result.execution_id, session_id, job_id,
                   ExecutionEventKind.STARTED,
                   f"Subprocess started: {_safe(argv[0], 50)}", ddir=ddir)
    result.status = ManagedExecutionStatus.RUNNING

    # 6. Execute subprocess — through the F085 exec guard; argv list, never a shell.
    start_time = time.monotonic()
    try:
        guarded = run_guarded(argv, _builder_exec_policy(timeout, max_bytes,
                                                         repo_path or None, env))
        if guarded.tripped_limit == "wall_timeout":
            # The guard CLASSIFIES a wall trip where subprocess.run RAISED one. Re-raise
            # so the timeout path below stays the one this module already had: the
            # migration changes the mechanism, never the observable outcome.
            raise subprocess.TimeoutExpired(argv, timeout)
        # A CompletedProcess keeps every downstream reader — returncode, stdout, stderr
        # — identical to the pre-migration shape; the slice below is then a no-op,
        # because the guard capped each stream WHILE reading it.
        proc = subprocess.CompletedProcess(argv, _guarded_exit_code(guarded),
                                           guarded.stdout, guarded.stderr)
        elapsed_ms = int((time.monotonic() - start_time) * 1000)
        result.duration_ms = elapsed_ms
        result.exit_code = proc.returncode

        # Cap output.
        stdout = proc.stdout[:max_bytes] if proc.stdout else b""
        stderr = proc.stderr[:max_bytes] if proc.stderr else b""

        # Store raw output privately.
        output_path = _save_raw_output(result.execution_id, job_id, stdout, stderr, ddir)
        result.output_ref = _safe_path_label(str(output_path))

        # R-0115: emit output_ref_created event for dogfood replay provenance.
        _append_event(result.execution_id, session_id, job_id,
                       ExecutionEventKind.OUTPUT_REF_CREATED,
                       f"Raw output stored privately: {result.output_ref}",
                       ddir=ddir)

        # Safe summary (first 200 chars of stdout, scrubbed).
        try:
            summary_text = stdout[:200].decode("utf-8", errors="replace")
        except Exception:
            summary_text = "(binary output)"
        result.safe_summary = _safe(summary_text, 300)

        if proc.returncode == 0:
            result.status = ManagedExecutionStatus.COMPLETED
            result.next_safe_action = f"remedy builder session-record-output {session_id} --artifact-ref {result.output_ref} --json"
        else:
            result.status = ManagedExecutionStatus.FAILED
            result.safe_summary = _safe(f"Exit code {proc.returncode}: {summary_text}", 300)
            result.next_safe_action = f"remedy execution show {result.execution_id} --json"

        _append_event(result.execution_id, session_id, job_id,
                       ExecutionEventKind.COMPLETED,
                       f"Exit code {proc.returncode}, {elapsed_ms}ms",
                       {"exit_code": str(proc.returncode), "duration_ms": str(elapsed_ms)},
                       ddir=ddir)

    except subprocess.TimeoutExpired:
        elapsed_ms = int((time.monotonic() - start_time) * 1000)
        result.duration_ms = elapsed_ms
        result.status = ManagedExecutionStatus.TIMEOUT
        result.safe_summary = f"Timeout after {timeout}s"
        result.next_safe_action = f"remedy execution show {result.execution_id} --json"
        _append_event(result.execution_id, session_id, job_id,
                       ExecutionEventKind.TIMEOUT,
                       f"Timeout after {timeout}s", ddir=ddir)

    except FileNotFoundError:
        result.status = ManagedExecutionStatus.FAILED
        result.blocking_reasons.append("command_not_found")
        result.safe_summary = f"Command not found: {_safe(argv[0], 50)}"
        result.next_safe_action = f"remedy execution template-show {template_id} --json"
        _append_event(result.execution_id, session_id, job_id,
                       ExecutionEventKind.FAILED,
                       f"Command not found: {_safe(argv[0], 50)}", ddir=ddir)

    except OSError as exc:
        result.status = ManagedExecutionStatus.FAILED
        result.blocking_reasons.append("os_error")
        result.safe_summary = _safe(str(exc), 200)
        result.next_safe_action = f"remedy execution show {result.execution_id} --json"
        _append_event(result.execution_id, session_id, job_id,
                       ExecutionEventKind.FAILED,
                       _safe(str(exc), 200), ddir=ddir)

    result.ended_at = _now()
    _save_execution_result(result, ddir)
    return result


# ---------------------------------------------------------------------------
# Raw output storage (private, 0o600)
# ---------------------------------------------------------------------------


def _save_raw_output(
    execution_id: str, job_id: str,
    stdout: bytes, stderr: bytes, ddir: Path,
) -> Path:
    """Store raw subprocess output in a private file. Never public."""
    jid = job_id or "_global"
    out_dir = _mbe_dir(jid, ddir) / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    os.chmod(out_dir, 0o700)
    out_path = out_dir / f"{execution_id}.raw"
    content = b"--- stdout ---\n" + stdout + b"\n--- stderr ---\n" + stderr
    out_path.write_bytes(content)
    os.chmod(out_path, 0o600)
    return out_path


# ---------------------------------------------------------------------------
# Execution result storage
# ---------------------------------------------------------------------------


def _save_execution_result(result: ManagedExecutionResult, ddir: Path) -> None:
    jid = result.job_id or "_global"
    _atomic_write(
        _mbe_dir(jid, ddir) / "results" / f"{result.execution_id}.json",
        result.to_dict(),
    )


def get_execution_result(execution_id: str, data_dir: Path | None = None) -> dict[str, Any] | None:
    ddir = _resolve_ddir(data_dir)
    # Search across workspaces.
    ws = ddir / "workspaces"
    if ws.is_dir():
        for child in sorted(ws.iterdir()):
            d = _load_json(child / _MBE_DIRNAME / "results" / f"{execution_id}.json")
            if d:
                return d
    return _load_json(_mbe_dir("_global", ddir) / "results" / f"{execution_id}.json")


def list_execution_results(job_id: str = "", data_dir: Path | None = None) -> list[dict[str, Any]]:
    ddir = _resolve_ddir(data_dir)
    if job_id:
        return _load_json_dir(_mbe_dir(job_id, ddir) / "results")
    out: list[dict] = []
    ws = ddir / "workspaces"
    if ws.is_dir():
        for child in sorted(ws.iterdir()):
            out.extend(_load_json_dir(child / _MBE_DIRNAME / "results"))
    return out


# ---------------------------------------------------------------------------
# Dogfood debug bundle
# ---------------------------------------------------------------------------


def build_debug_bundle(execution_id: str, data_dir: Path | None = None) -> dict[str, Any] | None:
    """Build a structured debug bundle for a managed execution. Private (operator-only)."""
    ddir = _resolve_ddir(data_dir)
    result = get_execution_result(execution_id, ddir)
    if not result:
        return None

    session_id = result.get("session_id", "")
    events = list_execution_events(session_id=session_id, data_dir=ddir)

    # Filter events for this execution only.
    exec_events = [e for e in events if e.get("execution_id") == execution_id]

    tmpl = get_command_template(result.get("template_id", ""), ddir)
    approval = get_execution_approval(session_id, ddir) if session_id else None

    # v1.1: approval validation summary.
    approval_validation: dict[str, Any] = {"valid": False, "codes": []}
    if approval:
        tid = result.get("template_id", "")
        codes = validate_execution_approval(session_id, tid, data_dir=ddir)
        approval_validation = {
            "valid": len(codes) == 0,
            "codes": codes,
            "scope": approval.get("approval_scope", ""),
            "max_runs": approval.get("max_runs", 0),
            "used_count": approval.get("used_count", 0),
            "expires_at": approval.get("expires_at", ""),
            "adapter_kind": approval.get("adapter_kind", ""),
            "package_id": approval.get("package_id", ""),
            "adapter_id": approval.get("adapter_id", ""),
        }

    # v1.1: repair suggestion when blocked by approval issues.
    repair_suggestion = ""
    blocking = result.get("blocking_reasons", [])
    if "approval_required" in blocking or "approval_not_found" in [c for c in approval_validation.get("codes", [])]:
        repair_suggestion = f"remedy execution approve {session_id} --template {result.get('template_id', '')} --json"
    elif "approval_expired" in blocking:
        repair_suggestion = f"Re-approve with new expiry: remedy execution approve {session_id} --template {result.get('template_id', '')} --json"
    elif "approval_exhausted" in blocking:
        repair_suggestion = f"Re-approve with higher max_runs: remedy execution approve {session_id} --template {result.get('template_id', '')} --max-runs N --json"

    # R-0110/R-0111: binding summary — session/package/adapter/template matching.
    session_exists = False
    try:
        from packages.orchestration.main_builder_adapter import load_builder_session
        session_exists = load_builder_session(session_id, ddir) is not None
    except ImportError:
        pass
    binding_summary: dict[str, Any] = {
        "session_exists": session_exists,
        "session_id_match": True,
        "template_id_match": True,
    }
    if approval:
        binding_summary["package_id"] = approval.get("package_id", "")
        binding_summary["adapter_id"] = approval.get("adapter_id", "")
        binding_summary["adapter_kind"] = approval.get("adapter_kind", "")
        if tmpl:
            binding_summary["template_adapter_kind"] = tmpl.get("adapter_kind", "")
            binding_summary["adapter_kind_match"] = (
                not approval.get("adapter_kind", "") or
                not tmpl.get("adapter_kind", "") or
                approval.get("adapter_kind", "") == tmpl.get("adapter_kind", "")
            )

    # R-0110/R-0115: event sequence summary.
    event_kinds_present = [e.get("kind", "") for e in exec_events]
    has_output_ref = bool(result.get("output_ref", ""))
    has_output_ref_event = ExecutionEventKind.OUTPUT_REF_CREATED in event_kinds_present

    return {
        "execution_id": execution_id,
        "session_id": session_id,
        "template_id": result.get("template_id", ""),
        "template_label": _safe(tmpl.get("label", ""), 100) if tmpl else "",
        "status": result.get("status", ""),
        "exit_code": result.get("exit_code"),
        "duration_ms": result.get("duration_ms", 0),
        "started_at": result.get("started_at", ""),
        "ended_at": result.get("ended_at", ""),
        "output_ref": result.get("output_ref", ""),
        "output_ref_present": has_output_ref,
        "output_ref_event_present": has_output_ref_event,
        "safe_summary": result.get("safe_summary", ""),
        "blocking_reasons": blocking,
        "next_safe_action": result.get("next_safe_action", ""),
        "approval": {
            "approved": bool(approval),
            "operator_id": _safe(approval.get("operator_id", ""), 100) if approval else "",
            "approved_at": approval.get("approved_at", "") if approval else "",
            "scope": approval.get("approval_scope", "") if approval else "",
            "max_runs": approval.get("max_runs", 0) if approval else 0,
            "used_count": approval.get("used_count", 0) if approval else 0,
            "expires_at": approval.get("expires_at", "") if approval else "",
        },
        "approval_validation": approval_validation,
        "binding_summary": binding_summary,
        "repair_suggestion": repair_suggestion,
        "event_sequence": event_kinds_present,
        "event_timeline": [
            {
                "kind": e.get("kind", ""),
                "timestamp": e.get("timestamp", ""),
                "safe_summary": e.get("safe_summary", ""),
            }
            for e in exec_events[:50]
        ],
        "schema_version": SCHEMA_VERSION,
    }


# ---------------------------------------------------------------------------
# Mission signal integration
# ---------------------------------------------------------------------------


def managed_execution_mission_signal(
    job_id: str, data_dir: Path | None = None,
) -> dict[str, Any]:
    """Safe summary of managed execution state for Mission Contract consumption."""
    ddir = _resolve_ddir(data_dir)
    results = list_execution_results(job_id, ddir)
    running = sum(1 for r in results if r.get("status") == ManagedExecutionStatus.RUNNING)
    completed = sum(1 for r in results if r.get("status") == ManagedExecutionStatus.COMPLETED)
    failed = sum(1 for r in results if r.get("status") == ManagedExecutionStatus.FAILED)
    timeout = sum(1 for r in results if r.get("status") == ManagedExecutionStatus.TIMEOUT)
    blocked = sum(1 for r in results if r.get("status") in (
        ManagedExecutionStatus.BLOCKED, ManagedExecutionStatus.APPROVAL_REQUIRED))
    return {
        "total_executions": len(results),
        "running_count": running,
        "completed_count": completed,
        "failed_count": failed,
        "timeout_count": timeout,
        "blocked_count": blocked,
        "has_active_executions": running > 0,
        "user_decision_required": blocked > 0,
        "execution_satisfies_mission": False,  # NEVER — downstream gates required
    }


# ---------------------------------------------------------------------------
# Integrity
# ---------------------------------------------------------------------------


def audit_template_safety(tmpl: dict[str, Any]) -> list[dict[str, str]]:
    """Flag unsafe command template configurations."""
    out: list[dict[str, str]] = []
    tid = tmpl.get("template_id", "")
    blob = json.dumps(tmpl).lower()
    # Shell metacharacters in argv.
    for tok in tmpl.get("argv_template", []):
        for meta in _SHELL_METACHARS:
            if meta in str(tok):
                out.append({"template_id": tid, "code": "shell_metachar_in_template"})
                break
        else:
            continue
        break
    # Forbidden programs.
    argv = tmpl.get("argv_template", [])
    if argv:
        prog = os.path.basename(str(argv[0]).strip("{}"))
        if prog in _FORBIDDEN_PROGRAMS:
            out.append({"template_id": tid, "code": "forbidden_program_in_template"})
    # Secrets/raw markers.
    if any(m.lower() in blob for m in _RAW_MARKERS):
        out.append({"template_id": tid, "code": "secret_or_raw_in_template"})
    # Absolute paths.
    if "/home/" in blob or "/users/" in blob or "/root/" in blob:
        out.append({"template_id": tid, "code": "absolute_path_in_template"})
    # Forbidden env keys.
    for key in tmpl.get("sanitized_env_keys", []):
        if key in _FORBIDDEN_ENV_KEYS:
            out.append({"template_id": tid, "code": "forbidden_env_key_in_template"})
            break
    # Timeout too high.
    if tmpl.get("timeout_seconds", 0) > MAX_TIMEOUT_SECONDS:
        out.append({"template_id": tid, "code": "timeout_exceeds_max"})
    return out


def audit_execution_result_safety(
    result: dict[str, Any],
    events: list[dict[str, Any]] | None = None,
) -> list[dict[str, str]]:
    """Flag unsafe execution result states (R-0110 hardened)."""
    out: list[dict[str, str]] = []
    eid = result.get("execution_id", "")
    blob = json.dumps(result).lower()
    # Secrets/raw markers in public fields.
    if any(m.lower() in blob for m in _RAW_MARKERS):
        out.append({"execution_id": eid, "code": "raw_or_secret_in_result"})
    # Absolute paths.
    if "/home/" in blob or "/users/" in blob or "/root/" in blob:
        out.append({"execution_id": eid, "code": "absolute_path_in_result"})
    # Unknown status.
    if result.get("status", "") not in _ALL_EXECUTION_STATUSES:
        out.append({"execution_id": eid, "code": "unknown_execution_status"})

    # R-0110: completed run must have output_ref.
    status = result.get("status", "")
    if status == ManagedExecutionStatus.COMPLETED and not result.get("output_ref", ""):
        out.append({"execution_id": eid, "code": "completed_missing_output_ref"})

    # R-0110: event sequence checks (if events provided).
    if events is not None:
        exec_events = [e for e in events if e.get("execution_id") == eid]
        kinds = [e.get("kind", "") for e in exec_events]
        if status == ManagedExecutionStatus.COMPLETED:
            if ExecutionEventKind.STARTED not in kinds:
                out.append({"execution_id": eid, "code": "completed_missing_started_event"})
            if ExecutionEventKind.COMPLETED not in kinds:
                out.append({"execution_id": eid, "code": "completed_missing_completed_event"})
            if ExecutionEventKind.OUTPUT_REF_CREATED not in kinds:
                out.append({"execution_id": eid, "code": "completed_missing_output_ref_event"})

    # R-0110: result must not claim repair/mission done.
    summary_lower = result.get("safe_summary", "").lower()
    for forbidden in ["repair_done", "mission_done", "repair_complete", "mission_complete"]:
        if forbidden in summary_lower:
            out.append({"execution_id": eid, "code": "result_claims_repair_or_mission_done"})
            break

    return out


def audit_approval_safety(approval: dict[str, Any], templates: list[dict[str, Any]] | None = None) -> list[dict[str, str]]:
    """Flag unsafe or invalid approval configurations (v1.1)."""
    out: list[dict[str, str]] = []
    aid = approval.get("approval_id", "")

    # Scope validity.
    scope = approval.get("approval_scope", "")
    if scope and scope not in _ALL_APPROVAL_SCOPES:
        out.append({"approval_id": aid, "code": "unknown_approval_scope"})

    # Exhaustion check.
    max_runs = int(approval.get("max_runs", 0))
    used_count = int(approval.get("used_count", 0))
    if max_runs > 0 and used_count > max_runs:
        out.append({"approval_id": aid, "code": "used_count_exceeds_max_runs"})

    # Expiry check — missing expiry is a violation.
    expires_at = approval.get("expires_at", "")
    if not expires_at:
        out.append({"approval_id": aid, "code": "missing_expires_at"})
    else:
        try:
            exp_dt = datetime.fromisoformat(expires_at)
            if datetime.now(timezone.utc) > exp_dt:
                out.append({"approval_id": aid, "code": "approval_currently_expired"})
        except (ValueError, TypeError):
            out.append({"approval_id": aid, "code": "invalid_expires_at_format"})

    # Adapter kind mismatch with template.
    if templates:
        tid = approval.get("template_id", "")
        ak = approval.get("adapter_kind", "")
        if tid and ak:
            for t in templates:
                if t.get("template_id") == tid:
                    tmpl_ak = t.get("adapter_kind", "")
                    if tmpl_ak and ak != tmpl_ak:
                        out.append({"approval_id": aid, "code": "adapter_kind_mismatch_with_template"})
                    break

    # Runtime/output cap validity.
    rt = int(approval.get("max_runtime_seconds", 0))
    if rt > MAX_TIMEOUT_SECONDS:
        out.append({"approval_id": aid, "code": "approval_runtime_exceeds_system_max"})
    ob = int(approval.get("max_output_bytes", 0))
    if ob > MAX_OUTPUT_BYTES:
        out.append({"approval_id": aid, "code": "approval_output_exceeds_system_max"})

    # Single-run scope with max_runs != 1.
    if scope == ApprovalScope.SINGLE_RUN and max_runs != 1 and max_runs != 0:
        out.append({"approval_id": aid, "code": "single_run_scope_max_runs_mismatch"})

    # Secrets in approval fields.
    blob = json.dumps(approval).lower()
    if any(m.lower() in blob for m in _RAW_MARKERS):
        out.append({"approval_id": aid, "code": "secret_or_raw_in_approval"})

    return out


def managed_execution_integrity(data_dir: Path | None = None) -> dict[str, Any]:
    """Read-only invariant check over templates + approvals + execution results (v1.1)."""
    ddir = _resolve_ddir(data_dir)
    violations: list[dict] = []
    templates = list_command_templates(ddir)
    for t in templates:
        violations.extend(audit_template_safety(t))
    approvals = list_execution_approvals(ddir)
    for a in approvals:
        violations.extend(audit_approval_safety(a, templates))
    results = list_execution_results(data_dir=ddir)
    # R-0110: load all events for event sequence checks.
    all_events = list_execution_events(data_dir=ddir)
    for r in results:
        violations.extend(audit_execution_result_safety(r, events=all_events))
    return {
        "version": 2,
        "template_count": len(templates),
        "approval_count": len(approvals),
        "execution_count": len(results),
        "violation_count": len(violations),
        "passed": not violations,
        "violations": violations[:50],
    }


# ---------------------------------------------------------------------------
# Public exports
# ---------------------------------------------------------------------------


__all__ = [
    "SCHEMA_VERSION",
    "ApprovalScope",
    "CommandTemplate", "ExecutionApproval", "ExecutionEvent", "ExecutionEventKind",
    "ManagedExecutionResult", "ManagedExecutionStatus",
    "default_command_templates", "save_command_template",
    "list_command_templates", "get_command_template",
    "enable_command_template", "disable_command_template",
    "update_command_template",
    "approve_managed_execution", "get_execution_approval",
    "list_execution_approvals", "validate_execution_approval",
    "run_managed_builder",
    "list_execution_events", "get_execution_result", "list_execution_results",
    "build_debug_bundle",
    "managed_execution_mission_signal",
    "audit_template_safety", "audit_execution_result_safety",
    "audit_approval_safety",
    "managed_execution_integrity",
]
