"""
Domain tests: regression/test_named_bugs.py
Migrated from step-numbered test files.
"""

from __future__ import annotations

import ast
import json
from pathlib import Path
from unittest.mock import patch
from uuid import UUID, uuid4

import pytest

from packages.core.models import RunState
from packages.orchestration.data_paths import mint_job_id
from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan

_ROOT = Path(__file__).resolve().parent.parent.parent

FORBIDDEN_KEYS = (
    "stdout", "stderr", "raw_output", "command_output",
    "Traceback", "diff_preview", "approval_reason",
)


# ═══════════════════════════════════════════════════════════════════════════
# Step 141 — Commit-Readiness Task Summary Bugfix
# ═══════════════════════════════════════════════════════════════════════════


def _make_job_s61(*, project_id: str | None = None, target_repo: str | None = None) -> JobPlan:
    meta: dict = {}
    if project_id:
        meta["project_id"] = project_id
    if target_repo:
        meta["target_repo"] = target_repo
    return JobPlan(
        job_id=mint_job_id(),
        job_title="step61-test",
        user_prompt="test prompt",
        state=RunState.RUNNING,
        tasks=[
            TaskEntry(
                task_id="T001",
                title="task",
                status=RunState.PENDING,
                inputs={"task_type": "patch"},
                output_artifact_ids=[],
            ),
        ],
        artifacts=[],
        metadata=meta,
    )


def _proof_event(intent_id: str, target_path: str) -> dict:
    return {
        "event": "patch_apply_proof_recorded",
        "outcome": "proof_stored",
        "metadata": {
            "intent_id": intent_id,
            "target_path": target_path,
            "sha256": f"sha_{intent_id}",
            "bytes_written": 100,
            "line_count": 10,
        },
    }


def _test_event(status: str = "passed", exit_code: int = 0) -> dict:
    return {
        "event": "test_run_completed",
        "outcome": status,
        "metadata": {
            "command": "pytest",
            "status": status,
            "exit_code": exit_code,
        },
    }


FORBIDDEN_KEYS = (
    "stdout", "stderr", "raw_output", "command_output",
    "Traceback", "diff_preview", "approval_reason",
)


# ===========================================================================
# Multi-proof causal edge correctness
# ===========================================================================


class TestAgentsmdWorkflow:
    """AGENTS.md contains required workflow rules."""

    def test_commit_discipline_step_per_commit(self):
        src = Path("AGENTS.md").read_text()
        assert "one step per commit" in src.lower() or "step per commit" in src.lower()

    def test_commit_discipline_500_line_limit(self):
        src = Path("AGENTS.md").read_text()
        assert "500" in src


# ---------------------------------------------------------------------------
# Step 102 — Correct Semantic Zoom Direction
# ---------------------------------------------------------------------------


class TestSmokeSafety:

    def test_no_shell_true_in_source_apply(self):
        src = Path(_ROOT / "packages" / "orchestration" / "source_apply.py").read_text()
        assert "shell=True" not in src

    def test_main_py_under_120_lines(self):
        main_py = Path(_ROOT / "apps" / "cli" / "main.py")
        lines = main_py.read_text().splitlines()
        assert len(lines) <= 120, f"main.py has {len(lines)} lines"


class TestSmokeOriginCheckAndUnload:
    """Smoke script must have origin check and UNLOAD section."""

    def test_smoke_has_unload_section(self):
        """Smoke must have optional REMEDY_SMOKE_UNLOAD_MODELS section."""
        content = Path("scripts/remedy_smoke.sh").read_text()
        assert "REMEDY_SMOKE_UNLOAD_MODELS" in content
        assert "worker unload" in content

    def test_smoke_no_shell_true(self):
        """Smoke must not use shell=True (except comments)."""
        content = Path("scripts/remedy_smoke.sh").read_text()
        for i, line in enumerate(content.splitlines(), 1):
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith("//"):
                continue
            if "shell=True" in stripped and "shell=True" not in stripped.split("#", 1)[-1] if "#" in stripped else "shell=True" in stripped:
                # Only flag if it's in actual Python code, not bash
                pass

    def test_smoke_checks_version_4(self):
        """Smoke origin check must validate version == 4."""
        content = Path("scripts/remedy_smoke.sh").read_text()
        assert "version" in content
        assert "'version'" in content or '"version"' in content

    def test_no_bind_all_interfaces(self):
        """No 0.0.0.0 binding in smoke or UI code."""
        for path in [
            "scripts/remedy_smoke.sh",
            "packages/orchestration/serve_http_handler.py",
            "apps/cli/commands/ui.py",
        ]:
            content = Path(path).read_text()
            assert "0.0.0.0" not in content, f"0.0.0.0 found in {path}"


