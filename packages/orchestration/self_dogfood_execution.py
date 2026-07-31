"""
Self-Dogfood Execution v0 (Steps 1429-1464).

After a human approves a self-dogfood ProposedTask, create + track a bounded
SelfImprovementAttempt that routes work through the EXISTING safe systems — it never
bypasses a gate, never edits code, never applies, never approves:

    approved ProposedTask (origin self_dogfood)
      → SelfImprovementAttempt
      → safe request package (no FailureArtifact required)
      → awaiting_external_candidate
      → [human relays request; candidate re-enters via provider intake-repair]
      → Provider Trust Gate → materialized PENDING intent
      → [human] remedy patch approve → remedy do continue
      → snapshot → apply → test → proof
      → reconcile → completed

This is an orchestrator / tracking rail. No provider/model/network/subprocess/
browser. No direct source_apply/patch_apply. No git ops, no PR, no main mutation, no
Job.tasks insertion. Mutation-capable execution is refused on main/master/unknown
branch. pending intent ≠ completed; no test/proof overclaim.

Public API::

    evaluate_self_execution_eligibility(proposed_task_id, job_id=None, data_dir=None) -> SelfExecEligibility
    start_self_execution(proposed_task_id, job_id=None, data_dir=None) -> SelfImprovementAttemptResult
    reconcile_self_attempt(attempt_id, data_dir=None) -> SelfImprovementAttemptResult
    list_attempts(data_dir=None) -> list[dict]
    get_attempt(attempt_id, data_dir=None) -> dict | None
    self_integrity_check(data_dir=None) -> dict
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

# ---------------------------------------------------------------------------
# Vocabularies (Steps 1430/1434)
# ---------------------------------------------------------------------------


class AttemptState:
    PROPOSED = "proposed"
    APPROVED = "approved"
    REQUEST_PREPARED = "request_prepared"
    AWAITING_EXTERNAL_CANDIDATE = "awaiting_external_candidate"
    CANDIDATE_IMPORTED = "candidate_imported"
    TRUST_REJECTED = "trust_rejected"
    TRUST_NEEDS_REVIEW = "trust_needs_review"
    INTENT_PENDING_APPROVAL = "intent_pending_approval"
    INTENT_APPROVED = "intent_approved"
    APPLY_STARTED = "apply_started"
    APPLIED = "applied"
    TESTED_PASSED = "tested_passed"
    TESTED_FAILED = "tested_failed"
    PROOF_VERIFIED = "proof_verified"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    EVIDENCE_INCOMPLETE = "evidence_incomplete"


_TERMINAL = frozenset({AttemptState.COMPLETED})
# Non-resumable error/terminal-ish states still allow reconcile but not a fresh start.
_ACTIVE = frozenset({
    AttemptState.PROPOSED, AttemptState.APPROVED, AttemptState.REQUEST_PREPARED,
    AttemptState.AWAITING_EXTERNAL_CANDIDATE, AttemptState.CANDIDATE_IMPORTED,
    AttemptState.TRUST_NEEDS_REVIEW, AttemptState.INTENT_PENDING_APPROVAL,
    AttemptState.INTENT_APPROVED, AttemptState.APPLY_STARTED, AttemptState.APPLIED,
    AttemptState.TESTED_PASSED, AttemptState.PROOF_VERIFIED,
})

# Legal forward transitions (idempotent self-transition always allowed).
_TRANSITIONS: dict[str, frozenset[str]] = {
    AttemptState.PROPOSED: frozenset({AttemptState.APPROVED, AttemptState.BLOCKED}),
    AttemptState.APPROVED: frozenset({AttemptState.REQUEST_PREPARED, AttemptState.BLOCKED}),
    AttemptState.REQUEST_PREPARED: frozenset({AttemptState.AWAITING_EXTERNAL_CANDIDATE, AttemptState.BLOCKED}),
    AttemptState.AWAITING_EXTERNAL_CANDIDATE: frozenset({
        AttemptState.CANDIDATE_IMPORTED, AttemptState.TRUST_REJECTED,
        AttemptState.TRUST_NEEDS_REVIEW, AttemptState.INTENT_PENDING_APPROVAL,
        AttemptState.BLOCKED}),
    AttemptState.CANDIDATE_IMPORTED: frozenset({
        AttemptState.TRUST_REJECTED, AttemptState.TRUST_NEEDS_REVIEW,
        AttemptState.INTENT_PENDING_APPROVAL, AttemptState.BLOCKED}),
    AttemptState.TRUST_NEEDS_REVIEW: frozenset({AttemptState.INTENT_PENDING_APPROVAL, AttemptState.BLOCKED}),
    AttemptState.INTENT_PENDING_APPROVAL: frozenset({
        AttemptState.INTENT_APPROVED, AttemptState.BLOCKED}),
    # COMPLETED is reachable ONLY via PROOF_VERIFIED (R-0085): no jump to completed
    # from intent-approved/tested without an authoritative verified proof.
    AttemptState.INTENT_APPROVED: frozenset({
        AttemptState.APPLY_STARTED, AttemptState.APPLIED, AttemptState.TESTED_PASSED,
        AttemptState.TESTED_FAILED, AttemptState.PROOF_VERIFIED,
        AttemptState.EVIDENCE_INCOMPLETE, AttemptState.BLOCKED}),
    AttemptState.APPLY_STARTED: frozenset({
        AttemptState.APPLIED, AttemptState.TESTED_PASSED, AttemptState.TESTED_FAILED,
        AttemptState.PROOF_VERIFIED, AttemptState.EVIDENCE_INCOMPLETE, AttemptState.BLOCKED}),
    AttemptState.APPLIED: frozenset({
        AttemptState.TESTED_PASSED, AttemptState.TESTED_FAILED, AttemptState.PROOF_VERIFIED,
        AttemptState.EVIDENCE_INCOMPLETE, AttemptState.BLOCKED}),
    AttemptState.TESTED_PASSED: frozenset({
        AttemptState.PROOF_VERIFIED, AttemptState.EVIDENCE_INCOMPLETE}),
    AttemptState.TESTED_FAILED: frozenset({AttemptState.BLOCKED, AttemptState.EVIDENCE_INCOMPLETE}),
    AttemptState.PROOF_VERIFIED: frozenset({AttemptState.COMPLETED}),
    AttemptState.TRUST_REJECTED: frozenset({AttemptState.BLOCKED}),
    AttemptState.EVIDENCE_INCOMPLETE: frozenset({AttemptState.BLOCKED}),
    AttemptState.BLOCKED: frozenset(),
    AttemptState.COMPLETED: frozenset(),
}


class StopReason:
    OK = "ok"
    AWAITING_EXTERNAL_CANDIDATE = "awaiting_external_candidate"
    PROPOSED_TASK_NOT_FOUND = "proposed_task_not_found"
    NOT_SELF_DOGFOOD = "not_self_dogfood"
    NOT_APPROVED = "not_approved"
    DUPLICATE_ACTIVE_ATTEMPT = "duplicate_active_attempt"
    REVIEW_FINDINGS_OPEN = "review_findings_open"
    CONTRACT_BLOCKED = "contract_blocked"
    MAIN_BRANCH_UNSAFE = "main_branch_unsafe"
    NO_TARGET_REPO = "no_target_repo"
    NO_JOB = "no_job"
    INTENT_PENDING_APPROVAL = "intent_pending_approval"
    INTENT_APPROVED = "intent_approved"
    COMPLETED = "completed"
    BLOCKED = "blocked"


# ---------------------------------------------------------------------------
# Models (Step 1430)
# ---------------------------------------------------------------------------


@dataclass
class SelfImprovementCheckpoint:
    phase: str
    status: str
    at: str
    ids: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {"phase": self.phase, "status": self.status, "at": self.at, "ids": self.ids}


@dataclass
class SelfImprovementLinkage:
    proposed_task_id: str = ""
    self_item_id: str = ""
    item_fingerprint: str = ""
    request_package_id: str = ""
    external_candidate_intake_id: str = ""
    provider_trust_report_id: str = ""
    provider_material_id: str = ""
    patch_intent_id: str = ""
    apply_id: str = ""
    test_run_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "proposed_task_id": self.proposed_task_id, "self_item_id": self.self_item_id,
            "item_fingerprint": self.item_fingerprint,
            "request_package_id": self.request_package_id,
            "external_candidate_intake_id": self.external_candidate_intake_id,
            "provider_trust_report_id": self.provider_trust_report_id,
            "provider_material_id": self.provider_material_id,
            "patch_intent_id": self.patch_intent_id, "apply_id": self.apply_id,
            "test_run_id": self.test_run_id,
        }


@dataclass
class SelfImprovementAttempt:
    attempt_id: str
    job_id: str = ""
    proposed_task_id: str = ""
    self_item_id: str = ""
    item_fingerprint: str = ""
    request_package_id: str = ""
    external_candidate_intake_id: str = ""
    provider_trust_report_id: str = ""
    provider_material_id: str = ""
    patch_intent_id: str = ""
    apply_id: str = ""
    test_run_id: str = ""
    proof_status: str = "unknown"
    state: str = AttemptState.PROPOSED
    stop_reason: str = ""
    evidence_status: str = "complete"
    next_safe_action: str = ""
    title: str = ""
    checkpoints: list[SelfImprovementCheckpoint] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "attempt_id": self.attempt_id, "job_id": self.job_id,
            "proposed_task_id": self.proposed_task_id, "self_item_id": self.self_item_id,
            "item_fingerprint": self.item_fingerprint,
            "request_package_id": self.request_package_id,
            "external_candidate_intake_id": self.external_candidate_intake_id,
            "provider_trust_report_id": self.provider_trust_report_id,
            "provider_material_id": self.provider_material_id,
            "patch_intent_id": self.patch_intent_id, "apply_id": self.apply_id,
            "test_run_id": self.test_run_id, "proof_status": self.proof_status,
            "state": self.state, "stop_reason": self.stop_reason,
            "evidence_status": self.evidence_status, "next_safe_action": self.next_safe_action,
            "title": self.title,
            "checkpoints": [c.to_dict() for c in self.checkpoints],
            "created_at": self.created_at, "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> SelfImprovementAttempt:
        cps = [SelfImprovementCheckpoint(**c) for c in d.get("checkpoints", [])]
        return cls(**{**{k: v for k, v in d.items() if k != "checkpoints"}, "checkpoints": cps})


@dataclass
class SelfExecEligibility:
    eligible: bool = False
    proposed_task_id: str = ""
    job_id: str = ""
    item_fingerprint: str = ""
    existing_attempt_id: str = ""
    blockers: list[str] = field(default_factory=list)
    stop_reason: str = ""
    next_safe_action: str = ""
    safe_summary: str = ""


@dataclass
class SelfImprovementAttemptResult:
    attempt_id: str = ""
    job_id: str = ""
    proposed_task_id: str = ""
    state: str = ""
    stop_reason: str = ""
    evidence_status: str = "complete"
    next_safe_action: str = ""
    request_package_id: str = ""
    patch_intent_id: str = ""
    proof_status: str = "unknown"
    safe_summary: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "attempt_id": self.attempt_id, "job_id": self.job_id,
            "proposed_task_id": self.proposed_task_id, "state": self.state,
            "stop_reason": self.stop_reason, "evidence_status": self.evidence_status,
            "next_safe_action": self.next_safe_action,
            "request_package_id": self.request_package_id,
            "patch_intent_id": self.patch_intent_id, "proof_status": self.proof_status,
            "safe_summary": self.safe_summary,
        }


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _self_provider_label(attempt_id: str) -> str:
    """Provider label that correlates an imported candidate to THIS attempt (R-0084)."""
    return f"self_dogfood:{attempt_id}"


def _scrub(text: str) -> str:
    from packages.orchestration.provider_trust import _scrub_public
    return _scrub_public(str(text))[:300]


# ---------------------------------------------------------------------------
# Branch / main safety (Step 1433) — read the repo HEAD file only, no
# subprocess. Worktree-safe since the R-0159 fix: accepts both `.git` forms.
# ---------------------------------------------------------------------------


def _git_head_file() -> Path | None:
    """HEAD location for both repo forms: `.git` directory (normal
    checkout) or `.git` gitfile pointer (linked worktree, R-0159)."""
    dot_git = Path(".git")
    if dot_git.is_dir():
        return dot_git / "HEAD"
    if dot_git.is_file():
        try:
            text = dot_git.read_text(encoding="utf-8",
                                     errors="replace").strip()
        except OSError:
            return None
        if text.startswith("gitdir: "):
            gitdir = Path(text[len("gitdir: "):].strip())
            if not gitdir.is_absolute():
                gitdir = dot_git.parent / gitdir
            return gitdir / "HEAD"
    return None


def current_branch() -> str:
    """Return the current git branch from the repo's HEAD file, or ""
    if unknown/detached. No subprocess, no git invocation. Accepts a
    `.git` directory and a linked worktree's gitfile pointer (R-0159)."""
    try:
        head = _git_head_file()
        if head is None or not head.exists():
            return ""
        text = head.read_text(encoding="utf-8", errors="replace").strip()
        if text.startswith("ref: refs/heads/"):
            return text[len("ref: refs/heads/"):].strip()
        return ""  # detached HEAD → unknown
    except OSError:
        return ""


