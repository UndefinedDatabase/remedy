"""Two-project isolation acceptance tests for F148 scoped listings.

Real CLI subprocess tests with isolated data root. Unit tests for
scope predicate and labels kept at the bottom.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from unittest.mock import patch
from uuid import uuid4

from packages.core.models import Job
from packages.orchestration.project_scope import ProjectScope, job_in_scope, scoped_jobs

_CLI = [sys.executable, "-m", "apps.cli.grouped"]

_P1 = str(uuid4())
_P2 = str(uuid4())


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _env(data_dir):
    return {
        **os.environ,
        "PYTHONPATH": os.getcwd(),
        "REMEDY_DATA_DIR": str(data_dir),
    }


def _git_repo(base, name):
    repo = base / name
    repo.mkdir()
    subprocess.run(
        ["git", "init", "-q", str(repo)], check=True, capture_output=True,
    )
    subprocess.run(
        ["git", "-C", str(repo), "commit", "--allow-empty", "-m", "init", "-q"],
        check=True, capture_output=True,
        env={**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
             "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"},
    )
    return repo


def _init_project(repo, env):
    result = subprocess.run(
        [*_CLI, "init"],
        capture_output=True, text=True, timeout=30,
        cwd=str(repo), env=env, stdin=subprocess.DEVNULL,
    )
    assert result.returncode == 0, result.stderr
    return result


def _run_cli(args, env, *, cwd=None, timeout=30):
    return subprocess.run(
        [*_CLI, *args],
        capture_output=True, text=True, timeout=timeout,
        cwd=cwd, env=env, stdin=subprocess.DEVNULL,
    )


def _create_job(repo, env, mission):
    """Create a job via 'remedy do' and return (short_id, full_id)."""
    result = _run_cli(
        ["do", mission, "--json"], env, cwd=str(repo),
    )
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    full_id = data["job_id"]
    return full_id[:8], full_id


def _write_legacy_job(data_dir, name="legacy-job"):
    """Write a job JSON with no project_id directly to the store."""
    jobs = data_dir / "jobs"
    jobs.mkdir(parents=True, exist_ok=True)
    jid = str(uuid4())
    (jobs / f"{jid}.json").write_text(json.dumps({
        "id": jid,
        "name": name,
        "state": "pending",
        "tasks": [],
        "artifacts": [],
        "metadata": {},
    }))
    return jid[:8], jid


def _get_project_slug(repo, env):
    result = _run_cli(["project", "current", "--json"], env, cwd=str(repo))
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)["slug"]


# ---------------------------------------------------------------------------
# CLI Subprocess Tests
# ---------------------------------------------------------------------------


class TestScopedListingsCLI:
    """Real subprocess tests: two projects, scoped listings."""

    def test_full_isolation_and_flags(self, tmp_path):
        data_dir = tmp_path / "data"
        env = _env(data_dir)

        repo_a = _git_repo(tmp_path, "alpha")
        repo_b = _git_repo(tmp_path, "beta")
        _init_project(repo_a, env)
        _init_project(repo_b, env)

        slug_a = _get_project_slug(repo_a, env)
        slug_b = _get_project_slug(repo_b, env)

        short_a1, _ = _create_job(repo_a, env, "alpha job one")
        short_a2, _ = _create_job(repo_a, env, "alpha job two")
        short_b1, _ = _create_job(repo_b, env, "beta job one")
        short_b2, _ = _create_job(repo_b, env, "beta job two")

        # Default: from repo A, only A's jobs
        result = _run_cli(["job", "list"], env, cwd=str(repo_a))
        assert result.returncode == 0
        assert "alpha job one" in result.stdout
        assert "alpha job two" in result.stdout
        assert "beta job one" not in result.stdout
        assert "beta job two" not in result.stdout

        # --all-projects: all four
        result = _run_cli(["job", "list", "--all-projects"], env, cwd=str(repo_a))
        assert result.returncode == 0
        assert "alpha job one" in result.stdout
        assert "beta job one" in result.stdout

        # --project B from repo A: only B's jobs
        result = _run_cli(
            ["job", "list", "--project", slug_b], env, cwd=str(repo_a),
        )
        assert result.returncode == 0
        assert "beta job one" in result.stdout
        assert "beta job two" in result.stdout
        assert "alpha job one" not in result.stdout

    def test_legacy_job_hidden_and_unscoped_label(self, tmp_path):
        data_dir = tmp_path / "data"
        env = _env(data_dir)

        repo_a = _git_repo(tmp_path, "alpha")
        _init_project(repo_a, env)
        _create_job(repo_a, env, "alpha job")
        _write_legacy_job(data_dir, "old-legacy")

        # Default (two projects exist → legacy hidden)
        # Actually only one project, so legacy visible (single-project rule)
        # Add second project to trigger multi-project hiding
        repo_b = _git_repo(tmp_path, "beta")
        _init_project(repo_b, env)

        result = _run_cli(["job", "list"], env, cwd=str(repo_a))
        assert result.returncode == 0
        assert "old-legacy" not in result.stdout

        # --all-projects: legacy visible with (unscoped)
        result = _run_cli(["job", "list", "--all-projects"], env, cwd=str(repo_a))
        assert result.returncode == 0
        assert "old-legacy" in result.stdout
        assert "(unscoped)" in result.stdout

    def test_adopt_persists(self, tmp_path):
        data_dir = tmp_path / "data"
        env = _env(data_dir)

        repo_a = _git_repo(tmp_path, "alpha")
        _init_project(repo_a, env)
        short_id, full_id = _write_legacy_job(data_dir, "orphan-to-adopt")

        # Adopt via short id
        result = _run_cli(
            ["project", "adopt", short_id], env, cwd=str(repo_a),
        )
        assert result.returncode == 0
        assert "Adopted" in result.stdout

        # Verify in next listing
        result = _run_cli(["job", "list"], env, cwd=str(repo_a))
        assert result.returncode == 0
        assert "orphan-to-adopt" in result.stdout
        assert "(unscoped)" not in result.stdout

    def test_orphaned_label_on_deleted_project(self, tmp_path):
        data_dir = tmp_path / "data"
        env = _env(data_dir)

        repo_a = _git_repo(tmp_path, "alpha")
        _init_project(repo_a, env)
        _create_job(repo_a, env, "alpha job")

        # Create a job with a fake project_id (simulates deleted project)
        jobs_dir = data_dir / "jobs"
        orphan_id = str(uuid4())
        fake_project = str(uuid4())
        (jobs_dir / f"{orphan_id}.json").write_text(json.dumps({
            "id": orphan_id,
            "name": "orphaned-job",
            "state": "pending",
            "tasks": [],
            "artifacts": [],
            "metadata": {},
            "project_id": fake_project,
        }))

        # --all-projects listing should show orphaned label and not crash
        result = _run_cli(["job", "list", "--all-projects"], env, cwd=str(repo_a))
        assert result.returncode == 0
        assert "orphaned-job" in result.stdout
        assert "(orphaned:" in result.stdout

    def test_status_scoped(self, tmp_path):
        data_dir = tmp_path / "data"
        env = _env(data_dir)

        repo_a = _git_repo(tmp_path, "alpha")
        repo_b = _git_repo(tmp_path, "beta")
        _init_project(repo_a, env)
        _init_project(repo_b, env)
        slug_a = _get_project_slug(repo_a, env)
        slug_b = _get_project_slug(repo_b, env)

        _create_job(repo_a, env, "alpha status job")
        _create_job(repo_b, env, "beta status job")

        # Default: from A shows A's slug
        result = _run_cli(["status", "--json"], env, cwd=str(repo_a))
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["scope"] == slug_a

        # --project B from cwd=A: project slug shows B, not A (R-0108)
        result = _run_cli(
            ["status", "--project", slug_b, "--json"], env, cwd=str(repo_a),
        )
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["project"] == slug_b
        assert data["scope"] == slug_b

        # --all-projects
        result = _run_cli(["status", "--all-projects", "--json"], env, cwd=str(repo_a))
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["scope"] == "all projects"


# ---------------------------------------------------------------------------
# Unit Tests (kept from T002/T003)
# ---------------------------------------------------------------------------


def _job(project_id: str | None = None, name: str = "j") -> Job:
    return Job(name=name, project_id=project_id)


class TestTwoProjectIsolation:
    """Jobs from project A must not appear in project B's listing."""

    def test_scoped_to_p1_hides_p2(self):
        j1 = _job(_P1, "alpha")
        j2 = _job(_P2, "beta")
        scope = ProjectScope(project_id=_P1, all_projects=False, source="flag")
        assert job_in_scope(j1, scope, _legacy_visible=False)
        assert not job_in_scope(j2, scope, _legacy_visible=False)

    def test_scoped_to_p2_hides_p1(self):
        j1 = _job(_P1, "alpha")
        j2 = _job(_P2, "beta")
        scope = ProjectScope(project_id=_P2, all_projects=False, source="flag")
        assert not job_in_scope(j1, scope, _legacy_visible=False)
        assert job_in_scope(j2, scope, _legacy_visible=False)

    def test_all_projects_shows_both(self):
        j1 = _job(_P1, "alpha")
        j2 = _job(_P2, "beta")
        scope = ProjectScope(project_id=None, all_projects=True, source="flag")
        assert job_in_scope(j1, scope, _legacy_visible=True)
        assert job_in_scope(j2, scope, _legacy_visible=True)

    def test_legacy_hidden_in_multi_project(self):
        legacy = _job(None, "old")
        scope = ProjectScope(project_id=_P1, all_projects=False, source="flag")
        assert not job_in_scope(legacy, scope, _legacy_visible=False)

    def test_legacy_visible_under_all(self):
        legacy = _job(None, "old")
        scope = ProjectScope(project_id=None, all_projects=True, source="flag")
        assert job_in_scope(legacy, scope, _legacy_visible=True)


