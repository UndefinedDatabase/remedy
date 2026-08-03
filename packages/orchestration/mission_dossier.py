"""F071 — the mission dossier: the orchestrator's working memory.

A long mission dies of context bloat unless something maintains a small,
structured account of it. That account is this module's document: five sections
in a fixed order, each holding one kind of fact.

    GOAL · MILESTONES · RISKS · DECISIONS · NEXT

Three disciplines this module holds to:

* **The goal is immutable.** It is copied ONCE, by :func:`start_dossier`, and
  nothing after that can change it.
* **Nothing is ever dropped silently.** Updating APPENDS; the only way a fact
  leaves a section is by being resolved into another one, on the record.
* **One home per fact.** A risk that closes moves to DECISIONS with its
  outcome rather than being written down twice (A9).

Section ORDER is fixed for cache friendliness: the dossier is the stable prefix
of the orchestrator prompt (``orchestrator_loop.assemble_context``), so a
reordering would invalidate a provider's prompt cache for no gain.
"""
from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass, replace

# ---------------------------------------------------------------------------
# The sections — fixed set, fixed order
# ---------------------------------------------------------------------------

SECTION_GOAL = "GOAL"
SECTION_MILESTONES = "MILESTONES"
SECTION_RISKS = "RISKS"
SECTION_DECISIONS = "DECISIONS"
SECTION_NEXT = "NEXT"

#: Every section, in the ONE order they are ever rendered. Assembly order is
#: part of the contract: this text is the cache-stable prefix of every
#: orchestrator prompt, so the same state must render to the same bytes.
DOSSIER_SECTIONS: tuple[str, ...] = (
    SECTION_GOAL,
    SECTION_MILESTONES,
    SECTION_RISKS,
    SECTION_DECISIONS,
    SECTION_NEXT,
)

#: How many decisions the DECISIONS section carries — "the last few, with
#: outcomes". Older ones are what compression is allowed to merge away.
MAX_RECENT_DECISIONS = 5

#: What the NEXT section says when no step has been recorded yet.
NO_NEXT_STEP = "(not decided yet)"


@dataclass(frozen=True)
class DossierItem:
    """One fact with exactly one home in the document.

    ``resolved`` and ``outcome`` carry the item's end state — a done milestone,
    a closed risk, a decision's result. While an item is OPEN
    (``resolved=False``), ``outcome`` holds what is blocking it, if anything.

    A9 edge: a fact that is both a risk and a decision is recorded ONCE, in
    DECISIONS, with the risk closed — :func:`resolve_risk` does exactly that.
    """

    id: str
    text: str
    resolved: bool = False
    outcome: str = ""


@dataclass(frozen=True)
class MissionDossier:
    """The maintained document. Immutable: every update returns a new version.

    ``over_budget`` is the honest flag — set when the rendered body is over the
    configured budget and compression did not (or could not) bring it under.
    ``budget_note`` says why in one line, for a human reading the file.
    """

    goal: str
    milestones: tuple[DossierItem, ...] = ()
    risks: tuple[DossierItem, ...] = ()
    decisions: tuple[DossierItem, ...] = ()
    next_step: str = ""
    #: 1 for the first dossier; incremented by every :func:`update`.
    version: int = 1
    over_budget: bool = False
    budget_note: str = ""


def start_dossier(goal: str) -> MissionDossier:
    """The first version of a mission's dossier. The ONE place the goal is copied.

    Whitespace is collapsed here and never again: the goal must render to the
    same bytes in version 1 and in version 40, which is what makes
    "goal byte-identical to iteration one" checkable at all.
    """
    text = " ".join(str(goal or "").split())
    if not text:
        raise ValueError("a mission dossier needs a goal")
    return MissionDossier(goal=text)


def open_items(dossier: MissionDossier) -> tuple[DossierItem, ...]:
    """Every item that is still open: not-done milestones and open risks.

    This is the set the compression rules protect — "keep every open item".
    Decisions are deliberately absent: they are recorded outcomes, and the
    DECISIONS section is specified as the RECENT few, so an old decision
    compressing away is intended behavior rather than a lost open item.
    """
    return tuple(
        item for item in (*dossier.milestones, *dossier.risks)
        if not item.resolved
    )


# ---------------------------------------------------------------------------
# Rendering — diff-friendly, one item per line
# ---------------------------------------------------------------------------


def _render_milestone(item: DossierItem) -> str:
    state = "done" if item.resolved else "open"
    line = f"- {item.id} [{state}] {item.text}".rstrip()
    if item.outcome:
        line += f" — {'outcome' if item.resolved else 'blocked'}: {item.outcome}"
    return line


def _render_risk(item: DossierItem) -> str:
    return f"- {item.id} {item.text}".rstrip()


def _render_decision(item: DossierItem) -> str:
    return f"- {item.id} {item.text} — outcome: {item.outcome or '(pending)'}"


