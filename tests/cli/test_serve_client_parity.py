"""The forwarded commands behave the same in both modes (F200, DECISIONs F200 D1 (3) and D3).

The amended feature file's acceptance reads: with the supervisor running, every
forwarded command prints the same output, exits with the same code and leaves the
same effect on disk as in direct mode, and one test module runs each of them in
both modes. This is that module. Every scenario runs twice through the real argv
dispatcher, once on a data root with no supervisor and once on a second data root
whose supervisor answers in a thread of this process, and the two runs are compared
after the ids that differ by construction — the job's, its tasks', the requests'
— and the timestamps are replaced by placeholders. Client mode is told apart from
direct mode by the door's own audit file, which only the door writes.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

import pytest

from apps.cli.grouped import main
from apps.cli.serve_client import DIRECT_ENV
from packages.orchestration.command_audit import AUDIT_FILENAME
from packages.orchestration.command_nonce import NONCE_DIRNAME
from packages.orchestration.pingpong_job import JOB_COMPLETED, _persist_job, parse_job_file
from tests.orchestration.test_serve_daemon import _Running

_JOB = """\
# Job: Serve Parity Test

## Task 1
Do the first thing.

Acceptance:
- it is done

## Task 2
Do the second thing.

Acceptance:
- it is done
"""

_HEX16 = re.compile(r"\b[0-9a-f]{16}\b")
_STAMP = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?")


@dataclass
class Run:
    """One mode's run of one scenario: what it printed, how it exited, what it wrote."""

    exit_code: int
    out: list[str]
    effects: dict
    audit: list[str]


def _cli(argv: list[str], capsys) -> tuple[int, str]:
    try:
        main(argv)
        code = 0
    except SystemExit as exc:
        code = exc.code if isinstance(exc.code, int) else 1
    return code, capsys.readouterr().out


def _normalise(text: str, job) -> str:
    text = text.replace(job.job_id, "<JOB>")
    for n, task in enumerate(job.tasks):
        text = text.replace(str(task.task_id), f"<T{n}>")
    return _STAMP.sub("<TS>", _HEX16.sub("<ID>", text))


def _effects(root: Path, job) -> dict:
    """Every control file under the job's control directory, normalised, by relative path,
    leaving out the door's own two records: its audit file and its nonce store."""
    base = root / "control" / "jobs" / job.job_id
    found = {}
    for path in sorted(base.rglob("*")) if base.is_dir() else ():
        rel_parts = path.relative_to(base).parts
        if path.is_file() and path.name != AUDIT_FILENAME and NONCE_DIRNAME not in rel_parts:
            rel = _normalise(str(path.relative_to(base)), job)
            found[rel] = _normalise(path.read_text(encoding="utf-8"), job)
    return found


def _audit(root: Path, job) -> list[str]:
    path = root / "control" / "jobs" / job.job_id / AUDIT_FILENAME
    if not path.exists():
        return []
    return [json.loads(line)["outcome"] for line in path.read_bytes().splitlines()]


def _scenario(mode: str, steps, tmp_path_factory, monkeypatch, capsys, *, state=None) -> Run:
    root = tmp_path_factory.mktemp("p" + mode[0])
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    monkeypatch.delenv(DIRECT_ENV, raising=False)
    repo = tmp_path_factory.mktemp("repo")
    job = parse_job_file(_JOB, str(repo))
    if state is not None:
        job.state = state
        _persist_job(job)
    supervisor = _Running(root) if mode == "client" else None
    try:
        code, out = 0, []
        for argv in steps(job):
            code, text = _cli(argv, capsys)
            out.append(_normalise(text, job))
    finally:
        if supervisor is not None:
            supervisor.close()
    return Run(code, out, _effects(root, job), _audit(root, job))


def _both(steps, tmp_path_factory, monkeypatch, capsys, **kwargs) -> tuple[Run, Run]:
    direct = _scenario("direct", steps, tmp_path_factory, monkeypatch, capsys, **kwargs)
    client = _scenario("client", steps, tmp_path_factory, monkeypatch, capsys, **kwargs)
    assert direct.audit == [], "a direct run must not go through the door"
    return direct, client


def _same(direct: Run, client: Run) -> None:
    assert (client.exit_code, client.out, client.effects) == (
        direct.exit_code, direct.out, direct.effects)


SCENARIOS = {
    "stop": lambda j: [["job", "stop", j.job_id, "--reason", "parity"]],
    "stop-json": lambda j: [["job", "stop", j.job_id, "--json"]],
    "stop-source": lambda j: [["job", "stop", j.job_id, "--source", "scheduler", "--json"]],
    "stop-twice": lambda j: [["job", "stop", j.job_id], ["job", "stop", j.job_id]],
    "pause": lambda j: [["job", "pause", j.job_id, "--reason", "hold"]],
    "pause-json": lambda j: [["job", "pause", j.job_id, "--json"]],
    "pause-task": lambda j: [["job", "pause", j.job_id, "--task", j.tasks[0].task_id]],
    "unpause-withdraws": lambda j: [["job", "pause", j.job_id], ["job", "unpause", j.job_id]],
    "unpause-nothing": lambda j: [["job", "unpause", j.job_id, "--json"]],
    "unpause-task": lambda j: [["job", "pause", j.job_id, "--task", j.tasks[1].task_id],
                               ["job", "unpause", j.job_id, "--task", j.tasks[1].task_id]],
}

