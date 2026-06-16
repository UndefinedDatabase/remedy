"""
Main Builder Adapter v0 + Token-Controlled External Session Rail (Steps 1961-2025).

A controlled external builder session rail for Remedy. Adapter types (Claude Code / Pi.dev /
OpenCode / generic CLI / fixture) are configurable but disabled by default. Request packages are
token-aware and minimal. Builder output is UNTRUSTED until External Builder Sandbox intake, trust/
quality checks, review, apply proof, and re-test gates pass.

  Workers execute. Remedy governs. No provider monopoly. Token reduction is first-class.

This module is METADATA + POLICY + EVALUATION + REPORTING only. It NEVER calls a provider/model/
Ollama/cloud/local service, the network, a browser, a subprocess, or a shell; it never executes
a builder, generates a candidate, applies/approves/tests anything, or writes to the repository.

Hard rules enforced here:
  - NO provider/model/Ollama/cloud/local execution, network, browser, subprocess, shell.
  - NO candidate generation, apply/approve/test/git/PR, MemPalace, secrets storage.
  - NO direct repo write in v0 (allows_direct_repo_write always False).
  - All real adapters disabled by default; fixture adapter only in explicit fixture/test mode.
  - Builder output always untrusted: candidate goes through External Builder Sandbox intake.
  - Session completion does not satisfy repair/mission (downstream gates required).
  - No secrets/API keys/raw prompts/raw transcripts/raw candidates/absolute private paths in any
    public export.
  - No hardcoded provider monopoly.

Public API::

    # Adapter registry
    default_builder_adapter_specs() -> list[BuilderAdapterSpec]
    list_builder_adapter_specs(data_dir=None) -> list[dict]
    get_builder_adapter_spec(adapter_id, data_dir=None) -> dict | None
    save_builder_adapter_spec(spec, data_dir=None) -> bool
    builder_adapter_integrity(data_dir=None) -> dict

    # Request packages
    build_builder_request_package(job_id, *, repair_id, adapter_id, context_pack, ...) -> BuilderRequestPackage

    # Session lifecycle
    create_builder_session(package_id, adapter_id, ...) -> BuilderSessionRecord
    mark_builder_session_waiting_for_operator(session_id, ...) -> BuilderSessionRecord | None
    record_builder_session_started(session_id, ...) -> BuilderSessionRecord | None
    record_builder_session_output(session_id, *, transcript_ref, candidate_artifact_ref, ...) -> BuilderSessionRecord | None
    record_builder_session_blocked(session_id, *, reason, ...) -> BuilderSessionRecord | None
    record_builder_session_intake_complete(session_id, *, sandbox_submission_id, ...) -> BuilderSessionRecord | None
    load_builder_session(session_id, ...) -> BuilderSessionRecord | None
    list_builder_sessions(job_id, ...) -> list[dict]

    # Fixture builder
    run_fixture_builder(session_id, *, fixture_scenario, ...) -> BuilderSessionRecord | None

    # Integration helpers
    builder_adapter_mission_signal(job_id, ...) -> dict
    recommend_builder_adapter(job_id, *, repair_id, ...) -> dict
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from packages.orchestration.provider_trust import _safe_path_label, _scrub_public

# ---------------------------------------------------------------------------
# Constants / vocabularies
# ---------------------------------------------------------------------------

SCHEMA_VERSION = "main-builder-adapter-v0"
_MBA_DIRNAME = "main_builder_adapter"

_RAW_MARKERS = ("diff --git", "-----BEGIN", "Traceback (most recent call last)", "sk-",
                "api_key", "apikey", "password", "secret_key")


class BuilderAdapterKind:
    CLAUDE_CODE = "claude_code"
    PI_DEV = "pi_dev"
    OPENCODE = "opencode"
    GENERIC_EXTERNAL_CLI_BUILDER = "generic_external_cli_builder"
    FIXTURE_BUILDER = "fixture_builder"
    UNKNOWN = "unknown"


_ALL_KINDS = frozenset({
    BuilderAdapterKind.CLAUDE_CODE, BuilderAdapterKind.PI_DEV,
    BuilderAdapterKind.OPENCODE, BuilderAdapterKind.GENERIC_EXTERNAL_CLI_BUILDER,
    BuilderAdapterKind.FIXTURE_BUILDER, BuilderAdapterKind.UNKNOWN,
})

_REAL_ADAPTER_KINDS = frozenset({
    BuilderAdapterKind.CLAUDE_CODE, BuilderAdapterKind.PI_DEV,
    BuilderAdapterKind.OPENCODE, BuilderAdapterKind.GENERIC_EXTERNAL_CLI_BUILDER,
})


class BuilderAdapterMode:
    DISABLED = "disabled"
    PACKAGE_ONLY = "package_only"
    OPERATOR_LAUNCHED = "operator_launched"
    CONTROLLED_SESSION = "controlled_session"
    FIXTURE_ONLY = "fixture_only"


_ALL_MODES = frozenset({
    BuilderAdapterMode.DISABLED, BuilderAdapterMode.PACKAGE_ONLY,
    BuilderAdapterMode.OPERATOR_LAUNCHED, BuilderAdapterMode.CONTROLLED_SESSION,
    BuilderAdapterMode.FIXTURE_ONLY,
})


class BuilderSessionStatus:
    NOT_STARTED = "not_started"
    PACKAGE_READY = "package_ready"
    WAITING_FOR_OPERATOR = "waiting_for_operator"
    RUNNING = "running"
    CANDIDATE_RECEIVED = "candidate_received"
    NEEDS_REVIEW = "needs_review"
    BLOCKED = "blocked"
    COMPLETED_INTAKE_ONLY = "completed_intake_only"


_ALL_SESSION_STATUSES = frozenset({
    BuilderSessionStatus.NOT_STARTED, BuilderSessionStatus.PACKAGE_READY,
    BuilderSessionStatus.WAITING_FOR_OPERATOR, BuilderSessionStatus.RUNNING,
    BuilderSessionStatus.CANDIDATE_RECEIVED, BuilderSessionStatus.NEEDS_REVIEW,
    BuilderSessionStatus.BLOCKED, BuilderSessionStatus.COMPLETED_INTAKE_ONLY,
})

_EXPECTED_OUTPUT_CONTRACT = (
    "Return EXACTLY ONE candidate as JSON or a single fenced unified diff. "
    "Repository-relative paths only. No secrets/tokens/.env values. No protected/generated/lock "
    "files. Do NOT claim the change was applied/tested/verified/merged. Include a summary of "
    "changes, touched files, risks, and suggested test commands. Output is UNTRUSTED: it will be "
    "quarantined, trust-checked, quality-evaluated, reviewed, and may be rejected; it is NEVER "
    "applied automatically."
)

_FORBIDDEN_ACTIONS = [
    "no_direct_apply", "no_direct_repo_write", "no_completion_claim",
    "no_secrets_in_output", "no_absolute_paths", "no_raw_logs",
    "no_protected_paths", "single_candidate_only",
]


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


_SK_PATTERN = re.compile(r"\bsk-[A-Za-z0-9_-]{6,}\b")


def _safe(text: str, limit: int = 300) -> str:
    """Truncate + scrub a string for public surfaces."""
    t = str(text or "")[:limit]
    t = _scrub_public(t)
    t = _SK_PATTERN.sub("[redacted-secret]", t)
    return t


def _safe_file_refs(refs: list[str], limit: int = 12) -> list[str]:
    out: list[str] = []
    for r in (refs or [])[:limit]:
        label = _safe_path_label(str(r))
        if label and ".." not in label:
            out.append(label)
    return out


@dataclass
class BuilderAdapterSpec:
    adapter_id: str = ""
    label: str = ""
    kind: str = BuilderAdapterKind.UNKNOWN
    enabled: bool = False
    mode: str = BuilderAdapterMode.DISABLED
    worker_id: str = ""
    allowed_task_types: list[str] = field(default_factory=lambda: ["repair"])
    max_estimated_tokens: int = 120_000
    requires_operator_approval: bool = True
    requires_external_sandbox_intake: bool = True
    allows_direct_repo_write: bool = False
    allows_network: bool = False
    command_template_id: str = ""
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "adapter_id": self.adapter_id, "label": _safe(self.label),
            "kind": self.kind, "enabled": bool(self.enabled),
            "mode": self.mode, "worker_id": self.worker_id,
            "allowed_task_types": list(self.allowed_task_types),
            "max_estimated_tokens": int(self.max_estimated_tokens),
            "requires_operator_approval": bool(self.requires_operator_approval),
            "requires_external_sandbox_intake": bool(self.requires_external_sandbox_intake),
            "allows_direct_repo_write": False,  # HARD: always False in v0
            "allows_network": bool(self.allows_network),
            "command_template_id": self.command_template_id,
            "notes": _safe(self.notes),
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> BuilderAdapterSpec:
        return cls(
            adapter_id=str(d.get("adapter_id", "")),
            label=str(d.get("label", "")),
            kind=str(d.get("kind", BuilderAdapterKind.UNKNOWN)),
            enabled=bool(d.get("enabled", False)),
            mode=str(d.get("mode", BuilderAdapterMode.DISABLED)),
            worker_id=str(d.get("worker_id", "")),
            allowed_task_types=list(d.get("allowed_task_types") or ["repair"]),
            max_estimated_tokens=int(d.get("max_estimated_tokens", 120_000)),
            requires_operator_approval=bool(d.get("requires_operator_approval", True)),
            requires_external_sandbox_intake=bool(d.get("requires_external_sandbox_intake", True)),
            allows_direct_repo_write=False,  # HARD: always False in v0
            allows_network=bool(d.get("allows_network", False)),
            command_template_id=str(d.get("command_template_id", "")),
            notes=str(d.get("notes", "")),
        )


@dataclass
class BuilderRequestPackage:
    package_id: str = ""
    job_id: str = ""
    repair_id: str = ""
    contract_id: str = ""
    task_type: str = "repair"
    goal_summary: str = ""
    acceptance_criteria_refs: list[str] = field(default_factory=list)
    context_pack_ref: str = ""
    safe_context_summary: str = ""
    forbidden_actions: list[str] = field(default_factory=lambda: list(_FORBIDDEN_ACTIONS))
    token_budget_summary: dict[str, Any] = field(default_factory=dict)
    expected_output_contract: str = _EXPECTED_OUTPUT_CONTRACT
    route_reason: str = ""
    adapter_id: str = ""
    requires_human_approval: bool = True
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "package_id": self.package_id, "job_id": self.job_id,
            "repair_id": self.repair_id, "contract_id": self.contract_id,
            "task_type": self.task_type,
            "goal_summary": _safe(self.goal_summary),
            "acceptance_criteria_refs": list(self.acceptance_criteria_refs)[:20],
            "context_pack_ref": self.context_pack_ref,
            "safe_context_summary": _safe(self.safe_context_summary),
            "forbidden_actions": list(self.forbidden_actions),
            "token_budget_summary": dict(self.token_budget_summary),
            "expected_output_contract": self.expected_output_contract,
            "route_reason": _safe(self.route_reason),
            "adapter_id": self.adapter_id,
            "requires_human_approval": bool(self.requires_human_approval),
            "created_at": self.created_at,
        }


@dataclass
class BuilderSessionRecord:
    session_id: str = ""
    adapter_id: str = ""
    package_id: str = ""
    job_id: str = ""
    repair_id: str = ""
    status: str = BuilderSessionStatus.NOT_STARTED
    started_at: str = ""
    ended_at: str = ""
    transcript_ref: str = ""
    candidate_artifact_ref: str = ""
    sandbox_submission_id: str = ""
    candidate_quality_status: str = ""
    review_status: str = ""
    next_safe_action: str = ""
    blocking_reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id, "adapter_id": self.adapter_id,
            "package_id": self.package_id, "job_id": self.job_id,
            "repair_id": self.repair_id, "status": self.status,
            "started_at": self.started_at, "ended_at": self.ended_at,
            "transcript_ref": self.transcript_ref,
            "candidate_artifact_ref": self.candidate_artifact_ref,
            "sandbox_submission_id": self.sandbox_submission_id,
            "candidate_quality_status": self.candidate_quality_status,
            "review_status": self.review_status,
            "next_safe_action": _safe(self.next_safe_action, 500),
            "blocking_reasons": [_safe(r) for r in self.blocking_reasons[:10]],
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> BuilderSessionRecord:
        return cls(
            session_id=str(d.get("session_id", "")),
            adapter_id=str(d.get("adapter_id", "")),
            package_id=str(d.get("package_id", "")),
            job_id=str(d.get("job_id", "")),
            repair_id=str(d.get("repair_id", "")),
            status=str(d.get("status", BuilderSessionStatus.NOT_STARTED)),
            started_at=str(d.get("started_at", "")),
            ended_at=str(d.get("ended_at", "")),
            transcript_ref=str(d.get("transcript_ref", "")),
            candidate_artifact_ref=str(d.get("candidate_artifact_ref", "")),
            sandbox_submission_id=str(d.get("sandbox_submission_id", "")),
            candidate_quality_status=str(d.get("candidate_quality_status", "")),
            review_status=str(d.get("review_status", "")),
            next_safe_action=str(d.get("next_safe_action", "")),
            blocking_reasons=list(d.get("blocking_reasons") or []),
        )


# ---------------------------------------------------------------------------
# Storage (atomic, corruption-aware, bounded)
# ---------------------------------------------------------------------------


def _resolve_ddir(data_dir: Path | None) -> Path:
    if data_dir is not None:
        return Path(data_dir)
    from packages.orchestration.data_paths import resolve_data_root
    return resolve_data_root()


def _mba_dir(job_id: str, ddir: Path) -> Path:
    return ddir / "workspaces" / job_id / _MBA_DIRNAME


def _atomic_write(p: Path, data: dict[str, Any]) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    os.chmod(p.parent, 0o700) if p.parent.exists() else None
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
# Adapter registry (Phase 3)
# ---------------------------------------------------------------------------


def default_builder_adapter_specs() -> list[BuilderAdapterSpec]:
    """Default adapter specs — all real adapters disabled, fixture only in fixture mode."""
    return [
        BuilderAdapterSpec(
            adapter_id="claude-code-v0", label="Claude Code", kind=BuilderAdapterKind.CLAUDE_CODE,
            enabled=False, mode=BuilderAdapterMode.DISABLED,
            requires_operator_approval=True, requires_external_sandbox_intake=True,
        ),
        BuilderAdapterSpec(
            adapter_id="pi-dev-v0", label="Pi.dev", kind=BuilderAdapterKind.PI_DEV,
            enabled=False, mode=BuilderAdapterMode.DISABLED,
            requires_operator_approval=True, requires_external_sandbox_intake=True,
        ),
        BuilderAdapterSpec(
            adapter_id="opencode-v0", label="OpenCode", kind=BuilderAdapterKind.OPENCODE,
            enabled=False, mode=BuilderAdapterMode.DISABLED,
            requires_operator_approval=True, requires_external_sandbox_intake=True,
        ),
        BuilderAdapterSpec(
            adapter_id="generic-cli-v0", label="Generic External CLI Builder",
            kind=BuilderAdapterKind.GENERIC_EXTERNAL_CLI_BUILDER,
            enabled=False, mode=BuilderAdapterMode.DISABLED,
            requires_operator_approval=True, requires_external_sandbox_intake=True,
        ),
        BuilderAdapterSpec(
            adapter_id="fixture-v0", label="Fixture Builder",
            kind=BuilderAdapterKind.FIXTURE_BUILDER,
            enabled=False, mode=BuilderAdapterMode.FIXTURE_ONLY,
            requires_operator_approval=False, requires_external_sandbox_intake=False,
        ),
    ]


def _adapters_dir(ddir: Path) -> Path:
    return ddir / _MBA_DIRNAME / "adapters"


def save_builder_adapter_spec(spec: BuilderAdapterSpec, data_dir: Path | None = None) -> bool:
    ddir = _resolve_ddir(data_dir)
    d = spec.to_dict()
    # HARD: never store secrets, never allow direct repo write.
    d["allows_direct_repo_write"] = False
    blob = json.dumps(d, default=str)
    for marker in _RAW_MARKERS:
        if marker.lower() in blob.lower():
            return False
    _atomic_write(_adapters_dir(ddir) / f"{spec.adapter_id}.json", d)
    return True


def list_builder_adapter_specs(data_dir: Path | None = None) -> list[dict[str, Any]]:
    ddir = _resolve_ddir(data_dir)
    stored = _load_json_dir(_adapters_dir(ddir))
    if stored:
        return stored
    return [s.to_dict() for s in default_builder_adapter_specs()]


def get_builder_adapter_spec(adapter_id: str, data_dir: Path | None = None) -> dict[str, Any] | None:
    for s in list_builder_adapter_specs(data_dir):
        if s.get("adapter_id") == adapter_id:
            return s
    return None


# ---------------------------------------------------------------------------
# Token-aware builder request package (Phase 4)
# ---------------------------------------------------------------------------


def build_builder_request_package(
    job_id: str, *, repair_id: str = "", adapter_id: str = "",
    context_pack: dict[str, Any] | None = None,
    acceptance_criteria: list[str] | None = None,
    token_hint: dict[str, Any] | None = None,
    tournament_hint: dict[str, Any] | None = None,
    route_reason: str = "",
    data_dir: Path | None = None,
) -> BuilderRequestPackage:
    """Build a minimal, token-aware request package for an external builder session.

    Never includes raw logs/diffs/candidates. Unknown/oversized token budgets require human
    approval. Package explains why this route was selected."""
    ddir = _resolve_ddir(data_dir)
    spec = get_builder_adapter_spec(adapter_id, ddir) if adapter_id else None
    th = token_hint or {}
    cp = context_pack or {}
    pkg = BuilderRequestPackage(
        package_id=uuid4().hex[:16],
        job_id=job_id, repair_id=repair_id, adapter_id=adapter_id,
        task_type="repair" if repair_id else "general",
        goal_summary=_safe(cp.get("goal_summary", "") or cp.get("safe_summary", ""), 300),
        acceptance_criteria_refs=list(acceptance_criteria or [])[:20],
        context_pack_ref=str(cp.get("context_pack_id", "") or cp.get("repair_id", "")),
        safe_context_summary=_safe(cp.get("safe_summary", ""), 300),
        token_budget_summary={
            "estimated_token_band": th.get("estimated_token_band", "unknown"),
            "budget_status": th.get("budget_status", "unknown"),
            "requires_human_approval": th.get("requires_human_approval", True),
            "local_first_recommended": th.get("local_first_recommended", False),
        },
        route_reason=_safe(route_reason or "operator_selected", 200),
        created_at=_now(),
    )
    # Determine approval requirement.
    budget_status = th.get("budget_status", "unknown")
    token_band = th.get("estimated_token_band", "unknown")
    needs_approval = (
        budget_status in ("unknown", "over_budget", "over")
        or token_band in ("unknown", "very_high", "huge")
        or (spec and spec.get("requires_operator_approval", True))
        or (not spec)  # unknown adapter
    )
    pkg.requires_human_approval = needs_approval
    # Persist.
    pkg_dir = _mba_dir(job_id, ddir) / "packages"
    _atomic_write(pkg_dir / f"{pkg.package_id}.json", pkg.to_dict())
    return pkg


# ---------------------------------------------------------------------------
# Session lifecycle (Phase 5)
# ---------------------------------------------------------------------------


def create_builder_session(
    package_id: str, adapter_id: str, *, job_id: str = "", repair_id: str = "",
    data_dir: Path | None = None,
) -> BuilderSessionRecord:
    """Create a new builder session record. Metadata only — no execution."""
    ddir = _resolve_ddir(data_dir)
    spec = get_builder_adapter_spec(adapter_id, ddir)
    session = BuilderSessionRecord(
        session_id=uuid4().hex[:16], adapter_id=adapter_id,
        package_id=package_id, job_id=job_id, repair_id=repair_id,
        status=BuilderSessionStatus.PACKAGE_READY,
        started_at=_now(),
    )
    if spec and not spec.get("enabled", False):
        session.status = BuilderSessionStatus.BLOCKED
        session.blocking_reasons = ["adapter_disabled"]
        session.next_safe_action = f"remedy builder adapter-enable {adapter_id} --mode operator_launched --json"
    elif spec and spec.get("requires_operator_approval", True):
        session.status = BuilderSessionStatus.WAITING_FOR_OPERATOR
        session.next_safe_action = f"remedy builder session-show {session.session_id} --json"
    else:
        session.next_safe_action = f"remedy builder session-show {session.session_id} --json"
    _save_session(session, ddir)
    return session


def mark_builder_session_waiting_for_operator(
    session_id: str, *, data_dir: Path | None = None,
) -> BuilderSessionRecord | None:
    ddir = _resolve_ddir(data_dir)
    session = _load_session(session_id, ddir)
    if not session:
        return None
    session.status = BuilderSessionStatus.WAITING_FOR_OPERATOR
    session.next_safe_action = f"remedy builder session-show {session_id} --json"
    _save_session(session, ddir)
    return session


def record_builder_session_started(
    session_id: str, *, data_dir: Path | None = None,
) -> BuilderSessionRecord | None:
    ddir = _resolve_ddir(data_dir)
    session = _load_session(session_id, ddir)
    if not session:
        return None
    session.status = BuilderSessionStatus.RUNNING
    session.started_at = session.started_at or _now()
    session.next_safe_action = f"remedy builder session-record-output {session_id} --artifact-ref <ref> --json"
    _save_session(session, ddir)
    return session


def record_builder_session_output(
    session_id: str, *, transcript_ref: str = "", candidate_artifact_ref: str = "",
    data_dir: Path | None = None,
) -> BuilderSessionRecord | None:
    """Record builder output refs. Never stores raw transcript/candidate content."""
    ddir = _resolve_ddir(data_dir)
    session = _load_session(session_id, ddir)
    if not session:
        return None
    session.transcript_ref = _safe(transcript_ref, 200)
    session.candidate_artifact_ref = _safe(candidate_artifact_ref, 200)
    session.status = BuilderSessionStatus.CANDIDATE_RECEIVED
    session.next_safe_action = f"remedy builder session-intake {session_id} --json"
    _save_session(session, ddir)
    return session


def record_builder_session_blocked(
    session_id: str, *, reason: str = "", data_dir: Path | None = None,
) -> BuilderSessionRecord | None:
    ddir = _resolve_ddir(data_dir)
    session = _load_session(session_id, ddir)
    if not session:
        return None
    session.status = BuilderSessionStatus.BLOCKED
    if reason:
        session.blocking_reasons.append(_safe(reason))
    session.next_safe_action = f"remedy builder session-show {session_id} --json"
    _save_session(session, ddir)
    return session


def record_builder_session_intake_complete(
    session_id: str, *, sandbox_submission_id: str = "",
    candidate_quality_status: str = "", data_dir: Path | None = None,
) -> BuilderSessionRecord | None:
    """Mark session intake complete. Does NOT mark repair/mission done."""
    ddir = _resolve_ddir(data_dir)
    session = _load_session(session_id, ddir)
    if not session:
        return None
    session.sandbox_submission_id = sandbox_submission_id
    session.candidate_quality_status = candidate_quality_status
    session.status = BuilderSessionStatus.COMPLETED_INTAKE_ONLY
    session.ended_at = _now()
    # Intake complete ≠ repaired — downstream gates still required.
    session.next_safe_action = f"remedy repair evaluate {session.repair_id} --json" if session.repair_id else ""
    _save_session(session, ddir)
    return session


def load_builder_session(session_id: str, data_dir: Path | None = None) -> BuilderSessionRecord | None:
    return _load_session(session_id, _resolve_ddir(data_dir))


def list_builder_sessions(job_id: str = "", data_dir: Path | None = None) -> list[dict[str, Any]]:
    ddir = _resolve_ddir(data_dir)
    if job_id:
        return _load_json_dir(_mba_dir(job_id, ddir) / "sessions")
    # Scan all workspaces.
    out: list[dict] = []
    ws = ddir / "workspaces"
    if ws.is_dir():
        for child in sorted(ws.iterdir()):
            out.extend(_load_json_dir(child / _MBA_DIRNAME / "sessions"))
    return out


def _save_session(session: BuilderSessionRecord, ddir: Path) -> None:
    job_id = session.job_id or "_global"
    _atomic_write(
        _mba_dir(job_id, ddir) / "sessions" / f"{session.session_id}.json",
        session.to_dict(),
    )


def _load_session(session_id: str, ddir: Path) -> BuilderSessionRecord | None:
    # Search across workspaces.
    ws = ddir / "workspaces"
    if ws.is_dir():
        for child in sorted(ws.iterdir()):
            p = child / _MBA_DIRNAME / "sessions" / f"{session_id}.json"
            d = _load_json(p)
            if d:
                return BuilderSessionRecord.from_dict(d)
    # Global fallback.
    d = _load_json(_mba_dir("_global", ddir) / "sessions" / f"{session_id}.json")
    if d:
        return BuilderSessionRecord.from_dict(d)
    return None


# ---------------------------------------------------------------------------
# Fixture builder (Phase 6)
# ---------------------------------------------------------------------------


class FixtureScenario:
    SUCCESS = "success"
    INVALID_CANDIDATE = "invalid_candidate"
    TRUST_REJECTED = "trust_rejected"
    BLOCKED = "blocked"
    OVERSIZED_OUTPUT = "oversized_output"
    NO_OUTPUT = "no_output"


_ALL_FIXTURE_SCENARIOS = frozenset({
    FixtureScenario.SUCCESS, FixtureScenario.INVALID_CANDIDATE,
    FixtureScenario.TRUST_REJECTED, FixtureScenario.BLOCKED,
    FixtureScenario.OVERSIZED_OUTPUT, FixtureScenario.NO_OUTPUT,
})


def run_fixture_builder(
    session_id: str, *, fixture_scenario: str = FixtureScenario.SUCCESS,
    data_dir: Path | None = None,
) -> BuilderSessionRecord | None:
    """Deterministic fixture builder — no network, no provider, no repo mutation.

    Output still goes through the same intake path as real builder output.
    Fixture mode must be explicitly selected (adapter kind = fixture_builder)."""
    ddir = _resolve_ddir(data_dir)
    session = _load_session(session_id, ddir)
    if not session:
        return None

    spec = get_builder_adapter_spec(session.adapter_id, ddir)
    if not spec or spec.get("kind") != BuilderAdapterKind.FIXTURE_BUILDER:
        session.status = BuilderSessionStatus.BLOCKED
        session.blocking_reasons.append("not_fixture_adapter")
        session.next_safe_action = f"remedy builder session-show {session_id} --json"
        _save_session(session, ddir)
        return session

    if fixture_scenario == FixtureScenario.SUCCESS:
        session.candidate_artifact_ref = f"fixture-candidate-{session_id}"
        session.status = BuilderSessionStatus.CANDIDATE_RECEIVED
        session.next_safe_action = f"remedy builder session-intake {session_id} --json"
    elif fixture_scenario == FixtureScenario.INVALID_CANDIDATE:
        session.candidate_artifact_ref = f"fixture-invalid-{session_id}"
        session.candidate_quality_status = "rejected"
        session.status = BuilderSessionStatus.NEEDS_REVIEW
        session.next_safe_action = f"remedy builder session-show {session_id} --json"
    elif fixture_scenario == FixtureScenario.TRUST_REJECTED:
        session.candidate_quality_status = "trust_rejected"
        session.status = BuilderSessionStatus.BLOCKED
        session.blocking_reasons.append("trust_rejected")
        session.next_safe_action = f"remedy builder session-show {session_id} --json"
    elif fixture_scenario == FixtureScenario.BLOCKED:
        session.status = BuilderSessionStatus.BLOCKED
        session.blocking_reasons.append("fixture_blocked_scenario")
        session.next_safe_action = f"remedy builder session-show {session_id} --json"
    elif fixture_scenario == FixtureScenario.OVERSIZED_OUTPUT:
        session.status = BuilderSessionStatus.BLOCKED
        session.blocking_reasons.append("oversized_output")
        session.next_safe_action = f"remedy builder session-show {session_id} --json"
    elif fixture_scenario == FixtureScenario.NO_OUTPUT:
        session.status = BuilderSessionStatus.BLOCKED
        session.blocking_reasons.append("no_output")
        session.next_safe_action = f"remedy builder session-show {session_id} --json"
    else:
        session.status = BuilderSessionStatus.BLOCKED
        session.blocking_reasons.append(f"unknown_fixture_scenario: {_safe(fixture_scenario)}")
        session.next_safe_action = f"remedy builder session-show {session_id} --json"

    session.ended_at = _now()
    _save_session(session, ddir)
    return session


# ---------------------------------------------------------------------------
# Builder adapter recommendation (Phase 10 — Token Economy/Tournament/Worker Registry)
# ---------------------------------------------------------------------------


def recommend_builder_adapter(
    job_id: str, *, repair_id: str = "",
    token_hint: dict[str, Any] | None = None,
    tournament_hint: dict[str, Any] | None = None,
    data_dir: Path | None = None,
) -> dict[str, Any]:
    """Recommend which builder adapter to use. Read-only, NEVER executes.

    Respects token budget, adapter enabled state, approval requirements.
    Expensive/unknown → human approval. Disabled/blocked → not recommended.
    Local/cheap → defer to local worker (not main builder adapter).
    Placeholder Ollama readiness is never faked."""
    ddir = _resolve_ddir(data_dir)
    th = token_hint or {}
    tt = tournament_hint or {}

    token_band = th.get("estimated_token_band", "unknown")
    budget_status = th.get("budget_status", "unknown")
    local_first = th.get("local_first_recommended", False)
    requires_approval = th.get("requires_human_approval", True)

    # Cheap/small tasks → prefer local, not main builder.
    if local_first and token_band in ("very_low", "low", "small"):
        return {
            "recommended_adapter_id": "",
            "recommended_kind": "",
            "recommendation": "prefer_local_worker",
            "reason": "Token band is small and local-first is recommended. Use local worker.",
            "requires_human_approval": False,
            "token_band": token_band,
            "budget_status": budget_status,
        }

    # Unknown/oversized → require human approval.
    if token_band in ("unknown",) or budget_status in ("unknown", "over_budget", "over"):
        return {
            "recommended_adapter_id": "",
            "recommended_kind": "",
            "recommendation": "human_decision_required",
            "reason": f"Token band ({token_band}) or budget ({budget_status}) unknown/over. Human decision required.",
            "requires_human_approval": True,
            "token_band": token_band,
            "budget_status": budget_status,
        }

    # Find first enabled adapter that fits.
    specs = list_builder_adapter_specs(ddir)
    for s in specs:
        if not s.get("enabled", False):
            continue
        if s.get("kind") == BuilderAdapterKind.FIXTURE_BUILDER:
            continue  # fixture not for real work
        aid = s.get("adapter_id", "")
        return {
            "recommended_adapter_id": aid,
            "recommended_kind": s.get("kind", ""),
            "recommendation": "adapter_available",
            "reason": f"Adapter {aid} is enabled and available.",
            "requires_human_approval": s.get("requires_operator_approval", True) or requires_approval,
            "token_band": token_band,
            "budget_status": budget_status,
        }

    # No enabled adapter.
    return {
        "recommended_adapter_id": "",
        "recommended_kind": "",
        "recommendation": "no_enabled_adapter",
        "reason": "No real builder adapter is enabled. Configure and enable one first.",
        "requires_human_approval": True,
        "token_band": token_band,
        "budget_status": budget_status,
    }


# ---------------------------------------------------------------------------
# Mission integration helper (Phase 9)
# ---------------------------------------------------------------------------


def builder_adapter_mission_signal(
    job_id: str, data_dir: Path | None = None,
) -> dict[str, Any]:
    """Safe summary of builder session state for Mission Contract consumption.

    Running/waiting sessions do NOT satisfy mission. Blocked sessions create required next action.
    Candidate received still requires downstream gates. Honest (no fake done)."""
    ddir = _resolve_ddir(data_dir)
    sessions = list_builder_sessions(job_id, ddir)
    running_count = 0
    waiting_count = 0
    blocked_count = 0
    candidate_count = 0
    intake_complete_count = 0
    user_decision = False
    for s in sessions:
        st = s.get("status", "")
        if st == BuilderSessionStatus.RUNNING:
            running_count += 1
        elif st == BuilderSessionStatus.WAITING_FOR_OPERATOR:
            waiting_count += 1
        elif st == BuilderSessionStatus.BLOCKED:
            blocked_count += 1
            user_decision = True
        elif st == BuilderSessionStatus.CANDIDATE_RECEIVED:
            candidate_count += 1
        elif st == BuilderSessionStatus.COMPLETED_INTAKE_ONLY:
            intake_complete_count += 1
    has_active = running_count + waiting_count + blocked_count + candidate_count > 0
    return {
        "running_session_count": running_count,
        "waiting_session_count": waiting_count,
        "blocked_session_count": blocked_count,
        "candidate_received_count": candidate_count,
        "intake_complete_count": intake_complete_count,
        "has_active_sessions": has_active,
        "user_decision_required": user_decision,
        "builder_satisfies_mission": False,  # NEVER — downstream gates required
    }


# ---------------------------------------------------------------------------
# Integrity (Phase 17)
# ---------------------------------------------------------------------------


def _next_action_is_catalog_valid(action: str) -> bool:
    if not action or not action.startswith("remedy "):
        return False
    valid_prefixes = (
        "remedy builder ", "remedy repair ", "remedy test ", "remedy patch ",
        "remedy external-builder ", "remedy job ", "remedy contract ",
        "remedy snapshot ", "remedy rollback ", "remedy overnight ", "remedy context ",
    )
    return any(action.startswith(p) for p in valid_prefixes)


def audit_adapter_spec_safety(spec: dict[str, Any]) -> list[dict[str, str]]:
    """Flag unsafe adapter configurations. Safe codes only."""
    out: list[dict[str, str]] = []
    aid = spec.get("adapter_id", "")
    kind = spec.get("kind", "")
    blob = json.dumps(spec).lower()
    # No direct repo write in v0.
    if spec.get("allows_direct_repo_write", False):
        out.append({"adapter_id": aid, "code": "direct_repo_write_enabled"})
    # Real adapter cannot bypass sandbox intake.
    if kind in _REAL_ADAPTER_KINDS and not spec.get("requires_external_sandbox_intake", True):
        out.append({"adapter_id": aid, "code": "real_adapter_bypasses_sandbox_intake"})
    # No secrets/raw in spec.
    if any(m.lower() in blob for m in _RAW_MARKERS):
        out.append({"adapter_id": aid, "code": "secret_or_raw_in_adapter_spec"})
    # Absolute paths.
    if "/home/" in blob or "/users/" in blob or "/root/" in blob:
        out.append({"adapter_id": aid, "code": "absolute_path_in_adapter_spec"})
    # Unknown kind/mode.
    if kind not in _ALL_KINDS:
        out.append({"adapter_id": aid, "code": "unknown_adapter_kind"})
    if spec.get("mode", "") not in _ALL_MODES:
        out.append({"adapter_id": aid, "code": "unknown_adapter_mode"})
    # Real adapter enabled without operator approval.
    if kind in _REAL_ADAPTER_KINDS and spec.get("enabled", False) and not spec.get("requires_operator_approval", True):
        out.append({"adapter_id": aid, "code": "real_adapter_enabled_without_approval"})
    # Fixture in production-like mode.
    if kind == BuilderAdapterKind.FIXTURE_BUILDER and spec.get("mode") in (
        BuilderAdapterMode.OPERATOR_LAUNCHED, BuilderAdapterMode.CONTROLLED_SESSION
    ):
        out.append({"adapter_id": aid, "code": "fixture_in_production_mode"})
    return out


def audit_session_safety(session: dict[str, Any]) -> list[dict[str, str]]:
    """Flag unsafe session states. Safe codes only."""
    out: list[dict[str, str]] = []
    sid = session.get("session_id", "")
    status = session.get("status", "")
    blob = json.dumps(session).lower()
    # No raw in public session.
    if any(m.lower() in blob for m in _RAW_MARKERS):
        out.append({"session_id": sid, "code": "raw_or_secret_in_session"})
    # Absolute paths.
    if "/home/" in blob or "/users/" in blob or "/root/" in blob:
        out.append({"session_id": sid, "code": "absolute_path_in_session"})
    # Unknown status.
    if status not in _ALL_SESSION_STATUSES:
        out.append({"session_id": sid, "code": "unknown_session_status"})
    # Next actions catalog-valid.
    nsa = session.get("next_safe_action", "")
    if nsa and "<" not in nsa and not _next_action_is_catalog_valid(nsa):
        out.append({"session_id": sid, "code": "non_catalog_next_action"})
    return out


def builder_adapter_integrity(data_dir: Path | None = None) -> dict[str, Any]:
    """Read-only invariant check over adapter specs + sessions. Safe codes only."""
    ddir = _resolve_ddir(data_dir)
    violations: list[dict] = []
    specs = list_builder_adapter_specs(ddir)
    for s in specs:
        violations.extend(audit_adapter_spec_safety(s))
    sessions = list_builder_sessions(data_dir=ddir)
    for sess in sessions:
        violations.extend(audit_session_safety(sess))
    return {
        "version": 1,
        "adapter_count": len(specs),
        "session_count": len(sessions),
        "violation_count": len(violations),
        "passed": not violations,
        "violations": violations[:50],
    }


# ---------------------------------------------------------------------------
# Public exports
# ---------------------------------------------------------------------------


__all__ = [
    "SCHEMA_VERSION",
    "BuilderAdapterKind", "BuilderAdapterMode", "BuilderSessionStatus",
    "BuilderAdapterSpec", "BuilderRequestPackage", "BuilderSessionRecord",
    "FixtureScenario",
    "default_builder_adapter_specs", "list_builder_adapter_specs",
    "get_builder_adapter_spec", "save_builder_adapter_spec",
    "build_builder_request_package",
    "create_builder_session", "mark_builder_session_waiting_for_operator",
    "record_builder_session_started", "record_builder_session_output",
    "record_builder_session_blocked", "record_builder_session_intake_complete",
    "load_builder_session", "list_builder_sessions",
    "run_fixture_builder",
    "recommend_builder_adapter", "builder_adapter_mission_signal",
    "audit_adapter_spec_safety", "audit_session_safety",
    "builder_adapter_integrity",
]