def _branch_is_mutation_safe() -> bool:
    b = current_branch()
    return bool(b) and b not in ("main", "master")


# ---------------------------------------------------------------------------
# Storage (Step 1431)
# ---------------------------------------------------------------------------


def _attempts_root(data_dir: Path) -> Path:
    return data_dir / "self_dogfood" / "attempts"


def _attempt_dir(attempt_id: str, data_dir: Path) -> Path:
    return _attempts_root(data_dir) / attempt_id


def _atomic_write(path: Path, data: bytes, mode: int = 0o600) -> bool:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_bytes(data)
        try:
            os.chmod(tmp, mode)
        except OSError:
            pass
        os.replace(tmp, path)
        try:
            os.chmod(path, mode)
        except OSError:
            pass
        return True
    except OSError:
        return False


def save_attempt(attempt: SelfImprovementAttempt, data_dir: Path) -> bool:
    attempt.updated_at = _now()
    adir = _attempt_dir(attempt.attempt_id, data_dir)
    return _atomic_write(adir / "attempt.json",
                         json.dumps(attempt.to_dict(), indent=2, sort_keys=True).encode("utf-8"))


def get_attempt(attempt_id: str, data_dir: Path | None = None) -> dict | None:
    from packages.orchestration.data_paths import resolve_data_root
    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    p = _attempt_dir(attempt_id, ddir) / "attempt.json"
    try:
        return json.loads(p.read_bytes())
    except (OSError, json.JSONDecodeError):
        return None


