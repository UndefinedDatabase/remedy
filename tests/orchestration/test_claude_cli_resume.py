"""The `claude-cli` provider carries a validated session reference on every call path.

DECISION F287 D2 (round 2, T001 first half): `build_claude_cli_args` gains a
validated `resume_session` keyword, and `ClaudeCliProvider` threads `resume`
through `build`/`review`, `_build_impl`/`_review_impl` and every `_call*`
seam, recording `resume_used`/`resume_session_ref` on a call that actually
resumed. `supports_resume` stays False this round: no production call passes
a resume yet. No real `claude` process runs here — the JSON paths patch
`packages.orchestration.pingpong_provider._guarded_cli_run` and the streamed
paths patch `packages.orchestration.stream_evidence.run_streamed_command`.
"""
from __future__ import annotations

import json
import subprocess
from unittest.mock import MagicMock, patch

import pytest

from packages.orchestration import pingpong_provider
from packages.orchestration.call_identity import prepare_call_input
from packages.orchestration.pingpong_loop import PingPongResult, _call_with_retry
from packages.orchestration.pingpong_provider import (
    _REVIEWER_JSON_SCHEMA,
    ClaudeCliProvider,
    _ReviewVerdictSchema,
    _to_json_schema_str,
    build_claude_cli_args,
)
from packages.orchestration.provider_timeouts import is_nonzero_exit_error, is_timeout_error
from packages.orchestration.rate_governor import is_rate_limit_error

#: The resume reference every test below resumes with.
REF = "5f0c2a1e-7b3d-4c9a-9e21-0d6f4b8a3c11"

_SO = {"schema_v": "rv1", "verdict": "pass", "findings": [],
       "confidence": "high", "summary": "ok"}


def _provider(**kw) -> ClaudeCliProvider:
    prov = ClaudeCliProvider(**kw)
    prov._claude_path = "/fake/claude"
    prov._cli_version = "1.0.0 (test)"
    prov._cli_version_resolved = True
    return prov


def _json_child(stdout: str, *, rc: int = 0, stderr: str = ""):
    proc = MagicMock(returncode=rc, stdout=stdout, stderr=stderr)
    return patch.object(pingpong_provider, "_guarded_cli_run", return_value=proc)


def _envelope(**kw) -> str:
    base = {"type": "result", "subtype": "success", "is_error": False}
    base.update(kw)
    return json.dumps(base)


class TestBuildClaudeCliArgsCarriesTheResumeReference:
    def test_resume_appends_two_adjacent_items_before_allowed_tools(self) -> None:
        argv = build_claude_cli_args(
            "claude", "P", resume_session=REF, write_mode="allowed-tools")
        idx = argv.index("--resume")
        assert argv[idx:idx + 2] == ["--resume", REF]
        assert idx < argv.index("--allowedTools")

    def test_without_resume_session_the_argv_has_no_resume_flag(self) -> None:
        argv = build_claude_cli_args("claude", "P")
        assert "--resume" not in argv

    @pytest.mark.parametrize("bad_ref", [
        "--dangerously-skip-permissions", "-r", "a b", "a/b", "x" * 129,
    ])
    def test_an_invalid_reference_raises_value_error(self, bad_ref: str) -> None:
        with pytest.raises(ValueError):
            build_claude_cli_args("claude", "P", resume_session=bad_ref)


class TestBuilderJsonPathRecordsResume:
    def test_success_sends_resume_and_records_it(self) -> None:
        proc = MagicMock(returncode=0, stdout=_envelope(result="done", session_id=REF), stderr="")
        with patch.object(pingpong_provider, "_guarded_cli_run", return_value=proc) as guarded:
            out = _provider().build("B", resume=REF)
        argv = guarded.call_args[0][0]
        idx = argv.index("--resume")
        assert argv[idx:idx + 2] == ["--resume", REF]
        assert out.resume_used is True
        assert out.resume_session_ref == REF

    def test_without_resume_sends_no_resume_and_defaults_stay_false(self) -> None:
        proc = MagicMock(returncode=0, stdout=_envelope(result="done"), stderr="")
        with patch.object(pingpong_provider, "_guarded_cli_run", return_value=proc) as guarded:
            out = _provider().build("B")
        argv = guarded.call_args[0][0]
        assert "--resume" not in argv
        assert out.resume_used is False
        assert out.resume_session_ref == ""


