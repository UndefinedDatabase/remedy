"""F011 T002 — stopping a real job, at a real safe point.

Every test here drives the actual `run_job` caller loop and the actual ping-pong loop with
deterministic fake providers. The stop is requested the way an operator requests it — by
writing the control file — from inside a provider call, so the question each test really
asks is: what did the runner do with a call that was ALREADY IN FLIGHT when the request
landed? The answer must always be: it finished it, kept its evidence, and started nothing.

No provider process, no network, no database, no signal, no thread. Deliberate stop fixtures
live only in pytest's temporary directories.
"""
from __future__ import annotations

import contextlib
import json
import os
import subprocess
import sys
import textwrap
from pathlib import Path

import psutil
import pytest

from packages.orchestration.data_paths import job_record_path, pingpong_runs_dir
from packages.orchestration.pingpong_job import (
    JOB_COMPLETED,
    JOB_STOPPED,
    STOP_POSTMORTEM_SUBDIR,
    TASK_APPLIED,
    TASK_PENDING,
    job_evidence_dir,
    load_job_plan,
    parse_job_file,
    run_job,
)
from packages.orchestration.pingpong_provider import FakeProvider
from packages.orchestration.safe_points import (
    request_stop,
    stop_archive_dir,
    stop_requested,
    stop_status,
)

_ONE_TASK_JOB = """\
# Job: Stop Test

## Task 1
Add a helper module.

Acceptance:
- module exists
"""

_TWO_TASK_JOB = """\
# Job: Stop Test

## Task 1
Add a helper module.

Acceptance:
- module exists

## Task 2
Add a second module.

Acceptance:
- module exists
"""

_THREE_TASK_JOB = """\
# Job: Stop Acceptance

## Task 1
Add module one.

Acceptance:
- module exists

## Task 2
Add module two.

Acceptance:
- module exists

## Task 3
Add module three.

Acceptance:
- module exists
"""


@pytest.fixture
def isolate_data_root(tmp_path: Path, monkeypatch) -> Path:
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


@pytest.fixture
def demo_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "README.md").write_text("# demo\n")
    return repo


class CountingProvider(FakeProvider):
    """A fake provider that counts its calls — and can stop the job from inside one.

    ``stop_on_build`` / ``stop_on_review`` fire while the call is IN FLIGHT: the control
    file appears, and then the call returns normally. That is precisely the race the
    feature exists to survive.
    """

    def __init__(self, *, job_id: str = "", stop_on_build: int = 0,
                 stop_on_review: int = 0, reason: str = "operator requested stop",
                 **kwargs) -> None:
        super().__init__(**kwargs)
        self.job_id = job_id
        self.stop_on_build = stop_on_build
        self.stop_on_review = stop_on_review
        self.reason = reason
        self.build_calls = 0
        self.review_calls = 0

    def build(self, prompt, **kwargs):
        self.build_calls += 1
        if self.stop_on_build and self.build_calls == self.stop_on_build:
            request_stop(self.job_id, self.reason, "test")
        return super().build(prompt, **kwargs)

    def review(self, prompt, **kwargs):
        self.review_calls += 1
        out = super().review(prompt, **kwargs)
        if self.stop_on_review and self.review_calls == self.stop_on_review:
            request_stop(self.job_id, self.reason, "test")
        return out


def _pass_provider(**kw):
    return CountingProvider(pass_on_round=1, fail_on_round=99, **kw)


def _stop_episodes(job_id: str) -> list[Path]:
    root = job_evidence_dir(job_id) / STOP_POSTMORTEM_SUBDIR
    return sorted(root.iterdir()) if root.is_dir() else []


def _events(data_root: Path, job_id: str, event: str) -> list[dict]:
    runs = data_root / "runs" / job_id
    out: list[dict] = []
    for f in sorted(runs.glob("*.jsonl")) if runs.is_dir() else []:
        for line in f.read_text().splitlines():
            if line.strip():
                raw = json.loads(line)
                if raw.get("event") == event:
                    out.append(raw)
    return out


