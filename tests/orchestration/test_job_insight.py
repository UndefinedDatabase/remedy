"""The reader of now and one job's insight, the stall reading and the model server probe
(DECISIONs F311 D1, D3 and its addendum, D4). Every model server answer is faked through
`job_insight.fetch_ollama_json`; nothing here reaches a real Ollama.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest

from packages.core.models import RunState
from packages.orchestration import job_insight as JI
from packages.orchestration.data_paths import worker_pulse_path
from packages.orchestration.execution_config import ExecutionConfig
from packages.orchestration.pingpong_job import TASK_APPLIED, TASK_RUNNING, JobPlan, TaskEntry, save_job_plan
from packages.orchestration.worker_pulse import WORKER_PULSE_VERSION, WorkerPulse

NOW = datetime(2026, 10, 21, 12, 0, 0, tzinfo=timezone.utc)
_ISO = "2026-10-21T12:00:00Z"
_UNREACHABLE = {"provider": "ollama", "host": "h", "state": "unreachable", "loaded": [], "queue": None}
_REACHABLE = {"provider": "ollama", "host": "h", "state": "reachable", "loaded": [], "queue": None}


@pytest.fixture(autouse=True)
def _data_root(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    return tmp_path


def _job(*, state: RunState = RunState.RUNNING, task_status: str = "pending",
         execution_config: ExecutionConfig | None = None, project_id: str = "") -> JobPlan:
    job = JobPlan(job_title="insight", tasks=[TaskEntry(title="do a thing", status=task_status)],
                 state=state, execution_config=execution_config or ExecutionConfig(builder="pi", reviewer="pi"),
                 project_id=project_id)
    save_job_plan(job)
    return job


def _write_pulse(job_id: str, *, role: str | None = None, provider: str | None = None,
                 model: str | None = None, round_no: int | None = None,
                 call_started_at: str | None = None, call_ended_at: str | None = None,
                 last_output_at: str = _ISO, stream: list | None = None,
                 bound_at: str = "2026-10-21T10:00:00Z") -> None:
    """A worker pulse with every field under the caller's own control (DECISION F311 D2's shape)."""
    from packages.common.secure_fs import durable_write_json

    path = worker_pulse_path(job_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    durable_write_json(path, {
        "version": WORKER_PULSE_VERSION, "job_id": job_id, "bound_at": bound_at,
        "role": role, "provider": provider, "model": model, "round": round_no,
        "call_kind": "attempt", "call_started_at": call_started_at, "call_ended_at": call_ended_at,
        "last_output_at": last_output_at, "stream": stream or [],
    })


# --- (a): T004's first acceptance line ---------------------------------------------------------

def test_a_running_job_with_a_pulse_is_the_one_entry_beside_an_absent_completed_job():
    ec = ExecutionConfig(builder="pi", reviewer="pi", max_rounds=5)
    running = _job(state=RunState.RUNNING, task_status=TASK_RUNNING, execution_config=ec)
    _write_pulse(running.job_id, role="builder", provider="pi", model="m", round_no=2,
                call_started_at="2026-10-21T11:59:50Z", last_output_at=_ISO,
                stream=[{"at": "2026-10-21T11:59:00Z", "role": "builder", "kind": "system", "text": "s1"},
                        {"at": "2026-10-21T11:59:30Z", "role": "builder", "kind": "tool_call",
                         "tool": "edit", "text": ""},
                        {"at": _ISO, "role": "builder", "kind": "model_text", "text": "done"}])
    completed = _job(state=RunState.COMPLETED)

    answer = JI.now_insight(now=NOW)
    jobs = answer["jobs"]
    assert [j["job"] for j in jobs] == [running.job_id]
    assert completed.job_id not in [j["job"] for j in jobs]

    entry = jobs[0]
    assert entry["task"] == {"id": running.tasks[0].task_id, "title": "do a thing"}
    assert entry["round"] == {"n": 2, "max": 5}
    assert entry["worker"] == {"role": "builder", "provider": "pi", "model": "m"}
    assert entry["phase"] == "repair"
    assert entry["budget"]["used"] == {"tokens": None, "calls": None, "minutes": None, "waited_s": None}
    assert entry["last_output_s"] == 0

    stream = JI.job_insight(running, now=NOW)["stream"]
    assert [e["kind"] for e in stream] == ["system", "tool_call", "model_text"]


# --- (b): one test per phase word ----------------------------------------------------------------

@pytest.mark.parametrize("phase,state,task_status,pulse_kwargs", [
    ("plan", RunState.PLANNED, "pending", None),
    ("build", RunState.RUNNING, TASK_RUNNING, {"role": "builder", "round_no": 1}),
    ("review", RunState.RUNNING, TASK_RUNNING, {"role": "reviewer", "round_no": 1}),
    ("repair", RunState.RUNNING, TASK_RUNNING, {"role": "builder", "round_no": 2}),
    ("apply_wait", RunState.COMPLETED, TASK_APPLIED, None),
    ("halted", RunState.PAUSED, "pending", None),
    ("ended", RunState.FAILED, "pending", None),
    ("unknown", RunState.RUNNING, TASK_RUNNING, None),
])
def test_phase_reads_each_word(phase, state, task_status, pulse_kwargs):
    job = _job(state=state, task_status=task_status)
    if pulse_kwargs:
        _write_pulse(job.job_id, provider="pi", model="m", last_output_at=_ISO, **pulse_kwargs)

    entry = JI.job_insight_entry(job, now=NOW, model_server=_REACHABLE, threshold_s=300, events=[])
    assert entry["phase"] == phase


# --- (c): one test per stall reason except waiting_lock -----------------------------------------

def test_waiting_decision_reads_answer_decision_and_extend_budget_for_a_budget_decision(monkeypatch):
    import packages.orchestration.client_story as client_story_mod

    job = _job(state=RunState.RUNNING, task_status=TASK_RUNNING)

    monkeypatch.setattr(client_story_mod, "job_story_open_decision",
                        lambda plan, events: SimpleNamespace(id="d1", type="patch_approval"))
    entry = JI.job_insight_entry(job, now=NOW, model_server=_REACHABLE, threshold_s=300, events=[])
    assert entry["stalled"] is True and entry["stall_reason"] == "waiting_decision"
    assert entry["waiting_on"] == {"decision": "d1", "type": "patch_approval"}
    assert JI.insight_advice(entry) == ["answer_decision"]

    monkeypatch.setattr(client_story_mod, "job_story_open_decision",
                        lambda plan, events: SimpleNamespace(id="d2", type="token_budget"))
    budget_entry = JI.job_insight_entry(job, now=NOW, model_server=_REACHABLE, threshold_s=300, events=[])
    assert JI.insight_advice(budget_entry) == ["extend_budget", "answer_decision"]


def test_model_unreachable_reads_wait_then_stop():
    job = _job(state=RunState.RUNNING, task_status=TASK_RUNNING)
    _write_pulse(job.job_id, role="builder", provider="pi", model="m", round_no=1, last_output_at=_ISO)

    entry = JI.job_insight_entry(job, now=NOW, model_server=_UNREACHABLE, threshold_s=300, events=[])
    assert entry["stalled"] is True and entry["stall_reason"] == "model_unreachable"
    assert JI.insight_advice(entry) == ["wait", "stop"]


def test_model_slow_reads_wait_then_stop():
    job = _job(state=RunState.RUNNING, task_status=TASK_RUNNING)
    _write_pulse(job.job_id, role="builder", provider="pi", model="m", round_no=1,
                call_started_at="2026-10-21T11:00:00Z", call_ended_at=None,
                last_output_at="2026-10-21T11:55:00Z")

    entry = JI.job_insight_entry(job, now=NOW, model_server=_REACHABLE, threshold_s=300, events=[])
    assert entry["stalled"] is True and entry["stall_reason"] == "model_slow"
    assert JI.insight_advice(entry) == ["wait", "stop"]


def test_no_output_reads_wait_then_stop():
    job = _job(state=RunState.RUNNING, task_status=TASK_RUNNING)
    _write_pulse(job.job_id, role="builder", provider="pi", model="m", round_no=1,
                call_started_at="2026-10-21T11:00:00Z", call_ended_at="2026-10-21T11:50:00Z",
                last_output_at="2026-10-21T11:55:00Z")

    entry = JI.job_insight_entry(job, now=NOW, model_server=_REACHABLE, threshold_s=300, events=[])
    assert entry["stalled"] is True and entry["stall_reason"] == "no_output"
    assert JI.insight_advice(entry) == ["wait", "stop"]


def test_unmeasured_reads_nothing():
    job = _job(state=RunState.RUNNING, task_status=TASK_RUNNING)

    entry = JI.job_insight_entry(job, now=NOW, model_server=_REACHABLE, threshold_s=300, events=[])
    assert entry["stalled"] is False and entry["stall_reason"] == "unmeasured"
    assert JI.insight_advice(entry) == ["nothing"]


def test_a_stopped_job_with_an_old_pulse_and_an_unreachable_server_reads_none():
    job = _job(state=RunState.STOPPED, task_status="pending")
    _write_pulse(job.job_id, role="builder", provider="pi", model="m", round_no=1,
                call_started_at="2026-10-21T08:00:00Z", call_ended_at="2026-10-21T08:05:00Z",
                last_output_at="2026-10-21T08:05:00Z")

    entry = JI.job_insight_entry(job, now=NOW, model_server=_UNREACHABLE, threshold_s=300, events=[])
    assert entry["stalled"] is False and entry["stall_reason"] == "none"
    assert JI.insight_advice(entry) == ["nothing"]


# --- (d): the threshold ---------------------------------------------------------------------

def test_stall_threshold_from_the_registered_key():
    job = _job(state=RunState.RUNNING, task_status=TASK_RUNNING)

    _write_pulse(job.job_id, role="builder", provider="pi", model="m", round_no=1,
                call_started_at="2026-10-21T11:58:00Z", call_ended_at="2026-10-21T11:58:30Z",
                last_output_at="2026-10-21T11:58:59Z")      # 61 seconds of silence
    entry = JI.job_insight_entry(job, now=NOW, model_server=_REACHABLE, threshold_s=60, events=[])
    assert entry["stall_reason"] == "no_output"

    _write_pulse(job.job_id, role="builder", provider="pi", model="m", round_no=1,
                call_started_at="2026-10-21T11:58:00Z", call_ended_at="2026-10-21T11:58:30Z",
                last_output_at="2026-10-21T11:59:01Z")      # 59 seconds of silence
    entry = JI.job_insight_entry(job, now=NOW, model_server=_REACHABLE, threshold_s=60, events=[])
    assert entry["stall_reason"] == "none"


def test_insight_stall_seconds_reads_the_env_var_else_the_default(monkeypatch):
    from packages.orchestration.config import reset_config

    monkeypatch.delenv("REMEDY_INSIGHT_STALL_SECONDS", raising=False)
    reset_config()
    assert JI.insight_stall_seconds() == 300

    monkeypatch.setenv("REMEDY_INSIGHT_STALL_SECONDS", "60")
    reset_config()
    assert JI.insight_stall_seconds() == 60

    monkeypatch.delenv("REMEDY_INSIGHT_STALL_SECONDS", raising=False)
    reset_config()
    assert JI.now_insight(now=NOW)["stall_threshold_s"] == 300


# --- (e): lines -------------------------------------------------------------------------------

def test_lines_clamps_and_slices_the_stream():
    job = _job(state=RunState.RUNNING, task_status=TASK_RUNNING)
    stream = [{"at": f"t{n}", "role": "builder", "kind": "system", "text": str(n)} for n in range(5)]
    _write_pulse(job.job_id, role="builder", provider="pi", model="m", round_no=1,
                last_output_at=_ISO, stream=stream)

    assert [e["text"] for e in JI.job_insight(job, lines=3, now=NOW)["stream"]] == ["2", "3", "4"]
    assert [e["text"] for e in JI.job_insight(job, lines=500, now=NOW)["stream"]] == ["0", "1", "2", "3", "4"]
    assert JI.job_insight(job, lines=-1, now=NOW)["stream"] == []


# --- (f): model_server_state ------------------------------------------------------------------

def test_model_server_state_reachable_with_two_loaded_models(monkeypatch):
    def fake_fetch(host, path, timeout):
        if path == "/api/tags":
            return {}
        assert path == "/api/ps"
        return {"models": [{"name": "a"}, {"name": "b"}]}

    monkeypatch.setattr(JI, "fetch_ollama_json", fake_fetch)
    state = JI.model_server_state()
    assert state["state"] == "reachable" and state["loaded"] == ["a", "b"] and state["queue"] is None


def test_model_server_state_reachable_with_ps_failing_reads_loaded_empty(monkeypatch):
    def fake_fetch(host, path, timeout):
        if path == "/api/tags":
            return {}
        raise OSError("ps down")

    monkeypatch.setattr(JI, "fetch_ollama_json", fake_fetch)
    state = JI.model_server_state()
    assert state["state"] == "reachable" and state["loaded"] == [] and state["queue"] is None


def test_model_server_state_unreachable_reads_loaded_empty(monkeypatch):
    def fake_fetch(host, path, timeout):
        raise OSError("down")

    monkeypatch.setattr(JI, "fetch_ollama_json", fake_fetch)
    state = JI.model_server_state()
    assert state["state"] == "unreachable" and state["loaded"] == [] and state["queue"] is None


# --- (g): now_insight's orders ------------------------------------------------------------------

def test_now_insight_orders_lists_waiting_and_excludes_running_and_done(monkeypatch):
    import packages.orchestration.serve_runs as serve_runs_mod
    from packages.orchestration.serve_paths import serve_paths

    paths = serve_paths()
    for order_id in ("ord-wait", "ord-run", "ord-done"):
        (paths.orders_dir / order_id).mkdir(parents=True)

    payloads = {
        "ord-wait": {"phase": "needs_plan_approval",
                    "jobs": [{"job_id": "job-w", "phase": "needs_plan_approval"}]},
        "ord-run": {"phase": "running", "jobs": [{"job_id": "job-r", "phase": "running"}]},
        "ord-done": {"phase": "done", "jobs": [{"job_id": "job-d", "phase": "applied"}]},
    }

    monkeypatch.setattr(serve_runs_mod, "read_order_record",
                        lambda paths_, order_id: SimpleNamespace(order_id=order_id))
    monkeypatch.setattr(serve_runs_mod, "order_record_payload",
                        lambda paths_, record: payloads[record.order_id])

    answer = JI.now_insight(now=NOW)
    orders = {o["order"]: o for o in answer["orders"]}
    assert set(orders) == {"ord-wait"}
    assert orders["ord-wait"]["phase"] == "needs_plan_approval"
    assert orders["ord-wait"]["jobs"] == ["job-w"]


# --- (h): redaction holds for the insight too ---------------------------------------------------

def test_a_secret_fed_through_add_pi_record_is_absent_from_job_insight():
    job = _job(state=RunState.RUNNING, task_status=TASK_RUNNING)
    path = worker_pulse_path(job.job_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    pulse = WorkerPulse(job.job_id, path, clock=lambda: NOW)
    pulse.bind()
    pulse.begin_call(role="builder", provider="pi", model="m", round_no=1, kind="attempt")
    secret = "sk-ant-api03-AAAABBBBCCCCDDDD1234"
    pulse.add_pi_record({"type": "message_end", "message": {
        "role": "assistant", "content": [{"type": "text", "text": f"the key is {secret}"}]}})

    result = JI.job_insight(job, now=NOW)
    assert secret not in json.dumps(result)


# --- (i): the answer keys ----------------------------------------------------------------------

def test_the_job_entry_and_now_insight_answer_keys():
    job = _job(state=RunState.PLANNED)

    entry = JI.job_insight_entry(job, now=NOW, model_server=_REACHABLE, threshold_s=300, events=[])
    assert set(entry) == {"job", "order", "project", "state", "phase", "task", "round", "worker",
                          "budget", "last_output_s", "stalled", "stall_reason", "waiting_on"}

    answer = JI.now_insight(now=NOW)
    assert set(answer) == {"jobs", "orders", "model_server", "workers", "stall_threshold_s"}
