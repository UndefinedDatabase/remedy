"""`remedy doctor health [--json]` (F199 T001, DECISION F199 D1): Remedy's own health checks,
each PASS, WARN or FAIL with a hint; the exit code is 1 on a FAIL and 0 otherwise.

Temporary data roots only. The settings, staging-copy and disk checks are replaced where a test
needs a fixed answer; the ledger check reads the isolated data root.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from apps.cli.grouped import main as grouped_main
from packages.orchestration import self_health
from packages.orchestration.data_paths import projects_dir
from packages.orchestration.self_health import (
    HEALTH_PASS,
    HEALTH_WARN,
    HealthCheckResult,
)
from packages.orchestration.token_ledger import LEDGER_FILENAME

REPO_ROOT = Path(__file__).resolve().parents[2]


def _fixed(check: str, level: str = HEALTH_PASS, detail: str = "fine", hint: str = ""):
    def _check(*_args, **_kwargs) -> HealthCheckResult:
        return HealthCheckResult(check, level, detail, hint)

    return _check


@pytest.fixture
def fixed_checks(monkeypatch):
    """The checks that read the machine answer PASS; the ledger check reads the data root."""
    monkeypatch.setattr(self_health, "check_config_coherence", _fixed("config"))
    monkeypatch.setattr(self_health, "check_providers", _fixed("providers"))
    monkeypatch.setattr(self_health, "check_staging_copies", _fixed("staging_copies"))
    monkeypatch.setattr(self_health, "check_disk_floor", _fixed("disk"))


def _garbage_ledger(root: Path) -> Path:
    path = root / "alpha" / LEDGER_FILENAME
    path.parent.mkdir(parents=True)
    path.write_bytes(b"this is not a database " * 20)
    return path


def test_every_check_passing_prints_pass_lines_and_exits_zero(fixed_checks, capsys):
    grouped_main(["doctor", "health"])
    lines = capsys.readouterr().out.splitlines()
    assert lines[0] == "Remedy health: PASS"
    assert [line for line in lines[1:] if line.startswith("  [PASS] ")] == lines[1:]
    assert len(lines) == 8
    assert not any("fix:" in line for line in lines)


def test_a_warning_prints_its_fix_line_and_still_exits_zero(fixed_checks, monkeypatch, capsys):
    monkeypatch.setattr(
        self_health, "check_staging_copies",
        _fixed("staging_copies", HEALTH_WARN, "6.0 GB can be freed", "run the preview"))
    grouped_main(["doctor", "health"])
    lines = capsys.readouterr().out.splitlines()
    assert lines[0] == "Remedy health: WARN"
    assert "  [WARN] staging_copies: 6.0 GB can be freed" in lines
    assert lines[lines.index("  [WARN] staging_copies: 6.0 GB can be freed") + 1] == (
        "         fix: run the preview")


def test_a_failing_ledger_exits_one_with_its_fail_and_fix_lines(fixed_checks, capsys):
    _garbage_ledger(projects_dir())
    with pytest.raises(SystemExit) as raised:
        grouped_main(["doctor", "health"])
    assert raised.value.code == 1
    lines = capsys.readouterr().out.splitlines()
    assert lines[0] == "Remedy health: FAIL"
    index = next(i for i, line in enumerate(lines) if line.startswith("  [FAIL] ledgers: "))
    assert lines[index + 1].startswith("         fix: ")


def test_json_with_every_check_passing_is_one_ok_object(fixed_checks, capsys):
    grouped_main(["doctor", "health", "--json"])
    document = json.loads(capsys.readouterr().out)
    assert document["ok"] is True
    assert document["verdict"] == "PASS"
    assert len(document["checks"]) == 7
    for check in document["checks"]:
        # The envelope writes every level's keys sorted, so the order is not the check's own.
        assert sorted(check) == ["check", "detail", "hint", "level"]


def test_json_with_a_failing_ledger_exits_one_with_the_failure_envelope(fixed_checks, capsys):
    _garbage_ledger(projects_dir())
    with pytest.raises(SystemExit) as raised:
        grouped_main(["doctor", "health", "--json"])
    assert raised.value.code == 1
    document = json.loads(capsys.readouterr().out)
    assert document["ok"] is False
    assert document["error"] == "health_failed"
    assert document["message"] == "1 of 7 health checks failed"
    ledgers = next(c for c in document["checks"] if c["check"] == "ledgers")
    assert ledgers["level"] == "FAIL"


def test_the_real_command_line_exits_one_on_a_failing_ledger(tmp_path):
    _garbage_ledger(tmp_path / "projects")
    env = dict(os.environ, REMEDY_DATA_DIR=str(tmp_path), PYTHONPATH=str(REPO_ROOT))
    completed = subprocess.run(
        [sys.executable, "-m", "apps.cli.main", "doctor", "health", "--json"],
        cwd=REPO_ROOT, env=env, capture_output=True, text=True, timeout=120)
    assert completed.returncode == 1
    document = json.loads(completed.stdout)
    ledgers = next(c for c in document["checks"] if c["check"] == "ledgers")
    assert ledgers["level"] == "FAIL"
