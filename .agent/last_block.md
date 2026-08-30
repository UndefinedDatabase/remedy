── STEP T002b-ii/2b(Reviewer) — F106 ─────────────────────────────────────
Goal: Mirror round 12's Builder-side design onto the Reviewer side of
T002b-ii step 2b: `compose_reviewer_prompt` gains a `resume_hunks_text`
parameter that, when non-empty, replaces the diff-shaped segment on
WHICHEVER of its two mutually exclusive branches (scoped ->
`reviewer_focused_diff`, unscoped -> `reviewer_staged_diff`) would
otherwise fire — same segment name/rank each branch already uses. The
call site computes it via round 11's frozen `render_repair_hunks(
select_repair_hunks(...))`, gated on the round-9 hoisted
`reviewer_resume_ref`. An empty render always falls back to the
unconditional path. With this round, T002 is fully closed on both sides.

Bundle:
  C0a — save this step block verbatim to .agent/authored/f106-r14.md
  C0b — mirror it into .agent/last_block.md
  C1  — rewrite .agent/plan.md for round 14 (PLAN14 below)
  C2  — append RECORD14 (booking round 13's PASS) to
        .agent/live_review.md, ONE paragraph
  C3  — append PROSESLIPR13 to .agent/prose_slips.md, ONE paragraph
  C4  — apply the four pairs below to packages/orchestration/pingpong_loop.py
  C5  — apply the golden-test changes to
        tests/orchestration/test_reviewer_prompt_golden.py
  C6  — rewrite .agent/handoff.md for round 14 handback

Change: exactly packages/orchestration/pingpong_loop.py and
tests/orchestration/test_reviewer_prompt_golden.py, plus the six
.agent/** paths named in C0a/C0b/C1/C2/C3/C6. No path under
packages/orchestration/diff_repair.py (frozen round 11, untouched), no
test_builder_prompt_golden.py (round 12's own shape, untouched), no
test_repair_loop.py (R-0759 already closed round 13, untouched).

Constraints:
1. C0a/C0b verbatim single-.agent-state-file saves (shutil.copyfile,
   never cp, never retyped), exempt from the 500-line cap.
2. C1 — PLAN14 is a REWRITE of .agent/plan.md, applied via
   shutil.copyfile from .remedy-wt/f106-r14-plan.md (38 lines, < 50,
   holds `## Goal`/`## Next Steps`, sha256
   516ba9577d45cdd146a8ee21c49b5317850abe4f564ab953c688efac9dd29ef2,
   1761 bytes).
3. C2 — ONE paragraph appended to .agent/live_review.md, never retyped:
   RECORD14 (.remedy-wt/f106-r14-record14.txt, 3499 bytes, sha256
   37c86639c47af99a655255799a95c934285a8896d0b00659d4525cdee4c70b22). Re-
   measure the file's own base length and trailing-newline state before
   appending. At this round's base the file is 1870717 bytes and does
   NOT end in a trailing newline, so the separator is "\n\n" (matching
   round 13's own corrected reading, not round 12's original mistake).
   Expected total: base + 2 + 3499 = base + 3501.
4. C3 — ONE paragraph appended to .agent/prose_slips.md, never retyped:
   PROSESLIPR13 (.remedy-wt/f106-r14-prose1.txt, 631 bytes, sha256
   edf3b1418ea3de3ad0db2e4a418581afaf78886d020792f57a1ff5d44e62d0ab).
   THIS FILE'S OWN CONVENTION: every entry, including this one, already
   carries its own trailing newline (re-verify: the file's current last
   byte is `\n`), so the append is base + "\n" + PROSESLIPR13 — a SINGLE
   newline separator here, not "\n\n" (constraint 3's file and this one
   use DIFFERENT conventions; do not copy one constraint's arithmetic
   into the other). Expected total at this round's base (37812 bytes):
   37812 + 1 + 631 = 38444.
