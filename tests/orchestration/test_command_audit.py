"""F009 T002 — the per-job command audit record.

DECISION F009 D6 fixes the record's path, mode, shape and field order; DECISION F009 D14
fixes which attempts reach a record at all, the `args_hash` format and the `outcome`
vocabulary. These tests hold the writer to all of it, and in particular to the two
properties an audit log is worthless without: the field order two later features already
plan to read, and the absence of any raw credential or raw argument value in its bytes.
"""
from __future__ import annotations

import json
import stat as _stat
from pathlib import Path

import pytest

from packages.orchestration.command_audit import (
    AUDIT_FIELD_ORDER,
    AUDIT_FILENAME,
    OUTCOMES,
    args_fingerprint,
    audit_command_attempt,
)
from packages.orchestration.safe_points import job_control_dir

JOB = "a1b2c3d4e5f60718"
TOKEN_FP = "tf:0123456789abcdef"


@pytest.fixture
def control(tmp_path: Path) -> Path:
    """A control root of our own. Nothing here touches the developer's real data dir."""
    return tmp_path / "control"


def audit_path(control_root: Path, job_id: str = JOB) -> Path:
    return job_control_dir(job_id, control_root) / AUDIT_FILENAME


def read_lines(control_root: Path, job_id: str = JOB) -> list[dict]:
    raw = audit_path(control_root, job_id).read_bytes()
    return [json.loads(line) for line in raw.splitlines()]


def test_the_outcome_vocabulary_is_the_closed_set_d14_ruled() -> None:
    """The closed set, in order. The last three are the tokens no caller writes yet."""
    assert OUTCOMES == (
        "rejected_token",
        "rejected_csrf",
        "rejected_job",
        "rejected_shape",
        "rejected_command",
        "rejected_rate",
        "not_implemented",
        "accepted",
        "replayed",
        "rejected_effect",
    )
    assert "accepted" in OUTCOMES
    assert "replayed" in OUTCOMES, "a replay is not the acceptance it repeats (R-0636)"
    assert "rejected_effect" in OUTCOMES, "an effect that raised is not the acceptance it failed to be"
    assert len(set(OUTCOMES)) == len(OUTCOMES)


def test_the_field_order_on_the_line_is_the_one_d6_fixed(control: Path) -> None:
    """Not the parsed keys — the ORDER the bytes carry, which is what a reader sees."""
    assert audit_command_attempt(JOB, token_fp=TOKEN_FP, command="do_job",
                                 args={"x": 1}, nonce="n-1", outcome="not_implemented",
                                 create=True, control_root_path=control) is True

    line = audit_path(control).read_bytes().splitlines()[0].decode()
    parsed = json.loads(line)
    assert tuple(parsed.keys()) == AUDIT_FIELD_ORDER
    positions = [line.index(f'"{field}"') for field in AUDIT_FIELD_ORDER]
    assert positions == sorted(positions), f"fields are out of order on the line: {line}"


def test_the_record_is_private_and_under_the_jobs_control_directory(control: Path) -> None:
    audit_command_attempt(JOB, token_fp=TOKEN_FP, command="do_job", args={},
                          nonce="n-1", outcome="rejected_rate", create=True,
                          control_root_path=control)

    path = audit_path(control)
    assert path.exists()
    assert path.parent == control / "jobs" / JOB
    assert _stat.S_IMODE(path.stat().st_mode) == 0o600


def test_two_attempts_append_two_lines(control: Path) -> None:
    audit_command_attempt(JOB, token_fp=TOKEN_FP, command="do_job", args={},
                          nonce="n-1", outcome="rejected_rate", create=True,
                          control_root_path=control)
    audit_command_attempt(JOB, token_fp=TOKEN_FP, command="proof_chain", args={},
                          nonce="n-2", outcome="not_implemented", create=True,
                          control_root_path=control)

    records = read_lines(control)
    assert [r["command"] for r in records] == ["do_job", "proof_chain"]
    assert [r["outcome"] for r in records] == ["rejected_rate", "not_implemented"]


def test_create_false_against_a_missing_directory_writes_nothing(control: Path) -> None:
    """DECISION F009 D14, clause one: a pre-credential refusal never creates a directory."""
    assert audit_command_attempt(JOB, token_fp=TOKEN_FP, command="", args={},
                                 nonce="", outcome="rejected_token", create=False,
                                 control_root_path=control) is False

    assert not control.exists(), "an unauthenticated attempt materialised a control root"


