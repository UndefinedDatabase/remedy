"""F053 T001 — the one human-readable account of a run.

Every run produces ONE report: what was attempted, what succeeded, what is
blocked and why, what it cost, what needs answering, and the single
recommended next action.

This module is a pure RENDERER.  It computes nothing new and it never
guesses: every value it prints already exists as structured data somewhere
else, and a source that is absent renders as ``not recorded`` rather than as
a plausible number (P6).  That rule is what makes the report safe to read
without opening the evidence — a reader can trust that a number they see was
measured, and that a number they do not see was not.

Deliberate absences (searched-for behavior that is NOT here):
  * Remedy deliberately does not RE-COMPUTE costs, durations, or verdicts in
    this module — `budget_guard.BudgetCounters.token_description` and the
    cycle records own those, and a second arithmetic path would be a second
    truth.
  * Remedy deliberately does not write the report from here.  The terminal
    -state writer and the ``remedy job report`` CLI are F053 T002; this
    module only turns sources into text.
  * Remedy deliberately does not read ``docs/roadmap/STATUS.md`` here.  The
    milestone distance and the capability lines come from a STATUS mirror
    passed IN (``ReportSources.status_mirror``); no production reader of that
    file exists yet, so both sections render ``not recorded`` until one does.

Sources (all pre-existing; see ``collect_report_sources``):
  job/task state      packages/core/models.py  Job.state / Task.status
  cycle summaries     long_run_executor.read_cycle_records (incl. the F052
                      healed_after_repair / repair_rounds_used fields)
  postmortems         failure_postmortem.read_postmortem
  open decisions      decision_queue.list_decisions / open_decisions
  token actuals       budget_guard.BudgetCounters (persisted job actuals)
  assumption log      flight_plan.render_assumptions_md and
                      escalation.render_escalation_assumptions_md
  run manifest        run_manifest.read_run_manifest
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Modes
# ---------------------------------------------------------------------------

#: The report written once at a terminal state (F053 T002 calls it).
MODE_FINAL = "final"
#: The snapshot of a run that is still going.  Never mutates state.
MODE_INTERIM = "interim"
VALID_MODES = frozenset({MODE_FINAL, MODE_INTERIM})

#: What a missing source renders as.  One spelling, everywhere: a reader who
#: greps the report for this string finds every gap in one pass.
NOT_RECORDED = "not recorded"

#: The loud interim banner.  A snapshot that could be mistaken for a final
#: report is worse than no snapshot at all.
INTERIM_BANNER = "INTERIM SNAPSHOT — run still in progress (rendered at {ts})"

#: A9: per-task lines cap at a readable count; the evidence area is the
#: archive, the report is the summary.
MAX_TASK_LINES = 20
#: The same cap for the two other unbounded lists a big run can produce.
MAX_BLOCKED_LINES = 20
MAX_CYCLE_LINES = 20
#: Capability lines cap lower than the rest (CALL-2 ruling, F053 R2 review):
#: they grow with the ROADMAP, not with the run, so an uncapped list would
#: eventually dwarf the account of the run it is attached to.
MAX_CAPABILITY_LINES = 10

#: F033 (finding R-0738): how a task's FOLDED apply state reads in a task line.
#: "partially applied" is the spelling the viewer badge and the tasks card
#: already use — one spelling per concept, across all three surfaces.  A state
#: this table does not know renders NOTHING rather than an invented phrase: the
#: same fail-quiet rule an absent source gets (P6).
APPLY_STATE_LABELS: dict[str, str] = {
    "applied": "applied",
    "reverted": "reverted",
    "not_applied": "not applied",
    "partial": "partially applied",
}

#: The final report's filename inside the job's evidence area (F053 T002).
#: FIXED, and the writer overwrites it: the acceptance rule is exactly one
#: report per terminal job, REGENERATED on resume-then-finish, never appended.
#: It sits beside the cycle records, in the same evidence area, so there is no
#: second evidence convention to learn.
REPORT_FILENAME = "report.md"

#: Where a report-write failure is recorded on the job.  The report is an
#: ACCOUNT of the run, not a gate on it — failing to write one must never turn
#: a finished run into a failed one.
REPORT_ERROR_METADATA_KEY = "report_error"


class ReportError(ValueError):
    """The renderer was called with an argument it cannot honour."""


# ---------------------------------------------------------------------------
# Momentum (mechanically defined — T1_F053.md)
# ---------------------------------------------------------------------------

MOMENTUM_FORWARD = "forward"
MOMENTUM_CIRCLING = "circling"
MOMENTUM_UNKNOWN = "unknown"

#: The escalation a circling run proposes.  Named, not implied: "circling"
#: without a proposal is an observation nobody can act on.
CIRCLING_ESCALATION = (
    "Escalate: cut the next round into smaller slices, re-plan the failing "
    "branch, or ask a human for a decision."
)


def _open_item_count(record: dict[str, Any]) -> int:
    """Open items a cycle left behind: failures plus escalations.

    Escalations are counted because a branch waiting on a question is not
    done — but they stay a SEPARATE number everywhere they are rendered
    (CycleRecord.tasks_escalated), because a question is not a failure.
    """
    return _as_int(record.get("tasks_failed")) + _as_int(record.get("tasks_escalated"))


def momentum_flag(cycle_records: list[dict[str, Any]] | None) -> str:
    """forward | circling | unknown, from the cycle records alone.

    Mechanical definition (T1_F053.md):
      circling  — the same non-empty verify failure class appears in >= 2
                  cycles, OR open items did not decrease across a round.
      forward   — every round closed items and no failure class recurred.
      unknown   — no cycle records: nothing to judge, and a guess here would
                  be exactly the invented value P6 forbids.
    """
    records = list(cycle_records or [])
    if not records:
        return MOMENTUM_UNKNOWN

    seen_classes: dict[str, int] = {}
    for record in records:
        klass = str(record.get("verify_failure_class") or "")
        if klass:
            seen_classes[klass] = seen_classes.get(klass, 0) + 1
    if any(count >= 2 for count in seen_classes.values()):
        return MOMENTUM_CIRCLING

    previous = None
    for record in records:
        current = _open_item_count(record)
        if previous is not None and current > 0 and current >= previous:
            return MOMENTUM_CIRCLING
        previous = current
    return MOMENTUM_FORWARD


# ---------------------------------------------------------------------------
# Next-action rule table
# ---------------------------------------------------------------------------

#: The report ends with EXACTLY ONE recommended next action, chosen by this
#: table, first match wins.  The table is data so the rule that fired can be
#: named in the report itself — a recommendation whose reason is invisible is
#: not reviewable.
#:
#:   (rule id, condition)
#:
#: Order is the priority order from T1_F053.md: an open decision outranks a
#: failure, because the run cannot proceed past a question no matter what
#: else is repaired.
NEXT_ACTION_RULES: tuple[tuple[str, str], ...] = (
    ("open-decision", "an open decision is waiting for an answer"),
    # F053 T002 (DECISION D2): an operator stop outranks the blocked rule.
    # A run somebody stopped on purpose is not a broken run, and telling its
    # operator to go read a postmortem would be a false alarm.
    ("stopped-by-operator", "the run stopped on operator request"),
    ("blocked-failed", "the run is blocked or a task failed"),
    ("all-green", "every task completed and nothing is open"),
    ("indeterminate", "no rule matched the recorded state"),
)

#: rule id -> the condition that fires it.  The table is load-bearing: a
#: NextAction whose rule id is not in it cannot be rendered.
NEXT_ACTION_CONDITIONS: dict[str, str] = dict(NEXT_ACTION_RULES)


@dataclass(frozen=True)
class NextAction:
    """The single recommended next action plus the rule that produced it."""

    rule_id: str
    action: str

    def __post_init__(self) -> None:
        if self.rule_id not in NEXT_ACTION_CONDITIONS:
            raise ReportError(f"next action uses an undocumented rule: {self.rule_id!r}")

    def render(self) -> str:
        """The action, with the rule and the condition that chose it.

        The condition is printed because a recommendation a reader cannot
        audit is a recommendation they have to take on trust.
        """
        return (f"{self.action}  _(rule: {self.rule_id} — "
                f"{NEXT_ACTION_CONDITIONS[self.rule_id]})_")


# ---------------------------------------------------------------------------
# Sources
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class StatusMirror:
    """The roadmap ledger, already parsed, handed to the renderer.

    Deliberately an INPUT and not a read: this module never parses
    ``docs/roadmap/STATUS.md`` itself (that file is operator territory —
    scope_fences.BUILTIN_DENY).  Until a producer exists, both sections this
    feeds render ``not recorded``.

    remaining_to_milestone: features still unchecked up to ``milestone``.
    accepted_capabilities:  ONLY accepted ``[x]`` state (P1) — what Remedy
                            can do NOW.
    in_progress_capabilities: ``[~]`` state; always rendered as in progress,
                            never as a capability.
    """

    milestone: str
    remaining_to_milestone: int
    accepted_capabilities: tuple[str, ...] = ()
    in_progress_capabilities: tuple[str, ...] = ()


@dataclass(frozen=True)
class TaskOutcome:
    """One task's one-line result, already resolved to text and a link."""

    task_id: str
    description: str
    status: str
    #: Relative path into the evidence area, or "" when nothing was written.
    #: Relative on purpose: an absolute path is unusable in a moved bundle.
    evidence_ref: str = ""
    #: The task's folded apply state (proof_chain.fold_task_apply_states), one of
    #: APPLY_STATE_LABELS' keys.  EMPTY means NOT RECORDED — this module's
    #: standing rule for an absent source (P6) — and renders no clause at all,
    #: which is what keeps a report of a job with no proof chain byte-identical
    #: to the one this module produced before hunk-level approval existed.
    apply_state: str = ""
    #: The two numbers behind that state, defaulted so every existing
    #: construction site keeps working unchanged.  Both are the FOLD's counts;
    #: this module re-derives neither (finding R-0738).
    applied_changes: int = 0
    total_changes: int = 0


