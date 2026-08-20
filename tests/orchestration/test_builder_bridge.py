"""Tests: builder bridge pipeline (BuilderOutput → parse → intent → apply → test)."""
from __future__ import annotations

import json
import subprocess

from packages.core.models import Job
from packages.orchestration import builder_bridge
from packages.orchestration.builder_models import BuilderOutput


class TestBuilderBridgeParseStage:
    def test_no_patch_text_fails_at_parse(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.builder_bridge import run_builder_bridge

        job = Job(name="test")
        output = BuilderOutput(summary="Plan", proposed_changes=["Plan stuff"])
        result = run_builder_bridge(output, tmp_path, job=job, data_dir=tmp_path)
        assert result.stage == "parse_failed"
        assert result.parse_result is not None
        assert result.parse_result.error_kind == "no_structured_patch_text"

    def test_prose_only_fails_at_parse(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.builder_bridge import run_builder_bridge

        job = Job(name="test")
        output = BuilderOutput(
            summary="Fix", proposed_changes=["Fix calc"],
            structured_patch_text="I think we should fix the function.",
        )
        result = run_builder_bridge(output, tmp_path, job=job, data_dir=tmp_path)
        assert result.stage == "parse_failed"
        assert result.parse_result.error_kind == "prose_only"

    def test_valid_json_parses(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.builder_bridge import run_builder_bridge

        job = Job(name="test")
        patch_text = json.dumps({
            "file_ops": [{"path": "calc.py", "action": "modify", "content": "x=1\n"}]
        })
        output = BuilderOutput(
            summary="Fix", proposed_changes=["Fix calc"],
            structured_patch_text=patch_text,
            structured_patch_format="json",
        )
        # autonomy_level=2 stops before apply
        result = run_builder_bridge(output, tmp_path, job=job, data_dir=tmp_path, autonomy_level=2)
        assert result.parse_result.parse_success is True
        assert result.stage == "approval_pending"


class TestBuilderBridgeApplyStage:
    def test_apply_with_autonomy_3(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.builder_bridge import run_builder_bridge

        job = Job(name="test")
        fix_content = "def add(a, b):\n    return a + b\n"
        patch_text = json.dumps({
            "file_ops": [{"path": "calc.py", "action": "create", "content": fix_content}]
        })
        output = BuilderOutput(
            summary="Fix", proposed_changes=["Fix calc"],
            structured_patch_text=patch_text,
            structured_patch_format="json",
        )
        result = run_builder_bridge(output, tmp_path, job=job, data_dir=tmp_path, autonomy_level=3)
        assert result.apply_success is True
        assert result.stage == "applied"
        assert (tmp_path / "calc.py").read_text() == fix_content

    def test_intent_created_and_approved(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.builder_bridge import run_builder_bridge

        job = Job(name="test")
        patch_text = json.dumps({
            "file_ops": [{"path": "a.py", "action": "create", "content": "x=1\n"}]
        })
        output = BuilderOutput(
            summary="Fix", proposed_changes=["Fix"],
            structured_patch_text=patch_text,
        )
        result = run_builder_bridge(output, tmp_path, job=job, data_dir=tmp_path, autonomy_level=3)
        assert result.intent_id != ""
        assert len(job.artifacts) >= 1


class TestBuilderBridgeTestStage:
    def test_full_pipeline_with_tests(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.builder_bridge import run_builder_bridge

        # Create test file first
        (tmp_path / "tests").mkdir()
        (tmp_path / "tests" / "test_calc.py").write_text(
            "from calc import add\n\ndef test_add():\n    assert add(2, 3) == 5\n"
        )
        fix_content = "def add(a, b):\n    return a + b\n"
        patch_text = json.dumps({
            "file_ops": [{"path": "calc.py", "action": "create", "content": fix_content}]
        })
        output = BuilderOutput(
            summary="Fix calc", proposed_changes=["Fix add"],
            structured_patch_text=patch_text,
        )
        job = Job(name="test")
        result = run_builder_bridge(output, tmp_path, job=job, data_dir=tmp_path, autonomy_level=4)
        assert result.apply_success is True
        assert result.test_passed is True
        assert result.stage == "proof_collected"

    def test_failing_test_detected(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.builder_bridge import run_builder_bridge

        # Create test that will fail
        (tmp_path / "tests").mkdir()
        (tmp_path / "tests" / "test_calc.py").write_text(
            "from calc import add\n\ndef test_add():\n    assert add(2, 3) == 99\n"
        )
        fix_content = "def add(a, b):\n    return a + b\n"
        patch_text = json.dumps({
            "file_ops": [{"path": "calc.py", "action": "create", "content": fix_content}]
        })
        output = BuilderOutput(
            summary="Fix calc", proposed_changes=["Fix add"],
            structured_patch_text=patch_text,
        )
        job = Job(name="test")
        result = run_builder_bridge(output, tmp_path, job=job, data_dir=tmp_path, autonomy_level=4)
        assert result.apply_success is True
        assert result.test_passed is False
        assert result.stage == "tested"


class TestBuilderBridgeEvents:
    def test_parse_event_emitted(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.builder_bridge import run_builder_bridge
        from packages.orchestration.timeline import load_run_events

        job = Job(name="test")
        patch_text = json.dumps({
            "file_ops": [{"path": "a.py", "action": "create", "content": "x\n"}]
        })
        output = BuilderOutput(
            summary="Fix", proposed_changes=["Fix"],
            structured_patch_text=patch_text,
        )
        run_builder_bridge(output, tmp_path, job=job, data_dir=tmp_path, autonomy_level=2)
        events = load_run_events(tmp_path, job.id)
        event_types = [e["event"] for e in events]
        assert "builder_patch_parsed" in event_types


class TestBuilderBridgeSafety:
    def test_shell_command_rejected(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.builder_bridge import run_builder_bridge

        job = Job(name="test")
        output = BuilderOutput(
            summary="Fix", proposed_changes=["Fix"],
            structured_patch_text="rm -rf / && echo done",
        )
        result = run_builder_bridge(output, tmp_path, job=job, data_dir=tmp_path)
        assert result.stage == "parse_failed"
        assert result.parse_result.error_kind == "unsafe_shell_command"

    def test_unsafe_path_rejected(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.builder_bridge import run_builder_bridge

        job = Job(name="test")
        patch_text = json.dumps({
            "file_ops": [{"path": "../etc/passwd", "action": "modify", "content": "x"}]
        })
        output = BuilderOutput(
            summary="Fix", proposed_changes=["Fix"],
            structured_patch_text=patch_text,
        )
        result = run_builder_bridge(output, tmp_path, job=job, data_dir=tmp_path, autonomy_level=3)
        assert result.stage == "parse_failed"
        assert result.parse_result.error_kind == "validation_failed"


def _run_bridge_test_stage(tmp_path):
    """Drive the bridge to stage 4 against a one-file fixture repo."""
    patch_text = json.dumps({
        "file_ops": [{"path": "calc.py", "action": "create", "content": "x = 1\n"}]
    })
    output = BuilderOutput(
        summary="Fix calc", proposed_changes=["Fix add"],
        structured_patch_text=patch_text,
    )
    return builder_bridge.run_builder_bridge(
        output, tmp_path, job=Job(name="test"), data_dir=tmp_path, autonomy_level=4
    )


class TestBuilderBridgeGuardSeam:
    """T002b's last `test`-class site, migrated onto the stage-1 guard."""

    def test_the_guard_receives_the_wall_the_cwd_and_the_bytecode_overlay(
        self, tmp_path, monkeypatch
    ):
        """Read off the call the seam receives, which the result cannot show."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        seen = {}

        def capture(cmd, **kwargs):
            seen.update(kwargs)
            return subprocess.CompletedProcess(list(cmd), 0, b"", b"")

        monkeypatch.setattr(builder_bridge, "run_guarded_test_command", capture)
        (tmp_path / "tests").mkdir()
        (tmp_path / "tests" / "test_calc.py").write_text("def test_ok():\n    pass\n")
        assert _run_bridge_test_stage(tmp_path).test_passed is True
        assert seen["timeout_sec"] == 60
        assert seen["cwd"] == str(tmp_path)
        assert seen["extra_env"] == {"PYTHONDONTWRITEBYTECODE": "1"}

    def test_a_secret_like_parent_variable_does_not_reach_the_test_child(
        self, tmp_path, monkeypatch
    ):
        """The overlay must still arrive while the parent's secret does not.

        Both halves are asserted inside the fixture repo's own test body, so the
        green `test_passed` below IS the assertion rather than a proxy for it.
        """
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        monkeypatch.setenv("REMEDY_BRIDGE_FAKE_TOKEN", "sk-not-a-real-secret")
        (tmp_path / "tests").mkdir()
        (tmp_path / "tests" / "test_env.py").write_text(
            "import os\n"
            "\n"
            "def test_env():\n"
            "    assert 'REMEDY_BRIDGE_FAKE_TOKEN' not in os.environ\n"
            "    assert os.environ.get('PYTHONDONTWRITEBYTECODE') == '1'\n"
        )
        assert _run_bridge_test_stage(tmp_path).test_passed is True
