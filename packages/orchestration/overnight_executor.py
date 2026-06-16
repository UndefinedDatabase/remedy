"""
Bounded Overnight Executor v0 — one foreground, explicitly-invoked, reviewable step
(Steps 1275-1304).

Remedy may perform AT MOST ONE bounded continuation/proposal step when a human
explicitly invokes it. This is NOT a daemon, scheduler, watcher, background worker,
or repeating loop. Every invocation is one run that:

    readiness check → select one catalog-backed safe action → (if policy permits)
    execute exactly one allowed central-service action → persist a run record /
    checkpoints → stop → produce a morning-style report.

Hard rules enforced here:
  - Foreground only. No subprocess/CLI to execute Remedy commands — the executor
    calls central services (do_continue, repair_loop) directly. No shell.
  - Default behavior is report-only. Execution requires an explicit policy override
    (``--allow-one-cycle`` from the CLI) AND an explicit action flag
    (allow_apply / allow_repair_apply / allow_repair_propose). No config file may
    silently enable execution.
  - ``max_cycles == 1`` — exactly one allowed action per invocation, never a loop.
  - No provider/Ollama. No auto-approval. No auto-revert. No git commit.
  - Idempotent: a retry never double-applies, double-tests, double-repair-proposes,
    or duplicates a run's effect (delegated services are themselves idempotent).
  - Gates (permission/approval/RunContract/snapshot/test) live in central services;
    the executor re-validates and calls them, never bypasses them.
  - PENDING/FAIL review verdict or an open blocker/high finding blocks execution.
  - No raw stdout/stderr, source, diffs, artifact bodies, secrets, tracebacks, or
    absolute private paths in any public surface.

Public API::

    run_overnight_executor(request, data_dir=None) -> OvernightRunResult
    build_executor_policy(...) -> BoundedOvernightPolicy
    export_run_result_json(result) -> dict
    render_overnight_run_report_markdown(result) -> str
    parse_review_findings(path=None) -> ReviewFindings
    list_run_records(job_id, data_dir=None) -> list[dict]
    latest_run_record(job_id, data_dir=None) -> dict | None
"""

from __future__ import annotations

import fcntl
import hashlib
import json
import os
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

from packages.orchestration.overnight_readiness import (
    BoundedOvernightPolicy,
    OvernightStopReason,
    build_overnight_readiness,
    default_overnight_policy,
    export_readiness_json,
)

# ---------------------------------------------------------------------------
# Vocabularies (Step 1276 / 1280 / 1286)
# ---------------------------------------------------------------------------


class OvernightExecutionMode:
    """How a run behaves. Default is always report-only."""

    REPORT_ONLY = "report_only"
    EXECUTE_ONE = "execute_one"


class OvernightExecutionPhase:
    REQUESTED = "requested"
    READINESS_BEFORE = "readiness_before"
    POLICY_CHECKED = "policy_checked"
    ACTION_SELECTED = "action_selected"
    LEASE_ACQUIRED = "lease_acquired"
    ACTION_STARTED = "action_started"
    ACTION_COMPLETED = "action_completed"
    READINESS_AFTER = "readiness_after"
    REPORT_WRITTEN = "report_written"
    STOPPED = "stopped"


OVERNIGHT_EXECUTION_PHASES = (
    OvernightExecutionPhase.REQUESTED,
    OvernightExecutionPhase.READINESS_BEFORE,
    OvernightExecutionPhase.POLICY_CHECKED,
    OvernightExecutionPhase.ACTION_SELECTED,
    OvernightExecutionPhase.LEASE_ACQUIRED,
    OvernightExecutionPhase.ACTION_STARTED,
    OvernightExecutionPhase.ACTION_COMPLETED,
    OvernightExecutionPhase.READINESS_AFTER,
    OvernightExecutionPhase.REPORT_WRITTEN,
    OvernightExecutionPhase.STOPPED,
)


# Executable action kinds the executor recognises. Anything else is read-only.
class OvernightActionKind:
    NONE = "none"
    REPORT_ONLY = "report_only"
    HUMAN_APPROVAL = "human_approval"
    DO_CONTINUE = "do_continue"
    REPAIR_PROPOSE = "repair_propose"


# Canonical executor stop reasons mirror the prep taxonomy (Step 1286).
_CANONICAL_STOP_REASONS = frozenset({
    OvernightStopReason.HUMAN_APPROVAL_REQUIRED,
    OvernightStopReason.CONTRACT_BLOCKED,
    OvernightStopReason.PERMISSION_MISSING,
    OvernightStopReason.BUDGET_EXHAUSTED,
    OvernightStopReason.NO_SAFE_ACTION,
    OvernightStopReason.UNKNOWN_RISK,
    OvernightStopReason.MEDIUM_OR_HIGH_RISK,
    OvernightStopReason.SNAPSHOT_MISSING,
    OvernightStopReason.SNAPSHOT_UNVERIFIED,
    OvernightStopReason.EVIDENCE_INCOMPLETE,
    OvernightStopReason.TEST_FAILED,
    OvernightStopReason.REPAIR_AVAILABLE,
    OvernightStopReason.REPAIR_PENDING_APPROVAL,
    OvernightStopReason.REPAIR_UNAVAILABLE,
    OvernightStopReason.REVIEW_FINDINGS_OPEN,
    OvernightStopReason.INTEGRITY_FAILED,
    OvernightStopReason.PROVIDER_UNAVAILABLE,
    OvernightStopReason.UNSUPPORTED_STATE,
    OvernightStopReason.COMPLETED_VERIFIED,
})


