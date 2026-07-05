"""Tests for provider_timeouts (F001 — adaptive provider timeouts + retry)."""
from __future__ import annotations

import pytest

from packages.orchestration.provider_timeouts import (
    MAX_RETRIES,
    PROFILES,
    RETRY_BACKOFFS,
    TimeoutProfile,
    compute_timeout,
    next_backoff,
    should_retry,
)


# ---------------------------------------------------------------------------
# Profile sanity
# ---------------------------------------------------------------------------

class TestProfiles:
    def test_three_profiles_exist(self):
        assert set(PROFILES) == {"fast", "normal", "patient"}

    def test_builder_base_gte_reviewer_base(self):
        for name, p in PROFILES.items():
            assert p.builder_base_s >= p.reviewer_base_s, f"{name}: builder < reviewer"

    def test_fast_cap_lt_normal_cap(self):
        assert PROFILES["fast"].cap_s < PROFILES["normal"].cap_s

    def test_normal_cap_lt_patient_cap(self):
        assert PROFILES["normal"].cap_s < PROFILES["patient"].cap_s


# ---------------------------------------------------------------------------
# compute_timeout
# ---------------------------------------------------------------------------

class TestComputeTimeout:
    def test_builder_zero_files_normal(self):
        assert compute_timeout("builder", 0, "normal") == 600

    def test_reviewer_zero_files_normal(self):
        assert compute_timeout("reviewer", 0, "normal") == 300

    def test_builder_gt_reviewer_same_inputs(self):
        for profile_name in PROFILES:
            for files in (0, 1, 5, 20):
                b = compute_timeout("builder", files, profile_name)
                r = compute_timeout("reviewer", files, profile_name)
                assert b >= r, f"{profile_name}/{files}: builder({b}) < reviewer({r})"

    def test_per_file_increment(self):
        p = PROFILES["normal"]
        t0 = compute_timeout("builder", 0, p)
        t5 = compute_timeout("builder", 5, p)
        assert t5 == t0 + 5 * p.per_allowed_file_s

    def test_cap_respected(self):
        for name, p in PROFILES.items():
            huge = compute_timeout("builder", 9999, p)
            assert huge == p.cap_s, f"{name}: exceeded cap"

    def test_negative_files_treated_as_zero(self):
        assert compute_timeout("builder", -3, "normal") == compute_timeout("builder", 0, "normal")

    def test_profile_by_name(self):
        assert compute_timeout("builder", 0, "fast") == PROFILES["fast"].builder_base_s

    def test_profile_by_instance(self):
        p = TimeoutProfile(builder_base_s=100, reviewer_base_s=50, per_allowed_file_s=10, cap_s=500)
        assert compute_timeout("builder", 3, p) == 130
        assert compute_timeout("reviewer", 3, p) == 80

    def test_unknown_profile_raises(self):
        with pytest.raises(ValueError, match="Unknown timeout profile"):
            compute_timeout("builder", 0, "turbo")

    def test_unknown_role_raises(self):
        with pytest.raises(ValueError, match="Unknown role"):
            compute_timeout("planner", 0, "normal")

    def test_all_profiles_x_roles_x_files(self):
        """Matrix test: 3 profiles × 2 roles × several file counts."""
        file_counts = [0, 1, 3, 10, 50, 200]
        for pname in PROFILES:
            for role in ("builder", "reviewer"):
                prev = -1
                for fc in file_counts:
                    t = compute_timeout(role, fc, pname)
                    assert t > 0
                    assert t >= prev, "timeout should be monotonically non-decreasing with files"
                    assert t <= PROFILES[pname].cap_s
                    prev = t


# ---------------------------------------------------------------------------
# should_retry
# ---------------------------------------------------------------------------

class TestShouldRetry:
    def test_timeout_retries(self):
        assert should_retry(is_timeout=True) is True

    def test_nonzero_exit_retries(self):
        assert should_retry(exit_code=1) is True
        assert should_retry(exit_code=137) is True

    def test_zero_exit_no_retry(self):
        assert should_retry(exit_code=0) is False

    def test_review_reject_never_retries(self):
        assert should_retry(is_review_reject=True) is False
        assert should_retry(is_review_reject=True, is_timeout=True) is False
        assert should_retry(is_review_reject=True, exit_code=1) is False

    def test_no_failure_no_retry(self):
        assert should_retry() is False


# ---------------------------------------------------------------------------
# next_backoff
# ---------------------------------------------------------------------------

class TestNextBackoff:
    def test_first_backoff(self):
        assert next_backoff(0) == 30

    def test_second_backoff(self):
        assert next_backoff(1) == 120

    def test_exhausted(self):
        assert next_backoff(2) is None
        assert next_backoff(99) is None

    def test_negative(self):
        assert next_backoff(-1) is None

    def test_max_retries_matches_backoffs(self):
        assert MAX_RETRIES == len(RETRY_BACKOFFS)