class TestStopBeforeTheFirstTask:
    def test_a_stop_requested_while_the_job_is_idle_costs_zero_provider_calls(
            self, isolate_data_root, demo_repo):
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        builder = _pass_provider()
        reviewer = _pass_provider()

        request_stop(job.job_id, "operator requested stop", "cli")
        stopped = run_job(job.job_id, builder_provider=builder,
                          reviewer_provider=reviewer, repair_rounds=0)

        assert stopped.status == JOB_STOPPED
        assert builder.build_calls == 0 and reviewer.review_calls == 0
        assert all(t.status == TASK_PENDING for t in stopped.tasks)

        # The episode is complete: consumed, archived, explained, and in the ledger.
        assert stop_requested(job.job_id) is None
        assert stop_status(job.job_id).consumed_count == 1
        assert (stop_archive_dir(job.job_id)
                / f"{stopped.stop_request_id}.json").is_file()
        assert len(_stop_episodes(job.job_id)) == 1
        assert len(_events(isolate_data_root, job.job_id, "job_stopped")) == 1

    def test_the_stopped_job_reloads_from_disk_as_stopped(
            self, isolate_data_root, demo_repo):
        job = parse_job_file(_ONE_TASK_JOB, str(demo_repo))
        request_stop(job.job_id, "later", "cli")
        run_job(job.job_id, builder_provider=_pass_provider(),
                reviewer_provider=_pass_provider(), repair_rounds=0)

        reloaded = load_job_plan(job.job_id)
        assert reloaded.status == JOB_STOPPED
        assert reloaded.stop_request_id and reloaded.stop_reason == "later"
        assert reloaded.stop_source == "cli" and reloaded.stopped_at
        assert reloaded.stop_postmortem_path.startswith(STOP_POSTMORTEM_SUBDIR)
        assert not reloaded.stop_error and not reloaded.stop_event_error


class TestStopDuringAProviderCall:
    def test_a_stop_during_the_builder_call_lets_that_call_finish_and_starts_no_reviewer(
            self, isolate_data_root, demo_repo):
        job = parse_job_file(_ONE_TASK_JOB, str(demo_repo))
        builder = _pass_provider(job_id=job.job_id, stop_on_build=1)
        reviewer = _pass_provider()

        stopped = run_job(job.job_id, builder_provider=builder,
                          reviewer_provider=reviewer, repair_rounds=0)

        assert builder.build_calls == 1          # the call in flight was NOT killed
        assert reviewer.review_calls == 0        # ...and the next one never began
        assert stopped.status == JOB_STOPPED
        assert stopped.tasks[0].status == TASK_PENDING
        assert stopped.tasks[0].final_status == "stopped"
        assert len(_stop_episodes(job.job_id)) == 1

    def test_a_stop_during_the_reviewer_call_starts_no_repair_round(
            self, isolate_data_root, demo_repo):
        job = parse_job_file(_ONE_TASK_JOB, str(demo_repo))
        # The default fake reviewer finds issues in round 1, so round 2 would be a repair.
        builder = CountingProvider(job_id=job.job_id)
        reviewer = CountingProvider(job_id=job.job_id, stop_on_review=1)

        stopped = run_job(job.job_id, builder_provider=builder,
                          reviewer_provider=reviewer, repair_rounds=2)

        assert reviewer.review_calls == 1        # the reviewer call finished
        assert builder.build_calls == 1          # the repair Builder call never started
        assert stopped.status == JOB_STOPPED
        assert stopped.tasks[0].status == TASK_PENDING

    def test_a_stop_before_the_parse_retry_leaves_the_malformed_response_alone(
            self, isolate_data_root, demo_repo):
        job = parse_job_file(_ONE_TASK_JOB, str(demo_repo))
        builder = CountingProvider(job_id=job.job_id)
        reviewer = CountingProvider(job_id=job.job_id, stop_on_review=1,
                                    malformed_review=True)

        stopped = run_job(job.job_id, builder_provider=builder,
                          reviewer_provider=reviewer, repair_rounds=0)

        assert reviewer.review_calls == 1        # the bounded parse retry never ran
        assert stopped.status == JOB_STOPPED
        assert stopped.tasks[0].status == TASK_PENDING

        run = json.loads((pingpong_runs_dir()
                          / f"{stopped.tasks[0].run_id}.json").read_text()) \
            if (pingpong_runs_dir()
                / f"{stopped.tasks[0].run_id}.json").is_file() else None
        if run is not None:
            assert run["reviewer_parse_retry_count"] == 0

    def test_a_stop_is_never_dressed_up_as_a_failure(self, isolate_data_root, demo_repo):
        job = parse_job_file(_ONE_TASK_JOB, str(demo_repo))
        builder = _pass_provider(job_id=job.job_id, stop_on_build=1)
        stopped = run_job(job.job_id, builder_provider=builder,
                          reviewer_provider=_pass_provider(), repair_rounds=0)

        assert stopped.status == JOB_STOPPED and not stopped.error
        assert stopped.tasks[0].final_status == "stopped"
        assert stopped.tasks[0].error == ""

        record = json.loads(
            (_stop_episodes(job.job_id)[0] / "postmortem.json").read_text())
        assert record["failure_class"] == "stopped"
        assert record["scope"] == "job"
        assert record["signal_source"] == "terminal_status"


