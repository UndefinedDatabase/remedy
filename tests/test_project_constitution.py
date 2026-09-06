"""
Tests for packages/orchestration/project_constitution.py and the
`remedy constitution` CLI command.

Coverage:
  - no repo (None)
  - stale/nonexistent repo path
  - empty repo directory
  - pyproject.toml with pytest → test_commands
  - pyproject.toml with ruff, mypy, black → lint_commands
  - pyproject.toml with build-system → build_commands
  - package.json scripts → test/build/lint commands
  - Makefile target detection (test/lint/build)
  - justfile target detection
  - pytest.ini / tox.ini → test_commands
  - AGENTS.md / CLAUDE.md / README.md / CONTRIBUTING.md convention extraction
  - SECURITY.md → approval hint
  - .github/workflows/ discovery
  - docs/ and other doc dirs detected
  - risky/protected paths detected
  - path boundary check (no escape via symlink/relative path)
  - secret files never read (.env, .key)
  - no command execution
  - no raw long file content in output
  - deduplication of commands
  - render_constitution covers all sections
  - CLI: prints constitution for valid job
  - CLI: invalid job ID exits 1
  - CLI: unknown job ID exits 1
  - CLI: no repo prints warning and exits 0
  - CLI: attached repo with pyproject shows pytest
  - CLI: run log event has counts only, no raw content
  - Cockpit: shows constitution source count in Important artifacts
  - Cockpit: no noisy attention item when constitution absent
  - Trust Report: shows constitution source count in Section 6
  - Trust Report: no attached repo shows appropriate line
"""

from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4

import pytest

from packages.core.models import Job, RunState
from packages.orchestration.cockpit import summarize_cockpit
from packages.orchestration.project_constitution import (
    ProjectConstitution,
    _is_safe_path,
    _safe_read,
    load_project_constitution,
    render_constitution,
)
from packages.orchestration.storage import save_job
from packages.orchestration.trust_report import summarize_trust_report

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_job(**kwargs) -> Job:
    defaults: dict = {"name": "Test constitution job", "state": RunState.PENDING}
    defaults.update(kwargs)
    return Job(**defaults)


def _write(tmp_path: Path, name: str, content: str) -> Path:
    p = tmp_path / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# No repo / missing repo
# ---------------------------------------------------------------------------


class TestNoRepo:
    def test_none_returns_warning(self):
        c = load_project_constitution(None)
        assert c.warnings
        assert any("no attached repo" in w for w in c.warnings)

    def test_none_has_empty_sources(self):
        c = load_project_constitution(None)
        assert c.source_files == []

    def test_nonexistent_path_returns_warning(self, tmp_path):
        c = load_project_constitution(tmp_path / "does_not_exist")
        assert c.warnings
        assert c.source_files == []

    def test_file_not_dir_returns_warning(self, tmp_path):
        f = tmp_path / "notadir.txt"
        f.write_text("hi")
        c = load_project_constitution(f)
        assert c.warnings

    def test_empty_repo_returns_no_sources(self, tmp_path):
        c = load_project_constitution(tmp_path)
        assert c.source_files == []
        assert c.warnings == []


# ---------------------------------------------------------------------------
# pyproject.toml extraction
# ---------------------------------------------------------------------------


