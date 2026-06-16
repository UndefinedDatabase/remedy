"""Tests for packages/orchestration/project_registry.py (Project Registry v0)."""

from __future__ import annotations

import json
from uuid import UUID, uuid4

import pytest

from packages.orchestration.project_registry import (
    ProjectNotFoundError,
    RemyProject,
    attach_job,
    attach_repo,
    export_project_json,
    list_projects,
    load_project,
    save_project,
    summarize_project,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_project(**kwargs) -> RemyProject:
    defaults = {"name": "Test Project"}
    defaults.update(kwargs)
    return RemyProject(**defaults)


class _FakeJob:
    def __init__(self, job_id: str, state: str = "pending", tasks=(), artifacts=()):
        self.id = UUID(job_id)
        self.state = type("S", (), {"value": state})()
        self.tasks = list(tasks)
        self.artifacts = list(artifacts)
        self.name = f"Job {job_id[:8]}"


# ---------------------------------------------------------------------------
# Model field tests
# ---------------------------------------------------------------------------


class TestRemyProjectModel:
    def test_default_id_is_uuid(self):
        p = _make_project()
        assert isinstance(p.id, UUID)

    def test_name_is_required(self):
        with pytest.raises(Exception):
            RemyProject()  # type: ignore[call-arg]

    def test_description_optional(self):
        p = _make_project()
        assert p.description is None

    def test_description_set(self):
        p = _make_project(description="hello")
        assert p.description == "hello"

    def test_created_at_is_utc(self):
        p = _make_project()
        assert p.created_at.tzinfo is not None

    def test_repo_paths_default_empty(self):
        p = _make_project()
        assert p.repo_paths == []

    def test_job_ids_default_empty(self):
        p = _make_project()
        assert p.job_ids == []

    def test_metadata_default_empty(self):
        p = _make_project()
        assert p.metadata == {}


# ---------------------------------------------------------------------------
# Storage roundtrip
# ---------------------------------------------------------------------------


class TestSaveLoadRoundtrip:
    def test_save_creates_file(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        p = _make_project()
        save_project(p)
        stored = (tmp_path / "projects" / f"{p.id}.json")
        assert stored.exists()

    def test_load_roundtrip(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        p = _make_project(name="Roundtrip", description="desc")
        save_project(p)
        loaded = load_project(p.id)
        assert loaded.id == p.id
        assert loaded.name == "Roundtrip"
        assert loaded.description == "desc"

    def test_load_missing_raises(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        missing_id = uuid4()
        with pytest.raises(ProjectNotFoundError) as exc:
            load_project(missing_id)
        assert exc.value.project_id == missing_id

    def test_list_empty(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        assert list_projects() == []

    def test_list_returns_all(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        p1 = _make_project(name="Alpha")
        p2 = _make_project(name="Beta")
        save_project(p1)
        save_project(p2)
        projects = list_projects()
        assert len(projects) == 2
        names = {p.name for p in projects}
        assert names == {"Alpha", "Beta"}

    def test_list_sorted_newest_first(self, tmp_path, monkeypatch):
        import time
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        p1 = _make_project(name="First")
        time.sleep(0.01)
        p2 = _make_project(name="Second")
        save_project(p1)
        save_project(p2)
        projects = list_projects()
        assert projects[0].name == "Second"

    def test_list_skips_corrupt_file(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        p = _make_project(name="Valid")
        save_project(p)
        corrupt = tmp_path / "projects" / "corrupt.json"
        corrupt.write_text("not-json{{{")
        projects = list_projects()
        assert len(projects) == 1
        assert projects[0].name == "Valid"


# ---------------------------------------------------------------------------
# attach_repo
# ---------------------------------------------------------------------------


class TestAttachRepo:
    def test_attach_adds_resolved_path(self, tmp_path):
        p = _make_project()
        added = attach_repo(p, str(tmp_path))
        assert added is True
        assert str(tmp_path.resolve()) in p.repo_paths

    def test_attach_idempotent(self, tmp_path):
        p = _make_project()
        attach_repo(p, str(tmp_path))
        added_again = attach_repo(p, str(tmp_path))
        assert added_again is False
        assert len(p.repo_paths) == 1

    def test_attach_multiple(self, tmp_path):
        p = _make_project()
        d1 = tmp_path / "r1"
        d2 = tmp_path / "r2"
        d1.mkdir()
        d2.mkdir()
        attach_repo(p, str(d1))
        attach_repo(p, str(d2))
        assert len(p.repo_paths) == 2


# ---------------------------------------------------------------------------
# attach_job
# ---------------------------------------------------------------------------


class TestAttachJob:
    def test_attach_adds_job_id(self):
        p = _make_project()
        jid = str(uuid4())
        added = attach_job(p, jid)
        assert added is True
        assert jid in p.job_ids

    def test_attach_idempotent(self):
        p = _make_project()
        jid = str(uuid4())
        attach_job(p, jid)
        added_again = attach_job(p, jid)
        assert added_again is False
        assert p.job_ids.count(jid) == 1

    def test_attach_multiple_jobs(self):
        p = _make_project()
        j1 = str(uuid4())
        j2 = str(uuid4())
        attach_job(p, j1)
        attach_job(p, j2)
        assert len(p.job_ids) == 2


# ---------------------------------------------------------------------------
# summarize_project
# ---------------------------------------------------------------------------


class TestSummarizeProject:
    def test_contains_project_name(self):
        p = _make_project(name="MyApp")
        text = summarize_project(p, [])
        assert "MyApp" in text

    def test_contains_project_id(self):
        p = _make_project()
        text = summarize_project(p, [])
        assert str(p.id) in text

    def test_no_repos_shows_none(self):
        p = _make_project()
        text = summarize_project(p, [])
        assert "(none)" in text

    def test_repos_listed(self, tmp_path):
        p = _make_project()
        attach_repo(p, str(tmp_path))
        text = summarize_project(p, [])
        assert str(tmp_path.resolve()) in text

    def test_no_jobs_shows_none(self):
        p = _make_project()
        text = summarize_project(p, [])
        assert "(none)" in text

    def test_no_artifact_content(self):
        p = _make_project()
        text = summarize_project(p, [])
        assert "artifact_content" not in text
        assert "approval_reason" not in text
        assert "diff" not in text

    def test_project_brain_placeholder_note(self):
        p = _make_project()
        text = summarize_project(p, [])
        assert "not implemented" in text.lower()

    def test_jobs_shown_with_state(self):
        p = _make_project()
        jid = str(uuid4())
        attach_job(p, jid)
        job = _FakeJob(jid, state="pending")
        text = summarize_project(p, [job])
        assert jid[:8] in text
        assert "pending" in text


# ---------------------------------------------------------------------------
# export_project_json schema
# ---------------------------------------------------------------------------


class TestExportProjectJson:
    def test_version_is_1(self):
        p = _make_project()
        d = export_project_json(p, [])
        assert d["version"] == 1

    def test_project_keys(self):
        p = _make_project(name="X", description="Y")
        d = export_project_json(p, [])
        proj = d["project"]
        assert "id" in proj
        assert "name" in proj
        assert "description" in proj
        assert "created_at" in proj

    def test_repo_paths_key(self, tmp_path):
        p = _make_project()
        attach_repo(p, str(tmp_path))
        d = export_project_json(p, [])
        assert isinstance(d["repo_paths"], list)
        assert len(d["repo_paths"]) == 1

    def test_jobs_list_structure(self):
        p = _make_project()
        jid = str(uuid4())
        attach_job(p, jid)
        job = _FakeJob(jid, state="done")
        d = export_project_json(p, [job])
        assert len(d["jobs"]) == 1
        j = d["jobs"][0]
        assert "id" in j
        assert "state" in j
        assert "task_count" in j
        assert "artifact_count" in j

    def test_unknown_job_state(self):
        p = _make_project()
        jid = str(uuid4())
        attach_job(p, jid)
        d = export_project_json(p, [])  # jobs list empty → unknown
        assert d["jobs"][0]["state"] == "unknown"

    def test_counts_keys(self):
        p = _make_project()
        d = export_project_json(p, [])
        counts = d["counts"]
        for key in ("repo_count", "job_count", "task_count", "artifact_count"):
            assert key in counts

    def test_future_layers_all_not_implemented(self):
        p = _make_project()
        d = export_project_json(p, [])
        for v in d["future_layers"].values():
            assert v == "not_implemented"

    def test_future_layers_keys(self):
        p = _make_project()
        d = export_project_json(p, [])
        expected = {
            "repo_brain", "project_brain", "global_brain",
            "mempalace", "mcp_skill_registry",
        }
        assert set(d["future_layers"].keys()) == expected

    def test_json_serialisable(self):
        p = _make_project(name="Serial")
        d = export_project_json(p, [])
        text = json.dumps(d)
        assert "Serial" in text

    def test_no_artifact_content_in_export(self):
        p = _make_project()
        d = export_project_json(p, [])
        text = json.dumps(d)
        assert "artifact_content" not in text
        assert "approval_reason" not in text


# ---------------------------------------------------------------------------
# ProjectNotFoundError
# ---------------------------------------------------------------------------


class TestProjectNotFoundError:
    def test_message_contains_id(self):
        uid = uuid4()
        err = ProjectNotFoundError(uid)
        assert str(uid) in str(err)

    def test_project_id_attribute(self):
        uid = uuid4()
        err = ProjectNotFoundError(uid)
        assert err.project_id == uid
