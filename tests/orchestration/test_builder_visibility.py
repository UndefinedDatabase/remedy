"""Tests: operator visibility for structured patch pipeline in dashboard."""
from __future__ import annotations

import json


class TestLiveStateBridgeFields:
    def test_bridge_fields_present_after_parse_event(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.builder_bridge import run_builder_bridge
        from packages.orchestration.builder_models import BuilderOutput
        from packages.orchestration.pingpong_job import JobPlan, save_job_plan
        from packages.orchestration.ui_server import _build_live_state_json

        job = JobPlan(job_title="test")
        save_job_plan(job)

        patch_text = json.dumps({
            "file_ops": [{"path": "a.py", "action": "create", "content": "x\n"}]
        })
        output = BuilderOutput(
            summary="Fix", proposed_changes=["Fix"],
            structured_patch_text=patch_text,
        )
        run_builder_bridge(output, tmp_path, job=job, data_dir=tmp_path, autonomy_level=2)

        state = _build_live_state_json(job)
        assert "builder_patch_parsed" in state
        assert state["builder_patch_parsed"] is True
        assert state["builder_patch_error"] == ""

    def test_bridge_fields_show_parse_error(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.builder_bridge import run_builder_bridge
        from packages.orchestration.builder_models import BuilderOutput
        from packages.orchestration.pingpong_job import JobPlan, save_job_plan
        from packages.orchestration.ui_server import _build_live_state_json

        job = JobPlan(job_title="test")
        save_job_plan(job)

        output = BuilderOutput(
            summary="Fix", proposed_changes=["Fix"],
            structured_patch_text="I think we should modify the code.",
        )
        run_builder_bridge(output, tmp_path, job=job, data_dir=tmp_path, autonomy_level=2)

        state = _build_live_state_json(job)
        assert state["builder_patch_parsed"] is False

    def test_repair_loop_cycle_in_state(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.builder_bridge import run_builder_bridge_loop
        from packages.orchestration.builder_models import BuilderOutput
        from packages.orchestration.pingpong_job import JobPlan, save_job_plan
        from packages.orchestration.ui_server import _build_live_state_json

        job = JobPlan(job_title="test")
        save_job_plan(job)

        (tmp_path / "calc.py").write_text("def add(a, b):\n    return 0\n")
        (tmp_path / "tests").mkdir()
        (tmp_path / "tests" / "test_calc.py").write_text(
            "from calc import add\n\ndef test_add():\n    assert add(2, 3) == 5\n"
        )

        def build_fn(repair_ctx):
            patch_text = json.dumps({
                "file_ops": [{"path": "calc.py", "action": "modify",
                              "content": "def add(a, b):\n    return a + b\n"}]
            })
            return BuilderOutput(
                summary="Fix", proposed_changes=["Fix"],
                structured_patch_text=patch_text,
            )

        run_builder_bridge_loop(
            build_fn, tmp_path, job=job, data_dir=tmp_path, max_cycles=2,
        )

        state = _build_live_state_json(job)
        assert state["repair_loop_cycle"] >= 1
        assert state["repair_loop_max_cycles"] >= 1

    def test_stage_map_recognizes_bridge_events(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.builder_bridge import run_builder_bridge
        from packages.orchestration.builder_models import BuilderOutput
        from packages.orchestration.pingpong_job import JobPlan, save_job_plan
        from packages.orchestration.ui_server import _build_live_state_json

        job = JobPlan(job_title="test")
        save_job_plan(job)

        patch_text = json.dumps({
            "file_ops": [{"path": "a.py", "action": "create", "content": "x\n"}]
        })
        output = BuilderOutput(
            summary="Fix", proposed_changes=["Fix"],
            structured_patch_text=patch_text,
        )
        run_builder_bridge(output, tmp_path, job=job, data_dir=tmp_path, autonomy_level=2)

        state = _build_live_state_json(job)
        # Last event should be builder_patch_parsed → stage="parsing"
        assert state["stage"] == "parsing"
