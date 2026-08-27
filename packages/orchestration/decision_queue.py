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
    UNKEYED_OPTION,
    DecisionEvidenceRef,
    DecisionEvidenceTriple,
    DecisionOptionOutcome,
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
                # F032 T002c: the richest evidence in the queue was the least
                # cited — the intent this card is about and the file it would
                # change are BOTH already on the record the branch reads, so the
                # receipts are taken from `pi` rather than derived afresh.  The
                # intent id is built by `list_patch_intents` from the artifact's
                # short id and the explanation's index, so it is never empty and
                # the branch already indexes it unguarded above.  The target
                # path is OPTIONAL — `related_file` on this same card already
                # defaults it to the empty string — and rule (c) of
                # `evidence_triple_problems` refuses a ref that points at
                # nothing, so that ref is emitted only when the value is there.
                _pa_target_path = str(pi.get("target_path", "") or "")
                _pa_refs = [DecisionEvidenceRef(
                    kind="decision",
                    target=pi["intent_id"],
                    label="the patch intent awaiting approval",
                )]
                if _pa_target_path:
                    _pa_refs.append(DecisionEvidenceRef(
                        kind="file",
                        target=_pa_target_path,
                        label="the file this patch would change",
                    ))
                decisions.append(HumanDecision(
                    id=f"pa:{pi['intent_id']}",
                    type="patch_approval",
                    status="open",
                    severity="blocker",
                    source="approval_queue",
                    related_node_id=f"pi:{pi['intent_id']}",
                    related_intent_id=pi["intent_id"],
                    related_file=pi.get("target_path", ""),
                    # F032 R9 (R-0713): the old `pi.get('target_path', '?')`
                    # default could never fire — `list_patch_intents` ALWAYS
                    # sets `target_path`, to the empty string when the
                    # explanation named no file, so the key is present-and-empty
                    # rather than absent and the card read "Patch intent for
                    #  awaits approval."  Reuse the value the ref guard above
                    # already computed and fall back on emptiness, so the
                    # placeholder this line was written to show finally shows.
                    safe_summary=f"Patch intent for {_pa_target_path or '?'} awaits approval.",
                    next_actions=(
                        f"remedy patch approve {job_id[:8]} {pi['intent_id']}",
                        f"remedy patch reject {job_id[:8]} {pi['intent_id']}",
                    ),
                    created_at=pi.get("created_at", ""),
                    resolved_at=None,
                    # NO `payload` IS ADDED HERE, deliberately.  This branch's
                    # `next_actions` are two full `remedy patch` command lines
                    # rather than two option words, so growing an options list
                    # would change what the browser renders as answers —
                    # `apps/ui/src/api/decisionCard.ts::decisionAnswers` prefers
                    # `payload.options` over `next_actions` — and amendment A3
                    # of `docs/roadmap/features/T5_F032.md` puts that OUT of
                    # F032's scope.  DECISION F032 D6 moved the budget stop's
                    # options only because its `next_actions` were ALREADY the
                    # two option words, so nothing new was grown there.  The
                    # optionless case of DECISION F032 D3 therefore applies and
                    # rule (h) requires EXACTLY ONE outcome, keyed
                    # `UNKEYED_OPTION`.
                    evidence=DecisionEvidenceTriple(
                        refs=tuple(_pa_refs),
                        outcomes=(DecisionOptionOutcome(
                            option=UNKEYED_OPTION,
                            expected_outcome=(
                                "The named file's pending change is settled "
                                "either way: approving applies the patch and "
                                "unblocks the task that produced it, while "
                                "rejecting leaves the working tree untouched."
                            ),
                            downside=(
                                "The judgement is made from the intent's "
                                "summary and target path rather than from the "
                                "applied diff, so a patch that is wrong in a "
                                "way the summary does not reveal is approved "
                                "as easily as a correct one."
                            ),
                        ),),
                    ),
                ))
    except (ImportError, ValueError, OSError, AttributeError):
        pass

    # 2. Stop reasons / blockers
    try:
        from packages.orchestration.stop_reasons import derive_stop_reasons
        stops = derive_stop_reasons(job, events)
        for sr in stops:
            if sr.status == "active":
                # F032 T002d: this branch COPIES a structured record into a card
                # and cited none of the identifiers it already holds.  All three
                # receipts are read off `sr` rather than derived afresh: the
                # record's own id — the value `sr:` above is already built from,
                # so it names the same record the card came from — the reason
                # code the run wrote, and the file the stop is about.  The last
                # two are OPTIONAL on the record: `_load_stops` defaults both to
                # the empty string and `derive_stop_reasons`' no-target-repo case
                # leaves `related_file` empty, so rule (c) of
                # `evidence_triple_problems`, which refuses a ref pointing at
                # nothing, would fire on a real card if either were unguarded.
                _sr_refs = [DecisionEvidenceRef(
                    kind="failure",
                    target=sr.id,
                    label="the stop record that raised this decision",
                )]
                if sr.reason_code:
                    _sr_refs.append(DecisionEvidenceRef(
                        kind="failure",
                        target=sr.reason_code,
                        label="the reason code the run recorded",
                    ))
                if sr.related_file:
                    _sr_refs.append(DecisionEvidenceRef(
                        kind="file",
                        target=sr.related_file,
                        label="the file this stop is about",
                    ))
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
                    # NO `payload` IS ADDED HERE, deliberately.  This branch
                    # copies the record's own `next_actions`, which are command
                    # lines rather than option words, so growing an options list
                    # would change what the browser renders as answers and
                    # amendment A3 of `docs/roadmap/features/T5_F032.md` puts
                    # that OUT of F032's scope — exactly as it did for the patch
                    # approval at R8.  DECISION F032 D3's optionless case
                    # therefore applies and rule (h) requires EXACTLY ONE
                    # outcome, keyed `UNKEYED_OPTION`.
                    evidence=DecisionEvidenceTriple(
                        refs=tuple(_sr_refs),
                        outcomes=(DecisionOptionOutcome(
                            option=UNKEYED_OPTION,
                            expected_outcome=(
                                "Clearing the named blocker lets the run "
                                "continue from where it stopped, with the work "
                                "already done still in place."
                            ),
                            downside=(
                                "Until it is cleared the run makes no further "
                                "progress, and a blocker cleared without "
                                "understanding why it fired can fire again."
                            ),
                        ),),
                    ),
                ))
    except (ImportError, ValueError, OSError, AttributeError):
        pass

    # 3. Test failures
    test_fails = [e for e in events
                  if e.get("event") == "test_run_completed"
                  and e.get("metadata", {}).get("status") == "failed"]
    for tf in test_fails[-3:]:
        meta = tf.get("metadata", {})
        # F032 R7 (R-0712): the ONLY emitter that produces this event,
        # `test_execution_service._safe_event_meta`, writes the key
        # `command_safe` and never `command` — `repair_loop` reads
        # `command_safe` off the same event in two places — so reading
        # `command` first rendered "Test '?' failed." on every real failure.
        # The older key is STILL HONOURED and is NOT dead code:
        # `_fixture_test_failure` in `tests/orchestration/test_decision_inbox.py`
        # writes `command`, and dropping the fallback would leave that card
        # showing the placeholder instead.
        cmd = str(meta.get("command_safe") or meta.get("command") or "?")
        # F032 T002b: both receipts come from THIS event, so the card cites the
        # same run the branch selected rather than a fresh derivation.  The run
        # id keeps its `unknown` default as a target — that is what the decision
        # id is already built from, and it is honest where an empty target,
        # which rule (c) of `evidence_triple_problems` refuses, would point at
        # nothing.  The command is cited only when it was actually resolved: the
        # `?` placeholder names no command and would be a ref to a question mark.
        _test_run_id = str(meta.get("test_run_id", "unknown"))
        _tf_refs = [DecisionEvidenceRef(
            kind="failure",
            target=_test_run_id,
            label="the test run that failed",
        )]
        if cmd and cmd != "?":
            _tf_refs.append(DecisionEvidenceRef(
                kind="failure",
                target=cmd,
                label="the command that was run",
            ))
        decisions.append(HumanDecision(
            id=f"tf:{_test_run_id[:8]}",
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
            # This branch offers no options — it carries no `payload` and its
            # `next_actions` are instructions rather than choices — so DECISION
            # F032 D3's optionless case applies and rule (h) requires EXACTLY
            # ONE outcome, keyed `UNKEYED_OPTION`.
            evidence=DecisionEvidenceTriple(
                refs=tuple(_tf_refs),
                outcomes=(DecisionOptionOutcome(
                    option=UNKEYED_OPTION,
                    expected_outcome=(
                        "Reading the named run's output shows which assertion "
                        "failed, so the repair targets the real cause instead "
                        "of a guess."
                    ),
                    downside=(
                        "The job stays blocked while that output is read, and "
                        "a failure caused by the environment rather than by "
                        "the change spends that time for nothing."
                    ),
                ),),
            ),
        ))

    # 4. Dirty repo
    git_reads = [e for e in events if e.get("event") == "git_status_read"]
    if git_reads:
        last = git_reads[-1].get("metadata", {})
        if last.get("dirty"):
            # F032 T002e: the thinnest branch in the queue cited nothing at all.
            # THE EVENT NAME IS THE ONE RECEIPT THIS BRANCH IS GUARANTEED TO
            # HAVE — the branch exists because that event was read — so it is
            # emitted unguarded, which is also what keeps rule (a) of
            # `evidence_triple_problems` satisfiable for the thin event
            # `_fixture_repo_dirty` in `tests/orchestration/test_decision_inbox.py`
            # writes, whose `metadata` carries `dirty` and nothing else.  The
            # status fingerprint is OPTIONAL for exactly that reason: only
            # `apps/cli/commands/repo.py` writes `status_hash`, so an
            # unguarded ref on it would point at nothing on that fixture and
            # rule (c) would refuse the whole card.  NOTHING IS EMITTED for
            # `branch`, `head_sha` or `changed_file_count`: no kind in
            # `DECISION_EVIDENCE_REF_KINDS` types a branch name, a commit or a
            # count without lying about what it is, and amendment A2 of
            # `docs/roadmap/features/T5_F032.md` forbids inventing vocabulary.
            _rd_refs = [DecisionEvidenceRef(
                kind="failure",
                target="git_status_read",
                label="the run-log event that reported the working tree dirty",
            )]
            _rd_status_hash = str(last.get("status_hash", "") or "")
            if _rd_status_hash:
                _rd_refs.append(DecisionEvidenceRef(
                    kind="failure",
                    target=_rd_status_hash,
                    label="the status fingerprint that reading recorded",
                ))
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
                # NO `payload` IS ADDED HERE, deliberately.  This branch's one
                # `next_action` is an instruction rather than a choice, so
                # DECISION F032 D3's optionless case applies and rule (h)
                # requires EXACTLY ONE outcome, keyed `UNKEYED_OPTION`.
                evidence=DecisionEvidenceTriple(
                    refs=tuple(_rd_refs),
                    outcomes=(DecisionOptionOutcome(
                        option=UNKEYED_OPTION,
                        expected_outcome=(
                            "Committing or stashing the target repository's "
                            "changes leaves a clean tree, so a later diff "
                            "shows only what this job did."
                        ),
                        downside=(
                            "The job waits while that happens, and stashing "
                            "work that is not this job's can hide changes "
                            "their author still needs."
                        ),
                    ),),
                ),
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
        # F032 T002a: the receipts behind the budget stop are built from what
        # this branch ALREADY read out of the stop event, so the card cites the
        # same evidence the guard acted on rather than a fresh derivation.  A
        # ref whose target is empty points at nothing and rule (c) of
        # `evidence_triple_problems` refuses it, so the optional two are emitted
        # only when the stop event actually carried them.
        _budget_refs = [DecisionEvidenceRef(
            kind="failure",
            target=budget_error,
            label="the stop reason the budget guard recorded",
        )]
        if _budget_limit:
            _budget_refs.append(DecisionEvidenceRef(
                kind="failure",
                target=_budget_limit,
                label="the budget limit that was exhausted",
            ))
        if _budget_request_id:
            _budget_refs.append(DecisionEvidenceRef(
                kind="decision",
                target=_budget_request_id,
                label="the request in flight when the budget was exhausted",
            ))
        # The limit is named as a WHOLE NOUN PHRASE and not interpolated as a
        # bare word, because the sentence has to read as English in both cases:
        # substituting the value alone produces "a raised the exhausted limit"
        # when the stop event carried no `exhausted_limit`.
        _limit_phrase = (f"the exhausted limit of {_budget_limit}"
                         if _budget_limit else "the exhausted limit")
        _budget_outcomes = (
            DecisionOptionOutcome(
                option="extend",
                expected_outcome=(
                    "The job resumes from its last safe point with "
                    f"{_limit_phrase} raised, and the work already paid for "
                    "is kept."
                ),
                downside=(
                    "Spend continues past the ceiling that was set, and the "
                    "same stop recurs if the run is not converging."
                ),
            ),
            DecisionOptionOutcome(
                option="abandon",
                expected_outcome=(
                    "The job stops with the artifacts it has, and nothing "
                    f"further is spent against {_limit_phrase}."
                ),
                downside=(
                    "The work in flight is left unfinished, and a later "
                    "resume pays again for the context this run had built."
                ),
            ),
        )
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
            # DECISION F032 D6: the two choices are stated where the emit gate
            # and the browser both already look.  `next_actions` is unchanged —
            # `decisionCard.decisionAnswers` prefers `payload.options` and
            # yields the same two answers in the same order.
            payload={"options": ["extend", "abandon"]},
            evidence=DecisionEvidenceTriple(
                refs=tuple(_budget_refs),
                outcomes=_budget_outcomes,
            ),
        ))

    # 6. Stale/needs_review memory cards
    try:
        from packages.memory.local_gateway import list_memory
        entries = list_memory()
        # `validity` and `review_status` are SEPARATE fields on the memory card
        # (`packages/memory/models.py:44-45`): "needs_review" is a value of
        # `review_status` only, so reading it out of `validity` selected nothing.
        memory_cards_to_review = [e for e in entries
                                  if e.validity == "stale"
                                  or e.review_status == "needs_review"]
        for me in memory_cards_to_review[:5]:
            # F032 R5 (R-0711): the card's one line has to say WHY a human is
            # being asked to look, and the predicate above admits cards for two
            # INDEPENDENT reasons — so the reason is derived from both fields.
            # Reading `validity` alone made a card flagged for review announce
            # itself as "active", which is true and explains nothing.
            is_stale = me.validity == "stale"
            is_flagged_for_review = me.review_status == "needs_review"
            if is_stale and is_flagged_for_review:
                reason = "is stale and flagged for review"
            elif is_stale:
                reason = "is stale"
            else:
                reason = "is flagged for review"
            # F032 T002e: R5 gave this card a reason and cited neither the card
            # it names nor the fields that reason was read off.  All three refs
            # are GUARDED and none of them alone would do: `MemoryEntry.key`
            # defaults to the empty string (`packages/memory/models.py`), and
            # each of the two field refs fires only in the arm that selected the
            # card, so an unguarded one would target the empty string and rule
            # (c) of `evidence_triple_problems` would refuse the whole card.
            # RULE (a) IS STILL SATISFIABLE WITH NO KEY AT ALL, and that is the
            # argument the key's guard rests on: the selecting predicate above
            # admits a card only when it is stale or flagged, so at least one of
            # the last two refs always fires.  The two booleans are the ones R5
            # already computed for the summary, so the receipts and the sentence
            # cannot drift apart.
            _mr_refs: list[DecisionEvidenceRef] = []
            if me.key:
                _mr_refs.append(DecisionEvidenceRef(
                    kind="decision",
                    target=me.key,
                    label="the memory card this review is about",
                ))
            if is_stale:
                _mr_refs.append(DecisionEvidenceRef(
                    kind="failure",
                    target=me.validity,
                    label="the validity the card carries",
                ))
            if is_flagged_for_review:
                _mr_refs.append(DecisionEvidenceRef(
                    kind="failure",
                    target=me.review_status,
                    label="the review status the card carries",
                ))
            decisions.append(HumanDecision(
                id=f"mem:{me.key}",
                type="memory_review",
                status="open",
                severity="info",
                source="memory",
                related_node_id="",
                related_intent_id="",
                related_file="",
                safe_summary=f"Memory '{me.key}' {reason}.",
                next_actions=(f"remedy memory card-show {me.key}",),
                created_at="",
                resolved_at=None,
                # NO `payload` IS ADDED HERE, deliberately.  This branch's one
                # `next_action` is a `remedy memory card-show` command rather
                # than a choice, so DECISION F032 D3's optionless case applies
                # and rule (h) requires EXACTLY ONE outcome, keyed
                # `UNKEYED_OPTION`.
                evidence=DecisionEvidenceTriple(
                    refs=tuple(_mr_refs),
                    outcomes=(DecisionOptionOutcome(
                        option=UNKEYED_OPTION,
                        expected_outcome=(
                            "Opening the named card shows what it claims and "
                            "when that was last confirmed, so it can be "
                            "re-approved, corrected or superseded instead of "
                            "trusted blind."
                        ),
                        downside=(
                            "Reading it takes time now, and a card left in "
                            "place while it is checked keeps feeding whatever "
                            "already reads it."
                        ),
                    ),),
                ),
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
            # F032 T002f, the PENDING arm.  The card's own id is the one receipt
            # this arm is guaranteed to hold — the branch exists because the
            # plan asked for approval — so it is emitted UNGUARDED, and that is
            # what keeps rule (a) of `evidence_triple_problems` satisfied for
            # the minimal job `tests/orchestration/test_mission_state.py` builds,
            # `Job(name="t", flight_plan={"_approval": "pending"})`, which
            # supplies no clarifications and no intake at all.  Each open
            # question is cited only when it HAS an id: `open_clarification_
            # questions` defaults that field to the empty string, and rule (c)
            # refuses a ref pointing at nothing, which would refuse the whole
            # card.  NOTHING IS EMITTED for the mission offer — it is an OFFER
            # attached to this card rather than evidence for the plan, and
            # amendment A2 of `docs/roadmap/features/T5_F032.md` forbids
            # inventing vocabulary to carry it.
            _fp_refs = [DecisionEvidenceRef(
                kind="decision",
                target="fp:approval",
                label="the flight-plan approval this job is waiting on",
            )]
            for _question in _questions:
                _question_id = str(_question.get("id", "") or "")
                if _question_id:
                    _fp_refs.append(DecisionEvidenceRef(
                        kind="decision",
                        target=_question_id,
                        label="the open question that ships with this plan",
                    ))
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
                # THE OUTCOMES ARE KEYED, not unkeyed: `_payload["options"]` is
                # set above on every pass, so rule (g) rather than rule (h)
                # applies and it compares the outcome keys against that list in
                # BOTH directions — exactly one outcome per option word, and no
                # option word this card does not offer.
                evidence=DecisionEvidenceTriple(
                    refs=tuple(_fp_refs),
                    outcomes=(
                        DecisionOptionOutcome(
                            option="approve",
                            expected_outcome=(
                                "The run starts and the plan's tasks execute "
                                "in the order it records, so the work that "
                                "follows is the work that was reviewed."
                            ),
                            downside=(
                                "Work begins against whatever the plan "
                                "assumed, and an assumption nobody checked is "
                                "paid for in rework."
                            ),
                        ),
                        DecisionOptionOutcome(
                            option="reject",
                            expected_outcome=(
                                "Nothing executes and the plan goes back for "
                                "revision, so a wrong scope costs a replan "
                                "rather than a run."
                            ),
                            downside=(
                                "The job makes no progress until a new plan is "
                                "approved, and the context this planning built "
                                "is spent again."
                            ),
                        ),
                    ),
                ),
            ))
        elif _fp_approval == "approved" and _flight_plan.get("_approval_audit"):
            audit = _flight_plan["_approval_audit"]
            reason = audit.get("reason", "auto-approved")
            # F032 T002f, the RESOLVED arm.  DECISION F032 D7 is why it owes a
            # triple at all: `enforce_decision_evidence` selects by TYPE ALONE
            # and never reads `status`, so both arms are enforced the moment
            # `flight_plan_approval` joins `TRIPLE_REQUIRED_TYPES`, and this card
            # is still RENDERED by `build_decision_inbox`.  Its refs are the
            # audit trail the answer actually left.  The card's own id is again
            # unguarded; `reason` reuses the variable computed above rather than
            # re-reading the dict, and both it and `mode` are GUARDED because
            # `tests/orchestration/test_decision_inbox.py` drives this arm with
            # an audit of `{"reason": "approved"}` and no `mode` key at all — an
            # unguarded `mode` ref would target the empty string there and rule
            # (c) would refuse the card.
            _fp_resolved_refs = [DecisionEvidenceRef(
                kind="decision",
                target="fp:approval",
                label="the flight-plan approval this record answers",
            )]
            if reason:
                _fp_resolved_refs.append(DecisionEvidenceRef(
                    kind="decision",
                    target=str(reason),
                    label="the reason recorded when the plan was approved",
                ))
            _fp_mode = str(audit.get("mode", "") or "")
            if _fp_mode:
                _fp_resolved_refs.append(DecisionEvidenceRef(
                    kind="decision",
                    target=_fp_mode,
                    label="how the approval was given",
                ))
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
                # NO `payload` IS ADDED HERE, deliberately: a resolved plan
                # offers nothing to answer, so DECISION F032 D3's optionless
                # case applies and rule (h) requires EXACTLY ONE outcome, keyed
                # `UNKEYED_OPTION`.  Per DECISION F032 D7 it states the
                # consequence of the answer that WAS recorded rather than of one
                # still to come.
                evidence=DecisionEvidenceTriple(
                    refs=tuple(_fp_resolved_refs),
                    outcomes=(DecisionOptionOutcome(
                        option=UNKEYED_OPTION,
                        expected_outcome=(
                            "The run executes the plan this approval named, so "
                            "the tasks it carries out are the agreed scope."
                        ),
                        downside=(
                            "A plan approved on an assumption that has since "
                            "changed keeps the run pointed at the old scope "
                            "until someone revisits it."
                        ),
                    ),),
                ),
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
    # in `TRIPLE_REQUIRED_TYPES`, which T002a made non-empty: `token_budget` is
    # in it from the commit that gave the budget stop a real triple, and each
    # remaining producer joins the same way, in its own upgrade commit.
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
