"""F308, DECISION F308 D2 — the split arithmetic, the strict decoder and the validator that
`packages/orchestration/run_task_list.py` carries for a task the run split over its class cap.

T001/T002 moved the F7 check and the manifest's acceptance of a recorded split into this module;
this file proves the pieces `test_run_manifest_call_task_binding.py` and
`test_job_task_runner.py` exercise end to end through the real split path.
"""
from __future__ import annotations

import dataclasses

import pytest

import tests.orchestration.test_run_manifest as T
from packages.orchestration import manifest_schema as _S
from packages.orchestration.run_manifest import decode_run_manifest_v1
from packages.orchestration.run_task_list import (
    decode_task_splits_v1,
    task_ids_after_splits,
    task_split_problems,
)


def _split(parent="T001", parts=("T001a", "T001b"), episode="ep1", reason="r"):
    return {"parent_task_id": parent, "part_task_ids": list(parts), "episode_id": episode,
            "reason": reason}


# --------------------------------------------------------------------------- task_ids_after_splits


class TestTaskIdsAfterSplits:
    def test_a_single_split_inserts_its_parts_after_the_parent(self):
        after, problems = task_ids_after_splits(["T001"], [_split()])
        assert after == ["T001", "T001a", "T001b"]
        assert problems == []

    def test_two_splits_apply_in_order(self):
        after, problems = task_ids_after_splits(
            ["T001", "T002"],
            [_split("T001", ["T001a"]), _split("T002", ["T002a"])])
        assert after == ["T001", "T001a", "T002", "T002a"]
        assert problems == []

    def test_a_parent_not_in_the_list_is_a_problem(self):
        after, problems = task_ids_after_splits(["T001"], [_split("T999", ["T999a"])])
        assert after == ["T001"]
        assert problems and "exactly once" in problems[0]

    def test_a_parent_declared_twice_is_a_problem(self):
        after, problems = task_ids_after_splits(["T001", "T001"], [_split("T001", ["T001a"])])
        assert problems and "exactly once" in problems[0]

    def test_a_parent_already_split_is_a_problem(self):
        after, problems = task_ids_after_splits(
            ["T001"], [_split("T001", ["T001a"]), _split("T001", ["T001c"])])
        assert any("already split" in p for p in problems), problems

    def test_empty_parts_are_a_problem(self):
        after, problems = task_ids_after_splits(["T001"], [_split("T001", [])])
        assert any("empty" in p for p in problems), problems

    def test_repeated_parts_are_a_problem(self):
        after, problems = task_ids_after_splits(
            ["T001"], [_split("T001", ["T001a", "T001a"])])
        assert any("repeat" in p for p in problems), problems

    def test_parts_already_in_the_list_are_a_problem(self):
        after, problems = task_ids_after_splits(
            ["T001", "T002"], [_split("T001", ["T002"])])
        assert any("already in the task list" in p for p in problems), problems

    def test_a_malformed_split_is_a_problem(self):
        after, problems = task_ids_after_splits(["T001"], [{"parent_task_id": "T001"}])
        assert after == ["T001"]
        assert any("not a map" in p for p in problems), problems


# --------------------------------------------------------------------------- decode_task_splits_v1


class TestDecodeTaskSplitsV1:
    def test_a_good_list_decodes(self):
        out = decode_task_splits_v1([_split()])
        assert out == (_split(),)

    def test_a_missing_key_raises(self):
        bad = _split()
        del bad["reason"]
        with pytest.raises(_S.SchemaError):
            decode_task_splits_v1([bad])

    def test_an_extra_key_raises(self):
        bad = _split()
        bad["extra"] = "x"
        with pytest.raises(_S.SchemaError):
            decode_task_splits_v1([bad])

    def test_a_wrong_type_raises(self):
        bad = _split()
        bad["part_task_ids"] = "T001a"
        with pytest.raises(_S.SchemaError):
            decode_task_splits_v1([bad])


# --------------------------------------------------------------------------- manifest encoding


class TestManifestEncodingOfTaskSplits:
    def test_a_manifest_without_splits_encodes_with_no_task_splits_key(self):
        m = T._mk(episode_id="ep1")
        assert "task_splits" not in m.to_json()

    def test_a_manifest_with_a_split_round_trips_through_the_strict_decoder(self):
        """`write_run_manifest`/`load_latest_manifest_verified` need a fully valid split episode
        — the parent's own `skipped`/`split` call_expectation, matching the declared ids after
        the split — which the shared `_mk` fixture (built for a plain executed task) cannot
        produce without reaching past what DECISION F308 D2 touches. The round trip is proved
        instead through the strict decoder every other boundary already uses, as the block's
        fallback names (said in the handback)."""
        m = dataclasses.replace(T._mk(episode_id="ep1"), task_splits=(_split(episode="ep1"),))
        decoded = decode_run_manifest_v1(m.canonical_bytes())
        assert decoded.task_splits == m.task_splits


# --------------------------------------------------------------------------- task_split_problems


class TestTaskSplitProblems:
    def test_an_episode_mismatch_is_a_problem(self):
        m = dataclasses.replace(
            T._mk(episode_id="ep1"),
            task_splits=(_split(parts=["T001a"], episode="ep2"),))
        probs = task_split_problems(m)
        assert any("not this manifest's episode" in p for p in probs), probs

    def test_a_parent_recorded_with_another_status_is_a_problem(self):
        """`T._mk`'s one call makes T001 `executed`/`applied_to_job_workspace` — never the
        `skipped`/`split` a split's parent must carry."""
        m = dataclasses.replace(
            T._mk(episode_id="ep1"),
            task_splits=(_split(parts=["T001a"], episode="ep1"),))
        probs = task_split_problems(m)
        assert any("not skipped/split" in p for p in probs), probs
