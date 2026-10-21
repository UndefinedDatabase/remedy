"""Tests for packages.orchestration.self_health — F199's health checks."""

from __future__ import annotations

import hashlib
import json
import os
import pathlib
import shutil
import sqlite3
import subprocess

import pytest

from packages.orchestration import self_health
from packages.orchestration.budget_resolution import BudgetConfigError
from packages.orchestration.config import load_config
from packages.orchestration.data_paths import projects_dir, resolve_data_root
from packages.orchestration.project_registry import RemyProject, save_project
from packages.orchestration.self_health import (
    CONFIG_HINT,
    CRASH_HINT,
    DISK_HINT,
    HEALTH_FAIL,
    HEALTH_PASS,
    HEALTH_WARN,
    LEDGER_HINT,
    PROVIDER_HINT,
    RECLAIM_HINT,
    SNAPSHOT_HINT,
    WORKTREE_HINT,
    HealthCheckResult,
    check_config_coherence,
    check_crash_reports,
    check_disk_floor,
    check_ledger_integrity,
    check_providers,
    check_snapshot_manifests,
    check_staging_copies,
    check_worktrees,
    health_exit_code,
    health_verdict,
    run_health_checks,
)
from packages.orchestration.token_ledger import LEDGER_FILENAME, open_ledger
from packages.orchestration.worktrees import WorktreeError

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
        '[remedy.ollama.builder]\nnum_predict = "b"\n'
        '[remedy.ui]\ncommand_rate_limit_per_minute = "c"\n'
        '[remedy.tests]\npytest_timeout_seconds = "d"\n'
    )
    result = check_config_coherence(_config_from(tmp_path, body))
    assert result.level == HEALTH_FAIL
    assert result.detail == (
        "4 configured values do not have their declared type: "
        "serve.api_port: expected int, got str; "
        "ollama.builder.num_predict: expected int, got str; "
        "ui.command_rate_limit_per_minute: expected int, got str; and 1 more")
    assert result.hint == CONFIG_HINT


def test_config_unreadable_fails(monkeypatch):
    def _raise():
        raise BudgetConfigError("bad budget")

    monkeypatch.setattr(self_health, "get_config", _raise)
    result = check_config_coherence()
    assert result == HealthCheckResult(
        "config", HEALTH_FAIL, "the configuration could not be read: bad budget", CONFIG_HINT)


def test_config_wrong_value_with_an_unknown_key_fails_not_warns(tmp_path):
    body = '[remedy.data]\nreclaim_warn_gb = "many"\n[remedy]\nfoo = 1\n'
    result = check_config_coherence(_config_from(tmp_path, body))
    assert result.level == HEALTH_FAIL
    assert "data.reclaim_warn_gb" in result.detail
    assert result.hint == CONFIG_HINT


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


def test_ledgers_a_database_that_opens_but_is_damaged_fails():
    path = _ledger_path("alpha")
    path.parent.mkdir(parents=True)
    connection = sqlite3.connect(path)
    connection.execute("CREATE TABLE t(a, b)")
    connection.execute("CREATE INDEX t_a ON t(a)")
    connection.executemany("INSERT INTO t VALUES (?, ?)", [(i, 100 - i) for i in range(50)])
    connection.commit()
    connection.execute("PRAGMA writable_schema=ON")
    connection.execute("UPDATE sqlite_master SET sql='CREATE INDEX t_a ON t(b)' WHERE name='t_a'")
    connection.commit()
    connection.close()
    result = check_ledger_integrity()
    assert result == HealthCheckResult(
        "ledgers", HEALTH_FAIL,
        "1 of 1 token ledgers failed SQLite's integrity check: projects/alpha/ledger.sqlite "
        "(row 1 missing from index t_a; row 2 missing from index t_a; "
        "row 3 missing from index t_a)",
        LEDGER_HINT)


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