class TestBuilderFailurePathNeverRecordsResume:
    def test_a_nonzero_exit_keeps_resume_defaults(self) -> None:
        with _json_child("", rc=1, stderr="boom"):
            out = _provider().build("B", resume=REF)
        assert out.error
        assert out.resume_used is False
        assert out.resume_session_ref == ""


class TestBuilderBadReferenceIsRefusedBeforeAnyCall:
    def test_bad_reference_never_reaches_the_stand_in(self) -> None:
        with patch.object(pingpong_provider, "_guarded_cli_run") as guarded:
            out = _provider().build("B", resume="--dangerously-skip-permissions")
        assert "refusing to resume" in out.error
        assert out.resume_used is False
        guarded.assert_not_called()


class TestStructuredReviewerJsonPathRecordsResume:
    def test_success_sends_resume_and_records_it(self, monkeypatch) -> None:
        monkeypatch.delenv("REMEDY_REVIEWER_FREETEXT", raising=False)
        proc = MagicMock(returncode=0, stdout=_envelope(structured_output=_SO), stderr="")
        with patch.object(pingpong_provider, "_guarded_cli_run", return_value=proc) as guarded:
            out = _provider().review("R", resume=REF)
        argv = guarded.call_args[0][0]
        idx = argv.index("--resume")
        assert argv[idx:idx + 2] == ["--resume", REF]
        assert out.verdict == "pass"
        assert out.resume_used is True
        assert out.resume_session_ref == REF


class TestFreeTextReviewerRecordsResume:
    def test_success_sends_resume_and_records_it(self, monkeypatch) -> None:
        monkeypatch.setenv("REMEDY_REVIEWER_FREETEXT", "1")
        passing = json.dumps(
            {"verdict": "pass", "findings": [], "confidence": "high", "summary": "ok"})
        proc = MagicMock(returncode=0, stdout=_envelope(result=passing), stderr="")
        with patch.object(pingpong_provider, "_guarded_cli_run", return_value=proc) as guarded:
            out = _provider().review("R", resume=REF)
        argv = guarded.call_args[0][0]
        idx = argv.index("--resume")
        assert argv[idx:idx + 2] == ["--resume", REF]
        assert out.resume_used is True


class TestStreamedPathsCarryResumeAndNeverRecordOnError:
    def test_streamed_builder_hands_the_stand_in_a_resume_argv(self, tmp_path) -> None:
        captured: dict = {}

        def _stub(argv, out_dir, **kwargs):
            captured["argv"] = argv
            raise RuntimeError("stand-in stop")

        with patch("packages.orchestration.stream_evidence.run_streamed_command", _stub):
            prov = _provider(stream_evidence=True, stream_evidence_dir=str(tmp_path))
            out = prov.build("B", resume=REF)
        idx = captured["argv"].index("--resume")
        assert captured["argv"][idx:idx + 2] == ["--resume", REF]
        assert out.error
        assert out.resume_used is False

    def test_streamed_structured_reviewer_hands_the_stand_in_a_resume_argv(
        self, tmp_path, monkeypatch,
    ) -> None:
        monkeypatch.delenv("REMEDY_REVIEWER_FREETEXT", raising=False)
        captured: dict = {}

        def _stub(argv, out_dir, **kwargs):
            captured["argv"] = argv
            raise RuntimeError("stand-in stop")

        with patch("packages.orchestration.stream_evidence.run_streamed_command", _stub):
            prov = _provider(stream_evidence=True, stream_evidence_dir=str(tmp_path))
            out = prov.review("R", resume=REF)
        idx = captured["argv"].index("--resume")
        assert captured["argv"][idx:idx + 2] == ["--resume", REF]
        assert out.error
        assert out.resume_used is False


class TestPreparedInputFingerprintChangesOnlyWithResume:
    def test_a_resumed_call_differs_and_two_fresh_calls_agree(self) -> None:
        proc = MagicMock(returncode=0, stdout=_envelope(result="done"), stderr="")
        with patch.object(pingpong_provider, "_guarded_cli_run", return_value=proc):
            with_resume = _provider().build("B", resume=REF)
            fresh1 = _provider().build("B")
            fresh2 = _provider().build("B")
        assert with_resume.prepared_input.fingerprint != fresh1.prepared_input.fingerprint
        assert fresh1.prepared_input.fingerprint == fresh2.prepared_input.fingerprint


