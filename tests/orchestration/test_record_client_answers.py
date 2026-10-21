"""F313 T003 — the recorded answers for the universe's kit (DECISION F313 D2 and its addendum).

`scripts/record_client_answers.py` records the real answers of the client commands into
`docs/system/client-answers-v1/`. These tests hold the folder to a fresh recording, read the words
the kit tests the Orb against out of it, and pin how the check compares a key read by type.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from scripts.record_client_answers import (
    CLIENT_ANSWERS_DIR,
    RECORDED_CASES,
    SILENT_JOB_ID,
    STUB_MODEL,
    WORKING_JOB_ID,
    _differences,
)

REPO_ROOT = Path(__file__).resolve().parents[2]


def _answer(name: str) -> dict:
    return json.loads((CLIENT_ANSWERS_DIR / f"{name}.json").read_text(encoding="utf-8"))


def test_the_folder_holds_one_answer_per_case_and_matches_a_fresh_recording():
    assert sorted(p.name for p in CLIENT_ANSWERS_DIR.glob("*.json")) == sorted(
        f"{name}.json" for name, _args, _jobs in RECORDED_CASES)
    env = {**os.environ, "PYTHONPATH": str(REPO_ROOT)}
    result = subprocess.run([sys.executable, str(REPO_ROOT / "scripts" / "record_client_answers.py"), "--check"],
                            cwd=str(REPO_ROOT), env=env, capture_output=True, text=True, timeout=300)
    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout.strip().endswith("client answers: match")


def test_every_recorded_answer_is_an_ok_envelope():
    for name, _args, _jobs in RECORDED_CASES:
        answer = _answer(name)
        assert answer["ok"] is True, name
        assert answer["schema_version"] == 1, name


def test_the_recorded_now_answers_read_an_idle_machine_and_two_running_jobs():
    idle = _answer("client-now-idle")
    assert idle["jobs"] == [] and idle["orders"] == []
    assert idle["workers"] == {"running": 0, "free": None}
    running = _answer("client-now-running")
    assert [entry["job"] for entry in running["jobs"]] == [SILENT_JOB_ID, WORKING_JOB_ID]
    assert running["workers"] == {"running": 2, "free": None}
    assert running["model_server"]["state"] == "reachable"
    assert running["model_server"]["loaded"] == [STUB_MODEL]
    assert running["model_server"]["queue"] is None


def test_the_recorded_insights_read_a_working_and_a_silent_worker():
    working = _answer("client-insight-working")
    assert (working["stalled"], working["stall_reason"], working["advice"]) == (False, "none", ["nothing"])
    assert [entry["kind"] for entry in working["stream"]] == ["model_text", "tool_call", "tool_result"]
    silent = _answer("client-insight-silent")
    assert (silent["stalled"], silent["stall_reason"], silent["advice"]) == (True, "model_slow", ["wait", "stop"])
    assert silent["last_output_s"] >= _answer("client-now-running")["stall_threshold_s"]
    assert silent["worker"] == {"role": "builder", "provider": "pi", "model": STUB_MODEL}


def test_the_recorded_story_reads_the_working_job():
    story = _answer("client-story-working")
    assert story["job_id"] == WORKING_JOB_ID
    assert story["end"]["action"] == "abandon"


def test_the_check_names_every_changed_answer_and_exits_1(tmp_path, monkeypatch, capsys):
    import scripts.record_client_answers as recorder

    for recorded in CLIENT_ANSWERS_DIR.glob("*.json"):
        (tmp_path / recorded.name).write_bytes(recorded.read_bytes())
    idle = json.loads((tmp_path / "client-now-idle.json").read_text(encoding="utf-8"))
    idle["stall_threshold_s"] = 1
    (tmp_path / "client-now-idle.json").write_text(json.dumps(idle), encoding="utf-8")
    (tmp_path / "client-now-extra.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(recorder, "CLIENT_ANSWERS_DIR", tmp_path)

    assert recorder.main(["--check"]) == 1
    out = capsys.readouterr().out
    assert "client-now-idle.stall_threshold_s: 1 became 300" in out
    assert "client-now-extra.json: no such case" in out
    assert out.strip().endswith("client answers: 2 difference(s)")


def test_the_check_compares_a_clock_key_by_type_and_every_other_key_by_value():
    assert _differences({"at": "2026-10-21T00:00:00Z"}, {"at": "2026-10-22T09:09:09Z"}, "case") == []
    assert _differences({"at": "2026-10-21T00:00:00Z"}, {"at": None}, "case") == [
        "case.at: type str became NoneType"]
    assert _differences({"stall_reason": "none"}, {"stall_reason": "no_output"}, "case") == [
        "case.stall_reason: 'none' became 'no_output'"]
    assert _differences({"jobs": [{"job": "a"}]}, {"jobs": []}, "case") == ["case.jobs: 1 items became 0"]
    assert _differences({"a": 1}, {"b": 1}, "case") == ["case.a: missing", "case.b: new"]
