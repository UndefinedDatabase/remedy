"""One job's run story: a read-only projection a client renders in its own words (amend1015 Phase 1.1).

`GET /api/v1/jobs/{job}/story` and its twin `remedy client story <job> --json` answer it. It is
built only from what the runner really writes: the job's record (its state, its tasks and their
statuses, its times, its stop and its decline), the run log's `task_run_started`,
`task_round_*` and `task_run_*` events, the job's open decisions, the apply records
(`job_apply.job_apply_landed`, an apply record reading `applied`), the job's result diff, and the
tokens and calls the one reader `job_tokens.job_token_summary` reads from the call ledgers. A
task's status is read through `task_lifecycle` and a result that waits for its apply through
`job_apply_pending_fields`, the readers the run report and the digest use (DECISION amend1015f
D8), so the story never maps a persisted word a second way.

Every word in the answer is one of `client_story_words`' closed lists; arguments are numbers and
paths relative to the repository. The story carries no prose Remedy wrote, no secret, no path
outside the repository, no shell command and no money figure. `note_open` is true exactly when
the job has not ended and at least one of its tasks can still take a note — the same two
conditions `steering.steer_task_command` checks — since `POST /api/v1/jobs/{job}/note` takes
one (DECISION F303 D2 (4)).

Public API::

    build_client_story(plan, *, events, now) -> dict
    job_client_story(job_id, plan) -> dict
"""

from __future__ import annotations

import re
import subprocess
from datetime import datetime, timezone
from pathlib import PurePosixPath
from typing import Any
from urllib.parse import quote

from packages.orchestration.client_story_words import STORY_QUESTIONS
from packages.orchestration.order_verification import job_verification
from packages.orchestration.task_lifecycle import task_lifecycle_or_empty

#: The run-log events that end one task's run.
_TASK_END_EVENTS = frozenset({"task_run_completed", "task_run_failed", "task_run_noop", "task_vetoed"})
#: The run-log events that mean a task's own check is running.
_TASK_CHECK_EVENTS = frozenset({"test_run_requested", "test_run_started"})
#: A task's lifecycle word to the status the story names it by.
_TASK_STORY_STATUS = {"planned": "waiting", "open": "running", "done": "done",
                      "skipped": "skipped", "blocked": "failed"}
#: The final statuses that mean the reviewer did not pass the task in the rounds it had.
_REVIEW_NOT_PASSED = frozenset({"review_failed", "repair_exhausted", "max_rounds_reached",
                                "review_inconsistent"})
#: The refusals of `task_deliverables.deliverable_files_refusal`, the first word of a task's error:
#: Remedy's own check of the change did not pass it (R-1342, R-1348, R-1363).
_DELIVERABLE_REFUSALS = frozenset({"named_files_unchanged", "protected_file_changed", "unrequested_file_changed"})
#: A stop reason `stop_reasons.derive_stop_reasons` computes afresh on every read: it has no record
#: an answer could resolve, so it is no question (DECISION amend1015f D13).
_DERIVED_STOP = "sr:derived_"
_PROVIDER_DOWN = frozenset({"provider_unavailable", "provider_timeout"})
#: A provider's id as the catalog names it (`claude`, `claude-cli`, `pi`, `ollama`, `fake`).
_PROVIDER_ID = re.compile(r"[a-z][a-z0-9-]{0,31}")


def _word(key: str, **args: Any) -> dict[str, Any]:
    return {"key": key, "args": args}


def _repo_path(value: Any) -> str | None:
    """VALUE when it is a path relative to the repository, else None (never a private path)."""
    text = str(value or "").strip()
    if not text or text.startswith(("/", "~", "\\")) or ".." in PurePosixPath(text).parts:
        return None
    return text


def _when(value: Any) -> datetime | None:
    try:
        moment = datetime.fromisoformat(str(value or ""))
    except ValueError:
        return None
    return moment if moment.tzinfo else moment.replace(tzinfo=timezone.utc)


