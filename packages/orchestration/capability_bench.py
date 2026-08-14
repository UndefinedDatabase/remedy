"""F082 T001 — the capability bench's per-order record, as a pure function.

The bench measures nothing the gauntlet does not already measure. One run of
one order leaves a ``run.json`` body behind
(:mod:`packages.orchestration.gauntlet_runner`) and the evaluator judges it
(:mod:`packages.orchestration.gauntlet_evaluator`); this module turns that pair
into ONE row of the bench's history, and does nothing else.

Pure on purpose: no disk read, no network, no clock. Everything a row needs
arrives as an argument, so a row can be built from a recorded fixture body and
the history a later round appends is a function of the evidence rather than of
when it happened to run.

**Unmeasured is ``None``, never zero.** R-0178 stated it and R-0407 showed what
the alternative costs — a false zero read as a measured cost, for every
gauntlet run. A field this module cannot source from the evidence in front of
it stays ``None``.

Remedy deliberately does NOT re-decide what passing means here. That definition
is :data:`packages.orchestration.gauntlet_evaluator.PASS_CRITERIA`, on F082's
do-not-touch list; the bench reads the verdict it is handed.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

#: What `gauntlet_matrix.postmortem_classes` substitutes for a postmortem that
#: recorded no class. Named once, so the bench cannot invent a second label for
#: the same absence.
POSTMORTEM_CLASS_ABSENT = "(absent)"


@dataclass(frozen=True)
class BenchRecord:
    """One order's result in one bench run — the row F082 T001 names.

    The feature file spells the pass field ``pass``; ``pass`` is a Python
    keyword, so the field here is ``passed``. The schema did not drift, the
    language did.
    """

    order_id: str
    #: Which bench line this row belongs to. The CALLER supplies it: R2 Q2
    #: found no source anywhere in the harness, because no single run can know
    #: which series it is part of.
    series: str
    #: Whether the evaluator called the run flawless. ``None`` means nobody
    #: judged it, which is not the same as failing.
    passed: bool | None
    #: Token actuals straight off the evidence body's ``tokens`` key, or
    #: ``None`` when the run measured none. Money is deliberately NOT here: R2
    #: Q5 found ``total_cost_usd`` never reaches ``run.json``, so a currency
    #: figure would be an invention rather than a measurement.
    cost: dict[str, int] | None
    #: The gauntlet's own ``wall_seconds``, renamed to the field the feature
    #: file names. Not a new measurement (R2 Q8).
    wall_s: float | None
    #: Always ``None`` today, and that is a measurement rather than an
    #: oversight. R2 Q7 traced ``repair_rounds_used`` to
    #: ``long_run_executor.CycleRecord`` and showed it is DROPPED at the
    #: ``orchestrator_loop.JobExecution`` boundary, so no gauntlet ``run.json``
    #: carries it. A later round may derive it from the ``cycle_repair_round``
    #: run-log events; until one does, the honest value is the absent one.
    repair_rounds: int | None
    postmortem_classes: tuple[str, ...]

    def to_json(self) -> dict[str, Any]:
        """The row as plain JSON-ready data, keys sorted, for the history file."""
        body: dict[str, Any] = {
            "order_id": self.order_id,
            "series": self.series,
            "passed": self.passed,
            "cost": dict(self.cost) if self.cost is not None else None,
            "wall_s": self.wall_s,
            "repair_rounds": self.repair_rounds,
            "postmortem_classes": list(self.postmortem_classes),
        }
        return {key: body[key] for key in sorted(body)}


def _postmortem_classes_of(evidence_body: dict[str, Any]) -> tuple[str, ...]:
    """Failure classes the run recorded, deduplicated, in first-seen order.

    The same rule as ``gauntlet_matrix.postmortem_classes``, applied to the
    SAME records read straight off the evidence body instead of through a
    ``RunVerdict``, so a row can be built from a recorded fixture with no
    evaluator in hand. First-seen rather than sorted: the order the run met its
    failures is itself information, and it is as deterministic as the file.
    """
    seen: list[str] = []
    for record in evidence_body.get("postmortems") or ():
        if not isinstance(record, dict):
            continue
        name = str(record.get("failure_class", "") or POSTMORTEM_CLASS_ABSENT)
        if name not in seen:
            seen.append(name)
    return tuple(seen)


def _passed_of(verdict: Any) -> bool | None:
    """Read ``flawless`` off the evaluator's verdict, accepting object or dict.

    Both shapes exist already: ``gauntlet_evaluator.evaluate_run`` returns the
    dataclass, and its ``to_json`` is what a recorded fixture carries.
    """
    if verdict is None:
        return None
    flawless = (verdict.get("flawless") if isinstance(verdict, dict)
                else getattr(verdict, "flawless", None))
    return None if flawless is None else bool(flawless)


def build_bench_record(*, evidence_body: dict[str, Any], series: str,
                       verdict: Any) -> BenchRecord:
    """One bench row from one run's evidence body plus the evaluator's verdict.

    Reads only what R2's inventory proved a gauntlet run already writes:
    ``order_id``, ``wall_seconds`` and ``tokens`` off the ``run.json`` body,
    and the ``failure_class`` of each postmortem it recorded. Everything else
    the feature file names is either supplied by the caller (``series``) or has
    no source in the harness and is therefore ``None`` (``repair_rounds``).
    """
    tokens = evidence_body.get("tokens")
    wall = evidence_body.get("wall_seconds")
    return BenchRecord(
        order_id=str(evidence_body.get("order_id", "")),
        series=series,
        passed=_passed_of(verdict),
        # No ``tokens`` key means the run measured nothing and said so with
        # ``tokens_source: unmeasured``. That is ``None``, never
        # ``{"in": 0, "out": 0}`` (R-0178, and R-0407 for what zero costs).
        cost={str(k): int(v) for k, v in tokens.items()} if isinstance(tokens, dict) else None,
        wall_s=float(wall) if isinstance(wall, (int, float)) and not isinstance(wall, bool) else None,
        repair_rounds=None,
        postmortem_classes=_postmortem_classes_of(evidence_body),
    )
