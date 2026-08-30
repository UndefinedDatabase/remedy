"""Contract tests for packages/orchestration/job_digest.py (F040 T001).

The FOUR state shapes the feature file names — green, blocked-with-decisions,
budget-stopped and mid-run — each get a fixture built through the REAL job model
and the REAL upstream state the digest composes over: tasks with real statuses,
decisions enqueued through ``escalation.enqueue_task_decision``, actuals
persisted as a real ``JobPlan``.  A fixture that monkeypatched the seams under
composition would prove nothing about the composition.

THE ONE-SOURCE PROPERTY is the reason this module exists and it is asserted
against ``recommended_next_action``'s own return value for the same job, never
against a hard-coded string.  A golden ALONE would keep passing while the digest
and the report drifted apart, which is precisely the failure F040 is built to
prevent — so the golden section at the bottom stands BESIDE that assertion and
never in place of it (DECISION F040 D6, finding R-0754): the goldens pin the
rendered envelope, the one-source test pins its agreement with the report, and a
label change reddens both.
"""

from __future__ import annotations

import dataclasses
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from packages.core.models import Job, RunState, Task
from packages.orchestration import budget_guard, decision_inbox
from packages.orchestration.budget_guard import (
    BudgetCounters,
    counters_from_persisted,
    decode_persisted_budget_actuals,
)
from packages.orchestration.decision_inbox import (
    build_decision_inbox,
    decision_urgency,
)
from packages.orchestration.escalation import enqueue_task_decision
from packages.orchestration.job_digest import (
    COST_BASIS_ABSENT,
    COST_BASIS_ACTUAL,
    COST_BASIS_LOWER_BOUND,
    COST_NOT_MEASURED,
    JOB_DIGEST_VERSION,
    OPEN_CARD_STATUS,
    build_job_digest,
)
from packages.orchestration.pingpong_job import JobPlan, save_job_plan
from packages.orchestration.run_report import (
    build_report_sources,
    recommended_next_action,
)

pytestmark = pytest.mark.unit

FIXED_NOW = datetime(2026, 8, 29, 12, 0, 0, tzinfo=timezone.utc)

#: The envelope's contract.  Read as a SET so a ninth key added without a
#: version bump reddens here rather than shipping unnoticed to a client that
#: never learns to read it.
DIGEST_KEYS = frozenset({
    "version", "job_id", "state", "headline", "cost", "ownership",
    "decisions", "primary_action",
})

GREEN = "green"
BLOCKED = "blocked_with_decisions"
BUDGET_STOPPED = "budget_stopped"
MID_RUN = "mid_run"
SHAPES = (GREEN, BLOCKED, BUDGET_STOPPED, MID_RUN)

#: The persisted actuals every cost fixture starts from — a real record that
#: ``decode_persisted_budget_actuals`` accepts, so the decode is never stubbed.
ACTUALS_STARTED_AT = "2026-08-29T11:00:00+00:00"
PERSISTED_ACTUALS = {
    "schema_version": "1.0.0",
    "provider_call_count": 4,
    "actual_call_count": 3,
    "unmeasured_call_count": 1,
    "total_tokens": 4200,
    "started_at": ACTUALS_STARTED_AT,
    "actual_sources": ["pingpong_actuals"],
}


@pytest.fixture(autouse=True)
def _isolated_data_root(tmp_path, monkeypatch):
    """Keep every on-disk source out of the fixtures.

    ``list_decisions`` calls ``list_memory()`` in the global scope and the cost
    path reads persisted job plans, so without this the repository's own state
    would leak into the digests below.
    """
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))


@pytest.fixture(autouse=True)
def _frozen_inbox_clock(monkeypatch):
    """Pin the inbox's clock so an age — and therefore an urgency — is exact.

    ``build_job_digest`` deliberately takes no ``now`` argument: a digest is
    about the moment it is asked for.  That leaves the wall clock as the only
    source of a card's age, and two readings taken either side of a second
    boundary would differ by one, so the peak-urgency assertions below would be
    flaky rather than wrong.  Freezing ``decision_inbox``'s own clock removes
    the boundary without touching anything the digest composes.
    """

    class _FrozenDatetime(datetime):
        @classmethod
        def now(cls, tz=None):  # noqa: D102 - the frozen reading
            return FIXED_NOW

    monkeypatch.setattr(decision_inbox, "datetime", _FrozenDatetime)


