"""F061 T001 — compile a job's intent and Flight Plan into a DoD.

``compile_dod`` merges three sources into one :class:`DoD`:

  1. **compiled** — checks the provider proposes from the user's intent,
     returned in the provider-facing :class:`DoDDraft` shape and validated
     with the same discipline as intake and the flight plan (schema-enforced,
     at most one parse retry, via ``run_structured_call``);
  2. **plan_acceptance** — a check for every plan acceptance line the compiled
     checks do not already cover, so the traceability rule holds by
     construction;
  3. **standard** — whatever registered standard-check providers contribute.
     The registry is the extension seam the product-smoke feature plugs into
     later; it is deliberately nothing more than a named list of callables.

The traceability rule, verbatim from the feature file, is
``dod_schema.TRACEABILITY_RULE``: *every plan acceptance line traceable to a
check id*. :func:`trace_acceptance` reports it for any DoD, and
:func:`assert_acceptance_traceable` raises on a violation — the rule is a
property of the artifact, not a promise about this compiler.

Without a provider the compiler still returns a real DoD, built deterministically
from the plan's acceptance lines and labeled ``compiled=False`` /
``origin="deterministic"``. The schema refuses the dishonest combination, so a
fallback DoD can never be presented as compiled.
"""
from __future__ import annotations

import json
import re
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from packages.orchestration.dod_schema import (
    DOD_DRAFT_SCHEMA_V,
    DOD_SCHEMA_V,
    TRACEABILITY_RULE,
    DoD,
    DoDCheck,
    DoDDraft,
    DraftCheck,
)
from packages.orchestration.schemas.models import FlightPlan
from packages.orchestration.structured_outputs import StructuredOutcome, run_structured_call

#: Fallback pytest selector when an acceptance line names no test path of its own.
DEFAULT_TEST_SELECTOR = "tests"

_ACC_ID_PREFIX = "acc"
_STD_ID_PREFIX = "std"
_MAX_DESCRIPTION_CHARS = 160

#: A test path or node id mentioned inside an acceptance line, e.g.
#: ``tests/orchestration/test_dod_compiler.py::test_x``. Used only to make the
#: deterministic fallback less coarse than "run everything" when the plan
#: already says where the proof lives.
_TEST_PATH_PATTERN = re.compile(
    r"tests?/[\w./-]*\.py(?:::[\w\[\]-]+)?"
    r"|tests?/[\w./-]+",
)


# ---------------------------------------------------------------------------
# Acceptance lines and the traceability rule
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class AcceptanceLine:
    """One acceptance criterion of one planned task.

    ``key`` is ``"<task_id>:<index>"`` — stable for a given plan, and what a
    check's ``acceptance_refs`` point at.
    """

    key: str
    task_id: str
    index: int
    text: str


def acceptance_line_key(task_id: str, index: int) -> str:
    """The stable key for the ``index``-th acceptance line of ``task_id``."""
    return f"{task_id}:{index}"


def plan_acceptance_lines(plan: FlightPlan) -> list[AcceptanceLine]:
    """Every acceptance line in the plan, in plan order."""
    lines: list[AcceptanceLine] = []
    for task in plan.tasks:
        for i, text in enumerate(task.acceptance):
            lines.append(AcceptanceLine(
                key=acceptance_line_key(task.id, i),
                task_id=task.id,
                index=i,
                text=text,
            ))
    return lines


@dataclass(frozen=True)
class TraceabilityReport:
    """Which acceptance lines map to which check ids."""

    #: acceptance key -> the check ids covering it (in DoD order).
    covered: dict[str, tuple[str, ...]]
    #: acceptance keys with no check at all — the rule's violations.
    uncovered: tuple[str, ...]
    #: ``acceptance_refs`` entries pointing at no acceptance line in this plan.
    dangling_refs: tuple[str, ...] = ()

    @property
    def ok(self) -> bool:
        """True when the traceability rule holds for this DoD and plan."""
        return not self.uncovered