class TestStopBetweenTasks:
    def test_an_applied_task_stays_applied_and_the_next_one_never_starts(
            self, isolate_data_root, demo_repo):
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        # The stop lands while task 1's reviewer call is in flight; the reviewer PASSES, so
        # task 1 reaches its apply boundary and is durable. The stop takes effect before
        # task 2 is dispatched.
        builder = _pass_provider(job_id=job.job_id)
        reviewer = _pass_provider(job_id=job.job_id, stop_on_review=1)

        stopped = run_job(job.job_id, builder_provider=builder,
                          reviewer_provider=reviewer, repair_rounds=0)

        assert stopped.status == JOB_STOPPED
        assert stopped.tasks[0].status == TASK_APPLIED   # durable work is never rolled back
        assert stopped.tasks[1].status == TASK_PENDING
        assert builder.build_calls == 1                  # task 2's Builder never ran


class TestResume:
    def test_a_stopped_job_resumes_at_the_first_pending_task(
            self, isolate_data_root, demo_repo):
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        builder = _pass_provider(job_id=job.job_id)
        reviewer = _pass_provider(job_id=job.job_id, stop_on_review=1)
        stopped = run_job(job.job_id, builder_provider=builder,
                          reviewer_provider=reviewer, repair_rounds=0)
        assert stopped.status == JOB_STOPPED
        first_run_id = stopped.tasks[0].run_id

        # No new request: the resume just continues.
        resumed = run_job(job.job_id, builder_provider=_pass_provider(),
                          reviewer_provider=_pass_provider(), repair_rounds=0)

        assert resumed.status == JOB_COMPLETED
        assert resumed.tasks[0].status == TASK_APPLIED
        assert resumed.tasks[0].run_id == first_run_id     # task 1 was NOT rerun
        assert resumed.tasks[1].status == TASK_APPLIED

    def test_stop_resume_stop_is_two_distinct_episodes(
            self, isolate_data_root, demo_repo):
        job = parse_job_file(_THREE_TASK_JOB, str(demo_repo))

        first = run_job(
            job.job_id,
            builder_provider=_pass_provider(job_id=job.job_id),
            reviewer_provider=_pass_provider(job_id=job.job_id, stop_on_review=1),
            repair_rounds=0)
        assert first.status == JOB_STOPPED

        second = run_job(
            job.job_id,
            builder_provider=_pass_provider(job_id=job.job_id),
            reviewer_provider=_pass_provider(job_id=job.job_id, stop_on_review=1,
                                             reason="second stop"),
            repair_rounds=0)
        assert second.status == JOB_STOPPED
        assert second.stop_request_id != first.stop_request_id
        assert second.stop_reason == "second stop"

        assert stop_status(job.job_id).consumed_count == 2
        assert len(list(stop_archive_dir(job.job_id).glob("*.json"))) == 2
        assert len(_stop_episodes(job.job_id)) == 2       # neither overwrote the other
        assert len(_events(isolate_data_root, job.job_id, "job_stopped")) == 2

        # Two tasks are durably applied by now; the third is still waiting.
        assert [t.status for t in second.tasks] == [
            TASK_APPLIED, TASK_APPLIED, TASK_PENDING]


class TestARecordingFailureIsNeverSilent:
    def test_an_unwritable_stop_postmortem_blocks_instead_of_faking_a_clean_stop(
            self, isolate_data_root, demo_repo, monkeypatch):
        job = parse_job_file(_ONE_TASK_JOB, str(demo_repo))

        import packages.orchestration.failure_postmortem as fp

        def _boom(*a, **k):
            raise OSError("disk went away")

        monkeypatch.setattr(fp, "write_postmortem", _boom)

        stopped = run_job(job.job_id, builder_provider=_pass_provider(
                              job_id=job.job_id, stop_on_build=1),
                          reviewer_provider=_pass_provider(), repair_rounds=0)

        # The primary stop survives — as a PENDING request, not as a job that claims to be
        # cleanly stopped with no record of why. The recording failure is durable.
        assert stopped.status != JOB_STOPPED          # no false clean checkpoint
        assert stopped.stop_request_id
        assert "stop_postmortem_write_failed" in stopped.stop_error
        assert not stopped.stop_postmortem_path
        assert load_job_plan(job.job_id).stop_error == stopped.stop_error
        assert stop_requested(job.job_id) is not None

        # ...and the evidence export turns it into a BLOCKING integrity failure.
        from packages.orchestration.job_evidence import export_job_evidence

        out = export_job_evidence(job.job_id, str(demo_repo.parent / "bundle"))
        integrity = json.loads(
            (Path(out["out_dir"]) / "postmortem_integrity.json").read_text())
        assert integrity["ok"] is False
        assert any("stop_postmortem_write_failed" in f["error"]
                   for f in integrity["failures"])