def _make_job(**overrides) -> Job:
    defaults = dict(
        name="f040-digest-job",
        user_prompt="Test the completion digest",
        tasks=[],
        metadata={"target_repo": "/tmp/repo"},
    )
    defaults.update(overrides)
    return Job(**defaults)


# ---------------------------------------------------------------------------
# The four state shapes
# ---------------------------------------------------------------------------


def _shape_green() -> tuple[Job, list[dict]]:
    """Every task completed, nothing open, a terminal status of all_green."""
    return _make_job(
        state=RunState.COMPLETED,
        tasks=[Task(description="write the composition", status=RunState.COMPLETED),
               Task(description="write its tests", status=RunState.COMPLETED)],
        metadata={"target_repo": "/tmp/repo", "cycle_terminal_status": "all_green"},
    ), []


def _shape_blocked_with_decisions() -> tuple[Job, list[dict]]:
    """Two open decisions with DIFFERENT ages and DIFFERENT blocked subtrees.

    The chain is linear, so the first task blocks three downstream and the third
    blocks one; the ages are ten minutes and one minute.  Both halves differ on
    purpose: a peak taken by age alone and a peak taken by blocked size alone
    would pick the same card if only one of the two varied.
    """
    job = _make_job(
        state=RunState.PAUSED,
        tasks=[Task(description=f"step {i}") for i in range(4)],
        metadata={"target_repo": "/tmp/repo", "cycle_terminal_status": "blocked"},
    )
    enqueue_task_decision(job, task_id=job.tasks[0].id,
                          question="Which database?",
                          options=["postgres", "sqlite"],
                          now=FIXED_NOW - timedelta(seconds=600))
    enqueue_task_decision(job, task_id=job.tasks[2].id,
                          question="Which index?",
                          now=FIXED_NOW - timedelta(seconds=60))
    return job, []


def _shape_budget_stopped() -> tuple[Job, list[dict]]:
    """A terminal status in the budget family, with nothing left to answer."""
    return _make_job(
        state=RunState.PAUSED,
        tasks=[Task(description="refactor the verifier", status=RunState.FAILED)],
        metadata={"target_repo": "/tmp/repo",
                  "cycle_terminal_status": "budget_exhausted",
                  "cycle_stop_reason": "budget_exhausted:tokens"},
    ), []


def _shape_mid_run() -> tuple[Job, list[dict]]:
    """Still going: one task done, one waiting, and no terminal status at all."""
    return _make_job(
        state=RunState.RUNNING,
        tasks=[Task(description="plan the work", status=RunState.COMPLETED),
               Task(description="do the work", status=RunState.RUNNING)],
        metadata={"target_repo": "/tmp/repo"},
    ), []


SHAPE_FIXTURES = {
    GREEN: _shape_green,
    BLOCKED: _shape_blocked_with_decisions,
    BUDGET_STOPPED: _shape_budget_stopped,
    MID_RUN: _shape_mid_run,
}


def test_every_named_shape_has_a_fixture():
    """The fixture set IS the feature file's set — no shape quietly untested."""
    assert tuple(sorted(SHAPE_FIXTURES)) == tuple(sorted(SHAPES))


# ---------------------------------------------------------------------------
# (a) The envelope
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("shape", SHAPES)
def test_the_envelope_carries_exactly_the_eight_specified_keys(shape):
    job, events = SHAPE_FIXTURES[shape]()
    digest = build_job_digest(job, events)
    assert set(digest) == set(DIGEST_KEYS), sorted(set(digest) ^ set(DIGEST_KEYS))


@pytest.mark.parametrize("shape", SHAPES)
def test_the_envelope_states_its_own_version(shape):
    job, events = SHAPE_FIXTURES[shape]()
    assert build_job_digest(job, events)["version"] == JOB_DIGEST_VERSION


