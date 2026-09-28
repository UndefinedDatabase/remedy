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
import types
from pathlib import Path

import pytest

import packages.orchestration.long_run_executor as lre
from packages.core.models import RunState
from packages.orchestration.data_paths import job_evidence_dir, job_evidence_index_dir
from packages.orchestration.dod_gate import GateResult, save_gate_result
from packages.orchestration.dod_runners import CheckEvidence
from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan
from packages.orchestration.result_tour import (
    MAX_TOUR_STOPS,
    TOUR_ANCHOR_KINDS,
    TOUR_BODY_MAX_CHARS,
    TOUR_ERROR_METADATA_KEY,
    TOUR_GENERATOR_FALLBACK,
    TOUR_GENERATOR_SUMMARY_ROLE,
    TOUR_NO_SOUND_STOPS,
    TOUR_SCHEMA,
    TOUR_VIEW_KEYS,
    ResultTourError,
    TourAnchorContext,
    build_fallback_tour,
    build_tour_prompt,
    collect_tour_context,
    generate_result_tour,
    load_result_tour,
    render_tour_lines,
    resolve_tour_stops,
    stored_tour_versions,
    tour_call_fn,
    tour_model_written,
    tour_path,
    tour_problems,
    tour_source_text,
    tour_view,
    write_result_tour,
)
from packages.orchestration.run_report import build_report_sources, write_final_report

pytestmark = pytest.mark.integration

#: The three fixture goldens (F036 T002, second half; DECISION F036 D4 (6)).
FIXTURES_DIR = Path(__file__).parent / "fixtures" / "result_tour"


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


# ---------------------------------------------------------------------------
# F036 T002 (first half) — generation through the summary role
# ---------------------------------------------------------------------------


def _generation_job() -> JobPlan:
    """A finished job with a report, a one-file diff and a passing gate."""
    job = _make_job(
        state=RunState.COMPLETED,
        tasks=[TaskEntry(title="write the module", status=RunState.COMPLETED,
                         acceptance="tests pass")],
        metadata={"target_repo": "/tmp/repo", "cycle_terminal_status": "all_green"},
    )
    _write_diff(str(job.job_id), _one_file_diff("packages/orchestration/foo.py"))
    write_final_report(job)
    _write_gate(str(job.job_id), [_make_check("c1", command="python3 -m pytest -q")],
               released=True)
    return job


def _clean_stop(title: str, body: str, task_id: str) -> dict:
    return {"title": title, "body": body, "anchor": {"kind": "node", "ref": task_id}}


def _fake_call_fn(response_text: str):
    def _call(prompt: str, attempt: int) -> str:
        return response_text
    return _call


# 13. no call function gives exactly build_fallback_tour's answer.


def test_generate_with_no_call_fn_matches_build_fallback_tour():
    job = _generation_job()
    assert generate_result_tour(job, call_fn=None) == build_fallback_tour(job)


# 14. three sound model stops: generator summary-role, mechanical first stop
#     kept first, the three model stops following it in order.


def test_three_sound_model_stops_follow_the_mechanical_first_stop():
    job = _generation_job()
    task_id = str(job.tasks[0].task_id)
    stops = [
        _clean_stop("Task summary", "The task write the module is complete.", task_id),
        _clean_stop("Task summary two", "Status is completed for this task.", task_id),
        _clean_stop("Task summary three", "This task finished successfully.", task_id),
    ]
    fake = _fake_call_fn(json.dumps({"stops": stops}))

    tour = generate_result_tour(job, call_fn=fake)

    assert tour_problems(tour) == []
    assert tour["generator"] == TOUR_GENERATOR_SUMMARY_ROLE
    assert tour["dropped"] == []
    assert tour["stops"][0]["title"] == "How the run ended"
    assert [s["title"] for s in tour["stops"][1:]] == [
        "Task summary", "Task summary two", "Task summary three"]


# 15. a number, a backtick span, a path and a denylisted word are each
#     dropped with a reason naming them, while two clean stops survive.


