"""Tests: real repair loop hardening on small-repo fixtures."""
from __future__ import annotations

import json

import pytest

from packages.orchestration.builder_models import BuilderOutput
from tests.orchestration.small_repo_fixtures import (
    create_repair_scenario_repo,
    fixture_patch_repair_cycle1,
    fixture_patch_repair_cycle2,
)


class TestDeterministicRepairLoop:
    def test_succeeds_in_two_cycles(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from packages.core.models import Job
        from packages.orchestration.builder_bridge import run_builder_bridge_loop
        from packages.orchestration.storage import save_job

        repo = create_repair_scenario_repo(tmp_path / "repo")
        cycle_patches = [fixture_patch_repair_cycle1(), fixture_patch_repair_cycle2()]

        def build_fn(ctx):
            idx = 0 if ctx is None else 1
            return BuilderOutput(
                summary="Fix calc",
                proposed_changes=["Fix functions"],
                structured_patch_text=json.dumps(cycle_patches[idx]),
                structured_patch_format="json",
            )

        job = Job(name="repair-test")
        save_job(job)
        result = run_builder_bridge_loop(
            build_fn, repo, job=job, data_dir=tmp_path / "data",
            max_cycles=3,
        )
        assert result.success is True
        assert result.cycles_run == 2
        assert result.stop_reason == ""
        assert (repo / "calc.py").read_text().strip().endswith("return a * b")

    def test_malformed_patch_stops_safely(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from packages.core.models import Job
        from packages.orchestration.builder_bridge import run_builder_bridge_loop
        from packages.orchestration.storage import save_job

        repo = create_repair_scenario_repo(tmp_path / "repo")

        def build_fn(ctx):
            return BuilderOutput(
                summary="Fix",
                proposed_changes=["Fix"],
                structured_patch_text="Just fix the code please",
            )

        job = Job(name="test")
        save_job(job)
        result = run_builder_bridge_loop(
            build_fn, repo, job=job, data_dir=tmp_path / "data",
            max_cycles=3,
        )
        assert result.success is False
        assert result.stop_reason == "provider_output_prose_only"
        assert result.cycles_run == 1

    def test_repeated_patch_stops_safely(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from packages.core.models import Job
        from packages.orchestration.builder_bridge import run_builder_bridge_loop
        from packages.orchestration.storage import save_job

        repo = create_repair_scenario_repo(tmp_path / "repo")
        same_patch = json.dumps(fixture_patch_repair_cycle1())

        def build_fn(ctx):
            return BuilderOutput(
                summary="Fix calc",
                proposed_changes=["Fix functions"],
                structured_patch_text=same_patch,
            )

        job = Job(name="test")
        save_job(job)
        result = run_builder_bridge_loop(
            build_fn, repo, job=job, data_dir=tmp_path / "data",
            max_cycles=3,
        )
        assert result.stop_reason == "repeated_patch_detected"
        assert result.success is False
        assert result.cycles_run <= 2

    def test_max_cycles_exhausted_stops_safely(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from packages.core.models import Job
        from packages.orchestration.builder_bridge import run_builder_bridge_loop
        from packages.orchestration.storage import save_job

        repo = create_repair_scenario_repo(tmp_path / "repo")
        counter = [0]

        def build_fn(ctx):
            counter[0] += 1
            patch = fixture_patch_repair_cycle1()
            patch["file_ops"][0]["content"] += f"\n# attempt {counter[0]}\n"
            return BuilderOutput(
                summary="Fix calc",
                proposed_changes=["Fix functions"],
                structured_patch_text=json.dumps(patch),
            )

        job = Job(name="test")
        save_job(job)
        result = run_builder_bridge_loop(
            build_fn, repo, job=job, data_dir=tmp_path / "data",
            max_cycles=2,
        )
        assert result.stop_reason == "repair_budget_exhausted"
        assert result.cycles_run == 2

    def test_source_apply_approval_gate_intact(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from packages.core.models import Job
        from packages.orchestration.builder_bridge import run_builder_bridge_loop
        from packages.orchestration.storage import save_job

        repo = create_repair_scenario_repo(tmp_path / "repo")

        def build_fn(ctx):
            return BuilderOutput(
                summary="Fix calc",
                proposed_changes=["Fix functions"],
                structured_patch_text=json.dumps(fixture_patch_repair_cycle2()),
            )

        job = Job(name="test")
        save_job(job)
        result = run_builder_bridge_loop(
            build_fn, repo, job=job, data_dir=tmp_path / "data",
            autonomy_level=2, max_cycles=2,
        )
        assert result.success is False
        assert result.final_result.stage == "approval_pending"
        assert result.final_result.stop_reason == "approval_required"

    def test_no_raw_output_leaks_in_repair_events(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from packages.core.models import Job
        from packages.orchestration.builder_bridge import run_builder_bridge_loop
        from packages.orchestration.storage import save_job
        from packages.orchestration.timeline import load_run_events

        repo = create_repair_scenario_repo(tmp_path / "repo")

        def build_fn(ctx):
            idx = 0 if ctx is None else 1
            patches = [fixture_patch_repair_cycle1(), fixture_patch_repair_cycle2()]
            return BuilderOutput(
                summary="Fix calc",
                proposed_changes=["Fix functions"],
                structured_patch_text=json.dumps(patches[idx]),
            )

        job = Job(name="test")
        save_job(job)
        run_builder_bridge_loop(
            build_fn, repo, job=job, data_dir=tmp_path / "data",
            max_cycles=3,
        )

        events = load_run_events(tmp_path / "data", job.id)
        for event in events:
            meta_str = str(event.get("metadata", {}))
            assert "return a - b" not in meta_str
            assert "return a + b" not in meta_str
            assert "return a * b" not in meta_str

    def test_events_recorded_per_cycle(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from packages.core.models import Job
        from packages.orchestration.builder_bridge import run_builder_bridge_loop
        from packages.orchestration.storage import save_job
        from packages.orchestration.timeline import load_run_events

        repo = create_repair_scenario_repo(tmp_path / "repo")

        def build_fn(ctx):
            idx = 0 if ctx is None else 1
            patches = [fixture_patch_repair_cycle1(), fixture_patch_repair_cycle2()]
            return BuilderOutput(
                summary="Fix calc",
                proposed_changes=["Fix functions"],
                structured_patch_text=json.dumps(patches[idx]),
            )

        job = Job(name="test")
        save_job(job)
        run_builder_bridge_loop(
            build_fn, repo, job=job, data_dir=tmp_path / "data",
            max_cycles=3,
        )

        events = load_run_events(tmp_path / "data", job.id)
        cycle_events = [e for e in events if e["event"] == "repair_loop_cycle_started"]
        assert len(cycle_events) == 2
        success_events = [e for e in events if e["event"] == "repair_loop_succeeded"]
        assert len(success_events) == 1
