"""F105 T003 site-3 content-equality golden for the flight-plan prompt.

This is the golden that pins `packages/orchestration/flight_plan.py`'s prompt
while its composition moves to the prompt-segment registry. The feature file
(docs/roadmap/features/T2_F105.md) asks for content equality "modulo ordering",
so what is pinned here is the segment SET and each segment's BYTES, not the
concatenated string: the migration deliberately moves the rules block ahead of
the repo facts and the intake so the cacheable prefix reaches the end of the
rules.

`_PRE_MIGRATION_PLAN_TEMPLATE` below is the frozen `_PLAN_PROMPT_TEMPLATE`
exactly as it stood at commit 70156f31. It was obtained with
`git show 70156f31:packages/orchestration/flight_plan.py` and sliced in by line
index; not one byte of it was retyped.

It must NEVER be edited to make a failing test pass. An intentional change to
the prompt's CONTENT is precisely the event this file exists to fail on: if a
future change is meant to alter the words, that change updates this constant in
its own reviewed diff, with the content change declared, and never as a
side-effect of getting a red suite green.
"""
from __future__ import annotations

import hashlib
import json

from packages.orchestration.flight_plan import (
    _build_plan_prompt,
    compose_flight_plan_prompt,
)
from packages.orchestration.prompt_segments import ComposedPrompt

_PRE_MIGRATION_PLAN_TEMPLATE = """\
You are a project planner. Given the intake and repo facts below, produce
a flight plan: a DAG of tasks with goals, acceptance criteria, dependencies,
and token band estimates.

## Intake
{intake_json}

## Repo Facts
{repo_facts}

## Rules
- Each task needs a unique id (e.g. "T001", "T002").
- depends_on lists task ids that must complete first.
- est_tokens_band is one of: S, M, L, XL.
- acceptance must have at least one non-empty criterion per task.
- No cycles in dependencies.
- Maximum 25 tasks.
- RESOLVE the intake's clarifications into plan choices wherever the
  intake, the repo facts, or ordinary engineering judgement settle them.
  Record each one you resolved in clarifications_resolved with your
  chosen answer — that is an assumption you are declaring, not a
  question. The target for a routine mission is zero questions left.
- Carry forward ONLY genuinely ambiguous questions: ones whose answer
  changes the plan and that you cannot settle from the material given.
  Leave those with an empty answer; a human resolves them once, at the
  plan-approval gate, and they are never asked again during the run.
- Every clarification needs a conservative default_answer and an impact
  line. A default keeps existing behavior or does nothing; it never
  deletes, overwrites, migrates, or otherwise takes a destructive path.
  If the safe choice is "change nothing", that is the default.

Return ONLY a JSON object matching the flight_plan_v1 schema.
"""


#: A SMALL fixed intake whose `json.dumps(..., indent=2)` carries no blank line,
#: so splitting a rendered prompt on the segment delimiter yields exactly one
#: part per segment.
_INTAKE = {"schema_v": "ji1", "goal": "ship the planner golden"}

#: A second intake, for the intake-independence check. Same shape, other bytes.
_OTHER_INTAKE = {"schema_v": "ji1", "goal": "ship something else entirely"}

#: ONE paragraph of repo facts, passed explicitly. `_build_plan_prompt` falls
#: back to `repo_facts_block()`, which reads the WORKING DIRECTORY, so a golden
#: pinned in CI would differ from one pinned locally. The `project_facts` seam
#: this round added is what makes this golden deterministic, and needing it is
#: why this site is third in the F105 migration order rather than second.
_PROJECT_FACTS = "Repo: remedy. Language: Python. Tests: pytest."


def _frozen_render(intake: dict | None = None) -> str:
    """The prompt as the pre-migration builder would have rendered it."""
    return _PRE_MIGRATION_PLAN_TEMPLATE.format(
        intake_json=json.dumps(_INTAKE if intake is None else intake, indent=2),
        repo_facts=_PROJECT_FACTS,
    )


def _segment_texts(text: str) -> list[str]:
    """The composed segments of ``text``; the manifest carries hashes, not text."""
    return text.split("\n\n")


def _composed(intake: dict | None = None) -> ComposedPrompt:
    """The composed prompt for the golden's fixed intake and repo facts."""
    return compose_flight_plan_prompt(
        _INTAKE if intake is None else intake, project_facts=_PROJECT_FACTS)


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


def test_rules_now_compose_ahead_of_the_intake():
    frozen = _frozen_render()
    assert frozen.index("## Rules") > frozen.index("## Intake")

    composed = _composed()
    assert composed.text.index("## Rules") < composed.text.index("## Intake")

    system, intake, repo_facts, rules, directive = frozen.split("\n\n")
    assert composed.text == "\n\n".join(
        [system, rules, repo_facts, intake, directive])


def test_manifest_names_and_ranks():
    composed = _composed()
    assert tuple(entry.name for entry in composed.manifest) == (
        "plan_system",
        "plan_rules",
        "plan_repo_facts",
        "plan_intake",
        "plan_schema_directive",
    )
    assert tuple(entry.rank for entry in composed.manifest) == (0, 1, 2, 4, 5)


def test_stable_segments_are_intake_independent():
    """The cacheable-prefix claim: only `plan_intake` moves with the intake.

    Unlike the mission rules (cap-scoped, DECISION F105 D4) these bytes carry
    no caller-varied parameter, so the claim is UNCONDITIONAL here.
    """
    one = _hashes_by_name(_composed())
    other = _hashes_by_name(_composed(_OTHER_INTAKE))

    for name in ("plan_system", "plan_rules", "plan_schema_directive"):
        assert one[name] == other[name]
    assert one["plan_intake"] != other["plan_intake"]


def test_build_plan_prompt_returns_the_composed_text():
    for intake in (_INTAKE, _OTHER_INTAKE):
        built = _build_plan_prompt(intake, project_facts=_PROJECT_FACTS)
        assert isinstance(built, str)
        assert built == _composed(intake).text

    # Reordered back into the pre-migration order, the composed bytes ARE the
    # frozen render — trailing newline included, which is why the schema
    # directive segment carries one.
    built = _build_plan_prompt(_INTAKE, project_facts=_PROJECT_FACTS)
    system, rules, repo_facts, intake, directive = built.split("\n\n")
    assert "\n\n".join(
        [system, intake, repo_facts, rules, directive]) == _frozen_render()
    assert built.endswith("\n")
    assert len(built) == len(_frozen_render())
