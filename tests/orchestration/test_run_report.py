"""F053 T001 — the run report renders honestly, or it renders "not recorded".

The three goldens are the contract: a green run, a blocked run with an open
decision, and a budget-exhausted run.  Everything else here defends the one
rule that makes the report worth reading — every number names its basis, and
a number that was never measured is never printed.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

import pytest

from packages.orchestration import loop_run, proof_chain
from packages.orchestration.run_report import (
    CIRCLING_ESCALATION,
    MODE_FINAL,
    MODE_INTERIM,
    MOMENTUM_CIRCLING,
    MOMENTUM_FORWARD,
    MOMENTUM_UNKNOWN,
    NEXT_ACTION_CONDITIONS,
    NEXT_ACTION_RULES,
    NOT_RECORDED,
    BlockedItem,
    NextAction,
    ReportError,
    ReportSources,
    StatusMirror,
    TaskOutcome,
    build_report_sources,
    momentum_flag,
    recommended_next_action,
    render_report,
    render_report_from_sources,
)
from packages.orchestration.status_mirror import (
    parse_status_ledger,
    read_status_mirror,
)

pytestmark = pytest.mark.unit


# ---------------------------------------------------------------------------
# Fixtures — three terminal states, built as data, never read from disk
# ---------------------------------------------------------------------------


def _green_sources() -> ReportSources:
    """All tasks completed, one clean cycle, actuals fully measured."""
    return ReportSources(
        job_id="11111111-1111-4111-8111-111111111111",
        job_name="green run",
        project_id="remedy",
        mission="Add the run report",
        state="completed",
        terminal_status="all_green",
        duration_text="4m 12s",
        tasks=(
            TaskOutcome("aaaaaaaa", "Write the renderer", "completed",
                        evidence_ref="tasks/aaaaaaaa/output.md"),
            TaskOutcome("bbbbbbbb", "Write the tests", "completed",
                        evidence_ref="tasks/bbbbbbbb/output.md"),
        ),
        token_description="4200 tokens",
        cost_basis=("pingpong_actuals",),
        elapsed_seconds=252.0,
        cycle_records=(
            {"cycle_index": 1, "tasks_completed": 2, "tasks_failed": 0,
             "tasks_escalated": 0, "verify_result": "passed",
             "verify_failure_class": ""},
        ),
        open_decision_count=0,
        assumptions_ref="assumptions.md",
        plan_ref="plan.md",
        manifest_ref="run_manifest.json",
        status_mirror=StatusMirror(
            milestone="F075",
            remaining_to_milestone=21,
            accepted_capabilities=("plan and execute a job",),
            in_progress_capabilities=("write a run report",),
        ),
        next_capability="report every run without being asked",
    )


def _blocked_decision_sources() -> ReportSources:
    """A task raised a question; its branch waits, and the report says how."""
    answer = ('remedy decision resolve 22222222 td:cccccccc '
              '--reason "<your answer>"')
    return ReportSources(
        job_id="22222222-2222-4222-8222-222222222222",
        job_name="blocked run",
        project_id="remedy",
        mission="Migrate the store",
        state="paused",
        terminal_status="blocked",
        stop_reason="task raised a decision",
        duration_text="1m 30s",
        tasks=(
            TaskOutcome("cccccccc", "Choose the migration order", "paused",
                        evidence_ref="tasks/cccccccc/output.md"),
            TaskOutcome("dddddddd", "Apply the migration", "pending"),
        ),
        blocked=(
            BlockedItem(
                task_id="cccccccc",
                reason="needs a decision on the migration order",
                failure_class="needs_decision",
                answer_command=answer,
                evidence_ref="tasks/cccccccc/postmortem.json",
            ),
        ),
        token_description="1800 tokens",
        cost_basis=("pingpong_actuals",),
        elapsed_seconds=90.0,
        cycle_records=(
            {"cycle_index": 1, "tasks_completed": 0, "tasks_failed": 0,
             "tasks_escalated": 1, "verify_result": "not_run",
             "verify_failure_class": ""},
        ),
        open_decision_lines=(
            "Open decisions: 1 — the run needs an answer",
            "  [blocker] task_decision td:cccccccc: needs a decision on the "
            "migration order",
            f"    -> {answer}",
        ),
        open_decision_count=1,
        open_assumptions=("A9: unmeasured provider calls count as unmeasured",),
        assumptions_ref="assumptions.md",
        plan_ref="plan.md",
        manifest_ref="run_manifest.json",
        status_mirror=StatusMirror(
            milestone="F075", remaining_to_milestone=21,
            accepted_capabilities=("plan and execute a job",)),
        next_capability="answer decisions from the CLI",
    )


def _budget_sources() -> ReportSources:
    """Stopped on budget, with unmeasured provider calls and a healed cycle."""
    return ReportSources(
        job_id="33333333-3333-4333-8333-333333333333",
        job_name="budget run",
        project_id="remedy",
        mission="Refactor the verifier",
        state="paused",
        terminal_status="budget_exhausted",
        stop_reason="budget_exhausted:tokens",
        duration_text="12m 05s",
        tasks=(
            TaskOutcome("eeeeeeee", "Refactor the verifier", "failed",
                        evidence_ref="tasks/eeeeeeee/output.md"),
        ),
        blocked=(
            BlockedItem(
                task_id="eeeeeeee",
                reason="budget exhausted before the task finished",
                failure_class="budget_exhausted",
                evidence_ref="tasks/eeeeeeee/postmortem.json",
            ),
        ),
        # The unmeasured notation is carried VERBATIM from
        # budget_guard.BudgetCounters.token_description().
        token_description=">= 91000 tokens (3 provider calls unmeasured)",
        cost_basis=("pingpong_actuals", "provider_evidence"),
        elapsed_seconds=725.0,
        cycle_records=(
            {"cycle_index": 1, "tasks_completed": 0, "tasks_failed": 1,
             "tasks_escalated": 0, "verify_result": "failed",
             "verify_failure_class": "test_failed",
             "repair_rounds_used": 2, "healed_after_repair": True,
             "healed_without_changes": True,
             "repair_summary": "2 rounds; verify passed again"},
        ),
        open_decision_count=0,
        assumptions_ref="assumptions.md",
        plan_ref="plan.md",
        manifest_ref="run_manifest.json",
        status_mirror=StatusMirror(
            milestone="F075", remaining_to_milestone=21,
            accepted_capabilities=("plan and execute a job",)),
        next_capability="raise the budget and resume",
        notes=("Normalization: 1 provider response was re-encoded to UTF-8.",),
    )


# ---------------------------------------------------------------------------
# Golden reports
# ---------------------------------------------------------------------------


GOLDEN_GREEN = """\
# Run report — green run