def _load_attempt(attempt_id: str, data_dir: Path) -> SelfImprovementAttempt | None:
    d = get_attempt(attempt_id, data_dir)
    return SelfImprovementAttempt.from_dict(d) if d else None


def list_attempts(data_dir: Path | None = None) -> list[dict]:
    from packages.orchestration.data_paths import resolve_data_root
    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    base = _attempts_root(ddir)
    if not base.is_dir():
        return []
    out: list[dict] = []
    try:
        for p in sorted(base.iterdir()):
            d = get_attempt(p.name, ddir)
            if d:
                out.append(d)
    except OSError:
        return []
    return out


def _find_attempt_by_fingerprint(fingerprint: str, data_dir: Path) -> dict | None:
    for a in list_attempts(data_dir):
        if a.get("item_fingerprint") == fingerprint:
            return a
    return None


def _transition(attempt: SelfImprovementAttempt, target: str) -> bool:
    """Apply a legal state transition (idempotent self-transition allowed)."""
    if target == attempt.state:
        return True
    if target in _TRANSITIONS.get(attempt.state, frozenset()):
        attempt.checkpoints.append(SelfImprovementCheckpoint(
            phase=target, status="entered", at=_now()))
        attempt.state = target
        return True
    return False


# ---------------------------------------------------------------------------
# Eligibility (Step 1432) + branch gate (1433)
# ---------------------------------------------------------------------------

