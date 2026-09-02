"""F105 T003 site-6 content-equality golden for the reviewer prompt.

This is the golden that pins `packages.orchestration.pingpong_loop`'s reviewer
prompt while its composition moves to the prompt-segment registry. It is the
LAST of the six T003 migration sites and the worst-ordered of them: the feature
file (docs/roadmap/features/T2_F105.md) asks for content equality "modulo
ordering", and here the rank-3 job context (`reviewer_scope`,
`reviewer_scope_contract`) moves ahead of the rank-4 `reviewer_goal`, and in the
fallback branch the rank-4 `reviewer_task_input` moves ahead of the rank-5
`reviewer_repair`. So the composed string is NOT byte-equal to the pre-migration
render except in the shape that has nothing to reorder; what is pinned here is
that the segment BYTES are unchanged and that reassembling them in the
pre-migration order reproduces the old render exactly.

The reviewer prompt has two MUTUALLY EXCLUSIVE branches — a scope packet is
present or it is not — and they emit different segments, so both are covered by
two fixture shapes each. The branch stays a branch over which segments are
REGISTERED: one unconditional registry would emit both diff shapes and both
scope shapes at once, which is a content change.

Unlike sites 1-3 this reviewer has no single template to freeze, so what is
frozen is the RENDER. `_FROZEN_RENDERS` below is the output of
`_build_reviewer_prompt` at commit 554d9521 for the four fixture shapes. It was
obtained by checking that commit out into a disposable `git worktree`, rendering
the four shapes there, and writing `repr()` of each render straight into this
file. Not one character of prompt text was retyped by hand.

It must NEVER be edited to make a failing test pass. An intentional change to
the prompt's CONTENT is precisely the event this file exists to fail on: if a
future change is meant to alter the words, that change updates these constants
in its own reviewed diff, with the content change declared, and never as a
side-effect of getting a red suite green.
"""
from __future__ import annotations

import hashlib

import pytest

from packages.orchestration.artifact_summary import FALLBACK_MARKER
from packages.orchestration.pingpong_loop import (
    _OVERSIZED_REVIEWER_SCOPED_DIFF_THRESHOLD_CHARS,
    _build_reviewer_prompt,
    _reviewer_tiered_diff_text,
    compose_reviewer_prompt,
)
from packages.orchestration.pingpong_provider import ReviewFinding
from packages.orchestration.prompt_segments import (
    PROMPT_SEGMENT_DELIMITER,
    ComposedPrompt,
)