#: How many door acceptances each scenario's client run must have made.
ACCEPTED = {"stop": 1, "stop-json": 1, "stop-source": 1, "stop-twice": 2, "pause": 1,
            "pause-json": 1, "pause-task": 1, "unpause-withdraws": 2, "unpause-nothing": 1,
            "unpause-task": 2}


@pytest.mark.parametrize("name", sorted(SCENARIOS))
def test_a_forwarded_command_prints_exits_and_writes_as_it_does_direct(
        name, tmp_path_factory, monkeypatch, capsys):
    direct, client = _both(SCENARIOS[name], tmp_path_factory, monkeypatch, capsys)
    _same(direct, client)
    assert direct.exit_code == 0
    assert client.audit == ["accepted"] * ACCEPTED[name]


def test_the_source_the_command_names_is_the_one_recorded_in_both_modes(
        tmp_path_factory, monkeypatch, capsys):
    direct, client = _both(SCENARIOS["stop-source"], tmp_path_factory, monkeypatch, capsys)
    for run in (direct, client):
        assert json.loads(run.effects["stop.json"])["source"] == "scheduler"


@pytest.mark.parametrize("argv", [
    lambda j: [["job", "pause", j.job_id, "--task", "T999"]],
    lambda j: [["job", "unpause", j.job_id, "--task", "T999", "--json"]],
], ids=["pause-unknown-task", "unpause-unknown-task"])
def test_a_refusal_a_read_decides_is_the_same_and_never_reaches_the_door(
        argv, tmp_path_factory, monkeypatch, capsys):
    direct, client = _both(argv, tmp_path_factory, monkeypatch, capsys)
    _same(direct, client)
    assert direct.exit_code == 1
    assert client.audit == []


@pytest.mark.parametrize("argv", [
    lambda j: [["job", "stop", j.job_id]],
    lambda j: [["job", "pause", j.job_id, "--json"]],
], ids=["stop", "pause"])
def test_a_completed_job_is_refused_the_same_way_in_both_modes(
        argv, tmp_path_factory, monkeypatch, capsys):
    direct, client = _both(argv, tmp_path_factory, monkeypatch, capsys, state=JOB_COMPLETED)
    _same(direct, client)
    assert direct.exit_code == 1
    assert client.audit == []


def test_a_refusal_the_door_answers_is_reported_with_the_commands_own_error(
        tmp_path_factory, monkeypatch, capsys):
    from apps.cli.serve_client import forward_effect

    root = tmp_path_factory.mktemp("pr")
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    job = parse_job_file(_JOB, str(tmp_path_factory.mktemp("repo")))
    supervisor = _Running(root)
    try:
        with pytest.raises(SystemExit) as caught:
            forward_effect(job.job_id, "do.run", {}, json_output=True,
                           error="run_not_started", subject="nothing ran")
    finally:
        supervisor.close()
    body = json.loads(capsys.readouterr().out)
    assert (caught.value.code, body["error"], body["status"]) == (1, "run_not_started", 400)
    assert body["message"] == ("nothing ran — the serve supervisor refused it: "
                               "command is not available on this channel")


def test_a_supervisor_that_stopped_answering_is_reported_and_nothing_is_written(
        tmp_path_factory, monkeypatch, capsys):
    from apps.cli.serve_client import forward_effect

    root = tmp_path_factory.mktemp("pu")
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    job = parse_job_file(_JOB, str(tmp_path_factory.mktemp("repo")))
    with pytest.raises(SystemExit) as caught:
        forward_effect(job.job_id, "job.stop", {}, json_output=True,
                       error="stop_not_requested", subject="no stop was requested")
    body = json.loads(capsys.readouterr().out)
    assert (caught.value.code, body["error"]) == (1, "serve_unreachable")
    assert _effects(root, job) == {}


def test_the_direct_variable_keeps_a_command_direct_while_a_supervisor_answers(
        tmp_path_factory, monkeypatch, capsys):
    root = tmp_path_factory.mktemp("pv")
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    job = parse_job_file(_JOB, str(tmp_path_factory.mktemp("repo")))
    supervisor = _Running(root)
    try:
        monkeypatch.setenv(DIRECT_ENV, "1")
        assert _cli(["job", "stop", job.job_id], capsys)[0] == 0
    finally:
        supervisor.close()
    assert _audit(root, job) == []
    assert json.loads((root / "control" / "jobs" / job.job_id / "stop.json")
                      .read_text(encoding="utf-8"))["source"] == "cli"
