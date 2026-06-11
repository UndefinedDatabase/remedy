"""Tests for run_contract.py — contract model, evaluate_run_action, path policy, budgets."""

from __future__ import annotations

import json

import pytest

from packages.orchestration.run_contract import (
    ALL_KNOWN_ACTIONS,
    ContractAction,
    RunActionDecision,
    RunBudgetStatus,
    RunContract,
    RunUsage,
    check_budget,
    evaluate_run_action,
    export_run_action_decision_json,
    export_run_contract_json,
    export_budget_status_json,
    export_usage_json,
    ensure_contract,
    load_contract,
    load_usage,
    migrate_contract,
    needs_contract_migration,
    save_contract,
    save_usage,
    summarize_run_contract,
    validate_run_contract,
)


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _contract(**overrides) -> RunContract:
    """Build a test contract with defaults."""
    defaults = dict(
        version=1,
        contract_id="rc-test",
        job_id="test-job-id",
        scope="job",
        autonomy_level=2,
        allowed_actions=("plan", "context", "build_artifact", "create_patch_intent", "write_metadata"),
        denied_actions=("apply", "source_apply", "arbitrary_shell", "cloud_provider"),
        max_loops=3,
        max_test_runs=2,
        max_runtime_seconds=300,
        allowed_paths=(),
        denied_paths=(".env", ".env.secret", ".git/"),
        stop_before_apply=True,
        stop_on_unknown_risk=True,
        stop_on_medium_risk=False,
        no_cloud=True,
        source="test",
    )
    defaults.update(overrides)
    return RunContract(**defaults)


# ---------------------------------------------------------------------------
# Step 1054: Approval gate regression
# ---------------------------------------------------------------------------


class TestApprovalGateRegression:
    def test_contract_blocks_apply_when_stop_before_apply(self):
        c = _contract(stop_before_apply=True)
        d = evaluate_run_action(c, "apply")
        assert not d.allowed
        assert d.status == "blocked"

    def test_contract_blocks_source_apply(self):
        c = _contract(stop_before_apply=True)
        d = evaluate_run_action(c, "source_apply")
        assert not d.allowed

    def test_do_run_does_not_import_source_apply(self):
        import inspect
        from packages.orchestration import do_run
        source = inspect.getsource(do_run)
        assert "from packages.orchestration.source_apply import" not in source
        assert "source_apply(" not in source

    def test_repair_loop_does_not_import_source_apply(self):
        import inspect
        from packages.orchestration import repair_loop
        source = inspect.getsource(repair_loop)
        assert "from packages.orchestration.source_apply import" not in source
        assert "source_apply(" not in source

    def test_no_fake_apply_phase(self):
        """do_run phases should not include a completed 'apply' phase."""
        from packages.orchestration.do_run import run_do
        import tempfile, os
        with tempfile.TemporaryDirectory() as tmp:
            result = run_do("test goal", tmp)
            for phase in result.phases:
                if phase.phase == "apply":
                    assert phase.status != "completed"


# ---------------------------------------------------------------------------
# Step 1055: Allowed action tests
# ---------------------------------------------------------------------------