class TestTheEvidenceExportCarriesTheStop:
    def test_the_bundle_contains_the_stop_record_and_no_absolute_path(
            self, isolate_data_root, demo_repo):
        job = parse_job_file(_ONE_TASK_JOB, str(demo_repo))
        stopped = run_job(job.job_id,
                          builder_provider=_pass_provider(job_id=job.job_id,
                                                          stop_on_build=1),
                          reviewer_provider=_pass_provider(), repair_rounds=0)

        from packages.orchestration.job_evidence import export_job_evidence

        out = export_job_evidence(job.job_id, str(demo_repo.parent / "bundle"))
        base = Path(out["out_dir"])
        record_path = (base / STOP_POSTMORTEM_SUBDIR / stopped.stop_request_id
                       / "postmortem.json")
        assert record_path.is_file()

        record = json.loads(record_path.read_text())
        assert record["failure_class"] == "stopped"
        raw = record_path.read_text()
        assert str(demo_repo) not in raw and str(isolate_data_root) not in raw

        integrity = json.loads((base / "postmortem_integrity.json").read_text())
        assert integrity["ok"] is True and integrity["failures"] == []

    def test_stats_count_the_stop_once_as_a_job_scope_failure(
            self, isolate_data_root, demo_repo):
        job = parse_job_file(_ONE_TASK_JOB, str(demo_repo))
        run_job(job.job_id,
                builder_provider=_pass_provider(job_id=job.job_id, stop_on_build=1),
                reviewer_provider=_pass_provider(), repair_rounds=0)

        from packages.orchestration.failure_stats import collect_failures
        from packages.orchestration.job_evidence import export_job_evidence

        exports = isolate_data_root / "evidence_exports"
        export_job_evidence(job.job_id, str(exports / job.job_id))

        stats = collect_failures(root=exports)
        assert stats["counts_by_class"]["stopped"] == 1
        assert stats["counts_by_scope"]["job"] == 1
        assert collect_failures(root=exports, job=job.job_id)["total_postmortems"] == 1


# ---------------------------------------------------------------------------
# Acceptance: a real runner process, stopped from a second process
# ---------------------------------------------------------------------------

_RUNNER = """\
import sys, time
from pathlib import Path
sys.path.insert(0, {repo!r})
from packages.orchestration.pingpong_job import parse_job_file, run_job
from packages.orchestration.pingpong_provider import FakeProvider


class SlowProvider(FakeProvider):
    '''A provider whose calls take real time, like the real ones do. Nothing here knows
    anything about the stop: the runner has to notice it on its own.'''

    def build(self, prompt, **kwargs):
        time.sleep(1.0)
        return super().build(prompt, **kwargs)

    def review(self, prompt, **kwargs):
        time.sleep(1.0)
        return super().review(prompt, **kwargs)


job = parse_job_file(Path({job_file!r}).read_text(), {target!r})
Path({idfile!r}).write_text(job.job_id)


def provider():
    return SlowProvider(pass_on_round=1, fail_on_round=99)


final = run_job(job.job_id, builder_provider=provider(),
                reviewer_provider=provider(), repair_rounds=0)
print("FINAL:" + final.status, flush=True)
"""


def _test_owned_children(baseline_pids: set[int], tmp_path: Path) -> list[psutil.Process]:
    """Children this TEST is responsible for — nobody else's.

    The reviewed test asserted ``psutil.Process().children(recursive=True) == []``, which is
    a claim about the whole pytest process. On the external review host that process already
    had an unrelated child (`artifact_tool_rpc_daemon-bun`), so a correct Remedy runner was
    reported as a leak. Scope it: a child counts only if it did not exist before we started
    AND it is ours — running from, or pointing at, this test's tmp_path.
    """
    owned: list[psutil.Process] = []
    for child in psutil.Process().children(recursive=True):
        try:
            if child.pid in baseline_pids:
                continue
            if child.status() == psutil.STATUS_ZOMBIE:
                continue                        # reaped, or about to be: not a live leak
            marker = str(tmp_path)
            cwd = ""
            with contextlib.suppress(psutil.Error):
                cwd = child.cwd() or ""
            cmdline = ""
            with contextlib.suppress(psutil.Error):
                cmdline = " ".join(child.cmdline())
            if marker in cwd or marker in cmdline:
                owned.append(child)
        except psutil.NoSuchProcess:
            continue
    return owned