#: The frozen renders. The first four were captured mechanically at 554d9521
#: (see the module docstring); "scoped_resumed" and "fallback_resumed" did
#: not exist at that commit and were captured the same way against THIS
#: branch instead — running `compose_reviewer_prompt` once per shape with
#: `resume_hunks_text` set and writing `repr()` of the pre-migration-order
#: reconstruction straight into this file (F106 round 14). NEVER edited to
#: make a failing test pass, the same rule as the other four.
_FROZEN_RENDERS = {
    'scoped_minimal': "You are a code Reviewer.\nReview the builder's changes against the original goal.\nBe strict but fair. Only flag real issues.\nReturn ONLY valid JSON. No markdown. No code fence. No explanation outside JSON.\n\n\n\n## Original Goal\nMake the widget resize with its container.\n\n## Review Scope Packet\nTask: Resize the widget\n\n### Changed Files\n- packages/widget.py | lines: 10-24 | symbols: resize | risk: public_api\n\n### Recommended Scope: hunk_only\nReason: Only two hunks changed.\nRecommended scope is `hunk_only`: focus only on the listed hunks (changed line ranges) and the related tests.\n\n### Related Tests\n- tests/test_widget.py\n\n### Evidence Refs\n- task_runs/T001/safe.diff\n\n### Prompt Hashes\nabc123\n\n### Estimated Review Tokens: 512\n\nFiles listed in changed_files and related_tests are within review scope unless the original goal explicitly forbids them. Do not flag those files as out-of-scope merely because they are tests or support files.\nFocus on the listed files/hunks unless risk tags or the scope reason require escalation.\nYou may escalate scope if you find evidence of broader issues, but state why.\n\n## Builder Summary\nRewrote resize() to read the container width first.\n",
    'scoped_full': "You are a code Reviewer.\nReview the builder's changes against the original goal.\nBe strict but fair. Only flag real issues.\nReturn ONLY valid JSON. No markdown. No code fence. No explanation outside JSON.\n\n\n\n## Original Goal\nMake the widget resize with its container.\n\n## Review Scope Packet\nTask: Resize the widget\n\n### Changed Files\n- packages/widget.py | lines: 10-24 | symbols: resize | risk: public_api\n\n### Recommended Scope: hunk_only\nReason: Only two hunks changed.\nRecommended scope is `hunk_only`: focus only on the listed hunks (changed line ranges) and the related tests.\n\n### Related Tests\n- tests/test_widget.py\n\n### Evidence Refs\n- task_runs/T001/safe.diff\n\n### Prompt Hashes\nabc123\n\n### Estimated Review Tokens: 512\n\nFiles listed in changed_files and related_tests are within review scope unless the original goal explicitly forbids them. Do not flag those files as out-of-scope merely because they are tests or support files.\nFocus on the listed files/hunks unless risk tags or the scope reason require escalation.\nYou may escalate scope if you find evidence of broader issues, but state why.\n\n## Scope Contract\nTouch only packages/widget.py.\n\n\n## RE-REVIEW — Repair Round 2\nThe Builder was asked to fix the findings below.\nFor each prior finding:\n1. Check if the fix is present in the diff and confirmed by tests.\n2. If fixed, do NOT re-report it.\n3. If NOT fixed or incorrectly fixed, re-report with the SAME ID.\n4. Report any NEW issues introduced by the repair as new findings.\n5. If tests fail, treat test failure as evidence of unfixed issues.\n6. Do NOT return pass if any prior finding is unfixed.\n7. Do NOT return pass if the repair introduced new problems.\n\n### Prior Findings\n\n- [high] R-0001: resize ignores the container width\n- [low] R-0002: stale comment above resize\n\n## Builder Summary\nRewrote resize() to read the container width first.\n\n## Focused Staged Diff\n```diff\n--- a/widget.py\n+++ b/widget.py\n+    resize()\n```\n\n## Test Result\n3 passed in 0.10s\n",
    'fallback_minimal': "You are a code Reviewer.\nReview the builder's changes against the original goal.\nBe strict but fair. Only flag real issues.\nReturn ONLY valid JSON. No markdown. No code fence. No explanation outside JSON.\n\n\n\n## Original Goal\nMake the widget resize with its container.\n\n## Builder Summary\nRewrote resize() to read the container width first.\n",
    'fallback_full': "You are a code Reviewer.\nReview the builder's changes against the original goal.\nBe strict but fair. Only flag real issues.\nReturn ONLY valid JSON. No markdown. No code fence. No explanation outside JSON.\n\n\n\n## Original Goal\nMake the widget resize with its container.\n\n## Scope Contract\nTouch only packages/widget.py.\n\n\n## RE-REVIEW — Repair Round 2\nThe Builder was asked to fix the findings below.\nFor each prior finding:\n1. Check if the fix is present in the diff and confirmed by tests.\n2. If fixed, do NOT re-report it.\n3. If NOT fixed or incorrectly fixed, re-report with the SAME ID.\n4. Report any NEW issues introduced by the repair as new findings.\n5. If tests fail, treat test failure as evidence of unfixed issues.\n6. Do NOT return pass if any prior finding is unfixed.\n7. Do NOT return pass if the repair introduced new problems.\n\n### Prior Findings\n\n- [high] R-0001: resize ignores the container width\n- [low] R-0002: stale comment above resize\n\n## Task Input Summary\nTask hash: 9f2b1c4d\nTask size: ~128 tokens\n\nResize the widget, keep the aspect ratio.\n\n## Builder Summary\nRewrote resize() to read the container width first.\n\n## Files Changed\n- packages/widget.py\n- tests/test_widget.py\n\n## Staged Unified Diff\n```diff\n--- a/widget.py\n+++ b/widget.py\n+    resize()\n```\n\n## Test Result\n3 passed in 0.10s\n",
    "scoped_resumed": "You are a code Reviewer.\nReview the builder's changes against the original goal.\nBe strict but fair. Only flag real issues.\nReturn ONLY valid JSON. No markdown. No code fence. No explanation outside JSON.\n\n\n\n## Original Goal\nMake the widget resize with its container.\n\n## Review Scope Packet\nTask: Resize the widget\n\n### Changed Files\n- packages/widget.py | lines: 10-24 | symbols: resize | risk: public_api\n\n### Recommended Scope: hunk_only\nReason: Only two hunks changed.\nRecommended scope is `hunk_only`: focus only on the listed hunks (changed line ranges) and the related tests.\n\n### Related Tests\n- tests/test_widget.py\n\n### Evidence Refs\n- task_runs/T001/safe.diff\n\n### Prompt Hashes\nabc123\n\n### Estimated Review Tokens: 512\n\nFiles listed in changed_files and related_tests are within review scope unless the original goal explicitly forbids them. Do not flag those files as out-of-scope merely because they are tests or support files.\nFocus on the listed files/hunks unless risk tags or the scope reason require escalation.\nYou may escalate scope if you find evidence of broader issues, but state why.\n\n## Scope Contract\nTouch only packages/widget.py.\n\n\n## RE-REVIEW — Repair Round 2\nThe Builder was asked to fix the findings below.\nFor each prior finding:\n1. Check if the fix is present in the diff and confirmed by tests.\n2. If fixed, do NOT re-report it.\n3. If NOT fixed or incorrectly fixed, re-report with the SAME ID.\n4. Report any NEW issues introduced by the repair as new findings.\n5. If tests fail, treat test failure as evidence of unfixed issues.\n6. Do NOT return pass if any prior finding is unfixed.\n7. Do NOT return pass if the repair introduced new problems.\n\n### Prior Findings\n\n- [high] R-0001: resize ignores the container width\n- [low] R-0002: stale comment above resize\n\n## Builder Summary\nRewrote resize() to read the container width first.\n\n## Resumed Session — Changed Regions Only\n\n### widget.py (lines 1-1)\n```\n    resize()\n```\n\n## Test Result\n3 passed in 0.10s\n",
    "fallback_resumed": "You are a code Reviewer.\nReview the builder's changes against the original goal.\nBe strict but fair. Only flag real issues.\nReturn ONLY valid JSON. No markdown. No code fence. No explanation outside JSON.\n\n\n\n## Original Goal\nMake the widget resize with its container.\n\n## Scope Contract\nTouch only packages/widget.py.\n\n\n## RE-REVIEW — Repair Round 2\nThe Builder was asked to fix the findings below.\nFor each prior finding:\n1. Check if the fix is present in the diff and confirmed by tests.\n2. If fixed, do NOT re-report it.\n3. If NOT fixed or incorrectly fixed, re-report with the SAME ID.\n4. Report any NEW issues introduced by the repair as new findings.\n5. If tests fail, treat test failure as evidence of unfixed issues.\n6. Do NOT return pass if any prior finding is unfixed.\n7. Do NOT return pass if the repair introduced new problems.\n\n### Prior Findings\n\n- [high] R-0001: resize ignores the container width\n- [low] R-0002: stale comment above resize\n\n## Task Input Summary\nTask hash: 9f2b1c4d\nTask size: ~128 tokens\n\nResize the widget, keep the aspect ratio.\n\n## Builder Summary\nRewrote resize() to read the container width first.\n\n## Files Changed\n- packages/widget.py\n- tests/test_widget.py\n\n## Resumed Session — Changed Regions Only\n\n### widget.py (lines 1-1)\n```\n    resize()\n```\n\n## Test Result\n3 passed in 0.10s\n",
}