def test_each_kind_of_new_claim_is_dropped_with_a_naming_reason():
    job = _generation_job()
    task_id = str(job.tasks[0].task_id)
    number_stop = _clean_stop("Number claim", "This closed 42 issues today.", task_id)
    backtick_stop = _clean_stop(
        "Backtick claim", "It touched `nonexistent_symbol` directly.", task_id)
    path_stop = _clean_stop("Path claim", "It also updated some/other/file.py.", task_id)
    word_stop = _clean_stop("Word claim", "Seamlessly finished the task.", task_id)
    good_one = _clean_stop("Good one", "The task write the module is complete.", task_id)
    good_two = _clean_stop("Good two", "Status is completed for this task.", task_id)
    fake = _fake_call_fn(json.dumps({"stops": [
        number_stop, backtick_stop, path_stop, word_stop, good_one, good_two]}))

    tour = generate_result_tour(job, call_fn=fake)

    assert tour_problems(tour) == []
    assert tour["generator"] == TOUR_GENERATOR_SUMMARY_ROLE
    reasons = {d["title"]: d["reason"] for d in tour["dropped"]}
    assert "42" in reasons["Number claim"]
    assert "nonexistent_symbol" in reasons["Backtick claim"]
    assert "some/other/file" in reasons["Path claim"]
    assert "seamlessly" in reasons["Word claim"]
    assert [s["title"] for s in tour["stops"]] == ["How the run ended", "Good one", "Good two"]


# 16. a stop anchored to an unknown task is dropped by the resolver, not the
#     claim check.


def test_a_stop_anchored_to_an_unknown_task_is_dropped_by_the_resolver():
    job = _generation_job()
    task_id = str(job.tasks[0].task_id)
    good = _clean_stop("Good stop", "The task write the module is complete.", task_id)
    unknown_anchor = {
        "title": "Unknown anchor", "body": "This references something else entirely.",
        "anchor": {"kind": "node", "ref": "not-a-real-task"},
    }
    fake = _fake_call_fn(json.dumps({"stops": [good, unknown_anchor]}))

    tour = generate_result_tour(job, call_fn=fake)

    assert tour_problems(tour) == []
    reason = next(d["reason"] for d in tour["dropped"] if d["title"] == "Unknown anchor")
    assert "does not resolve" in reason


# 17. nine sound model stops keep exactly eight stops in all, dropping the
#     rest past the ceiling.


def test_nine_sound_model_stops_keep_eight_in_all():
    job = _generation_job()
    task_id = str(job.tasks[0].task_id)
    # Letters, not digits: a digit in the title would itself be read as a
    # number claim by tour_claim_problems, which scans title AND body.
    letters = "ABCDEFGHI"
    stops = [_clean_stop(f"Filler {letter}", "This restates status completed for the task.",
                          task_id) for letter in letters]
    fake = _fake_call_fn(json.dumps({"stops": stops}))

    tour = generate_result_tour(job, call_fn=fake)

    assert tour_problems(tour) == []
    assert tour["generator"] == TOUR_GENERATOR_SUMMARY_ROLE
    assert len(tour["stops"]) == MAX_TOUR_STOPS
    assert tour["stops"][0]["title"] == "How the run ended"
    assert [s["title"] for s in tour["stops"][1:]] == [f"Filler {letter}" for letter in letters[:7]]
    assert len(tour["dropped"]) == 2
    assert all("ceiling" in d["reason"] for d in tour["dropped"])


# 18. every model stop dropped gives fallback:no_sound_stops, publishing the
#     mechanical tour, with the drops listed.