@pytest.mark.parametrize("shape", SHAPES)
def test_the_envelope_names_the_job_and_its_state(shape):
    job, events = SHAPE_FIXTURES[shape]()
    digest = build_job_digest(job, events)
    sources = build_report_sources(job)
    assert digest["job_id"] == str(job.id)
    assert digest["state"] == sources.state
    # The headline is the digest's own prose, but it must NAME the state it
    # reports rather than paraphrasing it into a second vocabulary.
    assert sources.state in digest["headline"]
    assert digest["headline"].endswith(".")


def test_the_headline_names_a_terminal_status_when_the_job_has_one():
    job, events = SHAPE_FIXTURES[BUDGET_STOPPED]()
    assert "budget_exhausted" in build_job_digest(job, events)["headline"]


def test_the_headline_of_a_running_job_claims_no_terminal_status():
    job, events = SHAPE_FIXTURES[MID_RUN]()
    headline = build_job_digest(job, events)["headline"]
    assert "terminal status" not in headline
    assert headline == "The run is running."


# ---------------------------------------------------------------------------
# (b) THE ONE-SOURCE PROPERTY — the whole point of the feature
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("shape", SHAPES)
def test_the_primary_action_is_the_reports_own_recommendation(shape):
    """The CTA and the report's recommendation cannot disagree, for any shape.

    Asserted against the FUNCTION'S RETURN VALUE for the same job — never
    against a literal — so a digest that re-derived the answer and happened to
    agree today would still fail the day the rule table moved.
    """
    job, events = SHAPE_FIXTURES[shape]()
    digest = build_job_digest(job, events)
    expected = recommended_next_action(build_report_sources(job))

    assert digest["primary_action"]["label"] == expected.action
    assert digest["primary_action"]["rule_id"] == expected.rule_id


def test_the_four_shapes_reach_four_different_rules():
    """Without this, the one-source test above would pass on a constant.

    Four shapes that all recommended the same thing would let a digest that
    returned one hard-coded action satisfy every assertion in this file.
    """
    rules = {shape: build_job_digest(*SHAPE_FIXTURES[shape]())["primary_action"]["rule_id"]
             for shape in SHAPES}
    assert rules == {
        GREEN: "all-green",
        BLOCKED: "open-decision",
        BUDGET_STOPPED: "blocked-failed",
        MID_RUN: "indeterminate",
    }


def test_the_blocked_shape_reaches_the_open_decision_rule():
    """The branch ``collect_report_sources`` alone could never reach.

    Rule 1 of the table branches on ``open_decision_count``, which only
    ``build_report_sources`` fills — a digest built on the bare collector would
    recommend anything but answering the question the run is waiting on.
    """
    job, events = SHAPE_FIXTURES[BLOCKED]()
    digest = build_job_digest(job, events)
    assert digest["primary_action"]["rule_id"] == "open-decision"
    assert digest["primary_action"]["label"].startswith("Answer the open decision")


# ---------------------------------------------------------------------------
# (c) Decisions — the count and the urgency peak
# ---------------------------------------------------------------------------


def test_the_open_count_is_the_reports_own_count():
    job, events = SHAPE_FIXTURES[BLOCKED]()
    digest = build_job_digest(job, events)
    assert digest["decisions"]["open_count"] == build_report_sources(job).open_decision_count
    # Two zeros compare equal: without this half the assertion passes on a
    # digest that always reports nothing open.
    assert digest["decisions"]["open_count"] == 2


def test_the_peak_urgency_is_the_maximum_over_the_open_cards():
    job, events = SHAPE_FIXTURES[BLOCKED]()
    digest = build_job_digest(job, events)

    cards = [c for c in build_decision_inbox(job, events)["decisions"]
             if c["status"] == OPEN_CARD_STATUS]
    assert len(cards) == 2, cards
    by_hand = max(decision_urgency(c) for c in cards)

    assert digest["decisions"]["peak_urgency"] == by_hand
    # And the peak is the OLDER card with the LARGER blocked subtree, computed
    # from the formula's own inputs rather than from a remembered number.
    peak = max(cards, key=decision_urgency)
    assert peak["age_seconds"] == 600
    assert peak["blocked_count"] == 3
    assert digest["decisions"]["peak_urgency"] == (3 + 1) * 600


