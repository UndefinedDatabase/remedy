"""amend1015 P1.1: every persisted task status maps to exactly one cockpit lifecycle word."""
from __future__ import annotations

import pytest

from packages.orchestration.run_manifest import VALID_TASK_STATUSES
from packages.orchestration.task_lifecycle import (
    TASK_LIFECYCLE_WORDS,
    task_lifecycle,
)


def test_every_valid_task_status_has_one_lifecycle_word():
    for status in sorted(VALID_TASK_STATUSES):
        assert task_lifecycle(status) in TASK_LIFECYCLE_WORDS, status


def test_a_finished_do_task_is_done():
    # The do lane finishes its task as applied_to_job_workspace (amend1015, Part 1).
    for status in ("applied_to_job_workspace", "passed", "completed"):
        assert task_lifecycle(status) == "done", status


def test_the_other_words():
    assert task_lifecycle("pending") == "planned"
    assert task_lifecycle("running") == "open"
    for status in ("blocked", "failed", "vetoed"):
        assert task_lifecycle(status) == "blocked", status
    assert task_lifecycle("skipped") == "skipped"


def test_an_unknown_status_raises():
    with pytest.raises(ValueError, match="no lifecycle"):
        task_lifecycle("half-done")
