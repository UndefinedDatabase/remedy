"""The reader of what runs now and one job's insight (DECISIONs F311 D1, D3 and its addendum, D4).

`now_insight()` and `job_insight()` build the answers `GET /api/v1/now` and
`GET /api/v1/jobs/{job}/insight` publish (their routes and twins land in a later round,
DECISION F311 D1): one JOB ENTRY shape, read from the job record, the worker pulse
(`worker_pulse.read_worker_pulse`, DECISION F311 D2), the decoded budget actuals, the job's
effective budgets, the order that lists the job and the job's open decision
(`client_story.job_story_open_decision`). `phase` and the stall reading follow DECISION F311 D3
exactly, with the addendum's two further phases (`halted`, `ended`) for a job that does not run
and its narrower stall reading for one, and its second addendum: `apply_wait` is read from the
job's own result alone. `model_server_state()` is the one Ollama probe DECISION
F311 D4 orders; `fetch_ollama_json` is this module's one network read, so a test fakes it alone
and reaches no real model server. Nothing here writes a file.

Public API::

    insight_stall_seconds() -> int
    fetch_ollama_json(host, path, timeout) -> Any
    model_server_state() -> dict
    job_insight_entry(plan, *, now, model_server, threshold_s, events=None) -> dict
    insight_advice(entry) -> list[str]
    job_insight(plan, *, lines=INSIGHT_LINES_DEFAULT, now=None) -> dict
    now_insight(*, now=None) -> dict
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from packages.orchestration.pi_provider import ollama_host

#: The words `phase` may read (DECISIONs F311 D3 and its addendum).
INSIGHT_PHASES = ("plan", "build", "review", "repair", "apply_wait", "halted", "ended", "unknown")
#: The words `stall_reason` may read (DECISION F311 D3). `waiting_lock` is never produced:
#: every lock in Remedy refuses at once rather than waiting, so there is no wait to see.
INSIGHT_STALL_REASONS = ("waiting_decision", "waiting_lock", "model_unreachable", "model_slow",
                         "no_output", "unmeasured", "none")
#: The words `advice` may list (DECISION F311 D3).
INSIGHT_ADVICE = ("extend_budget", "answer_decision", "wait", "stop", "apply", "nothing")
#: `job_insight`'s default `lines`, absent a query value.
INSIGHT_LINES_DEFAULT = 40
#: The most `lines` a caller may ask for.
INSIGHT_LINES_MAX = 200
#: The default of the registered key `insight.stall_seconds` (DECISION F311 D3).
INSIGHT_STALL_SECONDS_DEFAULT = 300
#: The timeout of one probe to the model server (DECISION F311 D4).
MODEL_SERVER_PROBE_TIMEOUT_S = 2.0

#: The order's own phases `now_insight` keeps a waiting order for (DECISION F311 D1).
_WAITING_ORDER_PHASES = ("planning", "needs_plan_approval", "waiting", "ready", "awaiting_apply")
#: The decision type a budget stop raises; `insight_advice` leads with `extend_budget` for one.
_BUDGET_DECISION_TYPE = "token_budget"


def insight_stall_seconds() -> int:
    """The registered key `insight.stall_seconds`: a positive int, else `INSIGHT_STALL_SECONDS_DEFAULT`."""
    from packages.orchestration.pi_loop_limits import _configured

    value, _source = _configured("insight.stall_seconds", INSIGHT_STALL_SECONDS_DEFAULT)
    return value


def fetch_ollama_json(host: str, path: str, timeout: float) -> Any:
    """`GET <host><path>` decoded as JSON; the module's ONE network read.

    Raises `OSError` (every `urllib.error.URLError` already is one) or `ValueError` on any
    failure: an unreachable host, a timeout, a non-200 answer `urlopen` raises on, or a body
    that is not valid JSON.
    """
    import urllib.request

    with urllib.request.urlopen(f"{host}{path}", timeout=timeout) as response:  # noqa: S310 — the operator's own configured host
        return json.loads(response.read().decode("utf-8"))


def model_server_state() -> dict[str, Any]:
    """The model server's state, as far as Ollama's own endpoints say (DECISION F311 D4)."""
    host = ollama_host()
    try:
        fetch_ollama_json(host, "/api/tags", MODEL_SERVER_PROBE_TIMEOUT_S)
    except (OSError, ValueError):
        return {"provider": "ollama", "host": host, "state": "unreachable", "loaded": [], "queue": None}
    loaded: list[str] = []
    try:
        ps = fetch_ollama_json(host, "/api/ps", MODEL_SERVER_PROBE_TIMEOUT_S)
        models = ps.get("models") if isinstance(ps, dict) else None
        if isinstance(models, list):
            loaded = [m["name"] for m in models if isinstance(m, dict) and isinstance(m.get("name"), str)]
    except (OSError, ValueError):
        loaded = []
    return {"provider": "ollama", "host": host, "state": "reachable", "loaded": loaded, "queue": None}


def _pulse_moment(value: Any) -> datetime | None:
    """VALUE, the time format `WorkerPulse._now_str` writes, parsed back to a UTC moment, or None."""
    if not isinstance(value, str) or not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def _insight_phase(state: str, pulse: dict[str, Any] | None, apply_wait: bool) -> str:
    """The job's phase (DECISIONs F311 D3 and its addendum). `apply_wait` wins over `halted`
    and `ended`."""
    if apply_wait:
        return "apply_wait"
    if state in ("pending", "planned"):
        return "plan"
    if state in ("paused", "blocked", "stopped"):
        return "halted"
    if state in ("completed", "failed", "cancelled"):
        return "ended"
    if state == "running":
        if pulse is None:
            return "unknown"
        role = pulse.get("role")
        round_no = pulse.get("round")
        if role == "reviewer":
            return "review"
        if role == "builder" and isinstance(round_no, int) and round_no > 1:
            return "repair"
        return "build"
    return "unknown"


def _stall_reading(state: str, pulse: dict[str, Any] | None, model_server: dict[str, Any],
                   threshold_s: int, last_output_s: int | None, waiting_on: dict[str, Any] | None,
                   ) -> tuple[bool, str]:
    """(`stalled`, `stall_reason`), DECISION F311 D3 and its addendum: the first reason that
    holds, in order; `stalled` is true for the first five of `INSIGHT_STALL_REASONS`."""
    if waiting_on is not None:
        return True, "waiting_decision"
    if state != "running":
        return False, "none"
    if pulse is None:
        return False, "unmeasured"
    call_open = bool(pulse.get("call_started_at")) and not pulse.get("call_ended_at")
    reachable = model_server.get("state") == "reachable"
    if pulse.get("provider") == "pi" and not reachable:
        return True, "model_unreachable"
    if last_output_s is not None and last_output_s >= threshold_s:
        return (True, "model_slow") if call_open and reachable else (True, "no_output")
    return False, "none"


# WHY one builder: `now` and `insight` answer one job entry shape (DECISION F311 D1).
def job_insight_entry(plan: Any, *, now: datetime, model_server: dict[str, Any], threshold_s: int,
                      events: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """The JOB ENTRY of PLAN (DECISION F311 D1): one shape shared by `job_insight` and `now_insight`."""
    from packages.orchestration.budget_guard import BudgetCounterError, decode_persisted_budget_actuals
    from packages.orchestration.budget_profiles import effective_job_budgets
    from packages.orchestration.budget_stop import budget_work_seconds
    from packages.orchestration.client_story import job_story_open_decision
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.execution_config import resolve_job_execution_config
    from packages.orchestration.job_apply_pending import job_apply_pending_fields
    from packages.orchestration.pingpong_job import TASK_RUNNING
    from packages.orchestration.serve_paths import serve_paths
    from packages.orchestration.serve_runs import order_record_for_job
    from packages.orchestration.timeline import load_run_events
    from packages.orchestration.worker_pulse import read_worker_pulse

    job_id = str(plan.job_id)
    if events is None:
        events = load_run_events(resolve_data_root(), job_id)

    paths = serve_paths()
    order_record = order_record_for_job(paths, job_id)
    order_id = order_record.order_id if order_record is not None else None

    state = str(getattr(plan.state, "value", plan.state))
    # R-1385, D3's second addendum: the job's own result decides, not a sibling's order phase.
    pending = job_apply_pending_fields(plan)
    apply_wait = pending["result_applied"] is False

    task = next((t for t in getattr(plan, "tasks", ()) or () if t.status == TASK_RUNNING), None)
    task_entry = {"id": task.task_id, "title": task.title} if task is not None else None

    pulse = read_worker_pulse(job_id)
    phase = _insight_phase(state, pulse, apply_wait)

    if pulse is None:
        round_entry: dict[str, Any] | None = None
        worker: dict[str, Any] | None = None
        last_output_s: int | None = None
    else:
        ec = getattr(plan, "execution_config", None)
        max_rounds = ec.max_rounds if ec is not None else resolve_job_execution_config(None).max_rounds
        round_entry = {"n": pulse.get("round"), "max": max_rounds}
        worker = {"role": pulse.get("role"), "provider": pulse.get("provider"), "model": pulse.get("model")}
        last_output_at = _pulse_moment(pulse.get("last_output_at"))
        last_output_s = max(0, int((now - last_output_at).total_seconds())) if last_output_at else None

    decision = job_story_open_decision(plan, events)
    waiting_on = {"decision": decision.id, "type": decision.type} if decision is not None else None

    used_tokens = used_calls = used_minutes = used_waited = None
    record = getattr(plan, "budget_actuals", None)
    if isinstance(record, dict) and record:
        try:
            actuals = decode_persisted_budget_actuals(
                record, first_running_at=getattr(plan, "first_running_at", "") or None)
        except BudgetCounterError:
            actuals = None
        if actuals is not None:
            used_tokens = actuals["total_tokens"]
            used_calls = actuals["provider_call_count"]
            used_minutes = int(budget_work_seconds(actuals, now) // 60)
            used_waited = actuals["waited_s"]

    try:
        # R-1384: a job whose own `budgets` do not validate must not fail the whole answer.
        budgets = effective_job_budgets(plan)
    except (ValueError, TypeError):
        budgets = None

    stalled, stall_reason = _stall_reading(state, pulse, model_server, threshold_s, last_output_s, waiting_on)

    return {
        "job": job_id,
        "order": order_id,
        "project": str(getattr(plan, "project_id", "") or "") or None,
        "state": state,
        "phase": phase,
        "task": task_entry,
        "round": round_entry,
        "worker": worker,
        "budget": {
            "used": {"tokens": used_tokens, "calls": used_calls, "minutes": used_minutes,
                     "waited_s": used_waited},
            "limits": {"tokens": budgets.max_total_tokens if budgets is not None else None,
                      "calls": budgets.max_provider_calls if budgets is not None else None,
                      "minutes": budgets.max_wall_clock_minutes if budgets is not None else None},
        },
        "last_output_s": last_output_s,
        "stalled": stalled,
        "stall_reason": stall_reason,
        "waiting_on": waiting_on,
    }


def insight_advice(entry: dict[str, Any]) -> list[str]:
    """DECISION F311 D3's advice, read from ENTRY alone."""
    reason = entry.get("stall_reason")
    if reason == "waiting_decision":
        waiting_on = entry.get("waiting_on") or {}
        advice = ["answer_decision"]
        if waiting_on.get("type") == _BUDGET_DECISION_TYPE:
            advice = ["extend_budget", *advice]
        return advice
    if reason in ("model_unreachable", "model_slow", "no_output"):
        return ["wait", "stop"]
    if entry.get("phase") == "apply_wait":
        return ["apply"]
    return ["nothing"]


