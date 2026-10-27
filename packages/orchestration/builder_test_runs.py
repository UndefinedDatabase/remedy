"""Operator amendment amend1027-green-builds, Part B: the builder's own test runs count.

Job a833542685514a0a (2026-10-26) ended `review_not_passed` although the builder said its Vitest
file ran 5 of 5 green: the loop's test phase knew only test runs it started itself, so a round
with no test command of its own read `tests_not_run`, three rounds in a row. This module reads
what the builder ran from its own stream instead:

* `bash_calls_of_stream` lists every Bash call of one streamed claude-cli call with the tail of
  its result, as the F317 evidence did (`builder_bash_calls.json` beside the run's streams);
* a call whose command begins with one of the builder's test commands
  (`claude_cli_command.builder_test_commands`) is a test run, and `read_test_result` reads its
  outcome from the runner's own summary line (pytest, Vitest, Playwright, Jest, go, cargo);
* `round_test_reading` is the loop's test phase for a round that started no test itself: the
  builder's last test run of the round, else "Projekt hat keinen Testbefehl" when the project
  names none (A4, no `tests_not_run`), else `tests_not_run` with the reason (B3);
* `builder_test_runs.json` in the job's evidence keeps each reading, so `job_verification` names
  the builder as a tester beside the DoD's own run, which stays the reading that counts (B2).

Remedy deliberately does not trust a builder's prose: only a command in the stream with a result
in the stream counts, and a result with no summary line the module knows reads unknown.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

#: The run's list of every Bash call its builder made, beside its streams.
BUILDER_BASH_CALLS_FILENAME = "builder_bash_calls.json"
#: The job's list of the builder's test runs, in its evidence folder.
BUILDER_TEST_RUNS_FILENAME = "builder_test_runs.json"
#: A4: the test phase's summary for a project that names no test command.
NO_TEST_COMMAND_SUMMARY = "Projekt hat keinen Testbefehl"
#: B3: the reasons a round ran no test, as a key and the words the story shows.
NOT_RUN_REASONS = {
    "permission_denied": "Erlaubnis verweigert",
    "sandbox_unavailable": "Sandbox nicht verfügbar",
    "no_test_command": "Projekt hat keinen Testbefehl",
    "command_not_found": "Befehl nicht gefunden",
    "timeout": "Zeitlimit",
    "not_attempted": "der Bauer hat keinen Testlauf gestartet",
}
#: How many characters of a test run's result are kept.
RESULT_TAIL_CHARS = 4000

_COUNT = r"(\d+)\s+{word}"
_PASSED = re.compile(_COUNT.format(word=r"(?:passed|passing)"), re.IGNORECASE)
_FAILED = re.compile(_COUNT.format(word=r"(?:failed|failing)"), re.IGNORECASE)
_ERRORS = re.compile(_COUNT.format(word=r"errors?\b"), re.IGNORECASE)
_CARGO = re.compile(r"test result: (ok|FAILED)\. (\d+) passed; (\d+) failed")
_TESTS_LINE = re.compile(r"\s*Tests:?\s")
_GO_OK = re.compile(r"^ok\s+\S+", re.MULTILINE)
_GO_FAIL = re.compile(r"^FAIL\s+\S+", re.MULTILINE)
_NOT_FOUND = re.compile(r"command not found|not found\b|No such file or directory|ENOENT", re.IGNORECASE)
_TIMED_OUT = re.compile(r"timed out|timeout", re.IGNORECASE)


def bash_calls_of_stream(raw_stream: Path) -> list[dict[str, Any]]:
    """Every Bash tool call of one streamed call: its command, its result's tail and its error flag."""
    calls: dict[str, dict[str, Any]] = {}
    try:
        lines = raw_stream.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []
    for line in lines:
        try:
            event = json.loads(line)
        except ValueError:
            continue
        message = event.get("message") if isinstance(event, dict) else None
        content = message.get("content") if isinstance(message, dict) else None
        for part in content if isinstance(content, list) else []:
            if not isinstance(part, dict):
                continue
            if part.get("type") == "tool_use" and part.get("name") == "Bash":
                command = (part.get("input") or {}).get("command")
                calls[str(part.get("id"))] = {"command": str(command or ""), "result_tail": "",
                                              "is_error": None}
            elif part.get("type") == "tool_result" and str(part.get("tool_use_id")) in calls:
                body = part.get("content")
                text = body if isinstance(body, str) else json.dumps(body, ensure_ascii=False)
                calls[str(part.get("tool_use_id"))].update(
                    result_tail=text[-RESULT_TAIL_CHARS:], is_error=bool(part.get("is_error")))
    return list(calls.values())


