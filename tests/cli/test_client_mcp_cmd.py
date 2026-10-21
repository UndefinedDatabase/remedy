"""`remedy client mcp` — F303 R5 C4, DECISION F303 D5.

Every test starts the command as a real child process, `python -m apps.cli.main client mcp ...`,
gives it the test's data root in its environment at call time, writes JSON-RPC lines to its
standard input and reads what it writes back. The certificates are real: a finished job is made
the way `tests/cli/test_certificate_cmd.py` makes one. No test reaches a network or a model.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from packages.orchestration.mcp_server import MCP_PROTOCOL_VERSION
from tests.cli.test_certificate_cmd import _ended_job

REPO_ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "remedy_data"))


def _mcp_child(args: list[str], messages: list[dict]) -> tuple[subprocess.CompletedProcess, list[dict]]:
    """Run `remedy client mcp ARGS` feeding MESSAGES, one per line, then the end of input."""
    env = dict(os.environ)
    env["PYTHONPATH"] = str(REPO_ROOT)
    done = subprocess.run(
        [sys.executable, "-m", "apps.cli.main", "client", "mcp", *args],
        input="".join(json.dumps(message) + "\n" for message in messages),
        cwd=REPO_ROOT, env=env, capture_output=True, text=True, timeout=300, check=False)
    answers = [json.loads(line) for line in done.stdout.splitlines() if line.strip()]
    return done, answers


def _call(message_id: int, name: str, arguments: dict | None = None) -> dict:
    params: dict = {"name": name}
    if arguments is not None:
        params["arguments"] = arguments
    return {"jsonrpc": "2.0", "id": message_id, "method": "tools/call", "params": params}


def _make_certificate(tmp_path: Path) -> tuple[str, Path]:
    job = _ended_job()
    jid = str(job.job_id)
    out = tmp_path / "made.zip"
    env = dict(os.environ)
    env["PYTHONPATH"] = str(REPO_ROOT)
    made = subprocess.run(
        [sys.executable, "-m", "apps.cli.main", "job", "certificate", jid, f"--out={out}"],
        cwd=REPO_ROOT, env=env, capture_output=True, text=True, timeout=300, check=False)
    assert made.returncode == 0, made.stderr
    return jid, out


def test_allowed_tools_are_listed_and_called_over_a_real_stdio_session(tmp_path):
    jid, certificate = _make_certificate(tmp_path)
    done, answers = _mcp_child(["--allow", "verify", "--allow", "gate_status"], [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
        _call(3, "verify", {"bundle": str(certificate)}),
        _call(4, "gate_status", {"job": jid}),
    ])
    assert done.returncode == 0
    assert done.stderr == ""
    assert [answer["id"] for answer in answers] == [1, 2, 3, 4]
    init = answers[0]["result"]
    assert init["protocolVersion"] == MCP_PROTOCOL_VERSION
    assert init["serverInfo"]["name"] == "remedy"
    assert init["serverInfo"]["version"]
    assert [tool["name"] for tool in answers[1]["result"]["tools"]] == ["gate_status", "verify"]

    verified = answers[2]["result"]
    assert verified["isError"] is False
    assert verified["structuredContent"]["ok"] is True
    assert verified["structuredContent"]["intact"] is True
    assert verified["structuredContent"]["problems"] == []

    status = answers[3]["result"]
    assert status["isError"] is False
    assert status["structuredContent"]["job_id"] == jid
    assert status["structuredContent"]["state"]
    assert "verification" in status["structuredContent"]


def test_closed_by_default_lists_no_tool_and_refuses_a_call():
    done, answers = _mcp_child([], [
        {"jsonrpc": "2.0", "id": 1, "method": "tools/list"},
        _call(2, "verify", {"bundle": "x.zip"}),
    ])
    assert done.returncode == 0
    assert answers[0]["result"] == {"tools": []}
    assert answers[1]["error"]["code"] == -32602


def test_an_allowed_name_no_tool_has_exits_2_with_standard_output_empty():
    done, _ = _mcp_child(["--allow", "nope"], [])
    assert done.returncode == 2
    assert done.stdout == ""
    for word in ("nope", "evidence_bundle", "gate_status", "verify"):
        assert word in done.stderr


def test_evidence_bundle_writes_the_certificate_and_a_second_call_to_the_path_is_refused(tmp_path):
    job = _ended_job()
    jid = str(job.job_id)
    target = tmp_path / "bundle.zip"
    done, answers = _mcp_child(["--allow", "evidence_bundle"], [
        _call(1, "evidence_bundle", {"job": jid, "out": str(target)}),
        _call(2, "evidence_bundle", {"job": jid, "out": str(target)}),
    ])
    assert done.returncode == 0
    first, second = (answer["result"] for answer in answers)
    assert first["isError"] is False
    assert target.is_file()
    assert second["isError"] is True
    assert second["structuredContent"]["error"] == "certificate_refused"
