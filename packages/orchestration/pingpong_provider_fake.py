"""The deterministic fake provider of the ping-pong loop, for automated tests.

F307 moved it here from ``pingpong_provider.py`` as that file's structural step (3) in
``docs/system/structure-ledger-v1.md``; ``create_provider`` there builds its subclass
``DeliverableFakeProvider`` (``fake_deliverable.py``) by the name ``fake``.
"""
from __future__ import annotations

from typing import Any

from packages.orchestration.call_identity import prepare_call_input
from packages.orchestration.pingpong_provider import BuilderOutput, ReviewerOutput, ReviewFinding

#: The tokens each fake build and each fake review reports (R-1323, DECISION F307 D20): fixed
#: numbers in the claude CLI's usage keys, so a fake run's ledger rows carry tokens as a real run's
#: do. The fake reports no cost, so its calls stay unpriced.
FAKE_BUILD_USAGE = {"input_tokens": 1200, "output_tokens": 300, "cache_read": 0, "cache_creation": 0}
FAKE_REVIEW_USAGE = {"input_tokens": 800, "output_tokens": 200, "cache_read": 0, "cache_creation": 0}


def fake_usage_actuals(usage: dict[str, int], session_id: str) -> dict[str, Any]:
    """One fake call's usage block: USAGE, a null cost, and SESSION_ID when the fake has one."""
    actuals: dict[str, Any] = {**usage, "total_cost_usd": None}
    if session_id:
        actuals["session_id"] = session_id
    return actuals


class FakeProvider:
    """Deterministic fake provider for automated testing.

    Round 1: Builder makes changes, Reviewer finds issues.
    Round 2: Builder repairs, Reviewer passes.
    Configurable via constructor for different test scenarios.
    """

    def __init__(
        self,
        *,
        builder_files: list[str] | None = None,
        fail_on_round: int = 1,
        pass_on_round: int = 2,
        max_rounds_before_block: int = 99,
        builder_error: str = "",
        reviewer_error: str = "",
        malformed_review: bool = False,
        malformed_review_recoverable: bool = False,
        supports_resume: bool = False,
        fake_session_id: str = "",
        resume_fails: bool = False,
    ) -> None:
        self._builder_files = builder_files or ["docs/README.md"]
        self._supports_resume = supports_resume
        self._fake_session_id = fake_session_id
        self._resume_fails = resume_fails
        self._fail_round = fail_on_round
        self._pass_round = pass_on_round
        self._max_block = max_rounds_before_block
        self._builder_error = builder_error
        self._reviewer_error = reviewer_error
        self._malformed_review = malformed_review
        self._malformed_review_recoverable = malformed_review_recoverable
        self._build_count = 0
        self._review_count = 0

    @property
    def name(self) -> str:
        return "fake"

    @property
    def supports_resume(self) -> bool:
        return self._supports_resume

    def build(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
        resume: str | None = None,
    ) -> BuilderOutput:
        self._build_count += 1
        if self._builder_error:
            return BuilderOutput(
                error=self._builder_error,
                provider="fake",
            )
        # F106 T002c: a test-only way to simulate a resume attempt that
        # errors, so the fallback-once path in pingpong_loop.py has
        # something real to fall back FROM. Only fires when a resume was
        # actually requested on a provider that claims to support it —
        # never on a plain (non-resume) call.
        if resume and self._supports_resume and self._resume_fails:
            return BuilderOutput(
                error="resume_lost: session context unavailable",
                provider="fake",
            )
        is_repair = self._build_count > 1
        # F106 T002a: honor an incoming resume request only when this fake was
        # constructed to support it — an unsupported provider's output is
        # byte-identical whether or not a caller passes ``resume``.
        resume_used = bool(resume) and self._supports_resume
        usage_actuals = fake_usage_actuals(FAKE_BUILD_USAGE, self._fake_session_id)
        return BuilderOutput(
            summary=f"{'Repair' if is_repair else 'Initial'} changes (round {self._build_count})",
            files_changed=list(self._builder_files),
            commands_suggested=[],
            assumptions=["Minimal changes only"],
            provider="fake",
            duration_ms=50,
            tokens_used=100,
            usage_actuals=usage_actuals,
            resume_used=resume_used,
            resume_session_ref=resume if resume_used else "",
            prepared_input=prepare_call_input(
                prompt=prompt, model="fake", mode="fake",
                options={"max_output_chars": max_output_chars}),
        )

    def review(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
        resume: str | None = None,
    ) -> ReviewerOutput:
        # F106 T002c: a test-only way to simulate a resume attempt that
        # errors, so the fallback-once path in pingpong_loop.py has
        # something real to fall back FROM. Only fires when a resume was
        # actually requested on a provider that claims to support it —
        # never on a plain (non-resume) call.
        if resume and self._supports_resume and self._resume_fails:
            return ReviewerOutput(
                error="resume_lost: session context unavailable",
                provider="fake",
            )
        out = self._review_impl(prompt, timeout_sec=timeout_sec,
                                max_output_chars=max_output_chars)
        # F106 T002b: honor an incoming resume request only when this fake
        # was constructed to support it — mirrors FakeProvider.build (T002a).
        out.resume_used = bool(resume) and self._supports_resume
        out.resume_session_ref = resume if out.resume_used else ""
        if not out.error:
            out.usage_actuals = fake_usage_actuals(FAKE_REVIEW_USAGE, self._fake_session_id)
        elif self._fake_session_id:
            out.usage_actuals = {"session_id": self._fake_session_id}
        out.prepared_input = prepare_call_input(
            prompt=prompt, model="fake", mode="fake",
            options={"max_output_chars": max_output_chars})
        return out

    def _review_impl(
        self,
        prompt: str,
        *,
        timeout_sec: int = 120,
        max_output_chars: int = 50000,
    ) -> ReviewerOutput:
        self._review_count += 1
        if self._reviewer_error:
            return ReviewerOutput(
                error=self._reviewer_error,
                provider="fake",
            )
        if self._malformed_review:
            return ReviewerOutput(
                verdict="",
                raw_text="not valid json {{{",
                error="malformed_output: no JSON found in reviewer response",
                provider="fake",
            )
        if self._malformed_review_recoverable and self._review_count == 1:
            return ReviewerOutput(
                verdict="",
                raw_text="Here is my review:\n{bad json",
                error="malformed_output: JSON parse error",
                provider="fake",
            )
        if self._review_count >= self._max_block:
            return ReviewerOutput(
                verdict="blocked",
                summary="Max rounds reached",
                provider="fake",
            )
        if self._review_count >= self._pass_round:
            return ReviewerOutput(
                verdict="pass",
                confidence="high",
                summary="All changes look correct after repair.",
                provider="fake",
                duration_ms=30,
                tokens_used=80,
            )
        # Findings on early rounds
        return ReviewerOutput(
            verdict="needs_repair",
            findings=[
                ReviewFinding(
                    id=f"R-{self._review_count:04d}",
                    severity="medium",
                    file=self._builder_files[0] if self._builder_files else "",
                    summary="Missing verification note",
                    details="The change is incomplete — add a verification note.",
                    required_fix="Add a verification note at the end of the file.",
                ),
            ],
            confidence="medium",
            summary=f"Found 1 issue in round {self._review_count}.",
            provider="fake",
            duration_ms=30,
            tokens_used=80,
        )