class TestPyprojectExtraction:
    def test_pytest_in_tool_section(self, tmp_path):
        _write(tmp_path, "pyproject.toml", "[tool.pytest.ini_options]\n")
        c = load_project_constitution(tmp_path)
        assert "pytest" in c.test_commands

    def test_pytest_minimal_mention(self, tmp_path):
        _write(tmp_path, "pyproject.toml", "[build-system]\nrequires=[\"setuptools\"]\n\n[tool.pytest]\n")
        c = load_project_constitution(tmp_path)
        assert "pytest" in c.test_commands

    def test_ruff_detected(self, tmp_path):
        _write(tmp_path, "pyproject.toml", "[tool.ruff]\nline-length = 88\n")
        c = load_project_constitution(tmp_path)
        assert any("ruff" in cmd for cmd in c.lint_commands)

    def test_mypy_detected(self, tmp_path):
        _write(tmp_path, "pyproject.toml", "[tool.mypy]\nstrict = true\n")
        c = load_project_constitution(tmp_path)
        assert any("mypy" in cmd for cmd in c.lint_commands)

    def test_black_detected(self, tmp_path):
        _write(tmp_path, "pyproject.toml", "[tool.black]\nline-length = 88\n")
        c = load_project_constitution(tmp_path)
        assert any("black" in cmd for cmd in c.lint_commands)

    def test_build_system_detected(self, tmp_path):
        _write(tmp_path, "pyproject.toml",
               "[build-system]\nrequires=[\"setuptools\"]\nbuild-backend=\"setuptools.build_meta\"\n")
        c = load_project_constitution(tmp_path)
        assert c.build_commands

    def test_hatch_build(self, tmp_path):
        _write(tmp_path, "pyproject.toml",
               "[build-system]\nrequires=[\"hatchling\"]\nbuild-backend=\"hatchling.build\"\n")
        c = load_project_constitution(tmp_path)
        assert any("hatch" in cmd for cmd in c.build_commands)

    def test_pyproject_in_source_files(self, tmp_path):
        _write(tmp_path, "pyproject.toml", "[tool.pytest]\n")
        c = load_project_constitution(tmp_path)
        assert "pyproject.toml" in c.source_files

    def test_commands_deduplicated(self, tmp_path):
        # Both pytest and [tool.pytest] would add pytest
        _write(tmp_path, "pyproject.toml",
               "[tool.pytest.ini_options]\n\n[tool.pytest]\n")
        c = load_project_constitution(tmp_path)
        assert c.test_commands.count("pytest") == 1


# ---------------------------------------------------------------------------
# package.json extraction
# ---------------------------------------------------------------------------


class TestPackageJsonExtraction:
    def test_npm_test_detected(self, tmp_path):
        data = {"scripts": {"test": "jest"}}
        _write(tmp_path, "package.json", json.dumps(data))
        c = load_project_constitution(tmp_path)
        assert any("npm test" in cmd or "jest" in cmd for cmd in c.test_commands)

    def test_npm_build_detected(self, tmp_path):
        data = {"scripts": {"build": "tsc"}}
        _write(tmp_path, "package.json", json.dumps(data))
        c = load_project_constitution(tmp_path)
        assert any("build" in cmd for cmd in c.build_commands)

    def test_npm_lint_detected(self, tmp_path):
        data = {"scripts": {"lint": "eslint ."}}
        _write(tmp_path, "package.json", json.dumps(data))
        c = load_project_constitution(tmp_path)
        assert any("lint" in cmd for cmd in c.lint_commands)

    def test_malformed_package_json_no_crash(self, tmp_path):
        _write(tmp_path, "package.json", "NOT_JSON{{{")
        c = load_project_constitution(tmp_path)  # must not raise
        assert isinstance(c, ProjectConstitution)

    def test_package_json_in_source_files(self, tmp_path):
        _write(tmp_path, "package.json", json.dumps({"scripts": {"test": "jest"}}))
        c = load_project_constitution(tmp_path)
        assert "package.json" in c.source_files


# ---------------------------------------------------------------------------
# Makefile / justfile extraction
# ---------------------------------------------------------------------------


class TestMakefileExtraction:
    def test_make_test_detected(self, tmp_path):
        _write(tmp_path, "Makefile", "test:\n\tpytest\n")
        c = load_project_constitution(tmp_path)
        assert any("make test" in cmd for cmd in c.test_commands)

    def test_make_lint_detected(self, tmp_path):
        _write(tmp_path, "Makefile", "lint:\n\truff check .\n")
        c = load_project_constitution(tmp_path)
        assert any("make lint" in cmd for cmd in c.lint_commands)

    def test_make_build_detected(self, tmp_path):
        _write(tmp_path, "Makefile", "build:\n\tpython -m build\n")
        c = load_project_constitution(tmp_path)
        assert any("make build" in cmd for cmd in c.build_commands)

    def test_makefile_in_source_files(self, tmp_path):
        _write(tmp_path, "Makefile", "test:\n\tpytest\n")
        c = load_project_constitution(tmp_path)
        assert "Makefile" in c.source_files

    def test_justfile_test_detected(self, tmp_path):
        _write(tmp_path, "justfile", "test:\n    pytest\n")
        c = load_project_constitution(tmp_path)
        assert any("just test" in cmd for cmd in c.test_commands)


# ---------------------------------------------------------------------------
# pytest.ini / tox.ini
# ---------------------------------------------------------------------------


