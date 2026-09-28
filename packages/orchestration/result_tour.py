"""F036 T001 — the stop shape, the anchor check and the mechanical tour (DECISION F036 D1).

Remedy deliberately does not write a stop whose anchor does not resolve against the job's own
records — an unanchored claim in a guided tour is worse than a shorter one (D1 (3)).

This module builds the guided result tour a job's terminal state can offer a human: at most
eight stops, each a title, a body and an anchor into something the job actually produced.
Building a tour (`collect_tour_context`, `build_fallback_tour`, `generate_result_tour`) stays
pure — no file, no model beyond the injected `call_fn`, no clock. `write_result_tour` is the one
function that touches disk, versioning the tour beside the job's report the way
`run_report.write_final_report` writes it (DECISION F036 D4); `long_run_executor._apply_terminal`
calls it at every reported terminal.
"""

from __future__ import annotations

import json
import logging
import re
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

from pydantic import BaseModel

from packages.common.secure_fs import durable_write_json
from packages.orchestration.data_paths import job_evidence_dir
from packages.orchestration.diff_view_source import build_diff_view
from packages.orchestration.dod_gate import DOD_RESULT_FILENAME, load_gate_result
from packages.orchestration.dod_runners import STATUS_PASSED
from packages.orchestration.evidence_index import resolve_job_evidence_dir
from packages.orchestration.failure_postmortem import FailureSignals, classify
from packages.orchestration.intake import make_structured_call_fn
from packages.orchestration.role_config import resolve_role_config
from packages.orchestration.run_report import NOT_RECORDED, ReportSources, build_report_sources
from packages.orchestration.structured_outputs import run_structured_call

TOUR_SCHEMA = "remedy.tour.v1"
TOUR_FILENAME = "tour.json"
MAX_TOUR_STOPS = 8
TOUR_TITLE_MAX_CHARS = 80
TOUR_BODY_MAX_CHARS = 400
TOUR_ANCHOR_KINDS = ("node", "diff", "evidence", "command")
TOUR_GENERATOR_FALLBACK = "fallback"
TOUR_TOP_LEVEL_AREA = "the top level"


class ResultTourError(ValueError):
    """A tour operation was asked for something it cannot honour."""


_LOGGER = logging.getLogger(__name__)

#: The minus sign the area body uses for a deletion count — U+2212, not a hyphen.
_MINUS_SIGN = "−"

#: Built from MAX_TOUR_STOPS, never restated as a bare literal.
_CEILING_REASON = f"past the {MAX_TOUR_STOPS}-stop ceiling"

_STOP_KEYS = frozenset({"title", "body", "anchor"})
_ANCHOR_KEYS = frozenset({"kind", "ref"})
_TOUR_KEYS = frozenset({"schema", "job_id", "generator", "stops", "dropped"})
_DROPPED_KEYS = frozenset({"title", "reason"})


# ---------------------------------------------------------------------------
# S2 — the anchor context, read from the job's own records
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TourAnchorContext:
    """Everything an anchor is checked against — read once, off the job's own records."""

    task_ids: tuple[str, ...] = ()
    #: (path, added, deleted), in diff order.
    diff_files: tuple[tuple[str, int, int], ...] = ()
    evidence_files: tuple[str, ...] = ()
    run_commands: tuple[str, ...] = ()


def _collect_diff_files(job_id: str) -> tuple[tuple[str, int, int], ...]:
    view = build_diff_view(resolve_job_evidence_dir(job_id))
    result: list[tuple[str, int, int]] = []
    for entry in view.get("files") or []:
        path = str(entry.get("path", ""))
        stats = entry.get("stats") or {}
        added = int(stats.get("added", 0) or 0)
        deleted = int(stats.get("deleted", 0) or 0)
        result.append((path, added, deleted))
    return tuple(result)


def _collect_evidence_files(job_id: str) -> tuple[str, ...]:
    """Sorted REGULAR FILES directly in the job's evidence directory.

    A directory (``cycles/``) is never one, and neither is a nested file. An absent
    directory or an OSError mid-listing both answer the same way: nothing to anchor to.
    """
    directory = job_evidence_dir(job_id)
    try:
        if not directory.is_dir():
            return ()
        names = sorted(child.name for child in directory.iterdir() if child.is_file())
    except OSError:
        return ()
    return tuple(names)


def _collect_run_commands(job_id: str) -> tuple[str, ...]:
    """Every recorded check's non-empty command, once, at its first occurrence."""
    recorded = load_gate_result(job_id)
    if not recorded:
        return ()
    seen: set[str] = set()
    commands: list[str] = []
    for check in recorded.get("checks") or []:
        if not isinstance(check, dict):
            continue
        command = str(check.get("command", "") or "")
        if command and command not in seen:
            seen.add(command)
            commands.append(command)
    return tuple(commands)