class TestAllowedActions:
    def test_allowed_metadata_write_passes(self):
        c = _contract()
        d = evaluate_run_action(c, "write_metadata")
        assert d.allowed
        assert d.status == "allowed"

    def test_denied_action_blocks(self):
        c = _contract()
        d = evaluate_run_action(c, "arbitrary_shell")
        assert not d.allowed
        assert d.status == "blocked"

    def test_unknown_action_not_in_allowed_blocks(self):
        c = _contract(allowed_actions=("plan",))
        d = evaluate_run_action(c, "totally_unknown_action")
        assert not d.allowed
        assert d.status == "blocked"

    def test_no_cloud_blocks_cloud_provider(self):
        c = _contract(no_cloud=True)
        d = evaluate_run_action(c, "cloud_provider")
        assert not d.allowed

    def test_no_cloud_blocks_network_fetch(self):
        c = _contract(no_cloud=True)
        d = evaluate_run_action(c, "network_fetch")
        assert not d.allowed

    def test_create_patch_intent_allowed_when_configured(self):
        c = _contract(allowed_actions=("create_patch_intent",))
        d = evaluate_run_action(c, "create_patch_intent")
        assert d.allowed

    def test_create_patch_intent_blocked_when_not_configured(self):
        c = _contract(allowed_actions=("plan",))
        d = evaluate_run_action(c, "create_patch_intent")
        assert not d.allowed

    def test_run_test_blocked_when_max_test_runs_exhausted(self):
        c = _contract(allowed_actions=("run_test",), max_test_runs=2)
        d = evaluate_run_action(c, "run_test", test_run_count=2)
        assert not d.allowed
        assert d.status == "exhausted"


# ---------------------------------------------------------------------------
# Step 1056: Path policy tests
# ---------------------------------------------------------------------------


class TestPathPolicy:
    def test_safe_path_allowed(self):
        c = _contract(allowed_paths=("docs/",), denied_paths=(".env",))
        d = evaluate_run_action(c, "write_metadata", path="docs/README.md")
        assert d.allowed

    def test_env_secret_blocked(self):
        c = _contract()
        d = evaluate_run_action(c, "write_metadata", path=".env.secret")
        assert not d.allowed
        assert "denied path" in d.reason.lower()

    def test_traversal_blocked(self):
        c = _contract()
        d = evaluate_run_action(c, "write_metadata", path="../etc/passwd")
        assert not d.allowed
        assert "traversal" in d.reason.lower()

    def test_absolute_path_blocked(self):
        c = _contract()
        d = evaluate_run_action(c, "write_metadata", path="/etc/passwd")
        assert not d.allowed
        assert "absolute" in d.reason.lower()

    def test_denied_path_wins_over_allowed(self):
        c = _contract(allowed_paths=("secrets/",), denied_paths=("secrets/key.pem",))
        d = evaluate_run_action(c, "write_metadata", path="secrets/key.pem")
        assert not d.allowed

    def test_allowed_paths_empty_no_repo_write(self):
        """Empty allowed_paths means no path restriction (action-level check only)."""
        c = _contract(allowed_paths=(), denied_paths=())
        d = evaluate_run_action(c, "write_metadata", path="some/file.py")
        assert d.allowed

    def test_env_does_not_block_environment_py(self):
        """R-0021: .env denied path must not block .environment.py"""
        c = _contract(denied_paths=(".env",))
        d = evaluate_run_action(c, "write_metadata", path=".environment.py")
        assert d.allowed, f"Expected allowed, got: {d.reason}"

    def test_env_blocks_env_exactly(self):
        c = _contract(denied_paths=(".env",))
        d = evaluate_run_action(c, "write_metadata", path=".env")
        assert not d.allowed

    def test_env_blocks_env_subdirectory(self):
        c = _contract(denied_paths=(".env",))
        d = evaluate_run_action(c, "write_metadata", path=".env/foo")
        assert not d.allowed

    def test_node_modules_does_not_block_node_modules_backup(self):
        c = _contract(denied_paths=("node_modules/",))
        d = evaluate_run_action(c, "write_metadata", path="node_modules_backup/file.js")
        assert d.allowed


# ---------------------------------------------------------------------------
# Step 1057: Loop/test budget tests
# ---------------------------------------------------------------------------


