"""Completion/return digest — the one-glance answer to "what happened while I was gone" (F040 T001).

PURE COMPOSITION over sources that already exist.  This module owns no storage,
writes no file, starts no subprocess and opens no socket: it reads the report's
own source set, the decision inbox's read path and the job's persisted budget
actuals, and turns the three into one small envelope.  A digest that persisted
anything would be a SECOND source of truth for state that already has one, and
the whole point of the feature is that there is only one.

THE ONE-SOURCE PROPERTY, which is what this module exists to protect: the
primary action comes VERBATIM from ``run_report.recommended_next_action``.  This
module never decides an action, never adds a rule, never reorders the table and
never special-cases a state — so the hero card's call to action and the run
report's recommendation are incapable of disagreeing.  A reader who wants to
change what Remedy recommends changes ``NEXT_ACTION_RULES`` in
``packages/orchestration/run_report.py`` and nothing here.

Deliberate absences (searched-for behavior that is NOT here):
  * Remedy deliberately does not emit a ``deep_link`` (DECISION F040 D5): the
    cockpit has no routing layer, so the envelope names the RULE and the client
    decides the affordance.  There is no always-null key to misread.
  * Remedy deliberately does not fill ``ownership`` (DECISION F040 D3): its
    producer F035 is unbuilt and there is no source to compose over.  The key
    is present and EMPTY from the first version so F035 fills it without a
    version bump.
  * Remedy deliberately does not write the digest anywhere.  The endpoint and
    the ``remedy job digest`` CLI are the next slices of F040; this module only
    turns sources into a dict.

Public API::

    JOB_DIGEST_VERSION — int, payload version of the digest envelope
    build_job_digest(job, events=None) -> dict
"""

from __future__ import annotations

from typing import Any

from packages.orchestration.decision_inbox import (
    build_decision_inbox,
    decision_urgency,
)
from packages.orchestration.run_report import (
    NOT_RECORDED,
    ReportSources,
    build_report_sources,
    recommended_next_action,
)

#: Payload version of the digest envelope.  The key set below is the contract:
#: a field added to it is a version bump, which is exactly why ``ownership``
#: ships empty rather than arriving later (DECISION F040 D3).
JOB_DIGEST_VERSION = 1

#: The EXACTNESS vocabulary of ``cost.basis``, per DECISION F040 D4 — the same
#: three words the cost ticker already publishes, and NEVER a member of
#: ``BudgetCounters.actual_sources``, which is PROVENANCE and answers a
#: different question.  Both fields were called "basis" until D4 separated them,
#: so a reader who lands here from the report's ``cost_basis`` is in the wrong
#: place: that one names WHERE the number came from, this one HOW EXACT it is.
COST_BASIS_ACTUAL = "actual"
COST_BASIS_LOWER_BOUND = "lower_bound"
COST_BASIS_ABSENT = "absent"

#: What ``BudgetCounters.cost_description()`` itself prints for a figure nobody
#: measured.  Stated here ONLY for the branch where ``budget_guard`` could not
#: be imported at all and there is no counters object to ask;
#: ``tests/orchestration/test_job_digest.py`` pins the two spellings equal so
#: this constant cannot drift away from the function it mirrors.
COST_NOT_MEASURED = "not-measured"

#: The card status ``decision_queue`` writes for a decision still waiting.  A
#: literal rather than an import because that module writes this string as a
#: literal in seven of its eight producing branches and exports no constant for
#: it; ``decision_queue.open_decisions`` filters on the same literal, so this
#: module and that one agree by construction rather than by coincidence.
OPEN_CARD_STATUS = "open"


def _report_sources(job: Any) -> ReportSources:
    """The report's own source set for *job*, or an empty one.

    ``build_report_sources`` — NOT ``collect_report_sources``: only the former
    merges ``_evidence_sources``, and only it fills ``open_decision_count`` and
    ``blocked``, which are the fields rules 1 and 3 of the next-action table
    branch on.  A digest built on the bare collector could never recommend
    answering a decision, which is the single most common thing a returning
    operator has to do.

    Guarded so no input makes the digest raise: an empty ``ReportSources``
    renders every value as its own absence and still yields a full envelope.
    """
    try:
        return build_report_sources(job)
    except Exception:  # noqa: BLE001 — a digest is an account, never a gate
        return ReportSources()


def _headline(sources: ReportSources) -> str:
    """One plain sentence: the run's state, and its terminal status when it has one.

    The digest's OWN prose, composed here rather than borrowed from the report,
    which renders its header as a bullet list no card can show.  An absent value
    renders ``not recorded`` — the report's single spelling for a source that was
    never written (P6) — because a headline that guessed would be the one line a
    returning operator trusts most and should trust least.
    """
    state = (sources.state or "").strip() or NOT_RECORDED
    terminal = (sources.terminal_status or "").strip()
    if terminal:
        return f"The run is {state} and its terminal status is {terminal}."
    return f"The run is {state}."