@dataclass(frozen=True)
class BlockedItem:
    """A task that is blocked, and the one thing a human can do about it."""

    task_id: str
    reason: str
    #: failure_postmortem.FailureClass value, or "" when no postmortem exists.
    failure_class: str = ""
    #: For a decision: the EXACT command that answers it
    #: (escalation.task_decision_answer_command).  Never abbreviated — a
    #: command that is not shown in full cannot be pasted.
    answer_command: str = ""
    evidence_ref: str = ""


@dataclass(frozen=True)
class DoDCheckRow:
    """One row of the Definition-of-Done matrix, already resolved to text."""

    check_id: str
    kind: str
    blocking: bool
    status: str
    #: Named reason for a red check; "" when it passed.
    reason: str = ""
    duration_ms: int = 0


@dataclass(frozen=True)
class ReportSources:
    """Everything the report renders, already structured.

    Every field is optional and every absent field renders ``not recorded``.
    Passing this in is what makes the renderer pure and its goldens stable:
    no clock, no disk, no provider.
    """

    job_id: str = ""
    job_name: str = ""
    project_id: str = ""
    mission: str = ""
    #: F045: the loop this run came from (loop_run.LOOP_REF_METADATA_KEY), so
    #: a report inside the evidence area names its own provenance.  Empty for
    #: every non-loop job, and an empty value prints NO line at all — see
    #: ``_header_lines`` — which is what keeps the existing goldens intact.
    loop_ref: str = ""
    state: str = ""
    terminal_status: str = ""
    stop_reason: str = ""
    started_at: str = ""
    ended_at: str = ""
    duration_text: str = ""
    tasks: tuple[TaskOutcome, ...] = ()
    blocked: tuple[BlockedItem, ...] = ()
    #: budget_guard.BudgetCounters.token_description() — carried VERBATIM,
    #: including its ">= N tokens (M provider calls unmeasured)" notation.
    token_description: str = ""
    #: Where that number came from (BudgetCounters.actual_sources).  Every
    #: cost line names its basis (P6); a cost without a basis is not printed.
    cost_basis: tuple[str, ...] = ()
    elapsed_seconds: float | None = None
    cycle_records: tuple[dict[str, Any], ...] = ()
    open_decision_lines: tuple[str, ...] = ()
    open_decision_count: int | None = None
    open_assumptions: tuple[str, ...] = ()
    assumptions_ref: str = ""
    manifest_ref: str = ""
    plan_ref: str = ""
    status_mirror: StatusMirror | None = None
    #: F053 next feature capability line ("can next"), supplied by the caller.
    next_capability: str = ""
    #: F061 T004 — the Definition-of-Done matrix, one row per check.
    dod_checks: tuple[DoDCheckRow, ...] = ()
    #: The gate's verdict: None when the job was never gated (no DoD).
    dod_released: bool | None = None
    notes: tuple[str, ...] = field(default_factory=tuple)