@pytest.mark.subprocess
class TestALiveRunnerStopsCleanly:
    def test_a_three_task_job_stopped_after_task_one_exits_clean_with_no_leftovers(
            self, tmp_path):
        repo_root = Path(__file__).resolve().parents[2]
        target = tmp_path / "repo"
        target.mkdir()
        (target / "README.md").write_text("# demo\n")
        data_dir = tmp_path / "remedy_data"
        data_dir.mkdir()

        job_file = tmp_path / "job.md"
        job_file.write_text(_THREE_TASK_JOB)
        idfile = tmp_path / "job_id.txt"
        script = tmp_path / "runner.py"
        script.write_text(textwrap.dedent(_RUNNER).format(
            repo=str(repo_root), job_file=str(job_file), target=str(target),
            idfile=str(idfile)))

        env = dict(os.environ, REMEDY_DATA_DIR=str(data_dir), PYTHONPATH=str(repo_root))
        # Whatever this process already had a child of (a tool daemon, an IDE helper) is not
        # ours and never becomes ours.
        baseline = {c.pid for c in psutil.Process().children(recursive=True)}
        proc = subprocess.Popen([sys.executable, str(script)], env=env,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True)
        try:
            # Wait for the runner to finish task 1, then stop it from HERE — a second
            # process, exactly like the operator's second terminal.
            import time

            deadline = time.monotonic() + 60.0
            job_id = ""
            while time.monotonic() < deadline:
                if idfile.is_file() and idfile.read_text().strip():
                    job_id = idfile.read_text().strip()
                    job_json = job_record_path(job_id, data_dir)
                    if job_json.is_file():
                        data = json.loads(job_json.read_text() or "{}")
                        statuses = [t["status"] for t in data.get("tasks", [])]
                        if statuses and statuses[0] == "applied_to_job_workspace":
                            break
                assert proc.poll() is None, "the runner exited before task 1 completed"
                time.sleep(0.05)
            else:
                pytest.fail("task 1 never completed within 60s")

            # THIS process is the operator's second terminal: it writes the control file
            # while the runner is mid-call in task 2.
            monkeypatch_env = os.environ.get("REMEDY_DATA_DIR")
            os.environ["REMEDY_DATA_DIR"] = str(data_dir)
            try:
                request_stop(job_id, "operator requested stop", "cli")
            finally:
                if monkeypatch_env is None:
                    os.environ.pop("REMEDY_DATA_DIR", None)
                else:
                    os.environ["REMEDY_DATA_DIR"] = monkeypatch_env

            out, err = proc.communicate(timeout=180)
            assert proc.returncode == 0, f"runner exited {proc.returncode}: {err}"
            assert "FINAL:stopped" in out, out
        finally:
            if proc.poll() is None:                     # never leave one behind
                proc.kill()
                proc.wait(timeout=30)

        data = json.loads(job_record_path(job_id, data_dir).read_text())
        statuses = [t["status"] for t in data["tasks"]]
        assert data["status"] == "stopped"
        assert statuses.count("applied_to_job_workspace") == 1
        assert statuses.count("pending") == 2

        assert not (data_dir / "control" / "jobs" / job_id / "stop.json").exists()
        archive = data_dir / "control" / "jobs" / job_id / "archive"
        assert len(list(archive.glob("*.json"))) == 1

        episodes = list((data_dir / "jobs" / job_id / "evidence"
                         / STOP_POSTMORTEM_SUBDIR).iterdir())
        assert len(episodes) == 1
        assert (episodes[0] / "postmortem.json").is_file()

        events = [json.loads(line)
                  for f in (data_dir / "runs" / job_id).glob("*.jsonl")
                  for line in f.read_text().splitlines() if line.strip()]
        assert len([e for e in events if e["event"] == "job_stopped"]) == 1

        # No leftover process: the runner owned everything it started. Scoped to the
        # processes THIS test created — an unrelated pre-existing child of the pytest
        # process is not a Remedy leak, and pretending otherwise made a correct runner
        # look broken on the review host.
        assert not psutil.pid_exists(proc.pid) or \
            psutil.Process(proc.pid).status() == psutil.STATUS_ZOMBIE
        assert _test_owned_children(baseline, tmp_path) == []


# ---------------------------------------------------------------------------
# Hardening round 1 — the durable stop transaction
# ---------------------------------------------------------------------------

