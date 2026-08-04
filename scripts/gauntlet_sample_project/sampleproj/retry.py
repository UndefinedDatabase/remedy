"""Retry backoff.

The cap is HARD-CODED on purpose: gauntlet order g01 asks for it to become
configurable while keeping this value as the default.
"""

#: Longest a single backoff may ever be, in seconds.
BACKOFF_CAP_SECONDS = 30

#: The first backoff, doubled on each following attempt.
BASE_BACKOFF_SECONDS = 1


def backoff_for(attempt: int) -> int:
    """Backoff in seconds for a 0-indexed attempt, never above the cap."""
    if attempt < 0:
        raise ValueError("attempt must be >= 0")
    return min(BASE_BACKOFF_SECONDS * (2 ** attempt), BACKOFF_CAP_SECONDS)


def backoff_series(attempts: int) -> list[int]:
    """The whole ladder, which is what a reader usually wants to see."""
    return [backoff_for(i) for i in range(attempts)]
