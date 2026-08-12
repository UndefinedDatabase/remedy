"""F105 T004 — the before/after cacheable-prefix measurement, per migrated role.

This module MEASURES; it does not re-pin prompt content. The six T003
content-equality goldens own the bytes, and every pre-migration form used here
is READ FROM THOSE GOLDENS rather than retyped: nothing in this file is a second
copy of a frozen template.

What is measured, per role, in characters:

    before_prefix   longest common prefix of two PRE-migration renders
    after_prefix    longest common prefix of the two COMPOSED renders
    before_total    length of the first PRE-migration render
    after_total     length of the first composed render

The two renders of a pair differ ONLY in volatile input — the per-task or
per-round content that carries the last stability ranks (TASK, STEERING) — and
are otherwise identical. That is the exact situation a provider prompt cache is
paid to exploit: a second round of the same job re-sends the same stable prefix.

The ONLY assertion this module makes about the numbers is the DIRECTIONAL one,
``after_prefix >= before_prefix``. Exact byte counts are deliberately NOT
asserted: a legitimate later prompt change would then break a test that is not
about content, and the goldens already own content.

How the pre-migration render is obtained differs by site, because the goldens
differ:

  - intake, plan, mission freeze a TEMPLATE, so the pre-migration render is that
    template formatted — via the golden's own ``_frozen_render`` helper where it
    already takes the volatile argument, and via the golden's own frozen
    constant with the golden's own other arguments where it does not. The
    mission case carries a guard test proving the parameterised call reproduces
    the golden's own render byte for byte.
  - builder and reviewer freeze RENDERS for fixed fixtures, so the pre-migration
    render for a varied fixture is REASSEMBLED from the composed segments in the
    golden's own ``_PRE_MIGRATION_ORDER``. That reassembly is not invented here:
    it is exactly what the goldens assert equals the frozen renders, and two
    guard tests below re-prove it at the parameterisation boundary.
  - orchestrator's pre-migration order was ALREADY rank order, so its composed
    text is byte-equal to the frozen render and the measurement is expected to
    come out unchanged. An honest zero-delta is a result, not a gap.

Run the table on its own from the repo root::

    python3 -m tests.orchestration.test_prompt_cache_prefix

The numbers in `docs/system/cache-optimal-prompt-ordering-v1.md` come from that
command, and from :func:`measure_cacheable_prefixes` alone, so the doc's figures
and this module's figures cannot drift.
"""
from __future__ import annotations

import os.path

import pytest

from packages.orchestration.flight_plan import compose_flight_plan_prompt
from packages.orchestration.intake import compose_intake_prompt
from packages.orchestration.mission_compiler import (
    compose_mission_prompt,
    resolve_milestone_cap,
)
from packages.orchestration.mission_plan_schema import (
    MAX_MILESTONE_DRAFT_JOBS,
    MISSION_PLAN_DRAFT_SCHEMA_V,
)
from packages.orchestration.orchestrator_loop import (
    OrchestratorContext,
    compose_orchestrator_prompt,
    context_digest,
)
from packages.orchestration.pingpong_loop import (
    compose_builder_prompt,
    compose_reviewer_prompt,
)
from packages.orchestration.prompt_segments import PROMPT_SEGMENT_DELIMITER
from tests.orchestration import test_builder_prompt_golden as builder_golden
from tests.orchestration import test_intake_prompt_golden as intake_golden
from tests.orchestration import test_mission_prompt_golden as mission_golden
from tests.orchestration import test_orchestrator_prompt_golden as orchestrator_golden
from tests.orchestration import test_plan_prompt_golden as plan_golden
from tests.orchestration import test_reviewer_prompt_golden as reviewer_golden

#: The six roles T003 migrated, in migration-site order.
ROLES = ("intake", "plan", "mission", "builder", "reviewer", "orchestrator")

#: The four measured figures, in table order.
FIGURES = ("before_prefix", "after_prefix", "before_total", "after_total")

# ---------------------------------------------------------------------------
# Volatile inputs. Each pair varies ONE thing that ranks TASK or later; every
# stable input is the golden's own fixture value, held fixed.
# ---------------------------------------------------------------------------

#: intake — the mission text (rank TASK).
_OTHER_MISSION = "Fix the flaky import in packages/orchestration/flight_plan.py"