# ---------------------------------------------------------------------------
# Small helpers — every one of them refuses to invent a value
# ---------------------------------------------------------------------------


def _as_int(value: Any) -> int:
    """An int, or 0 for anything that is not one.  Never raises into a render."""
    if isinstance(value, bool) or not isinstance(value, int):
        return 0
    return value


def _text(value: str | None) -> str:
    """The value, or the missing-source marker.  The only place that decides."""
    value = (value or "").strip()
    return value or NOT_RECORDED


def _link(label: str, ref: str) -> str:
    """A markdown link when there is a target, otherwise the bare label."""
    ref = (ref or "").strip()
    if not ref:
        return label
    return f"[{label}]({ref})"


def _capped(lines: list[str], limit: int, noun: str) -> list[str]:
    """The first *limit* lines plus an honest count of what was dropped (A9).

    Never a silent truncation: a report that quietly shows 20 of 200 tasks
    reads as a complete report and is not one.
    """
    if len(lines) <= limit:
        return lines
    dropped = len(lines) - limit
    return lines[:limit] + [f"- … and {dropped} more {noun} (see evidence)"]


# ---------------------------------------------------------------------------
# Next action
# ---------------------------------------------------------------------------


def recommended_next_action(sources: ReportSources) -> NextAction:
    """The one next action, by NEXT_ACTION_RULES, first match wins."""
    if sources.open_decision_count:
        command = ""
        for item in sources.blocked:
            if item.answer_command:
                command = item.answer_command
                break
        action = "Answer the open decision"
        if command:
            action = f"Answer the open decision: `{command}`"
        return NextAction("open-decision", action)

    terminal = (sources.terminal_status or "").strip().lower()
    if terminal == "stopped_by_operator":
        return NextAction(
            "stopped-by-operator",
            "Resume the run (or close it) — it stopped on request, "
            "nothing is broken")

    blocked_state = terminal in {"blocked", "budget_exhausted", "deadline_reached"}
    if sources.blocked or blocked_state:
        ref = next((b.evidence_ref for b in sources.blocked if b.evidence_ref), "")
        target = _link("the postmortem", ref) if ref else "the postmortem"
        return NextAction("blocked-failed", f"Inspect {target} and repair the blocked task")

    if sources.tasks and all(
            t.status.strip().lower() == "completed" for t in sources.tasks):
        return NextAction("all-green", "Review and merge the branch")

    return NextAction("indeterminate",
                      f"No recommendation — the run state is {NOT_RECORDED}")


