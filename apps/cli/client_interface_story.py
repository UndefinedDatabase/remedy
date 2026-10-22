"""The run story's part of the machine client interface (operator amendment amend1015-face-migration,
DECISION amend1015f D14).

`apps/cli/client_interface.py` imports from here the answer keys and the key tree of
`remedy client story`, the key tree of the interface's own `story` key, and the lines its page
renders for the story's words, so that module stays below the structure ratchet's limit. The words
themselves live in `packages/orchestration/client_story_words.py`.
"""

from __future__ import annotations

from typing import Any

#: The top-level keys `remedy client story <job> --json` can answer beside the envelope's own:
#: `build_client_story`'s keys, and `matches` of the `ambiguous_job_id` refusal.
CLIENT_STORY_ANSWER_KEYS: tuple[str, ...] = (
    "changes", "dirty_start", "end", "ended_at", "job_id", "matches", "next", "note_open", "numbers",
    "order",
    "started_at", "state", "state_detail", "steps", "updated_at", "verification",
)

#: A job's verification as `order_verification.job_verification` answers it (exec-1017 D2): the
#: `do.run` answer's `jobs` carry it whole; the story carries only `status` and `required`.
JOB_VERIFICATION_KEY_TREE: dict[str, Any] = {
    "status": {}, "required": {}, "request": {}, "reason": {},
    "runs": {"source": {}, "task_id": {}, "check_id": {}, "status": {}, "command": {}, "blocking": {}},
}

#: A phrase or a reason: its key, and its arguments by name; `story`'s phrases and reasons name them.
_WORD_TREE: dict[str, Any] = {"key": {}, "args": {"*": {}}}

#: The keys under the story's top-level keys.
CLIENT_STORY_KEY_TREE: dict[str, Any] = {
    "state_detail": {"file": {}, "round": {}, "reason": _WORD_TREE, "question": {},
                     "decision_id": {}, "changed_files": {}},
    "next": {"action": {}, "route": {"method": {}, "path": {}}},
    "end": {"action": {}, "route": {"method": {}, "path": {}}},
    "steps": {"id": {}, "status": {}, "phrase": _WORD_TREE, "tokens": {"in": {}, "out": {}},
              "tasks": {"title": {}, "status": {}, "rounds": {}, "files": {}}},
    "changes": {"path": {}, "added": {}, "removed": {}},
    "dirty_start": _WORD_TREE,
    "numbers": {"duration_s": {}, "tokens_in": {}, "tokens_out": {}, "calls": {}, "model_turns": {}, "rounds": {}},
    "verification": {"status": {}, "required": {}},
}

#: The keys of the interface's `story` key, `client_story_words.story_words()`; under `phrases`
#: and `reasons` each key is a word mapped to the names of its arguments.
STORY_WORDS_KEY_TREE: dict[str, Any] = {
    "states": {}, "step_ids": {}, "step_statuses": {}, "next_actions": {}, "end_actions": {},
    "phrases": {"*": {}}, "reasons": {"*": {}}, "questions": {}, "verification_statuses": {},
}

#: Each list of the `story` key and the label its page line carries.
STORY_WORD_LABELS: tuple[tuple[str, str], ...] = (
    ("states", "Story states"), ("step_ids", "Story steps"),
    ("step_statuses", "Story step statuses"), ("next_actions", "Story next actions"),
    ("end_actions", "Story end actions"),
    ("questions", "Story questions"), ("verification_statuses", "Story verification statuses"),
)


def _listed(values: Any) -> str:
    return ", ".join(f"`{value}`" for value in values) if values else "none"


def render_story_words_lines(story: dict[str, Any]) -> list[str]:
    """The page's `### Story words` part: each list on its line, then each phrase and reason key
    with the names of its arguments."""
    lines = ["", "### Story words", "",
             "The closed words of `remedy client story` and `GET /api/v1/jobs/{job}/story`. A "
             "phrase or a reason is `{key, args}`; its arguments are numbers, paths relative to the "
             "repository, and `provider`, a provider's id word.", ""]
    lines += [f"{label}: {_listed(story[key])}." for key, label in STORY_WORD_LABELS]
    lines += [f"Story phrase `{key}`: {_listed(args)}." for key, args in story["phrases"].items()]
    lines += [f"Story reason `{key}`: {_listed(args)}." for key, args in story["reasons"].items()]
    return lines


#: The key tree of `order_budget` in a `remedy do` answer: the order's ledger (scale audit 2026-10-17).
ORDER_BUDGET_KEY_TREE: dict = {
    "caps": {"*": {}}, "planner_calls": {}, "planner_calls_by_reason": {"*": {}},
    "refused_calls": {}, "estimated_planning_tokens": {}, "unmeasured_jobs": {},
    "used": dict.fromkeys(("calls", "tokens", "cost_usd", "elapsed_minutes"), {}),
    "jobs": {"*": dict.fromkeys(("calls", "tokens", "cost_usd", "measured", "unpriced_calls"), {})},
    "cost": dict.fromkeys(("cap_usd", "measured_usd", "unpriced_calls", "enforced"), {}),
    "calls": dict.fromkeys(("role", "reason", "attempt", "seconds", "prompt_chars", "response_chars",
                            "outcome", "estimated_tokens", "tokens_estimated"), {}),
}