#: Short, literal fixture values — the same ones the frozen renders were
#: captured with. Changing any of them invalidates every frozen render above.
_GOAL = "Make the widget resize with its container."
_BUILDER_SUMMARY = "Rewrote resize() to read the container width first."
_SCOPE_CONTRACT = "## Scope Contract\nTouch only packages/widget.py."
_SAFE_DIFF = "--- a/widget.py\n+++ b/widget.py\n+    resize()"
#: F106 T002b-ii step 2b, Reviewer side — the same pre-rendered hunk
#: selection fixture round 12 used for the Builder side, fed straight to
#: `compose_reviewer_prompt` as `resume_hunks_text`; that function performs
#: no rendering of its own.
_RESUME_HUNKS_TEXT = (
    "## Resumed Session — Changed Regions Only\n"
    "\n"
    "### widget.py (lines 1-1)\n"
    "```\n"
    "    resize()\n"
    "```\n"
)
_TEST_RESULT = "3 passed in 0.10s"
_FILES_CHANGED = ["packages/widget.py", "tests/test_widget.py"]
_TASK_EXCERPT = "Resize the widget, keep the aspect ratio."
_TASK_SHA256 = "9f2b1c4d"
_TASK_TOKENS = 128
_REPAIR_ROUND = 2

_PRIOR_FINDINGS = [
    ReviewFinding(
        id="R-0001",
        severity="high",
        file="packages/widget.py",
        summary="resize ignores the container width",
        required_fix="read the container width before resizing",
    ),
    ReviewFinding(
        id="R-0002",
        severity="low",
        file="packages/widget.py",
        summary="stale comment above resize",
    ),
]

