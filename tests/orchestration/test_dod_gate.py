"""F061 T004 — the job-end gate, the matrix, and the end-to-end proof.

What the order requires proof of:

  * a job goes green ONLY when every blocking check is green;
  * a red BLOCKING check holds the job open — status blocked, matrix present;
  * the SAME job releases after the fix;
  * a non-blocking red is reported, never gating;
  * the report renders the check matrix from the recorded evidence.

This is the gate in isolation. The job runner's end-to-end gate is
tests/orchestration/test_pingpong_job_dod_gate.py.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from packages.orchestration.dod_gate import (
    BLOCKER_PREFIX,
    DOD_FILENAME,
    MATRIX_HEADER,
    REASON_NO_RUNNER,
    GateResult,
    dod_path,
    evaluate_dod,
    gate_blocker,
    load_dod,
    load_gate_result,
    matrix_rows,
    render_matrix,
    result_path,
    run_job_gate,
    store_dod,
)
from packages.orchestration.dod_schema import DOD_SCHEMA_V, DoD, DoDCheck

EXIT_OK = ["python3", "-c", "print('gate ok')"]
EXIT_BAD = ["python3", "-c", "import sys; print('gate boom'); sys.exit(4)"]


def cmd_check(check_id: str, argv: list[str], *, blocking: bool = True) -> DoDCheck:
    return DoDCheck(id=check_id, kind="custom_cmd", spec={"argv": argv},
                    blocking=blocking, source="compiled")


def dod_of(*checks: DoDCheck, compiled: bool = True) -> DoD:
    return DoD(
        schema_v=DOD_SCHEMA_V,
        checks=list(checks),
        compiled=compiled,
        origin="provider" if compiled else "deterministic",
    )


@pytest.fixture
def data_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A private data root, so no test ever touches the real evidence area."""
    root = tmp_path / "data"
    root.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    return root


# ---------------------------------------------------------------------------
# The rule
# ---------------------------------------------------------------------------

class TestGateRule:
    def test_all_blocking_green_releases(self, tmp_path: Path):
        result = evaluate_dod(
            dod_of(cmd_check("a", EXIT_OK), cmd_check("b", EXIT_OK)), tmp_path)
        assert result.released is True
        assert result.blocked is False
        assert result.blocking_red == ()
        assert [e.status for e in result.evidence] == ["passed", "passed"]

    def test_one_red_blocking_check_holds(self, tmp_path: Path):
        result = evaluate_dod(
            dod_of(cmd_check("a", EXIT_OK), cmd_check("bad", EXIT_BAD)), tmp_path)
        assert result.released is False
        assert result.blocked is True
        assert result.blocking_red == ("bad",)

    def test_a_non_blocking_red_is_reported_not_gating(self, tmp_path: Path):
        result = evaluate_dod(
            dod_of(cmd_check("a", EXIT_OK),
                   cmd_check("soft", EXIT_BAD, blocking=False)), tmp_path)
        assert result.released is True, "a non-blocking red must not gate"
        assert result.blocking_red == ()
        assert result.reported_red == ("soft",)

    def test_every_check_runs_even_after_a_red_one(self, tmp_path: Path):
        """The matrix has to be complete; stopping at the first red hides work."""
        result = evaluate_dod(
            dod_of(cmd_check("first", EXIT_BAD), cmd_check("second", EXIT_OK)),
            tmp_path)
        assert [e.check_id for e in result.evidence] == ["first", "second"]
        assert [e.status for e in result.evidence] == ["failed", "passed"]

    def test_a_kind_with_no_runner_holds_rather_than_crashing(self, tmp_path: Path):
        """Unrunnable is not green — and it does not take the job down either."""
        unsupported = DoDCheck.model_construct(
            id="mystery", kind="telepathy", spec={}, blocking=True,
            acceptance_refs=[], description="", source="compiled")
        dod = DoD.model_construct(
            schema_v=DOD_SCHEMA_V, compiled=True, origin="provider",
            checks=[cmd_check("a", EXIT_OK), unsupported])

        result = evaluate_dod(dod, tmp_path)
        assert result.released is False
        assert result.blocking_red == ("mystery",)
        assert result.evidence[1].reason == REASON_NO_RUNNER

    def test_gate_blocker_names_the_red_checks(self, tmp_path: Path):
        result = evaluate_dod(dod_of(cmd_check("bad", EXIT_BAD)), tmp_path)
        blocker = gate_blocker(result)
        assert blocker.startswith(BLOCKER_PREFIX)
        assert "bad" in blocker

    def test_gate_blocker_is_empty_for_a_released_gate(self, tmp_path: Path):
        assert gate_blocker(evaluate_dod(dod_of(cmd_check("a", EXIT_OK)),
                                         tmp_path)) == ""
        assert gate_blocker(None) == ""


# ---------------------------------------------------------------------------
# Storage in the job's evidence area
# ---------------------------------------------------------------------------