def _task_events(events: list[dict[str, Any]]) -> tuple[dict[str, int], dict[str, dict[str, Any]]]:
    """(the highest round each task reached, the last run-log event of each task)."""
    rounds: dict[str, int] = {}
    last: dict[str, dict[str, Any]] = {}
    for event in events:
        task_id = str(event.get("task_id") or "")
        if not task_id:
            continue
        last[task_id] = event
        if event.get("event") == "task_round_completed":
            number = (event.get("metadata") or {}).get("round_number")
            if isinstance(number, int):
                rounds[task_id] = max(rounds.get(task_id, 0), number)
    return rounds, last


def _task_file(task: Any) -> str | None:
    inputs = getattr(task, "inputs", None) or {}
    candidates = [inputs.get("deliverable") if isinstance(inputs, dict) else None,
                  *(getattr(task, "files_hint", None) or ()),
                  *(getattr(task, "safe_diff_files", None) or ())]
    return next((path for path in map(_repo_path, candidates) if path), None)


def _task_files(task: Any) -> list[str]:
    manifest = getattr(task, "apply_manifest", None)
    proofs = [proof.path for proof in getattr(manifest, "applied_file_proofs", None) or ()]
    named = proofs or list(getattr(task, "safe_diff_files", None) or ())
    return [path for path in map(_repo_path, named) if path]


def _open_task(plan: Any, last: dict[str, dict[str, Any]]) -> tuple[Any, dict[str, Any] | None]:
    """The task whose run started and has not ended, with its last event; else the next task to run."""
    for task in plan.tasks:
        event = last.get(str(task.task_id))
        if event is not None and event.get("event") not in _TASK_END_EVENTS:
            return task, event
    pending = next((t for t in plan.tasks if task_lifecycle_or_empty(t.status) == "planned"), None)
    return pending, None


def _working_round(event: dict[str, Any] | None, rounds: dict[str, int], task_id: str) -> int:
    if event is None:
        return 1
    number = (event.get("metadata") or {}).get("round_number")
    if event.get("event") == "task_round_repaired" and isinstance(number, int):
        return number
    if event.get("event") == "task_round_completed" and isinstance(number, int):
        return number + 1
    return max(rounds.get(task_id, 0), 1)


def _changes(plan: Any) -> list[dict[str, Any]]:
    """The job's result diff as `{path, added, removed}` rows; none when it cannot be read."""
    from packages.orchestration.data_paths import job_dir
    from packages.orchestration.diff_parser import parse_unified_diff_to_view

    name = str(getattr(plan, "result_diff_path", "") or "")
    if not name or _repo_path(name) is None:
        return []
    try:
        view = parse_unified_diff_to_view((job_dir(plan.job_id) / name).read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, ValueError):
        return []
    rows = []
    for entry in view.get("files") or ():
        path = _repo_path(entry.get("path"))
        stats = entry.get("stats") or {}
        if path:
            rows.append({"path": path, "added": int(stats.get("added") or 0),
                         "removed": int(stats.get("deleted") or 0)})
    return rows


def _found_files(plan: Any) -> dict[str, Any] | None:
    """`found_files` for the tree the job started from, read from the job's own repository."""
    tree, repo = str(plan.job_initial_tree or ""), str(plan.repo_path or "")
    if not tree or not repo:
        return None
    try:
        listed = subprocess.run(["git", "-C", repo, "ls-tree", "-r", "-z", "--name-only", tree],
                                capture_output=True, timeout=10, check=True).stdout
    except (OSError, subprocess.SubprocessError):
        return None
    names = sorted(name for name in listed.decode("utf-8", "replace").split("\0") if name)
    return _word("found_files", n=len(names), first=_repo_path(names[0]) if names else None)


