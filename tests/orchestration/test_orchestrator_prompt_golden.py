"""F105 T003 site-4 content-equality golden for the orchestrator prompt.

This is the golden that pins `packages/orchestration/orchestrator_loop.py`'s
prompt — `build_orchestrator_prompt` and its system half
`build_orchestrator_system_prompt` — while their composition moves to the
prompt-segment registry. Unlike sites 1-3, this site's pre-migration order was
ALREADY rank order, so what is pinned here is BYTE equality (`==`) with the
pre-migration render rather than equality modulo ordering.

`_PRE_MIGRATION_SYSTEM_FORM` and `_PRE_MIGRATION_FULL_FORM` below are the two
frozen f-string bodies exactly as they stood at commit 04a3396d. They were
obtained with `git show 04a3396d:packages/orchestration/orchestrator_loop.py`,
sliced in by line index and unescaped with Python's own string unescaper; not
one byte of them was retyped. Their only placeholders are the protocol version,
the source path, the protocol text and the context text.

The protocol DOCUMENT is deliberately NOT frozen here. It is large, it is
expected to change, and freezing it would turn this golden into a second copy
of a document that already has one home
(`docs/agents/orchestrator_protocol.md`).

This file must NEVER be edited to make a failing test pass. An intentional
change to the prompt's CONTENT is precisely the event it exists to fail on: a
change meant to alter the words updates these constants in its own reviewed
diff, with the content change declared, and never as a side-effect of getting a
red suite green.
"""
from __future__ import annotations

import hashlib
import os.path
from dataclasses import replace

import pytest

from packages.orchestration.mission_plan_schema import (
    MISSION_PLAN_SCHEMA_V,
    Milestone,
    MissionPlan,
)
from packages.orchestration.mission_state import (
    create_mission,
    load_mission,
    set_mission_plan,
)
from packages.orchestration.orchestrator_loop import (
    PROTOCOL_DOC_RELATIVE,
    PROTOCOL_VERSION,
    assemble_context,
    build_orchestrator_prompt,
    build_orchestrator_system_prompt,
    compose_orchestrator_prompt,
    compose_orchestrator_system_prompt,
    orchestrator_protocol_text,
)
from packages.orchestration.prompt_segments import (
    PROMPT_SEGMENT_DELIMITER,
    ComposedPrompt,
)

PROJECT = "p-f105-orchestrator-golden"

_PRE_MIGRATION_SYSTEM_FORM = (
    "# Orchestrator protocol {version}\n"
    "# Source: {source} (versioned in the repository)\n"
    "\n"
    "{protocol_text}"
)

_PRE_MIGRATION_FULL_FORM = (
    "# Orchestrator protocol {version}\n"
    "# Source: {source} (versioned in the repository)\n"
    "\n"
    "{protocol_text}\n"
    "\n"
    "# Mission state\n"
    "\n"
    "{context_text}"
)

#: The two per-segment forms, SLICED out of the frozen constants above rather
#: than restated beside them: the system header is everything before the frozen
#: system form's first blank line, and the mission-state block is everything
#: after the frozen full form's protocol placeholder. Slicing keeps one frozen
#: source of truth, so a future content change cannot be half-applied.
_SYSTEM_SEGMENT_FORM = _PRE_MIGRATION_SYSTEM_FORM.split(PROMPT_SEGMENT_DELIMITER)[0]
_MISSION_STATE_SEGMENT_FORM = _PRE_MIGRATION_FULL_FORM.split(
    "{protocol_text}" + PROMPT_SEGMENT_DELIMITER)[1]


@pytest.fixture()
def mission(tmp_path):
    """A persisted mission with a compiled two-milestone plan.

    Built with the same verbs and the same shape as the `mission` fixture in
    `tests/orchestration/test_orchestrator_loop.py`, so this golden pins the
    prompt the loop's own tests exercise rather than one invented here. The
    mission root is `tmp_path`, so the repository's data root is never touched.
    """
    plan = MissionPlan(
        schema_v=MISSION_PLAN_SCHEMA_V,
        milestones=[
            Milestone(
                id=mid,
                goal=f"The outcome of {mid} holds",
                rationale=f"{mid} exists",
                depends_on=list(deps),
                jobs_draft=[{"title": f"{mid} work", "goal": f"do {mid}",
                             "est_band": "M"}],
            )
            for mid, deps in (("M001", ()), ("M002", ("M001",)))
        ],
        compiled=True,
        origin="provider",
    )
    created = create_mission(PROJECT, "Ship the thing", root=tmp_path)
    set_mission_plan(PROJECT, created.id, plan.model_dump(), tmp_path)
    return load_mission(PROJECT, created.id, tmp_path)


