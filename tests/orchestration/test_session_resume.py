"""Tests for the F106 session-resume capability surface (T001) and its
repair-path wiring (T002a, T002b-i, T002c-i, T002c-ii).

T001 covers: every concrete provider (`FakeProvider`, `ClaudeProvider`,
`ClaudeCliProvider`) exposes `supports_resume` and reads `False` by
construction this round; `build`/`review` accept an additive `resume`
keyword on all three without changing behavior; `BuilderOutput`/
`ReviewerOutput` default `resume_used`/`resume_session_ref` to `False`/"".
`ClaudeProvider`/`ClaudeCliProvider` are checked by signature only — no
real call is made, matching tests/orchestration/test_provider_mode.py's
own no-network convention for those two classes.

T002a covers: the repair round's Builder call actually passes `resume=`
built from the PRIOR round's captured session id, only when the Builder
provider honestly advertises `supports_resume`; every other path (initial
round, unsupported provider, no prior session id) passes `resume=None`.
`resume_used`/`resume_session_ref` land on the per-round `BuilderOutput`
only — surfacing them into the trust-bearing, closed-schema
`provider_evidence.json` is explicitly out of scope this round (see the
round's own step block). Real network/CLI providers are unaffected — this
round's production change lives only in the Builder call site of
`packages/orchestration/pingpong_loop.py`.

T002b-i covers the identical rule on the Reviewer side: the repair
round's PRIMARY `review()` attempt passes `resume=` built from the PRIOR
round's captured Reviewer session id, under the same three-way guard
(supported, is-repair, prior session id known). The bounded parse retry
(a separate call within the same round) is explicitly NOT threaded this
round — it always sends full context. `ReviewerOutput.resume_used`/
`resume_session_ref` land the same way `BuilderOutput`'s do.

T002c-i covers the Builder-side fallback-once rule: a resume attempt that
errors falls back ONCE, same round, to `resume=None`, recorded on the new
`BuilderOutput.resume_fallback` field — gated strictly on a resume having
actually been attempted, so a plain call failure is unaffected.
`FakeProvider`'s test-only `resume_fails` override makes this failure
mode reproducible without a real provider.

T002c-ii covers the identical rule on the Reviewer side: a resume attempt
that errors falls back ONCE, same round, to `resume=None`, recorded on the
new `ReviewerOutput.resume_fallback` field, under the same gating (a
resume must actually have been attempted). With both halves landed, T002c
is CLOSED; the delta-prompt shrink (T002b-ii) remains open.
"""

from __future__ import annotations

import dataclasses
import inspect
from pathlib import Path

import pytest

from packages.orchestration.pingpong_loop import run_pingpong
from packages.orchestration.pingpong_provider import (
    BuilderOutput,
    ClaudeCliProvider,
    ClaudeProvider,
    FakeProvider,
    ReviewerOutput,
)


class TestSupportsResumeDefaultsFalse:
    """Every adapter is honestly unsupported until T002 wires one."""

    def test_fake_provider_default_false(self):
        assert FakeProvider().supports_resume is False

    def test_fake_provider_constructor_override(self):
        assert FakeProvider(supports_resume=True).supports_resume is True

    def test_claude_provider_false(self):
        assert ClaudeProvider().supports_resume is False

    def test_claude_cli_provider_false(self):
        assert ClaudeCliProvider().supports_resume is False


class TestResumeParameterIsAdditive:
    """`resume` is accepted everywhere, with a `None` default, real call unmade."""

    def test_fake_provider_build_accepts_resume(self):
        sig = inspect.signature(FakeProvider.build)
        assert "resume" in sig.parameters
        assert sig.parameters["resume"].default is None

    def test_fake_provider_review_accepts_resume(self):
        sig = inspect.signature(FakeProvider.review)
        assert "resume" in sig.parameters
        assert sig.parameters["resume"].default is None

    def test_claude_provider_build_and_review_accept_resume(self):
        for meth in ("build", "review"):
            sig = inspect.signature(getattr(ClaudeProvider, meth))
            assert "resume" in sig.parameters
            assert sig.parameters["resume"].default is None

    def test_claude_cli_provider_build_and_review_accept_resume(self):
        for meth in ("build", "review"):
            sig = inspect.signature(getattr(ClaudeCliProvider, meth))
            assert "resume" in sig.parameters
            assert sig.parameters["resume"].default is None


