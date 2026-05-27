"""
Tests for Step 36 — Token Economy v0.

Coverage:
  - TokenPolicy dataclass is frozen and JSON-serializable
  - build_default_token_policy produces valid policy from a Job
  - export_token_policy_json returns dict with all required keys
  - summarize_token_policy returns non-empty string
  - Zero-token steps are deterministic operations
  - No network, no subprocess, no shell in module
"""

from __future__ import annotations

from uuid import uuid4

import pytest

from packages.core.models import Job, Task
from packages.orchestration.token_policy import (
    TokenPolicy,
    build_default_token_policy,
    export_token_policy_json,
    summarize_token_policy,
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


class TestTokenPolicyDataclass:
    def test_frozen(self) -> None:
        policy = build_default_token_policy(_make_job())
        with pytest.raises(AttributeError):
            policy.version = 99  # type: ignore[misc]

    def test_all_fields_present(self) -> None:
        policy = build_default_token_policy(_make_job())
        for field_name in (
            "version", "job_id", "scope", "zero_token_steps",
            "local_first_steps", "expensive_model_steps",
            "forbidden_context", "compaction_rules", "budget",
            "future_layers",
        ):
            assert hasattr(policy, field_name)


class TestBuildDefaultTokenPolicy:
    def test_returns_token_policy(self) -> None:
        policy = build_default_token_policy(_make_job())
        assert isinstance(policy, TokenPolicy)

    def test_version_is_1(self) -> None:
        policy = build_default_token_policy(_make_job())
        assert policy.version == 1

    def test_job_id_matches(self) -> None:
        job = _make_job()
        policy = build_default_token_policy(job)
        assert policy.job_id == str(job.id)

    def test_scope_contains_job_id(self) -> None:
        job = _make_job()
        policy = build_default_token_policy(job)
        assert str(job.id)[:8] in policy.scope

    def test_zero_token_steps_are_deterministic_ops(self) -> None:
        policy = build_default_token_policy(_make_job())
        assert len(policy.zero_token_steps) > 0
        for step in policy.zero_token_steps:
            assert isinstance(step, str)

    def test_command_discovery_is_zero_token(self) -> None:
        policy = build_default_token_policy(_make_job())
        assert "command_discovery" in policy.zero_token_steps

    def test_run_contract_inspection_is_zero_token(self) -> None:
        policy = build_default_token_policy(_make_job())
        assert "run_contract_inspection" in policy.zero_token_steps

    def test_token_policy_inspection_is_zero_token(self) -> None:
        policy = build_default_token_policy(_make_job())
        assert "token_policy_inspection" in policy.zero_token_steps

    def test_local_first_steps_non_empty(self) -> None:
        policy = build_default_token_policy(_make_job())
        assert len(policy.local_first_steps) > 0

    def test_expensive_steps_non_empty(self) -> None:
        policy = build_default_token_policy(_make_job())
        assert len(policy.expensive_model_steps) > 0

    def test_forbidden_context_non_empty(self) -> None:
        policy = build_default_token_policy(_make_job())
        assert len(policy.forbidden_context) > 0

    def test_budget_has_expected_keys(self) -> None:
        policy = build_default_token_policy(_make_job())
        assert "local_tokens" in policy.budget
        assert "expensive_tokens" in policy.budget

    def test_budget_scales_with_tasks(self) -> None:
        small = build_default_token_policy(_make_job(task_count=1))
        large = build_default_token_policy(_make_job(task_count=5))
        assert large.budget["expensive_tokens"] >= small.budget["expensive_tokens"]

    def test_no_overlap_zero_and_expensive(self) -> None:
        policy = build_default_token_policy(_make_job())
        zero_set = set(policy.zero_token_steps)
        expensive_set = set(policy.expensive_model_steps)
        assert zero_set.isdisjoint(expensive_set)


class TestExportTokenPolicyJson:
    def test_returns_dict(self) -> None:
        policy = build_default_token_policy(_make_job())
        result = export_token_policy_json(policy)
        assert isinstance(result, dict)

    def test_required_keys(self) -> None:
        policy = build_default_token_policy(_make_job())
        result = export_token_policy_json(policy)
        required = {
            "version", "job_id", "scope", "zero_token_steps",
            "local_first_steps", "expensive_model_steps",
            "forbidden_context", "compaction_rules", "budget",
            "future_layers",
        }
        assert required.issubset(set(result.keys()))

    def test_json_serializable(self) -> None:
        import json
        policy = build_default_token_policy(_make_job())
        result = export_token_policy_json(policy)
        serialized = json.dumps(result)
        assert isinstance(serialized, str)

    def test_lists_not_tuples(self) -> None:
        policy = build_default_token_policy(_make_job())
        result = export_token_policy_json(policy)
        assert isinstance(result["zero_token_steps"], list)
        assert isinstance(result["local_first_steps"], list)
        assert isinstance(result["expensive_model_steps"], list)


class TestSummarizeTokenPolicy:
    def test_returns_string(self) -> None:
        policy = build_default_token_policy(_make_job())
        summary = summarize_token_policy(policy)
        assert isinstance(summary, str)
        assert len(summary) > 50

    def test_contains_key_fields(self) -> None:
        policy = build_default_token_policy(_make_job())
        summary = summarize_token_policy(policy)
        assert "Token Policy" in summary
        assert "Zero-token" in summary
        assert "Local-first" in summary
        assert "Expensive" in summary


class TestTokenPolicyNoSubprocess:
    def test_no_subprocess_import(self) -> None:
        import packages.orchestration.token_policy as mod
        source = open(mod.__file__).read()
        assert "subprocess" not in source
        assert "os.system" not in source
        assert "shell=True" not in source

    def test_no_network_import(self) -> None:
        import packages.orchestration.token_policy as mod
        source = open(mod.__file__).read()
        assert "urllib" not in source
        assert "requests" not in source
        assert "httpx" not in source
