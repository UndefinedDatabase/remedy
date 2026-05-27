"""
Integration tests for Steps 35-37 — Execution Foundation.

Coverage:
  - Brain graph includes run_contract, token_policy, worker_adapter nodes
  - Brain detail builders work for new node types
  - Protocol interfaces exist and are runtime-checkable
  - R-0001 fix: execution safety guard uses raise, not assert
  - Run-log event metadata schemas
  - CLI command output (run-contract, token-policy, workers)
  - Brain node metadata alignment with run-log schemas
  - Docs drift detection
"""

from __future__ import annotations

import json
import re
import sys
from io import StringIO
from pathlib import Path
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


# ---------------------------------------------------------------------------
# Brain node metadata alignment tests
# ---------------------------------------------------------------------------


class TestBrainNodeMetadataAlignment:
    """Brain node metadata must match run-log event metadata schemas."""

    def test_run_contract_node_metadata_keys(self, tmp_path) -> None:
        job = _make_job()
        save_job(job)
        graph = build_project_brain(job, [])
        rc = [n for n in graph.nodes if n.type == NT_RUN_CONTRACT][0]
        expected = {"autonomy_level", "allowed_action_count", "denied_action_count", "max_loops", "scope"}
        assert set(rc.metadata.keys()) == expected

    def test_token_policy_node_metadata_keys(self, tmp_path) -> None:
        job = _make_job()
        save_job(job)
        graph = build_project_brain(job, [])
        tp = [n for n in graph.nodes if n.type == NT_TOKEN_POLICY][0]
        expected = {"scope", "zero_token_step_count", "local_first_step_count", "expensive_step_count"}
        assert set(tp.metadata.keys()) == expected

    def test_worker_adapter_node_metadata_scalar(self, tmp_path) -> None:
        job = _make_job()
        save_job(job)
        graph = build_project_brain(job, [])
        wa = [n for n in graph.nodes if n.type == NT_WORKER_ADAPTER][0]
        assert "supported_role_count" in wa.metadata
        assert isinstance(wa.metadata["supported_role_count"], int)
        assert "supported_roles" not in wa.metadata  # list form removed

    def test_run_contract_metadata_values(self, tmp_path) -> None:
        job = _make_job()
        save_job(job)
        graph = build_project_brain(job, [])
        rc = [n for n in graph.nodes if n.type == NT_RUN_CONTRACT][0]
        assert rc.metadata["autonomy_level"] == 1
        assert rc.metadata["scope"] == "job"
        assert isinstance(rc.metadata["allowed_action_count"], int)
        assert isinstance(rc.metadata["max_loops"], int)

    def test_token_policy_metadata_values(self, tmp_path) -> None:
        job = _make_job()
        save_job(job)
        graph = build_project_brain(job, [])
        tp = [n for n in graph.nodes if n.type == NT_TOKEN_POLICY][0]
        assert tp.metadata["scope"] == "job"
        assert tp.metadata["zero_token_step_count"] > 0
        assert isinstance(tp.metadata["local_first_step_count"], int)


# ---------------------------------------------------------------------------
# CLI command output tests (monkeypatch)
# ---------------------------------------------------------------------------


class TestCLIRunContract:
    def test_json_output_is_pure_json(self, tmp_path, monkeypatch, capsys) -> None:
        job = _make_job()
        save_job(job)
        monkeypatch.setattr(sys, "argv", [
            "remedy", "run-contract", str(job.id), "--json",
        ])
        from apps.cli.main import main
        with pytest.raises(SystemExit, match="0|None") if False else _no_exit(monkeypatch):
            main()
        out = capsys.readouterr().out.strip()
        data = json.loads(out)
        assert isinstance(data, dict)
        for key in ("autonomy_level", "scope", "version", "job_id", "allowed_actions", "denied_actions"):
            assert key in data, f"missing key: {key}"
        assert isinstance(data["autonomy_level"], int)
        assert data["scope"] == "job"

    def test_json_has_no_secret_leaks(self, tmp_path, monkeypatch, capsys) -> None:
        job = _make_job()
        save_job(job)
        monkeypatch.setattr(sys, "argv", [
            "remedy", "run-contract", str(job.id), "--json",
        ])
        from apps.cli.main import main
        with _no_exit(monkeypatch):
            main()
        raw = capsys.readouterr().out.lower()
        for bad in ("sk-", "ghp_", "password=", "begin private key"):
            assert bad not in raw, f"run-contract JSON leaks: {bad}"


