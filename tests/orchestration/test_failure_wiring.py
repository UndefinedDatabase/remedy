"""F010 T002 — post-mortems at the REAL failure exits.

Real code paths, no provider: the retry helper the loop actually uses, the writer the loop
actually calls, and the evidence export that really runs. The negative cases matter as much
as the positive ones — a call that recovers must leave *nothing* behind, or the histogram
starts counting weather instead of failures.
"""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from packages.orchestration import failure_postmortem as FP
from packages.orchestration.pingpong_loop import (
    PingPongResult,
    _call_with_retry,
    _pingpong_runs_dir,
    _record_call_failure,
)
from packages.orchestration.pingpong_provider import BuilderOutput, ReviewerOutput
from packages.orchestration.worktrees import WorktreeConflictError, WorktreeLockError


@pytest.fixture(autouse=True)
def data_root(tmp_path, monkeypatch) -> Path:
    root = tmp_path / "remedy_data"
    root.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    return root


@pytest.fixture
def demo_repo(tmp_path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "README.md").write_text("# Demo\n")
    return repo


def _run_dir(result: PingPongResult) -> Path:
    return _pingpong_runs_dir() / result.run_id


def _postmortems(result: PingPongResult) -> list[dict]:
    return [json.loads(p.read_text())
            for p in sorted(FP.collect_call_postmortems(_run_dir(result)))]


def _timeout_out() -> BuilderOutput:
    # The message the retry path itself recognises as a timeout — the same predicate,
    # so a call classified `provider_timeout` is exactly a call F001 retried as one.
    return BuilderOutput(error="provider_error: TimeoutExpired: after 600s",
                         provider="fake")


class TestOneLogicalCallOnePostmortem:
    @patch("packages.orchestration.pingpong_loop._time.sleep")
    def test_timeout_exhaustion_writes_exactly_one_call_postmortem(self, sleep):
        """Retries are exhausted; the call is abandoned. One record, with the evidence."""
        result = PingPongResult(job_id="J1", task_id="T001")
        calls = [0]
        reasons: list[str] = []

        def call_fn():
            calls[0] += 1
            return _timeout_out()

        out = _call_with_retry(call_fn, result=result, role="builder", provider="fake",
                               call_reasons=reasons)

        assert calls[0] == 3, "the existing retry policy ran: 1 call + 2 retries"
        assert result.retries_used == 2
        assert sleep.call_args_list[0][0][0] == 30, "F001's backoff schedule is untouched"

        _record_call_failure(result, out, role="builder", provider="fake", round_no=1,
                             call_reasons=reasons)

        records = _postmortems(result)
        assert len(records) == 1, "one logical call, one post-mortem"
        record = records[0]
        assert record["failure_class"] == "provider_timeout"
        assert record["scope"] == "call"
        assert record["retries_used"] == 2
        assert record["retry_reasons"], "the retry evidence travelled with the record"
        assert record["job_id"] == "J1" and record["task_id"] == "T001"
        assert all(not r.startswith("/") for r in record["evidence_refs"])

    @patch("packages.orchestration.pingpong_loop._time.sleep")
    def test_a_recovered_retry_writes_no_postmortem_at_all(self, _sleep):
        """The negative proof. A call that fails, retries and SUCCEEDS is not a failure."""
        result = PingPongResult(job_id="J1", task_id="T001")
        calls = [0]

        def call_fn():
            calls[0] += 1
            if calls[0] == 1:
                return _timeout_out()
            return BuilderOutput(summary="recovered", provider="fake")

        out = _call_with_retry(call_fn, result=result, role="builder", provider="fake")

        assert out.error == "" and result.retries_used == 1
        # The loop only records at its terminal exits, and this call never reached one.
        _record_call_failure(result, out, role="builder", provider="fake", round_no=1)
        assert _postmortems(result) == []

    def test_a_missing_provider_binary_is_provider_unavailable(self):
        result = PingPongResult(job_id="J1", task_id="T001")
        out = BuilderOutput(
            error="provider_error: FileNotFoundError: claude: command not found",
            provider="claude-cli")
        _record_call_failure(result, out, role="builder", provider="claude-cli", round_no=1)

        records = _postmortems(result)
        assert len(records) == 1
        assert records[0]["failure_class"] == "provider_unavailable"

    def test_a_final_nonzero_exit_is_provider_nonzero_exit(self):
        result = PingPongResult(job_id="J1", task_id="T001")
        out = BuilderOutput(error="claude CLI exited 1: internal error", provider="fake")
        _record_call_failure(result, out, role="builder", provider="fake", round_no=1)
        assert _postmortems(result)[0]["failure_class"] == "provider_nonzero_exit"

    def test_an_unrecovered_parse_retry_writes_one_parse_postmortem(self):
        """The parse retry is part of ONE logical review call: it records once, at the end."""
        result = PingPongResult(job_id="J1", task_id="T001")
        out = ReviewerOutput(
            error="malformed_output: not json", error_class="parse", provider="fake")
        out.parse_retried = True
        _record_call_failure(result, out, role="reviewer", provider="fake",
                             round_no=1, kind="parse-retry")

        records = _postmortems(result)
        assert len(records) == 1
        assert records[0]["failure_class"] == "parse"
        assert records[0]["role"] == "reviewer"
        assert "parse-retry" in records[0]["call_id"]

    def test_a_reviewer_rejection_is_not_recorded_as_a_provider_failure(self):
        result = PingPongResult(job_id="J1", task_id="T001")
        out = ReviewerOutput(verdict="needs_repair", summary="found issues", provider="fake")
        _record_call_failure(result, out, role="reviewer", provider="fake", round_no=1)
        assert _postmortems(result) == [], "a normal rejection is not a failed call"

    def test_the_provider_call_directory_is_reused_when_it_streams(self, tmp_path):
        """The post-mortem lands beside that call's own stream artifacts."""
        result = PingPongResult(job_id="J1", task_id="T001")
        call_dir = tmp_path / "streams" / "builder" / "round-01" / "attempt-01"
        call_dir.mkdir(parents=True)
        (call_dir / "raw_stream.jsonl").write_text("{}\n")

        class _Streaming:
            last_stream_call_dir = str(call_dir)

        out = _timeout_out()
        out.stream_call_id = "streams/builder/round-01/attempt-01"
        _record_call_failure(result, out, role="builder", provider="claude-cli",
                             provider_obj=_Streaming(), round_no=1)

        record = json.loads((call_dir / "postmortem.json").read_text())
        assert record["failure_class"] == "provider_timeout"
        assert record["evidence_refs"] == ["raw_stream.jsonl"]
        assert not (_run_dir(result) / "calls").exists(), "no parallel evidence tree"