def _canonical(reason: str) -> str:
    """Guarantee a canonical stop reason; default to unsupported_state."""
    return reason if reason in _CANONICAL_STOP_REASONS else OvernightStopReason.UNSUPPORTED_STATE


# ---------------------------------------------------------------------------
# Explicit execution policy (Step 1277)
# ---------------------------------------------------------------------------


def build_executor_policy(
    *,
    allow_one_cycle: bool = False,
    allow_apply: bool = False,
    allow_repair_propose: bool = False,
    allow_repair_apply: bool = False,
) -> BoundedOvernightPolicy:
    """Build the bounded policy for a single executor invocation (Step 1277).

    Without ``allow_one_cycle`` the policy is the safe default (report-only,
    ``max_cycles=0``) regardless of the other flags — execution can never be
    enabled implicitly. With it, exactly one cycle is permitted and only the
    explicitly-enabled action classes may run.
    """
    if not allow_one_cycle:
        return default_overnight_policy()
    return BoundedOvernightPolicy(
        max_cycles=1,
        max_test_runs=1,
        max_apply_count=1,
        max_repair_attempts=1,
        allow_apply=allow_apply,
        allow_repair_propose=allow_repair_propose,
        allow_repair_apply=allow_repair_apply,
        allow_provider=False,
        allow_revert=False,
    )


def executor_execution_permitted(policy: BoundedOvernightPolicy) -> bool:
    """True only if this policy may execute exactly one bounded action.

    Unlike ``BoundedOvernightPolicy.execution_enabled`` (apply-only), the executor
    also recognises repair-propose as a permitted single action. ``max_cycles``
    must be exactly 1 — never more (no loops).
    """
    return policy.max_cycles == 1 and (
        policy.allow_apply or policy.allow_repair_apply or policy.allow_repair_propose
    )


# ---------------------------------------------------------------------------
# Models (Step 1276)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class OvernightRunRequest:
    """Input to one executor invocation. Foreground, explicit."""

    job_id: str
    policy: BoundedOvernightPolicy = field(default_factory=default_overnight_policy)
    created_by: str = "cli_v0"
    source: str = "overnight_run_v0"


@dataclass(frozen=True)
class OvernightRunCheckpoint:
    """Durable per-phase checkpoint. Safe IDs/status only — no raw content."""

    phase: str
    status: str            # started | completed | blocked | skipped
    at: str
    evidence_status: str = "complete"
    ids: dict[str, str] = field(default_factory=dict)


@dataclass
class OvernightExecutionDecision:
    """Which action was selected and whether it may execute."""

    kind: str = OvernightActionKind.NONE
    label: str = ""
    command: str = ""
    entity_id: str = ""
    allowed: bool = False
    reason: str = ""
    stop_reason: str = OvernightStopReason.NO_SAFE_ACTION


@dataclass
class OvernightRunResult:
    """Full result of one executor invocation. No raw content."""

    version: int = 1
    run_id: str = ""
    job_id: str = ""
    created_by: str = ""
    mode: str = OvernightExecutionMode.REPORT_ONLY
    started_at: str = ""
    completed_at: str = ""
    policy_summary: dict[str, Any] = field(default_factory=dict)
    selected_action: dict[str, str] = field(default_factory=dict)
    executed_action: dict[str, str] = field(default_factory=dict)
    stop_reason: str = OvernightStopReason.NO_SAFE_ACTION
    next_safe_action: dict[str, str] = field(default_factory=dict)
    readiness_before: dict[str, Any] = field(default_factory=dict)
    readiness_after: dict[str, Any] = field(default_factory=dict)
    checklist_before: list[dict[str, str]] = field(default_factory=list)
    checklist_after: list[dict[str, str]] = field(default_factory=list)
    evidence_status: str = "complete"
    checkpoints: list[OvernightRunCheckpoint] = field(default_factory=list)
    error_status: str = ""
    review_findings: dict[str, Any] = field(default_factory=dict)
    record_path: str = ""
    safe_summary: str = ""
    # Data root for immediate per-phase checkpoint flushing (not exported).
    _data_dir: Any = field(default=None, repr=False, compare=False)

    def _checkpoint(self, phase: str, status: str, **ids: str) -> None:
        """Append a phase checkpoint AND flush it durably right away (Step 1280).

        Persisting before/after each phase — in particular immediately before and
        after the mutating action — means a crash leaves a durable trail and the
        write outcome is surfaced (a silent failure degrades ``error_status``).
        """
        cp = OvernightRunCheckpoint(
            phase=phase, status=status, at=_now(),
            evidence_status=self.evidence_status, ids={k: v for k, v in ids.items() if v},
        )
        self.checkpoints.append(cp)
        if self._data_dir is not None:
            ok = save_overnight_checkpoint(self.job_id, self.run_id, self._data_dir, cp)
            if not ok and not self.error_status:
                self.error_status = "checkpoint_persist_degraded"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Run record persistence (Step 1279) — atomic, append-only, no overwrite.
# ---------------------------------------------------------------------------


def _runs_dir(job_id: str, data_dir: Path) -> Path:
    return data_dir / "workspaces" / job_id / "overnight_runs"


def _run_dir(job_id: str, run_id: str, data_dir: Path) -> Path:
    return _runs_dir(job_id, data_dir) / run_id


def _atomic_write(path: Path, payload: bytes) -> bool:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_bytes(payload)
        try:
            os.chmod(tmp, 0o600)
        except OSError:
            pass
        os.replace(tmp, path)
        return True
    except OSError:
        return False


