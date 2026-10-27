"""The story of an order, not only of a job (operator amendment amend1023-universe-trust, Part 3).

`GET /api/v1/orders/{order}/story` and `remedy client order-story <order> --json` answer it: the
order's missions with their milestones, each milestone's jobs with a closed state word, each job's
tasks done and total, the round and the tool of the job that runs (read from F311's worker pulse),
and who gave the order. Every state word is in `ORDER_STORY_JOB_STATES`, listed under the `story`
key of `GET /api/v1/interface`, so a client translates each one into a sentence of its own language
(DECISION amend1023 D11). It is a read of what the order's records hold and changes nothing.

Remedy deliberately keeps no order-to-milestone index of its own: a job's milestone is the one its
record names (`mission_contract.JOB_MILESTONE_KEY`), and the milestones' goals are read from its
mission's plan, so the story can never list a job under a milestone it was not planned for.
"""
from __future__ import annotations

from typing import Any

#: What one job of the order is doing, one word: planned (it may run, or waits for its plan's
#: approval), waiting (for the job of the order named under `after_job`), running, blocked (with
#: the criterion it did not meet), done (a result waiting for its apply, or checks that passed),
#: applied, stopped (resumable), cancelled, declined and failed.
ORDER_STORY_JOB_STATES: tuple[str, ...] = (
    "planned", "waiting", "running", "blocked", "done", "applied", "stopped", "cancelled", "declined", "failed")

#: An order job's phase (`order_jobs.ORDER_JOB_PHASES`) read as its story word.
_STATE_OF_PHASE = {
    "running": "running", "waiting": "waiting", "ready": "planned", "needs_plan_approval": "planned",
    "awaiting_apply": "done", "checked": "done", "applied": "applied", "declined": "declined",
    "blocked": "blocked", "stopped": "stopped", "cancelled": "cancelled", "failed": "failed",
}

#: The top-level keys of the answer beside the envelope's own.
ORDER_STORY_ANSWER_KEYS: tuple[str, ...] = ("client", "missions", "order_id", "phase", "scope", "state")

#: The keys under them, as the machine client interface declares them.
ORDER_STORY_KEY_TREE: dict[str, Any] = {
    "scope": {"single_job": {}, "files": {}, "reason": {}, "decided": {}},
    "missions": {"mission_id": {}, "milestones": {"id": {}, "goal": {}, "jobs": {
        "job_id": {}, "number": {}, "title": {}, "state": {},
        "state_detail": {"after_job": {}, "after_job_id": {}, "criterion": {}},
        "tasks": {"done": {}, "total": {}}, "round": {"n": {}, "max": {}}, "tool": {}, "story": {}}}},
}


def _running_detail(job_id: str) -> tuple[dict[str, Any] | None, str | None]:
    """The round and the last tool of a running job's worker, from F311's insight; None where unknown."""
    from packages.orchestration.job_insight import job_insight
    from packages.orchestration.pingpong_job import load_job_plan

    plan = load_job_plan(job_id)
    if plan is None:
        return None, None
    insight = job_insight(plan, lines=40)
    tool = next((line.get("tool") for line in reversed(insight.get("stream") or []) if line.get("tool")), None)
    return insight.get("round"), str(tool) if tool else None


def _job_story(entry: dict[str, Any], numbers: dict[str, int]) -> dict[str, Any]:
    """One job of the order as the story tells it, from its `order_jobs_view` entry."""
    state = _STATE_OF_PHASE.get(str(entry.get("phase")), "failed")
    detail: dict[str, Any] = {}
    if state == "waiting" and entry.get("waits_for"):
        detail = {"after_job": numbers.get(str(entry["waits_for"])), "after_job_id": entry["waits_for"]}
    elif state in ("blocked", "failed") and entry.get("blocking_criterion"):
        detail = {"criterion": entry["blocking_criterion"]}
    round_, tool = _running_detail(str(entry["job_id"])) if state == "running" else (None, None)
    tasks = entry.get("tasks") or {}
    return {"job_id": entry["job_id"], "number": numbers[str(entry["job_id"])], "title": entry.get("title", ""),
            "state": state, "state_detail": detail,
            "tasks": {"done": tasks.get("done", 0), "total": tasks.get("total", 0)},
            "round": round_, "tool": tool, "story": entry.get("story")}


def _milestone_goals(mission_ids: set[str]) -> dict[str, dict[str, str]]:
    """Each mission's milestone goals by id, read from its current plan; {} for a mission with none."""
    from packages.orchestration.mission_compiler import mission_plan_of
    from packages.orchestration.mission_state import list_missions, project_ids_with_missions

    goals: dict[str, dict[str, str]] = {}
    for project_id in project_ids_with_missions() if mission_ids else []:
        for mission in list_missions(project_id):
            if str(mission.id) in mission_ids:
                plan = mission_plan_of(mission)
                goals[str(mission.id)] = {str(m.id): str(m.goal) for m in plan.milestones} if plan else {}
    return goals


def order_client_story(paths: Any, record: Any) -> dict[str, Any]:
    """The story of the order RECORD names: its state and phase as `remedy client order` reads them,
    who gave it, and its missions with their milestones and jobs, in planned order."""
    from packages.orchestration.mission_contract import JOB_MILESTONE_KEY
    from packages.orchestration.pingpong_job import load_job_plan
    from packages.orchestration.scope_decision import story_scope
    from packages.orchestration.serve_runs import order_record_payload

    payload = order_record_payload(paths, record)
    entries = payload["jobs"]
    numbers = {str(entry["job_id"]): position for position, entry in enumerate(entries, start=1)}
    goals = _milestone_goals({str(entry["mission_id"]) for entry in entries if entry.get("mission_id")})
    missions: dict[str | None, dict[str | None, list[dict[str, Any]]]] = {}
    for entry in entries:
        job = load_job_plan(str(entry["job_id"]))
        milestone = str((job.metadata or {}).get(JOB_MILESTONE_KEY) or "") or None if job is not None else None
        missions.setdefault(entry.get("mission_id"), {}).setdefault(milestone, []).append(_job_story(entry, numbers))
    return {
        "order_id": record.order_id, "client": record.client or None,
        "state": payload["state"], "phase": payload["phase"],
        # amend1026 D2: each job of one walk keeps the same scope decision, so the first one found speaks.
        "scope": next((found for found in (story_scope(str(entry["job_id"])) for entry in entries) if found), None),
        "missions": [{"mission_id": mission_id, "milestones": [
            {"id": milestone, "goal": goals.get(str(mission_id), {}).get(str(milestone)) if milestone else None,
             "jobs": jobs} for milestone, jobs in milestones.items()]}
            for mission_id, milestones in missions.items()],
    }


def order_story_answer(*, order: str) -> dict[str, Any]:
    """The answer `GET /api/v1/orders/{order}/story` and `remedy client order-story --json` share:
    the order's story, or `order_not_found` for an id no record names."""
    from apps.cli.json_envelope import build_error, build_ok
    from packages.orchestration.serve_paths import serve_paths
    from packages.orchestration.serve_runs import order_not_found_message, resolve_order_record

    paths = serve_paths()
    record = resolve_order_record(paths, order)
    if record is None:
        return build_error("order_not_found", order_not_found_message(order))
    return build_ok(**order_client_story(paths, record))