# ---------------------------------------------------------------------------
# Sections
# ---------------------------------------------------------------------------


def _header_lines(sources: ReportSources, mode: str, rendered_at: str) -> list[str]:
    lines: list[str] = []
    if mode == MODE_INTERIM:
        lines.append(f"> **{INTERIM_BANNER.format(ts=_text(rendered_at))}**")
        lines.append("")
    lines.append(f"# Run report — {_text(sources.job_name)}")
    lines.append("")
    lines.append(f"- Job: `{_text(sources.job_id)}`")
    lines.append(f"- Project: {_text(sources.project_id)}")
    # Quoted as-is: the mission may be in any language; the report is English
    # around it, and translating an operator's own words would be a rewrite.
    lines.append(f"- Mission: {_text(sources.mission)}")
    # F045: conditional on purpose — a job that came from no loop prints no
    # Loop line, which is why every pre-F045 golden stays byte-identical.
    if sources.loop_ref:
        lines.append(f"- Loop: {sources.loop_ref}")
    lines.append(f"- State: {_text(sources.state)}")
    lines.append(f"- Terminal status: {_text(sources.terminal_status)}")
    if sources.stop_reason:
        lines.append(f"- Stop reason: {sources.stop_reason}")
    lines.append(f"- Duration: {_text(sources.duration_text)}")
    lines.append("")
    return lines


def _apply_clause(task: TaskOutcome) -> str:
    """The task's apply clause, or "" when there is nothing recorded to say.

    R-0738's third surface: a reader must be able to tell a MIXED apply state
    from a complete one, with the two counts behind it, without opening the
    evidence.  An empty state — and any state APPLY_STATE_LABELS does not know —
    yields the empty string, so the task line is byte-identical to the one this
    module rendered before the state existed.
    """
    label = APPLY_STATE_LABELS.get(task.apply_state, "")
    if not label:
        return ""
    return (f" — {label} "
            f"({_as_int(task.applied_changes)}/{_as_int(task.total_changes)} changes)")


def _task_lines(sources: ReportSources) -> list[str]:
    lines = ["## Tasks", ""]
    if not sources.tasks:
        lines += [f"Tasks: {NOT_RECORDED}.", ""]
        return lines
    body = [
        f"- `{t.task_id}` — {_text(t.description)} — **{_text(t.status)}**"
        + _apply_clause(t)
        + (f" — {_link('evidence', t.evidence_ref)}" if t.evidence_ref else "")
        for t in sources.tasks
    ]
    lines += _capped(body, MAX_TASK_LINES, "tasks")
    lines.append("")
    return lines


def _blocked_lines(sources: ReportSources) -> list[str]:
    lines = ["## Blocked", ""]
    if not sources.blocked:
        lines += ["Nothing blocked.", ""]
        return lines
    body: list[str] = []
    for item in sources.blocked:
        parts = [f"- `{item.task_id}` — {_text(item.reason)}"]
        parts.append(f" — class: {_text(item.failure_class)}")
        if item.evidence_ref:
            parts.append(f" — {_link('postmortem', item.evidence_ref)}")
        body.append("".join(parts))
        if item.answer_command:
            body.append(f"  - answer with: `{item.answer_command}`")
    lines += _capped(body, MAX_BLOCKED_LINES, "blocked items")
    lines.append("")
    return lines


def _dod_lines(sources: ReportSources) -> list[str]:
    """The Definition-of-Done matrix (F061 T004).

    A job nobody compiled a DoD for renders ``not recorded`` — the same rule as
    every other absent source (P6). A gated job gets the full matrix, including
    the non-blocking reds, which are reported here precisely because they did
    NOT gate anything.
    """
    lines = ["## Definition of Done", ""]
    if not sources.dod_checks:
        lines += [f"Definition of Done: {NOT_RECORDED}.", ""]
        return lines

    if sources.dod_released is True:
        lines += ["Every blocking check is green — the gate released.", ""]
    elif sources.dod_released is False:
        blocking_red = [c.check_id for c in sources.dod_checks
                        if c.blocking and c.status != "passed"]
        lines += [
            "The gate is HOLDING this job open: "
            f"{len(blocking_red)} blocking check(s) red "
            f"({', '.join(blocking_red) or 'unnamed'}).", ""]

    lines.append("| check | kind | blocking | status | reason | duration |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    body = [
        f"| `{_text(c.check_id)}` | {_text(c.kind)} "
        f"| {'yes' if c.blocking else 'no'} | **{_text(c.status)}** "
        f"| {_text(c.reason) if c.reason else '-'} | {_as_int(c.duration_ms)}ms |"
        for c in sources.dod_checks
    ]
    lines += _capped(body, MAX_TASK_LINES, "checks")
    lines.append("")
    return lines


