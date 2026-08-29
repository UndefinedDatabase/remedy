"""F033: the operator's rejected hunks reach the NEXT builder prompt, verbatim.

THE ACCEPTANCE PROPERTY, and the reason this file exists: the feature file
``docs/roadmap/features/T5_F033.md`` requires that rejected hunks' reasons
appear "verbatim in the next trace". ``packages/orchestration/hunk_repair_findings.py``
renders them and ``tests/orchestration/test_hunk_repair_findings.py`` pins that
renderer. What is pinned HERE is the next link: that the rendered text survives
``compose_builder_prompt`` — segment registration, the ``"\\n"`` part join, the
one-newline-per-boundary adjustment and the ``PROMPT_SEGMENT_DELIMITER`` join —
BYTE FOR BYTE, so an operator's own words arrive at the next builder unchanged.

WHY A SUBSTRING ASSERTION AND NOT A NORMALISED ONE. Every reason below is chosen
to break under a normalisation: it carries leading spaces, an interior blank
line, a tab indent, a line whose first character is ``#`` and trailing spaces. A
test comparing stripped or re-wrapped forms would pass while composition quietly
rewrote what the operator typed, which is the exact failure the verbatim rule
exists to forbid. So each assertion is ``reason in composed.text`` on the RAW
reason.

THE VOCABULARY IS REFERENCED BY NAME. ``REJECTION_FINDINGS_HEADING``,
``REJECTION_FINDINGS_ENTRY_PREFIX`` and ``REJECTION_FINDINGS_REASON_INTRO`` are
imported and never retyped — the convention ``hunk_repair_findings.py``'s own
docstring states, because a test that retypes a heading passes for the wrong
reason the day the wording is improved.

THE RUN LOOP DOES SUPPLY A LEDGER, and the appended section below drives the real
loop to prove it. This paragraph once said the opposite and gave a reason that
was false when it was written: it claimed
``packages/orchestration/hunk_decision_record.py`` leaves no durable record,
when that module writes each exported ledger onto ``job.metadata`` under
``hunk_decisions`` and ``save_job`` at the write door makes the record durable.
That claim was finding R-0747 where it stood in ``pingpong_loop.py``, and
R-0748 here — one defect in two files, because the first fix and its gate were
both scoped to a path while the claim was not.
"""
from __future__ import annotations

import pytest

from packages.orchestration.hunk_ledger import (
    HUNK_LANDING_LANDED,
    HUNK_LANDING_NOT_LANDED,
    HUNK_LANDING_UNATTEMPTED,
    HUNK_STATE_APPROVED,
    HUNK_STATE_PENDING,
    HUNK_STATE_REJECTED,
    HunkDecisionLedger,
    HunkLedgerEntry,
)
from packages.orchestration.hunk_repair_findings import (
    REJECTION_FINDINGS_ENTRY_PREFIX,
    REJECTION_FINDINGS_HEADING,
    REJECTION_FINDINGS_REASON_INTRO,
)
from packages.orchestration.pingpong_loop import (
    _build_builder_prompt,
    compose_builder_prompt,
)
from packages.orchestration.pingpong_provider import ReviewFinding
from packages.orchestration.prompt_segments import SegmentStabilityRank

#: The segment this round adds. Named once so no test retypes it.
_SEGMENT = "builder_hunk_rejections"

_GOAL = "Make the widget resize with its container."
_CONTEXT = "## Repo Facts\nremedy, python, pytest."

#: THE HOSTILE REASON. Every character class that a strip, a re-wrap, an indent
#: or a comment-stripper would damage, in one string: two leading spaces, an
#: interior BLANK line, a tab-indented line, a line opening with ``#``, and two
#: trailing spaces. If composition normalises anything at all, this string stops
#: being a substring of the composed text.
_HOSTILE_REASON = (
    "  the resize helper is the wrong layer\n"
    "\n"
    "\tmove it beside the container instead\n"
    "# and drop the stale comment above it\n"
    "  "
)

_FINDINGS = [
    ReviewFinding(
        id="R-0001",
        severity="high",
        file="packages/widget.py",
        summary="resize ignores the container width",
        required_fix="read the container width before resizing",
    ),
]


