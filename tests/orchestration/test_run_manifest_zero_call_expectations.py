"""F6 (round 10) — a zero-call reference must PROVE zero calls were expected.

"No calls recorded" means two opposite things: this job genuinely had no work to do, or the
evidence went missing. A manifest that cannot tell them apart is not evidence of anything, and
before round 10 the difference was decided by looking at the mutable JobPlan — which by
verification time may have moved on.

So the episode record now carries a typed `CallExpectationV1`, decided at finalization while the
JobPlan and run records are still in hand. A published terminal reference may claim zero calls
only when its own embedded proof says zero were expected.

The contract's genuine zero-call cases are honoured exactly (T0_F012):
  * "Planning-only job (zero calls): valid manifest, empty hash list."
  * "a genuine zero-call (all-skipped) job, which stays valid and complete"
"""
from __future__ import annotations

import dataclasses
import json
import subprocess

import pytest

import tests.orchestration.test_run_manifest as T
from packages.orchestration import manifest_schema as _S
from packages.orchestration.run_manifest import (
    COVERAGE_COMPLETE,
    COVERAGE_INCOMPLETE,
    EXPECT_DISPATCHED_NO_CALLS,
    EXPECT_EXECUTED,
    EXPECT_NOT_DISPATCHED,
    EXPECT_PRIOR_EPISODE,
    EXPECT_SKIPPED,
    MODE_PUBLISHED_REFERENCE,
    PHASE_PLANNING_ONLY,
    PHASE_PRE_WORK_STOP,
    PHASE_WORKED,
    CallExpectationV1,
    EpisodeInputSnapshotV1,
    ManifestError,
    TaskCallExpectationV1,
    build_input_snapshot,
    build_run_manifest,
    decode_call_expectation_v1,
    load_latest_manifest_verified,
    validate_run_manifest,
    write_run_manifest,
)


@pytest.fixture
def data_root(tmp_path, monkeypatch):
    root = tmp_path / "remedy_data"
    root.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    return root


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / "repo"
    r.mkdir()
    subprocess.run("git init -q && git config user.email t@t && git config user.name t "
                   "&& echo '# demo' > README.md && git add -A && git commit -qm init",
                   shell=True, cwd=r, check=True)
    return r


def _prov():
    from packages.orchestration.pingpong_provider import FakeProvider
    return FakeProvider(pass_on_round=1, fail_on_round=99)


_JOB = "# Job: zero\n\n## Task 1\nx\n\nAcceptance:\n- y\n"


def _real_job(repo):
    from packages.orchestration.pingpong_job import load_job_plan, parse_job_file, run_job
    job = parse_job_file(_JOB, str(repo))
    run_job(job.job_id, builder_provider=_prov(), reviewer_provider=_prov(), repair_rounds=0)
    return load_job_plan(job.job_id)


def _manifest(job, status="completed", capture_phase="episode_start"):
    # A job that never ran carries no episode yet; the finalizer is always given one.
    if not job.active_episode_id:
        job.active_episode_id = "ep-zero"
    snap = build_input_snapshot(job, inspect_target=False, probe_versions=False)
    wrapper = EpisodeInputSnapshotV1(
        snapshot_v=1, episode_id=job.active_episode_id,
        captured_at="2026-07-16T00:00:00+00:00", capture_phase=capture_phase,
        status="ok", problems=(), input=snap)
    return build_run_manifest(job, status=status, episode_id=job.active_episode_id,
                              created_at="2026-07-16T00:00:00+00:00",
                              episode_snapshot=wrapper,
                              owned_episode_id=job.active_episode_id)


def _with_live_workspace(job, repo):
    """F10 (round 11): a WORKED episode acquires a workspace before it runs, so a fixture that
    models one has to have a real workspace under the canonical root — a worked episode with no
    workspace identity is exactly what the round-11 rules refuse."""
    import subprocess as _sp

    ws = repo / ".remedy-wt" / f"job-{job.job_id}"
    ws.parent.mkdir(parents=True, exist_ok=True)
    _sp.run(["git", "worktree", "add", "-q", "--detach", str(ws)], cwd=repo, check=True,
            capture_output=True)
    job.job_workspace_path = str(ws)
    job.job_initial_tree = "e" * 40
    job.episode_start_workspace_tree = "e" * 40
    return job


def _run_path(job, ix=0):
    from packages.orchestration.data_paths import run_dir
    return run_dir(job.tasks[ix].run_id) / "result.json"


