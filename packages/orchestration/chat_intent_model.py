"""F038 T002 — the model-written intent parse: when the mechanical parse reads a chat line as
unknown and `chat.model_written` is on, the `summary` role is asked for a verb, its arguments
and a confidence; every part of the reply is filtered, grounded and checked before
`chat_action_intent` builds the card (DECISION F038 D8).

Remedy deliberately does not let a model's reply choose a task or a decision: the focused task
id always fills `task_id`, and a decision id survives only when it is one of the open decisions
the caller passed in.
"""

from __future__ import annotations

import math
from collections.abc import Callable, Iterable
from typing import ClassVar

from pydantic import BaseModel

from packages.orchestration import chat_intent
from packages.orchestration.chat_answer import chat_call_fn, chat_model_written
from packages.orchestration.result_tour import PROVIDER_CALL_ERRORS
from packages.orchestration.structured_outputs import run_structured_call

#: `GeneratedChatIntent.SCHEMA_V`.
GENERATED_CHAT_INTENT_SCHEMA_V = "generated_chat_intent_v1"
#: A reply's confidence below this floor is treated as unknown (DECISION F038 D8 (4)).
CHAT_MODEL_MIN_CONFIDENCE = 0.7
#: Argument names a verb accepts but does not require, over the same verbs
#: `chat_intent.CHAT_VERB_REQUIRED_ARGS` already requires something of.
CHAT_VERB_OPTIONAL_ARGS: dict[str, tuple[str, ...]] = {
    "job.stop": ("reason",),
    "job.inject": ("after",),
}


class GeneratedChatIntent(BaseModel):
    """The schema the `summary` role is asked to fill for a model-written chat intent
    (DECISION F038 D8 (4)). `check`-free by design: `parse_chat_intent_with_model` is
    what filters, grounds and checks every part of the reply."""

    SCHEMA_V: ClassVar[str] = GENERATED_CHAT_INTENT_SCHEMA_V

    verb: str
    args: dict[str, str]
    confidence: float


#: `parse_chat_intent_with_model`'s own sentinel: distinguishes "no call_fn argument
#: was given" (ask `chat_call_fn(GeneratedChatIntent)` only when the switch is on)
#: from "call_fn=None was given" (the reply is unknown). A bare `None` default
#: cannot tell those apart, mirroring `chat_answer._UNSET_CALL_FN`.
_UNSET_CALL_FN = object()


def build_intent_prompt(
    text: str, *, focused_task_id: str, open_decision_ids: Iterable[str]
) -> str:
    """The prompt handed to the `summary` role: the request, every chat command with its
    title and argument names, the focused task, the open decisions and the answering
    rules (S4)."""
    lines = [
        "The chat received this request. Choose the one command below that carries it "
        "out, or an empty verb when none fits.",
        "",
        f"Request: {text}",
        "",
        "Commands:",
    ]
    for verb, required in chat_intent.CHAT_VERB_REQUIRED_ARGS.items():
        optional = CHAT_VERB_OPTIONAL_ARGS.get(verb, ())
        names = ", ".join(required + optional) if required or optional else "(none)"
        lines.append(f"- {verb} — {chat_intent.CHAT_VERB_TITLES[verb]}: {names}")

    open_decisions = list(open_decision_ids)
    lines.extend([
        "",
        f"Focused task: {focused_task_id or '(none)'}",
        f"Open decisions: {', '.join(open_decisions) if open_decisions else '(none)'}",
        "",
        "Rules:",
        "- reply with exactly one of the commands listed above, or an empty verb "
        "when none of them fits",
        "- use only that command's own argument names",
        "- never invent a task id or a decision id",
        "- give a confidence from 0 to 1",
    ])
    return "\n".join(lines)


def parse_chat_intent_with_model(
    text: str,
    *,
    focused_task_id: str = "",
    open_decision_ids: Iterable[str] = (),
    call_fn: Callable[[str, int], str] | None = _UNSET_CALL_FN,
) -> chat_intent.ChatIntent:
    """The mechanical parse first; only its UNKNOWN asks the model (S5).

    NEVER raises for a reply: a verb outside `chat_intent.CHAT_VERB_REQUIRED_ARGS`, a
    confidence that is not a finite number or is under `CHAT_MODEL_MIN_CONFIDENCE`, an
    exception of `PROVIDER_CALL_ERRORS`, and an outcome that is not ok are all unknown.
    A kept reply's arguments are its own verb's required and optional names only, each
    grounded: `task_id` is always `focused_task_id`, and `decision_id` survives only
    when it is one of `open_decision_ids`.
    """
    mechanical = chat_intent.parse_chat_intent(text, focused_task_id=focused_task_id)
    if mechanical.kind != chat_intent.CHAT_INTENT_UNKNOWN:
        return mechanical

    if call_fn is _UNSET_CALL_FN:
        call_fn = chat_call_fn(GeneratedChatIntent) if chat_model_written() else None
    if call_fn is None:
        return chat_intent.ChatIntent(kind=chat_intent.CHAT_INTENT_UNKNOWN)

    open_decisions = tuple(open_decision_ids)
    prompt = build_intent_prompt(
        text, focused_task_id=focused_task_id, open_decision_ids=open_decisions)
    try:
        outcome = run_structured_call(
            GeneratedChatIntent, prompt, call_fn, allow_parse_retry=True)
    except PROVIDER_CALL_ERRORS:
        return chat_intent.ChatIntent(kind=chat_intent.CHAT_INTENT_UNKNOWN)
    if not outcome.ok:
        return chat_intent.ChatIntent(kind=chat_intent.CHAT_INTENT_UNKNOWN)

    reply = outcome.value
    assert isinstance(reply, GeneratedChatIntent)
    verb = reply.verb
    if verb not in chat_intent.CHAT_VERB_REQUIRED_ARGS:
        return chat_intent.ChatIntent(kind=chat_intent.CHAT_INTENT_UNKNOWN)
    if not math.isfinite(reply.confidence) or reply.confidence < CHAT_MODEL_MIN_CONFIDENCE:
        return chat_intent.ChatIntent(kind=chat_intent.CHAT_INTENT_UNKNOWN)

    allowed_names = chat_intent.CHAT_VERB_REQUIRED_ARGS[verb] + CHAT_VERB_OPTIONAL_ARGS.get(
        verb, ())
    args: dict[str, str] = {}
    for name in allowed_names:
        value = reply.args.get(name, "")
        args[name] = value.strip() if isinstance(value, str) else ""
    if "task_id" in allowed_names:
        args["task_id"] = focused_task_id
    if "decision_id" in allowed_names:
        args["decision_id"] = args["decision_id"] if args["decision_id"] in open_decisions else ""

    return chat_intent.chat_action_intent(verb, args)