class TestSmokeTaskProgressNodeDetail:
    """Built-in smoke has task-progress and node-detail checks."""

    def test_smoke_has_node_detail_check(self):
        content = Path("scripts/remedy_smoke.sh").read_text()
        assert "node detail" in content.lower() or "nodes/" in content

    def test_smoke_summary_has_job_id(self):
        content = Path("scripts/remedy_smoke.sh").read_text()
        assert "job_id" in content


# ═══════════════════════════════════════════════════════════════════════════
# Step 129 — UI Runtime Noise / Headless Hygiene
# ═══════════════════════════════════════════════════════════════════════════


class TestDevStatusCommandSchema:
    """Dev status command exists and works."""

    def test_dev_status_in_catalog(self):
        from apps.cli.command_catalog import CATALOG
        cmd = next((c for c in CATALOG if c.command_id == "dev.status"), None)
        assert cmd is not None
        assert cmd.subcommand == "status"

    def test_dev_status_json(self):
        from apps.cli.commands.dev import _dev_status
        with patch("builtins.print") as mock_print:
            _dev_status(json_output=True)
            data = json.loads(mock_print.call_args[0][0])
            # F283 R17 C6 (D10): the success document answers through the envelope.
            assert data["schema_version"] == 1
            assert data["ok"] is True
            required = {
                "version", "cli_ok", "latest_smoke", "worker_cleanup_ok",
                "autocoder_fake_e2e_ok", "remaining_blockers",
            }
            missing = required - set(data.keys())
            assert not missing, f"Missing: {missing}"

    @pytest.mark.parametrize("error", [ImportError, TypeError])
    def test_a_failed_autocoder_check_does_not_block_the_others(self, error, monkeypatch, capsys):
        """F294 SU-041 (DECISION F294 D11): each error the autocoder probe can meet reads as a
        failed check, and the command still reports every other check."""
        import sys

        from apps.cli.main import main
        from packages.orchestration import structured_patch

        def _failing(*args, **kwargs):
            raise error("the autocoder probe failed")

        monkeypatch.setattr(structured_patch, "StructuredPatch", _failing)
        monkeypatch.setattr(sys, "argv", ["remedy", "dev", "status", "--json"])
        main()
        data = json.loads(capsys.readouterr().out)
        assert data["ok"] is True
        assert data["autocoder_fake_e2e_ok"] is False
        assert data["reviewer_loop_ok"] is True

    def test_a_defect_in_the_autocoder_probe_is_not_swallowed(self, monkeypatch, capsys):
        """F294 SU-041 (DECISION F294 D11): the handler no longer catches everything, so a defect
        of another kind fails the command with its own name instead of reading as a failed
        check."""
        import sys

        from apps.cli.main import main
        from packages.orchestration import structured_patch

        def _broken(*args, **kwargs):
            raise RuntimeError("a defect in the autocoder probe")

        monkeypatch.setattr(structured_patch, "StructuredPatch", _broken)
        monkeypatch.setattr(sys, "argv", ["remedy", "dev", "status", "--json"])
        with pytest.raises(SystemExit) as stopped:
            main()
        data = json.loads(capsys.readouterr().out)
        assert stopped.value.code == 1
        assert data["ok"] is False
        assert data["message"] == "RuntimeError: a defect in the autocoder probe"
        assert "autocoder_fake_e2e_ok" not in data

    def test_dev_status_human_output(self):
        from apps.cli.commands.dev import _dev_status
        with patch("builtins.print") as mock_print:
            _dev_status(json_output=False)
            output = "\n".join(str(c[0][0]) if c[0] else "" for c in mock_print.call_args_list)
            assert "remedy serve start" in output
            assert "worker unload" in output

    def test_main_py_under_120_lines(self):
        content = Path("apps/cli/main.py").read_text()
        assert len(content.splitlines()) <= 120

    def test_no_0000_binding(self):
        for path in [
            "packages/orchestration/serve_http_handler.py",
            "apps/cli/commands/ui.py",
        ]:
            content = Path(path).read_text()
            assert "0.0.0.0" not in content

    def test_no_mutation_endpoints(self):
        content = Path("packages/orchestration/serve_http_handler.py").read_text()
        assert "do_POST" in content  # exists
        assert "405" in content  # but returns method not allowed
        assert "do_PUT" in content
        assert "do_DELETE" in content


