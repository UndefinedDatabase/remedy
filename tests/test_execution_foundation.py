"""
Integration tests for Steps 35-37 — Execution Foundation.

Coverage:
  - Brain graph includes run_contract, token_policy, worker_adapter nodes
  - Brain detail builders work for new node types
  - Protocol interfaces exist and are runtime-checkable
  - R-0001 fix: execution safety guard uses raise, not assert
  - Run-log event metadata schemas
"""

from __future__ import annotations

from uuid import uuid4

import pytest

from packages.core.models import Job, Task
from packages.orchestration.project_brain import (
    ET_HAS_RUN_CONTRACT,
    ET_HAS_TOKEN_POLICY,
    ET_HAS_WORKER_ADAPTER,
    NT_RUN_CONTRACT,
    NT_TOKEN_POLICY,
    NT_WORKER_ADAPTER,
    build_project_brain,
)
from packages.orchestration.brain_detail import (
    build_brain_node_detail,
)
from packages.orchestration.storage import save_job


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_job() -> Job:
    return Job(
        id=uuid4(),
        name="test-job",
        user_prompt="test prompt",
        tasks=[Task(id=uuid4(), description="task-0")],
    )


# ---------------------------------------------------------------------------
# Brain graph integration
# ---------------------------------------------------------------------------


class TestBrainGraphNewNodes:
    def test_graph_has_run_contract_node(self, tmp_path) -> None:
        job = _make_job()
        save_job(job)
        graph = build_project_brain(job, [])
        rc_nodes = [n for n in graph.nodes if n.type == NT_RUN_CONTRACT]
        assert len(rc_nodes) == 1
        assert rc_nodes[0].status == "active"

    def test_graph_has_token_policy_node(self, tmp_path) -> None:
        job = _make_job()
        save_job(job)
        graph = build_project_brain(job, [])
        tp_nodes = [n for n in graph.nodes if n.type == NT_TOKEN_POLICY]
        assert len(tp_nodes) == 1
        assert tp_nodes[0].status == "active"

    def test_graph_has_worker_adapter_nodes(self, tmp_path) -> None:
        job = _make_job()
        save_job(job)
        graph = build_project_brain(job, [])
        wa_nodes = [n for n in graph.nodes if n.type == NT_WORKER_ADAPTER]
        assert len(wa_nodes) >= 5

    def test_run_contract_edge_exists(self, tmp_path) -> None:
        job = _make_job()
        save_job(job)
        graph = build_project_brain(job, [])
        rc_edges = [e for e in graph.edges if e.type == ET_HAS_RUN_CONTRACT]
        assert len(rc_edges) == 1

    def test_token_policy_edge_exists(self, tmp_path) -> None:
        job = _make_job()
        save_job(job)
        graph = build_project_brain(job, [])
        tp_edges = [e for e in graph.edges if e.type == ET_HAS_TOKEN_POLICY]
        assert len(tp_edges) == 1

    def test_worker_adapter_edges_exist(self, tmp_path) -> None:
        job = _make_job()
        save_job(job)
        graph = build_project_brain(job, [])
        wa_edges = [e for e in graph.edges if e.type == ET_HAS_WORKER_ADAPTER]
        assert len(wa_edges) >= 5


class TestBrainDetailNewTypes:
    def test_run_contract_detail(self, tmp_path) -> None:
        job = _make_job()
        save_job(job)
        graph = build_project_brain(job, [])
        detail = build_brain_node_detail(job, graph, "run_contract", [])
        assert detail.node_type == NT_RUN_CONTRACT
        assert "execution boundary" in detail.explanation.lower()

    def test_token_policy_detail(self, tmp_path) -> None:
        job = _make_job()
        save_job(job)
        graph = build_project_brain(job, [])
        detail = build_brain_node_detail(job, graph, "token_policy", [])
        assert detail.node_type == NT_TOKEN_POLICY
        assert "token" in detail.explanation.lower()

    def test_worker_adapter_detail(self, tmp_path) -> None:
        job = _make_job()
        save_job(job)
        graph = build_project_brain(job, [])
        detail = build_brain_node_detail(job, graph, "worker_adapter:ollama", [])
        assert detail.node_type == NT_WORKER_ADAPTER
        assert "ollama" in detail.explanation.lower()


# ---------------------------------------------------------------------------
# Protocol interface tests
# ---------------------------------------------------------------------------


class TestProtocolInterfaces:
    def test_run_contract_provider_exists(self) -> None:
        from packages.contracts.interfaces import RunContractProvider
        assert hasattr(RunContractProvider, "build")

    def test_token_policy_provider_exists(self) -> None:
        from packages.contracts.interfaces import TokenPolicyProvider
        assert hasattr(TokenPolicyProvider, "build")

    def test_run_contract_provider_is_runtime_checkable(self) -> None:
        from packages.contracts.interfaces import RunContractProvider

        class FakeProvider:
            def build(self, job: Job) -> dict:
                return {}

        assert isinstance(FakeProvider(), RunContractProvider)

    def test_token_policy_provider_is_runtime_checkable(self) -> None:
        from packages.contracts.interfaces import TokenPolicyProvider

        class FakeProvider:
            def build(self, job: Job) -> dict:
                return {}

        assert isinstance(FakeProvider(), TokenPolicyProvider)


# ---------------------------------------------------------------------------
# R-0001: Execution safety guard uses raise, not assert
# ---------------------------------------------------------------------------


class TestExecutionSafetyGuardRaise:
    def test_no_assert_in_safety_guard(self) -> None:
        import packages.orchestration.test_runner as mod
        source = open(mod.__file__).read()
        # Find the execution safety guard section
        guard_start = source.find("Execution safety guard")
        guard_end = source.find("Prepare output file")
        assert guard_start > 0
        assert guard_end > guard_start
        guard_section = source[guard_start:guard_end]
        assert "assert " not in guard_section
        assert "raise RuntimeError" in guard_section
