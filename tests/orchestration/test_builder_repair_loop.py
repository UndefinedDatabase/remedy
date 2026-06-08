"""Tests: bounded repair loop with structured patch via builder bridge."""
from __future__ import annotations

import json

import pytest

from packages.core.models import Job
from packages.orchestration.builder_models import BuilderOutput


def _make_output(fix_content: str, action: str = "modify") -> BuilderOutput:
    patch_text = json.dumps({
        "file_ops": [{"path": "calc.py", "action": action, "content": fix_content}]
    })
    return BuilderOutput(
        summary="Fix calc",
        proposed_changes=["Fix calc"],
        structured_patch_text=patch_text,
        structured_patch_format="json",
    )


class TestRepairLoopSuccess:
    def test_succeeds_on_first_cycle(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.builder_bridge import run_builder_bridge_loop

        (tmp_path / "calc.py").write_text("def add(a, b):\n    return a - b\n")
        (tmp_path / "tests").mkdir()
        (tmp_path / "tests" / "test_calc.py").write_text(
            "from calc import add\n\ndef test_add():\n    assert add(2, 3) == 5\n"
        )
        fix = "def add(a, b):\n    return a + b\n"

        def build_fn(repair_ctx):
            return _make_output(fix)

        job = Job(name="test")
        result = run_builder_bridge_loop(
            build_fn, tmp_path, job=job, data_dir=tmp_path, max_cycles=3,
        )
        assert result.success is True
        assert result.cycles_run == 1
        assert len(result.repair_contexts) == 0

    def test_succeeds_on_second_cycle(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.builder_bridge import run_builder_bridge_loop

        (tmp_path / "calc.py").write_text("def add(a, b):\n    return 0\n")
        (tmp_path / "tests").mkdir()
        (tmp_path / "tests" / "test_calc.py").write_text(
            "from calc import add\n\ndef test_add():\n    assert add(2, 3) == 5\n"
        )

        call_count = [0]
        def build_fn(repair_ctx):
            call_count[0] += 1
            if call_count[0] == 1:
                # Wrong fix first time
                return _make_output("def add(a, b):\n    return a - b\n")
            else:
                # Correct fix
                return _make_output("def add(a, b):\n    return a + b\n")

        job = Job(name="test")
        result = run_builder_bridge_loop(
            build_fn, tmp_path, job=job, data_dir=tmp_path, max_cycles=3,
        )
        assert result.success is True
        assert result.cycles_run == 2
        assert len(result.repair_contexts) == 1


class TestRepairLoopFailure:
    def test_stops_at_max_cycles(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.builder_bridge import run_builder_bridge_loop

        (tmp_path / "calc.py").write_text("def add(a, b):\n    return 0\n")
        (tmp_path / "tests").mkdir()
        (tmp_path / "tests" / "test_calc.py").write_text(
            "from calc import add\n\ndef test_add():\n    assert add(2, 3) == 5\n"
        )

        def build_fn(repair_ctx):
            return _make_output("def add(a, b):\n    return a - b\n")

        job = Job(name="test")
        result = run_builder_bridge_loop(
            build_fn, tmp_path, job=job, data_dir=tmp_path, max_cycles=2,
        )
        assert result.success is False
        assert result.cycles_run == 2

    def test_stops_on_parse_failure(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.builder_bridge import run_builder_bridge_loop

        def build_fn(repair_ctx):
            return BuilderOutput(summary="Plan", proposed_changes=["Plan stuff"])

        job = Job(name="test")
        result = run_builder_bridge_loop(
            build_fn, tmp_path, job=job, data_dir=tmp_path, max_cycles=3,
        )
        assert result.success is False
        assert result.cycles_run == 1
        assert result.final_result.stage == "parse_failed"


class TestRepairLoopRepairContext:
    def test_repair_context_passed_to_builder(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.builder_bridge import run_builder_bridge_loop

        (tmp_path / "calc.py").write_text("def add(a, b):\n    return 0\n")
        (tmp_path / "tests").mkdir()
        (tmp_path / "tests" / "test_calc.py").write_text(
            "from calc import add\n\ndef test_add():\n    assert add(2, 3) == 5\n"
        )

        received_contexts = []
        call_count = [0]
        def build_fn(repair_ctx):
            received_contexts.append(repair_ctx)
            call_count[0] += 1
            if call_count[0] <= 1:
                return _make_output("def add(a, b):\n    return a - b\n")
            return _make_output("def add(a, b):\n    return a + b\n")

        job = Job(name="test")
        run_builder_bridge_loop(
            build_fn, tmp_path, job=job, data_dir=tmp_path, max_cycles=3,
        )
        assert received_contexts[0] is None  # First call: no repair context
        assert received_contexts[1] is not None  # Second call: has repair context
        assert "failure_kind" in received_contexts[1]


class TestRepairLoopEvents:
    def test_cycle_events_emitted(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.builder_bridge import run_builder_bridge_loop
        from packages.orchestration.timeline import load_run_events

        (tmp_path / "calc.py").write_text("def add(a, b):\n    return 0\n")
        (tmp_path / "tests").mkdir()
        (tmp_path / "tests" / "test_calc.py").write_text(
            "from calc import add\n\ndef test_add():\n    assert add(2, 3) == 5\n"
        )

        def build_fn(repair_ctx):
            return _make_output("def add(a, b):\n    return a + b\n")

        job = Job(name="test")
        run_builder_bridge_loop(
            build_fn, tmp_path, job=job, data_dir=tmp_path, max_cycles=3,
        )
        events = load_run_events(tmp_path, job.id)
        event_types = [e["event"] for e in events]
        assert "repair_loop_cycle_started" in event_types
        assert "repair_loop_succeeded" in event_types