class TestConfigFiles:
    def test_pytest_ini_adds_test_command(self, tmp_path):
        _write(tmp_path, "pytest.ini", "[pytest]\ntestpaths = tests\n")
        c = load_project_constitution(tmp_path)
        assert "pytest" in c.test_commands

    def test_tox_ini_adds_test_command(self, tmp_path):
        _write(tmp_path, "tox.ini", "[tox]\nenvlist = py311\n")
        c = load_project_constitution(tmp_path)
        assert "pytest" in c.test_commands


# ---------------------------------------------------------------------------
# Text file convention extraction
# ---------------------------------------------------------------------------


class TestTextFileExtraction:
    def test_agents_md_in_source_files(self, tmp_path):
        _write(tmp_path, "AGENTS.md", "# Rules\nAlways run tests before merging.\n")
        c = load_project_constitution(tmp_path)
        assert "AGENTS.md" in c.source_files

    def test_claude_md_in_source_files(self, tmp_path):
        _write(tmp_path, "CLAUDE.md", "# Instructions\nNever commit secrets.\n")
        c = load_project_constitution(tmp_path)
        assert "CLAUDE.md" in c.source_files

    def test_convention_extracted_from_agents(self, tmp_path):
        _write(tmp_path, "AGENTS.md", "Always run tests before merging.\n")
        c = load_project_constitution(tmp_path)
        assert any("AGENTS.md" in conv for conv in c.repo_conventions)

    def test_do_not_extracted_as_convention(self, tmp_path):
        _write(tmp_path, "CLAUDE.md", "Do not modify pyproject.toml directly.\n")
        c = load_project_constitution(tmp_path)
        assert c.repo_conventions or c.forbidden_commands  # either bucket is fine

    def test_approval_hint_extracted(self, tmp_path):
        _write(tmp_path, "CONTRIBUTING.md", "All PRs require approval from a reviewer.\n")
        c = load_project_constitution(tmp_path)
        assert c.approval_rules

    def test_security_md_yields_approval_hint(self, tmp_path):
        _write(tmp_path, "SECURITY.md", "Report vulnerabilities to security@example.com\n")
        c = load_project_constitution(tmp_path)
        assert any("SECURITY" in r or "security" in r.lower() for r in c.approval_rules)

    def test_readme_in_source_files(self, tmp_path):
        _write(tmp_path, "README.md", "# My Project\nRun tests with pytest.\n")
        c = load_project_constitution(tmp_path)
        assert "README.md" in c.source_files


# ---------------------------------------------------------------------------
# Known path detection
# ---------------------------------------------------------------------------


class TestKnownPaths:
    def test_docs_dir_detected(self, tmp_path):
        (tmp_path / "docs").mkdir()
        c = load_project_constitution(tmp_path)
        assert any("docs" in p for p in c.doc_paths)

    def test_pyproject_in_protected(self, tmp_path):
        _write(tmp_path, "pyproject.toml", "[build-system]\n")
        c = load_project_constitution(tmp_path)
        assert "pyproject.toml" in c.protected_paths

    def test_env_file_in_risky(self, tmp_path):
        (tmp_path / ".env").write_text("SECRET=abc")
        c = load_project_constitution(tmp_path)
        assert any(".env" in p for p in c.risky_paths)

    def test_migrations_in_risky(self, tmp_path):
        (tmp_path / "migrations").mkdir()
        c = load_project_constitution(tmp_path)
        assert any("migrations" in p for p in c.risky_paths)

    def test_tests_dir_adds_definition_of_done(self, tmp_path):
        (tmp_path / "tests").mkdir()
        c = load_project_constitution(tmp_path)
        assert any("tests" in d or "test" in d for d in c.definition_of_done)


# ---------------------------------------------------------------------------
# GitHub workflows
# ---------------------------------------------------------------------------


class TestWorkflows:
    def test_workflow_files_in_source_files(self, tmp_path):
        wf_dir = tmp_path / ".github" / "workflows"
        wf_dir.mkdir(parents=True)
        (wf_dir / "ci.yml").write_text("steps:\n  - run: pytest\n")
        c = load_project_constitution(tmp_path)
        assert any("ci.yml" in s for s in c.source_files)

    def test_pytest_in_workflow_adds_test_command(self, tmp_path):
        wf_dir = tmp_path / ".github" / "workflows"
        wf_dir.mkdir(parents=True)
        (wf_dir / "ci.yml").write_text("steps:\n  - run: pytest\n")
        c = load_project_constitution(tmp_path)
        assert "pytest" in c.test_commands