class TestSupportsResumeStaysFalse:
    def test_supports_resume_is_false(self) -> None:
        assert ClaudeCliProvider().supports_resume is False


class TestAFreshCallsFingerprintIsUnchangedByF287:
    """R-1161: a call with no `resume` fingerprints exactly as it did before DECISION
    F287 D2 added `resume` threading — the new keyword must never become a silent
    extra material input for the ordinary, non-resuming call."""

    def test_a_fresh_build_fingerprint_equals_the_direct_formula(self) -> None:
        proc = MagicMock(returncode=0, stdout=_envelope(result="done"), stderr="")
        with patch.object(pingpong_provider, "_guarded_cli_run", return_value=proc):
            out = _provider().build("B")
        expected = prepare_call_input(
            prompt="B", model="", mode="cli-legacy", options={"write_mode": "none"})
        assert out.prepared_input.fingerprint == expected.fingerprint

    def test_a_fresh_structured_review_fingerprint_equals_the_direct_formula(
        self, monkeypatch,
    ) -> None:
        monkeypatch.delenv("REMEDY_REVIEWER_FREETEXT", raising=False)
        proc = MagicMock(returncode=0, stdout=_envelope(structured_output=_SO), stderr="")
        with patch.object(pingpong_provider, "_guarded_cli_run", return_value=proc):
            out = _provider().review("R")
        expected = prepare_call_input(
            prompt="R", model="", mode="cli-native",
            schema=_to_json_schema_str(_ReviewVerdictSchema),
            options={"write_mode": "none"})
        assert out.prepared_input.fingerprint == expected.fingerprint

    def test_a_fresh_freetext_review_fingerprint_equals_the_direct_formula(
        self, monkeypatch,
    ) -> None:
        monkeypatch.setenv("REMEDY_REVIEWER_FREETEXT", "1")
        passing = json.dumps(
            {"verdict": "pass", "findings": [], "confidence": "high", "summary": "ok"})
        proc = MagicMock(returncode=0, stdout=_envelope(result=passing), stderr="")
        with patch.object(pingpong_provider, "_guarded_cli_run", return_value=proc):
            out = _provider().review("R")
        expected = prepare_call_input(
            prompt="R" + "\n\n" + _REVIEWER_JSON_SCHEMA, model="", mode="cli-legacy",
            options={"write_mode": "none"})
        assert out.prepared_input.fingerprint == expected.fingerprint


class TestAReviewerErrorOutputNeverClaimsAResume:
    """R-1161: a reviewer call that asked to resume but came back unparseable must
    never report that it continued an earlier conversation — `resume_used` and
    `resume_session_ref` stay at their honest defaults on every error path."""

    def test_freetext_malformed_output_never_claims_a_resume(self, monkeypatch) -> None:
        monkeypatch.setenv("REMEDY_REVIEWER_FREETEXT", "1")
        proc = MagicMock(returncode=0, stdout=_envelope(result="no json here"), stderr="")
        with patch.object(pingpong_provider, "_guarded_cli_run", return_value=proc):
            out = _provider().review("R", resume=REF)
        assert out.error
        assert out.resume_used is False
        assert out.resume_session_ref == ""

    def test_structured_malformed_verdict_never_claims_a_resume(self, monkeypatch) -> None:
        monkeypatch.delenv("REMEDY_REVIEWER_FREETEXT", raising=False)
        proc = MagicMock(
            returncode=0,
            stdout=_envelope(structured_output={"schema_v": "rv1", "verdict": "nope"}),
            stderr="",
        )
        with patch.object(pingpong_provider, "_guarded_cli_run", return_value=proc):
            out = _provider().review("R", resume=REF)
        assert out.error
        assert out.resume_used is False
        assert out.resume_session_ref == ""