def _decision_lines(sources: ReportSources) -> list[str]:
    lines = ["## Open decisions", ""]
    if sources.open_decision_count is None:
        lines += [f"Open decisions: {NOT_RECORDED}.", ""]
        return lines
    if not sources.open_decision_count:
        lines += ["No open decisions.", ""]
        return lines
    # Rendered verbatim from decision_queue.render_open_decisions_lines so the
    # report and `remedy job status` cannot drift apart.
    lines += list(sources.open_decision_lines) or [
        f"Open decisions: {sources.open_decision_count} (detail {NOT_RECORDED})"]
    lines.append("")
    return lines


def _cost_lines(sources: ReportSources) -> list[str]:
    lines = ["## Cost", ""]
    if not sources.token_description:
        # No actuals is a normal outcome, not a zero.  A rendered "0 tokens"
        # would be an invented measurement.
        lines += [f"Tokens: {NOT_RECORDED} (no actuals persisted for this run).", ""]
        return lines
    basis = ", ".join(sources.cost_basis) if sources.cost_basis else NOT_RECORDED
    lines.append(f"- Tokens: {sources.token_description} — basis: {basis}")
    if sources.elapsed_seconds is None:
        lines.append(f"- Elapsed: {NOT_RECORDED} — basis: {NOT_RECORDED}")
    else:
        lines.append(
            f"- Elapsed: {sources.elapsed_seconds:.1f}s — basis: budget counters")
    lines.append("")
    return lines


def _cycle_lines(sources: ReportSources) -> list[str]:
    lines = ["## Cycles", ""]
    if not sources.cycle_records:
        lines += [f"Cycles: {NOT_RECORDED}.", ""]
        return lines
    body: list[str] = []
    for record in sources.cycle_records:
        index = _as_int(record.get("cycle_index"))
        verify = _text(str(record.get("verify_result") or ""))
        parts = [
            f"- Cycle {index}: {_as_int(record.get('tasks_completed'))} completed, "
            f"{_as_int(record.get('tasks_failed'))} failed, "
            f"{_as_int(record.get('tasks_escalated'))} escalated — verify: {verify}"
        ]
        klass = str(record.get("verify_failure_class") or "")
        if klass:
            parts.append(f" — failure class: {klass}")
        body.append("".join(parts))
        # F052 risk visibility: a heal is never implied by a green cycle, and a
        # heal that changed no file is a flake suspect a human must see.
        if record.get("healed_after_repair"):
            rounds = _as_int(record.get("repair_rounds_used"))
            note = f"  - healed after {rounds} repair round(s)"
            if record.get("healed_without_changes"):
                note += " — WITHOUT file changes (flake suspect)"
            body.append(note)
        summary = str(record.get("repair_summary") or "")
        if summary:
            body.append(f"  - repair: {summary}")
    lines += _capped(body, MAX_CYCLE_LINES, "cycles")
    lines.append("")
    return lines


def _assumption_lines(sources: ReportSources) -> list[str]:
    lines = ["## Open assumptions", ""]
    if not sources.open_assumptions:
        lines.append(
            "No open assumptions."
            if sources.assumptions_ref
            else f"Open assumptions: {NOT_RECORDED}.")
        if sources.assumptions_ref:
            lines.append("")
            lines.append(f"Assumption log: {_link('assumptions', sources.assumptions_ref)}")
        lines.append("")
        return lines
    lines += [f"- {a}" for a in sources.open_assumptions]
    if sources.assumptions_ref:
        lines.append(f"- Full log: {_link('assumptions', sources.assumptions_ref)}")
    lines.append("")
    return lines


def _momentum_lines(sources: ReportSources) -> list[str]:
    lines = ["## Momentum", ""]
    flag = momentum_flag(list(sources.cycle_records))
    if flag == MOMENTUM_UNKNOWN:
        lines += [f"Momentum: {NOT_RECORDED} (no cycle records).", ""]
        return lines
    if flag == MOMENTUM_CIRCLING:
        lines.append("⚠️ **Circling** — the same failure recurred, or open items "
                     "did not decrease over a round.")
        lines.append(f"- {CIRCLING_ESCALATION}")
        lines.append("")
        return lines
    lines += ["✅ Forward — every round closed items and nothing recurred.", ""]
    return lines


