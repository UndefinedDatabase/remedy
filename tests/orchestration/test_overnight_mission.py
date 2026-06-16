"""Overnight Mission Contract + Review/Repair Spine v0 tests (Steps 1854/1855).

Unit (models, validation, storage, contract creation, review-as-blocker, evaluation satisfied/blocked,
state machine, next actions, integrity, audit, redaction) + architecture guards. METADATA + STATE-
MACHINE + EVALUATION only — nothing here executes a worker, runs a test, or calls a provider.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from packages.orchestration import overnight_mission as om


def _review_file(tmp_path: Path, verdict: str, *, findings: str = "") -> Path:
    f = tmp_path / "live_review.md"
    f.write_text(f"## Verdict\n{verdict}\n\n## Findings\n{findings}\n")
    return f


@pytest.fixture()
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"; d.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    return d


# ---------------------------------------------------------------------------
# Models + validation
# ---------------------------------------------------------------------------


class TestModels:
    def test_contract_roundtrip_scrubs_goal(self):
        c = om.MissionContract(contract_id="msn-1", job_id="j", user_goal="x" * 500,
                               acceptance_criteria=["a"])
        d = om.export_mission_contract_json(c)
        assert len(d["user_goal"]) <= 301 and d["schema_version"]

    def test_validate_contract(self):
        c = om.MissionContract(contract_id="", required_gates=["bogus_gate"])
        errs = om.validate_mission_contract(c)
        assert any("contract_id" in e for e in errs)
        assert any("unknown required_gates" in e for e in errs)


# ---------------------------------------------------------------------------
# Storage + creation
# ---------------------------------------------------------------------------


class TestStorageCreation:
    def test_create_no_acceptance_needs_user(self, env):
        c = om.create_mission_contract_from_job("j1", user_goal="Fix bug", data_dir=env)
        assert c.contract_id and c.acceptance_criteria == []
        loaded = om.load_mission_contract(c.contract_id, data_dir=env)
        assert loaded is not None and loaded["contract_id"] == c.contract_id

    def test_conservative_defaults(self, env):
        c = om.create_mission_contract_from_job("j2", data_dir=env)
        assert c.require_clean_review is True
        assert c.require_tests_green is False  # no real test execution exists
        assert om.GATE_CLEAN_REVIEW in c.required_gates

    def test_gates_set_when_requested(self, env):
        c = om.create_mission_contract_from_job(
            "j3", required_gates=[om.GATE_CLEAN_REVIEW, om.GATE_TESTS_GREEN, om.GATE_PROOF_CHAIN],
            data_dir=env)
        assert c.require_tests_green is True and c.require_proof_chain is True

    def test_corrupt_contract_skipped(self, env):
        f = env / "workspaces" / "jC" / "overnight_mission" / "msn-bad" / "contract.json"
        f.parent.mkdir(parents=True)
        f.write_text("{ not json")
        assert om.list_mission_contracts(job_id="jC", data_dir=env) == []


# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------


class TestEvaluation:
    def test_needs_acceptance_criteria(self, env, monkeypatch):
        monkeypatch.setenv("REMEDY_REVIEW_FILE", str(_review_file(env.parent, "PASS")))
        c = om.create_mission_contract_from_job("j", user_goal="x", data_dir=env)
        e = om.evaluate_mission_contract(c, data_dir=env)
        assert e.status == om.MissionStatus.NEEDS_USER_ACCEPTANCE_CRITERIA
        assert e.satisfied is False and e.user_decision_required is True

    def test_satisfied_when_clean(self, env, monkeypatch):
        monkeypatch.setenv("REMEDY_REVIEW_FILE", str(_review_file(env.parent, "PASS")))
        c = om.create_mission_contract_from_job("j", acceptance_criteria=["done"], data_dir=env)
        e = om.evaluate_mission_contract(c, data_dir=env)
        # No job/ledger → 0 open tasks, 0 failed tests; clean review; clean-review gate only → satisfied
        assert e.satisfied is True
        assert e.status == om.MissionStatus.CONTRACT_SATISFIED
        assert e.phase == om.MissionPhase.SATISFIED

    def test_open_high_finding_blocks(self, env, monkeypatch):
        rf = ("### R-0001: x\n- **Status**: Open\n- **Severity**: High\n")
        monkeypatch.setenv("REMEDY_REVIEW_FILE", str(_review_file(env.parent, "FAIL", findings=rf)))
        c = om.create_mission_contract_from_job("j", acceptance_criteria=["done"], data_dir=env)
        e = om.evaluate_mission_contract(c, data_dir=env)
        assert e.satisfied is False
        assert e.status == om.MissionStatus.WAITING_FOR_REVIEW
        assert e.open_review_findings >= 1

    def test_pending_verdict_blocks(self, env, monkeypatch):
        monkeypatch.setenv("REMEDY_REVIEW_FILE", str(_review_file(env.parent, "PENDING")))
        c = om.create_mission_contract_from_job("j", acceptance_criteria=["done"], data_dir=env)
        e = om.evaluate_mission_contract(c, data_dir=env)
        assert e.satisfied is False
        assert any("not PASS" in r for r in e.blocked_reasons)

    def test_missing_proof_gate_blocks(self, env, monkeypatch):
        monkeypatch.setenv("REMEDY_REVIEW_FILE", str(_review_file(env.parent, "PASS")))
        c = om.create_mission_contract_from_job(
            "j", acceptance_criteria=["done"],
            required_gates=[om.GATE_CLEAN_REVIEW, om.GATE_PROOF_CHAIN], data_dir=env)
        e = om.evaluate_mission_contract(c, data_dir=env)
        assert e.satisfied is False
        assert any("proof_chain" in m for m in e.missing_proofs)

    def test_never_satisfied_without_acceptance_even_if_clean(self, env, monkeypatch):
        monkeypatch.setenv("REMEDY_REVIEW_FILE", str(_review_file(env.parent, "PASS")))
        c = om.create_mission_contract_from_job("j", data_dir=env)
        e = om.evaluate_mission_contract(c, data_dir=env)
        assert e.satisfied is False


# ---------------------------------------------------------------------------
# Next actions + state machine
# ---------------------------------------------------------------------------


class TestNextActions:
    def test_required_vs_optional_separation(self, env, monkeypatch):
        rf = ("### R-0001: x\n- **Status**: Open\n- **Severity**: High\n")
        monkeypatch.setenv("REMEDY_REVIEW_FILE", str(_review_file(env.parent, "FAIL", findings=rf)))
        c = om.create_mission_contract_from_job("j", acceptance_criteria=["done"], data_dir=env)
        e = om.evaluate_mission_contract(c, data_dir=env)
        assert e.required_next_actions  # blockers present
        assert e.optional_next_ideas == []  # no optional ideas while unsatisfied
        for a in e.required_next_actions:
            assert a["command"].startswith("remedy ")

    def test_next_actions_catalog_valid(self, env, monkeypatch):
        monkeypatch.setenv("REMEDY_REVIEW_FILE", str(_review_file(env.parent, "PENDING")))
        from apps.cli.command_catalog import CATALOG
        c = om.create_mission_contract_from_job("j", acceptance_criteria=["done"], data_dir=env)
        e = om.evaluate_mission_contract(c, data_dir=env)
        # Each emitted action's "group subcommand" must map to a real catalog command_id.
        groups = {(cmd.group_id, cmd.subcommand) for cmd in CATALOG}
        for action in e.next_safe_actions:
            toks = action.split()
            assert toks[0] == "remedy"
            assert (toks[1], toks[2]) in groups, f"non-catalog action: {action}"

    def test_state_machine_user_decision(self, env, monkeypatch):
        monkeypatch.setenv("REMEDY_REVIEW_FILE", str(_review_file(env.parent, "PASS")))
        c = om.create_mission_contract_from_job("j", data_dir=env)
        e = om.evaluate_mission_contract(c, data_dir=env)
        assert om.mission_state_machine(e) == om.MissionPhase.USER_DECISION


# ---------------------------------------------------------------------------
# Integrity + audit
# ---------------------------------------------------------------------------


class TestIntegrity:
    def test_real_evaluations_pass(self, env, monkeypatch):
        monkeypatch.setenv("REMEDY_REVIEW_FILE", str(_review_file(env.parent, "PASS")))
        c = om.create_mission_contract_from_job("j", acceptance_criteria=["done"], data_dir=env)
        om.evaluate_mission_contract(c, data_dir=env, persist=True)
        ig = om.mission_integrity(data_dir=env)
        assert ig["passed"] is True

    def test_audit_satisfied_with_open_findings(self):
        bad = {"contract_id": "c", "satisfied": True, "open_review_findings": 2}
        codes = {v["code"] for v in om.audit_evaluation_safety(bad)}
        assert "satisfied_with_open_findings" in codes

    def test_audit_satisfied_with_missing_gates(self):
        bad = {"contract_id": "c", "satisfied": True, "missing_proofs": ["proof_chain"]}
        codes = {v["code"] for v in om.audit_evaluation_safety(bad)}
        assert "satisfied_with_missing_gates" in codes

    def test_audit_satisfied_with_open_tasks(self):
        bad = {"contract_id": "c", "satisfied": True, "open_tasks": 3}
        codes = {v["code"] for v in om.audit_evaluation_safety(bad)}
        assert "satisfied_with_open_tasks" in codes

    def test_integrity_scans_supplied(self):
        bad = {"contract_id": "c", "satisfied": True, "failed_tests": 1}
        ig = om.mission_integrity(evaluations=[bad])
        assert ig["passed"] is False


# ---------------------------------------------------------------------------
# Redaction
# ---------------------------------------------------------------------------


class TestRedaction:
    def test_no_raw_or_paths(self, env, monkeypatch):
        monkeypatch.setenv("REMEDY_REVIEW_FILE", str(_review_file(env.parent, "PASS")))
        # user_goal with a real secret pattern + absolute path → both scrubbed by _scrub_public.
        c = om.create_mission_contract_from_job(
            "j", user_goal="password: hunter2secretvalue at /home/user/.env",
            acceptance_criteria=["done"], data_dir=env)
        d = c.to_dict()
        assert "hunter2secretvalue" not in d["user_goal"]
        assert "/home/user" not in d["user_goal"]
        e = om.evaluate_mission_contract(c, data_dir=env)
        blob = json.dumps(e.to_dict()).lower() + json.dumps(d).lower()
        for marker in ("hunter2secretvalue", "-----begin", "traceback"):
            assert marker not in blob, marker


# ---------------------------------------------------------------------------
# Architecture guards (Step 1854)
# ---------------------------------------------------------------------------


class TestArchitectureGuards:
    def _src(self) -> str:
        p = Path(__file__).resolve().parents[2] / "packages" / "orchestration" / "overnight_mission.py"
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
                    "import openai", "import anthropic", "import tiktoken", "import numpy",
                    "faiss", "chromadb"):
            assert bad not in src, bad

    def test_no_execution_or_apply(self):
        src = self._src()
        for bad in ("os.system", "Popen", "check_output", "do_continue(", "apply_patch(",
                    ".approve(", "os.fork", "eval(", "exec("):
            assert bad not in src, bad
