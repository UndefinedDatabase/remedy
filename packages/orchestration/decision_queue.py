"""
Human Decision Queue v1 — one safe surface for everything needing human attention.

Derives decisions from existing records: patch intents, stop reasons,
readiness, memory cards, repo status, worker recommendation, test runs.
Not a second source of truth — a read-only aggregation.

Public API::

    HumanDecision — frozen dataclass
    list_decisions(job, events) -> list[HumanDecision]
    get_decision(job, events, decision_id) -> HumanDecision | None
    explain_decisions(job, events) -> str
    export_decision_json(d) -> dict
    build_decision_summary(decisions) -> dict  (brain node metadata)
    sort_open_decisions_first(decisions) -> list[HumanDecision]
    open_decisions(decisions) -> list[HumanDecision]
    render_open_decisions_lines(decisions) -> list[str]  (status/report block)
    open_decisions_next_action(decisions) -> str
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from packages.core.models import Job

# F032 T001b: the import direction is ONE-WAY and stays that way —
# ``decision_evidence`` is pure and imports nothing from this module, so the
# emit gate below can live at the derivation point with no cycle to break.
from packages.orchestration.decision_evidence import (
    DECISION_EVIDENCE_STATUS_LEGACY,
    DECISION_EVIDENCE_STATUS_PRESENT,
    DecisionEvidenceTriple,
    enforce_decision_evidence,
    export_decision_evidence,
)


@dataclass(frozen=True)
class HumanDecision:
    """A single item requiring human attention."""

    id: str
    type: str  # patch_approval, stop_reason, test_failure, repo_dirty, ...
    status: str  # open, resolved
    severity: str  # info, warning, blocker
    source: str
    related_node_id: str
    related_intent_id: str
    related_file: str
    safe_summary: str
    next_actions: tuple[str, ...]
    created_at: str
    resolved_at: str | None
    #: Structured extras for decisions that carry more than a summary line.
    #: Additive (F034): every existing producer omits it and gets ``{}``.
    #: The flight-plan approval uses it to bundle the plan's open
    #: clarifications, so one decision covers the whole plan.
    payload: dict[str, Any] = field(default_factory=dict)
    #: The receipts behind this decision: refs, expected outcomes, downsides.
    #: Additive (F032 T001b) exactly as ``payload`` is: every existing producer
    #: omits it and gets ``None``, which renders as the honest legacy
    #: placeholder rather than as a fabricated triple.  IT MUST KEEP ITS
    #: DEFAULT — the twelve fields above are positionally required and a
    #: defaultless field here would break all nine construction sites at once.
    evidence: DecisionEvidenceTriple | None = None


DECISION_TYPES = frozenset({
    "patch_approval", "stop_reason", "test_failure", "repo_dirty",
    "token_budget", "worker_approval", "memory_review", "revert_missing",
    "flight_plan_approval",
    # F051: a task raised a question mid-run; its branch waits, the run does not.
    "task_decision",
})


def list_decisions(
    job: Job | Any,
    events: list[dict[str, Any]],
) -> list[HumanDecision]:
    """Derive all pending human decisions from existing state.

    Accepts both Core Job (has .id UUID) and JobPlan (has .job_id str).
    """
    decisions: list[HumanDecision] = []
    job_id = str(getattr(job, "job_id", None) or getattr(job, "id", ""))

    # 1. Pending patch approvals (Core Job only; JobPlan has no .artifacts).
    try:
        from packages.orchestration.approval_queue import APPROVAL_PENDING, list_patch_intents
        intents = list_patch_intents(job)
        for pi in intents:
            if pi.get("state") == APPROVAL_PENDING:
                decisions.append(HumanDecision(
                    id=f"pa:{pi['intent_id']}",
                    type="patch_approval",
                    status="open",
                    severity="blocker",
                    source="approval_queue",
                    related_node_id=f"pi:{pi['intent_id']}",
                    related_intent_id=pi["intent_id"],
                    related_file=pi.get("target_path", ""),
                    safe_summary=f"Patch intent for {pi.get('target_path', '?')} awaits approval.",
                    next_actions=(
                        f"remedy patch approve {job_id[:8]} {pi['intent_id']}",
                        f"remedy patch reject {job_id[:8]} {pi['intent_id']}",
                    ),
                    created_at=pi.get("created_at", ""),
                    resolved_at=None,
                ))
    except (ImportError, ValueError, OSError, AttributeError):
        pass

    # 2. Stop reasons / blockers
    try:
        from packages.orchestration.stop_reasons import derive_stop_reasons
        stops = derive_stop_reasons(job, events)
        for sr in stops:
            if sr.status == "active":
                decisions.append(HumanDecision(
                    id=f"sr:{sr.id}",
                    type="stop_reason",
                    status="open",
                    severity=sr.severity,
                    source=sr.source,
                    related_node_id=sr.related_node_id,
                    related_intent_id=sr.related_intent_id,
                    related_file=sr.related_file,
                    safe_summary=sr.safe_summary,
                    next_actions=sr.next_actions,
                    created_at=sr.created_at,
                    resolved_at=None,
                ))
    except (ImportError, ValueError, OSError, AttributeError):
        pass

    # 3. Test failures
    test_fails = [e for e in events
                  if e.get("event") == "test_run_completed"
                  and e.get("metadata", {}).get("status") == "failed"]
    for tf in test_fails[-3:]:
        meta = tf.get("metadata", {})
        cmd = str(meta.get("command", "?"))
        decisions.append(HumanDecision(
            id=f"tf:{meta.get('test_run_id', 'unknown')[:8]}",
            type="test_failure",
            status="open",
            severity="blocker",
            source="test_run",
            related_node_id="",
            related_intent_id="",
            related_file="",
            safe_summary=f"Test '{cmd}' failed.",
            next_actions=("Review test output.", f"remedy test run {job_id[:8]}"),
            created_at=str(tf.get("timestamp", "")),
            resolved_at=None,
        ))

    # 4. Dirty repo
    git_reads = [e for e in events if e.get("event") == "git_status_read"]
    if git_reads:
        last = git_reads[-1].get("metadata", {})
        if last.get("dirty"):
            decisions.append(HumanDecision(
                id="dirty_repo",
                type="repo_dirty",
                status="open",
                severity="warning",
                source="git_status",
                related_node_id="",
                related_intent_id="",
                related_file="",
                safe_summary="Target repository has uncommitted changes.",
                next_actions=("Commit or stash changes in target repo.",),
                created_at=str(git_reads[-1].get("timestamp", "")),
                resolved_at=None,
            ))

    # 5. Budget exhaustion — check job fields, metadata, AND stop events
    # JobPlan has no .metadata attribute; Core Job does. Safe for both.
    _job_meta = getattr(job, "metadata", None) or {}
    if not isinstance(_job_meta, dict):
        _job_meta = {}
    budget_error = str(
        _job_meta.get("budget_stop_reason", "")
        or _job_meta.get("error", "")
        or getattr(job, "error", "")
        or ""
    )
    if "budget_exhausted" not in budget_error:
        _stop_reason = str(getattr(job, "stop_reason", "") or "")
        _stop_source = str(getattr(job, "stop_source", "") or "")
        if "budget" in _stop_source or "budget_exhausted" in _stop_reason:
            budget_error = _stop_reason or "budget_exhausted"

    if "budget_exhausted" not in budget_error:
        for ev in events:
            if (ev.get("event") == "job_stopped"
                    and str((ev.get("metadata") or {}).get("source", "")) == "budget"):
                budget_error = str(
                    (ev.get("metadata") or {}).get("reason", "budget_exhausted"))
                break

    if budget_error and ("budget_exhausted" in budget_error or "budget" in budget_error):
        _budget_request_id = ""
        _budget_created_at = ""
        _budget_limit = ""
        for ev in events:
            if (ev.get("event") == "job_stopped"
                    and str((ev.get("metadata") or {}).get("source", "")) == "budget"):
                _budget_request_id = str(
                    (ev.get("metadata") or {}).get("request_id", ""))
                _budget_created_at = str(ev.get("timestamp", ""))
                _budget_limit = str(
                    (ev.get("metadata") or {}).get("exhausted_limit", ""))
                break
        _decision_id = (f"budget:{_budget_request_id}"
                        if _budget_request_id else "budget_exhausted")
        decisions.append(HumanDecision(
            id=_decision_id,
            type="token_budget",
            status="open",
            severity="blocker",
            source="budget_guard",
            related_node_id="",
            related_intent_id=_budget_request_id,
            related_file="",
            safe_summary=f"Job stopped: {budget_error[:200]}",
            next_actions=("extend", "abandon"),
            created_at=_budget_created_at,
            resolved_at=None,
        ))

    # 6. Stale/needs_review memory cards
    try:
        from packages.memory.local_gateway import list_memory
        entries = list_memory()
        # `validity` and `review_status` are SEPARATE fields on the memory card
        # (`packages/memory/models.py:44-45`): "needs_review" is a value of
        # `review_status` only, so reading it out of `validity` selected nothing.
        stale = [e for e in entries
                 if e.validity == "stale" or e.review_status == "needs_review"]
        for me in stale[:5]:
            decisions.append(HumanDecision(
                id=f"mem:{me.key}",
                type="memory_review",
                status="open",
                severity="info",
                source="memory",
                related_node_id="",
                related_intent_id="",
                related_file="",
                safe_summary=f"Memory '{me.key}' is {me.validity}.",
                next_actions=(f"remedy memory card-show {me.key}",),
                created_at="",
                resolved_at=None,
            ))
    except (ImportError, ValueError, OSError):
        pass

    # 7. Flight plan approval
    _flight_plan = getattr(job, "flight_plan", None)
    if isinstance(_flight_plan, dict):
        _fp_approval = _flight_plan.get("_approval")
        if _fp_approval == "pending":
            # F034: the plan's open questions ride THIS decision. One plan,
            # one human touchpoint — never one decision per question.
            from packages.orchestration.flight_plan import open_clarification_questions
            _questions = open_clarification_questions(
                _flight_plan.get("clarifications_resolved"))
            _actions = [
                f"remedy decision resolve {job_id[:8]} fp:approval --reason approve",
                f"remedy decision resolve {job_id[:8]} fp:approval --reason reject",
            ]
            # F056: intake may hint that this goal outlives one job.  The offer
            # rides THIS decision — no second human touchpoint — and it defaults
            # to NO: approving without --as-mission creates nothing.
            _intake = getattr(job, "intake", None)
            _mission_offer: dict[str, Any] = {}
            if isinstance(_intake, dict) and _intake.get("mission_candidate"):
                _mission_offer = {
                    "question": "Run as mission (a persistent goal above this job)?",
                    "default": "no",
                    "goal": str(_intake.get("goal", "") or ""),
                }
                _actions.append(
                    f"remedy decision resolve {job_id[:8]} fp:approval "
                    f"--reason approve --as-mission")
            _summary = "Flight plan awaiting approval."
            if _questions:
                _summary = (
                    f"Flight plan awaiting approval "
                    f"({len(_questions)} open question"
                    f"{'s' if len(_questions) != 1 else ''}).")
                _actions.insert(1, (
                    f"remedy decision resolve {job_id[:8]} fp:approval "
                    f"--reason approve --answer {_questions[0]['id']}=\"...\""))
            _payload: dict[str, Any] = {}
            # `options` is NOT a new vocabulary here: branch 8 already exports an
            # `options` key in its own payload below, and
            # `apps/ui/src/api/decisionCard.ts::decisionAnswers` prefers
            # `payload.options` over `next_actions` for EVERY card without
            # branching on the card's type. So the two words the write door
            # accepts (DECISION F031 D24) become this card's answer affordances
            # with no component change at all. The RESOLVED arm below carries no
            # options, because a resolved plan offers nothing to answer.
            _payload["options"] = ["approve", "reject"]
            if _questions:
                _payload["clarifications"] = _questions
            if _mission_offer:
                _payload["mission_offer"] = _mission_offer
            decisions.append(HumanDecision(
                id="fp:approval",
                type="flight_plan_approval",
                status="open",
                severity="blocker",
                source="flight_plan",
                related_node_id="",
                related_intent_id="",
                related_file="",
                safe_summary=_summary,
                next_actions=tuple(_actions),
                created_at="",
                resolved_at=None,
                payload=_payload,
            ))
        elif _fp_approval == "approved" and _flight_plan.get("_approval_audit"):
            audit = _flight_plan["_approval_audit"]
            reason = audit.get("reason", "auto-approved")
            decisions.append(HumanDecision(
                id="fp:approval",
                type="flight_plan_approval",
                status="resolved",
                severity="info",
                source="flight_plan",
                related_node_id="",
                related_intent_id="",
                related_file="",
                safe_summary=f"Flight plan {reason}.",
                next_actions=(),
                created_at="",
                resolved_at="",
            ))

    # 8. Task decisions raised mid-run (F051).  Derived from the escalation
    #    records on the job — not a second queue, the same read-only
    #    aggregation as every branch above.
    try:
        from packages.orchestration.escalation import (
            DECISION_TYPE_TASK_DECISION,
            ESCALATION_STATUS_OPEN,
            escalation_records,
            task_decision_answer_command,
        )
        for record in escalation_records(job):
            is_open = record.get("status") == ESCALATION_STATUS_OPEN
            options = [str(o) for o in (record.get("options") or [])]
            actions = tuple(
                task_decision_answer_command(job_id, str(record.get("decision_id")), opt)
                for opt in (options or ["<your answer>"])
            ) if is_open else ()
            decisions.append(HumanDecision(
                id=str(record.get("decision_id", "")),
                type=DECISION_TYPE_TASK_DECISION,
                status=ESCALATION_STATUS_OPEN if is_open else "resolved",
                severity="blocker" if is_open else "info",
                source="escalation",
                related_node_id=f"task:{str(record.get('task_id'))[:8]}",
                related_intent_id="",
                related_file="",
                safe_summary=(
                    f"Task {str(record.get('task_id'))[:8]} needs a decision: "
                    f"{record.get('question', '')}"
                    if is_open else
                    f"Task {str(record.get('task_id'))[:8]} decision answered "
                    f"({record.get('answer_source', '')}): {record.get('answer', '')}"
                ),
                next_actions=actions,
                created_at=str(record.get("created_at", "")),
                resolved_at=None if is_open else str(record.get("answered_at", "")),
                payload={
                    "task_id": str(record.get("task_id", "")),
                    "question": str(record.get("question", "")),
                    "options": options,
                    "safe_default": str(record.get("safe_default", "")),
                    "cross_references": [
                        str(x) for x in (record.get("cross_references") or [])],
                },
            ))
    except (ImportError, ValueError, OSError, AttributeError):
        pass

    # THE EMIT GATE (DECISION F032 D1): this derivation point is the one seam
    # every producer funnels through, so it is where an enforced decision type
    # is refused for arriving without its receipts.  It enforces only the types
    # in `TRIPLE_REQUIRED_TYPES`, which is EMPTY until T002 upgrades a producer.
    enforce_decision_evidence(decisions)
    return decisions


def get_decision(
    job: Job,
    events: list[dict[str, Any]],
    decision_id: str,
) -> HumanDecision | None:
    """Find a specific decision by ID."""
    for d in list_decisions(job, events):
        if d.id == decision_id:
            return d
    return None


def explain_decisions(job: Job, events: list[dict[str, Any]]) -> str:
    """Human-readable explanation of all pending decisions."""
    decisions = list_decisions(job, events)
    if not decisions:
        return f"No pending decisions for job {str(job.id)[:8]}."

    lines = [f"Human Decision Queue for {str(job.id)[:8]} ({len(decisions)} items)"]
    by_sev = {"blocker": 0, "warning": 0, "info": 0}
    for d in decisions:
        by_sev[d.severity] = by_sev.get(d.severity, 0) + 1
        status_mark = "[open]" if d.status == "open" else "[resolved]"
        lines.append(f"  {d.type} {status_mark} ({d.severity}): {d.safe_summary}")
        for a in d.next_actions[:2]:
            lines.append(f"    -> {a}")

    lines.append(f"\nSummary: {by_sev.get('blocker', 0)} blockers, "
                 f"{by_sev.get('warning', 0)} warnings, {by_sev.get('info', 0)} info")
    return "\n".join(lines)


def export_decision_json(d: HumanDecision) -> dict[str, Any]:
    """Export as safe JSON dict.

    ``evidence_refs`` and ``outcomes`` are ALWAYS present and are EMPTY when the
    decision carries no triple — never absent, because a key that appears only
    sometimes forces every reader to branch, and never fabricated, which is the
    failure mode ``docs/roadmap/features/T5_F032.md:29-31`` names.  The card's
    own ``evidence_status`` is what tells a legacy record apart from a poorly
    evidenced one (DECISION F032 D5).
    """
    wire_evidence = (
        export_decision_evidence(d.evidence)
        if d.evidence is not None
        else {"evidence_refs": [], "outcomes": []}
    )
    return {
        "id": d.id,
        "type": d.type,
        "status": d.status,
        "severity": d.severity,
        "source": d.source,
        "related_node_id": d.related_node_id,
        "related_intent_id": d.related_intent_id,
        "related_file": d.related_file,
        "safe_summary": d.safe_summary,
        "next_actions": list(d.next_actions),
        "created_at": d.created_at,
        "resolved_at": d.resolved_at,
        "payload": dict(d.payload),
        "evidence_refs": wire_evidence["evidence_refs"],
        "outcomes": wire_evidence["outcomes"],
        "evidence_status": (
            DECISION_EVIDENCE_STATUS_PRESENT
            if d.evidence is not None
            else DECISION_EVIDENCE_STATUS_LEGACY
        ),
    }


#: Severity order for the views below.  Unknown severities sort last rather
#: than raising: a decision with an odd severity must still be shown.
_SEVERITY_RANK = {"blocker": 0, "warning": 1, "info": 2}


def sort_open_decisions_first(
    decisions: list[HumanDecision],
) -> list[HumanDecision]:
    """Open before resolved, blockers before warnings before info; stable.

    Why: an unattended run's most important output is what it needs from a
    human, so every view that shows decisions shows those first (F051 T003).
    """
    return sorted(
        decisions,
        key=lambda d: (0 if d.status == "open" else 1,
                       _SEVERITY_RANK.get(d.severity, 3)),
    )


def open_decisions(decisions: list[HumanDecision]) -> list[HumanDecision]:
    """The still-open decisions, most urgent first."""
    return [d for d in sort_open_decisions_first(decisions) if d.status == "open"]


def render_open_decisions_lines(
    decisions: list[HumanDecision],
    *,
    indent: str = "  ",
) -> list[str]:
    """The block that status and report print FIRST — empty when nothing is open.

    Every line a human needs is here: what is being asked, and the exact
    command that answers it.  Nothing is truncated away: an answer command that
    is not shown in full cannot be pasted.
    """
    pending = open_decisions(decisions)
    if not pending:
        return []
    lines = [f"Open decisions: {len(pending)} — the run needs an answer"]
    for d in pending:
        lines.append(f"{indent}[{d.severity}] {d.type} {d.id}: {d.safe_summary}")
        for action in d.next_actions:
            lines.append(f"{indent}  -> {action}")
    return lines


def open_decisions_next_action(decisions: list[HumanDecision]) -> str:
    """The one command that answers the most urgent open decision, or ""."""
    for d in open_decisions(decisions):
        if d.next_actions:
            return d.next_actions[0]
    return ""


def build_decision_summary(decisions: list[HumanDecision]) -> dict[str, Any]:
    """Build safe metadata for brain node."""
    open_decisions = [d for d in decisions if d.status == "open"]
    by_sev = {"blocker": 0, "warning": 0, "info": 0}
    for d in open_decisions:
        by_sev[d.severity] = by_sev.get(d.severity, 0) + 1
    total_next = sum(len(d.next_actions) for d in open_decisions)
    return {
        "open_count": len(open_decisions),
        "high_count": by_sev.get("blocker", 0),
        "medium_count": by_sev.get("warning", 0),
        "low_count": by_sev.get("info", 0),
        "next_action_count": total_next,
    }