def save_run_record(result: OvernightRunResult, data_dir: Path) -> str:
    """Persist a run record atomically. Returns the record path ("" on failure).

    Records are append-only: each run lives in its own ``<run_id>/`` directory and
    is never overwritten. A morning report is written alongside the record.
    """
    rdir = _run_dir(result.job_id, result.run_id, data_dir)
    record = export_run_record_json(result)
    ok = _atomic_write(rdir / "record.json", json.dumps(record, indent=2, sort_keys=True).encode("utf-8"))
    if not ok:
        return ""
    _atomic_write(rdir / "report.md", render_overnight_run_report_markdown(result).encode("utf-8"))
    return str(rdir / "record.json")


def save_overnight_checkpoint(
    job_id: str, run_id: str, data_dir: Path, checkpoint: OvernightRunCheckpoint
) -> bool:
    """Append a durable per-phase checkpoint atomically (Step 1280)."""
    path = _run_dir(job_id, run_id, data_dir) / "checkpoints.json"
    existing = load_overnight_checkpoints(job_id, run_id, data_dir)
    existing.append(checkpoint)
    payload = [
        {"phase": c.phase, "status": c.status, "at": c.at,
         "evidence_status": c.evidence_status, "ids": c.ids}
        for c in existing
    ]
    return _atomic_write(path, json.dumps(payload, indent=2, sort_keys=True).encode("utf-8"))


def load_overnight_checkpoints(job_id: str, run_id: str, data_dir: Path) -> list[OvernightRunCheckpoint]:
    path = _run_dir(job_id, run_id, data_dir) / "checkpoints.json"
    if not path.exists():
        return []
    try:
        raw = json.loads(path.read_bytes())
    except (OSError, json.JSONDecodeError):
        return []
    out: list[OvernightRunCheckpoint] = []
    for c in raw if isinstance(raw, list) else []:
        out.append(OvernightRunCheckpoint(
            phase=c.get("phase", ""), status=c.get("status", ""), at=c.get("at", ""),
            evidence_status=c.get("evidence_status", "complete"), ids=c.get("ids", {}) or {}))
    return out


def list_run_ids(job_id: str, data_dir: Path | None = None) -> list[str]:
    from packages.orchestration.data_paths import resolve_data_root
    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    base = _runs_dir(job_id, ddir)
    if not base.is_dir():
        return []
    try:
        ids = [p.name for p in base.iterdir() if p.is_dir() and (p / "record.json").exists()]
    except OSError:
        return []
    ids.sort(key=lambda rid: _record_started_at(job_id, rid, ddir))
    return ids


def _record_started_at(job_id: str, run_id: str, data_dir: Path) -> str:
    rec = load_run_record(job_id, run_id, data_dir)
    return rec.get("started_at", "") if rec else ""


def load_run_record(job_id: str, run_id: str, data_dir: Path) -> dict[str, Any] | None:
    path = _run_dir(job_id, run_id, data_dir) / "record.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_bytes())
    except (OSError, json.JSONDecodeError):
        return None


def list_run_records(job_id: str, data_dir: Path | None = None) -> list[dict[str, Any]]:
    from packages.orchestration.data_paths import resolve_data_root
    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    out: list[dict[str, Any]] = []
    for rid in list_run_ids(job_id, ddir):
        rec = load_run_record(job_id, rid, ddir)
        if rec:
            out.append(rec)
    return out


def latest_run_record(job_id: str, data_dir: Path | None = None) -> dict[str, Any] | None:
    recs = list_run_records(job_id, data_dir)
    return recs[-1] if recs else None


# ---------------------------------------------------------------------------
# Executor lease (Step 1278) — foreground, bounded, released on every exit.
# ---------------------------------------------------------------------------


@dataclass
class OvernightExecutionLease:
    """File-backed exclusive lease for one foreground executor run.

    A job lock always serialises runs for the same job. A repo lock is taken only
    when the selected action mutates the repository, so two read-only runs against
    the same repo (different jobs) are allowed while two mutating runs are not.
    A stale lease is recoverable because flock is freed when the holder dies; the
    lock file is unlinked on clean release.
    """

    job_id: str
    repo_key: str
    mutates_repo: bool
    lease_dir: Path
    _fhs: list[Any] = field(default_factory=list, repr=False, compare=False)
    _paths: list[Path] = field(default_factory=list, repr=False, compare=False)

    def _names(self) -> list[str]:
        names = [f"ov-job-{self.job_id}.lock"]
        if self.mutates_repo and self.repo_key:
            repo_hash = hashlib.sha256(self.repo_key.encode("utf-8")).hexdigest()[:32]
            names.append(f"ov-repo-{repo_hash}.lock")
        return names

    def acquire(self, *, timeout_seconds: float = 2.0) -> bool:
        self.lease_dir.mkdir(parents=True, exist_ok=True)
        for name in self._names():
            path = self.lease_dir / name
            fh = open(path, "w")  # noqa: SIM115 — held while leased
            deadline = time.monotonic() + timeout_seconds
            acquired = False
            while True:
                try:
                    fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    fh.write(f"{os.getpid()}\n{_now()}\n")
                    fh.flush()
                    acquired = True
                    break
                except OSError:
                    if time.monotonic() >= deadline:
                        break
                    time.sleep(0.05)
            if not acquired:
                fh.close()
                self.release()
                return False
            self._fhs.append(fh)
            self._paths.append(path)
        return True

    def release(self) -> None:
        while self._fhs:
            fh = self._fhs.pop()
            try:
                fcntl.flock(fh, fcntl.LOCK_UN)
                fh.close()
            except OSError:
                pass
        while self._paths:
            p = self._paths.pop()
            try:
                p.unlink(missing_ok=True)
            except OSError:
                pass


