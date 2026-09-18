"""Tests for `remedy study run` (F266 T001 CLI wiring).

The load-bearing properties:
1. The command calls run_study with study_call_fn() as the default call_fn
2. It writes memory cards to the project store (action_class=write_metadata)
3. It respects --path, --project, and --json flags
4. It is registered in the catalog with user_facing=False
5. It is discoverable via the command registry
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from apps.cli.command_catalog import get_command, get_commands_for_group
from apps.cli.commands import collect_all_handlers


def _build_fixture_repo(tmp_path: Path) -> Path:
    """Build a minimal fixture repository with recognizable structure."""
    repo = tmp_path / "fixture_repo"
    repo.mkdir()

    # Create a basic structure that study._walk_repo will scan
    (repo / "README.md").write_text("# Test Repo\n")
    (repo / "pyproject.toml").write_text("[project]\nname = 'test'\n")
    (repo / ".gitignore").write_text("*.pyc\n")

    tests_dir = repo / "tests"
    tests_dir.mkdir()
    (tests_dir / "test_example.py").write_text("def test_pass(): pass\n")

    src_dir = repo / "src"
    src_dir.mkdir()
    (src_dir / "module.py").write_text("# module\n")

    return repo


def _setup_data_root(tmp_path: Path, monkeypatch) -> Path:
    """Set up a data root in a temporary directory."""
    data_root = tmp_path / "data"
    data_root.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_root))
    return data_root


def _setup_project(data_root: Path, monkeypatch) -> str:
    """Set up a registered project and return its ID."""
    from packages.orchestration.project_registry import RemyProject, save_project

    project = RemyProject(name="Study Test Project", slug="study-test")
    save_project(project)
    monkeypatch.setenv("REMEDY_PROJECT", "study-test")
    return str(project.id)


class TestStudyRunWritesCards:
    """The command writes memory cards to the project store."""

    def test_study_run_writes_cards_for_a_fixture_repo(self, tmp_path, monkeypatch, capsys):
        """Test that study run writes exactly 4 memory cards."""
        repo = _build_fixture_repo(tmp_path)
        data_root = _setup_data_root(tmp_path, monkeypatch)
        _setup_project(data_root, monkeypatch)

        from apps.cli.commands.study_cmd import _cmd_study_run

        # Run the command with JSON output to capture structured result
        _cmd_study_run(str(repo), project=str(repo), json_output=True)
        captured = capsys.readouterr()
        out = captured.out
        err = captured.err

        result = json.loads(out)
        assert result["cards_written"] == ["study:structure", "study:core_modules", "study:conventions", "study:entry_points"]
        assert result["partial"] is False
        # Verify the warning fired when no registered project found
        assert "No registered project found" in err
        # Verify stdout is still valid JSON despite warning on stderr
        assert json.loads(out) is not None

    def test_study_run_defaults_path_to_cwd(self, tmp_path, monkeypatch, capsys):
        """Test that study run with path=None studies the current directory."""
        repo = _build_fixture_repo(tmp_path)
        data_root = _setup_data_root(tmp_path, monkeypatch)
        _setup_project(data_root, monkeypatch)

        from apps.cli.commands.study_cmd import _cmd_study_run

        # Change to the fixture repo directory and call with path=None
        old_cwd = os.getcwd()
        try:
            os.chdir(str(repo))
            _cmd_study_run(None, project=str(repo), json_output=True)
        finally:
            os.chdir(old_cwd)

        out = capsys.readouterr().out
        result = json.loads(out)
        assert result["cards_written"]  # Should have written cards
        assert len(result["cards_written"]) == 4

    def test_study_run_resolves_same_project_as_teacher_ask_via_registered_project(self, tmp_path, monkeypatch, capsys):
        """Test that study run resolves the same project as teacher ask when registered."""
        from apps.cli.commands.study_cmd import _cmd_study_run
        from packages.orchestration.project_scope import resolve_scope

        repo = _build_fixture_repo(tmp_path)
        data_root = _setup_data_root(tmp_path, monkeypatch)
        project_id = _setup_project(data_root, monkeypatch)

        # Change to the fixture repo directory to enable project auto-detection
        old_cwd = os.getcwd()
        try:
            os.chdir(str(repo))
            # Call study run with project=None to test auto-detection
            _cmd_study_run(None, project=None, json_output=True)
        finally:
            os.chdir(old_cwd)

        # Extract the project_id from the JSON output
        captured = capsys.readouterr()
        result = json.loads(captured.out)
        study_project_id = result["project_id"]

        # Resolve scope the same way teacher ask does
        scope = resolve_scope(project_flag=None, all_projects=False, cwd=str(repo))
        teacher_project_id = scope.project_id

        # Both commands should resolve to the same project id
        assert study_project_id == teacher_project_id
        assert study_project_id == project_id

    def test_study_run_warns_and_falls_back_when_no_project_registered(self, tmp_path, monkeypatch, capsys):
        """Test that study run warns and falls back to path when no project registered."""
        from apps.cli.commands.study_cmd import _cmd_study_run

        repo = _build_fixture_repo(tmp_path)
        data_root = _setup_data_root(tmp_path, monkeypatch)
        # Do NOT call _setup_project, so no project is registered

        # Run the command with JSON output
        _cmd_study_run(str(repo), project=None, json_output=True)
        captured = capsys.readouterr()
        out = captured.out
        err = captured.err

        # Verify the warning is printed
        assert "No registered project found" in err

        # Verify stdout is still valid JSON
        result = json.loads(out)

        # Verify the project_id falls back to the absolute path
        assert result["project_id"] == os.path.abspath(str(repo))


class TestStudyCommandCatalogRegistration:
    """The study.run command is registered in the catalog correctly."""

    def test_study_command_registered_in_catalog(self):
        """Test that study.run entry exists in the catalog."""
        entry = get_command("study.run")
        assert entry.group_id == "study"
        assert entry.action_class == "write_metadata"
        assert entry.supports_json is True

    def test_study_command_in_study_group(self):
        """Test that study.run appears in the study group."""
        commands = get_commands_for_group("study")
        command_ids = [cmd.command_id for cmd in commands]
        assert "study.run" in command_ids

    def test_study_group_not_in_visible_group_order(self):
        """Test that study group is not in the default help order (DECISION F266 D3)."""
        from apps.cli.command_catalog import GROUPS, VISIBLE_GROUP_ORDER

        assert "study" not in VISIBLE_GROUP_ORDER
        assert GROUPS["study"].user_facing is False

    def test_study_group_not_hidden(self):
        """Test that study group is hidden=False but user_facing=False (advanced/internal tier)."""
        from apps.cli.command_catalog import GROUPS

        assert GROUPS["study"].hidden is False
        assert GROUPS["study"].user_facing is False


class TestStudyCommandReachability:
    """Tests that prove study.run is truly reachable through the CLI dispatch."""

    def test_study_run_in_collect_all_handlers(self):
        """Test that study.run is a key in collect_all_handlers() result (R-0959)."""
        handlers = collect_all_handlers()
        assert "study.run" in handlers
        assert callable(handlers["study.run"])

    def test_study_run_dispatch_e2e(self, tmp_path, monkeypatch):
        """Test that study run is callable through the real CLI dispatch (R-0959)."""
        # Build a fixture repo
        repo = tmp_path / "fixture_repo"
        repo.mkdir()
        (repo / "README.md").write_text("# Test Repo\n")
        (repo / "pyproject.toml").write_text("[project]\nname = 'test'\n")

        # Set up data root and isolate it
        data_root = tmp_path / "data"
        data_root.mkdir()
        monkeypatch.setenv("REMEDY_DATA_DIR", str(data_root))

        # Invoke study run through the real grouped CLI dispatch as a subprocess
        # Use --path option syntax (not positional argument)
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "apps.cli.grouped",
                "study",
                "run",
                "--path",
                str(repo),
                "--json",
            ],
            capture_output=True,
            text=True,
            timeout=90,
        )

        # The command must exit 0
        assert result.returncode == 0, f"study run failed: {result.stderr}"
        # The output must be valid JSON
        output = json.loads(result.stdout)
        # The output must contain expected keys
        assert "cards_written" in output
        assert "project_id" in output
