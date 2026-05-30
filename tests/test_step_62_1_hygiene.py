"""Tests for Step 62.1 — Hygiene Closure.

Shared symbols, no duplicate _section, brain detail registry completeness,
no silent exception swallow.
"""

from __future__ import annotations

import ast
from pathlib import Path
from uuid import uuid4

import pytest

from packages.core.models import Job, RunState, Task
from packages.orchestration.storage import save_job


def _make_job() -> Job:
    return Job(
        id=uuid4(),
        name="hygiene-test",
        user_prompt="test",
        state=RunState.RUNNING,
        tasks=[Task(id=uuid4(), description="t", status=RunState.PENDING,
                     inputs={"task_type": "patch"}, output_artifact_ids=[])],
        artifacts=[],
        metadata={},
    )


class TestSharedSymbols:
    def test_symbols_module_has_section(self):
        from packages.orchestration._symbols import section
        result = section("Test")
        assert "Test" in result
        assert "\u2500" in result

    def test_section_width_default(self):
        from packages.orchestration._symbols import section
        result = section("Hello")
        # Default width=50, so bar length = max(1, 50 - len("Hello") - 1) = 44
        assert result.count("\u2500") >= 44

    def test_section_width_custom(self):
        from packages.orchestration._symbols import section
        result = section("Hello", width=64)
        assert result.count("\u2500") >= 58


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


class TestBrainDetailRegistry:
    def test_registry_exists(self):
        from packages.orchestration.brain_detail import (
            _DETAIL_REGISTRY,
            _DETAIL_REGISTRY_JOB,
        )
        assert isinstance(_DETAIL_REGISTRY, dict)
        assert isinstance(_DETAIL_REGISTRY_JOB, dict)
        assert len(_DETAIL_REGISTRY) + len(_DETAIL_REGISTRY_JOB) >= 25

    def test_known_node_types_covered(self):
        """Every NT_* constant from project_brain must have a detail handler."""
        import packages.orchestration.project_brain as pb
        from packages.orchestration.brain_detail import (
            _DETAIL_REGISTRY,
            _DETAIL_REGISTRY_JOB,
        )

        all_nt = {
            v for name, v in vars(pb).items()
            if name.startswith("NT_") and isinstance(v, str)
        }
        covered = set(_DETAIL_REGISTRY.keys()) | set(_DETAIL_REGISTRY_JOB.keys())
        uncovered = all_nt - covered
        assert uncovered == set(), f"Node types without detail handler: {uncovered}"

    def test_all_handlers_callable(self):
        from packages.orchestration.brain_detail import (
            _DETAIL_REGISTRY,
            _DETAIL_REGISTRY_JOB,
        )
        for nt, handler in {**_DETAIL_REGISTRY, **_DETAIL_REGISTRY_JOB}.items():
            assert callable(handler), f"Handler for {nt} is not callable"

    def test_brain_detail_builds_for_all_node_types(self, tmp_path, monkeypatch):
        """build_brain_node_detail must not raise for any node in a real graph."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.brain_detail import build_brain_node_detail
        from packages.orchestration.project_brain import build_project_brain

        job = _make_job()
        save_job(job)
        graph = build_project_brain(job, [])
        for node in graph.nodes:
            detail = build_brain_node_detail(job, graph, node.id, [])
            assert detail.node_id == node.id
            assert detail.node_type == node.type


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
            "packages/orchestration/context_pack.py",
            "packages/orchestration/storage.py",
        ]
        for mod in modules:
            src = Path(mod).read_text()
            assert "except Exception:" not in src, f"{mod} has bare except Exception:"


class TestBrainViewerNarrowedException:
    def test_viewer_no_bare_except_exception(self):
        src = Path("packages/orchestration/brain_viewer.py").read_text()
        assert "except Exception:" not in src
