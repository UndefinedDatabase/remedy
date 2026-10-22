"""amend1015 Phase 1.1 — the closed words of the run story and their checker `story_problems`."""
from __future__ import annotations

from packages.orchestration.client_story_words import (
    STORY_PHRASES,
    STORY_REASONS,
    STORY_STEP_IDS,
    story_problems,
    story_words,
)


def test_the_words_are_published_as_plain_lists():
    words = story_words()
    assert words["step_ids"] == list(STORY_STEP_IDS)
    assert set(words["phrases"]) == set(STORY_PHRASES)
    assert set(words["reasons"]) == set(STORY_REASONS)
    assert {"tests_failed", "provider_unavailable", "budget_exhausted", "declined", "cancelled",
            "unknown"} <= set(words["reasons"])


def test_a_story_that_keeps_the_words_has_no_problem():
    story = {"state": "done", "state_detail": {"changed_files": 1},
             "next": {"action": "apply", "route": {"method": "POST", "path": "/api/v1/jobs/x/apply"}},
             "steps": [{"id": step, "status": "done", "phrase": None, "tokens": None}
                       for step in STORY_STEP_IDS]}
    story["steps"][0]["phrase"] = {"key": "found_files", "args": {"n": 1, "first": "README.md"}}
    story["steps"][2]["tasks"] = [{"title": "t", "status": "done", "rounds": 2, "files": []}]
    assert story_problems(story) == []


def test_the_checker_refuses_a_word_outside_the_lists():
    story = {"state": "done", "state_detail": {"reason": {"key": "lost", "args": {}}},
             "next": {"action": "push"}, "steps": [
                 {"id": "reading", "status": "done", "tokens": None,
                  "phrase": {"key": "found_files", "args": {"n": 1, "first": "/etc/passwd"}}}]}
    problems = story_problems(story)
    assert any("lost" in p for p in problems)
    assert any("next.action" in p for p in problems)
    assert any("five steps" in p for p in problems)
    assert any("inside the repository" in p for p in problems)
    assert story_problems({**story, "order": "costs $5"}) != []


def test_the_checker_reads_the_dirty_start_phrase_too():
    """R-1328: `dirty_start` is a phrase of the closed list, with its two counts and nothing else."""
    story = {"state": "done", "next": {"action": "none", "route": None},
             "steps": [{"id": step, "status": "done", "phrase": None} for step in STORY_STEP_IDS]}
    good = {"key": "dirty_start", "args": {"captured": 1, "preserved": 2}}
    assert story_problems({**story, "dirty_start": good}) == []
    assert story_problems({**story, "dirty_start": None}) == []
    assert story_problems({**story, "dirty_start": {"key": "dirty_start", "args": {"captured": 1}}}) != []
    assert story_problems({**story, "dirty_start": {"key": "dirty", "args": {}}}) != []