class TestTaskRollup:
    def _job_with_task(self, demo_repo, **task_kw):
        from packages.orchestration.pingpong_job import JobPlan, TaskEntry, _persist_job
        task = TaskEntry(task_id="T001", title="t", body="b", **task_kw)
        job = JobPlan(repo_path=str(demo_repo), job_title="F010 job", tasks=[task])
        _persist_job(job)
        return job

    def _export(self, job, out: Path) -> dict:
        from packages.orchestration.job_evidence import export_job_evidence
        return export_job_evidence(job.job_id, str(out))

    @pytest.mark.parametrize("status,final_status,error,expected", [
        ("failed", "test_failed", "3 tests failed", "test_failed"),
        ("failed", "review_failed", "reviewer rejected", "review_failed"),
        ("blocked", "worktree_lock", "lock held by run r9", "worktree_lock"),
        ("blocked", "worktree_conflict", "both changed x.py", "worktree_conflict"),
        ("failed", "runtime_probe_failed", "supervisor_missing", "runtime_probe_failed"),
        ("failed", "provider_unavailable", "claude: command not found",
         "provider_unavailable"),
    ])
    def test_a_terminal_task_gets_exactly_one_rollup(
        self, demo_repo, tmp_path, status, final_status, error, expected,
    ):
        job = self._job_with_task(demo_repo, status=status, final_status=final_status,
                                  error=error)
        out = tmp_path / "evidence"
        self._export(job, out)

        rollup = out / "task_runs" / "T001" / "postmortem.json"
        assert rollup.is_file()
        record = json.loads(rollup.read_text())
        assert record["scope"] == "task"
        assert record["failure_class"] == expected
        assert record["signal_source"] == "terminal_status"
        assert record["job_id"] == job.job_id
        assert not any(str(v).startswith("/") for v in record.values() if isinstance(v, str))

    def test_a_passing_task_gets_no_rollup(self, demo_repo, tmp_path):
        job = self._job_with_task(demo_repo, status="passed", final_status="staged_review_passed")
        out = tmp_path / "evidence"
        self._export(job, out)
        assert not (out / "task_runs" / "T001" / "postmortem.json").exists()

    def test_re_exporting_does_not_duplicate_the_rollup(self, demo_repo, tmp_path):
        job = self._job_with_task(demo_repo, status="failed", final_status="test_failed",
                                  error="tests failed")
        out = tmp_path / "evidence"
        self._export(job, out)
        self._export(job, out)                # finalization runs again
        task_dir = out / "task_runs" / "T001"
        assert len(list(task_dir.glob("postmortem*.json"))) == 1

    def test_the_rollup_references_the_call_postmortems_relatively(
        self, demo_repo, tmp_path,
    ):
        job = self._job_with_task(demo_repo, status="failed", final_status="review_failed",
                                  error="reviewer failed", run_id="run-f010")

        # the call-level record this run left behind
        result = PingPongResult(job_id=job.job_id, task_id="T001", run_id="run-f010")
        _record_call_failure(result, _timeout_out(), role="builder", provider="fake",
                             round_no=1)

        out = tmp_path / "evidence"
        self._export(job, out)

        record = json.loads((out / "task_runs" / "T001" / "postmortem.json").read_text())
        assert record["failure_class"] == "review_failed"
        assert record["evidence_refs"], "the rollup points at the call-level records"
        for ref in record["evidence_refs"]:
            assert not ref.startswith("/") and ".." not in ref
            assert (out / "task_runs" / "T001" / ref).is_file(), "and they are IN the bundle"

    def test_a_task_with_no_provider_call_still_rolls_up(self, demo_repo, tmp_path):
        job = self._job_with_task(demo_repo, status="blocked", final_status="worktree_lock",
                                  error="lock held")
        out = tmp_path / "evidence"
        self._export(job, out)
        record = json.loads((out / "task_runs" / "T001" / "postmortem.json").read_text())
        assert record["failure_class"] == "worktree_lock"
        assert record["evidence_refs"] == []


