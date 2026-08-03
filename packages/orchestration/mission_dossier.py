"""F071 — the mission dossier: the orchestrator's working memory.

A long mission dies of context bloat unless something maintains a small,
structured account of it. That account is this module's document: five sections
in a fixed order, each holding one kind of fact, under a hard token budget
taken from config.

    GOAL · MILESTONES · RISKS · DECISIONS · NEXT

The disciplines this module holds to:

* **The goal is immutable.** It is copied ONCE, by :func:`start_dossier`, and
  nothing after that can change it. The compression contract has no ``goal``
  field at all (:class:`DossierCompression`), so "never drop the goal" is the
  shape of the schema rather than a sentence in a prompt.
* **Nothing is ever truncated.** Over budget, ONE schema-validated provider
  call rewrites the overweight sections under explicit rules. A compression
  that fails — no provider, a bad answer, a broken rule — keeps the previous
  dossier with the new facts appended and FLAGS it. An honest over-budget
  dossier is worth more than a quietly shortened one.
* **One home per fact.** A risk that closes moves to DECISIONS with its
  outcome rather than being written down twice (A9).
* **The counting basis is labeled, never invented.** The budget counts through
  the EXISTING seam (``token_economy.estimate_text_tokens``) and carries the
  actuals feature's own confidence vocabulary with every count (P6). Remedy
  deliberately does NOT ship a tokenizer for this — see
  :data:`DOSSIER_TOKEN_BASIS`.
* **Over budget is flagged, never truncated.** A document that does not fit
  says so, in the file, and stays complete. Every version is kept as
  ``dossier_v<N>.md`` so a human can audit what changed between two of them.

Section ORDER is fixed for cache friendliness: the dossier is the stable prefix
of the orchestrator prompt (``orchestrator_loop.assemble_context``), so a
reordering would invalidate a provider's prompt cache for no gain.
"""
from __future__ import annotations

import json
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any, ClassVar, Literal

from pydantic import Field