def collect_tour_context(job: Any) -> TourAnchorContext:
    """The anchor context for *job* — task ids, diff files, evidence files, run commands."""
    job_id = str(job.job_id)
    return TourAnchorContext(
        task_ids=tuple(str(task.task_id) for task in job.tasks),
        diff_files=_collect_diff_files(job_id),
        evidence_files=_collect_evidence_files(job_id),
        run_commands=_collect_run_commands(job_id),
    )


# ---------------------------------------------------------------------------
# S3 — the stop shape and its refusal
# ---------------------------------------------------------------------------


def tour_stop_problems(stop: Any) -> list[str]:
    """One readable line per way *stop* breaks its shape; `[]` for a sound stop."""
    if not isinstance(stop, dict):
        return [f"a tour stop must be a dict, got {type(stop).__name__}"]

    problems: list[str] = []
    keys = set(stop.keys())
    if keys != _STOP_KEYS:
        problems.append(
            f"a tour stop's keys must be exactly {sorted(_STOP_KEYS)}, got {sorted(keys)}")

    title = stop.get("title")
    if not isinstance(title, str):
        problems.append(f"a stop's title must be a string, got {type(title).__name__}")
    elif not title.strip():
        problems.append("a stop's title must not be empty")
    elif "\n" in title:
        problems.append("a stop's title must not hold a newline")
    elif len(title) > TOUR_TITLE_MAX_CHARS:
        problems.append(
            f"a stop's title must be at most {TOUR_TITLE_MAX_CHARS} characters, "
            f"got {len(title)}")

    body = stop.get("body")
    if not isinstance(body, str):
        problems.append(f"a stop's body must be a string, got {type(body).__name__}")
    elif not body.strip():
        problems.append("a stop's body must not be empty")
    elif len(body) > TOUR_BODY_MAX_CHARS:
        problems.append(
            f"a stop's body must be at most {TOUR_BODY_MAX_CHARS} characters, got {len(body)}")

    anchor = stop.get("anchor")
    if not isinstance(anchor, dict) or set(anchor.keys()) != _ANCHOR_KEYS:
        problems.append("a stop's anchor must be a dict of exactly 'kind' and 'ref'")
    else:
        kind = anchor.get("kind")
        if kind not in TOUR_ANCHOR_KINDS:
            problems.append(
                f"a stop's anchor kind must be one of {TOUR_ANCHOR_KINDS}, got {kind!r}")
        ref = anchor.get("ref")
        if not isinstance(ref, str) or not ref:
            problems.append("a stop's anchor ref must be a non-empty string")

    return problems


def tour_problems(tour: Any) -> list[str]:
    """One readable line per way *tour* breaks its shape; `[]` for a sound tour."""
    if not isinstance(tour, dict):
        return [f"a tour must be a dict, got {type(tour).__name__}"]

    problems: list[str] = []
    keys = set(tour.keys())
    if keys != _TOUR_KEYS:
        problems.append(
            f"a tour's keys must be exactly {sorted(_TOUR_KEYS)}, got {sorted(keys)}")

    schema = tour.get("schema")
    if schema != TOUR_SCHEMA:
        problems.append(f"a tour's schema must be {TOUR_SCHEMA!r}, got {schema!r}")

    job_id = tour.get("job_id")
    if not isinstance(job_id, str) or not job_id:
        problems.append("a tour's job_id must be a non-empty string")

    generator = tour.get("generator")
    if not isinstance(generator, str) or not generator:
        problems.append("a tour's generator must be a non-empty string")

    stops = tour.get("stops")
    if not isinstance(stops, list):
        problems.append(f"a tour's stops must be a list, got {type(stops).__name__}")
    else:
        if len(stops) > MAX_TOUR_STOPS:
            problems.append(
                f"a tour must hold at most {MAX_TOUR_STOPS} stops, got {len(stops)}")
        for index, stop in enumerate(stops):
            problems.extend(f"stop {index}: {line}" for line in tour_stop_problems(stop))

    dropped = tour.get("dropped")
    if not isinstance(dropped, list):
        problems.append(f"a tour's dropped must be a list, got {type(dropped).__name__}")
    else:
        for index, entry in enumerate(dropped):
            if not isinstance(entry, dict) or set(entry.keys()) != _DROPPED_KEYS:
                problems.append(
                    f"dropped {index}: must be a dict of exactly {sorted(_DROPPED_KEYS)}")
                continue
            if not isinstance(entry.get("title"), str):
                problems.append(f"dropped {index}: title must be a string")
            if not isinstance(entry.get("reason"), str):
                problems.append(f"dropped {index}: reason must be a string")

    return problems