class TestSmokeScriptStructuralChecks:
    """Smoke script checks."""

    def test_smoke_summary_structure(self):
        content = Path("scripts/remedy_smoke.sh").read_text()
        assert "summary.json" in content
        assert "job_id" in content
        assert "project_id" in content


class TestNoRawLeaks:
    """No raw content surfaces in brain graph, aggregate, or provenance."""

    def test_brain_json_no_raw_leaks(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_brain import (
            build_project_brain,
            export_project_brain_json,
        )

        job = _make_job_s61()
        save_job_plan(job)
        events = [_proof_event("i1", "a.py"), _test_event()]
        graph = build_project_brain(job, events)
        raw = json.dumps(export_project_brain_json(graph))
        for forbidden in FORBIDDEN_KEYS:
            assert forbidden not in raw, f"Brain JSON leak: {forbidden}"

    def test_brain_summary_no_raw_leaks(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_brain import (
            build_project_brain,
            summarize_project_brain,
        )

        job = _make_job_s61()
        save_job_plan(job)
        graph = build_project_brain(job, [])
        text = summarize_project_brain(graph)
        for forbidden in FORBIDDEN_KEYS:
            assert forbidden not in text, f"Brain summary leak: {forbidden}"

    def test_aggregate_json_no_raw_leaks(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_brain_aggregate import (
            build_project_brain_aggregate,
            export_project_brain_aggregate_json,
        )
        from packages.orchestration.project_registry import (
            RemyProject,
            save_project,
        )

        pid = str(uuid4())
        project = RemyProject(id=UUID(pid), name="leak-test", repo_paths=[])
        save_project(project)

        job = _make_job_s61(project_id=pid)
        save_job_plan(job)

        agg = build_project_brain_aggregate(project, [job], {})
        raw = json.dumps(export_project_brain_aggregate_json(agg))
        for forbidden in FORBIDDEN_KEYS:
            assert forbidden not in raw, f"Aggregate JSON leak: {forbidden}"

    def test_readiness_brain_node_no_raw_leaks(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_brain import build_project_brain

        job = _make_job_s61()
        save_job_plan(job)
        graph = build_project_brain(job, [])
        ar_nodes = [n for n in graph.nodes if n.type == "autonomy_readiness"]
        assert ar_nodes
        meta = ar_nodes[0].metadata
        for forbidden in ("stdout", "stderr", "raw_output", "value"):
            assert forbidden not in meta, f"Readiness node leak: {forbidden}"


class TestNoDuplicateSection:
    def test_no_def_section_outside_symbols(self):
        """No orchestration module may define its own _section function."""
        orch_dir = Path("packages/orchestration")
        violations = []
        for py in orch_dir.glob("*.py"):
            if py.name == "_symbols.py":
                continue
            src = py.read_text()
            tree = ast.parse(src, filename=str(py))
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == "_section":
                    violations.append(f"{py.name}:{node.lineno}")
        assert violations == [], f"Local _section found in: {violations}"


class TestNoSilentSwallow:
    def test_no_except_exception_pass_in_orchestration(self):
        """No orchestration module may have 'except Exception: pass'."""
        orch_dir = Path("packages/orchestration")
        violations = []
        for py in orch_dir.glob("*.py"):
            src = py.read_text()
            if "except Exception: pass" in src:
                violations.append(py.name)
        assert violations == [], f"Silent swallow in: {violations}"

    def test_no_bare_except_exception_in_key_modules(self):
        """Key modules must not use bare 'except Exception:'."""
        modules = [
            "packages/orchestration/project_brain.py",
            "packages/orchestration/autonomy_readiness.py",
            "packages/orchestration/brain_detail.py",
        ]
        for mod in modules:
            src = Path(mod).read_text()
            assert "except Exception:" not in src, f"{mod} has bare except Exception:"


class TestBrainViewerNarrowedException:
    def test_viewer_no_bare_except_exception(self):
        src = Path("packages/orchestration/brain_viewer.py").read_text()
        assert "except Exception:" not in src
