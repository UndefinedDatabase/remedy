"""F105 T003 site-2 content-equality golden for the mission prompt.

This is the golden that pins `packages/orchestration/mission_compiler.py`'s
prompt while its composition moves to the prompt-segment registry. The feature
file (docs/roadmap/features/T2_F105.md) asks for content equality "modulo
ordering", so what is pinned here is the segment SET and each segment's BYTES,
not the concatenated string: the migration deliberately moves the rules block
ahead of the repo facts and the goal so the cacheable prefix reaches the end of
the rules.

`_PRE_MIGRATION_MISSION_TEMPLATE` below is the frozen `_MISSION_PROMPT_TEMPLATE`
exactly as it stood at commit ed5b2421. It was obtained with
`git show ed5b2421:packages/orchestration/mission_compiler.py` and sliced in by
line index; not one byte of it was retyped.

It must NEVER be edited to make a failing test pass. An intentional change to
the prompt's CONTENT is precisely the event this file exists to fail on: if a
future change is meant to alter the words, that change updates this constant in
its own reviewed diff, with the content change declared, and never as a
side-effect of getting a red suite green.
"""
from __future__ import annotations

import hashlib

from packages.orchestration.mission_compiler import (
    build_mission_prompt,
    compose_mission_prompt,
    resolve_milestone_cap,
)
from packages.orchestration.mission_plan_schema import (
    MAX_MILESTONE_DRAFT_JOBS,
    MISSION_PLAN_DRAFT_SCHEMA_V,
)
from packages.orchestration.prompt_segments import ComposedPrompt

_PRE_MIGRATION_MISSION_TEMPLATE = """\
You are compiling a mission plan. A MISSION is a long-lived goal that outlives
any single job. Break the goal below into the ordered milestones that reach it.

## Mission Goal
{goal}

## Repo Facts
{repo_facts}

## Rules
- A milestone is an OUTCOME, not a step: state what is TRUE once it is
  reached ("the payments API stays releasable"), never the actions taken to
  get there ("add tests, refactor the client"). A milestone phrased as a task
  list is rejected.
- Each milestone needs a unique id (e.g. "M001", "M002") with no whitespace.
- depends_on lists the milestone ids that must be reached first. No cycles.
- Maximum {max_milestones} milestones. If the goal seems to need more, the
  milestones are too small — raise their altitude instead.
- rationale says in one line why this milestone exists.
- jobs_draft is an OUTLINE of the work the milestone will probably need:
  {{"title": "...", "goal": "...", "est_band": "S|M|L|XL"}}. These are sketches
  for a human to read, NOT runnable jobs, and nothing starts them. At most
  {max_draft_jobs} per milestone, and every title and goal must be non-empty —
  a milestone needing more outlines than that is a project, not a milestone.
- risks lists what could make this mission fail.
- assumptions lists what you decided on your own because the goal did not say.
  Prefer conservative choices: an assumption keeps existing behavior or does
  nothing; it never deletes, overwrites or migrates.

Return ONLY a JSON object matching the {schema_v} schema.
"""


#: A single-line goal with no blank line in it, so splitting a rendered prompt
#: on the segment delimiter yields exactly one part per segment.
_GOAL = "The mission compiler keeps its prompt bytes under a golden"

#: ONE paragraph of repo facts, passed explicitly. `build_mission_prompt` falls
#: back to `repo_facts_block()`, which reads the working tree — an explicit
#: block is what makes this golden deterministic without a new seam, and that
#: `build_mission_prompt` already accepts `project_facts` is why this site is
#: second in the F105 migration order.
_PROJECT_FACTS = "Repo: remedy. Language: Python. Tests: pytest."

#: A caller-supplied milestone cap. `gauntlet_runner.py` varies this per call,
#: which is what makes the rules segment cap-scoped (DECISION F105 D4).
_EXPLICIT_CAP = 3


def _frozen_render(max_milestones: int | None = None) -> str:
    """The prompt as the pre-migration builder would have rendered it."""
    return _PRE_MIGRATION_MISSION_TEMPLATE.format(
        goal=_GOAL.strip(),
        repo_facts=_PROJECT_FACTS,
        max_milestones=resolve_milestone_cap(max_milestones),
        max_draft_jobs=MAX_MILESTONE_DRAFT_JOBS,
        schema_v=MISSION_PLAN_DRAFT_SCHEMA_V,
    )


def _segment_texts(text: str) -> list[str]:
    """The composed segments of ``text``; the manifest carries hashes, not text."""
    return text.split("\n\n")


def _composed(max_milestones: int | None = None) -> ComposedPrompt:
    """The composed prompt for the golden's fixed goal and repo facts."""
    return compose_mission_prompt(
        _GOAL, project_facts=_PROJECT_FACTS, max_milestones=max_milestones)


def _hashes_by_name(composed: ComposedPrompt) -> dict[str, str]:
    return {entry.name: entry.sha256 for entry in composed.manifest}


def test_segment_texts_equal_the_pre_migration_parts():
    frozen_parts = _frozen_render().split("\n\n")
    assert len(frozen_parts) == 5

    composed = _composed()
    composed_parts = _segment_texts(composed.text)
    assert sorted(composed_parts) == sorted(frozen_parts)

    frozen_hashes = sorted(
        hashlib.sha256(part.encode("utf-8")).hexdigest() for part in frozen_parts
    )
    assert sorted(entry.sha256 for entry in composed.manifest) == frozen_hashes


def test_rules_now_compose_ahead_of_the_goal():
    frozen = _frozen_render()
    assert frozen.index("## Rules") > frozen.index("## Mission Goal")

    composed = _composed()
    assert composed.text.index("## Rules") < composed.text.index("## Mission Goal")

    system, goal, repo_facts, rules, directive = frozen.split("\n\n")
    assert composed.text == "\n\n".join(
        [system, rules, repo_facts, goal, directive])


def test_manifest_names_and_ranks():
    composed = _composed()
    assert tuple(entry.name for entry in composed.manifest) == (
        "mission_system",
        "mission_rules",
        "mission_repo_facts",
        "mission_goal",
        "mission_schema_directive",
    )
    assert tuple(entry.rank for entry in composed.manifest) == (0, 1, 2, 4, 5)


def test_rules_segment_is_cap_scoped():
    """DECISION F105 D4: the rules are stable PER CAP VALUE, not per role."""
    same_a = _hashes_by_name(_composed(_EXPLICIT_CAP))
    same_b = _hashes_by_name(_composed(_EXPLICIT_CAP))
    other = _hashes_by_name(_composed(_EXPLICIT_CAP + 1))

    assert same_a == same_b
    assert same_a["mission_rules"] != other["mission_rules"]
    for name in (
        "mission_system",
        "mission_repo_facts",
        "mission_goal",
        "mission_schema_directive",
    ):
        assert same_a[name] == other[name]


def test_build_mission_prompt_returns_the_composed_text():
    for cap in (None, _EXPLICIT_CAP):
        built = build_mission_prompt(
            _GOAL, project_facts=_PROJECT_FACTS, max_milestones=cap)
        assert isinstance(built, str)
        assert built == _composed(cap).text

    # Reordered back into the pre-migration order, the composed bytes ARE the
    # frozen render — trailing newline included, which is why the schema
    # directive segment carries one.
    built = build_mission_prompt(_GOAL, project_facts=_PROJECT_FACTS)
    system, rules, repo_facts, goal, directive = built.split("\n\n")
    assert "\n\n".join([system, goal, repo_facts, rules, directive]) == _frozen_render()
    assert built.endswith("\n")
    assert len(built) == len(_frozen_render())
