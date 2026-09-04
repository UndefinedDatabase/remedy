"""F016 — table-driven tests for Flight-Plan task-granularity normalization."""
from __future__ import annotations

from dataclasses import dataclass, field

import pytest

from packages.orchestration.schemas.models import FlightPlan, PlannedTask
from packages.orchestration.task_granularity import (
    GranularityConfig,
    normalize_plan,
    split_one_task,
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


def test_split_one_task_splits_by_acceptance_clusters() -> None:
    task = _task("T1", acceptance=["one", "two", "three", "four"], band="XL")

    children = split_one_task(task)

    assert children is not None
    assert [c.id for c in children] == ["T1a", "T1b", "T1c", "T1d"]
    assert [c.acceptance for c in children] == [["one"], ["two"], ["three"], ["four"]]


def test_split_one_task_returns_none_when_unsplittable() -> None:
    task = _task("T1", acceptance=["ship it"], band="XL")

    assert split_one_task(task) is None


def test_split_one_task_avoids_collisions_against_a_supplied_used_ids_set() -> None:
    task = _task("T1", acceptance=["one", "two"], band="XL")
    used = {"T1", "T1a"}

    children = split_one_task(task, used_ids=used)

    assert children is not None
    assert [c.id for c in children] == ["T1ax", "T1b"]
    assert used == {"T1", "T1a", "T1ax", "T1b"}


def test_split_one_task_matches_apply_splits_output_for_the_same_task() -> None:
    """No forked heuristic: the plan-time path (`normalize_plan`) and this
    single-task seam produce identical children for the same task."""
    plan = _plan([_task("T1", acceptance=["one", "two", "three", "four"], band="XL")])
    via_plan = normalize_plan(plan, GranularityConfig())

    via_seam = split_one_task(
        _task("T1", acceptance=["one", "two", "three", "four"], band="XL")
    )

    assert via_seam is not None
    assert list(via_plan.plan.tasks) == via_seam


# ---------------------------------------------------------------------------
# Merge table (T002)
# ---------------------------------------------------------------------------

def _small(task_id: str, files: list[str], deps: list[str] | None = None):
    return _task(task_id, acceptance=[f"do {task_id}"], band="S",
                 files=files, deps=deps)


MERGE_CASES: list[Case] = [
    Case(
        name="three_consecutive_small_tasks_merge_into_one",
        tasks=[
            _small("T1", ["src/app/a.py"]),
            _small("T2", ["src/app/b.py"], deps=["T1"]),
            _small("T3", ["src/app/c.py"], deps=["T2"]),
        ],
        expected_ids=["T1"],
        expected_bands=["M"],
        expected_deps=[[]],
        expected_kinds=["merge"],
        expected_acceptance=[["do T1", "do T2", "do T3"]],
    ),
    Case(
        name="external_dependency_on_middle_member_blocks_the_merge",
        tasks=[
            _small("T1", ["src/app/a.py"]),
            _small("T2", ["src/app/b.py"], deps=["T1"]),
            _small("T3", ["src/app/c.py"], deps=["T2"]),
            _task("T9", acceptance=["later"], band="L", deps=["T2"]),
        ],
        expected_ids=["T1", "T2", "T3", "T9"],
        expected_bands=["S", "S", "S", "L"],
        expected_deps=[[], ["T1"], ["T2"], ["T2"]],
        expected_kinds=["aborted"],
    ),
    Case(
        name="group_cap_three_with_four_candidates_yields_three_plus_one",
        tasks=[
            _small("T1", ["src/app/a.py"]),
            _small("T2", ["src/app/b.py"], deps=["T1"]),
            _small("T3", ["src/app/c.py"], deps=["T2"]),
            _small("T4", ["src/app/d.py"], deps=["T3"]),
        ],
        expected_ids=["T1", "T4"],
        expected_bands=["M", "S"],
        expected_deps=[[], ["T1"]],
        expected_kinds=["merge"],
        expected_acceptance=[["do T1", "do T2", "do T3"], ["do T4"]],
    ),
    Case(
        name="non_overlapping_files_hint_prevents_a_run",
        tasks=[
            _small("T1", ["src/app/a.py"]),
            _small("T2", ["docs/guide.md"], deps=["T1"]),
        ],
        expected_ids=["T1", "T2"],
        expected_bands=["S", "S"],
        expected_deps=[[], ["T1"]],
        expected_kinds=[],
    ),
    Case(
        name="a_task_with_too_many_acceptance_items_is_no_candidate",
        tasks=[
            _small("T1", ["src/app/a.py"]),
            _task("T2", acceptance=["a", "b", "c", "d"], band="S",
                  files=["src/app/b.py"], deps=["T1"]),
        ],
        # T2 is above the acceptance threshold: it splits instead of merging.
        expected_ids=["T1", "T2a", "T2b", "T2c", "T2d"],
        expected_bands=["S", "M", "M", "M", "M"],
        expected_deps=[[], ["T1"], ["T2a"], ["T2b"], ["T2c"]],
        expected_kinds=["split"],
    ),
]


@pytest.mark.parametrize("case", MERGE_CASES, ids=lambda c: c.name)
def test_merge_table(case: Case) -> None:
    result = normalize_plan(_plan(case.tasks), case.cfg)
    tasks = result.plan.tasks

    assert [t.id for t in tasks] == case.expected_ids
    assert [t.est_tokens_band for t in tasks] == case.expected_bands
    assert [list(t.depends_on) for t in tasks] == case.expected_deps
    assert [t.kind for t in result.transformations] == case.expected_kinds
    if case.expected_acceptance is not None:
        assert [list(t.acceptance) for t in tasks] == case.expected_acceptance


def test_merged_task_joins_titles_and_unions_files() -> None:
    plan = _plan([
        _small("T1", ["src/app/a.py"]),
        _small("T2", ["src/app/a.py", "src/app/b.py"], deps=["T1"]),
    ])
    (merged,) = normalize_plan(plan, GranularityConfig()).plan.tasks

    assert merged.title == "task T1 + task T2"
    assert list(merged.files_hint) == ["src/app/a.py", "src/app/b.py"]
    assert merged.est_tokens_band == "M"


def test_merge_record_names_sources_result_and_heuristic_band() -> None:
    plan = _plan([
        _small("T1", ["src/app/a.py"]),
        _small("T2", ["src/app/b.py"], deps=["T1"]),
    ])
    (record,) = normalize_plan(plan, GranularityConfig()).transformations

    assert record.kind == "merge"
    assert record.source_ids == ["T1", "T2"]
    assert record.result_ids == ["T1"]
    assert "heuristically" in record.reason


def test_blocked_merge_is_recorded_with_the_reason() -> None:
    plan = _plan([
        _small("T1", ["src/app/a.py"]),
        _small("T2", ["src/app/b.py"], deps=["T1"]),
        _small("T3", ["src/app/c.py"], deps=["T2"]),
        _task("T9", acceptance=["later"], band="L", deps=["T2"]),
    ])
    (record,) = normalize_plan(plan, GranularityConfig()).transformations

    assert record.kind == "aborted"
    assert record.source_ids == ["T1", "T2", "T3"]
    assert "not the last member" in record.reason


def test_external_dependency_on_the_last_member_still_merges() -> None:
    plan = _plan([
        _small("T1", ["src/app/a.py"]),
        _small("T2", ["src/app/b.py"], deps=["T1"]),
        _task("T9", acceptance=["later"], band="L", deps=["T2"]),
    ])
    result = normalize_plan(plan, GranularityConfig())

    assert [t.id for t in result.plan.tasks] == ["T1", "T9"]
    by_id = {t.id: t for t in result.plan.tasks}
    assert list(by_id["T9"].depends_on) == ["T1"]


def test_merge_that_would_close_a_cycle_is_refused() -> None:
    # T9 depends on the last member T2 and T1 depends on T9: contracting
    # T1+T2 into one node would make that node depend on itself.
    plan = _plan([
        _task("T9", acceptance=["outside"], band="L", deps=["T2"]),
        _small("T1", ["src/app/a.py"], deps=["T9"]),
        _small("T2", ["src/app/b.py"]),
    ])
    result = normalize_plan(plan, GranularityConfig())

    assert [t.id for t in result.plan.tasks] == ["T9", "T1", "T2"]
    (record,) = result.transformations
    assert record.kind == "aborted"
    assert "cycle" in record.reason


# ---------------------------------------------------------------------------
# Mixed fixture (T003 acceptance)
# ---------------------------------------------------------------------------

def _mixed_fixture() -> list[PlannedTask]:
    """One XL/four-acceptance task, three trivial neighbors, one M task."""
    return [
        _task(
            "T1",
            acceptance=["parser core", "runner loop", "docs page", "cli flag"],
            band="XL",
            files=["src/parser.py", "src/runner.py", "docs/page.md",
                   "cli/flag.py"],
        ),
        _small("T2", ["lib/util/a.py"], deps=["T1"]),
        _small("T3", ["lib/util/b.py"], deps=["T2"]),
        _small("T4", ["lib/util/c.py"], deps=["T3"]),
        _task("T5", acceptance=["wire it", "prove it"], band="M",
              deps=["T4"]),
    ]


_HEURISTIC = "assigned heuristically (no cost history — F016 v1)"

_MIXED_GOLDEN = [
    {
        "kind": "split",
        "source_ids": ["T1"],
        "result_ids": ["T1a", "T1b", "T1c", "T1d"],
        "reason": (
            "split (band XL at/above split band XL + acceptance count 4 > 3) "
            f"into 4 acceptance clusters; children band M {_HEURISTIC}"),
    },
    {
        "kind": "merge",
        "source_ids": ["T2", "T3", "T4"],
        "result_ids": ["T2"],
        "reason": (
            "merged 3 consecutive S-band tasks sharing files_hint tokens; "
            f"band M {_HEURISTIC}"),
    },
]


def test_mixed_fixture_normalizes_and_matches_the_golden_record() -> None:
    """Acceptance fixture: one XL task, three trivial neighbors, one M task."""
    result = normalize_plan(_plan(_mixed_fixture()), GranularityConfig())
    tasks = result.plan.tasks

    assert [t.id for t in tasks] == ["T1a", "T1b", "T1c", "T1d", "T2", "T5"]
    assert [t.est_tokens_band for t in tasks] == [
        "M", "M", "M", "M", "M", "M"]
    assert [list(t.depends_on) for t in tasks] == [
        [], ["T1a"], ["T1b"], ["T1c"], ["T1d"], ["T2"]]
    # The M task came through untouched.
    assert tasks[-1] == _mixed_fixture()[-1].model_copy(
        update={"depends_on": ["T2"]})
    assert result.as_dicts() == _MIXED_GOLDEN


def test_normalizing_twice_yields_identical_output() -> None:
    first = normalize_plan(_plan(_mixed_fixture()), GranularityConfig())
    second = normalize_plan(_plan(_mixed_fixture()), GranularityConfig())

    assert first.plan.model_dump() == second.plan.model_dump()
    assert first.as_dicts() == second.as_dicts()

    # ...and the normalized plan is a fixed point: nothing left to right-size.
    again = normalize_plan(first.plan, GranularityConfig())
    assert again.plan is first.plan
    assert again.transformations == []


def test_disabled_flag_is_a_byte_identical_pass_through() -> None:
    plan = _plan(_mixed_fixture())
    before = plan.model_dump()
    result = normalize_plan(plan, GranularityConfig(enabled=False))

    assert result.plan is plan
    assert result.plan.model_dump() == before
    assert result.transformations == []


def test_revalidation_failure_aborts_to_the_original_plan() -> None:
    # 24 tasks + a 4-way split would be 27, over the schema's 25-task cap:
    # the new FlightPlan cannot be constructed, so nothing is applied.
    tasks = [_task(f"F{i:03d}", acceptance=["a"], band="M") for i in range(23)]
    tasks.append(_task("T1", acceptance=["one", "two", "three", "four"],
                       band="XL"))
    plan = _plan(tasks)
    result = normalize_plan(plan, GranularityConfig())

    assert result.plan is plan
    (record,) = result.transformations
    assert record.kind == "aborted"
    assert "25-task cap" in record.reason
    assert record.source_ids == [t.id for t in tasks]


def test_merge_group_size_one_disables_merging() -> None:
    plan = _plan([
        _small("T1", ["src/app/a.py"]),
        _small("T2", ["src/app/b.py"], deps=["T1"]),
    ])
    result = normalize_plan(plan, GranularityConfig(merge_group_size=1))

    assert [t.id for t in result.plan.tasks] == ["T1", "T2"]
    assert result.transformations == []
