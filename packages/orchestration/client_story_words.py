"""The closed words of the run story (operator amendment amend1015-face-migration, Phase 1.1).

`GET /api/v1/jobs/{job}/story` and `remedy client story <job> --json` answer one job's story in
a fixed shape whose every word is one of the lists below, so a client translates each word into
its own language and never shows a sentence Remedy wrote. A phrase and a reason are objects
`{"key": <word>, "args": {...}}`; the tuple beside each key names its arguments, each a number or
a path relative to the repository, and `provider` a provider's id word (DECISION amend1015f D6 and
D12). `story_problems` checks one answer against all of it. The machine client interface
(`apps/cli/client_interface.py`) publishes these lists under its `story` key.

Inside one major version of the interface these lists only grow.
"""

from __future__ import annotations

import json

#: What the job is doing now, one word. `queued` (exec-1017c, R-1340): planned and not running; its
#: `state_detail.after_job` names the job of its order it runs after, when it waits for that one.
STORY_STATES: tuple[str, ...] = (
    "reading", "planning", "working", "checking", "done", "done_applied", "stopped", "failed",
    "waiting", "queued",
)

#: The five steps of every story, always in this order.
STORY_STEP_IDS: tuple[str, ...] = ("reading", "planning", "building", "checking", "finished")

#: The status of one step, and of one task under the building step.
STORY_STEP_STATUSES: tuple[str, ...] = ("waiting", "running", "done", "skipped", "failed")

#: The one next step the story names; `decline` is offered beside `apply` by every client and is
#: never the one next step on its own. `retry` is named by no state since amend1015c D3: no route
#: re-attempts a task that ended blocked (R-1331), and the list only grows. `run` starts a queued job
#: that waits for nothing, `resume` a stopped one; both are `POST /api/v1/jobs/{job}/run` (exec-1017c).
STORY_NEXT_ACTIONS: tuple[str, ...] = ("apply", "decline", "answer", "retry", "none", "run", "resume")
#: How a job that has not ended is ended for good, the story's `end` (exec-1018b, R-1360): a completed
#: result waiting for its apply is declined, any other open job abandoned; `end` is null once it ended.
STORY_END_ACTIONS: tuple[str, ...] = ("abandon", "decline")

#: Every phrase key a step carries, each with the names of its arguments.
STORY_PHRASES: dict[str, tuple[str, ...]] = {
    "found_files": ("n", "first"),
    "planned_tasks": ("n",),
    "working_on_file": ("file", "round"),
    "changed_file_in_rounds": ("file", "rounds"),
    "changed_files": ("n",),
    "no_file_changed": (),
    "no_test_command": (),
    "tests_not_run": (),
    "tests_not_requested": (),
    "tests_passed": ("n",),
    "tests_failed": ("n",),
    "provider_unavailable": ("provider",),
    "review_not_passed": ("rounds",),
    "waiting_for_apply": ("n",),
    "applied": ("n",),
    "declined": (),
}

#: Every reason key `state_detail.reason` carries while the job is stopped or failed. `stopped` is a
#: stop on request, resumable; `cancelled` is a cancel, which ends the job for good (exec-1017c);
#: `sandbox_unavailable` a test command the tool sandbox could not run, so no test ran (R-1343);
#: `project_rules_too_large` the repository's instructions for coding agents are too large for one
#: model call to carry whole, so no call was started (R-1347).
STORY_REASONS: dict[str, tuple[str, ...]] = {
    "provider_unavailable": ("provider",),
    "tests_failed": ("n",),
    "review_not_passed": ("rounds",),
    "target_changed": (),
    "budget_exhausted": (),
    "declined": (),
    "cancelled": (),
    "paused": (),
    "unknown": (),
    "stopped": (),
    "sandbox_unavailable": (),
    "project_rules_too_large": (),
}

#: The job's verification status, `verification.status` (exec-1017 D2): its tests ran and passed or
#: failed, were asked for and did not run, were not asked for and did not run, or the job runs still.
STORY_VERIFICATION_STATUSES: tuple[str, ...] = ("passed", "failed", "not_run", "not_required", "pending")