#: A small but complete review scope packet. Its presence is what selects the
#: SCOPED branch of the reviewer prompt; its absence selects the fallback.
_SCOPE_PACKET = {
    "schema_version": "1.0.0",
    "task_id": "T001",
    "task_title": "Resize the widget",
    "changed_files": ["packages/widget.py"],
    "changed_line_ranges": {"packages/widget.py": [[10, 24]]},
    "changed_symbols": {"packages/widget.py": ["resize"]},
    "risk_tags": {"packages/widget.py": ["public_api"]},
    "prompt_hashes": ["abc123"],
    "evidence_refs": ["task_runs/T001/safe.diff"],
    "related_tests": ["tests/test_widget.py"],
    "open_findings": [],
    "estimated_review_tokens": 512,
    "recommended_scope": "hunk_only",
    "scope_reason": "Only two hunks changed.",
}

#: The shapes the golden covers, two per mutually exclusive branch: the
#: scoped branch with nothing but its packet, with everything, and (F106
#: T002b-ii step 2b) with everything plus a resumed session's shrunk diff;
#: the fallback branch the same three ways.
_SHAPES: dict[str, dict] = {
    "scoped_minimal": dict(scope_packet=_SCOPE_PACKET),
    "scoped_full": dict(
        scope_packet=_SCOPE_PACKET,
        scope_contract=_SCOPE_CONTRACT,
        prior_findings=_PRIOR_FINDINGS,
        repair_round=_REPAIR_ROUND,
        safe_diff=_SAFE_DIFF,
        test_result=_TEST_RESULT,
    ),
    "scoped_resumed": dict(
        scope_packet=_SCOPE_PACKET,
        scope_contract=_SCOPE_CONTRACT,
        prior_findings=_PRIOR_FINDINGS,
        repair_round=_REPAIR_ROUND,
        safe_diff=_SAFE_DIFF,
        test_result=_TEST_RESULT,
        resume_hunks_text=_RESUME_HUNKS_TEXT,
    ),
    "fallback_minimal": {},
    "fallback_full": dict(
        scope_contract=_SCOPE_CONTRACT,
        prior_findings=_PRIOR_FINDINGS,
        repair_round=_REPAIR_ROUND,
        task_excerpt=_TASK_EXCERPT,
        task_sha256=_TASK_SHA256,
        task_tokens_estimated=_TASK_TOKENS,
        files_changed=_FILES_CHANGED,
        safe_diff=_SAFE_DIFF,
        test_result=_TEST_RESULT,
    ),
    "fallback_resumed": dict(
        scope_contract=_SCOPE_CONTRACT,
        prior_findings=_PRIOR_FINDINGS,
        repair_round=_REPAIR_ROUND,
        task_excerpt=_TASK_EXCERPT,
        task_sha256=_TASK_SHA256,
        task_tokens_estimated=_TASK_TOKENS,
        files_changed=_FILES_CHANGED,
        safe_diff=_SAFE_DIFF,
        test_result=_TEST_RESULT,
        resume_hunks_text=_RESUME_HUNKS_TEXT,
    ),
}

