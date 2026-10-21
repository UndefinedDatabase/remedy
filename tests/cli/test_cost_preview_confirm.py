"""F114 T002 — tests for the shared cost-preview confirmation helper.

Covers `render_estimate_line` / `confirm_cost_preview` in
`apps.cli.cost_preview_confirm`, mocking `_stdin_is_a_tty` and
`builtins.input`.
"""
from __future__ import annotations

import json

import pytest

from apps.cli import cost_preview_confirm as cpc
from packages.orchestration.cost_preview import CostBandEstimate
from packages.orchestration.data_paths import job_dir, resolve_data_root
from packages.orchestration.permission_matrix import JOB_LEVEL_FILENAME, PERMISSION_GRANTS_FILENAME

AVAILABLE = CostBandEstimate(0.16, 2.40, "class defaults (low/high) x price=0.02", {})
UNAVAILABLE = CostBandEstimate(None, None, "estimate_unavailable", {})


def _pin_level(root, job_id: str, level: str) -> None:
    """Pin ``job_id``'s autonomy level under ``root``, as `pin_job_level` would write it."""
    folder = job_dir(job_id, root)
    folder.mkdir(parents=True, exist_ok=True)
    (folder / JOB_LEVEL_FILENAME).write_text(json.dumps({"level": level}), encoding="utf-8")


def _grant_lines(root) -> list[dict]:
    path = root / "autonomy" / PERMISSION_GRANTS_FILENAME
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


class TestRenderEstimateLine:
    def test_available_estimate_shows_the_band_and_basis(self):
        line = cpc.render_estimate_line(AVAILABLE)
        assert "$0.1600" in line
        assert "$2.4000" in line
        assert "class defaults (low/high) x price=0.02" in line

    def test_unavailable_estimate_says_so_and_still_carries_a_basis(self):
        line = cpc.render_estimate_line(UNAVAILABLE)
        assert "unavailable" in line
        assert "estimate_unavailable" in line


class TestUnderThreshold:
    def test_under_threshold_proceeds_without_any_prompt(self, capsys):
        result = cpc.confirm_cost_preview(
            AVAILABLE, confirm_above_usd=10.0, yes=False, command_name="do")
        assert result is True
        assert "estimated" in capsys.readouterr().out

    def test_under_threshold_never_touches_stdin(self, monkeypatch, capsys):
        monkeypatch.setattr(cpc, "_stdin_is_a_tty", lambda: (_ for _ in ()).throw(
            AssertionError("must not be called when under threshold")))
        cpc.confirm_cost_preview(
            AVAILABLE, confirm_above_usd=10.0, yes=False, command_name="do")


class TestOverThresholdWithYes:
    def test_yes_skips_the_prompt_and_proceeds(self, capsys):
        result = cpc.confirm_cost_preview(
            AVAILABLE, confirm_above_usd=0.5, yes=True, command_name="do")
        assert result is True
        out = capsys.readouterr().out
        assert "--yes" in out

    def test_yes_never_touches_stdin(self, monkeypatch):
        monkeypatch.setattr(cpc, "_stdin_is_a_tty", lambda: (_ for _ in ()).throw(
            AssertionError("must not be called when --yes")))
        cpc.confirm_cost_preview(
            AVAILABLE, confirm_above_usd=0.5, yes=True, command_name="do")


class TestOverThresholdNonTty:
    def test_non_tty_exits_with_usage_code_never_hangs(self, monkeypatch, capsys):
        monkeypatch.setattr(cpc, "_stdin_is_a_tty", lambda: False)
        with pytest.raises(SystemExit) as exc:
            cpc.confirm_cost_preview(
                AVAILABLE, confirm_above_usd=0.5, yes=False, command_name="do")
        assert exc.value.code == cpc.EXIT_USAGE
        assert exc.value.code != 0
        err = capsys.readouterr().err
        assert "--yes" in err
        assert "do" in err

    def test_non_tty_never_calls_input(self, monkeypatch):
        monkeypatch.setattr(cpc, "_stdin_is_a_tty", lambda: False)
        monkeypatch.setattr("builtins.input", lambda prompt="": (_ for _ in ()).throw(
            AssertionError("must not prompt on non-tty")))
        with pytest.raises(SystemExit):
            cpc.confirm_cost_preview(
                AVAILABLE, confirm_above_usd=0.5, yes=False, command_name="do")


