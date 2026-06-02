"""Tests: small-repo fixtures for autocoder validation."""
from __future__ import annotations

import json
import subprocess
import sys

import pytest

from tests.orchestration.small_repo_fixtures import (
    create_missing_function_repo,
    create_repair_scenario_repo,
    create_wrong_return_repo,
    fixture_patch_missing_function,
    fixture_patch_repair_cycle1,
    fixture_patch_repair_cycle2,
    fixture_patch_wrong_return,
)


class TestRepoCreation:
    def test_missing_function_repo_has_expected_files(self, tmp_path):
        repo = create_missing_function_repo(tmp_path / "repo")
        assert (repo / "app.py").is_file()
        assert (repo / "tests" / "test_app.py").is_file()
        assert (repo / "tests" / "__init__.py").is_file()
        content = (repo / "app.py").read_text()
        assert "def hello" not in content

    def test_wrong_return_repo_has_expected_files(self, tmp_path):
        repo = create_wrong_return_repo(tmp_path / "repo")
        assert (repo / "app.py").is_file()
        content = (repo / "app.py").read_text()
        assert "goodbye" in content

    def test_repair_scenario_repo_has_expected_files(self, tmp_path):
        repo = create_repair_scenario_repo(tmp_path / "repo")
        assert (repo / "calc.py").is_file()
        assert (repo / "tests" / "test_calc.py").is_file()
        content = (repo / "calc.py").read_text()
        assert "return a - b" in content
        assert "return a + b" in content


class TestRepoTestExecution:
    def test_missing_function_repo_fails_before_patch(self, tmp_path):
        repo = create_missing_function_repo(tmp_path / "repo")
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "-x", "-q", "--no-header"],
            capture_output=True, text=True, timeout=30, cwd=str(repo),
        )
        assert proc.returncode != 0

    def test_wrong_return_repo_fails_before_patch(self, tmp_path):
        repo = create_wrong_return_repo(tmp_path / "repo")
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "-x", "-q", "--no-header"],
            capture_output=True, text=True, timeout=30, cwd=str(repo),
        )
        assert proc.returncode != 0

    def test_repair_scenario_repo_fails_before_patch(self, tmp_path):
        repo = create_repair_scenario_repo(tmp_path / "repo")
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "-x", "-q", "--no-header"],
            capture_output=True, text=True, timeout=30, cwd=str(repo),
        )
        assert proc.returncode != 0


class TestFixturePatchApplication:
    def test_missing_function_patch_makes_tests_pass(self, tmp_path):
        repo = create_missing_function_repo(tmp_path / "repo")
        patch = fixture_patch_missing_function()
        for op in patch["file_ops"]:
            (repo / op["path"]).write_text(op["content"], encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "-x", "-q", "--no-header"],
            capture_output=True, text=True, timeout=30, cwd=str(repo),
        )
        assert proc.returncode == 0

    def test_wrong_return_patch_makes_tests_pass(self, tmp_path):
        repo = create_wrong_return_repo(tmp_path / "repo")
        patch = fixture_patch_wrong_return()
        for op in patch["file_ops"]:
            (repo / op["path"]).write_text(op["content"], encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "-x", "-q", "--no-header"],
            capture_output=True, text=True, timeout=30, cwd=str(repo),
        )
        assert proc.returncode == 0

    def test_repair_cycle1_still_fails(self, tmp_path):
        repo = create_repair_scenario_repo(tmp_path / "repo")
        patch = fixture_patch_repair_cycle1()
        for op in patch["file_ops"]:
            (repo / op["path"]).write_text(op["content"], encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "-x", "-q", "--no-header"],
            capture_output=True, text=True, timeout=30, cwd=str(repo),
        )
        assert proc.returncode != 0

    def test_repair_cycle2_makes_tests_pass(self, tmp_path):
        repo = create_repair_scenario_repo(tmp_path / "repo")
        patch = fixture_patch_repair_cycle2()
        for op in patch["file_ops"]:
            (repo / op["path"]).write_text(op["content"], encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "-x", "-q", "--no-header"],
            capture_output=True, text=True, timeout=30, cwd=str(repo),
        )
        assert proc.returncode == 0


class TestBridgeIntegration:
    def test_fixture_bridge_e2e_missing_function(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from packages.core.models import Job
        from packages.orchestration.builder_bridge import run_builder_bridge
        from packages.orchestration.builder_models import BuilderOutput

        repo = create_missing_function_repo(tmp_path / "repo")
        patch = fixture_patch_missing_function()
        output = BuilderOutput(
            summary="Add hello function",
            proposed_changes=["Add hello() to app.py"],
            structured_patch_text=json.dumps(patch),
            structured_patch_format="json",
        )
        job = Job(name="fixture-smoke")
        result = run_builder_bridge(
            output, repo, job=job, data_dir=tmp_path / "data",
            autonomy_level=4,
        )
        assert result.parse_result.parse_success is True
        assert result.apply_success is True
        assert result.test_passed is True
        assert result.stage == "proof_collected"

    def test_fixture_bridge_e2e_wrong_return(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from packages.core.models import Job
        from packages.orchestration.builder_bridge import run_builder_bridge
        from packages.orchestration.builder_models import BuilderOutput

        repo = create_wrong_return_repo(tmp_path / "repo")
        patch = fixture_patch_wrong_return()
        output = BuilderOutput(
            summary="Fix hello return value",
            proposed_changes=["Fix hello() return"],
            structured_patch_text=json.dumps(patch),
            structured_patch_format="json",
        )
        job = Job(name="fixture-smoke")
        result = run_builder_bridge(
            output, repo, job=job, data_dir=tmp_path / "data",
            autonomy_level=4,
        )
        assert result.parse_result.parse_success is True
        assert result.apply_success is True
        assert result.test_passed is True

    def test_no_raw_output_in_bridge_events(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from packages.core.models import Job
        from packages.orchestration.builder_bridge import run_builder_bridge
        from packages.orchestration.builder_models import BuilderOutput
        from packages.orchestration.timeline import load_run_events

        repo = create_missing_function_repo(tmp_path / "repo")
        patch = fixture_patch_missing_function()
        output = BuilderOutput(
            summary="Add hello function",
            proposed_changes=["Add hello() to app.py"],
            structured_patch_text=json.dumps(patch),
            structured_patch_format="json",
        )
        job = Job(name="test")
        run_builder_bridge(
            output, repo, job=job, data_dir=tmp_path / "data",
            autonomy_level=4,
        )
        events = load_run_events(tmp_path / "data", job.id)
        for event in events:
            meta = event.get("metadata", {})
            for key, val in meta.items():
                if isinstance(val, str):
                    assert "def hello" not in val, f"Raw content leaked in {key}"
                    assert "return" not in val or key in ("error_kind",), \
                        f"Suspicious content in {key}: {val[:60]}"