class TestLoopTestBudget:
    def test_max_loops_zero_blocks(self):
        c = _contract(max_loops=0)
        d = evaluate_run_action(c, "plan", loop_index=0)
        assert not d.allowed
        assert d.status == "exhausted"

    def test_max_loops_one_allows_first(self):
        c = _contract(max_loops=1)
        d = evaluate_run_action(c, "plan", loop_index=0)
        assert d.allowed

    def test_max_loops_one_blocks_second(self):
        c = _contract(max_loops=1)
        d = evaluate_run_action(c, "plan", loop_index=1)
        assert not d.allowed

    def test_max_test_runs_zero_blocks_test(self):
        c = _contract(max_test_runs=0, allowed_actions=("run_test",))
        d = evaluate_run_action(c, "run_test", test_run_count=0)
        assert not d.allowed
        assert d.status == "exhausted"

    def test_budget_visible_in_json(self):
        c = _contract(max_loops=2, max_test_runs=5)
        exported = export_run_contract_json(c)
        assert exported["max_loops"] == 2
        assert exported["max_test_runs"] == 5

    def test_decision_json_has_status(self):
        c = _contract(max_loops=0)
        d = evaluate_run_action(c, "plan", loop_index=0)
        j = export_run_action_decision_json(d)
        assert j["status"] == "exhausted"
        assert j["allowed"] is False


# ---------------------------------------------------------------------------
# Risk policy tests
# ---------------------------------------------------------------------------


class TestRiskPolicy:
    def test_unknown_risk_blocks_when_configured(self):
        c = _contract(stop_on_unknown_risk=True)
        d = evaluate_run_action(c, "plan", risk="unknown")
        assert not d.allowed

    def test_medium_risk_passes_when_not_configured(self):
        c = _contract(stop_on_medium_risk=False)
        d = evaluate_run_action(c, "plan", risk="medium")
        assert d.allowed

    def test_medium_risk_blocks_when_configured(self):
        c = _contract(stop_on_medium_risk=True)
        d = evaluate_run_action(c, "plan", risk="medium")
        assert not d.allowed


# ---------------------------------------------------------------------------
# Export safety
# ---------------------------------------------------------------------------


class TestExportSafety:
    def test_contract_json_no_traceback(self):
        c = _contract()
        j = json.dumps(export_run_contract_json(c))
        assert "Traceback" not in j

    def test_contract_json_has_all_fields(self):
        c = _contract()
        j = export_run_contract_json(c)
        for key in ("version", "contract_id", "job_id", "allowed_actions",
                     "denied_actions", "max_loops", "max_test_runs",
                     "stop_before_apply", "no_cloud", "denied_paths"):
            assert key in j

    def test_summarize_includes_key_info(self):
        c = _contract()
        s = summarize_run_contract(c)
        assert "Run Contract" in s
        assert "Max loops" in s
        assert "Stop before apply" in s


# ---------------------------------------------------------------------------
# Step 1066: Contract persistence tests
# ---------------------------------------------------------------------------


def _make_job(**kwargs):
    """Create a minimal Job for testing."""
    from packages.core.models import Job
    defaults = dict(name="test-job")
    defaults.update(kwargs)
    return Job(**defaults)


class TestContractPersistence:
    def test_save_and_load_roundtrip(self):
        job = _make_job()
        c = _contract(job_id=str(job.id))
        save_contract(job, c)
        loaded = load_contract(job)
        assert loaded is not None
        assert loaded.contract_id == c.contract_id
        assert loaded.job_id == c.job_id
        assert loaded.allowed_actions == c.allowed_actions
        assert loaded.denied_actions == c.denied_actions
        assert loaded.denied_paths == c.denied_paths
        assert loaded.max_loops == c.max_loops
        assert loaded.max_test_runs == c.max_test_runs

    def test_load_returns_none_when_absent(self):
        job = _make_job()
        assert load_contract(job) is None

    def test_load_returns_none_for_non_dict(self):
        job = _make_job()
        job.metadata["run_contract"] = "not-a-dict"
        assert load_contract(job) is None

    def test_ensure_creates_contract_on_first_call(self):
        job = _make_job()
        c = ensure_contract(job)
        assert c.contract_id.startswith("rc-")
        assert c.job_id == str(job.id)
        assert c.source == "default_v1"

    def test_ensure_returns_same_contract_on_second_call(self):
        job = _make_job()
        c1 = ensure_contract(job)
        c2 = ensure_contract(job)
        assert c1.contract_id == c2.contract_id
        assert c1.created_at == c2.created_at

    def test_ensure_preserves_custom_contract(self):
        job = _make_job()
        custom = _contract(contract_id="custom-id", source="user_override")
        save_contract(job, custom)
        loaded = ensure_contract(job)
        assert loaded.contract_id == "custom-id"
        assert loaded.source == "user_override"

    def test_saved_contract_survives_json_roundtrip(self):
        """Contract survives Job JSON serialization (as in storage.py)."""
        job = _make_job()
        c = ensure_contract(job)
        # Simulate save_job / load_job roundtrip
        json_str = job.model_dump_json()
        from packages.core.models import Job
        restored = Job.model_validate_json(json_str)
        loaded = load_contract(restored)
        assert loaded is not None
        assert loaded.contract_id == c.contract_id
        assert loaded.created_at == c.created_at
        assert loaded.denied_paths == c.denied_paths