_SELF_DOGFOOD_PREFIX = "self_dogfood:"


def _review_blocks() -> tuple[bool, str]:
    from packages.orchestration.overnight_executor import (
        parse_review_findings,
        review_findings_block_execution,
    )
    agent_dir = Path(os.environ.get("REMEDY_AGENT_DIR") or ".agent")
    return review_findings_block_execution(parse_review_findings(agent_dir / "live_review.md"))


def evaluate_self_execution_eligibility(
    proposed_task_id: str, job_id: str | None = None, data_dir: Path | None = None,
) -> SelfExecEligibility:
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.proposed_tasks import (
        ProposedTaskStatus,
        get_proposed_task,
    )
    from packages.orchestration.run_contract import (
        ContractAction,
        ensure_contract,
        evaluate_run_action,
    )
    from packages.orchestration.storage import JobNotFoundError, load_job

    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    elig = SelfExecEligibility(proposed_task_id=proposed_task_id)

    # Resolve job: ProposedTasks are stored per job, so we need the job id.
    jid = job_id or ""
    task = None
    if jid:
        task = get_proposed_task(jid, proposed_task_id, ddir)
    if task is None:
        # Scan jobs is out of scope; require an explicit job for v0.
        elig.blockers.append("proposed_task_not_found")
        elig.stop_reason = StopReason.PROPOSED_TASK_NOT_FOUND
        elig.next_safe_action = "remedy decision list <job_id> --json"
        elig.safe_summary = "Proposed task not found (provide --job-id)."
        return elig
    elig.job_id = jid

    if getattr(task, "task_type", "") != "self_dogfood":
        elig.blockers.append("not_self_dogfood")
        elig.stop_reason = StopReason.NOT_SELF_DOGFOOD
        elig.next_safe_action = "remedy self inspect --json"
        elig.safe_summary = "Proposed task is not a self-dogfood task."
        return elig

    if task.status != ProposedTaskStatus.APPROVED_FOR_BUILD:
        elig.blockers.append("not_approved")
        elig.stop_reason = StopReason.NOT_APPROVED
        elig.next_safe_action = f"remedy decision list {jid} --json"
        elig.safe_summary = "Proposed task is not approved for build."
        return elig

    fp = (task.origin_recommendation_id or "")
    if fp.startswith(_SELF_DOGFOOD_PREFIX):
        fp = fp[len(_SELF_DOGFOOD_PREFIX):]
    elig.item_fingerprint = fp

    # Review must not be PENDING/FAIL/open blocker-high.
    blocked, _ = _review_blocks()
    if blocked:
        elig.blockers.append("review_findings_open")
        elig.stop_reason = StopReason.REVIEW_FINDINGS_OPEN
        elig.next_safe_action = "remedy self inspect --json"
        elig.safe_summary = "Live review is PENDING/FAIL/open blocker-high."
        return elig

    # Contract gate.
    try:
        job = load_job(UUID(jid), ddir)
    except (ValueError, JobNotFoundError):
        elig.blockers.append("no_job")
        elig.stop_reason = StopReason.NO_JOB
        elig.next_safe_action = "remedy job list --json"
        elig.safe_summary = "Job not found."
        return elig
    contract = ensure_contract(job)
    if not evaluate_run_action(contract, ContractAction.SELF_EXECUTE_PREPARE).allowed:
        elig.blockers.append("contract_blocked")
        elig.stop_reason = StopReason.CONTRACT_BLOCKED
        elig.next_safe_action = f"remedy contract inspect {jid} --json"
        elig.safe_summary = "Contract denies self execution preparation."
        return elig

    # Target repo + branch safety (mutation-capable chain).
    if not (job.metadata or {}).get("target_repo"):
        elig.blockers.append("no_target_repo")
        elig.stop_reason = StopReason.NO_TARGET_REPO
        elig.next_safe_action = f"remedy job attach-repo {jid} <path>"
        elig.safe_summary = "No target repository attached."
        return elig
    if not _branch_is_mutation_safe():
        elig.blockers.append("main_branch_unsafe")
        elig.stop_reason = StopReason.MAIN_BRANCH_UNSAFE
        elig.next_safe_action = "remedy self status --json"
        elig.safe_summary = ("Self execution refuses main/master/unknown branch "
                             "(would lead to a mutation-capable apply).")
        return elig

    # No active unresolved attempt for the same fingerprint (unless resuming it).
    existing = _find_attempt_by_fingerprint(fp, ddir) if fp else None
    if existing and existing.get("state") in _ACTIVE:
        elig.existing_attempt_id = existing.get("attempt_id", "")
        # Resuming is allowed; signal it (not a blocker).
    elig.eligible = True
    elig.safe_summary = "Eligible for self execution preparation."
    return elig


