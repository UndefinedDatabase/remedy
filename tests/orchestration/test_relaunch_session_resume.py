"""R-1055 — the relaunch of an interrupted task resumes its parked provider session.

A park returns the interrupted task to `pending`, so its relaunch starts a new run.
Before the repair nothing on disk named the session the parked run had used, and the
new run's first calls could only start fresh, so T5_F025.md's "the resumed run provably
reuses its provider sessions where supported" was not met. Now every round's builder
and reviewer blocks in the run's `result.json` carry the session the call reported and
whether it resumed one, and `run_job` hands the parked run's sessions to the relaunch's
first calls. The load-bearing test is
:meth:`TestAParkedTaskResumesOnRelaunch.test_the_relaunch_resumes_the_parked_builder_session`,
which parks a real job mid-build and relaunches it through the real `run_job`.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from packages.orchestration import pause_control as pc
from packages.orchestration import pingpong_provider
from packages.orchestration.pingpong_job import (
    JOB_COMPLETED,
    JOB_PAUSED,
    JOB_STOPPED,
    parse_job_file,
    run_job,
)
from packages.orchestration.pingpong_loop import (
    export_pingpong_json,
    load_run,
    parked_session_refs,
    resume_declined_reasons,
    run_pingpong,
)
from packages.orchestration.pingpong_provider import (
    ClaudeCliProvider,
    ClaudeProvider,
    FakeProvider,
    OllamaPingPongProvider,
)
from packages.orchestration.safe_points import request_stop
from tests.orchestration.test_job_stop_integration import (  # noqa: F401
    _ONE_TASK_JOB,
    demo_repo,
    isolate_data_root,
)
from tests.orchestration.test_pause_resume import PauseTriggerProvider


def _resuming(session_id: str, **kwargs) -> FakeProvider:
    return FakeProvider(pass_on_round=1, fail_on_round=99, supports_resume=True,
                        fake_session_id=session_id, **kwargs)


class TestParkedSessionRefs:
    """The reader of a persisted run record, by role, last round winning."""

    def test_the_last_round_that_reported_a_session_wins(self):
        record = {"rounds": [
            {"builder": {"session_id": "b-1"}, "reviewer": {"session_id": "r-1"}},
            {"builder": {"session_id": "b-2"}},
        ]}
        assert parked_session_refs(record) == {"builder": "b-2", "reviewer": "r-1"}

    @pytest.mark.parametrize("record", [
        None,
        {},
        {"rounds": []},
        {"rounds": [{"builder": {"summary": "a record written before R-1055"}}]},
        {"rounds": [{"builder": {"session_id": ""}, "reviewer": {"session_id": ""}}]},
    ])
    def test_a_record_that_names_no_session_resumes_nothing(self, record):
        assert parked_session_refs(record) == {}


class TestTheRunRecordCarriesEachCallsSession:

    def test_each_round_block_names_its_session_and_whether_it_resumed(
            self, isolate_data_root, demo_repo):
        provider = _resuming("sess-1")
        result = run_pingpong("Fix README", str(demo_repo),
                              builder_provider=provider, reviewer_provider=provider)
        exported = export_pingpong_json(result)
        builder = exported["rounds"][0]["builder"]
        reviewer = exported["rounds"][0]["reviewer"]
        for block in (builder, reviewer):
            assert block["session_id"] == "sess-1"
            assert block["resume_used"] is False
            assert block["resume_session_ref"] == ""
            assert block["resume_fallback"] is False
        assert exported["resumed_from_run_id"] == ""
        assert parked_session_refs(load_run(result.run_id)) == {
            "builder": "sess-1", "reviewer": "sess-1"}


class TestTheFirstCallsResumeTheOfferedSessions:

    def test_both_roles_resume_on_round_one_when_supported(self, isolate_data_root, demo_repo):
        provider = _resuming("sess-new")
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            resume_sessions={"builder": "sess-parked-b", "reviewer": "sess-parked-r"},
            resumed_from_run_id="parked-run",
        )
        first = result.rounds[0]
        assert first.builder_output.resume_used is True
        assert first.builder_output.resume_session_ref == "sess-parked-b"
        assert first.reviewer_output.resume_used is True
        assert first.reviewer_output.resume_session_ref == "sess-parked-r"
        exported = export_pingpong_json(result)
        assert exported["resumed_from_run_id"] == "parked-run"
        assert exported["rounds"][0]["builder"]["resume_used"] is True
        assert exported["rounds"][0]["reviewer"]["resume_session_ref"] == "sess-parked-r"

    def test_a_provider_without_resume_is_offered_nothing(self, isolate_data_root, demo_repo):
        provider = FakeProvider(pass_on_round=1, fail_on_round=99, fake_session_id="sess-new")
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            resume_sessions={"builder": "sess-parked-b", "reviewer": "sess-parked-r"},
            resumed_from_run_id="parked-run",
        )
        assert result.rounds[0].builder_output.resume_used is False
        assert result.rounds[0].reviewer_output.resume_used is False

    def test_a_lost_parked_session_falls_back_once_and_the_round_completes(
            self, isolate_data_root, demo_repo):
        provider = _resuming("sess-new", resume_fails=True)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            resume_sessions={"builder": "sess-parked-b"},
            resumed_from_run_id="parked-run",
        )
        assert result.rounds[0].builder_output.resume_fallback is True
        assert result.rounds[0].builder_output.error == ""
        assert result.final_status == "staged_review_passed"


class TestAParkedTaskResumesOnRelaunch:

    def test_the_relaunch_resumes_the_parked_builder_session(
            self, isolate_data_root, demo_repo):
        job = parse_job_file(_ONE_TASK_JOB, str(demo_repo))
        builder = PauseTriggerProvider(
            on_build=1,
            trigger=lambda: pc.request_pause(job.job_id, "mid-build pause", "cli"),
            pass_on_round=1, fail_on_round=99,
            supports_resume=True, fake_session_id="sess-parked")
        parked = run_job(job.job_id, builder_provider=builder,
                         reviewer_provider=_resuming("sess-parked-review"), repair_rounds=0)
        assert parked.state == JOB_PAUSED
        parked_run_id = parked.tasks[0].run_id
        assert parked_run_id
        assert parked_session_refs(load_run(parked_run_id)) == {"builder": "sess-parked"}

        resumed = run_job(job.job_id, builder_provider=_resuming("sess-relaunch"),
                          reviewer_provider=_resuming("sess-relaunch-review"), repair_rounds=0)
        assert resumed.state == JOB_COMPLETED
        record = load_run(resumed.tasks[0].run_id)
        assert resumed.tasks[0].run_id != parked_run_id
        assert record["resumed_from_run_id"] == parked_run_id
        assert record["rounds"][0]["builder"]["resume_used"] is True
        assert record["rounds"][0]["builder"]["resume_session_ref"] == "sess-parked"
        assert record["rounds"][0]["reviewer"]["resume_used"] is False

    def test_a_task_that_was_never_interrupted_resumes_nothing(
            self, isolate_data_root, demo_repo):
        job = parse_job_file(_ONE_TASK_JOB, str(demo_repo))
        done = run_job(job.job_id, builder_provider=_resuming("sess-1"),
                       reviewer_provider=_resuming("sess-2"), repair_rounds=0)
        assert done.state == JOB_COMPLETED
        record = load_run(done.tasks[0].run_id)
        assert record["resumed_from_run_id"] == ""
        assert record["rounds"][0]["builder"]["resume_used"] is False


class TestAParkedClaudeCliTaskResumesOnRelaunch:
    """DECISION F287 D5: with the providers `run_job` builds for itself (T002), a
    relaunch on `claude-cli` resumes the parked session in the job's own worktree;
    in copy mode -- where every run gets its own directory -- the resume is refused
    and the round falls back once, exactly as a real `claude --resume` behaves
    against a session it cannot find under the calling directory.

    ONE stand-in replaces `pingpong_provider._guarded_cli_run` for the parked run
    and its relaunch together: it remembers, for every session id it hands out, the
    directory of the call that created it, and refuses any `--resume` naming a
    session minted under a different directory. A successful builder call also
    writes one line into a file under its own working directory, so every task has
    a real change to apply.
    """

    @staticmethod
    def _make_stand_in(interrupt):
        """Build the `_guarded_cli_run` replacement shared by the parked run and its
        relaunch. `interrupt` fires once, on the first builder call, before that
        call answers -- the same race `PauseTriggerProvider`/`CountingProvider`
        prove for `FakeProvider`, reused here against the real `claude-cli` call
        path. Returns ``(stand_in, calls)``; ``calls`` records every call's role,
        cwd, `--resume` value and the session id it was handed (empty when
        refused), in call order."""
        state = {"n": 0, "session_dir": {}, "interrupted": False}
        calls: list[dict] = []

        def _run(cmd, timeout_sec, cwd):
            is_reviewer = "--json-schema" in cmd
            role = "reviewer" if is_reviewer else "builder"
            resume = cmd[cmd.index("--resume") + 1] if "--resume" in cmd else ""
            call = {"role": role, "cwd": cwd, "resume": resume, "session_id": ""}
            calls.append(call)

            if role == "builder" and not state["interrupted"]:
                state["interrupted"] = True
                interrupt()

            if resume:
                created_in = state["session_dir"].get(resume)
                if created_in != cwd:
                    return MagicMock(
                        returncode=1, stdout="",
                        stderr=f"No conversation found with session ID: {resume}",
                    )

            state["n"] += 1
            session_id = f"sess-{role[0]}{state['n']}"
            state["session_dir"][session_id] = cwd
            call["session_id"] = session_id

            if role == "builder":
                readme = Path(cwd) / "docs" / "README.md"
                readme.parent.mkdir(parents=True, exist_ok=True)
                with readme.open("a") as fh:
                    fh.write(f"- stand-in change {session_id}\n")
                payload = {
                    "type": "result", "subtype": "success", "is_error": False,
                    "result": "- docs/README.md",
                    "usage": {"input_tokens": 10, "output_tokens": 10},
                    "session_id": session_id,
                }
            else:
                payload = {
                    "type": "result", "subtype": "success", "is_error": False,
                    "structured_output": {
                        "schema_v": "rv1", "verdict": "pass", "findings": [],
                        "confidence": "high", "summary": "ok",
                    },
                    "usage": {"input_tokens": 10, "output_tokens": 10},
                    "session_id": session_id,
                }
            return MagicMock(returncode=0, stdout=json.dumps(payload), stderr="")

        return _run, calls

    @staticmethod
    def _init_git_repo(repo: Path) -> None:
        """Mirrors `.remedy-wt/f287-r6/probe_cwd_git.py`: a minimal git target so
        `run_job` gives the job its own worktree instead of a filtered copy."""
        for args in (["init", "-q"], ["add", "-A"],
                     ["-c", "user.email=p@p", "-c", "user.name=p", "commit", "-qm", "init"]):
            subprocess.run(["git", "-C", str(repo), *args], check=True)

    def test_a_git_target_pause_resumes_the_parked_builder_session_on_relaunch(
            self, isolate_data_root, demo_repo):
        self._init_git_repo(demo_repo)
        job = parse_job_file(_ONE_TASK_JOB, str(demo_repo))
        stand_in, calls = self._make_stand_in(
            lambda: pc.request_pause(job.job_id, "mid-build pause", "cli"))

        with patch.object(pingpong_provider, "_guarded_cli_run", side_effect=stand_in), \
             patch.object(pingpong_provider.ClaudeCliProvider, "_get_claude_path",
                          lambda self: "/fake/claude"), \
             patch.object(pingpong_provider.ClaudeCliProvider, "_resolve_version",
                          lambda self: "1.0.0 (test)"):
            parked = run_job(
                job.job_id, builder_name="claude-cli", reviewer_name="claude-cli",
                builder_model="claude-sonnet-4-6", reviewer_model="claude-sonnet-4-6",
                repair_rounds=0)
            assert parked.state == JOB_PAUSED
            parked_run_id = parked.tasks[0].run_id
            assert parked_run_id

            builder_calls = [c for c in calls if c["role"] == "builder"]
            assert len(builder_calls) == 1
            parked_builder_call = builder_calls[0]
            assert parked_builder_call["resume"] == ""

            resumed = run_job(
                job.job_id, builder_name="claude-cli", reviewer_name="claude-cli",
                builder_model="claude-sonnet-4-6", reviewer_model="claude-sonnet-4-6",
                repair_rounds=0)

        assert resumed.state == JOB_COMPLETED
        relaunch_builder_calls = [c for c in calls if c["role"] == "builder"][1:]
        assert relaunch_builder_calls
        first_relaunch_builder_call = relaunch_builder_calls[0]
        assert first_relaunch_builder_call["cwd"] == parked_builder_call["cwd"]
        assert first_relaunch_builder_call["resume"] == parked_builder_call["session_id"]

        record = load_run(resumed.tasks[0].run_id)
        assert record["resumed_from_run_id"] == parked_run_id
        assert record["rounds"][0]["builder"]["resume_used"] is True
        assert (record["rounds"][0]["builder"]["resume_session_ref"]
                == parked_builder_call["session_id"])

    def test_a_git_target_stop_resumes_the_parked_builder_session_on_relaunch(
            self, isolate_data_root, demo_repo):
        self._init_git_repo(demo_repo)
        job = parse_job_file(_ONE_TASK_JOB, str(demo_repo))
        stand_in, calls = self._make_stand_in(
            lambda: request_stop(job.job_id, "mid-build stop", "cli"))

        with patch.object(pingpong_provider, "_guarded_cli_run", side_effect=stand_in), \
             patch.object(pingpong_provider.ClaudeCliProvider, "_get_claude_path",
                          lambda self: "/fake/claude"), \
             patch.object(pingpong_provider.ClaudeCliProvider, "_resolve_version",
                          lambda self: "1.0.0 (test)"):
            interrupted = run_job(
                job.job_id, builder_name="claude-cli", reviewer_name="claude-cli",
                builder_model="claude-sonnet-4-6", reviewer_model="claude-sonnet-4-6",
                repair_rounds=0)
            assert interrupted.state == JOB_STOPPED
            interrupted_run_id = interrupted.tasks[0].run_id
            assert interrupted_run_id

            builder_calls = [c for c in calls if c["role"] == "builder"]
            assert len(builder_calls) == 1
            interrupted_builder_call = builder_calls[0]

            resumed = run_job(
                job.job_id, builder_name="claude-cli", reviewer_name="claude-cli",
                builder_model="claude-sonnet-4-6", reviewer_model="claude-sonnet-4-6",
                repair_rounds=0)

        assert resumed.state == JOB_COMPLETED
        relaunch_builder_calls = [c for c in calls if c["role"] == "builder"][1:]
        assert relaunch_builder_calls
        first_relaunch_builder_call = relaunch_builder_calls[0]
        assert first_relaunch_builder_call["cwd"] == interrupted_builder_call["cwd"]
        assert first_relaunch_builder_call["resume"] == interrupted_builder_call["session_id"]

        record = load_run(resumed.tasks[0].run_id)
        assert record["resumed_from_run_id"] == interrupted_run_id
        assert record["rounds"][0]["builder"]["resume_used"] is True
        assert (record["rounds"][0]["builder"]["resume_session_ref"]
                == interrupted_builder_call["session_id"])

    def test_a_copy_mode_pause_falls_back_once_on_relaunch(
            self, isolate_data_root, demo_repo):
        # demo_repo is NOT a git repository: isolation_mode resolves to "copy", and
        # every run gets its own directory (DECISION F287 D5) -- unlike the worktree
        # the two tests above share across the park and the relaunch.
        job = parse_job_file(_ONE_TASK_JOB, str(demo_repo))
        stand_in, calls = self._make_stand_in(
            lambda: pc.request_pause(job.job_id, "mid-build pause", "cli"))

        with patch.object(pingpong_provider, "_guarded_cli_run", side_effect=stand_in), \
             patch.object(pingpong_provider.ClaudeCliProvider, "_get_claude_path",
                          lambda self: "/fake/claude"), \
             patch.object(pingpong_provider.ClaudeCliProvider, "_resolve_version",
                          lambda self: "1.0.0 (test)"):
            parked = run_job(
                job.job_id, builder_name="claude-cli", reviewer_name="claude-cli",
                builder_model="claude-sonnet-4-6", reviewer_model="claude-sonnet-4-6",
                repair_rounds=0)
            assert parked.state == JOB_PAUSED
            builder_calls = [c for c in calls if c["role"] == "builder"]
            assert len(builder_calls) == 1
            parked_builder_call = builder_calls[0]

            resumed = run_job(
                job.job_id, builder_name="claude-cli", reviewer_name="claude-cli",
                builder_model="claude-sonnet-4-6", reviewer_model="claude-sonnet-4-6",
                repair_rounds=0)

        assert resumed.state == JOB_COMPLETED
        relaunch_builder_calls = [c for c in calls if c["role"] == "builder"][1:]
        assert len(relaunch_builder_calls) == 2
        refused_call, fallback_call = relaunch_builder_calls
        assert refused_call["cwd"] != parked_builder_call["cwd"]
        assert refused_call["resume"] == parked_builder_call["session_id"]
        assert refused_call["session_id"] == ""
        assert fallback_call["resume"] == ""

        record = load_run(resumed.tasks[0].run_id)
        assert record["rounds"][0]["builder"]["resume_fallback"] is True
        assert record["rounds"][0]["builder"]["resume_used"] is False


class TestAnOfferedSessionAProviderCannotResumeIsNamed:
    """F287 T003 (DECISION F287 D7): a relaunch that offers a parked session to
    a provider that cannot resume it names the role and the reason under
    `resume_declined`, instead of dropping the offer without a trace."""

    def test_each_offered_role_names_its_providers_own_reason(self):
        assert resume_declined_reasons(
            {"builder": "b", "reviewer": "r"},
            builder=ClaudeProvider(), reviewer=OllamaPingPongProvider(),
        ) == {
            "builder": "the Anthropic API keeps no conversation between calls",
            "reviewer": "an Ollama chat call keeps no conversation between calls",
        }

    def test_a_provider_that_actually_supports_resume_declines_nothing(self):
        assert resume_declined_reasons(
            {"builder": "b", "reviewer": "r"},
            builder=ClaudeCliProvider(), reviewer=ClaudeCliProvider(),
        ) == {}

    def test_a_role_offered_no_session_is_absent_even_when_it_cannot_resume(self):
        assert resume_declined_reasons(
            {"builder": "b"},
            builder=FakeProvider(supports_resume=True), reviewer=FakeProvider(),
        ) == {}

    def test_run_pingpong_records_the_declined_roles_in_its_export_and_on_disk(
            self, isolate_data_root, demo_repo):
        p = FakeProvider(pass_on_round=1, fail_on_round=99, fake_session_id="sess-new")
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=p, reviewer_provider=p,
            resume_sessions={"builder": "sess-parked-b", "reviewer": "sess-parked-r"},
            resumed_from_run_id="parked-run",
        )
        assert result.final_status == "staged_review_passed"
        assert result.rounds[0].builder_output.resume_used is False
        assert result.rounds[0].reviewer_output.resume_used is False
        expected = {
            "builder": "the fake provider cannot resume a session",
            "reviewer": "the fake provider cannot resume a session",
        }
        assert export_pingpong_json(result)["resume_declined"] == expected
        assert load_run(result.run_id)["resume_declined"] == expected

    def test_a_run_offered_nothing_exports_an_empty_mapping(
            self, isolate_data_root, demo_repo):
        provider = _resuming("sess-1")
        result = run_pingpong("Fix README", str(demo_repo),
                              builder_provider=provider, reviewer_provider=provider)
        assert export_pingpong_json(result)["resume_declined"] == {}

    def test_the_relaunch_names_the_role_and_reason_the_provider_declined_to_resume(
            self, isolate_data_root, demo_repo):
        job = parse_job_file(_ONE_TASK_JOB, str(demo_repo))
        builder = PauseTriggerProvider(
            on_build=1,
            trigger=lambda: pc.request_pause(job.job_id, "mid-build pause", "cli"),
            pass_on_round=1, fail_on_round=99,
            supports_resume=True, fake_session_id="sess-parked")
        parked = run_job(job.job_id, builder_provider=builder,
                         reviewer_provider=_resuming("sess-parked-review"), repair_rounds=0)
        assert parked.state == JOB_PAUSED
        parked_run_id = parked.tasks[0].run_id
        assert parked_run_id

        resumed = run_job(
            job.job_id,
            builder_provider=FakeProvider(pass_on_round=1, fail_on_round=99),
            reviewer_provider=FakeProvider(pass_on_round=1, fail_on_round=99),
            repair_rounds=0,
        )
        assert resumed.state == JOB_COMPLETED
        record = load_run(resumed.tasks[0].run_id)
        assert record["resumed_from_run_id"] == parked_run_id
        assert record["rounds"][0]["builder"]["resume_used"] is False
        assert record["resume_declined"] == {
            "builder": "the fake provider cannot resume a session",
        }
