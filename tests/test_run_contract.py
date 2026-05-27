"""
Tests for Step 35 — Run Contract v0.

Coverage:
  - RunContract dataclass is frozen and JSON-serializable
  - build_default_run_contract produces valid contract from a Job
  - export_run_contract_json returns dict with all required keys
  - summarize_run_contract returns non-empty string
  - Default contract has correct field values
  - No network, no subprocess, no shell in module
"""

from __future__ import annotations

from uuid import uuid4

import pytest

from packages.core.models import Job, Task
from packages.orchestration.run_contract import (
    RunContract,
    build_default_run_contract,
    export_run_contract_json,
    summarize_run_contract,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_job(*, task_count: int = 0) -> Job:
    tasks = [
        Task(id=uuid4(), description=f"task-{i}")
        for i in range(task_count)
    ]
    return Job(
        id=uuid4(),
        name="test-job",
        user_prompt="test prompt",
        tasks=tasks,
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestRunContractDataclass:
    def test_frozen(self) -> None:
        contract = build_default_run_contract(_make_job())
        with pytest.raises(AttributeError):
            contract.version = 99  # type: ignore[misc]

    def test_all_fields_present(self) -> None:
        contract = build_default_run_contract(_make_job())
        assert hasattr(contract, "version")
        assert hasattr(contract, "scope")
        assert hasattr(contract, "autonomy_level")
        assert hasattr(contract, "allowed_actions")
        assert hasattr(contract, "denied_actions")
        assert hasattr(contract, "max_loops")
        assert hasattr(contract, "max_tokens")
        assert hasattr(contract, "max_cost_cents")
        assert hasattr(contract, "model_policy")
        assert hasattr(contract, "command_policy")
        assert hasattr(contract, "stop_conditions")
        assert hasattr(contract, "requires_approval_for")
        assert hasattr(contract, "source")
        assert hasattr(contract, "notes")


class TestBuildDefaultRunContract:
    def test_returns_run_contract(self) -> None:
        contract = build_default_run_contract(_make_job())
        assert isinstance(contract, RunContract)

    def test_version_is_1(self) -> None:
        contract = build_default_run_contract(_make_job())
        assert contract.version == 1

    def test_autonomy_level_is_int(self) -> None:
        contract = build_default_run_contract(_make_job())
        assert isinstance(contract.autonomy_level, int)
        assert contract.autonomy_level == 1

    def test_scope_is_job(self) -> None:
        contract = build_default_run_contract(_make_job())
        assert contract.scope == "job"

    def test_job_id_matches(self) -> None:
        job = _make_job()
        contract = build_default_run_contract(job)
        assert contract.job_id == str(job.id)

    def test_allowed_actions_non_empty(self) -> None:
        contract = build_default_run_contract(_make_job())
        assert len(contract.allowed_actions) > 0
        assert all(isinstance(a, str) for a in contract.allowed_actions)

    def test_denied_actions_non_empty(self) -> None:
        contract = build_default_run_contract(_make_job())
        assert len(contract.denied_actions) > 0

    def test_no_overlap_allowed_denied(self) -> None:
        contract = build_default_run_contract(_make_job())
        allowed_set = set(contract.allowed_actions)
        denied_set = set(contract.denied_actions)
        assert allowed_set.isdisjoint(denied_set)

    def test_model_policy_local_first(self) -> None:
        contract = build_default_run_contract(_make_job())
        assert contract.model_policy == "local_first"

    def test_command_policy_allowlist(self) -> None:
        contract = build_default_run_contract(_make_job())
        assert contract.command_policy == "allowlist_only"

    def test_stop_conditions_non_empty(self) -> None:
        contract = build_default_run_contract(_make_job())
        assert len(contract.stop_conditions) > 0

    def test_requires_approval_non_empty(self) -> None:
        contract = build_default_run_contract(_make_job())
        assert len(contract.requires_approval_for) > 0

    def test_source_is_default(self) -> None:
        contract = build_default_run_contract(_make_job())
        assert contract.source == "default_v1"


class TestExportRunContractJson:
    def test_returns_dict(self) -> None:
        contract = build_default_run_contract(_make_job())
        result = export_run_contract_json(contract)
        assert isinstance(result, dict)

    def test_required_keys(self) -> None:
        contract = build_default_run_contract(_make_job())
        result = export_run_contract_json(contract)
        required = {
            "version", "job_id", "scope", "autonomy_level", "allowed_actions",
            "denied_actions", "max_loops", "max_tokens", "max_cost_cents",
            "model_policy", "command_policy", "stop_conditions",
            "requires_approval_for", "source", "notes",
        }
        assert required.issubset(set(result.keys()))

    def test_json_serializable(self) -> None:
        import json
        contract = build_default_run_contract(_make_job())
        result = export_run_contract_json(contract)
        serialized = json.dumps(result)
        assert isinstance(serialized, str)

    def test_lists_not_tuples(self) -> None:
        contract = build_default_run_contract(_make_job())
        result = export_run_contract_json(contract)
        assert isinstance(result["allowed_actions"], list)
        assert isinstance(result["denied_actions"], list)
        assert isinstance(result["stop_conditions"], list)
        assert isinstance(result["requires_approval_for"], list)


class TestSummarizeRunContract:
    def test_returns_string(self) -> None:
        contract = build_default_run_contract(_make_job())
        summary = summarize_run_contract(contract)
        assert isinstance(summary, str)
        assert len(summary) > 50

    def test_contains_key_fields(self) -> None:
        contract = build_default_run_contract(_make_job())
        summary = summarize_run_contract(contract)
        assert "Run Contract" in summary
        assert "local_first" in summary
        assert "allowlist_only" in summary


class TestRunContractNoSubprocess:
    """Verify the module makes no network or subprocess calls."""

    def test_no_subprocess_import(self) -> None:
        import packages.orchestration.run_contract as mod
        source = open(mod.__file__).read()
        assert "subprocess" not in source
        assert "os.system" not in source
        assert "shell=True" not in source

    def test_no_network_import(self) -> None:
        import packages.orchestration.run_contract as mod
        source = open(mod.__file__).read()
        assert "import urllib" not in source
        assert "import requests" not in source
        assert "import httpx" not in source
