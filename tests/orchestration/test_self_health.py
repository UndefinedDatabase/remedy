"""Tests for packages.orchestration.self_health — F199's health checks."""

from __future__ import annotations

import pathlib

import pytest

from packages.orchestration import self_health
from packages.orchestration.budget_resolution import BudgetConfigError
from packages.orchestration.config import load_config
from packages.orchestration.data_paths import projects_dir
from packages.orchestration.self_health import (
    CONFIG_HINT,
    DISK_HINT,
    HEALTH_FAIL,
    HEALTH_PASS,
    HEALTH_WARN,
    LEDGER_HINT,
    RECLAIM_HINT,
    HealthCheckResult,
    check_config_coherence,
    check_disk_floor,
    check_ledger_integrity,
    check_staging_copies,
    health_exit_code,
    health_verdict,
    home_relative_text,
    run_health_checks,
)
from packages.orchestration.token_ledger import LEDGER_FILENAME, open_ledger

GIB = 1024 ** 3


def _config_from(tmp_path: pathlib.Path, body: str):
    """A real remedy.toml in tmp_path, loaded the way the product loads one."""
    toml_path = tmp_path / "remedy.toml"
    toml_path.write_text(body)
    return load_config(
        project_path=toml_path, user_path=pathlib.Path("/nonexistent/user.toml"))


def _ledger_path(project_id: str) -> pathlib.Path:
    return projects_dir() / project_id / LEDGER_FILENAME