from packages.orchestration.mission_state import mission_evidence_dir
from packages.orchestration.structured_base import _Strict, _Structured

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

    ALL THREE lists are keyed by id and merged the same way: a fact whose id is
    already present REPLACES that line in place (a milestone's state changes, a
    risk is restated, a decision's outcome arrives later), and a new id
    appends at the end. That is what keeps "one line each" true across any
    number of iterations, and it is the same one-home-per-fact rule the rest of
    the module holds to — a restated decision does not become a second decision.
    The DECISIONS section renders the most recent :data:`MAX_RECENT_DECISIONS`
    of the accumulated record.
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


# ---------------------------------------------------------------------------
# The budget — config key, existing counting seam, labeled basis (P6)
# ---------------------------------------------------------------------------

#: Config key for the hard budget. Conservative by default: the dossier is the
#: prompt PREFIX every iteration pays for, so its cost is recurring.
CONFIG_KEY_MAX_TOKENS = "dossier.max_tokens"

#: Used when no config is readable at all. Matches the key's own default.
DEFAULT_MAX_TOKENS = 3000

#: WHAT counted, named so a reader never has to guess. Remedy deliberately does
#: NOT ship a tokenizer for the dossier: F003 established that a count with no
#: provider-measured usage behind it is a character heuristic, and inventing a
#: second counter here would only make the number look more authoritative than
#: it is (P6). A provider call's measured actuals are recorded separately, as
#: that CALL's cost — never as this document's size.
DOSSIER_TOKEN_BASIS = "estimate:chars_per_token (token_economy.estimate_text_tokens)"

#: The confidence vocabulary is the actuals feature's own
#: (``token_measurement``): a character heuristic is ``low``, always.
DOSSIER_TOKEN_CONFIDENCE = "low"


@dataclass(frozen=True)
class DossierTokenCount:
    """A token count that always says what basis produced it."""

    tokens: int
    basis: str = DOSSIER_TOKEN_BASIS
    confidence: str = DOSSIER_TOKEN_CONFIDENCE

    def to_json(self) -> dict[str, Any]:
        return {"tokens": self.tokens, "basis": self.basis,
                "confidence": self.confidence}


def count_dossier_tokens(text: str) -> DossierTokenCount:
    """Count one text through the EXISTING seam, labeled with its basis."""
    from packages.orchestration.token_economy import estimate_text_tokens

    return DossierTokenCount(tokens=estimate_text_tokens(text))


def dossier_tokens(dossier: MissionDossier) -> DossierTokenCount:
    """What this dossier's BODY costs — the number the budget is checked against."""
    return count_dossier_tokens(render_dossier_body(dossier))


def dossier_budget_from_config(config: Any = None, *,
                               max_tokens: int | None = None) -> int:
    """Flag beats config beats default — the precedence the loop's limits use."""
    if max_tokens is not None:
        requested = int(max_tokens)
    else:
        if config is None:
            from packages.orchestration.config import get_config

            config = get_config()
        value = config.get(CONFIG_KEY_MAX_TOKENS)
        requested = DEFAULT_MAX_TOKENS if value is None else int(value)
    if requested < 1:
        raise ValueError(f"dossier budget must be >= 1 token, got {requested}")
    return requested


# ---------------------------------------------------------------------------
# Versioning — every rewrite auditable
# ---------------------------------------------------------------------------

#: One file per version, in the mission's own evidence area beside its plan and
#: its ledger. Versions are never overwritten: a human auditing what a
#: compression dropped needs the version before it to still exist.
DOSSIER_VERSION_TEMPLATE = "dossier_v{version}.md"


def dossier_version_path(project_id: str, mission_id: str, version: int,
                         root: Path | None = None) -> Path:
    """Where one version of one mission's dossier lives."""
    return (mission_evidence_dir(project_id, mission_id, root)
            / DOSSIER_VERSION_TEMPLATE.format(version=int(version)))


def write_dossier_version(project_id: str, mission_id: str,
                          dossier: MissionDossier,
                          root: Path | None = None) -> Path:
    """Store this version. The live prompt uses the newest; the rest are evidence.

    R-0173: a stored version is never overwritten with different bytes. Writing
    the SAME bytes again is a no-op — an idempotent retry must not be an error
    — but different content under a version number that already exists would
    destroy the audit evidence the versioning exists to keep, so it raises
    instead. The original file is left untouched.
    """
    path = dossier_version_path(project_id, mission_id, dossier.version, root)
    text = render_dossier(dossier)
    if path.is_file():
        if path.read_text(encoding="utf-8") == text:
            return path
        raise ValueError(
            f"{path} already holds a different dossier version "
            f"{dossier.version}; stored versions are never overwritten")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def dossier_versions(project_id: str, mission_id: str,
                     root: Path | None = None) -> list[int]:
    """Every stored version number, ascending. Unreadable names are skipped."""
    directory = mission_evidence_dir(project_id, mission_id, root)
    if not directory.is_dir():
        return []
    prefix, suffix = DOSSIER_VERSION_TEMPLATE.split("{version}")
    found: list[int] = []
    for path in directory.glob(f"{prefix}*{suffix}"):
        raw = path.name[len(prefix):-len(suffix)]
        if raw.isdigit():
            found.append(int(raw))
    return sorted(found)


def latest_dossier_version(project_id: str, mission_id: str,
                           root: Path | None = None) -> int:
    """The newest stored version, or 0 when nothing is stored yet."""
    versions = dossier_versions(project_id, mission_id, root)
    return versions[-1] if versions else 0


# ---------------------------------------------------------------------------
# T002 — compression: the ONE provider call, under explicit rules
# ---------------------------------------------------------------------------

#: The provider-facing contract. NOT registered in ``schemas.models``: a
#: compression answer never leaves this module's own call and is never
#: persisted under its tag — what reaches disk is the rewritten dossier
#: markdown. Same reasoning as ``dod_draft_v1`` / ``mission_plan_draft_v1``.
DOSSIER_COMPRESSION_SCHEMA_V = "dossier_compress_draft_v1"

#: The rules the compression runs under, VERBATIM. They are quoted into the
#: prompt and enforced afterwards by :func:`compression_rule_violation` — a
#: rule that only ever appeared in a prompt would be a hope, not a constraint.
COMPRESSION_RULES: tuple[str, ...] = (
    "merge resolved risks away",
    "keep every open item",
    "never drop the goal",
)


class CompressedItem(_Strict):
    """One rewritten line, keyed by the id of a fact that is ALREADY recorded.

    Deliberately carries no state field. The provider rewrites TEXT; whether a
    milestone is done or a risk is closed is carried over from the previous
    dossier, so a compression cannot promote a milestone to done or reopen a
    risk. The authority boundary is the schema's shape, as it is for the
    orchestrator's move.
    """

    id: str
    text: str


class DossierCompression(_Structured):
    """A rewritten dossier (schema ``dossier_compress_draft_v1``).

    There is NO ``goal`` field, and that absence is the enforcement of "never
    drop the goal": the provider has no channel through which to change,
    shorten or omit it. Nothing in the prompt can widen the contract.
    """

    SCHEMA_V: ClassVar[str] = DOSSIER_COMPRESSION_SCHEMA_V
    schema_v: Literal["dossier_compress_draft_v1"]  # required: no default
    milestones: list[CompressedItem] = Field(default_factory=list)
    risks: list[CompressedItem] = Field(default_factory=list)
    decisions: list[CompressedItem] = Field(default_factory=list)
    next_step: str = ""


_COMPRESSION_PROMPT_TEMPLATE = """\
You are compressing a mission dossier that has grown past its token budget.
Rewrite it SHORTER while keeping everything that still matters.

## Current dossier

{body}

## Rules
- {rules}

Concretely:
- Every id below must appear in your answer, with its line rewritten shorter:
  {required}
- Use ONLY ids that already appear in the dossier above. Never invent one.
- These ids are resolved and must NOT appear in "risks" — fold what is worth
  keeping about them into a shorter "decisions" line instead:
  {resolved}
- Answer with one line per id: {{"id": "...", "text": "..."}}.
- next_step is the single next step. Keep it or restate it shorter.

You are not given the mission goal to rewrite, and you must not restate it:
it is preserved outside this call.
"""


def build_compression_prompt(dossier: MissionDossier) -> str:
    """The prompt for the one compression call, with the rules quoted verbatim."""
    required = ", ".join(item.id for item in open_items(dossier)) or "(none)"
    resolved = ", ".join(
        r.id for r in dossier.risks if r.resolved) or "(none)"
    return _COMPRESSION_PROMPT_TEMPLATE.format(
        body=render_dossier_body(dossier),
        rules="\n- ".join(COMPRESSION_RULES),
        required=required,
        resolved=resolved,
    )


def _rebuild(previous: MissionDossier,
             answer: DossierCompression) -> MissionDossier:
    """The compressed dossier: rewritten text, carried-over state, SAME goal.

    The goal is copied from ``previous`` — the same string object the dossier
    started with — so "byte-identical to iteration one" is true by
    construction rather than by the provider's cooperation.
    """
    def carry(current: Sequence[DossierItem],
              rewritten: Sequence[CompressedItem]) -> tuple[DossierItem, ...]:
        by_id = {item.id: item for item in current}
        return tuple(replace(by_id[item.id], text=item.text)
                     for item in rewritten if item.id in by_id)

    return replace(
        previous,
        milestones=carry(previous.milestones, answer.milestones),
        # A resolved risk is not re-listed here — it lives in DECISIONS with
        # its outcome, which is where the compression was told to fold it.
        risks=carry(previous.risks, answer.risks),
        decisions=carry(previous.decisions, answer.decisions),
        next_step=answer.next_step.strip() or previous.next_step,
    )


def _check_rules(previous: MissionDossier, answer: DossierCompression,
                 ) -> tuple[str, MissionDossier]:
    """``(violation, rebuilt)`` — the rule check and the document it judged.

    R-0172: "keep every open item" is verified against the REBUILT document,
    never against the answer's raw id lists. ``_rebuild`` carries items PER
    SECTION, so an open risk returned under ``milestones`` is present in the
    answer and absent from the rebuild — checking the answer would pass it and
    then silently drop the item, which is the exact failure this module exists
    to prevent. The rebuild is what would reach disk, so the rebuild is what
    gets judged.
    """
    known = {item.id for item in
             (*previous.milestones, *previous.risks, *previous.decisions)}
    returned = {item.id for item in
                (*answer.milestones, *answer.risks, *answer.decisions)}
    invented = sorted(returned - known)
    rebuilt = _rebuild(previous, answer)
    if invented:
        return (f"the answer invents fact(s) the dossier never recorded: "
                f"{', '.join(invented)}"), rebuilt

    kept = {item.id for item in (*rebuilt.milestones, *rebuilt.risks)}
    lost = sorted(item.id for item in open_items(previous)
                  if item.id not in kept)
    if lost:
        return (f"{COMPRESSION_RULES[1]}: open item(s) {', '.join(lost)} were "
                f"dropped"), rebuilt

    resolved_ids = {r.id for r in previous.risks if r.resolved}
    still_there = sorted(
        item.id for item in rebuilt.risks if item.id in resolved_ids)
    if still_there:
        return (f"{COMPRESSION_RULES[0]}: resolved risk(s) "
                f"{', '.join(still_there)} are still listed as risks"), rebuilt
    return "", rebuilt


def compression_rule_violation(previous: MissionDossier,
                               answer: DossierCompression) -> str:
    """Why this answer breaks the rules, or "" when it holds to them.

    Checked, not believed — and checked against the document the answer would
    actually produce. See :func:`_check_rules`.
    """
    return _check_rules(previous, answer)[0]


@dataclass(frozen=True)
class CompressionResult:
    """What the one compression call produced — or honestly did not."""

    ok: bool
    dossier: MissionDossier
    status: str
    detail: str = ""
    calls: int = 0
    cost: dict[str, Any] = field(default_factory=dict)


#: The dossier fit; no call was made.
COMPRESSION_WITHIN_BUDGET = "within_budget"
#: The rewrite happened and held to the rules.
COMPRESSION_OK = "compressed"
#: No provider was given, so there was nothing to compress WITH.
COMPRESSION_NO_PROVIDER = "no_provider"
#: The provider answered with something that is not a valid compression.
COMPRESSION_INVALID_ANSWER = "invalid_answer"
#: The answer validated but broke one of the explicit rules.
COMPRESSION_RULE_VIOLATION = "rule_violation"
#: The provider call itself raised.
COMPRESSION_PROVIDER_ERROR = "provider_error"


def compress_dossier(dossier: MissionDossier,
                     call_fn: Callable[[str, int], str],
                     *,
                     on_call: Callable[[int, str, bool, str], None] | None = None,
                     ) -> CompressionResult:
    """Rewrite an over-budget dossier in ONE schema-validated provider call.

    Exactly one call: ``allow_parse_retry=False``. The feature specifies a
    single compression call, and a retry would make the "one call" claim false
    while buying nothing — the honest over-budget fallback is already a
    complete, correct document, so there is nothing to salvage a second call
    for.

    Every failure route returns the dossier UNCHANGED with a status saying
    which route it was. Nothing here truncates; the caller flags.
    """
    from packages.orchestration.orchestrator_loop import measure_call_cost
    from packages.orchestration.structured_outputs import run_structured_call

    try:
        outcome = run_structured_call(
            DossierCompression,
            build_compression_prompt(dossier),
            call_fn,
            on_call=on_call,
            allow_parse_retry=False)
    except Exception as exc:
        return CompressionResult(
            ok=False, dossier=dossier, status=COMPRESSION_PROVIDER_ERROR,
            detail=f"the compression call raised: {exc}")

    cost = measure_call_cost(outcome)
    if not outcome.ok:
        return CompressionResult(
            ok=False, dossier=dossier, status=COMPRESSION_INVALID_ANSWER,
            detail=f"parse-class failure: {outcome.hint}".strip(),
            calls=outcome.calls, cost=cost)

    answer: DossierCompression = outcome.value
    # The rebuild is judged and then returned — the SAME object, so nothing
    # can pass the rule check and then be rebuilt differently (R-0172).
    violation, rebuilt = _check_rules(dossier, answer)
    if violation:
        return CompressionResult(
            ok=False, dossier=dossier, status=COMPRESSION_RULE_VIOLATION,
            detail=violation, calls=outcome.calls, cost=cost)

    return CompressionResult(
        ok=True, dossier=rebuilt, status=COMPRESSION_OK,
        calls=outcome.calls, cost=cost)


@dataclass(frozen=True)
class DossierUpdate:
    """One iteration's update: the new dossier and how it met its budget."""

    dossier: MissionDossier
    tokens: DossierTokenCount
    budget: int
    status: str
    detail: str = ""
    calls: int = 0
    cost: dict[str, Any] = field(default_factory=dict)

    @property
    def over_budget(self) -> bool:
        return self.dossier.over_budget


def _flag(dossier: MissionDossier, count: DossierTokenCount, budget: int,
          reason: str) -> MissionDossier:
    """Mark a dossier as over budget, saying by how much and why."""
    return replace(
        dossier, over_budget=True,
        budget_note=(f"{count.tokens} tokens against a {budget}-token budget "
                     f"(basis: {count.basis}); {reason}"))


def update(dossier: MissionDossier, facts: IterationFacts, *,
           call_fn: Callable[[str, int], str] | None = None,
           budget: int | None = None,
           config: Any = None,
           on_call: Callable[[int, str, bool, str], None] | None = None,
           ) -> DossierUpdate:
    """Append one iteration's facts and keep the document inside its budget.

    Within budget: the appended dossier, no call, no flag. Over budget: ONE
    compression call. If that call fails for ANY reason — no provider, a bad
    answer, a rule violation, an exception — the result is the previous
    dossier with the raw facts appended and an honest over-budget flag. It is
    never a truncation, and a compression that ran but did not free enough
    room still says so.
    """
    limit = dossier_budget_from_config(config, max_tokens=budget)
    appended = replace(append_facts(dossier, facts),
                       over_budget=False, budget_note="")
    count = dossier_tokens(appended)
    if count.tokens <= limit:
        return DossierUpdate(dossier=appended, tokens=count, budget=limit,
                             status=COMPRESSION_WITHIN_BUDGET)

    if call_fn is None:
        reason = "no provider was given, so no compression was attempted"
        return DossierUpdate(
            dossier=_flag(appended, count, limit, reason), tokens=count,
            budget=limit, status=COMPRESSION_NO_PROVIDER, detail=reason)

    result = compress_dossier(appended, call_fn, on_call=on_call)
    if not result.ok:
        return DossierUpdate(
            dossier=_flag(appended, count, limit, result.detail), tokens=count,
            budget=limit, status=result.status, detail=result.detail,
            calls=result.calls, cost=result.cost)

    recount = dossier_tokens(result.dossier)
    if recount.tokens > limit:
        reason = "the compression ran but the document is still over budget"
        return DossierUpdate(
            dossier=_flag(result.dossier, recount, limit, reason),
            tokens=recount, budget=limit, status=COMPRESSION_OK, detail=reason,
            calls=result.calls, cost=result.cost)

    return DossierUpdate(dossier=result.dossier, tokens=recount, budget=limit,
                         status=COMPRESSION_OK, calls=result.calls,
                         cost=result.cost)


# ---------------------------------------------------------------------------
# T003 — loop integration: the maintained document drives the live prompt
# ---------------------------------------------------------------------------

#: The live STRUCTURED state, beside the versioned markdown in the mission's
#: evidence area. The ``dossier_v<N>.md`` files are the human-readable audit
#: trail — diffable, never overwritten — and this file is what the next
#: iteration loads to keep appending. Remedy deliberately does NOT parse the
#: markdown back: a second representation that has to round-trip is a second
#: source of truth, and a compression's result would be at the mercy of a
#: renderer change.
DOSSIER_STATE_FILENAME = "dossier_state.json"


def dossier_state_path(project_id: str, mission_id: str,
                       root: Path | None = None) -> Path:
    """Where one mission's live dossier state lives."""
    return (mission_evidence_dir(project_id, mission_id, root)
            / DOSSIER_STATE_FILENAME)


def _item_json(item: DossierItem) -> dict[str, Any]:
    return {"id": item.id, "text": item.text, "resolved": item.resolved,
            "outcome": item.outcome}


def _item_of(body: Any) -> DossierItem:
    return DossierItem(id=str(body.get("id", "")), text=str(body.get("text", "")),
                       resolved=bool(body.get("resolved", False)),
                       outcome=str(body.get("outcome", "") or ""))


def dossier_to_json(dossier: MissionDossier) -> dict[str, Any]:
    """The dossier as a plain dict — the state file's whole content."""
    return {
        "goal": dossier.goal,
        "milestones": [_item_json(m) for m in dossier.milestones],
        "risks": [_item_json(r) for r in dossier.risks],
        "decisions": [_item_json(d) for d in dossier.decisions],
        "next_step": dossier.next_step,
        "version": dossier.version,
        "over_budget": dossier.over_budget,
        "budget_note": dossier.budget_note,
    }


def dossier_of_json(body: dict[str, Any]) -> MissionDossier:
    """Rebuild a dossier from :func:`dossier_to_json`'s output."""
    return MissionDossier(
        goal=str(body.get("goal", "")),
        milestones=tuple(_item_of(m) for m in body.get("milestones") or ()),
        risks=tuple(_item_of(r) for r in body.get("risks") or ()),
        decisions=tuple(_item_of(d) for d in body.get("decisions") or ()),
        next_step=str(body.get("next_step", "") or ""),
        version=int(body.get("version", 1) or 1),
        over_budget=bool(body.get("over_budget", False)),
        budget_note=str(body.get("budget_note", "") or ""),
    )


def save_dossier_state(project_id: str, mission_id: str,
                       dossier: MissionDossier,
                       root: Path | None = None) -> Path:
    """Persist the live state. Rewritten every iteration — the versions archive."""
    path = dossier_state_path(project_id, mission_id, root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(dossier_to_json(dossier), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    return path


def load_dossier_state(project_id: str, mission_id: str,
                       root: Path | None = None) -> MissionDossier | None:
    """The live state, or None when this mission has no dossier yet.

    An unreadable state file reads as ABSENT rather than raising: a mission
    whose dossier cannot be loaded still gets a fresh one built from its own
    record, which is degraded but never a dead loop.
    """
    path = dossier_state_path(project_id, mission_id, root)
    if not path.is_file():
        return None
    try:
        body = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(body, dict) or not body.get("goal"):
        return None
    return dossier_of_json(body)


def newest_dossier_text(project_id: str, mission_id: str,
                        root: Path | None = None) -> str:
    """The newest stored version's text — what the live prompt uses. "" if none."""
    version = latest_dossier_version(project_id, mission_id, root)
    if not version:
        return ""
    path = dossier_version_path(project_id, mission_id, version, root)
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


#: Id prefix for a risk carried over from the compiled mission plan. Prefixed
#: and index-stable so the same plan risk keeps the same id across iterations —
#: an id that moved would look like a new fact every time.
PLAN_RISK_ID_TEMPLATE = "PR{index:03d}"

#: Id prefix for one recorded loop iteration in DECISIONS.
ITERATION_ID_TEMPLATE = "I{iteration:03d}"


def mission_iteration_facts(mission: Any, *,
                            done_milestones: Sequence[str] = (),
                            ledger: Sequence[dict[str, Any]] = (),
                            ) -> IterationFacts:
    """One iteration's facts, read from the mission record and its own ledger.

    Every fact here is ALREADY recorded somewhere Remedy owns — the compiled
    plan and the append-only decision ledger. Nothing is invented for the
    dossier, so a dossier line can always be traced back to the artifact that
    produced it.
    """
    from packages.orchestration.mission_compiler import mission_plan_of

    plan = mission_plan_of(mission)
    done = set(done_milestones)
    milestones: list[DossierItem] = []
    risks: list[DossierItem] = []
    next_step = ""
    if plan is not None:
        for ms in plan.milestones:
            unmet = sorted(set(ms.depends_on) - done)
            milestones.append(DossierItem(
                id=ms.id, text=ms.goal, resolved=ms.id in done,
                outcome=(f"depends on {', '.join(unmet)}" if unmet else "")))
            if ms.id not in done and not unmet and not next_step:
                next_step = f"advance milestone {ms.id}: {ms.goal}"
        risks = [
            DossierItem(id=PLAN_RISK_ID_TEMPLATE.format(index=index), text=text)
            for index, text in enumerate(plan.risks, start=1)]
    if not next_step:
        next_step = ("every milestone is done — decide whether the mission "
                     "goal is met")

    decisions = [
        DossierItem(
            id=ITERATION_ID_TEMPLATE.format(
                iteration=int(entry.get("iteration", 0) or 0)),
            text=str((entry.get("move") or {}).get("kind", "") or "no move"),
            resolved=True,
            outcome=str((entry.get("outcome") or {}).get("status", "") or ""))
        for entry in ledger]
    return IterationFacts(milestones=milestones, risks=risks,
                          decisions=decisions, next_step=next_step)


def refresh_mission_dossier(project_id: str, mission_id: str, mission: Any, *,
                            root: Path | None = None,
                            call_fn: Callable[[str, int], str] | None = None,
                            budget: int | None = None,
                            config: Any = None) -> DossierUpdate:
    """Advance the mission's dossier by one iteration and store the new version.

    Load the live state (or start one from the mission's goal) -> append this
    iteration's facts -> enforce the budget -> RECONCILE the version against
    the archive -> write ``dossier_v<N>.md`` and the state file. ``call_fn`` is
    the COMPRESSION provider; omitted, an over-budget dossier keeps its honest
    flag rather than making a call the loop's own budget never authorized.

    R-0175 — the reconcile step, and why it is here. The version file is
    written before the state file, so a process that dies between the two
    leaves the archive one ahead of the live state. Without reconciliation the
    next refresh recomputes a version number the archive already holds; as soon
    as any fact has drifted, the never-overwrite guard (R-0173) raises — on
    that refresh and on every retry after it, wedging the mission until a
    human deletes evidence files. Fast-forwarding past the archive's high-water
    mark costs one number and lets a torn write heal itself, while the archive
    stays append-only and the guard stays intact.
    """
    import dataclasses

    from packages.orchestration.mission_compiler import mission_goal
    from packages.orchestration.orchestrator_loop import (
        done_milestones,
        read_ledger,
    )

    current = load_dossier_state(project_id, mission_id, root)
    if current is None:
        current = start_dossier(mission_goal(mission) or f"mission {mission_id}")
    facts = mission_iteration_facts(
        mission, done_milestones=done_milestones(mission),
        ledger=read_ledger(project_id, mission_id, root))
    result = update(current, facts, call_fn=call_fn, budget=budget,
                    config=config)

    latest = latest_dossier_version(project_id, mission_id, root)
    if result.dossier.version <= latest:
        result = dataclasses.replace(
            result,
            dossier=dataclasses.replace(result.dossier, version=latest + 1))

    write_dossier_version(project_id, mission_id, result.dossier, root)
    save_dossier_state(project_id, mission_id, result.dossier, root)
    return result


# ---------------------------------------------------------------------------
# T003 — the recall harness: quality is MEASURED, not assumed
# ---------------------------------------------------------------------------
#
# A REUSABLE deliverable, named as such: F079 (cross-session handoffs) runs the
# same harness against its own artifact. It lives here rather than in a test
# file precisely so a second feature can import it — a harness only the tests
# can reach is not a harness, it is a test.


@dataclass(frozen=True)
class RecallFact:
    """One seeded fact the harness will later look for.

    ``kind`` is ``"milestone"``, ``"risk"`` or ``"decision"``. A fact seeded
    with ``resolved=True`` is one the dossier is ALLOWED to compress away —
    that asymmetry against open facts is the property being measured.
    """

    id: str
    text: str
    kind: str = "risk"
    resolved: bool = False
    outcome: str = ""


#: The seeded 10-fact fixture: open milestones, open risks, risks that close
#: during the run, and recorded decisions. Deliberately mixed — a harness that
#: only seeded open facts could not show the asymmetry it exists to show.
RECALL_FIXTURE_FACTS: tuple[RecallFact, ...] = (
    RecallFact("M001", "the ledger rewrite is released", "milestone"),
    RecallFact("M002", "the payments API stays releasable", "milestone"),
    RecallFact("R001", "the migration is not reversible"),
    RecallFact("R002", "the smoke suite has no fixture project"),
    RecallFact("R003", "the vendor sandbox rate-limits the nightly run"),
    RecallFact("R004", "the staging database predates the schema",
               resolved=True, outcome="staging was rebuilt from the dump"),
    RecallFact("R005", "no rollback was ever rehearsed",
               resolved=True, outcome="rehearsed on 2026-07-30, 4 minutes"),
    RecallFact("D001", "settle on one ledger writer", "decision",
               resolved=True, outcome="reused the existing writer"),
    RecallFact("D002", "keep the legacy endpoint for one release", "decision",
               resolved=True, outcome="kept, deprecation noted"),
    RecallFact("D003", "run the gauntlet before the cutover", "decision",
               resolved=True, outcome="scheduled"),
)

#: Tight on purpose: the fixture must cross the budget partway through, so the
#: harness measures recall through at least one compression or flag, not just
#: through plain appends.
RECALL_BUDGET_TOKENS = 120


@dataclass(frozen=True)
class RecallResult:
    """What the harness measured, per fact — never a single pass/fail number."""

    dossier: MissionDossier
    #: Open facts still findable in the newest dossier. The acceptance set.
    answerable: tuple[str, ...] = ()
    #: Open facts that are NOT findable. Must be empty; any entry is a defect.
    missing: tuple[str, ...] = ()
    #: Resolved facts no longer rendered — allowed, and the point.
    compressed_away: tuple[str, ...] = ()
    #: One entry per simulated iteration, in order.
    updates: tuple[DossierUpdate, ...] = ()

    @property
    def recalled_all_open(self) -> bool:
        return not self.missing


def _recall_iteration_facts(chunk: Sequence[RecallFact]) -> IterationFacts:
    """One iteration's worth of seeded facts, routed to their own sections."""
    milestones = [DossierItem(id=f.id, text=f.text, resolved=f.resolved,
                              outcome=f.outcome)
                  for f in chunk if f.kind == "milestone"]
    risks = [DossierItem(id=f.id, text=f.text) for f in chunk
             if f.kind == "risk"]
    decisions = [DossierItem(id=f.id, text=f.text, resolved=f.resolved,
                             outcome=f.outcome)
                 for f in chunk if f.kind == "decision"]
    # A risk that closes is SEEDED open and then resolved, so the run exercises
    # the real transition rather than a pre-closed shortcut.
    closed = [(f.id, f.outcome) for f in chunk
              if f.kind == "risk" and f.resolved]
    return IterationFacts(milestones=milestones, risks=risks,
                          decisions=decisions, resolved_risks=closed,
                          next_step=f"process {len(chunk)} new fact(s)")


def run_recall_harness(facts: Sequence[RecallFact] = RECALL_FIXTURE_FACTS, *,
                       goal: str = "The seeded mission goal is met",
                       budget: int = RECALL_BUDGET_TOKENS,
                       per_iteration: int = 2,
                       call_fn: Callable[[str, int], str] | None = None,
                       config: Any = None) -> RecallResult:
    """Seed facts across simulated iterations, then measure what survived.

    A fact counts as ANSWERABLE when its id is findable in the newest
    dossier's rendered body — the dossier alone, with no mission record, no
    ledger and no provider to fall back on. That is the whole claim being
    tested: the document is sufficient by itself.

    Open facts must all be answerable. Resolved ones MAY compress away, and
    :attr:`RecallResult.compressed_away` reports which did, so the asymmetry
    is visible rather than assumed.
    """
    dossier = start_dossier(goal)
    updates: list[DossierUpdate] = []
    for start in range(0, len(facts), max(1, per_iteration)):
        chunk = facts[start:start + max(1, per_iteration)]
        result = update(dossier, _recall_iteration_facts(chunk),
                        call_fn=call_fn, budget=budget, config=config)
        dossier = result.dossier
        updates.append(result)

    text = render_dossier_body(dossier)
    open_ids = [f.id for f in facts if not f.resolved]
    resolved_ids = [f.id for f in facts if f.resolved]
    return RecallResult(
        dossier=dossier,
        answerable=tuple(i for i in open_ids if i in text),
        missing=tuple(i for i in open_ids if i not in text),
        compressed_away=tuple(i for i in resolved_ids if i not in text),
        updates=tuple(updates),
    )


def recall_report(result: RecallResult) -> str:
    """The measurement as a human reads it — every number, no verdict word."""
    return "\n".join([
        f"iterations:      {len(result.updates)}",
        f"dossier version: {result.dossier.version}",
        f"tokens:          {dossier_tokens(result.dossier).tokens} "
        f"(basis: {DOSSIER_TOKEN_BASIS})",
        f"over budget:     {result.dossier.over_budget}",
        f"open answerable: {len(result.answerable)} "
        f"({', '.join(result.answerable) or 'none'})",
        f"open missing:    {len(result.missing)} "
        f"({', '.join(result.missing) or 'none'})",
        f"compressed away: {len(result.compressed_away)} "
        f"({', '.join(result.compressed_away) or 'none'})",
    ])
