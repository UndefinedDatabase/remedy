"""
Teacher model transport — the model half of Stage 2 (F255 T004).

``teacher_qa`` is everything about a teacher answer that must not depend on a
model; THIS module is the one part that does. It resolves the teacher's own
transport, calls it once, and records the single ledger row that question cost
through the ``teacher_spend`` seam — the seam T004's own plan carried as an
uncalled risk until this module called it.

WHY THE TEACHER OWNS A TRANSPORT AT ALL: DECISION F255 D8. No generic
text-completion provider exists under ``packages/providers/`` — the closest,
``OllamaPlanner.raw_call``, REQUIRES a schema and resolves model, host,
temperature and num_predict from the PLANNER's configuration surface. A tutor
answer is prose, and borrowing the planner's configuration would make
``teacher.model`` decorative. So the teacher gets one narrow transport behind an
INJECTABLE seam: the ``call`` parameter of :func:`ask_teacher`, defaulting to
:func:`ollama_teacher_call`. Every test injects that seam, so the suite never
opens a socket and never needs a running Ollama.

WHY THE REFUSAL IS NOT "NO MODEL CONFIGURED": DECISION F255 D9.
``resolve_role_config`` fills an unset model from the provider's default, so no
configuration ever reaches that state. Stage 2 refuses when the resolved
provider has NO TEACHER TRANSPORT, when that transport's dependency is absent,
or when the call fails — and each refusal NAMES the provider and the model it
refused for, so the operator can act on it.

A REFUSAL IS NEVER BILLED. There was no model call to pay for, and a row
recording one would be the fabrication ``token_ledger`` refuses.

Remedy deliberately opens NO file here and writes none of its own: the only
write on this path is the one ledger row ``record_teacher_question`` makes, and
that is why ``remedy teach ask`` declares ``write_metadata`` rather than
``read_only`` (DECISION F255 D10).

Public API:: ``TEACHER_TRANSPORTS``, ``TeacherTransportUnavailable``,
``TeacherReply``, ``TeacherAnswer``, ``resolve_teacher_transport``,
``ollama_teacher_call``, ``ask_teacher``.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from packages.orchestration.role_config import resolve_role_config
from packages.orchestration.teacher_qa import (
    DEFAULT_LEVEL,
    build_teacher_context,
    no_model_refusal,
    render_prompt,
)
from packages.orchestration.teacher_spend import (
    TEACHER_ROLE,
    TeacherUsage,
    record_teacher_question,
)

#: The provider names the teacher can ACTUALLY call. It holds ``ollama`` and
#: nothing else, because that is the only transport this round builds; a
#: provider outside this tuple is refused honestly rather than mis-called.
TEACHER_TRANSPORTS: tuple[str, ...] = ("ollama",)

#: The Ollama host default, the same one
#: packages/providers/ollama_planner/provider.py uses. The configured value is
#: read from the existing ``ollama.host`` key, so the teacher adds no second
#: spelling of "where Ollama lives".
_DEFAULT_OLLAMA_HOST = "http://localhost:11434"


class TeacherTransportUnavailable(RuntimeError):
    """A teacher transport could not be used: its dependency is absent, or the call failed.

    Raised by a transport, never by :func:`ask_teacher`, which catches it and
    turns it into a refusal — a teacher that could fail a run would not be the
    passive role F255 specifies.
    """


@dataclass(frozen=True)
class TeacherReply:
    """What ONE transport call returned: the prose, and what it reported it cost."""

    text: str
    usage: TeacherUsage


@dataclass(frozen=True)
class TeacherAnswer:
    """One answered — or refused — teacher question, and its ledger consequence.

    ``call_id`` is the ledger row's id and is None on a refusal, because a
    refusal writes no row. ``billed`` carries ``record_teacher_question``'s own
    durability flag rather than an assumption about it.
    """

    text: str
    model: str
    refused: bool
    call_id: str | None
    billed: bool


def _ollama_host() -> str:
    """Where Ollama lives, from the existing ``ollama.host`` config key."""
    from packages.orchestration.config import get_config

    return get_config().get("ollama.host") or _DEFAULT_OLLAMA_HOST


def _reported_field(response: Any, name: str) -> Any:
    """One usage field of a provider reply, or None when the provider is silent.

    A reply may be an object or a mapping depending on the client version, and
    an ABSENT count must stay absent: substituting 0 for a figure nobody
    reported is the fabrication ``teacher_spend`` documents as worse than an
    honest unknown.
    """
    if isinstance(response, Mapping):
        return response.get(name)
    return getattr(response, name, None)


def _reply_usage(response: Any) -> TeacherUsage:
    """The usage a reply REPORTED, with every unreported figure left NULL.

    ``cost_usd`` is never set here: Ollama reports no price, and computing one
    would invent the figure ``stats cost`` exists to refuse.
    """
    tokens_in = _reported_field(response, "prompt_eval_count")
    tokens_out = _reported_field(response, "eval_count")
    return TeacherUsage(
        tokens_in=tokens_in if isinstance(tokens_in, int) else None,
        tokens_out=tokens_out if isinstance(tokens_out, int) else None,
    )


def _reply_text(response: Any) -> str:
    """The prose of a chat reply, tolerant of the client's two response shapes."""
    message = _reported_field(response, "message")
    content = _reported_field(message, "content") if message is not None else None
    return content if isinstance(content, str) else ""