class TestEvidenceFieldsDefault:
    """`resume_used`/`resume_session_ref` are honest, inert defaults."""

    def test_builder_output_defaults(self):
        out = BuilderOutput()
        assert out.resume_used is False
        assert out.resume_session_ref == ""

    def test_reviewer_output_defaults(self):
        out = ReviewerOutput()
        assert out.resume_used is False
        assert out.resume_session_ref == ""


class TestZeroBehaviorChange:
    """Passing `resume=` to `FakeProvider` changes nothing observable.

    `ClaudeProvider`/`ClaudeCliProvider` are excluded from this class: they
    require real network/CLI access to exercise `build`/`review` at all,
    which is out of scope for this round (their signatures are covered
    above; the behavior-equality property is the same by construction,
    since `resume` is accepted and unused on every adapter this round).
    """

    def test_build_identical_with_and_without_resume(self):
        plain = FakeProvider().build("do the thing")
        resumed = FakeProvider().build("do the thing", resume="some-session-ref")
        for field in dataclasses.fields(plain):
            assert getattr(plain, field.name) == getattr(resumed, field.name), field.name

    def test_review_identical_with_and_without_resume(self):
        plain = FakeProvider().review("do the thing")
        resumed = FakeProvider().review("do the thing", resume="some-session-ref")
        for field in dataclasses.fields(plain):
            assert getattr(plain, field.name) == getattr(resumed, field.name), field.name


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path: Path, monkeypatch):
    """Redirect REMEDY_DATA_DIR to tmp so tests don't write to the real data root."""
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


@pytest.fixture
def demo_repo(tmp_path: Path) -> Path:
    """Minimal demo repo, matching tests/orchestration/test_pingpong.py's own fixture."""
    (tmp_path / "README.md").write_text("# Demo\nA demo project.\n")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "README.md").write_text("# Docs\nDocumentation here.\n")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.py").write_text("def hello():\n    return 'hello'\n")
    (tmp_path / ".env").write_text("API_KEY=secret123\n")
    (tmp_path / ".env.local").write_text("DB_PASSWORD=hunter2\n")
    return tmp_path


class TestT002aBuilderResumeThreading:
    """The repair round's Builder call resumes only when honestly earned."""

    def test_repair_round_resumes_when_supported_and_session_known(self, demo_repo: Path):
        provider = FakeProvider(
            fail_on_round=1, pass_on_round=2,
            supports_resume=True, fake_session_id="sess-1",
        )
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            repair_rounds=2,
        )
        assert len(result.rounds) >= 2
        assert result.rounds[0].builder_output.resume_used is False
        assert result.rounds[0].builder_output.resume_session_ref == ""
        assert result.rounds[1].builder_output.resume_used is True
        assert result.rounds[1].builder_output.resume_session_ref == "sess-1"

    def test_repair_round_does_not_resume_when_provider_unsupported(self, demo_repo: Path):
        provider = FakeProvider(
            fail_on_round=1, pass_on_round=2,
            supports_resume=False, fake_session_id="sess-1",
        )
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            repair_rounds=2,
        )
        assert len(result.rounds) >= 2
        assert all(rd.builder_output.resume_used is False for rd in result.rounds)

    def test_repair_round_does_not_resume_without_a_prior_session_id(self, demo_repo: Path):
        provider = FakeProvider(fail_on_round=1, pass_on_round=2, supports_resume=True)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            repair_rounds=2,
        )
        assert len(result.rounds) >= 2
        assert all(rd.builder_output.resume_used is False for rd in result.rounds)

    def test_initial_round_never_resumes(self, demo_repo: Path):
        provider = FakeProvider(supports_resume=True, fake_session_id="sess-1")
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
        )
        assert result.rounds[0].builder_output.resume_used is False


