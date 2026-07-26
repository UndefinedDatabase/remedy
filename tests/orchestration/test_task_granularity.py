"""F016 — table-driven tests for Flight-Plan task-granularity normalization."""
from __future__ import annotations

from dataclasses import dataclass, field

import pytest

from packages.orchestration.schemas.models import FlightPlan, PlannedTask
from packages.orchestration.task_granularity import (
    GranularityConfig,
    normalize_plan,
)

# ---------------------------------------------------------------------------
# Fixture helpers
# ---------------------------------------------------------------------------

def _task(
    task_id: str,
    *,
    acceptance: list[str],
    band: str = "M",
    files: list[str] | None = None,
    deps: list[str] | None = None,
    title: str | None = None,
) -> PlannedTask:
    return PlannedTask(
        id=task_id,
        title=title or f"task {task_id}",
        goal=f"goal {task_id}",
        acceptance=list(acceptance),
        depends_on=list(deps or []),
        est_tokens_band=band,
        files_hint=list(files or []),
    )


def _plan(tasks: list[PlannedTask]) -> FlightPlan:
    return FlightPlan(schema_v="flight_plan_v1", tasks=list(tasks))


@dataclass(frozen=True)
class Case:
    """One normalization case: input tasks -> expected tasks + record kinds."""

    name: str
    tasks: list[PlannedTask]
    expected_ids: list[str]
    expected_bands: list[str]
    expected_deps: list[list[str]]
    expected_kinds: list[str]
    expected_acceptance: list[list[str]] | None = None
    cfg: GranularityConfig = field(default_factory=GranularityConfig)


# ---------------------------------------------------------------------------
# Split table (T001)
# ---------------------------------------------------------------------------

SPLIT_CASES: list[Case] = [
    Case(
        name="xl_three_acceptance_splits_into_chained_children",
        tasks=[
            _task("t0", acceptance=["seed"], band="S"),
            _task(
                "T1",
                acceptance=["implement parser", "parser tests", "docs"],
                band="XL",
                files=["src/p.py", "tests/t.py", "docs/d.md"],
                deps=["t0"],
            ),
        ],
        expected_ids=["t0", "T1a", "T1b", "T1c"],
        expected_bands=["S", "M", "M", "M"],
        expected_deps=[[], ["t0"], ["T1a"], ["T1b"]],
        expected_kinds=["split"],
        expected_acceptance=[
            ["seed"], ["implement parser"], ["parser tests"], ["docs"],
        ],
    ),
    Case(
        name="xl_single_acceptance_is_flagged_unsplittable",
        tasks=[
            _task("T1", acceptance=["ship it"], band="XL", files=["src/p.py"]),
        ],
        expected_ids=["T1"],
        expected_bands=["XL"],
        expected_deps=[[]],
        expected_kinds=["unsplittable_flag"],
        expected_acceptance=[["ship it"]],
    ),
    Case(
        name="l_band_at_acceptance_threshold_is_untouched",
        tasks=[
            _task("T1", acceptance=["a", "b", "c"], band="L",
                  files=["src/p.py"]),
        ],
        expected_ids=["T1"],
        expected_bands=["L"],
        expected_deps=[[]],
        expected_kinds=[],
        expected_acceptance=[["a", "b", "c"]],
    ),
    Case(
        name="m_band_above_acceptance_count_splits",
        tasks=[
            _task("T1", acceptance=["one", "two", "three", "four"], band="M"),
        ],
        expected_ids=["T1a", "T1b", "T1c", "T1d"],
        expected_bands=["M", "M", "M", "M"],
        expected_deps=[[], ["T1a"], ["T1b"], ["T1c"]],
        expected_kinds=["split"],
        expected_acceptance=[["one"], ["two"], ["three"], ["four"]],
    ),
]


@pytest.mark.parametrize("case", SPLIT_CASES, ids=lambda c: c.name)
def test_split_table(case: Case) -> None:
    result = normalize_plan(_plan(case.tasks), case.cfg)
    tasks = result.plan.tasks

    assert [t.id for t in tasks] == case.expected_ids
    assert [t.est_tokens_band for t in tasks] == case.expected_bands
    assert [list(t.depends_on) for t in tasks] == case.expected_deps
    assert [t.kind for t in result.transformations] == case.expected_kinds
    if case.expected_acceptance is not None:
        assert [list(t.acceptance) for t in tasks] == case.expected_acceptance


def test_untouched_plan_is_the_same_object() -> None:
    """No rule fired -> the original plan object comes back, empty record."""
    plan = _plan([_task("T1", acceptance=["a", "b", "c"], band="L")])
    result = normalize_plan(plan, GranularityConfig())

    assert result.plan is plan
    assert result.transformations == []


def test_split_record_names_source_children_and_heuristic_band() -> None:
    plan = _plan([
        _task("T1", acceptance=["one", "two", "three", "four"], band="XL"),
    ])
    result = normalize_plan(plan, GranularityConfig())

    (record,) = result.transformations
    assert record.kind == "split"
    assert record.source_ids == ["T1"]
    assert record.result_ids == ["T1a", "T1b", "T1c", "T1d"]
    assert "heuristically" in record.reason
    assert "band XL at/above split band XL" in record.reason
    assert "acceptance count 4 > 3" in record.reason


def test_unsplittable_record_is_recorded_not_silent() -> None:
    plan = _plan([_task("T1", acceptance=["ship it"], band="XL")])
    result = normalize_plan(plan, GranularityConfig())

    (record,) = result.transformations
    assert record.kind == "unsplittable_flag"
    assert record.source_ids == ["T1"]
    assert record.result_ids == ["T1"]
    assert "single acceptance criterion" in record.reason


def test_dependents_of_a_split_task_point_at_the_chain_end() -> None:
    plan = _plan([
        _task("T1", acceptance=["one", "two", "three", "four"], band="XL"),
        _task("T2", acceptance=["after"], band="S", deps=["T1"]),
    ])
    result = normalize_plan(plan, GranularityConfig())

    by_id = {t.id: t for t in result.plan.tasks}
    assert list(by_id["T2"].depends_on) == ["T1d"]


def test_acceptance_items_sharing_files_cluster_together() -> None:
    plan = _plan([
        _task(
            "T1",
            acceptance=["parser code", "parser docs", "runner wiring"],
            band="XL",
            files=["src/parser/core.py", "src/runner/loop.py"],
        ),
    ])
    result = normalize_plan(plan, GranularityConfig())

    tasks = result.plan.tasks
    assert [list(t.acceptance) for t in tasks] == [
        ["parser code", "parser docs"],
        ["runner wiring"],
    ]
    assert [list(t.files_hint) for t in tasks] == [
        ["src/parser/core.py"],
        ["src/runner/loop.py"],
    ]


def test_split_band_config_lowers_the_trigger() -> None:
    plan = _plan([_task("T1", acceptance=["a", "b"], band="L")])
    result = normalize_plan(plan, GranularityConfig(split_band="L"))

    assert [t.id for t in result.plan.tasks] == ["T1a", "T1b"]
    assert [t.kind for t in result.transformations] == ["split"]


def test_invalid_split_band_is_rejected_loudly() -> None:
    with pytest.raises(ValueError, match="split_band"):
        GranularityConfig(split_band="huge")
