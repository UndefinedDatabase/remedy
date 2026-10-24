"""Operator amendment amend1024-one-real-order, Part B: the planner's scope decision and the lane it
makes. No model is reached: every call function here is scripted."""
from __future__ import annotations

import json

import pytest

from packages.orchestration.do_lane import (
    DO_LANE_BOUNDED,
    DO_LANE_FULL,
    DoLaneDecision,
    lane_after_scope_decision,
)
from packages.orchestration.scope_decision import (
    SCOPE_DECISION_MAX_PATHS,
    SCOPE_ONE_JOB,
    SCOPE_REGEX_FALLBACK,
    SCOPE_SEVERAL_JOBS,
    decide_order_scope,
    record_scope_decision,
    scope_decision_prompt,
)


def _answering(answer):
    return lambda prompt, attempt: answer if isinstance(answer, str) else json.dumps(answer)


def test_the_prompt_shows_paths_only_and_cuts_at_the_limit():
    files = [f"src/m{i}.py" for i in range(SCOPE_DECISION_MAX_PATHS + 5)]
    prompt = scope_decision_prompt("Mach den Gruß freundlicher.", files)
    assert "ORDER:\nMach den Gruß freundlicher." in prompt
    assert f"src/m{SCOPE_DECISION_MAX_PATHS - 1}.py" in prompt
    assert f"src/m{SCOPE_DECISION_MAX_PATHS}.py" not in prompt
    assert "... and 5 more paths not shown" in prompt
    assert "single_job" in prompt and "German" in prompt


def test_an_answer_of_one_job_is_recorded_with_its_files_and_reason():
    record = decide_order_scope("o", ["a.py"], provider="ollama", call_fn=_answering(
        {"single_job": True, "files": ["a.py"], "reason": "Eine Funktion ändert sich."}))
    assert (record["outcome"], record["decided"], record["single_job"]) == ("answered", SCOPE_ONE_JOB, True)
    assert record["files"] == ["a.py"] and record["reason"] == "Eine Funktion ändert sich."
    assert record["planner"] == "ollama" and record["paths_total"] == 1


@pytest.mark.parametrize(("reason", "decided"), [("Zwei Dienste, zwei Lieferungen.", SCOPE_SEVERAL_JOBS),
                                                  ("", SCOPE_ONE_JOB), ("   ", SCOPE_ONE_JOB)])
def test_several_jobs_need_a_reason(reason, decided):
    record = decide_order_scope("o", [], provider="ollama", call_fn=_answering(
        {"single_job": False, "files": [], "reason": reason}))
    assert record["decided"] == decided


def test_no_answer_falls_back_to_the_regex_lanes_and_says_why(monkeypatch):
    monkeypatch.setattr("packages.orchestration.intake.make_structured_call_fn", lambda *a, **k: None)
    assert decide_order_scope("o", [], provider="ollama")["outcome"] == "planner_unreachable"

    def _broken(prompt, attempt):
        raise TimeoutError("the planner did not answer")

    failed = decide_order_scope("o", [], provider="ollama", call_fn=_broken)
    assert (failed["outcome"], failed["decided"]) == ("planner_failed", SCOPE_REGEX_FALLBACK)
    assert "TimeoutError" in failed["detail"]
    invalid = decide_order_scope("o", [], provider="ollama", call_fn=_answering("not json at all"))
    assert (invalid["outcome"], invalid["decided"], invalid["calls"]) == ("answer_invalid", SCOPE_REGEX_FALLBACK, 2)
    extra = decide_order_scope("o", [], provider="ollama", call_fn=_answering(
        {"single_job": True, "files": [], "reason": "x", "milestones": 3}))
    assert extra["outcome"] == "answer_invalid"            # exactly the three fields, nothing more


def test_one_job_turns_a_full_lane_into_one_job_without_milestones():
    full = DoLaneDecision(DO_LANE_FULL, "the scope of the order is not clearly one file")
    lane = lane_after_scope_decision(full, {"decided": SCOPE_ONE_JOB, "reason": "Ein Gruß.", "files": []})
    assert lane.lane == DO_LANE_FULL and lane.scope_decided
    assert lane.single_job == "the planner's scope decision says one job (Ein Gruß.)"
    assert "routing alone: the scope of the order is not clearly one file" in lane.reason


def test_a_bounded_lane_stays_bounded_only_while_the_planner_names_its_files():
    bounded = DoLaneDecision(DO_LANE_BOUNDED, "the order names one file, README.md", "README.md")
    agreed = lane_after_scope_decision(bounded, {"decided": SCOPE_ONE_JOB, "reason": "r", "files": ["README.md"]})
    assert agreed.bounded and agreed.deliverable == "README.md"
    wider = lane_after_scope_decision(
        bounded, {"decided": SCOPE_ONE_JOB, "reason": "r", "files": ["README.md", "greet/core.py"]})
    assert (wider.lane, wider.deliverable, wider.scope_decided) == (DO_LANE_FULL, "", True)
    several = lane_after_scope_decision(bounded, {"decided": SCOPE_SEVERAL_JOBS, "reason": "Zwei Teile."})
    assert several.lane == DO_LANE_FULL and not several.single_job


def test_without_an_answer_the_lane_is_the_regex_lane_unchanged():
    full = DoLaneDecision(DO_LANE_FULL, "why")
    assert lane_after_scope_decision(full, {"decided": SCOPE_REGEX_FALLBACK}) is full


def test_the_decision_is_kept_in_the_jobs_evidence_folder(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    from packages.orchestration.data_paths import job_evidence_dir

    record_scope_decision({"decided": SCOPE_ONE_JOB, "reason": "Ein Satz."}, "a1b2c3d4e5f60718")
    kept = json.loads((job_evidence_dir("a1b2c3d4e5f60718") / "scope_decision.json").read_text(encoding="utf-8"))
    assert kept == {"decided": SCOPE_ONE_JOB, "reason": "Ein Satz."}
    record_scope_decision(None, "a1b2c3d4e5f60719")
    assert not (job_evidence_dir("a1b2c3d4e5f60719") / "scope_decision.json").exists()