def test_create_false_writes_into_a_directory_that_already_exists(control: Path) -> None:
    audit_command_attempt(JOB, token_fp=TOKEN_FP, command="do_job", args={},
                          nonce="n-1", outcome="not_implemented", create=True,
                          control_root_path=control)

    assert audit_command_attempt(JOB, token_fp=TOKEN_FP, command="", args={},
                                 nonce="", outcome="rejected_csrf", create=False,
                                 control_root_path=control) is True

    assert [r["outcome"] for r in read_lines(control)] == ["not_implemented", "rejected_csrf"]


def test_create_true_makes_the_job_control_directory(control: Path) -> None:
    assert not control.exists()

    assert audit_command_attempt(JOB, token_fp=TOKEN_FP, command="do_job", args={},
                                 nonce="n-1", outcome="rejected_shape", create=True,
                                 control_root_path=control) is True

    job_dir = control / "jobs" / JOB
    assert job_dir.is_dir()
    assert _stat.S_IMODE(job_dir.stat().st_mode) == 0o700


@pytest.mark.parametrize("bad_job_id", ["../escape", "", "with/slash", "x" * 65, None])
def test_a_job_id_that_does_not_validate_writes_nothing_and_returns_false(
        control: Path, bad_job_id: object) -> None:
    """The door hands over a path segment straight from a URL and never pre-validates it."""
    assert audit_command_attempt(bad_job_id, token_fp=TOKEN_FP, command="do_job",
                                 args={}, nonce="n-1", outcome="rejected_job",
                                 create=True, control_root_path=control) is False

    assert not control.exists()


def test_neither_the_raw_token_nor_the_raw_args_reach_the_file(control: Path) -> None:
    from packages.orchestration.ui_server import token_fingerprint

    raw_token = "s3cret-token-value-do-not-log"
    secret_arg = "/home/alice/private/keyfile"

    audit_command_attempt(JOB, token_fp=token_fingerprint(raw_token), command="do_job",
                          args={"path": secret_arg}, nonce="n-1",
                          outcome="not_implemented", create=True,
                          control_root_path=control)

    written = audit_path(control).read_bytes()
    assert raw_token.encode() not in written
    assert secret_arg.encode() not in written
    assert b"alice" not in written
    assert token_fingerprint(raw_token).encode() in written, "the fingerprint IS wanted"


def test_a_missing_nonce_is_written_as_the_empty_string(control: Path) -> None:
    audit_command_attempt(JOB, token_fp=TOKEN_FP, command="", args=None, nonce=None,
                          outcome="rejected_token", create=True,
                          control_root_path=control)

    record = read_lines(control)[0]
    assert record["nonce"] == ""
    assert "nonce" in record, "the field is present on every line, absent on none"


def test_equal_args_hash_equal_and_different_args_hash_differently() -> None:
    assert args_fingerprint({"a": 1, "b": 2}) == args_fingerprint({"b": 2, "a": 1}), (
        "key order must not change the hash — json_bytes sorts keys")
    assert args_fingerprint({"a": 1}) != args_fingerprint({"a": 2})
    assert args_fingerprint({}) != args_fingerprint({"a": 1})
    assert args_fingerprint({"a": 1}).startswith("ah:")
    assert len(args_fingerprint({"a": 1})) == len("ah:") + 16


def test_the_args_hash_is_written_and_the_hash_is_the_one_the_helper_gives(
        control: Path) -> None:
    args = {"job": "j-1", "depth": 3}

    audit_command_attempt(JOB, token_fp=TOKEN_FP, command="do_job", args=args,
                          nonce="n-1", outcome="not_implemented", create=True,
                          control_root_path=control)

    assert read_lines(control)[0]["args_hash"] == args_fingerprint(args)


def test_every_record_is_exactly_one_line(control: Path) -> None:
    """A record carrying a newline in its own values would split the log's line grammar."""
    audit_command_attempt(JOB, token_fp=TOKEN_FP, command="do_job",
                          args={"note": "two\nlines"}, nonce="n\n1",
                          outcome="not_implemented", create=True,
                          control_root_path=control)

    raw = audit_path(control).read_bytes()
    assert raw.count(b"\n") == 1, f"one attempt wrote {raw.count(chr(10).encode())} lines"
    assert json.loads(raw)["nonce"] == "n\n1", "the value survives, JSON-escaped"