def dossier_sections(dossier: MissionDossier) -> tuple[tuple[str, str], ...]:
    """Section name -> body, in :data:`DOSSIER_SECTIONS` order, always all five.

    An empty section still renders — a document whose sections appear and
    disappear with its content is not diff-friendly, and a reader cannot tell
    "no open risks" from "the risks section was dropped".
    """
    milestones = "\n".join(_render_milestone(m) for m in dossier.milestones)
    # RISKS is OPEN-ONLY by construction: a resolved risk has moved to
    # DECISIONS with its outcome, so rendering it here would be its second home.
    risks = "\n".join(
        _render_risk(r) for r in dossier.risks if not r.resolved)
    recent = dossier.decisions[-MAX_RECENT_DECISIONS:]
    decisions = "\n".join(_render_decision(d) for d in recent)
    return (
        (SECTION_GOAL, dossier.goal),
        (SECTION_MILESTONES, milestones or "(none yet)"),
        (SECTION_RISKS, risks or "(none open)"),
        (SECTION_DECISIONS, decisions or "(none yet)"),
        (SECTION_NEXT, dossier.next_step or NO_NEXT_STEP),
    )


def render_dossier_body(dossier: MissionDossier) -> str:
    """The budgeted content: the five sections and nothing else.

    The over-budget flag is deliberately NOT part of this text. The flag is
    metadata ABOUT the document; counting it would make the budget check
    depend on its own previous verdict.
    """
    return "\n\n".join(
        f"## {name}\n\n{body}" for name, body in dossier_sections(dossier)) + "\n"


def render_dossier(dossier: MissionDossier) -> str:
    """The document as it is written to disk: the body, plus an honest flag."""
    text = render_dossier_body(dossier)
    if dossier.over_budget:
        text += (f"\n> OVER BUDGET — {dossier.budget_note}\n"
                 f"> Nothing was truncated; this document is complete.\n")
    return text


# ---------------------------------------------------------------------------
# update() — append mechanics
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class IterationFacts:
    """What one iteration adds to the dossier.

    Milestones and risks are keyed by id: a fact whose id is already present
    REPLACES that line (a milestone's state changes; a risk is restated), which
    is what keeps "one line each" true across any number of iterations. A new
    id appends. Decisions always append — they are a history.
    """

    milestones: Sequence[DossierItem] = ()
    risks: Sequence[DossierItem] = ()
    decisions: Sequence[DossierItem] = ()
    #: Replaces the single NEXT step when non-empty; "" leaves it alone.
    next_step: str = ""
    #: Risk ids whose risk is now closed. Each moves to DECISIONS with its
    #: outcome — one home per fact (A9).
    resolved_risks: Sequence[tuple[str, str]] = ()


def _merge_by_id(current: Sequence[DossierItem],
                 incoming: Iterable[DossierItem]) -> tuple[DossierItem, ...]:
    """Replace items whose id is already present, in place; append the rest."""
    merged = list(current)
    index = {item.id: position for position, item in enumerate(merged)}
    for item in incoming:
        if item.id in index:
            merged[index[item.id]] = item
        else:
            index[item.id] = len(merged)
            merged.append(item)
    return tuple(merged)


def resolve_risk(dossier: MissionDossier, risk_id: str,
                 outcome: str) -> MissionDossier:
    """Close a risk and record the fact ONCE, in DECISIONS, with its outcome.

    The A9 edge made mechanical: a fact that is both a risk and a decision does
    not live in two sections. The risk is marked resolved — which removes it
    from the open-only RISKS rendering — and the same id carries its outcome
    into DECISIONS.
    """
    risks = tuple(
        replace(r, resolved=True, outcome=outcome) if r.id == risk_id else r
        for r in dossier.risks)
    if risks == dossier.risks:
        return dossier
    closed = next(r for r in risks if r.id == risk_id)
    decision = DossierItem(id=risk_id, text=closed.text, resolved=True,
                           outcome=outcome)
    return replace(dossier, risks=risks,
                   decisions=_merge_by_id(dossier.decisions, (decision,)))


def append_facts(dossier: MissionDossier,
                 facts: IterationFacts) -> MissionDossier:
    """One iteration's facts, appended into their sections. The GOAL is untouched.

    Pure: no budget check, no provider, no disk. The budget discipline is a
    separate step layered on top of this one, so the append mechanics stay
    testable without a provider anywhere near them.
    """
    updated = replace(
        dossier,
        milestones=_merge_by_id(dossier.milestones, facts.milestones),
        risks=_merge_by_id(dossier.risks, facts.risks),
        decisions=_merge_by_id(dossier.decisions, facts.decisions),
        next_step=facts.next_step.strip() or dossier.next_step,
        version=dossier.version + 1,
    )
    for risk_id, outcome in facts.resolved_risks:
        updated = resolve_risk(updated, risk_id, outcome)
    return updated