def denied_commands_of_stream(raw_stream: Path) -> list[str]:
    """The Bash commands the CLI refused, from the stream's final `permission_denials`."""
    found: list[str] = []
    try:
        lines = raw_stream.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []
    for line in lines:
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if isinstance(event, dict) and event.get("type") == "result":
            found += [str((denial.get("tool_input") or {}).get("command") or "")
                      for denial in event.get("permission_denials") or [] if isinstance(denial, dict)]
    return found


def read_test_result(text: str, is_error: bool | None) -> tuple[bool | None, str]:
    """(passed, summary) of one test run's output: True green, False red, None unknown.

    Counts the runner's own summary words (`5 passed`, `1 failed`, `2 errors`) on its summary line,
    cargo's `test result:` lines, or go's `ok`/`FAIL` package lines; a run with failures or errors, or one the tool reported as an error
    with no passing count, is red; one with passes and neither is green; anything else unknown.
    """
    cargo = _CARGO.findall(text)
    lines = [line for line in text.splitlines() if _PASSED.search(line) or _FAILED.search(line)]
    tests = [line for line in lines if _TESTS_LINE.match(line)]
    if cargo:
        passed, failed = sum(int(m[1]) for m in cargo), sum(int(m[2]) for m in cargo)
    elif lines:
        # The runner's own summary line: Vitest's and Jest's `Tests` line, else the last count line
        # (pytest's `1 failed, 4 passed in 0.1s`, Playwright's `3 passed (4.1s)`).
        line = (tests or lines)[-1]
        passed = sum(int(n) for n in _PASSED.findall(line))
        failed = sum(int(n) for n in _FAILED.findall(line)) + sum(int(n) for n in _ERRORS.findall(line))
    else:   # go test: one `ok` or `FAIL` line per package
        passed, failed = len(_GO_OK.findall(text)), len(_GO_FAIL.findall(text))
    summary = f"{passed} passed, {failed} failed"
    if failed:
        return False, summary
    if passed and not is_error:
        return True, summary
    if is_error:
        return False if passed else None, summary
    return None, summary


def is_test_command(command: str, test_commands: tuple[str, ...]) -> bool:
    """Whether COMMAND runs one of TEST_COMMANDS: its first part (before a pipe, without a trailing
    `2>&1`) begins with one of them, word for word."""
    head = command.split("|", 1)[0].replace("2>&1", "").strip()
    return any(head == prefix or head.startswith(prefix + " ") for prefix in test_commands)


def _round_streams(stream_dir: str | None, round_num: int) -> list[Path]:
    """The raw streams of the builder's calls in round ROUND_NUM (`streams/builder/round-NN/*`)."""
    if not stream_dir:
        return []
    found = []
    for raw in sorted(Path(stream_dir).glob("streams/*/round-*/*/raw_stream.jsonl")):
        role, round_dir = raw.parts[-4], raw.parts[-3]
        if role != "reviewer" and round_dir.split("-", 1)[1].lstrip("0") == str(round_num):
            found.append(raw)
    return found