5. C4 — FOUR REWRITE pairs against packages/orchestration/pingpong_loop.py,
   applied IN ORDER, each independently verified: FROM exactly 1x
   pre-commit/0x post; TO exactly 0x pre-commit/1x post;
   `TO contains FROM: false` for every one. Exactly as validated by the
   reviewer in a disposable worktree before this block was authored
   (ast.parse clean, ruff clean, full suite green, mutation red-proofed
   — you are REPRODUCING this, not discovering it fresh):
     PAIR1-SIGNATURE — `compose_reviewer_prompt`'s keyword-only parameter
       list gains `resume_hunks_text: str = "",` as the new last entry,
       immediately before `) -> ComposedPrompt:`, right after
       `task_id: str = "",`.
     PAIR2-BODY-BRANCH — the diff-segment selection block (`if scoped:
       if safe_diff: ... elif diff_summary: ... elif safe_diff: ... elif
       diff_summary: ...`) gains a NEW `if resume_hunks_text:` check as
       the FIRST branch inside the `if scoped:` leg (appending
       `[resume_hunks_text]` to `reviewer_focused_diff`, no fence, no
       cap) and a NEW `elif resume_hunks_text:` check as the FIRST leg
       of the outer `if scoped: ... elif ...` chain (appending
       `[resume_hunks_text]` to `reviewer_staged_diff`). Every existing
       `elif safe_diff`/`elif diff_summary` branch is otherwise BYTE
       UNCHANGED — only re-flowed under the two new checks. A six-line
       comment above the scoped-branch check names this round, DECISION
       F106 D1(b), and states the empty-string fallback.
     PAIR3-BUILD-REVIEWER-PROMPT-SHIM — `_build_reviewer_prompt` (the
       test-only passthrough wrapper) gains the identical
       `resume_hunks_text: str = "",` parameter and forwards it
       unchanged into its own `compose_reviewer_prompt(...)` call, plus
       a one-clause docstring update.
     PAIR4-CALLSITE — immediately before the existing
       `reviewer_composed = compose_reviewer_prompt(...)` call (which
       already exists, unchanged in its own body except gaining
       `resume_hunks_text=reviewer_resume_hunks_text,` as its new last
       kwarg), insert an eight-line comment plus the
       `reviewer_resume_hunks_text` computation: empty string by
       default; when `reviewer_resume_ref and reviewer_safe_diff` are
       both truthy, import `render_repair_hunks`/`select_repair_hunks`
       from `packages.orchestration.diff_repair` and
       `parse_diff_line_ranges` from
       `packages.orchestration.review_scope`, then set it to
       `render_repair_hunks(select_repair_hunks(staging,
       parse_diff_line_ranges(reviewer_safe_diff),
       max_total_chars=_REVIEWER_DIFF_CAP))` — note `_REVIEWER_DIFF_CAP`
       (30000, the UNSCOPED cap) is used for BOTH branches' render
       budget; the scoped branch's own smaller `_REVIEWER_SCOPED_DIFF_CAP`
       is a full-diff cap and is deliberately NOT reused here, since the
       shrink render is a new, independent budget rather than a
       substitute for either existing cap.
   Simplest correct application: shutil.copyfile the whole scratch file
   at .remedy-wt/f106-r14-pingpong_loop.py onto
   packages/orchestration/pingpong_loop.py directly (already validated
   end to end); verify the four pairs' own properties AFTER the copy,
   against the real committed diff, never before. sha256 of the target
   file after copying (re-measure, do not trust this number over your
   own sha256sum):
   16540f25c16c1bd3a48165ba8863594dec365d922d449306f3e714b847a47262,
   207851 bytes.