- Job: `11111111-1111-4111-8111-111111111111`
- Project: remedy
- Mission: Add the run report
- State: completed
- Terminal status: all_green
- Duration: 4m 12s

## Tasks

- `aaaaaaaa` — Write the renderer — **completed** — [evidence](tasks/aaaaaaaa/output.md)
- `bbbbbbbb` — Write the tests — **completed** — [evidence](tasks/bbbbbbbb/output.md)

## Blocked

Nothing blocked.

## Definition of Done

Definition of Done: not recorded.

## Open decisions

No open decisions.

## Cost

- Tokens: 4200 tokens — basis: pingpong_actuals
- Elapsed: 252.0s — basis: budget counters

## Cycles

- Cycle 1: 2 completed, 0 failed, 0 escalated — verify: passed

## Open assumptions

No open assumptions.

Assumption log: [assumptions](assumptions.md)

## Momentum

✅ Forward — every round closed items and nothing recurred.

## Milestone

- 21 features remain to F075

## Capabilities

- Can now: plan and execute a job
- In progress: write a run report
- Can next: report every run without being asked

## References

- Plan: [plan](plan.md)
- Run manifest: [run_manifest.json](run_manifest.json)

## Recommended next action

Review and merge the branch  _(rule: all-green — every task completed and nothing is open)_
"""


GOLDEN_BLOCKED = """\
# Run report — blocked run

- Job: `22222222-2222-4222-8222-222222222222`
- Project: remedy
- Mission: Migrate the store
- State: paused
- Terminal status: blocked
- Stop reason: task raised a decision
- Duration: 1m 30s

## Tasks

- `cccccccc` — Choose the migration order — **paused** — [evidence](tasks/cccccccc/output.md)
- `dddddddd` — Apply the migration — **pending**

## Blocked

- `cccccccc` — needs a decision on the migration order — class: needs_decision — [postmortem](tasks/cccccccc/postmortem.json)
  - answer with: `remedy decision resolve 22222222 td:cccccccc --reason "<your answer>"`

## Definition of Done

Definition of Done: not recorded.

## Open decisions

Open decisions: 1 — the run needs an answer
  [blocker] task_decision td:cccccccc: needs a decision on the migration order
    -> remedy decision resolve 22222222 td:cccccccc --reason "<your answer>"

## Cost

- Tokens: 1800 tokens — basis: pingpong_actuals
- Elapsed: 90.0s — basis: budget counters

## Cycles

- Cycle 1: 0 completed, 0 failed, 1 escalated — verify: not_run

## Open assumptions

- A9: unmeasured provider calls count as unmeasured
- Full log: [assumptions](assumptions.md)

## Momentum

✅ Forward — every round closed items and nothing recurred.

## Milestone

- 21 features remain to F075

## Capabilities

- Can now: plan and execute a job
- Can next: answer decisions from the CLI

## References

- Plan: [plan](plan.md)
- Run manifest: [run_manifest.json](run_manifest.json)

## Recommended next action

Answer the open decision: `remedy decision resolve 22222222 td:cccccccc --reason "<your answer>"`  _(rule: open-decision — an open decision is waiting for an answer)_
"""


GOLDEN_BUDGET = """\
# Run report — budget run

- Job: `33333333-3333-4333-8333-333333333333`
- Project: remedy
- Mission: Refactor the verifier
- State: paused
- Terminal status: budget_exhausted
- Stop reason: budget_exhausted:tokens
- Duration: 12m 05s

## Tasks

- `eeeeeeee` — Refactor the verifier — **failed** — [evidence](tasks/eeeeeeee/output.md)

## Blocked

- `eeeeeeee` — budget exhausted before the task finished — class: budget_exhausted — [postmortem](tasks/eeeeeeee/postmortem.json)

## Definition of Done

Definition of Done: not recorded.

## Open decisions

No open decisions.

## Cost

- Tokens: >= 91000 tokens (3 provider calls unmeasured) — basis: pingpong_actuals, provider_evidence
- Elapsed: 725.0s — basis: budget counters

## Cycles

- Cycle 1: 0 completed, 1 failed, 0 escalated — verify: failed — failure class: test_failed
  - healed after 2 repair round(s) — WITHOUT file changes (flake suspect)
  - repair: 2 rounds; verify passed again

## Open assumptions

No open assumptions.

Assumption log: [assumptions](assumptions.md)