#: mission — the compiled goal (rank TASK). The cap is left at its default so
#: the cap-scoped rules segment (DECISION F105 D4) is held fixed.
_OTHER_GOAL = "The mission compiler keeps its manifest under a golden as well"

#: builder / reviewer — the task and its round number (ranks TASK / TASK).
_OTHER_BUILDER_GOAL = "Make the widget keep its aspect ratio while resizing."
_OTHER_REVIEWER_GOAL = "Make the widget keep its aspect ratio while resizing."

#: orchestrator — the assembled mission-state text (rank JOB_CONTEXT). Built
#: directly rather than through a mission fixture: `OrchestratorContext` is a
#: frozen dataclass whose `.text` is the only field composition reads, which is
#: why the golden's own cacheable-prefix test varies it with `replace(...)`.
_CONTEXT_TEXT = "## Mission dossier\n\nShip the thing.\n\n## Milestones\n- M001: ready"
_OTHER_CONTEXT_TEXT = "## Mission dossier\n\nA different mission."


def _context(text: str) -> OrchestratorContext:
    return OrchestratorContext(text=text, digest=context_digest(text))


# ---------------------------------------------------------------------------
# Pre-migration renders, read from the goldens.
# ---------------------------------------------------------------------------


def _mission_frozen_render(goal: str) -> str:
    """`mission_golden._frozen_render`, with the GOAL opened up as a parameter.

    Every other argument is the golden's own; the frozen template is the
    golden's own constant. `test_the_mission_parameterisation_is_faithful`
    proves this reproduces the golden's render for the golden's own goal.
    """
    return mission_golden._PRE_MIGRATION_MISSION_TEMPLATE.format(
        goal=goal.strip(),
        repo_facts=mission_golden._PROJECT_FACTS,
        max_milestones=resolve_milestone_cap(None),
        max_draft_jobs=MAX_MILESTONE_DRAFT_JOBS,
        schema_v=MISSION_PLAN_DRAFT_SCHEMA_V,
    )


def _reassembled_pre_migration_render(composed, golden) -> str:
    """The pre-migration render of ``composed``, per the golden's own order.

    The golden asserts that its segments, reordered by `_PRE_MIGRATION_ORDER`
    and joined on the delimiter, ARE the frozen render byte for byte. That is
    what makes this reconstruction legitimate for fixture values the frozen
    renders do not cover — and `_segment_texts` re-verifies every slice against
    its manifest hash on the way through.
    """
    texts = golden._segment_texts(composed)
    ordered = [texts[name] for name in golden._PRE_MIGRATION_ORDER if name in texts]
    assert len(ordered) == len(texts)
    return PROMPT_SEGMENT_DELIMITER.join(ordered)


def _builder_composed(goal: str, round_number: int):
    shape = dict(builder_golden._SHAPES["full"])
    shape["round_number"] = round_number
    return compose_builder_prompt(goal, builder_golden._CONTEXT, **shape)


def _reviewer_composed(goal: str):
    return compose_reviewer_prompt(
        goal, reviewer_golden._BUILDER_SUMMARY,
        **reviewer_golden._SHAPES["scoped_full"])


# ---------------------------------------------------------------------------
# One (before_pair, after_pair) provider per role.
# ---------------------------------------------------------------------------


def _pair_intake() -> tuple[tuple[str, str], tuple[str, str]]:
    missions = (intake_golden._MISSION, _OTHER_MISSION)
    before = tuple(intake_golden._frozen_render(m) for m in missions)
    after = tuple(compose_intake_prompt(m).text for m in missions)
    return before, after


def _pair_plan() -> tuple[tuple[str, str], tuple[str, str]]:
    intakes = (plan_golden._INTAKE, plan_golden._OTHER_INTAKE)
    before = tuple(plan_golden._frozen_render(i) for i in intakes)
    after = tuple(
        compose_flight_plan_prompt(
            i, project_facts=plan_golden._PROJECT_FACTS).text
        for i in intakes
    )
    return before, after


def _pair_mission() -> tuple[tuple[str, str], tuple[str, str]]:
    goals = (mission_golden._GOAL, _OTHER_GOAL)
    before = tuple(_mission_frozen_render(g) for g in goals)
    after = tuple(
        compose_mission_prompt(
            g, project_facts=mission_golden._PROJECT_FACTS).text
        for g in goals
    )
    return before, after


