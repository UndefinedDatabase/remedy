"""Tests for the prompt segment registry and composition (F105 T001).

Each test pins one property the cache-optimal ordering depends on: rank order,
registration-order tie-break, byte stability, a stable prefix ahead of the
volatile tail, the injection-free delimiter, manifest fidelity, the token cap,
duplicate rejection, the empty case, and the documented rank scale itself.
"""
from __future__ import annotations

import hashlib

import pytest

from packages.orchestration.prompt_segments import (
    CONVENTIONS_TOKEN_CAP,
    PROMPT_SEGMENT_DELIMITER,
    ComposedPrompt,
    PromptSegment,
    PromptSegmentError,
    PromptSegmentRegistry,
    SegmentStabilityRank,
    compose_prompt_segments,
)


def _registry_with(*specs: tuple[str, SegmentStabilityRank, str]) -> PromptSegmentRegistry:
    registry = PromptSegmentRegistry()
    for name, rank, text in specs:
        registry.register(name, rank, text)
    return registry


def _compose(registry: PromptSegmentRegistry) -> ComposedPrompt:
    return compose_prompt_segments(registry.registered_segments())


# ---------------------------------------------------------------------------
# 1-2: ordering
# ---------------------------------------------------------------------------


class TestPromptSegmentOrdering:
    def test_scrambled_registration_composes_in_rank_order(self):
        registry = _registry_with(
            ("steering", SegmentStabilityRank.STEERING, "steer"),
            ("dossier", SegmentStabilityRank.DOSSIER, "doss"),
            ("system", SegmentStabilityRank.SYSTEM, "sys"),
            ("task", SegmentStabilityRank.TASK, "task"),
            ("conventions", SegmentStabilityRank.CONVENTIONS, "conv"),
            ("job", SegmentStabilityRank.JOB_CONTEXT, "job"),
        )
        composed = _compose(registry)
        assert [entry.name for entry in composed.manifest] == [
            "system", "conventions", "dossier", "job", "task", "steering",
        ]
        assert composed.text == "sys\n\nconv\n\ndoss\n\njob\n\ntask\n\nsteer"

    def test_equal_ranks_keep_registration_order(self):
        registry = _registry_with(
            ("conventions_b", SegmentStabilityRank.CONVENTIONS, "second"),
            ("conventions_a", SegmentStabilityRank.CONVENTIONS, "first"),
        )
        composed = _compose(registry)
        assert [entry.name for entry in composed.manifest] == ["conventions_b", "conventions_a"]
        assert composed.text == "second\n\nfirst"

    def test_registered_segments_is_registration_order_not_rank_order(self):
        registry = _registry_with(
            ("task", SegmentStabilityRank.TASK, "task"),
            ("system", SegmentStabilityRank.SYSTEM, "sys"),
        )
        assert [seg.name for seg in registry.registered_segments()] == ["task", "system"]


# ---------------------------------------------------------------------------
# 3-4: byte stability and the volatile tail
# ---------------------------------------------------------------------------