def _failure_reason(plan: Any, rounds: dict[str, int]) -> dict[str, Any]:
    """Why a job ended blocked or failed, as one closed reason."""
    tasks = list(plan.tasks)
    finals = {str(t.final_status or "") for t in tasks}
    if finals & _PROVIDER_DOWN:
        config = getattr(plan, "execution_config", None)
        name = str(getattr(config, "builder", "") or "")
        return _word("provider_unavailable", provider=name if _PROVIDER_ID.fullmatch(name) else "unknown")
    if "sandbox_unavailable" in finals or _sandbox_refused_a_check(plan):   # R-1343: no test could run
        return _word("sandbox_unavailable")
    if any("project_rules_too_large" in str(t.final_status_detail or "") for t in tasks):
        return _word("project_rules_too_large")     # R-1347: the repository's instructions exceed one call
    failed_tests = [r for r in job_verification(plan)["runs"] if r["status"] == "failed"]
    if failed_tests or any(t.final_status == "test_failed" for t in tasks):
        return _word("tests_failed", n=max(len(failed_tests), 1))
    # rel-1019 (R-1367): a change Remedy's file check refused read `unknown`, although the release
    # matrix promised `review_not_passed`, the word a protected-file refusal was said to read.
    stuck = [t for t in tasks if t.final_status in _REVIEW_NOT_PASSED
             or str(t.error or "").split(":", 1)[0] in _DELIVERABLE_REFUSALS]
    if stuck:
        return _word("review_not_passed", rounds=max(rounds.get(str(t.task_id), 0) for t in stuck))
    if "target_mutation_blocked" in finals:
        return _word("target_changed")
    if getattr(plan, "stop_source", "") == "budget" or "budget_exhausted" in finals:
        return _word("budget_exhausted")      # a job budget, or a Pi loop ended at its cap (exec-1017 D4)
    return _word("unknown")


def _sandbox_refused_a_check(plan: Any) -> bool:
    """True when the tool sandbox refused one of the job's DoD checks, which then ran nothing."""
    from packages.orchestration.dod_gate import load_gate_result

    checks = (load_gate_result(str(plan.job_id)) or {}).get("checks") or []
    return any(isinstance(check, dict) and check.get("reason") == "sandbox_unavailable" for check in checks)


def _story_state(plan: Any, decision: Any, pending: dict[str, Any], declined: bool,
                 opened: tuple[Any, dict[str, Any] | None], rounds: dict[str, int],
                 ) -> tuple[str, dict[str, Any]]:
    """(the story's state, its state_detail) for the job's record as it stands."""
    state = getattr(plan.state, "value", str(plan.state))
    if decision is not None:
        kind = decision.type if decision.type in STORY_QUESTIONS else "other"
        return "waiting", {"question": kind, "decision_id": decision.id}
    if state == "completed":
        if pending["result_applied"] is True:
            return "done_applied", {}
        if declined:
            return "stopped", {"reason": _word("declined")}
        return "done", {}
    if state in ("failed", "blocked"):
        return "failed", {"reason": _failure_reason(plan, rounds)}
    if state in ("stopped", "cancelled", "paused"):
        reason = ("paused" if state == "paused" else "cancelled" if state == "cancelled" else
                  "budget_exhausted" if getattr(plan, "stop_source", "") == "budget" else "stopped")
        return "stopped", {"reason": _word(reason)}
    if state == "running":
        task, event = opened
        if task is None:
            return ("checking" if plan.tasks else "reading"), {}
        if event is None and all(task_lifecycle_or_empty(t.status) == "planned" for t in plan.tasks):
            return "reading", {}
        if event is not None and event.get("event") in _TASK_CHECK_EVENTS:
            return "checking", {}
        return "working", {"file": _task_file(task),
                           "round": _working_round(event, rounds, str(task.task_id))}
    if not plan.tasks:
        return "reading", {}
    # rel-1019 (R-1366): a rejected plan is final for its job (`REJECTED_PLAN_NEXT_STEP`): the person
    # said no, so it reads declined; before, it read `queued` and offered `run`, which every run refuses.
    from packages.orchestration.job_plan import task_plan_blocks_execution

    if task_plan_blocks_execution(plan) == "rejected":
        return "stopped", {"reason": _word("declined")}
    # exec-1017c (R-1340): planned, nothing runs it. Before, it read `planning` with that step
    # `running` and no next step, so a client showed a job of a split order as busy forever.
    after = _waits_for_job(plan)
    return "queued", ({"after_job": after} if after else {})