class TestTypedWorktreeExceptions:
    """The real typed exceptions, classified as themselves."""

    def test_a_worktree_lock_error(self):
        verdict = FP.classify(FP.FailureSignals(exception=WorktreeLockError("held")))
        assert verdict.failure_class is FP.FailureClass.WORKTREE_LOCK

    def test_a_worktree_conflict_error(self):
        verdict = FP.classify(FP.FailureSignals(exception=WorktreeConflictError("clash")))
        assert verdict.failure_class is FP.FailureClass.WORKTREE_CONFLICT


# ---------------------------------------------------------------------------
# The REAL provider timeout wording (external finding 3)
# ---------------------------------------------------------------------------

CLAUDE_TIMEOUT = "provider_error: RuntimeError: claude CLI timed out after 600s"


class TestTheRealClaudeTimeoutMessage:
    """`ClaudeCliProvider` says "timed out after 600s" — not "timeout", not
    "TimeoutExpired". The reviewed build neither retried it nor classified it."""

    def test_the_real_message_is_a_timeout_to_the_shared_predicate(self):
        from packages.orchestration.provider_timeouts import is_timeout_error
        assert is_timeout_error(CLAUDE_TIMEOUT)
        assert FP.classify(FP.FailureSignals(error_text=CLAUDE_TIMEOUT)).failure_class is (
            FP.FailureClass.PROVIDER_TIMEOUT)

    @patch("packages.orchestration.pingpong_loop._time.sleep")
    def test_the_retry_path_treats_the_real_message_as_retryable(self, sleep):
        result = PingPongResult()
        calls = [0]

        def call_fn():
            calls[0] += 1
            if calls[0] == 1:
                return BuilderOutput(error=CLAUDE_TIMEOUT, provider="claude-cli")
            return BuilderOutput(summary="recovered", provider="claude-cli")

        out = _call_with_retry(call_fn, result=result, role="builder",
                               provider="claude-cli")

        assert out.error == "" and result.retries_used == 1
        assert sleep.call_args_list[0][0][0] == 30, "F001's backoff is unchanged"
        _record_call_failure(result, out, role="builder", provider="claude-cli", round_no=1)
        assert _postmortems(result) == [], "a recovered retry records nothing"

    @patch("packages.orchestration.pingpong_loop._time.sleep")
    def test_exhausted_real_timeouts_write_exactly_one_provider_timeout_record(self, _s):
        result = PingPongResult(job_id="J1", task_id="T001")
        out = _call_with_retry(
            lambda: BuilderOutput(error=CLAUDE_TIMEOUT, provider="claude-cli"),
            result=result, role="builder", provider="claude-cli")

        _record_call_failure(result, out, role="builder", provider="claude-cli", round_no=1)
        records = _postmortems(result)
        assert len(records) == 1
        assert records[0]["failure_class"] == "provider_timeout"
        assert result.retries_used == 2


# ---------------------------------------------------------------------------
# The target-mutation guard (external finding 2)
# ---------------------------------------------------------------------------

class TestTargetGuardExemptionIsStrict:
    """The exemption is for `repo/.data` — and for nothing else.

    A data root that IS the repository, or an ancestor of it, would exempt every file in
    the tree and silently switch the whole guard off. The reviewer reproduced exactly that.
    """

    def _changed(self, repo: Path):
        from packages.orchestration.pingpong_loop import (
            _classify_target_changes,
            _snapshot_target,
        )
        before = _snapshot_target(repo)
        (repo / "source.py").write_text("mutated by the builder\n")
        return _classify_target_changes(repo, before)

    @pytest.fixture
    def repo(self, tmp_path) -> Path:
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "source.py").write_text("original\n")
        return repo

    def test_data_root_inside_the_repo_exempts_only_what_is_inside_it(
        self, repo, monkeypatch,
    ):
        """The real case: a visible data root inside the repo (what the test suites use).

        Remedy's own run records and post-mortems under it are operational; the source file
        beside it is still a target mutation.
        """
        data_root = repo / "remedy_data"
        (data_root / "pingpong_runs").mkdir(parents=True)
        monkeypatch.setenv("REMEDY_DATA_DIR", str(data_root))

        from packages.orchestration.pingpong_loop import (
            _classify_target_changes,
            _snapshot_target,
        )
        before = _snapshot_target(repo)
        (data_root / "pingpong_runs" / "postmortem.json").write_text("{}\n")
        (repo / "source.py").write_text("mutated\n")
        content, operational, _noise = _classify_target_changes(repo, before)

        assert content == ["source.py"], "the source change is still meaningful"
        assert any("remedy_data" in o for o in operational), (
            "Remedy writing its own evidence is not a builder mutation")

    def test_data_root_equal_to_the_repo_exempts_nothing(self, repo, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(repo))
        content, operational, _ = self._changed(repo)
        assert content == ["source.py"]
        assert "source.py" not in operational

    def test_data_root_above_the_repo_exempts_nothing(self, repo, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(repo.parent))
        content, operational, _ = self._changed(repo)
        assert content == ["source.py"]
        assert "source.py" not in operational

    def test_a_sibling_data_root_exempts_nothing(self, repo, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "elsewhere"))
        content, operational, _ = self._changed(repo)
        assert content == ["source.py"]
        assert "source.py" not in operational

    def test_a_symlinked_data_root_does_not_widen_the_exemption(
        self, repo, tmp_path, monkeypatch,
    ):
        outside = tmp_path / "outside_data"
        outside.mkdir()
        (repo / ".data").symlink_to(outside, target_is_directory=True)
        monkeypatch.setenv("REMEDY_DATA_DIR", str(repo / ".data"))

        content, operational, _ = self._changed(repo)
        assert content == ["source.py"], "a symlinked data root exempts no source file"
        assert "source.py" not in operational


