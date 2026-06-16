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

import hashlib
import json
import os
import re
import subprocess
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from packages.orchestration.provider_trust import _safe_path_label, _scrub_public


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


@dataclass
class ExecutionApproval:
    approval_id: str = ""
    session_id: str = ""
    template_id: str = ""
    operator_id: str = ""
    approved_at: str = ""
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "approval_id": self.approval_id,
            "session_id": self.session_id,
            "template_id": self.template_id,
            "operator_id": _safe(self.operator_id, 100),
            "approved_at": self.approved_at,
            "notes": _safe(self.notes),
            "schema_version": SCHEMA_VERSION,
        }


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


_ALL_EVENT_KINDS = frozenset({
    ExecutionEventKind.REQUESTED, ExecutionEventKind.APPROVED,
    ExecutionEventKind.STARTED, ExecutionEventKind.COMPLETED,
    ExecutionEventKind.FAILED, ExecutionEventKind.TIMEOUT,
    ExecutionEventKind.INTAKE_STARTED, ExecutionEventKind.INTAKE_COMPLETED,
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


# ---------------------------------------------------------------------------
# Operator approval gate
# ---------------------------------------------------------------------------


def approve_managed_execution(
    session_id: str, template_id: str, *, operator_id: str = "",
    data_dir: Path | None = None,
) -> ExecutionApproval | None:
    """Record operator approval for a managed execution. No auto-approval."""
    ddir = _resolve_ddir(data_dir)
    tmpl = get_command_template(template_id, ddir)
    if not tmpl:
        return None
    if not tmpl.get("enabled", False):
        return None
    approval = ExecutionApproval(
        approval_id=uuid4().hex[:16],
        session_id=session_id,
        template_id=template_id,
        operator_id=operator_id or "operator",
        approved_at=_now(),
    )
    _atomic_write(
        _global_mbe_dir(ddir) / "approvals" / f"{session_id}.json",
        approval.to_dict(),
    )
    return approval


def get_execution_approval(session_id: str, data_dir: Path | None = None) -> dict[str, Any] | None:
    ddir = _resolve_ddir(data_dir)
    return _load_json(_global_mbe_dir(ddir) / "approvals" / f"{session_id}.json")


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


# ---------------------------------------------------------------------------
# Managed runner (the ONLY subprocess execution point for builders)
# ---------------------------------------------------------------------------


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

    # 2. Check approval.
    if tmpl.get("requires_approval", True):
        approval = get_execution_approval(session_id, ddir)
        if not approval or approval.get("template_id") != template_id:
            result.status = ManagedExecutionStatus.APPROVAL_REQUIRED
            result.blocking_reasons.append("approval_required")
            result.next_safe_action = f"remedy execution approve {session_id} --template {template_id} --json"
            result.ended_at = _now()
            _save_execution_result(result, ddir)
            _append_event(result.execution_id, session_id, job_id,
                           ExecutionEventKind.REQUESTED,
                           "Execution requested; approval required", ddir=ddir)
            return result

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

    # 5. Record start event.
    _append_event(result.execution_id, session_id, job_id,
                   ExecutionEventKind.STARTED,
                   f"Subprocess started: {_safe(argv[0], 50)}", ddir=ddir)
    result.status = ManagedExecutionStatus.RUNNING

    # 6. Execute subprocess — shell=False ALWAYS.
    start_time = time.monotonic()
    try:
        proc = subprocess.run(
            argv,
            shell=False,  # HARD: never True
            capture_output=True,
            timeout=timeout,
            env=env,
            cwd=repo_path or None,
        )
        elapsed_ms = int((time.monotonic() - start_time) * 1000)
        result.duration_ms = elapsed_ms
        result.exit_code = proc.returncode

        # Cap output.
        stdout = proc.stdout[:max_bytes] if proc.stdout else b""
        stderr = proc.stderr[:max_bytes] if proc.stderr else b""

        # Store raw output privately.
        output_path = _save_raw_output(result.execution_id, job_id, stdout, stderr, ddir)
        result.output_ref = _safe_path_label(str(output_path))

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
        "safe_summary": result.get("safe_summary", ""),
        "blocking_reasons": result.get("blocking_reasons", []),
        "approval": {
            "approved": bool(approval),
            "operator_id": _safe(approval.get("operator_id", ""), 100) if approval else "",
            "approved_at": approval.get("approved_at", "") if approval else "",
        },
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


def audit_execution_result_safety(result: dict[str, Any]) -> list[dict[str, str]]:
    """Flag unsafe execution result states."""
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
    return out


def managed_execution_integrity(data_dir: Path | None = None) -> dict[str, Any]:
    """Read-only invariant check over templates + execution results."""
    ddir = _resolve_ddir(data_dir)
    violations: list[dict] = []
    templates = list_command_templates(ddir)
    for t in templates:
        violations.extend(audit_template_safety(t))
    results = list_execution_results(data_dir=ddir)
    for r in results:
        violations.extend(audit_execution_result_safety(r))
    return {
        "version": 1,
        "template_count": len(templates),
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
    "CommandTemplate", "ExecutionApproval", "ExecutionEvent", "ExecutionEventKind",
    "ManagedExecutionResult", "ManagedExecutionStatus",
    "default_command_templates", "save_command_template",
    "list_command_templates", "get_command_template",
    "approve_managed_execution", "get_execution_approval",
    "run_managed_builder",
    "list_execution_events", "get_execution_result", "list_execution_results",
    "build_debug_bundle",
    "managed_execution_mission_signal",
    "audit_template_safety", "audit_execution_result_safety",
    "managed_execution_integrity",
]