def _repo_key(job: Any) -> str:
    repo = (job.metadata or {}).get("target_repo", "") or ""
    if not repo:
        return ""
    try:
        return str(Path(repo).resolve())
    except OSError:
        return repo


# ---------------------------------------------------------------------------
# Review-findings source (Step 1285) — parse .agent/live_review.md safely.
# ---------------------------------------------------------------------------


@dataclass
class ReviewFindings:
    """Safe summary of the latest live review. Counts/status only — no details."""

    verdict: str = "unknown"      # pass | pass_with_risks | pending | fail | unknown
    open_blocker: int = 0
    open_high: int = 0
    open_medium: int = 0
    open_low: int = 0
    source: str = "unavailable"   # live_review | unavailable | malformed

    @property
    def open_blocker_or_high(self) -> int:
        return self.open_blocker + self.open_high

    def to_dict(self) -> dict[str, Any]:
        return {
            "verdict": self.verdict, "open_blocker": self.open_blocker,
            "open_high": self.open_high, "open_medium": self.open_medium,
            "open_low": self.open_low, "source": self.source,
        }


_VERDICT_MAP = {
    "PASS WITH RISKS": "pass_with_risks",
    "PASS": "pass",
    "PENDING": "pending",
    "FAIL": "fail",
}


def parse_review_findings(path: Path | None = None) -> ReviewFindings:
    """Parse the latest verdict and open finding counts from the live review file.

    Returns ``unknown`` when the file is missing or malformed. Exposes counts and
    a coarse verdict only — never raw finding text (Step 1285 redaction).

    The path defaults to ``.agent/live_review.md``; ``REMEDY_REVIEW_FILE`` overrides
    it (used by tests to supply a controlled verdict without touching the repo file).
    """
    if path is not None:
        p = Path(path)
    else:
        env = os.environ.get("REMEDY_REVIEW_FILE", "")
        p = Path(env) if env else Path(".agent") / "live_review.md"
    if not p.exists():
        return ReviewFindings(verdict="unknown", source="unavailable")
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ReviewFindings(verdict="unknown", source="malformed")

    findings = ReviewFindings(source="live_review")

    # Latest verdict: first non-empty line under a "## Verdict" heading.
    verdict_raw = ""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.strip().lower().startswith("## verdict"):
            for nxt in lines[i + 1:]:
                if nxt.strip():
                    verdict_raw = nxt.strip().upper()
                    break
            break
    findings.verdict = "unknown"
    for key, val in _VERDICT_MAP.items():  # ordered: "PASS WITH RISKS" before "PASS"
        if verdict_raw.startswith(key):
            findings.verdict = val
            break
    if not verdict_raw:
        # No verdict line at all → malformed/unknown.
        findings.source = "malformed" if findings.source == "live_review" else findings.source

    # Open findings: blocks beginning "### R-XXXX" with Status: Open.
    blocks = _split_finding_blocks(text)
    for block in blocks:
        status = _field_value(block, "status")
        severity = _field_value(block, "severity")
        if status != "open":
            continue
        if severity == "blocker":
            findings.open_blocker += 1
        elif severity == "high":
            findings.open_high += 1
        elif severity == "medium":
            findings.open_medium += 1
        elif severity == "low":
            findings.open_low += 1
    return findings


def _split_finding_blocks(text: str) -> list[str]:
    blocks: list[str] = []
    current: list[str] = []
    in_block = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("### R-"):
            if current:
                blocks.append("\n".join(current))
            current = [line]
            in_block = True
        elif in_block:
            if stripped.startswith("### ") or stripped.startswith("## "):
                blocks.append("\n".join(current))
                current = []
                in_block = False
            else:
                current.append(line)
    if current:
        blocks.append("\n".join(current))
    return blocks


def _field_value(block: str, field_name: str) -> str:
    needle = f"**{field_name}**".lower()
    for line in block.splitlines():
        low = line.strip().lower()
        if low.startswith("- " + needle) or low.startswith(needle):
            _, _, rhs = line.partition(":")
            return rhs.strip().lower()
    return ""


def review_findings_block_execution(findings: ReviewFindings) -> tuple[bool, str]:
    """Decide whether the review state blocks unattended execution (Step 1285).

    Blocks on: unknown/malformed verdict, PENDING, FAIL, or any open blocker/high
    finding. PASS / PASS WITH RISKS with no open blocker/high may proceed.
    """
    if findings.verdict in ("unknown",) or findings.source in ("unavailable", "malformed"):
        return True, OvernightStopReason.REVIEW_FINDINGS_OPEN
    if findings.verdict in ("pending", "fail"):
        return True, OvernightStopReason.REVIEW_FINDINGS_OPEN
    if findings.open_blocker_or_high > 0:
        return True, OvernightStopReason.REVIEW_FINDINGS_OPEN
    return False, ""


# ---------------------------------------------------------------------------
# Action selection contract (Step 1281)
# ---------------------------------------------------------------------------


def _classify_action(command: str) -> str:
    cmd = (command or "").strip()
    if "do continue" in cmd or "do --continue" in cmd:
        return OvernightActionKind.DO_CONTINUE
    if "repair propose" in cmd:
        return OvernightActionKind.REPAIR_PROPOSE
    if "patch approve" in cmd:
        return OvernightActionKind.HUMAN_APPROVAL
    if cmd:
        return OvernightActionKind.REPORT_ONLY
    return OvernightActionKind.NONE