class DoDTraceabilityError(Exception):
    """A DoD leaves at least one plan acceptance line without a check."""


def trace_acceptance(dod: DoD, plan: FlightPlan) -> TraceabilityReport:
    """Map every plan acceptance line to the check ids that cover it."""
    lines = plan_acceptance_lines(plan)
    known = {line.key for line in lines}
    covered: dict[str, list[str]] = {line.key: [] for line in lines}
    dangling: list[str] = []

    for check in dod.checks:
        for ref in check.acceptance_refs:
            if ref in known:
                covered[ref].append(check.id)
            elif ref not in dangling:
                dangling.append(ref)

    return TraceabilityReport(
        covered={key: tuple(ids) for key, ids in covered.items()},
        uncovered=tuple(key for key, ids in covered.items() if not ids),
        dangling_refs=tuple(dangling),
    )


def assert_acceptance_traceable(dod: DoD, plan: FlightPlan) -> TraceabilityReport:
    """Enforce the rule: *every plan acceptance line traceable to a check id*.

    Returns the report when it holds; raises :class:`DoDTraceabilityError`
    naming the uncovered lines when it does not.
    """
    report = trace_acceptance(dod, plan)
    if not report.ok:
        raise DoDTraceabilityError(
            f"{TRACEABILITY_RULE}: uncovered acceptance line(s): "
            f"{', '.join(report.uncovered)}")
    return report


# ---------------------------------------------------------------------------
# Standard-check registry (the extension seam)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class StandardCheckContext:
    """What a standard-check provider gets to look at."""

    intake: dict[str, Any]
    plan: FlightPlan


#: name -> provider. A plain ordered mapping: registration order decides check
#: order, and a duplicate name is an error rather than a silent overwrite.
_STANDARD_PROVIDERS: dict[str, Callable[[StandardCheckContext], list[DraftCheck]]] = {}


def register_standard_check_provider(
    name: str,
    provider: Callable[[StandardCheckContext], list[DraftCheck]],
) -> None:
    """Register a standard-check provider under ``name``.

    The seam the product-smoke feature registers its block into. Providers
    return draft checks; the compiler assigns ``source="standard"`` and makes
    the ids unique — a provider cannot label its own provenance.
    """
    if not name or not name.strip():
        raise ValueError("standard-check provider needs a non-empty name")
    if name in _STANDARD_PROVIDERS:
        raise ValueError(f"standard-check provider already registered: {name!r}")
    _STANDARD_PROVIDERS[name] = provider


def unregister_standard_check_provider(name: str) -> None:
    """Remove a registered provider. Unknown names are ignored."""
    _STANDARD_PROVIDERS.pop(name, None)


def registered_standard_check_providers() -> tuple[str, ...]:
    """Names of the registered providers, in registration order."""
    return tuple(_STANDARD_PROVIDERS)


def build_standard_checks(ctx: StandardCheckContext) -> list[DraftCheck]:
    """Collect the draft checks every registered provider contributes."""
    out: list[DraftCheck] = []
    for provider in _STANDARD_PROVIDERS.values():
        out.extend(provider(ctx) or [])
    return out


# ---------------------------------------------------------------------------
# Deterministic construction
# ---------------------------------------------------------------------------

def _unique_id(base: str, taken: set[str]) -> str:
    """``base``, or ``base-2``/``base-3``… when it is already taken."""
    if base not in taken:
        taken.add(base)
        return base
    n = 2
    while f"{base}-{n}" in taken:
        n += 1
    ident = f"{base}-{n}"
    taken.add(ident)
    return ident


def _selector_for(text: str, default_selector: str) -> str:
    """The test path an acceptance line names, else the default selector."""
    match = _TEST_PATH_PATTERN.search(text)
    return match.group() if match else default_selector


def _describe(text: str) -> str:
    collapsed = " ".join(str(text).split())
    if len(collapsed) <= _MAX_DESCRIPTION_CHARS:
        return collapsed
    return collapsed[: _MAX_DESCRIPTION_CHARS - 1] + "…"


