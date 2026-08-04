"""Backoff: doubling, and the cap that stops it."""
import pytest

from sampleproj.retry import BACKOFF_CAP_SECONDS, backoff_for, backoff_series


def test_the_first_backoff_is_the_base():
    assert backoff_for(0) == 1


def test_backoff_doubles_until_it_reaches_the_cap():
    assert backoff_series(4) == [1, 2, 4, 8]


def test_the_cap_holds():
    assert backoff_for(20) == BACKOFF_CAP_SECONDS


def test_a_negative_attempt_is_refused():
    with pytest.raises(ValueError, match="attempt must be >= 0"):
        backoff_for(-1)
