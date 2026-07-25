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


def _resolve_attr_chain(node: ast.expr) -> str | None:
    """Resolve an AST attribute chain to a dotted name string."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = _resolve_attr_chain(node.value)
        if parent is not None:
            return f"{parent}.{node.attr}"
    return None


def _find_worktree_project_id_violations(root: Path) -> list[str]:
    """Detect all forms of worktrees.project_id usage outside allowed files.

    Catches: from-import, aliased from-import, from-import of module itself,
    full module import, aliased full module import, and attribute access on
    any resolved alias including full dotted chains.
    """
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

        worktree_aliases: set[str] = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module:
                    for alias in node.names:
                        if "worktrees" in node.module and alias.name == "project_id":
                            violations.append(
                                f"{rel}:{node.lineno}: "
                                f"imports project_id from {node.module}"
                            )
                        if alias.name == "worktrees":
                            local = alias.asname or "worktrees"
                            worktree_aliases.add(local)

            if isinstance(node, ast.Import):
                for alias in node.names:
                    if "worktrees" in alias.name:
                        local = alias.asname or alias.name.split(".")[-1]
                        worktree_aliases.add(local)

            if isinstance(node, ast.Attribute) and node.attr == "project_id":
                chain = _resolve_attr_chain(node.value)
                if chain is not None:
                    parts = chain.split(".")
                    if parts[0] in worktree_aliases or "worktrees" in parts:
                        violations.append(
                            f"{rel}:{node.lineno}: "
                            f"uses {chain}.project_id"
                        )

    return violations


class TestWorkspaceKeyGuard:
    """No production file outside the allowed set may import worktrees.project_id.

    Uses AST parsing to detect direct imports, aliased imports, full module
    imports, and aliased full module imports.
    """

    def test_no_forbidden_imports(self):
        root = Path(__file__).resolve().parents[2]
        violations = _find_worktree_project_id_violations(root)
        assert not violations, (
            "Forbidden worktrees.project_id usage outside allowed files:\n"
            + "\n".join(violations)
        )

    def test_detects_aliased_module_import(self, tmp_path):
        """Synthetic test: aliased module import must be detected."""
        (tmp_path / "fake_module.py").write_text(
            "import packages.orchestration.worktrees as wt\n"
            "val = wt.project_id('/some/path')\n"
        )
        violations = _find_worktree_project_id_violations(tmp_path)
        assert any("wt.project_id" in v for v in violations)

    def test_allows_legitimate_files(self, tmp_path):
        """Synthetic test: allowed files are not flagged."""
        allowed = tmp_path / "packages" / "orchestration"
        allowed.mkdir(parents=True)
        (allowed / "worktrees.py").write_text(
            "def project_id(p): return 'x'\n"
        )
        violations = _find_worktree_project_id_violations(tmp_path)
        assert not violations

    def test_detects_from_import_worktrees_alias(self, tmp_path):
        """from packages.orchestration import worktrees as wt; wt.project_id(...)"""
        (tmp_path / "bad.py").write_text(
            "from packages.orchestration import worktrees as wt\n"
            "val = wt.project_id('/some/path')\n"
        )
        violations = _find_worktree_project_id_violations(tmp_path)
        assert any("wt.project_id" in v for v in violations)

    def test_detects_from_import_worktrees_no_alias(self, tmp_path):
        """from packages.orchestration import worktrees; worktrees.project_id(...)"""
        (tmp_path / "bad.py").write_text(
            "from packages.orchestration import worktrees\n"
            "val = worktrees.project_id('/some/path')\n"
        )
        violations = _find_worktree_project_id_violations(tmp_path)
        assert any("worktrees.project_id" in v for v in violations)

    def test_detects_full_dotted_chain(self, tmp_path):
        """import packages.orchestration.worktrees; packages.orchestration.worktrees.project_id(...)"""
        (tmp_path / "bad.py").write_text(
            "import packages.orchestration.worktrees\n"
            "val = packages.orchestration.worktrees.project_id('/some/path')\n"
        )
        violations = _find_worktree_project_id_violations(tmp_path)
        assert any("packages.orchestration.worktrees.project_id" in v for v in violations)

    def test_no_false_positive_unrelated_attr(self, tmp_path):
        """project_id on unrelated module must not trigger."""
        (tmp_path / "ok.py").write_text(
            "import some_other_module\n"
            "val = some_other_module.project_id('x')\n"
        )
        violations = _find_worktree_project_id_violations(tmp_path)
        assert not violations
