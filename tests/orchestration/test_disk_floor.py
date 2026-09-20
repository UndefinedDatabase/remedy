"""F276 T004 — the disk floor, a budget like the others.

THE PROBE IS NEVER THE REAL FILESYSTEM HERE. The autouse fixture below rebinds
``budget_guard.FREE_DISK_PROBE`` to a probe that RAISES, for every test in this
file, so a test that forgets to inject fails loudly instead of quietly reading
whatever the machine the suite runs on happens to have free. A disk assertion
made against the real filesystem is not a test, it is a weather report — and it
would be green on a roomy machine and red on a full one, which is exactly
backwards.

No test here calls a model provider: the two ``run_job`` tests use the fake
builder and reviewer over a temporary git repository, and both stop BEFORE the
first provider call by construction.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from packages.core.models import JobBudgets
from packages.orchestration import budget_guard
from packages.orchestration.budget_guard import (
    FREE_DISK_LIMIT,
    BudgetCounters,
    evaluate_budget,
)

JOB_TEXT = """# One-task job

## Task 1 — write the readme

Write `docs/README.md`.
"""


class ProbeWasReadFromTheRealFilesystem(AssertionError):
    """Raised by the seam when a test forgot to inject its own probe."""


def _forbidden_probe() -> int:
    raise ProbeWasReadFromTheRealFilesystem(
        "a disk-floor test read the real filesystem; inject a probe")


@pytest.fixture(autouse=True)
def _no_real_disk(monkeypatch):
    monkeypatch.setattr(budget_guard, "FREE_DISK_PROBE", _forbidden_probe)


@pytest.fixture(autouse=True)
def _isolate_data_root(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "remedy_data"))


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=str(repo), capture_output=True,
                   text=True, check=True)


@pytest.fixture
def repo(tmp_path) -> Path:
    r = tmp_path / "repo"
    r.mkdir()
    _git(r, "init", "-q")
    _git(r, "config", "user.email", "t@e.com")
    _git(r, "config", "user.name", "T")
    _git(r, "config", "commit.gpgsign", "false")
    (r / "base.txt").write_text("base\n")
    _git(r, "add", "-A")
    _git(r, "commit", "-qm", "init")
    return r


def _counters() -> BudgetCounters:
    return BudgetCounters()


# ---------------------------------------------------------------------------
# The floor's default, and its config override
# ---------------------------------------------------------------------------


class TestTheFloorsDefaultAndItsOverride:
    def test_the_floor_is_absent_by_default(self):
        """Absent, not zero: `JobBudgets` says "absent means no limit" and a
        default number would hand a budget to every job that has none."""
        assert JobBudgets().min_free_disk_bytes is None

    def test_no_budget_config_still_resolves_to_no_budgets_at_all(self, tmp_path):
        """The regression this default exists to avoid: `resolve_job_budgets`
        must keep answering None when nothing is configured, because a
        `JobBudgets` where there was None changes `run_contract`'s limits and
        starts a budget tick for every job."""
        from packages.orchestration.budget_resolution import resolve_job_budgets

        assert resolve_job_budgets(config_path=str(tmp_path / "absent.toml")) is None

    def test_the_toml_key_sets_the_floor(self, tmp_path):
        from packages.orchestration.budget_resolution import resolve_job_budgets

        cfg = tmp_path / "remedy.toml"
        cfg.write_text("[remedy]\n\"budget.min_free_disk_bytes\" = 4096\n")
        budgets = resolve_job_budgets(config_path=str(cfg))
        assert budgets is not None
        assert budgets.min_free_disk_bytes == 4096

    def test_the_env_var_sets_the_floor(self, tmp_path, monkeypatch):
        from packages.orchestration.budget_resolution import resolve_job_budgets

        monkeypatch.setenv("REMEDY_BUDGET_MIN_FREE_DISK_BYTES", "8192")
        budgets = resolve_job_budgets(config_path=str(tmp_path / "absent.toml"))
        assert budgets is not None
        assert budgets.min_free_disk_bytes == 8192

    def test_a_non_positive_floor_is_refused_like_every_other_integer_limit(self):
        with pytest.raises(ValueError, match="strictly positive"):
            JobBudgets(min_free_disk_bytes=0)


# ---------------------------------------------------------------------------
# evaluate_budget
# ---------------------------------------------------------------------------


class TestEvaluateBudgetReadsTheFloor:
    def test_below_the_floor_is_exhausted(self):
        r = evaluate_budget(JobBudgets(min_free_disk_bytes=1000), _counters(),
                            free_disk_probe=lambda: 999)
        assert r.exhausted is True
        assert r.first_exhausted_limit == FREE_DISK_LIMIT

    def test_above_the_floor_is_not_exhausted(self):
        r = evaluate_budget(JobBudgets(min_free_disk_bytes=1000), _counters(),
                            free_disk_probe=lambda: 1001)
        assert r.exhausted is False
        assert r.first_exhausted_limit is None

    def test_exactly_at_the_floor_is_not_exhausted(self):
        """A FLOOR of N accepts N. Every other limit here is exhausted at
        `counter >= limit`; this one at `free < floor`, and the boundary is the
        place the two directions are easiest to confuse."""
        r = evaluate_budget(JobBudgets(min_free_disk_bytes=1000), _counters(),
                            free_disk_probe=lambda: 1000)
        assert r.exhausted is False

    def test_the_reading_is_reported_in_both_directions(self):
        below = evaluate_budget(JobBudgets(min_free_disk_bytes=1000), _counters(),
                                free_disk_probe=lambda: 7)
        above = evaluate_budget(JobBudgets(min_free_disk_bytes=1000), _counters(),
                                free_disk_probe=lambda: 7000)
        assert "free_disk: 7/1000 bytes" in below.source_descriptions
        assert "free_disk: 7000/1000 bytes" in above.source_descriptions

    def test_the_module_seam_answers_when_no_per_call_probe_is_given(self, monkeypatch):
        monkeypatch.setattr(budget_guard, "FREE_DISK_PROBE", lambda: 5)
        r = evaluate_budget(JobBudgets(min_free_disk_bytes=1000), _counters())
        assert r.exhausted is True
        assert r.first_exhausted_limit == FREE_DISK_LIMIT

    def test_a_probe_that_raises_warns_and_never_stops_the_job(self):
        """A mount point that vanishes under a stat must not kill a healthy job."""
        def _boom() -> int:
            raise OSError("mount went away")

        r = evaluate_budget(JobBudgets(min_free_disk_bytes=1000), _counters(),
                            free_disk_probe=_boom)
        assert r.exhausted is False
        assert any("free disk could not be read" in w for w in r.warnings)


class TestTheDefaultChangesNoExistingJob:
    """The regression guard for the default chosen: with the floor ABSENT the
    probe is never called at all, so every job that predates F276 evaluates
    exactly the calls it evaluated before. The autouse probe RAISES, so a
    single stray call turns this red."""

    def test_no_floor_means_the_probe_is_never_called(self):
        r = evaluate_budget(JobBudgets(max_provider_calls=10), _counters())
        assert r.exhausted is False

    def test_no_floor_leaves_the_source_descriptions_free_of_disk(self):
        r = evaluate_budget(JobBudgets(max_provider_calls=10), _counters())
        assert not any(s.startswith("free_disk") for s in r.source_descriptions)

    def test_an_empty_budget_still_evaluates_without_touching_disk(self):
        r = evaluate_budget(JobBudgets(), _counters())
        assert (r.exhausted, r.first_exhausted_limit, r.warnings) == (False, None, ())


class TestTheForbiddenProbeIsActuallyInForce:
    """The guard that makes every other test in this file mean something.

    ``evaluate_budget`` deliberately SWALLOWS a raising probe into a warning, so
    the forbidden probe cannot fail a test by exception; what it does instead is
    make the evaluation say, in its own warning text, that it was the forbidden
    probe that answered — and then never exhaust, so no assertion about
    exhaustion can accidentally pass on the real filesystem."""

    def test_the_seam_is_the_forbidden_probe_unless_a_test_injects(self):
        r = evaluate_budget(JobBudgets(min_free_disk_bytes=1), _counters())
        assert r.exhausted is False
        assert any("ProbeWasReadFromTheRealFilesystem" in w for w in r.warnings)

    def test_the_real_probe_is_not_installed_during_this_file(self):
        assert budget_guard.FREE_DISK_PROBE is not budget_guard.default_free_disk_bytes


# ---------------------------------------------------------------------------
# The safe point and the STOPPED path
# ---------------------------------------------------------------------------


class TestTheSafePointStopsOnTheFloor:
    def test_should_stop_names_the_disk_limit(self, tmp_path):
        from packages.orchestration.safe_points import should_stop

        r = should_stop("disk-job-001", budgets=JobBudgets(min_free_disk_bytes=1000),
                        counters=_counters(), control_root_path=tmp_path,
                        free_disk_probe=lambda: 1)
        assert r.should_stop is True
        assert r.source == "budget"
        assert r.reason == f"budget_exhausted:{FREE_DISK_LIMIT}"

    def test_should_stop_continues_above_the_floor(self, tmp_path):
        from packages.orchestration.safe_points import should_stop

        r = should_stop("disk-job-002", budgets=JobBudgets(min_free_disk_bytes=1000),
                        counters=_counters(), control_root_path=tmp_path,
                        free_disk_probe=lambda: 10_000)
        assert r.should_stop is False


def _postmortem_of(job) -> dict:
    from packages.orchestration.data_paths import job_evidence_dir

    assert job.stop_postmortem_path, "the stop wrote no post-mortem path"
    path = job_evidence_dir(job.job_id) / job.stop_postmortem_path
    return json.loads(Path(path).read_text(encoding="utf-8"))


class TestAJobStartBelowTheFloorIsRefused:
    def test_the_job_reaches_stopped_before_any_work(self, repo, monkeypatch):
        from packages.orchestration.pingpong_job import (
            JOB_STOPPED,
            parse_job_file,
            run_job,
        )

        monkeypatch.setattr(budget_guard, "FREE_DISK_PROBE", lambda: 1)
        job_id = str(parse_job_file(JOB_TEXT, str(repo)).job_id)

        done = run_job(job_id, builder_name="fake", reviewer_name="fake",
                       budgets={"min_free_disk_bytes": 10**15})

        assert done.state == JOB_STOPPED
        assert done.stop_source == "budget"
        assert done.stop_reason == f"budget_exhausted:{FREE_DISK_LIMIT}"
        assert all(t.status == "pending" for t in done.tasks)
        # "BEFORE ANY WORK" made measurable. A stopped job with pending tasks is
        # ALSO what a build with no job-start check produces — the next safe
        # point stops it just as dead. These two fields separate the two: the
        # pre-work stop returns before `first_running_at` is stamped and before
        # the job workspace is acquired, and a job stopped one safe point later
        # carries both.
        assert done.first_running_at == ""
        assert done.job_workspace_path == ""

    def test_the_post_mortem_reason_is_disk_exhausted(self, repo, monkeypatch):
        from packages.orchestration.pingpong_job import parse_job_file, run_job

        monkeypatch.setattr(budget_guard, "FREE_DISK_PROBE", lambda: 1)
        job_id = str(parse_job_file(JOB_TEXT, str(repo)).job_id)

        done = run_job(job_id, builder_name="fake", reviewer_name="fake",
                       budgets={"min_free_disk_bytes": 10**15})

        record = _postmortem_of(done)
        assert record["terminal_status"] == "disk_exhausted"
        assert record["failure_class"] == "disk_exhausted"

    def test_a_job_above_the_floor_is_not_refused(self, repo, monkeypatch):
        from packages.orchestration.pingpong_job import JOB_STOPPED, parse_job_file, run_job

        monkeypatch.setattr(budget_guard, "FREE_DISK_PROBE", lambda: 10**15)
        job_id = str(parse_job_file(JOB_TEXT, str(repo)).job_id)

        done = run_job(job_id, builder_name="fake", reviewer_name="fake",
                       budgets={"min_free_disk_bytes": 1000})

        assert done.state != JOB_STOPPED


class TestAnInFlightJobBelowTheFloorStops:
    """The disk falls away AFTER the job started: the first reading is roomy,
    every later one is not, so the job passes its start check and stops at the
    task-dispatch safe point — before the first provider call."""

    def test_the_job_reaches_stopped_at_a_safe_point(self, repo, monkeypatch):
        from packages.orchestration.pingpong_job import (
            JOB_STOPPED,
            parse_job_file,
            run_job,
        )

        readings = iter([10**15])
        monkeypatch.setattr(budget_guard, "FREE_DISK_PROBE",
                            lambda: next(readings, 1))
        job_id = str(parse_job_file(JOB_TEXT, str(repo)).job_id)

        done = run_job(job_id, builder_name="fake", reviewer_name="fake",
                       budgets={"min_free_disk_bytes": 10**9})

        assert done.state == JOB_STOPPED
        assert done.stop_reason == f"budget_exhausted:{FREE_DISK_LIMIT}"
        assert done.first_running_at, "the job started before it was stopped"
        # The DISCRIMINATOR for WHICH safe point caught it, MEASURED rather than
        # assumed. `run_job` hands `_stop_check` into the ping-pong loop as well,
        # so deleting the task-dispatch safe point leaves the job stopped and its
        # task back at `pending` all the same — defence in depth, and a test that
        # asserted only those two would be satisfied by the deletion. What the
        # deletion cannot hide is that the loop RAN: it mints a run id and
        # appends it to `run_refs`. An empty `run_refs` is the proof that the
        # stop landed before dispatch, which is the whole promise of a safe
        # point: zero work started once a budget is gone.
        assert [t.status for t in done.tasks] == ["pending"]
        assert done.run_refs == []
        assert [t.run_id for t in done.tasks] == [""]

    def test_its_post_mortem_reason_is_disk_exhausted(self, repo, monkeypatch):
        from packages.orchestration.pingpong_job import parse_job_file, run_job

        readings = iter([10**15])
        monkeypatch.setattr(budget_guard, "FREE_DISK_PROBE",
                            lambda: next(readings, 1))
        job_id = str(parse_job_file(JOB_TEXT, str(repo)).job_id)

        done = run_job(job_id, builder_name="fake", reviewer_name="fake",
                       budgets={"min_free_disk_bytes": 10**9})

        record = _postmortem_of(done)
        assert record["terminal_status"] == "disk_exhausted"
        assert record["failure_class"] == "disk_exhausted"

    def test_the_disk_is_named_first_when_two_limits_are_exhausted(self):
        """`_LIMIT_ORDER` puts the disk first on purpose: it is the one limit
        the operator cannot simply raise their way past."""
        from datetime import datetime, timedelta, timezone

        past = datetime.now(timezone.utc) - timedelta(hours=1)
        r = evaluate_budget(JobBudgets(deadline=past, min_free_disk_bytes=1000),
                            _counters(), free_disk_probe=lambda: 1)
        assert r.exhausted is True
        assert r.first_exhausted_limit == FREE_DISK_LIMIT


class TestTheTerminalStatusDiscriminator:
    """The post-mortem branch itself, at the seam it lives in.

    The two signals differ in ONE character sequence — the limit name inside the
    reason — and everything else about them is identical, so if the disk's
    terminal status had simply REPLACED the older one rather than joining it,
    the second test here goes red."""

    def _written(self, reason: str, source: str) -> dict:
        from packages.orchestration.pingpong_job import (
            JobPlan,
            _persist_job,
            _write_stop_postmortem,
        )
        from packages.orchestration.safe_points import StopSignal

        job = JobPlan(state="running")
        _persist_job(job)
        signal = StopSignal(job_id=job.job_id, request_id="stop_0123456789abcdef",
                            reason=reason, source=source)
        _write_stop_postmortem(job, signal, "")
        assert job.stop_error == "", job.stop_error
        return _postmortem_of(job)

    def test_the_disk_limit_writes_disk_exhausted(self):
        record = self._written(f"budget_exhausted:{FREE_DISK_LIMIT}", "budget")
        assert record["terminal_status"] == "disk_exhausted"
        assert record["failure_class"] == "disk_exhausted"

    def test_every_other_limit_still_writes_budget_exhausted(self):
        record = self._written("budget_exhausted:max_total_tokens", "budget")
        assert record["terminal_status"] == "budget_exhausted"
        assert record["failure_class"] == "budget_exhausted"

    def test_an_operator_stop_still_writes_stopped(self):
        record = self._written("operator asked", "cli")
        assert record["terminal_status"] == "stopped"
        assert record["failure_class"] == "stopped"


# ---------------------------------------------------------------------------
# remedy doctor core
# ---------------------------------------------------------------------------


def _doctor_json(capsys, **ns_kwargs) -> dict:
    import argparse

    from apps.cli.commands.worker_facade_cmd import _cmd_doctor_core

    _cmd_doctor_core(argparse.Namespace(json=True, **ns_kwargs))
    return json.loads(capsys.readouterr().out)


class TestDoctorReadsTheInjectedProbe:
    def test_the_section_states_both_numbers(self, capsys, monkeypatch, tmp_path):
        monkeypatch.setattr(budget_guard, "FREE_DISK_PROBE", lambda: 4242)
        monkeypatch.setenv("REMEDY_BUDGET_MIN_FREE_DISK_BYTES", "1000")
        monkeypatch.chdir(tmp_path)

        out = _doctor_json(capsys)
        assert out["disk"]["free_bytes"] == 4242
        assert out["disk"]["floor_bytes"] == 1000
        assert out["disk"]["floor_met"] is True

    def test_a_floor_that_is_not_met_blocks_ready(self, capsys, monkeypatch, tmp_path):
        monkeypatch.setattr(budget_guard, "FREE_DISK_PROBE", lambda: 10)
        monkeypatch.setenv("REMEDY_BUDGET_MIN_FREE_DISK_BYTES", "1000")
        monkeypatch.chdir(tmp_path)

        out = _doctor_json(capsys)
        assert out["disk"]["floor_met"] is False
        assert "disk_floor" in out["blockers"]
        assert out["ready"] is False

    def test_no_configured_floor_is_met_and_keeps_ready(self, capsys, monkeypatch, tmp_path):
        monkeypatch.setattr(budget_guard, "FREE_DISK_PROBE", lambda: 10)
        monkeypatch.delenv("REMEDY_BUDGET_MIN_FREE_DISK_BYTES", raising=False)
        monkeypatch.chdir(tmp_path)

        out = _doctor_json(capsys)
        assert out["disk"]["floor_bytes"] is None
        assert out["disk"]["floor_met"] is True
        assert "disk_floor" not in out["blockers"]

    def test_text_mode_prints_both_numbers_and_the_verdict(
            self, capsys, monkeypatch, tmp_path):
        import argparse

        from apps.cli.commands.worker_facade_cmd import _cmd_doctor_core

        monkeypatch.setattr(budget_guard, "FREE_DISK_PROBE", lambda: 10)
        monkeypatch.setenv("REMEDY_BUDGET_MIN_FREE_DISK_BYTES", "1000")
        monkeypatch.chdir(tmp_path)

        _cmd_doctor_core(argparse.Namespace(json=False))
        text = capsys.readouterr().out
        assert "10 bytes free" in text
        assert "floor: 1000 bytes" in text
        assert "floor met: NO" in text