class TestJobGate:
    def test_a_job_without_a_dod_is_not_gated(self, data_root: Path, tmp_path: Path):
        """The whole feature is additive: no DoD, no gate, no behaviour change."""
        assert run_job_gate("11111111-1111-4111-8111-111111111111", tmp_path) is None

    def test_the_dod_and_its_result_live_under_the_data_root(
            self, data_root: Path, tmp_path: Path):
        job_id = "22222222-2222-4222-8222-222222222222"
        stored = store_dod(job_id, dod_of(cmd_check("a", EXIT_OK)))

        assert stored == dod_path(job_id)
        assert data_root in stored.parents, "the DoD must live in the data root"
        assert tmp_path not in Path(str(stored).replace(str(data_root), "x")).parents

        run_job_gate(job_id, tmp_path)
        assert result_path(job_id).is_file()
        assert data_root in result_path(job_id).parents

    def test_round_trip_and_recorded_result(self, data_root: Path, tmp_path: Path):
        job_id = "33333333-3333-4333-8333-333333333333"
        dod = dod_of(cmd_check("a", EXIT_OK), cmd_check("soft", EXIT_BAD,
                                                        blocking=False))
        store_dod(job_id, dod)
        assert load_dod(job_id) == dod

        result = run_job_gate(job_id, tmp_path)
        assert result is not None and result.released is True

        recorded = load_gate_result(job_id)
        assert recorded is not None
        assert recorded["released"] is True
        assert recorded["reported_red"] == ["soft"]
        assert [c["check_id"] for c in recorded["checks"]] == ["a", "soft"]
        assert recorded["checks"][0]["command"] == " ".join(EXIT_OK)

    def test_an_unreadable_dod_holds_the_job(self, data_root: Path, tmp_path: Path):
        """A corrupt definition of done releases nothing. Fail closed."""
        job_id = "44444444-4444-4444-8444-444444444444"
        store_dod(job_id, dod_of(cmd_check("a", EXIT_OK)))
        dod_path(job_id).write_text("{ not json", encoding="utf-8")

        result = run_job_gate(job_id, tmp_path)
        assert result is not None
        assert result.released is False
        assert DOD_FILENAME in result.error
        assert gate_blocker(result).startswith(BLOCKER_PREFIX)

    def test_re_running_the_gate_overwrites_the_previous_result(
            self, data_root: Path, tmp_path: Path):
        """The matrix always describes the LAST run, never a stale one."""
        job_id = "55555555-5555-4555-8555-555555555555"
        store_dod(job_id, dod_of(cmd_check("a", EXIT_BAD)))
        assert run_job_gate(job_id, tmp_path).released is False

        store_dod(job_id, dod_of(cmd_check("a", EXIT_OK)))
        assert run_job_gate(job_id, tmp_path).released is True
        assert load_gate_result(job_id)["released"] is True


# ---------------------------------------------------------------------------
# The matrix
# ---------------------------------------------------------------------------

class TestMatrix:
    def test_rows_carry_the_ordered_columns(self, tmp_path: Path):
        result = evaluate_dod(
            dod_of(cmd_check("a", EXIT_OK),
                   cmd_check("soft", EXIT_BAD, blocking=False)), tmp_path)
        rows = matrix_rows(result)
        assert len(MATRIX_HEADER) == 6
        assert rows[0][:5] == ("a", "custom_cmd", "yes", "passed", "-")
        assert rows[1][:5] == ("soft", "custom_cmd", "no", "failed", "nonzero_exit")
        assert rows[0][5].endswith("ms")

    def test_rows_read_the_same_from_the_stored_json(self, tmp_path: Path):
        result = evaluate_dod(dod_of(cmd_check("a", EXIT_OK)), tmp_path)
        assert matrix_rows(result) == matrix_rows(
            json.loads(json.dumps(result.to_json())))

    def test_render_says_so_when_there_is_no_matrix(self):
        assert "No Definition of Done" in render_matrix(None)
        assert "No Definition of Done" in render_matrix(GateResult(released=True))

    def test_render_is_a_markdown_table(self, tmp_path: Path):
        table = render_matrix(evaluate_dod(dod_of(cmd_check("a", EXIT_OK)), tmp_path))
        assert table.splitlines()[0].startswith("| check | kind |")
        assert "| a | custom_cmd | yes | passed |" in table


# ---------------------------------------------------------------------------
# The report section
# ---------------------------------------------------------------------------