def test_staging_copies_exactly_at_the_level_warn(monkeypatch):
    monkeypatch.setattr(self_health, "reclaim_preview_bytes", lambda root: 5 * GIB)
    result = check_staging_copies(warn_gb=5)
    assert result == HealthCheckResult(
        "staging_copies", HEALTH_WARN,
        "5.0 GB of staging copies can be freed, at or above the warning level of 5 GB",
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


def test_config_warning_with_the_home_path_reaches_the_detail_as_tilde(tmp_path):
    config = _config_from(tmp_path, "[remedy.data]\nreclaim_warn_gb = 7\n")
    config.load_report.warnings.append(f"Unknown key in {pathlib.Path.home()}/remedy.toml: foo")
    result = check_config_coherence(config)
    assert result.level == HEALTH_WARN
    assert result.detail.endswith("Unknown key in ~/remedy.toml: foo")
    assert str(pathlib.Path.home()) not in result.detail


# --- snapshots --------------------------------------------------------------


def _snapshot_dir_of(job: str, snap: str) -> pathlib.Path:
    return resolve_data_root() / "workspaces" / job / "repository_snapshots" / snap


def _write_snapshot(job: str, snap: str, blob: bytes = b"before") -> pathlib.Path:
    """A snapshot folder under the isolated data root, hashed by the rule the product checks."""
    snap_dir = _snapshot_dir_of(job, snap)
    (snap_dir / "blobs").mkdir(parents=True)
    (snap_dir / "blobs" / "a").write_bytes(blob)
    manifest = {
        "snapshot_id": snap,
        "entries": [{
            "recovery_blob_ref": "blobs/a",
            "before_sha256": hashlib.sha256(blob).hexdigest(),
        }],
    }
    manifest["manifest_hash"] = hashlib.sha256(
        json.dumps(manifest, indent=2, sort_keys=True).encode("utf-8")).hexdigest()
    (snap_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True))
    return snap_dir


def test_snapshots_none_pass():
    assert check_snapshot_manifests() == HealthCheckResult(
        "snapshots", HEALTH_PASS, "no workspace snapshot exists yet")


def test_snapshots_a_good_one_passes():
    _write_snapshot("job1", "snap1")
    assert check_snapshot_manifests() == HealthCheckResult(
        "snapshots", HEALTH_PASS, "1 of 1 newest workspace snapshots passed their hash check")


def test_snapshots_a_changed_blob_fails_naming_the_folder():
    snap_dir = _write_snapshot("job1", "snap1")
    (snap_dir / "blobs" / "a").write_bytes(b"after")
    assert check_snapshot_manifests() == HealthCheckResult(
        "snapshots", HEALTH_FAIL,
        "1 of 1 newest workspace snapshots failed their hash check: "
        "workspaces/job1/repository_snapshots/snap1 (1 recovery files changed)",
        SNAPSHOT_HINT)


def test_snapshots_a_removed_blob_fails():
    snap_dir = _write_snapshot("job1", "snap1")
    (snap_dir / "blobs" / "a").unlink()
    assert check_snapshot_manifests() == HealthCheckResult(
        "snapshots", HEALTH_FAIL,
        "1 of 1 newest workspace snapshots failed their hash check: "
        "workspaces/job1/repository_snapshots/snap1 (1 recovery files missing)",
        SNAPSHOT_HINT)


def test_snapshots_an_edited_manifest_fails():
    snap_dir = _write_snapshot("job1", "snap1")
    path = snap_dir / "manifest.json"
    manifest = json.loads(path.read_text())
    manifest["entries"].append({"recovery_blob_ref": ""})
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True))
    assert check_snapshot_manifests() == HealthCheckResult(
        "snapshots", HEALTH_FAIL,
        "1 of 1 newest workspace snapshots failed their hash check: "
        "workspaces/job1/repository_snapshots/snap1 "
        "(its manifest does not match its recorded hash)",
        SNAPSHOT_HINT)


def test_snapshots_a_manifest_that_is_a_json_list_fails_naming_the_folder():
    snap_dir = _write_snapshot("job1", "snap1")
    (snap_dir / "manifest.json").write_text("[1, 2]")
    assert check_snapshot_manifests() == HealthCheckResult(
        "snapshots", HEALTH_FAIL,
        "1 of 1 newest workspace snapshots failed their hash check: "
        "workspaces/job1/repository_snapshots/snap1 (its manifest cannot be read)",
        SNAPSHOT_HINT)


def test_snapshots_only_the_newest_sample_is_read():
    old = _write_snapshot("job1", "old")
    _write_snapshot("job1", "mid")
    _write_snapshot("job1", "new")
    (old / "blobs" / "a").write_bytes(b"after")
    for index, snap in enumerate(("old", "mid", "new")):
        stamp = 1_000_000 + index
        os.utime(_snapshot_dir_of("job1", snap) / "manifest.json", (stamp, stamp))
    assert check_snapshot_manifests(sample=2) == HealthCheckResult(
        "snapshots", HEALTH_PASS, "2 of 2 newest workspace snapshots passed their hash check")
    assert check_snapshot_manifests(sample=3).level == HEALTH_FAIL


