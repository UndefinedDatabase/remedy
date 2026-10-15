"""Pi timeouts are ceilings, never floors (operator amendment amend1014c, R2).

A fake `pi` executable at the process boundary; the production resolution path and the shipped
constants are exercised, nothing is monkeypatched to make an answer true.
"""
from __future__ import annotations

import os
import time
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest

import packages.orchestration.pi_provider as PP
from packages.orchestration.execution_config import resolve_job_execution_config
from packages.orchestration.provider_timeouts import PI_DEFAULT_TIMEOUT_SEC
from tests.orchestration.test_pi_provider import fake_pi, good_stream, workspace  # noqa: F401 (fixtures)


@pytest.fixture(autouse=True)
def _no_leftover_job_clock():
    PP._JOB_TIME_LEFT.set(None)
    yield
    PP._JOB_TIME_LEFT.set(None)


def _pid_is_gone(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return True
    return False


def test_an_explicit_one_second_timeout_kills_the_child_near_one_second(fake_pi, workspace):
    fake_pi.behave(stdout=good_stream(), sleep=30)
    started = time.monotonic()
    out = PP.PiProvider(role="builder", cwd=str(workspace)).build("x", timeout_sec=1)
    elapsed = time.monotonic() - started
    assert "pi_timeout" in out.error and elapsed < 10
    assert PP.PI_DEFAULT_TIMEOUT_SEC == 900 == PI_DEFAULT_TIMEOUT_SEC          # the shipped value
    deadline = time.monotonic() + 5
    while not _pid_is_gone(fake_pi.call()["pid"]) and time.monotonic() < deadline:
        time.sleep(0.1)
    assert _pid_is_gone(fake_pi.call()["pid"])


def test_an_omitted_timeout_gets_the_documented_pi_default(fake_pi, workspace, monkeypatch):
    seen: dict = {}
    real = PP.run_guarded
    monkeypatch.setattr(PP, "run_guarded", lambda argv, policy: (seen.update(wall=policy.wall_timeout_seconds), real(argv, policy))[1])
    PP.PiProvider(role="builder", cwd=str(workspace)).build("x")
    assert seen["wall"] == 900.0
    PP.PiProvider(role="reviewer", cwd=str(workspace)).build("x", timeout_sec=45)
    assert seen["wall"] == 45.0                                          # an explicit value is not raised


def test_the_default_applies_only_when_nobody_set_a_timeout():
    default_pi = resolve_job_execution_config(None, builder_name="pi", reviewer_name="pi")
    assert (default_pi.timeout_sec, default_pi.timeout_sec_source) == (900, "default")
    explicit = resolve_job_execution_config(None, builder_name="pi", reviewer_name="pi", timeout_sec=30)
    assert (explicit.timeout_sec, explicit.timeout_sec_source) == (30, "invocation")
    other = resolve_job_execution_config(None, builder_name="claude-cli", reviewer_name="claude-cli")
    assert other.timeout_sec == 120


def _job(**budgets):
    return SimpleNamespace(budgets=budgets or None,
                           first_running_at=(datetime.now(timezone.utc) - timedelta(seconds=10)).isoformat())


def test_a_larger_timeout_is_capped_by_the_remaining_job_wall_budget():
    PP.bind_job_clock(_job(max_wall_clock_minutes=1))                    # about fifty seconds left
    seconds, why = PP.effective_pi_timeout(900)
    assert 40 < seconds <= 50 and why["bound_by"] == "max_wall_clock_minutes"
    assert why["configured_sec"] == 900 and why["effective_sec"] == round(seconds, 1)


def test_a_nearer_deadline_wins_over_the_default_and_the_configured_timeout():
    soon = (datetime.now(timezone.utc) + timedelta(seconds=20)).isoformat()
    PP.bind_job_clock(_job(max_wall_clock_minutes=30, deadline=soon))
    seconds, why = PP.effective_pi_timeout(PI_DEFAULT_TIMEOUT_SEC)
    assert seconds <= 20 and why["bound_by"] == "deadline"
    assert PP.effective_pi_timeout(5)[0] == 5.0 and PP.effective_pi_timeout(5)[1]["bound_by"] == "configured"


def test_a_job_with_no_time_left_starts_no_pi_process(fake_pi, workspace):
    PP.bind_job_clock(_job(max_wall_clock_minutes=1,
                           deadline=(datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat()))
    out = PP.PiProvider(role="builder", cwd=str(workspace)).build("x")
    assert "pi_timeout" in out.error and not (fake_pi.dir / "call.json").exists()


def test_timeout_evidence_is_recorded_and_the_error_stays_bounded(fake_pi, workspace, tmp_path):
    fake_pi.behave(stdout=good_stream(), sleep=30)
    provider = PP.PiProvider(role="builder", cwd=str(workspace), evidence_dir=str(tmp_path / "run"))
    out = provider.build("x", timeout_sec=1)
    assert out.error.startswith("provider_error: pi_timeout") and len(out.error) < 300
    assert provider.last_evidence["timeout"] == {
        "configured_sec": 1, "job_left_sec": None, "job_ceiling": "", "effective_sec": 1.0,
        "bound_by": "configured"}
