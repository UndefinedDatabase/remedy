"""Tests for run_contract.py — contract model, evaluate_run_action, path policy, budgets."""

from __future__ import annotations

import json

import pytest

from packages.orchestration.run_contract import (
    RunActionDecision,
    RunContract,
    evaluate_run_action,
    export_run_action_decision_json,
    export_run_contract_json,
    ensure_contract,
    load_contract,
    save_contract,
    summarize_run_contract,
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