# ---------------------------------------------------------------------------
# S4 — the anchor check
# ---------------------------------------------------------------------------


def anchor_problem(anchor: dict[str, Any], context: TourAnchorContext) -> str:
    """"" when *anchor* resolves against *context*; else one line naming the kind and ref."""
    kind = anchor["kind"]
    ref = anchor["ref"]
    if kind == "node":
        resolved = ref in context.task_ids
    elif kind == "diff":
        resolved = ref in {path for path, _added, _deleted in context.diff_files}
    elif kind == "evidence":
        resolved = ref in context.evidence_files
    elif kind == "command":
        resolved = ref in context.run_commands
    else:
        resolved = False
    if resolved:
        return ""
    return f"anchor {kind}:{ref!r} does not resolve against the job's own records"


# ---------------------------------------------------------------------------
# S5 — the resolver
# ---------------------------------------------------------------------------


def resolve_tour_stops(
    stops: list[Any], context: TourAnchorContext,
) -> tuple[list[dict], list[dict]]:
    """Walk *stops* in order, keeping at most MAX_TOUR_STOPS sound, resolving ones.

    Every drop is logged once and recorded with its title (when the stop had a string
    one) and its reason. A kept stop is a NEW dict equal to the input; the input is
    never changed.
    """
    kept: list[dict] = []
    dropped: list[dict] = []

    for stop in stops:
        problems = tour_stop_problems(stop)
        if problems:
            reason = "; ".join(problems)
        else:
            issue = anchor_problem(stop["anchor"], context)
            if issue:
                reason = issue
            elif len(kept) >= MAX_TOUR_STOPS:
                reason = _CEILING_REASON
            else:
                kept.append(dict(stop))
                continue

        title = stop.get("title") if isinstance(stop, dict) else None
        drop_title = title if isinstance(title, str) else ""
        dropped.append({"title": drop_title, "reason": reason})
        _LOGGER.warning("dropped tour stop %r: %s", drop_title, reason)

    return kept, dropped


# ---------------------------------------------------------------------------
# S6 — the mechanical tour
# ---------------------------------------------------------------------------


def _bounded_text(text: str, bound: int) -> str:
    """*text* unchanged when it fits *bound*; else its first ``bound - 1`` chars plus "…"."""
    if len(text) <= bound:
        return text
    return text[: bound - 1] + "…"


def _how_the_run_ended_stop(sources: ReportSources, context: TourAnchorContext) -> dict:
    parts = [f"State: {sources.state or NOT_RECORDED}"]
    if sources.terminal_status:
        parts.append(f"terminal status: {sources.terminal_status}")
    if sources.stop_reason:
        parts.append(f"stop reason: {sources.stop_reason}")
    if sources.mission:
        parts.append(f"mission: {sources.mission}")
    body = "; ".join(parts) + "."

    if "report.md" in context.evidence_files or not context.task_ids:
        anchor = {"kind": "evidence", "ref": "report.md"}
    else:
        anchor = {"kind": "node", "ref": context.task_ids[0]}

    return {
        "title": _bounded_text("How the run ended", TOUR_TITLE_MAX_CHARS),
        "body": _bounded_text(body, TOUR_BODY_MAX_CHARS),
        "anchor": anchor,
    }


def _diff_files_clause(files: list[tuple[str, int, int]]) -> str:
    count = len(files)
    noun = "file" if count == 1 else "files"
    total_added = sum(added for _path, added, _deleted in files)
    total_deleted = sum(deleted for _path, _added, deleted in files)
    entries = ", ".join(
        f"{path} (+{added} {_MINUS_SIGN}{deleted})" for path, added, deleted in files)
    return (f"{count} changed {noun} (+{total_added} {_MINUS_SIGN}{total_deleted}): "
            f"{entries}")


def _diff_areas(
    diff_files: tuple[tuple[str, int, int], ...],
) -> list[tuple[str, list[tuple[str, int, int]]]]:
    """Changed files grouped by area, areas kept in the order of their first file."""
    order: list[str] = []
    grouped: dict[str, list[tuple[str, int, int]]] = {}
    for path, added, deleted in diff_files:
        area = path.split("/", 1)[0] if "/" in path else TOUR_TOP_LEVEL_AREA
        if area not in grouped:
            grouped[area] = []
            order.append(area)
        grouped[area].append((path, added, deleted))
    return [(area, grouped[area]) for area in order]


