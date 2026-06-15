"""Runtime CLI tests for `remedy token` and `remedy context-pack` (Step 1776).

Subprocess tests. ESTIMATES + METADATA only — no execution/apply/approve/test. Safe JSON, safe
errors, no tracebacks, no raw context.
"""
from __future__ import annotations

import json

import pytest

from tests.cli.runtime_helpers import run_grouped_cli


@pytest.fixture()
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"; d.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    return d


def test_budget_show_default(env):
    r = run_grouped_cli(["token", "budget-show", "job-1", "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["max_context_tokens"] > 0 and "Traceback" not in r.stdout


def test_budget_set_roundtrip(env):
    r = run_grouped_cli(["token", "budget-set", "job-2", "--max-context-tokens", "16000",
                         "--prefer-local-under-tokens", "5000", "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["saved"] is True and d["max_context_tokens"] == 16000
    r2 = run_grouped_cli(["token", "budget-show", "job-2", "--json"], env)
    assert json.loads(r2.stdout)["prefer_local_under_tokens"] == 5000


def test_budget_set_invalid_number(env):
    r = run_grouped_cli(["token", "budget-set", "job-3", "--max-context-tokens", "abc", "--json"], env)
    assert r.returncode == 1
    assert "Traceback" not in r.stderr

    r2 = run_grouped_cli(["token", "budget-set", "job-3", "--max-context-tokens", "0", "--json"], env)
    assert r2.returncode == 1


def test_estimate_no_job_safe(env):
    r = run_grouped_cli(["token", "estimate", "no-such-job", "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["estimated"] is True and "no_context_inspection_available" in d["warnings"]
    assert "Traceback" not in r.stdout


def test_economy_report(env):
    r = run_grouped_cli(["token", "economy-report", "job-4", "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert "decision" in d and d["estimated"] is True
    # next actions are catalog-valid and never execution commands
    for a in d.get("next_safe_actions", []):
        assert a.startswith("remedy ") and " run" not in a


def test_context_pack_recommend(env):
    r = run_grouped_cli(["context-pack", "recommend", "job-5", "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["recommended_pack_kind"] in (
        "minimal", "focused", "balanced", "full", "defer_for_human")
    assert d["memory_candidates_persisted"] is False
    assert "Traceback" not in r.stdout


def test_json_purity_no_raw(env):
    r = run_grouped_cli(["token", "economy-report", "job-6", "--json"], env)
    blob = r.stdout.lower()
    for marker in ("sk-ant", "/home/", "/users/", "price_usd", "cost_usd", "traceback"):
        assert marker not in blob, marker
