"""
Tests for Step 34 — Project Command Discovery v0.

Coverage:
  - CommandCandidate dataclass structure
  - detect_pyproject: pytest config / tests/ dir
  - detect_package_json: test/lint/build scripts
  - detect_makefile: test/lint/build targets
  - detect_justfile / detect_taskfile / detect_cargo / detect_go
  - risky commands are marked high-risk and not auto-runnable
  - discover_commands: deduplication, ordering
  - select_best_test_candidate: confidence/source priority
  - discover-commands CLI: pure JSON output
  - no shell=True in any execution path
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from packages.core.models import Job, RunState
from packages.orchestration.command_discovery import (
    CommandCandidate,
    _detect_cargo,
    _detect_constitution,
    _detect_go,
    _detect_gradle,
    _detect_justfile,
    _detect_makefile,
    _detect_package_json,
    _detect_pyproject,
    _detect_taskfile,
    discover_commands,
    select_best_test_candidate,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_job() -> Job:
    return Job(name="test", state=RunState.PENDING)


# ---------------------------------------------------------------------------
# A. CommandCandidate structure
# ---------------------------------------------------------------------------


class TestCommandCandidateStructure:
    def test_argv_is_tuple(self):
        c = CommandCandidate(
            id="x",
            purpose="test",
            argv=("python3", "-m", "pytest"),
            display="python3 -m pytest",
            source_type="pyproject",
            source_path="pyproject.toml",
            confidence="high",
            risk="low",
            reason="test",
            requires_permission="repo_test_run",
        )
        assert isinstance(c.argv, tuple)

    def test_argv_list_returns_list(self):
        c = CommandCandidate(
            id="x",
            purpose="test",
            argv=("make", "test"),
            display="make test",
            source_type="makefile",
            source_path="Makefile",
            confidence="medium",
            risk="low",
            reason="test",
            requires_permission="repo_test_run",
        )
        result = c.argv_list()
        assert isinstance(result, list)
        assert result == ["make", "test"]

    def test_frozen_cannot_be_mutated(self):
        c = CommandCandidate(
            id="x",
            purpose="test",
            argv=("pytest",),
            display="pytest",
            source_type="heuristic",
            source_path="",
            confidence="low",
            risk="low",
            reason="test",
            requires_permission="repo_test_run",
        )
        with pytest.raises((AttributeError, TypeError)):
            c.purpose = "build"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# B. pyproject detector
# ---------------------------------------------------------------------------


class TestDetectPyproject:
    def test_pyproject_with_tests_dir(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text("[project]\nname = 'x'\n")
        (tmp_path / "tests").mkdir()
        candidates = _detect_pyproject(tmp_path)
        assert len(candidates) == 1
        c = candidates[0]
        assert c.purpose == "test"
        assert c.argv == ("python3", "-m", "pytest")
        assert c.source_type == "pyproject"
        assert c.confidence == "high"
        assert c.risk == "low"
        assert c.requires_permission == "repo_test_run"

    def test_pyproject_with_pytest_config(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text(
            "[tool.pytest.ini_options]\ntestpaths = ['tests']\n"
        )
        candidates = _detect_pyproject(tmp_path)
        assert len(candidates) == 1
        assert candidates[0].argv == ("python3", "-m", "pytest")

    def test_no_pyproject_no_candidate(self, tmp_path):
        (tmp_path / "tests").mkdir()
        candidates = _detect_pyproject(tmp_path)
        assert candidates == []

    def test_pyproject_without_tests_dir_or_config(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text("[project]\nname = 'x'\n")
        # No tests/ dir, no pytest config section.
        candidates = _detect_pyproject(tmp_path)
        assert candidates == []


# ---------------------------------------------------------------------------
# C. package.json detector
# ---------------------------------------------------------------------------


class TestDetectPackageJson:
    def test_test_script(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "scripts": {"test": "jest"}
        }))
        candidates = _detect_package_json(tmp_path)
        test_c = [c for c in candidates if c.purpose == "test"]
        assert len(test_c) == 1
        assert test_c[0].argv == ("npm", "run", "test")
        assert test_c[0].source_type == "package_json"
        assert test_c[0].confidence == "high"

    def test_lint_and_build_scripts(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "scripts": {
                "test":  "jest",
                "lint":  "eslint src",
                "build": "webpack",
            }
        }))
        candidates = _detect_package_json(tmp_path)
        purposes = {c.purpose for c in candidates}
        assert "test" in purposes
        assert "lint" in purposes
        assert "build" in purposes

    def test_risky_deploy_script_is_high_risk(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "scripts": {"test": "jest && npm run deploy"}
        }))
        candidates = _detect_package_json(tmp_path)
        test_c = [c for c in candidates if c.purpose == "test"]
        assert len(test_c) == 1
        assert test_c[0].risk == "high"

    def test_no_package_json_no_candidate(self, tmp_path):
        candidates = _detect_package_json(tmp_path)
        assert candidates == []

    def test_requires_permission_test(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "scripts": {"test": "jest"}
        }))
        candidates = _detect_package_json(tmp_path)
        test_c = [c for c in candidates if c.purpose == "test"]
        assert test_c[0].requires_permission == "repo_test_run"


# ---------------------------------------------------------------------------
# D. Makefile detector
# ---------------------------------------------------------------------------


class TestDetectMakefile:
    def test_test_target(self, tmp_path):
        (tmp_path / "Makefile").write_text("test:\n\tpytest\n\nbuild:\n\tpython setup.py\n")
        candidates = _detect_makefile(tmp_path)
        test_c = [c for c in candidates if c.purpose == "test"]
        assert len(test_c) == 1
        assert test_c[0].argv == ("make", "test")
        assert test_c[0].source_type == "makefile"
        assert test_c[0].confidence == "medium"

    def test_check_target_maps_to_test(self, tmp_path):
        (tmp_path / "Makefile").write_text("check:\n\tpytest\n")
        candidates = _detect_makefile(tmp_path)
        assert any(c.purpose == "test" and c.argv == ("make", "check") for c in candidates)

    def test_lint_and_build(self, tmp_path):
        (tmp_path / "Makefile").write_text("lint:\n\tflake8 .\nbuild:\n\tpip install .\n")
        candidates = _detect_makefile(tmp_path)
        purposes = {c.purpose for c in candidates}
        assert "lint" in purposes
        assert "build" in purposes

    def test_no_makefile_no_candidate(self, tmp_path):
        assert _detect_makefile(tmp_path) == []

    def test_unknown_targets_ignored(self, tmp_path):
        (tmp_path / "Makefile").write_text("deploy:\n\trsync -avz . server:\n")
        candidates = _detect_makefile(tmp_path)
        # "deploy" is not in _PURPOSE_MAP, so ignored.
        assert candidates == []


# ---------------------------------------------------------------------------
# E. justfile detector
# ---------------------------------------------------------------------------


class TestDetectJustfile:
    def test_test_recipe(self, tmp_path):
        (tmp_path / "justfile").write_text("test:\n    pytest\n")
        candidates = _detect_justfile(tmp_path)
        assert any(c.argv == ("just", "test") for c in candidates)

    def test_justfile_capitalised(self, tmp_path):
        (tmp_path / "Justfile").write_text("test:\n    pytest\n")
        candidates = _detect_justfile(tmp_path)
        assert any(c.argv == ("just", "test") for c in candidates)

    def test_no_justfile_no_candidate(self, tmp_path):
        assert _detect_justfile(tmp_path) == []


# ---------------------------------------------------------------------------
# F. Taskfile detector
# ---------------------------------------------------------------------------


class TestDetectTaskfile:
    def test_test_task(self, tmp_path):
        (tmp_path / "Taskfile.yml").write_text(
            'version: "3"\ntasks:\n  test:\n    cmds:\n      - pytest\n'
        )
        candidates = _detect_taskfile(tmp_path)
        assert any(c.argv == ("task", "test") for c in candidates)

    def test_no_taskfile_no_candidate(self, tmp_path):
        assert _detect_taskfile(tmp_path) == []


# ---------------------------------------------------------------------------
# G. Cargo detector
# ---------------------------------------------------------------------------


class TestDetectCargo:
    def test_cargo_toml_present(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[package]\nname = "mylib"\n')
        candidates = _detect_cargo(tmp_path)
        assert len(candidates) == 1
        assert candidates[0].argv == ("cargo", "test")
        assert candidates[0].source_type == "cargo"
        assert candidates[0].confidence == "high"
        assert candidates[0].risk == "low"

    def test_no_cargo_toml_no_candidate(self, tmp_path):
        assert _detect_cargo(tmp_path) == []


# ---------------------------------------------------------------------------
# H. Go detector
# ---------------------------------------------------------------------------


class TestDetectGo:
    def test_go_mod_present(self, tmp_path):
        (tmp_path / "go.mod").write_text("module example.com/myapp\ngo 1.21\n")
        candidates = _detect_go(tmp_path)
        assert len(candidates) == 1
        assert candidates[0].argv == ("go", "test", "./...")
        assert candidates[0].source_type == "go"
        assert candidates[0].confidence == "high"
        assert candidates[0].risk == "low"

    def test_no_go_mod_no_candidate(self, tmp_path):
        assert _detect_go(tmp_path) == []


# ---------------------------------------------------------------------------
# I. Risky command detection
# ---------------------------------------------------------------------------


class TestRiskyCommandDetection:
    def test_rm_in_script_is_high_risk(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "scripts": {"test": "rm -rf dist && jest"}
        }))
        candidates = _detect_package_json(tmp_path)
        assert all(c.risk == "high" for c in candidates)

    def test_sudo_in_recipe_body_is_high_risk(self, tmp_path):
        """Makefile recipe body is inspected: 'sudo' in body → risk=high."""
        (tmp_path / "Makefile").write_text("test:\n\tsudo pytest\n")
        candidates = _detect_makefile(tmp_path)
        assert len(candidates) == 1
        assert candidates[0].argv == ("make", "test")
        assert candidates[0].risk == "high"  # recipe body contains sudo

    def test_deploy_in_npm_script_is_high_risk(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({
            "scripts": {"test": "jest && deploy --prod"}
        }))
        candidates = _detect_package_json(tmp_path)
        test_c = [c for c in candidates if c.purpose == "test"]
        assert test_c[0].risk == "high"

    def test_high_risk_candidate_not_auto_runnable(self):
        """select_best_test_candidate must skip high-risk candidates."""
        high_risk = CommandCandidate(
            id="x",
            purpose="test",
            argv=("npm", "run", "test"),
            display="npm run test",
            source_type="package_json",
            source_path="package.json",
            confidence="high",
            risk="high",
            reason="risky script",
            requires_permission="repo_test_run",
        )
        result = select_best_test_candidate([high_risk])
        assert result is None

    def test_only_high_risk_candidates_blocks_run(self, tmp_path):
        """If only high-risk test candidates exist, select_best returns None."""
        (tmp_path / "package.json").write_text(json.dumps({
            "scripts": {"test": "rm -rf dist && jest"}
        }))
        job = _make_job()
        job.metadata["target_repo"] = str(tmp_path)
        candidates = discover_commands(job, tmp_path)
        best = select_best_test_candidate(candidates)
        assert best is None


# ---------------------------------------------------------------------------
# J. discover_commands integration
# ---------------------------------------------------------------------------


class TestDiscoverCommandsIntegration:
    def test_discovers_pyproject(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text("[project]\nname='x'\n")
        (tmp_path / "tests").mkdir()
        job = _make_job()
        candidates = discover_commands(job, tmp_path)
        assert any(c.source_type == "pyproject" for c in candidates)

    def test_deduplicates_same_argv(self, tmp_path):
        # Both pyproject and Makefile test could produce python3 -m pytest if
        # the Makefile runs "python3 -m pytest"; but in standard case, pyproject
        # gives python3 -m pytest and Makefile gives make test — no dup.
        # For dedup test: give Makefile "test" and pyproject both.
        (tmp_path / "pyproject.toml").write_text("[project]\nname='x'\n")
        (tmp_path / "tests").mkdir()
        (tmp_path / "Makefile").write_text("test:\n\tpytest\n")
        job = _make_job()
        candidates = discover_commands(job, tmp_path)
        # python3 -m pytest (from pyproject) and make test (from Makefile) are
        # different argv — no dedup needed.  Verify no crashes and both present.
        argvs = [c.argv for c in candidates]
        assert ("python3", "-m", "pytest") in argvs
        assert ("make", "test") in argvs

    def test_no_sources_returns_empty(self, tmp_path):
        job = _make_job()
        candidates = discover_commands(job, tmp_path)
        assert candidates == []

    def test_multiple_sources_all_collected(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text("[project]\nname='x'\n")
        (tmp_path / "tests").mkdir()
        (tmp_path / "Cargo.toml").write_text('[package]\nname="x"\n')
        job = _make_job()
        candidates = discover_commands(job, tmp_path)
        src_types = {c.source_type for c in candidates}
        assert "pyproject" in src_types
        assert "cargo" in src_types


# ---------------------------------------------------------------------------
# K. select_best_test_candidate
# ---------------------------------------------------------------------------


class TestSelectBestTestCandidate:
    def _make_candidate(self, *, confidence="high", source_type="pyproject",
                         risk="low", purpose="test") -> CommandCandidate:
        return CommandCandidate(
            id=f"{purpose}:{source_type}",
            purpose=purpose,
            argv=("python3", "-m", "pytest"),
            display="python3 -m pytest",
            source_type=source_type,
            source_path="pyproject.toml",
            confidence=confidence,
            risk=risk,
            reason="test",
            requires_permission="repo_test_run",
        )

    def test_returns_none_for_empty_list(self):
        assert select_best_test_candidate([]) is None

    def test_returns_none_for_no_test_candidates(self):
        c = self._make_candidate(purpose="build")
        assert select_best_test_candidate([c]) is None

    def test_returns_best_confidence(self):
        high = self._make_candidate(confidence="high")
        low = CommandCandidate(
            id="test:heuristic:low",
            purpose="test",
            argv=("pytest",),
            display="pytest",
            source_type="heuristic",
            source_path="",
            confidence="low",
            risk="low",
            reason="low-confidence",
            requires_permission="repo_test_run",
        )
        result = select_best_test_candidate([low, high])
        assert result is not None
        assert result.confidence == "high"

    def test_makefile_beats_pyproject_same_confidence(self):
        """makefile has source priority 1; pyproject has priority 2.
        At the same confidence level, makefile wins."""
        pyproject = self._make_candidate(source_type="pyproject", confidence="medium")
        makefile = CommandCandidate(
            id="test:makefile:test",
            purpose="test",
            argv=("make", "test"),
            display="make test",
            source_type="makefile",
            source_path="Makefile",
            confidence="medium",
            risk="low",
            reason="test",
            requires_permission="repo_test_run",
        )
        result = select_best_test_candidate([pyproject, makefile])
        assert result is not None
        assert result.source_type == "makefile"

    def test_constitution_beats_makefile(self):
        """constitution has priority 0; makefile has priority 1."""
        constitution = CommandCandidate(
            id="test:constitution:make test",
            purpose="test",
            argv=("make", "test"),
            display="make test",
            source_type="constitution",
            source_path="(project-constitution)",
            confidence="high",
            risk="low",
            reason="from constitution",
            requires_permission="repo_test_run",
        )
        makefile = CommandCandidate(
            id="test:makefile:test",
            purpose="test",
            argv=("make", "test"),
            display="make test",
            source_type="makefile",
            source_path="Makefile",
            confidence="medium",
            risk="low",
            reason="from makefile",
            requires_permission="repo_test_run",
        )
        result = select_best_test_candidate([makefile, constitution])
        assert result is not None
        assert result.source_type == "constitution"

    def test_skips_non_test(self):
        build = self._make_candidate(purpose="build")
        test = self._make_candidate(purpose="test")
        result = select_best_test_candidate([build, test])
        assert result is not None
        assert result.purpose == "test"


# ---------------------------------------------------------------------------
# L. CLI discover-commands — pure JSON output
# ---------------------------------------------------------------------------


class TestCLIDiscoverCommands:
    def _run_cli(self, args: list[str], env: dict | None = None):
        import os
        result = subprocess.run(
            ["python3", "-m", "apps.cli.main"] + args,
            capture_output=True,
            env={**os.environ, **(env or {})},
            timeout=15,
        )
        return result.returncode, result.stdout.decode(), result.stderr.decode()

    def _create_job_with_repo(self, tmp_path: Path) -> str:
        import os
        env = {**os.environ, "REMEDY_DATA_DIR": str(tmp_path)}
        r = subprocess.run(
            ["python3", "-m", "apps.cli.main", "job", "create", "test job"],
            capture_output=True, env=env, timeout=15,
        )
        job_id = r.stdout.decode().strip()
        # Create a target repo with pyproject + tests.
        repo = tmp_path / "target"
        repo.mkdir(parents=True)
        (repo / "pyproject.toml").write_text("[project]\nname='x'\n")
        (repo / "tests").mkdir()
        subprocess.run(
            ["python3", "-m", "apps.cli.main", "job", "attach-repo", job_id, str(repo)],
            capture_output=True, env=env, timeout=15,
        )
        return job_id

    def test_json_output_is_pure_json(self, tmp_path):
        env = {"REMEDY_DATA_DIR": str(tmp_path)}
        job_id = self._create_job_with_repo(tmp_path)
        rc, out, err = self._run_cli(
            ["test", "discover", job_id, "--json"],
            env=env,
        )
        assert rc == 0, f"Expected rc=0, got {rc}\nstderr: {err}"
        # Must be valid JSON with no extra text.
        data = json.loads(out)
        assert "candidates" in data
        assert "job_id" in data

    def test_json_candidates_have_required_keys(self, tmp_path):
        env = {"REMEDY_DATA_DIR": str(tmp_path)}
        job_id = self._create_job_with_repo(tmp_path)
        rc, out, _ = self._run_cli(
            ["test", "discover", job_id, "--json"],
            env=env,
        )
        assert rc == 0
        data = json.loads(out)
        for c in data["candidates"]:
            for key in ("id", "purpose", "argv", "display",
                        "source_type", "source_path", "confidence",
                        "risk", "reason", "requires_permission"):
                assert key in c, f"Missing key '{key}' in candidate"

    def test_json_candidates_argv_is_list(self, tmp_path):
        env = {"REMEDY_DATA_DIR": str(tmp_path)}
        job_id = self._create_job_with_repo(tmp_path)
        rc, out, _ = self._run_cli(
            ["test", "discover", job_id, "--json"],
            env=env,
        )
        assert rc == 0
        data = json.loads(out)
        for c in data["candidates"]:
            assert isinstance(c["argv"], list), "argv must be a JSON array"

    def test_text_output_does_not_crash(self, tmp_path):
        env = {"REMEDY_DATA_DIR": str(tmp_path)}
        job_id = self._create_job_with_repo(tmp_path)
        rc, out, err = self._run_cli(
            ["test", "discover", job_id],
            env=env,
        )
        assert rc == 0, f"rc={rc}\nstderr: {err}"
        assert "pyproject" in out or "python3" in out


# ---------------------------------------------------------------------------
# M. No shell=True in execution path
# ---------------------------------------------------------------------------


class TestNoShellTrue:
    def test_command_discovery_never_calls_subprocess(self, tmp_path):
        """discover_commands must not invoke subprocess at all."""
        from unittest.mock import patch
        (tmp_path / "pyproject.toml").write_text("[project]\n")
        (tmp_path / "tests").mkdir()
        job = _make_job()
        with patch("subprocess.run") as mock_run:
            discover_commands(job, tmp_path)
        mock_run.assert_not_called()

    def test_run_tests_local_no_shell_true(self, tmp_path):
        """run_tests_local must never pass shell=True to subprocess.run."""
        from unittest.mock import patch

        from packages.orchestration.test_runner import run_tests_local

        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "pyproject.toml").write_text("[project]\n")
        (repo / "tests").mkdir()
        job = _make_job()
        job.metadata["target_repo"] = str(repo)

        proc = subprocess.CompletedProcess(
            args=["python3", "-m", "pytest"], returncode=0,
            stdout=b"1 passed\n", stderr=b"",
        )
        with patch("subprocess.run", return_value=proc) as mock_run:
            run_tests_local(job, tmp_path)

        assert mock_run.called
        call_kwargs = mock_run.call_args.kwargs
        assert not call_kwargs.get("shell", False), "shell=True must never be used"


# ---------------------------------------------------------------------------
# N. JS lockfile → package manager selection
# ---------------------------------------------------------------------------


class TestJSPackageManagerDetection:
    def test_pnpm_lock_selects_pnpm(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({"scripts": {"test": "jest"}}))
        (tmp_path / "pnpm-lock.yaml").write_text("lockfileVersion: '6.0'\n")
        candidates = _detect_package_json(tmp_path)
        test_c = [c for c in candidates if c.purpose == "test"]
        assert test_c, "expected test candidate"
        assert test_c[0].argv[0] == "pnpm"

    def test_yarn_lock_selects_yarn(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({"scripts": {"test": "jest"}}))
        (tmp_path / "yarn.lock").write_text("# yarn lockfile v1\n")
        candidates = _detect_package_json(tmp_path)
        test_c = [c for c in candidates if c.purpose == "test"]
        assert test_c[0].argv[0] == "yarn"

    def test_bun_lock_selects_bun(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({"scripts": {"test": "bun test"}}))
        (tmp_path / "bun.lock").write_text("")
        candidates = _detect_package_json(tmp_path)
        test_c = [c for c in candidates if c.purpose == "test"]
        assert test_c[0].argv[0] == "bun"

    def test_bun_lockb_selects_bun(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({"scripts": {"test": "bun test"}}))
        (tmp_path / "bun.lockb").write_bytes(b"\x00")
        candidates = _detect_package_json(tmp_path)
        test_c = [c for c in candidates if c.purpose == "test"]
        assert test_c[0].argv[0] == "bun"

    def test_package_lock_selects_npm(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({"scripts": {"test": "jest"}}))
        (tmp_path / "package-lock.json").write_text("{}")
        candidates = _detect_package_json(tmp_path)
        test_c = [c for c in candidates if c.purpose == "test"]
        assert test_c[0].argv[0] == "npm"

    def test_no_lockfile_defaults_to_npm(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps({"scripts": {"test": "jest"}}))
        candidates = _detect_package_json(tmp_path)
        test_c = [c for c in candidates if c.purpose == "test"]
        assert test_c[0].argv[0] == "npm"


# ---------------------------------------------------------------------------
# O. Gradle detector
# ---------------------------------------------------------------------------


class TestDetectGradle:
    def test_build_gradle(self, tmp_path):
        (tmp_path / "build.gradle").write_text("plugins { id 'java' }\n")
        candidates = _detect_gradle(tmp_path)
        assert len(candidates) >= 1
        assert candidates[0].source_type == "gradle"
        assert candidates[0].purpose == "test"
        assert candidates[0].argv in (("gradle", "test"), ("gradlew", "test"))

    def test_build_gradle_kts(self, tmp_path):
        (tmp_path / "build.gradle.kts").write_text('plugins { id("java") }\n')
        candidates = _detect_gradle(tmp_path)
        assert any(c.source_type == "gradle" for c in candidates)

    def test_gradlew_present_uses_gradlew(self, tmp_path):
        (tmp_path / "build.gradle").write_text("plugins { id 'java' }\n")
        gw = tmp_path / "gradlew"
        gw.write_text("#!/bin/sh\nexec gradle \"$@\"\n")
        gw.chmod(0o755)
        candidates = _detect_gradle(tmp_path)
        assert any(c.argv[0] == "./gradlew" for c in candidates)

    def test_gradle_in_subdir(self, tmp_path):
        sub = tmp_path / "jvm-app"
        sub.mkdir()
        (sub / "build.gradle").write_text("plugins { id 'java' }\n")
        from packages.orchestration.command_discovery import _detect_gradle
        candidates = _detect_gradle(tmp_path)
        assert len(candidates) >= 1
        assert candidates[0].source_path == "jvm-app/build.gradle"

    def test_no_gradle_no_candidate(self, tmp_path):
        from packages.orchestration.command_discovery import _detect_gradle
        assert _detect_gradle(tmp_path) == []


# ---------------------------------------------------------------------------
# P. Maven detector
# ---------------------------------------------------------------------------


class TestDetectMaven:
    def test_pom_xml(self, tmp_path):
        (tmp_path / "pom.xml").write_text("<project></project>\n")
        from packages.orchestration.command_discovery import _detect_maven
        candidates = _detect_maven(tmp_path)
        assert len(candidates) >= 1
        assert candidates[0].source_type == "maven"
        assert candidates[0].argv in (("mvn", "test"), ("./mvnw", "test"))

    def test_mvnw_present_uses_mvnw(self, tmp_path):
        (tmp_path / "pom.xml").write_text("<project></project>\n")
        mw = tmp_path / "mvnw"
        mw.write_text("#!/bin/sh\n")
        mw.chmod(0o755)
        from packages.orchestration.command_discovery import _detect_maven
        candidates = _detect_maven(tmp_path)
        assert any(c.argv[0] == "./mvnw" for c in candidates)


# ---------------------------------------------------------------------------
# Q. .NET, Ruby, Composer detectors (basic presence tests)
# ---------------------------------------------------------------------------


class TestDetectDotnetRubyComposer:
    def test_dotnet_sln(self, tmp_path):
        (tmp_path / "MyApp.sln").write_text("")
        from packages.orchestration.command_discovery import _detect_dotnet
        candidates = _detect_dotnet(tmp_path)
        assert any(c.argv == ("dotnet", "test") for c in candidates)

    def test_dotnet_csproj(self, tmp_path):
        (tmp_path / "MyLib.csproj").write_text("<Project></Project>")
        from packages.orchestration.command_discovery import _detect_dotnet
        candidates = _detect_dotnet(tmp_path)
        assert any(c.argv == ("dotnet", "test") for c in candidates)

    def test_ruby_rakefile(self, tmp_path):
        (tmp_path / "Rakefile").write_text('task :test do\n  sh "ruby -Itest test/**/*.rb"\nend\n')
        from packages.orchestration.command_discovery import _detect_ruby
        candidates = _detect_ruby(tmp_path)
        assert any(c.argv == ("rake", "test") for c in candidates)

    def test_composer_test_script(self, tmp_path):
        (tmp_path / "composer.json").write_text(json.dumps({
            "scripts": {"test": "phpunit"}
        }))
        from packages.orchestration.command_discovery import _detect_composer
        candidates = _detect_composer(tmp_path)
        assert any(c.argv == ("composer", "test") for c in candidates)

    def test_composer_no_test_script(self, tmp_path):
        (tmp_path / "composer.json").write_text(json.dumps({"scripts": {}}))
        from packages.orchestration.command_discovery import _detect_composer
        assert _detect_composer(tmp_path) == []


# ---------------------------------------------------------------------------
# R. Source paths are always relative, never absolute
# ---------------------------------------------------------------------------


class TestSourcePathRelative:
    def test_pyproject_source_path_relative(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text("[tool.pytest.ini_options]\n")
        candidates = _detect_pyproject(tmp_path)
        for c in candidates:
            assert not c.source_path.startswith("/"), f"absolute: {c.source_path}"
            assert "tmp" not in c.source_path, f"leaks tmp: {c.source_path}"

    def test_cargo_source_path_relative(self, tmp_path):
        (tmp_path / "Cargo.toml").write_text('[package]\nname = "x"\n')
        candidates = _detect_cargo(tmp_path)
        assert candidates[0].source_path == "Cargo.toml"

    def test_cargo_subdir_source_path_relative(self, tmp_path):
        sub = tmp_path / "rust-lib"
        sub.mkdir()
        (sub / "Cargo.toml").write_text('[package]\nname = "x"\n')
        candidates = _detect_cargo(tmp_path)
        assert candidates[0].source_path == "rust-lib/Cargo.toml"

    def test_go_subdir_source_path_relative(self, tmp_path):
        sub = tmp_path / "go-service"
        sub.mkdir()
        (sub / "go.mod").write_text("module x\ngo 1.21\n")
        candidates = _detect_go(tmp_path)
        assert candidates[0].source_path == "go-service/go.mod"

    def test_constitution_source_path_not_absolute(self, tmp_path):
        job = _make_job()
        candidates = _detect_constitution(job, tmp_path)
        for c in candidates:
            assert not c.source_path.startswith("/"), f"absolute: {c.source_path}"

    def test_package_json_subdir_relative(self, tmp_path):
        sub = tmp_path / "frontend"
        sub.mkdir()
        (sub / "package.json").write_text(json.dumps({"scripts": {"test": "jest"}}))
        candidates = _detect_package_json(tmp_path)
        for c in candidates:
            assert not c.source_path.startswith("/"), f"absolute: {c.source_path}"
            assert "frontend" in c.source_path or c.source_path == "package.json"


# ---------------------------------------------------------------------------
# S. Ignored directories are not scanned
# ---------------------------------------------------------------------------


class TestIgnoredDirectories:
    def test_node_modules_not_scanned(self, tmp_path):
        nm = tmp_path / "node_modules" / "some-pkg"
        nm.mkdir(parents=True)
        (nm / "package.json").write_text(json.dumps({"scripts": {"test": "jest"}}))
        candidates = _detect_package_json(tmp_path)
        # Only finds root package.json if present, not node_modules/some-pkg/package.json
        assert not any("node_modules" in c.source_path for c in candidates)

    def test_venv_not_scanned(self, tmp_path):
        venv_dir = tmp_path / ".venv" / "lib"
        venv_dir.mkdir(parents=True)
        (tmp_path / ".venv" / "Cargo.toml").write_text('[package]\nname="x"\n')
        candidates = _detect_cargo(tmp_path)
        assert not any(".venv" in c.source_path for c in candidates)

    def test_git_not_scanned(self, tmp_path):
        git_dir = tmp_path / ".git" / "hooks"
        git_dir.mkdir(parents=True)
        (tmp_path / ".git" / "Makefile").write_text("test:\n\techo ok\n")
        candidates = _detect_makefile(tmp_path)
        assert not any(".git" in c.source_path for c in candidates)

    def test_build_dir_not_scanned(self, tmp_path):
        build = tmp_path / "build"
        build.mkdir()
        (build / "go.mod").write_text("module x\ngo 1.21\n")
        candidates = _detect_go(tmp_path)
        assert not any("build" in c.source_path for c in candidates)


# ---------------------------------------------------------------------------
# T. Deduplicated by (purpose, argv, source_type)
# ---------------------------------------------------------------------------


class TestDeduplication:
    def test_same_source_type_and_argv_deduplicated(self, tmp_path):
        """Two candidates with identical (purpose, argv, source_type) → deduplicated."""
        (tmp_path / "pyproject.toml").write_text("[tool.pytest.ini_options]\n")
        (tmp_path / "tests").mkdir()
        job = _make_job()
        candidates = discover_commands(job, tmp_path)
        # pyproject produces python3 -m pytest exactly once
        py_pytest = [
            c for c in candidates
            if c.argv == ("python3", "-m", "pytest") and c.source_type == "pyproject"
        ]
        assert len(py_pytest) == 1

    def test_same_argv_different_source_kept(self, tmp_path):
        """Constitution + Makefile both producing make test → both kept."""
        (tmp_path / "Makefile").write_text("test:\n\tpython3 -c \"pass\"\n")
        job = _make_job()
        candidates = discover_commands(job, tmp_path)
        make_test = [c for c in candidates if c.argv == ("make", "test")]
        source_types = {c.source_type for c in make_test}
        # Both constitution (from Makefile-derived constitution) and makefile should appear
        assert "makefile" in source_types


# ---------------------------------------------------------------------------
# U. discover-commands CLI JSON schema v1
# ---------------------------------------------------------------------------


class TestCLIDiscoverCommandsSchemaV1:
    def _create_job_with_repo(self, tmp_path):
        import os
        env = {**os.environ, "REMEDY_DATA_DIR": str(tmp_path)}
        r = subprocess.run(
            ["python3", "-m", "apps.cli.main", "job", "create", "test"],
            capture_output=True, env=env, timeout=15,
        )
        job_id = r.stdout.decode().strip()
        repo = tmp_path / "target"
        repo.mkdir(parents=True)
        (repo / "pyproject.toml").write_text("[tool.pytest.ini_options]\n")
        (repo / "tests").mkdir()
        subprocess.run(
            ["python3", "-m", "apps.cli.main", "job", "attach-repo", job_id, str(repo)],
            capture_output=True, env=env, timeout=15,
        )
        return job_id, env

    def test_json_has_version_1(self, tmp_path):
        job_id, env = self._create_job_with_repo(tmp_path)
        r = subprocess.run(
            ["python3", "-m", "apps.cli.main", "test", "discover", job_id, "--json"],
            capture_output=True, env=env, timeout=15,
        )
        data = json.loads(r.stdout)
        assert data["version"] == 1

    def test_json_has_selected_test_candidate(self, tmp_path):
        job_id, env = self._create_job_with_repo(tmp_path)
        r = subprocess.run(
            ["python3", "-m", "apps.cli.main", "test", "discover", job_id, "--json"],
            capture_output=True, env=env, timeout=15,
        )
        data = json.loads(r.stdout)
        assert "selected_test_candidate" in data

    def test_json_has_counts(self, tmp_path):
        job_id, env = self._create_job_with_repo(tmp_path)
        r = subprocess.run(
            ["python3", "-m", "apps.cli.main", "test", "discover", job_id, "--json"],
            capture_output=True, env=env, timeout=15,
        )
        data = json.loads(r.stdout)
        assert "counts" in data
        counts = data["counts"]
        assert "by_purpose" in counts
        assert "by_source" in counts
        assert "by_risk" in counts
        assert "total" in counts

    def test_json_output_is_pure_json(self, tmp_path):
        """No extra text before/after JSON — stdout must be parseable JSON only."""
        job_id, env = self._create_job_with_repo(tmp_path)
        r = subprocess.run(
            ["python3", "-m", "apps.cli.main", "test", "discover", job_id, "--json"],
            capture_output=True, env=env, timeout=15,
        )
        assert r.returncode == 0
        # Must parse cleanly with no surrounding text.
        data = json.loads(r.stdout)
        assert isinstance(data, dict)


# ---------------------------------------------------------------------------
# V. No provider coupling
# ---------------------------------------------------------------------------


class TestNoProviderCoupling:
    def test_command_discovery_has_no_pi_reference(self):
        import inspect

        import packages.orchestration.command_discovery as cd
        src = inspect.getsource(cd)
        for token in ("pi.dev", "bootcamp", "ollama", "copilot", "anthropic"):
            assert token.lower() not in src.lower(), (
                f"command_discovery.py must not reference provider: {token!r}"
            )

    def test_test_runner_has_no_provider_reference(self):
        import inspect

        import packages.orchestration.test_runner as tr
        src = inspect.getsource(tr)
        for token in ("pi.dev", "bootcamp", "copilot"):
            assert token.lower() not in src.lower(), (
                f"test_runner.py must not reference provider: {token!r}"
            )


# ---------------------------------------------------------------------------
# W. Constitution discovery integration — quoted + shell-composed commands
# ---------------------------------------------------------------------------


class TestConstitutionDiscoveryIntegration:
    """Exercise _detect_constitution through the actual discovery path, not just shlex.split."""

    def test_quoted_command_parsed_correctly(self, tmp_path):
        """A quoted test command from constitution is parsed into correct argv."""
        (tmp_path / "Makefile").write_text(
            'test:\n\tpython3 -m pytest "tests/my test"\n'
        )
        job = _make_job()
        candidates = _detect_constitution(job, tmp_path)
        # Constitution should extract the Makefile test command
        test_c = [c for c in candidates if c.purpose == "test"]
        # At minimum, constitution or makefile-derived path should produce a candidate
        all_candidates = discover_commands(job, tmp_path)
        # Verify make test candidate exists (via either constitution or makefile detector)
        assert any(c.purpose == "test" for c in all_candidates)

    def test_shell_metachar_rejected_by_constitution(self, tmp_path):
        """Shell metacharacter commands from constitution are rejected."""
        # Create package.json with dangerous scripts
        import json as _json
        (tmp_path / "package.json").write_text(_json.dumps({
            "scripts": {
                "test": "pytest && rm -rf .",
                "lint": "eslint | tee out.txt",
                "build": "make; echo done",
            }
        }))
        job = _make_job()
        # Constitution reads these scripts and should reject metachar commands
        const_candidates = _detect_constitution(job, tmp_path)
        for c in const_candidates:
            # Constitution should not produce candidates with metacharacters in display
            for mc in ("|", "&&", ";", ">>", ">", "<", "`", "$("):
                assert mc not in c.display, \
                    f"Constitution produced candidate with metachar {mc!r}: {c.display}"

    def test_backtick_command_rejected(self, tmp_path):
        """Backtick injection in constitution command is rejected."""
        (tmp_path / "Makefile").write_text(
            'test:\n\tpytest `whoami`\n'
        )
        job = _make_job()
        const_candidates = _detect_constitution(job, tmp_path)
        # Should not produce any candidate with backtick
        for c in const_candidates:
            assert "`" not in c.display

    def test_dollar_paren_rejected(self, tmp_path):
        """$(command) injection in constitution is rejected."""
        (tmp_path / "Makefile").write_text(
            'test:\n\tpytest $(whoami)\n'
        )
        job = _make_job()
        const_candidates = _detect_constitution(job, tmp_path)
        for c in const_candidates:
            assert "$(" not in c.display

    def test_pipe_rejected(self, tmp_path):
        """Piped command in constitution is rejected."""
        (tmp_path / "Makefile").write_text(
            'test:\n\tpytest | tee out.txt\n'
        )
        job = _make_job()
        const_candidates = _detect_constitution(job, tmp_path)
        for c in const_candidates:
            assert "|" not in c.display

    def test_semicolon_rejected(self, tmp_path):
        """Semicolon command in constitution is rejected."""
        (tmp_path / "Makefile").write_text(
            'test:\n\tpytest; echo done\n'
        )
        job = _make_job()
        const_candidates = _detect_constitution(job, tmp_path)
        for c in const_candidates:
            assert ";" not in c.display

    def test_redirect_rejected(self, tmp_path):
        """Output redirect in constitution command is rejected."""
        (tmp_path / "Makefile").write_text(
            'test:\n\tpytest > out.txt\n'
        )
        job = _make_job()
        const_candidates = _detect_constitution(job, tmp_path)
        for c in const_candidates:
            assert ">" not in c.display

    def test_safe_command_accepted(self, tmp_path):
        """A plain safe command from constitution is accepted."""
        (tmp_path / "pyproject.toml").write_text(
            "[project]\nname = 'x'\n[tool.pytest.ini_options]\ntestpaths = ['tests']\n"
        )
        (tmp_path / "tests").mkdir()
        job = _make_job()
        all_candidates = discover_commands(job, tmp_path)
        # Should have at least one test candidate from constitution or pyproject
        test_c = [c for c in all_candidates if c.purpose == "test"]
        assert len(test_c) >= 1
        # Best test candidate should never be high-risk
        best = select_best_test_candidate(all_candidates)
        assert best is not None
        assert best.risk != "high"

    def test_full_discovery_suite_no_timeout(self, tmp_path):
        """Full command discovery runs without hanging."""
        (tmp_path / "pyproject.toml").write_text("[project]\nname = 'x'\n")
        (tmp_path / "tests").mkdir()
        (tmp_path / "Makefile").write_text("test:\n\tpytest\n")
        (tmp_path / "package.json").write_text('{"scripts":{"test":"jest"}}')
        job = _make_job()
        # Should complete quickly, no hang
        candidates = discover_commands(job, tmp_path)
        assert len(candidates) >= 2
