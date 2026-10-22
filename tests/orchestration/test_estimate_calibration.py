"""F074 T001 — the estimate calibration measured from fixture ledgers.

Every ledger here is written through `token_ledger.record_call` and every job record as the
`tasks[].task_class` a real job stores, under the test's own data root, so the table is measured
exactly as a project's would be.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from packages.orchestration.data_paths import job_record_path
from packages.orchestration.estimate_calibration import (
    CALIBRATION_SNAPSHOT_FILENAME,
    TASK_TOTAL_ROLE,
    CalibrationDistribution,
    build_calibration_table,
    calibrated_class_tokens,
    calibration_basis_label,
    calibration_snapshot_path,
    calibration_table_from_json,
    damped_distribution,
    load_calibration_table,
    resolve_calibration_for_root,
)
from packages.orchestration.token_ledger import CallRecord, record_call, token_ledger_path_for

PROJECT = "11111111-2222-3333-4444-555555555555"
NOW = datetime(2026, 10, 20, 12, 0, tzinfo=timezone.utc)
RECENT = "2026-10-15T09:00:00+00:00"


def _call(root: Path, job: str, task: str | None, role: str, tokens_in: int | None, tokens_out: int | None,
          *, cost: float | None = None, ts: str = RECENT, seq: int = 0) -> None:
    written = record_call(CallRecord(
        call_id=f"{job}:{task}:{role}:{seq}", job_id=job, task_id=task, role=role, model="m",
        ts_utc=ts, tokens_in=tokens_in, tokens_out=tokens_out, cost_usd=cost,
        cost_basis="unknown" if cost is None else "provider_reported"),
        path=token_ledger_path_for(PROJECT, root))
    assert written


def _job(root: Path, job: str, classes: dict[str, str | None]) -> None:
    path = job_record_path(job, root)
    path.parent.mkdir(parents=True, exist_ok=True)
    tasks = [{"task_id": task_id, "task_class": task_class} for task_id, task_class in classes.items()]
    path.write_text(json.dumps({"job_id": job, "tasks": tasks}), encoding="utf-8")


def _fat_class(root: Path, count: int = 20, task_class: str = "standard_build") -> None:
    """``count`` tasks of one class: builder k*1000 tokens and k*0.01 USD, reviewer 500 tokens unpriced."""
    for k in range(1, count + 1):
        job = f"job{task_class}{k:02d}"
        _job(root, job, {"T001": task_class})
        _call(root, job, "T001", "builder", k * 1000 - 100, 100, cost=round(k * 0.01, 2))
        _call(root, job, "T001", "reviewer", 400, 100)


class TestDampedDistribution:
    def test_trims_one_in_twenty_from_each_end_and_counts_every_sample(self):
        values = [float(v) for v in range(1, 41)]
        dist = damped_distribution(values)
        # Two trimmed from each end leaves 3..38: P20 at position 7, P50 at 17.5, P80 at 28 of 36 values.
        assert dist == CalibrationDistribution(n=40, p20=10.0, p50=20.5, p80=31.0)

    def test_keeps_one_or_two_samples_untrimmed(self):
        assert damped_distribution([7.0]) == CalibrationDistribution(n=1, p20=7.0, p50=7.0, p80=7.0)
        assert damped_distribution([1.0, 3.0]) == CalibrationDistribution(n=2, p20=1.4, p50=2.0, p80=2.6)

    def test_refuses_an_empty_sample(self):
        with pytest.raises(ValueError):
            damped_distribution([])


class TestBuildCalibrationTable:
    def test_fixture_percentiles_are_exact_per_role_and_for_the_whole_task(self, tmp_path):
        _fat_class(tmp_path)
        table = build_calibration_table(PROJECT, now=NOW, root=tmp_path)
        assert table.ledger_present and table.unclassified_tasks == 0 and table.unmeasured_tasks == 0
        builder = table.lookup("standard_build", "builder")
        # 1000..20000, one trimmed from each end: P20 at 3.4, P50 at 8.5, P80 at 13.6 of 18 values.
        assert builder.tokens == CalibrationDistribution(n=20, p20=5400.0, p50=10500.0, p80=15600.0)
        assert builder.cost_usd == CalibrationDistribution(n=20, p20=0.054, p50=0.105, p80=0.156)
        reviewer = table.lookup("standard_build", "reviewer")
        assert reviewer.tokens == CalibrationDistribution(n=20, p20=500.0, p50=500.0, p80=500.0)
        assert reviewer.cost_usd is None
        whole = table.lookup("standard_build", TASK_TOTAL_ROLE)
        assert whole.tokens == CalibrationDistribution(n=20, p20=5900.0, p50=11000.0, p80=16100.0)
        # One unpriced role leaves the whole task without a cost, never half of one.
        assert whole.cost_usd is None

    def test_a_fat_class_is_calibrated_and_a_thin_one_stays_on_its_default(self, tmp_path):
        _fat_class(tmp_path)
        _fat_class(tmp_path, count=3, task_class="format")
        table = build_calibration_table(PROJECT, now=NOW, root=tmp_path)
        assert table.lookup("format", TASK_TOTAL_ROLE).tokens.n == 3
        assert table.calibrated_tokens("format") is None
        assert table.calibrated_tokens("standard_build").n == 20
        assert calibrated_class_tokens(table, "standard_build") == table.calibrated_tokens("standard_build")
        assert calibrated_class_tokens(table, "architecture") is None
        assert calibrated_class_tokens(table, None) is None
        assert calibrated_class_tokens(None, "standard_build") is None

    def test_the_floor_is_the_configured_one(self, tmp_path):
        _fat_class(tmp_path, count=3, task_class="format")
        assert build_calibration_table(PROJECT, now=NOW, sample_floor=3, root=tmp_path).calibrated_tokens("format")
        assert build_calibration_table(PROJECT, now=NOW, sample_floor=4, root=tmp_path).calibrated_tokens(
            "format") is None

    def test_one_runaway_task_does_not_drag_the_p80(self, tmp_path):
        for k, tokens in enumerate((100, 110, 120, 130, 100000)):
            _job(tmp_path, f"jobrun{k}", {"T001": "extract"})
            _call(tmp_path, f"jobrun{k}", "T001", "builder", tokens, 0)
        table = build_calibration_table(PROJECT, now=NOW, sample_floor=5, root=tmp_path)
        tokens = table.calibrated_tokens("extract")
        # Undamped, the P80 of these five would sit at 20104; trimmed, it is 126.
        assert tokens == CalibrationDistribution(n=5, p20=114.0, p50=120.0, p80=126.0)

    def test_old_tasks_age_out_of_the_window(self, tmp_path):
        _fat_class(tmp_path, count=2, task_class="format")
        _job(tmp_path, "jobold", {"T001": "format"})
        _call(tmp_path, "jobold", "T001", "builder", 99000, 0, ts=(NOW - timedelta(days=91)).isoformat())
        table = build_calibration_table(PROJECT, now=NOW, root=tmp_path)
        assert table.lookup("format", "builder").tokens.n == 2
        assert build_calibration_table(PROJECT, now=NOW, window_days=92, root=tmp_path).lookup(
            "format", "builder").tokens.n == 3

    def test_a_task_is_placed_in_the_window_by_its_latest_call(self, tmp_path):
        # The builder's call is older than the window and the reviewer's is not: the task counts whole.
        _job(tmp_path, "jobspan", {"T001": "format"})
        _call(tmp_path, "jobspan", "T001", "builder", 1000, 0, ts=(NOW - timedelta(days=95)).isoformat())
        _call(tmp_path, "jobspan", "T001", "reviewer", 2000, 0, ts=RECENT)
        table = build_calibration_table(PROJECT, now=NOW, root=tmp_path)
        assert table.lookup("format", "builder").tokens == CalibrationDistribution(
            n=1, p20=1000.0, p50=1000.0, p80=1000.0)
        assert table.lookup("format", TASK_TOTAL_ROLE).tokens == CalibrationDistribution(
            n=1, p20=3000.0, p50=3000.0, p80=3000.0)

    def test_unclassified_unmeasured_and_teacher_calls_are_counted_never_guessed(self, tmp_path):
        _job(tmp_path, "jobnoclass", {"T001": None})
        _call(tmp_path, "jobnoclass", "T001", "builder", 1000, 10)
        _call(tmp_path, "jobgone", "T001", "builder", 1000, 10)
        _job(tmp_path, "jobhalf", {"T001": "format"})
        _call(tmp_path, "jobhalf", "T001", "builder", 1000, None)
        _call(tmp_path, "jobhalf", "T001", "reviewer", 300, 20)
        _call(tmp_path, "jobteach", None, "teacher", 5000, 50)
        table = build_calibration_table(PROJECT, now=NOW, root=tmp_path)
        assert table.unclassified_tasks == 2
        assert table.unmeasured_tasks == 1
        assert table.lookup("format", "builder") is None
        assert table.lookup("format", "reviewer").tokens.n == 1
        assert table.lookup("format", TASK_TOTAL_ROLE) is None
        assert {entry.role for entry in table.entries} == {"reviewer"}

    def test_a_missing_ledger_is_an_empty_table_and_creates_nothing(self, tmp_path):
        table = build_calibration_table(PROJECT, now=NOW, root=tmp_path)
        assert not table.ledger_present and table.entries == ()
        assert not token_ledger_path_for(PROJECT, tmp_path).parent.exists()

    def test_the_measurement_is_read_only_on_the_ledger(self, tmp_path):
        _fat_class(tmp_path)
        folder = token_ledger_path_for(PROJECT, tmp_path).parent

        def state() -> dict[str, str]:
            return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(folder.iterdir())}

        before = state()
        build_calibration_table(PROJECT, now=NOW, root=tmp_path)
        assert state() == before


class TestSnapshot:
    def test_a_fresh_snapshot_is_reused_and_a_stale_one_is_measured_again(self, tmp_path):
        _fat_class(tmp_path, count=2, task_class="format")
        first = load_calibration_table(PROJECT, now=NOW, root=tmp_path)
        path = calibration_snapshot_path(PROJECT, tmp_path)
        assert path.name == CALIBRATION_SNAPSHOT_FILENAME
        assert path.parent == token_ledger_path_for(PROJECT, tmp_path).parent
        assert calibration_table_from_json(json.loads(path.read_text(encoding="utf-8"))) == first
        _job(tmp_path, "joblate", {"T001": "format"})
        _call(tmp_path, "joblate", "T001", "builder", 7000, 0)
        fresh = load_calibration_table(PROJECT, now=NOW + timedelta(minutes=59), root=tmp_path)
        assert fresh == first and fresh.lookup("format", "builder").tokens.n == 2
        stale = load_calibration_table(PROJECT, now=NOW + timedelta(minutes=61), root=tmp_path)
        assert stale.lookup("format", "builder").tokens.n == 3
        assert stale.updated_at == (NOW + timedelta(minutes=61)).isoformat()

    def test_the_age_limit_is_the_configured_one(self, tmp_path):
        _fat_class(tmp_path, count=2, task_class="format")
        load_calibration_table(PROJECT, now=NOW, root=tmp_path)
        _job(tmp_path, "joblate", {"T001": "format"})
        _call(tmp_path, "joblate", "T001", "builder", 7000, 0)
        later = NOW + timedelta(seconds=120)
        assert load_calibration_table(PROJECT, now=later, max_age_seconds=60, root=tmp_path).lookup(
            "format", "builder").tokens.n == 3

    def test_a_snapshot_built_with_another_window_or_floor_is_not_used(self, tmp_path):
        _fat_class(tmp_path, count=2, task_class="format")
        load_calibration_table(PROJECT, now=NOW, root=tmp_path)
        assert load_calibration_table(PROJECT, now=NOW, sample_floor=2, root=tmp_path).sample_floor == 2
        assert load_calibration_table(PROJECT, now=NOW, window_days=30, root=tmp_path).window_days == 30

    def test_an_unreadable_or_future_snapshot_is_measured_again(self, tmp_path):
        _fat_class(tmp_path, count=2, task_class="format")
        path = calibration_snapshot_path(PROJECT, tmp_path)
        path.write_text("{not json", encoding="utf-8")
        assert load_calibration_table(PROJECT, now=NOW, root=tmp_path).ledger_present
        assert json.loads(path.read_text(encoding="utf-8"))["updated_at"] == NOW.isoformat()
        future = load_calibration_table(PROJECT, now=NOW - timedelta(minutes=5), root=tmp_path)
        assert future.updated_at == (NOW - timedelta(minutes=5)).isoformat()

    def test_no_ledger_writes_no_snapshot(self, tmp_path):
        # The project's folder exists, as a registered project's does before its first call is recorded.
        token_ledger_path_for(PROJECT, tmp_path).parent.mkdir(parents=True)
        table = load_calibration_table(PROJECT, now=NOW, root=tmp_path)
        assert not table.ledger_present
        assert not calibration_snapshot_path(PROJECT, tmp_path).exists()


class TestResolveForRoot:
    def test_an_unregistered_root_has_no_calibration(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        assert resolve_calibration_for_root(repo, window_days=90, sample_floor=20, max_age_seconds=3600) is None

    def test_a_registered_root_reads_its_own_project_ledger(self, tmp_path):
        from packages.orchestration.data_paths import resolve_data_root
        from packages.orchestration.project_registry import register_project_repo

        repo = tmp_path / "repo"
        repo.mkdir()
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        project = register_project_repo("Calibrated", repo)
        root = resolve_data_root()
        _job(root, "jobreg", {"T001": "format"})
        record_call(CallRecord(call_id="jobreg:T001:1", job_id="jobreg", task_id="T001", role="builder",
                               ts_utc=datetime.now(timezone.utc).isoformat(), tokens_in=10, tokens_out=5),
                    project_id=str(project.id))
        table = resolve_calibration_for_root(repo, window_days=90, sample_floor=1, max_age_seconds=3600)
        assert table is not None and table.project_id == str(project.id)
        assert table.calibrated_tokens("format").p50 == 15.0


def test_the_basis_label_names_the_sample_count():
    assert calibration_basis_label(37) == "calibrated(37)"
