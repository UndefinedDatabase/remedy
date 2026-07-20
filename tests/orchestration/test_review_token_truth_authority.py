"""F2 (round 32) — the root token_truth is authoritative only when it equals the canonical aggregate
of the per-task token_accounting/provider_evidence. A forged root count or model that no task supports
BLOCKS, even though the final-verifier report reproduces the same contradictory input."""
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
_b = importlib.util.spec_from_file_location(
    "_brm_tta", REPO_ROOT / "scripts" / "build_review_manifest.py")
_brm = importlib.util.module_from_spec(_b); _b.loader.exec_module(_brm)
_e = importlib.util.spec_from_file_location(
    "_e2e_tta", REPO_ROOT / "tests" / "orchestration" / "test_review_authoritative_e2e.py")
_E2E = importlib.util.module_from_spec(_e); _e.loader.exec_module(_E2E)

pytestmark = pytest.mark.skipif(
    __import__("shutil").which("git") is None, reason="git required")


def _bundle(tmp_path):
    repo, base, head = _E2E._build_repo(tmp_path)
    ev, _s, _a = _E2E._write_evidence(repo, base, head, tmp_path / "evidence")
    return repo, ev


def _view(ev):
    return _brm._view_from_dir(str(ev))


class TestTokenTruthAuthority:
    def test_canonical_bundle_is_verified_equal(self, tmp_path):
        repo, ev = _bundle(tmp_path)
        os.chdir(repo)
        r = _brm._token_truth_authority(_view(ev))
        assert r["status"] == "VERIFIED_EQUAL" and r["equal"] is True

    @pytest.mark.parametrize("field,val", [
        ("provider_call_count", 1),
        ("prompt_trace_count", 1),
        ("cost_call_count", 1),
        ("actual_call_count", 1),
        ("builder_configured_model", "forged-model"),
        ("reviewer_configured_model", "forged-model"),
        ("model", "forged-model"),
        ("actual_model_verified", True),
        ("actual_available", True),
        ("measurement_confidence", "high"),
        ("total_cost_usd", 9.99),
    ])
    def test_forged_root_field_blocks(self, tmp_path, field, val):
        repo, ev = _bundle(tmp_path)
        os.chdir(repo)
        tt = json.loads((ev / "token_truth.json").read_text())
        tt[field] = val
        (ev / "token_truth.json").write_text(json.dumps(tt))
        r = _brm._token_truth_authority(_view(ev))
        assert r["status"] == "MISMATCH" and r["equal"] is False
        p0 = r["problems"][0]
        assert "not the aggregate" in p0 or "invalid" in p0

    def test_forged_root_blocks_full_build_manifest(self, tmp_path):
        # The reviewer's exact reproduction: forge root while every task says zero → not READY.
        repo, ev = _bundle(tmp_path)
        os.chdir(repo)
        tt = json.loads((ev / "token_truth.json").read_text())
        tt["provider_call_count"] = 1
        (ev / "token_truth.json").write_text(json.dumps(tt))
        man = _brm.build_manifest(str(ev), selection_mode="explicit")
        assert man["token_truth_authority"]["status"] == "MISMATCH"
        assert man["package_status"] != "READY_FOR_REVIEW"

    def test_unknown_root_field_blocks(self, tmp_path):
        repo, ev = _bundle(tmp_path)
        os.chdir(repo)
        tt = json.loads((ev / "token_truth.json").read_text())
        tt["surprise_field"] = 1
        (ev / "token_truth.json").write_text(json.dumps(tt))
        assert _brm._token_truth_authority(_view(ev))["status"] == "MISMATCH"

    def test_producer_failure_is_not_success(self, tmp_path, monkeypatch):
        repo, ev = _bundle(tmp_path)
        os.chdir(repo)
        import packages.orchestration.token_truth as tt
        monkeypatch.setattr(tt, "build_token_truth", lambda _d: (_ for _ in ()).throw(RuntimeError("x")))
        r = _brm._token_truth_authority(_view(ev))
        assert r["status"] == "PRODUCER_ERROR" and r["equal"] is False
