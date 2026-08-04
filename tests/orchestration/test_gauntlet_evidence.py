"""F075 T001 — reading recorded gauntlet evidence.

The evaluator is only as trustworthy as its reader. Two properties are proven
here and nowhere else:

  * **Reading never raises.** Missing, malformed, non-object and wrong-version
    evidence all come back as a ``RunEvidence`` carrying ``load_error``. A
    gauntlet that threw on unreadable evidence would lose the run instead of
    failing it, and a lost run is a run that silently does not count.
  * **The run order is a property of the bytes on disk.** Directory-name sort,
    so the same evidence always produces the same matrix.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from packages.orchestration.gauntlet_evidence import (
    DOD_RESULT_FILENAME,
    GAUNTLET_RUN_VERSION,
    RUN_FILENAME,
    load_run,
    run_dirs,
)

#: The recorded evidence the dry-run proof runs against, and the golden matrix
#: rendered from it. Shared with the evaluator and matrix tests so there is one
#: spelling of these paths.
FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures" / "gauntlet"
RECORDED_DIR = FIXTURE_ROOT / "recorded"
GOLDEN_DIR = FIXTURE_ROOT / "golden"

FLAWLESS_BODY: dict = {
    "gauntlet_run_version": GAUNTLET_RUN_VERSION,
    "order_id": "g01-pure-code-change",
    "kind": "pure_code_change",
    "terminal_status": "achieved",
    "wall_seconds": 612.5,
    "tokens": {"in": 120_000, "out": 30_000},
    "operator_interventions": [],
    "data_root_hash_before": "sha256:aaaa",
    "data_root_hash_after": "sha256:aaaa",
    "postmortems": [],
    "open_decisions": [],
    "era_defects": [],
    "injections": [],
    "evidence_links": {"ledger": "ledger.jsonl"},
}

RELEASED_GATE: dict = {
    "released": True, "blocking_red": [], "reported_red": [], "error": "",
    "checks": [{"check_id": "tests", "kind": "command", "source": "dod",
                "blocking": True, "status": "green", "reason": "",
                "command": "pytest", "exit_code": 0, "duration_ms": 1200,
                "output_tail": ""}],
}


def write_run(root: Path, name: str, body: dict | str,
              gate: dict | str | None = None) -> Path:
    """One run directory. ``body``/``gate`` as a str is written raw — that is
    how malformed evidence gets into a test without a mock."""
    run_dir = root / name
    run_dir.mkdir(parents=True)
    text = body if isinstance(body, str) else json.dumps(body)
    (run_dir / RUN_FILENAME).write_text(text, encoding="utf-8")
    if gate is not None:
        gate_text = gate if isinstance(gate, str) else json.dumps(gate)
        (run_dir / DOD_RESULT_FILENAME).write_text(gate_text, encoding="utf-8")
    return run_dir


def test_loads_every_recorded_field(tmp_path: Path) -> None:
    run_dir = write_run(tmp_path, "run-01", FLAWLESS_BODY, RELEASED_GATE)
    ev = load_run(run_dir)
    assert ev.load_error == ""
    assert ev.run_dir == "run-01"
    assert ev.order_id == "g01-pure-code-change"
    assert ev.kind == "pure_code_change"
    assert ev.terminal_status == "achieved"
    assert ev.wall_seconds == 612.5
    assert (ev.tokens_in, ev.tokens_out) == (120_000, 30_000)
    assert ev.data_root_hash_before == ev.data_root_hash_after == "sha256:aaaa"
    assert ev.evidence_links == {"ledger": "ledger.jsonl"}
    assert ev.dod_result is not None and ev.dod_result["released"] is True


def test_absent_gate_result_is_legal_and_stays_none(tmp_path: Path) -> None:
    ev = load_run(write_run(tmp_path, "run-01", FLAWLESS_BODY))
    assert ev.load_error == ""
    assert ev.dod_result is None


def test_missing_run_file_is_a_load_error_not_an_exception(tmp_path: Path) -> None:
    empty = tmp_path / "run-01"
    empty.mkdir()
    ev = load_run(empty)
    assert RUN_FILENAME in ev.load_error
    assert ev.terminal_status == ""


def test_malformed_json_is_a_load_error(tmp_path: Path) -> None:
    ev = load_run(write_run(tmp_path, "run-01", "{ not json"))
    assert ev.load_error.startswith(f"unreadable {RUN_FILENAME}")


def test_non_object_run_file_is_a_load_error(tmp_path: Path) -> None:
    ev = load_run(write_run(tmp_path, "run-01", "[1, 2, 3]"))
    assert ev.load_error == f"{RUN_FILENAME} is not an object"


def test_unknown_version_is_refused_and_names_both_versions(tmp_path: Path) -> None:
    body = dict(FLAWLESS_BODY, gauntlet_run_version=GAUNTLET_RUN_VERSION + 1)
    ev = load_run(write_run(tmp_path, "run-01", body))
    assert "unsupported gauntlet_run_version" in ev.load_error
    assert str(GAUNTLET_RUN_VERSION) in ev.load_error
    # The order id survives so an unreadable run can still be named in the report.
    assert ev.order_id == "g01-pure-code-change"


def test_broken_gate_result_is_a_load_error(tmp_path: Path) -> None:
    ev = load_run(write_run(tmp_path, "run-01", FLAWLESS_BODY, "{ nope"))
    assert ev.load_error.startswith(f"unreadable {DOD_RESULT_FILENAME}")


def test_non_object_gate_result_is_a_load_error(tmp_path: Path) -> None:
    ev = load_run(write_run(tmp_path, "run-01", FLAWLESS_BODY, "[]"))
    assert ev.load_error == f"{DOD_RESULT_FILENAME} is not an object"


def test_wrong_typed_lists_degrade_to_empty_rather_than_raising(tmp_path: Path) -> None:
    body = dict(FLAWLESS_BODY, operator_interventions="remedy job resume",
                postmortems={"scope": "task"}, injections=None,
                evidence_links=["ledger.jsonl"])
    ev = load_run(write_run(tmp_path, "run-01", body))
    assert ev.load_error == ""
    assert ev.operator_interventions == ()
    assert ev.postmortems == ()
    assert ev.injections == ()
    assert ev.evidence_links == {}


def test_non_dict_list_members_are_dropped(tmp_path: Path) -> None:
    body = dict(FLAWLESS_BODY, postmortems=["oops", {"failure_class": "test_failed"}])
    ev = load_run(write_run(tmp_path, "run-01", body))
    assert ev.postmortems == ({"failure_class": "test_failed"},)


# --- R-0178: a malformed number is a load error, never a silent zero ---------
#
# The matrix is what a human reads before flipping multi-cycle defaults. A cost
# that renders as 0 because the value was unreadable understates exactly what
# that reader is weighing, so each field gets its own falsification.

@pytest.mark.parametrize("bad", ["a while", None, True, [], {}, "612.5"])
def test_a_non_numeric_wall_seconds_is_a_load_error(tmp_path: Path, bad) -> None:
    ev = load_run(write_run(tmp_path / repr(bad), "run-01",
                            dict(FLAWLESS_BODY, wall_seconds=bad)))
    assert ev.load_error == f"wall_seconds is not a number: {bad!r}"


@pytest.mark.parametrize("bad", ["many", None, False, ["1"]])
def test_a_non_numeric_tokens_in_is_a_load_error(tmp_path: Path, bad) -> None:
    body = dict(FLAWLESS_BODY, tokens={"in": bad, "out": 30_000})
    ev = load_run(write_run(tmp_path / repr(bad), "run-01", body))
    assert ev.load_error == f"tokens.in is not a number: {bad!r}"


@pytest.mark.parametrize("bad", ["many", None, True, {"n": 1}])
def test_a_non_numeric_tokens_out_is_a_load_error(tmp_path: Path, bad) -> None:
    body = dict(FLAWLESS_BODY, tokens={"in": 120_000, "out": bad})
    ev = load_run(write_run(tmp_path / repr(bad), "run-01", body))
    assert ev.load_error == f"tokens.out is not a number: {bad!r}"


def test_a_non_object_tokens_value_is_a_load_error(tmp_path: Path) -> None:
    ev = load_run(write_run(tmp_path, "run-01", dict(FLAWLESS_BODY, tokens="many")))
    assert ev.load_error == "tokens is not an object: 'many'"


def test_absent_numbers_still_default_because_absence_is_not_malformation(
        tmp_path: Path) -> None:
    """A run that recorded no token count says zero honestly."""
    body = {k: v for k, v in FLAWLESS_BODY.items()
            if k not in ("wall_seconds", "tokens")}
    ev = load_run(write_run(tmp_path, "run-01", body))
    assert ev.load_error == ""
    assert (ev.wall_seconds, ev.tokens_in, ev.tokens_out) == (0.0, 0, 0)


def test_a_half_recorded_tokens_object_defaults_only_the_absent_half(
        tmp_path: Path) -> None:
    ev = load_run(write_run(tmp_path, "run-01",
                            dict(FLAWLESS_BODY, tokens={"in": 42})))
    assert ev.load_error == ""
    assert (ev.tokens_in, ev.tokens_out) == (42, 0)


def test_an_integer_wall_seconds_is_accepted_as_a_number(tmp_path: Path) -> None:
    ev = load_run(write_run(tmp_path, "run-01", dict(FLAWLESS_BODY, wall_seconds=612)))
    assert ev.load_error == ""
    assert ev.wall_seconds == 612.0


def test_a_malformed_number_makes_the_run_not_flawless(tmp_path: Path) -> None:
    """The point of the finding: unreadable cost must cost the run its pass."""
    from packages.orchestration.gauntlet_evaluator import evaluate_run

    verdict = evaluate_run(load_run(write_run(
        tmp_path, "run-01", dict(FLAWLESS_BODY, wall_seconds="a while"), RELEASED_GATE)))
    assert verdict.flawless is False
    assert not any(verdict.criteria.values())


def test_run_order_is_the_sorted_directory_name(tmp_path: Path) -> None:
    for name in ("run-03", "run-01", "run-02"):
        write_run(tmp_path, name, dict(FLAWLESS_BODY, order_id=name))
    assert [p.name for p in run_dirs(tmp_path)] == ["run-01", "run-02", "run-03"]


def test_directories_without_a_run_file_are_not_runs(tmp_path: Path) -> None:
    write_run(tmp_path, "run-01", FLAWLESS_BODY)
    (tmp_path / "matrix").mkdir()
    (tmp_path / "matrix" / "matrix.md").write_text("# report", encoding="utf-8")
    assert [p.name for p in run_dirs(tmp_path)] == ["run-01"]


def test_missing_evidence_dir_is_no_runs_not_an_error(tmp_path: Path) -> None:
    assert run_dirs(tmp_path / "nowhere") == []
