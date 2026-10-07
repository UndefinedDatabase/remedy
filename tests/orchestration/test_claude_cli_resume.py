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
from unittest.mock import MagicMock, patch

import pytest

from packages.orchestration import pingpong_provider
from packages.orchestration.pingpong_provider import ClaudeCliProvider, build_claude_cli_args

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
