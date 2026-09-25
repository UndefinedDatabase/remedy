"""F025 R8 T1 — DECISION F025 D6: a park records the episode it ends.

Reuses `test_pause_resume.py`'s own fixtures, fakes and job texts by import —
the same real `run_job` caller loop, the same fake providers, and a pause
requested the way an operator requests it. Each scenario proves the SAME
shape: the parked episode's manifest is written with status `paused`, carries
no stop request id and an empty `run_manifest_error`, and the relaunch's
completed episode finds it in the canonical chain — no error, two episodes,
`paused` then `completed`.
"""
from __future__ import annotations

import dataclasses

from packages.orchestration import pause_control as pc
from packages.orchestration.pingpong_job import (
    JOB_COMPLETED,
    JOB_PAUSED,
    job_evidence_dir,
    parse_job_file,
    run_job,
)
from packages.orchestration.run_manifest import (
    COVERAGE_COMPLETE,
    MODE_PUBLISHED_REFERENCE,
    load_episode_manifest_verified,
    load_latest_manifest_verified,
    validate_run_manifest,
)

# Reused exactly, per the block: the fixtures, fakes and job texts a pause is
# already driven through honestly.
from tests.orchestration.test_pause_resume import (  # noqa: F401
    _ONE_TASK_JOB,
    _TWO_TASK_JOB,
    PauseTriggerProvider,
    _pass_provider,
    demo_repo,
    isolate_data_root,
)


def _paused_episode(job):
    """The manifest of the episode a park just ended — loaded through the same
    anchored trust chain production reads it through."""
    ev = job_evidence_dir(job.job_id)
    return load_episode_manifest_verified(ev, job.active_episode_id,
                                          expected_job_id=job.job_id)


def _assert_paused_manifest(m) -> None:
    assert m.status == "paused"
    assert m.stop_request_id == ""
    assert m.coverage.status == COVERAGE_COMPLETE, m.coverage.problems
    assert validate_run_manifest(m, mode=MODE_PUBLISHED_REFERENCE) == []


def _assert_relaunch_completes_over_two_episodes(job_id: str) -> None:
    """The relaunch: a `completed` manifest over two episodes, `paused` then
    `completed`, and an empty `run_manifest_error` — R-1056's fix."""
    resumed = run_job(job_id, builder_provider=_pass_provider(),
                      reviewer_provider=_pass_provider(), repair_rounds=0)
    assert resumed.state == JOB_COMPLETED
    assert resumed.run_manifest_error == ""
    assert [e["status"] for e in resumed.run_manifest_episodes] == ["paused", "completed"]

    ev = job_evidence_dir(job_id)
    latest = load_latest_manifest_verified(ev, job_id=job_id)
    assert latest.status == "completed"
    assert latest.episode_ordinal == 2
    assert validate_run_manifest(latest, mode=MODE_PUBLISHED_REFERENCE) == []


class TestJobScopeParkMidBuild:
    """A job-scope park while a call is in flight (`test_pause_resume.py`'s
    TestRow1 scenario) — the episode-start snapshot is already bound by the
    time the park lands, so this is a `paused`/`worked` episode."""

    def test_the_parked_episode_is_recorded_and_the_relaunch_completes_clean(
            self, isolate_data_root, demo_repo):
        job = parse_job_file(_ONE_TASK_JOB, str(demo_repo))
        builder = PauseTriggerProvider(
            on_build=1,
            trigger=lambda: pc.request_pause(job.job_id, "mid-build pause", "cli"),
            pass_on_round=1, fail_on_round=99)
        parked = run_job(job.job_id, builder_provider=builder,
                         reviewer_provider=_pass_provider(), repair_rounds=0)
        assert parked.state == JOB_PAUSED
        assert parked.run_manifest_error == ""
        _assert_paused_manifest(_paused_episode(parked))

        _assert_relaunch_completes_over_two_episodes(job.job_id)


class TestTaskScopeParkInFlight:
    """A task-scope park while that task's own call is in flight
    (`test_pause_resume.py`'s TestRow5 scenario)."""

    def test_the_parked_episode_is_recorded_and_the_relaunch_completes_clean(
            self, isolate_data_root, demo_repo):
        job = parse_job_file(_ONE_TASK_JOB, str(demo_repo))
        task_id = job.tasks[0].task_id
        builder = PauseTriggerProvider(
            on_build=1,
            trigger=lambda: pc.request_task_pause(job.job_id, task_id, "look at this", "cli"),
            pass_on_round=1, fail_on_round=99)
        parked = run_job(job.job_id, builder_provider=builder,
                         reviewer_provider=_pass_provider(), repair_rounds=0)
        assert parked.state == JOB_PAUSED
        assert parked.pause.get("scope") == "task"
        assert parked.run_manifest_error == ""
        _assert_paused_manifest(_paused_episode(parked))

        pc.release_task_pause(job.job_id, task_id)
        _assert_relaunch_completes_over_two_episodes(job.job_id)


class TestJobScopePauseBeforeAnyWork:
    """A pause requested before the run ever starts (`test_pause_resume.py`'s
    TestRow2 scenario) — no episode-start snapshot exists yet, so `_park_job`
    must capture one itself, at `pre_work_stop`, exactly as `run_job`'s own
    pre-work stop branch does."""

    def test_the_parked_episode_is_recorded_and_the_relaunch_completes_clean(
            self, isolate_data_root, demo_repo):
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        pc.request_pause(job.job_id, "taking a break", "cli")
        parked = run_job(job.job_id, builder_provider=_pass_provider(),
                         reviewer_provider=_pass_provider(), repair_rounds=0)
        assert parked.state == JOB_PAUSED
        assert parked.run_manifest_error == ""
        m = _paused_episode(parked)
        _assert_paused_manifest(m)
        assert m.episode_snapshot.capture_phase == "pre_work_stop"
        assert m.calls == ()

        _assert_relaunch_completes_over_two_episodes(job.job_id)


class TestTaskCapPause:
    """The task cap's own pause (`test_pause_resume.py`'s TestRow10 scenario)
    — it carries no `job.pause` record at all (S1), so its manifest write is
    the only proof the park happened."""

    def test_the_parked_episode_is_recorded_and_the_relaunch_completes_clean(
            self, isolate_data_root, demo_repo):
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        capped = run_job(job.job_id, builder_provider=_pass_provider(),
                         reviewer_provider=_pass_provider(), repair_rounds=0,
                         max_tasks=1)
        assert capped.state == JOB_PAUSED
        assert capped.pause == {}
        assert capped.run_manifest_error == ""
        _assert_paused_manifest(_paused_episode(capped))

        _assert_relaunch_completes_over_two_episodes(job.job_id)


class TestAPausedManifestRefusesAStopRequestId:
    """DECISION F025 D6's validator rule: only a stopped manifest may carry a
    stop request id (`validate_run_manifest`'s F5/F7 rule, unchanged by this
    round) — a paused one carrying one is refused exactly the same way."""

    def test_a_stop_request_id_on_a_paused_manifest_is_refused(
            self, isolate_data_root, demo_repo):
        job = parse_job_file(_ONE_TASK_JOB, str(demo_repo))
        pc.request_pause(job.job_id, "taking a break", "cli")
        parked = run_job(job.job_id, builder_provider=_pass_provider(),
                         reviewer_provider=_pass_provider(), repair_rounds=0)
        assert parked.state == JOB_PAUSED

        forged = dataclasses.replace(_paused_episode(parked), stop_request_id="not-a-stop")
        probs = validate_run_manifest(forged, mode=MODE_PUBLISHED_REFERENCE)
        assert any("carries a stop_request_id" in p for p in probs), probs