def _entity_id_from_command(command: str, kind: str) -> str:
    """Extract the target entity from the selected command so the executed entity
    is always exactly the selected/displayed one (R-0082).

    ``remedy repair propose <job_id> <failure_artifact_id> --json`` → the fa id.
    """
    if kind != OvernightActionKind.REPAIR_PROPOSE:
        return ""
    parts = (command or "").split()
    # parts: ["remedy", "repair", "propose", "<job>", "<fa>", "--json"]
    return parts[4] if len(parts) >= 5 else ""


def _select_decision(job_id: str, data_dir: Path, policy: BoundedOvernightPolicy) -> OvernightExecutionDecision:
    """Select one safe action and decide whether it may execute (Steps 1281/1284).

    Uses the prep-layer selector for the action, then validates: the command is
    catalog-backed, the action class is policy-permitted, and execution is enabled.
    Final permission/contract/snapshot truth is re-checked by the central service
    the adapter calls — this is a pre-flight, never a substitute.
    """
    # Re-gather inputs so entity existence is current (Step 1281).
    from packages.orchestration import overnight_readiness as OV
    from packages.orchestration.do_run import validate_next_safe_action_command
    from packages.orchestration.overnight_readiness import select_overnight_next_action
    inp = OV._gather_inputs(job_id, data_dir)
    na = select_overnight_next_action(inp, job_id)
    kind = _classify_action(na.command)
    decision = OvernightExecutionDecision(
        kind=kind, label=na.label, command=na.command,
        entity_id=_entity_id_from_command(na.command, kind), allowed=False)

    # Catalog-backed check (no fake actions).
    if na.command and not validate_next_safe_action_command(na.command):
        decision.kind = OvernightActionKind.NONE
        decision.reason = "Selected command is not catalog-backed."
        decision.stop_reason = OvernightStopReason.NO_SAFE_ACTION
        return decision

    if kind == OvernightActionKind.HUMAN_APPROVAL:
        decision.reason = "A human approval is required before any execution."
        decision.stop_reason = OvernightStopReason.HUMAN_APPROVAL_REQUIRED
        return decision

    if kind == OvernightActionKind.DO_CONTINUE:
        if not (policy.allow_apply or policy.allow_repair_apply):
            decision.reason = "Policy does not permit apply (allow_apply/allow_repair_apply)."
            decision.stop_reason = OvernightStopReason.HUMAN_APPROVAL_REQUIRED
            return decision
        decision.allowed = executor_execution_permitted(policy)
        decision.stop_reason = OvernightStopReason.HUMAN_APPROVAL_REQUIRED
        decision.reason = "" if decision.allowed else "Execution not enabled (need one-cycle policy)."
        return decision

    if kind == OvernightActionKind.REPAIR_PROPOSE:
        if not policy.allow_repair_propose:
            decision.reason = "Policy does not permit repair propose (allow_repair_propose)."
            decision.stop_reason = OvernightStopReason.HUMAN_APPROVAL_REQUIRED
            return decision
        decision.allowed = executor_execution_permitted(policy)
        decision.stop_reason = OvernightStopReason.HUMAN_APPROVAL_REQUIRED
        decision.reason = "" if decision.allowed else "Execution not enabled (need one-cycle policy)."
        return decision

    # Read-only / no action: nothing to execute.
    decision.reason = "No safe automatic action; human review required."
    decision.stop_reason = OvernightStopReason.NO_SAFE_ACTION
    return decision


# ---------------------------------------------------------------------------
# Action adapters (Step 1282) — explicit, no shell, no subprocess, no generic runner.
# ---------------------------------------------------------------------------


_CONTINUE_STOP_MAP = {
    "completed_verified": OvernightStopReason.COMPLETED_VERIFIED,
    "test_failed_repair_available": OvernightStopReason.REPAIR_AVAILABLE,
    "evidence_incomplete": OvernightStopReason.EVIDENCE_INCOMPLETE,
    "snapshot_failed": OvernightStopReason.SNAPSHOT_UNVERIFIED,
    "apply_failed": OvernightStopReason.UNSUPPORTED_STATE,
    "test_blocked": OvernightStopReason.EVIDENCE_INCOMPLETE,
    "lease_unavailable": OvernightStopReason.UNSUPPORTED_STATE,
    "blocked_ineligible": OvernightStopReason.UNSUPPORTED_STATE,
    "error": OvernightStopReason.UNSUPPORTED_STATE,
}

_REPAIR_STOP_MAP = {
    "approval_required": OvernightStopReason.REPAIR_PENDING_APPROVAL,
    "fix_task_created": OvernightStopReason.REPAIR_PENDING_APPROVAL,
    "repair_builder_unavailable": OvernightStopReason.REPAIR_UNAVAILABLE,
    "blocked_ineligible": OvernightStopReason.UNSUPPORTED_STATE,
    "evidence_incomplete": OvernightStopReason.EVIDENCE_INCOMPLETE,
    "failed": OvernightStopReason.UNSUPPORTED_STATE,
    "error": OvernightStopReason.UNSUPPORTED_STATE,
}


@dataclass
class _AdapterOutcome:
    executed: bool
    stop_reason: str
    evidence_status: str
    next_command: str
    next_label: str
    ids: dict[str, str]