# --------------------------------------------------------------------------- FALSE zero calls


class TestFalseZeroCallReferencesBlock:
    def test_an_executed_task_without_a_run_id_blocks(self, data_root, repo):
        """THE finding: an applied task whose run id had gone missing produced calls=[],
        coverage=complete, and a published reference that certified its own blind spot."""
        from packages.orchestration.pingpong_job import _persist_job, load_job_plan
        job = _real_job(repo)
        assert job.tasks[0].status == "applied_to_job_workspace"
        job.tasks[0].run_id = ""
        _persist_job(job)

        m = _manifest(load_job_plan(job.job_id))
        assert m.calls == ()
        assert m.coverage.status == COVERAGE_INCOMPLETE
        assert "has no run id" in "; ".join(m.coverage.problems)
        # and it cannot be published as a reference
        assert validate_run_manifest(m, mode=MODE_PUBLISHED_REFERENCE) != []

    def test_an_executed_task_with_a_missing_run_record_blocks(self, data_root, repo):
        job = _real_job(repo)
        _run_path(job).unlink()
        m = _manifest(job)
        assert m.coverage.status == COVERAGE_INCOMPLETE
        assert "missing run record" in "; ".join(m.coverage.problems)

    def test_an_executed_task_with_no_finalized_calls_field_blocks(self, data_root, repo):
        job = _real_job(repo)
        p = _run_path(job)
        d = json.loads(p.read_text())
        d.pop("finalized_calls")
        p.write_text(json.dumps(d))
        m = _manifest(job)
        assert m.coverage.status == COVERAGE_INCOMPLETE
        assert "no finalized_calls field" in "; ".join(m.coverage.problems)

    def test_an_executed_task_with_an_empty_finalized_calls_list_blocks(self, data_root, repo):
        """The run is readable and says nothing happened, while the task's own status says it
        ran. One of them is wrong, so neither is evidence."""
        job = _real_job(repo)
        p = _run_path(job)
        d = json.loads(p.read_text())
        d["finalized_calls"] = []
        p.write_text(json.dumps(d))
        m = _manifest(job)
        assert m.calls == ()
        assert m.coverage.status == COVERAGE_INCOMPLETE
        assert "recorded no finalized calls" in "; ".join(m.coverage.problems)

    def test_a_stored_zero_call_reference_without_a_proof_is_rejected(self, tmp_path):
        """Even if such bytes reach disk some other way, the canonical loader refuses them."""
        m = dataclasses.replace(
            T._mk(episode_id="ep1", calls=()),
            call_expectation=CallExpectationV1(
                episode_phase=PHASE_WORKED,
                tasks=(TaskCallExpectationV1(task_id="T001", expectation=EXPECT_EXECUTED,
                                             run_id="r1", expected_call_count=1),)))
        probs = validate_run_manifest(m, mode=MODE_PUBLISHED_REFERENCE)
        assert any("expected exactly 1 call(s) but the manifest carries 0" in p
                   for p in probs), probs

    def test_the_writer_refuses_a_false_zero_call_reference(self, tmp_path):
        ev = tmp_path / "ev"
        ev.mkdir()
        m = dataclasses.replace(
            T._mk(episode_id="ep1", calls=()),
            call_expectation=CallExpectationV1(
                episode_phase=PHASE_WORKED,
                tasks=(TaskCallExpectationV1(task_id="T001", expectation=EXPECT_EXECUTED,
                                             run_id="r1", expected_call_count=1),)))
        with pytest.raises(ManifestError):
            write_run_manifest(ev, m, root=tmp_path)


# --------------------------------------------------------------------------- GENUINE zero calls