# ---------------------------------------------------------------------------
# Streamed call post-mortems survive the export (external finding 1)
# ---------------------------------------------------------------------------

class TestStreamedCallPostmortemExport:
    def _job(self, demo_repo, **task_kw):
        from packages.orchestration.pingpong_job import JobPlan, TaskEntry, _persist_job
        job = JobPlan(repo_path=str(demo_repo), job_title="streamed job",
                      tasks=[TaskEntry(task_id="T001", title="t", body="b", **task_kw)])
        _persist_job(job)
        return job

    def test_a_streamed_call_record_reaches_the_bundle_and_is_counted_once(
        self, demo_repo, tmp_path,
    ):
        from packages.orchestration.failure_stats import collect_failures
        from packages.orchestration.job_evidence import export_job_evidence
        from packages.orchestration.pingpong_job import _task_stream_dir

        job = self._job(demo_repo, status="failed", final_status="review_failed",
                        error="reviewer failed", run_id="run-streamed")

        # exactly the production layout: jobs/<job>/evidence/task_runs/<task>/streams/...
        streams_root = _task_stream_dir(job.job_id, "T001") / "streams"
        call_dir = streams_root / "builder" / "round-01" / "attempt-01"
        call_dir.mkdir(parents=True)
        (call_dir / "raw_stream.jsonl").write_text("{}\n")
        FP.write_postmortem(
            call_dir,
            FP.PostmortemV1(
                failure_class=FP.FailureClass.PROVIDER_TIMEOUT,
                signal_source=FP.SIGNAL_ERROR_TEXT, scope="call",
                job_id=job.job_id, task_id="T001", run_id="run-streamed",
                role="builder", provider="claude-cli", raw_reason=CLAUDE_TIMEOUT,
            ),
            root=streams_root,
        )

        out = Path(__import__("packages.orchestration.data_paths", fromlist=["x"])
                   .evidence_exports_dir()) / job.job_id
        export_job_evidence(job.job_id, str(out))

        canonical = (out / "task_runs" / "T001" / "call_postmortems"
                     / "streams" / "builder" / "round-01" / "attempt-01"
                     / "postmortem.json")
        assert canonical.is_file(), "the streamed record never reached the bundle"

        rollup = json.loads((out / "task_runs" / "T001" / "postmortem.json").read_text())
        assert rollup["evidence_refs"] == [
            "call_postmortems/streams/builder/round-01/attempt-01/postmortem.json"]
        assert (out / "task_runs" / "T001" / rollup["evidence_refs"][0]).is_file()

        stats = collect_failures()
        assert stats["counts_by_scope"]["call"] == 1
        assert stats["counts_by_scope"]["task"] == 1
        assert stats["total_postmortems"] == 2, "the source copy was not double-counted"

        export_job_evidence(job.job_id, str(out))          # re-export: idempotent
        assert collect_failures()["total_postmortems"] == 2

    def test_the_raw_stream_artifacts_still_travel(self, demo_repo, tmp_path):
        from packages.orchestration.job_evidence import export_job_evidence
        from packages.orchestration.pingpong_job import _task_stream_dir

        job = self._job(demo_repo, status="failed", final_status="test_failed",
                        error="tests failed", run_id="run-streamed")
        call_dir = (_task_stream_dir(job.job_id, "T001") / "streams"
                    / "builder" / "round-01" / "attempt-01")
        call_dir.mkdir(parents=True)
        (call_dir / "raw_stream.jsonl").write_text("{}\n")

        out = tmp_path / "evidence"
        export_job_evidence(job.job_id, str(out))
        assert (out / "task_runs" / "T001" / "streams" / "builder" / "round-01"
                / "attempt-01" / "raw_stream.jsonl").is_file()


# ---------------------------------------------------------------------------
# A job that failed before any task ran (external finding 6)
# ---------------------------------------------------------------------------