from packages.orchestration.pingpong_job import (  # noqa: E402
    JOB_BLOCKED,
)
from packages.orchestration.safe_points import (  # noqa: E402
    archived_signals,
)


class TestAPreExistingStopBeatsEveryKindOfWork:
    def test_a_pending_stop_is_honoured_before_the_workspace_is_even_acquired(
            self, isolate_data_root, demo_repo, monkeypatch):
        """The reviewed build acquired the job worktree FIRST. When acquisition failed, the
        job came out `blocked` with the operator's stop still sitting on disk, unread."""
        import packages.orchestration.pingpong_job as PJ

        acquisitions: list[str] = []

        def _explode(job):
            acquisitions.append(job.job_id)
            raise RuntimeError("worktree lock held by another process")

        monkeypatch.setattr(PJ, "_acquire_job_workspace", _explode)

        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        request_stop(job.job_id, "operator requested stop", "cli")

        builder = _pass_provider()
        stopped = run_job(job.job_id, builder_provider=builder,
                          reviewer_provider=_pass_provider(), repair_rounds=0)

        assert acquisitions == [], "the workspace was acquired despite a pending stop"
        assert stopped.status == JOB_STOPPED and stopped.status != JOB_BLOCKED
        assert builder.build_calls == 0
        assert all(t.status == TASK_PENDING for t in stopped.tasks)
        assert stop_requested(job.job_id) is None
        assert len(_stop_episodes(job.job_id)) == 1
        assert len(_events(isolate_data_root, job.job_id, "job_stopped")) == 1


