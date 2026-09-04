"""Token Economy + Context Budget Optimizer v0 tests (Steps 1774/1777/1778).

Unit (models, estimate helpers, profile storage, context budget estimate, pack recommendation,
savings, unknown handling, redaction, integrity) + architecture guards. ESTIMATES + METADATA only —
nothing here executes a worker or calls a model.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from uuid import uuid4

import pytest

from packages.orchestration import token_economy as te

# ---------------------------------------------------------------------------
# Job + repo fixtures (small bounded repo so inspect_context is deterministic)
# ---------------------------------------------------------------------------


def _job_with_repo(env: Path, *, files: dict[str, str]) -> str:
    from packages.core.models import Job, RunState, Task
    from packages.orchestration.storage import save_job
    repo = env / f"repo-{uuid4().hex[:6]}"
    repo.mkdir(parents=True)
    for rel, content in files.items():
        p = repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
    task = Task(description="t")
    job = Job(id=uuid4(), name="te", user_prompt="x", state=RunState.RUNNING, tasks=[task],
              artifacts=[], metadata={"target_repo": str(repo)})
    save_job(job, root=env)
    return str(job.id)


@pytest.fixture()
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"; d.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    return d


# ---------------------------------------------------------------------------
# Estimate helpers
# ---------------------------------------------------------------------------


class TestEstimateHelpers:
    def test_text_tokens_stable(self):
        assert te.estimate_text_tokens("x" * 100) == 25
        assert te.estimate_text_tokens("") == 0
        assert te.estimate_text_tokens(None) == 0  # type: ignore[arg-type]

    def test_context_tokens_mixed_items(self):
        total = te.estimate_context_tokens([{"estimated_tokens": 500}, {"size_bytes": 4000}, "abcd"])
        assert total == 500 + 1000 + 1

    def test_context_tokens_invalid(self):
        assert te.estimate_context_tokens(None) == 0
        assert te.estimate_context_tokens([{"estimated_tokens": -5}]) == 0

    def test_task_band(self):
        assert te.estimate_task_token_band("repair", 4000) == te.TokenBand.LOW
        assert te.estimate_task_token_band("repair", 20000) == te.TokenBand.MEDIUM
        assert te.estimate_task_token_band("repair", 50000) == te.TokenBand.HIGH
        assert te.estimate_task_token_band("repair", -1) == te.TokenBand.UNKNOWN

    def test_route_band_unknown_stays_unknown(self):
        from packages.orchestration.worker_registry import get_worker_spec
        ext = get_worker_spec("external.builder_package")  # token band unknown
        assert te.estimate_route_token_band(ext, 4000) == te.TokenBand.UNKNOWN
        assert te.estimate_route_token_band(None, 4000) == te.TokenBand.UNKNOWN

    def test_savings(self):
        s = te.estimate_token_savings(10000, 3000)
        assert s["saved_tokens"] == 7000 and s["band"] == te.TokenBand.HIGH
        assert s["estimated"] is True and s["verified"] is False

    def test_savings_invalid_unknown(self):
        s = te.estimate_token_savings(-1, 5)
        assert s["saved_tokens"] == "unknown" and s["band"] == te.TokenBand.UNKNOWN


# ---------------------------------------------------------------------------
# Budget profile model + storage
# ---------------------------------------------------------------------------


class TestBudgetProfile:
    def test_default_floors(self):
        p = te.default_token_budget_profile("j")
        assert p.max_context_tokens > 0 and p.prefer_local_under_tokens > 0 and p.profile_id

    def test_persistence_roundtrip(self, tmp_path):
        p = te.default_token_budget_profile("jP")
        p.max_context_tokens = 16000
        assert te.save_token_budget_profile(p, data_dir=tmp_path) is True
        loaded = te.load_token_budget_profile("jP", data_dir=tmp_path)
        assert loaded.max_context_tokens == 16000

    def test_corrupt_profile_default(self, tmp_path):
        f = tmp_path / "workspaces" / "jC" / "token_economy" / "budget_profile.json"
        f.parent.mkdir(parents=True)
        f.write_text("{ not json")
        p = te.load_token_budget_profile("jC", data_dir=tmp_path)
        assert p.profile_id and p.max_context_tokens > 0

    def test_floor_enforced_on_save(self, tmp_path):
        p = te.default_token_budget_profile("jF")
        p.max_context_tokens = 0
        te.save_token_budget_profile(p, data_dir=tmp_path)
        loaded = te.load_token_budget_profile("jF", data_dir=tmp_path)
        assert loaded.max_context_tokens >= 1

    def test_export_no_absolute_paths(self):
        blob = json.dumps(te.export_token_budget_profile_json(te.default_token_budget_profile("j")))
        assert "/home/" not in blob and "/Users/" not in blob


# ---------------------------------------------------------------------------
# Context budget estimate + pack recommendation
# ---------------------------------------------------------------------------


class TestContextBudget:
    def test_estimate_no_job_warns_not_fake_zero(self, env):
        est = te.estimate_context_budget("no-such-job")
        assert "no_context_inspection_available" in est.warnings
        assert est.estimated_total_tokens == 0
        assert est.confidence == "estimated_low"

    def test_estimate_with_repo(self, env):
        jid = _job_with_repo(env, files={"README.md": "hello\n" * 100, "src/a.py": "x = 1\n" * 50})
        est = te.estimate_context_budget(jid)
        assert est.estimated_input_tokens >= 0
        d = est.to_dict()
        assert d["estimated"] is True and d["verified"] is False

    def test_pack_no_job_defers(self, env):
        rec = te.recommend_context_pack("no-such-job")
        assert rec.recommended_pack_kind == te.ContextPackKind.DEFER_FOR_HUMAN

    def test_pack_excludes_protected(self, env):
        jid = _job_with_repo(env, files={"README.md": "hi\n", ".env": "SECRET=abc\n",
                                         "src/a.py": "x=1\n"})
        rec = te.recommend_context_pack(jid)
        blob = json.dumps(rec.to_dict()).lower()
        assert "secret=abc" not in blob  # raw content never dumped
        assert rec.to_dict()["memory_candidates_persisted"] is False
        # .env must not be an included ref
        assert not any(".env" in r for r in rec.included_context_refs)

    def test_pack_memory_candidates_are_suggestions(self, env):
        jid = _job_with_repo(env, files={"README.md": "hi\n", "src/a.py": "x=1\n"})
        rec = te.recommend_context_pack(jid)
        assert rec.to_dict()["memory_candidates_persisted"] is False


# ---------------------------------------------------------------------------
# TokenEconomyDecision
# ---------------------------------------------------------------------------


class TestDecision:
    def test_no_job_unknown_band_not_cheap(self, env):
        d = te.compute_token_economy_decision("no-such-job", task_type="repair")
        assert d.estimated_token_band == te.TokenBand.UNKNOWN  # unknown context never "low"/cheap

    # R-0098 — unknown context/budget must require approval and never claim a cheap/local fit.
    def test_unknown_context_requires_approval(self, env):
        d = te.compute_token_economy_decision("no-such-job", task_type="repair")
        assert d.requires_human_approval is True
        assert "unknown_context_or_budget" in d.warnings
        assert "fits the estimated budget" not in d.reason.lower()
        assert "unknown" in d.reason.lower()
        # next action points to a safe inspection, not a cheap-route-ready implication.
        assert "context inspect" in d.next_safe_action or "route-policy" in d.next_safe_action

    def test_unknown_context_hint_not_local_first(self, env):
        h = te.routing_token_hint("no-such-job")
        assert h["requires_human_approval"] is True
        assert h["local_first_recommended"] is False

    def test_local_route_no_approval_when_cheap(self, env):
        jid = _job_with_repo(env, files={"README.md": "hi\n", "src/a.py": "x=1\n"})
        d = te.compute_token_economy_decision(jid, task_type="repair")
        # small repo → local route, cheap, no approval
        assert d.recommended_worker_id == "local.candidate_generator"
        assert d.requires_human_approval is False

    def test_over_threshold_requires_approval(self, env):
        jid = _job_with_repo(env, files={"README.md": "hi\n"})
        p = te.load_token_budget_profile(jid, data_dir=env)
        p.require_human_approval_over_tokens = 1  # any estimate triggers approval
        te.save_token_budget_profile(p, data_dir=env)
        # force a non-zero estimate by adding a bigger file
        jid2 = _job_with_repo(env, files={"src/big.py": "x = 1\n" * 5000})
        p2 = te.load_token_budget_profile(jid2, data_dir=env)
        p2.require_human_approval_over_tokens = 1
        te.save_token_budget_profile(p2, data_dir=env)
        d = te.compute_token_economy_decision(jid2, task_type="repair")
        assert d.requires_human_approval is True


# ---------------------------------------------------------------------------
# Routing hint
# ---------------------------------------------------------------------------


class TestRoutingHint:
    def test_hint_shape(self, env):
        jid = _job_with_repo(env, files={"README.md": "hi\n", "src/a.py": "x=1\n"})
        h = te.routing_token_hint(jid)
        for k in ("estimated_token_band", "budget_status", "context_pack_kind",
                  "requires_human_approval", "next_safe_action", "local_first_recommended"):
            assert k in h
        assert h["estimated"] is True

    def test_hint_empty_job_unknown_band(self):
        # Empty job → no inspection → token band UNKNOWN (never silently "cheap"); the safe local
        # default route may still be recommended without approval (local is inherently safe).
        h = te.routing_token_hint("")
        assert h["estimated_token_band"] == te.TokenBand.UNKNOWN
        assert h["estimated"] is True


# ---------------------------------------------------------------------------
# Integrity + redaction
# ---------------------------------------------------------------------------


class TestIntegrity:
    def test_empty_passes(self, tmp_path):
        ig = te.token_economy_integrity(data_dir=tmp_path)
        assert ig["passed"] is True and ig["violation_count"] == 0

    def test_non_positive_budget_flagged(self, tmp_path):
        f = tmp_path / "workspaces" / "jB" / "token_economy" / "budget_profile.json"
        f.parent.mkdir(parents=True)
        f.write_text(json.dumps({"profile_id": "tb-x", "job_id": "jB", "max_context_tokens": 0,
                                 "max_generation_tokens": 100, "max_total_estimated_tokens": 100}))
        ig = te.token_economy_integrity(data_dir=tmp_path)
        codes = {v.get("code") for v in ig["violations"]}
        assert "non_positive_budget" in codes
        assert ig["passed"] is False

    def test_exact_pricing_flagged(self, tmp_path):
        f = tmp_path / "workspaces" / "jP" / "token_economy" / "budget_profile.json"
        f.parent.mkdir(parents=True)
        f.write_text(json.dumps({"profile_id": "tb-y", "job_id": "jP",
                                 "max_context_tokens": 100, "max_generation_tokens": 100,
                                 "max_total_estimated_tokens": 100, "cost_usd": 12.50}))
        ig = te.token_economy_integrity(data_dir=tmp_path)
        codes = {v.get("code") for v in ig["violations"]}
        assert "exact_pricing_claimed" in codes

    # R-0099 — decision-state audit catches unknown-without-approval / unknown-as-fit.
    def test_audit_flags_unknown_band_without_approval(self):
        v = te.audit_decision_safety({
            "decision_id": "te-x", "estimated_token_band": "unknown",
            "budget_status": "within_budget", "requires_human_approval": False, "warnings": []})
        codes = {x["code"] for x in v}
        assert "unknown_token_band_without_approval" in codes

    def test_audit_flags_unknown_budget_without_approval(self):
        v = te.audit_decision_safety({
            "decision_id": "te-y", "estimated_token_band": "low",
            "budget_status": "unknown_budget", "requires_human_approval": False, "warnings": []})
        codes = {x["code"] for x in v}
        assert "unknown_budget_without_approval" in codes

    def test_audit_flags_no_inspection_without_approval(self):
        v = te.audit_decision_safety({
            "decision_id": "te-z", "estimated_token_band": "low", "budget_status": "within_budget",
            "requires_human_approval": False, "warnings": ["no_context_inspection_available"]})
        codes = {x["code"] for x in v}
        assert "no_inspection_without_approval" in codes

    def test_audit_flags_unknown_presented_as_fit(self):
        v = te.audit_decision_safety({
            "decision_id": "te-w", "estimated_token_band": "unknown", "budget_status": "unknown_budget",
            "requires_human_approval": True,
            "reason": "Cheap/local route fits the estimated budget", "warnings": []})
        codes = {x["code"] for x in v}
        assert "unknown_context_presented_as_fit" in codes

    def test_audit_safe_decision_clean(self):
        assert te.audit_decision_safety({
            "decision_id": "ok", "estimated_token_band": "low", "budget_status": "within_budget",
            "requires_human_approval": False, "reason": "Cheap/local route fits the estimated budget",
            "warnings": []}) == []

    def test_integrity_scans_decisions(self, tmp_path):
        bad = {"decision_id": "te-bad", "estimated_token_band": "unknown",
               "budget_status": "unknown_budget", "requires_human_approval": False, "warnings": []}
        ig = te.token_economy_integrity(data_dir=tmp_path, decisions=[bad])
        assert ig["passed"] is False
        codes = {v.get("code") for v in ig["violations"]}
        assert "unknown_token_band_without_approval" in codes

    def test_real_unknown_decision_is_safe_under_audit(self, env):
        # The fixed compute_token_economy_decision must produce a decision that PASSES the audit.
        d = te.compute_token_economy_decision("no-such-job", task_type="repair")
        assert te.audit_decision_safety(d.to_dict()) == []

    def test_report_no_raw_or_pricing(self, env):
        jid = _job_with_repo(env, files={"README.md": "hi\n", ".env": "TOKEN=sk-secret\n"})
        rep = te.token_economy_report(jid)
        blob = json.dumps(rep).lower()
        for marker in ("sk-secret", "/home/", "/users/", "price_usd", "cost_usd"):
            assert marker not in blob, marker


# ---------------------------------------------------------------------------
# Architecture guards (Step 1778)
# ---------------------------------------------------------------------------


class TestArchitectureGuards:
    def _src(self) -> str:
        p = Path(__file__).resolve().parents[2] / "packages" / "orchestration" / "token_economy.py"
        src = p.read_text(encoding="utf-8")
        src = re.sub(r'"""[\s\S]*?"""', "", src)
        src = re.sub(r"'''[\s\S]*?'''", "", src)
        src = re.sub(r'"(?:\\.|[^"\\])*"', '""', src)
        src = re.sub(r"'(?:\\.|[^'\\])*'", "''", src)
        return src

    def test_no_forbidden_imports(self):
        src = self._src()
        for bad in ("import requests", "import socket", "import urllib", "import httpx",
                    "import subprocess", "subprocess.", "shell=True", "import ollama",
                    "import openai", "import anthropic", "import tiktoken"):
            assert bad not in src, bad

    def test_no_execution_or_apply(self):
        src = self._src()
        for bad in ("os.system", "Popen", "check_output", "do_continue(", "apply_patch(",
                    ".approve(", "os.fork", "eval(", "exec("):
            assert bad not in src, bad


# ---------------------------------------------------------------------------
# tokens_to_cost_usd (F114 T001 — extracted from budget_guard.predict_next_task_cost)
# ---------------------------------------------------------------------------


class TestTokensToCostUsd:
    def test_ordinary_multiply(self):
        # 8000 tokens x $0.02/1k = $0.16 — the exact figure
        # test_predictive_budget.py's TestBreachBoundary pins for the same inputs.
        assert te.tokens_to_cost_usd(8000, 0.02) == 0.16

    def test_zero_tokens_is_a_measured_zero_not_none(self):
        assert te.tokens_to_cost_usd(0, 0.02) == 0.0

    def test_none_tokens_propagates_none(self):
        assert te.tokens_to_cost_usd(None, 0.02) is None

    def test_none_price_basis_propagates_none(self):
        assert te.tokens_to_cost_usd(8000, None) is None

    def test_both_none_propagates_none(self):
        assert te.tokens_to_cost_usd(None, None) is None