def _pair_builder() -> tuple[tuple[str, str], tuple[str, str]]:
    shapes = (
        (builder_golden._GOAL, builder_golden._ROUND),
        (_OTHER_BUILDER_GOAL, builder_golden._OTHER_ROUND),
    )
    composed = [_builder_composed(goal, rnd) for goal, rnd in shapes]
    before = tuple(
        _reassembled_pre_migration_render(c, builder_golden) for c in composed)
    after = tuple(c.text for c in composed)
    return before, after


def _pair_reviewer() -> tuple[tuple[str, str], tuple[str, str]]:
    goals = (reviewer_golden._GOAL, _OTHER_REVIEWER_GOAL)
    composed = [_reviewer_composed(g) for g in goals]
    before = tuple(
        _reassembled_pre_migration_render(c, reviewer_golden) for c in composed)
    after = tuple(c.text for c in composed)
    return before, after


def _pair_orchestrator() -> tuple[tuple[str, str], tuple[str, str]]:
    texts = (_CONTEXT_TEXT, _OTHER_CONTEXT_TEXT)
    before = tuple(orchestrator_golden._frozen_full_render(t) for t in texts)
    after = tuple(compose_orchestrator_prompt(_context(t)).text for t in texts)
    return before, after


_PAIRS = {
    "intake": _pair_intake,
    "plan": _pair_plan,
    "mission": _pair_mission,
    "builder": _pair_builder,
    "reviewer": _pair_reviewer,
    "orchestrator": _pair_orchestrator,
}


def _common_prefix_chars(one: str, other: str) -> int:
    return len(os.path.commonprefix([one, other]))


def measure_cacheable_prefixes() -> dict[str, dict[str, int]]:
    """The before/after cacheable-prefix table, role -> the four figures.

    The single source of the numbers: the doc quotes this, the tests assert on
    this, and the CLI-style invocation in the module docstring prints this, so
    the three cannot drift apart.
    """
    table: dict[str, dict[str, int]] = {}
    for role in ROLES:
        before, after = _PAIRS[role]()
        table[role] = {
            "before_prefix": _common_prefix_chars(*before),
            "after_prefix": _common_prefix_chars(*after),
            "before_total": len(before[0]),
            "after_total": len(after[0]),
        }
    return table


def render_measurement_table() -> str:
    """The measurement as a markdown table — the doc's figures, verbatim."""
    lines = [
        "| Role | before_prefix | after_prefix | before_total | after_total |",
        "|---|---|---|---|---|",
    ]
    for role, figures in measure_cacheable_prefixes().items():
        cells = " | ".join(str(figures[name]) for name in FIGURES)
        lines.append(f"| {role} | {cells} |")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_every_migrated_role_is_measured():
    table = measure_cacheable_prefixes()
    assert tuple(table) == ROLES
    for role, figures in table.items():
        assert tuple(figures) == FIGURES, role


@pytest.mark.parametrize("role", ROLES)
def test_the_cacheable_prefix_never_shrank(role):
    """F105's directional acceptance: reordering never costs cacheable prefix."""
    figures = measure_cacheable_prefixes()[role]
    assert figures["after_prefix"] >= figures["before_prefix"], (
        f"{role}: after_prefix {figures['after_prefix']} "
        f"< before_prefix {figures['before_prefix']}")


@pytest.mark.parametrize("role", ROLES)
def test_the_volatile_input_really_varies(role):
    """Guards against a vacuous measurement: identical renders share everything."""
    before, after = _PAIRS[role]()
    assert before[0] != before[1], role
    assert after[0] != after[1], role


def test_the_mission_parameterisation_is_faithful():
    """Opening the goal up as a parameter changed nothing else in the render."""
    assert _mission_frozen_render(mission_golden._GOAL) == (
        mission_golden._frozen_render())


def test_the_builder_reassembly_reproduces_the_frozen_render():
    """The reassembled pre-migration render is the golden's own, byte for byte."""
    composed = _builder_composed(builder_golden._GOAL, builder_golden._ROUND)
    assert _reassembled_pre_migration_render(composed, builder_golden) == (
        builder_golden._FROZEN_RENDERS["full"])


def test_the_reviewer_reassembly_reproduces_the_frozen_render():
    composed = _reviewer_composed(reviewer_golden._GOAL)
    assert _reassembled_pre_migration_render(composed, reviewer_golden) == (
        reviewer_golden._FROZEN_RENDERS["scoped_full"])


if __name__ == "__main__":  # pragma: no cover - the doc's reproduction command
    print(render_measurement_table())