def _waits_for_job(plan: Any) -> str:
    """The job of the same order *plan* runs after, while that one's result has not landed; else ""."""
    from packages.orchestration.job_apply import job_apply_landed
    from packages.orchestration.order_jobs import ORDER_JOB_WAITS_KEY

    after = str((getattr(plan, "metadata", None) or {}).get(ORDER_JOB_WAITS_KEY) or "")
    return after if after and not job_apply_landed(after) else ""


def _task_rows(plan: Any, rounds: dict[str, int]) -> list[dict[str, Any]]:
    return [{"title": str(task.title or ""),
             "status": _TASK_STORY_STATUS.get(task_lifecycle_or_empty(task.status), "waiting"),
             "rounds": rounds.get(str(task.task_id)),
             "files": _task_files(task)} for task in plan.tasks]


def _building(tasks: list[dict[str, Any]], state: str, detail: dict[str, Any],
              changes: list[dict[str, Any]], rounds: dict[str, int]) -> tuple[str, Any]:
    """(the building step's status, its phrase)."""
    statuses = [task["status"] for task in tasks]
    if "failed" in statuses or (state == "failed" and statuses):
        reason = detail.get("reason") or {}
        return "failed", reason if reason.get("key") in ("provider_unavailable", "tests_failed",
                                                          "review_not_passed") else None
    if statuses and all(s in ("done", "skipped") for s in statuses):
        if "done" not in statuses:
            return "skipped", None
        if len(changes) == 1:
            total = sum(rounds.values()) or None
            return "done", _word("changed_file_in_rounds", file=changes[0]["path"], rounds=total)
        return "done", _word("changed_files", n=len(changes)) if changes else _word("no_file_changed")
    if state == "working":
        return "running", _word("working_on_file", file=detail.get("file"), round=detail.get("round"))
    if "running" in statuses:
        return "running", None
    return ("skipped" if state == "stopped" else "waiting"), None


def _checking(plan: Any, state: str, building: str) -> tuple[str, Any]:
    """(the checking step's status, its phrase): the tasks' own test runs and the job's DoD test checks.

    exec-1017 D2: read through `job_verification`, so a DoD that ran the tests is never "no test
    command", and tests the order asked for that did not run are never "not requested".
    """
    found = job_verification(plan)
    failed = sum(1 for run in found["runs"] if run["status"] == "failed")
    if failed:
        phrase: Any = _word("tests_failed", n=failed)
    elif found["runs"]:
        phrase = _word("tests_passed", n=len(found["runs"]))
    elif found["status"] == "not_required":
        phrase = _word("tests_not_requested")
    elif found["reason"].startswith("no check ran"):
        phrase = _word("no_test_command")
    else:
        phrase = _word("tests_not_run")
    if state == "checking":
        return "running", phrase
    if state in ("done", "done_applied") or (state in ("stopped", "waiting") and building == "done"):
        return "done", phrase
    if state == "failed" and phrase["key"] == "tests_failed":
        return "failed", phrase
    if state in ("failed", "stopped"):
        return "skipped", None
    return "waiting", None


def _finished(state: str, detail: dict[str, Any], changes: list[dict[str, Any]]) -> tuple[str, Any]:
    if state == "done":
        return "done", _word("waiting_for_apply", n=len(changes))
    if state == "done_applied":
        return "done", _word("applied", n=len(changes))
    if state == "failed":
        return "failed", None
    if state == "stopped":
        declined = (detail.get("reason") or {}).get("key") == "declined"
        return "skipped", _word("declined") if declined else None
    return "waiting", None