## Momentum

✅ Forward — every round closed items and nothing recurred.

## Milestone

- 21 features remain to F075

## Capabilities

- Can now: plan and execute a job
- Can next: raise the budget and resume

## References

- Plan: [plan](plan.md)
- Run manifest: [run_manifest.json](run_manifest.json)

> Normalization: 1 provider response was re-encoded to UTF-8.

## Recommended next action

Inspect [the postmortem](tasks/eeeeeeee/postmortem.json) and repair the blocked task  _(rule: blocked-failed — the run is blocked or a task failed)_
"""


class TestGoldenReports:
    """The three fixture terminals from T1_F053.md Acceptance."""

    def test_green_terminal_matches_golden(self):
        assert render_report_from_sources(_green_sources()) == GOLDEN_GREEN

    def test_blocked_with_decision_matches_golden(self):
        assert render_report_from_sources(_blocked_decision_sources()) == GOLDEN_BLOCKED

    def test_budget_terminal_matches_golden(self):
        assert render_report_from_sources(_budget_sources()) == GOLDEN_BUDGET


class TestCostBasis:
    """Every number names where it came from, or it is not a number (P6)."""

    @pytest.mark.parametrize("sources", [
        _green_sources(), _blocked_decision_sources(), _budget_sources(),
    ])
    def test_every_cost_line_carries_a_basis(self, sources):
        cost_lines = [
            line for line in render_report_from_sources(sources).splitlines()
            if line.startswith("- Tokens:") or line.startswith("- Elapsed:")
        ]
        assert cost_lines, "the cost section rendered no lines at all"
        for line in cost_lines:
            assert " — basis: " in line, f"cost line without a basis: {line}"

    def test_unmeasured_notation_is_carried_verbatim(self):
        """The notation comes from BudgetCounters.token_description(); the
        report never re-words it, because a re-worded caveat is a new claim."""
        report = render_report_from_sources(_budget_sources())
        assert ">= 91000 tokens (3 provider calls unmeasured)" in report


class TestMissingSourcesAreNotInvented:
    """The negative test: nothing is filled in, ever."""

    def test_missing_actuals_render_not_recorded(self):
        sources = ReportSources(job_name="no actuals", token_description="")
        report = render_report_from_sources(sources)
        assert f"Tokens: {NOT_RECORDED}" in report

    def test_missing_actuals_never_render_a_zero(self):
        """A zero is a measurement. A run with no actuals made none."""
        sources = ReportSources(job_name="no actuals", token_description="")
        cost = _section(render_report_from_sources(sources), "Cost")
        assert not re.search(r"\b0 tokens\b", cost), cost
        assert "0.0s" not in cost, cost

    def test_every_absent_source_names_itself(self):
        """An empty ReportSources renders a report made only of gaps — and
        every gap says so rather than rendering an empty section."""
        report = render_report_from_sources(ReportSources())
        for heading in ("Tasks", "Open decisions", "Cost", "Cycles",
                        "Open assumptions", "Momentum", "Milestone",
                        "Capabilities"):
            assert NOT_RECORDED in _section(report, heading), heading

    def test_missing_status_mirror_does_not_invent_a_milestone(self):
        report = render_report_from_sources(ReportSources(job_name="x"))
        milestone = _section(report, "Milestone")
        assert NOT_RECORDED in milestone
        assert not re.search(r"\d+ features remain", milestone), milestone

    def test_in_progress_state_never_becomes_a_capability(self):
        """P1: only accepted [x] state may say "can now"."""
        sources = ReportSources(
            job_name="x",
            status_mirror=StatusMirror(
                milestone="F075", remaining_to_milestone=3,
                accepted_capabilities=(),
                in_progress_capabilities=("write a run report",)))
        capabilities = _section(render_report_from_sources(sources), "Capabilities")
        assert "- In progress: write a run report" in capabilities
        assert "- Can now: write a run report" not in capabilities
        assert "- Can now: nothing accepted yet" in capabilities


class TestInterimMode:
    """A snapshot that could pass for a final report is the whole risk."""

    def test_interim_renders_the_loud_label(self):
        report = render_report_from_sources(
            _green_sources(), mode=MODE_INTERIM,
            rendered_at="2026-07-31T10:00:00+00:00")
        assert report.splitlines()[0] == (
            "> **INTERIM SNAPSHOT — run still in progress "
            "(rendered at 2026-07-31T10:00:00+00:00)**")

    def test_final_mode_has_no_interim_label(self):
        assert "INTERIM SNAPSHOT" not in render_report_from_sources(_green_sources())

    def test_interim_keeps_the_same_structure(self):
        """Same sections, same order — only the banner differs."""
        final = render_report_from_sources(_green_sources())
        interim = render_report_from_sources(
            _green_sources(), mode=MODE_INTERIM, rendered_at="2026-07-31T10:00:00+00:00")
        assert _headings(interim) == _headings(final)

    def test_interim_without_a_timestamp_is_refused(self):
        with pytest.raises(ReportError, match="rendered_at"):
            render_report_from_sources(_green_sources(), mode=MODE_INTERIM)

    def test_interim_does_not_mutate_the_sources(self):
        sources = _green_sources()
        before = repr(sources)
        render_report_from_sources(sources, mode=MODE_INTERIM,
                                   rendered_at="2026-07-31T10:00:00+00:00")
        assert repr(sources) == before


class TestDeterminism:
    """No clock, no disk, no randomness — twice is the same bytes."""

    @pytest.mark.parametrize("sources", [
        _green_sources(), _blocked_decision_sources(), _budget_sources(),
    ])
    def test_double_render_is_byte_identical(self, sources):
        assert render_report_from_sources(sources) == render_report_from_sources(sources)

    def test_double_render_of_interim_is_byte_identical(self):
        ts = "2026-07-31T10:00:00+00:00"
        first = render_report_from_sources(_green_sources(), mode=MODE_INTERIM,
                                           rendered_at=ts)
        second = render_report_from_sources(_green_sources(), mode=MODE_INTERIM,
                                            rendered_at=ts)
        assert first == second

    def test_rebuilt_fixtures_render_identically(self):
        """Two independently built fixtures with the same content agree —
        catches ordering that depends on object identity."""
        assert render_report_from_sources(_green_sources()) == \
            render_report_from_sources(_green_sources())


class TestStatusMirrorProducer:
    """F053 T002 / DECISION D2 — the ledger reader the feature presumed existed.

    The fixture is the self-repo's ledger SHAPE, not the file itself: pinning
    the real STATUS.md would make these tests fail every time the roadmap
    advances, which is a test that measures the calendar.
    """

    LEDGER = """\