class TestTheStopIsNeverLost:
    def _stopped_job(self, demo_repo):
        job = parse_job_file(_ONE_TASK_JOB, str(demo_repo))
        request_stop(job.job_id, "operator requested stop", "cli")
        return job

    def test_a_failing_job_persist_leaves_the_request_pending(
            self, isolate_data_root, demo_repo, monkeypatch):
        """The reviewed build deleted `stop.json` BEFORE persisting the job. A persist
        failure then left `planned` on disk and no request anywhere: the stop was gone."""
        import packages.orchestration.pingpong_job as PJ

        job = self._stopped_job(demo_repo)
        calls = {"n": 0}
        real_persist = PJ._persist_job

        def _fail_on_the_stopped_write(j):
            if j.status == JOB_STOPPED:
                calls["n"] += 1
                raise OSError("disk full")
            return real_persist(j)

        with monkeypatch.context() as m:
            m.setattr(PJ, "_persist_job", _fail_on_the_stopped_write)
            with pytest.raises(OSError):
                run_job(job.job_id, builder_provider=_pass_provider(),
                        reviewer_provider=_pass_provider(), repair_rounds=0)

        assert calls["n"] == 1
        on_disk = load_job_plan(job.job_id)
        assert on_disk.status != JOB_STOPPED          # nothing lied about being stopped
        pending = stop_requested(job.job_id)
        assert pending is not None                    # ...and the request is still there

        # The retry completes the SAME episode — exactly once, not twice.
        builder = _pass_provider()
        stopped = run_job(job.job_id, builder_provider=builder,
                          reviewer_provider=_pass_provider(), repair_rounds=0)

        assert stopped.status == JOB_STOPPED
        assert stopped.stop_request_id == pending.request_id
        assert builder.build_calls == 0
        assert len(archived_signals(job.job_id)) == 1
        assert len(_stop_episodes(job.job_id)) == 1
        assert len(_events(isolate_data_root, job.job_id, "job_stopped")) == 1
        assert stop_requested(job.job_id) is None

    def test_an_archive_failure_creates_no_consumed_episode(
            self, isolate_data_root, demo_repo, monkeypatch):
        """An unarchived request is not a consumed episode. The reviewed build stopped the
        job anyway, wrote the event and the post-mortem, and recorded an empty archive
        reference — a clean-looking stop with no history behind it."""
        import packages.orchestration.safe_points as SP

        job = self._stopped_job(demo_repo)
        pending = stop_requested(job.job_id)

        def _boom(*a, **k):
            raise SP.StopControlError("the archive area is unwritable")

        builder = _pass_provider()
        with monkeypatch.context() as m:
            m.setattr(SP, "archive_stop", _boom)
            result = run_job(job.job_id, builder_provider=builder,
                             reviewer_provider=_pass_provider(), repair_rounds=0)

        assert builder.build_calls == 0               # no work began: fail-safe
        assert result.status != JOB_STOPPED           # no false clean episode
        assert "stop_archive_failed" in result.stop_error
        assert stop_requested(job.job_id) == pending  # the request is still pending
        assert _events(isolate_data_root, job.job_id, "job_stopped") == []
        assert _stop_episodes(job.job_id) == []
        assert archived_signals(job.job_id) == []

        # ...and the recording failure blocks the package rather than passing quietly.
        from packages.orchestration.job_evidence import export_job_evidence

        out = export_job_evidence(job.job_id, str(demo_repo.parent / "blocked_bundle"))
        integrity = json.loads(
            (Path(out["out_dir"]) / "postmortem_integrity.json").read_text())
        assert integrity["ok"] is False

        # Restore the archive and finish: ONE of everything, for the same request id.
        stopped = run_job(job.job_id, builder_provider=_pass_provider(),
                          reviewer_provider=_pass_provider(), repair_rounds=0)
        assert stopped.status == JOB_STOPPED
        assert stopped.stop_request_id == pending.request_id
        assert len(archived_signals(job.job_id)) == 1
        assert len(_stop_episodes(job.job_id)) == 1
        assert len(_events(isolate_data_root, job.job_id, "job_stopped")) == 1
        assert not stopped.stop_error

    @pytest.mark.parametrize("crash_after", ["archive", "postmortem", "event", "persist"])
    def test_every_crash_window_converges_to_exactly_one_episode(
            self, isolate_data_root, demo_repo, monkeypatch, crash_after):
        """Kill the finalization at each step in turn, then run again. Whatever happened,
        the result must be one archive, one post-mortem, one event — for the one request."""
        import packages.orchestration.pingpong_job as PJ
        import packages.orchestration.safe_points as SP

        job = self._stopped_job(demo_repo)
        pending = stop_requested(job.job_id)

        real_archive = SP.archive_stop
        real_pm = PJ._write_stop_postmortem
        real_event = PJ._append_job_stopped_event
        real_persist = PJ._persist_job

        class _Crash(RuntimeError):
            pass

        def _after(step, fn):
            def _wrapped(*a, **k):
                out = fn(*a, **k)
                raise _Crash(step)
            return _wrapped

        def _persist_then_crash(j):
            real_persist(j)
            if j.status == JOB_STOPPED:
                raise _Crash("persist")

        with monkeypatch.context() as m:
            if crash_after == "archive":
                m.setattr(SP, "archive_stop", _after("archive", real_archive))
            elif crash_after == "postmortem":
                m.setattr(PJ, "_write_stop_postmortem", _after("pm", real_pm))
            elif crash_after == "event":
                m.setattr(PJ, "_append_job_stopped_event", _after("ev", real_event))
            else:
                m.setattr(PJ, "_persist_job", _persist_then_crash)

            # The archive-step crash is absorbed by the fail-safe path (the request stays
            # pending and the runner stops doing work); the later steps propagate.
            with contextlib.suppress(_Crash):
                run_job(job.job_id, builder_provider=_pass_provider(),
                        reviewer_provider=_pass_provider(), repair_rounds=0)
            assert load_job_plan(job.job_id).status != JOB_COMPLETED

        # Replay: the runner sees the pending request (or the stopped job) and finishes.
        stopped = run_job(job.job_id, builder_provider=_pass_provider(),
                          reviewer_provider=_pass_provider(), repair_rounds=0)

        assert stopped.status == JOB_STOPPED
        assert stopped.stop_request_id == pending.request_id
        assert len(archived_signals(job.job_id)) == 1
        assert len(_stop_episodes(job.job_id)) == 1
        assert len(_events(isolate_data_root, job.job_id, "job_stopped")) == 1
        assert stop_requested(job.job_id) is None

    def test_a_failed_acknowledgement_leaves_a_stopped_job_and_no_duplicates(
            self, isolate_data_root, demo_repo, monkeypatch):
        import packages.orchestration.safe_points as SP

        job = self._stopped_job(demo_repo)
        pending = stop_requested(job.job_id)
        with monkeypatch.context() as m:
            m.setattr(SP, "acknowledge_stop",
                      lambda *a, **k: (_ for _ in ()).throw(OSError("read-only")))
            stopped = run_job(job.job_id, builder_provider=_pass_provider(),
                              reviewer_provider=_pass_provider(), repair_rounds=0)

        assert stopped.status == JOB_STOPPED          # the job IS stopped and durable
        assert "stop_acknowledge_failed" in stopped.stop_error
        assert stop_requested(job.job_id) == pending  # only the tidying failed

        again = run_job(job.job_id, builder_provider=_pass_provider(),
                        reviewer_provider=_pass_provider(), repair_rounds=0)
        assert again.status == JOB_STOPPED
        assert stop_requested(job.job_id) is None     # now acknowledged
        assert len(_events(isolate_data_root, job.job_id, "job_stopped")) == 1
        assert len(_stop_episodes(job.job_id)) == 1