# ---------------------------------------------------------------------------
# Self request package (Step 1435) — no FailureArtifact required.
# ---------------------------------------------------------------------------

_CANDIDATE_SCHEMA = {
    "summary": "<one-line safe summary>",
    "target_files": ["relative/path.md"],
    "patch_format": "unified_diff",
    "unified_diff": "<a single unified diff>",
    "rationale": "<why this implements the improvement>",
    "risk_notes": "<risks/uncertainty>",
}


def _build_self_request_text(item: Any, job_id: str) -> str:
    schema = json.dumps(_CANDIDATE_SCHEMA, indent=2)
    title = _scrub(getattr(item, "title", "") or "Self-improvement")
    detail = _scrub(getattr(item, "detail", ""))
    itype = getattr(item, "item_type", "")
    prio = getattr(item, "priority", "")
    conf = getattr(item, "confidence", "")
    constraints = [
        "Return EXACTLY ONE candidate change. No alternatives.",
        "Use ONLY relative repo paths. No absolute paths, no traversal.",
        "v0 can only auto-apply a SINGLE Markdown (.md) create or modify.",
        "No secrets, tokens, credentials, or .env values.",
        "No protected files (.env, .git, node_modules, caches, lock files).",
        "Do NOT claim the change was applied or tested.",
        "No raw stdout/stderr, tracebacks, or unrelated prose.",
    ]
    lines = [
        f"# Self-improvement request — {title}", "",
        "You are an EXTERNAL candidate generator. Produce a safe candidate change for "
        "the self-improvement below. Your output is UNTRUSTED and will be quarantined "
        "and validated before any use.", "",
        "## Item", f"type: {itype}\npriority: {prio}\nconfidence: {conf}", "",
        "## Detail", detail or "(none)", "",
        "## Expected outcome",
        "A safe, minimal change that addresses the item (docs/markdown in v0).", "",
        "## Constraints", "\n".join(f"- {c}" for c in constraints), "",
        "## Required response format",
        "Return either a single JSON object:\n```json\n" + schema + "\n```\n"
        "OR a single fenced unified diff:\n```diff\n<one unified diff>\n```", "",
        "## How Remedy will handle your output",
        "Quarantined + trust-validated; an accepted candidate becomes a PENDING patch "
        "intent that a human must approve before anything is applied via `do continue`.",
    ]
    return "\n".join(lines)


