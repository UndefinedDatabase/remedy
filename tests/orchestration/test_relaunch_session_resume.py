"""R-1055 — the relaunch of an interrupted task resumes its parked provider session.

A park returns the interrupted task to `pending`, so its relaunch starts a new run.
Before the repair nothing on disk named the session the parked run had used, and the
new run's first calls could only start fresh, so T5_F025.md's "the resumed run provably
reuses its provider sessions where supported" was not met. Now every round's builder
and reviewer blocks in the run's `result.json` carry the session the call reported and
whether it resumed one, and `run_job` hands the parked run's sessions to the relaunch's
first calls. The load-bearing test is
:meth:`TestAParkedTaskResumesOnRelaunch.test_the_relaunch_resumes_the_parked_builder_session`,
which parks a real job mid-build and relaunches it through the real `run_job`.
"""
from __future__ import annotations

import pytest

from packages.orchestration import pause_control as pc
from packages.orchestration.pingpong_job import (
    JOB_COMPLETED,
    JOB_PAUSED,
    parse_job_file,
    run_job,
)
from packages.orchestration.pingpong_loop import (
    export_pingpong_json,
    load_run,
    parked_session_refs,
    run_pingpong,
)
from packages.orchestration.pingpong_provider import FakeProvider
from tests.orchestration.test_job_stop_integration import (  # noqa: F401
    _ONE_TASK_JOB,
    demo_repo,
    isolate_data_root,
)
from tests.orchestration.test_pause_resume import PauseTriggerProvider


def _resuming(session_id: str, **kwargs) -> FakeProvider:
    return FakeProvider(pass_on_round=1, fail_on_round=99, supports_resume=True,
                        fake_session_id=session_id, **kwargs)


class TestParkedSessionRefs:
    """The reader of a persisted run record, by role, last round winning."""

    def test_the_last_round_that_reported_a_session_wins(self):
        record = {"rounds": [
            {"builder": {"session_id": "b-1"}, "reviewer": {"session_id": "r-1"}},
            {"builder": {"session_id": "b-2"}},
        ]}
        assert parked_session_refs(record) == {"builder": "b-2", "reviewer": "r-1"}

    @pytest.mark.parametrize("record", [
        None,
        {},
        {"rounds": []},
        {"rounds": [{"builder": {"summary": "a record written before R-1055"}}]},
        {"rounds": [{"builder": {"session_id": ""}, "reviewer": {"session_id": ""}}]},
    ])
    def test_a_record_that_names_no_session_resumes_nothing(self, record):
        assert parked_session_refs(record) == {}


class TestTheRunRecordCarriesEachCallsSession:

    def test_each_round_block_names_its_session_and_whether_it_resumed(
            self, isolate_data_root, demo_repo):
        provider = _resuming("sess-1")
        result = run_pingpong("Fix README", str(demo_repo),
                              builder_provider=provider, reviewer_provider=provider)
        exported = export_pingpong_json(result)
        builder = exported["rounds"][0]["builder"]
        reviewer = exported["rounds"][0]["reviewer"]
        for block in (builder, reviewer):
            assert block["session_id"] == "sess-1"
            assert block["resume_used"] is False
            assert block["resume_session_ref"] == ""
            assert block["resume_fallback"] is False
        assert exported["resumed_from_run_id"] == ""
        assert parked_session_refs(load_run(result.run_id)) == {
            "builder": "sess-1", "reviewer": "sess-1"}


class TestTheFirstCallsResumeTheOfferedSessions:

    def test_both_roles_resume_on_round_one_when_supported(self, isolate_data_root, demo_repo):
        provider = _resuming("sess-new")
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            resume_sessions={"builder": "sess-parked-b", "reviewer": "sess-parked-r"},
            resumed_from_run_id="parked-run",
        )
        first = result.rounds[0]
        assert first.builder_output.resume_used is True
        assert first.builder_output.resume_session_ref == "sess-parked-b"
        assert first.reviewer_output.resume_used is True
        assert first.reviewer_output.resume_session_ref == "sess-parked-r"
        exported = export_pingpong_json(result)
        assert exported["resumed_from_run_id"] == "parked-run"
        assert exported["rounds"][0]["builder"]["resume_used"] is True
        assert exported["rounds"][0]["reviewer"]["resume_session_ref"] == "sess-parked-r"

    def test_a_provider_without_resume_is_offered_nothing(self, isolate_data_root, demo_repo):
        provider = FakeProvider(pass_on_round=1, fail_on_round=99, fake_session_id="sess-new")
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            resume_sessions={"builder": "sess-parked-b", "reviewer": "sess-parked-r"},
            resumed_from_run_id="parked-run",
        )
        assert result.rounds[0].builder_output.resume_used is False
        assert result.rounds[0].reviewer_output.resume_used is False

    def test_a_lost_parked_session_falls_back_once_and_the_round_completes(
            self, isolate_data_root, demo_repo):
        provider = _resuming("sess-new", resume_fails=True)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            resume_sessions={"builder": "sess-parked-b"},
            resumed_from_run_id="parked-run",
        )
        assert result.rounds[0].builder_output.resume_fallback is True
        assert result.rounds[0].builder_output.error == ""
        assert result.final_status == "staged_review_passed"


class TestAParkedTaskResumesOnRelaunch:

    def test_the_relaunch_resumes_the_parked_builder_session(
            self, isolate_data_root, demo_repo):
        job = parse_job_file(_ONE_TASK_JOB, str(demo_repo))
        builder = PauseTriggerProvider(
            on_build=1,
            trigger=lambda: pc.request_pause(job.job_id, "mid-build pause", "cli"),
            pass_on_round=1, fail_on_round=99,
            supports_resume=True, fake_session_id="sess-parked")
        parked = run_job(job.job_id, builder_provider=builder,
                         reviewer_provider=_resuming("sess-parked-review"), repair_rounds=0)
        assert parked.state == JOB_PAUSED
        parked_run_id = parked.tasks[0].run_id
        assert parked_run_id
        assert parked_session_refs(load_run(parked_run_id)) == {"builder": "sess-parked"}

        resumed = run_job(job.job_id, builder_provider=_resuming("sess-relaunch"),
                          reviewer_provider=_resuming("sess-relaunch-review"), repair_rounds=0)
        assert resumed.state == JOB_COMPLETED
        record = load_run(resumed.tasks[0].run_id)
        assert resumed.tasks[0].run_id != parked_run_id
        assert record["resumed_from_run_id"] == parked_run_id
        assert record["rounds"][0]["builder"]["resume_used"] is True
        assert record["rounds"][0]["builder"]["resume_session_ref"] == "sess-parked"
        assert record["rounds"][0]["reviewer"]["resume_used"] is False

    def test_a_task_that_was_never_interrupted_resumes_nothing(
            self, isolate_data_root, demo_repo):
        job = parse_job_file(_ONE_TASK_JOB, str(demo_repo))
        done = run_job(job.job_id, builder_provider=_resuming("sess-1"),
                       reviewer_provider=_resuming("sess-2"), repair_rounds=0)
        assert done.state == JOB_COMPLETED
        record = load_run(done.tasks[0].run_id)
        assert record["resumed_from_run_id"] == ""
        assert record["rounds"][0]["builder"]["resume_used"] is False