class TestGenuineZeroCallReferencesStayValid:
    def test_a_pre_work_stop_is_a_valid_zero_call_reference(self, data_root, repo):
        """The contract's genuine case: the job stopped before any work began."""
        from packages.orchestration.pingpong_job import (
            JOB_STOPPED,
            job_evidence_dir,
            parse_job_file,
            run_job,
        )
        from packages.orchestration.safe_points import request_stop

        job = parse_job_file(_JOB, str(repo))
        request_stop(job.job_id, "operator requested stop", "test")
        done = run_job(job.job_id, builder_provider=_prov(), reviewer_provider=_prov(),
                       repair_rounds=0)
        assert done.status == JOB_STOPPED

        ref = load_latest_manifest_verified(job_evidence_dir(job.job_id), job_id=job.job_id)
        assert ref.calls == ()
        assert ref.coverage.status == COVERAGE_COMPLETE
        assert ref.call_expectation.expects_zero_calls()
        assert ref.call_expectation.episode_phase == PHASE_PRE_WORK_STOP
        assert [t.expectation for t in ref.call_expectation.tasks] == [EXPECT_NOT_DISPATCHED]
        assert validate_run_manifest(ref, mode=MODE_PUBLISHED_REFERENCE) == []

    def test_an_all_skipped_job_is_a_valid_zero_call_reference(self, data_root, repo):
        """T0_F012: "a genuine zero-call (all-skipped) job ... stays valid and complete"."""
        from packages.orchestration.pingpong_job import TASK_SKIPPED, parse_job_file
        job = _with_live_workspace(parse_job_file(_JOB, str(repo)), repo)
        job.tasks[0].status = TASK_SKIPPED
        m = _manifest(job)
        assert m.calls == ()
        assert m.coverage.status == COVERAGE_COMPLETE, m.coverage.problems
        assert m.call_expectation.expects_zero_calls()
        assert [t.expectation for t in m.call_expectation.tasks] == [EXPECT_SKIPPED]
        assert validate_run_manifest(m, mode=MODE_PUBLISHED_REFERENCE) == []

    def test_a_planning_only_job_is_a_valid_zero_call_reference(self, data_root, repo):
        """T0_F012: "Planning-only job (zero calls): valid manifest, empty hash list"."""
        from packages.orchestration.pingpong_job import parse_job_file
        job = parse_job_file(_JOB, str(repo))          # planned, never run
        # F7 (round 11): a planning-only episode is captured in an explicit PLANNING phase — the
        # phase is a fact of the capture, never inferred from the status afterwards.
        m = _manifest(job, status="planned", capture_phase=PHASE_PLANNING_ONLY)
        assert m.calls == ()
        assert m.coverage.status == COVERAGE_COMPLETE, m.coverage.problems
        assert m.call_expectation.episode_phase == PHASE_PLANNING_ONLY
        assert m.call_expectation.expects_zero_calls()
        assert validate_run_manifest(m, mode=MODE_PUBLISHED_REFERENCE) == []

    def test_a_not_yet_dispatched_task_expects_nothing(self, data_root, repo):
        """A task never reached (a stop boundary) owes no calls. F7 (round 11): this is a
        STOPPED episode — a completed one cannot contain an undispatched task."""
        from packages.orchestration.pingpong_job import TASK_PENDING, parse_job_file
        job = _with_live_workspace(parse_job_file(_JOB, str(repo)), repo)
        job.tasks[0].status = TASK_PENDING
        m = _manifest(job, status="stopped")
        m = dataclasses.replace(m, stop_request_id="stop-1")
        assert m.coverage.status == COVERAGE_COMPLETE, m.coverage.problems
        assert [t.expectation for t in m.call_expectation.tasks] == [EXPECT_NOT_DISPATCHED]
        assert validate_run_manifest(m, mode=MODE_PUBLISHED_REFERENCE) == []

    def test_a_failed_task_that_never_reached_a_call_is_honest(self, data_root, repo):
        """A task can die before its first provider call. Zero calls is then the honest record —
        and it is labelled as such rather than silently blank."""
        from packages.orchestration.pingpong_job import parse_job_file
        job = _with_live_workspace(parse_job_file(_JOB, str(repo)), repo)
        job.tasks[0].status = "failed"
        job.tasks[0].run_id = ""
        m = dataclasses.replace(_manifest(job, status="stopped"), stop_request_id="stop-1")
        assert m.coverage.status == COVERAGE_COMPLETE, m.coverage.problems
        # F4 (round 12): failed with NO run is `failed_pre_dispatch` — its own truth. Calling it
        # "not dispatched" would lose the failure; "dispatched_no_calls" would invent a run.
        from packages.orchestration.run_manifest import EXPECT_FAILED_PRE_DISPATCH
        assert [t.expectation for t in m.call_expectation.tasks] == [EXPECT_FAILED_PRE_DISPATCH]


# --------------------------------------------------------------------------- the record itself