#: The order the pre-migration `parts` list emitted these segments in. ONE list
#: serves both branches: no shape ever carries a segment from both, and the
#: segments they share kept the same relative order on either side of the
#: branch. Ordering the composed segments by THIS and joining them must give
#: back the frozen render byte for byte — that is what "content equality modulo
#: ordering" means at this site.
_PRE_MIGRATION_ORDER = (
    "reviewer_system",
    "reviewer_goal",
    "reviewer_spec_compliance",
    "reviewer_scope",
    "reviewer_scope_contract",
    "reviewer_repair",
    "reviewer_task_input",
    "reviewer_builder_summary",
    "reviewer_files_changed",
    "reviewer_focused_diff",
    "reviewer_staged_diff",
    "reviewer_test_result",
)


def _composed(shape: str) -> ComposedPrompt:
    return compose_reviewer_prompt(_GOAL, _BUILDER_SUMMARY, **_SHAPES[shape])


def _segment_bounds(composed: ComposedPrompt) -> dict[str, tuple[int, int]]:
    """Each segment's [start, end) character span inside ``composed.text``.

    The manifest carries `chars` per segment, so the spans are computed rather
    than guessed by splitting on the delimiter — the reviewer's segments contain
    blank lines of their own and a split would shred them.
    """
    bounds: dict[str, tuple[int, int]] = {}
    position = 0
    for entry in composed.manifest:
        bounds[entry.name] = (position, position + entry.chars)
        position += entry.chars + len(PROMPT_SEGMENT_DELIMITER)
    assert position - len(PROMPT_SEGMENT_DELIMITER) == len(composed.text)
    return bounds


def _segment_texts(composed: ComposedPrompt) -> dict[str, str]:
    """The composed text sliced back into its segments, verified by hash."""
    texts: dict[str, str] = {}
    bounds = _segment_bounds(composed)
    for entry in composed.manifest:
        start, end = bounds[entry.name]
        chunk = composed.text[start:end]
        assert hashlib.sha256(chunk.encode("utf-8")).hexdigest() == entry.sha256
        texts[entry.name] = chunk
    return texts


@pytest.mark.parametrize("shape", sorted(_SHAPES))
def test_segments_reassemble_into_the_frozen_render(shape):
    composed = _composed(shape)
    texts = _segment_texts(composed)

    ordered = [texts[name] for name in _PRE_MIGRATION_ORDER if name in texts]
    assert len(ordered) == len(texts)
    assert sorted(ordered) == sorted(texts.values())

    assert PROMPT_SEGMENT_DELIMITER.join(ordered) == _FROZEN_RENDERS[shape]

    frozen_hashes = sorted(
        hashlib.sha256(part.encode("utf-8")).hexdigest() for part in ordered
    )
    assert sorted(entry.sha256 for entry in composed.manifest) == frozen_hashes


def test_the_reorder_is_real():
    """`fallback_minimal` has nothing to reorder; both full shapes move bytes."""
    assert (_composed("fallback_minimal").text
            == _FROZEN_RENDERS["fallback_minimal"])
    for shape in ("scoped_full", "fallback_full"):
        assert _composed(shape).text != _FROZEN_RENDERS[shape], shape