# --- worktrees --------------------------------------------------------------


def _git(repo: pathlib.Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-c", "user.email=t@example.com", "-c", "user.name=t", *args],
        cwd=repo, capture_output=True, text=True, check=True, timeout=60)
    return completed.stdout


def _registered_repo(tmp_path: pathlib.Path) -> pathlib.Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "commit", "-q", "--allow-empty", "-m", "first")
    save_project(RemyProject(
        name="demo", canonical_repo_path=str(repo), repo_paths=[str(repo)]))
    return repo


def test_worktrees_no_project_passes():
    assert check_worktrees() == HealthCheckResult(
        "worktrees", HEALTH_PASS, "no registered project has a repository on this machine")


def test_worktrees_a_clean_repository_passes(tmp_path):
    _registered_repo(tmp_path)
    assert check_worktrees() == HealthCheckResult(
        "worktrees", HEALTH_PASS, "1 repositories checked; no worktree is prunable")


def test_worktrees_a_gone_folder_warns_and_nothing_is_removed(tmp_path):
    repo = _registered_repo(tmp_path)
    gone = tmp_path / "wt"
    _git(repo, "worktree", "add", "-q", str(gone))
    shutil.rmtree(gone)
    assert check_worktrees() == HealthCheckResult(
        "worktrees", HEALTH_WARN,
        f"1 worktrees git calls prunable, their folders gone: {repo}: {gone}",
        WORKTREE_HINT)
    assert str(gone) in _git(repo, "worktree", "list", "--porcelain")


def test_worktrees_an_unreadable_repository_is_named(tmp_path, monkeypatch):
    repo = _registered_repo(tmp_path)

    def _raise(_repo):
        raise WorktreeError("x")

    monkeypatch.setattr(self_health, "list_worktrees", _raise)
    result = check_worktrees()
    assert result.level == HEALTH_PASS
    assert result.detail.endswith(f"; git could not read 1 repositories: {repo}")


# --- providers --------------------------------------------------------------


def _which_of(*names: str):
    return lambda name: f"/bin/{name}" if name in names else None


def test_providers_all_reachable_pass():
    result = check_providers(_which_of("claude", "ollama"), {"ANTHROPIC_API_KEY": "k"})
    assert result == HealthCheckResult(
        "providers", HEALTH_PASS, "reachable: claude-cli, claude, ollama; no provider was called")


def test_providers_only_ollama_passes_and_names_the_rest():
    result = check_providers(_which_of("ollama"), {})
    assert result == HealthCheckResult(
        "providers", HEALTH_PASS,
        "reachable: ollama; not reachable: claude-cli, claude; no provider was called")


def test_providers_none_reachable_warns_with_the_three_gaps():
    result = check_providers(_which_of(), {})
    assert result == HealthCheckResult(
        "providers", HEALTH_WARN,
        "no provider can be reached: claude-cli needs the claude command on the path; "
        "claude needs ANTHROPIC_API_KEY set; ollama needs the ollama command on the path",
        PROVIDER_HINT)


def test_providers_never_put_the_key_in_a_text():
    for which in (_which_of(), _which_of("ollama")):
        result = check_providers(which, {"ANTHROPIC_API_KEY": "sk-test-secret"})
        assert "sk-test-secret" not in result.detail
        assert "sk-test-secret" not in result.hint


def test_providers_a_key_of_spaces_counts_as_unset():
    result = check_providers(_which_of(), {"ANTHROPIC_API_KEY": "   "})
    assert result.level == HEALTH_WARN


# --- the set ----------------------------------------------------------------


def test_run_health_checks_answers_nine_checks_in_order():
    results = run_health_checks()
    assert [r.check for r in results] == [
        "config", "ledgers", "snapshots", "worktrees", "providers", "default_chain", "staging_copies", "disk",
        "crash_reports"]


# --- crash reports ----------------------------------------------------------


def test_crash_reports_none_pass():
    assert check_crash_reports() == HealthCheckResult(
        "crash_reports", HEALTH_PASS, "no crash report in the last 7 days")


def test_crash_reports_a_recent_one_warns_naming_it():
    from packages.orchestration.crash_report import write_crash_report

    try:
        raise ValueError("planted")
    except ValueError as caught:
        path = write_crash_report(caught, command="job.list")
    assert path is not None
    assert check_crash_reports() == HealthCheckResult(
        "crash_reports", HEALTH_WARN,
        f"1 crash reports in the last 7 days; the newest is crash/{path.name}",
        CRASH_HINT)


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
