"""F4 (round 12) — task status, Run ownership and the CallExpectation are ONE lifecycle record.

Persisted contradictions used to be normalized away:

    task.status = skipped,  task.run_id = r1  →  expectation skipped,        run_id discarded
    task.status = pending,  task.run_id = r1  →  expectation not_dispatched, run_id discarded

Erasing the run id makes the record look tidy and destroys the only sign that two persisted facts
disagreed. The record now keeps BOTH — the task's status at finalization and its dispatch state —
and the run id is never dropped to make an expectation validate.

One subtlety the reproduction did not cover, and the contract does: `pending` + a run is NOT a
contradiction. F011's mid-flight stop ("the call in flight finishes, nothing new starts") leaves
the task pending for the resume while its run already holds the finalized call. The lie would be
an expectation claiming "never dispatched" while a run exists — so THAT is what is refused.
`skipped` + a run IS a contradiction: skipping happens before dispatch.
"""
from __future__ import annotations

import json
import subprocess

import pytest

from packages.orchestration.pingpong_job import (
    TASK_APPLIED,
    TASK_PENDING,
    TASK_SKIPPED,
    load_job_plan,
    parse_job_file,
    run_job,
)
from packages.orchestration.run_manifest import (
    COVERAGE_COMPLETE,
    COVERAGE_INCOMPLETE,
    DISPATCH_NEVER,
    DISPATCH_THIS_EPISODE,
    EXPECT_DISPATCHED_NO_CALLS,
    EXPECT_EXECUTED,
    EXPECT_FAILED_PRE_DISPATCH,
    EXPECT_NOT_DISPATCHED,
    MODE_PUBLISHED_REFERENCE,
    EpisodeInputSnapshotV1,
    build_input_snapshot,
    build_run_manifest,
    validate_run_manifest,
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


_JOB = "# Job: tl\n\n## Task 1\nx\n\nAcceptance:\n- y\n"


def _ran(repo):
    job = parse_job_file(_JOB, str(repo))
    run_job(job.job_id, builder_provider=_prov(), reviewer_provider=_prov(), repair_rounds=0)
    return load_job_plan(job.job_id)


def _finalize(job, *, status="stopped", stop="stop-1", bind=False):
    """`bind=True` applies the production artifact binding the WRITER does, so the result can be
    validated as a published reference."""
    from packages.orchestration.run_manifest import _bind_artifact_refs

    snap = build_input_snapshot(job, inspect_target=False, probe_versions=False)
    wrapper = EpisodeInputSnapshotV1(
        snapshot_v=1, episode_id=job.active_episode_id,
        captured_at="2026-07-16T00:00:00+00:00", capture_phase="episode_start",
        status="ok", problems=(), input=snap)
    m = build_run_manifest(job, status=status, episode_id=job.active_episode_id,
                           created_at="2026-07-16T00:00:00+00:00",
                           episode_snapshot=wrapper,
                           owned_episode_id=job.active_episode_id,
                           stop_request_id=stop)
    return _bind_artifact_refs(m) if bind else m


def _run_path(job):
    from packages.orchestration.data_paths import run_dir
    return run_dir(job.tasks[0].run_id) / "result.json"


def _te(m):
    return m.call_expectation.tasks[0]


# --------------------------------------------------------------------------- contradictions


class TestPersistedContradictionsAreReportedNotNormalized:
    def test_a_skipped_task_that_owns_a_run_blocks(self, data_root, repo):
        """THE finding: the run id was discarded and the record looked clean."""
        job = _ran(repo)
        run_id = job.tasks[0].run_id
        job.tasks[0].status = TASK_SKIPPED
        m = _finalize(job)
        assert m.coverage.status == COVERAGE_INCOMPLETE
        assert "cannot own a run" in "; ".join(m.coverage.problems)
        assert _te(m).run_id == run_id, "the contradictory run id was erased"
        assert _te(m).task_status_at_finalization == TASK_SKIPPED

    def test_the_record_keeps_both_persisted_facts(self, data_root, repo):
        job = _ran(repo)
        job.tasks[0].status = TASK_SKIPPED
        te = _te(_finalize(job))
        assert te.task_status_at_finalization == TASK_SKIPPED
        assert te.dispatch_state == DISPATCH_THIS_EPISODE
        assert te.run_id and te.ledger_ref

    def test_an_expectation_may_never_claim_never_dispatched_while_owning_a_run(self):
        """The validator's half of the rule: whatever a collector produced, a stored record that
        says 'never dispatched' AND names a run cannot be published."""
        import dataclasses

        import tests.orchestration.test_run_manifest as T
        from packages.orchestration.run_manifest import (
            CallExpectationV1,
            TaskCallExpectationV1,
        )
        m = T._mk(episode_id="ep1", calls=())
        forged = dataclasses.replace(m, call_expectation=CallExpectationV1(
            tasks=(TaskCallExpectationV1(
                task_id="T001", expectation=EXPECT_NOT_DISPATCHED, run_id="r1",
                task_status_at_finalization="pending", dispatch_state=DISPATCH_NEVER),)))
        probs = validate_run_manifest(forged, mode=MODE_PUBLISHED_REFERENCE)
        assert any("never dispatched and the owner of a run" in p for p in probs), probs


# --------------------------------------------------------------------------- the real states


class TestTheLifecycleStatesProductionProduces:
    def test_a_pending_task_with_a_run_is_a_mid_flight_stop_not_a_contradiction(
            self, data_root, repo):
        """F011: the call in flight finishes, nothing new starts — the task is pending for the
        resume and its run already holds the work. The expectation says what happened."""
        job = _ran(repo)
        job.tasks[0].status = TASK_PENDING
        m = _finalize(job, bind=True)
        assert m.coverage.status == COVERAGE_COMPLETE, m.coverage.problems
        te = _te(m)
        assert te.expectation == EXPECT_EXECUTED
        assert te.task_status_at_finalization == TASK_PENDING
        assert te.run_id == job.tasks[0].run_id
        assert validate_run_manifest(m, mode=MODE_PUBLISHED_REFERENCE) == []

    def test_an_applied_task_without_a_run_blocks(self, data_root, repo):
        job = _ran(repo)
        job.tasks[0].run_id = ""
        m = _finalize(job)
        assert m.coverage.status == COVERAGE_INCOMPLETE
        assert "has no run id" in "; ".join(m.coverage.problems)

    def test_a_failed_task_with_no_run_is_failed_pre_dispatch(self, data_root, repo):
        job = _ran(repo)
        job.tasks[0].status = "failed"
        job.tasks[0].run_id = ""
        m = _finalize(job)
        te = _te(m)
        assert te.expectation == EXPECT_FAILED_PRE_DISPATCH
        assert te.dispatch_state == DISPATCH_NEVER
        assert not te.run_id and not te.ledger_ref
        assert m.coverage.status == COVERAGE_COMPLETE, m.coverage.problems

    def test_dispatched_no_calls_requires_a_real_sealed_zero_entry_ledger(
            self, data_root, repo):
        """A run that exists and recorded nothing is a real state — and it must be able to show
        the ledger it is talking about."""
        job = _ran(repo)
        p = _run_path(job)
        d = json.loads(p.read_text())
        d["finalized_calls"] = []
        p.write_text(json.dumps(d))
        job.tasks[0].status = "failed"
        m = _finalize(job)
        te = _te(m)
        assert te.expectation == EXPECT_DISPATCHED_NO_CALLS
        assert te.run_id == job.tasks[0].run_id
        assert len(te.finalized_calls_sha256) == 64
        lg = next(x for x in m.call_ledgers if x.run_id == te.run_id)
        assert lg.entries == () and lg.complete is True
        assert m.coverage.status == COVERAGE_COMPLETE, m.coverage.problems

    def test_an_executed_task_has_a_real_ledger_with_exact_entries(self, data_root, repo):
        job = _ran(repo)
        m = _finalize(job, status="completed", stop="", bind=True)
        te = _te(m)
        assert te.expectation == EXPECT_EXECUTED
        assert te.task_status_at_finalization == TASK_APPLIED
        assert te.expected_call_count == te.observed_call_count == len(m.calls) >= 1
        lg = next(x for x in m.call_ledgers if x.run_id == te.run_id)
        assert len(lg.entries) == len(m.calls)
        assert validate_run_manifest(m, mode=MODE_PUBLISHED_REFERENCE) == []

    def test_a_missing_run_record_blocks(self, data_root, repo):
        job = _ran(repo)
        _run_path(job).unlink()
        m = _finalize(job)
        assert m.coverage.status == COVERAGE_INCOMPLETE
        assert "missing run record" in "; ".join(m.coverage.problems)

    def test_a_missing_finalized_calls_ledger_field_blocks(self, data_root, repo):
        job = _ran(repo)
        p = _run_path(job)
        d = json.loads(p.read_text())
        d.pop("finalized_calls")
        p.write_text(json.dumps(d))
        m = _finalize(job)
        assert m.coverage.status == COVERAGE_INCOMPLETE
        assert "no finalized_calls field" in "; ".join(m.coverage.problems)