class TestJobLevelPostmortem:
    @pytest.mark.parametrize("exc_name,expected", [
        ("WorktreeLockError", "worktree_lock"),
        ("WorktreeConflictError", "worktree_conflict"),
    ])
    def test_a_workspace_acquisition_failure_emits_one_job_postmortem(
        self, demo_repo, monkeypatch, exc_name, expected,
    ):
        from packages.orchestration import pingpong_job as PJ
        from packages.orchestration.failure_stats import collect_failures
        from packages.orchestration.job_evidence import export_job_evidence

        exc_type = {"WorktreeLockError": WorktreeLockError,
                    "WorktreeConflictError": WorktreeConflictError}[exc_name]

        def boom(job):
            raise exc_type("job worktree is locked by run r9")

        monkeypatch.setattr(PJ, "_acquire_job_workspace", boom)

        job = PJ.JobPlan(repo_path=str(demo_repo), job_title="locked job",
                         tasks=[PJ.TaskEntry(task_id="T001", title="t", body="b")])
        PJ._persist_job(job)

        done = PJ.run_job(job.job_id)
        assert done.status == "blocked"
        assert done.tasks[0].status == "pending", "no task ever ran"

        record = json.loads(PJ.job_postmortem_path(job.job_id).read_text())
        assert record["scope"] == "job"
        assert record["failure_class"] == expected
        assert record["signal_source"] == "typed_exception"
        assert record["task_id"] == "", "the pending task is not blamed"

        out = Path(__import__("packages.orchestration.data_paths", fromlist=["x"])
                   .evidence_exports_dir()) / job.job_id
        export_job_evidence(job.job_id, str(out))
        assert json.loads((out / "postmortem.json").read_text())["failure_class"] == expected
        assert not (out / "task_runs" / "T001" / "postmortem.json").exists(), (
            "a pending task must not get a fake rollup")

        stats = collect_failures()
        assert stats["counts_by_scope"]["job"] == 1
        assert stats["counts_by_class"][expected] == 1


# ---------------------------------------------------------------------------
# A post-mortem that could NOT be written (external finding 4)
# ---------------------------------------------------------------------------

class TestWriteFailureIsVisibleAndBlocking:
    def test_a_call_level_write_failure_is_durable_in_the_run_json(self, monkeypatch):
        from packages.orchestration import pingpong_loop as PL

        def refuse(directory, record, *, root=None):
            raise FP.PostmortemError("injected: evidence directory is read-only")

        monkeypatch.setattr(FP, "write_postmortem", refuse)

        result = PingPongResult(job_id="J1", task_id="T001")
        out = BuilderOutput(error="claude CLI exited 1: internal error", provider="fake")
        _record_call_failure(result, out, role="builder", provider="fake", round_no=1)

        assert "injected" in result.postmortem_error
        assert result.postmortem_paths == []

        exported = PL.export_pingpong_json(result)
        assert "injected" in exported["postmortem_error"], "the failure was not durable"
        assert exported["postmortem_paths"] == []
        # ...and the ORIGINAL failure is untouched: no misleading new class.
        assert out.error == "claude CLI exited 1: internal error"

    def test_a_recorded_write_failure_blocks_the_package(self, demo_repo, tmp_path):
        """A bundle that lost a required record must not present clean gates."""
        from packages.orchestration.final_verifier import build_final_verifier_report
        from packages.orchestration.job_evidence import export_job_evidence
        from packages.orchestration.pingpong_job import JobPlan, TaskEntry, _persist_job
        from packages.orchestration.pingpong_loop import _pingpong_runs_dir

        job = JobPlan(repo_path=str(demo_repo), job_title="broken recording",
                      tasks=[TaskEntry(task_id="T001", title="t", body="b",
                                       status="failed", final_status="review_failed",
                                       error="reviewer failed", run_id="run-broken")])
        _persist_job(job)

        run_dir = _pingpong_runs_dir() / "run-broken"
        run_dir.mkdir(parents=True)
        (run_dir / "result.json").write_text(json.dumps({
            "run_id": "run-broken",
            "postmortem_paths": [],
            "postmortem_error": "PostmortemError: evidence directory is read-only",
        }) + "\n")

        out = tmp_path / "evidence"
        export_job_evidence(job.job_id, str(out))

        integrity = json.loads((out / "postmortem_integrity.json").read_text())
        assert integrity["ok"] is False
        assert integrity["failures"][0]["task_id"] == "T001"
        assert "read-only" in integrity["failures"][0]["error"]

        report = build_final_verifier_report(str(out))
        assert report["postmortem_integrity_blocked"] is True
        assert report["verdict"] == "BLOCKED", "a lost post-mortem cannot pass the gates"

    def test_a_healthy_export_reports_clean_postmortem_integrity(self, demo_repo, tmp_path):
        from packages.orchestration.job_evidence import export_job_evidence
        from packages.orchestration.pingpong_job import JobPlan, TaskEntry, _persist_job

        job = JobPlan(repo_path=str(demo_repo), job_title="healthy",
                      tasks=[TaskEntry(task_id="T001", title="t", body="b",
                                       status="failed", final_status="test_failed",
                                       error="tests failed")])
        _persist_job(job)
        out = tmp_path / "evidence"
        export_job_evidence(job.job_id, str(out))

        integrity = json.loads((out / "postmortem_integrity.json").read_text())
        assert integrity == {"schema_version": "1.0.0", "ok": True, "failures": []}


# ---------------------------------------------------------------------------
# Finding 2 — a symlinked data root exempts NOTHING
# ---------------------------------------------------------------------------