def test_a_green_run_has_nothing_open_and_no_urgency():
    job, events = SHAPE_FIXTURES[GREEN]()
    digest = build_job_digest(job, events)
    assert digest["decisions"]["open_count"] == 0
    assert digest["decisions"]["peak_urgency"] == 0


# ---------------------------------------------------------------------------
# (d) Ownership — an honest absence, per DECISION F040 D3
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("shape", SHAPES)
def test_ownership_is_empty_by_decision_f040_d3(shape):
    """EMPTY ON PURPOSE, not an oversight and not a bug to "fix".

    DECISION F040 D3: the ownership sentences come from F035, which is unbuilt
    and ships no importable source, so there is nothing to compose over.  The
    key is in the envelope from version 1 so F035 fills it without a version
    bump, and the card omits the section rather than inventing a sentence.
    """
    job, events = SHAPE_FIXTURES[shape]()
    assert build_job_digest(job, events)["ownership"] == []


# ---------------------------------------------------------------------------
# (e) Cost — the EXACTNESS basis of DECISION F040 D4
# ---------------------------------------------------------------------------


def _persist_actuals(job: Job) -> None:
    """Give *job* a real persisted plan carrying the actuals record above."""
    save_job_plan(JobPlan(
        job_id=str(job.id),
        first_running_at=ACTUALS_STARTED_AT,
        budget_actuals=dict(PERSISTED_ACTUALS),
    ))


def _stand_in_for_the_price_producer(monkeypatch, *, cost, unpriced, priced):
    """Add the F104 money fields the persisted route does not carry yet.

    MEASURED, and pinned by the test below: ``counters_from_persisted`` sets
    none of ``measured_cost_usd``, ``unpriced_call_count`` or
    ``priced_call_count``, so counters built from a persisted record always
    report an unpriced run and the digest's ``lower_bound`` and ``actual`` bases
    are unreachable through that route TODAY.  Everything here stays real — the
    plan is loaded, the record decoded, the counters built by the shipped
    function — and only the three money fields are supplied, standing in for the
    producer that will set them.  Delete this helper the day the route carries
    them and assert the bases directly.
    """
    real = budget_guard.counters_from_persisted

    def _with_money(validated, **kwargs):
        return dataclasses.replace(
            real(validated, **kwargs),
            measured_cost_usd=cost,
            unpriced_call_count=unpriced,
            priced_call_count=priced,
        )

    monkeypatch.setattr(budget_guard, "counters_from_persisted", _with_money)


def test_the_persisted_cost_route_carries_no_money_today():
    """The measurement the two monkeypatched tests below rest on.

    When this reddens the route has learned to price a run: drop
    ``_stand_in_for_the_price_producer`` and let the fixtures speak for
    themselves.
    """
    counters = counters_from_persisted(
        decode_persisted_budget_actuals(dict(PERSISTED_ACTUALS),
                                        first_running_at=ACTUALS_STARTED_AT))
    assert counters.measured_cost_usd is None
    assert counters.unpriced_call_count == 0
    assert counters.priced_call_count == 0


def test_the_absent_spelling_is_the_counters_own():
    """The module's fallback constant cannot drift from the function it mirrors."""
    assert COST_NOT_MEASURED == BudgetCounters().cost_description()


def test_cost_basis_is_absent_when_no_actuals_are_persisted():
    job, events = SHAPE_FIXTURES[GREEN]()
    cost = build_job_digest(job, events)["cost"]
    assert cost["basis"] == COST_BASIS_ABSENT
    assert cost["value"] == BudgetCounters().cost_description()
    assert cost["value"] == "not-measured"


