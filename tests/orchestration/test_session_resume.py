"""Tests for the F106 T001 session-resume capability surface.

Covers: every concrete provider (`FakeProvider`, `ClaudeProvider`,
`ClaudeCliProvider`) exposes `supports_resume` and reads `False` by
construction this round; `build`/`review` accept an additive `resume`
keyword on all three without changing behavior; `BuilderOutput`/
`ReviewerOutput` default `resume_used`/`resume_session_ref` to `False`/"".
`ClaudeProvider`/`ClaudeCliProvider` are checked by signature only — no
real call is made, matching tests/orchestration/test_provider_mode.py's
own no-network convention for those two classes.
"""

from __future__ import annotations

import dataclasses
import inspect

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
