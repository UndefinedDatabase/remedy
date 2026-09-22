"""Runtime CLI tests for Real Test Execution + Snapshot/Rollback Proof v1 (Step 1887/1895).

Subprocess tests. Read result/list/integrity + record snapshot proofs. No execution of the
real suite here. Safe JSON, safe errors, no tracebacks, honest restore flags.
"""
from __future__ import annotations

import json
from uuid import uuid4

import pytest

from packages.orchestration.data_paths import mint_job_id
from tests.cli.runtime_helpers import run_grouped_cli


def _job(env):
    from packages.core.models import RunState
    from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan
    repo = env / f"repo-{uuid4().hex[:6]}"; repo.mkdir(parents=True); (repo / "a.py").write_text("x=1\n")
    job = JobPlan(job_id=mint_job_id(), job_title="m", user_prompt="x", state=RunState.RUNNING,
              tasks=[TaskEntry(title="t")], artifacts=[], metadata={"target_repo": str(repo)})
    save_job_plan(job, root=env)
    return str(job.job_id)


@pytest.fixture()
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"; d.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    return d


def test_snapshot_create_show(env):
    """F283 R18 C4 (DECISION F283 D10) — the success document, through the real
    subprocess dispatcher, carries the envelope `emit_ok` added this round. The
    record's OWN `schema_version` (a domain string, unrelated to the envelope's
    integer of the same name) survives renamed to `record_schema_version`
    (`_envelope_safe` in `real_test_execution_cmd.py`) rather than being
    dropped, since the two clash by name only."""
    jid = _job(env)
    r = run_grouped_cli(["snapshot", "create", jid, "--json"], env)
    assert r.returncode == 0, r.stderr
    d = json.loads(r.stdout)
    assert d["schema_version"] == 1
    assert d["ok"] is True
    assert d["record_schema_version"] == "real-test-execution-v1"
    assert d["restore_available"] is False and "Traceback" not in r.stdout
    r2 = run_grouped_cli(["snapshot", "show", d["snapshot_id"], "--json"], env)
    body2 = json.loads(r2.stdout)
    assert body2["schema_version"] == 1
    assert body2["ok"] is True
    assert body2["snapshot_id"] == d["snapshot_id"]


def test_test_list_empty(env):
    jid = _job(env)
    r = run_grouped_cli(["test", "list", jid, "--json"], env)
    assert r.returncode == 0, r.stderr
    assert json.loads(r.stdout)["run_count"] == 0


def test_test_list_empty_text_message(env):
    jid = _job(env)
    r = run_grouped_cli(["test", "list", jid], env)
    assert r.returncode == 0, r.stderr
    assert f"No test runs for {jid[:8]}." in r.stdout


def test_test_list_text_shows_per_row(capsys):
    from argparse import Namespace
    from unittest.mock import patch

    from apps.cli.commands.real_test_execution_cmd import _cmd_test_list

    job_id = str(uuid4())
    fake_runs = [{"test_run_id": "run-1", "status": "passed", "exit_code": 0,
                  "created_at": "2026-09-04T00:00:00+00:00"}]
    args = Namespace(job_id=job_id, json=False)
    with patch("packages.orchestration.real_test_execution.list_test_runs", return_value=fake_runs):
        _cmd_test_list(args)

    out = capsys.readouterr().out
    assert "run-1" in out
    assert "status=passed" in out
    assert "exit=0" in out
    assert "created=2026-09-04T00:00:00+00:00" in out


_DATED_RUNS = [
    {"test_run_id": "run-old", "status": "passed", "exit_code": 0,
     "created_at": "2026-09-01T00:00:00+00:00"},
    {"test_run_id": "run-new", "status": "failed", "exit_code": 1,
     "created_at": "2026-09-03T00:00:00+00:00"},
]


def _test_list_json(capsys, **flags):
    from argparse import Namespace
    from unittest.mock import patch

    from apps.cli.commands.real_test_execution_cmd import _cmd_test_list

    args = Namespace(job_id=str(uuid4()), json=True, **flags)
    with patch("packages.orchestration.real_test_execution.list_test_runs",
               return_value=list(_DATED_RUNS)):
        _cmd_test_list(args)
    return json.loads(capsys.readouterr().out)


def test_test_list_is_newest_first_and_limit_caps_it(capsys):
    """R-0796: `test list` honours the shared list options."""
    assert [r["test_run_id"] for r in _test_list_json(capsys)["runs"]] == ["run-new", "run-old"]
    capped = _test_list_json(capsys, limit="1")
    assert capped["run_count"] == 1
    assert [r["test_run_id"] for r in capped["runs"]] == ["run-new"]


def test_test_list_since_and_until_filter_by_created_at(capsys):
    body = _test_list_json(capsys, since="2026-09-02T00:00:00+00:00",
                           until="2026-09-04T00:00:00+00:00")
    assert [r["test_run_id"] for r in body["runs"]] == ["run-new"]


def test_test_list_unknown_sort_field_exits_nonzero(capsys):
    """F283 R12 C3 — `invalid_list_option` used to print to stderr regardless of
    `--json`; the plain rule now answers the envelope on stdout when the flag holds,
    matching every other mechanical refusal in this module."""
    with pytest.raises(SystemExit) as exc:
        _test_list_json(capsys, sort="bogus")
    assert exc.value.code == 1
    captured = capsys.readouterr()
    assert captured.err == ""
    body = json.loads(captured.out)
    assert body["schema_version"] == 1
    assert body["ok"] is False
    assert body["error"] == "invalid_list_option"
    assert "valid fields: created_at, status, test_run_id" in body["message"]


def test_test_integrity(env):
    jid = _job(env)
    run_grouped_cli(["snapshot", "create", jid, "--json"], env)
    r = run_grouped_cli(["test", "integrity", "--json"], env)
    assert r.returncode == 0, r.stderr
    assert json.loads(r.stdout)["passed"] is True


def test_invalid_ids(env):
    r1 = run_grouped_cli(["test", "result", "nope", "--json"], env)
    assert r1.returncode == 1 and "Traceback" not in r1.stderr
    r2 = run_grouped_cli(["snapshot", "show", "nope", "--json"], env)
    assert r2.returncode == 1


def test_test_result_not_found_answers_the_envelope(env):
    """F283 R12 C3 — `_cmd_test_result`'s bare `Error: test run not found` line moves
    onto `fail()` by the plain rule; `--json` now answers the envelope instead of the
    prose it always printed regardless of the flag."""
    r = run_grouped_cli(["test", "result", "nope", "--json"], env)
    assert r.returncode == 1
    assert r.stderr == ""
    body = json.loads(r.stdout)
    assert body["schema_version"] == 1
    assert body["ok"] is False
    assert body["error"] == "test_run_not_found"


def test_snapshot_show_not_found_answers_the_envelope(env):
    """F283 R12 C3 — `_cmd_snapshot_show`'s bare `Error: snapshot proof not found`
    line moves onto `fail()` the same way."""
    r = run_grouped_cli(["snapshot", "show", "nope", "--json"], env)
    assert r.returncode == 1
    assert r.stderr == ""
    body = json.loads(r.stdout)
    assert body["schema_version"] == 1
    assert body["ok"] is False
    assert body["error"] == "snapshot_proof_not_found"


def test_json_purity(env):
    jid = _job(env)
    r = run_grouped_cli(["snapshot", "create", jid, "--json"], env)
    blob = r.stdout.lower()
    for marker in ("sk-ant", "/home/", "/users/", "traceback"):
        assert marker not in blob, marker
