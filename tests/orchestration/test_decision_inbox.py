"""Contract tests for packages/orchestration/decision_inbox.py (F031 T001).

Every fixture is built through the REAL upstream state ``list_decisions``
reads — a patch intent on an artifact, a job with no target repo, a
``test_run_completed`` event, an escalation record — and never by constructing
a ``HumanDecision`` or monkeypatching ``list_decisions``.  A fixture that
bypasses the derivation would prove nothing about it.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from packages.core.models import Artifact, Job, Task
from packages.orchestration.dag_schedule import blocked_downstream
from packages.orchestration.decision_inbox import (
    DECISION_INBOX_VERSION,
    build_decision_inbox,
)
from packages.orchestration.decision_queue import export_decision_json, list_decisions
from packages.orchestration.escalation import (
    answer_task_decision,
    enqueue_task_decision,
)

#: DECISION F031 D3 — the eight types a branch of ``list_decisions`` actually
#: produces.  ``worker_approval`` and ``revert_missing`` have no producer at
#: all (source inventory Q3) and therefore get no fixture here.
PRODUCING_DECISION_TYPES = (
    "patch_approval",
    "stop_reason",
    "test_failure",
    "repo_dirty",
    "token_budget",
    "memory_review",
    "flight_plan_approval",
    "task_decision",
)

#: DECISION F031 D19 — the types the write door's ``decision.resolve`` can
#: actually answer.  ``_dispatch_decision_resolve`` reaches a record only
#: through ``escalation.find_task_decision``, which iterates escalation records
#: alone, so ``task_decision`` is the whole set and finding R-0693 measures it.
ANSWERABLE_DECISION_TYPES = ("task_decision",)

FIXED_NOW = datetime(2026, 8, 23, 12, 0, 0, tzinfo=timezone.utc)


@pytest.fixture(autouse=True)
def _isolated_data_root(tmp_path, monkeypatch):
    """Keep the memory gateway (and everything else on disk) out of the tests.

    ``list_decisions`` calls ``list_memory()`` in the global scope, so without
    this the repository's own memory cards would leak decisions into every
    fixture below.
    """
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))


def _make_job(**overrides) -> Job:
    defaults = dict(
        name="f031-inbox-job",
        user_prompt="Test the decision inbox",
        tasks=[],
        metadata={"target_repo": "/tmp/repo"},
    )
    defaults.update(overrides)
    return Job(**defaults)


def _linear_task_chain(count: int) -> list[Task]:
    """Tasks with no flight metadata — the legacy rule chains each to its predecessor."""
    return [Task(description=f"step {i}") for i in range(count)]


def _cards_by_type(inbox: dict) -> dict[str, dict]:
    return {card["type"]: card for card in inbox["decisions"]}


# ---------------------------------------------------------------------------
# (a) A fixture per PRODUCING type
# ---------------------------------------------------------------------------


def _fixture_patch_approval() -> tuple[Job, list[dict]]:
    artifact = Artifact(
        name="patch",
        content="",
        metadata={
            "patch_intent_explanations": [
                {"file": "README.md", "action": "modify", "risk": "low",
                 "reason": "docs", "summary": "touch the readme"},
            ],
        },
    )
    return _make_job(artifacts=[artifact]), []


def _fixture_stop_reason() -> tuple[Job, list[dict]]:
    # No target repo attached — derive_stop_reasons raises "no_target_repo".
    return _make_job(metadata={}), []


def _fixture_test_failure() -> tuple[Job, list[dict]]:
    return _make_job(), [{
        "event": "test_run_completed",
        "timestamp": "2026-08-23T11:00:00+00:00",
        "metadata": {"status": "failed", "command": "pytest -q",
                     "test_run_id": "abcdef1234"},
    }]


def _fixture_repo_dirty() -> tuple[Job, list[dict]]:
    return _make_job(), [{
        "event": "git_status_read",
        "timestamp": "2026-08-23T11:30:00+00:00",
        "metadata": {"dirty": True},
    }]


def _fixture_token_budget() -> tuple[Job, list[dict]]:
    return _make_job(metadata={"target_repo": "/tmp/repo",
                               "budget_stop_reason": "budget_exhausted"}), []


def _fixture_memory_review() -> tuple[Job, list[dict]]:
    from packages.memory.local_gateway import mark_stale, store_memory
    entry = store_memory("inbox_probe", "a card the inbox must surface")
    mark_stale(str(entry.id))
    return _make_job(), []


def _fixture_flight_plan_approval() -> tuple[Job, list[dict]]:
    return _make_job(flight_plan={"_approval": "pending"}), []


def _fixture_task_decision() -> tuple[Job, list[dict]]:
    job = _make_job(tasks=_linear_task_chain(3))
    enqueue_task_decision(
        job,
        task_id=job.tasks[0].id,
        question="Which database?",
        options=["postgres", "sqlite"],
        now=FIXED_NOW - timedelta(seconds=90),
    )
    return job, []


PRODUCING_FIXTURES = {
    "patch_approval": _fixture_patch_approval,
    "stop_reason": _fixture_stop_reason,
    "test_failure": _fixture_test_failure,
    "repo_dirty": _fixture_repo_dirty,
    "token_budget": _fixture_token_budget,
    "memory_review": _fixture_memory_review,
    "flight_plan_approval": _fixture_flight_plan_approval,
    "task_decision": _fixture_task_decision,
}


def test_every_producing_type_has_a_fixture():
    """The fixture set IS DECISION F031 D3's set — no type quietly untested."""
    assert tuple(sorted(PRODUCING_FIXTURES)) == tuple(sorted(PRODUCING_DECISION_TYPES))