@pytest.mark.parametrize("shape", sorted(_SHAPES))
def test_manifest_ranks_are_non_decreasing(shape):
    ranks = [entry.rank for entry in _composed(shape).manifest]
    assert ranks == sorted(ranks)


def test_the_scoped_full_shape_registers_its_segments_in_rank_order():
    composed = _composed("scoped_full")
    assert tuple(entry.name for entry in composed.manifest) == (
        "reviewer_system",
        "reviewer_scope",
        "reviewer_scope_contract",
        "reviewer_goal",
        "reviewer_repair",
        "reviewer_builder_summary",
        "reviewer_focused_diff",
        "reviewer_test_result",
    )
    assert tuple(entry.rank for entry in composed.manifest) == (
        0, 3, 3, 4, 5, 5, 5, 5)


def test_the_fallback_full_shape_registers_its_segments_in_rank_order():
    composed = _composed("fallback_full")
    assert tuple(entry.name for entry in composed.manifest) == (
        "reviewer_system",
        "reviewer_scope_contract",
        "reviewer_goal",
        "reviewer_task_input",
        "reviewer_repair",
        "reviewer_builder_summary",
        "reviewer_files_changed",
        "reviewer_staged_diff",
        "reviewer_test_result",
    )
    assert tuple(entry.rank for entry in composed.manifest) == (
        0, 3, 4, 4, 5, 5, 5, 5, 5)


def test_the_rank_inversions_are_fixed_in_the_manifest():
    """Positional string checks would pass by accident; assert on the manifest."""
    scoped = [entry.name for entry in _composed("scoped_full").manifest]
    assert scoped.index("reviewer_scope") < scoped.index("reviewer_goal")
    assert scoped.index("reviewer_scope_contract") < scoped.index("reviewer_goal")

    fallback = [entry.name for entry in _composed("fallback_full").manifest]
    assert (fallback.index("reviewer_scope_contract")
            < fallback.index("reviewer_goal"))
    assert (fallback.index("reviewer_task_input")
            < fallback.index("reviewer_repair"))

    frozen = _FROZEN_RENDERS["scoped_full"]
    goal_at = frozen.index("## Original Goal")
    assert frozen.index("## Review Scope Packet") > goal_at
    assert frozen.index("## Scope Contract") > goal_at

    frozen = _FROZEN_RENDERS["fallback_full"]
    assert frozen.index("## Scope Contract") > frozen.index("## Original Goal")
    assert (frozen.index("## Task Input Summary")
            > frozen.index("## RE-REVIEW — Repair Round 2"))


@pytest.mark.parametrize("shape", sorted(_SHAPES))
def test_build_reviewer_prompt_returns_the_composed_text(shape):
    built = _build_reviewer_prompt(_GOAL, _BUILDER_SUMMARY, **_SHAPES[shape])
    assert isinstance(built, str)
    assert built == _composed(shape).text