def test_every_stop_dropped_gives_the_no_sound_stops_fallback():
    job = _generation_job()
    task_id = str(job.tasks[0].task_id)
    bad_one = _clean_stop("Bad one", "This closed 42 issues today.", task_id)
    bad_two = _clean_stop("Bad two", "Seamlessly wrapped up.", task_id)
    fake = _fake_call_fn(json.dumps({"stops": [bad_one, bad_two]}))

    tour = generate_result_tour(job, call_fn=fake)

    assert tour_problems(tour) == []
    assert tour["generator"] == f"fallback:{TOUR_NO_SOUND_STOPS}"
    dropped_titles = [d["title"] for d in tour["dropped"]]
    assert "Bad one" in dropped_titles
    assert "Bad two" in dropped_titles
    assert tour["stops"] == build_fallback_tour(job)["stops"]


# 19. a call_fn raising RuntimeError, one raising OSError, and one answering
#     unparseable text each fall back without raising; the unparseable one is
#     called twice, and on_call fires once per real call.


def test_provider_errors_and_unparseable_text_fall_back_without_raising():
    job = _generation_job()

    def raises_runtime(prompt: str, attempt: int) -> str:
        raise RuntimeError("boom")

    def raises_os(prompt: str, attempt: int) -> str:
        raise OSError("boom")

    tour_rt = generate_result_tour(job, call_fn=raises_runtime)
    assert tour_problems(tour_rt) == []
    assert tour_rt["generator"].startswith("fallback:")

    tour_os = generate_result_tour(job, call_fn=raises_os)
    assert tour_problems(tour_os) == []
    assert tour_os["generator"].startswith("fallback:")

    calls: list[int] = []

    def unparseable(prompt: str, attempt: int) -> str:
        calls.append(attempt)
        return "not json at all"

    on_call_log: list[int] = []

    def on_call(attempt: int, schema_v: str, is_retry: bool, prompt: str) -> None:
        on_call_log.append(attempt)

    tour_bad = generate_result_tour(job, call_fn=unparseable, on_call=on_call)
    assert tour_problems(tour_bad) == []
    assert tour_bad["generator"].startswith("fallback:")
    assert len(calls) == 2
    assert len(on_call_log) == 2


# 20. the prompt holds the source text, every allowed anchor line, and the
#     numeral 7 (MAX_TOUR_STOPS - 1).


def test_the_prompt_holds_source_text_anchor_lines_and_the_numeral_seven():
    job = _generation_job()
    context = collect_tour_context(job)
    sources = build_report_sources(job)
    source_text = tour_source_text(job, sources, context)

    prompt = build_tour_prompt(source_text, context)

    assert source_text in prompt
    for task_id in context.task_ids:
        assert f"node {task_id}" in prompt
    for path, _added, _deleted in context.diff_files:
        assert f"diff {path}" in prompt
    for name in context.evidence_files:
        assert f"evidence {name}" in prompt
    for command in context.run_commands:
        assert f"command {command}" in prompt
    assert "7" in prompt


# 21. the source text lists a task's acceptance and each changed file with
#     its counts.


def test_source_text_lists_task_acceptance_and_changed_file_counts():
    job = _generation_job()
    context = collect_tour_context(job)
    sources = build_report_sources(job)

    source_text = tour_source_text(job, sources, context)

    assert "acceptance: tests pass" in source_text
    assert "changed file packages/orchestration/foo.py (+1 −0)" in source_text


# 22. tour_call_fn asks resolve_role_config for "summary" and hands
#     GeneratedTourContent to make_structured_call_fn; answers None under the
#     suite's refused Ollama.


def test_tour_call_fn_asks_resolve_role_config_and_make_structured_call_fn(monkeypatch):
    import packages.orchestration.result_tour as result_tour_module

    calls: dict[str, object] = {}

    def fake_resolve_role_config(role):
        calls["role"] = role
        return types.SimpleNamespace(model="fake-model")

    def fake_make_structured_call_fn(model_cls, *, model=None, provider=None):
        calls["model_cls"] = model_cls
        calls["model"] = model
        return None

    monkeypatch.setattr(result_tour_module, "resolve_role_config", fake_resolve_role_config)
    monkeypatch.setattr(
        result_tour_module, "make_structured_call_fn", fake_make_structured_call_fn)

    result = result_tour_module.tour_call_fn()

    assert result is None
    assert calls["role"] == "summary"
    assert calls["model_cls"] is result_tour_module.GeneratedTourContent
    assert calls["model"] == "fake-model"