def job_insight(plan: Any, *, lines: int = INSIGHT_LINES_DEFAULT, now: datetime | None = None,
               ) -> dict[str, Any]:
    """PLAN's job entry plus `stream` (its pulse's last LINES entries) and `advice`. One probe."""
    from packages.orchestration.worker_pulse import read_worker_pulse

    moment = now or datetime.now(timezone.utc)
    threshold_s = insight_stall_seconds()
    server = model_server_state()
    entry = job_insight_entry(plan, now=moment, model_server=server, threshold_s=threshold_s)

    pulse = read_worker_pulse(str(plan.job_id))
    clamped = max(0, min(lines, INSIGHT_LINES_MAX))
    stream: list[dict[str, Any]] = []
    if pulse is not None and clamped > 0:
        stream = list(pulse.get("stream") or [])[-clamped:]

    result = dict(entry)
    result["stream"] = stream
    result["advice"] = insight_advice(entry)
    return result


def now_insight(*, now: datetime | None = None) -> dict[str, Any]:
    """Every living job, every waiting order, the model server and the workers. One probe."""
    from packages.orchestration.pingpong_job import JOB_RUNNING, list_job_plans_safe, load_job_plan
    from packages.orchestration.serve_paths import serve_paths
    from packages.orchestration.serve_runs import order_record_payload, read_order_record

    moment = now or datetime.now(timezone.utc)
    threshold_s = insight_stall_seconds()
    server = model_server_state()

    plans, _degraded, _skipped = list_job_plans_safe()
    running = [p for p in plans if str(getattr(p.state, "value", p.state)) == str(JOB_RUNNING)]
    jobs = [job_insight_entry(p, now=moment, model_server=server, threshold_s=threshold_s) for p in running]

    orders: list[dict[str, Any]] = []
    paths = serve_paths()
    if paths.orders_dir.is_dir():
        for child in paths.orders_dir.iterdir():
            record = read_order_record(paths, child.name)
            if record is None:
                continue
            payload = order_record_payload(paths, record)
            if payload["phase"] not in _WAITING_ORDER_PHASES:
                continue
            job_rows = payload["jobs"]
            if any(row.get("phase") == "running" for row in job_rows):
                continue
            job_ids = [str(row.get("job_id") or "") for row in job_rows]
            project = None
            for job_id in job_ids:
                job_plan = load_job_plan(job_id) if job_id else None
                project_id = str(getattr(job_plan, "project_id", "") or "") if job_plan is not None else ""
                if project_id:
                    project = project_id
                    break
            orders.append({"order": record.order_id, "project": project,
                          "phase": payload["phase"], "jobs": job_ids})

    return {
        "jobs": jobs,
        "orders": orders,
        "model_server": server,
        "workers": {"running": len(jobs), "free": None},
        "stall_threshold_s": threshold_s,
    }