class TestDataRootSymlinksExemptNothing:
    def _changed(self, repo: Path):
        from packages.orchestration.pingpong_loop import (
            _classify_target_changes,
            _snapshot_target,
        )
        before = _snapshot_target(repo)
        (repo / "src" / "source.py").write_text("mutated by the builder\n")
        return _classify_target_changes(repo, before)

    @pytest.fixture
    def repo(self, tmp_path) -> Path:
        repo = tmp_path / "repo"
        (repo / "src").mkdir(parents=True)
        (repo / "src" / "source.py").write_text("original\n")
        return repo

    def test_a_real_data_directory_inside_the_repo_still_works(self, repo, monkeypatch):
        data = repo / "remedy_data"
        (data / "pingpong_runs").mkdir(parents=True)
        monkeypatch.setenv("REMEDY_DATA_DIR", str(data))

        from packages.orchestration.pingpong_loop import (
            _classify_target_changes,
            _snapshot_target,
        )
        before = _snapshot_target(repo)
        (data / "pingpong_runs" / "postmortem.json").write_text("{}\n")
        (repo / "src" / "source.py").write_text("mutated\n")
        content, operational, _ = _classify_target_changes(repo, before)

        assert content == ["src/source.py"]
        assert any("remedy_data" in o for o in operational)

    def test_a_data_root_symlinked_into_the_source_tree_exempts_nothing(
        self, repo, monkeypatch,
    ):
        """`repo/remedy_data -> repo/src` would otherwise make every source file
        "Remedy's own data"."""
        (repo / "remedy_data").symlink_to(repo / "src", target_is_directory=True)
        monkeypatch.setenv("REMEDY_DATA_DIR", str(repo / "remedy_data"))

        content, operational, _ = self._changed(repo)
        assert content == ["src/source.py"], "a symlinked data root disabled the guard"
        assert "src/source.py" not in operational

    def test_a_data_root_symlinked_outside_exempts_nothing(self, repo, tmp_path, monkeypatch):
        outside = tmp_path / "outside_data"
        outside.mkdir()
        (repo / "remedy_data").symlink_to(outside, target_is_directory=True)
        monkeypatch.setenv("REMEDY_DATA_DIR", str(repo / "remedy_data"))

        content, _operational, _ = self._changed(repo)
        assert content == ["src/source.py"]

    def test_an_intermediate_symlinked_component_exempts_nothing(
        self, repo, monkeypatch,
    ):
        """`repo/var -> repo/src`, data root `repo/var/data`: the link is on the way in."""
        (repo / "var").symlink_to(repo / "src", target_is_directory=True)
        monkeypatch.setenv("REMEDY_DATA_DIR", str(repo / "var" / "data"))

        content, operational, _ = self._changed(repo)
        assert content == ["src/source.py"]
        assert "src/source.py" not in operational

    def test_an_ordinary_source_file_stays_meaningful(self, repo, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(repo / "remedy_data"))
        (repo / "remedy_data").mkdir()
        content, _o, _n = self._changed(repo)
        assert content == ["src/source.py"]


# ---------------------------------------------------------------------------
# Finding 4 — retry evidence belongs to ONE logical call
# ---------------------------------------------------------------------------

class TestRetryEvidenceIsCallLocal:
    @patch("packages.orchestration.pingpong_loop._time.sleep")
    def test_a_recovered_builder_timeout_never_classifies_a_later_reviewer_failure(
        self, _sleep,
    ):
        """The reviewer's unknown error is not a `provider_timeout` because the BUILDER
        timed out twenty minutes ago."""
        result = PingPongResult(job_id="J1", task_id="T001")

        builder_reasons: list[str] = []
        calls = [0]

        def builder_fn():
            calls[0] += 1
            if calls[0] == 1:
                return _timeout_out()
            return BuilderOutput(summary="recovered", provider="fake")

        _call_with_retry(builder_fn, result=result, role="builder", provider="fake",
                         call_reasons=builder_reasons)
        assert result.retries_used == 1 and builder_reasons, "the builder really retried"

        reviewer_reasons: list[str] = []
        reviewer_out = _call_with_retry(
            lambda: ReviewerOutput(error="something nobody has ever seen", provider="fake"),
            result=result, role="reviewer", provider="fake",
            call_reasons=reviewer_reasons)

        _record_call_failure(result, reviewer_out, role="reviewer", provider="fake",
                             round_no=1, call_reasons=reviewer_reasons)

        record = _postmortems(result)[0]
        assert record["failure_class"] == "unknown"
        assert record["signal_source"] == "none"
        assert record["retry_reasons"] == [], "the builder's retries leaked into the reviewer"
        assert record["retries_used"] == 0
        assert record["role"] == "reviewer"
        # ...and the run-global summary is untouched for compatibility.
        assert result.retries_used == 1 and len(result.retry_reasons) == 1

    @patch("packages.orchestration.pingpong_loop._time.sleep")
    def test_builder_exhaustion_carries_only_builder_reasons(self, _sleep):
        result = PingPongResult(job_id="J1", task_id="T001")
        reasons: list[str] = []
        out = _call_with_retry(lambda: _timeout_out(), result=result, role="builder",
                               provider="fake", call_reasons=reasons)
        _record_call_failure(result, out, role="builder", provider="fake", round_no=1,
                             call_reasons=reasons)

        record = _postmortems(result)[0]
        assert record["retries_used"] == 2
        assert all(r.startswith("builder:") for r in record["retry_reasons"])

    @patch("packages.orchestration.pingpong_loop._time.sleep")
    def test_a_reviewer_parse_retry_shares_the_reviewer_evidence_only(self, _sleep):
        """One logical reviewer call = its attempt plus its single parse retry."""
        result = PingPongResult(job_id="J1", task_id="T001")
        # a builder retry earlier in the same run
        _call_with_retry(lambda: BuilderOutput(summary="ok", provider="fake"),
                         result=result, role="builder", provider="fake")
        result.retry_reasons.append("builder:attempt1:provider_error: TimeoutExpired")
        result.retries_used += 1

        reviewer_reasons: list[str] = []
        _call_with_retry(
            lambda: ReviewerOutput(error="malformed_output: not json",
                                   error_class="parse", provider="fake"),
            result=result, role="reviewer", provider="fake",
            call_reasons=reviewer_reasons)
        retry_out = _call_with_retry(
            lambda: ReviewerOutput(error="malformed_output: still not json",
                                   error_class="parse", provider="fake"),
            result=result, role="reviewer", provider="fake", is_parse_retry=True,
            call_reasons=reviewer_reasons)
        retry_out.parse_retried = True

        _record_call_failure(result, retry_out, role="reviewer", provider="fake",
                             round_no=1, kind="parse-retry",
                             call_reasons=reviewer_reasons)

        record = _postmortems(result)[0]
        assert record["failure_class"] == "parse"
        assert not any("builder:" in r for r in record["retry_reasons"])

    @patch("packages.orchestration.pingpong_loop._time.sleep")
    def test_a_recovered_parse_retry_writes_nothing(self, _sleep):
        result = PingPongResult(job_id="J1", task_id="T001")
        reasons: list[str] = []
        out = _call_with_retry(
            lambda: ReviewerOutput(verdict="pass", summary="ok", provider="fake"),
            result=result, role="reviewer", provider="fake", call_reasons=reasons)
        _record_call_failure(result, out, role="reviewer", provider="fake", round_no=1,
                             call_reasons=reasons)
        assert _postmortems(result) == []