def _adapt_do_continue(job_id: str, data_dir: Path) -> _AdapterOutcome:
    """Run exactly one continuation cycle through the central do_continue service.

    The service owns every gate (eligibility/permission/contract/snapshot/test) and
    is itself idempotent (a retry after a successful apply does not re-apply). This
    adapter never bypasses it and never loops.
    """
    from packages.orchestration.do_continue import (
        ContinueRequest,
        export_continue_result_json,
        run_do_continue,
    )
    res = run_do_continue(ContinueRequest(job_id=job_id, source="overnight_executor_v0"), data_dir)
    data = export_continue_result_json(res)
    stop = _CONTINUE_STOP_MAP.get(res.stop_reason, OvernightStopReason.UNSUPPORTED_STATE)
    return _AdapterOutcome(
        executed=True, stop_reason=stop, evidence_status=res.evidence_status or "unknown",
        next_command=res.next_safe_action or "", next_label="Continue follow-up",
        ids={k: str(data.get(k, "")) for k in ("intent_id", "apply_id", "test_run_id",
                                               "failure_artifact_id", "proof_status")
             if data.get(k)},
    )


def _adapt_repair_propose(job_id: str, failure_artifact_id: str, data_dir: Path) -> _AdapterOutcome:
    """Create one repair PROPOSAL through the central Repair Loop v1 service.

    Docs-only fixture builder (no source rewrite, no apply, no test, no provider).
    Idempotent: a repeated propose returns the existing attempt without duplicating
    the Fix Task / Repair Artifact / Patch Intent.
    """
    from packages.orchestration.repair_loop import (
        export_repair_attempt_json,
        run_repair_attempt,
    )
    res = run_repair_attempt(
        job_id, failure_artifact_id, fixture_builder=True,
        source_fixture_builder=False, data_dir=data_dir, source="overnight_executor_v0",
    )
    data = export_repair_attempt_json(res)
    stop = _REPAIR_STOP_MAP.get(res.stop_reason, OvernightStopReason.UNSUPPORTED_STATE)
    na = data.get("next_safe_action") or {}
    return _AdapterOutcome(
        executed=True, stop_reason=stop, evidence_status=res.evidence_status or "unknown",
        next_command=na.get("command", "") if isinstance(na, dict) else "",
        next_label=na.get("label", "Approve repair") if isinstance(na, dict) else "Approve repair",
        ids={k: str(data.get(k, "")) for k in ("attempt_id", "repair_task_id",
                                               "repair_intent_id", "repair_artifact_id")
             if data.get(k)},
    )


def _first_unresolved_failure_id(job_id: str, data_dir: Path) -> str:
    from packages.orchestration import overnight_readiness as OV
    inp = OV._gather_inputs(job_id, data_dir)
    if inp is None:
        return ""
    for a in inp.failure_artifacts:
        if not (a.metadata or {}).get("failure_resolved"):
            return str(a.id)
    return ""


# ---------------------------------------------------------------------------
# Top-level executor (Steps 1283-1288)
# ---------------------------------------------------------------------------


def _checklist_pairs(readiness_export: dict[str, Any]) -> list[dict[str, str]]:
    return [{"id": c.get("id", ""), "status": c.get("status", "")}
            for c in readiness_export.get("checklist", [])]


