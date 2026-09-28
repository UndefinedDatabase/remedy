"""F035 T002 (DECISION F035 D3) — the phrase catalog: the ONE place a sentence about who
did what, through which door, is worded in the "you did X" dialect. Every ledger entry
`build_ownership_ledger` (`packages/orchestration/ownership.py`) produces renders through
here into exactly one plain sentence; the job report's Ownership section and the
digest's `ownership` key both read the same sentences, so the two surfaces cannot say two
different things about one action.

This module imports only `ownership` among the orchestration modules (for `OwnershipError`,
which an unknown action still raises), reads no file and opens no clock: given the same
entry it renders the same sentence every time.
"""
from __future__ import annotations

from typing import Any

from packages.orchestration.ownership import OwnershipError

__all__ = [
    "ownership_actor_phrase",
    "ownership_sentence",
    "ownership_sentences",
]


def ownership_actor_phrase(actor: dict[str, Any]) -> str:
    """S1 — the actor phrase, first match wins.

    An unattended action (`auto_approved`) always reads as the operator's own `--yes`,
    regardless of the kind or door its record otherwise carries. A `default_policy` or
    `remedy` kind names the mechanism rather than a door. Otherwise the door — `browser`
    (with its token number when one was assigned) or `cli` — names how a human acted; an
    actor whose record names no door, or names the plain word `human`, is simply `You`,
    and any other recorded value is kept verbatim as "recorded as <value>".
    """
    if actor.get("auto_approved"):
        return "You (auto-approved via --yes)"
    kind = actor.get("kind")
    if kind == "default_policy":
        return "The default policy (you accepted at plan approval)"
    if kind == "remedy":
        return f"Remedy's {actor.get('recorded_as', '')} (under this job's configuration)"
    door = actor.get("door")
    token_number = actor.get("token_number", 0)
    if door == "browser" and isinstance(token_number, int) and token_number > 0:
        return f"You (browser, token #{token_number})"
    if door == "browser":
        return "You (browser)"
    if door == "cli":
        return "You (command line)"
    recorded_as = actor.get("recorded_as", "")
    if recorded_as in ("", "human"):
        return "You"
    return f"You (recorded as {recorded_as})"


def _task_phrase(task_id: str, titles: dict[str, str] | None, *, capital: bool = False) -> str:
    """S2 — `task <id>`, or `Task <id>` when *capital*, followed by ` (<title>)` when
    *titles* holds a non-empty title for *task_id* different from the id itself."""
    phrase = f"{'Task' if capital else 'task'} {task_id}"
    title = (titles or {}).get(task_id, "")
    if title and title != task_id:
        phrase += f" ({title})"
    return phrase


def _reason_clause(text: str) -> str:
    """`R` — ` — reason: "<text>"` when *text* is not "", and nothing otherwise."""
    if text:
        return f" — reason: “{text}”"
    return ""


def ownership_sentence(entry: dict[str, Any], titles: dict[str, str] | None = None) -> str:
    """S3 — one entry, rendered into exactly one plain sentence. Raises `OwnershipError`
    for an action with no template."""
    action = entry.get("action")
    actor_phrase = ownership_actor_phrase(entry.get("actor") or {})
    task_id = entry.get("task_id", "")
    task_phrase = _task_phrase(task_id, titles)
    text = entry.get("text", "") or ""
    consequence = entry.get("consequence") or {}
    detail = entry.get("detail") or {}
    kind = consequence.get("kind")
    ids = consequence.get("task_ids") or []
    ref = consequence.get("ref", "")
    reason = _reason_clause(text)

    if action == "task_vetoed":
        sentence = f"{actor_phrase} vetoed {task_phrase}{reason}."
        if kind == "unreachable":
            n = len(ids)
            word = "task" if n == 1 else "tasks"
            sentence += f" {n} downstream {word} could not run: {', '.join(ids)}."
        elif kind == "inert":
            sentence += f" The veto took no effect: {ref}."
        return sentence

    if action == "veto_answered":
        sentence = f"{actor_phrase} answered the replan proposal for {task_phrase}: {text}."
        if ref != "":
            sentence += f" The follow-up job is {ref}."
        return sentence

    if action == "task_injected":
        sentence = f"{actor_phrase} added a task: “{text}”."
        if kind == "task_added":
            added_phrase = _task_phrase(ids[0], titles) if ids else ""
            sentence += f" It became {added_phrase}."
        elif kind == "inert":
            sentence += f" It was not added: {ref}."
        elif kind == "not_folded":
            sentence += " It waits for the next safe point."
        return sentence

    if action == "subtree_rerun":
        sentence = (
            f"{actor_phrase} reran {task_phrase} and the tasks that depend on it: "
            f"{', '.join(ids)}."
        )
        model_override = detail.get("model_override", "")
        if model_override != "":
            sentence += f" Model override: {model_override}."
        return sentence

    if action == "plan_edited":
        command = detail.get("command", "")
        sentence = f"{actor_phrase} edited the plan ({command})"
        if task_id != "":
            sentence += f" for {task_phrase}"
        sentence += f"; the plan is now {ref}."
        return sentence

    if action == "task_edited":
        command = detail.get("command", "")
        return (
            f"{actor_phrase} edited {task_phrase} while the job ran ({command}); "
            f"the plan is now {ref}."
        )

    if action == "steering_sent":
        sentence = f"{actor_phrase} sent a steering message: “{text}”."
        if kind == "consumed":
            consumer = _task_phrase(ids[0], titles, capital=True) if ids else ""
            sentence += f" {consumer} took it in at {ref}."
        else:
            sentence += " No task has taken it in yet."
        return sentence

    if action == "note_sent":
        sentence = f"{actor_phrase} sent a note to {task_phrase}: “{text}”."
        if kind == "consumed":
            sentence += f" It was taken in at {ref}."
        else:
            sentence += " The task has not taken it in."
        return sentence

    if action == "job_paused":
        sentence = f"{actor_phrase} paused the job{reason}."
        if ids:
            sentence += f" Withheld: {', '.join(ids)}."
        return sentence

    if action == "task_paused":
        return f"{actor_phrase} paused {task_phrase}{reason}."

    if action == "job_resumed":
        return f"{actor_phrase} resumed the job."

    if action == "task_resumed":
        return f"{actor_phrase} resumed {task_phrase}."

    if action == "job_stopped":
        return f"{actor_phrase} stopped the job{reason}."

    if action == "hunk_approved":
        hunk_id = detail.get("hunk_id", "")
        return f"{actor_phrase} approved hunk {hunk_id} of {task_phrase}."

    if action == "hunk_rejected":
        hunk_id = detail.get("hunk_id", "")
        return f"{actor_phrase} rejected hunk {hunk_id} of {task_phrase}{reason}."

    if action == "decision_answered":
        question = detail.get("question", "")
        return (
            f"{actor_phrase} answered “{question}” for {task_phrase}: "
            f"“{text}”."
        )

    if action == "clarification_answered":
        question = detail.get("question", "")
        return (
            f"{actor_phrase} answered the plan question “{question}”: "
            f"“{text}”."
        )

    if action == "plan_approved":
        return f"{actor_phrase} approved the plan."

    if action == "plan_rejected":
        return f"{actor_phrase} rejected the plan."

    raise OwnershipError(f"no ownership sentence template for action {action!r}")


def ownership_sentences(ledger: dict[str, Any], titles: dict[str, str] | None = None) -> list[str]:
    """S3 — the whole ledger's entries, in order, each through `ownership_sentence`."""
    return [ownership_sentence(entry, titles=titles) for entry in ledger.get("entries", [])]