def _rejected(hunk_id: str, reason: str) -> HunkLedgerEntry:
    return HunkLedgerEntry(
        hunk_id=hunk_id,
        state=HUNK_STATE_REJECTED,
        reason=reason,
        landing=HUNK_LANDING_NOT_LANDED,
    )


def _ledger(*entries: HunkLedgerEntry) -> HunkDecisionLedger:
    return HunkDecisionLedger(entries=tuple(entries))


def _compose(**kwargs):
    return compose_builder_prompt(_GOAL, _CONTEXT, **kwargs)


def _names(composed) -> list[str]:
    return [entry.name for entry in composed.manifest]


# ---------------------------------------------------------------- B1, B2


def test_a_hostile_reason_reaches_the_composed_prompt_as_an_exact_substring():
    """B1, the acceptance property: verbatim means byte for byte, not modulo whitespace."""
    composed = _compose(hunk_ledger=_ledger(_rejected("h-9c1f", _HOSTILE_REASON)))

    assert _HOSTILE_REASON in composed.text

    # And the vocabulary around it arrived too — by NAME, never by spelling.
    assert REJECTION_FINDINGS_HEADING in composed.text
    assert REJECTION_FINDINGS_ENTRY_PREFIX + "h-9c1f" in composed.text
    assert REJECTION_FINDINGS_REASON_INTRO in composed.text
    # The reason sits BELOW its intro line, which is what "verbatim below" means.
    assert composed.text.index(_HOSTILE_REASON) > composed.text.index(
        REJECTION_FINDINGS_REASON_INTRO
    )


def test_each_hostile_feature_survives_on_its_own():
    """B1 again, one property per reason, so a failure names the damage."""
    cases = {
        "leading_spaces": "   indented by three",
        "interior_blank_line": "first line\n\nthird line",
        "tab_indent": "\tone tab in front",
        "hash_first_character": "# not a heading, an operator's words",
        "trailing_spaces": "trailing two  ",
        "trailing_tab": "trailing tab\t",
        "carriage_return": "a line\r\nand another",
        "internal_run_of_spaces": "kept     five spaces",
    }
    for label, reason in cases.items():
        composed = _compose(hunk_ledger=_ledger(_rejected("h-1", reason)))
        assert reason in composed.text, label


def test_a_reason_ending_in_a_newline_keeps_that_newline():
    """B2: the boundary helper eats the RENDERER's structural newline, not the operator's.

    ``render_rejection_findings`` always terminates a non-empty block with a
    structural newline of its own, and ``_drop_one_newline_per_segment_boundary``
    removes exactly one newline at each boundary. This pins that the byte
    consumed there is the renderer's and never the last byte of a reason.
    """
    reason = "the operator pressed enter at the end\n"
    composed = _compose(hunk_ledger=_ledger(_rejected("h-2", reason)))
    assert reason in composed.text


def test_two_rejections_keep_the_ledger_order_and_both_reasons():
    first = "first rejection, verbatim  "
    second = "\tsecond rejection, verbatim"
    composed = _compose(
        hunk_ledger=_ledger(_rejected("h-a", first), _rejected("h-b", second))
    )
    assert first in composed.text
    assert second in composed.text
    assert composed.text.index(first) < composed.text.index(second)


# ---------------------------------------------------------------- B3


def test_no_rejection_registers_no_segment_and_changes_no_byte():
    """B3: the default, an empty ledger and an approvals-only ledger are all silent."""
    baseline = _compose()
    assert _SEGMENT not in _names(baseline)

    approvals_only = _ledger(
        HunkLedgerEntry(
            hunk_id="h-ok",
            state=HUNK_STATE_APPROVED,
            reason="",
            landing=HUNK_LANDING_LANDED,
        ),
        HunkLedgerEntry(
            hunk_id="h-wait",
            state=HUNK_STATE_PENDING,
            reason="",
            landing=HUNK_LANDING_UNATTEMPTED,
        ),
    )
    for ledger in (None, _ledger(), approvals_only):
        composed = _compose(hunk_ledger=ledger)
        assert _SEGMENT not in _names(composed)
        assert composed.text == baseline.text
        assert _names(composed) == _names(baseline)


