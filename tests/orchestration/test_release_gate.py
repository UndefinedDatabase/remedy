"""Seeded-failure tests for the release gate (T2_F086 T003).

T2_F086's Acceptance names four refusals — red CI, tag/version mismatch, missing
changelog section, budget breach — and asks for one test each. Every test below
starts from a request that PASSES and changes exactly one field, so if the
accepting case ever stops accepting, its own test fails first rather than the
others going quietly meaningless.
"""

from __future__ import annotations

from dataclasses import replace

import pytest

from packages.orchestration.release_gate import (
    WHEEL_SIZE_BUDGET_BYTES,
    ReleaseRequest,
    changelog_section,
    normalise_tag,
    refuse_release,
)

CHANGELOG = """# Changelog

## [1.2.3] - 2026-01-01

### Added
- A thing that was added.

## [1.2.2] - 2025-12-01

### Fixed
- A thing that was fixed.
"""

ACCEPTING = ReleaseRequest(
    tag="v1.2.3",
    version="1.2.3",
    changelog=CHANGELOG,
    wheel_bytes=2_040_197,
    ci_green=True,
)


def _with(**changes) -> ReleaseRequest:
    """The accepting release with exactly `changes` applied."""
    return replace(ACCEPTING, **changes)


@pytest.mark.unit
class TestTheGateAccepts:
    def test_a_sound_release_is_not_refused(self):
        assert refuse_release(ACCEPTING) == ()

    def test_a_bare_tag_without_the_v_prefix_also_matches(self):
        assert refuse_release(_with(tag="1.2.3")) == ()
        assert normalise_tag("1.2.3") == "1.2.3"


@pytest.mark.unit
class TestTheGateRefuses:
    """One test per refusal T2_F086's Acceptance names."""

    def test_red_ci_is_refused(self):
        assert any("CI is not green" in r for r in refuse_release(_with(ci_green=False)))

    def test_a_tag_that_does_not_match_the_version_is_refused(self):
        reasons = refuse_release(_with(tag="v9.9.9"))
        assert any("does not match distribution version" in r for r in reasons)

    def test_a_missing_changelog_section_is_refused(self):
        reasons = refuse_release(_with(version="4.5.6", tag="v4.5.6"))
        assert any("no section for version" in r for r in reasons)

    def test_an_empty_changelog_section_is_refused(self):
        empty = "# Changelog\n\n## [1.2.3] - 2026-01-01\n\n## [1.2.2] - 2025-12-01\n\n- x\n"
        assert any("is empty" in r for r in refuse_release(_with(changelog=empty)))

    def test_a_wheel_over_the_budget_is_refused(self):
        reasons = refuse_release(_with(wheel_bytes=WHEEL_SIZE_BUDGET_BYTES + 1))
        assert any("over the" in r and "budget" in r for r in reasons)

    def test_a_wheel_exactly_at_the_budget_is_not_refused(self):
        assert refuse_release(_with(wheel_bytes=WHEEL_SIZE_BUDGET_BYTES)) == ()

    def test_every_broken_rule_is_named_not_only_the_first(self):
        reasons = refuse_release(
            _with(ci_green=False, tag="v9.9.9", wheel_bytes=WHEEL_SIZE_BUDGET_BYTES + 1)
        )
        assert len(reasons) == 3


@pytest.mark.unit
class TestChangelogParsing:
    def test_a_section_runs_only_to_the_next_heading(self):
        body = changelog_section(CHANGELOG, "1.2.3")
        assert "A thing that was added." in body
        assert "A thing that was fixed." not in body

    def test_an_absent_version_has_no_section(self):
        assert changelog_section(CHANGELOG, "0.0.0-absent") is None

    def test_the_last_section_runs_to_the_end_of_the_file(self):
        body = changelog_section(CHANGELOG, "1.2.2")
        assert "A thing that was fixed." in body