class TestPromptSegmentByteStability:
    def test_composing_twice_yields_identical_bytes(self):
        registry = _registry_with(
            ("system", SegmentStabilityRank.SYSTEM, "sys"),
            ("dossier", SegmentStabilityRank.DOSSIER, "doss"),
            ("task", SegmentStabilityRank.TASK, "task"),
        )
        first = _compose(registry)
        second = _compose(registry)
        assert first.text.encode("utf-8") == second.text.encode("utf-8")
        assert first.manifest == second.manifest

    def test_stable_prefix_survives_a_changed_volatile_tail(self):
        stable = (
            ("system", SegmentStabilityRank.SYSTEM, "you are the builder"),
            ("conventions", SegmentStabilityRank.CONVENTIONS, "write discoverable code"),
            ("dossier", SegmentStabilityRank.DOSSIER, "mission dossier v1"),
            ("job", SegmentStabilityRank.JOB_CONTEXT, "job J-1"),
        )
        first = _compose(_registry_with(
            *stable,
            ("task", SegmentStabilityRank.TASK, "task one"),
            ("steering", SegmentStabilityRank.STEERING, "steer one"),
        ))
        second = _compose(_registry_with(
            *stable,
            ("task", SegmentStabilityRank.TASK, "a completely different task text"),
            ("steering", SegmentStabilityRank.STEERING, "and different steering"),
        ))

        prefix_len = len(_compose(_registry_with(*stable)).text)
        first_prefix = first.text.encode("utf-8")[:prefix_len]
        second_prefix = second.text.encode("utf-8")[:prefix_len]
        assert hashlib.sha256(first_prefix).hexdigest() == hashlib.sha256(second_prefix).hexdigest()
        # The tails really do differ — otherwise the prefix claim is vacuous.
        assert first.text != second.text

    def test_stable_prefix_hash_breaks_when_a_stable_segment_changes(self):
        volatile = (("task", SegmentStabilityRank.TASK, "task one"),)
        first = _compose(_registry_with(
            ("system", SegmentStabilityRank.SYSTEM, "you are the builder"), *volatile))
        second = _compose(_registry_with(
            ("system", SegmentStabilityRank.SYSTEM, "you are the reviewer"), *volatile))
        assert first.text.split(PROMPT_SEGMENT_DELIMITER)[0] != second.text.split(
            PROMPT_SEGMENT_DELIMITER)[0]


# ---------------------------------------------------------------------------
# 5: delimiter stability — no injected headers, labels or markers
# ---------------------------------------------------------------------------


class TestPromptSegmentDelimiter:
    def test_delimiter_is_a_plain_blank_line(self):
        assert PROMPT_SEGMENT_DELIMITER == "\n\n"

    def test_exactly_one_blank_line_between_adjacent_segments(self):
        composed = _compose(_registry_with(
            ("system", SegmentStabilityRank.SYSTEM, "alpha"),
            ("task", SegmentStabilityRank.TASK, "beta"),
        ))
        assert composed.text == "alpha\n\nbeta"
        assert "\n\n\n" not in composed.text

    def test_single_segment_composition_adds_nothing(self):
        composed = _compose(_registry_with(
            ("system", SegmentStabilityRank.SYSTEM, "just this"),
        ))
        assert composed.text == "just this"

    def test_no_names_ranks_or_markers_are_injected_into_the_text(self):
        composed = _compose(_registry_with(
            ("system_segment_name", SegmentStabilityRank.SYSTEM, "alpha"),
            ("task_segment_name", SegmentStabilityRank.TASK, "beta"),
        ))
        assert composed.text == "alpha\n\nbeta"
        for injected in ("system_segment_name", "task_segment_name", "SYSTEM", "TASK",
                         "rank", "---", "###", "<segment"):
            assert injected not in composed.text


# ---------------------------------------------------------------------------
# 6: manifest fidelity
# ---------------------------------------------------------------------------


class TestPromptSegmentManifest:
    def test_manifest_matches_the_composed_text(self):
        texts = {"system": "you are remedy", "dossier": "döss", "task": "do it"}
        composed = _compose(_registry_with(
            ("task", SegmentStabilityRank.TASK, texts["task"]),
            ("system", SegmentStabilityRank.SYSTEM, texts["system"]),
            ("dossier", SegmentStabilityRank.DOSSIER, texts["dossier"]),
        ))
        assert [entry.name for entry in composed.manifest] == ["system", "dossier", "task"]
        assert [entry.rank for entry in composed.manifest] == [0, 2, 4]
        assert composed.text.split(PROMPT_SEGMENT_DELIMITER) == [
            texts["system"], texts["dossier"], texts["task"],
        ]
        for entry in composed.manifest:
            source = texts[entry.name]
            # Recomputed here on purpose: trusting the module's own hash would
            # make this test agree with any bug the module has.
            assert entry.sha256 == hashlib.sha256(source.encode("utf-8")).hexdigest()
            assert entry.chars == len(source)
            assert entry.tokens_estimated >= 1

    def test_manifest_as_dicts_is_json_ready_and_in_order(self):
        composed = _compose(_registry_with(
            ("task", SegmentStabilityRank.TASK, "do it"),
            ("system", SegmentStabilityRank.SYSTEM, "you are remedy"),
        ))
        rows = composed.manifest_as_dicts()
        assert [row["name"] for row in rows] == ["system", "task"]
        assert set(rows[0]) == {"name", "rank", "sha256", "chars", "tokens_estimated"}
        assert rows[0]["rank"] == 0 and isinstance(rows[0]["rank"], int)