def acceptance_checks(
    lines: list[AcceptanceLine],
    *,
    taken: set[str],
    default_selector: str = DEFAULT_TEST_SELECTOR,
) -> list[DoDCheck]:
    """One pytest check per DISTINCT selector across ``lines``.

    Lines that resolve to the same selector share a check — the rule asks for
    at least one check id per acceptance line, not for a duplicate process per
    line. Every line still appears in exactly one check's ``acceptance_refs``,
    so the mapping stays total.
    """
    by_selector: dict[str, list[AcceptanceLine]] = {}
    for line in lines:
        by_selector.setdefault(_selector_for(line.text, default_selector), []).append(line)

    checks: list[DoDCheck] = []
    for n, (selector, group) in enumerate(by_selector.items(), 1):
        checks.append(DoDCheck(
            id=_unique_id(f"{_ACC_ID_PREFIX}-{n:03d}", taken),
            kind="pytest",
            spec={"selector": selector},
            blocking=True,
            source="plan_acceptance",
            acceptance_refs=[line.key for line in group],
            description=_describe(group[0].text),
        ))
    return checks


def deterministic_dod(
    plan: FlightPlan,
    *,
    intake: dict[str, Any] | None = None,
    default_selector: str = DEFAULT_TEST_SELECTOR,
) -> DoD:
    """Build the honest no-provider DoD from the plan's acceptance lines.

    Coarser than a compiled DoD — it proves the named tests are green rather
    than reasoning about intent — but it is real, runnable, and labeled for
    what it is: ``compiled=False``, ``origin="deterministic"``.
    """
    taken: set[str] = set()
    checks = acceptance_checks(
        plan_acceptance_lines(plan), taken=taken, default_selector=default_selector)
    checks.extend(_standard_checks_as_compiled(
        StandardCheckContext(intake=dict(intake or {}), plan=plan), taken=taken))
    return DoD(
        schema_v=DOD_SCHEMA_V,
        checks=checks,
        compiled=False,
        origin="deterministic",
    )


def _standard_checks_as_compiled(
    ctx: StandardCheckContext, *, taken: set[str],
) -> list[DoDCheck]:
    out: list[DoDCheck] = []
    for draft in build_standard_checks(ctx):
        data = draft.model_dump()
        data["id"] = _unique_id(f"{_STD_ID_PREFIX}-{draft.id}", taken)
        out.append(DoDCheck(**data, source="standard"))
    return out


# ---------------------------------------------------------------------------
# Provider path
# ---------------------------------------------------------------------------

_DOD_PROMPT_TEMPLATE = """\
You are compiling a Definition of Done. Given the job intake and the approved
flight plan below, propose the concrete checks that prove this work is done.

## Intake
{intake_json}

## Flight Plan Acceptance Lines
{acceptance_lines}

## Rules
- Each check needs a unique id (e.g. "c1", "lint", "build").
- kind is one of: pytest, lint, build, runtime_flow, custom_cmd.
- spec is declarative and kind-specific:
  - pytest: {{"selector": "<path or node id>"}}
  - lint:   {{"tool": "<linter>", "args": [...], "paths": [...]}}
  - build:  {{"tool": "<build tool>", "args": [...]}}
  - custom_cmd: {{"argv": ["<program>", "<arg>", ...]}}
  - runtime_flow: {{"steps": [{{"action": "...", "expect": "..."}}]}}
- blocking is true when a red check means the job is NOT done.
- acceptance_refs lists the acceptance-line keys (shown above) a check
  proves. Cover as many as you can justify; anything you leave uncovered
  gets a generated check instead.
- Propose only checks that can actually run in this repository. Do not
  invent tools or paths that are not evidenced by the intake or the plan.

Return ONLY a JSON object matching the {schema_v} schema.
"""


