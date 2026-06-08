"""Smoke tests for the builder bridge pipeline.

- Fixture smoke: runs deterministic BuilderOutput → full pipeline (no Ollama)
- Real Ollama smoke: opt-in via REMEDY_SMOKE_OLLAMA=1 (skipped by default)
"""
from __future__ import annotations

import json
import os

import pytest

from packages.core.models import Job
from packages.orchestration.builder_models import BuilderOutput


class TestFixtureBridgeSmoke:
    """CI-safe fixture smoke: BuilderOutput → parse → apply → test → proof."""

    def test_fixture_e2e_creates_and_fixes_calc(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.builder_bridge import run_builder_bridge

        # Setup: failing test
        (tmp_path / "tests").mkdir()
        (tmp_path / "tests" / "test_calc.py").write_text(
            "from calc import add, mul\n\n"
            "def test_add():\n    assert add(2, 3) == 5\n\n"
            "def test_mul():\n    assert mul(4, 5) == 20\n"
        )

        # BuilderOutput with fix
        fix_content = (
            "def add(a, b):\n    return a + b\n\n"
            "def mul(a, b):\n    return a * b\n"
        )
        patch_text = json.dumps({
            "file_ops": [
                {"path": "calc.py", "action": "create", "content": fix_content}
            ]
        })
        output = BuilderOutput(
            summary="Fix calc add and mul",
            proposed_changes=["Fix add to use +", "Fix mul to use *"],
            structured_patch_text=patch_text,
            structured_patch_format="json",
        )

        job = Job(name="fixture-smoke")
        result = run_builder_bridge(
            output, tmp_path, job=job, data_dir=tmp_path, autonomy_level=4,
        )

        assert result.parse_result.parse_success is True
        assert result.apply_success is True
        assert result.test_passed is True
        assert result.stage == "proof_collected"
        assert (tmp_path / "calc.py").exists()

    def test_fixture_unified_diff_e2e(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.builder_bridge import run_builder_bridge

        # Setup: existing wrong calc.py + test
        (tmp_path / "calc.py").write_text("def add(a, b):\n    return a - b\n")
        (tmp_path / "tests").mkdir()
        (tmp_path / "tests" / "test_calc.py").write_text(
            "from calc import add\n\ndef test_add():\n    assert add(2, 3) == 5\n"
        )

        # BuilderOutput with unified diff — note: source_apply only supports file_ops
        # so this tests parse but won't apply unified diff. Just verify parse stage.
        diff_text = (
            "--- a/calc.py\n+++ b/calc.py\n"
            "@@ -1,2 +1,2 @@\n def add(a, b):\n-    return a - b\n+    return a + b\n"
        )
        output = BuilderOutput(
            summary="Fix calc", proposed_changes=["Fix add"],
            structured_patch_text=diff_text,
            structured_patch_format="unified_diff",
        )
        job = Job(name="diff-smoke")
        result = run_builder_bridge(
            output, tmp_path, job=job, data_dir=tmp_path, autonomy_level=2,
        )
        assert result.parse_result.parse_success is True
        assert "calc.py" in result.parse_result.target_paths

    def test_fixture_fenced_json_e2e(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.builder_bridge import run_builder_bridge

        (tmp_path / "tests").mkdir()
        (tmp_path / "tests" / "test_calc.py").write_text(
            "from calc import add\n\ndef test_add():\n    assert add(1, 1) == 2\n"
        )
        fix_content = "def add(a, b):\\n    return a + b\\n"
        fenced = f'```json\n{{"file_ops": [{{"path": "calc.py", "action": "create", "content": "{fix_content}"}}]}}\n```'
        output = BuilderOutput(
            summary="Fix", proposed_changes=["Fix"],
            structured_patch_text=fenced,
        )
        job = Job(name="fenced-smoke")
        result = run_builder_bridge(
            output, tmp_path, job=job, data_dir=tmp_path, autonomy_level=4,
        )
        assert result.parse_result.parse_success is True
        assert result.apply_success is True


@pytest.mark.skipif(
    not os.environ.get("REMEDY_SMOKE_OLLAMA"),
    reason="Set REMEDY_SMOKE_OLLAMA=1 to run real Ollama smoke test",
)
class TestRealOllamaSmoke:
    """Real Ollama smoke test — requires running Ollama server."""

    def test_ollama_builder_produces_output(self):
        from uuid import uuid4
        from packages.orchestration.builder_models import (
            BuilderOutput,
            TaskExecutionContext,
            parse_builder_patch,
        )
        from packages.providers.ollama_builder.provider import OllamaBuilder

        builder = OllamaBuilder()
        context = TaskExecutionContext(
            job_id=uuid4(),
            task_id=uuid4(),
            job_prompt="Create a Python function that adds two numbers",
            task_type="code_change",
            task_description="Write an add function in calc.py",
        )
        output = builder.build(context)
        assert isinstance(output, BuilderOutput)
        assert output.summary
        assert len(output.proposed_changes) >= 1

        # If structured patch present, verify it parses
        if output.structured_patch_text:
            result = parse_builder_patch(output)
            # Don't assert success — model may or may not produce valid patch
            assert result.output_hash != ""