# ---------------------------------------------------------------------------
# 7-9: registration failures and the empty case
# ---------------------------------------------------------------------------


class TestPromptSegmentRegistration:
    def test_over_cap_registration_raises_and_names_segment_and_numbers(self):
        registry = PromptSegmentRegistry()
        with pytest.raises(PromptSegmentError) as excinfo:
            registry.register("conventions", SegmentStabilityRank.CONVENTIONS,
                              "x" * 4000, token_cap=CONVENTIONS_TOKEN_CAP)
        message = str(excinfo.value)
        assert "conventions" in message
        assert "1000" in message           # the chars/4 estimate for 4000 chars
        assert str(CONVENTIONS_TOKEN_CAP) in message
        assert registry.registered_segments() == ()

    def test_under_cap_registration_does_not_raise(self):
        registry = PromptSegmentRegistry()
        segment = registry.register("conventions", SegmentStabilityRank.CONVENTIONS,
                                    "x" * 400, token_cap=CONVENTIONS_TOKEN_CAP)
        assert isinstance(segment, PromptSegment)
        assert registry.registered_segments() == (segment,)

    def test_conventions_token_cap_is_the_documented_number(self):
        assert CONVENTIONS_TOKEN_CAP == 800

    def test_duplicate_name_raises(self):
        registry = _registry_with(("system", SegmentStabilityRank.SYSTEM, "a"))
        with pytest.raises(PromptSegmentError) as excinfo:
            registry.register("system", SegmentStabilityRank.TASK, "b")
        assert "system" in str(excinfo.value)
        assert len(registry.registered_segments()) == 1

    def test_blank_name_raises(self):
        registry = PromptSegmentRegistry()
        with pytest.raises(PromptSegmentError):
            registry.register("   ", SegmentStabilityRank.SYSTEM, "a")

    def test_unknown_rank_raises(self):
        registry = PromptSegmentRegistry()
        with pytest.raises(PromptSegmentError):
            registry.register("system", 99, "a")  # type: ignore[arg-type]

    def test_empty_composition_is_not_an_error(self):
        composed = compose_prompt_segments([])
        assert composed.text == ""
        assert composed.manifest == ()
        assert composed.manifest_as_dicts() == []


# ---------------------------------------------------------------------------
# 10: the documented rank scale, pinned against silent renumbering
# ---------------------------------------------------------------------------


class TestSegmentStabilityRankScale:
    def test_members_and_values_are_exactly_the_documented_scale(self):
        assert [(member.name, member.value) for member in SegmentStabilityRank] == [
            ("SYSTEM", 0),
            ("CONVENTIONS", 1),
            ("DOSSIER", 2),
            ("JOB_CONTEXT", 3),
            ("TASK", 4),
            ("STEERING", 5),
        ]

    def test_ranks_compare_as_integers(self):
        assert SegmentStabilityRank.SYSTEM < SegmentStabilityRank.CONVENTIONS
        assert SegmentStabilityRank.TASK < SegmentStabilityRank.STEERING
        assert int(SegmentStabilityRank.STEERING) == 5


# ---------------------------------------------------------------------------
# Architecture guard: no tokenizer dependency sneaks in behind the estimate.
# ---------------------------------------------------------------------------


class TestPromptSegmentArchitectureGuards:
    def test_no_tokenizer_or_provider_imports(self):
        from pathlib import Path

        src = (Path(__file__).resolve().parents[2] / "packages" / "orchestration"
               / "prompt_segments.py").read_text(encoding="utf-8")
        for bad in ("import tiktoken", "import requests", "import httpx", "import openai",
                    "import anthropic", "import subprocess", "import socket"):
            assert bad not in src, bad