# ---------------------------------------------------------------------------
# Finding 5 — postmortem_paths are unique, relative references
# ---------------------------------------------------------------------------

class TestPostmortemPathReferences:
    def test_a_streamed_record_keeps_its_stream_namespace(self, tmp_path):
        result = PingPongResult(job_id="J1", task_id="T001")
        streams = tmp_path / "streams"
        call_dir = streams / "builder" / "round-01" / "attempt-01"
        call_dir.mkdir(parents=True)

        class _Streaming:
            last_stream_call_dir = str(call_dir)

        out = _timeout_out()
        _record_call_failure(result, out, role="builder", provider="claude-cli",
                             provider_obj=_Streaming(), round_no=1)

        assert result.postmortem_paths == [
            "streams/builder/round-01/attempt-01/postmortem.json"]

    def test_a_fallback_record_keeps_its_call_namespace(self):
        result = PingPongResult(job_id="J1", task_id="T001")
        _record_call_failure(result, _timeout_out(), role="reviewer", provider="fake",
                             round_no=2, kind="parse-retry")
        assert result.postmortem_paths == [
            "calls/reviewer/round-02/parse-retry/postmortem.json"]
        assert not any(p.startswith("/") for p in result.postmortem_paths)


# ---------------------------------------------------------------------------
# Finding 3 — a job-level write failure survives persist + reload, and BLOCKS
# ---------------------------------------------------------------------------

class TestJobPostmortemFailurePersists:
    def test_a_failed_job_record_survives_reload_and_blocks_the_package(
        self, demo_repo, tmp_path, monkeypatch,
    ):
        from packages.orchestration import pingpong_job as PJ
        from packages.orchestration.final_verifier import build_final_verifier_report
        from packages.orchestration.job_evidence import export_job_evidence

        def lock(job):
            raise WorktreeLockError("job worktree is locked by run r9")

        def refuse(directory, record, *, root=None):
            raise FP.PostmortemError(
                f"forced fail: read-only: {tmp_path}/pingpong_runs/r1/postmortem.json")

        monkeypatch.setattr(PJ, "_acquire_job_workspace", lock)
        monkeypatch.setattr(FP, "write_postmortem", refuse)

        job = PJ.JobPlan(repo_path=str(demo_repo), job_title="locked + unwritable",
                         tasks=[PJ.TaskEntry(task_id="T001", title="t", body="b")])
        PJ._persist_job(job)
        PJ.run_job(job.job_id)

        # the process/reload boundary the reviewed build lost the failure across
        reloaded = PJ.load_job_plan(job.job_id)
        assert reloaded.status == "blocked"
        assert "workspace_creation_failed" in reloaded.error, "the PRIMARY failure survives"
        assert "forced fail" in reloaded.postmortem_error, "the recording failure survives"
        assert "read-only" in reloaded.postmortem_error
        assert str(tmp_path) not in reloaded.postmortem_error, "an absolute path leaked"
        assert reloaded.tasks[0].status == "pending"

        out = tmp_path / "evidence"
        export_job_evidence(job.job_id, str(out))

        integrity = json.loads((out / "postmortem_integrity.json").read_text())
        assert integrity["ok"] is False
        assert integrity["failures"][0]["scope"] == "job"
        assert "forced fail" in integrity["failures"][0]["error"]

        report = build_final_verifier_report(str(out))
        assert report["postmortem_integrity_blocked"] is True
        assert report["verdict"] == "BLOCKED"
        assert not (out / "task_runs" / "T001" / "postmortem.json").exists(), (
            "a pending task must not get a fake record")

    def test_an_old_job_file_without_the_postmortem_block_still_loads(
        self, demo_repo, monkeypatch,
    ):
        from packages.orchestration import pingpong_job as PJ
        from packages.orchestration.data_paths import job_dir

        job = PJ.JobPlan(repo_path=str(demo_repo), job_title="old",
                         tasks=[PJ.TaskEntry(task_id="T001", title="t", body="b")])
        PJ._persist_job(job)

        path = job_dir(job.job_id) / "job.json"
        data = json.loads(path.read_text())
        data.pop("postmortem", None)           # a job written before F010 existed
        path.write_text(json.dumps(data, indent=2))

        reloaded = PJ.load_job_plan(job.job_id)
        assert reloaded is not None
        assert reloaded.postmortem_path == "" and reloaded.postmortem_error == ""