class TestT002bReviewerResumeThreading:
    """The repair round's PRIMARY Reviewer attempt resumes only when earned."""

    def test_repair_round_resumes_when_supported_and_session_known(self, demo_repo: Path):
        provider = FakeProvider(
            fail_on_round=1, pass_on_round=2,
            supports_resume=True, fake_session_id="sess-1",
        )
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            repair_rounds=2,
        )
        assert len(result.rounds) >= 2
        assert result.rounds[0].reviewer_output.resume_used is False
        assert result.rounds[0].reviewer_output.resume_session_ref == ""
        assert result.rounds[1].reviewer_output.resume_used is True
        assert result.rounds[1].reviewer_output.resume_session_ref == "sess-1"

    def test_repair_round_does_not_resume_when_provider_unsupported(self, demo_repo: Path):
        provider = FakeProvider(
            fail_on_round=1, pass_on_round=2,
            supports_resume=False, fake_session_id="sess-1",
        )
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            repair_rounds=2,
        )
        assert len(result.rounds) >= 2
        assert all(rd.reviewer_output.resume_used is False for rd in result.rounds)

    def test_repair_round_does_not_resume_without_a_prior_session_id(self, demo_repo: Path):
        provider = FakeProvider(fail_on_round=1, pass_on_round=2, supports_resume=True)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            repair_rounds=2,
        )
        assert len(result.rounds) >= 2
        assert all(rd.reviewer_output.resume_used is False for rd in result.rounds)

    def test_initial_round_never_resumes(self, demo_repo: Path):
        provider = FakeProvider(supports_resume=True, fake_session_id="sess-1")
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
        )
        assert result.rounds[0].reviewer_output.resume_used is False


class TestT002cBuilderFallbackOnce:
    """A resume attempt that errors falls back once to full context, same round."""

    def test_resume_error_falls_back_and_round_completes(self, demo_repo: Path):
        provider = FakeProvider(
            fail_on_round=1, pass_on_round=2,
            supports_resume=True, fake_session_id="sess-1", resume_fails=True,
        )
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            repair_rounds=2,
        )
        assert len(result.rounds) >= 2
        assert result.rounds[1].builder_output.error == ""
        assert result.rounds[1].builder_output.resume_used is False
        assert result.rounds[1].builder_output.resume_fallback is True
        assert result.final_status == "staged_review_passed"

    def test_no_fallback_when_no_resume_attempted(self, demo_repo: Path):
        provider = FakeProvider(supports_resume=True, fake_session_id="sess-1", resume_fails=True)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
        )
        assert result.rounds[0].builder_output.error == ""
        assert result.rounds[0].builder_output.resume_fallback is False

    def test_no_fallback_when_provider_unsupported(self, demo_repo: Path):
        provider = FakeProvider(
            fail_on_round=1, pass_on_round=2,
            supports_resume=False, fake_session_id="sess-1", resume_fails=True,
        )
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            repair_rounds=2,
        )
        assert len(result.rounds) >= 2
        assert all(rd.builder_output.resume_fallback is False for rd in result.rounds)


class TestT002cReviewerFallbackOnce:
    """A resume attempt that errors falls back once to full context, same round."""

    def test_resume_error_falls_back_and_round_completes(self, demo_repo: Path):
        provider = FakeProvider(
            fail_on_round=1, pass_on_round=2,
            supports_resume=True, fake_session_id="sess-1", resume_fails=True,
        )
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            repair_rounds=2,
        )
        assert len(result.rounds) >= 2
        assert result.rounds[1].reviewer_output.error == ""
        assert result.rounds[1].reviewer_output.resume_used is False
        assert result.rounds[1].reviewer_output.resume_fallback is True
        assert result.final_status == "staged_review_passed"

    def test_no_fallback_when_no_resume_attempted(self, demo_repo: Path):
        provider = FakeProvider(supports_resume=True, fake_session_id="sess-1", resume_fails=True)
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
        )
        assert result.rounds[0].reviewer_output.error == ""
        assert result.rounds[0].reviewer_output.resume_fallback is False

    def test_no_fallback_when_provider_unsupported(self, demo_repo: Path):
        provider = FakeProvider(
            fail_on_round=1, pass_on_round=2,
            supports_resume=False, fake_session_id="sess-1", resume_fails=True,
        )
        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_provider=provider, reviewer_provider=provider,
            repair_rounds=2,
        )
        assert len(result.rounds) >= 2
        assert all(rd.reviewer_output.resume_fallback is False for rd in result.rounds)