# ---------------------------------------------------------------------------
# Safety: path boundary and secret files
# ---------------------------------------------------------------------------


class TestSafety:
    def test_safe_path_within_repo(self, tmp_path):
        f = tmp_path / "README.md"
        f.write_text("hi")
        assert _is_safe_path(f, tmp_path) is True

    def test_safe_path_outside_repo(self, tmp_path):
        outside = tmp_path.parent / "outside.txt"
        assert _is_safe_path(outside, tmp_path) is False

    def test_env_file_not_read(self, tmp_path):
        env_file = tmp_path / ".env"
        env_file.write_text("SECRET=hunter2")
        result = _safe_read(env_file, tmp_path)
        assert result is None

    def test_key_file_not_read(self, tmp_path):
        key_file = tmp_path / "id_rsa.key"
        key_file.write_text("PRIVATE KEY")
        result = _safe_read(key_file, tmp_path)
        assert result is None

    def test_secret_prefixed_file_not_read(self, tmp_path):
        sec_file = tmp_path / "secrets.yml"
        sec_file.write_text("password: abc")
        result = _safe_read(sec_file, tmp_path)
        assert result is None

    def test_constitution_never_executes_commands(self, tmp_path):
        """load_project_constitution must not start any subprocess."""
        import subprocess
        original_run = subprocess.run
        called = []

        def fake_run(*args, **kwargs):
            called.append(args)
            return original_run(*args, **kwargs)

        _write(tmp_path, "Makefile", "test:\n\tpytest\n")
        # Patch subprocess.run for duration of call
        import unittest.mock as mock
        with mock.patch("subprocess.run", side_effect=fake_run):
            load_project_constitution(tmp_path)
        assert called == [], "subprocess.run must not be called"

    def test_no_raw_content_in_constitution_fields(self, tmp_path):
        """Extraction must not store full file content verbatim in constitution fields."""
        long_content = "# README\n" + ("This is a very long line. " * 50 + "\n") * 20
        _write(tmp_path, "README.md", long_content)
        c = load_project_constitution(tmp_path)
        # No field should contain a 500+ char string (which would be raw file content)
        for field_val in [
            c.repo_conventions, c.approval_rules, c.definition_of_done,
            c.forbidden_commands,
        ]:
            for item in field_val:
                assert len(item) < 500, f"field item too long (raw content?): {item[:100]}"

    def test_symlink_escape_blocked(self, tmp_path):
        """_is_safe_path must return False for a symlink that points outside repo_root."""
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        outside_file = tmp_path / "secret.txt"
        outside_file.write_text("top secret")
        link = repo_root / "escape_link"
        try:
            link.symlink_to(outside_file)
        except (OSError, NotImplementedError):
            pytest.skip("symlink creation not available on this platform")
        assert _is_safe_path(link, repo_root) is False


# ---------------------------------------------------------------------------
# render_constitution
# ---------------------------------------------------------------------------


class TestRenderConstitution:
    def test_header_present(self, tmp_path):
        c = load_project_constitution(tmp_path)
        out = render_constitution(c, tmp_path)
        assert "Remedy Project Constitution" in out

    def test_all_sections_present(self, tmp_path):
        c = load_project_constitution(tmp_path)
        out = render_constitution(c, tmp_path)
        for section in ["Source files", "Test commands", "Build commands",
                         "Lint", "Risky", "Approval hints", "Definition of done"]:
            assert section in out, f"Missing section: {section}"

    def test_no_repo_renders_warning(self):
        c = load_project_constitution(None)
        out = render_constitution(c, None)
        assert "no attached repo" in out or "unavailable" in out

    def test_pytest_in_test_section(self, tmp_path):
        _write(tmp_path, "pyproject.toml", "[tool.pytest]\n")
        c = load_project_constitution(tmp_path)
        out = render_constitution(c, tmp_path)
        assert "pytest" in out

    def test_source_count_in_header(self, tmp_path):
        _write(tmp_path, "pyproject.toml", "[tool.pytest]\n")
        c = load_project_constitution(tmp_path)
        out = render_constitution(c, tmp_path)
        assert "1 file(s)" in out or "Sources: 1" in out


# ---------------------------------------------------------------------------
# CLI: remedy constitution
# ---------------------------------------------------------------------------