@pytest.mark.parametrize("decision_type", PRODUCING_DECISION_TYPES)
def test_card_appears_for_each_producing_type(decision_type):
    job, events = PRODUCING_FIXTURES[decision_type]()
    inbox = build_decision_inbox(job, events, now=FIXED_NOW)

    assert inbox["version"] == DECISION_INBOX_VERSION
    assert inbox["job_id"] == str(job.id)

    cards = _cards_by_type(inbox)
    assert decision_type in cards, f"no card of type {decision_type}: {sorted(cards)}"
    card = cards[decision_type]
    assert "age_seconds" in card
    assert "blocked_count" in card
    assert isinstance(card["blocked_count"], int)
    assert "answerable_by_decision_resolve" in card
    assert isinstance(card["answerable_by_decision_resolve"], bool)


# ---------------------------------------------------------------------------
# (b) The blocked math, against the DAG module and never a literal
# ---------------------------------------------------------------------------


def test_blocked_count_equals_dag_blocked_downstream():
    job = _make_job(tasks=_linear_task_chain(4))
    first = job.tasks[0]
    enqueue_task_decision(job, task_id=first.id, question="Wait for me?",
                          now=FIXED_NOW)

    inbox = build_decision_inbox(job, [], now=FIXED_NOW)
    card = _cards_by_type(inbox)["task_decision"]

    expected = len(blocked_downstream(job.tasks, {first.id}))
    assert card["blocked_count"] == expected
    # Without this half the assertion above passes on a module that always
    # returns 0: two zeros compare equal.
    assert card["blocked_count"] > 0


# ---------------------------------------------------------------------------
# (c) Every other type reports 0
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "decision_type",
    [t for t in PRODUCING_DECISION_TYPES if t != "task_decision"],
)
def test_non_task_decision_types_report_zero_blocked(decision_type):
    job, events = PRODUCING_FIXTURES[decision_type]()
    inbox = build_decision_inbox(job, events, now=FIXED_NOW)
    card = _cards_by_type(inbox)[decision_type]
    assert card["blocked_count"] == 0


# ---------------------------------------------------------------------------
# (d) Age
# ---------------------------------------------------------------------------


def test_age_seconds_is_the_exact_integer_for_a_known_stamp():
    job = _make_job(tasks=_linear_task_chain(1))
    enqueue_task_decision(job, task_id=job.tasks[0].id, question="How old?",
                          now=FIXED_NOW - timedelta(seconds=125))
    card = _cards_by_type(build_decision_inbox(job, [], now=FIXED_NOW))["task_decision"]
    assert card["age_seconds"] == 125


def test_age_seconds_is_none_for_an_empty_stamp():
    # The flight-plan branch writes created_at="" — the empty case, upstream.
    job, events = _fixture_flight_plan_approval()
    card = _cards_by_type(
        build_decision_inbox(job, events, now=FIXED_NOW))["flight_plan_approval"]
    assert card["age_seconds"] is None


def test_age_seconds_is_none_for_a_malformed_stamp():
    job = _make_job(tasks=_linear_task_chain(1))
    record = enqueue_task_decision(job, task_id=job.tasks[0].id,
                                   question="When?", now=FIXED_NOW)
    record["created_at"] = "not-a-timestamp"
    card = _cards_by_type(build_decision_inbox(job, [], now=FIXED_NOW))["task_decision"]
    assert card["age_seconds"] is None