class TestOverThresholdTty:
    def test_tty_answering_yes_proceeds(self, monkeypatch):
        monkeypatch.setattr(cpc, "_stdin_is_a_tty", lambda: True)
        monkeypatch.setattr("builtins.input", lambda prompt="": "y")
        result = cpc.confirm_cost_preview(
            AVAILABLE, confirm_above_usd=0.5, yes=False, command_name="do")
        assert result is True

    def test_tty_declining_returns_false_without_raising(self, monkeypatch):
        monkeypatch.setattr(cpc, "_stdin_is_a_tty", lambda: True)
        monkeypatch.setattr("builtins.input", lambda prompt="": "n")
        result = cpc.confirm_cost_preview(
            AVAILABLE, confirm_above_usd=0.5, yes=False, command_name="do")
        assert result is False


class TestUnavailableIsTreatedAsExpensive:
    def test_unavailable_estimate_requires_confirmation_even_at_a_huge_threshold(
            self, monkeypatch):
        monkeypatch.setattr(cpc, "_stdin_is_a_tty", lambda: False)
        with pytest.raises(SystemExit) as exc:
            cpc.confirm_cost_preview(
                UNAVAILABLE, confirm_above_usd=999999.0, yes=False, command_name="do")
        assert exc.value.code == cpc.EXIT_USAGE

    def test_unavailable_estimate_with_yes_still_proceeds(self):
        result = cpc.confirm_cost_preview(
            UNAVAILABLE, confirm_above_usd=999999.0, yes=True, command_name="do")
        assert result is True