def _cost_counters(job: Any) -> Any | None:
    """The job's persisted cost actuals as a ``BudgetCounters``, or None.

    WHY THIS READS THE PERSISTED ACTUALS A SECOND TIME, after
    ``build_report_sources`` has already read them through
    ``run_report._evidence_sources``: ``ReportSources`` carries only the RENDERED
    ``token_description`` and the PROVENANCE tuple ``cost_basis``, and keeps no
    ``measured_cost_usd`` at all — so the EXACTNESS basis DECISION F040 D4 asks
    for is simply not recoverable from it without parsing a rendered string.
    Reading the source twice is cheaper, and far safer, than parsing prose.

    Obtained exactly the way ``_evidence_sources`` obtains it, at
    ``packages/orchestration/run_report.py:829-845``, and guarded on its own in
    the same style: a job with no plan, no actuals or an unreadable record costs
    the digest this ONE clause and never the rest of it.  A job with no actuals
    yields an EMPTY counters object rather than None, so even the absent case
    reports a figure this module did not write.
    """
    try:
        from packages.orchestration.budget_guard import (
            BudgetCounters,
            counters_from_persisted,
            decode_persisted_budget_actuals,
        )
        from packages.orchestration.pingpong_job import load_job_plan

        job_id = str(getattr(job, "id", "") or "")
        plan = load_job_plan(job_id) if job_id else None
        actuals = getattr(plan, "budget_actuals", None) if plan is not None else None
        if actuals is None:
            return BudgetCounters()
        return counters_from_persisted(
            decode_persisted_budget_actuals(
                actuals,
                first_running_at=getattr(plan, "first_running_at", "") or None))
    except Exception:  # noqa: BLE001 — no actuals is "absent", never a zero
        return None


def _cost_section(counters: Any | None) -> dict[str, str]:
    """The cost figure and its EXACTNESS basis, per DECISION F040 D4.

    The VALUE is whatever ``cost_description()`` returned, carried verbatim, so
    the digest, the report and ``remedy job budget`` cannot print different money
    for one job — this module never re-derives a number.  The BASIS is derived
    from the SAME counters object the value came from, by the rule D4 fixes:
    ``measured_cost_usd is None`` is ``absent``, any unpriced provider call makes
    the figure a floor and reads ``lower_bound``, and everything else is
    ``actual``.
    """
    if counters is None:
        return {"value": COST_NOT_MEASURED, "basis": COST_BASIS_ABSENT}
    value = str(counters.cost_description())
    if counters.measured_cost_usd is None:
        return {"value": value, "basis": COST_BASIS_ABSENT}
    if counters.unpriced_call_count > 0:
        return {"value": value, "basis": COST_BASIS_LOWER_BOUND}
    return {"value": value, "basis": COST_BASIS_ACTUAL}


def _peak_urgency(job: Any, events: list[dict[str, Any]] | None) -> int:
    """The most urgent OPEN card's score, or 0 when nothing is waiting.

    ``decision_urgency`` is IMPORTED, never restated: DECISION F040 D2 made
    ``packages/orchestration/decision_inbox.py`` the single home of that formula
    for exactly this call site, and a second copy of the arithmetic here would
    reintroduce the drift that decision exists to end.

    RESOLVED cards are excluded because urgency is a question about what still
    needs answering; an answered card scoring into the peak would make a job
    look busier the more of its questions had been settled.
    """
    try:
        inbox = build_decision_inbox(job, list(events or []))
    except Exception:  # noqa: BLE001 — an unreadable inbox is no peak, never a guess
        return 0
    scores = [
        decision_urgency(card)
        for card in inbox.get("decisions", ())
        if isinstance(card, dict) and card.get("status") == OPEN_CARD_STATUS
    ]
    return max(scores) if scores else 0


def build_job_digest(
    job: Any,
    events: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """The digest envelope for one job: state, cost, decisions and ONE action.

    *events* defaults to None and is passed through to the inbox read path, so a
    caller that already loaded the run's events does not load them twice.

    TOTAL by construction: no input makes this raise.  A job with no plan, no
    actuals, no tasks and no decisions produces a COMPLETE envelope whose values
    say exactly that — the eight keys are always present, because a key that
    appears only sometimes forces every reader to branch.
    """
    sources = _report_sources(job)
    # THE ONE-SOURCE PROPERTY: the same sources object the digest describes is
    # the one the rule table is asked about, and both halves of the answer are
    # taken from the returned NextAction rather than re-derived from either.
    action = recommended_next_action(sources)
    open_count = sources.open_decision_count
    return {
        "version": JOB_DIGEST_VERSION,
        "job_id": str(sources.job_id or ""),
        "state": (sources.state or "").strip() or NOT_RECORDED,
        "headline": _headline(sources),
        "cost": _cost_section(_cost_counters(job)),
        # DECISION F040 D3: F035 owns the ownership sentences and is unbuilt, so
        # there is NO source to read.  This empty list is a decision, not a bug —
        # the card omits the section rather than inventing a sentence, and F035
        # fills the key without a version bump when it lands.
        "ownership": [],
        "decisions": {
            # ``open_decision_count`` is None when the evidence-area read failed
            # outright, which is not evidence of zero open decisions but is the
            # only honest number a count field can carry.
            "open_count": open_count if isinstance(open_count, int) else 0,
            "peak_urgency": _peak_urgency(job, events),
        },
        "primary_action": {"label": action.action, "rule_id": action.rule_id},
    }