def _make_ledger(project_id: str) -> pathlib.Path:
    path = _ledger_path(project_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    open_ledger(path).close()
    return path


# --- config -----------------------------------------------------------------


def test_config_clean_file_passes(tmp_path):
    result = check_config_coherence(_config_from(tmp_path, "[remedy.data]\nreclaim_warn_gb = 7\n"))
    assert result == HealthCheckResult(
        "config", HEALTH_PASS, "every configured value has its declared type", "")


def test_config_word_for_integer_fails_naming_the_key(tmp_path):
    config = _config_from(tmp_path, '[remedy.data]\nreclaim_warn_gb = "many"\n')
    result = check_config_coherence(config)
    assert result.level == HEALTH_FAIL
    assert result.detail == (
        "1 configured values do not have their declared type: "
        "data.reclaim_warn_gb: expected int, got str")
    assert result.hint == CONFIG_HINT


def test_config_unknown_key_warns_naming_it(tmp_path):
    result = check_config_coherence(_config_from(tmp_path, "[remedy]\nfoo = 1\n"))
    assert result.level == HEALTH_WARN
    assert result.detail.startswith("1 warnings while reading the configuration: ")
    assert result.detail.endswith("remedy.toml: foo")
    assert result.hint == CONFIG_HINT


def test_config_four_wrong_values_get_the_more_tail(tmp_path):
    body = (
        '[remedy.serve]\napi_port = "a"\n'
        '[remedy.ui]\nport = "b"\ncommand_rate_limit_per_minute = "c"\n'
        '[remedy.tests]\npytest_timeout_seconds = "d"\n'
    )
    result = check_config_coherence(_config_from(tmp_path, body))
    assert result.level == HEALTH_FAIL
    assert result.detail == (
        "4 configured values do not have their declared type: "
        "serve.api_port: expected int, got str; "
        "ui.port: expected int, got str; "
        "ui.command_rate_limit_per_minute: expected int, got str; and 1 more")
    assert result.hint == CONFIG_HINT


def test_config_unreadable_fails(monkeypatch):
    def _raise():
        raise BudgetConfigError("bad budget")

    monkeypatch.setattr(self_health, "get_config", _raise)
    result = check_config_coherence()
    assert result == HealthCheckResult(
        "config", HEALTH_FAIL, "the configuration could not be read: bad budget", CONFIG_HINT)


# --- ledgers ----------------------------------------------------------------


def test_ledgers_none_pass():
    result = check_ledger_integrity()
    assert result == HealthCheckResult("ledgers", HEALTH_PASS, "no token ledger exists yet", "")


def test_ledgers_good_one_passes():
    _make_ledger("alpha")
    result = check_ledger_integrity()
    assert result == HealthCheckResult(
        "ledgers", HEALTH_PASS, "1 of 1 token ledgers passed SQLite's integrity check", "")


def test_ledgers_garbage_file_fails_and_is_left_untouched():
    path = _ledger_path("alpha")
    path.parent.mkdir(parents=True)
    path.write_bytes(b"this is not a database " * 20)
    before_bytes = path.read_bytes()
    before_files = sorted(p.name for p in path.parent.iterdir())
    result = check_ledger_integrity()
    assert result.level == HEALTH_FAIL
    assert result.detail.startswith("1 of 1 token ledgers failed SQLite's integrity check: ")
    assert "projects/alpha/ledger.sqlite" in result.detail
    assert "file is not a database" in result.detail
    assert result.hint == LEDGER_HINT
    assert path.read_bytes() == before_bytes
    assert sorted(p.name for p in path.parent.iterdir()) == before_files


def test_ledgers_overwritten_pages_fail():
    path = _make_ledger("alpha")
    data = path.read_bytes()
    assert len(data) > 100
    path.write_bytes(data[:100] + b"\xff" * (len(data) - 100))
    result = check_ledger_integrity()
    assert result.level == HEALTH_FAIL
    assert "projects/alpha/ledger.sqlite" in result.detail
    assert result.hint == LEDGER_HINT


def test_ledgers_one_good_one_bad_counts_both():
    _make_ledger("alpha")
    bad = _ledger_path("beta")
    bad.parent.mkdir(parents=True)
    bad.write_bytes(b"garbage" * 100)
    result = check_ledger_integrity()
    assert result.level == HEALTH_FAIL
    assert result.detail.startswith("1 of 2 token ledgers failed SQLite's integrity check: ")
    assert "projects/beta/ledger.sqlite" in result.detail
    assert "projects/alpha/ledger.sqlite" not in result.detail


# --- staging copies ---------------------------------------------------------


def test_staging_copies_at_or_above_the_level_warn(monkeypatch):
    monkeypatch.setattr(self_health, "reclaim_preview_bytes", lambda root: 6 * GIB)
    result = check_staging_copies(warn_gb=5)
    assert result == HealthCheckResult(
        "staging_copies", HEALTH_WARN,
        "6.0 GB of staging copies can be freed, at or above the warning level of 5 GB",
        RECLAIM_HINT)


def test_staging_copies_none_pass(monkeypatch):
    monkeypatch.setattr(self_health, "reclaim_preview_bytes", lambda root: 0)
    result = check_staging_copies(warn_gb=5)
    assert result == HealthCheckResult(
        "staging_copies", HEALTH_PASS,
        "0.0 GB of staging copies can be freed, below the warning level of 5 GB", "")


def test_staging_copies_unmeasurable_warns(monkeypatch):
    def _raise(root):
        raise OSError("boom")

    monkeypatch.setattr(self_health, "reclaim_preview_bytes", _raise)
    result = check_staging_copies(warn_gb=5)
    assert result == HealthCheckResult(
        "staging_copies", HEALTH_WARN,
        "the staging copies could not be measured: boom", RECLAIM_HINT)


# --- disk -------------------------------------------------------------------


def test_disk_below_floor_fails(monkeypatch):
    monkeypatch.setattr(self_health, "resolve_min_free_disk_bytes", lambda: 100)
    result = check_disk_floor(lambda: 10)
    assert result == HealthCheckResult(
        "disk", HEALTH_FAIL, "10 bytes free, below the configured floor of 100 bytes", DISK_HINT)


def test_disk_at_floor_passes(monkeypatch):
    monkeypatch.setattr(self_health, "resolve_min_free_disk_bytes", lambda: 100)
    result = check_disk_floor(lambda: 100)
    assert result == HealthCheckResult(
        "disk", HEALTH_PASS, "100 bytes free; the floor is 100 bytes", "")


def test_disk_without_floor_passes(monkeypatch):
    monkeypatch.setattr(self_health, "resolve_min_free_disk_bytes", lambda: None)
    result = check_disk_floor(lambda: 50)
    assert result == HealthCheckResult(
        "disk", HEALTH_PASS,
        "50 bytes free; no floor is configured (budget.min_free_disk_bytes)", "")


def test_disk_unreadable_warns(monkeypatch):
    monkeypatch.setattr(self_health, "resolve_min_free_disk_bytes", lambda: 100)

    def _raise() -> int:
        raise OSError("no disk")

    result = check_disk_floor(_raise)
    assert result == HealthCheckResult(
        "disk", HEALTH_WARN, "the free disk could not be read: no disk", CONFIG_HINT)


# --- home folder ------------------------------------------------------------


def test_home_relative_text_replaces_the_home_path(tmp_path):
    assert home_relative_text(f"{tmp_path}/x", tmp_path) == "~/x"


def test_home_relative_text_leaves_text_for_a_root_home():
    assert home_relative_text("/x/y", pathlib.Path("/")) == "/x/y"


def test_config_warning_with_the_home_path_reaches_the_detail_as_tilde(tmp_path):
    config = _config_from(tmp_path, "[remedy.data]\nreclaim_warn_gb = 7\n")
    config.load_report.warnings.append(f"Unknown key in {pathlib.Path.home()}/remedy.toml: foo")
    result = check_config_coherence(config)
    assert result.level == HEALTH_WARN
    assert result.detail.endswith("Unknown key in ~/remedy.toml: foo")
    assert str(pathlib.Path.home()) not in result.detail


# --- the set ----------------------------------------------------------------


def test_run_health_checks_answers_four_checks_in_order():
    results = run_health_checks()
    assert [r.check for r in results] == ["config", "ledgers", "staging_copies", "disk"]


def _result(level: str) -> HealthCheckResult:
    return HealthCheckResult("x", level, "d")


@pytest.mark.parametrize(
    ("levels", "verdict", "code"),
    [
        ([HEALTH_PASS, HEALTH_WARN], HEALTH_WARN, 0),
        ([HEALTH_PASS, HEALTH_FAIL, HEALTH_WARN], HEALTH_FAIL, 1),
        ([], HEALTH_PASS, 0),
    ],
)
def test_verdict_and_exit_code(levels, verdict, code):
    results = [_result(level) for level in levels]
    assert health_verdict(results) == verdict
    assert health_exit_code(results) == code


def test_as_json_has_exactly_the_four_keys_in_order():
    payload = HealthCheckResult("c", HEALTH_WARN, "d", "h").as_json()
    assert list(payload) == ["check", "level", "detail", "hint"]
    assert payload == {"check": "c", "level": HEALTH_WARN, "detail": "d", "hint": "h"}
