"""Tests for F146 — project slug, legacy migration, and cwd resolution."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from uuid import uuid4

import pytest

from packages.orchestration.project_registry import (
    ProjectNotFoundError,
    RemyProject,
    _managed_worktree_parent,
    _migrate_legacy,
    find_project_by_repo,
    list_projects,
    load_project,
    require_project,
    resolve_project,
    save_project,
    select_project,
    slugify,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_project(**kwargs) -> RemyProject:
    defaults: dict = {"name": "Test Project"}
    defaults.update(kwargs)
    return RemyProject(**defaults)


def _init_git(path: Path) -> None:
    """Create a minimal bare-bones git repo at *path*."""
    path.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["git", "init", "--initial-branch=main"],
        cwd=str(path),
        capture_output=True,
        check=True,
    )
    subprocess.run(
        ["git", "commit", "--allow-empty", "-m", "init"],
        cwd=str(path),
        capture_output=True,
        check=True,
        env={
            "GIT_AUTHOR_NAME": "test",
            "GIT_AUTHOR_EMAIL": "t@t",
            "GIT_COMMITTER_NAME": "test",
            "GIT_COMMITTER_EMAIL": "t@t",
            "HOME": str(path),
            "PATH": "/usr/bin:/bin",
        },
    )


# ---------------------------------------------------------------------------
# slugify
# ---------------------------------------------------------------------------


class TestSlugify:
    def test_simple_name(self):
        assert slugify("My Project") == "my-project"

    def test_preserves_numbers(self):
        assert slugify("app2") == "app2"

    def test_strips_special_chars(self):
        assert slugify("Hello, World!") == "hello-world"

    def test_collapses_runs(self):
        assert slugify("a---b___c") == "a-b-c"

    def test_strips_leading_trailing_dashes(self):
        assert slugify("---hello---") == "hello"

    def test_empty_string_fallback(self):
        assert slugify("---") == "project"

    def test_already_kebab(self):
        assert slugify("my-app") == "my-app"

    def test_mixed_case(self):
        assert slugify("MyApp") == "myapp"

    def test_unicode_stripped(self):
        assert slugify("café") == "caf"

    def test_whitespace_trimmed(self):
        assert slugify("  hello  ") == "hello"


# ---------------------------------------------------------------------------
# New model fields
# ---------------------------------------------------------------------------


class TestNewFields:
    def test_slug_default_none(self):
        p = _make_project()
        assert p.slug is None

    def test_canonical_repo_path_default_none(self):
        p = _make_project()
        assert p.canonical_repo_path is None

    def test_slug_set(self):
        p = _make_project(slug="my-slug")
        assert p.slug == "my-slug"

    def test_canonical_repo_path_set(self):
        p = _make_project(canonical_repo_path="/some/path")
        assert p.canonical_repo_path == "/some/path"

    def test_roundtrip_with_new_fields(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        p = _make_project(slug="test-slug", canonical_repo_path="/repos/test")
        save_project(p)
        loaded = load_project(p.id)
        assert loaded.slug == "test-slug"
        assert loaded.canonical_repo_path == "/repos/test"


# ---------------------------------------------------------------------------
# Legacy migration
# ---------------------------------------------------------------------------


class TestLegacyMigration:
    def test_derives_slug_from_name(self):
        p = _make_project(name="My App")
        assert p.slug is None
        changed = _migrate_legacy(p)
        assert changed is True
        assert p.slug == "my-app"

    def test_derives_canonical_from_repo_paths(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        p = _make_project(repo_paths=[str(repo)])
        changed = _migrate_legacy(p)
        assert changed is True
        assert p.canonical_repo_path == str(repo.resolve())

    def test_no_change_when_already_set(self):
        p = _make_project(slug="existing", canonical_repo_path="/path")
        changed = _migrate_legacy(p)
        assert changed is False

    def test_no_canonical_without_repo_paths(self):
        p = _make_project()
        _migrate_legacy(p)
        assert p.canonical_repo_path is None

    def test_load_triggers_migration(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        p = _make_project(name="Legacy App")
        d = tmp_path / "projects"
        d.mkdir(parents=True, exist_ok=True)
        raw = p.model_dump_json(indent=2)
        data = json.loads(raw)
        data.pop("slug", None)
        data.pop("canonical_repo_path", None)
        (d / f"{p.id}.json").write_text(json.dumps(data, indent=2))
        loaded = load_project(p.id)
        assert loaded.slug == "legacy-app"
        persisted = json.loads((d / f"{p.id}.json").read_text())
        assert persisted["slug"] == "legacy-app"

    def test_list_triggers_migration(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        p = _make_project(name="List Migrate")
        d = tmp_path / "projects"
        d.mkdir(parents=True, exist_ok=True)
        raw = p.model_dump_json(indent=2)
        data = json.loads(raw)
        data.pop("slug", None)
        (d / f"{p.id}.json").write_text(json.dumps(data, indent=2))
        projects = list_projects()
        assert projects[0].slug == "list-migrate"

    def test_slug_collision_suffix(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        p1 = _make_project(name="App", slug="app")
        save_project(p1)
        p2 = _make_project(name="App")
        _migrate_legacy(p2)
        assert p2.slug == "app-2"

    def test_slug_collision_triple(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        p1 = _make_project(name="App", slug="app")
        save_project(p1)
        p2 = _make_project(name="App", slug="app-2")
        save_project(p2)
        p3 = _make_project(name="App")
        _migrate_legacy(p3)
        assert p3.slug == "app-3"


# ---------------------------------------------------------------------------
# ProjectNotFoundError extended
# ---------------------------------------------------------------------------


class TestProjectNotFoundErrorExtended:
    def test_uuid_form_unchanged(self):
        uid = uuid4()
        err = ProjectNotFoundError(uid)
        assert err.project_id == uid
        assert str(uid) in str(err)
        assert err.cwd is None

    def test_cwd_form_fix_it(self):
        err = ProjectNotFoundError(cwd="/some/repo")
        assert "remedy init" in str(err)
        assert err.cwd == "/some/repo"
        assert err.project_id is None


# ---------------------------------------------------------------------------
# Managed worktree parent mapping
# ---------------------------------------------------------------------------


class TestManagedWorktreeParent:
    def test_normal_path_returns_none(self):
        assert _managed_worktree_parent(Path("/home/user/repo")) is None

    def test_worktree_path_returns_parent(self):
        parent = _managed_worktree_parent(
            Path("/home/user/repo/.remedy-wt/job-123")
        )
        assert parent == Path("/home/user/repo")

    def test_nested_path_returns_first_parent(self):
        parent = _managed_worktree_parent(
            Path("/repos/myproject/.remedy-wt/j1/subdir")
        )
        assert parent == Path("/repos/myproject")


# ---------------------------------------------------------------------------
# find_project_by_repo
# ---------------------------------------------------------------------------


class TestFindProjectByRepo:
    def test_match_by_canonical(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        p = _make_project(
            slug="test", canonical_repo_path="/repos/test"
        )
        save_project(p)
        found = find_project_by_repo("/repos/test")
        assert found is not None
        assert found.id == p.id

    def test_match_by_repo_paths(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        p = _make_project(slug="test", repo_paths=["/repos/alt"])
        save_project(p)
        found = find_project_by_repo("/repos/alt")
        assert found is not None
        assert found.id == p.id

    def test_no_match(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        p = _make_project(slug="test", canonical_repo_path="/repos/test")
        save_project(p)
        assert find_project_by_repo("/repos/other") is None

    def test_duplicate_newest_wins(self, tmp_path, monkeypatch):
        import time

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        p_old = _make_project(
            name="Old", slug="old", canonical_repo_path="/repos/dup"
        )
        save_project(p_old)
        time.sleep(0.01)
        p_new = _make_project(
            name="New", slug="new", canonical_repo_path="/repos/dup"
        )
        save_project(p_new)
        found = find_project_by_repo("/repos/dup")
        assert found is not None
        assert found.id == p_new.id


# ---------------------------------------------------------------------------
# resolve_project
# ---------------------------------------------------------------------------


class TestResolveProject:
    def test_non_git_returns_none(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        d = tmp_path / "not-a-repo"
        d.mkdir()
        assert resolve_project(d) is None

    def test_unregistered_git_returns_none(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        repo = tmp_path / "myrepo"
        _init_git(repo)
        assert resolve_project(repo) is None

    def test_registered_repo_resolves(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        repo = tmp_path / "myrepo"
        _init_git(repo)
        p = _make_project(
            slug="myrepo",
            canonical_repo_path=str(repo.resolve()),
        )
        save_project(p)
        found = resolve_project(repo)
        assert found is not None
        assert found.id == p.id

    def test_subdir_resolves_to_repo_root(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        repo = tmp_path / "myrepo"
        _init_git(repo)
        sub = repo / "src" / "deep"
        sub.mkdir(parents=True)
        p = _make_project(
            slug="myrepo",
            canonical_repo_path=str(repo.resolve()),
        )
        save_project(p)
        found = resolve_project(sub)
        assert found is not None
        assert found.id == p.id

    def test_symlink_resolves(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        repo = tmp_path / "real-repo"
        _init_git(repo)
        link = tmp_path / "link-repo"
        link.symlink_to(repo)
        p = _make_project(
            slug="real-repo",
            canonical_repo_path=str(repo.resolve()),
        )
        save_project(p)
        found = resolve_project(link)
        assert found is not None
        assert found.id == p.id


# ---------------------------------------------------------------------------
# require_project
# ---------------------------------------------------------------------------


class TestRequireProject:
    def test_returns_project_when_found(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        repo = tmp_path / "myrepo"
        _init_git(repo)
        p = _make_project(
            slug="myrepo",
            canonical_repo_path=str(repo.resolve()),
        )
        save_project(p)
        found = require_project(repo)
        assert found.id == p.id

    def test_raises_with_fix_it(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        repo = tmp_path / "unknown"
        _init_git(repo)
        with pytest.raises(ProjectNotFoundError) as exc:
            require_project(repo)
        assert "remedy init" in str(exc.value)
        assert exc.value.cwd == str(repo)

    def test_raises_for_non_git(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        d = tmp_path / "not-git"
        d.mkdir()
        with pytest.raises(ProjectNotFoundError) as exc:
            require_project(d)
        assert "remedy init" in str(exc.value)


# ---------------------------------------------------------------------------
# Same-dirname distinct slugs
# ---------------------------------------------------------------------------


class TestSameDirnameDistinctSlugs:
    def test_two_projects_same_name_get_distinct_slugs(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        p1 = _make_project(name="myapp", slug="myapp")
        save_project(p1)
        p2 = _make_project(name="myapp")
        _migrate_legacy(p2)
        assert p2.slug == "myapp-2"
        assert p1.slug != p2.slug


# ---------------------------------------------------------------------------
# T002 — select_project precedence
# ---------------------------------------------------------------------------


class TestSelectProject:
    """Full precedence matrix: flag > env > cwd > error."""

    def _setup_repo_and_project(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        repo = tmp_path / "myrepo"
        _init_git(repo)
        p = _make_project(
            slug="myrepo",
            canonical_repo_path=str(repo.resolve()),
        )
        save_project(p)
        return repo, p

    def test_flag_uuid(self, tmp_path, monkeypatch):
        repo, p = self._setup_repo_and_project(tmp_path, monkeypatch)
        found, source = select_project(str(p.id), repo)
        assert found.id == p.id
        assert source == "flag"

    def test_flag_slug(self, tmp_path, monkeypatch):
        repo, p = self._setup_repo_and_project(tmp_path, monkeypatch)
        found, source = select_project("myrepo", repo)
        assert found.id == p.id
        assert source == "flag"

    def test_env_uuid(self, tmp_path, monkeypatch):
        repo, p = self._setup_repo_and_project(tmp_path, monkeypatch)
        monkeypatch.setenv("REMEDY_PROJECT", str(p.id))
        found, source = select_project(None, repo)
        assert found.id == p.id
        assert source == "env"

    def test_env_slug(self, tmp_path, monkeypatch):
        repo, p = self._setup_repo_and_project(tmp_path, monkeypatch)
        monkeypatch.setenv("REMEDY_PROJECT", "myrepo")
        found, source = select_project(None, repo)
        assert found.id == p.id
        assert source == "env"

    def test_cwd_autodetection(self, tmp_path, monkeypatch):
        repo, p = self._setup_repo_and_project(tmp_path, monkeypatch)
        monkeypatch.delenv("REMEDY_PROJECT", raising=False)
        found, source = select_project(None, repo)
        assert found.id == p.id
        assert source == "cwd"

    def test_error_when_nothing_matches(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        monkeypatch.delenv("REMEDY_PROJECT", raising=False)
        d = tmp_path / "nope"
        _init_git(d)
        with pytest.raises(ProjectNotFoundError):
            select_project(None, d)

    def test_flag_beats_env(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        repo = tmp_path / "r"
        _init_git(repo)
        p1 = _make_project(name="flag-proj", slug="flag-proj")
        save_project(p1)
        p2 = _make_project(name="env-proj", slug="env-proj")
        save_project(p2)
        monkeypatch.setenv("REMEDY_PROJECT", "env-proj")
        found, source = select_project("flag-proj", repo)
        assert found.id == p1.id
        assert source == "flag"

    def test_env_beats_cwd(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        repo = tmp_path / "r"
        _init_git(repo)
        p_cwd = _make_project(
            name="cwd-proj",
            slug="cwd-proj",
            canonical_repo_path=str(repo.resolve()),
        )
        save_project(p_cwd)
        p_env = _make_project(name="env-proj", slug="env-proj")
        save_project(p_env)
        monkeypatch.setenv("REMEDY_PROJECT", "env-proj")
        found, source = select_project(None, repo)
        assert found.id == p_env.id
        assert source == "env"

    def test_flag_beats_env_and_cwd(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        repo = tmp_path / "r"
        _init_git(repo)
        p_flag = _make_project(name="flag", slug="flag-p")
        save_project(p_flag)
        p_env = _make_project(name="env", slug="env-p")
        save_project(p_env)
        p_cwd = _make_project(
            name="cwd",
            slug="cwd-p",
            canonical_repo_path=str(repo.resolve()),
        )
        save_project(p_cwd)
        monkeypatch.setenv("REMEDY_PROJECT", "env-p")
        found, source = select_project("flag-p", repo)
        assert found.id == p_flag.id
        assert source == "flag"

    def test_empty_flag_treated_as_absent(self, tmp_path, monkeypatch):
        repo, p = self._setup_repo_and_project(tmp_path, monkeypatch)
        monkeypatch.delenv("REMEDY_PROJECT", raising=False)
        found, source = select_project("  ", repo)
        assert source == "cwd"

    def test_empty_env_treated_as_absent(self, tmp_path, monkeypatch):
        repo, p = self._setup_repo_and_project(tmp_path, monkeypatch)
        monkeypatch.setenv("REMEDY_PROJECT", "  ")
        found, source = select_project(None, repo)
        assert source == "cwd"

    def test_invalid_flag_raises(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        d = tmp_path / "x"
        d.mkdir()
        with pytest.raises(ProjectNotFoundError):
            select_project("nonexistent-slug", d)
