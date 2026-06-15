"""Runtime CLI tests for `remedy worker registry-*` and `remedy route-policy` (Step 1735).

Subprocess tests. Metadata + policy only — no worker execution/apply/approve/test. Safe JSON, safe
errors, catalog-valid next actions, no tracebacks.
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


def test_worker_registry_list(env):
    r = run_grouped_cli(["worker", "registry-list", "--json"], env)
    assert r.returncode == 0, r.stderr
    out = json.loads(r.stdout)
    assert out["worker_count"] >= 7
    assert "Traceback" not in r.stdout
    ids = {w["worker_id"] for w in out["workers"]}
    assert "local.candidate_generator" in ids and "ollama.placeholder" in ids


def test_worker_registry_show(env):
    r = run_grouped_cli(["worker", "registry-show", "ollama.placeholder", "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["is_placeholder"] is True and d["enabled"] is False


def test_worker_registry_show_invalid_id(env):
    r = run_grouped_cli(["worker", "registry-show", "no.such.worker", "--json"], env)
    assert r.returncode == 1
    assert "Traceback" not in r.stdout and "Traceback" not in r.stderr


def test_worker_registry_integrity(env):
    r = run_grouped_cli(["worker", "registry-integrity", "--json"], env)
    assert r.returncode == 0, r.stderr
    assert json.loads(r.stdout)["passed"] is True


def test_route_policy_show_default(env):
    r = run_grouped_cli(["route-policy", "show", "job-1", "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["prefer_local_for_cheap_tasks"] is True
    assert d["blocked_worker_ids"] == []


def test_route_policy_set_and_roundtrip(env):
    r = run_grouped_cli(["route-policy", "set", "job-2", "--block-worker",
                         "cloud.placeholder", "--max-cost-tier", "cheap",
                         "--prefer-local-for-cheap-tasks", "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["saved"] is True
    assert "cloud.placeholder" in d["blocked_worker_ids"]
    assert d["max_cost_tier"] == "cheap"
    # Round-trip via show.
    r2 = run_grouped_cli(["route-policy", "show", "job-2", "--json"], env)
    assert json.loads(r2.stdout)["max_cost_tier"] == "cheap"


def test_route_policy_set_invalid_worker(env):
    r = run_grouped_cli(["route-policy", "set", "job-3", "--block-worker", "ghost", "--json"], env)
    assert r.returncode == 1
    assert "Traceback" not in r.stderr


def test_route_policy_set_disabled_worker_select_errors(env):
    r = run_grouped_cli(["route-policy", "set", "job-4", "--select-worker",
                         "cloud.placeholder", "--json"], env)
    assert r.returncode == 1
    assert "disabled" in (r.stdout + r.stderr).lower()


def test_route_policy_set_invalid_cost_tier(env):
    r = run_grouped_cli(["route-policy", "set", "job-5", "--max-cost-tier", "bogus", "--json"], env)
    assert r.returncode == 1


def test_route_policy_evaluate(env):
    r = run_grouped_cli(["route-policy", "evaluate", "job-6", "--task-type", "repair", "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["recommended_worker_id"] == "local.candidate_generator"
    assert "Traceback" not in r.stdout
    # next action is catalog-valid and never an execution command.
    assert d["next_safe_action"].startswith("remedy ")
    assert " run" not in d["next_safe_action"]


def test_evaluate_after_blocking_local(env):
    run_grouped_cli(["route-policy", "set", "job-7", "--block-worker",
                     "local.candidate_generator", "--max-cost-tier", "cheap", "--json"], env)
    r = run_grouped_cli(["route-policy", "evaluate", "job-7", "--task-type", "repair", "--json"], env)
    d = json.loads(r.stdout)
    assert d["recommended_worker_id"] != "local.candidate_generator"