def run_overnight_executor(
    request: OvernightRunRequest,
    data_dir: Path | None = None,
) -> OvernightRunResult:
    """Perform exactly one bounded, foreground, reviewable executor step.

    Report-only by default. Executes one allowed central-service action only when
    the policy explicitly permits it (``--allow-one-cycle`` + an action flag) and
    every gate passes (readiness, review findings, policy, central service). Never
    loops, never runs in the background, never bypasses a gate.
    """
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.storage import load_job

    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    policy = request.policy or default_overnight_policy()
    mode = (OvernightExecutionMode.EXECUTE_ONE
            if executor_execution_permitted(policy) else OvernightExecutionMode.REPORT_ONLY)

    result = OvernightRunResult(
        run_id=uuid4().hex[:12], job_id=request.job_id, created_by=request.created_by,
        mode=mode, started_at=_now(), policy_summary=_policy_summary(policy),
    )
    result._data_dir = ddir  # enable immediate per-phase checkpoint flushing
    result._checkpoint(OvernightExecutionPhase.REQUESTED, "completed")

    # ── Readiness before ────────────────────────────────────────────────
    before = build_overnight_readiness(request.job_id, ddir, policy)
    result.readiness_before = export_readiness_json(before)
    result.checklist_before = _checklist_pairs(result.readiness_before)
    result._checkpoint(OvernightExecutionPhase.READINESS_BEFORE, "completed")

    if "job_not_found" in before.blockers:
        result.stop_reason = OvernightStopReason.UNSUPPORTED_STATE
        result.evidence_status = "unknown"
        result.safe_summary = "Job not found — nothing to execute."
        return _finalize(result, ddir)

    # ── Select one action ───────────────────────────────────────────────
    decision = _select_decision(request.job_id, ddir, policy)
    result.selected_action = {"kind": decision.kind, "label": decision.label,
                              "command": decision.command}
    result._checkpoint(OvernightExecutionPhase.ACTION_SELECTED, "completed", kind=decision.kind)

    # ── Policy + review gate (Steps 1284-1285) ──────────────────────────
    findings = parse_review_findings()
    result.review_findings = findings.to_dict()
    review_blocks, review_stop = review_findings_block_execution(findings)
    budget_exhausted = "budget_exhausted" in before.blockers

    execute = decision.allowed and mode == OvernightExecutionMode.EXECUTE_ONE
    gate_stop = decision.stop_reason
    # An apply (do_continue) must not run into a blocker/high-risk state. A repair
    # PROPOSAL is the safe response to a failure, so it is gated only on blocker-
    # severity risks (integrity), not on the high risks it exists to address.
    if decision.kind == OvernightActionKind.DO_CONTINUE:
        risky = any(r.severity in ("blocker", "high") for r in before.risks)
    else:
        risky = any(r.severity == "blocker" for r in before.risks
                    if r.id != "budget_exhausted")
    # Budget (test runs / loops) only constrains the apply cycle. A repair PROPOSAL
    # consumes no test/loop budget, so an exhausted test budget does not block it.
    budget_blocks = budget_exhausted and decision.kind == OvernightActionKind.DO_CONTINUE
    if execute and review_blocks:
        execute = False
        gate_stop = review_stop
    elif execute and budget_blocks:
        execute = False
        gate_stop = OvernightStopReason.BUDGET_EXHAUSTED
    elif execute and risky:
        execute = False
        gate_stop = OvernightStopReason.MEDIUM_OR_HIGH_RISK
    result._checkpoint(OvernightExecutionPhase.POLICY_CHECKED,
                       "completed" if execute else "blocked")

    if not execute:
        result.executed_action = {"kind": OvernightActionKind.NONE}
        result.stop_reason = _canonical(gate_stop)
        result.next_safe_action = {"label": decision.label, "command": decision.command}
        result.safe_summary = _summary_for(result, decision, executed=False)
        return _finalize_after_readiness(result, request.job_id, ddir, policy)

    # ── Execute exactly one action (Step 1282) ──────────────────────────
    job = load_job(UUID(request.job_id), ddir)  # for repo key + existence
    mutates = decision.kind == OvernightActionKind.DO_CONTINUE
    lease = OvernightExecutionLease(
        job_id=request.job_id, repo_key=_repo_key(job), mutates_repo=mutates,
        lease_dir=_runs_dir(request.job_id, ddir) / "leases",
    )
    if not lease.acquire(timeout_seconds=2.0):
        result.executed_action = {"kind": OvernightActionKind.NONE}
        result.stop_reason = OvernightStopReason.UNSUPPORTED_STATE
        result.evidence_status = "unknown"
        result.safe_summary = "Another overnight run is active for this job/repo."
        result._checkpoint(OvernightExecutionPhase.LEASE_ACQUIRED, "blocked")
        return _finalize_after_readiness(result, request.job_id, ddir, policy)

    result._checkpoint(OvernightExecutionPhase.LEASE_ACQUIRED, "completed")
    try:
        result._checkpoint(OvernightExecutionPhase.ACTION_STARTED, "started", kind=decision.kind)
        try:
            if decision.kind == OvernightActionKind.DO_CONTINUE:
                outcome = _adapt_do_continue(request.job_id, ddir)
            else:  # REPAIR_PROPOSE
                # Honor the entity in the selected/validated command (R-0082); only
                # fall back to first-unresolved if the command carried none.
                fa = decision.entity_id or _first_unresolved_failure_id(request.job_id, ddir)
                if not fa:
                    outcome = _AdapterOutcome(
                        executed=False, stop_reason=OvernightStopReason.NO_SAFE_ACTION,
                        evidence_status="unknown", next_command="", next_label="", ids={})
                else:
                    outcome = _adapt_repair_propose(request.job_id, fa, ddir)
        except (OSError, ValueError, KeyError, TypeError, AttributeError, RuntimeError) as exc:
            result.error_status = type(exc).__name__
            result.executed_action = {"kind": decision.kind}
            result.stop_reason = OvernightStopReason.UNSUPPORTED_STATE
            result.evidence_status = "unknown"
            result._checkpoint(OvernightExecutionPhase.ACTION_COMPLETED, "blocked")
            result.safe_summary = "Action raised an error — stopped safely."
            return _finalize_after_readiness(result, request.job_id, ddir, policy)

        result.executed_action = {"kind": decision.kind, "label": decision.label,
                                  "command": decision.command, **outcome.ids}
        result.stop_reason = _canonical(outcome.stop_reason)
        result.evidence_status = outcome.evidence_status
        if outcome.next_command:
            result.next_safe_action = {"label": outcome.next_label, "command": outcome.next_command}
        result._checkpoint(OvernightExecutionPhase.ACTION_COMPLETED,
                           "completed" if outcome.executed else "skipped")
    finally:
        lease.release()

    result.safe_summary = _summary_for(result, decision, executed=True)
    return _finalize_after_readiness(result, request.job_id, ddir, policy)


def _finalize_after_readiness(
    result: OvernightRunResult, job_id: str, data_dir: Path, policy: BoundedOvernightPolicy
) -> OvernightRunResult:
    """Recompute readiness after the run and persist (Steps 1280/1287)."""
    after = build_overnight_readiness(job_id, data_dir, policy)
    result.readiness_after = export_readiness_json(after)
    result.checklist_after = _checklist_pairs(result.readiness_after)
    result._checkpoint(OvernightExecutionPhase.READINESS_AFTER, "completed")
    return _finalize(result, data_dir)


def _finalize(result: OvernightRunResult, data_dir: Path) -> OvernightRunResult:
    # Per-phase checkpoints are already flushed durably as they happen
    # (result._checkpoint persists immediately). Here we only write the final
    # record/report and the closing phases.
    result.completed_at = _now()
    if not result.safe_summary:
        result.safe_summary = f"Overnight run {result.run_id[:8]}: {result.stop_reason}."
    result.record_path = save_run_record(result, data_dir)
    result._checkpoint(OvernightExecutionPhase.REPORT_WRITTEN,
                       "completed" if result.record_path else "blocked")
    result._checkpoint(OvernightExecutionPhase.STOPPED, "completed")
    return result


def _summary_for(result: OvernightRunResult, decision: OvernightExecutionDecision, *, executed: bool) -> str:
    if executed:
        return (f"Executed {decision.kind} (one cycle); stop={result.stop_reason}; "
                f"evidence={result.evidence_status}.")
    return (f"Report-only: selected {decision.kind or 'none'}; not executed; "
            f"stop={result.stop_reason}.")


