"""F038 T002 — the chat's mechanical intent parse: a typed request becomes a QUESTION for
the read path, an ACTION for exactly one exposed command, or UNKNOWN; an action becomes a
card a person confirms, naming what it would send and what is still missing; and only a
complete card yields the write door's request body, in the door's own argument names
(DECISION F038 D6).

Remedy deliberately does not let the chat act on its own: nothing here sends a command,
writes a file or calls a model, and a card is never confirmable until a person's own words
supplied every argument the door requires.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from packages.orchestration.command_nonce import nonce_is_valid

#: The three shapes `parse_chat_intent` returns.
CHAT_INTENT_QUESTION = "question"
CHAT_INTENT_ACTION = "action"
CHAT_INTENT_UNKNOWN = "unknown"

#: The unknown card's title (S4).
CHAT_UNKNOWN_TITLE = "I can't do that yet"

#: The unknown card's one line names these, in this order (S4).
CHAT_AVAILABLE_ACTIONS = (
    "stop", "pause", "resume", "a note to the builder", "veto", "rerun",
)

#: Every verb T002's first round can reach, each with the write door's own argument names
#: (DECISION F038 D6) — the names `packages/orchestration/ui_server.py`'s `_dispatch_*`
#: methods read off `payload["args"]`, not the command line's. An empty tuple means the
#: door needs nothing beyond `command` and `client_nonce`.
CHAT_VERB_REQUIRED_ARGS: dict[str, tuple[str, ...]] = {
    "job.stop": (),
    "job.pause": (),
    "job.unpause": (),
    "job.steer": ("task_id", "message"),
    "chat.send": ("message",),
    "job.veto-task": ("task_id", "reason"),
    "job.rerun-subtree": ("task_id",),
    "decision.resolve": ("decision_id", "answer"),
    "job.inject": ("text",),
}

#: The card's title for each verb above, over the same keys in the same order.
CHAT_VERB_TITLES: dict[str, str] = {
    "job.stop": "Stop the job",
    "job.pause": "Pause the job",
    "job.unpause": "Resume the job",
    "job.steer": "Send a note to the task's builder",
    "chat.send": "Send a message to the job",
    "job.veto-task": "Veto the task",
    "job.rerun-subtree": "Rerun the task and the tasks after it",
    "decision.resolve": "Answer the decision",
    "job.inject": "Add a task to the plan",
}


class ChatIntentError(ValueError):
    """Raised for a card or a payload this module refuses to build."""


@dataclass(frozen=True)
class ChatIntent:
    """What `parse_chat_intent` read off one line of text: a kind, and for an ACTION its
    verb, its non-empty arguments, and the required names it still lacks."""

    kind: str
    verb: str = ""
    args: dict[str, str] = field(default_factory=dict)
    missing: tuple[str, ...] = ()


@dataclass(frozen=True)
class ChatActionCard:
    """What a person confirms: the verb, a title, the lines that state it, the arguments
    the door would receive, what is still missing, and whether it is complete."""

    verb: str
    title: str
    lines: tuple[str, ...]
    args: dict[str, str]
    missing: tuple[str, ...]
    confirmable: bool


#: Question words S3 names, checked as whole words at the start of the folded text.
_QUESTION_WORDS = (
    "what", "why", "how", "when", "where", "which", "who", "did", "does", "do",
    "is", "are", "was", "were", "can", "could", "has", "have",
)
_QUESTION_PATTERN = re.compile(
    r"^(?:" + "|".join(_QUESTION_WORDS) + r")\b", re.IGNORECASE)

#: A note's four openers, each a whole word, then any run of spaces, ':' or ',' before the
#: message that follows (S3). Order does not affect matching: each opener's own following
#: character decides which one, if any, matches at position 0.
_NOTE_PATTERN = re.compile(
    r"^(?:tell the builder|tell it|note|steer)\b[ :,]*", re.IGNORECASE)

_RUN_AGAIN_PATTERN = re.compile(r"^run again\b", re.IGNORECASE)
_BECAUSE_PATTERN = re.compile(r"\bbecause\b", re.IGNORECASE)

_STOP_WORDS = frozenset({"stop", "cancel", "abort"})
_UNPAUSE_WORDS = frozenset({"resume", "unpause", "continue"})
_VETO_WORDS = frozenset({"veto", "skip", "drop"})
_RERUN_WORDS = frozenset({"rerun", "retry"})


def _fold(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _reason_after_because(text: str) -> str:
    match = _BECAUSE_PATTERN.search(text)
    return text[match.end():].strip() if match else ""


def _is_question(folded: str) -> bool:
    return folded.endswith("?") or bool(_QUESTION_PATTERN.match(folded))


#: The model-written parse (`chat_intent_model.py`) builds its intents through this
#: same missing-argument rule.
def chat_action_intent(verb: str, raw_args: dict[str, str]) -> ChatIntent:
    required = CHAT_VERB_REQUIRED_ARGS[verb]
    args = {name: value for name, value in raw_args.items() if value}
    missing = tuple(name for name in required if not raw_args.get(name))
    return ChatIntent(kind=CHAT_INTENT_ACTION, verb=verb, args=args, missing=missing)


def parse_chat_intent(text: str, *, focused_task_id: str = "") -> ChatIntent:
    """One line of chat becomes a QUESTION, an ACTION or UNKNOWN (S3)."""
    folded = _fold(text)
    if folded[:7].lower() == "please ":
        folded = folded[7:]
    if not folded:
        return ChatIntent(kind=CHAT_INTENT_UNKNOWN)
    if _is_question(folded):
        return ChatIntent(kind=CHAT_INTENT_QUESTION)

    first_word = folded.split(" ", 1)[0].lower()

    if first_word in _STOP_WORDS:
        return chat_action_intent("job.stop", {"reason": _reason_after_because(folded)})
    if first_word == "pause":
        return chat_action_intent("job.pause", {})
    if first_word in _UNPAUSE_WORDS:
        return chat_action_intent("job.unpause", {})

    note_match = _NOTE_PATTERN.match(folded)
    if note_match:
        message = folded[note_match.end():]
        if focused_task_id:
            return chat_action_intent(
                "job.steer", {"task_id": focused_task_id, "message": message})
        return chat_action_intent("chat.send", {"message": message})

    if first_word in _VETO_WORDS:
        return chat_action_intent(
            "job.veto-task",
            {"task_id": focused_task_id, "reason": _reason_after_because(folded)})

    if first_word in _RERUN_WORDS or _RUN_AGAIN_PATTERN.match(folded):
        return chat_action_intent("job.rerun-subtree", {"task_id": focused_task_id})

    return ChatIntent(kind=CHAT_INTENT_UNKNOWN)


def build_action_card(intent: ChatIntent, *, job_id: str) -> ChatActionCard:
    """An intent becomes what a person confirms (S4). A QUESTION has nothing to confirm:
    it belongs to the read path, and building a card for it is a caller error."""
    if intent.kind == CHAT_INTENT_QUESTION:
        raise ChatIntentError(
            "a question belongs to the read path, not an action card")
    if intent.kind == CHAT_INTENT_UNKNOWN:
        available = ", ".join(CHAT_AVAILABLE_ACTIONS)
        return ChatActionCard(
            verb="", title=CHAT_UNKNOWN_TITLE,
            lines=(f"Available: {available}.",),
            args={}, missing=(), confirmable=False)

    lines = [f"Job: {job_id}"]
    if "task_id" in intent.args:
        lines.append(f"Task: {intent.args['task_id']}")
    if "decision_id" in intent.args:
        lines.append(f"Decision: {intent.args['decision_id']}")
    if "answer" in intent.args:
        lines.append(f"Answer: {intent.args['answer']}")
    if "message" in intent.args:
        lines.append(f"Message: {intent.args['message']}")
    if "text" in intent.args:
        lines.append(f"Text: {intent.args['text']}")
    if "after" in intent.args:
        lines.append(f"After: {intent.args['after']}")
    if "reason" in intent.args:
        lines.append(f"Reason: {intent.args['reason']}")
    if intent.missing:
        lines.append(f"Needs: {', '.join(intent.missing)}. Say it again with them.")
    lines.append(f"Command: {intent.verb}")
    return ChatActionCard(
        verb=intent.verb, title=CHAT_VERB_TITLES[intent.verb], lines=tuple(lines),
        args=dict(intent.args), missing=intent.missing, confirmable=not intent.missing)


def card_command_payload(card: ChatActionCard, *, client_nonce: str) -> dict:
    """A complete card's body, in the write door's own argument names (S5)."""
    if not card.confirmable:
        raise ChatIntentError(
            "this card is not confirmable, so it has no command to send")
    if not nonce_is_valid(client_nonce):
        raise ChatIntentError("client_nonce is not a usable id")
    return {"command": card.verb, "client_nonce": client_nonce, "args": dict(card.args)}