def test_tour_call_fn_returns_none_under_the_suites_refused_ollama():
    # tests/conftest.py::_no_live_ollama_reach (autouse) already refuses a
    # live Ollama connection for every unmarked test.
    assert tour_call_fn() is None


# ---------------------------------------------------------------------------
# F036 T002 (second half) — storage: versions, the writer (DECISION F036 D4)
# ---------------------------------------------------------------------------


def test_two_writes_give_tour_json_then_tour_v2_json():
    job = _make_job(tasks=[TaskEntry(title="t")])

    first = write_result_tour(job, call_fn=None)
    second = write_result_tour(job, call_fn=None)

    assert first == tour_path(str(job.job_id), 1)
    assert second == tour_path(str(job.job_id), 2)
    assert stored_tour_versions(str(job.job_id)) == [1, 2]
    version, tour = load_result_tour(str(job.job_id))
    assert version == 2
    assert tour == build_fallback_tour(job)


def test_tour_v1_tour_vx_and_a_directory_tour_v3_are_not_versions():
    job = _make_job(tasks=[TaskEntry(title="t")])
    ev_dir = job_evidence_dir(str(job.job_id))
    ev_dir.mkdir(parents=True, exist_ok=True)
    (ev_dir / "tour_v1.json").write_text("{}", encoding="utf-8")
    (ev_dir / "tour_vx.json").write_text("{}", encoding="utf-8")
    (ev_dir / "tour_v3.json").mkdir()

    assert stored_tour_versions(str(job.job_id)) == []


# F036 D7 (1): the switch. `write_result_tour` unset now asks `tour_call_fn()`
# only when `tour_model_written()` is true; the old blanket "unset always
# calls it once" reading these four tests replace is exactly what R-1089
# named.


def test_tour_model_written_reads_false_by_default():
    assert tour_model_written() is False


def test_call_fn_none_never_calls_tour_call_fn_whatever_the_key(monkeypatch):
    import packages.orchestration.result_tour as result_tour_module

    calls: list[int] = []

    def spy():
        calls.append(1)
        return None

    monkeypatch.setattr(result_tour_module, "tour_call_fn", spy)
    job = _make_job(tasks=[TaskEntry(title="t")])

    write_result_tour(job, call_fn=None)
    assert calls == []

    monkeypatch.setenv("REMEDY_TOUR_MODEL_WRITTEN", "1")
    from packages.orchestration.config import reset_config

    reset_config()
    write_result_tour(job, call_fn=None)
    assert calls == []


def test_unset_calls_tour_call_fn_only_when_the_switch_is_on(monkeypatch):
    import packages.orchestration.result_tour as result_tour_module

    calls: list[int] = []

    def spy():
        calls.append(1)
        return None

    monkeypatch.setattr(result_tour_module, "tour_call_fn", spy)
    job = _make_job(tasks=[TaskEntry(title="t")])

    write_result_tour(job)
    assert calls == []

    monkeypatch.setenv("REMEDY_TOUR_MODEL_WRITTEN", "1")
    from packages.orchestration.config import reset_config

    reset_config()
    write_result_tour(job)
    assert calls == [1]


def test_a_call_function_handed_in_is_used_whatever_the_key(monkeypatch):
    """A call function HANDED IN (S1) is used as given — the switch governs
    only the unset default, never an explicit argument."""
    import packages.orchestration.result_tour as result_tour_module

    never_called: list[int] = []
    monkeypatch.setattr(result_tour_module, "tour_call_fn",
                        lambda: never_called.append(1) or None)
    job = _make_job(tasks=[TaskEntry(title="t")])

    handed_in_calls: list[int] = []

    def handed_in(prompt: str, max_retries: int) -> str:
        handed_in_calls.append(1)
        return "not valid json — forces the fallback path, never tour_call_fn"

    monkeypatch.setenv("REMEDY_TOUR_MODEL_WRITTEN", "1")
    from packages.orchestration.config import reset_config

    reset_config()
    write_result_tour(job, call_fn=handed_in)

    assert handed_in_calls, "the handed-in call function must be the one used"
    assert never_called == [], "tour_call_fn must not be consulted when call_fn is given"


