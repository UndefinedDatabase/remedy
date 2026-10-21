"""R-1323, DECISION F307 D20: the fake provider reports fixed token numbers and no cost."""
from __future__ import annotations

from packages.orchestration.pingpong_provider_fake import (
    FAKE_BUILD_USAGE,
    FAKE_REVIEW_USAGE,
    FakeProvider,
    fake_usage_actuals,
)

_KEYS = {"input_tokens", "output_tokens", "cache_read", "cache_creation"}


def test_a_build_and_a_review_report_their_fixed_tokens_and_no_cost():
    fake = FakeProvider()

    build = fake.build("make it")
    review = fake.review("check it")

    assert build.usage_actuals == {**FAKE_BUILD_USAGE, "total_cost_usd": None}
    assert review.usage_actuals == {**FAKE_REVIEW_USAGE, "total_cost_usd": None}
    assert set(FAKE_BUILD_USAGE) == set(FAKE_REVIEW_USAGE) == _KEYS
    assert all(FAKE_BUILD_USAGE[key] >= 0 and FAKE_REVIEW_USAGE[key] >= 0 for key in _KEYS)
    assert FAKE_BUILD_USAGE["input_tokens"] > 0 and FAKE_REVIEW_USAGE["output_tokens"] > 0


def test_a_fake_with_a_session_keeps_it_beside_its_tokens():
    fake = FakeProvider(fake_session_id="sess-1")

    assert fake.build("make it").usage_actuals["session_id"] == "sess-1"
    assert fake.review("check it").usage_actuals["session_id"] == "sess-1"
    assert "session_id" not in fake_usage_actuals(FAKE_BUILD_USAGE, "")


def test_a_call_that_failed_reports_no_tokens():
    assert FakeProvider(builder_error="provider_unavailable: down").build("make it").usage_actuals is None
    assert FakeProvider(reviewer_error="provider_unavailable: down").review("check it").usage_actuals is None