class TestARefusedResumeIsNotRetried:
    """DECISION F287 D3: a failed claude-cli call that was given a resume answers
    `resume_refused:` instead of `provider_error:` — a string none of the transport
    retry predicates match — so `_call_with_retry` returns it at once instead of
    spending the 30s/120s backoff on a conversation the CLI already refused to
    continue. A call with no resume keeps its old `provider_error:` text and its
    old retry count, unchanged."""

    #: The stderr a real `claude --resume <ref>` call prints for a dead session.
    _REFUSAL_STDERR = "No conversation found with session ID: " + REF

    def test_builder_nonzero_exit_with_resume_answers_resume_refused_and_matches_no_retry_predicate(
        self,
    ) -> None:
        with _json_child("", rc=1, stderr=self._REFUSAL_STDERR):
            out = _provider().build("B", resume=REF)
        assert out.error.startswith("resume_refused:")
        assert is_timeout_error(out.error) is False
        assert is_nonzero_exit_error(out.error) is False
        assert is_rate_limit_error(out.error) is False
        assert out.exit_code == 1
        assert "No conversation found" in out.stderr_tail

    def test_builder_timeout_with_resume_answers_resume_refused_and_matches_no_timeout_predicate(
        self,
    ) -> None:
        with patch.object(
            pingpong_provider, "_guarded_cli_run",
            side_effect=subprocess.TimeoutExpired(["claude"], 5),
        ):
            out = _provider().build("B", resume=REF)
        assert out.error.startswith("resume_refused:")
        assert is_timeout_error(out.error) is False

    def test_structured_reviewer_nonzero_exit_with_resume_answers_resume_refused(
        self, monkeypatch,
    ) -> None:
        monkeypatch.delenv("REMEDY_REVIEWER_FREETEXT", raising=False)
        with _json_child("", rc=1, stderr=self._REFUSAL_STDERR):
            out = _provider().review("R", resume=REF)
        assert out.error.startswith("resume_refused:")

    def test_builder_nonzero_exit_without_resume_keeps_provider_error_unchanged(self) -> None:
        with _json_child("", rc=1, stderr=self._REFUSAL_STDERR):
            out = _provider().build("B")
        assert out.error.startswith("provider_error:")
        assert is_nonzero_exit_error(out.error) is True

    @patch("packages.orchestration.pingpong_loop._time.sleep")
    def test_call_with_retry_runs_a_resumed_builder_failure_once_but_retries_a_plain_one(
        self, _sleep,
    ) -> None:
        calls = {"n": 0}

        def _stand_in(cmd, timeout_sec, cwd):
            calls["n"] += 1
            return MagicMock(returncode=1, stdout="", stderr=self._REFUSAL_STDERR)

        with patch.object(pingpong_provider, "_guarded_cli_run", side_effect=_stand_in):
            result = PingPongResult(job_id="J1", task_id="T001")
            out = _call_with_retry(
                lambda: _provider().build("B", resume=REF),
                result=result, role="builder", provider="claude-cli",
            )
        assert calls["n"] == 1
        assert result.retries_used == 0
        assert out.error.startswith("resume_refused:")

        calls["n"] = 0
        with patch.object(pingpong_provider, "_guarded_cli_run", side_effect=_stand_in):
            result2 = PingPongResult(job_id="J1", task_id="T001")
            out2 = _call_with_retry(
                lambda: _provider().build("B"),
                result=result2, role="builder", provider="claude-cli",
            )
        assert calls["n"] == 3
        assert result2.retries_used == 2
        assert out2.error.startswith("provider_error:")

    @patch("packages.orchestration.pingpong_loop._time.sleep")
    def test_call_with_retry_runs_a_resumed_reviewer_failure_once(
        self, _sleep, monkeypatch,
    ) -> None:
        monkeypatch.delenv("REMEDY_REVIEWER_FREETEXT", raising=False)
        calls = {"n": 0}

        def _stand_in(cmd, timeout_sec, cwd):
            calls["n"] += 1
            return MagicMock(returncode=1, stdout="", stderr=self._REFUSAL_STDERR)

        with patch.object(pingpong_provider, "_guarded_cli_run", side_effect=_stand_in):
            result = PingPongResult(job_id="J1", task_id="T001")
            out = _call_with_retry(
                lambda: _provider().review("R", resume=REF),
                result=result, role="reviewer", provider="claude-cli",
            )
        assert calls["n"] == 1
        assert out.error.startswith("resume_refused:")