def test_a_failing_write_records_tour_error_and_a_later_good_write_clears_it(monkeypatch):
    import packages.orchestration.result_tour as result_tour_module

    job = _make_job(tasks=[TaskEntry(title="t")])
    real_durable_write_json = result_tour_module.durable_write_json

    def boom(*_args, **_kwargs):
        raise OSError("disk gone")

    monkeypatch.setattr(result_tour_module, "durable_write_json", boom)

    result = write_result_tour(job, call_fn=None)

    assert result is None
    assert "OSError: disk gone" in job.metadata[TOUR_ERROR_METADATA_KEY]

    # Restore ONLY this one attribute — `monkeypatch.undo()` would also roll
    # back the autouse fixture's own REMEDY_DATA_DIR patch (same `monkeypatch`
    # instance), sending the next write to the real data root (R-0803).
    monkeypatch.setattr(result_tour_module, "durable_write_json", real_durable_write_json)
    result2 = write_result_tour(job, call_fn=None)

    assert result2 == tour_path(str(job.job_id), 1)
    assert TOUR_ERROR_METADATA_KEY not in job.metadata


def test_load_result_tour_answers_none_with_nothing_stored():
    job = _make_job(tasks=[TaskEntry(title="t")])
    assert load_result_tour(str(job.job_id)) is None


def test_load_result_tour_raises_for_unparseable_json():
    job = _make_job(tasks=[TaskEntry(title="t")])
    path = tour_path(str(job.job_id), 1)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("not json", encoding="utf-8")

    with pytest.raises(ResultTourError, match="does not read"):
        load_result_tour(str(job.job_id))


def test_load_result_tour_raises_for_an_unsound_tour():
    job = _make_job(tasks=[TaskEntry(title="t")])
    path = tour_path(str(job.job_id), 1)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"schema": TOUR_SCHEMA}), encoding="utf-8")

    with pytest.raises(ResultTourError, match="is not sound"):
        load_result_tour(str(job.job_id))


# ---------------------------------------------------------------------------
# S3 — the renderer
# ---------------------------------------------------------------------------


def test_render_tour_lines_gives_the_exact_s3_lines_with_a_multiline_body():
    tour = {
        "schema": TOUR_SCHEMA,
        "job_id": "abc123",
        "generator": "fallback",
        "stops": [
            {"title": "First stop", "body": "one line",
             "anchor": {"kind": "evidence", "ref": "report.md"}},
            {"title": "Second stop", "body": "line one\nline two",
             "anchor": {"kind": "diff", "ref": "packages/x.py"}},
        ],
        "dropped": [],
    }

    assert render_tour_lines(tour) == [
        "Guided tour of job abc123 (fallback, 2 stops)",
        "  1. First stop",
        "     one line",
        "     -> evidence: report.md",
        "  2. Second stop",
        "     line one",
        "     line two",
        "     -> diff: packages/x.py",
    ]


def test_render_tour_lines_singular_stop_noun():
    tour = {
        "schema": TOUR_SCHEMA, "job_id": "j", "generator": "fallback",
        "stops": [{"title": "Only", "body": "b",
                   "anchor": {"kind": "evidence", "ref": "report.md"}}],
        "dropped": [],
    }
    assert render_tour_lines(tour)[0] == "Guided tour of job j (fallback, 1 stop)"


# ---------------------------------------------------------------------------
# S4 — the hook: `_apply_terminal` writes exactly one tour per reported
# terminal, and none for a terminal that gets no report.
# ---------------------------------------------------------------------------