def _area_stop(area: str, files: list[tuple[str, int, int]]) -> dict:
    title = ("What changed in the top level" if area == TOUR_TOP_LEVEL_AREA
             else f"What changed in {area}/")
    return {
        "title": _bounded_text(title, TOUR_TITLE_MAX_CHARS),
        "body": _bounded_text(_diff_files_clause(files), TOUR_BODY_MAX_CHARS),
        "anchor": {"kind": "diff", "ref": files[0][0]},
    }


def _gathering_stop(remaining: list[tuple[str, list[tuple[str, int, int]]]]) -> dict:
    gathered_files = [entry for _area, files in remaining for entry in files]
    body = f"{len(remaining)} more areas; " + _diff_files_clause(gathered_files)
    return {
        "title": _bounded_text("What else changed", TOUR_TITLE_MAX_CHARS),
        "body": _bounded_text(body, TOUR_BODY_MAX_CHARS),
        "anchor": {"kind": "diff", "ref": gathered_files[0][0]},
    }


def _changed_area_stops(context: TourAnchorContext, room: int) -> list[dict]:
    areas = _diff_areas(context.diff_files)
    if not areas or room <= 0:
        return []
    if len(areas) <= room:
        return [_area_stop(area, files) for area, files in areas]
    stops = [_area_stop(area, files) for area, files in areas[: room - 1]]
    stops.append(_gathering_stop(areas[room - 1:]))
    return stops


def _how_to_run_it_stop(context: TourAnchorContext) -> dict | None:
    if not context.run_commands:
        return None
    command = context.run_commands[0]
    return {
        "title": _bounded_text("How to run it", TOUR_TITLE_MAX_CHARS),
        "body": _bounded_text(
            f"The Definition of Done ran: {command}", TOUR_BODY_MAX_CHARS),
        "anchor": {"kind": "command", "ref": command},
    }


def _definition_of_done_stop(sources: ReportSources) -> dict | None:
    if sources.dod_released is None:
        return None
    total = len(sources.dod_checks)
    passed = sum(1 for check in sources.dod_checks if check.status == STATUS_PASSED)
    verb = "released" if sources.dod_released else "held"
    body = f"{passed} of {total} checks passed; the gate {verb} the job."
    not_passed = [check.check_id for check in sources.dod_checks
                  if check.status != STATUS_PASSED]
    if not_passed:
        body += f" Not passed: {', '.join(not_passed)}."
    return {
        "title": _bounded_text("Definition of Done", TOUR_TITLE_MAX_CHARS),
        "body": _bounded_text(body, TOUR_BODY_MAX_CHARS),
        "anchor": {"kind": "evidence", "ref": DOD_RESULT_FILENAME},
    }


def fallback_tour_stops(sources: ReportSources, context: TourAnchorContext) -> list[dict]:
    """The mechanical tour's stops, in order: how it ended, what changed, how to run
    it, and the Definition of Done — pure and deterministic over *sources* and *context*.
    """
    how_to_run_it = _how_to_run_it_stop(context)
    dod_stop = _definition_of_done_stop(sources)
    room = MAX_TOUR_STOPS - 1 - (1 if how_to_run_it else 0) - (1 if dod_stop else 0)

    stops = [_how_the_run_ended_stop(sources, context)]
    stops.extend(_changed_area_stops(context, room))
    if how_to_run_it is not None:
        stops.append(how_to_run_it)
    if dod_stop is not None:
        stops.append(dod_stop)
    return stops


# ---------------------------------------------------------------------------
# S7 — the build
# ---------------------------------------------------------------------------


def _assemble_fallback_tour(
    job: Any,
    sources: ReportSources,
    context: TourAnchorContext,
    generator: str = TOUR_GENERATOR_FALLBACK,
) -> dict:
    """The mechanical tour's dict, with *generator* free to be overridden.

    `build_fallback_tour` is this with `generator` left at its default — kept
    as ONE implementation so a generation fallback (F036 T002) and the plain
    mechanical tour (F036 T001) can never quietly diverge.
    """
    stops = fallback_tour_stops(sources, context)
    kept, dropped = resolve_tour_stops(stops, context)
    return {
        "schema": TOUR_SCHEMA,
        "job_id": str(job.job_id),
        "generator": generator,
        "stops": kept,
        "dropped": list(dropped),
    }


def build_fallback_tour(job: Any) -> dict:
    """The mechanical tour for *job*: every stop sound, every anchor resolved.

    `tour_problems` of this function's answer is always `[]`.
    """
    context = collect_tour_context(job)
    sources = build_report_sources(job)
    return _assemble_fallback_tour(job, sources, context)


# ---------------------------------------------------------------------------
# F036 T002 (first half) — the model-written tour through the summary role
# ---------------------------------------------------------------------------