def _store_request(attempt_id: str, data_dir: Path, text: str) -> str:
    rpid = uuid4().hex[:16]
    rdir = _attempt_dir(attempt_id, data_dir)
    _atomic_write(rdir / "request.md", text.encode("utf-8", errors="replace"))
    return rpid


# ---------------------------------------------------------------------------
# Start / resume (Steps 1432/1434/1435/1436)
# ---------------------------------------------------------------------------


def _result_from_attempt(a: SelfImprovementAttempt) -> SelfImprovementAttemptResult:
    return SelfImprovementAttemptResult(
        attempt_id=a.attempt_id, job_id=a.job_id, proposed_task_id=a.proposed_task_id,
        state=a.state, stop_reason=a.stop_reason, evidence_status=a.evidence_status,
        next_safe_action=a.next_safe_action, request_package_id=a.request_package_id,
        patch_intent_id=a.patch_intent_id, proof_status=a.proof_status,
        safe_summary=f"Self attempt {a.attempt_id[:8]}: {a.state}.")


def start_self_execution(
    proposed_task_id: str, job_id: str | None = None, data_dir: Path | None = None,
) -> SelfImprovementAttemptResult:
    """Create or resume a SelfImprovementAttempt and prepare a request package.
    Stops at awaiting_external_candidate. No apply, no provider, no approval."""
    from packages.orchestration import self_dogfood as SD
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.proposed_tasks import get_proposed_task

    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    elig = evaluate_self_execution_eligibility(proposed_task_id, job_id, ddir)
    if not elig.eligible:
        r = SelfImprovementAttemptResult(
            proposed_task_id=proposed_task_id, job_id=elig.job_id, state=AttemptState.BLOCKED,
            stop_reason=elig.stop_reason, next_safe_action=elig.next_safe_action,
            evidence_status="unknown", safe_summary=elig.safe_summary)
        return r

    jid = elig.job_id

    # Resume an existing active attempt for this fingerprint.
    if elig.existing_attempt_id:
        a = _load_attempt(elig.existing_attempt_id, ddir)
        if a is not None:
            return _result_from_attempt(a)

    # Resolve the self-improvement item (for the request) from current inspection.
    item = None
    try:
        insp = SD.build_self_dogfood_inspection(jid, ddir)
        item = next((i for i in insp.items if i.fingerprint == elig.item_fingerprint), None)
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        item = None

    task = get_proposed_task(jid, proposed_task_id, ddir)
    attempt = SelfImprovementAttempt(
        attempt_id=uuid4().hex[:16], job_id=jid, proposed_task_id=proposed_task_id,
        self_item_id=elig.item_fingerprint, item_fingerprint=elig.item_fingerprint,
        title=_scrub(getattr(task, "title", "") or (getattr(item, "title", "") if item else "")),
        state=AttemptState.PROPOSED, created_at=_now(),
    )
    _transition(attempt, AttemptState.APPROVED)

    # Build + store request package.
    text = _build_self_request_text(item if item is not None else task, jid)
    attempt.request_package_id = _store_request(attempt.attempt_id, ddir, text)
    _transition(attempt, AttemptState.REQUEST_PREPARED)
    _transition(attempt, AttemptState.AWAITING_EXTERNAL_CANDIDATE)
    attempt.stop_reason = StopReason.AWAITING_EXTERNAL_CANDIDATE
    attempt.next_safe_action = (
        f"remedy provider intake-repair {jid} --input <response_file> "
        f"--provider {_self_provider_label(attempt.attempt_id)} --json")
    save_attempt(attempt, ddir)
    return _result_from_attempt(attempt)