def test_age_seconds_clamps_a_future_stamp_to_zero():
    job = _make_job(tasks=_linear_task_chain(1))
    enqueue_task_decision(job, task_id=job.tasks[0].id, question="From the future?",
                          now=FIXED_NOW + timedelta(hours=1))
    card = _cards_by_type(build_decision_inbox(job, [], now=FIXED_NOW))["task_decision"]
    assert card["age_seconds"] == 0


# ---------------------------------------------------------------------------
# (e) Honesty — unreadable entries still render
# ---------------------------------------------------------------------------


def test_task_id_that_is_not_a_uuid_reports_zero_and_raises_nothing():
    job = _make_job(tasks=_linear_task_chain(3))
    record = enqueue_task_decision(job, task_id=job.tasks[0].id,
                                   question="Who am I?", now=FIXED_NOW)
    record["task_id"] = "definitely-not-a-uuid"
    card = _cards_by_type(build_decision_inbox(job, [], now=FIXED_NOW))["task_decision"]
    assert card["blocked_count"] == 0


def test_job_without_tasks_reports_zero_and_raises_nothing():
    job = _make_job(tasks=[])
    enqueue_task_decision(job, task_id="6f1f2b8e-1f0e-4a1b-9c3d-000000000001",
                          question="Nothing behind me?", now=FIXED_NOW)
    card = _cards_by_type(build_decision_inbox(job, [], now=FIXED_NOW))["task_decision"]
    assert card["blocked_count"] == 0


# ---------------------------------------------------------------------------
# (f) Shape — exactly the queue's keys plus the three additive ones
# ---------------------------------------------------------------------------


def test_card_keys_are_the_export_keys_plus_exactly_three():
    job, events = _fixture_task_decision()
    decision = list_decisions(job, events)[0]
    expected = set(export_decision_json(decision)) | {
        "age_seconds",
        "blocked_count",
        "answerable_by_decision_resolve",
    }

    inbox = build_decision_inbox(job, events, now=FIXED_NOW)
    for card in inbox["decisions"]:
        assert set(card) == expected, f"unexpected card keys: {sorted(set(card) ^ expected)}"


def test_inbox_top_level_keys_match_the_cli_json_spelling():
    job, events = _fixture_task_decision()
    inbox = build_decision_inbox(job, events, now=FIXED_NOW)
    assert set(inbox) == {"version", "job_id", "decisions"}


# ---------------------------------------------------------------------------
# (g) Answerability — the write door's own predicate (DECISION F031 D19)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("decision_type", PRODUCING_DECISION_TYPES)
def test_answerable_key_matches_what_the_write_door_accepts(decision_type):
    """Every producing type's own card reports whether the door can answer it."""
    job, events = PRODUCING_FIXTURES[decision_type]()
    inbox = build_decision_inbox(job, events, now=FIXED_NOW)
    card = _cards_by_type(inbox)[decision_type]
    assert card["answerable_by_decision_resolve"] == (
        decision_type in ANSWERABLE_DECISION_TYPES
    ), f"{decision_type}: door answerability disagrees with ANSWERABLE_DECISION_TYPES"


def test_answerable_key_goes_false_once_the_decision_has_been_answered():
    """The door refuses a record that is not OPEN, so the key must too (R-0695).

    A type check cannot tell these two states apart: both cards read
    ``task_decision``.  The transition is pinned in ONE test so a helper that
    answers only the existence half is caught.
    """
    job, events = _fixture_task_decision()
    before = _cards_by_type(build_decision_inbox(job, events, now=FIXED_NOW))
    open_card = before["task_decision"]
    assert open_card["status"] == "open"
    assert open_card["answerable_by_decision_resolve"] is True

    answered = answer_task_decision(job, open_card["id"], answer="postgres",
                                    now=FIXED_NOW)
    assert answered is not None

    # The door's real refusal, asserted rather than assumed: the second answer
    # is what `_dispatch_decision_resolve` turns into 409 `rejected_state`.
    assert answer_task_decision(job, open_card["id"], answer="sqlite",
                                now=FIXED_NOW) is None

    card = _cards_by_type(build_decision_inbox(job, events, now=FIXED_NOW))["task_decision"]
    assert card["status"] == "resolved"
    assert card["answerable_by_decision_resolve"] is False