# The teacher's OWN transport: one free-text chat, no schema, no planner config.
def ollama_teacher_call(prompt: str, *, model: str) -> TeacherReply:
    """Send ``prompt`` to Ollama as ONE free-text chat and return the reply.

    NO schema is passed, deliberately: a tutor answer is prose, and
    ``format=`` would force it into a shape the question did not ask for. A
    missing ``ollama`` package or any call failure raises
    :class:`TeacherTransportUnavailable`, which the caller turns into a refusal.
    """
    try:
        import ollama
    except ImportError as exc:
        raise TeacherTransportUnavailable(
            "the 'ollama' package is not installed; install it with: pip install ollama"
        ) from exc

    try:
        client = ollama.Client(host=_ollama_host())
        response = client.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception as exc:
        raise TeacherTransportUnavailable(f"the Ollama call failed: {exc}") from exc

    return TeacherReply(text=_reply_text(response), usage=_reply_usage(response))


def resolve_teacher_transport(config_file: object | None = None) -> tuple[str, str] | None:
    """The ``(provider, model)`` the teacher can call, or None when it cannot.

    Resolves through ``resolve_role_config("teacher")`` — the same surface every
    other role uses — and returns None when the resolved provider is not in
    :data:`TEACHER_TRANSPORTS`. None is the ONLY refusal condition here: the
    model is never inspected, because ``resolve_role_config`` always fills one.
    """
    config = resolve_role_config(TEACHER_ROLE, config_file=config_file)
    if config.provider not in TEACHER_TRANSPORTS:
        return None
    return config.provider, config.model


def _refusal(provider: str, model: str, *, because: str) -> TeacherAnswer:
    """An honest refusal NAMING the provider and model, billed to nobody."""
    return TeacherAnswer(
        text=no_model_refusal(
            f"the teacher role resolves to provider {provider!r} with model "
            f"{model!r}, and {because}"
        ),
        model=model,
        refused=True,
        call_id=None,
        billed=False,
    )


def ask_teacher(
    question: str,
    *,
    events: Sequence[Mapping[str, Any]] = (),
    code: str | None = None,
    code_path: str | None = None,
    level: str = DEFAULT_LEVEL,
    call: Callable[..., TeacherReply] | None = None,
    job_id: str | None = None,
    project_id: str | None = None,
    ledger_path: Path | str | None = None,
) -> TeacherAnswer:
    """Answer ONE operator question through the teacher's own model.

    In order: build the grounded context, resolve the transport, render the
    prompt, call it, and record exactly ONE ledger row for the call that
    happened. A refusal — no usable transport, or a transport that failed —
    returns before any row is written, because there was no call to bill.

    ``call`` is the injectable seam (DECISION F255 D8); it defaults to
    :func:`ollama_teacher_call` and every test supplies a fake, so no test in
    this repository opens a socket to answer a teacher question.
    """
    context = build_teacher_context(
        question, events=events, code=code, code_path=code_path, level=level
    )
    configured = resolve_role_config(TEACHER_ROLE)
    transport = resolve_teacher_transport()
    if transport is None:
        return _refusal(
            configured.provider,
            configured.model,
            because=(
                "that provider has no teacher transport "
                f"(the teacher can call: {', '.join(TEACHER_TRANSPORTS)})"
            ),
        )

    provider, model = transport
    try:
        reply = (call or ollama_teacher_call)(render_prompt(context), model=model)
    except TeacherTransportUnavailable as exc:
        return _refusal(provider, model, because=f"that transport is unavailable: {exc}")

    call_id, billed = record_teacher_question(
        model=model,
        usage=reply.usage,
        job_id=job_id,
        path=ledger_path,
        project_id=project_id,
    )
    return TeacherAnswer(
        text=reply.text,
        model=model,
        refused=False,
        call_id=call_id,
        billed=billed,
    )