# REMEDY STATUS — Execution-Order Truth

> Grammar: `[ ]` todo · `[~]` in progress · `[x]` done · `[!]` blocked.

## Tier 0 — Foundation & Trust Core

- [x] F001 — Adaptive provider timeouts (PR #123 · commit 4856006 · PASS)
- [x] F003 — Real token/cost measurement (PR #123 · evidence: some.zip)
- [~] F053 — Final & interim report
- [ ] F056 — Missions: persistent goal
- [ ] F075 — MILESTONE GATE: 10 flawless self-runs
- [ ] F080 — Machine-readable roadmap mirror
"""

    def test_milestone_and_distance_come_from_the_ledger(self):
        mirror = parse_status_ledger(self.LEDGER)
        assert mirror is not None
        assert mirror.milestone == "F075"
        # F053 [~], F056 [ ], F075 [ ] — the milestone counts itself in.
        assert mirror.remaining_to_milestone == 3

    def test_entries_after_the_milestone_are_not_counted(self):
        """F080 sits below the gate and must not inflate the distance."""
        assert parse_status_ledger(self.LEDGER).remaining_to_milestone == 3

    def test_capabilities_split_accepted_from_in_progress(self):
        """P1 again, at the source: [x] is capability, [~] is work."""
        mirror = parse_status_ledger(self.LEDGER)
        assert mirror.accepted_capabilities == (
            "Adaptive provider timeouts", "Real token/cost measurement")
        assert mirror.in_progress_capabilities == ("Final & interim report",)

    def test_evidence_parenthetical_is_stripped_from_capabilities(self):
        """A "can now" line carrying a zip filename helps nobody."""
        for capability in parse_status_ledger(self.LEDGER).accepted_capabilities:
            assert "PR #" not in capability
            assert ".zip" not in capability

    def test_an_explicit_milestone_id_overrides_the_gate_line(self):
        mirror = parse_status_ledger(self.LEDGER, milestone_id="F056")
        assert mirror.milestone == "F056"
        assert mirror.remaining_to_milestone == 2

    def test_blocked_entries_do_not_count_toward_the_distance(self):
        ledger = self.LEDGER.replace("- [ ] F056 — Missions: persistent goal",
                                     "- [!] F056 — Missions: persistent goal")
        assert parse_status_ledger(ledger).remaining_to_milestone == 2

    @pytest.mark.parametrize("text,why", [
        ("", "empty file"),
        ("# STATUS\n\nNothing here at all.\n", "no entries"),
        ("- [ ] F001 — Something\n- [x] F002 — Something else\n", "no milestone"),
    ])
    def test_an_untrustworthy_ledger_yields_none_not_a_guess(self, text, why):
        assert parse_status_ledger(text) is None, why

    def test_a_missing_repo_or_ledger_yields_none(self, tmp_path):
        assert read_status_mirror(None) is None
        assert read_status_mirror("") is None
        assert read_status_mirror(tmp_path) is None          # repo without a ledger

    def test_a_real_repo_root_is_read(self, tmp_path):
        ledger = tmp_path / "docs" / "roadmap"
        ledger.mkdir(parents=True)
        (ledger / "STATUS.md").write_text(self.LEDGER, encoding="utf-8")
        mirror = read_status_mirror(tmp_path)
        assert mirror is not None and mirror.milestone == "F075"

    def test_an_unreadable_ledger_never_raises_into_a_render(self, tmp_path):
        """A directory where the file should be: absent, not an exception."""
        (tmp_path / "docs" / "roadmap" / "STATUS.md").mkdir(parents=True)
        assert read_status_mirror(tmp_path) is None

    def test_the_mirror_feeds_the_report_sections(self, tmp_path):
        ledger = tmp_path / "docs" / "roadmap"
        ledger.mkdir(parents=True)
        (ledger / "STATUS.md").write_text(self.LEDGER, encoding="utf-8")
        sources = ReportSources(job_name="x",
                                status_mirror=read_status_mirror(tmp_path))
        report = render_report_from_sources(sources)
        assert "- 3 features remain to F075" in _section(report, "Milestone")
        capabilities = _section(report, "Capabilities")
        assert "- Can now: Adaptive provider timeouts" in capabilities
        assert "- In progress: Final & interim report" in capabilities
        assert "- Can now: Final & interim report" not in capabilities

    def test_a_repo_without_a_ledger_renders_not_recorded(self, tmp_path):
        sources = ReportSources(job_name="x",
                                status_mirror=read_status_mirror(tmp_path))
        assert NOT_RECORDED in _section(render_report_from_sources(sources),
                                        "Milestone")


class TestStoppedByOperatorRule:
    """DECISION D2: a run stopped on purpose is not a broken run."""

    def _stopped(self, **overrides) -> ReportSources:
        base = dict(job_name="stopped run", terminal_status="stopped_by_operator",
                    stop_reason="operator requested stop",
                    tasks=(TaskOutcome("aaaaaaaa", "Do the thing", "paused"),))
        base.update(overrides)
        return ReportSources(**base)

    def test_an_operator_stop_gets_its_own_rule(self):
        assert recommended_next_action(self._stopped()).rule_id == "stopped-by-operator"

    def test_the_action_is_the_amendment_wording(self):
        action = recommended_next_action(self._stopped()).action
        assert action == ("Resume the run (or close it) — it stopped on "
                          "request, nothing is broken")

    def test_it_never_sends_the_operator_to_a_postmortem(self):
        """The false alarm this rule exists to prevent."""
        report = render_report_from_sources(self._stopped())
        assert "postmortem" not in _section(report, "Recommended next action")

    def test_an_open_decision_still_outranks_it(self):
        """Ranked BETWEEN open-decision and blocked-failed — so it loses here."""
        sources = self._stopped(open_decision_count=1)
        assert recommended_next_action(sources).rule_id == "open-decision"

    def test_it_outranks_the_blocked_rule(self):
        """…and wins here, even with a blocked item present."""
        sources = self._stopped(blocked=(
            BlockedItem("aaaaaaaa", "stopped mid-flight", failure_class="stopped"),))
        assert recommended_next_action(sources).rule_id == "stopped-by-operator"

    def test_other_stop_terminals_still_route_to_the_postmortem(self):
        for terminal in ("blocked", "budget_exhausted", "deadline_reached"):
            sources = self._stopped(terminal_status=terminal)
            assert recommended_next_action(sources).rule_id == "blocked-failed", terminal

    def test_the_rule_table_order_is_the_documented_priority(self):
        ids = [rule_id for rule_id, _condition in NEXT_ACTION_RULES]
        assert ids == ["open-decision", "stopped-by-operator", "blocked-failed",
                       "all-green", "indeterminate"]

    def test_the_new_rule_is_documented_like_every_other(self):
        assert NEXT_ACTION_CONDITIONS["stopped-by-operator"] == (
            "the run stopped on operator request")


class TestNextActionRuleTable:
    """Exactly one recommendation, and its rule is documented."""

    def test_exactly_one_recommendation_line(self):
        for sources in (_green_sources(), _blocked_decision_sources(),
                        _budget_sources()):
            body = _section(render_report_from_sources(sources),
                            "Recommended next action")
            lines = [line for line in body.splitlines() if line.strip()]
            assert len(lines) == 1, lines

    def test_open_decision_outranks_a_failure(self):
        """A run that is both blocked AND awaiting an answer asks for the
        answer: no repair gets past an unanswered question."""
        sources = _blocked_decision_sources()
        assert recommended_next_action(sources).rule_id == "open-decision"

    def test_blocked_without_a_decision_points_at_the_postmortem(self):
        assert recommended_next_action(_budget_sources()).rule_id == "blocked-failed"

    def test_all_green_recommends_the_branch(self):
        assert recommended_next_action(_green_sources()).rule_id == "all-green"

    def test_unknown_state_is_indeterminate_not_a_guess(self):
        action = recommended_next_action(ReportSources())
        assert action.rule_id == "indeterminate"
        assert NOT_RECORDED in action.action

    def test_every_rule_id_is_documented(self):
        for sources in (_green_sources(), _blocked_decision_sources(),
                        _budget_sources(), ReportSources()):
            assert recommended_next_action(sources).rule_id in NEXT_ACTION_CONDITIONS

    def test_an_undocumented_rule_cannot_be_built(self):
        with pytest.raises(ReportError, match="undocumented rule"):
            NextAction("made-up", "do something")

    def test_the_answer_command_is_never_abbreviated(self):
        """A command that is not shown in full cannot be pasted."""
        report = render_report_from_sources(_blocked_decision_sources())
        command = ('remedy decision resolve 22222222 td:cccccccc '
                   '--reason "<your answer>"')
        # Blocked item, open-decisions block, recommendation — in full each time.
        assert report.count(command) == 3
        assert "…" not in report


class TestMomentumFlag:
    """The mechanical definition, not a feeling."""

    def test_no_cycles_is_unknown(self):
        assert momentum_flag([]) == MOMENTUM_UNKNOWN
        assert momentum_flag(None) == MOMENTUM_UNKNOWN

    def test_closing_items_is_forward(self):
        records = [
            {"cycle_index": 1, "tasks_failed": 3, "tasks_escalated": 0},
            {"cycle_index": 2, "tasks_failed": 1, "tasks_escalated": 0},
            {"cycle_index": 3, "tasks_failed": 0, "tasks_escalated": 0},
        ]
        assert momentum_flag(records) == MOMENTUM_FORWARD

    def test_a_recurring_failure_class_is_circling(self):
        records = [
            {"cycle_index": 1, "tasks_failed": 2, "verify_failure_class": "test_failed"},
            {"cycle_index": 2, "tasks_failed": 1, "verify_failure_class": "test_failed"},
        ]
        assert momentum_flag(records) == MOMENTUM_CIRCLING

    def test_open_items_not_decreasing_is_circling(self):
        records = [
            {"cycle_index": 1, "tasks_failed": 2, "tasks_escalated": 0},
            {"cycle_index": 2, "tasks_failed": 2, "tasks_escalated": 0},
        ]
        assert momentum_flag(records) == MOMENTUM_CIRCLING

    def test_circling_renders_a_warning_and_an_escalation(self):
        sources = ReportSources(
            job_name="circling",
            cycle_records=(
                {"cycle_index": 1, "tasks_failed": 2,
                 "verify_failure_class": "test_failed"},
                {"cycle_index": 2, "tasks_failed": 2,
                 "verify_failure_class": "test_failed"},
            ))
        momentum = _section(render_report_from_sources(sources), "Momentum")
        assert "Circling" in momentum
        assert CIRCLING_ESCALATION in momentum

    def test_a_heal_is_never_silent(self):
        """F052 risk visibility: a healed cycle says so in the report."""
        cycles = _section(render_report_from_sources(_budget_sources()), "Cycles")
        assert "healed after 2 repair round(s)" in cycles
        assert "WITHOUT file changes (flake suspect)" in cycles


class TestBigRuns:
    """A9: the report is a summary; the evidence area is the archive."""

    def test_task_lines_cap_with_an_honest_count(self):
        sources = ReportSources(
            job_name="huge",
            tasks=tuple(TaskOutcome(f"t{i:04d}", f"task {i}", "completed")
                        for i in range(60)))
        tasks = _section(render_report_from_sources(sources), "Tasks")
        assert "… and 40 more tasks (see evidence)" in tasks
        assert len([line for line in tasks.splitlines() if line.startswith("- `")]) == 20

    def test_a_short_list_is_never_capped(self):
        tasks = _section(render_report_from_sources(_green_sources()), "Tasks")
        assert "more tasks" not in tasks

    def test_capability_lines_cap_with_an_honest_count(self):
        """CALL-2 ruling: capabilities grow with the ROADMAP, not the run."""
        sources = ReportSources(
            job_name="mature",
            status_mirror=StatusMirror(
                milestone="F075", remaining_to_milestone=3,
                accepted_capabilities=tuple(f"feature {i}" for i in range(30))))
        capabilities = _section(render_report_from_sources(sources), "Capabilities")
        can_now = [line for line in capabilities.splitlines()
                   if line.startswith("- Can now: ")]
        assert len(can_now) == 10
        assert "… and 20 more accepted features (see evidence)" in capabilities

    def test_the_goldens_are_below_the_capability_cap(self):
        """One accepted capability: capped output must be identical to before."""
        capabilities = _section(render_report_from_sources(_green_sources()),
                                "Capabilities")
        assert "- Can now: plan and execute a job" in capabilities
        assert "more accepted features" not in capabilities


class TestLanguageAndQuoting:
    """Reports are English; the mission is quoted as-is (A9)."""

    def test_report_is_english_for_a_non_english_mission(self):
        sources = ReportSources(
            job_name="lauf",
            mission="Baue den Bericht und prüfe die Kosten",
            tasks=(TaskOutcome("aaaaaaaa", "Renderer schreiben", "completed"),))
        report = render_report_from_sources(sources)
        assert "# Run report — lauf" in report
        assert "## Recommended next action" in report
        assert "- Mission: Baue den Bericht und prüfe die Kosten" in report

    def test_task_descriptions_are_quoted_not_translated(self):
        sources = ReportSources(
            job_name="lauf",
            tasks=(TaskOutcome("aaaaaaaa", "Renderer schreiben", "completed"),))
        assert "Renderer schreiben" in render_report_from_sources(sources)


class TestRenderReportEntryPoint:
    """render_report(job, mode) is the signature T1_F053.md specifies."""

    def test_render_report_accepts_injected_sources(self):
        report = render_report(object(), MODE_FINAL, sources=_green_sources())
        assert report == GOLDEN_GREEN

    def test_render_report_rejects_an_unknown_mode(self):
        with pytest.raises(ReportError, match="unknown report mode"):
            render_report(object(), "summary", sources=_green_sources())

    def test_render_report_collects_from_a_job_when_no_sources_given(self):
        job = _FakeJob()
        report = render_report(job)
        assert "# Run report — fake job" in report
        assert "- `abcdefgh` — Do the thing — **completed**" in report
        assert "- Terminal status: all_green" in report

    def test_interim_mode_supplies_its_own_timestamp(self):
        """render_report may reach for the clock; the pure renderer may not."""
        report = render_report(_FakeJob(), MODE_INTERIM)
        assert report.splitlines()[0].startswith("> **INTERIM SNAPSHOT")


class TestLoopProvenanceLine:
    """F045 — a run that came from a loop says so, in its own report.

    The report lives inside ``job_evidence_dir``, so this one line is what
    makes the loop reference visible in the evidence area as well.
    """

    def test_a_loop_job_renders_the_loop_line_right_after_the_mission(self):
        job = _FakeJob()
        job.metadata[loop_run.LOOP_REF_METADATA_KEY] = "nightly-tidy"
        lines = render_report(job).splitlines()
        at = [i for i, line in enumerate(lines) if line == "- Loop: nightly-tidy"]
        assert len(at) == 1, lines
        assert at[0] == lines.index("- Mission: Do the thing") + 1, lines

    def test_a_job_without_a_loop_renders_no_loop_line_anywhere(self):
        """The negative pin the three goldens depend on — whole text, not a slice."""
        job = _FakeJob()
        assert loop_run.LOOP_REF_METADATA_KEY not in job.metadata
        report = render_report(job)
        assert [ln for ln in report.splitlines() if ln.startswith("- Loop:")] == []

    def test_the_key_is_read_from_the_loop_run_constant_not_a_literal(self, monkeypatch):
        """Renaming the writer's constant must move the reader with it."""
        monkeypatch.setattr(loop_run, "LOOP_REF_METADATA_KEY", "renamed_loop_ref")
        stale = _FakeJob()
        stale.metadata["loop_ref"] = "stale-literal"
        stale_lines = render_report(stale).splitlines()
        assert [ln for ln in stale_lines if ln.startswith("- Loop:")] == []
        renamed = _FakeJob()
        renamed.metadata["renamed_loop_ref"] = "nightly-tidy"
        assert "- Loop: nightly-tidy" in render_report(renamed).splitlines()


class TestTheTaskLineTellsAMixedApplyStateApart:
    """F033, finding R-0738's THIRD surface: the run report's own task line.

    The viewer badge and the tasks card already tell a MIXED apply state from a
    complete one. This pins the report doing the same, with the two counts
    behind the word, and — just as loudly — pins that a task with NOTHING
    recorded still renders the line the three goldens above contain.
    """

    def test_a_partial_apply_reads_as_partially_applied_with_its_counts(self):
        """The MIXED case, built explicitly rather than observed off a fixture."""
        assert _one_task_line(TaskOutcome(
            "aaaaaaaa", "Apply the hunks", "completed",
            apply_state="partial", applied_changes=5, total_changes=8)) == (
            "- `aaaaaaaa` — Apply the hunks — **completed**"
            " — partially applied (5/8 changes)")

    def test_a_complete_apply_reads_as_applied_with_its_counts(self):
        assert _one_task_line(TaskOutcome(
            "aaaaaaaa", "Apply the hunks", "completed",
            apply_state="applied", applied_changes=8, total_changes=8)) == (
            "- `aaaaaaaa` — Apply the hunks — **completed** — applied (8/8 changes)")

    def test_a_reverted_task_reads_as_reverted_with_zero_applied(self):
        assert _one_task_line(TaskOutcome(
            "aaaaaaaa", "Apply the hunks", "completed",
            apply_state="reverted", applied_changes=0, total_changes=8)) == (
            "- `aaaaaaaa` — Apply the hunks — **completed** — reverted (0/8 changes)")

    def test_an_unapplied_task_reads_as_not_applied_with_zero_applied(self):
        assert _one_task_line(TaskOutcome(
            "aaaaaaaa", "Apply the hunks", "completed",
            apply_state="not_applied", applied_changes=0, total_changes=8)) == (
            "- `aaaaaaaa` — Apply the hunks — **completed** — not applied (0/8 changes)")

    def test_an_unrecorded_apply_state_renders_the_line_unchanged(self):
        """The property the three golden full-text reports depend on.

        Measured rather than restated: the line is compared against the SAME
        line rendered from an outcome built WITHOUT naming any of the three
        fields this round added.
        """
        without_the_new_fields = TaskOutcome(
            "aaaaaaaa", "Write the renderer", "completed",
            evidence_ref="tasks/aaaaaaaa/output.md")
        at_their_not_recorded_defaults = TaskOutcome(
            "aaaaaaaa", "Write the renderer", "completed",
            evidence_ref="tasks/aaaaaaaa/output.md",
            apply_state="", applied_changes=0, total_changes=0)
        assert (_one_task_line(at_their_not_recorded_defaults)
                == _one_task_line(without_the_new_fields))
        assert "changes)" not in _one_task_line(without_the_new_fields)

    def test_counts_without_a_state_still_render_no_clause(self):
        """Counts are never evidence of an apply on their own (P6)."""
        assert _one_task_line(TaskOutcome(
            "aaaaaaaa", "Write the renderer", "completed",
            apply_state="", applied_changes=5, total_changes=8)) == _one_task_line(
            TaskOutcome("aaaaaaaa", "Write the renderer", "completed"))

    def test_an_apply_state_the_table_does_not_know_renders_no_clause(self):
        """Fail quiet, exactly as an absent source does — never an invented phrase."""
        unknown = _one_task_line(TaskOutcome(
            "aaaaaaaa", "Apply the hunks", "completed",
            apply_state="half_applied", applied_changes=5, total_changes=8))
        assert unknown == _one_task_line(
            TaskOutcome("aaaaaaaa", "Apply the hunks", "completed"))
        assert "half_applied" not in unknown
        assert "changes)" not in unknown


class TestTheApplyStateIsAttachedByTheFullTaskId:
    """The attach in ``build_report_sources``, and the trap it must not fall into."""

    def test_two_tasks_sharing_eight_id_characters_keep_their_own_state(
            self, monkeypatch):
        """``TaskOutcome.task_id`` is ``str(t.id)[:8]`` — a TRUNCATION.

        The fold keys on the FULL id. An attach that looked the state up by the
        truncated value would give these two tasks each other's answer (or, with
        a full-id-keyed fold, no answer at all) and would still pass every other
        test in this file. This is the one that fails.
        """
        first = "abcdef01-1111-4111-8111-111111111111"
        second = "abcdef01-2222-4222-8222-222222222222"
        assert first[:8] == second[:8]
        assert first != second
        job = _FakeJob()
        job.tasks = [_FakeTask(first, "Apply the first hunks", "completed"),
                     _FakeTask(second, "Apply the second hunks", "completed")]
        chain = _FakeProofChain([
            _FakeProofChange(first, "applied"),
            _FakeProofChange(first, "applied"),
            _FakeProofChange(second, "applied"),
            _FakeProofChange(second, "not_applied"),
        ])
        monkeypatch.setattr(proof_chain, "build_proof_chain", lambda *a, **k: chain)

        lines = _section(
            render_report_from_sources(build_report_sources(job)), "Tasks"
        ).strip().splitlines()
        assert [line.split(" — ")[0] for line in lines] == ["- `abcdef01`"] * 2
        by_description = {line.split(" — ")[1]: line for line in lines}
        assert by_description["Apply the first hunks"].endswith(
            "**completed** — applied (2/2 changes)")
        assert by_description["Apply the second hunks"].endswith(
            "**completed** — partially applied (1/2 changes)")

    def test_the_attached_counts_are_the_folds_own_numbers(self, monkeypatch):
        """The counts survive the attach, and they are not recomputed here."""
        task_id = "cccccccc"  # eight characters: the truncation is the identity
        job = _FakeJob()
        job.tasks = [_FakeTask(task_id, "Apply the hunks", "completed")]
        chain = _FakeProofChain([
            _FakeProofChange(task_id, "applied"),
            _FakeProofChange(task_id, "applied"),
            _FakeProofChange(task_id, "applied"),
            _FakeProofChange(task_id, "reverted"),
            _FakeProofChange(task_id, "not_applied"),
        ])
        monkeypatch.setattr(proof_chain, "build_proof_chain", lambda *a, **k: chain)

        outcome = build_report_sources(job).tasks[0]
        folded = proof_chain.fold_task_apply_states(chain)[task_id]
        assert (outcome.apply_state, outcome.applied_changes, outcome.total_changes) == (
            folded.state, folded.applied, folded.total)
        assert (outcome.applied_changes, outcome.total_changes) == (3, 5)
        assert _one_task_line(outcome).endswith("partially applied (3/5 changes)")


class TestTheProofChainModuleDocumentsItsWholePublicApi:
    """R-0746 — the export list and the module are read AGAINST each other.

    A curated list that is only ever checked by being re-typed is the defect
    R-0746 already is: round 18 gave ``proof_chain.py`` a fifth public function
    and its ``Public API::`` block went on naming four. This walks the module's
    own AST, so the list cannot go stale again without a red test.

    It lives here, beside this round's other tests, because this is the round
    that gives the shared apply fold its second importer.
    """

    def test_every_public_module_level_function_is_named_in_the_public_api_block(self):
        tree = ast.parse(Path(proof_chain.__file__).read_text(encoding="utf-8"))
        public = [node.name for node in tree.body
                  if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                  and not node.name.startswith("_")]
        assert public, "the AST walk found no public function — the guard is vacuous"
        assert "fold_task_apply_states" in public, (
            "the shared apply fold is no longer a public module-level function of "
            f"proof_chain.py; the walk found {public}")
        block = _public_api_block(ast.get_docstring(tree) or "")
        assert block.strip(), "proof_chain.py's docstring carries no `Public API::` block"
        missing = [name for name in public
                   if not re.search(rf"^\s*{re.escape(name)}\(", block, re.M)]
        assert missing == [], (
            "public in proof_chain.py but absent from its own `Public API::` block: "
            f"{missing}")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


class _FakeProofChange:
    """The two attributes ``fold_task_apply_states`` reads off a ProofChange."""

    def __init__(self, task_id: str, apply_state: str):
        self.task_id = task_id
        self.apply_state = apply_state


class _FakeProofChain:
    def __init__(self, changes):
        self.changes = list(changes)


def _one_task_line(task: TaskOutcome) -> str:
    """The single rendered body line of a report whose only task is *task*."""
    body = _section(
        render_report_from_sources(ReportSources(tasks=(task,))), "Tasks"
    ).strip().splitlines()
    assert len(body) == 1, body
    return body[0]


def _public_api_block(docstring: str) -> str:
    """The indented block under ``Public API::`` in a module docstring."""
    lines = docstring.splitlines()
    start = next((i for i, line in enumerate(lines)
                  if line.strip() == "Public API::"), None)
    if start is None:
        return ""
    body: list[str] = []
    for line in lines[start + 1:]:
        if line.strip() and not line.startswith((" ", "\t")):
            break
        body.append(line)
    return "\n".join(body)


class _FakeTask:
    def __init__(self, task_id: str, description: str, status: str):
        self.id = task_id
        self.description = description
        self.status = status


class _FakeJob:
    """The duck-typed shape collect_report_sources reads off a core Job."""

    def __init__(self):
        self.id = "44444444-4444-4444-8444-444444444444"
        self.name = "fake job"
        self.project_id = "remedy"
        self.mission = "Do the thing"
        self.state = "completed"
        self.tasks = [_FakeTask("abcdefghijkl", "Do the thing", "completed")]
        self.metadata = {"cycle_terminal_status": "all_green"}


def _headings(report: str) -> list[str]:
    return [line for line in report.splitlines() if line.startswith("## ")]


def _section(report: str, heading: str) -> str:
    """The body under ``## <heading>``, up to the next ``## `` heading."""
    lines = report.splitlines()
    try:
        start = lines.index(f"## {heading}")
    except ValueError:  # pragma: no cover - a failed lookup is the assertion
        raise AssertionError(f"no section {heading!r} in report:\n{report}") from None
    body: list[str] = []
    for line in lines[start + 1:]:
        if line.startswith("## "):
            break
        body.append(line)
    return "\n".join(body)
