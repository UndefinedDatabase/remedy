"""The worker pulse (DECISION F311 D2): bind, one call, its mapped stream entries, the throttle,
`read_worker_pulse`'s refusals, a swallowed write failure, and the binding ContextVar.

A fake clock, advanced by hand, makes the throttle and the timestamps exact rather than racing
the real one. Every path stays under an isolated ``tmp_path``; nothing here reads the operator's
data root.
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest

from packages.orchestration import data_paths
from packages.orchestration.worker_pulse import (
    PULSE_STREAM_LIMIT,
    PULSE_TEXT_LIMIT,
    WORKER_PULSE_VERSION,
    WorkerPulse,
    bind_worker_pulse,
    current_worker_pulse,
    read_worker_pulse,
)


class FakeClock:
    """A callable clock, advanced by hand, so the throttle and the timestamps are exact."""

    def __init__(self) -> None:
        self._now = datetime(2026, 10, 21, 0, 0, 0, tzinfo=timezone.utc)

    def __call__(self) -> datetime:
        return self._now

    def advance(self, seconds: float) -> None:
        self._now += timedelta(seconds=seconds)

    def iso(self) -> str:
        return self._now.strftime("%Y-%m-%dT%H:%M:%SZ")


@pytest.fixture
def clock() -> FakeClock:
    return FakeClock()


@pytest.fixture
def pulse(tmp_path, clock) -> WorkerPulse:
    # `durable_write` needs its destination directory to already exist (it never creates one),
    # and using the real `data_paths` layout lets a test read a pulse back with `read_worker_pulse`.
    path = data_paths.worker_pulse_path("job-pulse-1", tmp_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return WorkerPulse("job-pulse-1", path, clock=clock)


# --- (a), (b): bind and begin_call -----------------------------------------------------------

def test_bind_writes_a_fresh_pulse_at_the_job_s_worker_pulse_path(tmp_path, monkeypatch, clock):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    path = data_paths.worker_pulse_path("job-pulse-1")
    path.parent.mkdir(parents=True, exist_ok=True)
    wp = WorkerPulse("job-pulse-1", path, clock=clock)

    wp.bind()

    on_disk = json.loads(path.read_text(encoding="utf-8"))
    assert on_disk["version"] == WORKER_PULSE_VERSION and on_disk["job_id"] == "job-pulse-1"
    assert on_disk["bound_at"] == on_disk["last_output_at"] == clock.iso()
    assert on_disk["stream"] == []
    for field in ("role", "provider", "model", "round", "call_kind", "call_started_at", "call_ended_at"):
        assert on_disk[field] is None


def test_begin_call_writes_role_provider_model_round_and_kind(pulse, clock, tmp_path):
    pulse.bind()
    clock.advance(5)

    pulse.begin_call(role="builder", provider="pi", model="m", round_no=3, kind="attempt")

    back = read_worker_pulse("job-pulse-1", tmp_path)
    assert (back["role"], back["provider"], back["model"], back["round"], back["call_kind"]) == (
        "builder", "pi", "m", 3, "attempt")
    assert back["call_started_at"] == clock.iso() and back["call_ended_at"] is None


# --- (c): one test per mapped record kind, and the two that map to none ----------------------

def _last_entry(wp: WorkerPulse) -> dict:
    return wp.snapshot()["stream"][-1]


def test_an_assistant_message_end_maps_to_a_model_text_entry(pulse, clock):
    pulse.bind()
    pulse.begin_call(role="builder", provider="pi", model="m", round_no=1, kind="attempt")

    pulse.add_pi_record({"type": "message_end", "message": {
        "role": "assistant", "content": [{"type": "text", "text": "hello "}, {"type": "text", "text": "world"}]}})

    assert _last_entry(pulse) == {"at": clock.iso(), "role": "builder", "kind": "model_text", "text": "hello world"}


def test_a_tool_execution_start_maps_to_a_tool_call_entry_with_its_args(pulse, clock):
    pulse.bind()
    pulse.begin_call(role="builder", provider="pi", model="m", round_no=1, kind="attempt")

    pulse.add_pi_record({"type": "tool_execution_start", "toolName": "edit", "args": {"path": "a.py"}})

    assert _last_entry(pulse) == {"at": clock.iso(), "role": "builder", "kind": "tool_call",
                                  "tool": "edit", "text": '{"path":"a.py"}'}


def test_a_tool_execution_start_without_args_carries_empty_text(pulse):
    pulse.bind()
    pulse.begin_call(role="builder", provider="pi", model="m", round_no=1, kind="attempt")

    pulse.add_pi_record({"type": "tool_execution_start"})

    assert _last_entry(pulse)["tool"] == "?" and _last_entry(pulse)["text"] == ""


def test_a_tool_execution_end_maps_to_a_tool_result_entry_with_its_length(pulse, clock):
    pulse.bind()
    pulse.begin_call(role="reviewer", provider="pi", model="m", round_no=1, kind="attempt")

    pulse.add_pi_record({"type": "tool_execution_end", "toolName": "edit", "result": {"ok": True}})

    length = len(json.dumps({"ok": True}, sort_keys=True, separators=(",", ":")))
    assert _last_entry(pulse) == {"at": clock.iso(), "role": "reviewer", "kind": "tool_result",
                                  "tool": "edit", "length": length}


def test_a_tool_execution_end_without_a_result_carries_zero_length(pulse):
    pulse.bind()
    pulse.begin_call(role="builder", provider="pi", model="m", round_no=1, kind="attempt")

    pulse.add_pi_record({"type": "tool_execution_end", "toolName": "edit"})

    assert _last_entry(pulse)["length"] == 0


def test_auto_retry_start_maps_to_a_system_entry(pulse, clock):
    pulse.bind()
    pulse.begin_call(role="builder", provider="pi", model="m", round_no=1, kind="attempt")

    pulse.add_pi_record({"type": "auto_retry_start"})

    assert _last_entry(pulse) == {"at": clock.iso(), "role": "builder", "kind": "system", "text": "auto_retry_start"}


def test_agent_settled_maps_to_a_system_entry(pulse, clock):
    pulse.bind()
    pulse.begin_call(role="builder", provider="pi", model="m", round_no=1, kind="attempt")

    pulse.add_pi_record({"type": "agent_settled", "aborted": False})

    assert _last_entry(pulse) == {"at": clock.iso(), "role": "builder", "kind": "system", "text": "agent_settled"}


def test_a_user_message_end_and_an_unknown_record_add_no_entry(pulse):
    pulse.bind()
    pulse.begin_call(role="builder", provider="pi", model="m", round_no=1, kind="attempt")

    pulse.add_pi_record({"type": "message_end", "message": {"role": "user", "content": [
        {"type": "text", "text": "a prompt"}]}})
    pulse.add_pi_record({"type": "some_unknown_kind", "x": 1})

    assert pulse.snapshot()["stream"] == []


# --- (d): the stream is bounded at PULSE_STREAM_LIMIT, oldest dropped first ------------------

def test_the_stream_keeps_only_the_last_200_entries(pulse):
    pulse.bind()
    pulse.begin_call(role="builder", provider="pi", model="m", round_no=1, kind="attempt")

    for n in range(205):
        pulse.add_pi_record({"type": "tool_execution_start", "toolName": f"t{n}"})

    stream = pulse.snapshot()["stream"]
    assert len(stream) == PULSE_STREAM_LIMIT == 200
    assert stream[0]["tool"] == "t5"          # the first 5 of 205 were dropped
    assert stream[-1]["tool"] == "t204"


# --- (e): the text cut, and redaction before it ever reaches disk ---------------------------

def test_a_long_model_text_is_cut_to_the_text_limit(pulse):
    pulse.bind()
    pulse.begin_call(role="builder", provider="pi", model="m", round_no=1, kind="attempt")

    pulse.add_pi_record({"type": "message_end", "message": {
        "role": "assistant", "content": [{"type": "text", "text": "x" * 500}]}})

    assert _last_entry(pulse)["text"] == "x" * PULSE_TEXT_LIMIT == "x" * 200


def test_a_secret_in_the_text_is_redacted_before_it_reaches_the_file(pulse):
    secret = "sk-ant-api03-AAAABBBBCCCCDDDD1234"
    pulse.bind()
    pulse.begin_call(role="builder", provider="pi", model="m", round_no=1, kind="attempt")

    pulse.add_pi_record({"type": "message_end", "message": {
        "role": "assistant", "content": [{"type": "text", "text": f"the key is {secret}"}]}})

    assert secret not in _last_entry(pulse)["text"]
    assert secret not in pulse._path.read_text(encoding="utf-8")


# --- (f): the write throttle -----------------------------------------------------------------

def test_the_disk_write_is_throttled_but_end_call_always_writes_at_once(pulse, clock):
    pulse.bind()
    pulse.begin_call(role="builder", provider="pi", model="m", round_no=1, kind="attempt")   # writes; t=0

    clock.advance(2.1)
    pulse.add_pi_record({"type": "tool_execution_start", "toolName": "a"})                   # writes; t=2.1
    on_disk = json.loads(pulse._path.read_text(encoding="utf-8"))
    assert len(on_disk["stream"]) == 1

    clock.advance(1.0)
    pulse.add_pi_record({"type": "tool_execution_start", "toolName": "b"})                   # too soon; t=3.1
    on_disk = json.loads(pulse._path.read_text(encoding="utf-8"))
    assert len(on_disk["stream"]) == 1                            # not yet flushed
    assert len(pulse.snapshot()["stream"]) == 2                   # but held in memory

    clock.advance(2.5)
    pulse.add_pi_record({"type": "tool_execution_start", "toolName": "c"})                   # flushes; t=5.6
    on_disk = json.loads(pulse._path.read_text(encoding="utf-8"))
    assert len(on_disk["stream"]) == 3
    assert on_disk["call_ended_at"] is None

    clock.advance(0.1)                                            # well under the throttle interval
    pulse.end_call()
    on_disk = json.loads(pulse._path.read_text(encoding="utf-8"))
    assert on_disk["call_ended_at"] == clock.iso()


# --- (g): read_worker_pulse's refusals --------------------------------------------------------

def test_read_worker_pulse_answers_none_for_absent_or_malformed_or_wrong_version(tmp_path):
    job_id = "job-read-1"
    path = data_paths.worker_pulse_path(job_id, tmp_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    assert read_worker_pulse(job_id, tmp_path) is None             # absent

    path.write_text("[]", encoding="utf-8")
    assert read_worker_pulse(job_id, tmp_path) is None              # not an object

    path.write_text("{not json", encoding="utf-8")
    assert read_worker_pulse(job_id, tmp_path) is None               # invalid JSON

    path.write_text(json.dumps({"version": 2, "job_id": job_id}), encoding="utf-8")
    assert read_worker_pulse(job_id, tmp_path) is None               # wrong version

    path.write_text(json.dumps({"version": WORKER_PULSE_VERSION, "job_id": job_id}), encoding="utf-8")
    assert read_worker_pulse(job_id, tmp_path) == {"version": WORKER_PULSE_VERSION, "job_id": job_id}


# --- (h): a write failure is swallowed --------------------------------------------------------

def test_a_write_that_raises_oserror_leaves_add_pi_record_returning_normally(pulse, monkeypatch, clock):
    pulse.bind()
    pulse.begin_call(role="builder", provider="pi", model="m", round_no=1, kind="attempt")

    def _boom(*a, **k):
        raise OSError("disk full")

    monkeypatch.setattr("packages.orchestration.worker_pulse.durable_write_json", _boom)
    clock.advance(10)                 # past the throttle interval, so this write is actually attempted

    pulse.add_pi_record({"type": "tool_execution_start", "toolName": "edit"})     # must not raise

    assert pulse.snapshot()["stream"][-1]["tool"] == "edit"


# --- R-1383: `bind_job_clock` binds the pulse too, for a job with an id -----------------------

@pytest.fixture
def _restore_job_clock_bindings():
    """R-1387: `bind_job_clock` binds four ContextVars (the pulse's, the job clock's, the stop
    request's and the tokens-left one); this fixture saves each with a `.set(...)` token before
    the test runs and resets every one after, so a later test in the same process does not
    inherit this test's pulse, clock, stop-request or token-budget closures."""
    from packages.orchestration import pi_loop_limits, pi_provider
    from packages.orchestration import worker_pulse as worker_pulse_mod

    variables = (pi_provider._JOB_TIME_LEFT, pi_provider._JOB_STOP_REQUESTED,
                pi_loop_limits._JOB_TOKENS_LEFT, worker_pulse_mod._CURRENT_PULSE)
    tokens = [variable.set(variable.get()) for variable in variables]
    yield
    for variable, token in zip(variables, tokens):
        variable.reset(token)


def test_bind_job_clock_also_binds_a_fresh_worker_pulse(tmp_path, monkeypatch, _restore_job_clock_bindings):
    """R-1383: a run's own `bind_job_clock` leaves `read_worker_pulse` answering a fresh pulse,
    not only the direct `bind_worker_pulse` the other tests of this file call."""
    from packages.orchestration import pi_provider
    from packages.orchestration.pingpong_job import JobPlan

    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    job_id = "job-bind-clock-1"
    data_paths.worker_pulse_path(job_id).parent.mkdir(parents=True, exist_ok=True)   # a saved record's own folder

    # A real JobPlan, not a bare SimpleNamespace: `bind_job_clock` binds lazy closures
    # (`pi_loop_limits`'s `_JOB_TOKENS_LEFT`) that read `job.budgets` etc. on their NEXT call,
    # possibly from a later test, so the job object must carry every attribute they read.
    pi_provider.bind_job_clock(JobPlan(job_id=job_id))

    back = read_worker_pulse(job_id)
    assert back is not None and back["bound_at"] is not None and back["stream"] == []
    for field in ("role", "provider", "model", "round", "call_kind", "call_started_at", "call_ended_at"):
        assert back[field] is None


# --- (i): the binding ContextVar --------------------------------------------------------------

def test_bind_worker_pulse_binds_for_a_job_with_an_id_and_unbinds_without_one(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))

    bound = bind_worker_pulse(SimpleNamespace(job_id="job-bind-1"))
    assert bound is not None and current_worker_pulse() is bound

    unbound = bind_worker_pulse(SimpleNamespace())
    assert unbound is None and current_worker_pulse() is None
