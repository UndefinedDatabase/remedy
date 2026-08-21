"""Tests for teacher Q&A grounding — Stage 2's deterministic half (F255 T004).

These pin the three acceptance rules that must NOT depend on a model call:
every fact names its grounding source, the sources are never mixed silently,
and the level dial changes depth without changing the claim set.

Deliberately NOT tested here: the model call itself and the ledger attribution,
which are T004's second round and need a real provider seam to be honest about.
"""
from __future__ import annotations

import pytest

from packages.orchestration.teacher_qa import (
    DEFAULT_LEVEL,
    GROUNDING_SOURCES,
    LEVEL_DEPTH,
    LEVELS,
    SOURCE_CODE,
    SOURCE_CONCEPT,
    SOURCE_LEDGER,
    build_teacher_context,
    claim_set,
    no_model_refusal,
    render_prompt,
)

_EVENTS = [
    {"event": "job_created", "timestamp": "2026-08-21T00:00:01Z"},
    {"event": "task_run_started", "task_id": "t7", "timestamp": "2026-08-21T00:00:02Z"},
]

_CODE = "def add(a, b):\n    return a + b\n"


class TestGroundingSourcesAreLabelled:
    def test_every_fact_carries_a_known_source(self):
        ctx = build_teacher_context("what happened?", events=_EVENTS, code=_CODE)
        assert ctx.facts
        for fact in ctx.facts:
            assert fact.source in GROUNDING_SOURCES

    def test_ledger_facts_come_only_from_events(self):
        ctx = build_teacher_context("what happened?", events=_EVENTS)
        ledger = [f for f in ctx.facts if f.source == SOURCE_LEDGER]
        assert [f.text for f in ledger] == [
            "The job was created.",
            "A task started: t7",
        ]
        assert not [f for f in ctx.facts if f.source == SOURCE_CODE]

    @pytest.mark.parametrize("code", [None, "", "   \n"])
    def test_no_code_fact_without_real_code(self, code):
        ctx = build_teacher_context("what does add do?", events=_EVENTS, code=code)
        assert not [f for f in ctx.facts if f.source == SOURCE_CODE]

    def test_a_code_fact_names_where_it_was_read(self):
        ctx = build_teacher_context("?", code=_CODE, code_path="apps/x.py")
        code_facts = [f for f in ctx.facts if f.source == SOURCE_CODE]
        assert len(code_facts) == 1
        assert code_facts[0].text.startswith("apps/x.py:")

    def test_the_prompt_labels_each_source_block(self):
        prompt = render_prompt(build_teacher_context("?", events=_EVENTS, code=_CODE))
        for source in GROUNDING_SOURCES:
            assert f"[{source}]" in prompt

    def test_an_empty_context_still_declares_the_concept_source(self):
        prompt = render_prompt(build_teacher_context("what is a mutex?"))
        assert f"[{SOURCE_CONCEPT}]" in prompt
        assert f"[{SOURCE_LEDGER}]" not in prompt
        assert f"[{SOURCE_CODE}]" not in prompt


class TestTheLevelDialChangesDepthNotFacts:
    @pytest.mark.parametrize("level", LEVELS)
    def test_the_claim_set_is_the_same_at_every_level(self, level):
        baseline = claim_set(build_teacher_context("q", events=_EVENTS, code=_CODE))
        at_level = claim_set(
            build_teacher_context("q", events=_EVENTS, code=_CODE, level=level)
        )
        assert at_level == baseline

    @pytest.mark.parametrize("level", LEVELS)
    def test_each_level_asks_for_its_own_depth(self, level):
        prompt = render_prompt(build_teacher_context("q", events=_EVENTS, level=level))
        assert LEVEL_DEPTH[level] in prompt

    def test_the_three_levels_ask_for_three_different_depths(self):
        assert len({LEVEL_DEPTH[level] for level in LEVELS}) == len(LEVELS)

    def test_an_unknown_level_falls_back_and_never_raises(self):
        ctx = build_teacher_context("q", events=_EVENTS, level="wizard")
        assert ctx.level == DEFAULT_LEVEL

    def test_every_level_has_a_depth_and_the_default_is_one_of_them(self):
        assert set(LEVELS) == set(LEVEL_DEPTH)
        assert DEFAULT_LEVEL in LEVELS


class TestHonestyWithoutAModel:
    def test_the_refusal_names_the_reason_and_points_at_stage_1(self):
        message = no_model_refusal("no teacher model is configured")
        assert "no teacher model is configured" in message
        assert "remedy teach narrate" in message

    def test_building_a_context_calls_no_model_and_reads_no_file(self):
        # Zero-token by construction: the context is a pure function of its
        # arguments, so Stage 2's grounding half costs nothing.
        ctx = build_teacher_context("q", events=_EVENTS, code=_CODE)
        assert claim_set(ctx) == claim_set(
            build_teacher_context("q", events=_EVENTS, code=_CODE)
        )