# ---------------------------------------------------------------------------
# Reconcile (Step 1441) — refresh attempt state from durable truth. No apply.
# ---------------------------------------------------------------------------


def reconcile_self_attempt(
    attempt_id: str, data_dir: Path | None = None,
) -> SelfImprovementAttemptResult:
    """Refresh an attempt's state from existing durable truth (ProposedTask, provider
    trust reports, materialization, patch intent approval, proof). Never applies,
    approves, runs tests, or calls a provider."""
    from packages.orchestration.approval_queue import APPROVAL_APPROVED, get_patch_intent
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.provider_trust import load_trust_reports
    from packages.orchestration.storage import JobNotFoundError, load_job

    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    a = _load_attempt(attempt_id, ddir)
    if a is None:
        return SelfImprovementAttemptResult(
            attempt_id=attempt_id, state=AttemptState.BLOCKED,
            stop_reason="attempt_not_found", evidence_status="unknown",
            next_safe_action="remedy self status --json",
            safe_summary="Self attempt not found.")
    if a.state in _TERMINAL:
        return _result_from_attempt(a)

    try:
        job = load_job(UUID(a.job_id), ddir)
    except (ValueError, JobNotFoundError):
        a.stop_reason = StopReason.NO_JOB
        save_attempt(a, ddir)
        return _result_from_attempt(a)

    # Link a materialized provider intent — DETERMINISTICALLY (R-0084). The candidate
    # for THIS attempt must be imported with provider label "self_dogfood:<attempt_id>"
    # (the exact label the request's intake command supplies), so we only link a trust
    # report whose provider_name matches this attempt. No cross-attempt mislink.
    if not a.patch_intent_id:
        want_provider = _self_provider_label(a.attempt_id)
        linked_intents = {x.get("patch_intent_id") for x in list_attempts(ddir)
                          if x.get("attempt_id") != a.attempt_id and x.get("patch_intent_id")}
        reports = sorted(load_trust_reports(job).values(),
                         key=lambda r: r.get("received_at", ""))
        for rep in reversed(reports):
            iid = rep.get("repair_intent_id", "")
            if (iid and iid not in linked_intents
                    and rep.get("provider_name", "") == want_provider):
                a.patch_intent_id = iid
                a.provider_trust_report_id = rep.get("report_id", "")
                a.provider_material_id = rep.get("material_id", "")
                _transition(a, AttemptState.CANDIDATE_IMPORTED)
                _transition(a, AttemptState.INTENT_PENDING_APPROVAL)
                break

    if a.patch_intent_id:
        intent = get_patch_intent(job, a.patch_intent_id)
        if intent is None:
            a.stop_reason = StopReason.BLOCKED
        else:
            if intent.get("state") == APPROVAL_APPROVED and a.state == AttemptState.INTENT_PENDING_APPROVAL:
                _transition(a, AttemptState.INTENT_APPROVED)
            # Proof from authoritative chain for this intent.
            proof = _intent_proof_status(job, a.patch_intent_id, ddir)
            a.proof_status = proof
            if proof == "verified":
                _transition(a, AttemptState.PROOF_VERIFIED)
                _transition(a, AttemptState.COMPLETED)
                a.stop_reason = StopReason.COMPLETED
            elif proof in ("failed",):
                a.evidence_status = "degraded"

    # Set next safe action by state.
    a.next_safe_action = _next_action_for(a)
    if not a.stop_reason:
        a.stop_reason = a.state
    save_attempt(a, ddir)
    return _result_from_attempt(a)


