"""F036 T001 — the stop shape, the anchor check and the mechanical tour (DECISION F036 D1).

Remedy deliberately does not write a stop whose anchor does not resolve against the job's own
records — an unanchored claim in a guided tour is worse than a shorter one (D1 (3)).

This module builds the guided result tour a job's terminal state can offer a human: at most
eight stops, each a title, a body and an anchor into something the job actually produced. Apart
from `collect_tour_context`, which reads the job's own records, this module is pure — it writes
no file, calls no model and reads no clock. Nothing calls it yet; F036 T002 wires it at the job
terminal and removes this module's `ALLOWED_UNWIRED` entry.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from packages.orchestration.data_paths import job_evidence_dir
from packages.orchestration.diff_view_source import build_diff_view
from packages.orchestration.dod_gate import DOD_RESULT_FILENAME, load_gate_result
from packages.orchestration.dod_runners import STATUS_PASSED
from packages.orchestration.evidence_index import resolve_job_evidence_dir
from packages.orchestration.run_report import NOT_RECORDED, ReportSources, build_report_sources

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


def build_fallback_tour(job: Any) -> dict:
    """The mechanical tour for *job*: every stop sound, every anchor resolved.

    `tour_problems` of this function's answer is always `[]`.
    """
    context = collect_tour_context(job)
    stops = fallback_tour_stops(build_report_sources(job), context)
    kept, dropped = resolve_tour_stops(stops, context)
    return {
        "schema": TOUR_SCHEMA,
        "job_id": str(job.job_id),
        "generator": TOUR_GENERATOR_FALLBACK,
        "stops": kept,
        "dropped": dropped,
    }
