"""F113 T003a, DECISION F113 D2 — the side-role calls a task run made, as evidence and in the ledger.

The rows are read from summaries planted in a run directory first, then from a real run whose job
evidence export writes them beside the task's other evidence and mirrors them into the cost ledger.
"""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from types import SimpleNamespace

import pytest

from packages.orchestration import side_role_calls
from packages.orchestration.artifact_summary import generate_artifact_summary, save_summary
from packages.orchestration.data_paths import run_dir
from packages.orchestration.side_role_calls import (
    SIDE_ROLE_CALLS_FILENAME,
    SideRoleCallRow,
    SideRoleCallSummary,
    query_side_role_calls,
    record_side_role_calls,
    rows_from_evidence_file,
    side_role_call_rows,
    write_task_side_role_calls,
)
from packages.orchestration.side_role_routing import ROUTE_FALLBACK, ROUTE_LOCAL, SideRoleRoute
from packages.orchestration.token_ledger import token_ledger_path_for
from tests.orchestration import test_tier_escalation

REPLY = json.dumps({"l1": "a summary", "l2": []})
LOCAL = SideRoleRoute("summary", ROUTE_LOCAL, "box", "muse-glimmer", "")
DOWN = SideRoleRoute("summary", ROUTE_FALLBACK, "box", "", "provider_unavailable: local endpoint box at x did not answer")


def plant(run_path: Path, role_round: str, route: SideRoleRoute | None) -> None:
    """Cache one summary under `run_path` the way the loop's tiered diff does, with `route` on its call_fn."""
    def call_fn(prompt: str, attempt: int) -> str:
        return REPLY

    if route is not None:
        call_fn.side_role_route = route  # type: ignore[attr-defined]
    artifact = run_path / "calls" / role_round / "tiered_diff.diff"
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text("diff", encoding="utf-8")
    save_summary(artifact, generate_artifact_summary([], str(artifact), "abc", call_fn))


def rows(run_path: Path) -> list[SideRoleCallRow]:
    return side_role_call_rows(run_path, job_id="job-1", task_id="T001", run_id="run-1")


class TestTheRows:
    def test_each_routed_summary_gives_one_row_with_its_basis(self, tmp_path):
        plant(tmp_path, "builder/round-02", LOCAL)
        plant(tmp_path, "reviewer/round-03", DOWN)
        local, down = rows(tmp_path)
        assert (local.call_ref, local.role, local.route, local.endpoint, local.routed_model, local.cost_basis) == (
            "calls/builder/round-02/tiered_diff.diff.summary.json", "summary", "local", "box", "muse-glimmer",
            "local_zero")
        assert (down.call_ref, down.route, down.routed_model, down.reason, down.cost_basis) == (
            "calls/reviewer/round-03/tiered_diff.diff.summary.json", "fallback", "", DOWN.reason, "unknown")
        assert (local.job_id, local.task_id, local.run_id) == ("job-1", "T001", "run-1")

    def test_a_local_calls_tokens_are_unmeasured_never_zero(self, tmp_path):
        plant(tmp_path, "builder/round-02", LOCAL)
        (row,) = rows(tmp_path)
        assert row.tokens_out is None

    def test_a_summary_without_a_route_gives_no_row(self, tmp_path):
        plant(tmp_path, "builder/round-02", None)
        assert rows(tmp_path) == []

    def test_a_file_that_is_not_a_summary_is_skipped_and_named(self, tmp_path, caplog):
        plant(tmp_path, "builder/round-02", LOCAL)
        broken = tmp_path / "calls" / "builder" / "round-03" / "x.summary.json"
        broken.parent.mkdir(parents=True)
        broken.write_text("{not json", encoding="utf-8")
        assert [row.call_ref for row in rows(tmp_path)] == ["calls/builder/round-02/tiered_diff.diff.summary.json"]
        assert "x.summary.json does not read as a summary" in caplog.text


class TestTheLedger:
    def test_the_rows_round_trip_and_a_re_export_replaces_its_own(self, tmp_path):
        plant(tmp_path / "run", "builder/round-02", LOCAL)
        plant(tmp_path / "run", "builder/round-03", LOCAL)
        plant(tmp_path / "run", "reviewer/round-03", DOWN)
        path = tmp_path / "ledger.sqlite"
        assert record_side_role_calls(rows(tmp_path / "run"), path=path) == 3
        record_side_role_calls(rows(tmp_path / "run"), path=path)
        assert query_side_role_calls(path=path) == [
            SideRoleCallSummary(role="summary", route="fallback", cost_basis="unknown", calls=1),
            SideRoleCallSummary(role="summary", route="local", cost_basis="local_zero", calls=2),
        ]

    def test_the_table_carries_its_own_schema_key(self, tmp_path):
        path = tmp_path / "ledger.sqlite"
        record_side_role_calls([], path=path)
        with sqlite3.connect(path) as conn:
            meta = dict(conn.execute("SELECT key, value FROM meta").fetchall())
        assert meta[side_role_calls.SIDE_ROLE_CALLS_SCHEMA_KEY] == "1"

    def test_the_table_admits_only_the_two_bases(self, tmp_path):
        path = tmp_path / "ledger.sqlite"
        plant(tmp_path / "run", "builder/round-02", LOCAL)
        (row,) = rows(tmp_path / "run")
        with pytest.raises(sqlite3.IntegrityError):
            record_side_role_calls([SideRoleCallRow(**{**row.__dict__, "cost_basis": "price_table"})], path=path)