def _intent_proof_status(job: Any, intent_id: str, data_dir: Path) -> str:
    try:
        from packages.orchestration.proof_chain import build_proof_chain
        from packages.orchestration.timeline import load_run_events
        events = load_run_events(data_dir, UUID(str(job.id)))
        chain = build_proof_chain(job, events, data_dir=data_dir)
        change = next((c for c in chain.changes if c.intent_id == intent_id), None)
        if change is not None:
            return change.proof_status
        return chain.overall_status if chain.changes else "unknown"
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        return "unknown"


def _next_action_for(a: SelfImprovementAttempt) -> str:
    s = a.state
    if s == AttemptState.AWAITING_EXTERNAL_CANDIDATE:
        return (f"remedy provider intake-repair {a.job_id} --input <response_file> "
                f"--provider {_self_provider_label(a.attempt_id)} --json")
    if s == AttemptState.INTENT_PENDING_APPROVAL and a.patch_intent_id:
        return f"remedy patch approve {a.job_id} {a.patch_intent_id} --json"
    if s == AttemptState.INTENT_APPROVED and a.patch_intent_id:
        return f"remedy do continue {a.job_id} --intent-id {a.patch_intent_id} --json"
    if s == AttemptState.COMPLETED:
        return f"remedy self status --attempt-id {a.attempt_id} --json"
    return f"remedy self reconcile {a.attempt_id} --json"


# ---------------------------------------------------------------------------
# Self integrity (Step 1462) — read-only
# ---------------------------------------------------------------------------


def self_integrity_check(data_dir: Path | None = None) -> dict[str, Any]:
    attempts = list_attempts(data_dir)
    fps: dict[str, int] = {}
    issues: list[str] = []
    for a in attempts:
        fp = a.get("item_fingerprint", "")
        fps[fp] = fps.get(fp, 0) + 1
        if a.get("state") in _ACTIVE and not a.get("request_package_id"):
            issues.append(f"attempt_missing_request:{a.get('attempt_id','')[:8]}")
        if a.get("state") == AttemptState.COMPLETED and a.get("proof_status") != "verified":
            issues.append(f"completed_without_proof:{a.get('attempt_id','')[:8]}")
    dups = [fp for fp, n in fps.items() if fp and n > 1]
    if dups:
        issues.append(f"duplicate_fingerprints:{len(dups)}")
    on_main = not _branch_is_mutation_safe() and any(a.get("state") in _ACTIVE for a in attempts)
    if on_main:
        issues.append("active_attempt_on_main")
    return {"attempt_count": len(attempts), "issue_count": len(issues),
            "issues": issues, "passed": not issues}


# ---------------------------------------------------------------------------
# Exports
# ---------------------------------------------------------------------------


def export_result_json(result: SelfImprovementAttemptResult) -> dict[str, Any]:
    return result.to_dict()


def export_attempt_safe(d: dict) -> dict[str, Any]:
    """Public-safe attempt view (drops nothing sensitive — attempts hold IDs only)."""
    return d
