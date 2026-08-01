"""F061 T004 — the job-end gate, the matrix, and the end-to-end proof.

What the order requires proof of:

  * a job goes green ONLY when every blocking check is green;
  * a red BLOCKING check holds the job open — status blocked, matrix present;
  * the SAME job releases after the fix;
  * a non-blocking red is reported, never gating;
  * the report renders the check matrix from the recorded evidence.

The end-to-end part drives the real ``run_job_fulfill`` spine against a fixture
repo — no provider, no network. Everything else is the gate in isolation.
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
# End to end, through the real fulfillment spine
# ---------------------------------------------------------------------------

class TestEndToEnd:
    """The whole point: a job ends green only when its blocking checks do.

    Drives the real ``run_job_fulfill`` — the same entry point the CLI uses —
    against a fixture repo. No provider, no network.
    """

    def _job(self, tmp_path: Path):
        from packages.core.models import Job
        from packages.orchestration.job_fulfillment import create_demo_repo
        from packages.orchestration.storage import save_job

        repo = create_demo_repo(tmp_path)
        job = Job(name="dod gate e2e", metadata={"target_repo": str(repo)})
        save_job(job, root=tmp_path)
        return job, repo

    def _fulfill(self, job_id: str, repo: Path, tmp_path: Path):
        from packages.orchestration.job_fulfillment import run_job_fulfill
        return run_job_fulfill(job_id, repo, data_dir=tmp_path)

    def _job_state(self, job_id: str, tmp_path: Path) -> str:
        from uuid import UUID

        from packages.orchestration.storage import load_job
        job = load_job(UUID(job_id), tmp_path)
        return job.state.value if hasattr(job.state, "value") else str(job.state)

    def test_a_job_without_a_dod_still_ends_green(self, tmp_path, monkeypatch):
        """The gate is additive: it cannot change a job it was never given."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job, repo = self._job(tmp_path)

        record = self._fulfill(str(job.id), repo, tmp_path)

        assert record.status.value == "completed_verified"
        assert record.dod_released is None, "never gated"
        assert self._job_state(str(job.id), tmp_path) == "completed"

    def test_all_blocking_green_lets_the_job_end_green(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job, repo = self._job(tmp_path)
        store_dod(str(job.id), dod_of(cmd_check("smoke", EXIT_OK)))

        record = self._fulfill(str(job.id), repo, tmp_path)

        assert record.dod_released is True
        assert record.status.value == "completed_verified"
        assert record.contract_blockers == []
        assert self._job_state(str(job.id), tmp_path) == "completed"

    def test_a_red_blocking_check_holds_the_job_open(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job, repo = self._job(tmp_path)
        store_dod(str(job.id), dod_of(cmd_check("smoke", EXIT_BAD)))

        record = self._fulfill(str(job.id), repo, tmp_path)

        assert record.dod_released is False
        assert record.dod_blocking_red == ["smoke"]
        assert record.status.value == "blocked"
        assert any(b.startswith(BLOCKER_PREFIX) for b in record.contract_blockers)
        # Held OPEN, not completed.
        assert self._job_state(str(job.id), tmp_path) != "completed"
        # And the matrix is there to say why.
        recorded = load_gate_result(str(job.id))
        assert recorded is not None and recorded["released"] is False
        assert matrix_rows(recorded)[0][3] == "failed"

    def test_the_same_job_releases_after_the_fix(self, tmp_path, monkeypatch):
        """The gate holds, the check is fixed, the gate releases. Same job."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job, repo = self._job(tmp_path)
        store_dod(str(job.id), dod_of(cmd_check("smoke", EXIT_BAD)))

        held = self._fulfill(str(job.id), repo, tmp_path)
        assert held.status.value == "blocked"
        assert self._job_state(str(job.id), tmp_path) != "completed"

        # The fix: the same check, now green.
        store_dod(str(job.id), dod_of(cmd_check("smoke", EXIT_OK)))
        released = self._fulfill(str(job.id), repo, tmp_path)

        assert released.dod_released is True
        assert released.status.value == "completed_verified"
        assert self._job_state(str(job.id), tmp_path) == "completed"

    def test_a_non_blocking_red_does_not_hold_the_job(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job, repo = self._job(tmp_path)
        store_dod(str(job.id), dod_of(
            cmd_check("smoke", EXIT_OK),
            cmd_check("nice-to-have", EXIT_BAD, blocking=False)))

        record = self._fulfill(str(job.id), repo, tmp_path)

        assert record.dod_released is True
        assert record.dod_reported_red == ["nice-to-have"]
        assert record.status.value == "completed_verified"
        assert self._job_state(str(job.id), tmp_path) == "completed"

    def test_the_gate_run_is_recorded_on_the_timeline(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job, repo = self._job(tmp_path)
        store_dod(str(job.id), dod_of(cmd_check("smoke", EXIT_OK)))
        self._fulfill(str(job.id), repo, tmp_path)

        from packages.orchestration.timeline import load_run_events
        events = [e for e in load_run_events(tmp_path, job.id)
                  if e.get("event") == "dod_gate_evaluated"]
        assert len(events) == 1
        assert events[0]["metadata"]["released"] is True


# ---------------------------------------------------------------------------
# `remedy job dod <id>`
# ---------------------------------------------------------------------------

class TestJobDodCommand:
    def _job(self, tmp_path: Path):
        from packages.core.models import Job
        from packages.orchestration.storage import save_job

        job = Job(name="dod cli", metadata={})
        save_job(job, root=tmp_path)
        return job

    def _run(self, job_id: str, *, json_output: bool = False) -> str:
        import contextlib
        import io

        from apps.cli.commands.job import _cmd_job_dod

        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            _cmd_job_dod(job_id, json_output=json_output)
        return buf.getvalue()

    def test_a_job_with_no_dod_says_so(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = self._job(tmp_path)
        assert "no Definition of Done" in self._run(str(job.id))

    def test_a_compiled_dod_that_has_not_run_lists_the_checks(
            self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = self._job(tmp_path)
        store_dod(str(job.id), dod_of(cmd_check("smoke", EXIT_OK)))

        out = self._run(str(job.id))
        assert "compiled, 1 check(s), 1 blocking" in out
        assert "The gate has not run yet" in out
        assert "smoke" in out

    def test_the_matrix_is_shown_after_the_gate_ran(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = self._job(tmp_path)
        store_dod(str(job.id), dod_of(
            cmd_check("smoke", EXIT_BAD),
            cmd_check("soft", EXIT_BAD, blocking=False)))
        run_job_gate(str(job.id), tmp_path)

        out = self._run(str(job.id))
        for column in MATRIX_HEADER:
            assert column in out
        assert "Gate: HOLDING — blocking check(s) red: smoke" in out
        assert "Non-blocking reds (reported, not gating): soft" in out

    def test_a_released_gate_reads_as_released(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = self._job(tmp_path)
        store_dod(str(job.id), dod_of(cmd_check("smoke", EXIT_OK)))
        run_job_gate(str(job.id), tmp_path)

        assert "Gate: RELEASED" in self._run(str(job.id))

    def test_json_output_carries_the_gate_record(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = self._job(tmp_path)
        store_dod(str(job.id), dod_of(cmd_check("smoke", EXIT_OK)))
        run_job_gate(str(job.id), tmp_path)

        payload = json.loads(self._run(str(job.id), json_output=True))
        assert payload["compiled"] is True
        assert payload["check_count"] == 1
        assert payload["gate"]["released"] is True
        assert payload["gate"]["checks"][0]["check_id"] == "smoke"

    def test_an_unknown_job_exits_cleanly(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        with pytest.raises(SystemExit) as exc:
            self._run("99999999-9999-4999-8999-999999999999")
        assert exc.value.code == 1

    def test_the_command_is_read_only_and_runs_nothing(self, tmp_path, monkeypatch):
        """It shows the LAST gate run; it never starts a check of its own."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = self._job(tmp_path)
        store_dod(str(job.id), dod_of(cmd_check("smoke", EXIT_OK)))

        self._run(str(job.id))
        assert load_gate_result(str(job.id)) is None, (
            "the CLI must not have run the gate")