class TestTheEvidence:
    def _run(self, tmp_path, monkeypatch, *routes):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        for role_round, route in routes:
            plant(run_dir("run-1"), role_round, route)
        out = tmp_path / "task_runs" / "T001"
        out.mkdir(parents=True)
        return out, SimpleNamespace(task_id="T001")

    def test_the_file_is_written_read_back_and_mirrored(self, tmp_path, monkeypatch):
        out, task = self._run(tmp_path, monkeypatch, ("builder/round-02", LOCAL))
        written = write_task_side_role_calls({"run_id": "run-1"}, task, out, "task_runs/T001", "proj-1", "job-1")
        assert written == {f"task_runs/T001/{SIDE_ROLE_CALLS_FILENAME}": str(out / SIDE_ROLE_CALLS_FILENAME)}
        on_disk = json.loads((out / SIDE_ROLE_CALLS_FILENAME).read_text(encoding="utf-8"))
        assert [row["cost_basis"] for row in on_disk["rows"]] == ["local_zero"]
        assert rows_from_evidence_file(out / SIDE_ROLE_CALLS_FILENAME) == side_role_call_rows(
            run_dir("run-1"), job_id="job-1", task_id="T001", run_id="run-1")
        assert query_side_role_calls(project_id="proj-1") == [
            SideRoleCallSummary(role="summary", route="local", cost_basis="local_zero", calls=1)]

    def test_no_ledger_target_writes_the_file_and_touches_no_ledger(self, tmp_path, monkeypatch):
        out, task = self._run(tmp_path, monkeypatch, ("builder/round-02", LOCAL))
        written = write_task_side_role_calls({"run_id": "run-1"}, task, out, "task_runs/T001", None, "job-1")
        assert list(written) == [f"task_runs/T001/{SIDE_ROLE_CALLS_FILENAME}"]
        assert not token_ledger_path_for("proj-1").exists()
        assert list((tmp_path / "data").rglob("ledger.sqlite")) == []

    def test_a_run_without_routed_summaries_writes_nothing(self, tmp_path, monkeypatch):
        out, task = self._run(tmp_path, monkeypatch, ("builder/round-02", None))
        assert write_task_side_role_calls({"run_id": "run-1"}, task, out, "task_runs/T001", "p", "job-1") == {}
        assert write_task_side_role_calls({}, task, out, "task_runs/T001", "p", "job-1") == {}
        assert list(out.iterdir()) == []

    def test_a_mirror_that_fails_never_fails_the_export(self, tmp_path, monkeypatch, caplog):
        def broken(rows, **kwargs):
            raise OSError("disk full")

        out, task = self._run(tmp_path, monkeypatch, ("builder/round-02", LOCAL))
        monkeypatch.setattr(side_role_calls, "record_side_role_calls", broken)
        written = write_task_side_role_calls({"run_id": "run-1"}, task, out, "task_runs/T001", "proj-1", "job-1")
        assert list(written) == [f"task_runs/T001/{SIDE_ROLE_CALLS_FILENAME}"]
        assert "side-role call mirror FAILED" in caplog.text

    def test_a_job_export_writes_the_side_role_calls_of_a_real_run(self, monkeypatch, tmp_path):
        from packages.orchestration.job_evidence import _write_task_run_evidence

        result, _, _ = test_tier_escalation.TestARealRun()._run(monkeypatch, tmp_path)
        plant(run_dir(result.run_id), "builder/round-02", LOCAL)
        task = SimpleNamespace(task_id="T001", run_id=result.run_id, task_class="standard_build", status="passed")
        written: dict[str, str] = {}
        _write_task_run_evidence(task, str(tmp_path / "evidence"), written, ledger_project_id="proj-1", job_id="job-1")
        assert f"task_runs/T001/{SIDE_ROLE_CALLS_FILENAME}" in written
        assert query_side_role_calls(project_id="proj-1") == [
            SideRoleCallSummary(role="summary", route="local", cost_basis="local_zero", calls=1)]