@pytest.fixture()
def context(mission):
    """One iteration's assembled context, from the loop's own assembly verb."""
    return assemble_context(mission)


def _frozen_system_render() -> str:
    """The system prompt as the pre-migration builder would have rendered it."""
    return _PRE_MIGRATION_SYSTEM_FORM.format(
        version=PROTOCOL_VERSION,
        source=PROTOCOL_DOC_RELATIVE,
        protocol_text=orchestrator_protocol_text(),
    )


def _frozen_full_render(context_text: str) -> str:
    """The full prompt as the pre-migration builder would have rendered it."""
    return _PRE_MIGRATION_FULL_FORM.format(
        version=PROTOCOL_VERSION,
        source=PROTOCOL_DOC_RELATIVE,
        protocol_text=orchestrator_protocol_text(),
        context_text=context_text,
    )


def _expected_segment_texts(context_text: str) -> list[str]:
    """The three segment texts, rendered from the frozen forms alone."""
    return [
        _SYSTEM_SEGMENT_FORM.format(
            version=PROTOCOL_VERSION, source=PROTOCOL_DOC_RELATIVE),
        orchestrator_protocol_text(),
        _MISSION_STATE_SEGMENT_FORM.format(context_text=context_text),
    ]


def _rows(composed: ComposedPrompt) -> list[tuple[str, int, str]]:
    """Manifest rows as plain tuples, so two manifests compare by value."""
    return [(entry.name, entry.rank, entry.sha256) for entry in composed.manifest]


def _hashes_by_name(composed: ComposedPrompt) -> dict[str, str]:
    return {entry.name: entry.sha256 for entry in composed.manifest}


def test_system_prompt_is_byte_equal_to_the_pre_migration_render():
    assert build_orchestrator_system_prompt() == _frozen_system_render()


def test_full_prompt_is_byte_equal_to_the_pre_migration_render(context):
    assert build_orchestrator_prompt(context) == _frozen_full_render(context.text)


def test_manifest_carries_the_three_declared_segments_in_rank_order(context):
    manifest = compose_orchestrator_prompt(context).manifest
    assert [entry.name for entry in manifest] == [
        "orchestrator_system",
        "orchestrator_protocol",
        "orchestrator_mission_state",
    ]
    ranks = [entry.rank for entry in manifest]
    assert ranks == [0, 1, 3]
    assert all(a <= b for a, b in zip(ranks, ranks[1:])), (
        f"ranks must be non-decreasing, got {ranks}")


def test_composition_injects_no_bytes_of_its_own(context):
    composed = compose_orchestrator_prompt(context)
    expected = _expected_segment_texts(context.text)

    for entry, text in zip(composed.manifest, expected, strict=True):
        assert entry.sha256 == hashlib.sha256(
            text.encode("utf-8")).hexdigest(), entry.name

    assert composed.text == PROMPT_SEGMENT_DELIMITER.join(expected)


def test_only_the_mission_state_segment_moves_with_the_context(context):
    """The cacheable-prefix payoff, MEASURED: the stable prefix survives.

    The shared prefix cannot end EXACTLY at the protocol segment's last byte,
    and the reason is structural rather than a weakened claim: the segment that
    follows opens with the constant `# Mission state` header, so any two
    renders share that header too. What is asserted is therefore the property
    that matters — the whole stable prefix is byte-identical, and the first
    difference falls inside the volatile segment — with the measured shared
    prefix length carried into the message so the number is visible on failure.
    """
    other = replace(context, text="## Mission dossier\n\nA different mission.")
    one = compose_orchestrator_prompt(context)
    two = compose_orchestrator_prompt(other)

    stable = PROMPT_SEGMENT_DELIMITER.join(_expected_segment_texts(context.text)[:2])
    shared = len(os.path.commonprefix([one.text, two.text]))
    assert one.text[:len(stable)] == two.text[:len(stable)]
    assert shared >= len(stable), (
        f"shared prefix is {shared} chars but the protocol segment "
        f"ends at {len(stable)}")
    assert shared < min(len(one.text), len(two.text)), (
        f"the two prompts never diverge; shared prefix is {shared} chars")

    one_hashes, two_hashes = _hashes_by_name(one), _hashes_by_name(two)
    assert one_hashes["orchestrator_system"] == two_hashes["orchestrator_system"]
    assert one_hashes["orchestrator_protocol"] == two_hashes["orchestrator_protocol"]
    assert (one_hashes["orchestrator_mission_state"]
            != two_hashes["orchestrator_mission_state"])


def test_the_system_manifest_is_the_prefix_of_the_full_one(context):
    system = compose_orchestrator_system_prompt()
    full = compose_orchestrator_prompt(context)
    assert len(system.manifest) == 2
    assert _rows(system) == _rows(full)[:2]