# ---------------------------------------------------------------------------
# Finding 2 (round 3) — relative and symlink-addressed data roots
# ---------------------------------------------------------------------------

class TestDataRootAddressing:
    """`REMEDY_DATA_DIR=remedy_data` is an ordinary configuration.

    The reviewed build compared that relative string against an absolute repository path,
    concluded "not inside", and then reported Remedy's own post-mortem as a builder mutation
    of the target repo.
    """

    @pytest.fixture
    def repo(self, tmp_path) -> Path:
        repo = tmp_path / "repo"
        (repo / "src").mkdir(parents=True)
        (repo / "src" / "source.py").write_text("original\n")
        return repo

    def _run(self, addressed_repo: Path, real_repo: Path):
        from packages.orchestration.pingpong_loop import (
            _classify_target_changes,
            _snapshot_target,
        )
        before = _snapshot_target(addressed_repo)
        (real_repo / "remedy_data" / "runs").mkdir(parents=True, exist_ok=True)
        (real_repo / "remedy_data" / "runs" / "postmortem.json").write_text("{}\n")
        (real_repo / "src" / "source.py").write_text("mutated\n")
        return _classify_target_changes(addressed_repo, before)

    def test_a_relative_data_dir_is_operational(self, repo, monkeypatch):
        monkeypatch.chdir(repo)
        monkeypatch.setenv("REMEDY_DATA_DIR", "remedy_data")
        content, operational, _ = self._run(repo, repo)
        assert content == ["src/source.py"]
        assert operational == ["remedy_data/runs/postmortem.json"]

    def test_a_dot_relative_data_dir_is_operational(self, repo, monkeypatch):
        monkeypatch.chdir(repo)
        monkeypatch.setenv("REMEDY_DATA_DIR", "./remedy_data")
        content, operational, _ = self._run(repo, repo)
        assert content == ["src/source.py"]
        assert operational == ["remedy_data/runs/postmortem.json"]

    def test_an_absolute_data_dir_is_operational(self, repo, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(repo / "remedy_data"))
        content, operational, _ = self._run(repo, repo)
        assert content == ["src/source.py"]
        assert operational == ["remedy_data/runs/postmortem.json"]

    def test_the_repository_addressed_through_a_symlink_still_works(
        self, repo, tmp_path, monkeypatch,
    ):
        link = tmp_path / "repo-link"
        link.symlink_to(repo, target_is_directory=True)
        monkeypatch.setenv("REMEDY_DATA_DIR", str(link / "remedy_data"))

        content, operational, _ = self._run(link, repo)
        assert content == ["src/source.py"]
        assert operational == ["remedy_data/runs/postmortem.json"]

    def test_the_repository_addressed_by_its_real_path_still_works(
        self, repo, tmp_path, monkeypatch,
    ):
        link = tmp_path / "repo-link"
        link.symlink_to(repo, target_is_directory=True)
        monkeypatch.setenv("REMEDY_DATA_DIR", str(link / "remedy_data"))

        content, operational, _ = self._run(repo, repo)      # addressed really this time
        assert content == ["src/source.py"]
        assert operational == ["remedy_data/runs/postmortem.json"]

    @pytest.mark.parametrize("spelling", ["final", "intermediate"])
    def test_a_data_root_symlinked_into_the_source_tree_exempts_nothing(
        self, repo, monkeypatch, spelling,
    ):
        if spelling == "final":
            (repo / "remedy_data").symlink_to(repo / "src", target_is_directory=True)
            monkeypatch.setenv("REMEDY_DATA_DIR", str(repo / "remedy_data"))
        else:
            (repo / "var").symlink_to(repo / "src", target_is_directory=True)
            monkeypatch.setenv("REMEDY_DATA_DIR", str(repo / "var" / "data"))

        from packages.orchestration.pingpong_loop import _is_remedy_data_path
        assert _is_remedy_data_path(repo, "src/source.py") is False

    @pytest.mark.parametrize("where", ["equal", "parent", "sibling", "outside"])
    def test_a_data_root_that_is_not_strictly_inside_exempts_nothing(
        self, repo, tmp_path, monkeypatch, where,
    ):
        target = {
            "equal": repo,
            "parent": repo.parent,
            "sibling": tmp_path / "sibling",
            "outside": tmp_path.parent / "outside-data",
        }[where]
        monkeypatch.setenv("REMEDY_DATA_DIR", str(target))
        from packages.orchestration.pingpong_loop import _is_remedy_data_path
        assert _is_remedy_data_path(repo, "src/source.py") is False
