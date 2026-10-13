"""`remedy doctor logs <job> [--run <id>] [--json]` (F203 T002, DECISION F203 D4): the operations
log's lines of one job, oldest first. Lines are written by hand into the isolated data root's log
folder; the command only reads.
"""
from __future__ import annotations

import json

import pytest

from apps.cli.grouped import main as grouped_main
from packages.orchestration.structured_log import LOG_FILE_NAME, logs_dir


def _line(job_id, run_id, message, **extra) -> str:
    entry = {
        "ts": "2026-10-13T08:05:09.042Z", "level": "INFO", "logger": "pkg.mod", "message": message,
        "job_id": job_id, "task_id": "T001" if run_id else None, "run_id": run_id,
    }
    entry.update(extra)
    return json.dumps(entry)


@pytest.fixture
def written_log():
    folder = logs_dir()
    folder.mkdir(parents=True, exist_ok=True)
    lines = [
        _line("abc123", "r1", "first"),
        _line("abc123", "r2", "second", level="ERROR", exception="Traceback\nValueError: boom"),
        _line("other", "r3", "elsewhere"),
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
    document = json.loads(_run(["doctor", "logs", "abc", "--json"], capsys))
    assert document["ok"] is True
    assert document["job_id"] == "abc"
    assert document["run_id"] is None
    assert [entry["message"] for entry in document["entries"]] == ["first", "second"]
    assert document["unreadable"] == 1
    assert document["files"] == [LOG_FILE_NAME]


def test_text_prints_one_line_per_entry_and_the_skipped_sentence(written_log, capsys):
    lines = _run(["doctor", "logs", "abc"], capsys).splitlines()
    assert lines == [
        "2026-10-13T08:05:09.042Z INFO pkg.mod task=T001 run=r1 first",
        "2026-10-13T08:05:09.042Z ERROR pkg.mod task=T001 run=r2 second",
        "    Traceback",
        "    ValueError: boom",
        "1 lines of the log are not JSON and were skipped.",
    ]


def test_run_narrows_the_text_and_the_json_form(written_log, capsys):
    text = _run(["doctor", "logs", "abc", "--run", "r2"], capsys)
    assert "second" in text
    assert "first" not in text
    document = json.loads(_run(["doctor", "logs", "abc", "--run", "r2", "--json"], capsys))
    assert document["run_id"] == "r2"
    assert [entry["message"] for entry in document["entries"]] == ["second"]


def test_a_job_with_no_line_prints_the_sentence_and_exits_zero(written_log, capsys):
    assert "No operations-log lines for job zzz." in _run(["doctor", "logs", "zzz"], capsys)
    narrowed = _run(["doctor", "logs", "abc", "--run", "nope"], capsys)
    assert "No operations-log lines for job abc and run nope." in narrowed