#: Compact schema version, per the SCHEMA_V convention run_structured_call
#: requires (packages/orchestration/schemas/models.py:schema_v_of).
GENERATED_TOUR_SCHEMA_V = "generated_tour_v1"

#: The generator label a fully sound model-written tour carries.
TOUR_GENERATOR_SUMMARY_ROLE = "summary-role"

#: The fallback reason when every model stop was dropped, leaving fewer than
#: two stops to publish.
TOUR_NO_SOUND_STOPS = "no_sound_stops"

#: Marketing words a records-only tour must never carry. Lower-case; matched
#: as a WHOLE word (hyphens included) against the lower-cased stop text, so a
#: hyphenated entry like "world-class" cannot hide inside a longer word.
TOUR_CLAIM_DENYLIST: tuple[str, ...] = (
    "seamless", "seamlessly", "robust", "flawless", "perfect", "perfectly",
    "guaranteed", "bulletproof", "effortless", "blazing", "world-class",
    "best-in-class", "state-of-the-art", "cutting-edge", "production-ready",
    "enterprise-grade",
)


class GeneratedTourAnchor(BaseModel):
    """One model-proposed anchor — judged by :func:`anchor_problem`, not here."""

    kind: str
    ref: str


class GeneratedTourStop(BaseModel):
    """One model-proposed stop — judged by :func:`tour_stop_problems` and
    :func:`tour_claim_problems`, not here: this schema fixes the shape only."""

    title: str
    body: str
    anchor: GeneratedTourAnchor


class GeneratedTourContent(BaseModel):
    """The schema the ``summary`` role is asked to fill for a generated tour.

    No length or value constraint of its own: :func:`resolve_tour_stops` and
    :func:`tour_claim_problems` are what actually judge a proposed stop, so
    this class only fixes the shape a response must parse into.
    """

    SCHEMA_V: ClassVar[str] = GENERATED_TOUR_SCHEMA_V

    stops: list[GeneratedTourStop]


# ---------------------------------------------------------------------------
# S2 — the source text: one fact per line, off the job's own records
# ---------------------------------------------------------------------------