class TestResumeHunksTextReplacesTheDiffOnEitherBranch:
    """F106 T002b-ii step 2b, Reviewer side (DECISION F106 D1(b)) — a resumed
    session's diff segment carries the pre-rendered hunk selection instead of
    the capped diff, on BOTH the scoped and fallback branches, in the SAME
    segment name/rank each branch already uses."""

    def test_scoped_resumed_keeps_scoped_fulls_segment_order_and_ranks(self):
        scoped_full = _composed("scoped_full")
        scoped_resumed = _composed("scoped_resumed")
        assert (tuple(e.name for e in scoped_resumed.manifest)
                == tuple(e.name for e in scoped_full.manifest))
        assert (tuple(e.rank for e in scoped_resumed.manifest)
                == tuple(e.rank for e in scoped_full.manifest))

    def test_fallback_resumed_keeps_fallback_fulls_segment_order_and_ranks(self):
        fallback_full = _composed("fallback_full")
        fallback_resumed = _composed("fallback_resumed")
        assert (tuple(e.name for e in fallback_resumed.manifest)
                == tuple(e.name for e in fallback_full.manifest))
        assert (tuple(e.rank for e in fallback_resumed.manifest)
                == tuple(e.rank for e in fallback_full.manifest))

    def test_scoped_resumeds_diff_segment_is_the_raw_render(self):
        texts = _segment_texts(_composed("scoped_resumed"))
        assert texts["reviewer_focused_diff"] == _RESUME_HUNKS_TEXT.rstrip("\n")

    def test_fallback_resumeds_diff_segment_is_the_raw_render(self):
        texts = _segment_texts(_composed("fallback_resumed"))
        assert texts["reviewer_staged_diff"] == _RESUME_HUNKS_TEXT.rstrip("\n")

    def test_scoped_fulls_diff_segment_is_unchanged_by_resumed_existing(self):
        texts = _segment_texts(_composed("scoped_full"))
        assert texts["reviewer_focused_diff"] == (
            "## Focused Staged Diff\n```diff\n" + _SAFE_DIFF + "\n```"
        )

    def test_fallback_fulls_diff_segment_is_unchanged_by_resumed_existing(self):
        texts = _segment_texts(_composed("fallback_full"))
        assert texts["reviewer_staged_diff"] == (
            "## Staged Unified Diff\n```diff\n" + _SAFE_DIFF + "\n```"
        )

    def test_an_empty_resume_hunks_text_falls_back_to_the_full_diff_scoped(self):
        """No `test_result` follows here, so this diff segment is the LAST
        rank-5 segment and keeps its own trailing newline — unlike
        `scoped_full`'s same segment above, which `test_result` follows."""
        composed = compose_reviewer_prompt(
            _GOAL, _BUILDER_SUMMARY, scope_packet=_SCOPE_PACKET,
            safe_diff=_SAFE_DIFF, resume_hunks_text="",
        )
        texts = _segment_texts(composed)
        assert texts["reviewer_focused_diff"] == (
            "## Focused Staged Diff\n```diff\n" + _SAFE_DIFF + "\n```\n"
        )

    def test_an_empty_resume_hunks_text_falls_back_to_the_full_diff_fallback(self):
        """No `test_result` follows here either, same last-segment reasoning
        as the scoped case above."""
        composed = compose_reviewer_prompt(
            _GOAL, _BUILDER_SUMMARY, safe_diff=_SAFE_DIFF, resume_hunks_text="",
        )
        texts = _segment_texts(composed)
        assert texts["reviewer_staged_diff"] == (
            "## Staged Unified Diff\n```diff\n" + _SAFE_DIFF + "\n```\n"
        )


