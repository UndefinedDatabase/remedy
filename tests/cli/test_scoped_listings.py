"""Two-project isolation test for scoped job listings (F148 T003)."""

from __future__ import annotations

from unittest.mock import patch
from uuid import uuid4

from packages.core.models import Job
from packages.orchestration.project_scope import ProjectScope, job_in_scope, scoped_jobs

_P1 = str(uuid4())
_P2 = str(uuid4())


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
    """scoped_jobs returns only matching jobs and passes through degraded/skipped."""

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
    """Display labels for _scope_label."""

    def test_no_label_when_not_all_projects(self):
        from apps.cli.commands.job import _scope_label

        j = _job(_P1)
        scope = ProjectScope(project_id=_P1, all_projects=False, source="flag")
        assert _scope_label(j, scope) == ""

    def test_unscoped_label(self):
        from apps.cli.commands.job import _scope_label

        j = _job(None)
        scope = ProjectScope(project_id=None, all_projects=True, source="flag")
        assert _scope_label(j, scope) == "  (unscoped)"

    def test_other_project_label(self):
        from apps.cli.commands.job import _scope_label

        j = _job(_P2)
        scope = ProjectScope(project_id=_P1, all_projects=True, source="flag")
        label = _scope_label(j, scope)
        assert "(project:" in label
        assert _P2[:8] in label

    def test_same_project_no_label_under_all(self):
        from apps.cli.commands.job import _scope_label

        j = _job(_P1)
        scope = ProjectScope(project_id=_P1, all_projects=True, source="flag")
        assert _scope_label(j, scope) == ""