def _steps(plan: Any, state: str, detail: dict[str, Any], changes: list[dict[str, Any]],
           rounds: dict[str, int], tokens: dict[str, Any] | None) -> list[dict[str, Any]]:
    """The five steps in their fixed order, each `{id, status, phrase, tokens}`; building adds `tasks`."""
    tasks = _task_rows(plan, rounds)
    planning = "running" if state == "planning" else ("done" if plan.tasks else "waiting")
    building, building_phrase = _building(tasks, state, detail, changes, rounds)
    checking, checking_phrase = _checking(plan, state, building)
    finished, finished_phrase = _finished(state, detail, changes)
    return [
        {"id": "reading", "status": "running" if state == "reading" else "done",
         "phrase": _found_files(plan), "tokens": None},
        {"id": "planning", "status": planning,
         "phrase": _word("planned_tasks", n=len(tasks)) if tasks else None, "tokens": None},
        {"id": "building", "status": building, "phrase": building_phrase, "tasks": tasks,
         "tokens": tokens},
        {"id": "checking", "status": checking, "phrase": checking_phrase, "tokens": None},
        {"id": "finished", "status": finished, "phrase": finished_phrase, "tokens": None},
    ]


def _next(job_id: str, state: str, detail: dict[str, Any], pending: dict[str, Any]) -> dict[str, Any]:
    """The one next step and the documented HTTP operation that takes it."""
    base = f"/api/v1/jobs/{job_id}"
    if state == "done" and pending["result_applied"] is False:
        return {"action": "apply", "route": {"method": "POST", "path": f"{base}/apply"}}
    if state == "waiting":
        decision = quote(str(detail["decision_id"]), safe="")
        return {"action": "answer", "route": {"method": "POST", "path": f"{base}/decisions/{decision}"}}
    # exec-1017c: a queued job that waits for nothing runs, a stop on request resumes; one queued
    # after another job waits for that job's apply, which is that job's own next step.
    if state == "queued" and "after_job" not in detail:
        return {"action": "run", "route": {"method": "POST", "path": f"{base}/run"}}
    if state == "stopped" and (detail.get("reason") or {}).get("key") == "stopped":
        return {"action": "resume", "route": {"method": "POST", "path": f"{base}/run"}}
    # amend1015c D3 (R-1331): Remedy deliberately offers no `retry` for a failed job: a run of it
    # re-attempts no task that ended blocked or failed and ends blocked again, and no route of the
    # public API puts such a task back to pending yet. `retry` stays in the closed list for that route.
    return {"action": "none", "route": None}


def _end(plan: Any, state: str, declined: bool) -> dict[str, Any] | None:
    """How the person ends the job PLAN for good, or None once it has ended (exec-1018b, R-1360).

    `next` is the one step forward; `end` is always the way out, so a client can close every job that
    is still open, whatever it waits for: a completed result waiting for its apply is declined, any
    other open job (queued, running, stopped, blocked, waiting for an answer) is abandoned.
    """
    raw = str(getattr(plan.state, "value", plan.state))
    if raw in ("failed", "cancelled") or state == "done_applied" or declined:
        return None
    action = "decline" if raw == "completed" else "abandon"
    return {"action": action, "route": {"method": "POST", "path": f"/api/v1/jobs/{plan.job_id}/{action}"}}


def _iso(moment: datetime | None) -> str | None:
    return moment.isoformat() if moment is not None else None


def _times(plan: Any, state: str, events: list[dict[str, Any]], declined: dict[str, Any] | None,
           ) -> tuple[datetime | None, datetime | None, datetime | None]:
    """(started, ended, updated): ended is None while the job has not ended; a job that ended
    without a `finished_at` ended at its stop, else at its newest run-log event."""
    from packages.orchestration.job_apply import list_job_apply_records

    newest_event = _when(events[-1].get("timestamp")) if events else None
    started = _when(plan.first_running_at)
    ended = None
    if state in ("done", "done_applied", "failed", "stopped"):
        ended = _when(plan.finished_at) or _when(plan.stopped_at) or newest_event
    moments = [_when(plan.created_at), started, ended, newest_event,
               _when((declined or {}).get("declined_at")),
               *(_when(r.get("finished_at")) for r in list_job_apply_records(str(plan.job_id)))]
    known = [moment for moment in moments if moment is not None]
    return started, ended, max(known) if known else None