class TestTieredDiffTextReplacesTheScopedFlatCap:
    """F108 T003b-ii (DECISION F108 D4) -- mirrors the builder side's
    ``TestTieredDiffTextReplacesTheFlatCap`` exactly, for the new
    ``tiered_diff_text`` parameter, but on the SCOPED branch only: the
    fallback branch never sees ``tiered_diff_text`` (test 4 below)."""

    _TIERED_DIFF_TEXT = (
        "## Current Staged Diff (summarized)\n"
        "a tiered two-file diff summary\n"
        "\n"
        "### widget.py (file:widget.py)\n"
        "widget.py's resize now reads the container width\n"
        "\n"
        "Full diff: reviewer diff, round 8 (F108: not yet persisted to evidence) "
        "(12345 characters)\n"
    )

    def test_tiered_diff_text_replaces_the_scoped_flat_capped_diff(self):
        composed = compose_reviewer_prompt(
            _GOAL, _BUILDER_SUMMARY, scope_packet=_SCOPE_PACKET,
            safe_diff=_SAFE_DIFF, test_result=_TEST_RESULT,
            tiered_diff_text=self._TIERED_DIFF_TEXT,
        )
        texts = _segment_texts(composed)
        assert texts["reviewer_focused_diff"] == self._TIERED_DIFF_TEXT.rstrip("\n")

    def test_resume_hunks_text_still_takes_precedence_over_tiered_diff_text_on_scoped(self):
        composed = compose_reviewer_prompt(
            _GOAL, _BUILDER_SUMMARY, scope_packet=_SCOPE_PACKET,
            safe_diff=_SAFE_DIFF, test_result=_TEST_RESULT,
            tiered_diff_text=self._TIERED_DIFF_TEXT,
            resume_hunks_text=_RESUME_HUNKS_TEXT,
        )
        texts = _segment_texts(composed)
        assert texts["reviewer_focused_diff"] == _RESUME_HUNKS_TEXT.rstrip("\n")

    def test_an_empty_tiered_diff_text_falls_back_to_the_scoped_flat_capped_diff(self):
        composed = compose_reviewer_prompt(
            _GOAL, _BUILDER_SUMMARY, scope_packet=_SCOPE_PACKET,
            safe_diff=_SAFE_DIFF, test_result=_TEST_RESULT, tiered_diff_text="",
        )
        texts = _segment_texts(composed)
        assert texts["reviewer_focused_diff"] == (
            "## Focused Staged Diff\n```diff\n" + _SAFE_DIFF + "\n```"
        )

    def test_tiered_diff_text_is_inert_on_the_fallback_branch(self):
        composed = compose_reviewer_prompt(
            _GOAL, _BUILDER_SUMMARY, safe_diff=_SAFE_DIFF, test_result=_TEST_RESULT,
            tiered_diff_text=self._TIERED_DIFF_TEXT,
        )
        texts = _segment_texts(composed)
        assert texts["reviewer_staged_diff"] == (
            "## Staged Unified Diff\n```diff\n" + _SAFE_DIFF + "\n```"
        )
        assert "reviewer_focused_diff" not in texts


class TestReviewerTieredDiffTextHelper:
    """Direct unit tests of ``_reviewer_tiered_diff_text``, the pure gating
    helper `run_pingpong` uses to compute `tiered_diff_text` on the SCOPED
    branch (F108 DECISION F108 D4)."""

    def test_returns_empty_when_resumed(self):
        def call_fn_factory():
            raise AssertionError("call_fn_factory must not be called")

        result = _reviewer_tiered_diff_text(
            _SAFE_DIFF, _SCOPE_PACKET, True, call_fn_factory,
            threshold_chars=10, full_ref="test-ref",
        )
        assert result == ""

    def test_returns_empty_when_no_scope_packet(self):
        def call_fn_factory():
            raise AssertionError("call_fn_factory must not be called")

        result = _reviewer_tiered_diff_text(
            "x" * 100, None, False, call_fn_factory,
            threshold_chars=10, full_ref="test-ref",
        )
        assert result == ""

    def test_returns_empty_when_under_threshold(self):
        def call_fn_factory():
            raise AssertionError("call_fn_factory must not be called")

        result = _reviewer_tiered_diff_text(
            _SAFE_DIFF, _SCOPE_PACKET, False, call_fn_factory,
            threshold_chars=len(_SAFE_DIFF) + 1, full_ref="test-ref",
        )
        assert result == ""

    def test_over_threshold_calls_render_tiered_diff_text_and_call_fn_factory_only_then(self):
        calls = {"count": 0}

        def call_fn_factory():
            calls["count"] += 1
            return None

        safe_diff = "x" * (_OVERSIZED_REVIEWER_SCOPED_DIFF_THRESHOLD_CHARS + 100)
        result = _reviewer_tiered_diff_text(
            safe_diff, _SCOPE_PACKET, False, call_fn_factory,
            threshold_chars=_OVERSIZED_REVIEWER_SCOPED_DIFF_THRESHOLD_CHARS,
            full_ref="test-ref",
        )
        assert calls["count"] == 1
        assert result != ""
        assert FALLBACK_MARKER in result
