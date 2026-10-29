"""Operator order beweis, F327: the planner spends no order budget on narration, and the order's
call cap always keeps three full rounds of builder and reviewer free for the job."""
from __future__ import annotations

from types import SimpleNamespace

import pytest

from packages.orchestration import do_study, study
from packages.orchestration.order_ledger import OrderCallLedger, OrderCallRefusedError


def _answer(prompt: str, attempt: int) -> str:
    return "ok"


def test_the_study_narration_is_recorded_but_never_counted_or_refused():
    ledger = OrderCallLedger(caps={"max_provider_calls": 1})
    ledger.jobs["j"] = {"calls": 1, "tokens": 0, "cost_usd": None, "measured": True, "unpriced_calls": 0}
    assert ledger.exhausted()
    narrate = ledger.wrap("study_narration", _answer)
    for _ in range(4):
        assert narrate("p", 300) == "ok"
    assert ledger.planner_calls == 0 and ledger.used()["calls"] == 1
    assert ledger.summary()["uncounted_calls"] == 4
    with pytest.raises(OrderCallRefusedError):
        ledger.wrap("intake", _answer)("p", 0)


def test_a_planner_call_the_walk_can_do_without_is_refused_before_it_eats_the_jobs_three_rounds():
    ledger = OrderCallLedger(caps={"max_provider_calls": 8})
    ledger.wrap("scope_decision", _answer)("p", 0)
    ledger.wrap("intake", _answer)("p", 0)
    with pytest.raises(OrderCallRefusedError, match="keeps 6 of its 8 provider calls free"):
        ledger.wrap("mission_plan", _answer)("p", 0)
    assert ledger.remaining()["max_provider_calls"] == 6
    assert ledger.wrap("task_plan", _answer)("p", 0) == "ok"    # the job's own plan is never refused for it
    assert ledger.reserve_shortfall() == ""


def test_a_cap_below_the_reserve_is_said_and_refuses_nothing_for_it():
    ledger = OrderCallLedger(caps={"max_provider_calls": 4})
    assert ledger.reserve_shortfall() == (
        "The order's cap of 4 provider calls cannot keep 3 full rounds of builder and reviewer "
        "(6 calls) free, so Remedy plans the smallest size, one job.")
    assert ledger.wrap("intake", _answer)("p", 0) == "ok"
    assert OrderCallLedger(caps=None).reserve_shortfall() == ""


def test_a_studied_project_whose_manifest_changed_is_studied_without_narration(monkeypatch, tmp_path):
    seen = {}
    lane = SimpleNamespace(hold=False, bounded=False, reason="")
    monkeypatch.setattr(do_study, "settle_do_lane", lambda ctx: lane)
    monkeypatch.setattr(do_study, "repo_has_committed_file", lambda root: True)
    monkeypatch.setattr(study, "study_stale_reason", lambda root, head: "package.json changed since the study")
    monkeypatch.setattr(study, "study_call_fn", lambda: _answer)
    monkeypatch.setattr(study, "study_runs_local", lambda: True)
    monkeypatch.setattr(study, "record_study_pass", lambda project_id, root: None)
    monkeypatch.setattr(study, "run_study", lambda root, project_id, call_fn: seen.setdefault("fn", call_fn)
                        or SimpleNamespace(cards_written=[], partial=False))
    project = SimpleNamespace(metadata={"studied_at": "2026-10-28", "studied_head": "abc"}, id="p", slug="p")
    ctx = SimpleNamespace(no_llm=False, tiny_repo=False, repo_root=str(tmp_path), project=project, ledger=None)
    status, detail = do_study.do_step_study(ctx)
    assert seen["fn"] is None and "package.json changed since the study" in detail


def test_the_narration_is_skipped_when_the_study_model_is_not_local(monkeypatch):
    from packages.orchestration import role_config

    monkeypatch.setattr(role_config, "resolve_role_config",
                        lambda role: SimpleNamespace(provider="claude-cli", model="opus"))
    monkeypatch.setattr(study, "resolve_role_config", role_config.resolve_role_config)
    assert study.study_runs_local() is False
    monkeypatch.setattr(study, "resolve_role_config",
                        lambda role: SimpleNamespace(provider="ollama", model="qwen3:8b"))
    assert study.study_runs_local() is True
