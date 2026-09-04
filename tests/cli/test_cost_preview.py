"""F114 T003 — acceptance tests for job.run's cost-preview behavior.

Unlike tests/orchestration/test_long_run_executor.py's own gate tests
(which mock confirm_cost_preview itself to isolate the wiring), these
exercise the REAL confirm_cost_preview end to end through job.run, per
docs/roadmap/features/T3_F114.md's acceptance section: a pipe exits with
the --yes hint, --yes proceeds audited, and every printed estimate
carries its basis label.
"""
from __future__ import annotations

import pytest


class TestJobRunCostPreviewAcceptance:
    def test_non_tty_without_yes_exits_with_the_job_run_hint(self, monkeypatch):
        from apps.cli.commands import job as job_cmd

        monkeypatch.setattr("apps.cli.cost_preview_confirm._stdin_is_a_tty", lambda: False)
        ran: list[str] = []
        monkeypatch.setattr(job_cmd, "_cmd_run_next_task_local", ran.append)

        with pytest.raises(SystemExit) as exc:
            job_cmd._cmd_job_run_cycles("abc12345")

        assert exc.value.code == 2
        assert ran == []

    def test_non_tty_without_yes_names_job_run_in_the_hint(self, monkeypatch, capsys):
        from apps.cli.commands import job as job_cmd

        monkeypatch.setattr("apps.cli.cost_preview_confirm._stdin_is_a_tty", lambda: False)
        monkeypatch.setattr(job_cmd, "_cmd_run_next_task_local", lambda _: None)

        with pytest.raises(SystemExit):
            job_cmd._cmd_job_run_cycles("abc12345")

        err = capsys.readouterr().err
        assert "--yes" in err
        assert "job.run" in err

    def test_yes_flag_proceeds_through_the_real_gate_without_a_tty(self, monkeypatch):
        from apps.cli.commands import job as job_cmd

        monkeypatch.setattr("apps.cli.cost_preview_confirm._stdin_is_a_tty", lambda: False)
        ran: list[str] = []
        monkeypatch.setattr(job_cmd, "_cmd_run_next_task_local", ran.append)

        job_cmd._cmd_job_run_cycles("abc12345", yes=True)

        assert ran == ["abc12345"]

    def test_unattended_proceeds_through_the_real_gate_without_a_tty(self, monkeypatch):
        from apps.cli.commands import job as job_cmd

        monkeypatch.setattr("apps.cli.cost_preview_confirm._stdin_is_a_tty", lambda: False)
        ran: list[str] = []
        monkeypatch.setattr(job_cmd, "_cmd_run_next_task_local", ran.append)

        job_cmd._cmd_job_run_cycles("abc12345", unattended=True)

        assert ran == ["abc12345"]

    def test_the_printed_preview_line_carries_its_basis_label(self, monkeypatch, capsys):
        # A9: every shown number carries its basis label - job.run's own
        # printed line is no exception, even in the unavailable case.
        from apps.cli.commands import job as job_cmd

        monkeypatch.setattr(job_cmd, "_cmd_run_next_task_local", lambda _: None)

        job_cmd._cmd_job_run_cycles("abc12345", yes=True)

        out = capsys.readouterr().out
        assert "basis:" in out
        assert "estimate_unavailable" in out