def tour_source_text(job: Any, sources: ReportSources, context: TourAnchorContext) -> str:
    """The job's own records, one fact per line — the ONLY text the model sees.

    :func:`tour_claim_problems` checks a proposed stop against exactly this
    text, so a fact this function omits is a fact the model cannot cite
    either.
    """
    lines = [f"state: {sources.state or NOT_RECORDED}"]
    if sources.terminal_status:
        lines.append(f"terminal status: {sources.terminal_status}")
    if sources.stop_reason:
        lines.append(f"stop reason: {sources.stop_reason}")
    if sources.mission:
        lines.append(f"mission: {sources.mission}")

    for task in job.tasks:
        line = f"task {task.task_id}: {task.title}; status {task.status}"
        if task.acceptance:
            line += f"; acceptance: {task.acceptance}"
        lines.append(line)

    for path, added, deleted in context.diff_files:
        lines.append(f"changed file {path} (+{added} {_MINUS_SIGN}{deleted})")

    for name in context.evidence_files:
        lines.append(f"evidence file {name}")

    for command in context.run_commands:
        lines.append(f"command {command}")

    if sources.dod_released is not None:
        dod_stop = _definition_of_done_stop(sources)
        assert dod_stop is not None
        lines.append(f"Definition of Done: {dod_stop['body']}")
        for check in sources.dod_checks:
            lines.append(f"check {check.check_id} ({check.kind}): {check.status}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# S3 — no new claims: a proposed stop may only restate the source text
# ---------------------------------------------------------------------------

#: A run of digits between word boundaries.
_TOUR_NUMBER_RE = re.compile(r"\b\d+\b")
#: A span between two backticks.
_TOUR_BACKTICK_SPAN_RE = re.compile(r"`([^`]+)`")
#: A slashed path whose segments may hold dots and hyphens, ending at a word character so a
#: sentence's closing full stop is never read as part of it (R-1087), or a word/dot/short
#: letter extension — the two path shapes S3 names.
_TOUR_PATH_TOKEN_RE = re.compile(r"(?:[\w.-]+/)+[\w.-]*\w|\w+\.[A-Za-z]{1,5}\b")


def tour_claim_problems(stop: dict[str, Any], source_text: str) -> list[str]:
    """One readable line per claim *stop* makes that *source_text* does not hold.

    Four kinds of breach, each its own reason: a number the source text does
    not carry as a number, a backtick span it does not contain, a path it
    does not contain (read off the stop's text with backtick spans removed,
    so a path already reported as a backtick breach is not reported twice),
    and a :data:`TOUR_CLAIM_DENYLIST` word matched whole, case-insensitively.
    `[]` for a stop that only restates the records.
    """
    text = f"{stop.get('title', '')} {stop.get('body', '')}"
    problems: list[str] = []

    source_numbers = set(_TOUR_NUMBER_RE.findall(source_text))
    seen_numbers: set[str] = set()
    for number in _TOUR_NUMBER_RE.findall(text):
        if number in source_numbers or number in seen_numbers:
            continue
        seen_numbers.add(number)
        problems.append(f"the number {number!r} is not in the records")

    seen_spans: set[str] = set()
    for span in _TOUR_BACKTICK_SPAN_RE.findall(text):
        if span in source_text or span in seen_spans:
            continue
        seen_spans.add(span)
        problems.append(f"the backtick span `{span}` is not in the records")

    stripped_text = _TOUR_BACKTICK_SPAN_RE.sub(" ", text)
    seen_paths: set[str] = set()
    for path in _TOUR_PATH_TOKEN_RE.findall(stripped_text):
        if path in source_text or path in seen_paths:
            continue
        seen_paths.add(path)
        problems.append(f"the path {path!r} is not in the records")

    lowered = text.lower()
    for word in TOUR_CLAIM_DENYLIST:
        pattern = r"(?<![\w-])" + re.escape(word) + r"(?![\w-])"
        if re.search(pattern, lowered):
            problems.append(f"the claim word {word!r} is not allowed")

    return problems


# ---------------------------------------------------------------------------
# S4 — the prompt: the source text, the allowed anchors, then the rules
# ---------------------------------------------------------------------------


def build_tour_prompt(source_text: str, context: TourAnchorContext) -> str:
    """The prompt handed to the ``summary`` role: records, anchors, rules."""
    anchor_lines = [f"node {task_id}" for task_id in context.task_ids]
    anchor_lines += [f"diff {path}" for path, _added, _deleted in context.diff_files]
    anchor_lines += [f"evidence {name}" for name in context.evidence_files]
    anchor_lines += [f"command {command}" for command in context.run_commands]

    rules = "\n".join([
        "Rules:",
        f"- at most {MAX_TOUR_STOPS - 1} stops",
        f"- a title of at most {TOUR_TITLE_MAX_CHARS} characters on one line",
        f"- a body of at most {TOUR_BODY_MAX_CHARS} characters",
        "- every anchor copied from the list above",
        "- every sentence restates the records above and adds no claim",
    ])

    return "\n".join([
        source_text,
        "",
        "Allowed anchors:",
        *anchor_lines,
        "",
        rules,
    ])


# ---------------------------------------------------------------------------
# S5 — generation: the summary role, no new claims, the mechanical fallback
# ---------------------------------------------------------------------------


def _provider_call_error_types() -> tuple[type[BaseException], ...]:
    """Built once at import — see :data:`PROVIDER_CALL_ERRORS`."""
    types: list[type[BaseException]] = [OSError, RuntimeError, ValueError, ImportError]
    try:
        import ollama
        types += [ollama.RequestError, ollama.ResponseError]
    except ImportError:
        pass
    try:
        import httpx
        types.append(httpx.HTTPError)
    except ImportError:
        pass
    return tuple(types)


#: Built once at import. Every exception a `call_fn` may raise that this
#: module treats as a provider failure rather than a programming error.
PROVIDER_CALL_ERRORS: tuple[type[BaseException], ...] = _provider_call_error_types()


def generate_result_tour(
    job: Any,
    call_fn: Callable[[str, int], str] | None = None,
    *,
    on_call: Callable[[int, str, bool, str], None] | None = None,
) -> dict:
    """Generate a guided tour through the ``summary`` role, or fall back.

    NEVER raises: an exception of :data:`PROVIDER_CALL_ERRORS`, an outcome
    that is not ok, and a model answer with fewer than two sound stops all
    become the mechanical tour, labelled with why. `tour_problems` of this
    function's answer is always `[]`.

    The kept stops are always the mechanical tour's FIRST stop followed by
    every sound model stop resolve_tour_stops still admits — so a generated
    tour never opens with something the model invented.
    """
    context = collect_tour_context(job)
    sources = build_report_sources(job)

    if call_fn is None:
        return _assemble_fallback_tour(job, sources, context)

    source_text = tour_source_text(job, sources, context)
    prompt = build_tour_prompt(source_text, context)

    try:
        outcome = run_structured_call(
            GeneratedTourContent, prompt, call_fn, on_call=on_call, allow_parse_retry=True,
        )
    except PROVIDER_CALL_ERRORS as exc:
        classification = classify(FailureSignals(exception=exc))
        return _assemble_fallback_tour(
            job, sources, context,
            f"{TOUR_GENERATOR_FALLBACK}:{classification.failure_class.value}")

    if not outcome.ok:
        classification = classify(
            FailureSignals(error_class=outcome.error_class, error_text=outcome.hint))
        return _assemble_fallback_tour(
            job, sources, context,
            f"{TOUR_GENERATOR_FALLBACK}:{classification.failure_class.value}")

    assert isinstance(outcome.value, GeneratedTourContent)

    claim_dropped: list[dict] = []
    sound_stops: list[dict] = []
    for model_stop in outcome.value.stops:
        stop_dict = model_stop.model_dump()
        problems = tour_claim_problems(stop_dict, source_text)
        if problems:
            claim_dropped.append({"title": stop_dict["title"], "reason": "; ".join(problems)})
        else:
            sound_stops.append(stop_dict)

    mechanical_first = fallback_tour_stops(sources, context)[0]
    kept, resolver_dropped = resolve_tour_stops([mechanical_first, *sound_stops], context)

    if len(kept) < 2:
        fallback = _assemble_fallback_tour(
            job, sources, context, f"{TOUR_GENERATOR_FALLBACK}:{TOUR_NO_SOUND_STOPS}")
        fallback["dropped"] = [*claim_dropped, *resolver_dropped, *fallback["dropped"]]
        return fallback

    return {
        "schema": TOUR_SCHEMA,
        "job_id": str(job.job_id),
        "generator": TOUR_GENERATOR_SUMMARY_ROLE,
        "stops": kept,
        "dropped": [*claim_dropped, *resolver_dropped],
    }


# ---------------------------------------------------------------------------
# S6 — the call function: the `summary` role, inventoried in model_routing.py
# ---------------------------------------------------------------------------


def tour_call_fn() -> Callable[[str, int], str] | None:
    """Build a call_fn for the `summary` role, or None.

    Mirrors `artifact_summary.summary_call_fn`: `resolve_role_config("summary")`
    supplies the model, `make_structured_call_fn` does the rest. Honest `None`
    under the same conditions that factory already returns `None` for — never
    raises. This call site is one of the ten entries of
    `model_routing.ROLE_CONFIG_CALL_SITES`.
    """
    role_cfg = resolve_role_config("summary")
    return make_structured_call_fn(GeneratedTourContent, model=role_cfg.model)


# ---------------------------------------------------------------------------
# F036 T002 (second half) — storage: versions, the writer, the renderer
# (DECISION F036 D4)
# ---------------------------------------------------------------------------

#: The key `write_result_tour` records a write failure under — mirrors
#: `run_report.REPORT_ERROR_METADATA_KEY`.
TOUR_ERROR_METADATA_KEY = "tour_error"

#: A stored tour's version suffix: `tour_v<N>.json`, N a decimal of 2 or more.
_TOUR_VERSION_RE = re.compile(r"tour_v(\d+)\.json")

#: `write_result_tour`'s own sentinel: distinguishes "no call_fn argument was
#: given" (ask `tour_call_fn()`) from "call_fn=None was given" (build the
#: mechanical tour). A bare `None` default cannot tell those apart.
_UNSET_CALL_FN = object()


def tour_path(job_id: str, version: int) -> Path:
    """Where version *version* of *job_id*'s tour lives (DECISION F036 D4 (1)).

    Version 1 is ``tour.json``, beside ``report.md``; version 2 and above is
    ``tour_v<N>.json`` — the same versioned-render shape
    ``job_plan.write_plan_md`` uses for ``plan.md`` / ``plan_v<N>.md``.
    """
    directory = job_evidence_dir(job_id)
    if version == 1:
        return directory / TOUR_FILENAME
    return directory / f"tour_v{version}.json"


def stored_tour_versions(job_id: str) -> list[int]:
    """Every version *job_id* has stored, sorted ascending; ``[]`` for none.

    Only a REGULAR FILE directly in the job's evidence directory counts, named
    exactly ``tour.json`` (version 1) or ``tour_v<N>.json`` with N a decimal
    of 2 or more — a directory of either name, or a file matching neither
    shape, names no version. An absent directory or an ``OSError`` mid
    listing both answer ``[]``, the way ``_collect_evidence_files`` does.
    """
    directory = job_evidence_dir(job_id)
    versions: list[int] = []
    try:
        if not directory.is_dir():
            return []
        for child in directory.iterdir():
            if not child.is_file():
                continue
            if child.name == TOUR_FILENAME:
                versions.append(1)
                continue
            match = _TOUR_VERSION_RE.fullmatch(child.name)
            if match is None:
                continue
            number = int(match.group(1))
            if number >= 2:
                versions.append(number)
    except OSError:
        return []
    return sorted(versions)


def load_result_tour(job_id: str) -> tuple[int, dict] | None:
    """The latest stored tour for *job_id*: ``(version, tour)``, or ``None``.

    Raises :class:`ResultTourError`, naming the version, when the highest
    stored file does not read or parse, or when :func:`tour_problems` of its
    contents is not ``[]`` — an unsound or unreadable stored tour is never
    silently treated as absent.
    """
    versions = stored_tour_versions(job_id)
    if not versions:
        return None
    version = versions[-1]
    path = tour_path(job_id, version)
    try:
        tour = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ResultTourError(
            f"tour version {version} of job {job_id} does not read: "
            f"{type(exc).__name__}: {exc}") from exc
    problems = tour_problems(tour)
    if problems:
        raise ResultTourError(
            f"tour version {version} of job {job_id} is not sound: {'; '.join(problems)}")
    return version, tour


def write_result_tour(
    job: Any, *, call_fn: Callable[[str, int], str] | None = _UNSET_CALL_FN,
) -> Path | None:
    """Write the next version of *job*'s tour beside its report (DECISION F036 D4 (2), (3)).

    ``call_fn`` unset asks :func:`tour_call_fn` for the ``summary`` role's call
    function; ``call_fn=None`` given explicitly builds the mechanical tour
    instead — the same distinction :func:`generate_result_tour` makes. Never
    raises for an ``OSError``, a ``ValueError`` or a :class:`ResultTourError`:
    such a failure is recorded on the job under ``TOUR_ERROR_METADATA_KEY`` and
    the answer is ``None``, the way ``run_report.write_final_report`` treats a
    report failure — a tour is an account of the run, and losing the account
    must not lose the run. On success that key is removed and the answer is
    the path written.
    """
    try:
        resolved_call_fn = tour_call_fn() if call_fn is _UNSET_CALL_FN else call_fn
        tour = generate_result_tour(job, resolved_call_fn)
        job_id = str(job.job_id)
        directory = job_evidence_dir(job_id)
        directory.mkdir(parents=True, exist_ok=True)
        versions = stored_tour_versions(job_id)
        next_version = (versions[-1] if versions else 0) + 1
        path = tour_path(job_id, next_version)
        durable_write_json(path, tour)
    except (OSError, ValueError, ResultTourError) as exc:
        metadata = getattr(job, "metadata", None)
        if isinstance(metadata, dict):
            metadata[TOUR_ERROR_METADATA_KEY] = f"{type(exc).__name__}: {exc}"
        return None
    metadata = getattr(job, "metadata", None)
    if isinstance(metadata, dict):
        metadata.pop(TOUR_ERROR_METADATA_KEY, None)
    return path


# ---------------------------------------------------------------------------
# F036 T003 (first half) — one view for the browser and the command line
# (DECISION F036 D5)
# ---------------------------------------------------------------------------

#: The view's own key set — the `tour` route and `_tour_section` both build from this.
TOUR_VIEW_KEYS = ("stored", "version", "tour", "error")


def tour_view(job: Any) -> dict:
    """The one view served at `GET /api/jobs/<job_id>/tour` and shown on the command line's
    `tour` section (DECISION F036 D5): `{"stored", "version", "tour", "error"}`.

    The latest stored tour, `stored` true, its own version, `error` ""; with nothing stored,
    `build_fallback_tour(job)`, `stored` false, `version` 0, `error` ""; and when the stored
    tour does not read, `build_fallback_tour(job)`, `stored` false, `version` 0, `error` the
    :class:`ResultTourError`'s message — there is always a tour to show. Writes nothing.
    """
    job_id = str(job.job_id)
    try:
        loaded = load_result_tour(job_id)
    except ResultTourError as exc:
        return {"stored": False, "version": 0, "tour": build_fallback_tour(job), "error": str(exc)}
    if loaded is None:
        return {"stored": False, "version": 0, "tour": build_fallback_tour(job), "error": ""}
    version, tour = loaded
    return {"stored": True, "version": version, "tour": tour, "error": ""}


def render_tour_lines(tour: dict[str, Any]) -> list[str]:
    """The tour rendered for the command line (DECISION F036 D4 (5)) — one
    renderer for both `job show --tour` and T003's browser overlay stops.
    """
    stops = tour["stops"]
    noun = "stop" if len(stops) == 1 else "stops"
    lines = [f"Guided tour of job {tour['job_id']} ({tour['generator']}, {len(stops)} {noun})"]
    for index, stop in enumerate(stops, start=1):
        lines.append(f"  {index}. {stop['title']}")
        lines.extend(f"     {line}" for line in stop["body"].splitlines())
        anchor = stop["anchor"]
        lines.append(f"     -> {anchor['kind']}: {anchor['ref']}")
    return lines
