"""A failed `claude` CLI call leaves its cause on disk (finding R-1016).

A self-use run ended ``provider_unavailable`` after 514 seconds and nothing it wrote
named why. Whenever a role's provider call ends in the state that becomes
``provider_unavailable``, the provider's output object, the run record and the job
task's ``final_status_detail`` carry the child's exit code and the last 20 lines of
its standard error, passed through the stream-evidence secret redaction.
"""
from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from packages.orchestration import pingpong_provider
from packages.orchestration.pingpong_job import (
    TaskEntry,
    final_status_detail_of,
)
from packages.orchestration.pingpong_loop import PingPongResult, PingPongRound, export_pingpong_json
from packages.orchestration.pingpong_provider import ClaudeCliProvider

_STDERR = "\n".join([f"line {n}" for n in range(1, 30)] + ["nested session refused"]) + "\n"


def _provider() -> ClaudeCliProvider:
    prov = ClaudeCliProvider()
    prov._claude_path = "/fake/claude"
    prov._cli_version = "1.0.0 (test)"
    prov._cli_version_resolved = True
    return prov


def _failing_child(stderr: str = _STDERR, rc: int = 1):
    proc = MagicMock(returncode=rc, stdout="", stderr=stderr)
    return patch.object(pingpong_provider, "_guarded_cli_run", return_value=proc)


class TestTheProviderOutputCarriesTheChildsExitAndStderr:
    def test_builder(self) -> None:
        with _failing_child():
            out = _provider().build("BUILD")
        assert out.exit_code == 1
        assert "nested session refused" in out.stderr_tail
        assert "exited 1" in out.error and "nested session refused" in out.error

    def test_structured_reviewer(self) -> None:
        with _failing_child():
            out = _provider().review("REVIEW")
        assert out.exit_code == 1
        assert "nested session refused" in out.stderr_tail
        assert "exited 1" in out.error and "nested session refused" in out.error

    def test_free_text_reviewer(self, monkeypatch) -> None:
        monkeypatch.setenv("REMEDY_REVIEWER_FREETEXT", "1")
        with _failing_child():
            out = _provider().review("REVIEW")
        assert out.exit_code == 1
        assert "nested session refused" in out.stderr_tail

    def test_the_tail_is_the_last_twenty_lines(self) -> None:
        with _failing_child():
            out = _provider().build("BUILD")
        lines = out.stderr_tail.splitlines()
        assert len(lines) == 20
        assert lines[0] == "line 11" and lines[-1] == "nested session refused"

    def test_the_tail_is_redacted(self) -> None:
        secret = "ANTHROPIC_API_KEY=sk-ant-api03-abcdefghijklmnopqrstuvwxyz0123456789"
        with _failing_child(stderr=f"boot\n{secret}\nnested session refused\n"):
            out = _provider().build("BUILD")
        assert "sk-ant-api03-abcdefghijklmnopqrstuvwxyz0123456789" not in out.stderr_tail
        assert "sk-ant-api03-abcdefghijklmnopqrstuvwxyz0123456789" not in out.error
        assert "nested session refused" in out.stderr_tail

    def test_a_successful_call_records_no_exit_detail(self) -> None:
        proc = MagicMock(returncode=0, stdout='{"type": "result", "result": "done"}', stderr="noise")
        with patch.object(pingpong_provider, "_guarded_cli_run", return_value=proc):
            out = _provider().build("BUILD")
        assert out.exit_code is None and out.stderr_tail == ""


class TestTheRunRecordCarriesIt:
    def test_the_builder_block_of_the_run_record(self) -> None:
        with _failing_child():
            out = _provider().build("BUILD")
        result = PingPongResult(goal="g")
        result.rounds.append(PingPongRound(round_number=1, builder_output=out))
        builder = export_pingpong_json(result)["rounds"][0]["builder"]
        assert builder["exit_code"] == 1
        assert "nested session refused" in builder["stderr_tail"]

    def test_an_ordinary_round_gains_no_keys(self) -> None:
        out = pingpong_provider.BuilderOutput(summary="ok", provider="fake")
        result = PingPongResult(goal="g")
        result.rounds.append(PingPongRound(round_number=1, builder_output=out))
        builder = export_pingpong_json(result)["rounds"][0]["builder"]
        assert "exit_code" not in builder and "stderr_tail" not in builder


class TestTheJobTaskCarriesIt:
    def test_provider_unavailable_carries_the_run_error(self) -> None:
        result = SimpleNamespace(
            final_status="provider_unavailable",
            error="provider_error: RuntimeError: claude CLI exited 1: nested session refused")
        assert "exited 1" in final_status_detail_of(result)
        assert "nested session refused" in final_status_detail_of(result)

    def test_other_outcomes_carry_nothing(self) -> None:
        result = SimpleNamespace(final_status="staged_review_passed", error="")
        assert final_status_detail_of(result) == ""

    def test_the_detail_survives_the_job_file_round_trip(self) -> None:
        from packages.orchestration.pingpong_job import JobPlan, _export_job, _import_job
        job = JobPlan(job_id="j1")
        job.tasks.append(TaskEntry(task_id="T001", title="t",
                                   final_status="provider_unavailable",
                                   final_status_detail="claude CLI exited 1: nested session refused"))
        again = _import_job(_export_job(job))
        assert again.tasks[0].final_status_detail == "claude CLI exited 1: nested session refused"