def round_test_reading(*, stream_dir: str | None, round_num: int, workspace: str | None,
                       job_id: str = "", run_id: str = "", task_id: str = "") -> tuple[bool | None, str, bool]:
    """The test phase of a round that started no test itself: (passed, summary, tests_not_run).

    Writes every Bash call of the round to the run's `builder_bash_calls.json` and the builder's
    test runs to the job's `builder_test_runs.json`. The round's last test run decides; with none,
    a project with no test command reads `NO_TEST_COMMAND_SUMMARY` and is not `tests_not_run`
    (A4), and any other round is `tests_not_run` with its reason (B3).
    """
    from packages.orchestration.claude_cli_command import builder_test_commands

    tests = builder_test_commands(workspace)
    calls, denied = [], []
    for raw in _round_streams(stream_dir, round_num):
        calls += [{**call, "round": round_num, "stream": str(raw.relative_to(stream_dir or ""))}
                  for call in bash_calls_of_stream(raw)]
        denied += denied_commands_of_stream(raw)
    if calls and stream_dir:
        _append_json(Path(stream_dir) / BUILDER_BASH_CALLS_FILENAME, calls)
    runs = []
    for call in calls:
        if not is_test_command(call["command"], tests) or call["is_error"] is None:
            continue
        passed, summary = read_test_result(call["result_tail"], call["is_error"])
        runs.append({"job_id": job_id, "run_id": run_id, "task_id": task_id, "round": round_num,
                     "command": call["command"][:500], "passed": passed, "summary": summary,
                     "output_tail": call["result_tail"]})
    judged = [run for run in runs if run["passed"] is not None]
    if judged:
        result: tuple[bool | None, str, bool] = (
            judged[-1]["passed"], f"builder ran `{judged[-1]['command']}`: {judged[-1]['summary']}", False)
    elif not _project_has_test_command(workspace):
        result = (None, NO_TEST_COMMAND_SUMMARY, False)
    else:
        key = not_run_reason_key(runs, denied, tests)
        runs.append({"job_id": job_id, "run_id": run_id, "task_id": task_id, "round": round_num,
                     "command": "", "passed": None, "reason_key": key})
        result = (None, f"tests_not_run: {NOT_RUN_REASONS[key]}", True)
    if runs and job_id:
        from packages.orchestration.data_paths import job_evidence_dir

        _append_json(Path(job_evidence_dir(job_id)) / BUILDER_TEST_RUNS_FILENAME, runs)
    return result


def not_run_reason_key(runs: list[dict[str, Any]], denied: list[str], tests: tuple[str, ...]) -> str:
    """B3: why a round ran no judged test, as a key of `NOT_RUN_REASONS`."""
    if any(is_test_command(command, tests) for command in denied):
        return "permission_denied"
    tails = " ".join(str(run.get("output_tail") or "") for run in runs)
    if runs and _NOT_FOUND.search(tails):
        return "command_not_found"
    if runs and _TIMED_OUT.search(tails):
        return "timeout"
    return "not_attempted"


def _project_has_test_command(workspace: str | None) -> bool:
    from packages.orchestration.project_tests import ProjectTestConfigError, find_project_test_command

    if not workspace:
        return True
    try:
        return find_project_test_command(Path(workspace), "python3") is not None
    except (ProjectTestConfigError, OSError):
        return True


def _append_json(path: Path, rows: list[dict[str, Any]]) -> None:
    """Add ROWS to the JSON list at PATH; a file that cannot be read starts over."""
    try:
        existing = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        existing = []
    if not isinstance(existing, list):
        existing = []
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([*existing, *rows], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_builder_test_runs(job_id: str) -> list[dict[str, Any]]:
    """The builder's test runs of JOB_ID, oldest first; [] when none were recorded."""
    from packages.orchestration.data_paths import job_evidence_dir

    try:
        rows = json.loads((Path(job_evidence_dir(job_id)) / BUILDER_TEST_RUNS_FILENAME).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    return [row for row in rows if isinstance(row, dict)] if isinstance(rows, list) else []