class TestTheExpectationRecordIsSelfContained:
    def test_a_real_run_records_what_it_executed(self, data_root, repo):
        job = _real_job(repo)
        m = _manifest(job)
        assert m.coverage.status == COVERAGE_COMPLETE, m.coverage.problems
        te = m.call_expectation.tasks[0]
        assert te.task_id == "T001"
        assert te.expectation == EXPECT_EXECUTED
        assert te.run_id == job.tasks[0].run_id
        # F9 (round 11): EXACT counts plus the ledger seal that says which ledger was counted.
        assert te.expected_call_count == te.observed_call_count == len(m.calls) >= 1
        assert len(te.finalized_calls_sha256) == 64

    def test_the_proof_survives_the_canonical_round_trip(self, data_root, repo, tmp_path):
        """It is only a proof if it is IN the record — verification must never need the JobPlan."""
        from packages.orchestration.pingpong_job import job_evidence_dir
        job = _real_job(repo)
        ref = load_latest_manifest_verified(job_evidence_dir(job.job_id), job_id=job.job_id)
        raw = json.loads(ref.canonical_bytes())
        assert raw["call_expectation"]["tasks"][0]["expectation"] == EXPECT_EXECUTED
        assert decode_call_expectation_v1(raw["call_expectation"]) == ref.call_expectation

    def test_the_expectation_is_provenance_not_a_material_input(self, data_root, repo):
        """Two runs of the same inputs must hash the same logically, so what a run EXPECTED of
        its tasks (a fact about that execution) is provenance, never input identity."""
        job = _real_job(repo)
        m = _manifest(job)
        assert "call_expectation" not in m.logical_input_projection()
        assert "call_expectation" in m.provenance_projection()

    @pytest.mark.parametrize("bad", ["", "vibes", "worked ", "PRE_WORK_STOP"])
    def test_an_unknown_phase_is_rejected(self, bad):
        with pytest.raises(_S.SchemaError):
            decode_call_expectation_v1({"expectation_v": 1, "episode_phase": bad, "tasks": []})

    def test_an_unknown_task_expectation_is_rejected(self):
        with pytest.raises(_S.SchemaError):
            decode_call_expectation_v1({
                "expectation_v": 1, "episode_phase": PHASE_WORKED,
                "tasks": [{"task_id": "T001", "expectation": "probably-ran", "run_id": "",
                           "expected_min_calls": 0}]})

    def test_an_unknown_field_is_rejected(self):
        with pytest.raises(_S.SchemaError):
            decode_call_expectation_v1({"expectation_v": 1, "episode_phase": PHASE_WORKED,
                                        "tasks": [], "SMUGGLED": 1})

    def test_an_unsupported_version_is_rejected(self):
        with pytest.raises(_S.SchemaError):
            decode_call_expectation_v1({"expectation_v": 2, "episode_phase": PHASE_WORKED,
                                        "tasks": []})

    def test_an_executed_expectation_must_expect_a_call(self):
        m = dataclasses.replace(
            T._mk(episode_id="ep1"),
            call_expectation=CallExpectationV1(
                tasks=(TaskCallExpectationV1(task_id="T001", expectation=EXPECT_EXECUTED,
                                             run_id="r", expected_call_count=0),)))
        assert any("executed but expects no calls" in p
                   for p in validate_run_manifest(m, mode=MODE_PUBLISHED_REFERENCE))

    @pytest.mark.parametrize("expectation", [EXPECT_SKIPPED, EXPECT_NOT_DISPATCHED,
                                             EXPECT_PRIOR_EPISODE, EXPECT_DISPATCHED_NO_CALLS])
    def test_a_zero_call_expectation_must_not_expect_calls(self, expectation):
        m = dataclasses.replace(
            T._mk(episode_id="ep1", calls=()),
            call_expectation=CallExpectationV1(
                tasks=(TaskCallExpectationV1(task_id="T001", expectation=expectation,
                                             run_id="r", expected_call_count=2),)))
        assert any("expects 2 call(s)" in p
                   for p in validate_run_manifest(m, mode=MODE_PUBLISHED_REFERENCE))

    def test_the_proof_must_cover_exactly_the_embedded_task_list(self):
        m = dataclasses.replace(
            T._mk(episode_id="ep1", calls=()),
            call_expectation=CallExpectationV1(
                tasks=(TaskCallExpectationV1(task_id="T999", expectation=EXPECT_SKIPPED),)))
        assert any("not exactly the embedded" in p
                   for p in validate_run_manifest(m, mode=MODE_PUBLISHED_REFERENCE))
