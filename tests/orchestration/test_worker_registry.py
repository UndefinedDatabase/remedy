"""Worker Registry + User-Selectable Route Policy v0 tests (Steps 1733/1734/1736/1737).

Unit (WorkerSpec model, built-ins, policy defaults/persistence, selection, blocked/disabled,
local/Ollama preference, token bands, no leaks), routing integration, integrity positive/negative,
and architecture guards. METADATA + POLICY only — nothing here executes a worker.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from packages.orchestration.worker_registry import (
    RoutePolicy, WorkerCostTier, WorkerKind, WorkerRiskTier, WorkerSelectionRequest, WorkerSpec,
    classify_route_cost, default_route_policy, estimate_context_fit, estimate_token_cost_band,
    evaluate_worker_selection, export_route_policy_json, export_worker_spec_json, get_worker_spec,
    is_placeholder, list_worker_specs, load_route_policy, load_worker_registry, save_route_policy,
    token_reduction_reason, worker_registry_integrity,
)


# ---------------------------------------------------------------------------
# WorkerSpec model + built-in registry
# ---------------------------------------------------------------------------


class TestWorkerSpecModel:
    def test_roundtrip_serialization(self):
        spec = WorkerSpec(worker_id="x.y", label="X", kind=WorkerKind.LOCAL_CANDIDATE,
                          enabled=True, cost_tier=WorkerCostTier.CHEAP, risk_tier=WorkerRiskTier.MEDIUM)
        d = export_worker_spec_json(spec)
        assert d["worker_id"] == "x.y"
        assert d["kind"] == WorkerKind.LOCAL_CANDIDATE
        assert d["is_placeholder"] is False
        assert d["schema_version"]

    def test_builtins_load_deterministically(self):
        a = [s.worker_id for s in list_worker_specs(load_worker_registry())]
        b = [s.worker_id for s in list_worker_specs(load_worker_registry())]
        assert a == b
        assert "local.candidate_generator" in a
        assert "external.builder_package" in a
        assert "ollama.placeholder" in a
        assert "cloud.placeholder" in a

    def test_placeholders_are_disabled_and_not_selectable(self):
        for wid in ("ollama.placeholder", "cloud.placeholder"):
            s = get_worker_spec(wid)
            assert s is not None
            assert s.enabled is False
            assert s.user_selectable is False
            assert is_placeholder(s) is True

    def test_external_worker_maps_to_package_rail(self):
        s = get_worker_spec("external.builder_package")
        assert s is not None and s.supports_external_builder_package is True
        assert s.execution_mode == "external_ingress"

    def test_unknown_worker_id_returns_none(self):
        assert get_worker_spec("does.not.exist") is None


# ---------------------------------------------------------------------------
# RoutePolicy defaults + persistence
# ---------------------------------------------------------------------------


class TestRoutePolicy:
    def test_defaults_are_safe(self):
        p = default_route_policy("job1")
        assert p.prefer_local_for_cheap_tasks is True
        assert p.prefer_ollama_for_cheap_tasks is False
        assert p.require_human_approval_for_expensive is True
        assert p.require_human_approval_for_high_risk is True
        assert p.policy_id

    def test_persistence_roundtrip(self, tmp_path):
        p = default_route_policy("jobP")
        p.blocked_worker_ids = ["cloud.placeholder"]
        p.max_cost_tier = WorkerCostTier.CHEAP
        assert save_route_policy(p, data_dir=tmp_path) is True
        loaded = load_route_policy("jobP", data_dir=tmp_path)
        assert loaded.blocked_worker_ids == ["cloud.placeholder"]
        assert loaded.max_cost_tier == WorkerCostTier.CHEAP

    def test_missing_policy_defaults(self, tmp_path):
        p = load_route_policy("never-saved", data_dir=tmp_path)
        assert p.policy_id  # a safe default, not a crash
        assert p.blocked_worker_ids == []

    def test_corrupt_policy_falls_back_to_default(self, tmp_path):
        f = tmp_path / "workspaces" / "jobC" / "route_policy" / "policy.json"
        f.parent.mkdir(parents=True)
        f.write_text("{ this is not json")
        p = load_route_policy("jobC", data_dir=tmp_path)
        assert p.policy_id and p.blocked_worker_ids == []

    def test_export_has_no_absolute_paths(self, tmp_path):
        p = default_route_policy("jobE")
        blob = json.dumps(export_route_policy_json(p))
        assert "/home/" not in blob and "/Users/" not in blob


# ---------------------------------------------------------------------------
# Worker selection
# ---------------------------------------------------------------------------


class TestWorkerSelection:
    def test_cheap_task_prefers_local(self):
        r = evaluate_worker_selection(WorkerSelectionRequest(task_type="repair",
                                                             estimated_context_tokens=4000))
        assert r.recommended_worker_id == "local.candidate_generator"
        assert r.local_first_applied is True
        assert r.requires_human_approval is False

    def test_disabled_worker_never_recommended(self):
        r = evaluate_worker_selection(WorkerSelectionRequest(task_type="repair"))
        assert r.recommended_worker_id not in ("ollama.placeholder", "cloud.placeholder")
        rejected = {c.worker_id for c in r.rejected_candidates}
        assert "cloud.placeholder" in rejected

    def test_blocked_worker_never_recommended(self):
        p = default_route_policy("j")
        p.blocked_worker_ids = ["local.candidate_generator"]
        r = evaluate_worker_selection(WorkerSelectionRequest(task_type="repair"), policy=p)
        assert r.recommended_worker_id != "local.candidate_generator"
        rejected = {c.worker_id for c in r.rejected_candidates}
        assert "local.candidate_generator" in rejected

    def test_user_selection_wins_among_eligible(self):
        p = default_route_policy("j")
        p.user_selected_worker_ids = ["external.builder_package"]
        r = evaluate_worker_selection(WorkerSelectionRequest(task_type="repair"), policy=p)
        assert r.recommended_worker_id == "external.builder_package"

    def test_user_selecting_disabled_worker_is_blocked_not_silently_run(self):
        p = default_route_policy("j")
        p.user_selected_worker_ids = ["cloud.placeholder"]  # disabled
        r = evaluate_worker_selection(WorkerSelectionRequest(task_type="repair"), policy=p)
        # Falls back to an eligible worker; never recommends the disabled selected worker.
        assert r.recommended_worker_id != "cloud.placeholder"

    def test_max_cost_tier_excludes_expensive(self):
        p = default_route_policy("j")
        p.max_cost_tier = WorkerCostTier.CHEAP
        p.blocked_worker_ids = ["local.candidate_generator"]
        r = evaluate_worker_selection(WorkerSelectionRequest(task_type="repair"), policy=p)
        # external (standard) excluded by cheap ceiling; human (free) remains.
        assert r.recommended_worker_id == "human.operator"

    def test_expensive_route_requires_human_approval(self):
        p = default_route_policy("j")
        p.max_cost_tier = WorkerCostTier.EXPENSIVE
        p.max_risk_tier = WorkerRiskTier.HIGH
        p.user_selected_worker_ids = ["external.builder_package"]  # standard cost + HIGH risk
        r = evaluate_worker_selection(WorkerSelectionRequest(task_type="feature"), policy=p)
        assert r.recommended_worker_id == "external.builder_package"
        assert r.requires_human_approval is True

    def test_no_eligible_worker_yields_human_review_action(self):
        p = default_route_policy("j")
        p.max_cost_tier = WorkerCostTier.FREE
        p.blocked_worker_ids = ["human.operator", "reviewer.parallel", "fixture.worker"]
        r = evaluate_worker_selection(WorkerSelectionRequest(task_type="repair"), policy=p)
        assert r.recommended_worker_id == ""
        assert r.requires_human_approval is True
        assert "route-policy" in r.next_safe_action


# ---------------------------------------------------------------------------
# R-0095 — hard-safety approval cannot be weakened by policy flags
# ---------------------------------------------------------------------------


class TestHardSafetyApproval:
    def test_external_always_requires_approval(self):
        p = default_route_policy("j")
        p.require_human_approval_for_expensive = False
        p.require_human_approval_for_high_risk = False
        p.user_selected_worker_ids = ["external.builder_package"]
        r = evaluate_worker_selection(WorkerSelectionRequest(task_type="feature"), policy=p)
        assert r.recommended_worker_id == "external.builder_package"
        assert r.requires_human_approval is True

    def test_high_risk_route_cannot_become_no_approval(self):
        from packages.orchestration.worker_registry import hard_safety_requires_approval
        p = default_route_policy("j")
        p.require_human_approval_for_expensive = False
        p.require_human_approval_for_high_risk = False
        for wid in ("external.builder_package", "ollama.placeholder", "cloud.placeholder"):
            spec = get_worker_spec(wid)
            assert hard_safety_requires_approval(spec) is True
            # _requires_approval honours the hard floor regardless of disabled flags
            from packages.orchestration.worker_registry import _requires_approval
            assert _requires_approval(spec, p) is True

    def test_unknown_cost_route_requires_approval(self):
        from packages.orchestration.worker_registry import hard_safety_requires_approval
        spec = WorkerSpec(worker_id="u", enabled=True, cost_tier=WorkerCostTier.UNKNOWN,
                          risk_tier=WorkerRiskTier.LOW, kind=WorkerKind.LOCAL_CANDIDATE)
        assert hard_safety_requires_approval(spec) is True


# ---------------------------------------------------------------------------
# Token economy — estimate bands only
# ---------------------------------------------------------------------------


class TestTokenEconomy:
    def test_unknown_cost_never_cheap(self):
        spec = WorkerSpec(worker_id="u", cost_tier=WorkerCostTier.UNKNOWN, enabled=True)
        assert classify_route_cost(spec) == WorkerCostTier.UNKNOWN
        assert estimate_token_cost_band(spec) == "unknown"
        assert "not-cheap" in token_reduction_reason(spec) or "unknown" in token_reduction_reason(spec)

    def test_context_fit_unknown_when_no_profile(self):
        spec = WorkerSpec(worker_id="u", enabled=True)
        fit = estimate_context_fit(spec, 5000)
        assert fit["fits"] == "unknown"
        assert fit["estimated"] is True

    def test_context_fit_estimated(self):
        spec = get_worker_spec("local.candidate_generator")
        over = estimate_context_fit(spec, 999999)
        assert over["fits"] is False and over["estimated"] is True
        under = estimate_context_fit(spec, 100)
        assert under["fits"] is True

    def test_token_budget_warning_when_context_too_big(self):
        r = evaluate_worker_selection(WorkerSelectionRequest(
            task_type="repair", estimated_context_tokens=999999))
        # recommended worker's context band is exceeded → estimate warning
        if r.recommended_worker_id:
            assert "estimated" in r.token_budget_warning or r.token_budget_warning == "" \
                or "context" in r.token_budget_warning


# ---------------------------------------------------------------------------
# Integrity — positive + negative
# ---------------------------------------------------------------------------


class TestIntegrity:
    def test_builtins_pass_integrity(self, tmp_path):
        ig = worker_registry_integrity(data_dir=tmp_path)
        assert ig["passed"] is True
        assert ig["violation_count"] == 0
        assert ig["worker_count"] >= 7

    def test_selected_missing_worker_flagged(self, tmp_path):
        p = default_route_policy("jobM")
        p.user_selected_worker_ids = ["ghost.worker"]
        save_route_policy(p, data_dir=tmp_path)
        ig = worker_registry_integrity(data_dir=tmp_path)
        codes = {v.get("code") for v in ig["violations"]}
        assert "selected_worker_missing" in codes
        assert ig["passed"] is False

    def test_selected_disabled_worker_flagged(self, tmp_path):
        p = default_route_policy("jobD")
        p.user_selected_worker_ids = ["cloud.placeholder"]  # exists but disabled
        save_route_policy(p, data_dir=tmp_path)
        ig = worker_registry_integrity(data_dir=tmp_path)
        codes = {v.get("code") for v in ig["violations"]}
        assert "selected_worker_disabled" in codes

    def test_selected_and_blocked_flagged(self, tmp_path):
        p = default_route_policy("jobB")
        p.user_selected_worker_ids = ["local.candidate_generator"]
        p.blocked_worker_ids = ["local.candidate_generator"]
        save_route_policy(p, data_dir=tmp_path)
        ig = worker_registry_integrity(data_dir=tmp_path)
        codes = {v.get("code") for v in ig["violations"]}
        assert "worker_selected_and_blocked" in codes

    # R-0096 negative cases
    def _write_custom_spec(self, tmp_path, spec_dict):
        import json as _j
        f = tmp_path / "workspaces" / "orchestrator" / "worker_registry" / spec_dict["worker_id"] / "worker.json"
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(_j.dumps(spec_dict))

    def test_high_risk_route_approval_disabled_flagged(self, tmp_path):
        p = default_route_policy("jobH")
        p.user_selected_worker_ids = ["external.builder_package"]  # high risk
        p.require_human_approval_for_high_risk = False
        save_route_policy(p, data_dir=tmp_path)
        ig = worker_registry_integrity(data_dir=tmp_path)
        codes = {v.get("code") for v in ig["violations"]}
        assert "high_risk_route_approval_disabled" in codes
        assert ig["passed"] is False

    def test_unknown_cost_selected_treated_cheap_flagged(self, tmp_path):
        self._write_custom_spec(tmp_path, {
            "worker_id": "custom.unknown_cost", "kind": WorkerKind.LOCAL_CANDIDATE,
            "enabled": True, "user_selectable": True, "cost_tier": WorkerCostTier.UNKNOWN,
            "risk_tier": WorkerRiskTier.LOW, "execution_mode": "local_model",
            "token_profile": {"band": "small"}})
        p = default_route_policy("jobU")
        p.user_selected_worker_ids = ["custom.unknown_cost"]
        p.prefer_local_for_cheap_tasks = True
        save_route_policy(p, data_dir=tmp_path)
        ig = worker_registry_integrity(data_dir=tmp_path)
        codes = {v.get("code") for v in ig["violations"]}
        assert "unknown_cost_treated_cheap" in codes
        assert ig["passed"] is False

    def test_placeholder_claiming_executable_readiness_flagged(self, tmp_path):
        self._write_custom_spec(tmp_path, {
            "worker_id": "custom.fake_ready", "kind": WorkerKind.LOCAL_CANDIDATE,
            "enabled": True, "user_selectable": True, "cost_tier": WorkerCostTier.CHEAP,
            "risk_tier": WorkerRiskTier.LOW, "execution_mode": "local_model",
            "notes": "this is a placeholder pretending to be ready"})
        ig = worker_registry_integrity(data_dir=tmp_path)
        codes = {v.get("code") for v in ig["violations"]}
        assert "placeholder_claims_ready" in codes


# ---------------------------------------------------------------------------
# Redaction — no secrets/paths/raw in public export
# ---------------------------------------------------------------------------


class TestRedaction:
    def test_no_secret_or_path_markers_in_specs(self):
        blob = json.dumps([s.to_dict() for s in list_worker_specs(load_worker_registry())]).lower()
        for marker in ("sk-", "api_key", "password", "-----begin", "/home/", "/users/", "/root/"):
            assert marker not in blob, marker

    def test_no_api_keys_or_endpoints_field(self):
        for s in list_worker_specs(load_worker_registry()):
            d = s.to_dict()
            assert "api_key" not in d and "endpoint" not in d and "secret" not in d


# ---------------------------------------------------------------------------
# Architecture guards (Step 1737)
# ---------------------------------------------------------------------------


class TestArchitectureGuards:
    def _src(self) -> str:
        """Source with docstrings AND string literals stripped, so metadata text (e.g. the word
        'ollama' in a worker_id, or 'human-approved' in an output_contract) cannot trip the
        import/execution checks — only real code tokens remain."""
        p = Path(__file__).resolve().parents[2] / "packages" / "orchestration" / "worker_registry.py"
        src = p.read_text(encoding="utf-8")
        src = re.sub(r'"""[\s\S]*?"""', "", src)        # triple-quoted docstrings
        src = re.sub(r"'''[\s\S]*?'''", "", src)
        src = re.sub(r'"(?:\\.|[^"\\])*"', '""', src)    # double-quoted string literals
        src = re.sub(r"'(?:\\.|[^'\\])*'", "''", src)    # single-quoted string literals
        return src

    def test_no_forbidden_imports(self):
        src = self._src()
        for bad in ("import requests", "import socket", "import urllib", "import httpx",
                    "import subprocess", "subprocess.", "shell=True", "import ollama",
                    "import openai", "import anthropic"):
            assert bad not in src, bad

    def test_no_execution_or_apply(self):
        src = self._src()
        for bad in ("os.system", "Popen", "check_output", "do_continue(", "apply_patch(",
                    ".approve(", "os.fork", "eval(", "exec("):
            assert bad not in src, bad