class TestScopedJobsIntegration:
    def test_two_project_filtering(self):
        j1 = _job(_P1, "alpha")
        j2 = _job(_P2, "beta")
        j_legacy = _job(None, "old")
        mock_jobs = [j1, j2, j_legacy]

        scope = ProjectScope(project_id=_P1, all_projects=False, source="flag")
        with patch(
            "packages.orchestration.storage.list_jobs_safe",
            return_value=(mock_jobs, False, []),
        ), patch(
            "packages.orchestration.project_scope._project_count",
            return_value=2,
        ):
            jobs, degraded, skipped = scoped_jobs(scope)

        names = [j.name for j in jobs]
        assert "alpha" in names
        assert "beta" not in names
        assert "old" not in names
        assert not degraded

    def test_all_projects_returns_everything(self):
        j1 = _job(_P1, "alpha")
        j2 = _job(_P2, "beta")
        j_legacy = _job(None, "old")
        mock_jobs = [j1, j2, j_legacy]

        scope = ProjectScope(project_id=None, all_projects=True, source="flag")
        with patch(
            "packages.orchestration.storage.list_jobs_safe",
            return_value=(mock_jobs, True, ["bad.json"]),
        ):
            jobs, degraded, skipped = scoped_jobs(scope)

        assert len(jobs) == 3
        assert degraded is True
        assert skipped == ["bad.json"]


class TestScopeLabel:
    def test_unscoped_label(self):
        from apps.cli.commands.job import _scope_label
        j = _job(None)
        scope = ProjectScope(project_id=None, all_projects=True, source="flag")
        assert _scope_label(j, scope, set()) == "  (unscoped)"

    def test_orphaned_label(self):
        from apps.cli.commands.job import _scope_label
        j = _job("dead-project-id-1234")
        scope = ProjectScope(project_id=_P1, all_projects=True, source="flag")
        label = _scope_label(j, scope, {_P1})
        assert "(orphaned:" in label

    def test_same_project_no_label(self):
        from apps.cli.commands.job import _scope_label
        j = _job(_P1)
        scope = ProjectScope(project_id=_P1, all_projects=False, source="flag")
        assert _scope_label(j, scope, {_P1}) == ""

    def test_other_project_label_under_all(self):
        from apps.cli.commands.job import _scope_label
        j = _job(_P2)
        scope = ProjectScope(project_id=_P1, all_projects=True, source="flag")
        label = _scope_label(j, scope, {_P1, _P2})
        assert "(project:" in label
        assert _P2[:8] in label