# ---------------------------------------------------------------------------
# Step 1067: Contract migration tests
# ---------------------------------------------------------------------------


class TestContractMigration:
    def test_old_job_needs_migration(self):
        job = _make_job()
        assert needs_contract_migration(job)

    def test_new_job_does_not_need_migration(self):
        job = _make_job()
        ensure_contract(job)
        assert not needs_contract_migration(job)

    def test_migrate_creates_contract(self):
        job = _make_job()
        c = migrate_contract(job)
        assert c.contract_id.startswith("rc-")
        assert not needs_contract_migration(job)

    def test_migrate_is_idempotent(self):
        job = _make_job()
        c1 = migrate_contract(job)
        c2 = migrate_contract(job)
        assert c1.contract_id == c2.contract_id
        assert c1.created_at == c2.created_at

    def test_migrate_preserves_existing_metadata(self):
        job = _make_job()
        job.metadata["some_other_key"] = "preserved"
        migrate_contract(job)
        assert job.metadata["some_other_key"] == "preserved"


# ---------------------------------------------------------------------------
# Step 1068: Canonical action vocabulary tests
# ---------------------------------------------------------------------------


class TestCanonicalActions:
    def test_all_known_actions_non_empty(self):
        assert len(ALL_KNOWN_ACTIONS) >= 16

    def test_contract_action_constants_are_strings(self):
        assert ContractAction.PLAN == "plan"
        assert ContractAction.APPLY == "apply"
        assert ContractAction.ARBITRARY_SHELL == "arbitrary_shell"

    def test_default_contract_uses_canonical_actions(self):
        job = _make_job()
        c = ensure_contract(job)
        for a in c.allowed_actions:
            assert a in ALL_KNOWN_ACTIONS, f"{a} not in ALL_KNOWN_ACTIONS"
        for a in c.denied_actions:
            assert a in ALL_KNOWN_ACTIONS, f"{a} not in ALL_KNOWN_ACTIONS"
        for a in c.requires_approval_for:
            assert a in ALL_KNOWN_ACTIONS, f"requires_approval_for {a!r} not canonical"

    def test_high_risk_command_execution_not_canonical(self):
        assert "high_risk_command_execution" not in ALL_KNOWN_ACTIONS

    def test_arbitrary_shell_is_canonical(self):
        assert ContractAction.ARBITRARY_SHELL in ALL_KNOWN_ACTIONS

    def test_default_requires_approval_canonical(self):
        from packages.orchestration.run_contract import _DEFAULT_REQUIRES_APPROVAL
        for a in _DEFAULT_REQUIRES_APPROVAL:
            assert a in ALL_KNOWN_ACTIONS, f"_DEFAULT_REQUIRES_APPROVAL {a!r} not canonical"


# ---------------------------------------------------------------------------
# Step 1069: Contract validation tests
# ---------------------------------------------------------------------------


