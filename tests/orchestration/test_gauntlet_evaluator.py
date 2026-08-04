"""F075 T001 — the pass definition, proven falsifiable.

A pass definition nothing can fail is not a pass definition, so the shape of
this file is deliberate: one flawless baseline, then one test per criterion in
:data:`PASS_CRITERIA` that flips exactly that criterion and asserts the run
stops being flawless. That is the acceptance bar of T1_F075.md.

The era finding classes (R-0141/R-0143/R-0144/R-0145/R-0146/R-0147/R-0148) and
the four harness-failure injection classes get classification-mapping tests:
the evaluator must be able to NAME them, not merely reject the run.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from packages.orchestration.era_integrity import (
    DEFECT_CORRUPTED_AUTHORED_TEXT,
    DEFECT_DROPPED_FLAG,
    DEFECT_FINDING_CLASSES,
    DEFECT_INCOMPLETE_ACCOUNTING,
    DEFECT_SELF_AUTHORED_VERDICT,
    DEFECT_SELF_CONSISTENCY_PROOF,
)
from packages.orchestration.failure_postmortem import FailureClass
from packages.orchestration.gauntlet_evaluator import (
    ACCEPTED_DISPOSITIONS,
    CRITERION_DATA_ROOT_UNTOUCHED,
    CRITERION_DOD_BLOCKING_GREEN,
    CRITERION_EVIDENCE_WELL_FORMED,
    CRITERION_INJECTIONS_DEGRADED,
    CRITERION_NO_ERA_DEFECTS,
    CRITERION_NO_OPEN_DECISIONS,
    CRITERION_NO_UNKNOWN_POSTMORTEMS,
    CRITERION_START_COMMAND_ONLY,
    CRITERION_TERMINAL_GREEN,
    DISPOSITION_CORRUPTED_ARTIFACT_ACCEPTED,
    DISPOSITION_SILENT_SUCCESS,
    FAILURE_DATA_ROOT_POLLUTED,
    FAILURE_DOD_BLOCKING_RED,
    FAILURE_ERA_DEFECT,
    FAILURE_INJECTION_NOT_DEGRADED,
    FAILURE_KINDS,
    FAILURE_MALFORMED_EVIDENCE,
    FAILURE_OPEN_DECISION,
    FAILURE_OPERATOR_INTERVENTION,
    FAILURE_TERMINAL_NOT_GREEN,
    FAILURE_UNKNOWN_POSTMORTEM,
    INJECTION_CLASSES,
    INJECTION_HARNESS_DEATH_MID_DISPATCH,
    INJECTION_HARNESS_DEATH_MID_WRITE,
    INJECTION_PROVIDER_API_ERROR_MID_MOVE,
    INJECTION_TRUNCATED_MODEL_RESPONSE,
    PASS_CRITERIA,
    REJECTED_DISPOSITIONS,
    evaluate_evidence_dir,
    evaluate_run,
)
from packages.orchestration.gauntlet_evidence import load_run
from packages.orchestration.orchestrator_loop import (
    TERMINAL_ITERATION_LIMIT,
    TERMINAL_STOPPED,
    TERMINAL_WAITING,
)
from tests.orchestration.test_gauntlet_evidence import (
    FLAWLESS_BODY,
    RELEASED_GATE,
    write_run,
)


def verdict_for(tmp_path: Path, **overrides) -> object:
    """One run built from the flawless baseline with fields overridden.

    ``gate`` is popped separately: it is a sibling file, not a ``run.json`` key.
    """
    gate = overrides.pop("gate", RELEASED_GATE)
    body = dict(FLAWLESS_BODY, **overrides)
    return evaluate_run(load_run(write_run(tmp_path, "run-01", body, gate)))


# ---------------------------------------------------------------------------
# The baseline every falsification test is measured against
# ---------------------------------------------------------------------------

def test_the_baseline_run_is_flawless(tmp_path: Path) -> None:
    v = verdict_for(tmp_path)
    assert v.flawless is True
    assert v.failures == ()
    assert all(v.criteria[name] for name in PASS_CRITERIA)


def test_every_criterion_appears_in_the_verdict(tmp_path: Path) -> None:
    v = verdict_for(tmp_path)
    assert set(v.criteria) == set(PASS_CRITERIA)
    assert list(v.to_json()["criteria"]) == list(PASS_CRITERIA)


# ---------------------------------------------------------------------------
# One flip per criterion — the falsifiability bar
# ---------------------------------------------------------------------------

def test_an_operator_command_falsifies_start_command_only(tmp_path: Path) -> None:
    v = verdict_for(tmp_path, operator_interventions=["remedy job resume 4f1c"])
    assert v.flawless is False
    assert v.criteria[CRITERION_START_COMMAND_ONLY] is False
    assert [f.kind for f in v.failures] == [FAILURE_OPERATOR_INTERVENTION]
    assert "remedy job resume 4f1c" in v.failures[0].detail
    # Only the flipped criterion moves.
    assert all(v.criteria[n] for n in PASS_CRITERIA if n != CRITERION_START_COMMAND_ONLY)


@pytest.mark.parametrize("terminal", [
    TERMINAL_ITERATION_LIMIT, TERMINAL_WAITING, TERMINAL_STOPPED, "aborted", "",
])
def test_any_non_achieved_terminal_falsifies_terminal_green(
        tmp_path: Path, terminal: str) -> None:
    v = verdict_for(tmp_path / terminal.replace("_", "-"), terminal_status=terminal)
    assert v.flawless is False
    assert v.criteria[CRITERION_TERMINAL_GREEN] is False
    assert [f.kind for f in v.failures] == [FAILURE_TERMINAL_NOT_GREEN]


def test_a_blocking_red_dod_check_falsifies_dod_blocking_green(tmp_path: Path) -> None:
    held = dict(RELEASED_GATE, released=False, blocking_red=["tests"])
    v = verdict_for(tmp_path, gate=held)
    assert v.flawless is False
    assert v.criteria[CRITERION_DOD_BLOCKING_GREEN] is False
    assert [f.kind for f in v.failures] == [FAILURE_DOD_BLOCKING_RED]
    # The blocker line has one author: dod_gate.
    assert v.failures[0].detail == "dod_blocking_red:tests"


def test_a_gate_that_could_not_evaluate_falsifies_dod_blocking_green(
        tmp_path: Path) -> None:
    held = dict(RELEASED_GATE, released=False, error="no_runner", blocking_red=[])
    v = verdict_for(tmp_path, gate=held)
    assert v.criteria[CRITERION_DOD_BLOCKING_GREEN] is False
    assert v.failures[0].detail == "dod_blocking_red:no_runner"


def test_a_gate_verdict_at_war_with_itself_is_reported_as_such(tmp_path: Path) -> None:
    """``released`` with an error is a shape the gate never writes: edited or
    truncated evidence, reported rather than resolved in either direction."""
    contradictory = dict(RELEASED_GATE, released=True, error="no_runner")
    v = verdict_for(tmp_path, gate=contradictory)
    assert v.criteria[CRITERION_DOD_BLOCKING_GREEN] is False
    assert "contradicts itself" in v.failures[0].detail


def test_a_run_that_never_reached_the_gate_is_not_a_silent_pass(tmp_path: Path) -> None:
    v = verdict_for(tmp_path, gate=None)
    assert v.flawless is False
    assert v.criteria[CRITERION_DOD_BLOCKING_GREEN] is False
    assert "never produced a verdict" in v.failures[0].detail


def test_an_unknown_postmortem_falsifies_no_unknown_postmortems(tmp_path: Path) -> None:
    v = verdict_for(tmp_path, postmortems=[
        {"scope": "task", "failure_class": FailureClass.UNKNOWN.value},
    ])
    assert v.flawless is False
    assert v.criteria[CRITERION_NO_UNKNOWN_POSTMORTEMS] is False
    assert [f.kind for f in v.failures] == [FAILURE_UNKNOWN_POSTMORTEM]


def test_a_postmortem_without_a_class_is_treated_as_unknown(tmp_path: Path) -> None:
    v = verdict_for(tmp_path, postmortems=[{"scope": "call"}])
    assert v.criteria[CRITERION_NO_UNKNOWN_POSTMORTEMS] is False
    assert "(absent)" in v.failures[0].detail


def test_a_classified_postmortem_does_not_falsify_the_run(tmp_path: Path) -> None:
    """A failure that HAPPENED and was understood is not a flaw in the run —
    surviving the flaky world is part of flawless (T1_F075.md, A9)."""
    v = verdict_for(tmp_path, postmortems=[
        {"scope": "task", "failure_class": FailureClass.TEST_FAILED.value},
    ])
    assert v.flawless is True


def test_an_open_decision_falsifies_no_open_decisions(tmp_path: Path) -> None:
    v = verdict_for(tmp_path, open_decisions=[
        {"decision_id": "td:1", "question": "which database?"},
    ])
    assert v.flawless is False
    assert v.criteria[CRITERION_NO_OPEN_DECISIONS] is False
    assert [f.kind for f in v.failures] == [FAILURE_OPEN_DECISION]
    assert "which database?" in v.failures[0].detail


def test_a_changed_data_root_falsifies_host_data_root_untouched(tmp_path: Path) -> None:
    v = verdict_for(tmp_path, data_root_hash_after="sha256:bbbb")
    assert v.flawless is False
    assert v.criteria[CRITERION_DATA_ROOT_UNTOUCHED] is False
    assert [f.kind for f in v.failures] == [FAILURE_DATA_ROOT_POLLUTED]
    assert "sha256:aaaa -> sha256:bbbb" in v.failures[0].detail


def test_an_unhashed_data_root_falsifies_host_data_root_untouched(tmp_path: Path) -> None:
    """Not measuring is not the same as not polluting, and never passes as it."""
    v = verdict_for(tmp_path, data_root_hash_before="", data_root_hash_after="")
    assert v.criteria[CRITERION_DATA_ROOT_UNTOUCHED] is False
    assert "was not hashed" in v.failures[0].detail


def test_an_era_defect_falsifies_no_era_defect_classes(tmp_path: Path) -> None:
    v = verdict_for(tmp_path, era_defects=[
        {"kind": DEFECT_SELF_AUTHORED_VERDICT, "detail": "verdict authored by the worker"},
    ])
    assert v.flawless is False
    assert v.criteria[CRITERION_NO_ERA_DEFECTS] is False
    assert [f.kind for f in v.failures] == [FAILURE_ERA_DEFECT]
    assert v.failures[0].finding_class == "R-0144"


def test_an_injection_that_vanished_falsifies_injections_degraded(tmp_path: Path) -> None:
    v = verdict_for(tmp_path, injections=[
        {"class": INJECTION_TRUNCATED_MODEL_RESPONSE,
         "disposition": DISPOSITION_SILENT_SUCCESS,
         "detail": "the truncated move was accepted as complete"},
    ])
    assert v.flawless is False
    assert v.criteria[CRITERION_INJECTIONS_DEGRADED] is False
    assert [f.kind for f in v.failures] == [FAILURE_INJECTION_NOT_DEGRADED]
    assert v.failures[0].injection_class == INJECTION_TRUNCATED_MODEL_RESPONSE


def test_unreadable_evidence_falsifies_evidence_well_formed(tmp_path: Path) -> None:
    v = evaluate_run(load_run(write_run(tmp_path, "run-01", "{ not json")))
    assert v.flawless is False
    assert v.criteria[CRITERION_EVIDENCE_WELL_FORMED] is False
    # Nothing was proven, so nothing is reported green.
    assert not any(v.criteria.values())
    assert [f.kind for f in v.failures] == [FAILURE_MALFORMED_EVIDENCE]


# ---------------------------------------------------------------------------
# Classification — the evaluator must NAME what it rejects
# ---------------------------------------------------------------------------

ERA_KINDS = (
    DEFECT_INCOMPLETE_ACCOUNTING,
    DEFECT_SELF_AUTHORED_VERDICT,
    DEFECT_DROPPED_FLAG,
    DEFECT_SELF_CONSISTENCY_PROOF,
    DEFECT_CORRUPTED_AUTHORED_TEXT,
)


@pytest.mark.parametrize("kind", ERA_KINDS)
def test_every_era_class_is_named_with_its_finding_ids(tmp_path: Path, kind: str) -> None:
    v = verdict_for(tmp_path / kind, era_defects=[{"kind": kind, "detail": "d"}])
    assert v.flawless is False
    assert v.failures[0].finding_class == DEFECT_FINDING_CLASSES[kind]
    assert kind in v.failures[0].detail


def test_the_era_classes_cover_every_finding_id_the_operator_named() -> None:
    """R-0141/R-0143/R-0144/R-0145/R-0146/R-0147/R-0148, all of them."""
    named = {part for ids in DEFECT_FINDING_CLASSES.values() for part in ids.split("/")}
    assert named == {"R-0141", "R-0143", "R-0144", "R-0145",
                     "R-0146", "R-0147", "R-0148"}


def test_the_four_injection_classes_are_the_operator_addition() -> None:
    assert set(INJECTION_CLASSES) == {
        INJECTION_PROVIDER_API_ERROR_MID_MOVE,
        INJECTION_TRUNCATED_MODEL_RESPONSE,
        INJECTION_HARNESS_DEATH_MID_DISPATCH,
        INJECTION_HARNESS_DEATH_MID_WRITE,
    }


@pytest.mark.parametrize("injection", INJECTION_CLASSES)
@pytest.mark.parametrize("disposition", ACCEPTED_DISPOSITIONS)
def test_a_degraded_injection_keeps_the_run_eligible(
        tmp_path: Path, injection: str, disposition: str) -> None:
    v = verdict_for(tmp_path / f"{injection}-{disposition}",
                    injections=[{"class": injection, "disposition": disposition,
                                 "detail": "degraded"}])
    assert v.flawless is True


@pytest.mark.parametrize("injection", INJECTION_CLASSES)
@pytest.mark.parametrize("disposition", REJECTED_DISPOSITIONS)
def test_a_mishandled_injection_names_class_and_disposition(
        tmp_path: Path, injection: str, disposition: str) -> None:
    v = verdict_for(tmp_path / f"{injection}-{disposition}",
                    injections=[{"class": injection, "disposition": disposition,
                                 "detail": "mishandled"}])
    assert v.flawless is False
    assert v.failures[0].injection_class == injection
    assert disposition in v.failures[0].detail
    assert "a named mishandling" in v.failures[0].detail
    # The harness's own sentence survives into the report.
    assert "recorded: mishandled" in v.failures[0].detail


def test_an_unclassified_disposition_is_rejected_not_assumed_fine(tmp_path: Path) -> None:
    v = verdict_for(tmp_path, injections=[
        {"class": INJECTION_HARNESS_DEATH_MID_WRITE, "disposition": "handled somehow"},
    ])
    assert v.flawless is False
    assert "an unclassified disposition" in v.failures[0].detail


def test_an_unknown_injection_class_is_refused(tmp_path: Path) -> None:
    v = verdict_for(tmp_path, injections=[
        {"class": "cosmic_ray", "disposition": ACCEPTED_DISPOSITIONS[0]},
    ])
    assert v.flawless is False
    assert "unknown injection class cosmic_ray" in v.failures[0].detail


def test_corrupted_artifact_accepted_is_its_own_named_disposition(tmp_path: Path) -> None:
    v = verdict_for(tmp_path, injections=[
        {"class": INJECTION_HARNESS_DEATH_MID_WRITE,
         "disposition": DISPOSITION_CORRUPTED_ARTIFACT_ACCEPTED},
    ])
    assert v.flawless is False
    assert DISPOSITION_CORRUPTED_ARTIFACT_ACCEPTED in v.failures[0].detail


def test_every_produced_failure_kind_is_declared(tmp_path: Path) -> None:
    v = verdict_for(
        tmp_path,
        operator_interventions=["remedy job resume"],
        terminal_status=TERMINAL_STOPPED,
        gate=dict(RELEASED_GATE, released=False, blocking_red=["tests"]),
        postmortems=[{"scope": "task", "failure_class": FailureClass.UNKNOWN.value}],
        open_decisions=[{"decision_id": "td:1"}],
        data_root_hash_after="sha256:bbbb",
        era_defects=[{"kind": DEFECT_DROPPED_FLAG, "detail": "d"}],
        injections=[{"class": INJECTION_HARNESS_DEATH_MID_DISPATCH,
                     "disposition": DISPOSITION_SILENT_SUCCESS}],
    )
    assert v.flawless is False
    assert not any(v.criteria[n] for n in PASS_CRITERIA
                   if n != CRITERION_EVIDENCE_WELL_FORMED)
    assert {f.kind for f in v.failures} <= set(FAILURE_KINDS)
    assert len({f.kind for f in v.failures}) == len(PASS_CRITERIA) - 1


# ---------------------------------------------------------------------------
# The campaign verdict
# ---------------------------------------------------------------------------

def build_set(root: Path, count: int, *, spoil: int | None = None) -> Path:
    evidence = root / "evidence"
    for index in range(1, count + 1):
        body = dict(FLAWLESS_BODY, order_id=f"g{index:02d}")
        if index == spoil:
            body["terminal_status"] = TERMINAL_ITERATION_LIMIT
        write_run(evidence, f"run-{index:02d}", body, RELEASED_GATE)
    return evidence


def test_ten_flawless_runs_pass(tmp_path: Path) -> None:
    verdict = evaluate_evidence_dir(build_set(tmp_path, 10))
    assert verdict.passed is True
    assert verdict.flawless_count == 10
    assert [r.order_id for r in verdict.runs] == [f"g{i:02d}" for i in range(1, 11)]


def test_one_bad_run_out_of_ten_fails_the_campaign(tmp_path: Path) -> None:
    verdict = evaluate_evidence_dir(build_set(tmp_path, 10, spoil=7))
    assert verdict.passed is False
    assert verdict.flawless_count == 9
    assert verdict.failure_kinds() == (FAILURE_TERMINAL_NOT_GREEN,)


def test_an_empty_evidence_dir_does_not_pass_vacuously(tmp_path: Path) -> None:
    verdict = evaluate_evidence_dir(tmp_path / "empty")
    assert verdict.runs == ()
    assert verdict.passed is False
    assert verdict.flawless_count == 0


def test_only_selects_one_run_by_canonical_index(tmp_path: Path) -> None:
    verdict = evaluate_evidence_dir(build_set(tmp_path, 10, spoil=3), only=3)
    assert [r.order_id for r in verdict.runs] == ["g03"]
    assert verdict.passed is False


def test_only_outside_the_range_is_refused(tmp_path: Path) -> None:
    evidence = build_set(tmp_path, 10)
    for bad in (0, 11, -1):
        with pytest.raises(IndexError):
            evaluate_evidence_dir(evidence, only=bad)


def test_verdict_json_is_serialisable_and_names_the_failures(tmp_path: Path) -> None:
    verdict = evaluate_evidence_dir(build_set(tmp_path, 2, spoil=2))
    payload = json.dumps([r.to_json() for r in verdict.runs], sort_keys=True)
    assert FAILURE_TERMINAL_NOT_GREEN in payload
    assert json.loads(payload)[0]["flawless"] is True