class TestCmdConstitution:
    def _save(self, tmp_path, monkeypatch, **kwargs) -> Job:
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job(**kwargs)
        save_job(job)
        return job

    def test_prints_constitution_for_valid_job(self, tmp_path, monkeypatch, capsys):
        job = self._save(tmp_path, monkeypatch)
        from apps.cli.commands.brain import _cmd_constitution
        _cmd_constitution(str(job.id))
        out = capsys.readouterr().out
        assert "Remedy Project Constitution" in out

    def test_no_repo_attached_exits_0(self, tmp_path, monkeypatch, capsys):
        job = self._save(tmp_path, monkeypatch)
        from apps.cli.commands.brain import _cmd_constitution
        _cmd_constitution(str(job.id))  # must not raise
        out = capsys.readouterr().out
        assert "no attached repo" in out.lower() or "unavailable" in out.lower()

    def test_attached_repo_with_pyproject_shows_pytest(
        self, tmp_path, monkeypatch, capsys
    ):
        repo_dir = tmp_path / "repo"
        repo_dir.mkdir()
        (repo_dir / "pyproject.toml").write_text("[tool.pytest]\n")
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        job.metadata["target_repo"] = str(repo_dir)
        save_job(job)
        from apps.cli.commands.brain import _cmd_constitution
        _cmd_constitution(str(job.id))
        out = capsys.readouterr().out
        assert "pytest" in out

    def test_invalid_job_id_exits_1(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from apps.cli.commands.brain import _cmd_constitution
        with pytest.raises(SystemExit) as exc_info:
            _cmd_constitution("not-a-uuid")
        assert exc_info.value.code == 1

    def test_unknown_job_id_exits_1(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from apps.cli.commands.brain import _cmd_constitution
        with pytest.raises(SystemExit) as exc_info:
            _cmd_constitution(str(uuid4()))
        assert exc_info.value.code == 1

    def test_run_log_event_has_counts_only(self, tmp_path, monkeypatch, capsys):
        """Run log event must contain counts/booleans, not raw file content."""
        repo_dir = tmp_path / "repo"
        repo_dir.mkdir()
        (repo_dir / "pyproject.toml").write_text("[tool.pytest]\n")
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        job.metadata["target_repo"] = str(repo_dir)
        save_job(job)
        from apps.cli.commands.brain import _cmd_constitution
        _cmd_constitution(str(job.id))
        capsys.readouterr()
        # Check run log
        runs_dir = tmp_path / "job_logs" / str(job.id)
        events = []
        for f in runs_dir.glob("*.jsonl"):
            for line in f.read_text().splitlines():
                if line.strip():
                    events.append(json.loads(line))
        ev = next((e for e in events if e.get("event") == "project_constitution_loaded"), None)
        assert ev is not None
        meta = ev.get("metadata", {})
        assert "source_count" in meta
        assert "warning_count" in meta
        assert "has_test_commands" in meta
        # No raw text in any run log file
        combined_raw_content = "".join(f.read_text() for f in runs_dir.glob("*.jsonl"))
        assert "[tool.pytest]" not in combined_raw_content


# ---------------------------------------------------------------------------
# Cockpit integration
# ---------------------------------------------------------------------------


class TestCockpitConstitutionIntegration:
    def test_constitution_line_shown_in_artifacts(self, tmp_path):
        job = _make_job()
        constitution = ProjectConstitution(source_files=["pyproject.toml", "Makefile"])
        out = summarize_cockpit(job, [], constitution=constitution)
        assert "constitution:" in out
        assert "2" in out

    def test_no_constitution_no_artifact_line(self):
        job = _make_job()
        out = summarize_cockpit(job, [], constitution=None)
        assert "constitution:" not in out

    def test_zero_sources_still_shows_line(self, tmp_path):
        job = _make_job()
        constitution = ProjectConstitution(source_files=[])
        out = summarize_cockpit(job, [], constitution=constitution)
        assert "constitution:" in out
        assert "0" in out

    def test_no_noisy_attention_item_when_absent(self):
        """Absent constitution must not add a 'constitution:' artifact line."""
        job = Job(name="Unnamed job", state=RunState.PENDING)  # avoid 'constitution' in name
        out = summarize_cockpit(job, [], constitution=None)
        assert "constitution:" not in out


# ---------------------------------------------------------------------------
# Trust Report integration
# ---------------------------------------------------------------------------


class TestTrustReportConstitutionIntegration:
    def test_constitution_source_count_shown(self):
        job = _make_job()
        constitution = ProjectConstitution(source_files=["pyproject.toml", "AGENTS.md"])
        out = summarize_trust_report(job, [], constitution=constitution)
        assert "Project Constitution" in out
        assert "2 source file(s)" in out

    def test_no_repo_shows_appropriate_line(self):
        job = _make_job()
        out = summarize_trust_report(job, [], constitution=None)
        assert "Project Constitution" in out
        assert "no attached repo" in out

    def test_no_sources_found_message(self):
        """Empty repo (no known files found, no warnings) → 'no sources found'."""
        job = _make_job()
        constitution = ProjectConstitution(source_files=[])  # no warnings = clean empty repo
        out = summarize_trust_report(job, [], constitution=constitution)
        assert "Project Constitution" in out
        assert "no sources found" in out

    def test_stale_repo_shows_unavailable(self):
        """Constitution with warnings but no sources → stale/non-dir repo message."""
        job = _make_job()
        constitution = ProjectConstitution(
            source_files=[],
            warnings=["attached repo does not exist: /gone"],
        )
        out = summarize_trust_report(job, [], constitution=constitution)
        assert "Project Constitution" in out
        assert "unavailable" in out or "missing" in out

    def test_attached_repo_not_loaded_shows_command_hint(self):
        """When repo is attached but constitution not loaded, hint shown."""
        job = _make_job()
        job.metadata["target_repo"] = "/some/repo"
        out = summarize_trust_report(job, [], constitution=None)
        assert "constitution" in out.lower()


# ---------------------------------------------------------------------------
# Trust Report CLI integration (Step 21.1 — constitution loaded at render time)
# ---------------------------------------------------------------------------


class TestTrustReportCLIConstitution:
    def _setup_repo(self, tmp_path, monkeypatch) -> tuple[Job, Path]:
        """Create a job with an attached repo containing pyproject.toml."""
        repo_dir = tmp_path / "repo"
        repo_dir.mkdir()
        (repo_dir / "pyproject.toml").write_text("[tool.pytest]\n")
        (repo_dir / "AGENTS.md").write_text(
            "Always run tests before merging.\n"
            "Never commit to main directly.\n"
        )
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        job.metadata["target_repo"] = str(repo_dir)
        save_job(job)
        return job, repo_dir

    def test_attached_repo_shows_available_from_n_sources(
        self, tmp_path, monkeypatch, capsys
    ):
        job, _ = self._setup_repo(tmp_path, monkeypatch)
        from apps.cli.commands.brain import _cmd_trust_report
        _cmd_trust_report(str(job.id))
        out = capsys.readouterr().out
        assert "Project Constitution" in out
        assert "available from" in out
        assert "source file(s)" in out

    def test_attached_repo_does_not_say_not_loaded(self, tmp_path, monkeypatch, capsys):
        """The old 'not loaded' hint must not appear when repo is attached."""
        job, _ = self._setup_repo(tmp_path, monkeypatch)
        from apps.cli.commands.brain import _cmd_trust_report
        _cmd_trust_report(str(job.id))
        out = capsys.readouterr().out
        assert "not loaded" not in out

    def test_no_repo_shows_no_attached_repo(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        from apps.cli.commands.brain import _cmd_trust_report
        _cmd_trust_report(str(job.id))
        out = capsys.readouterr().out
        assert "no attached repo" in out.lower()

    def test_empty_repo_shows_no_sources_found(self, tmp_path, monkeypatch, capsys):
        repo_dir = tmp_path / "repo"
        repo_dir.mkdir()
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        job.metadata["target_repo"] = str(repo_dir)
        save_job(job)
        from apps.cli.commands.brain import _cmd_trust_report
        _cmd_trust_report(str(job.id))
        out = capsys.readouterr().out
        assert "Project Constitution" in out
        assert "no sources found" in out

    def test_stale_repo_shows_unavailable(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        job.metadata["target_repo"] = str(tmp_path / "does_not_exist")
        save_job(job)
        from apps.cli.commands.brain import _cmd_trust_report
        _cmd_trust_report(str(job.id))
        out = capsys.readouterr().out
        assert "Project Constitution" in out
        assert "unavailable" in out or "missing" in out

    def test_no_raw_conventions_in_trust_report_output(self, tmp_path, monkeypatch, capsys):
        """Trust report must not dump raw AGENTS.md lines from the constitution."""
        job, _ = self._setup_repo(tmp_path, monkeypatch)
        from apps.cli.commands.brain import _cmd_trust_report
        _cmd_trust_report(str(job.id))
        out = capsys.readouterr().out
        # The trust report shows constitution summary only, not full convention list
        assert "Never commit to main directly" not in out
        assert "Always run tests before merging" not in out


# ---------------------------------------------------------------------------
# Timeline rendering (Step 21.1)
# ---------------------------------------------------------------------------


class TestTimelineConstitutionEvent:
    def test_constitution_event_renders_as_loaded(self):
        from packages.orchestration.timeline import summarize_timeline

        job = _make_job(state=RunState.PENDING)
        events = [
            {
                "event": "project_constitution_loaded",
                "job_id": str(job.id),
                "run_id": "r",
                "timestamp": "2026-05-05T10:00:00+00:00",
                "outcome": "loaded",
                "metadata": {
                    "source_count": 4,
                    "warning_count": 0,
                    "has_test_commands": True,
                },
            }
        ]
        out = summarize_timeline(job, events)
        assert "Project Constitution loaded" in out

    def test_constitution_event_shows_source_count(self):
        from packages.orchestration.timeline import summarize_timeline

        job = _make_job()
        events = [
            {
                "event": "project_constitution_loaded",
                "job_id": str(job.id),
                "run_id": "r",
                "timestamp": "2026-05-05T10:00:00+00:00",
                "metadata": {"source_count": 3, "warning_count": 0, "has_test_commands": True},
            }
        ]
        out = summarize_timeline(job, events)
        assert "sources=3" in out

    def test_constitution_event_shows_tests_yes(self):
        from packages.orchestration.timeline import summarize_timeline

        job = _make_job()
        events = [
            {
                "event": "project_constitution_loaded",
                "job_id": str(job.id),
                "run_id": "r",
                "timestamp": "2026-05-05T10:00:00+00:00",
                "metadata": {"source_count": 1, "warning_count": 0, "has_test_commands": True},
            }
        ]
        out = summarize_timeline(job, events)
        assert "tests=yes" in out

    def test_constitution_event_shows_tests_no(self):
        from packages.orchestration.timeline import summarize_timeline

        job = _make_job()
        events = [
            {
                "event": "project_constitution_loaded",
                "job_id": str(job.id),
                "run_id": "r",
                "timestamp": "2026-05-05T10:00:00+00:00",
                "metadata": {"source_count": 0, "warning_count": 1, "has_test_commands": False},
            }
        ]
        out = summarize_timeline(job, events)
        assert "tests=no" in out
        assert "warnings=1" in out

    def test_constitution_event_shows_no_warnings_when_zero(self):
        from packages.orchestration.timeline import summarize_timeline

        job = _make_job()
        events = [
            {
                "event": "project_constitution_loaded",
                "job_id": str(job.id),
                "run_id": "r",
                "timestamp": "2026-05-05T10:00:00+00:00",
                "metadata": {"source_count": 2, "warning_count": 0, "has_test_commands": True},
            }
        ]
        out = summarize_timeline(job, events)
        assert "warnings=" not in out  # no warnings field when count is 0

    def test_constitution_event_no_raw_content(self):
        """Timeline rendering must not show raw source file contents."""
        from packages.orchestration.timeline import summarize_timeline

        job = _make_job()
        events = [
            {
                "event": "project_constitution_loaded",
                "job_id": str(job.id),
                "run_id": "r",
                "timestamp": "2026-05-05T10:00:00+00:00",
                "metadata": {
                    "source_count": 1,
                    "warning_count": 0,
                    "has_test_commands": True,
                    # Even if raw content were accidentally stored, it must not render
                    "raw_content": "MUST_NOT_APPEAR_IN_TIMELINE",
                },
            }
        ]
        out = summarize_timeline(job, events)
        assert "MUST_NOT_APPEAR_IN_TIMELINE" not in out

    def test_generic_event_no_longer_shows_for_constitution(self):
        """The old '○ project_constitution_loaded' generic fallback is replaced."""
        from packages.orchestration.timeline import summarize_timeline

        job = _make_job()
        events = [
            {
                "event": "project_constitution_loaded",
                "job_id": str(job.id),
                "run_id": "r",
                "timestamp": "2026-05-05T10:00:00+00:00",
                "metadata": {"source_count": 2, "warning_count": 0, "has_test_commands": True},
            }
        ]
        out = summarize_timeline(job, events)
        # Must NOT be the raw event name; must be the human-readable label
        assert "○ project_constitution_loaded" not in out
        assert "Project Constitution loaded" in out