_HOOK_TERMINALS = (
    lre.TERMINAL_ALL_GREEN,
    lre.TERMINAL_STOPPED_BY_OPERATOR,
    lre.TERMINAL_BUDGET_EXHAUSTED,
    lre.TERMINAL_DEADLINE_REACHED,
    lre.TERMINAL_BLOCKED,
)


def _hook_job() -> JobPlan:
    return JobPlan(
        job_title="tour-hook-job",
        user_prompt="build the thing",
        tasks=[TaskEntry(title="task 0", inputs={"task_type": "documentation"})],
        state=RunState.PLANNED,
    )


class TestApplyTerminalWritesTheTour:

    @pytest.mark.parametrize("terminal", _HOOK_TERMINALS)
    def test_each_reported_terminal_writes_exactly_one_tour(self, terminal):
        job = _hook_job()

        lre._apply_terminal(job, terminal, "some reason")

        assert stored_tour_versions(str(job.job_id)) == [1]
        _version, tour = load_result_tour(str(job.job_id))
        assert tour["stops"][0]["anchor"] == {"kind": "evidence", "ref": "report.md"}

    def test_the_reported_terminals_are_exactly_the_five_tested_above(self):
        assert lre.REPORTED_TERMINALS == frozenset(_HOOK_TERMINALS)

    def test_max_cycles_reached_writes_no_tour(self):
        job = _hook_job()
        lre._apply_terminal(job, lre.TERMINAL_MAX_CYCLES_REACHED, "")
        assert stored_tour_versions(str(job.job_id)) == []

    def test_write_report_false_writes_no_tour(self):
        job = _hook_job()
        lre._apply_terminal(job, lre.TERMINAL_ALL_GREEN, "", write_report=False)
        assert stored_tour_versions(str(job.job_id)) == []

    def test_with_the_switch_off_all_green_writes_a_fallback_tour_and_never_calls_tour_call_fn(
            self, monkeypatch):
        """R-1089's own scenario: a reported terminal must make no model call
        the operator did not switch on (DECISION F036 D7 (1))."""
        import packages.orchestration.result_tour as result_tour_module

        calls: list[int] = []
        monkeypatch.setattr(result_tour_module, "tour_call_fn",
                            lambda: calls.append(1) or None)
        job = _hook_job()

        lre._apply_terminal(job, lre.TERMINAL_ALL_GREEN, "")

        assert calls == []
        _version, tour = load_result_tour(str(job.job_id))
        assert tour["generator"] == TOUR_GENERATOR_FALLBACK


# ---------------------------------------------------------------------------
# S7 — the fixture goldens: two mechanical tours and one generated tour, each
# pinned as a whole tour under tests/orchestration/fixtures/result_tour/.
# ---------------------------------------------------------------------------


def _golden_green_job() -> JobPlan:
    """A completed job with a report, a two-area diff and a released gate of
    one passing check — `golden_green_mechanical.json` / `golden_generated.json`."""
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
    return job


def _golden_held_job() -> JobPlan:
    """A blocked job with a report and a held gate of one passing and one
    failed check — `golden_held_mechanical.json`."""
    job = _make_job(
        state=RunState.BLOCKED,
        tasks=[TaskEntry(title="finish the task", status=RunState.BLOCKED)],
        metadata={"target_repo": "/tmp/repo", "cycle_terminal_status": "blocked",
                  "cycle_stop_reason": "no_ready_tasks"},
    )
    write_final_report(job)
    checks = [
        _make_check("c-ok", command="make lint", status="passed"),
        _make_check("c-bad", command="python3 -m pytest -q", status="failed"),
    ]
    _write_gate(str(job.job_id), checks, released=False)
    return job


def _load_golden(name: str, job_id) -> dict:
    """A golden fixture's tour, its `<job>` placeholder swapped for *job_id*."""
    text = (FIXTURES_DIR / name).read_text(encoding="utf-8")
    return json.loads(text.replace("<job>", str(job_id)))