def _milestone_lines(sources: ReportSources) -> list[str]:
    lines = ["## Milestone", ""]
    mirror = sources.status_mirror
    if mirror is None:
        # Computed from the STATUS mirror or not at all — a hand-maintained
        # count is the exact thing this feature exists to prevent.
        lines += [f"Milestone distance: {NOT_RECORDED} (no STATUS mirror).", ""]
        return lines
    lines.append(
        f"- {mirror.remaining_to_milestone} features remain to {mirror.milestone}")
    lines.append("")
    return lines


def _capability_lines(sources: ReportSources) -> list[str]:
    lines = ["## Capabilities", ""]
    mirror = sources.status_mirror
    if mirror is None:
        lines += [f"- Can now: {NOT_RECORDED} (no STATUS mirror)"]
    elif mirror.accepted_capabilities:
        # P1: ONLY accepted [x] state may appear here.  A9: capped like every
        # other unbounded list — the ledger has 28 accepted entries today and
        # roughly 250 at roadmap end, and a report that lists them all is no
        # longer a summary of THIS run.
        lines += _capped([f"- Can now: {c}" for c in mirror.accepted_capabilities],
                         MAX_CAPABILITY_LINES, "accepted features")
    else:
        lines += ["- Can now: nothing accepted yet"]
    if mirror is not None:
        # [~] state is work, not capability.  It never crosses into "can now".
        lines += _capped(
            [f"- In progress: {c}" for c in mirror.in_progress_capabilities],
            MAX_CAPABILITY_LINES, "accepted features")
    lines.append(f"- Can next: {_text(sources.next_capability)}")
    lines.append("")
    return lines


def _reference_lines(sources: ReportSources) -> list[str]:
    lines = ["## References", ""]
    lines.append(f"- Plan: {_link('plan', sources.plan_ref) if sources.plan_ref else NOT_RECORDED}")
    lines.append(
        f"- Run manifest: "
        f"{_link('run_manifest.json', sources.manifest_ref) if sources.manifest_ref else NOT_RECORDED}")
    lines.append("")
    return lines


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def render_report_from_sources(sources: ReportSources, *,
                               mode: str = MODE_FINAL,
                               rendered_at: str = "") -> str:
    """The renderer proper: structured sources in, markdown out.

    Deterministic by construction — no clock, no disk, no randomness.  The
    only time value is *rendered_at*, which the caller supplies, so two
    renders of the same sources are byte-identical.
    """
    if mode not in VALID_MODES:
        raise ReportError(f"unknown report mode: {mode!r}")
    if mode == MODE_INTERIM and not rendered_at:
        raise ReportError("interim mode requires rendered_at — an unlabeled "
                          "snapshot cannot be told apart from a final report")

    lines: list[str] = []
    lines += _header_lines(sources, mode, rendered_at)
    lines += _task_lines(sources)
    lines += _blocked_lines(sources)
    lines += _dod_lines(sources)
    lines += _decision_lines(sources)
    lines += _cost_lines(sources)
    lines += _cycle_lines(sources)
    lines += _assumption_lines(sources)
    lines += _momentum_lines(sources)
    lines += _milestone_lines(sources)
    lines += _capability_lines(sources)
    lines += _reference_lines(sources)
    for note in sources.notes:
        lines.append(f"> {note}")
    if sources.notes:
        lines.append("")
    lines.append("## Recommended next action")
    lines.append("")
    lines.append(recommended_next_action(sources).render())
    lines.append("")
    return "\n".join(lines)


def render_report(job: Any, mode: str = MODE_FINAL, *,
                  sources: ReportSources | None = None,
                  rendered_at: str = "") -> str:
    """Render the report for *job* (T1_F053.md Design signature).

    *sources* overrides collection, which is how the goldens stay pure: tests
    hand in fixtures instead of a data root.  When it is None the sources are
    collected from the job and its evidence area, best effort — a source that
    cannot be read is a ``not recorded`` line, never a raised exception, and
    never a substituted value.
    """
    if mode not in VALID_MODES:
        raise ReportError(f"unknown report mode: {mode!r}")
    if sources is None:
        sources = collect_report_sources(job)
    if mode == MODE_INTERIM and not rendered_at:
        rendered_at = datetime.now(timezone.utc).isoformat()
    return render_report_from_sources(sources, mode=mode, rendered_at=rendered_at)


def _job_repo_root(job: Any) -> str:
    """The repository this job ran against, or "" when that is not knowable.

    ``packages.core.models.Job`` carries no repo path — the persisted
    ``pingpong_job.JobPlan`` does (``repo_path``), which is the same source the
    cycle loop reads its budget actuals from.  An unreadable or absent plan is
    not an error here: it means the milestone is simply not knowable, and the
    report says "not recorded" rather than guessing a repository.
    """
    try:
        from packages.orchestration.pingpong_job import load_job_plan

        plan = load_job_plan(str(getattr(job, "id", "") or ""))
    except Exception:  # noqa: BLE001 — a report must not depend on the plan store
        return ""
    return str(getattr(plan, "repo_path", "") or "") if plan is not None else ""


