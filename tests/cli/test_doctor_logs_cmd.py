"""`remedy doctor logs <job> [--run <id>] [--json]` (F203 T002, DECISION F203 D4): the operations
log's lines of one job, oldest first. Lines are written by hand into the isolated data root's log
folder; the command only reads.
"""
from __future__ import annotations

import json
import os
from collections import Counter

import pytest

from apps.cli.grouped import main as grouped_main
from packages.orchestration.structured_log import LOG_FILE_NAME, logs_dir
from tests.cli.in_process_cli import run_cli_in_process
from tests.cli.test_golden_path import _git_repo, _init_project, _run_do


def _line(job_id, run_id, message, **extra) -> str:
    entry = {
        "ts": "2026-10-13T08:05:09.042Z", "level": "INFO", "logger": "pkg.mod", "message": message,
        "job_id": job_id, "task_id": "T001" if run_id else None, "run_id": run_id,
    }
    entry.update(extra)
    return json.dumps(entry)


#: The saved job the lines belong to, and one with no line; the command resolves a job id
#: before it reads (operator amendment amend1014-luna-mission-fixes B.3).
JOB = "abc1230000000000"
QUIET = "ccc0000000000000"


@pytest.fixture
def written_log():
    from packages.orchestration.pingpong_job import JobPlan, save_job_plan

    for job_id in (JOB, QUIET):
        save_job_plan(JobPlan(job_id=job_id, job_title="logs"))
    folder = logs_dir()
    folder.mkdir(parents=True, exist_ok=True)
    lines = [
        _line(JOB, "r1", "first"),
        _line(JOB, "r2", "second", level="ERROR", exception="Traceback\nValueError: boom"),
        _line("def4560000000000", "r3", "elsewhere"),
        "not json at all",
    ]
    (folder / LOG_FILE_NAME).write_text("\n".join(lines) + "\n", encoding="utf-8")


def _run(argv, capsys) -> str:
    try:
        grouped_main(argv)
    except SystemExit as exc:
        assert exc.code in (0, None)
    return capsys.readouterr().out


def test_json_answers_the_matching_entries_and_the_counts(written_log, capsys):
    document = json.loads(_run(["doctor", "logs", "abc123", "--json"], capsys))
    assert document["ok"] is True
    assert document["job_id"] == JOB
    assert document["run_id"] is None
    assert [entry["message"] for entry in document["entries"]] == ["first", "second"]
    assert document["unreadable"] == 1
    assert document["files"] == [LOG_FILE_NAME]


def test_text_prints_one_line_per_entry_and_the_skipped_sentence(written_log, capsys):
    lines = _run(["doctor", "logs", "abc123"], capsys).splitlines()
    assert lines == [
        "2026-10-13T08:05:09.042Z INFO pkg.mod task=T001 run=r1 first",
        "2026-10-13T08:05:09.042Z ERROR pkg.mod task=T001 run=r2 second",
        "    Traceback",
        "    ValueError: boom",
        "1 lines of the log are not JSON and were skipped.",
    ]


def test_run_narrows_the_text_and_the_json_form(written_log, capsys):
    text = _run(["doctor", "logs", "abc123", "--run", "r2"], capsys)
    assert "second" in text
    assert "first" not in text
    document = json.loads(_run(["doctor", "logs", "abc123", "--run", "r2", "--json"], capsys))
    assert document["run_id"] == "r2"
    assert [entry["message"] for entry in document["entries"]] == ["second"]


def test_a_job_with_no_line_prints_the_sentence_and_exits_zero(written_log, capsys):
    assert f"No operations-log lines for job {QUIET}." in _run(["doctor", "logs", "ccc0"], capsys)
    narrowed = _run(["doctor", "logs", "abc123", "--run", "nope"], capsys)
    assert f"No operations-log lines for job {JOB} and run nope." in narrowed


@pytest.mark.parametrize(("value", "token"), [
    ("zzz", "invalid_job_id"), ("feed99", "invalid_job_id"), ("abc12300-0000-4000-8000-000000000000", "job_not_found"),
])
def test_a_value_that_names_no_job_is_refused(written_log, capsys, value, token):
    with pytest.raises(SystemExit) as ended:
        grouped_main(["doctor", "logs", value, "--json"])
    assert ended.value.code == 1
    assert json.loads(capsys.readouterr().out)["error"] == token


def _event_word(entry: dict) -> str:
    """The timeline event a mirrored line names: the first word of its message, minus a colon."""
    return entry["message"].split()[0].rstrip(":")


def test_a_fake_runs_lines_are_its_whole_timeline(tmp_path):
    """A whole small job on the fake providers: every timeline line has its twin in the log."""
    repo = _git_repo(tmp_path)
    data_root = tmp_path / "data"
    env = {**os.environ, "PYTHONPATH": os.getcwd(), "REMEDY_DATA_DIR": str(data_root)}
    _init_project(repo, env)
    done = _run_do(repo, env, "build a readme", ["--json"])
    assert done.returncode == 0, done.stderr
    [job_id] = json.loads(done.stdout)["job_ids"]

    timeline = [
        json.loads(text)
        for path in sorted((data_root / "job_logs" / job_id).glob("*.jsonl"))
        for text in path.read_text(encoding="utf-8").splitlines() if text.strip()
    ]
    assert timeline, "the run wrote no timeline line"

    shown = run_cli_in_process(["doctor", "logs", job_id, "--json"], repo, env)
    assert shown.returncode == 0, shown.stderr
    entries = json.loads(shown.stdout)["entries"]
    mirrored = [entry for entry in entries if entry["logger"] == "packages.orchestration.run_log"]
    assert all(entry["job_id"] == job_id for entry in mirrored)
    assert Counter((_event_word(e), e["task_id"]) for e in mirrored) == (
        Counter((line["event"], line.get("task_id")) for line in timeline))
    for line in timeline:
        attempt = line["metadata"].get("attempt_id")
        if attempt:
            assert any(e["run_id"] == attempt and _event_word(e) == line["event"]
                       for e in mirrored), line
    stamps = [entry["ts"] for entry in entries]
    assert stamps == sorted(stamps)