class TestContractValidation:
    def test_valid_contract_no_errors(self):
        c = _contract()
        errors = validate_run_contract(c)
        assert errors == []

    def test_default_contract_valid(self):
        job = _make_job()
        c = ensure_contract(job)
        errors = validate_run_contract(c)
        assert errors == []

    def test_negative_max_loops_error(self):
        c = _contract(max_loops=-1)
        errors = validate_run_contract(c)
        assert any("max_loops" in e for e in errors)

    def test_empty_contract_id_error(self):
        c = _contract(contract_id="")
        errors = validate_run_contract(c)
        assert any("contract_id" in e for e in errors)

    def test_overlap_allowed_denied_error(self):
        c = _contract(
            allowed_actions=("plan", "apply"),
            denied_actions=("apply",),
        )
        errors = validate_run_contract(c)
        assert any("both allowed and denied" in e for e in errors)

    def test_absolute_denied_path_error(self):
        c = _contract(denied_paths=("/etc/passwd",))
        errors = validate_run_contract(c)
        assert any("absolute path" in e for e in errors)

    def test_unknown_action_is_error(self):
        c = _contract(allowed_actions=("totally_made_up_action",), denied_actions=())
        errors = validate_run_contract(c)
        assert any("unknown actions" in e for e in errors)

    def test_unknown_requires_approval_action_is_error(self):
        c = _contract(requires_approval_for=("high_risk_command_execution",))
        errors = validate_run_contract(c)
        assert any("unknown actions" in e for e in errors)

    def test_default_contract_validates_zero_errors(self):
        from packages.orchestration.run_contract import build_default_run_contract
        job = _make_job()
        c = build_default_run_contract(job)
        errors = validate_run_contract(c)
        assert errors == [], f"default contract has errors: {errors}"


# ---------------------------------------------------------------------------
# Step 1087: Default test policy tests
# ---------------------------------------------------------------------------


class TestDefaultTestPolicy:
    def test_run_test_in_default_allowed_actions(self):
        job = _make_job()
        c = ensure_contract(job)
        assert ContractAction.RUN_TEST in c.allowed_actions

    def test_max_test_runs_zero_by_default(self):
        job = _make_job()
        c = ensure_contract(job)
        assert c.max_test_runs == 0

    def test_run_test_blocked_by_zero_budget(self):
        job = _make_job()
        c = ensure_contract(job)
        d = evaluate_run_action(c, ContractAction.RUN_TEST)
        assert not d.allowed
        assert d.status == "exhausted"
        assert "max_test_runs" in d.reason

    def test_permission_alone_insufficient(self):
        # Even with max_test_runs=1, contract gate is separate from permission
        c = _contract(allowed_actions=(ContractAction.RUN_TEST,), max_test_runs=0)
        d = evaluate_run_action(c, ContractAction.RUN_TEST)
        assert not d.allowed

    def test_contract_budget_alone_insufficient_to_block_without_permission(self):
        # With max_test_runs>0, contract gate allows — but permission gate is external
        c = _contract(allowed_actions=(ContractAction.RUN_TEST,), max_test_runs=2)
        usage = RunUsage(test_runs_used=0)
        d = evaluate_run_action(c, ContractAction.RUN_TEST, usage=usage)
        assert d.allowed  # contract budget gate passes; permission is external

    def test_both_gates_set_allows_contract_level(self):
        c = _contract(allowed_actions=(ContractAction.RUN_TEST,), max_test_runs=3)
        usage = RunUsage(test_runs_used=1)
        d = evaluate_run_action(c, ContractAction.RUN_TEST, usage=usage)
        assert d.allowed

    def test_exhausted_budget_blocks_run_test(self):
        c = _contract(allowed_actions=(ContractAction.RUN_TEST,), max_test_runs=1)
        usage = RunUsage(test_runs_used=1)
        d = evaluate_run_action(c, ContractAction.RUN_TEST, usage=usage)
        assert not d.allowed
        assert d.status == "exhausted"


