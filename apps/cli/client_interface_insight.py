"""The insight's part of the machine client interface (F311 T003, DECISION F311 D5).

`apps/cli/client_interface.py` imports from here the answer keys and the key trees of
`remedy client now` and `remedy client insight`, and the lines its page renders for the insight's
words, so that module stays below the structure ratchet's limit. The words themselves live in
`packages/orchestration/job_insight.py`, in the shape of `client_interface_story.py`.
"""

from __future__ import annotations

from typing import Any

#: The top-level keys `remedy client now --json` can answer beside the envelope's own:
#: `now_insight`'s keys (DECISION F311 D1).
CLIENT_NOW_ANSWER_KEYS: tuple[str, ...] = ("jobs", "model_server", "orders", "stall_threshold_s", "workers")

#: The top-level keys `remedy client insight <job> --json` can answer beside the envelope's own:
#: `job_insight`'s keys, and `matches` of the `ambiguous_job_id` refusal, as the story's has it.
CLIENT_INSIGHT_ANSWER_KEYS: tuple[str, ...] = (
    "advice", "budget", "job", "last_output_s", "matches", "order", "phase", "project", "round",
    "stall_reason", "stalled", "state", "stream", "task", "waiting_on", "worker",
)

#: The keys under a JOB ENTRY's own keys (DECISION F311 D1): one tree, shared by `client.now`'s
#: `jobs` and `client.insight`'s top level, not two copies.
JOB_ENTRY_KEY_TREE: dict[str, Any] = {
    "task": {"id": {}, "title": {}},
    "round": {"n": {}, "max": {}},
    "worker": {"role": {}, "provider": {}, "model": {}},
    "budget": {
        "used": {"tokens": {}, "calls": {}, "minutes": {}, "waited_s": {}},
        "limits": {"tokens": {}, "calls": {}, "minutes": {}},
    },
    "waiting_on": {"decision": {}, "type": {}},
}

#: The keys under `client.now`'s top-level keys.
CLIENT_NOW_KEY_TREE: dict[str, Any] = {
    "jobs": JOB_ENTRY_KEY_TREE,
    "orders": {"order": {}, "project": {}, "phase": {}, "jobs": {}},
    "model_server": {"provider": {}, "host": {}, "state": {}, "loaded": {}, "queue": {}},
    "workers": {"running": {}, "free": {}},
}

#: The keys under `client.insight`'s top-level keys: the JOB ENTRY's own, plus `stream`.
CLIENT_INSIGHT_KEY_TREE: dict[str, Any] = {
    **JOB_ENTRY_KEY_TREE,
    "stream": {"at": {}, "role": {}, "kind": {}, "tool": {}, "text": {}, "length": {}},
}

#: The keys of the interface's `insight` key, `job_insight.insight_words()` (DECISION F311 D5).
INSIGHT_WORDS_KEY_TREE: dict[str, Any] = {
    "phases": {}, "stall_reasons": {}, "stream_kinds": {}, "advice": {}, "model_server_states": {},
}

#: Each list of the `insight` key and the label its page line carries.
INSIGHT_WORD_LABELS: tuple[tuple[str, str], ...] = (
    ("phases", "Insight phases"), ("stall_reasons", "Insight stall reasons"),
    ("stream_kinds", "Insight stream kinds"), ("advice", "Insight advice"),
    ("model_server_states", "Insight model server states"),
)


def _listed(values: Any) -> str:
    return ", ".join(f"`{value}`" for value in values) if values else "none"


def render_insight_words_lines(words: dict[str, Any]) -> list[str]:
    """The page's `### Insight words` part: each list of `words` on its own line."""
    lines = ["", "### Insight words", "",
             "The closed words of `remedy client now`, `remedy client insight` and "
             "`GET /api/v1/now` and `GET /api/v1/jobs/{job}/insight`.", ""]
    lines += [f"{label}: {_listed(words[key])}." for key, label in INSIGHT_WORD_LABELS]
    return lines