6. C5 — shutil.copyfile the whole scratch file at
   .remedy-wt/f106-r14-test_reviewer_prompt_golden.py onto
   tests/orchestration/test_reviewer_prompt_golden.py. It adds TWO new
   fixture shapes ("scoped_resumed" and "fallback_resumed", one per
   mutually exclusive branch, each mirroring its own "_full" sibling
   with `resume_hunks_text` set), two new frozen render entries
   (captured by RUNNING the current branch's own `compose_reviewer_prompt`
   twice and writing `repr()` of each reconstructed pre-migration-order
   render — not retyped, provenance stated inline), and a new
   `TestResumeHunksTextReplacesTheDiffOnEitherBranch` class (8 tests,
   covering both branches' segment order/rank, both branches' raw-render
   content, both "_full" shapes staying byte-unchanged, and both
   branches' empty-string fallback). No existing `_FROZEN_RENDERS` entry,
   `_SHAPES` entry, or test function is edited or removed — confirm by
   diffing the four pre-existing dict values byte-for-byte against the
   pre-commit file. sha256 of the target file after copying:
   87f17dd5afd279d836d72a37774d8a458fb909ef6450fb899e08629625b27132,
   24483 bytes.
7. Mutation red-proof for C4 is MANDATORY (production code), disposable
   worktree only (self_drive_protocol.md G5). Recipe: replace BOTH
   `if resume_hunks_text:` (inside the `if scoped:` leg) and
   `elif resume_hunks_text:` (the outer chain's first leg) with
   `if False:  # MUTATED` / `elif False:  # MUTATED` respectively, and
   confirm `python3 -B -m pytest
   tests/orchestration/test_reviewer_prompt_golden.py -q` goes RED at
   exactly 4 failures
   (`test_segments_reassemble_into_the_frozen_render[fallback_resumed]`,
   `test_segments_reassemble_into_the_frozen_render[scoped_resumed]`,
   `TestResumeHunksTextReplacesTheDiffOnEitherBranch::test_scoped_resumeds_diff_segment_is_the_raw_render`,
   `TestResumeHunksTextReplacesTheDiffOnEitherBranch::test_fallback_resumeds_diff_segment_is_the_raw_render`),
   26 passed — the reviewer already ran this exact recipe pre-delegation
   and got this exact split; reproduce it, then revert BOTH lines and
   confirm 30 passed again before removing the worktree.
8. No `.agent/**` file other than plan.md, live_review.md,
   prose_slips.md, last_block.md, handoff.md and the one new
   authored/f106-r14.md is touched.

Done when (8 gates, exact commands):
  G1 TRANSPORT — `.agent/authored/f106-r14.md` and `.agent/last_block.md`
     byte-equal (sha256), both equal to this block's own bytes as
     received.
  G2 THE PLAN — `.agent/plan.md` sha256 equals
     516ba9577d45cdd146a8ee21c49b5317850abe4f564ab953c688efac9dd29ef2,
     `wc -l` < 50, holds `## Goal`/`## Next Steps`.
  G3 THE LIVE_REVIEW APPEND — re-measure `.agent/live_review.md`'s
     length and trailing-byte state immediately before C2 (BASE);
     confirm post-C2 length equals BASE + 3501 AND the file's last
     `\n\n`-delimited unit equals RECORD14 exactly.
  G4 THE PROSE_SLIPS APPEND — re-measure `.agent/prose_slips.md`'s
     length immediately before C3 (BASE2); confirm post-C3 length
     equals BASE2 + 632 AND the file's last `\n\n`-delimited unit equals
     PROSESLIPR13 exactly.
  G5 THE LEDGER — line-anchored regex counts before and after C2: `^-
     (R-\d+) — ` unmoved at 320; `^Done: (R-\d+) — ` (distinct ids)
     unmoved at 57; `^DECISION (F\d+ D\d+) — ` unmoved at 20 (this round
     books no new finding or decision).
  G6 THE CODE — `ast.parse` on both touched files, exit 0; `ruff check
     packages/orchestration/pingpong_loop.py
     tests/orchestration/test_reviewer_prompt_golden.py`, exit 0, "All
     checks passed!"; the four C4 pairs and the C5 whole-file sha256,
     independently re-measured against the real committed files.
     `git diff --stat` for `packages/orchestration/diff_repair.py`,
     `tests/orchestration/test_builder_prompt_golden.py` and
     `tests/orchestration/test_repair_loop.py`: all three EMPTY.
  G7 THE TESTS AND MUTATION — `python3 -m pytest
     tests/orchestration/test_reviewer_prompt_golden.py -q`, REAL exit
     0, 30 passed. Then the broadened zero-behavior-change suite:
     `python3 -m pytest tests/orchestration/test_reviewer_prompt_golden.py
     tests/orchestration/test_builder_prompt_golden.py
     tests/orchestration/test_pingpong.py
     tests/orchestration/test_provider_mode.py
     tests/orchestration/test_provider_evidence_integration.py
     tests/orchestration/test_session_resume.py
     tests/orchestration/test_builder_prompt_quality.py
     tests/orchestration/test_builder_prompt_hunk_rejections.py
     tests/orchestration/test_provider_retry.py -q`, REAL exit 0, 270
     passed. Then constraint 7's mutation red-proof, reported as:
     unmutated exit+count, mutated exit+count+failing-test-names,
     reverted exit+count, worktree removed, `git worktree list`
     afterward shows only the primary checkout.
  G8 THE TREE — `git status --porcelain` empty, `git ls-files --others
     --exclude-standard` empty, every commit's insertions via `git diff
     --numstat <sha>^..<sha>` (C0a/C0b exempt as verbatim `.agent/**`
     state-file saves).

Handback: completion report (every gate above, one line each, REAL
numbers only) + rewrite .agent/handoff.md with the standard sections.
─────────────────────────────────────────────────────────────────────────


PLAN14 (exact byte-for-byte content of .remedy-wt/f106-r14-plan.md;
apply via shutil.copyfile, never retype):

# Plan — F106 Session resume instead of rebuild

Branch: feature/f106-session-resume, cut from `main` at `811c2d7e`.
SESSION 4, round 14.

## Goal
Repair rounds stop resending the world: where the provider supports resuming
a session, a repair call resumes the original session and sends only the
findings delta, with an honest automatic fallback to full context when the
session is gone, flagged in evidence. Correctness never depends on resume
working.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| T001, T002a, T002b-i, T002c, T002b-ii step 1, R-0758 | done | rounds 2-10 |
| T002b-ii step 2a/2b (Builder side), R-0759 | done | rounds 11-13 |
| T002b-ii step 2b (Reviewer side): wire the shrink in | done | this round |
| T003: measured fixture comparison + docs | open | next |

## Next Steps
1. T003: a fixture repair chain showing MEASURED token reduction with
   resume versus without (Goal & Done's own acceptance criterion,
   docs/roadmap/features/T3_F106.md). Needs a `FakeProvider` chain with
   `supports_resume=True` across two repair rounds, comparing prompt
   char counts (or a token estimate) with and without a resumed session,
   plus docs recording the measured numbers. T002 (both sides of
   T002b-ii step 2b) is now fully closed, so T003 is unblocked.
2. Once T003 lands, F106 moves to closure per
   docs/roadmap/STATUS_closure_protocol.md.

## Risks
- No adapter's `supports_resume` is true in production yet — only
  `FakeProvider` ever resumes or fails a resume; T003's fixture chain is
  necessarily `FakeProvider`-driven for the same reason T001-T002 were.
- DECISION F106 D1's D1-compatibility reading governed both sides of the
  shrink; T003 measures the OUTCOME of that decision, not a new one.