class TestReportMatrix:
    def test_report_renders_the_matrix_from_recorded_evidence(self):
        from packages.orchestration.run_report import (
            MODE_FINAL,
            DoDCheckRow,
            ReportSources,
            render_report_from_sources,
        )

        report = render_report_from_sources(ReportSources(
            job_id="abc", dod_released=False,
            dod_checks=(
                DoDCheckRow("tests", "pytest", True, "failed", "nonzero_exit", 120),
                DoDCheckRow("lint", "lint", False, "failed", "tool_unavailable", 3),
            ),
        ), mode=MODE_FINAL)

        assert "## Definition of Done" in report
        assert "The gate is HOLDING this job open: 1 blocking check(s) red" in report
        assert "| `tests` | pytest | yes | **failed** | nonzero_exit | 120ms |" in report
        assert "| `lint` | lint | no | **failed** | tool_unavailable | 3ms |" in report

    def test_report_says_not_recorded_when_a_job_was_never_gated(self):
        from packages.orchestration.run_report import (
            MODE_FINAL,
            ReportSources,
            render_report_from_sources,
        )

        report = render_report_from_sources(ReportSources(job_id="abc"),
                                            mode=MODE_FINAL)
        assert "## Definition of Done" in report
        assert "Definition of Done: not recorded." in report

    def test_a_released_gate_says_so(self):
        from packages.orchestration.run_report import (
            MODE_FINAL,
            DoDCheckRow,
            ReportSources,
            render_report_from_sources,
        )

        report = render_report_from_sources(ReportSources(
            job_id="abc", dod_released=True,
            dod_checks=(DoDCheckRow("tests", "pytest", True, "passed", "", 9),),
        ), mode=MODE_FINAL)
        assert "the gate released" in report


# ---------------------------------------------------------------------------
# The `dod` section of `remedy job show <id> --full` (formerly its own command)
# ---------------------------------------------------------------------------

class TestJobDodCommand:
    def _job(self, tmp_path: Path):
        from packages.orchestration.pingpong_job import JobPlan, save_job_plan

        job = JobPlan(job_title="dod cli", metadata={})
        save_job_plan(job, root=tmp_path)
        return job

    def _show(self, capsys, job_id: str):
        """`job show <id> --full`: the dod section's envelope, and its text (the last section) on stderr."""
        from apps.cli.grouped import main

        main(["job", "show", job_id, "--full"])
        shown = capsys.readouterr()
        return json.loads(shown.out)["sections"]["dod"], shown.err.split("--- Dod ---\n", 1)[1]

    def _text(self, capsys, job_id: str) -> str:
        return self._show(capsys, job_id)[1]

    def test_a_job_with_no_dod_says_so(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = self._job(tmp_path)
        section, text = self._show(capsys, str(job.job_id))
        assert "no Definition of Done" in text
        assert section == {"ok": True, "data": {
            "job_id": str(job.job_id), "compiled": None, "origin": None, "check_count": 0, "gate": None}}

    def test_a_compiled_dod_that_has_not_run_lists_the_checks(
            self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = self._job(tmp_path)
        store_dod(str(job.job_id), dod_of(cmd_check("smoke", EXIT_OK)))

        out = self._text(capsys, str(job.job_id))
        assert "compiled, 1 check(s), 1 blocking" in out
        assert "The gate has not run yet" in out
        assert "smoke" in out

    def test_the_matrix_is_shown_after_the_gate_ran(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = self._job(tmp_path)
        store_dod(str(job.job_id), dod_of(
            cmd_check("smoke", EXIT_BAD),
            cmd_check("soft", EXIT_BAD, blocking=False)))
        run_job_gate(str(job.job_id), tmp_path)

        out = self._text(capsys, str(job.job_id))
        for column in MATRIX_HEADER:
            assert column in out
        assert "Gate: HOLDING — blocking check(s) red: smoke" in out
        assert "Non-blocking reds (reported, not gating): soft" in out

    def test_a_released_gate_reads_as_released(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = self._job(tmp_path)
        store_dod(str(job.job_id), dod_of(cmd_check("smoke", EXIT_OK)))
        run_job_gate(str(job.job_id), tmp_path)

        assert "Gate: RELEASED" in self._text(capsys, str(job.job_id))

    def test_json_output_carries_the_gate_record(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = self._job(tmp_path)
        store_dod(str(job.job_id), dod_of(cmd_check("smoke", EXIT_OK)))
        run_job_gate(str(job.job_id), tmp_path)

        section, _text = self._show(capsys, str(job.job_id))
        payload = section["data"]
        assert section["ok"] is True
        assert payload["compiled"] is True
        assert payload["check_count"] == 1
        assert payload["gate"]["released"] is True
        assert payload["gate"]["checks"][0]["check_id"] == "smoke"

    def test_an_unknown_job_exits_cleanly(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        with pytest.raises(SystemExit) as exc:
            self._show(capsys, "99999999-9999-4999-8999-999999999999")
        assert exc.value.code == 1

    def test_the_command_is_read_only_and_runs_nothing(self, tmp_path, monkeypatch, capsys):
        """It shows the LAST gate run; it never starts a check of its own."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = self._job(tmp_path)
        store_dod(str(job.job_id), dod_of(cmd_check("smoke", EXIT_OK)))

        self._show(capsys, str(job.job_id))
        assert load_gate_result(str(job.job_id)) is None, (
            "the CLI must not have run the gate")