def collect_report_sources(job: Any) -> ReportSources:
    """Gather the report's sources off an in-memory job.

    The STATUS mirror is read here when — and only when — a repo root is
    knowable and that repo carries the ledger (F053 T002, DECISION D2); a run
    against somebody else's repository has no milestone and renders
    "not recorded".  The remaining evidence-area sources (cycle records,
    postmortems, manifest) are attached by the terminal-state writer.
    """
    from packages.orchestration.loop_run import LOOP_REF_METADATA_KEY
    from packages.orchestration.status_mirror import read_status_mirror

    tasks = tuple(
        TaskOutcome(
            task_id=str(getattr(t, "id", ""))[:8],
            description=str(getattr(t, "description", "") or ""),
            status=getattr(getattr(t, "status", None), "value",
                           str(getattr(t, "status", "") or "")),
        )
        for t in (getattr(job, "tasks", None) or ())
    )
    metadata = getattr(job, "metadata", None) or {}
    return ReportSources(
        job_id=str(getattr(job, "id", "") or ""),
        job_name=str(getattr(job, "name", "") or ""),
        project_id=str(getattr(job, "project_id", "") or ""),
        mission=str(getattr(job, "mission", "") or ""),
        loop_ref=str(metadata.get(LOOP_REF_METADATA_KEY, "") or ""),
        state=getattr(getattr(job, "state", None), "value",
                      str(getattr(job, "state", "") or "")),
        terminal_status=str(metadata.get("cycle_terminal_status", "") or ""),
        stop_reason=str(metadata.get("cycle_stop_reason", "") or ""),
        tasks=tasks,
        status_mirror=read_status_mirror(_job_repo_root(job) or None),
    )


# ---------------------------------------------------------------------------
# Evidence-area sources and the ONE writer (T002)
# ---------------------------------------------------------------------------


def _evidence_sources(job: Any) -> dict[str, Any]:
    """Evidence-area sources for a job, each read independently.

    Every read is guarded on its own: one unreadable source must not cost the
    report the others.  A source that cannot be read is simply absent, and
    absent renders "not recorded" — the same rule everywhere (P6).
    """
    job_id = str(getattr(job, "id", "") or "")
    extra: dict[str, Any] = {}

    try:
        from packages.orchestration.long_run_executor import read_cycle_records

        extra["cycle_records"] = tuple(read_cycle_records(job_id))
    except Exception:  # noqa: BLE001 — an account of the run, not a gate on it
        pass

    # Costs come from the actuals the job runner persisted — the same source
    # `remedy job budget` reads.  The unmeasured notation is carried verbatim
    # from BudgetCounters; this module never re-derives a token number.
    try:
        from packages.orchestration.budget_guard import (
            counters_from_persisted,
            decode_persisted_budget_actuals,
        )
        from packages.orchestration.pingpong_job import load_job_plan

        plan = load_job_plan(job_id)
        actuals = getattr(plan, "budget_actuals", None) if plan is not None else None
        if actuals is not None:
            counters = counters_from_persisted(
                decode_persisted_budget_actuals(
                    actuals,
                    first_running_at=getattr(plan, "first_running_at", "") or None))
            extra["token_description"] = counters.token_description()
            extra["cost_basis"] = tuple(counters.actual_sources)
            extra["elapsed_seconds"] = counters.elapsed_seconds
    except Exception:  # noqa: BLE001 — no actuals is "not recorded", never a zero
        pass

    # F061 T004: the gate persists its last run beside the report. Absent file
    # = the job was never gated, which renders "not recorded" — never a green.
    try:
        from packages.orchestration.dod_gate import load_gate_result

        recorded = load_gate_result(job_id)
        if recorded is not None:
            extra["dod_released"] = bool(recorded.get("released"))
            extra["dod_checks"] = tuple(
                DoDCheckRow(
                    check_id=str(c.get("check_id", "")),
                    kind=str(c.get("kind", "")),
                    blocking=bool(c.get("blocking")),
                    status=str(c.get("status", "")),
                    reason=str(c.get("reason", "") or ""),
                    duration_ms=_as_int(c.get("duration_ms")),
                )
                for c in (recorded.get("checks") or [])
                if isinstance(c, dict)
            )
    except Exception:  # noqa: BLE001 — an unreadable gate record is "not recorded"
        pass

    try:
        from packages.orchestration.decision_queue import (
            list_decisions,
            open_decisions,
            render_open_decisions_lines,
        )

        decisions = list_decisions(job, [])
        still_open = open_decisions(decisions)
        extra["open_decision_count"] = len(still_open)
        extra["open_decision_lines"] = tuple(render_open_decisions_lines(decisions))
        extra["blocked"] = tuple(
            BlockedItem(
                task_id=d.related_node_id or d.id,
                reason=d.safe_summary,
                failure_class=d.type,
                answer_command=d.next_actions[0] if d.next_actions else "",
            )
            for d in still_open
        )
    except Exception:  # noqa: BLE001
        pass

    return extra


