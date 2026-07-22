"""Tests for F146 CLI — project current, project attach, workspace-key guard."""

from __future__ import annotations

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
# _cmd_project_current
# ---------------------------------------------------------------------------


class TestProjectCurrentCommand:
    def test_shows_slug_and_id(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
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

    def test_json_output(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
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

        _cmd_project_current(json_output=True)
        out = capsys.readouterr().out
        data = json.loads(out)
        assert data["slug"] == "myrepo"
        assert data["id"] == str(p.id)

    def test_exit_3_when_unresolved(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        repo = tmp_path / "unknown"
        _init_git(repo)
        monkeypatch.chdir(repo)

        from apps.cli.commands.project import _cmd_project_current

        with pytest.raises(SystemExit) as exc:
            _cmd_project_current()
        assert exc.value.code == 3


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
# Workspace-key guard test
# ---------------------------------------------------------------------------


_ALLOWED_FILES = {
    "packages/orchestration/worktrees.py",
    "packages/runtimes/dev_server.py",
}


class TestWorkspaceKeyGuard:
    """No production file outside the allowed set may import worktrees.project_id."""

    def test_no_forbidden_imports(self):
        from pathlib import Path

        root = Path(__file__).resolve().parents[2]
        forbidden_patterns = [
            "from packages.orchestration.worktrees import project_id",
            "from packages.orchestration.worktrees import (\n"
            "    project_id",
            "worktrees.project_id(",
        ]

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
                text = py.read_text()
            except OSError:
                continue
            for pattern in forbidden_patterns:
                if pattern in text:
                    violations.append(f"{rel}: {pattern!r}")

        assert not violations, (
            "Forbidden worktrees.project_id usage outside allowed files:\n"
            + "\n".join(violations)
        )