class TestCLITokenPolicy:
    def test_json_output_is_pure_json(self, tmp_path, monkeypatch, capsys) -> None:
        job = _make_job()
        save_job(job)
        monkeypatch.setattr(sys, "argv", [
            "remedy", "token-policy", str(job.id), "--json",
        ])
        from apps.cli.main import main
        with _no_exit(monkeypatch):
            main()
        out = capsys.readouterr().out.strip()
        data = json.loads(out)
        for key in ("scope", "version", "zero_token_steps", "forbidden_context", "budget"):
            assert key in data, f"missing key: {key}"
        assert data["scope"] == "job"

    def test_json_has_no_secret_leaks(self, tmp_path, monkeypatch, capsys) -> None:
        job = _make_job()
        save_job(job)
        monkeypatch.setattr(sys, "argv", [
            "remedy", "token-policy", str(job.id), "--json",
        ])
        from apps.cli.main import main
        with _no_exit(monkeypatch):
            main()
        raw = capsys.readouterr().out.lower()
        for bad in ("sk-", "ghp_", "password=", "begin private key"):
            assert bad not in raw, f"token-policy JSON leaks: {bad}"

    def test_category_names_allowed_in_output(self, tmp_path, monkeypatch, capsys) -> None:
        """Category names like 'api_keys' are expected in forbidden_context — not leaks."""
        job = _make_job()
        save_job(job)
        monkeypatch.setattr(sys, "argv", [
            "remedy", "token-policy", str(job.id), "--json",
        ])
        from apps.cli.main import main
        with _no_exit(monkeypatch):
            main()
        data = json.loads(capsys.readouterr().out)
        fc = data["forbidden_context"]
        assert "api_keys" in fc
        assert "environment_secrets" in fc


class TestCLIWorkers:
    def test_json_output_is_pure_json(self, tmp_path, monkeypatch, capsys) -> None:
        monkeypatch.setattr(sys, "argv", ["remedy", "workers", "--json"])
        from apps.cli.main import main
        with _no_exit(monkeypatch):
            main()
        out = capsys.readouterr().out.strip()
        data = json.loads(out)
        assert isinstance(data, dict)
        assert data["version"] == 1
        assert isinstance(data["providers"], list)
        assert len(data["providers"]) >= 5

    def test_json_has_no_secret_leaks(self, tmp_path, monkeypatch, capsys) -> None:
        monkeypatch.setattr(sys, "argv", ["remedy", "workers", "--json"])
        from apps.cli.main import main
        with _no_exit(monkeypatch):
            main()
        raw = capsys.readouterr().out.lower()
        for bad in ("sk-", "ghp_", "password=", "begin private key"):
            assert bad not in raw, f"workers JSON leaks: {bad}"


class _no_exit:
    """Context manager that catches SystemExit(0) from argparse/CLI."""

    def __init__(self, monkeypatch):
        self._mp = monkeypatch

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is SystemExit and (exc_val.code is None or exc_val.code == 0):
            return True
        return False


# ---------------------------------------------------------------------------
# Docs drift-detection tests
# ---------------------------------------------------------------------------


_ARCH_DOC = Path(__file__).resolve().parent.parent / "docs" / "architecture.md"


class TestDocsDriftDetection:
    """Detect drift between docs/architecture.md and actual code values."""

    def test_run_contract_scope_matches_code(self) -> None:
        from packages.orchestration.run_contract import build_default_run_contract
        job = _make_job()
        rc = build_default_run_contract(job)
        doc = _ARCH_DOC.read_text()
        assert f"| scope" in doc
        assert '`job`' in doc, "docs must document scope = job"
        assert rc.scope == "job"

    def test_run_contract_autonomy_level_matches_code(self) -> None:
        from packages.orchestration.run_contract import build_default_run_contract
        job = _make_job()
        rc = build_default_run_contract(job)
        doc = _ARCH_DOC.read_text()
        assert "| autonomy_level" in doc
        assert "int" in doc.split("autonomy_level")[1][:50], "docs must say autonomy_level is int"
        assert isinstance(rc.autonomy_level, int)

    def test_run_contract_has_job_id_in_docs(self) -> None:
        doc = _ARCH_DOC.read_text()
        assert "| job_id" in doc, "docs must document job_id field"

    def test_run_log_rc_metadata_matches_code(self) -> None:
        doc = _ARCH_DOC.read_text()
        # Docs must list the actual run-log metadata keys
        for key in ("autonomy_level", "allowed_action_count", "denied_action_count", "max_loops", "scope"):
            assert key in doc, f"architecture.md missing run_contract_inspected key: {key}"
        # Must NOT list stale keys
        rc_section = doc[doc.index("run_contract_inspected"):doc.index("run_contract_inspected") + 200]
        assert "model_policy" not in rc_section, "stale model_policy in run_contract_inspected docs"
        assert "command_policy" not in rc_section, "stale command_policy in run_contract_inspected docs"

    def test_run_log_tp_metadata_matches_code(self) -> None:
        doc = _ARCH_DOC.read_text()
        for key in ("zero_token_step_count", "local_first_step_count", "expensive_step_count"):
            assert key in doc, f"architecture.md missing token_policy_inspected key: {key}"
        tp_section = doc[doc.index("token_policy_inspected"):doc.index("token_policy_inspected") + 200]
        assert "version" not in tp_section.split(",")[0] or "version" not in tp_section[:30], \
            "token_policy_inspected docs should not lead with stale 'version' key"