def test_golden_green_mechanical_tour_equals_its_fixture():
    job = _golden_green_job()
    assert build_fallback_tour(job) == _load_golden("golden_green_mechanical.json", job.job_id)


def test_golden_held_mechanical_tour_equals_its_fixture():
    job = _golden_held_job()
    assert build_fallback_tour(job) == _load_golden("golden_held_mechanical.json", job.job_id)


def test_golden_generated_tour_equals_its_fixture():
    job = _golden_green_job()
    model_answer_text = (FIXTURES_DIR / "model_answer.json").read_text(encoding="utf-8")
    fake = _fake_call_fn(model_answer_text)

    tour = generate_result_tour(job, call_fn=fake)

    assert tour == _load_golden("golden_generated.json", job.job_id)
    assert tour["generator"] == TOUR_GENERATOR_SUMMARY_ROLE
    assert len(tour["dropped"]) == 3


# ---------------------------------------------------------------------------
# F036 T003 (first half) — tour_view, the one view the browser and the
# command line both build from (DECISION F036 D5)
# ---------------------------------------------------------------------------


def test_tour_view_for_a_stored_tour():
    job = _make_job(tasks=[TaskEntry(title="t")])
    write_result_tour(job, call_fn=None)

    view = tour_view(job)

    assert set(view) == set(TOUR_VIEW_KEYS)
    assert view["stored"] is True
    assert view["version"] == 1
    assert view["error"] == ""
    assert view["tour"] == build_fallback_tour(job)


def test_tour_view_for_none_stored():
    job = _make_job(tasks=[TaskEntry(title="t")])

    view = tour_view(job)

    assert set(view) == set(TOUR_VIEW_KEYS)
    assert view["stored"] is False
    assert view["version"] == 0
    assert view["error"] == ""
    assert view["tour"] == build_fallback_tour(job)


def test_tour_view_for_an_unreadable_stored_tour():
    job = _make_job(tasks=[TaskEntry(title="t")])
    path = tour_path(str(job.job_id), 1)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("not json", encoding="utf-8")

    view = tour_view(job)

    assert set(view) == set(TOUR_VIEW_KEYS)
    assert view["stored"] is False
    assert view["version"] == 0
    assert "does not read" in view["error"]
    assert view["tour"] == build_fallback_tour(job)


# ---------------------------------------------------------------------------
# R-1087 — a slashed path's segments may hold dots and hyphens, and the path
# ends at a word character so a sentence's closing full stop is never read
# as part of it.
# ---------------------------------------------------------------------------


def test_a_model_stop_naming_an_invented_dotted_hyphenated_path_is_dropped_with_the_whole_path():
    job = _generation_job()
    task_id = str(job.tasks[0].task_id)
    good = _clean_stop("Good stop", "The task write the module is complete.", task_id)
    invented_path_stop = _clean_stop(
        "Invented docs", "See docs/my-guide/intro.v2.md for the design.", task_id)
    fake = _fake_call_fn(json.dumps({"stops": [good, invented_path_stop]}))

    tour = generate_result_tour(job, call_fn=fake)

    reason = next(d["reason"] for d in tour["dropped"] if d["title"] == "Invented docs")
    assert "docs/my-guide/intro.v2.md" in reason
    assert reason.count("docs/my-guide/intro.v2.md") == 1


def test_a_model_stop_whose_body_ends_with_a_recorded_path_and_a_full_stop_is_kept():
    job = _generation_job()
    diff_stop = {
        "title": "What changed",
        "body": "This run changed packages/orchestration/foo.py.",
        "anchor": {"kind": "diff", "ref": "packages/orchestration/foo.py"},
    }
    fake = _fake_call_fn(json.dumps({"stops": [diff_stop]}))

    tour = generate_result_tour(job, call_fn=fake)

    assert tour["dropped"] == []
    assert [s["title"] for s in tour["stops"]] == ["How the run ended", "What changed"]