def test_the_parameter_is_keyword_only():
    """Positional supply would silently land the ledger in ``round_number``."""
    with pytest.raises(TypeError):
        compose_builder_prompt(_GOAL, _CONTEXT, _ledger())  # type: ignore[misc]


# ---------------------------------------------------------------- B4, B5


def test_the_directive_is_still_the_last_segment_when_rejections_are_present():
    """B4: steering rank is shared, so ORDER here is registration order."""
    composed = _compose(hunk_ledger=_ledger(_rejected("h-3", "reason")))
    names = _names(composed)
    assert _SEGMENT in names
    assert names[-1] == "builder_directive"
    assert names.index(_SEGMENT) < names.index("builder_directive")


def test_rejections_sit_between_the_repair_findings_and_the_directive():
    """B4: with reviewer findings supplied too, all three steering segments order."""
    composed = _compose(
        findings=_FINDINGS,
        hunk_ledger=_ledger(_rejected("h-4", "reason")),
    )
    names = _names(composed)
    assert names.index("builder_repair") < names.index(_SEGMENT)
    assert names.index(_SEGMENT) < names.index("builder_directive")
    assert names[-1] == "builder_directive"


def test_the_segment_is_registered_at_steering_rank():
    composed = _compose(hunk_ledger=_ledger(_rejected("h-5", "reason")))
    entry = next(e for e in composed.manifest if e.name == _SEGMENT)
    assert entry.rank == SegmentStabilityRank.STEERING


def test_manifest_ranks_stay_non_decreasing_with_the_segment_present():
    """B5."""
    for kwargs in (
        dict(hunk_ledger=_ledger(_rejected("h-6", "reason"))),
        dict(findings=_FINDINGS, hunk_ledger=_ledger(_rejected("h-7", "reason"))),
        dict(
            findings=_FINDINGS,
            staged_state="M packages/widget.py",
            safe_diff="--- a/w.py\n+++ b/w.py\n+    resize()",
            task_body="Resize the widget.",
            scope_contract="## Scope Contract\nTouch only packages/widget.py.",
            test_result="3 passed in 0.10s",
            hunk_ledger=_ledger(_rejected("h-8", _HOSTILE_REASON)),
        ),
    ):
        composed = _compose(**kwargs)
        assert _SEGMENT in _names(composed)
        ranks = [entry.rank for entry in composed.manifest]
        assert ranks == sorted(ranks)


def test_the_segment_hash_and_span_agree_with_the_composed_text():
    """The manifest is not decoration: slice the segment back out and hash it."""
    import hashlib

    from packages.orchestration.prompt_segments import PROMPT_SEGMENT_DELIMITER

    composed = _compose(hunk_ledger=_ledger(_rejected("h-9", _HOSTILE_REASON)))
    position = 0
    span = None
    for entry in composed.manifest:
        if entry.name == _SEGMENT:
            span = (position, position + entry.chars)
        position += entry.chars + len(PROMPT_SEGMENT_DELIMITER)
    assert span is not None
    chunk = composed.text[span[0]:span[1]]
    segment = next(e for e in composed.manifest if e.name == _SEGMENT)
    assert hashlib.sha256(chunk.encode("utf-8")).hexdigest() == segment.sha256
    assert _HOSTILE_REASON in chunk


# ---------------------------------------------------------------- B6


def test_a_malformed_ledger_composes_without_raising_and_registers_nothing():
    """B6: the renderer is TOTAL, so composition inherits totality — it never throws here."""

    class _NoEntries:
        pass

    class _EntryWithoutReason:
        state = HUNK_STATE_REJECTED
        hunk_id = "h-broken"

    class _EntriesNotIterable:
        entries = 7

    class _BadEntryHolder:
        entries = (_EntryWithoutReason(),)

    baseline = _compose()
    for ledger in (
        _NoEntries(),
        _EntriesNotIterable(),
        _BadEntryHolder(),
        object(),
        "not a ledger at all",
        42,
    ):
        composed = _compose(hunk_ledger=ledger)
        assert _SEGMENT not in _names(composed)
        assert composed.text == baseline.text


