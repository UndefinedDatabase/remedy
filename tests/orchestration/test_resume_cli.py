"""F047 T002 — ``remedy job resume <id>``.

The four acceptance proofs the task slice requires:

  * a pending stop request is CONSUMED and the job does not run;
  * worktree drift refuses, and the message names BOTH heads;
  * a never-checkpointed job says so and continues from persisted state;
  * an all-green job is a friendly no-op with exit 0.

Plus the order of those checks, which is the actual contract: the stop
request is evaluated before the head comparison, and the head comparison
before the plan-approval gate.

The executor is stubbed in every test here — this slice is about the
decisions taken BEFORE handing off, not about running tasks.
"""
from __future__ import annotations

from pathlib import Path

import pytest

import apps.cli.commands.job as job_cmd
import packages.orchestration.checkpoints as cp
from packages.core.models import Job, RunState, Task
from packages.orchestration.checkpoints import (
    Checkpoint,
    verify_digest_for,
    write_checkpoint,
)
from packages.orchestration.safe_points import request_stop, stop_requested
from packages.orchestration.storage import save_job


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path: Path, monkeypatch) -> Path:
    """Autouse: jobs, checkpoints and the control area all land under tmp_path."""
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


@pytest.fixture
def handed_off(monkeypatch) -> list[tuple]:
    """Record every hand-off to the multi-cycle executor instead of running it."""
    calls: list[tuple] = []
    monkeypatch.setattr(
        job_cmd, "_cmd_job_run_cycles",
        lambda job_id, **kwargs: calls.append((job_id, kwargs)))
    return calls


def make_job(*, pending: int = 2, completed: int = 0) -> Job:
    tasks = [Task(title=f"done{i}", description="d", status=RunState.COMPLETED)
             for i in range(completed)]
    tasks += [Task(title=f"todo{i}", description="d") for i in range(pending)]
    job = Job(name="resume-job", tasks=tasks)
    save_job(job)
    return job


def put_checkpoint(job: Job, index: int = 1, *, head: str = "") -> Checkpoint:
    checkpoint = Checkpoint(
        cycle_index=index,
        job_id=str(job.id),
        job_snapshot_path=f"jobs/{job.id}.json",
        job_snapshot_sha256="sha256:" + "0" * 64,
        worktree_head=head,
        budget_spent_tokens=42,
        verify_result="passed",
        verify_digest=verify_digest_for("passed", None),
        next_intent={"kind": "cycle", "cycle_index": index + 1},
        created_at="2026-07-26T12:00:00+00:00",
    )
    write_checkpoint(str(job.id), checkpoint)
    return checkpoint


def resume(job: Job, **kwargs):
    return job_cmd._cmd_job_resume(str(job.id), **kwargs)


# ---------------------------------------------------------------------------
# 1. A pending stop request wins, and is consumed
# ---------------------------------------------------------------------------


class TestPendingStopRequest:
    def test_the_request_is_consumed_and_the_job_does_not_run(
            self, handed_off, capsys):
        job = make_job()
        put_checkpoint(job)
        request_stop(str(job.id), reason="operator changed their mind")

        resume(job)

        assert handed_off == []                       # nothing ran
        assert stop_requested(str(job.id)) is None    # consumed, not merely read
        out = capsys.readouterr().out
        assert "stop request consumed" in out
        assert "not resuming" in out
        assert "operator changed their mind" in out

    def test_it_is_checked_before_the_worktree_head(self, handed_off, capsys):
        """A stopped job with drifted worktree reports the STOP, not the drift."""
        job = make_job()
        put_checkpoint(job, head="a" * 40)
        request_stop(str(job.id), reason="stop first")

        resume(job)

        captured = capsys.readouterr()
        assert "stop request consumed" in captured.out
        assert "worktree has moved" not in captured.err
        assert handed_off == []

    def test_it_is_checked_before_the_plan_approval_gate(self, handed_off, capsys):
        job = make_job()
        job.flight_plan = {"_approval": "pending"}
        save_job(job)
        request_stop(str(job.id), reason="stop first")

        resume(job)

        captured = capsys.readouterr()
        assert "stop request consumed" in captured.out
        assert "awaiting approval" not in captured.err

    def test_json_output_reports_the_stop(self, handed_off, capsys):
        import json as _json

        job = make_job()
        request_stop(str(job.id), reason="halt")
        resume(job, json_output=True)

        payload = _json.loads(capsys.readouterr().out)
        assert payload["resumed"] is False
        assert payload["action"] == "stopped"
        assert payload["stop_reason"] == "halt"

    def test_no_stop_request_means_the_job_runs(self, handed_off):
        job = make_job()
        put_checkpoint(job)
        resume(job)
        assert len(handed_off) == 1


