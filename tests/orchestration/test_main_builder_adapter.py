"""Unit tests for Main Builder Adapter v0 (Steps 1961-2025).

Covers: models, storage, registry, request packages, session lifecycle, fixture builder,
integrity checks, mission signal, adapter recommendation, architecture guards.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from uuid import uuid4

import pytest

from packages.orchestration import main_builder_adapter as mba


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"
    d.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    return d


def _job(env, *, name="test-job"):
    from packages.core.models import Job, RunState, Task
    from packages.orchestration.storage import save_job
    job = Job(id=uuid4(), name=name, user_prompt="fix", state=RunState.RUNNING,
              tasks=[Task(description="t")], metadata={"target_repo": str(env / "repo")})
    save_job(job, root=env)
    return str(job.id)


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------


class TestModels:
    def test_adapter_spec_roundtrip(self):
        spec = mba.BuilderAdapterSpec(adapter_id="test", label="Test", kind="claude_code")
        d = spec.to_dict()
        assert d["adapter_id"] == "test"
        assert d["allows_direct_repo_write"] is False  # HARD invariant
        rt = mba.BuilderAdapterSpec.from_dict(d)
        assert rt.adapter_id == "test"
        assert rt.allows_direct_repo_write is False

    def test_adapter_spec_forces_no_direct_repo_write(self):
        spec = mba.BuilderAdapterSpec(adapter_id="bad", allows_direct_repo_write=True)
        d = spec.to_dict()
        assert d["allows_direct_repo_write"] is False

    def test_request_package_scrubs(self):
        pkg = mba.BuilderRequestPackage(
            package_id="p1", goal_summary="fix /home/user/secret sk-ant-xxxx bug",
        )
        d = pkg.to_dict()
        assert "/home/" not in d["goal_summary"]
        assert "sk-ant" not in d["goal_summary"]

    def test_session_record_roundtrip(self):
        sr = mba.BuilderSessionRecord(session_id="s1", status="running")
        d = sr.to_dict()
        rt = mba.BuilderSessionRecord.from_dict(d)
        assert rt.session_id == "s1"
        assert rt.status == "running"

    def test_session_record_scrubs_blocking_reasons(self):
        sr = mba.BuilderSessionRecord(
            session_id="s1", blocking_reasons=["secret sk-ant-key leaked"]
        )
        d = sr.to_dict()
        blob = json.dumps(d).lower()
        assert "sk-ant" not in blob


# ---------------------------------------------------------------------------
# Registry tests
# ---------------------------------------------------------------------------


class TestRegistry:
    def test_defaults_all_real_disabled(self):
        specs = mba.default_builder_adapter_specs()
        real = [s for s in specs if s.kind in mba._REAL_ADAPTER_KINDS]
        assert all(not s.enabled for s in real)
        assert all(s.requires_operator_approval for s in real)
        assert all(s.requires_external_sandbox_intake for s in real)
        assert all(not s.allows_direct_repo_write for s in real)

    def test_fixture_adapter_disabled_by_default(self):
        specs = mba.default_builder_adapter_specs()
        fixture = [s for s in specs if s.kind == mba.BuilderAdapterKind.FIXTURE_BUILDER]
        assert len(fixture) == 1
        assert not fixture[0].enabled
        assert fixture[0].mode == mba.BuilderAdapterMode.FIXTURE_ONLY

    def test_list_returns_defaults_when_no_stored(self, env):
        specs = mba.list_builder_adapter_specs(env)
        assert len(specs) == 5
        assert all(not s.get("allows_direct_repo_write") for s in specs)

    def test_save_and_load(self, env):
        spec = mba.BuilderAdapterSpec(adapter_id="test-save", label="X", kind="claude_code")
        ok = mba.save_builder_adapter_spec(spec, env)
        assert ok
        loaded = mba.get_builder_adapter_spec("test-save", env)
        assert loaded is not None
        assert loaded["adapter_id"] == "test-save"

    def test_save_scrubs_secret_from_storage(self, env):
        spec = mba.BuilderAdapterSpec(adapter_id="scrub-test", label="ok", notes="has sk-ant-secret123456789 inside")
        ok = mba.save_builder_adapter_spec(spec, env)
        assert ok
        loaded = mba.get_builder_adapter_spec("scrub-test", env)
        assert "sk-ant" not in json.dumps(loaded)

    def test_disabled_adapter_cannot_be_selected_for_session(self, env):
        jid = _job(env)
        pkg = mba.build_builder_request_package(jid, adapter_id="claude-code-v0", data_dir=env)
        session = mba.create_builder_session(pkg.package_id, "claude-code-v0", job_id=jid, data_dir=env)
        assert session.status == mba.BuilderSessionStatus.BLOCKED
        assert "adapter_disabled" in session.blocking_reasons


# ---------------------------------------------------------------------------
# Request package tests
# ---------------------------------------------------------------------------


class TestRequestPackage:
    def test_minimal_package(self, env):
        jid = _job(env)
        pkg = mba.build_builder_request_package(jid, data_dir=env)
        assert pkg.package_id
        assert pkg.job_id == jid
        assert pkg.forbidden_actions
        assert pkg.expected_output_contract

    def test_unknown_token_requires_approval(self, env):
        jid = _job(env)
        pkg = mba.build_builder_request_package(jid, token_hint={"estimated_token_band": "unknown"}, data_dir=env)
        assert pkg.requires_human_approval is True

    def test_oversized_token_requires_approval(self, env):
        jid = _job(env)
        pkg = mba.build_builder_request_package(
            jid, token_hint={"estimated_token_band": "very_high", "budget_status": "over_budget"},
            data_dir=env,
        )
        assert pkg.requires_human_approval is True

    def test_package_redaction(self, env):
        jid = _job(env)
        pkg = mba.build_builder_request_package(
            jid, context_pack={"safe_summary": "/home/user/secret sk-ant-key123456789 Traceback"},
            data_dir=env,
        )
        blob = json.dumps(pkg.to_dict()).lower()
        assert "sk-ant" not in blob
        assert "/home/" not in blob

    def test_expected_output_contract_present(self, env):
        jid = _job(env)
        pkg = mba.build_builder_request_package(jid, data_dir=env)
        assert "UNTRUSTED" in pkg.expected_output_contract
        assert "NEVER applied automatically" in pkg.expected_output_contract

    def test_route_reason_present(self, env):
        jid = _job(env)
        pkg = mba.build_builder_request_package(jid, route_reason="test_reason", data_dir=env)
        assert "test_reason" in pkg.to_dict()["route_reason"]


# ---------------------------------------------------------------------------
# Session lifecycle tests
# ---------------------------------------------------------------------------


class TestSessionLifecycle:
    def test_create_with_enabled_adapter(self, env):
        jid = _job(env)
        spec = mba.BuilderAdapterSpec(adapter_id="test-a", kind="claude_code", enabled=True,
                                       mode="operator_launched", requires_operator_approval=True)
        mba.save_builder_adapter_spec(spec, env)
        session = mba.create_builder_session("pkg1", "test-a", job_id=jid, data_dir=env)
        assert session.status == mba.BuilderSessionStatus.WAITING_FOR_OPERATOR

    def test_record_output(self, env):
        jid = _job(env)
        spec = mba.BuilderAdapterSpec(adapter_id="test-b", kind="claude_code", enabled=True,
                                       mode="operator_launched", requires_operator_approval=False)
        mba.save_builder_adapter_spec(spec, env)
        session = mba.create_builder_session("pkg2", "test-b", job_id=jid, data_dir=env)
        updated = mba.record_builder_session_output(session.session_id, candidate_artifact_ref="ref1", data_dir=env)
        assert updated.status == mba.BuilderSessionStatus.CANDIDATE_RECEIVED
        assert updated.candidate_artifact_ref == "ref1"

    def test_record_blocked(self, env):
        jid = _job(env)
        spec = mba.BuilderAdapterSpec(adapter_id="test-c", kind="claude_code", enabled=True,
                                       mode="operator_launched", requires_operator_approval=False)
        mba.save_builder_adapter_spec(spec, env)
        session = mba.create_builder_session("pkg3", "test-c", job_id=jid, data_dir=env)
        updated = mba.record_builder_session_blocked(session.session_id, reason="test_block", data_dir=env)
        assert updated.status == mba.BuilderSessionStatus.BLOCKED
        assert "test_block" in updated.blocking_reasons

    def test_intake_complete_does_not_satisfy_repair(self, env):
        jid = _job(env)
        spec = mba.BuilderAdapterSpec(adapter_id="test-d", kind="claude_code", enabled=True,
                                       mode="operator_launched", requires_operator_approval=False)
        mba.save_builder_adapter_spec(spec, env)
        session = mba.create_builder_session("pkg4", "test-d", job_id=jid, repair_id="r1", data_dir=env)
        mba.record_builder_session_output(session.session_id, candidate_artifact_ref="ref", data_dir=env)
        updated = mba.record_builder_session_intake_complete(session.session_id, sandbox_submission_id="sub1", data_dir=env)
        assert updated.status == mba.BuilderSessionStatus.COMPLETED_INTAKE_ONLY
        # Next action should point to repair evaluate, not claim done.
        assert "repair evaluate" in updated.next_safe_action

    def test_load_and_list(self, env):
        jid = _job(env)
        spec = mba.BuilderAdapterSpec(adapter_id="test-e", kind="claude_code", enabled=True,
                                       mode="operator_launched", requires_operator_approval=False)
        mba.save_builder_adapter_spec(spec, env)
        s1 = mba.create_builder_session("p1", "test-e", job_id=jid, data_dir=env)
        s2 = mba.create_builder_session("p2", "test-e", job_id=jid, data_dir=env)
        loaded = mba.load_builder_session(s1.session_id, env)
        assert loaded is not None
        assert loaded.session_id == s1.session_id
        sessions = mba.list_builder_sessions(jid, env)
        assert len(sessions) >= 2


# ---------------------------------------------------------------------------
# Fixture builder tests
# ---------------------------------------------------------------------------


class TestFixtureBuilder:
    def _fixture_session(self, env):
        jid = _job(env)
        spec = mba.BuilderAdapterSpec(adapter_id="fixture-v0", kind="fixture_builder", enabled=True,
                                       mode="fixture_only", requires_operator_approval=False)
        mba.save_builder_adapter_spec(spec, env)
        return mba.create_builder_session("fp1", "fixture-v0", job_id=jid, data_dir=env), jid

    def test_fixture_success(self, env):
        session, _ = self._fixture_session(env)
        result = mba.run_fixture_builder(session.session_id, fixture_scenario="success", data_dir=env)
        assert result.status == mba.BuilderSessionStatus.CANDIDATE_RECEIVED
        assert result.candidate_artifact_ref

    def test_fixture_trust_rejected(self, env):
        session, _ = self._fixture_session(env)
        result = mba.run_fixture_builder(session.session_id, fixture_scenario="trust_rejected", data_dir=env)
        assert result.status == mba.BuilderSessionStatus.BLOCKED
        assert "trust_rejected" in result.blocking_reasons

    def test_fixture_blocked(self, env):
        session, _ = self._fixture_session(env)
        result = mba.run_fixture_builder(session.session_id, fixture_scenario="blocked", data_dir=env)
        assert result.status == mba.BuilderSessionStatus.BLOCKED

    def test_fixture_no_output(self, env):
        session, _ = self._fixture_session(env)
        result = mba.run_fixture_builder(session.session_id, fixture_scenario="no_output", data_dir=env)
        assert result.status == mba.BuilderSessionStatus.BLOCKED
        assert "no_output" in result.blocking_reasons

    def test_fixture_oversized_output(self, env):
        session, _ = self._fixture_session(env)
        result = mba.run_fixture_builder(session.session_id, fixture_scenario="oversized_output", data_dir=env)
        assert result.status == mba.BuilderSessionStatus.BLOCKED
        assert "oversized_output" in result.blocking_reasons

    def test_non_fixture_adapter_blocked(self, env):
        jid = _job(env)
        spec = mba.BuilderAdapterSpec(adapter_id="real-a", kind="claude_code", enabled=True,
                                       mode="operator_launched", requires_operator_approval=False)
        mba.save_builder_adapter_spec(spec, env)
        session = mba.create_builder_session("fp2", "real-a", job_id=jid, data_dir=env)
        result = mba.run_fixture_builder(session.session_id, data_dir=env)
        assert result.status == mba.BuilderSessionStatus.BLOCKED
        assert "not_fixture_adapter" in result.blocking_reasons

    def test_fixture_does_not_mark_repair_done(self, env):
        session, _ = self._fixture_session(env)
        result = mba.run_fixture_builder(session.session_id, fixture_scenario="success", data_dir=env)
        # candidate_received ≠ repaired — downstream gates still needed
        assert result.status != mba.BuilderSessionStatus.COMPLETED_INTAKE_ONLY


# ---------------------------------------------------------------------------
# Mission signal tests
# ---------------------------------------------------------------------------


class TestMissionSignal:
    def test_empty_sessions(self, env):
        jid = _job(env)
        sig = mba.builder_adapter_mission_signal(jid, env)
        assert sig["builder_satisfies_mission"] is False
        assert sig["has_active_sessions"] is False

    def test_blocked_session_creates_user_decision(self, env):
        jid = _job(env)
        spec = mba.BuilderAdapterSpec(adapter_id="test-m", kind="claude_code", enabled=True,
                                       mode="operator_launched", requires_operator_approval=False)
        mba.save_builder_adapter_spec(spec, env)
        session = mba.create_builder_session("mp1", "test-m", job_id=jid, data_dir=env)
        mba.record_builder_session_blocked(session.session_id, reason="test", data_dir=env)
        sig = mba.builder_adapter_mission_signal(jid, env)
        assert sig["blocked_session_count"] == 1
        assert sig["user_decision_required"] is True
        assert sig["builder_satisfies_mission"] is False


# ---------------------------------------------------------------------------
# Adapter recommendation tests
# ---------------------------------------------------------------------------


class TestRecommendation:
    def test_cheap_prefers_local(self):
        r = mba.recommend_builder_adapter("j1", token_hint={
            "estimated_token_band": "low", "local_first_recommended": True,
        })
        assert r["recommendation"] == "prefer_local_worker"

    def test_unknown_requires_human(self):
        r = mba.recommend_builder_adapter("j1", token_hint={
            "estimated_token_band": "unknown",
        })
        assert r["recommendation"] == "human_decision_required"
        assert r["requires_human_approval"] is True

    def test_no_enabled_adapter(self, env):
        r = mba.recommend_builder_adapter("j1", token_hint={
            "estimated_token_band": "medium", "budget_status": "within_budget",
        }, data_dir=env)
        assert r["recommendation"] == "no_enabled_adapter"

    def test_enabled_adapter_recommended(self, env):
        spec = mba.BuilderAdapterSpec(adapter_id="rec-a", kind="claude_code", enabled=True,
                                       mode="operator_launched")
        mba.save_builder_adapter_spec(spec, env)
        r = mba.recommend_builder_adapter("j1", token_hint={
            "estimated_token_band": "medium", "budget_status": "within_budget",
        }, data_dir=env)
        assert r["recommendation"] == "adapter_available"
        assert r["recommended_adapter_id"] == "rec-a"


# ---------------------------------------------------------------------------
# Integrity tests
# ---------------------------------------------------------------------------


class TestIntegrity:
    def test_defaults_pass(self, env):
        result = mba.builder_adapter_integrity(env)
        assert result["passed"] is True

    def test_direct_repo_write_fails(self):
        codes = {c["code"] for c in mba.audit_adapter_spec_safety(
            {"adapter_id": "bad", "kind": "claude_code", "allows_direct_repo_write": True})}
        assert "direct_repo_write_enabled" in codes

    def test_real_adapter_bypasses_sandbox(self):
        codes = {c["code"] for c in mba.audit_adapter_spec_safety(
            {"adapter_id": "bad", "kind": "claude_code", "requires_external_sandbox_intake": False})}
        assert "real_adapter_bypasses_sandbox_intake" in codes

    def test_secret_in_spec(self):
        codes = {c["code"] for c in mba.audit_adapter_spec_safety(
            {"adapter_id": "bad", "kind": "claude_code", "notes": "sk-ant-secret123456789"})}
        assert "secret_or_raw_in_adapter_spec" in codes

    def test_absolute_path_in_spec(self):
        codes = {c["code"] for c in mba.audit_adapter_spec_safety(
            {"adapter_id": "bad", "kind": "claude_code", "notes": "/home/user/secret"})}
        assert "absolute_path_in_adapter_spec" in codes

    def test_unknown_kind(self):
        codes = {c["code"] for c in mba.audit_adapter_spec_safety(
            {"adapter_id": "bad", "kind": "nonexistent"})}
        assert "unknown_adapter_kind" in codes

    def test_unknown_mode(self):
        codes = {c["code"] for c in mba.audit_adapter_spec_safety(
            {"adapter_id": "bad", "kind": "claude_code", "mode": "turbo_blast"})}
        assert "unknown_adapter_mode" in codes

    def test_real_adapter_enabled_without_approval(self):
        codes = {c["code"] for c in mba.audit_adapter_spec_safety(
            {"adapter_id": "bad", "kind": "claude_code", "enabled": True,
             "requires_operator_approval": False})}
        assert "real_adapter_enabled_without_approval" in codes

    def test_fixture_in_production_mode(self):
        codes = {c["code"] for c in mba.audit_adapter_spec_safety(
            {"adapter_id": "bad", "kind": "fixture_builder", "mode": "operator_launched"})}
        assert "fixture_in_production_mode" in codes

    def test_session_raw_leak(self):
        codes = {c["code"] for c in mba.audit_session_safety(
            {"session_id": "s1", "status": "running", "next_safe_action": "",
             "blocking_reasons": ["sk-ant-key12345678901234"]})}
        assert "raw_or_secret_in_session" in codes

    def test_session_unknown_status(self):
        codes = {c["code"] for c in mba.audit_session_safety(
            {"session_id": "s1", "status": "hyper_running", "next_safe_action": ""})}
        assert "unknown_session_status" in codes

    def test_session_non_catalog_action(self):
        codes = {c["code"] for c in mba.audit_session_safety(
            {"session_id": "s1", "status": "running",
             "next_safe_action": "rm -rf /"})}
        assert "non_catalog_next_action" in codes

    def test_clean_session_passes(self):
        violations = mba.audit_session_safety(
            {"session_id": "s1", "status": "running",
             "next_safe_action": "remedy builder session-show s1 --json"})
        assert len(violations) == 0

    # Negative: BLOCKED adapter correctly not flagged as unknown.
    def test_known_status_no_flag(self):
        for st in mba._ALL_SESSION_STATUSES:
            violations = mba.audit_session_safety(
                {"session_id": "s1", "status": st, "next_safe_action": ""})
            codes = {v["code"] for v in violations}
            assert "unknown_session_status" not in codes


# ---------------------------------------------------------------------------
# Architecture guards
# ---------------------------------------------------------------------------


class TestArchitectureGuards:
    def _src(self) -> str:
        p = Path(__file__).resolve().parents[2] / "packages" / "orchestration" / "main_builder_adapter.py"
        src = p.read_text(encoding="utf-8")
        src = re.sub(r'"""[\s\S]*?"""', "", src)
        src = re.sub(r"'''[\s\S]*?'''", "", src)
        src = re.sub(r'"(?:\\.|[^"\\])*"', '""', src)
        src = re.sub(r"'(?:\\.|[^'\\])*'", "''", src)
        return src

    def test_no_forbidden_imports(self):
        src = self._src()
        for bad in ("import subprocess", "subprocess.", "shell=True", "os.system", "Popen",
                    "import requests", "import socket", "import ollama", "import openai",
                    "import anthropic", "faiss", "chromadb", "import numpy"):
            assert bad not in src, bad

    def test_no_execution_or_apply(self):
        src = self._src()
        for bad in ("auto_apply", "auto_approve", "git push", "git commit", "git merge",
                    "do continue", "execute_worker", "run_provider", "call_model",
                    "start_ollama", "eval(", "exec(", "os.popen"):
            assert bad not in src, bad