def _policy_summary(p: BoundedOvernightPolicy) -> dict[str, Any]:
    return {
        "max_cycles": p.max_cycles, "allow_apply": p.allow_apply,
        "allow_repair_propose": p.allow_repair_propose,
        "allow_repair_apply": p.allow_repair_apply, "allow_provider": p.allow_provider,
        "allow_revert": p.allow_revert,
        "execution_permitted": executor_execution_permitted(p),
    }


# ---------------------------------------------------------------------------
# Export / render (no raw content)
# ---------------------------------------------------------------------------


def export_run_record_json(result: OvernightRunResult) -> dict[str, Any]:
    """Durable run record (persisted). Stable schema, no raw content."""
    return {
        "version": result.version,
        "run_id": result.run_id,
        "job_id": result.job_id,
        "created_by": result.created_by,
        "mode": result.mode,
        "started_at": result.started_at,
        "completed_at": result.completed_at,
        "policy_summary": result.policy_summary,
        "selected_action": result.selected_action,
        "executed_action": result.executed_action,
        "stop_reason": result.stop_reason,
        "next_safe_action": result.next_safe_action,
        "evidence_status": result.evidence_status,
        "error_status": result.error_status,
        "review_findings": result.review_findings,
        "checklist_before": result.checklist_before,
        "checklist_after": result.checklist_after,
        "checkpoints": [
            {"phase": c.phase, "status": c.status, "at": c.at,
             "evidence_status": c.evidence_status, "ids": c.ids}
            for c in result.checkpoints
        ],
        "safe_summary": result.safe_summary,
    }


def export_run_result_json(result: OvernightRunResult) -> dict[str, Any]:
    """Full CLI-facing result (record + readiness before/after). No raw content."""
    out = export_run_record_json(result)
    out["readiness_before"] = result.readiness_before
    out["readiness_after"] = result.readiness_after
    out["record_path"] = _safe_rel(result.record_path)
    return out


def _safe_rel(path: str) -> str:
    """Reduce an absolute path to a safe, repo-relative-ish suffix (no abs paths)."""
    if not path:
        return ""
    marker = "overnight_runs"
    idx = path.find(marker)
    return path[idx:] if idx >= 0 else Path(path).name


_CHECK_ICON = {"done": "[x]", "pending": "[ ]", "blocked": "[!]", "risk": "[~]",
               "skipped": "[-]", "unknown": "[?]"}


def render_overnight_run_report_markdown(result: OvernightRunResult) -> str:
    """Morning-style report for one executor run (Step 1287). No raw content."""
    rb, ra = result.readiness_before, result.readiness_after
    lines: list[str] = []
    lines.append(f"# Overnight Run Report — job {str(result.job_id)[:8]} / run {result.run_id[:8]}")
    lines.append("")
    lines.append(f"- Mode: **{result.mode}**")
    lines.append(f"- Selected: {result.selected_action.get('kind', 'none')} "
                 f"({result.selected_action.get('command', '') or 'n/a'})")
    lines.append(f"- Executed: {result.executed_action.get('kind', 'none')}")
    lines.append(f"- Stop reason: **{result.stop_reason}**")
    lines.append(f"- Evidence: {result.evidence_status}")
    if result.error_status:
        lines.append(f"- Error: {result.error_status}")
    lines.append("")
    lines.append("## Summary")
    lines.append(result.safe_summary)
    lines.append("")
    lines.append("## Review findings (gate)")
    rf = result.review_findings or {}
    lines.append(f"- Verdict: {rf.get('verdict', 'unknown')} "
                 f"(blocker={rf.get('open_blocker', 0)}, high={rf.get('open_high', 0)})")
    lines.append("")
    lines.append("## Checklist before → after")
    after_map = {c["id"]: c["status"] for c in result.checklist_after}
    for c in result.checklist_before:
        b = c["status"]
        a = after_map.get(c["id"], b)
        arrow = f"{b} → {a}" if a != b else b
        lines.append(f"- {_CHECK_ICON.get(a, '[ ]')} {c['id']}: {arrow}")
    lines.append("")
    lines.append("## Budgets (after)")
    bs = (ra or {}).get("budget_summary", {})
    lines.append(f"- Loops: {bs.get('loops_used')}/{bs.get('max_loops')}")
    lines.append(f"- Test runs: {bs.get('test_runs_used')}/{bs.get('max_test_runs')}")
    lines.append("")
    lines.append("## Risks (after)")
    for r in (ra or {}).get("risks", []):
        lines.append(f"- ({r['severity']}) {r['summary']}")
    lines.append("")
    lines.append("## Next safe action")
    na = result.next_safe_action
    if na and na.get("command"):
        lines.append(f"- {na.get('label', 'Next')}: `{na['command']}`")
    else:
        lines.append("- (none)")
    return "\n".join(lines)


def summarize_run_result(result: OvernightRunResult) -> str:
    """Human-readable one-run summary (no raw content)."""
    lines = [
        f"overnight run: {result.job_id[:8]} / {result.run_id[:8]}",
        f"Mode: {result.mode}",
        f"Selected: {result.selected_action.get('kind', 'none')}",
        f"Executed: {result.executed_action.get('kind', 'none')}",
        f"Stop: {result.stop_reason}",
        f"Evidence: {result.evidence_status}",
    ]
    na = result.next_safe_action
    if na and na.get("command"):
        lines.append(f"Next: $ {na['command']}")
    if result.record_path:
        lines.append(f"Record: {_safe_rel(result.record_path)}")
    return "\n".join(lines)
