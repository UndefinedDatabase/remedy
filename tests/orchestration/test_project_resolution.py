"""Tests for F146 — project slug, legacy migration, cwd resolution, selection, and registry integrity."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from uuid import uuid4

import pytest

from packages.orchestration.project_registry import (
    AmbiguousProjectError,
    InvalidProjectSelectorError,
    NotAGitRepoError,
    ProjectNotFoundError,
    RemyProject,
    RepoOwnershipConflictError,
    _list_projects_readonly,
    _load_project_readonly,
    _lookup_by_slug_or_uuid_readonly,
    _managed_worktree_parent,
    _migrate_legacy,
    _project_set_readonly,
    attach_repo_canonical,
    find_project_by_repo,
    list_projects,
    load_project,
    migrate_legacy_projects,
    register_project_repo,
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
# 1. slugify
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
# 2. New model fields
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
# 3. Atomic save
# ---------------------------------------------------------------------------


class TestAtomicSave:
    def test_save_uses_atomic_replace(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        p = _make_project(slug="atomic")
        save_project(p)
        target = tmp_path / "projects" / f"{p.id}.json"
        assert target.exists()
        data = json.loads(target.read_text())
        assert data["slug"] == "atomic"

    def test_no_partial_on_failure(self, tmp_path, monkeypatch):
        """No .tmp files should linger after a successful save."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        p = _make_project(slug="partial-test")
        save_project(p)
        tmp_files = list((tmp_path / "projects").glob("*.tmp"))
        assert tmp_files == []


# ---------------------------------------------------------------------------
# 4. Legacy migration
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
# 5. Read-only resolution proof (bytes/mtime)
# ---------------------------------------------------------------------------


class TestReadOnlyResolution:
    def test_resolve_does_not_write(self, tmp_path, monkeypatch):
        """resolve_project must not modify any project file on disk."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        repo = tmp_path / "myrepo"
        _init_git(repo)
        p = _make_project(slug="myrepo", canonical_repo_path=str(repo.resolve()))
        save_project(p)

        proj_file = tmp_path / "projects" / f"{p.id}.json"
        before_bytes = proj_file.read_bytes()
        before_mtime = proj_file.stat().st_mtime_ns

        found = resolve_project(repo)
        assert found is not None
        assert found.id == p.id

        after_bytes = proj_file.read_bytes()
        after_mtime = proj_file.stat().st_mtime_ns
        assert before_bytes == after_bytes
        assert before_mtime == after_mtime

    def test_resolve_legacy_project_does_not_write(self, tmp_path, monkeypatch):
        """resolve_project on a legacy record (no slug) must not persist migration."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        repo = tmp_path / "myrepo"
        _init_git(repo)
        d = tmp_path / "projects"
        d.mkdir(parents=True, exist_ok=True)
        p = _make_project(name="Legacy")
        data = json.loads(p.model_dump_json(indent=2))
        data.pop("slug", None)
        data["canonical_repo_path"] = str(repo.resolve())
        data["repo_paths"] = [str(repo.resolve())]
        (d / f"{p.id}.json").write_text(json.dumps(data, indent=2))

        before_bytes = (d / f"{p.id}.json").read_bytes()
        before_mtime = (d / f"{p.id}.json").stat().st_mtime_ns

        found = resolve_project(repo)
        assert found is not None

        after_bytes = (d / f"{p.id}.json").read_bytes()
        after_mtime = (d / f"{p.id}.json").stat().st_mtime_ns
        assert before_bytes == after_bytes
        assert before_mtime == after_mtime


# ---------------------------------------------------------------------------
# 6. ProjectNotFoundError
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
# 7. AmbiguousProjectError
# ---------------------------------------------------------------------------