# ---------------------------------------------------------------------------
# Step 1075: Usage ledger tests
# ---------------------------------------------------------------------------


class TestUsageLedger:
    def test_default_usage_is_zero(self):
        u = RunUsage()
        assert u.loops_used == 0
        assert u.test_runs_used == 0
        assert u.runtime_seconds_used == 0.0

    def test_save_and_load_usage(self):
        job = _make_job()
        u = RunUsage(loops_used=3, test_runs_used=1, runtime_seconds_used=42.5)
        save_usage(job, u)
        loaded = load_usage(job)
        assert loaded.loops_used == 3
        assert loaded.test_runs_used == 1
        assert loaded.runtime_seconds_used == 42.5

    def test_load_usage_absent_returns_zero(self):
        job = _make_job()
        u = load_usage(job)
        assert u.loops_used == 0

    def test_usage_survives_json_roundtrip(self):
        job = _make_job()
        u = RunUsage(loops_used=5, tokens_used=1000)
        save_usage(job, u)
        json_str = job.model_dump_json()
        from packages.core.models import Job
        restored = Job.model_validate_json(json_str)
        loaded = load_usage(restored)
        assert loaded.loops_used == 5
        assert loaded.tokens_used == 1000

    def test_export_usage_json(self):
        u = RunUsage(loops_used=2, cost_cents_used=3.5)
        d = export_usage_json(u)
        assert d["loops_used"] == 2
        assert d["cost_cents_used"] == 3.5


# ---------------------------------------------------------------------------
# Step 1076: Budget enforcement tests
# ---------------------------------------------------------------------------


class TestBudgetEnforcement:
    def test_within_budget(self):
        c = _contract(max_loops=10, max_test_runs=5)
        u = RunUsage(loops_used=3, test_runs_used=2)
        status = check_budget(c, u)
        assert status.within_budget
        assert status.remaining["loops"] == 7
        assert status.remaining["test_runs"] == 3

    def test_loops_exhausted(self):
        c = _contract(max_loops=3)
        u = RunUsage(loops_used=3)
        status = check_budget(c, u)
        assert not status.within_budget
        assert "max_loops" in status.exhausted_budgets

    def test_runtime_exhausted(self):
        c = _contract(max_loops=10)
        c2 = RunContract(**{**{f: getattr(c, f) for f in ["version", "contract_id", "job_id", "scope",
            "autonomy_level", "allowed_actions", "denied_actions", "max_loops", "max_test_runs",
            "max_runtime_seconds", "max_tokens", "max_cost_cents", "allowed_paths", "denied_paths",
            "stop_before_apply", "stop_on_unknown_risk", "stop_on_medium_risk", "prefer_local",
            "no_cloud", "model_policy", "command_policy", "stop_conditions", "requires_approval_for",
            "source", "created_at", "notes"]}, "max_runtime_seconds": 60})
        u = RunUsage(runtime_seconds_used=61.0)
        status = check_budget(c2, u)
        assert not status.within_budget
        assert "max_runtime_seconds" in status.exhausted_budgets

    def test_evaluate_with_usage_blocks(self):
        c = _contract(max_loops=3)
        u = RunUsage(loops_used=3)
        d = evaluate_run_action(c, "plan", usage=u)
        assert not d.allowed
        assert d.status == "exhausted"

    def test_evaluate_with_usage_allows(self):
        c = _contract(max_loops=3)
        u = RunUsage(loops_used=2)
        d = evaluate_run_action(c, "plan", usage=u)
        assert d.allowed

    def test_export_budget_status(self):
        status = RunBudgetStatus(within_budget=False, exhausted_budgets=("max_loops",), remaining={"loops": 0})
        d = export_budget_status_json(status)
        assert d["within_budget"] is False
        assert "max_loops" in d["exhausted_budgets"]
