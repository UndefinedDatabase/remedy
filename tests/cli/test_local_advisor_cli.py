"""Runtime CLI tests for `remedy local-advisor` + `orchestrator decide --use-local-advisor`
(Step 1525).

Subprocess tests. Advisor disabled by default; a missing/unavailable local advisor must never
break deterministic orchestration. No real Ollama: tests use the disabled path and an
unreachable loopback endpoint (connection refused) — never an external host. Bounded timeout.
"""
from __future__ import annotations

import json
from uuid import uuid4

import pytest

from tests.cli.runtime_helpers import run_grouped_cli


@pytest.fixture()
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"; d.mkdir()
    ad = tmp_path / "agent"; ad.mkdir()
    for f in ("live_review.md", "plan.md", "context.md"):
        (ad / f).write_text("## Verdict\nPASS\n")
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    monkeypatch.setenv("REMEDY_AGENT_DIR", str(ad))
    # Ensure no ambient advisor config leaks in.
    for k in ("REMEDY_LOCAL_ADVISOR_ENABLED", "REMEDY_LOCAL_ADVISOR_ENDPOINT",
              "REMEDY_LOCAL_ADVISOR_MODEL"):
        monkeypatch.delenv(k, raising=False)
    return d


def test_status_disabled_json(env):
    r = run_grouped_cli(["local-advisor", "status", "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["enabled"] is False
    assert d["available"] is False
    assert "Traceback" not in r.stdout and "Traceback" not in r.stderr


def test_status_external_endpoint_blocked(env, monkeypatch):
    monkeypatch.setenv("REMEDY_LOCAL_ADVISOR_ENABLED", "1")
    monkeypatch.setenv("REMEDY_LOCAL_ADVISOR_ENDPOINT", "http://evil.example.com:11434")
    monkeypatch.setenv("REMEDY_LOCAL_ADVISOR_MODEL", "m")
    r = run_grouped_cli(["local-advisor", "status", "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    # External endpoint can never make the advisor available, and is never echoed raw.
    assert d["available"] is False
    assert "evil.example.com" not in r.stdout


def test_decide_without_advisor_unchanged(env):
    r = run_grouped_cli(["orchestrator", "decide", "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["stop_reason"] in ("selected", "human_review_required", "no_safe_action",
                                "evidence_incomplete")
    # No advisor consulted → advisor is absent/None.
    assert d.get("advisor") in (None, {})


def test_decide_with_advisor_unavailable_safe(env, monkeypatch):
    # Enabled + loopback endpoint that refuses connection → advisor unavailable, decision intact.
    monkeypatch.setenv("REMEDY_LOCAL_ADVISOR_ENABLED", "1")
    monkeypatch.setenv("REMEDY_LOCAL_ADVISOR_ENDPOINT", "http://127.0.0.1:1")
    monkeypatch.setenv("REMEDY_LOCAL_ADVISOR_MODEL", "m")
    r = run_grouped_cli(["orchestrator", "decide", "--use-local-advisor", "--json"], env, timeout=20)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["stop_reason"] in ("selected", "human_review_required", "no_safe_action",
                                "evidence_incomplete")
    adv = d.get("advisor") or {}
    assert adv.get("status") in ("unavailable", "blocked")
    assert adv.get("decision_impact") == "no_change"
    assert "Traceback" not in r.stderr


def test_local_advisor_run_missing_decision_safe(env, monkeypatch):
    monkeypatch.setenv("REMEDY_LOCAL_ADVISOR_ENABLED", "1")
    monkeypatch.setenv("REMEDY_LOCAL_ADVISOR_ENDPOINT", "http://127.0.0.1:1")
    monkeypatch.setenv("REMEDY_LOCAL_ADVISOR_MODEL", "m")
    r = run_grouped_cli(["local-advisor", "run", "--json"], env, timeout=20)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    # Builds a deterministic decision first, then advises (advisor unavailable here).
    assert "next_safe_action" in d
    assert "Traceback" not in r.stderr


def test_run_disabled_safe(env):
    r = run_grouped_cli(["local-advisor", "run", "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d.get("status") == "disabled"
    assert "Traceback" not in r.stderr