# ---------------------------------------------------------------------------
# 2. Worktree drift refuses and names both heads
# ---------------------------------------------------------------------------


class TestWorktreeHeadVerification:
    def test_a_mismatch_refuses_and_names_both_heads(
            self, handed_off, monkeypatch, capsys):
        job = make_job()
        put_checkpoint(job, head="a" * 40)
        monkeypatch.setattr(job_cmd_checkpoints(), "resolve_live_worktree_head",
                            lambda _jid: "b" * 40)

        with pytest.raises(SystemExit) as exc:
            resume(job)

        assert exc.value.code == 3
        err = capsys.readouterr().err
        assert "a" * 40 in err and "b" * 40 in err
        assert "checkpoint head" in err and "worktree head" in err
        assert handed_off == []

    def test_the_refusal_offers_options_and_never_rebases(
            self, handed_off, monkeypatch, capsys):
        job = make_job()
        put_checkpoint(job, head="a" * 40)
        monkeypatch.setattr(job_cmd_checkpoints(), "resolve_live_worktree_head",
                            lambda _jid: "b" * 40)

        with pytest.raises(SystemExit):
            resume(job)

        err = capsys.readouterr().err
        assert "refuses to rebase silently" in err
        assert "start a fresh run" in err

    def test_a_matching_head_runs(self, handed_off, monkeypatch):
        job = make_job()
        put_checkpoint(job, head="a" * 40)
        monkeypatch.setattr(job_cmd_checkpoints(), "resolve_live_worktree_head",
                            lambda _jid: "a" * 40)
        resume(job)
        assert len(handed_off) == 1

    def test_an_unknown_live_head_is_not_treated_as_a_mismatch(
            self, handed_off, monkeypatch):
        """"" means unknown. Refusing on unknown would block every copy-mode job."""
        job = make_job()
        put_checkpoint(job, head="a" * 40)
        monkeypatch.setattr(job_cmd_checkpoints(), "resolve_live_worktree_head",
                            lambda _jid: "")
        resume(job)
        assert len(handed_off) == 1

    def test_a_checkpoint_without_a_head_skips_the_comparison(
            self, handed_off, monkeypatch):
        job = make_job()
        put_checkpoint(job, head="")
        monkeypatch.setattr(job_cmd_checkpoints(), "resolve_live_worktree_head",
                            lambda _jid: pytest.fail("must not be consulted"))
        resume(job)
        assert len(handed_off) == 1

    def test_head_at_reports_nothing_for_a_path_that_is_not_a_worktree(self, tmp_path):
        from packages.orchestration.worktrees import head_at

        assert head_at(tmp_path / "nope") == ""
        assert head_at("") == ""


def job_cmd_checkpoints():
    """The checkpoints module object the resume command imports from."""
    return cp


# ---------------------------------------------------------------------------
# 3. The plan-approval gate is consulted, not bypassed
# ---------------------------------------------------------------------------


class TestPlanApprovalGate:
    def test_a_pending_plan_blocks_the_resume(self, handed_off, capsys):
        job = make_job()
        job.flight_plan = {"_approval": "pending"}
        save_job(job)
        put_checkpoint(job)

        with pytest.raises(SystemExit) as exc:
            resume(job)

        assert exc.value.code == 3
        assert "awaiting approval" in capsys.readouterr().err
        assert handed_off == []

    def test_a_rejected_plan_blocks_the_resume(self, handed_off, capsys):
        job = make_job()
        job.flight_plan = {"_approval": "rejected"}
        save_job(job)

        with pytest.raises(SystemExit) as exc:
            resume(job)

        assert exc.value.code == 3
        assert "rejected" in capsys.readouterr().err
        assert handed_off == []

    def test_an_approved_plan_runs(self, handed_off):
        job = make_job()
        job.flight_plan = {"_approval": "approved"}
        save_job(job)
        put_checkpoint(job)
        resume(job)
        assert len(handed_off) == 1


# ---------------------------------------------------------------------------
# 4. Honest degradations
# ---------------------------------------------------------------------------


