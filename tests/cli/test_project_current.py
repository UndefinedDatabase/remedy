"""Tests for F146 CLI — project current, project attach, workspace-key guard."""

from __future__ import annotations

import ast
import json
import subprocess
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _init_git(path: Path) -> None:
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


def _make_and_save(tmp_path, monkeypatch, **kwargs):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    from packages.orchestration.project_registry import RemyProject, save_project

    defaults = {"name": "Test Project"}
    defaults.update(kwargs)
    p = RemyProject(**defaults)
    save_project(p)
    return p


# ---------------------------------------------------------------------------
# _cmd_project_current — exact JSON schema
# ---------------------------------------------------------------------------


class TestProjectCurrentCommand:
    def test_shows_slug_and_id(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        monkeypatch.delenv("REMEDY_PROJECT", raising=False)
        repo = tmp_path / "myrepo"
        _init_git(repo)
        p = _make_and_save(
            tmp_path,
            monkeypatch,
            slug="myrepo",
            canonical_repo_path=str(repo.resolve()),
        )
        monkeypatch.chdir(repo)

        from apps.cli.commands.project import _cmd_project_current

        _cmd_project_current()
        out = capsys.readouterr().out
        assert "myrepo" in out
        assert str(p.id) in out

    def test_json_output_exact_schema(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        monkeypatch.delenv("REMEDY_PROJECT", raising=False)
        repo = tmp_path / "myrepo"
        _init_git(repo)
        p = _make_and_save(
            tmp_path,
            monkeypatch,
            slug="myrepo",
            canonical_repo_path=str(repo.resolve()),
            job_ids=["j1", "j2", "j3"],
        )
        monkeypatch.chdir(repo)

        from apps.cli.commands.project import _cmd_project_current

        _cmd_project_current(json_output=True)
        out = capsys.readouterr().out
        data = json.loads(out)
        assert data["project_id"] == str(p.id)
        assert data["slug"] == "myrepo"
        assert data["repo"] == str(repo.resolve())
        assert data["job_count"] == 3
        assert data["selection_source"] == "cwd"
        assert set(data.keys()) == {"project_id", "slug", "repo", "job_count", "selection_source"}

    def test_exit_3_when_unresolved(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        monkeypatch.delenv("REMEDY_PROJECT", raising=False)
        repo = tmp_path / "unknown"
        _init_git(repo)
        monkeypatch.chdir(repo)

        from apps.cli.commands.project import _cmd_project_current

        with pytest.raises(SystemExit) as exc:
            _cmd_project_current()
        assert exc.value.code == 3

    def test_project_flag_overrides_cwd(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        monkeypatch.delenv("REMEDY_PROJECT", raising=False)
        repo = tmp_path / "myrepo"
        _init_git(repo)
        _make_and_save(
            tmp_path, monkeypatch,
            slug="cwd-proj",
            canonical_repo_path=str(repo.resolve()),
        )
        p_flag = _make_and_save(
            tmp_path, monkeypatch,
            slug="flag-proj",
        )
        monkeypatch.chdir(repo)

        from apps.cli.commands.project import _cmd_project_current

        _cmd_project_current(project_flag="flag-proj", json_output=True)
        out = capsys.readouterr().out
        data = json.loads(out)
        assert data["project_id"] == str(p_flag.id)
        assert data["selection_source"] == "flag"

    def test_env_source_in_json(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        repo = tmp_path / "myrepo"
        _init_git(repo)
        p = _make_and_save(
            tmp_path, monkeypatch,
            slug="env-proj",
            canonical_repo_path=str(repo.resolve()),
        )
        monkeypatch.setenv("REMEDY_PROJECT", "env-proj")
        monkeypatch.chdir(repo)

        from apps.cli.commands.project import _cmd_project_current

        _cmd_project_current(json_output=True)
        out = capsys.readouterr().out
        data = json.loads(out)
        assert data["selection_source"] == "environment"

    def test_job_count_uses_job_ids_len(self, tmp_path, monkeypatch, capsys):
        """job_count must be len(project.job_ids), not count of loadable jobs."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        monkeypatch.delenv("REMEDY_PROJECT", raising=False)
        repo = tmp_path / "myrepo"
        _init_git(repo)
        _make_and_save(
            tmp_path, monkeypatch,
            slug="myrepo",
            canonical_repo_path=str(repo.resolve()),
            job_ids=["fake-job-1", "fake-job-2"],
        )
        monkeypatch.chdir(repo)

        from apps.cli.commands.project import _cmd_project_current

        _cmd_project_current(json_output=True)
        out = capsys.readouterr().out
        data = json.loads(out)
        assert data["job_count"] == 2


# ---------------------------------------------------------------------------
# _cmd_list_projects slug column
# ---------------------------------------------------------------------------


class TestListProjectsSlug:
    def test_slug_in_list_output(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        _make_and_save(tmp_path, monkeypatch, name="My App", slug="my-app")

        from apps.cli.commands.project import _cmd_list_projects

        _cmd_list_projects()
        out = capsys.readouterr().out
        assert "my-app" in out
        assert "My App" in out


# ---------------------------------------------------------------------------
# project attach — git validation, ownership, JSON output
# ---------------------------------------------------------------------------


class TestProjectAttachCommand:
    def test_attach_rejects_non_git(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        monkeypatch.delenv("REMEDY_PROJECT", raising=False)
        repo = tmp_path / "myrepo"
        _init_git(repo)
        _make_and_save(
            tmp_path, monkeypatch,
            slug="myrepo",
            canonical_repo_path=str(repo.resolve()),
        )
        monkeypatch.chdir(repo)
        not_git = tmp_path / "not-a-repo"
        not_git.mkdir()

        from apps.cli.commands.project import _cmd_project_attach_repo

        with pytest.raises(SystemExit) as exc:
            _cmd_project_attach_repo(str(not_git))
        assert exc.value.code == 2

    def test_attach_json_output(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        monkeypatch.delenv("REMEDY_PROJECT", raising=False)
        repo1 = tmp_path / "repo1"
        _init_git(repo1)
        p = _make_and_save(
            tmp_path, monkeypatch,
            slug="myproj",
            canonical_repo_path=str(repo1.resolve()),
            repo_paths=[str(repo1.resolve())],
        )
        monkeypatch.chdir(repo1)
        repo2 = tmp_path / "repo2"
        _init_git(repo2)

        from apps.cli.commands.project import _cmd_project_attach_repo

        _cmd_project_attach_repo(str(repo2))
        out = capsys.readouterr().out
        data = json.loads(out)
        assert data["project_id"] == str(p.id)
        assert data["changed"] is True
        assert data["new_repo"] == str(repo2.resolve())

    def test_attach_same_path_idempotent(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        monkeypatch.delenv("REMEDY_PROJECT", raising=False)
        repo = tmp_path / "myrepo"
        _init_git(repo)
        _make_and_save(
            tmp_path, monkeypatch,
            slug="myproj",
            canonical_repo_path=str(repo.resolve()),
            repo_paths=[str(repo.resolve())],
        )
        monkeypatch.chdir(repo)

        from apps.cli.commands.project import _cmd_project_attach_repo

        _cmd_project_attach_repo(str(repo))
        out = capsys.readouterr().out
        data = json.loads(out)
        assert data["changed"] is False

    def test_attach_with_project_flag(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        monkeypatch.delenv("REMEDY_PROJECT", raising=False)
        repo1 = tmp_path / "repo1"
        _init_git(repo1)
        repo2 = tmp_path / "repo2"
        _init_git(repo2)
        p = _make_and_save(
            tmp_path, monkeypatch,
            slug="target",
            canonical_repo_path=str(repo1.resolve()),
            repo_paths=[str(repo1.resolve())],
        )
        monkeypatch.chdir(tmp_path)

        from apps.cli.commands.project import _cmd_project_attach_repo

        _cmd_project_attach_repo(str(repo2), project_flag="target")
        out = capsys.readouterr().out
        data = json.loads(out)
        assert data["project_id"] == str(p.id)
        assert data["changed"] is True


# ---------------------------------------------------------------------------
# Workspace-key guard test — AST-based
# ---------------------------------------------------------------------------


_ALLOWED_FILES = {
    "packages/orchestration/worktrees.py",
    "packages/runtimes/dev_server.py",
}


class TestWorkspaceKeyGuard:
    """No production file outside the allowed set may import worktrees.project_id.

    Uses AST parsing to avoid false positives from string search.
    """

    def test_no_forbidden_imports(self):
        root = Path(__file__).resolve().parents[2]
        violations: list[str] = []

        for py in sorted(root.rglob("*.py")):
            rel = str(py.relative_to(root))
            if rel.startswith("tests/"):
                continue
            if rel.startswith("."):
                continue
            if rel in _ALLOWED_FILES:
                continue
            try:
                source = py.read_text()
            except OSError:
                continue
            try:
                tree = ast.parse(source, filename=rel)
            except SyntaxError:
                continue

            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    if node.module and "worktrees" in node.module:
                        for alias in node.names:
                            if alias.name == "project_id":
                                violations.append(
                                    f"{rel}:{node.lineno}: "
                                    f"imports project_id from {node.module}"
                                )
                if isinstance(node, ast.Attribute):
                    if (
                        node.attr == "project_id"
                        and isinstance(node.value, ast.Name)
                        and node.value.id == "worktrees"
                    ):
                        violations.append(
                            f"{rel}:{node.lineno}: "
                            f"uses worktrees.project_id"
                        )

        assert not violations, (
            "Forbidden worktrees.project_id usage outside allowed files:\n"
            + "\n".join(violations)
        )
