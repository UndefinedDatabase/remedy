"""F036 T001 — the result tour's stop shape, anchor check and mechanical tour.

Every fixture below writes its on-disk records through the REAL writers
(`run_report.write_final_report`, `dod_gate.save_gate_result`, an
`evidence_index` record holding `workspace.diff`) so the module under test is
exercised the way the job terminal will actually call it — never through a
monkeypatched shortcut.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

import pytest

from packages.core.models import RunState
from packages.orchestration.data_paths import job_evidence_dir, job_evidence_index_dir
from packages.orchestration.dod_gate import GateResult, save_gate_result
from packages.orchestration.dod_runners import CheckEvidence
from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan
from packages.orchestration.result_tour import (
    MAX_TOUR_STOPS,
    TOUR_ANCHOR_KINDS,
    TOUR_BODY_MAX_CHARS,
    TOUR_SCHEMA,
    TourAnchorContext,
    build_fallback_tour,
    collect_tour_context,
    resolve_tour_stops,
    tour_problems,
)
from packages.orchestration.run_report import write_final_report

pytestmark = pytest.mark.integration


@pytest.fixture(autouse=True)
def _isolated_data_root(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))


# ---------------------------------------------------------------------------
# Fixture helpers — the real writers, never a monkeypatch of this module.
# ---------------------------------------------------------------------------


def _make_job(**overrides) -> JobPlan:
    defaults = dict(
        job_title="f036-tour-job",
        user_prompt="Build the result tour",
        tasks=[],
        metadata={"target_repo": "/tmp/repo"},
    )
    defaults.update(overrides)
    job = JobPlan(**defaults)
    save_job_plan(job)
    return job


def _write_diff(job_id: str, diff_text: str) -> Path:
    """Write `workspace.diff` for *job_id* and index it, so `build_diff_view` reads it."""
    ev_dir = job_evidence_dir(job_id)
    ev_dir.mkdir(parents=True, exist_ok=True)
    (ev_dir / "workspace.diff").write_text(diff_text, encoding="utf-8")
    idx_dir = job_evidence_index_dir()
    idx_dir.mkdir(parents=True, exist_ok=True)
    (idx_dir / f"{job_id}.json").write_text(
        json.dumps({"evidence_dir_local": str(ev_dir)}), encoding="utf-8")
    return ev_dir


def _one_file_diff(path: str, *, added_line: str = "+y = 2", deleted_line: str = "") -> str:
    """A minimal valid unified diff for one file: +1 added line, optionally 1 deleted."""
    body = [f"diff --git a/{path} b/{path}\n", f"--- a/{path}\n", f"+++ b/{path}\n"]
    if deleted_line:
        body += ["@@ -1,1 +1,1 @@\n", f"-{deleted_line}\n", f"{added_line}\n"]
    else:
        body += ["@@ -1,1 +1,2 @@\n", " x = 1\n", f"{added_line}\n"]
    return "".join(body)


def _multi_file_diff(paths: list[str]) -> str:
    return "".join(_one_file_diff(path) for path in paths)


def _make_check(check_id: str, *, command: str, status: str = "passed",
                blocking: bool = True) -> CheckEvidence:
    return CheckEvidence(
        check_id=check_id, kind="pytest", source="dod.json", blocking=blocking,
        status=status, reason="" if status == "passed" else "nonzero_exit",
        command=command, argv=tuple(command.split(" ")), cwd="", exit_code=0,
        duration_ms=5, output_tail="",
    )


def _write_gate(job_id: str, checks: list[CheckEvidence], *, released: bool) -> None:
    blocking_red = tuple(c.check_id for c in checks if c.blocking and c.status != "passed")
    reported_red = tuple(c.check_id for c in checks
                         if not c.blocking and c.status != "passed")
    save_gate_result(job_id, GateResult(
        released=released, evidence=tuple(checks),
        blocking_red=blocking_red, reported_red=reported_red))


# ---------------------------------------------------------------------------
# 1. a finished job, a report, a two-area diff and a passing gate: exactly the
#    five S6 stops, with exact titles, bodies and anchors.
# ---------------------------------------------------------------------------


def test_a_finished_job_with_report_diff_and_gate_yields_exactly_five_stops():
    job = _make_job(
        state=RunState.COMPLETED,
        tasks=[TaskEntry(title="write the module", status=RunState.COMPLETED),
               TaskEntry(title="write its tests", status=RunState.COMPLETED)],
        metadata={"target_repo": "/tmp/repo", "cycle_terminal_status": "all_green"},
    )
    diff_text = (_one_file_diff("packages/orchestration/foo.py")
                 + _one_file_diff("apps/ui/bar.ts", added_line="+new", deleted_line="old"))
    _write_diff(str(job.job_id), diff_text)
    write_final_report(job)
    _write_gate(str(job.job_id), [_make_check("c1", command="python3 -m pytest -q")],
               released=True)

    tour = build_fallback_tour(job)
    assert tour_problems(tour) == []
    assert [s["title"] for s in tour["stops"]] == [
        "How the run ended",
        "What changed in packages/",
        "What changed in apps/",
        "How to run it",
        "Definition of Done",
    ]
    assert tour["dropped"] == []

    how_ended, pkg_area, apps_area, how_to_run, dod = tour["stops"]
    assert how_ended == {
        "title": "How the run ended",
        "body": "State: completed; terminal status: all_green.",
        "anchor": {"kind": "evidence", "ref": "report.md"},
    }
    assert pkg_area == {
        "title": "What changed in packages/",
        "body": "1 changed file (+1 −0): packages/orchestration/foo.py (+1 −0)",
        "anchor": {"kind": "diff", "ref": "packages/orchestration/foo.py"},
    }
    assert apps_area == {
        "title": "What changed in apps/",
        "body": "1 changed file (+1 −1): apps/ui/bar.ts (+1 −1)",
        "anchor": {"kind": "diff", "ref": "apps/ui/bar.ts"},
    }
    assert how_to_run == {
        "title": "How to run it",
        "body": "The Definition of Done ran: python3 -m pytest -q",
        "anchor": {"kind": "command", "ref": "python3 -m pytest -q"},
    }
    assert dod == {
        "title": "Definition of Done",
        "body": "1 of 1 checks passed; the gate released the job.",
        "anchor": {"kind": "evidence", "ref": "dod_result.json"},
    }


# ---------------------------------------------------------------------------
# 2. no diff, no gate, no report: only stop (a), anchored to the first task.
# ---------------------------------------------------------------------------


def test_no_diff_no_gate_no_report_yields_only_the_first_stop_anchored_to_the_first_task():
    job = _make_job(
        state=RunState.RUNNING,
        tasks=[TaskEntry(title="do the work", status=RunState.RUNNING)],
    )
    tour = build_fallback_tour(job)
    assert tour_problems(tour) == []
    assert len(tour["stops"]) == 1
    assert tour["dropped"] == []
    assert tour["stops"][0]["anchor"] == {"kind": "node", "ref": str(job.tasks[0].task_id)}
    assert tour["stops"][0]["body"] == "State: running."


# ---------------------------------------------------------------------------
# 3. report.md present wins over the first task.
# ---------------------------------------------------------------------------


def test_report_md_present_wins_over_the_first_task():
    job = _make_job(
        state=RunState.COMPLETED,
        tasks=[TaskEntry(title="do the work", status=RunState.COMPLETED)],
        metadata={"target_repo": "/tmp/repo", "cycle_terminal_status": "all_green"},
    )
    write_final_report(job)
    tour = build_fallback_tour(job)
    assert tour["stops"][0]["anchor"] == {"kind": "evidence", "ref": "report.md"}


# ---------------------------------------------------------------------------
# 4. a directory named "cycles" in the evidence directory is not an evidence file.
# ---------------------------------------------------------------------------


def test_a_cycles_directory_is_not_an_evidence_file():
    job = _make_job(tasks=[TaskEntry(title="t")])
    ev_dir = job_evidence_dir(str(job.job_id))
    ev_dir.mkdir(parents=True, exist_ok=True)
    (ev_dir / "cycles").mkdir()
    (ev_dir / "report.md").write_text("# report\n", encoding="utf-8")

    context = collect_tour_context(job)
    assert context.evidence_files == ("report.md",)
    assert "cycles" not in context.evidence_files


# ---------------------------------------------------------------------------
# 5. two checks sharing a command give one run command; the FIRST recorded
#    command overall is the run stop's.
# ---------------------------------------------------------------------------


def test_duplicate_commands_dedupe_and_the_first_recorded_command_is_used():
    job = _make_job(tasks=[TaskEntry(title="t")])
    checks = [
        _make_check("c1", command="make lint"),
        _make_check("c2", command="python3 -m pytest -q"),
        _make_check("c3", command="python3 -m pytest -q"),
    ]
    _write_gate(str(job.job_id), checks, released=True)

    context = collect_tour_context(job)
    assert context.run_commands == ("make lint", "python3 -m pytest -q")

    tour = build_fallback_tour(job)
    run_stop = next(s for s in tour["stops"] if s["title"] == "How to run it")
    assert run_stop["body"] == "The Definition of Done ran: make lint"
    assert run_stop["anchor"] == {"kind": "command", "ref": "make lint"}


# ---------------------------------------------------------------------------
# 6. a held gate with a red check reads "held" and names the check.
# ---------------------------------------------------------------------------


def test_a_held_gate_with_a_red_check_reads_held_and_names_the_check():
    job = _make_job(tasks=[TaskEntry(title="t")])
    checks = [
        _make_check("c-ok", command="make lint", status="passed"),
        _make_check("c-bad", command="python3 -m pytest -q", status="failed"),
    ]
    _write_gate(str(job.job_id), checks, released=False)

    tour = build_fallback_tour(job)
    dod_stop = next(s for s in tour["stops"] if s["title"] == "Definition of Done")
    assert dod_stop["body"] == "1 of 2 checks passed; the gate held the job. Not passed: c-bad."


# ---------------------------------------------------------------------------
# 7. ten areas with a run command and a gate: exactly eight stops.
# ---------------------------------------------------------------------------


def test_ten_areas_with_run_command_and_gate_yield_exactly_eight_stops():
    job = _make_job(
        state=RunState.COMPLETED,
        tasks=[TaskEntry(title="t", status=RunState.COMPLETED)],
        metadata={"target_repo": "/tmp/repo", "cycle_terminal_status": "all_green"},
    )
    paths = [f"area{i}/file.py" for i in range(10)]
    _write_diff(str(job.job_id), _multi_file_diff(paths))
    _write_gate(str(job.job_id), [_make_check("c1", command="run-cmd")], released=True)

    tour = build_fallback_tour(job)
    assert tour_problems(tour) == []
    assert tour["dropped"] == []
    stops = tour["stops"]
    assert len(stops) == 8
    assert stops[5]["title"] == "What else changed"
    assert stops[5]["body"].startswith("6 more areas; ")
    assert stops[6]["title"] == "How to run it"
    assert stops[7]["title"] == "Definition of Done"


# ---------------------------------------------------------------------------
# 8. a mission longer than 400 characters is cut to exactly 400, ending "…",
#    and the stop is kept.
# ---------------------------------------------------------------------------


def test_a_long_mission_is_cut_to_exactly_the_body_bound_and_kept():
    job = _make_job(
        state=RunState.RUNNING,
        tasks=[TaskEntry(title="t", status=RunState.RUNNING)],
        mission="M" * 450,
    )
    tour = build_fallback_tour(job)
    assert tour["dropped"] == []
    assert len(tour["stops"]) == 1
    body = tour["stops"][0]["body"]
    assert len(body) == TOUR_BODY_MAX_CHARS
    assert body.endswith("…")


# ---------------------------------------------------------------------------
# 9. the resolver drops each of eight bad stops with its own reason, plus a
#    ninth otherwise-sound stop that overflows the eight-stop ceiling.
# ---------------------------------------------------------------------------


def _sound_stop(title: str, ref: str = "task-1") -> dict:
    return {"title": title, "body": "Body text.",
            "anchor": {"kind": "node", "ref": ref}}


def _resolver_context() -> TourAnchorContext:
    return TourAnchorContext(
        task_ids=("task-1",),
        diff_files=(("area/file.py", 1, 0),),
        evidence_files=("report.md",),
        run_commands=("run this command",),
    )


def test_resolver_drops_eight_bad_shapes_and_a_ninth_over_ceiling_stop():
    context = _resolver_context()
    fillers = [_sound_stop(f"Filler {i}") for i in range(MAX_TOUR_STOPS)]
    bad = [
        {"title": "Bad node", "body": "Body text.",
         "anchor": {"kind": "node", "ref": "missing-task"}},
        {"title": "Bad diff", "body": "Body text.",
         "anchor": {"kind": "diff", "ref": "nope/file.py"}},
        {"title": "Bad evidence", "body": "Body text.",
         "anchor": {"kind": "evidence", "ref": "missing.json"}},
        {"title": "Bad command", "body": "Body text.",
         # a recorded command ("run this command") cut short by its last word
         "anchor": {"kind": "command", "ref": "run this"}},
        {"title": "Bad\ntitle", "body": "Body text.",
         "anchor": {"kind": "node", "ref": "task-1"}},
        {"title": "Bad kind", "body": "Body text.",
         "anchor": {"kind": "bogus", "ref": "task-1"}},
        {"title": "Missing key", "anchor": {"kind": "node", "ref": "task-1"}},
        "not a dict",
    ]
    ninth_sound = _sound_stop("Ninth sound")

    kept, dropped = resolve_tour_stops([*fillers, *bad, ninth_sound], context)

    assert len(kept) == MAX_TOUR_STOPS
    assert kept == fillers
    assert len(dropped) == len(bad) + 1

    assert dropped[0] == {"title": "Bad node",
                          "reason": "anchor node:'missing-task' does not resolve "
                                    "against the job's own records"}
    assert dropped[1]["title"] == "Bad diff"
    assert "diff:'nope/file.py' does not resolve" in dropped[1]["reason"]
    assert dropped[2]["title"] == "Bad evidence"
    assert "evidence:'missing.json' does not resolve" in dropped[2]["reason"]
    assert dropped[3]["title"] == "Bad command"
    assert "command:'run this' does not resolve" in dropped[3]["reason"]
    assert dropped[4]["title"] == "Bad\ntitle"
    assert "newline" in dropped[4]["reason"]
    assert dropped[5]["title"] == "Bad kind"
    assert "anchor kind" in dropped[5]["reason"]
    assert dropped[6]["title"] == "Missing key"
    assert "keys must be exactly" in dropped[6]["reason"]
    assert dropped[7] == {"title": "", "reason": "a tour stop must be a dict, got str"}
    assert dropped[8] == {"title": "Ninth sound",
                          "reason": f"past the {MAX_TOUR_STOPS}-stop ceiling"}


# ---------------------------------------------------------------------------
# 10. the resolver never mutates its input and logs one warning per drop.
# ---------------------------------------------------------------------------


def test_resolver_never_mutates_its_input_and_logs_one_warning_per_drop(caplog):
    context = _resolver_context()
    good = _sound_stop("Good")
    bad = {"title": "Bad kind", "body": "Body text.",
           "anchor": {"kind": "bogus", "ref": "task-1"}}
    stops = [good, bad]
    frozen = json.dumps(stops, sort_keys=True)

    with caplog.at_level(logging.WARNING, logger="packages.orchestration.result_tour"):
        kept, dropped = resolve_tour_stops(stops, context)

    assert json.dumps(stops, sort_keys=True) == frozen  # unchanged, byte for byte
    assert kept == [good]
    assert kept[0] is not good  # a NEW dict, not the input object
    assert len(dropped) == 1
    warnings = [r for r in caplog.records if r.levelno == logging.WARNING]
    assert len(warnings) == 1


# ---------------------------------------------------------------------------
# 11. tour_problems accepts build_fallback_tour's answer and reports a wrong
#     schema, nine stops and a malformed dropped entry.
# ---------------------------------------------------------------------------


def test_tour_problems_accepts_a_real_build_and_catches_three_mutations():
    job = _make_job(tasks=[TaskEntry(title="t")])
    tour = build_fallback_tour(job)
    assert tour_problems(tour) == []

    wrong_schema = {**tour, "schema": "not-a-real-schema"}
    problems = tour_problems(wrong_schema)
    assert any("schema" in p for p in problems)

    one_stop = tour["stops"][0]
    nine_stops = {**tour, "stops": [one_stop] * (MAX_TOUR_STOPS + 1)}
    problems = tour_problems(nine_stops)
    assert any("at most 8 stops" in p for p in problems)

    malformed_dropped = {**tour, "dropped": [{"title": "x"}]}
    problems = tour_problems(malformed_dropped)
    assert any("dropped 0" in p for p in problems)


# ---------------------------------------------------------------------------
# 12. two builds over the same records are equal.
# ---------------------------------------------------------------------------


def test_two_builds_over_the_same_records_are_equal():
    job = _make_job(
        state=RunState.COMPLETED,
        tasks=[TaskEntry(title="t", status=RunState.COMPLETED)],
        metadata={"target_repo": "/tmp/repo", "cycle_terminal_status": "all_green"},
    )
    _write_diff(str(job.job_id), _one_file_diff("packages/orchestration/foo.py"))
    write_final_report(job)
    _write_gate(str(job.job_id), [_make_check("c1", command="python3 -m pytest -q")],
               released=True)

    first = build_fallback_tour(job)
    second = build_fallback_tour(job)
    assert first == second


# ---------------------------------------------------------------------------
# Sanity: the module's own contract constants agree with the spec.
# ---------------------------------------------------------------------------


def test_the_schema_and_anchor_kinds_match_the_design():
    assert TOUR_SCHEMA == "remedy.tour.v1"
    assert TOUR_ANCHOR_KINDS == ("node", "diff", "evidence", "command")