def _folded_apply_states(job: Any) -> dict[str, Any]:
    """Each task's folded apply state, keyed by the FULL task id, or ``{}``.

    Guarded on its own like every other evidence-area read in this module: an
    unreadable timeline, an unbuildable chain or a missing proof module costs
    the report this ONE clause and never the rest of it.  Absent renders as no
    clause at all, which is the same P6 rule as every other missing source —
    never an invented apply state.

    The fold itself lives in ``packages.orchestration.proof_chain`` beside the
    ``ProofChange.apply_state`` field it reads, so the report and the cockpit
    give the same answer and neither imports the other (finding R-0738).
    """
    try:
        from packages.orchestration.data_paths import resolve_data_root
        from packages.orchestration.proof_chain import (
            build_proof_chain,
            fold_task_apply_states,
        )
        from packages.orchestration.timeline import load_run_events

        job_id = str(getattr(job, "id", "") or "")
        if not job_id:
            return {}
        data_dir = resolve_data_root()
        events = load_run_events(data_dir, job_id)
        return fold_task_apply_states(
            build_proof_chain(job, events, data_dir=data_dir))
    except Exception:  # noqa: BLE001 — an account of the run, not a gate on it
        return {}


def _tasks_with_apply_state(job: Any, tasks: tuple[TaskOutcome, ...]
                            ) -> tuple[TaskOutcome, ...] | None:
    """*tasks* with each one's folded apply state attached, or None to change nothing.

    WHY THIS RE-READS ``job.tasks`` INSTEAD OF USING ``TaskOutcome.task_id``:
    ``collect_report_sources`` sets that field to ``str(t.id)[:8]``, a
    TRUNCATION, while ``fold_task_apply_states`` keys on the FULL task id.  Two
    tasks whose ids agree in their first eight characters would take each
    other's apply state if the truncated value were used as a lookup key.  So
    the full ids are re-read from the SAME iteration ``collect_report_sources``
    used, and paired positionally with the outcomes it produced; the truncated
    value is never a key.
    """
    folded = _folded_apply_states(job)
    if not folded or not tasks:
        return None
    full_ids = [str(getattr(t, "id", "") or "")
                for t in (getattr(job, "tasks", None) or ())]
    if len(full_ids) != len(tasks):
        # The two iterations disagree, so the pairing is not knowable.  Saying
        # nothing is the honest answer; guessing an alignment is not.
        return None
    attached: list[TaskOutcome] = []
    for full_id, outcome in zip(full_ids, tasks):
        state = folded.get(full_id)
        if state is None:
            attached.append(outcome)
            continue
        attached.append(replace(
            outcome,
            apply_state=str(getattr(state, "state", "") or ""),
            applied_changes=_as_int(getattr(state, "applied", 0)),
            total_changes=_as_int(getattr(state, "total", 0)),
        ))
    return tuple(attached)


def build_report_sources(job: Any) -> ReportSources:
    """The full source set: what lives on the job, plus its evidence area.

    This is what both the terminal writer and the CLI render from, so a final
    report and an interim snapshot of the same job describe it the same way.
    """
    base = collect_report_sources(job)
    extra = _evidence_sources(job)
    attached = _tasks_with_apply_state(job, base.tasks)
    if attached is not None:
        extra["tasks"] = attached
    if not extra:
        return base
    return replace(base, **extra)


def report_path(job_id: str) -> Path:
    """Where this job's one report lives.

    Built on the same ``job_evidence_dir`` every other job-level record uses —
    the report sits beside the ``cycles/`` directory, not in an area of its own.
    """
    from packages.orchestration.pingpong_job import job_evidence_dir
    from packages.orchestration.safe_points import validate_job_id

    return Path(job_evidence_dir(validate_job_id(job_id))) / REPORT_FILENAME


def write_final_report(job: Any, *, sources: ReportSources | None = None) -> Path | None:
    """Write THE final report for *job*, returning its path (or None on failure).

    One writer, one file, overwritten in place: a job that is resumed and then
    finishes again REGENERATES its report rather than appending to it, so the
    file always describes the run as it actually ended (F053 acceptance).

    Never raises. A failure is recorded on the job under
    ``REPORT_ERROR_METADATA_KEY`` and the run carries on — the report is an
    account of the run, and losing the account must not lose the run.
    """
    try:
        job_id = str(getattr(job, "id", "") or "")
        text = render_report_from_sources(
            sources if sources is not None else build_report_sources(job),
            mode=MODE_FINAL)
        path = report_path(job_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    except Exception as exc:  # noqa: BLE001 — see docstring
        metadata = getattr(job, "metadata", None)
        if isinstance(metadata, dict):
            metadata[REPORT_ERROR_METADATA_KEY] = f"{type(exc).__name__}: {exc}"
        return None
    metadata = getattr(job, "metadata", None)
    if isinstance(metadata, dict):
        metadata.pop(REPORT_ERROR_METADATA_KEY, None)
    return path
