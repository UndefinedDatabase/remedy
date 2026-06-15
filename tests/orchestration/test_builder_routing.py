"""Unit + integration tests for Expensive Builder Routing v0 (Steps 1596-1602).

Routing/policy/planning ONLY. The router NEVER executes a builder/model/provider, generates
a candidate, calls the network/subprocess, imports a provider SDK, applies/approves, or creates
Patch Intents/ProposedTasks. External builder is NEVER recommended without request package +
Trust Gate + Verification + budget + low loop risk + no pending approval/intent. No raw prompt/
response/source/diff/log/secrets/paths in any surface. Every next action is catalog-backed.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from packages.orchestration.builder_routing import (
    BuilderRoutingRequest, BuilderRoutingPolicy, BuilderRoutingTier, BuilderRoutingStopReason,
    BuilderRoutingJustification, LoopGovernorStatus, default_builder_routing_policy,
    select_builder_routing_decision, export_builder_routing_json, load_builder_routing_traces,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_job(data_dir, *, failure=True, related=None, repair_attempts=None,
              trust=None):
    from packages.core.models import Job, Artifact, ArtifactKind, RunState
    from packages.orchestration.storage import save_job
    arts = []
    fid = ""
    if failure:
        fa = Artifact(name="tf", content="x", kind=ArtifactKind.VERIFICATION, task_id=None,
                      metadata={"test_failure": True, "related_files": related or []})
        arts.append(fa)
        fid = str(fa.id)
    meta = {"target_repo": "."}
    if repair_attempts:
        meta["repair_attempts_v1"] = repair_attempts
    if trust:
        meta["provider_trust_reports_v0"] = trust
    job = Job(id=uuid4(), name="r", user_prompt="x", state=RunState.RUNNING,
              artifacts=arts, metadata=meta)
    save_job(job, root=data_dir)
    return str(job.id), fid


def _failed_attempt(fid: str) -> dict:
    aid = uuid4().hex[:8]
    return {aid: {"attempt_id": aid, "failure_artifact_id": fid, "status": "tested_failed",
                  "repair_kind": "docs_fixture", "expected_effect": "documentation_only"}}


@pytest.fixture()
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"
    d.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    rv = tmp_path / "review.md"
    rv.write_text("## Verdict\nPASS\n")
    monkeypatch.setenv("REMEDY_REVIEW_FILE", str(rv))
    for k in ("REMEDY_LOCAL_ADVISOR_ENABLED", "REMEDY_LOCAL_ADVISOR_ENDPOINT",
              "REMEDY_LOCAL_ADVISOR_MODEL"):
        monkeypatch.delenv(k, raising=False)
    return d


def _advisor_on(monkeypatch):
    monkeypatch.setenv("REMEDY_LOCAL_ADVISOR_ENABLED", "1")
    monkeypatch.setenv("REMEDY_LOCAL_ADVISOR_ENDPOINT", "http://127.0.0.1:11434")
    monkeypatch.setenv("REMEDY_LOCAL_ADVISOR_MODEL", "m")


def _req(jid, fid="", **kw):
    return BuilderRoutingRequest(job_id=jid, failure_artifact_id=fid, **kw)


# ---------------------------------------------------------------------------
# Step 1596 — routing quality
# ---------------------------------------------------------------------------


class TestRoutingQuality:
    def test_pending_approval_beats_new_builder_route(self, env):
        # An accepted-unverified trust report → deterministic verify, not generation.
        jid, fid = _make_job(env, related=["docs/g.md"], trust={
            "tr1": {"report_id": "tr1", "trust_status": "accepted", "quarantine_id": "q",
                    "candidate": {"has_patch": True, "target_files": ["docs/g.md"]}}})
        d = select_builder_routing_decision(_req(jid, fid), data_dir=env)
        assert d.selected_tier == BuilderRoutingTier.DETERMINISTIC_ONLY
        assert "provider verify" in d.next_safe_action

    def test_deterministic_fix_blocks_expensive_builder(self, env):
        # Unresolved failure, no repair attempt → deterministic repair propose dominates.
        jid, fid = _make_job(env)
        pol = BuilderRoutingPolicy(allow_external_candidate_generator=True,
                                   max_estimated_cost=10)
        d = select_builder_routing_decision(_req(jid, fid), pol, data_dir=env)
        assert d.selected_tier == BuilderRoutingTier.DETERMINISTIC_ONLY
        assert "repair propose" in d.next_safe_action

    def test_ambiguity_recommends_local_advisor_when_unused(self, env, monkeypatch):
        _advisor_on(monkeypatch)
        # Failed repair → no deterministic propose → advisor untried → LOCAL_ADVISOR.
        jid, fid = _make_job(env, repair_attempts=None)
        jid, fid = _make_job(env, related=["docs/g.md"])
        # add a failed repair attempt so the deterministic propose option is gone
        from packages.orchestration.storage import load_job, save_job
        job = load_job(UUID(jid), env)
        job.metadata["repair_attempts_v1"] = _failed_attempt(fid)
        save_job(job, root=env)
        d = select_builder_routing_decision(_req(jid, fid), data_dir=env)
        assert d.selected_tier == BuilderRoutingTier.LOCAL_ADVISOR
        assert "--use-local-advisor" in d.next_safe_action

    def test_request_package_missing_recommends_prepare(self, env, monkeypatch):
        # Need exists, advisor disabled, no request package → NO_SAFE_ROUTE + prepare request.
        jid, fid = _make_job(env, related=["docs/g.md"])
        from packages.orchestration.storage import load_job, save_job
        job = load_job(UUID(jid), env)
        job.metadata["repair_attempts_v1"] = _failed_attempt(fid)
        save_job(job, root=env)
        d = select_builder_routing_decision(_req(jid, fid), data_dir=env)
        assert d.selected_tier == BuilderRoutingTier.NO_SAFE_ROUTE
        assert d.stop_reason == BuilderRoutingStopReason.MISSING_REQUEST_PACKAGE
        assert "repair request" in d.next_safe_action

    def test_external_requires_explicit_policy(self, env):
        # Even with a request package + need, default policy (external disabled) never routes external.
        jid, fid = _make_job(env, related=["docs/g.md"])
        _add_request_package(env, jid, fid)
        from packages.orchestration.storage import load_job, save_job
        job = load_job(UUID(jid), env)
        job.metadata["repair_attempts_v1"] = _failed_attempt(fid)
        save_job(job, root=env)
        d = select_builder_routing_decision(_req(jid, fid), data_dir=env)
        assert d.selected_tier != BuilderRoutingTier.EXTERNAL_CANDIDATE_GENERATOR


# ---------------------------------------------------------------------------
# Step 1597 — budget / policy
# ---------------------------------------------------------------------------


def _add_request_package(env, jid, fid):
    from packages.orchestration.storage import load_job, save_job
    job = load_job(UUID(jid), env)
    job.metadata["repair_request_packages_v0"] = {
        "rp1": {"request_package_id": "rp1", "job_id": jid, "failure_artifact_id": fid,
                "target_kind": "docs"}}
    save_job(job, root=env)


class TestBudgetPolicy:
    def test_external_disabled_by_default(self, env):
        assert default_builder_routing_policy().allow_external_candidate_generator is False

    def test_local_candidate_disabled_by_default(self, env):
        assert default_builder_routing_policy().allow_local_candidate_generator is False

    def test_unknown_external_cost_blocks_external(self, env):
        # External allowed but max_estimated_cost unknown → external not selected.
        jid, fid = _make_job(env, related=["docs/g.md"])
        _add_request_package(env, jid, fid)
        from packages.orchestration.storage import load_job, save_job
        job = load_job(UUID(jid), env)
        job.metadata["repair_attempts_v1"] = _failed_attempt(fid)
        save_job(job, root=env)
        pol = BuilderRoutingPolicy(allow_external_candidate_generator=True)  # cost unknown
        d = select_builder_routing_decision(_req(jid, fid), pol, data_dir=env)
        assert d.selected_tier != BuilderRoutingTier.EXTERNAL_CANDIDATE_GENERATOR

    def test_external_route_with_known_cost(self, env):
        jid, fid = _make_job(env, related=["docs/g.md"])
        _add_request_package(env, jid, fid)
        from packages.orchestration.storage import load_job, save_job
        job = load_job(UUID(jid), env)
        job.metadata["repair_attempts_v1"] = _failed_attempt(fid)
        save_job(job, root=env)
        pol = BuilderRoutingPolicy(allow_external_candidate_generator=True, max_estimated_cost=5)
        d = select_builder_routing_decision(_req(jid, fid, user_requested=True), pol, data_dir=env)
        assert d.selected_tier == BuilderRoutingTier.EXTERNAL_CANDIDATE_GENERATOR
        # Hard preconditions present.
        for code in (BuilderRoutingJustification.REQUEST_PACKAGE_READY,
                     BuilderRoutingJustification.TRUST_AND_VERIFICATION_AVAILABLE,
                     BuilderRoutingJustification.BUDGET_AVAILABLE,
                     BuilderRoutingJustification.LOOP_RISK_LOW):
            assert code in d.justification_codes

    def test_local_candidate_route_when_enabled(self, env):
        jid, fid = _make_job(env, related=["docs/g.md"])
        _add_request_package(env, jid, fid)
        from packages.orchestration.storage import load_job, save_job
        job = load_job(UUID(jid), env)
        job.metadata["repair_attempts_v1"] = _failed_attempt(fid)
        save_job(job, root=env)
        pol = BuilderRoutingPolicy(allow_local_candidate_generator=True)
        d = select_builder_routing_decision(_req(jid, fid), pol, data_dir=env)
        assert d.selected_tier == BuilderRoutingTier.LOCAL_CANDIDATE_GENERATOR

    def test_loop_high_blocks_generation(self, env):
        # Two prior verification rejections → loop governor → human review.
        jid, fid = _make_job(env, related=["docs/g.md"])
        _add_request_package(env, jid, fid)
        from packages.orchestration.storage import load_job, save_job
        job = load_job(UUID(jid), env)
        job.metadata["repair_attempts_v1"] = _failed_attempt(fid)
        job.metadata["provider_verifications_v1"] = {
            "v1": {"decision": "verification_rejected", "candidate_hash": "h1"},
            "v2": {"decision": "verification_rejected", "candidate_hash": "h2"}}
        save_job(job, root=env)
        pol = BuilderRoutingPolicy(allow_external_candidate_generator=True, max_estimated_cost=5)
        d = select_builder_routing_decision(_req(jid, fid), pol, data_dir=env)
        assert d.selected_tier == BuilderRoutingTier.HUMAN_REVIEW_REQUIRED
        assert d.loop_guard_status == LoopGovernorStatus.HUMAN_REVIEW_REQUIRED


# ---------------------------------------------------------------------------
# Step 1599 — redaction
# ---------------------------------------------------------------------------


class TestRedaction:
    def test_no_raw_leak_in_export(self, env):
        leak = ("secret token sk-ABCDEFGHIJKLMNOP /home/user/.ssh/id_rsa "
                "Traceback (most recent call last): --- a/x.py +++ b/x.py")
        jid, fid = _make_job(env, related=[leak])
        d = select_builder_routing_decision(_req(jid, fid), data_dir=env)
        blob = json.dumps(export_builder_routing_json(d))
        for bad in ("sk-ABCDEFGHIJKLMNOP", "/home/user/.ssh/id_rsa", "Traceback"):
            assert bad not in blob

    def test_trace_on_disk_safe(self, env):
        jid, fid = _make_job(env)
        select_builder_routing_decision(_req(jid, fid), data_dir=env)
        traces = load_builder_routing_traces(scope=f"job:{jid}", data_dir=env)
        assert traces
        blob = json.dumps(traces)
        for bad in ("/home/", "-----BEGIN", "Traceback"):
            assert bad not in blob


# ---------------------------------------------------------------------------
# Step 1600 — architecture guards
# ---------------------------------------------------------------------------


class TestArchitectureGuards:
    def _code(self):
        src = Path("packages/orchestration/builder_routing.py").read_text()
        out, in_doc = [], False
        for ln in src.splitlines():
            s = ln.strip()
            if s.startswith('"""'):
                if s.count('"""') == 1:
                    in_doc = not in_doc
                continue
            if in_doc or s.startswith("#"):
                continue
            out.append(ln)
        return "\n".join(out)

    def test_no_forbidden_imports(self):
        code = self._code()
        for bad in ("import requests", "import httpx", "import openai", "import anthropic",
                    "import subprocess", "shell=True", "urllib.request", "import socket",
                    "selenium", "playwright"):
            assert bad not in code, f"forbidden token: {bad}"

    def test_no_execution_or_mutation(self):
        code = self._code()
        for bad in ("source_apply", "patch_apply", "apply_patch", "run_do_continue",
                    "approve_intent", "create_pr", "git commit", "git push",
                    "add_patch_intent", "add_proposed_task", ".tasks.append",
                    "run_local_advisor", "intake_provider_repair"):
            assert bad not in code, f"forbidden execution token: {bad}"

    def test_export_has_no_raw_fields(self):
        from packages.orchestration.builder_routing import BuilderRoutingDecision
        d = export_builder_routing_json(BuilderRoutingDecision(routing_id="r", job_id="j"))
        for forbidden in ("raw", "prompt", "response", "diff", "source", "stdout", "stderr"):
            assert forbidden not in d


# ---------------------------------------------------------------------------
# Idempotency + no-job safety
# ---------------------------------------------------------------------------


class TestSelectorBasics:
    def test_missing_job_safe(self, env):
        d = select_builder_routing_decision(_req(str(uuid4())), data_dir=env)
        assert d.selected_tier == BuilderRoutingTier.NO_SAFE_ROUTE
        assert d.stop_reason == BuilderRoutingStopReason.JOB_NOT_FOUND

    def test_idempotent_reuse(self, env):
        jid, fid = _make_job(env)
        a = select_builder_routing_decision(_req(jid, fid), data_dir=env)
        b = select_builder_routing_decision(_req(jid, fid), data_dir=env)
        assert a.routing_id == b.routing_id
        c = select_builder_routing_decision(_req(jid, fid, new=True), data_dir=env)
        assert c.routing_id != a.routing_id