def _build_dod_prompt(intake: dict[str, Any], lines: list[AcceptanceLine]) -> str:
    rendered = "\n".join(f"- {line.key}: {line.text}" for line in lines) or "(none)"
    return _DOD_PROMPT_TEMPLATE.format(
        intake_json=json.dumps(intake, indent=2, sort_keys=True),
        acceptance_lines=rendered,
        schema_v=DOD_DRAFT_SCHEMA_V,
    )


@dataclass
class DoDCompileResult:
    """Outcome of a DoD compilation, provider path or fallback."""

    dod: DoD
    #: ``"llm"`` when the provider produced the compiled checks, else
    #: ``"deterministic"``. Mirrors ``dod.origin``; kept for symmetry with
    #: IntakeResult/FlightPlanResult.
    source: str
    #: Why the provider path was not used, when it was not.
    error_hint: str = ""
    calls: int = 0
    call_log: list[dict[str, Any]] = field(default_factory=list)
    #: The traceability report for the returned DoD. Always computed.
    traceability: TraceabilityReport | None = None


def compile_dod(
    intake: dict[str, Any],
    plan: FlightPlan,
    call_fn: Callable[[str, int], str] | None = None,
    *,
    on_call: Callable[[int, str, bool, str], None] | None = None,
    default_selector: str = DEFAULT_TEST_SELECTOR,
) -> DoDCompileResult:
    """Compile intake + plan into a DoD, merging the three check sources.

    ``call_fn is None`` — or any provider failure — yields the deterministic
    fallback rather than an exception or an empty DoD: a job without a
    provider still gets a real, runnable definition of done.

    The returned DoD always satisfies the traceability rule; the report is
    attached so a caller can show the mapping without recomputing it.
    """
    lines = plan_acceptance_lines(plan)

    if call_fn is None:
        return _fallback(plan, intake, default_selector, hint="no provider")

    try:
        outcome: StructuredOutcome = run_structured_call(
            DoDDraft,
            _build_dod_prompt(intake, lines),
            call_fn,
            on_call=on_call,
            allow_parse_retry=True,
        )
    except Exception as exc:
        return _fallback(
            plan, intake, default_selector, hint=f"provider error: {exc}")

    if not outcome.ok:
        result = _fallback(plan, intake, default_selector, hint=outcome.hint)
        result.calls = outcome.calls
        result.call_log = outcome.call_log
        return result

    assert isinstance(outcome.value, DoDDraft)

    taken: set[str] = set()
    checks: list[DoDCheck] = []
    for draft in outcome.value.checks:
        data = draft.model_dump()
        data["id"] = _unique_id(draft.id, taken)
        checks.append(DoDCheck(**data, source="compiled"))

    # Traceability by construction: only the lines no compiled check claims
    # get a generated check. A compiled check that already names a line is
    # taken at its word — the rule asks for coverage, not for duplication.
    claimed = {ref for check in checks for ref in check.acceptance_refs}
    uncovered = [line for line in lines if line.key not in claimed]
    checks.extend(acceptance_checks(
        uncovered, taken=taken, default_selector=default_selector))
    checks.extend(_standard_checks_as_compiled(
        StandardCheckContext(intake=dict(intake or {}), plan=plan), taken=taken))

    dod = DoD(
        schema_v=DOD_SCHEMA_V, checks=checks, compiled=True, origin="provider")
    return DoDCompileResult(
        dod=dod,
        source="llm",
        calls=outcome.calls,
        call_log=outcome.call_log,
        traceability=assert_acceptance_traceable(dod, plan),
    )


def _fallback(
    plan: FlightPlan,
    intake: dict[str, Any] | None,
    default_selector: str,
    *,
    hint: str,
) -> DoDCompileResult:
    dod = deterministic_dod(
        plan, intake=intake, default_selector=default_selector)
    return DoDCompileResult(
        dod=dod,
        source="deterministic",
        error_hint=hint,
        traceability=assert_acceptance_traceable(dod, plan),
    )