def test_cost_basis_is_lower_bound_when_calls_are_unpriced(monkeypatch):
    job, events = SHAPE_FIXTURES[GREEN]()
    _persist_actuals(job)
    _stand_in_for_the_price_producer(monkeypatch, cost=0.5, unpriced=2, priced=1)

    cost = build_job_digest(job, events)["cost"]
    expected = BudgetCounters(measured_cost_usd=0.5, unpriced_call_count=2,
                              priced_call_count=1).cost_description()
    assert cost["basis"] == COST_BASIS_LOWER_BOUND
    # The value is the string cost_description() produced, not a figure this
    # module re-rendered: the ">= " floor notation survives verbatim.
    assert cost["value"] == expected
    assert cost["value"].startswith(">= $")


def test_cost_basis_is_actual_when_every_call_is_priced(monkeypatch):
    job, events = SHAPE_FIXTURES[GREEN]()
    _persist_actuals(job)
    _stand_in_for_the_price_producer(monkeypatch, cost=1.25, unpriced=0, priced=3)

    cost = build_job_digest(job, events)["cost"]
    expected = BudgetCounters(measured_cost_usd=1.25, unpriced_call_count=0,
                              priced_call_count=3).cost_description()
    assert cost["basis"] == COST_BASIS_ACTUAL
    assert cost["value"] == expected
    assert cost["value"] == "$1.2500"


@pytest.mark.parametrize("shape", SHAPES)
def test_the_basis_is_never_a_provenance_value(shape):
    """DECISION F040 D4: basis is EXACTNESS, never ``actual_sources``.

    The two fields were both called "basis" until D4 separated them, and the
    client's ``~`` treatment reads this one — a provenance value arriving here
    would render as an unknown and silently drop the estimate mark.
    """
    job, events = SHAPE_FIXTURES[shape]()
    basis = build_job_digest(job, events)["cost"]["basis"]
    assert basis in {COST_BASIS_ACTUAL, COST_BASIS_LOWER_BOUND, COST_BASIS_ABSENT}
    assert basis not in set(budget_guard.VALID_ACTUAL_SOURCES)


# ---------------------------------------------------------------------------
# (f) Totality — no input makes the digest raise
# ---------------------------------------------------------------------------


class _NothingJob:
    """A job-shaped object with no plan, no actuals, no tasks and no decisions."""


def test_a_job_with_nothing_on_it_still_yields_a_full_envelope():
    digest = build_job_digest(_NothingJob())
    assert set(digest) == set(DIGEST_KEYS)
    assert digest["version"] == JOB_DIGEST_VERSION
    assert digest["ownership"] == []
    assert digest["decisions"] == {"open_count": 0, "peak_urgency": 0}
    assert digest["cost"] == {"value": COST_NOT_MEASURED, "basis": COST_BASIS_ABSENT}
    # Absent renders as the report's ONE spelling for a source nobody wrote —
    # never a zero, never a plausible word.
    assert digest["state"] == "not recorded"
    assert digest["headline"] == "The run is not recorded."


def test_an_empty_job_still_yields_a_full_envelope():
    digest = build_job_digest(_make_job(metadata={}))
    assert set(digest) == set(DIGEST_KEYS)
    assert isinstance(digest["decisions"]["open_count"], int)
    assert isinstance(digest["decisions"]["peak_urgency"], int)
    assert isinstance(digest["primary_action"]["label"], str)
    assert isinstance(digest["primary_action"]["rule_id"], str)


def test_events_default_to_none_and_are_passed_through():
    """A caller that already loaded the events does not make the inbox reload them."""
    job, _ = SHAPE_FIXTURES[BLOCKED]()
    assert build_job_digest(job) == build_job_digest(job, [])
    assert build_job_digest(job, None) == build_job_digest(job, [])


# ---------------------------------------------------------------------------
# (g) The stored envelope goldens — T001's "Fixture goldens exact" clause
# ---------------------------------------------------------------------------
#
# DECISION F040 D6 (finding R-0754): the acceptance clause is met by ENVELOPE
# goldens — one stored JSON per state shape, compared WHOLE against the envelope
# the SAME fixture above builds.  They live in this module because the
# determinism the comparison rests on comes from its two autouse fixtures, and a
# golden that depended on a fixture it did not inherit would be a flake waiting
# for a slow machine.
#
# GENERATED ONCE AND THEN FROZEN.  Nothing in this section writes into
# GOLDEN_DIR: no write mode, no ``write_text``, no ``json.dump``, no regenerate
# flag and no environment switch, because a golden a test re-blesses on mismatch
# checks nothing — the rule ``test_cost_report.py`` already states for its own
# pair.  Re-generating one is deliberately a manual act.


