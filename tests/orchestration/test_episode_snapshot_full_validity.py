"""F8 (round 10) — ONE exact JobInput validator, used everywhere.

`is_ok()` and the strict raw decoder used to be two different rule sets pretending to be one.
A snapshot with empty required hashes and an empty isolation mode said `is_ok() == True` — and
then failed its own strict decode the moment it was read back off disk. A record cannot be valid
on the way out and invalid on the way in; that is not validation, it is a coin flip.

There is now one rule set: `validate_job_input_definition` returns the exact problems, the raw
decoder applies it and raises, and `is_ok()` calls the same function. This suite pins their
EQUIVALENCE, so a future edit cannot let them drift apart again.
"""
from __future__ import annotations

import copy
import dataclasses

import pytest

import tests.orchestration.test_run_manifest as T
from packages.orchestration import manifest_schema as _S
from packages.orchestration.run_manifest import (
    JOB_INPUT_EXECUTION_FIELDS,
    JOB_INPUT_TOP_FIELDS,
    decode_job_input_definition_v1,
    validate_job_input_definition,
)


def _ji(**over):
    d = copy.deepcopy(T._job_input())
    d.update(over)
    return d


def _wrapper(job_input):
    return T._wrap(dataclasses.replace(T._snap(), job_input=job_input), episode_id="ep1")


def _decoder_rejects(job_input) -> bool:
    try:
        decode_job_input_definition_v1(job_input)
        return False
    except _S.SchemaError:
        return True


#: Every mutation here must be rejected by BOTH the typed predicate and the raw decoder.
_BROKEN = {
    "empty job_title_sha256": _ji(job_title_sha256=""),
    "empty job_file_sha256": _ji(job_file_sha256=""),
    "empty isolation_mode": _ji(isolation_mode=""),
    "malformed job_file_sha256": _ji(job_file_sha256="nope"),
    "unsupported isolation_mode": _ji(isolation_mode="teleport"),
    "unsupported version": _ji(job_input_v=2),
    "tasks not a list": _ji(tasks={}),
    "unknown top field": _ji(SMUGGLED="x"),
}


def _without_execution_field(field):
    d = _ji()
    d["execution"].pop(field)
    return d


for _f in sorted(JOB_INPUT_EXECUTION_FIELDS):
    _BROKEN[f"missing execution.{_f}"] = _without_execution_field(_f)

for _f in sorted(JOB_INPUT_TOP_FIELDS):
    _d = _ji()
    _d.pop(_f)
    _BROKEN[f"missing {_f}"] = _d


# --------------------------------------------------------------------------- equivalence


class TestTheTypedPredicateAndTheRawDecoderAgree:
    @pytest.mark.parametrize("case", sorted(_BROKEN))
    def test_a_broken_definition_is_rejected_by_both(self, case):
        job_input = _BROKEN[case]
        assert validate_job_input_definition(job_input), f"{case}: the validator accepted it"
        assert _decoder_rejects(job_input), f"{case}: the strict decoder accepted it"
        assert not _wrapper(job_input).is_ok(), f"{case}: is_ok() accepted it"

    def test_a_complete_definition_is_accepted_by_both(self):
        job_input = _ji()
        assert validate_job_input_definition(job_input) == []
        decode_job_input_definition_v1(job_input)
        assert _wrapper(job_input).is_ok()

    def test_the_decoder_is_literally_the_validator(self):
        """The decoder must not carry a second copy of the rules — it applies THE rule set."""
        import inspect
        src = inspect.getsource(decode_job_input_definition_v1)
        assert "validate_job_input_definition(raw)" in src


# --------------------------------------------------------------------------- the finding


class TestIsOkRejectsWhatTheDecoderWouldReject:
    def test_the_reproduced_case(self):
        """THE finding: empty required hashes + empty isolation mode → is_ok() was True."""
        job_input = _ji(job_title_sha256="", job_file_sha256="", isolation_mode="")
        w = _wrapper(job_input)
        assert not w.is_ok()
        assert _decoder_rejects(job_input)

    def test_a_missing_execution_field_makes_is_ok_false(self):
        assert not _wrapper(_without_execution_field("builder_model")).is_ok()

    def test_an_empty_execution_block_makes_is_ok_false(self):
        assert not _wrapper(_ji(execution={})).is_ok()

    def test_a_snapshot_with_a_leaked_secret_test_command_is_not_ok(self):
        d = _ji()
        d["execution"]["test_command"]["redacted"] = "TOKEN=ghp_averyrealtokenvalue pytest"
        assert not _wrapper(d).is_ok()

    def test_the_wrapper_only_check_is_still_separate(self):
        """`wrapper_shape_is_valid()` deliberately says nothing about the payload — it must not
        quietly become the trust decision."""
        w = _wrapper(_ji(job_file_sha256=""))
        assert w.wrapper_shape_is_valid()
        assert not w.is_ok()


# --------------------------------------------------------------------------- capture blocks


class TestCaptureAndFinalizationUseTheSameRules:
    def test_finalization_refuses_a_snapshot_that_is_not_ok(self):
        from packages.orchestration.run_manifest import ManifestError, build_run_manifest

        class _Job:
            job_id = "j"
            tasks: list = []
            execution_config = None

        with pytest.raises(ManifestError):
            build_run_manifest(_Job(), status="completed", episode_id="ep1",
                               created_at="2026-07-16T00:00:00+00:00",
                               episode_snapshot=_wrapper(_ji(job_file_sha256="")))

    def test_a_valid_definition_round_trips_through_the_decoder_unchanged(self):
        job_input = _ji()
        assert decode_job_input_definition_v1(job_input) == job_input
