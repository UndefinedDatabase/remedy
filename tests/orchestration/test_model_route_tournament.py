"""Model/Route Tournament Harness v0 tests (Steps 1814/1815).

Unit (models, competitor discovery, evidence gathering, scoring hard ceilings, report generation,
storage, integrity, audit, redaction) + architecture guards. EVIDENCE + SCORING + REPORTING only —
nothing here executes a worker.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from uuid import uuid4

import pytest

from packages.orchestration import model_route_tournament as mrt


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _competitor(**kw):
    base = dict(competitor_id="cmp-1", route_id="r", worker_id="w", worker_kind="local_candidate",
                enabled=True, eligible=True, cost_tier="cheap", risk_tier="medium",
                approval_required=False, is_placeholder=False)
    base.update(kw)
    return mrt.TournamentCompetitor(**base)


def _evidence(cid="cmp-1", *, run_count=0, proof=0.0, reject=0.0, loop=0, subs=0, token_band="low"):
    ev = mrt.TournamentEvidence(competitor_id=cid)
    ev.candidate_quality_summary = {"run_count": run_count, "proof_verified_rate": proof,
                                    "rejection_rate": reject, "loop_risk": loop}
    ev.token_economy_summary = {"estimated_token_band": token_band}
    ev.submission_summary = {"submission_count": subs}
    return ev


@pytest.fixture()
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"; d.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    return d


# ---------------------------------------------------------------------------
# Models + serialization
# ---------------------------------------------------------------------------


class TestModels:
    def test_report_roundtrip(self):
        r = mrt.TournamentReport(tournament_id="trn-1", job_id="j", status=mrt.TournamentStatus.COMPLETE)
        d = mrt.export_tournament_report_json(r)
        assert d["tournament_id"] == "trn-1" and d["schema_version"]

    def test_spec_export(self):
        s = mrt.TournamentSpec(tournament_id="trn-2", worker_ids=["a", "b"])
        assert mrt.export_tournament_spec_json(s)["worker_ids"] == ["a", "b"]


# ---------------------------------------------------------------------------
# Competitor discovery
# ---------------------------------------------------------------------------


class TestCompetitors:
    def test_discovers_registry_workers(self, env):
        comps = mrt.list_tournament_competitors("j", task_type="repair", data_dir=env)
        wids = {c.worker_id for c in comps}
        assert "local.candidate_generator" in wids and "external.builder_package" in wids
        assert "ollama.placeholder" in wids

    def test_placeholders_marked(self, env):
        comps = {c.worker_id: c for c in mrt.list_tournament_competitors("j", data_dir=env)}
        assert comps["ollama.placeholder"].is_placeholder is True
        assert comps["cloud.placeholder"].eligible is False  # disabled → ineligible

    def test_blocked_worker_ineligible(self, env):
        from packages.orchestration.worker_registry import default_route_policy, save_route_policy
        p = default_route_policy("jB"); p.blocked_worker_ids = ["local.candidate_generator"]
        save_route_policy(p, data_dir=env)
        comps = {c.worker_id: c for c in mrt.list_tournament_competitors("jB", data_dir=env)}
        assert comps["local.candidate_generator"].eligible is False


# ---------------------------------------------------------------------------
# Scoring hard ceilings
# ---------------------------------------------------------------------------


class TestScoringCeilings:
    def test_insufficient_evidence(self):
        s = mrt._score_competitor(_competitor(), _evidence(run_count=0, subs=0), "j")
        assert s.score_band == mrt.ScoreBand.INSUFFICIENT_EVIDENCE

    def test_ineligible_blocked(self):
        s = mrt._score_competitor(_competitor(eligible=False, blocked_reason="disabled"),
                                  _evidence(run_count=5, proof=1.0), "j")
        assert s.score_band == mrt.ScoreBand.BLOCKED

    def test_rejected_history_not_strong(self):
        s = mrt._score_competitor(_competitor(cost_tier="free"),
                                  _evidence(run_count=10, proof=0.1, reject=0.6), "j")
        assert s.score_band in (mrt.ScoreBand.WEAK, mrt.ScoreBand.BLOCKED)

    def test_cheap_but_unsafe_cannot_win(self):
        # cheap/free cost but high rejection → must not be strong/excellent
        s = mrt._score_competitor(_competitor(cost_tier="free"),
                                  _evidence(run_count=10, proof=0.0, reject=0.9), "j")
        assert s.score_band == mrt.ScoreBand.BLOCKED

    def test_no_proof_not_excellent(self):
        s = mrt._score_competitor(_competitor(),
                                  _evidence(run_count=10, proof=0.0, reject=0.1), "j")
        assert s.score_band != mrt.ScoreBand.EXCELLENT

    def test_placeholder_not_winner_band(self):
        s = mrt._score_competitor(_competitor(is_placeholder=True),
                                  _evidence(run_count=10, proof=1.0, reject=0.0), "j")
        assert s.score_band not in (mrt.ScoreBand.EXCELLENT, mrt.ScoreBand.STRONG)

    def test_strong_with_proof(self):
        s = mrt._score_competitor(_competitor(approval_required=True),
                                  _evidence(run_count=10, proof=0.8, reject=0.0), "j")
        assert s.score_band in (mrt.ScoreBand.STRONG, mrt.ScoreBand.EXCELLENT)

    def test_excellent_requires_known_band_and_no_approval(self):
        s = mrt._score_competitor(_competitor(approval_required=False),
                                  _evidence(run_count=10, proof=0.9, reject=0.0, token_band="low"), "j")
        assert s.score_band == mrt.ScoreBand.EXCELLENT


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------


class TestReport:
    def test_no_evidence_no_winner(self, env):
        rep = mrt.generate_tournament_report("j", task_type="repair", data_dir=env, persist=False)
        assert rep.winner_competitor_id == ""
        assert rep.status == mrt.TournamentStatus.INSUFFICIENT_EVIDENCE
        assert rep.confidence == "low"

    def test_report_has_safe_next_actions(self, env):
        rep = mrt.generate_tournament_report("j", data_dir=env, persist=False)
        for a in rep.next_safe_actions:
            assert a.startswith("remedy ") and " run" not in a

    def test_competitors_scored(self, env):
        rep = mrt.generate_tournament_report("j", data_dir=env, persist=False)
        assert len(rep.scores) == len(rep.competitors)
        assert all(s.rank >= 1 for s in rep.scores)


# ---------------------------------------------------------------------------
# Storage
# ---------------------------------------------------------------------------


class TestStorage:
    def test_save_load_list(self, env):
        rep = mrt.generate_tournament_report("jS", data_dir=env, persist=True)
        loaded = mrt.load_tournament_report(rep.tournament_id, data_dir=env)
        assert loaded is not None and loaded["tournament_id"] == rep.tournament_id
        assert len(mrt.list_tournament_reports(job_id="jS", data_dir=env)) == 1

    def test_corrupt_report_skipped(self, env):
        f = env / "workspaces" / "jC" / "model_route_tournament" / "trn-bad" / "report.json"
        f.parent.mkdir(parents=True)
        f.write_text("{ not json")
        assert mrt.list_tournament_reports(job_id="jC", data_dir=env) == []


# ---------------------------------------------------------------------------
# Integrity + audit
# ---------------------------------------------------------------------------


class TestIntegrity:
    def test_real_report_passes(self, env):
        mrt.generate_tournament_report("jI", data_dir=env, persist=True)
        ig = mrt.tournament_integrity(data_dir=env)
        assert ig["passed"] is True

    def test_audit_winner_with_insufficient_evidence(self):
        bad = {"tournament_id": "t", "status": "insufficient_evidence",
               "winner_competitor_id": "cmp-1", "scores": [], "competitors": []}
        codes = {v["code"] for v in mrt.audit_report_safety(bad)}
        assert "winner_with_insufficient_evidence" in codes

    def test_audit_placeholder_ranked_winner(self):
        bad = {"tournament_id": "t", "status": "complete", "winner_competitor_id": "cmp-1",
               "scores": [{"competitor_id": "cmp-1", "score_band": "strong"}],
               "competitors": [{"competitor_id": "cmp-1", "is_placeholder": True, "eligible": True}]}
        codes = {v["code"] for v in mrt.audit_report_safety(bad)}
        assert "placeholder_ranked_winner" in codes

    def test_audit_winner_not_winner_band(self):
        bad = {"tournament_id": "t", "status": "complete", "winner_competitor_id": "cmp-1",
               "scores": [{"competitor_id": "cmp-1", "score_band": "usable"}],
               "competitors": [{"competitor_id": "cmp-1", "eligible": True}]}
        codes = {v["code"] for v in mrt.audit_report_safety(bad)}
        assert "winner_not_winner_band" in codes

    def test_integrity_scans_supplied_reports(self):
        bad = {"tournament_id": "t", "status": "insufficient_evidence",
               "winner_competitor_id": "x", "scores": [], "competitors": []}
        ig = mrt.tournament_integrity(reports=[bad])
        assert ig["passed"] is False


# ---------------------------------------------------------------------------
# Redaction
# ---------------------------------------------------------------------------


class TestRedaction:
    def test_report_no_raw_or_paths(self, env):
        rep = mrt.generate_tournament_report("jR", data_dir=env, persist=False)
        blob = json.dumps(rep.to_dict()).lower()
        for marker in ("sk-ant", "/home/", "/users/", "api_key", "-----begin", "traceback"):
            assert marker not in blob, marker


# ---------------------------------------------------------------------------
# Architecture guards (Step 1815)
# ---------------------------------------------------------------------------


class TestArchitectureGuards:
    def _src(self) -> str:
        p = Path(__file__).resolve().parents[2] / "packages" / "orchestration" / "model_route_tournament.py"
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