def test_a_ledger_whose_second_entry_is_broken_registers_nothing_at_all():
    """A PARTIAL block is worse than none: the renderer discards work in progress."""
    baseline = _compose()

    class _EntryWithoutReason:
        state = HUNK_STATE_REJECTED
        hunk_id = "h-broken"

    class _Mixed:
        entries = (_rejected("h-good", "a readable reason"), _EntryWithoutReason())

    composed = _compose(hunk_ledger=_Mixed())
    assert _SEGMENT not in _names(composed)
    assert composed.text == baseline.text
    assert "a readable reason" not in composed.text


# ---------------------------------------------------------------- B7


def test_build_builder_prompt_forwards_the_parameter_unchanged():
    """B7."""
    ledger = _ledger(_rejected("h-10", _HOSTILE_REASON))
    built = _build_builder_prompt(_GOAL, _CONTEXT, hunk_ledger=ledger)
    assert built == _compose(hunk_ledger=ledger).text
    assert _HOSTILE_REASON in built
    # And with no ledger it is byte-equal to the call that omits the parameter.
    assert _build_builder_prompt(_GOAL, _CONTEXT) == _build_builder_prompt(
        _GOAL, _CONTEXT, hunk_ledger=None
    )


# ---------------------------------------------------------------------------
# THE ACCEPTANCE TEST — the REAL loop, end to end
#
# THE MODULE DOCSTRING ABOVE IS SUPERSEDED FROM HERE DOWN, and it is corrected here rather than
# rewritten because this section was APPENDED under an append-only obligation and no line above
# it may move. Its closing paragraph says "nothing here asserts that the RUN LOOP supplies a
# ledger. It does not yet". As of this round it DOES: ``run_pingpong`` carries a ``hunk_ledger``
# parameter and forwards it to ``compose_builder_prompt``, and the two tests below drive the
# real loop over a demo repo to prove it.
#
# WHY THE CHAIN HAS THREE LINKS INSTEAD OF ONE ASSERTION. A prompt trace entry carries a
# ``segment_manifest`` but NO prompt text — ``prompt_text_redacted`` is not the composed text
# and no attribute on the entry holds it — so "the reason is in the loop's prompt" cannot be
# asserted directly off the trace. Instead:
#   (a) some ``result.prompt_traces`` entry has a manifest row named ``builder_hunk_rejections``
#       — the REAL loop composed the segment, from the ledger it was handed;
#   (b) composing DIRECTLY with the same ledger and cutting that segment back out by its own
#       manifest span, the operator's reason is an EXACT SUBSTRING of it;
#   (c) the ``sha256`` on the row from (a) EQUALS the sha256 of the text from (b).
# Link (c) is what joins them: it is the loop's own bytes, not a second composition's, that (b)
# inspected. It holds because the segment's digest depends ONLY on the ledger — every other
# argument to ``compose_builder_prompt`` differs between the loop's call and (b)'s, including
# the goal, the context, the round number and the staged state.
#
# The two fixtures below are LOCAL COPIES of ``tests/orchestration/test_pingpong.py``'s
# ``isolate_data_root`` and ``demo_repo``, restated for the reason this suite's neighbours give
# for restating recipes: a test file reaching into another test file's fixtures couples two
# suites that have no reason to move together. ``REMEDY_DATA_DIR`` is set with
# ``monkeypatch.setenv`` and could not be set any other way — the sandbox this repository is
# built in denies every shell form of assigning it.

#: A rejection reason for the LOOP test, hostile in the three ways a prompt pipeline is most
#: likely to damage: two LEADING spaces, an INTERIOR BLANK LINE and a TAB indent.
_LOOP_REASON = (
    "  this hunk edits the wrong module\n"
    "\n"
    "\tput it beside the container in packages/widget.py instead\n"
)


@pytest.fixture
def loop_data_root(tmp_path, monkeypatch):
    """``REMEDY_DATA_DIR`` redirected into ``tmp_path`` so the loop writes to no real data root."""
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


