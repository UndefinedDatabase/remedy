"""Adaptive provider timeouts and retry policy (F001).

Defines timeout profiles (fast, normal, patient) that compute role-aware,
task-size-aware timeouts. Retry logic for transient provider failures
(timeout, nonzero exit) with bounded backoff. Never retries review rejects.

Public API:
    PROFILES             — dict of named TimeoutProfile instances
    compute_timeout()    — seconds for a given role + file count + profile
    should_retry()       — whether a provider failure is retryable
    next_backoff()       — backoff seconds for attempt N
    RETRY_BACKOFFS       — backoff schedule [30, 120]
    MAX_RETRIES          — hard cap on retry attempts
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TimeoutProfile:
    """Timeout parameters for a named profile.

    builder_base_s / reviewer_base_s: base timeout per role.
    per_allowed_file_s: added per file in allowed_files.
    cap_s: hard ceiling.
    """
    builder_base_s: int = 600
    reviewer_base_s: int = 300
    per_allowed_file_s: int = 60
    cap_s: int = 2400


PROFILES: dict[str, TimeoutProfile] = {
    "fast": TimeoutProfile(
        builder_base_s=180,
        reviewer_base_s=90,
        per_allowed_file_s=15,
        cap_s=600,
    ),
    "normal": TimeoutProfile(
        builder_base_s=600,
        reviewer_base_s=300,
        per_allowed_file_s=60,
        cap_s=2400,
    ),
    "patient": TimeoutProfile(
        builder_base_s=1200,
        reviewer_base_s=600,
        per_allowed_file_s=120,
        cap_s=7200,
    ),
}

RETRY_BACKOFFS: list[int] = [30, 120]
MAX_RETRIES: int = len(RETRY_BACKOFFS)


def compute_timeout(
    role: str,
    allowed_files: int,
    profile: TimeoutProfile | str = "normal",
) -> int:
    """Compute timeout in seconds for a provider call.

    Args:
        role: "builder" or "reviewer".
        allowed_files: number of files the task touches.
        profile: a TimeoutProfile instance or profile name string.

    Returns:
        Timeout in seconds, capped by profile.cap_s.
        Builder timeout is always >= reviewer timeout for the same inputs.

    Raises:
        ValueError: unknown profile name or invalid role.
    """
    if isinstance(profile, str):
        if profile not in PROFILES:
            raise ValueError(
                f"Unknown timeout profile {profile!r}. "
                f"Available: {', '.join(sorted(PROFILES))}"
            )
        profile = PROFILES[profile]

    if role == "builder":
        base = profile.builder_base_s
    elif role == "reviewer":
        base = profile.reviewer_base_s
    else:
        raise ValueError(f"Unknown role {role!r}. Expected 'builder' or 'reviewer'.")

    files = max(0, allowed_files)
    raw = base + files * profile.per_allowed_file_s
    return min(raw, profile.cap_s)


def is_timeout_error(error: str | None) -> bool:
    """Does this provider error string mean "the call timed out"?

    THE timeout predicate — the retry path and F010's classifier both call this one
    function, because two definitions of "timed out" drift apart.

    It recognises the wording the provider ACTUALLY emits. ``ClaudeCliProvider`` raises
    ``claude CLI timed out after 600s``, which contains neither ``timeout`` nor
    ``TimeoutExpired``: the reviewed build therefore neither retried a real Claude timeout
    nor classified one, and reported it as ``unknown``. ``timed out`` is now matched too.
    Timeout profiles, values, retry count and backoff are untouched — only the RECOGNITION
    of a timeout was wrong, and it was wrong in both places at once.
    """
    if not error:
        return False
    lowered = error.lower()
    return "timeout" in lowered or "timed out" in lowered or "TimeoutExpired" in error


def is_nonzero_exit_error(error: str | None) -> bool:
    """Does this provider error string mean "the process exited non-zero"?

    Same story as :func:`is_timeout_error`: extracted verbatim from the retry path, not
    re-derived. Matches the messages the retry policy already treated as a non-zero exit.
    """
    if not error:
        return False
    lowered = error.lower()
    return "exited" in lowered or "nonzero" in lowered


def should_retry(
    *,
    is_timeout: bool = False,
    exit_code: int | None = None,
    is_review_reject: bool = False,
) -> bool:
    """Decide whether a provider failure should be retried.

    Retries on: timeout, nonzero process exit.
    Never retries: review rejects (needs_repair, fail, blocked).
    """
    if is_review_reject:
        return False
    if is_timeout:
        return True
    if exit_code is not None and exit_code != 0:
        return True
    return False


def next_backoff(attempt: int) -> int | None:
    """Return backoff seconds for the given attempt (0-indexed).

    Returns None if no more retries are allowed.
    """
    if attempt < 0 or attempt >= len(RETRY_BACKOFFS):
        return None
    return RETRY_BACKOFFS[attempt]
