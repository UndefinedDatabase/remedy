"""F105 T003 site-1 content-equality golden for the intake prompt.

This is the golden that pins `packages/orchestration/intake.py`'s prompt while
its composition moves to the prompt-segment registry. The feature file
(docs/roadmap/features/T2_F105.md) asks for content equality "modulo ordering",
so what is pinned here is the segment SET and each segment's BYTES, not the
concatenated string: the migration deliberately moves the rules block ahead of
the mission text so the cacheable prefix reaches the end of the rules.

`_PRE_MIGRATION_INTAKE_TEMPLATE` below is the frozen `_INTAKE_PROMPT_TEMPLATE`
exactly as it stood at commit 9d773b14. It was obtained with
`git show 9d773b14:packages/orchestration/intake.py` and sliced in by line
index; not one byte of it was retyped.

It must NEVER be edited to make a failing test pass. An intentional change to
the prompt's CONTENT is precisely the event this file exists to fail on: if a
future change is meant to alter the words, that change updates this constant in
its own reviewed diff, with the content change declared, and never as a
side-effect of getting a red suite green.
"""
from __future__ import annotations

import hashlib

from packages.orchestration import intake
from packages.orchestration.intake import _build_intake_prompt, compose_intake_prompt

_PRE_MIGRATION_INTAKE_TEMPLATE = """\
Analyze this mission and produce a structured job intake.

Mission:
{mission}

Rules:
- goal: one clear sentence stating the objective
- context_refs: file paths, URLs, or identifiers mentioned
- constraints: explicit limitations or requirements
- acceptance_hints: how to verify completion
- truncated_input: true only if the mission text is visibly cut off
- clarifications: open questions with default answers and impact
- mission_candidate: true only if this goal plainly outlives a single job
  (ongoing upkeep, a multi-stage effort, a standing commitment). It creates
  nothing on its own — it only offers the choice to a human."""


#: A single-line mission with no blank line in it, so splitting a rendered
#: prompt on the segment delimiter yields exactly one part per segment.
_MISSION = "Fix the flaky import in packages/orchestration/intake.py"

#: Longer than `_MAX_PROMPT_MISSION_CHARS` (8000), so truncation applies.
_OVERSIZE_MISSION = "m" * 9000


def _frozen_render(mission: str) -> str:
    """The prompt as the pre-migration builder would have rendered it."""
    return _PRE_MIGRATION_INTAKE_TEMPLATE.format(mission=mission)


def _segment_texts(text: str) -> list[str]:
    """The composed segments of ``text``; the manifest carries hashes, not text."""
    return text.split("\n\n")


def test_segment_texts_equal_the_pre_migration_parts():
    frozen_parts = _frozen_render(_MISSION).split("\n\n")
    assert len(frozen_parts) == 3

    composed = compose_intake_prompt(_MISSION)
    composed_parts = _segment_texts(composed.text)
    assert sorted(composed_parts) == sorted(frozen_parts)

    frozen_hashes = sorted(
        hashlib.sha256(part.encode("utf-8")).hexdigest() for part in frozen_parts
    )
    assert sorted(entry.sha256 for entry in composed.manifest) == frozen_hashes


def test_rules_now_compose_ahead_of_the_mission():
    frozen = _frozen_render(_MISSION)
    assert frozen.index("Rules:") > frozen.index("Mission:")

    composed = compose_intake_prompt(_MISSION)
    assert composed.text.index("Rules:") < composed.text.index("Mission:")

    system_part, mission_part, rules_part = frozen.split("\n\n")
    assert composed.text == "\n\n".join([system_part, rules_part, mission_part])


def test_manifest_names_and_ranks():
    composed = compose_intake_prompt(_MISSION)
    assert tuple(entry.name for entry in composed.manifest) == (
        "intake_system",
        "intake_rules",
        "intake_mission",
    )
    assert tuple(entry.rank for entry in composed.manifest) == (0, 1, 4)


def test_oversize_mission_still_truncates():
    composed = compose_intake_prompt(_OVERSIZE_MISSION)
    assert len(composed.manifest) == 3

    parts = _segment_texts(composed.text)
    assert len(parts) == 3
    assert composed.manifest[-1].name == "intake_mission"
    assert parts[-1].endswith(intake._TRUNCATION_MARKER)


def test_build_intake_prompt_returns_the_composed_text():
    for mission in (_MISSION, _OVERSIZE_MISSION):
        built = _build_intake_prompt(mission)
        assert isinstance(built, str)
        assert built == compose_intake_prompt(mission).text
