"""Tests for project_scope.py (F148 T002)."""

from __future__ import annotations

from uuid import uuid4

import pytest

from packages.core.models import Job
from packages.orchestration.project_scope import (
    ProjectScope,
    job_in_scope,
    resolve_scope,
    scoped_jobs,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _job(project_id: str | None = None, name: str = "j") -> Job:
    return Job(name=name, project_id=project_id)


PROJ_A = str(uuid4())
PROJ_B = str(uuid4())


# ---------------------------------------------------------------------------
# job_in_scope — two projects
# ---------------------------------------------------------------------------

class TestJobInScopeMultiProject:
    """Two projects registered — legacy jobs hidden unless --all."""

    @pytest.fixture(autouse=True)
    def _patch_count(self, monkeypatch):
        monkeypatch.setattr(
            "packages.orchestration.project_scope._project_count",
            lambda: 2,
        )

    def test_scoped_job_matches(self):
        scope = ProjectScope(project_id=PROJ_A, all_projects=False, source="cwd")
        assert job_in_scope(_job(PROJ_A), scope) is True

    def test_scoped_job_other_project_hidden(self):
        scope = ProjectScope(project_id=PROJ_A, all_projects=False, source="cwd")
        assert job_in_scope(_job(PROJ_B), scope) is False

    def test_legacy_job_hidden_multi_project(self):
        scope = ProjectScope(project_id=PROJ_A, all_projects=False, source="cwd")
        assert job_in_scope(_job(None), scope) is False

    def test_all_projects_shows_everything(self):
        scope = ProjectScope(project_id=None, all_projects=True, source="flag")
        assert job_in_scope(_job(PROJ_A), scope) is True
        assert job_in_scope(_job(PROJ_B), scope) is True
        assert job_in_scope(_job(None), scope) is True


# ---------------------------------------------------------------------------
# job_in_scope — single project
# ---------------------------------------------------------------------------

class TestJobInScopeSingleProject:
    """One project registered — legacy jobs visible."""

    @pytest.fixture(autouse=True)
    def _patch_count(self, monkeypatch):
        monkeypatch.setattr(
            "packages.orchestration.project_scope._project_count",
            lambda: 1,
        )

    def test_legacy_job_visible_single_project(self):
        scope = ProjectScope(project_id=PROJ_A, all_projects=False, source="cwd")
        assert job_in_scope(_job(None), scope) is True

    def test_scoped_job_matches_single(self):
        scope = ProjectScope(project_id=PROJ_A, all_projects=False, source="cwd")
        assert job_in_scope(_job(PROJ_A), scope) is True


# ---------------------------------------------------------------------------
# job_in_scope — zero projects
# ---------------------------------------------------------------------------

class TestJobInScopeZeroProjects:
    """No projects registered — everything visible."""

    @pytest.fixture(autouse=True)
    def _patch_count(self, monkeypatch):
        monkeypatch.setattr(
            "packages.orchestration.project_scope._project_count",
            lambda: 0,
        )

    def test_legacy_job_visible_zero_projects(self):
        scope = ProjectScope(project_id=None, all_projects=True, source="fallback")
        assert job_in_scope(_job(None), scope) is True


# ---------------------------------------------------------------------------
# job_in_scope — all-projects always shows legacy
# ---------------------------------------------------------------------------

class TestLegacyAlwaysVisibleUnderAll:

    @pytest.fixture(autouse=True)
    def _patch_count(self, monkeypatch):
        monkeypatch.setattr(
            "packages.orchestration.project_scope._project_count",
            lambda: 5,
        )

    def test_all_projects_shows_legacy(self):
        scope = ProjectScope(project_id=None, all_projects=True, source="flag")
        assert job_in_scope(_job(None), scope) is True


# ---------------------------------------------------------------------------
# resolve_scope — selector precedence
# ---------------------------------------------------------------------------

class TestResolveScope:

    def test_all_projects_flag(self):
        scope = resolve_scope(all_projects=True)
        assert scope.all_projects is True
        assert scope.project_id is None
        assert scope.source == "flag"

    def test_project_flag_resolved(self, monkeypatch):
        from packages.orchestration.project_registry import RemyProject

        fake = RemyProject(name="test", slug="test")

        monkeypatch.setattr(
            "packages.orchestration.project_registry.select_project",
            lambda flag, cwd: (fake, "flag"),
        )

        scope = resolve_scope(project_flag="test")
        assert scope.project_id == str(fake.id)
        assert scope.all_projects is False
        assert scope.source == "flag"

    def test_fallback_when_no_project(self, monkeypatch):
        from packages.orchestration.project_registry import ProjectNotFoundError

        def _raise(*a, **kw):
            raise ProjectNotFoundError(cwd=".")

        monkeypatch.setattr(
            "packages.orchestration.project_registry.select_project",
            _raise,
        )

        scope = resolve_scope()
        assert scope.all_projects is True
        assert scope.source == "fallback"


# ---------------------------------------------------------------------------
# scoped_jobs — unreadable-files passthrough
# ---------------------------------------------------------------------------

class TestScopedJobs:

    @pytest.fixture(autouse=True)
    def _patch_count(self, monkeypatch):
        monkeypatch.setattr(
            "packages.orchestration.project_scope._project_count",
            lambda: 2,
        )

    def test_filters_and_passes_degraded(self, monkeypatch):
        jobs = [
            _job(PROJ_A, name="a1"),
            _job(PROJ_B, name="b1"),
            _job(None, name="legacy"),
        ]
        monkeypatch.setattr(
            "packages.orchestration.storage.list_jobs_safe",
            lambda root=None: (jobs, True, ["bad.json"]),
        )

        scope = ProjectScope(project_id=PROJ_A, all_projects=False, source="cwd")
        filtered, degraded, skipped = scoped_jobs(scope)

        assert len(filtered) == 1
        assert filtered[0].name == "a1"
        assert degraded is True
        assert skipped == ["bad.json"]

    def test_all_projects_returns_all(self, monkeypatch):
        jobs = [
            _job(PROJ_A, name="a1"),
            _job(PROJ_B, name="b1"),
            _job(None, name="legacy"),
        ]
        monkeypatch.setattr(
            "packages.orchestration.storage.list_jobs_safe",
            lambda root=None: (jobs, False, []),
        )

        scope = ProjectScope(project_id=None, all_projects=True, source="flag")
        filtered, degraded, skipped = scoped_jobs(scope)

        assert len(filtered) == 3
        assert degraded is False