GOLDEN_DIR = Path(__file__).parent / "fixtures" / "job_digest" / "golden"

#: The three IDENTITIES ``_normalize`` replaces, and the placeholders they
#: become.  An identity names WHICH job or WHICH decision; it never says
#: anything the digest is asserting.  NOTHING MAY BE ADDED TO THIS LIST — a
#: normalized headline, CTA word, rule id, count or urgency would make every
#: golden below vacuous, which is the exact failure DECISION F040 D6 exists to
#: prevent, and ``test_the_normalization_leaves_the_ctas_own_words`` is the
#: guard that reddens when someone tries.
JOB_ID_PLACEHOLDER = "<job-id>"
JOB_PREFIX_PLACEHOLDER = "<job-prefix>"
DECISION_ID_PLACEHOLDER = "td:<decision-id>"

#: ``escalation.enqueue_task_decision`` mints ``td:`` followed by a hex digest,
#: and the open-decision CTA embeds one verbatim inside its answer command.
DECISION_ID_PATTERN = re.compile(r"td:[0-9a-f]+")


def _normalize(envelope, job):
    """*envelope* with its three per-build identities replaced, recursively.

    RECURSIVELY, and inside strings, because the interesting text is exactly
    where the identities hide: the blocked shape's CTA label embeds both the
    job's first-eight prefix and a ``td:`` decision id in the answer command it
    quotes.  A substitution that only reached top-level values would leave the
    goldens flaky precisely at the field the acceptance criterion is about.

    The full UUID is replaced BEFORE its prefix, so the prefix substitution
    cannot eat the first eight characters of the id and leave a tail behind.
    """
    job_id = str(getattr(job, "id", "") or "")
    prefix = job_id[:8]

    def _replace(value):
        if isinstance(value, str):
            text = value.replace(job_id, JOB_ID_PLACEHOLDER) if job_id else value
            if prefix:
                text = text.replace(prefix, JOB_PREFIX_PLACEHOLDER)
            return DECISION_ID_PATTERN.sub(DECISION_ID_PLACEHOLDER, text)
        if isinstance(value, dict):
            return {key: _replace(item) for key, item in value.items()}
        if isinstance(value, list):
            return [_replace(item) for item in value]
        return value

    return _replace(envelope)


def _read_golden(shape):
    """The stored envelope for *shape*.  READ ONLY, by construction."""
    return json.loads((GOLDEN_DIR / f"{shape}.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("shape", SHAPES)
def test_the_normalized_envelope_equals_its_stored_golden(shape):
    """A golden re-blessed on every change checks nothing, so this one never is."""
    job, events = SHAPE_FIXTURES[shape]()
    assert _normalize(build_job_digest(job, events), job) == _read_golden(shape)


def test_the_golden_directory_holds_exactly_one_file_per_shape():
    """A shape added later without a golden reddens HERE, not silently nowhere."""
    names = sorted(path.name for path in GOLDEN_DIR.iterdir())
    assert len(names) == len(SHAPES)
    assert names == sorted(f"{shape}.json" for shape in SHAPES)


def test_the_normalization_leaves_the_ctas_own_words():
    """The NARROWNESS guard: widen ``_normalize`` past the identities and this dies.

    The blocked shape's label is the only published copy that carries an
    identity, so a substitution that swallowed the CTA's wording along with the
    ids would still satisfy the comparison above — both sides would move
    together.  This one reads the WORDS, and asserts the placeholder is present
    so it cannot pass on a label that was never normalized at all.
    """
    job, events = SHAPE_FIXTURES[BLOCKED]()
    label = _normalize(build_job_digest(job, events), job)["primary_action"]["label"]
    assert "Answer the open decision" in label
    assert "remedy decision resolve" in label
    assert DECISION_ID_PLACEHOLDER in label