class TestDegradations:
    def test_no_checkpoint_says_so_and_continues(self, handed_off, capsys):
        job = make_job()
        resume(job)
        out = capsys.readouterr().out
        assert "no checkpoint found — continuing from persisted job state" in out
        assert len(handed_off) == 1

    def test_a_checkpoint_is_named_in_the_resume_line(self, handed_off, capsys):
        job = make_job()
        put_checkpoint(job, index=7)
        resume(job)
        out = capsys.readouterr().out
        assert "resuming from checkpoint 7" in out
        assert "spent=42 tokens" in out

    def test_all_corrupt_refuses_rather_than_pretending_none_exist(
            self, handed_off, capsys):
        import json as _json

        job = make_job()
        path = write_checkpoint(
            str(job.id),
            Checkpoint(cycle_index=1, job_id=str(job.id), worktree_head="a" * 40))
        raw = _json.loads(path.read_text(encoding="utf-8"))
        raw["record"]["worktree_head"] = "tampered"
        path.write_text(_json.dumps(raw), encoding="utf-8")

        with pytest.raises(SystemExit) as exc:
            resume(job)

        assert exc.value.code == 1
        err = capsys.readouterr().err
        assert "failed hash verification" in err
        assert "checkpoint_0001.json" in err
        assert "kept on disk" in err
        assert handed_off == []

    def test_an_all_green_job_is_a_friendly_no_op(self, handed_off, capsys):
        job = make_job(pending=0, completed=3)
        put_checkpoint(job)
        resume(job)                                  # exit 0 == no SystemExit
        assert "already all green — nothing to resume" in capsys.readouterr().out
        assert handed_off == []

    def test_an_all_green_job_reports_the_no_op_as_json(self, handed_off, capsys):
        import json as _json

        job = make_job(pending=0, completed=2)
        resume(job, json_output=True)
        payload = _json.loads(capsys.readouterr().out)
        assert payload == {"job_id": str(job.id), "action": "noop",
                           "resumed": False, "reason": "all_green"}

    def test_a_job_with_no_tasks_at_all_is_not_mistaken_for_all_green(
            self, handed_off, capsys):
        job = make_job(pending=0, completed=0)
        resume(job)
        assert "already all green" not in capsys.readouterr().out
        assert len(handed_off) == 1

    def test_an_unknown_job_exits_one(self, handed_off, capsys):
        with pytest.raises(SystemExit) as exc:
            job_cmd._cmd_job_resume("99999999-9999-4999-8999-999999999999")
        assert exc.value.code == 1
        assert "Job not found" in capsys.readouterr().err


# ---------------------------------------------------------------------------
# Hand-off and registration
# ---------------------------------------------------------------------------


class TestHandOff:
    def test_flags_are_passed_through_to_the_executor(self, handed_off):
        job = make_job()
        put_checkpoint(job)
        resume(job, cycles=3, json_output=True)
        _job_id, kwargs = handed_off[0]
        assert kwargs == {"cycles": 3, "json_output": True}

    def test_the_command_is_registered_exactly_once(self):
        from apps.cli.command_catalog import CATALOG, get_command

        assert len([c for c in CATALOG if c.command_id == "job.resume"]) == 1
        entry = get_command("job.resume")
        assert entry.subcommand == "resume"
        assert entry.supports_json is True
        args = {a.name: a for a in entry.args}
        assert "--cycles" in args
        assert args["--checkpoint"].required is False   # F047 is the default mode

    def test_the_dispatch_table_reaches_the_cycle_resume_without_a_checkpoint(
            self, monkeypatch):
        seen: list[tuple] = []
        monkeypatch.setattr(job_cmd, "_cmd_job_resume",
                            lambda job_id, **kw: seen.append((job_id, kw)))

        class _Args:
            job_id = "abcdef12"
            cycles = "2"
            checkpoint = ""
            json = True

        job_cmd.COMMAND_HANDLERS["job.resume"](_Args())
        assert seen == [("abcdef12", {"cycles": 2, "json_output": True})]

    def test_a_checkpoint_id_still_reaches_the_event_replay_resume(self, monkeypatch):
        """The pre-existing --checkpoint contract is untouched by F047."""
        seen: list[tuple] = []
        monkeypatch.setattr(job_cmd, "_cmd_resume",
                            lambda job_id, **kw: seen.append((job_id, kw)))
        monkeypatch.setattr(job_cmd, "_cmd_job_resume",
                            lambda *_a, **_kw: pytest.fail("must not be reached"))

        class _Args:
            job_id = "abcdef12"
            checkpoint = "cp-7"
            dry_run = True
            json = False

        job_cmd.COMMAND_HANDLERS["job.resume"](_Args())
        assert seen == [("abcdef12", {"checkpoint_id": "cp-7", "dry_run": True,
                                      "json_output": False})]