class TestAmbiguousProjectError:
    def test_duplicate_slug_raises(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        d = tmp_path / "projects"
        d.mkdir(parents=True, exist_ok=True)
        p1 = _make_project(name="App", slug="app")
        p2 = _make_project(name="App2", slug="app")
        (d / f"{p1.id}.json").write_text(p1.model_dump_json(indent=2))
        (d / f"{p2.id}.json").write_text(p2.model_dump_json(indent=2))
        with pytest.raises(AmbiguousProjectError) as exc:
            _lookup_by_slug_or_uuid_readonly("app")
        assert exc.value.slug == "app"
        assert len(exc.value.project_ids) == 2


# ---------------------------------------------------------------------------
# 8. Managed worktree parent mapping
# ---------------------------------------------------------------------------


class TestManagedWorktreeParent:
    def test_normal_path_returns_none(self):
        assert _managed_worktree_parent(Path("/home/user/repo")) is None

    def test_worktree_path_without_git_returns_none(self, tmp_path):
        """A path with .remedy-wt component but no git common-dir is not trusted."""
        wt = tmp_path / "repo" / ".remedy-wt" / "job-123"
        wt.mkdir(parents=True)
        result = _managed_worktree_parent(wt)
        assert result is None


# ---------------------------------------------------------------------------
# 9. find_project_by_repo
# ---------------------------------------------------------------------------


class TestFindProjectByRepo:
    def test_match_by_canonical(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        p = _make_project(slug="test", canonical_repo_path="/repos/test")
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
# 10. resolve_project
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
# 11. require_project
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
# 12. Same-dirname distinct slugs
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
# 13. select_project precedence
# ---------------------------------------------------------------------------


class TestSelectProject:
    """Full precedence matrix: flag > environment > cwd > error."""

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
        assert source == "environment"

    def test_env_slug(self, tmp_path, monkeypatch):
        repo, p = self._setup_repo_and_project(tmp_path, monkeypatch)
        monkeypatch.setenv("REMEDY_PROJECT", "myrepo")
        found, source = select_project(None, repo)
        assert found.id == p.id
        assert source == "environment"

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
        assert source == "environment"

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

    def test_empty_flag_raises_invalid(self, tmp_path, monkeypatch):
        repo, p = self._setup_repo_and_project(tmp_path, monkeypatch)
        monkeypatch.delenv("REMEDY_PROJECT", raising=False)
        with pytest.raises(InvalidProjectSelectorError) as exc:
            select_project("  ", repo)
        assert exc.value.source == "flag"

    def test_empty_env_raises_invalid(self, tmp_path, monkeypatch):
        repo, p = self._setup_repo_and_project(tmp_path, monkeypatch)
        monkeypatch.setenv("REMEDY_PROJECT", "  ")
        with pytest.raises(InvalidProjectSelectorError) as exc:
            select_project(None, repo)
        assert exc.value.source == "environment"

    def test_invalid_flag_raises(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        d = tmp_path / "x"
        d.mkdir()
        with pytest.raises(ProjectNotFoundError):
            select_project("nonexistent-slug", d)


# ---------------------------------------------------------------------------
# 14. Registration primitive
# ---------------------------------------------------------------------------


class TestRegisterProjectRepo:
    def test_creates_with_slug_and_canonical(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        repo = tmp_path / "myrepo"
        _init_git(repo)
        p = register_project_repo("My Repo", str(repo))
        assert p.slug is not None
        assert p.slug == "myrepo"
        assert p.canonical_repo_path == str(repo.resolve())

    def test_same_repo_returns_existing(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        repo = tmp_path / "myrepo"
        _init_git(repo)
        p1 = register_project_repo("My Repo", str(repo))
        p2 = register_project_repo("My Repo Again", str(repo))
        assert p1.id == p2.id

    def test_create_project_assigns_slug_immediately(self, tmp_path, monkeypatch):
        """_cmd_create_project must assign slug immediately, not null."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        import contextlib
        import io

        from apps.cli.commands.project import _cmd_create_project
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            _cmd_create_project("New App", None)
        uid_str = buf.getvalue().strip()
        from uuid import UUID
        loaded = load_project(UUID(uid_str))
        assert loaded.slug is not None
        assert loaded.slug == "new-app"

    def test_rejects_non_git_directory(self, tmp_path, monkeypatch):
        """register_project_repo must raise NotAGitRepoError for a plain dir."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        plain = tmp_path / "not-a-repo"
        plain.mkdir()
        with pytest.raises(NotAGitRepoError):
            register_project_repo("Test", str(plain))

    def test_slug_from_repo_dir_name(self, tmp_path, monkeypatch):
        """Slug must derive from the repository directory name, not display name."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        repo = tmp_path / "my-cool-repo"
        _init_git(repo)
        p = register_project_repo("Some Display Name", str(repo))
        assert p.slug == "my-cool-repo"


# ---------------------------------------------------------------------------
# 15. Slug validation in save_project
# ---------------------------------------------------------------------------


class TestSlugValidation:
    def test_null_slug_auto_derives(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        p = _make_project(slug=None, name="Auto Derive")
        save_project(p)
        assert p.slug == "auto-derive"

    def test_rejects_empty_slug(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        p = _make_project(slug="")
        with pytest.raises(ValueError, match="must not be empty"):
            save_project(p)

    def test_rejects_non_kebab(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        p = _make_project(slug="Not Kebab Case")
        with pytest.raises(ValueError, match="not valid kebab-case"):
            save_project(p)

    def test_rejects_uppercase(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        p = _make_project(slug="MyApp")
        with pytest.raises(ValueError, match="not valid kebab-case"):
            save_project(p)

    def test_rejects_duplicate_slug(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        p1 = _make_project(slug="taken")
        save_project(p1)
        p2 = _make_project(slug="taken")
        with pytest.raises(ValueError, match="already used"):
            save_project(p2)

    def test_allows_same_project_resave(self, tmp_path, monkeypatch):
        """Re-saving a project with its own slug must not raise duplicate."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        p = _make_project(slug="resave")
        save_project(p)
        p.name = "Updated Name"
        save_project(p)
        loaded = load_project(p.id)
        assert loaded.name == "Updated Name"
        assert loaded.slug == "resave"


# ---------------------------------------------------------------------------
# 16. Deterministic batch migration ordering
# ---------------------------------------------------------------------------


class TestDeterministicMigration:
    def test_migration_order_by_created_at_then_uuid(self, tmp_path, monkeypatch):
        """Batch migration must sort by (created_at asc, UUID asc) before allocating slugs."""
        from datetime import datetime, timezone

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        d = tmp_path / "projects"
        d.mkdir(parents=True, exist_ok=True)

        t1 = datetime(2024, 1, 1, tzinfo=timezone.utc)
        t2 = datetime(2024, 1, 2, tzinfo=timezone.utc)

        id_a = uuid4()
        id_b = uuid4()
        earlier_id, later_id = sorted([id_a, id_b], key=str)

        p_later = _make_project(name="App")
        p_later.id = later_id
        p_later.created_at = t1
        raw_later = json.loads(p_later.model_dump_json())
        raw_later.pop("slug", None)
        (d / f"{later_id}.json").write_text(json.dumps(raw_later))

        p_earlier = _make_project(name="App")
        p_earlier.id = earlier_id
        p_earlier.created_at = t1
        raw_earlier = json.loads(p_earlier.model_dump_json())
        raw_earlier.pop("slug", None)
        (d / f"{earlier_id}.json").write_text(json.dumps(raw_earlier))

        count = migrate_legacy_projects()
        assert count == 2

        loaded_earlier = load_project(earlier_id)
        loaded_later = load_project(later_id)
        assert loaded_earlier.slug == "app"
        assert loaded_later.slug == "app-2"

    def test_migration_skips_already_migrated(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        p = _make_project(slug="existing")
        save_project(p)
        count = migrate_legacy_projects()
        assert count == 0


# ---------------------------------------------------------------------------
# 17. Read-only lookup (flag/env)
# ---------------------------------------------------------------------------


class TestReadOnlyLookup:
    def test_flag_lookup_does_not_write(self, tmp_path, monkeypatch):
        """select_project(flag=...) must never write to disk."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        monkeypatch.delenv("REMEDY_PROJECT", raising=False)
        d = tmp_path / "projects"
        d.mkdir(parents=True, exist_ok=True)
        p = _make_project(name="Legacy Flag")
        raw = json.loads(p.model_dump_json())
        raw.pop("slug", None)
        raw["repo_paths"] = ["/some/repo"]
        (d / f"{p.id}.json").write_text(json.dumps(raw))

        before_bytes = (d / f"{p.id}.json").read_bytes()
        before_mtime = (d / f"{p.id}.json").stat().st_mtime_ns

        found, source = select_project(str(p.id), tmp_path)
        assert found.id == p.id
        assert source == "flag"

        after_bytes = (d / f"{p.id}.json").read_bytes()
        after_mtime = (d / f"{p.id}.json").stat().st_mtime_ns
        assert before_bytes == after_bytes
        assert before_mtime == after_mtime

    def test_env_lookup_does_not_write(self, tmp_path, monkeypatch):
        """select_project via REMEDY_PROJECT must never write to disk."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        d = tmp_path / "projects"
        d.mkdir(parents=True, exist_ok=True)
        p = _make_project(name="Legacy Env")
        raw = json.loads(p.model_dump_json())
        raw.pop("slug", None)
        (d / f"{p.id}.json").write_text(json.dumps(raw))
        monkeypatch.setenv("REMEDY_PROJECT", str(p.id))

        before_bytes = (d / f"{p.id}.json").read_bytes()
        before_mtime = (d / f"{p.id}.json").stat().st_mtime_ns

        found, source = select_project(None, tmp_path)
        assert found.id == p.id
        assert source == "environment"

        after_bytes = (d / f"{p.id}.json").read_bytes()
        after_mtime = (d / f"{p.id}.json").stat().st_mtime_ns
        assert before_bytes == after_bytes
        assert before_mtime == after_mtime


# ---------------------------------------------------------------------------
# 18. Unknown selector diagnostics
# ---------------------------------------------------------------------------


class TestUnknownSelectorDiagnostics:
    def test_flag_not_found_includes_value_and_source(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        monkeypatch.delenv("REMEDY_PROJECT", raising=False)
        with pytest.raises(ProjectNotFoundError) as exc:
            select_project("nonexistent-slug", tmp_path)
        assert "nonexistent-slug" in str(exc.value)
        assert "flag" in str(exc.value)
        assert exc.value.selector_value == "nonexistent-slug"
        assert exc.value.selector_source == "flag"

    def test_env_not_found_includes_value_and_source(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        monkeypatch.setenv("REMEDY_PROJECT", "ghost-proj")
        with pytest.raises(ProjectNotFoundError) as exc:
            select_project(None, tmp_path)
        assert "ghost-proj" in str(exc.value)
        assert "environment" in str(exc.value)
        assert exc.value.selector_value == "ghost-proj"
        assert exc.value.selector_source == "environment"


# ---------------------------------------------------------------------------
# 19. Canonical attach service
# ---------------------------------------------------------------------------


class TestCanonicalAttach:
    def test_attach_new_repo(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        repo = tmp_path / "myrepo"
        _init_git(repo)
        p = _make_project(slug="proj", canonical_repo_path=str(repo.resolve()),
                          repo_paths=[str(repo.resolve())])
        save_project(p)
        repo2 = tmp_path / "repo2"
        _init_git(repo2)
        changed, real = attach_repo_canonical(p, str(repo2))
        assert changed is True
        assert real == str(repo2.resolve())
        loaded = load_project(p.id)
        assert real in loaded.repo_paths

    def test_attach_dedup_same_path(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        repo = tmp_path / "myrepo"
        _init_git(repo)
        p = _make_project(slug="proj", canonical_repo_path=str(repo.resolve()),
                          repo_paths=[str(repo.resolve())])
        save_project(p)
        changed, real = attach_repo_canonical(p, str(repo))
        assert changed is False

    def test_attach_rebinds_canonical(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        repo1 = tmp_path / "repo1"
        _init_git(repo1)
        repo2 = tmp_path / "repo2"
        _init_git(repo2)
        p = _make_project(slug="proj", canonical_repo_path=str(repo1.resolve()),
                          repo_paths=[str(repo1.resolve())])
        save_project(p)
        changed, real = attach_repo_canonical(p, str(repo2))
        assert changed is True
        assert p.canonical_repo_path == str(repo2.resolve())

    def test_attach_rejects_non_git(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        p = _make_project(slug="proj")
        save_project(p)
        plain = tmp_path / "not-git"
        plain.mkdir()
        with pytest.raises(NotAGitRepoError):
            attach_repo_canonical(p, str(plain))

    def test_attach_rejects_ownership_conflict(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        repo = tmp_path / "shared-repo"
        _init_git(repo)
        p1 = _make_project(slug="owner", canonical_repo_path=str(repo.resolve()),
                           repo_paths=[str(repo.resolve())])
        save_project(p1)
        p2 = _make_project(slug="intruder")
        save_project(p2)
        with pytest.raises(RepoOwnershipConflictError):
            attach_repo_canonical(p2, str(repo))

    def test_attach_dedup_repo_paths(self, tmp_path, monkeypatch):
        """After canonical rebind, repo_paths must have no duplicates."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        repo = tmp_path / "myrepo"
        _init_git(repo)
        real = str(repo.resolve())
        p = _make_project(slug="proj", canonical_repo_path=real,
                          repo_paths=[real, real])
        save_project(p)
        changed, _ = attach_repo_canonical(p, str(repo))
        assert changed is True
        loaded = load_project(p.id)
        assert loaded.repo_paths.count(real) == 1


# ---------------------------------------------------------------------------
# 20. Feature-aware runtime integration gate
# ---------------------------------------------------------------------------


class TestFeatureAwareGate:
    def test_f146_gate_excludes_f018_checks(self):
        from packages.orchestration.runtime_integration_gate import (
            _select_checks_for_feature,
        )

        static, bindings = _select_checks_for_feature("f146")
        check_ids = [c["check_id"] for c in static]
        binding_ids = [b["check_id"] for b in bindings]

        assert all(not cid.startswith("f018_") for cid in check_ids)
        assert all(cid.startswith("f146_") for cid in binding_ids)
        assert any(cid.startswith("f146_") for cid in check_ids)
        assert any(cid.startswith("job_evidence_") for cid in check_ids)

    def test_none_feature_returns_all(self):
        from packages.orchestration.runtime_integration_gate import (
            INTEGRATION_CHECKS,
            TEST_EXECUTION_BINDINGS,
            _select_checks_for_feature,
        )

        static, bindings = _select_checks_for_feature(None)
        assert len(static) == len(INTEGRATION_CHECKS)
        assert len(bindings) == len(TEST_EXECUTION_BINDINGS)

    def test_f146_gate_builds_successfully(self, tmp_path):
        from packages.orchestration.runtime_integration_gate import (
            build_runtime_integration_gate,
        )

        gate = build_runtime_integration_gate(
            str(Path(__file__).resolve().parents[2]),
            feature_id="f146",
        )
        assert gate["schema_version"] == "1.1.0"
        assert "checks_total" in gate
        f146_checks = [c for c in gate["checks"] if c["check_id"].startswith("f146_")]
        assert len(f146_checks) > 0
        f018_checks = [c for c in gate["checks"] if c["check_id"].startswith("f018_")]
        assert len(f018_checks) == 0


# ---------------------------------------------------------------------------
# R4: Deterministic read-only projection
# ---------------------------------------------------------------------------


class TestDeterministicReadonlyProjection:
    """_project_set_readonly allocates unique slugs across the full set
    deterministically, regardless of disk enumeration order."""

    def test_reverse_order_same_slugs(self, tmp_path, monkeypatch):
        """Two same-name legacy projects get consistent slugs regardless of load order."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        d = tmp_path / "projects"
        d.mkdir(parents=True, exist_ok=True)

        from datetime import datetime, timezone
        t1 = datetime(2024, 1, 1, tzinfo=timezone.utc)
        t2 = datetime(2024, 1, 2, tzinfo=timezone.utc)

        p1 = _make_project(name="My App", created_at=t1)
        p2 = _make_project(name="My App", created_at=t2)

        data1 = json.loads(p1.model_dump_json())
        data2 = json.loads(p2.model_dump_json())
        data1.pop("slug", None)
        data2.pop("slug", None)
        (d / f"{p1.id}.json").write_text(json.dumps(data1))
        (d / f"{p2.id}.json").write_text(json.dumps(data2))

        result = _project_set_readonly()
        slugs = {str(p.id): p.slug for p in result}

        assert slugs[str(p1.id)] == "my-app"
        assert slugs[str(p2.id)] == "my-app-2"

    def test_projection_never_writes(self, tmp_path, monkeypatch):
        """_project_set_readonly must not modify any file on disk."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        d = tmp_path / "projects"
        d.mkdir(parents=True, exist_ok=True)

        p = _make_project(name="NoWrite")
        data = json.loads(p.model_dump_json())
        data.pop("slug", None)
        f = d / f"{p.id}.json"
        f.write_text(json.dumps(data))

        before_bytes = f.read_bytes()
        before_mtime = f.stat().st_mtime_ns

        result = _project_set_readonly()
        assert len(result) == 1
        assert result[0].slug == "nowrite"

        assert f.read_bytes() == before_bytes
        assert f.stat().st_mtime_ns == before_mtime

    def test_persisted_slug_reserved(self, tmp_path, monkeypatch):
        """A project with persisted slug keeps it; legacy record gets suffix."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        d = tmp_path / "projects"
        d.mkdir(parents=True, exist_ok=True)

        p1 = _make_project(name="Widget", slug="widget")
        save_project(p1)

        from datetime import datetime, timezone
        p2 = _make_project(name="Widget", created_at=datetime(2020, 1, 1, tzinfo=timezone.utc))
        data2 = json.loads(p2.model_dump_json())
        data2.pop("slug", None)
        (d / f"{p2.id}.json").write_text(json.dumps(data2))

        result = _project_set_readonly()
        slugs = {str(p.id): p.slug for p in result}
        assert slugs[str(p1.id)] == "widget"
        assert slugs[str(p2.id)] == "widget-2"

    def test_load_readonly_uses_projection(self, tmp_path, monkeypatch):
        """_load_project_readonly returns deterministic slug from full-set projection."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        d = tmp_path / "projects"
        d.mkdir(parents=True, exist_ok=True)

        from datetime import datetime, timezone
        p1 = _make_project(name="Dup", created_at=datetime(2024, 1, 1, tzinfo=timezone.utc))
        p2 = _make_project(name="Dup", created_at=datetime(2024, 6, 1, tzinfo=timezone.utc))

        for p in [p1, p2]:
            data = json.loads(p.model_dump_json())
            data.pop("slug", None)
            (d / f"{p.id}.json").write_text(json.dumps(data))

        loaded = _load_project_readonly(d / f"{p1.id}.json")
        assert loaded.slug == "dup"

        loaded2 = _load_project_readonly(d / f"{p2.id}.json")
        assert loaded2.slug == "dup-2"

    def test_list_readonly_sorted_newest_first(self, tmp_path, monkeypatch):
        """_list_projects_readonly returns projects sorted by created_at descending."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        d = tmp_path / "projects"
        d.mkdir(parents=True, exist_ok=True)

        from datetime import datetime, timezone
        p1 = _make_project(name="Old", slug="old", created_at=datetime(2023, 1, 1, tzinfo=timezone.utc))
        p2 = _make_project(name="New", slug="new", created_at=datetime(2025, 1, 1, tzinfo=timezone.utc))
        save_project(p1)
        save_project(p2)

        result = _list_projects_readonly()
        assert result[0].name == "New"
        assert result[1].name == "Old"


# ---------------------------------------------------------------------------
# R4: Gate feature_id propagation
# ---------------------------------------------------------------------------


class TestGateFeatureId:
    def test_feature_id_in_output(self):
        from packages.orchestration.runtime_integration_gate import (
            build_runtime_integration_gate,
        )
        gate = build_runtime_integration_gate(
            str(Path(__file__).resolve().parents[2]),
            feature_id="f146",
        )
        assert gate["feature_id"] == "f146"

    def test_no_feature_id_when_none(self):
        from packages.orchestration.runtime_integration_gate import (
            build_runtime_integration_gate,
        )
        gate = build_runtime_integration_gate(
            str(Path(__file__).resolve().parents[2]),
        )
        assert "feature_id" not in gate

    def test_f146_registry_binding_exists(self):
        from packages.orchestration.runtime_integration_gate import (
            TEST_EXECUTION_BINDINGS,
        )
        ids = [b["check_id"] for b in TEST_EXECUTION_BINDINGS]
        assert "f146_test_registry_execution" in ids

    def test_refresh_preserves_feature_id(self, tmp_path):
        """refresh_staged_evidence reads feature_id from existing gate and propagates."""
        import os
        import sys
        sys.path.insert(0, os.path.abspath("."))

        from packages.orchestration.runtime_integration_gate import (
            build_runtime_integration_gate,
        )
        repo_root = str(Path(__file__).resolve().parents[2])

        gate = build_runtime_integration_gate(repo_root, feature_id="f146")
        gate_path = tmp_path / "runtime_integration_gate.json"
        gate_path.write_text(json.dumps(gate, indent=1, sort_keys=True))

        from scripts.refresh_review_evidence import refresh_staged_evidence
        report = refresh_staged_evidence(str(tmp_path), repo_root)

        refreshed_gate = json.loads(gate_path.read_text())
        assert refreshed_gate.get("feature_id") == "f146"
        assert not report["issues"]

    def test_refresh_without_feature_id(self, tmp_path):
        """refresh_staged_evidence with no feature_id produces gate without it."""
        from packages.orchestration.runtime_integration_gate import (
            build_runtime_integration_gate,
        )
        repo_root = str(Path(__file__).resolve().parents[2])

        gate = build_runtime_integration_gate(repo_root)
        gate_path = tmp_path / "runtime_integration_gate.json"
        gate_path.write_text(json.dumps(gate, indent=1, sort_keys=True))

        from scripts.refresh_review_evidence import refresh_staged_evidence
        report = refresh_staged_evidence(str(tmp_path), repo_root)

        refreshed_gate = json.loads(gate_path.read_text())
        assert "feature_id" not in refreshed_gate