class TestAsksThePermissionMatrix:
    """DECISION F141 D5 (2): a proceeding expensive estimate asks `expensive`, auditing the
    approval that let it through. A data root under `tmp_path`, so nothing here touches the
    real one."""

    def test_yes_with_a_job_pinned_at_l2_records_one_flag_grant(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        root = resolve_data_root()
        _pin_level(root, "job-l2", "L2")

        result = cpc.confirm_cost_preview(
            AVAILABLE, confirm_above_usd=0.5, yes=True, command_name="job.resume",
            job_id="job-l2")

        assert result is True
        lines = _grant_lines(root)
        assert len(lines) == 1
        line = lines[0]
        assert line["action"] == "expensive"
        assert line["approval_kind"] == "flag"
        assert line["approval_ref"] == "--yes"
        assert line["job_id"] == "job-l2"

    def test_yes_flag_unattended_records_that_ref(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        root = resolve_data_root()
        _pin_level(root, "job-l2", "L2")

        result = cpc.confirm_cost_preview(
            AVAILABLE, confirm_above_usd=0.5, yes=True, command_name="job.resume",
            job_id="job-l2", yes_flag="--unattended")

        assert result is True
        lines = _grant_lines(root)
        assert len(lines) == 1
        assert lines[0]["approval_ref"] == "--unattended"

    def test_prompt_y_records_kind_prompt_and_the_command_name(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        root = resolve_data_root()
        _pin_level(root, "job-l2", "L2")
        monkeypatch.setattr(cpc, "_stdin_is_a_tty", lambda: True)
        monkeypatch.setattr("builtins.input", lambda prompt="": "y")

        result = cpc.confirm_cost_preview(
            AVAILABLE, confirm_above_usd=0.5, yes=False, command_name="job.resume",
            job_id="job-l2")

        assert result is True
        lines = _grant_lines(root)
        assert len(lines) == 1
        line = lines[0]
        assert line["action"] == "expensive"
        assert line["approval_kind"] == "prompt"
        assert line["approval_ref"] == "job.resume"
        assert line["job_id"] == "job-l2"

    def test_declined_prompt_cheap_estimate_and_missing_terminal_record_nothing(
            self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        root = resolve_data_root()
        _pin_level(root, "job-l2", "L2")

        monkeypatch.setattr(cpc, "_stdin_is_a_tty", lambda: True)
        monkeypatch.setattr("builtins.input", lambda prompt="": "n")
        declined = cpc.confirm_cost_preview(
            AVAILABLE, confirm_above_usd=0.5, yes=False, command_name="job.resume",
            job_id="job-l2")
        assert declined is False
        assert _grant_lines(root) == []

        cheap = cpc.confirm_cost_preview(
            AVAILABLE, confirm_above_usd=10.0, yes=False, command_name="job.resume",
            job_id="job-l2")
        assert cheap is True
        assert _grant_lines(root) == []

        monkeypatch.setattr(cpc, "_stdin_is_a_tty", lambda: False)
        with pytest.raises(SystemExit):
            cpc.confirm_cost_preview(
                AVAILABLE, confirm_above_usd=0.5, yes=False, command_name="job.resume",
                job_id="job-l2")
        assert _grant_lines(root) == []

    def test_job_pinned_at_l5_proceeds_on_yes_and_records_nothing_but_still_prompts(
            self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        root = resolve_data_root()
        _pin_level(root, "job-l5", "L5")

        result = cpc.confirm_cost_preview(
            AVAILABLE, confirm_above_usd=0.5, yes=True, command_name="job.resume",
            job_id="job-l5")
        assert result is True
        assert _grant_lines(root) == []

        monkeypatch.setattr(cpc, "_stdin_is_a_tty", lambda: True)
        monkeypatch.setattr("builtins.input", lambda prompt="": "y")
        result = cpc.confirm_cost_preview(
            AVAILABLE, confirm_above_usd=0.5, yes=False, command_name="job.resume",
            job_id="job-l5")
        assert result is True
        assert _grant_lines(root) == []


class TestJsonOutputKeepsStdoutTheOneParseableObject:
    """DECISION F283 D2 — under `json_output=True` every human line moves to
    stderr, and the non-terminal refusal answers through `fail()` instead of
    printing its own `Error: ` line."""

    def test_yes_under_json_writes_nothing_to_stdout_and_the_line_to_stderr(
            self, capsys):
        result = cpc.confirm_cost_preview(
            AVAILABLE, confirm_above_usd=0.5, yes=True, command_name="do",
            json_output=True)
        assert result is True
        captured = capsys.readouterr()
        assert captured.out == ""
        assert "--yes" in captured.err

    def test_non_tty_under_json_exits_usage_with_empty_stderr_and_an_envelope(
            self, monkeypatch, capsys):
        monkeypatch.setattr(cpc, "_stdin_is_a_tty", lambda: False)
        with pytest.raises(SystemExit) as exc:
            cpc.confirm_cost_preview(
                AVAILABLE, confirm_above_usd=0.5, yes=False, command_name="do",
                json_output=True)
        assert exc.value.code == cpc.EXIT_USAGE
        captured = capsys.readouterr()
        assert captured.err == ""
        body = json.loads(captured.out)
        assert body["ok"] is False
        assert body["error"] == "confirmation_required"
        assert "do" in body["message"]


# ── F295 T003: on a real open pipe, the confirmation never reads stdin ───────

#: Run as its own process whose stdin is an open pipe: the confirmation for an
#: unavailable estimate, which always asks, with `--yes` given or not (argv[1]).
_CONFIRM_ON_AN_OPEN_PIPE = (
    "import sys\n"
    "from apps.cli.cost_preview_confirm import confirm_cost_preview\n"
    "from packages.orchestration.cost_preview import CostBandEstimate\n"
    "proceed = confirm_cost_preview(CostBandEstimate(None, None, 'estimate_unavailable', {}),\n"
    "                               confirm_above_usd=0.5, yes=sys.argv[1] == 'yes',\n"
    "                               command_name='job rerun-subtree', json_output=True)\n"
    "print('proceed' if proceed else 'declined')\n"
)


@pytest.mark.parametrize(("yes", "exit_code", "marker"), [
    ("yes", 0, "proceed"),
    ("no", cpc.EXIT_USAGE, '"error": "confirmation_required"'),
], ids=["with-yes-it-proceeds", "without-yes-it-refuses"])
def test_on_an_open_pipe_the_confirmation_answers_without_reading_stdin(
        tmp_path, yes, exit_code, marker):
    """F295 T003: the F114 confirmation in a real process whose stdin is a pipe nobody
    writes to and nobody closes. A read would block until the timeout below;
    `communicate()` is never used, because it closes the pipe."""
    import subprocess
    import sys
    from pathlib import Path

    repo = Path(__file__).resolve().parents[2]
    out_path = tmp_path / "confirm.out"
    with open(out_path, "wb") as out:
        proc = subprocess.Popen([sys.executable, "-c", _CONFIRM_ON_AN_OPEN_PIPE, yes],
                                cwd=str(repo), stdin=subprocess.PIPE, stdout=out,
                                stderr=subprocess.DEVNULL)
        try:
            proc.wait(timeout=60)
        finally:
            proc.stdin.close()
            if proc.poll() is None:
                proc.kill()
                proc.wait()

    assert proc.returncode == exit_code
    assert marker in out_path.read_text()