class TestTheRunRecordCarriesTheStop:
    def test_a_stopped_run_json_has_the_safe_stop_block(self, isolate_data_root,
                                                        demo_repo):
        from packages.orchestration.pingpong_loop import load_run

        job = parse_job_file(_ONE_TASK_JOB, str(demo_repo))
        stopped = run_job(job.job_id,
                          builder_provider=_pass_provider(job_id=job.job_id,
                                                          stop_on_build=1),
                          reviewer_provider=_pass_provider(), repair_rounds=0)

        run = load_run(stopped.tasks[0].run_id)
        assert run["final_status"] == "stopped"
        block = run["stop"]
        assert block["stop_signal_v"] == 1
        assert block["request_id"] == stopped.stop_request_id
        assert block["reason"] == "operator requested stop"
        assert block["source"] == "test"
        assert block["requested_at"]

        # The STOP block is the F011 surface: nothing in it is a path or a secret. (The
        # surrounding run record has always carried its own staging path; that is F004's
        # existing contract, not ours to change here.)
        raw = json.dumps(block)
        assert str(demo_repo) not in raw and str(isolate_data_root) not in raw

    def test_an_ordinary_run_json_has_no_stop_block(self, isolate_data_root, demo_repo):
        from packages.orchestration.pingpong_loop import load_run

        job = parse_job_file(_ONE_TASK_JOB, str(demo_repo))
        done = run_job(job.job_id, builder_provider=_pass_provider(),
                       reviewer_provider=_pass_provider(), repair_rounds=0)
        assert done.status == JOB_COMPLETED
        assert "stop" not in load_run(done.tasks[0].run_id)


class TestNothingUntrustedReachesTheEvidence:
    def test_a_planted_control_file_cannot_leak_a_secret_into_event_or_postmortem(
            self, isolate_data_root, demo_repo):
        job = parse_job_file(_ONE_TASK_JOB, str(demo_repo))
        control = isolate_data_root / "control" / "jobs" / job.job_id
        control.mkdir(parents=True)
        (control / "stop.json").write_text(json.dumps({
            "stop_signal_v": 1,
            "request_id": "abc123def456abcd",
            "reason": f"token=sk-live-abcdef123456 in {demo_repo}",
            "source": str(demo_repo),
            "requested_at": "API_KEY=supersecret /home/alice/private",
        }))

        stopped = run_job(job.job_id, builder_provider=_pass_provider(),
                          reviewer_provider=_pass_provider(), repair_rounds=0)
        assert stopped.status == JOB_STOPPED

        record = (_stop_episodes(job.job_id)[0] / "postmortem.json").read_text()
        events = json.dumps(_events(isolate_data_root, job.job_id, "job_stopped"))
        job_json = job_record_path(job.job_id, isolate_data_root).read_text()

        for blob in (record, events, job_json):
            assert "sk-live-abcdef123456" not in blob
            assert "supersecret" not in blob
            assert "/home/alice/private" not in blob

        # The planted SOURCE was an absolute path; none of it reaches the stop fields.
        stop_fields = json.dumps(json.loads(job_json)["stop"])
        assert str(demo_repo) not in stop_fields
        assert str(demo_repo) not in record and str(demo_repo) not in events


@pytest.mark.subprocess
class TestTheNoLeftoverCheckIsScopedButStillStrict:
    """The scoping must ignore other people's processes — and still catch ours."""

    def test_an_unrelated_pre_existing_child_is_not_counted_as_a_leak(self, tmp_path):
        stranger = subprocess.Popen(
            [sys.executable, "-c", "import time; time.sleep(30)"],
            cwd="/", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            baseline = {c.pid for c in psutil.Process().children(recursive=True)}
            assert stranger.pid in baseline
            assert _test_owned_children(baseline, tmp_path) == []
        finally:
            stranger.kill()
            stranger.wait(timeout=30)

    def test_a_leaked_test_owned_child_is_still_detected(self, tmp_path):
        baseline = {c.pid for c in psutil.Process().children(recursive=True)}
        marker = tmp_path / "loop.py"
        marker.write_text("import time\nwhile True: time.sleep(0.2)\n")
        leaked = subprocess.Popen([sys.executable, str(marker)], cwd=str(tmp_path),
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            owned = _test_owned_children(baseline, tmp_path)
            assert [c.pid for c in owned] == [leaked.pid], "a real leak went unnoticed"
        finally:
            leaked.kill()
            leaked.wait(timeout=30)