@pytest.fixture
def loop_demo_repo(tmp_path):
    """A minimal demo repo, the shape the ping-pong suite's own ``demo_repo`` builds."""
    (tmp_path / "README.md").write_text("# Demo\nA demo project.\n")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "README.md").write_text("# Docs\nDocumentation here.\n")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.py").write_text("def hello():\n    return 'hello'\n")
    return tmp_path


def _manifest_rows(result, name: str) -> list[dict]:
    """Every manifest row called ``name``, over every prompt trace the run recorded."""
    return [
        row
        for entry in result.prompt_traces
        for row in entry.segment_manifest
        if row["name"] == name
    ]


def _segment_text(composed, name: str) -> str:
    """One segment cut back out of a composed prompt by its OWN manifest span."""
    from packages.orchestration.prompt_segments import PROMPT_SEGMENT_DELIMITER

    position = 0
    for entry in composed.manifest:
        if entry.name == name:
            return composed.text[position:position + entry.chars]
        position += entry.chars + len(PROMPT_SEGMENT_DELIMITER)
    raise AssertionError(f"{name} is not in {[e.name for e in composed.manifest]}")


def _run_loop(repo, **kwargs):
    """The ping-pong suite's own invocation, with fake providers on both sides."""
    from packages.orchestration.pingpong_loop import run_pingpong

    return run_pingpong(
        "Fix README", str(repo), builder_name="fake", reviewer_name="fake", **kwargs
    )


def test_a_rejection_reason_reaches_the_real_loops_composed_builder_prompt(
    loop_demo_repo, loop_data_root
) -> None:
    """THE ACCEPTANCE PROPERTY OF THIS ROUND: an operator's words reach the REAL loop's prompt.

    Not ``compose_builder_prompt`` called by a test, but ``run_pingpong`` — the function the
    job runner calls — composing the segment from a ledger handed to it.
    """
    import hashlib

    ledger = _ledger(_rejected("h-loop", _LOOP_REASON))
    result = _run_loop(loop_demo_repo, hunk_ledger=ledger)

    # The run really produced traces with manifests, so the assertions below cannot pass by
    # being vacuous.
    assert result.prompt_traces
    assert any(entry.segment_manifest for entry in result.prompt_traces)

    # (a) the REAL loop composed the segment.
    rows = _manifest_rows(result, _SEGMENT)
    assert len(rows) == 1, [
        [row["name"] for row in entry.segment_manifest] for entry in result.prompt_traces
    ]

    # (b) the same ledger composed directly, with EVERY other argument different — a different
    # goal, a different context, reviewer findings, a staged state and a task body — still
    # carries the reason byte for byte.
    composed = _compose(
        findings=_FINDINGS,
        staged_state="M packages/widget.py",
        task_body="Resize the widget.",
        hunk_ledger=ledger,
    )
    chunk = _segment_text(composed, _SEGMENT)
    assert _LOOP_REASON in chunk
    assert REJECTION_FINDINGS_HEADING in chunk
    assert REJECTION_FINDINGS_ENTRY_PREFIX + "h-loop" in chunk
    assert REJECTION_FINDINGS_REASON_INTRO in chunk

    # (c) the LOOP's own bytes are the bytes (b) inspected. This is the link that makes the two
    # halves one claim instead of two: the digest is the loop's, the text is (b)'s.
    assert rows[0]["sha256"] == hashlib.sha256(chunk.encode("utf-8")).hexdigest()


def test_a_loop_round_with_no_hunk_ledger_composes_no_rejection_segment(
    loop_demo_repo, loop_data_root
) -> None:
    """THE NEGATIVE HALF, and what makes the test above discriminating.

    Without the parameter the same run composes no ``builder_hunk_rejections`` row at all, so
    the positive test cannot be passing on a segment the loop registers unconditionally.
    """
    result = _run_loop(loop_demo_repo)

    assert result.prompt_traces
    names = [
        row["name"] for entry in result.prompt_traces for row in entry.segment_manifest
    ]
    # Non-vacuous: the plain run DOES compose a builder prompt with segments, just not this one.
    assert "builder_system" in names
    assert _SEGMENT not in names
    assert _manifest_rows(result, _SEGMENT) == []