#: The kinds of question a waiting job asks, `state_detail.question`: the type of its open
#: decision as `packages/orchestration/decision_queue.py` writes it, and `other` for a type this
#: list does not name yet. The question's own text stays in the decision route.
STORY_QUESTIONS: tuple[str, ...] = (
    "patch_approval", "stop_reason", "test_failure", "token_budget", "memory_review",
    "task_plan_approval", "task_decision", "proposal", "other",
)


def story_words() -> dict[str, object]:
    """The lists above as one JSON-ready dict, the `story` key of the machine client interface."""
    return {
        "states": list(STORY_STATES),
        "step_ids": list(STORY_STEP_IDS),
        "step_statuses": list(STORY_STEP_STATUSES),
        "next_actions": list(STORY_NEXT_ACTIONS),
        "end_actions": list(STORY_END_ACTIONS),
        "phrases": {key: list(args) for key, args in STORY_PHRASES.items()},
        "reasons": {key: list(args) for key, args in STORY_REASONS.items()},
        "questions": list(STORY_QUESTIONS),
        "verification_statuses": list(STORY_VERIFICATION_STATUSES),
    }


def _arg_problem(key: str, name: str, value: object) -> str:
    if value is None or isinstance(value, bool):
        return "" if value is None else f"{key}.{name} is a boolean"
    if isinstance(value, int):
        return ""
    if not isinstance(value, str):
        return f"{key}.{name} is neither a number nor a text"
    if name == "provider":
        ok = value.replace("-", "").isalnum() and value[:1].isalpha() and value == value.lower()
        return "" if ok and len(value) <= 32 else f"{key}.{name} is not a provider id"
    parts = value.split("/")
    if value.startswith(("/", "~", "\\")) or ".." in parts or any(c in value for c in "$`;|&<>\n"):
        return f"{key}.{name} is not a path inside the repository"
    return ""


def _word_problems(word: object, closed: dict[str, tuple[str, ...]], where: str) -> list[str]:
    if word is None:
        return []
    if not isinstance(word, dict) or set(word) != {"key", "args"}:
        return [f"{where} is not a {{key, args}} object"]
    key, args = word["key"], word["args"]
    if key not in closed:
        return [f"{where} key {key!r} is not in the closed list"]
    if not isinstance(args, dict) or set(args) != set(closed[key]):
        return [f"{where} {key} carries args {sorted(args) if isinstance(args, dict) else args!r}"]
    return [problem for name, value in args.items() if (problem := _arg_problem(key, name, value))]


def story_problems(story: dict[str, object]) -> list[str]:
    """Every way STORY leaves the closed words of this module; [] for a story that keeps them."""
    problems: list[str] = []
    if story.get("state") not in STORY_STATES:
        problems.append(f"state {story.get('state')!r} is not in the closed list")
    detail = story.get("state_detail") or {}
    if isinstance(detail, dict):
        problems += _word_problems(detail.get("reason"), STORY_REASONS, "state_detail.reason")
        if "question" in detail and detail["question"] not in STORY_QUESTIONS:
            problems.append(f"question {detail['question']!r} is not in the closed list")
    verification = story.get("verification")
    if isinstance(verification, dict) and verification.get("status") not in STORY_VERIFICATION_STATUSES:
        problems.append(f"verification status {verification.get('status')!r} is not in the closed list")
    nxt = story.get("next") or {}
    if not isinstance(nxt, dict) or nxt.get("action") not in STORY_NEXT_ACTIONS:
        problems.append("next.action is not in the closed list")
    end = story.get("end")
    if end is not None and (not isinstance(end, dict) or end.get("action") not in STORY_END_ACTIONS):
        problems.append("end.action is not in the closed list")
    steps = story.get("steps") or []
    if [s.get("id") for s in steps if isinstance(s, dict)] != list(STORY_STEP_IDS):
        problems.append("steps are not the five steps in their order")
    for step in steps if isinstance(steps, list) else []:
        if not isinstance(step, dict):
            continue
        if step.get("status") not in STORY_STEP_STATUSES:
            problems.append(f"step {step.get('id')} status {step.get('status')!r} is not closed")
        problems += _word_problems(step.get("phrase"), STORY_PHRASES, f"step {step.get('id')} phrase")
        for task in step.get("tasks") or []:
            if task.get("status") not in STORY_STEP_STATUSES:
                problems.append(f"task status {task.get('status')!r} is not closed")
    text = json.dumps(story)
    if "$" in text or '"cost_usd"' in text:
        problems.append("the story names money")
    return problems
