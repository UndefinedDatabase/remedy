"""
Teacher Q&A grounding — the deterministic half of Stage 2 (F255 T004).

Stage 2 answers an operator question through the teacher's own model. THIS
module is everything about that answer which must not depend on a model: which
grounding source each fact came from, what the level dial changes, and what is
refused when no model is configured. Keeping it here makes the honesty rules of
docs/agents/teacher_conventions.md TESTABLE without a network call.

Remedy deliberately opens NO file here and provides no writer, exactly as
``teacher_narration`` does not. The caller supplies run events already read by
``packages.orchestration.timeline.load_run_events`` and code text already read
read-only, so the read-only invariant stays a property of the whole teacher path
rather than a claim about part of it (DECISION F255 D5).

Each fact is built ONLY from the input its source names, which is what stops the
three sources being mixed silently. :func:`claim_set` is computed from the facts
alone and never from the level, so "the same question at two levels yields
answers whose claim set is the same" is a property of the type rather than a
hope about a prompt.

Public API:: ``GROUNDING_SOURCES`` / ``SOURCE_HONESTY``, ``LEVELS`` /
``DEFAULT_LEVEL`` / ``LEVEL_DEPTH``, ``GroundedFact`` / ``TeacherContext``,
``build_teacher_context``, ``claim_set``, ``render_prompt``,
``no_model_refusal``.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from packages.orchestration.teacher_narration import narrate_run_events

#: The three grounding sources, in the order
#: docs/agents/teacher_conventions.md lists them: what is happening, what this
#: code does, and what a term means.
SOURCE_LEDGER = "ledger"
SOURCE_CODE = "code"
SOURCE_CONCEPT = "concept"

GROUNDING_SOURCES: tuple[str, ...] = (SOURCE_LEDGER, SOURCE_CODE, SOURCE_CONCEPT)

#: The honesty rule each source carries, quoted into the prompt beside its facts
#: so the model is told the rule at the point it would break it.
SOURCE_HONESTY: dict[str, str] = {
    SOURCE_LEDGER: "Assert only what these events show; where they are silent, say unknown.",
    SOURCE_CODE: "Explain only the code shown; never invent a call site, a flag or a file.",
    SOURCE_CONCEPT: "General knowledge, explicitly not a claim about this project's state.",
}

#: The level dial. It selects a DEPTH instruction and nothing else.
LEVELS: tuple[str, ...] = ("student", "beginner", "pro")

DEFAULT_LEVEL = "beginner"

#: Depth per level. Every entry asks for the SAME facts at a different length,
#: which is what keeps :func:`claim_set` level-independent.
LEVEL_DEPTH: dict[str, str] = {
    "student": "Explain from scratch in short plain sentences. Define every term you use.",
    "beginner": "Explain plainly. Define a term the first time it appears.",
    "pro": "Be brief and precise. Skip definitions of common terms.",
}


@dataclass(frozen=True)
class GroundedFact:
    """One fact and the source it is allowed to be asserted from."""

    source: str
    text: str


@dataclass(frozen=True)
class TeacherContext:
    """The small context Stage 2 sends: a question, a level, and labelled facts."""

    question: str
    level: str
    facts: tuple[GroundedFact, ...]


def build_teacher_context(
    question: str,
    *,
    events: Sequence[Mapping[str, Any]] = (),
    code: str | None = None,
    code_path: str | None = None,
    level: str = DEFAULT_LEVEL,
) -> TeacherContext:
    """Assemble the small context for one question.

    Ledger facts are the Stage 1 narration of ``events``, reused rather than
    re-derived. A code fact exists only when code was actually supplied, because
    a fact about code nobody read is the invention this role must refuse. An
    unrecognised ``level`` falls back to :data:`DEFAULT_LEVEL` rather than
    raising: a teacher that could fail a run would not be passive.
    """
    if level not in LEVEL_DEPTH:
        level = DEFAULT_LEVEL

    facts: list[GroundedFact] = [
        GroundedFact(SOURCE_LEDGER, sentence) for sentence in narrate_run_events(list(events))
    ]
    if code is not None and code.strip():
        where = code_path or "the supplied code"
        facts.append(GroundedFact(SOURCE_CODE, f"{where}:\n{code}"))

    return TeacherContext(question=question, level=level, facts=tuple(facts))


def claim_set(context: TeacherContext) -> tuple[str, ...]:
    """The facts this answer may assert, as ``"<source>: <text>"`` strings.

    Computed from the facts ALONE: the level is deliberately not an input, so
    two contexts differing only in level have equal claim sets.
    """
    return tuple(f"{fact.source}: {fact.text}" for fact in context.facts)


def render_prompt(context: TeacherContext) -> str:
    """Render the prompt for one question, grouped by grounding source.

    Each block names its source and carries that source's honesty rule, and the
    question comes last so the cache-stable material sits in front of it.
    """
    lines: list[str] = []
    for source in GROUNDING_SOURCES:
        texts = [fact.text for fact in context.facts if fact.source == source]
        if not texts and source != SOURCE_CONCEPT:
            continue
        lines.append(f"[{source}] {SOURCE_HONESTY[source]}")
        lines.extend(texts)
        lines.append("")
    lines.append(LEVEL_DEPTH[context.level])
    lines.append(f"Question: {context.question}")
    lines.append("Name the source you answer from.")
    return "\n".join(lines)


def no_model_refusal(reason: str) -> str:
    """The honest refusal when Stage 2 has no model to call.

    Names Stage 1 explicitly, because Stage 1 is offline by construction and
    keeps working — the operator should be told what they still have.
    """
    return (
        f"I cannot answer that: {reason}. "
        "Stage 1 narration still works offline: run `remedy teach narrate <job_id>`."
    )