# WHY public: the story, the diff's apply guard and the insight (DECISION F311 D1) read one open decision.
def job_story_open_decision(plan: Any, events: list[dict[str, Any]]) -> Any:
    from packages.orchestration.decision_queue import list_decisions

    try:
        open_ones = [d for d in list_decisions(plan, events)
                     if d.status == "open" and not str(d.id).startswith(_DERIVED_STOP)]
    except (OSError, ValueError):
        return None
    return min(open_ones, key=lambda d: str(d.id)) if open_ones else None


# WHY: a client shows a note field only where a note would really be accepted (DECISION F303 D2 (4)).
def _note_open(plan: Any) -> bool:
    """True when `steering.steer_task_command` would still accept a note for one of PLAN's tasks."""
    from packages.orchestration.pingpong_job import job_is_terminal
    from packages.orchestration.steering import STEERABLE_TASK_STATUSES

    if job_is_terminal(plan.state):
        return False
    return any((task.status.value if hasattr(task.status, "value") else str(task.status))
              in STEERABLE_TASK_STATUSES for task in plan.tasks)


# WHY: the one builder of the story, so the route, its twin command and every test read one shape.
def build_client_story(plan: Any, *, events: list[dict[str, Any]],
                       now: datetime | None = None) -> dict[str, Any]:
    """The run story of the job PLAN, from its record and EVENTS (its run log, oldest first)."""
    from packages.orchestration.job_apply import job_result_decline
    from packages.orchestration.job_apply_pending import job_apply_pending_fields
    from packages.orchestration.job_tokens import job_token_summary

    rounds, last = _task_events(events)
    pending = job_apply_pending_fields(plan)
    declined = job_result_decline(plan)
    state, detail = _story_state(plan, job_story_open_decision(plan, events), pending, declined is not None,
                                 _open_task(plan, last), rounds)
    changes = _changes(plan)
    if state in ("done", "done_applied"):
        detail = {"changed_files": len(changes)}
    summary = job_token_summary(plan)
    measured = summary["tokens_in"] is not None or summary["tokens_out"] is not None
    started, ended, updated = _times(plan, state, events, declined)
    duration = None
    if started is not None:
        duration = max(0, int(((ended or now or datetime.now(timezone.utc)) - started).total_seconds()))
    return {
        "order": str(plan.user_prompt or plan.mission or plan.job_title or ""),
        "job_id": str(plan.job_id),
        "updated_at": _iso(updated),
        "started_at": _iso(started),
        "ended_at": _iso(ended),
        "state": state,
        "state_detail": detail,
        "next": _next(str(plan.job_id), state, detail, pending),
        "end": _end(plan, state, declined is not None),
        "steps": _steps(plan, state, detail, changes, rounds,
                        {"in": summary["tokens_in"], "out": summary["tokens_out"]} if measured else None),
        "changes": changes,
        "verification": {key: value for key, value in job_verification(plan).items()
                         if key in ("status", "required")},
        "numbers": {
            "duration_s": duration,
            "tokens_in": summary["tokens_in"],
            "tokens_out": summary["tokens_out"],
            "calls": summary["harness_invocations"] if summary["roles"] else None,
            "model_turns": summary["model_turns"],
            "rounds": sum(rounds.values()) if rounds else None,
        },
        "note_open": _note_open(plan),
    }


def job_client_story(job_id: str, plan: Any) -> dict[str, Any]:
    """The story of the resolved job JOB_ID whose record is PLAN, with its run log read from the data
    root this process resolves; `remedy client story` and `GET /api/v1/jobs/{job}/story` share it."""
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.timeline import load_run_events

    return build_client_story(plan, events=load_run_events(resolve_data_root(), job_id))
