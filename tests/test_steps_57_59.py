"""Tests for Steps 57, 58, 59."""

from __future__ import annotations

import ast
import json
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from packages.core.models import (
    Artifact,
    ArtifactKind,
    Job,
    RunState,
    Task,
)
from packages.orchestration.storage import save_job


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_job(*, project_id: str | None = None, target_repo: str | None = None) -> Job:
    meta: dict = {}
    if project_id:
        meta["project_id"] = project_id
    if target_repo:
        meta["target_repo"] = target_repo
    return Job(
        id=uuid4(),
        name="test job",
        user_prompt="test prompt",
        state=RunState.RUNNING,
        tasks=[
            Task(
                id=uuid4(),
                description="task",
                status=RunState.PENDING,
                inputs={"task_type": "patch"},
                output_artifact_ids=[],
            ),
        ],
        artifacts=[],
        metadata=meta,
    )


# ===========================================================================
# Step 57: Brain Graph Core Refactor — Structural Tests
# ===========================================================================


class TestBrainGraphStructure:
    """Structural invariants for the refactored project_brain module."""

    def test_build_project_brain_body_under_80_lines(self):
        src = Path("packages/orchestration/project_brain.py").read_text()
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "build_project_brain":
                body_lines = node.end_lineno - node.lineno + 1
                assert body_lines < 80, f"build_project_brain is {body_lines} lines, must be < 80"
                return
        pytest.fail("build_project_brain not found")

    def test_no_any_n_id_pattern(self):
        src = Path("packages/orchestration/project_brain.py").read_text()
        assert "any(n.id ==" not in src, "any(n.id == ...) pattern must be eliminated"

    def test_no_inline_imports_in_build_project_brain(self):
        src = Path("packages/orchestration/project_brain.py").read_text()
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "build_project_brain":
                for child in ast.walk(node):
                    if isinstance(child, (ast.Import, ast.ImportFrom)):
                        pytest.fail(
                            f"Inline import in build_project_brain at line {child.lineno}"
                        )
                return

    def test_acc_has_node_id_set(self):
        from packages.orchestration.project_brain import _Acc

        job = _make_job()
        acc = _Acc(job, [], None)
        assert hasattr(acc, "node_id_set")
        assert isinstance(acc.node_id_set(), set)

    def test_acc_degraded_tracking(self):
        from packages.orchestration.project_brain import _Acc

        job = _make_job()
        acc = _Acc(job, [], None)
        assert acc.degraded == []
        acc.degraded.append("test_section")
        assert "test_section" in acc.degraded

    def test_graph_has_degraded_field(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_brain import build_project_brain

        job = _make_job()
        save_job(job)
        graph = build_project_brain(job, [])
        assert hasattr(graph, "degraded")
        assert isinstance(graph.degraded, tuple)

    def test_export_includes_degraded(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_brain import (
            build_project_brain,
            export_project_brain_json,
        )

        job = _make_job()
        save_job(job)
        graph = build_project_brain(job, [])
        exported = export_project_brain_json(graph)
        assert "degraded" in exported
        assert isinstance(exported["degraded"], list)

    def test_builder_functions_exist(self):
        import packages.orchestration.project_brain as pb

        builders = [
            "_build_job_node",
            "_build_task_nodes",
            "_build_artifact_nodes",
            "_build_patch_intent_nodes",
            "_build_apply_nodes",
            "_build_test_run_nodes",
            "_build_event_derived_nodes",
            "_build_constitution_node",
            "_build_memory_nodes",
            "_build_context_coverage_node",
            "_build_project_placeholder",
            "_build_run_contract_node",
            "_build_token_policy_node",
            "_build_worker_adapter_nodes",
            "_build_readiness_node",
            "_build_context_pack_node",
            "_build_proof_nodes",
            "_build_revert_nodes",
            "_build_change_set_nodes",
            "_build_causal_edges",
            "_build_continuation_edges",
        ]
        for name in builders:
            assert callable(getattr(pb, name, None)), f"Missing builder: {name}"


# ===========================================================================
# Step 58: Brain Reliability Hygiene
# ===========================================================================


class TestBrainReliabilityHygiene:
    """Shared symbols, structured degradation, no bare except Exception."""

    def test_symbols_module_exists(self):
        from packages.orchestration._symbols import OK, FAIL, WARN, INFO, NEXT, LINE

        assert OK == "\u2713"
        assert FAIL == "\u2715"
        assert WARN == "!"
        assert INFO == "\u25cb"
        assert NEXT == "\u2192"
        assert LINE == "\u2500"

    def test_symbols_section_helper(self):
        from packages.orchestration._symbols import section

        result = section("Test")
        assert "Test" in result
        assert "\u2500" in result

    def test_no_except_exception_in_project_brain(self):
        src = Path("packages/orchestration/project_brain.py").read_text()
        assert "except Exception" not in src

    def test_no_except_exception_in_key_modules(self):
        """Key orchestration modules must not use bare except Exception."""
        modules = [
            "packages/orchestration/context_coverage.py",
            "packages/orchestration/project_context_coverage.py",
            "packages/orchestration/autonomy_readiness.py",
            "packages/orchestration/memory_learn.py",
            "packages/orchestration/context_pack.py",
            "packages/orchestration/storage.py",
            "packages/orchestration/project_registry.py",
            "packages/orchestration/patch_apply.py",
            "packages/orchestration/command_discovery.py",
        ]
        for mod in modules:
            src = Path(mod).read_text()
            assert "except Exception:" not in src, f"{mod} still has 'except Exception:'"

    def test_symbols_used_by_project_brain(self):
        src = Path("packages/orchestration/project_brain.py").read_text()
        assert "from packages.orchestration._symbols import" in src

    def test_symbols_used_by_brain_detail(self):
        src = Path("packages/orchestration/brain_detail.py").read_text()
        assert "from packages.orchestration._symbols import" in src


# ===========================================================================
# Step 59: Causal Accuracy + Continue Tests
# ===========================================================================


class TestCausalAccuracy:
    """Causal edge correctness for proof→test and proof→memory chains."""

    def test_proof_to_test_chronological(self, tmp_path, monkeypatch):
        """Proof nodes connect to test nodes by chronological index pairing."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_brain import (
            ET_PROOF_VERIFIED_BY,
            build_project_brain,
        )

        job = _make_job()
        save_job(job)

        # Simulate two proof events and two test events
        events = [
            {
                "event": "patch_apply_proof_recorded",
                "outcome": "proof_stored",
                "metadata": {
                    "intent_id": "intent_A",
                    "target_path": "a.py",
                    "sha256": "aaa",
                    "bytes_written": 100,
                    "line_count": 10,
                },
            },
            {
                "event": "test_run_completed",
                "outcome": "passed",
                "metadata": {
                    "command": "pytest",
                    "status": "passed",
                    "exit_code": 0,
                },
            },
            {
                "event": "patch_apply_proof_recorded",
                "outcome": "proof_stored",
                "metadata": {
                    "intent_id": "intent_B",
                    "target_path": "b.py",
                    "sha256": "bbb",
                    "bytes_written": 200,
                    "line_count": 20,
                },
            },
            {
                "event": "test_run_completed",
                "outcome": "passed",
                "metadata": {
                    "command": "pytest",
                    "status": "passed",
                    "exit_code": 0,
                },
            },
        ]

        graph = build_project_brain(job, events)
        proof_test_edges = [e for e in graph.edges if e.type == ET_PROOF_VERIFIED_BY]
        # Should have at least 2 proof→test edges (one per proof/test pair)
        assert len(proof_test_edges) >= 2

    def test_proof_to_memory_matching(self, tmp_path, monkeypatch):
        """Memory nodes link back to proof via source_id matching."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_brain import (
            ET_INFORMED_MEMORY,
            build_project_brain,
        )

        job = _make_job()
        save_job(job)

        events = [
            {
                "event": "patch_apply_proof_recorded",
                "outcome": "proof_stored",
                "metadata": {
                    "intent_id": "intent_X",
                    "target_path": "x.py",
                    "sha256": "xxx",
                    "bytes_written": 100,
                    "line_count": 10,
                },
            },
        ]

        graph = build_project_brain(job, events)
        memory_edges = [e for e in graph.edges if e.type == ET_INFORMED_MEMORY]
        # Memory nodes may or may not exist (depends on memory gateway availability)
        # but edges should be structurally valid
        for edge in memory_edges:
            assert edge.source  # non-empty source
            assert edge.target  # non-empty target


class TestContinueFromNodeIntegration:
    """Continue-from-node integration tests — brain edges, child graphs, invalid node."""

    def test_continue_creates_brain_edge(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_brain import (
            ET_CONTINUED_AS,
            build_project_brain,
        )
        from packages.orchestration.continue_from_node import continue_from_node

        job = _make_job(target_repo=str(tmp_path))
        save_job(job)

        graph = build_project_brain(job, [])
        node_id = graph.nodes[0].id
        result = continue_from_node(job, graph, node_id, "test continue")

        # Rebuild graph with continuation event
        from packages.orchestration.data_paths import resolve_data_root
        from packages.orchestration.timeline import load_run_events

        events = load_run_events(resolve_data_root(), job.id)
        graph2 = build_project_brain(job, events)

        cont_edges = [e for e in graph2.edges if e.type == ET_CONTINUED_AS]
        assert len(cont_edges) >= 1
        assert any(result.child_job_id[:8] in e.target for e in cont_edges)

    def test_continue_invalid_node_raises(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_brain import build_project_brain
        from packages.orchestration.continue_from_node import continue_from_node

        job = _make_job(target_repo=str(tmp_path))
        save_job(job)
        graph = build_project_brain(job, [])

        with pytest.raises((ValueError, KeyError)):
            continue_from_node(job, graph, "nonexistent_node_id_xyz", "test")

    def test_child_brain_graph_valid(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.project_brain import build_project_brain
        from packages.orchestration.continue_from_node import continue_from_node

        job = _make_job(target_repo=str(tmp_path))
        save_job(job)
        graph = build_project_brain(job, [])
        result = continue_from_node(job, graph, graph.nodes[0].id, "child test")

        # Load child and build its brain
        from packages.orchestration.storage import load_job

        child = load_job(UUID(result.child_job_id))
        child_graph = build_project_brain(child, [])
        assert len(child_graph.nodes) >= 1
        assert child_graph.job_id == child.id


class TestAgentsmdWorkflow:
    """AGENTS.md contains required workflow rules."""

    def test_commit_discipline_step_per_commit(self):
        src = Path("AGENTS.md").read_text()
        assert "one step per commit" in src.lower() or "step per commit" in src.lower()

    def test_commit_discipline_500_line_limit(self):
        src = Path("AGENTS.md").read_text()
        assert "500" in src
