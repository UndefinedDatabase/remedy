── STEP R-0759-fix — F106 ────────────────────────────────────────────────
Goal: Fix R-0759 (registered round 12): four separately-defined fake
Reviewer classes in tests/orchestration/test_repair_loop.py do not
accept the `resume` keyword the Reviewer call site has passed
unconditionally since round 6, an honest ignored no-op mirroring
R-0758's own fix shape. No production file touched.

Bundle:
  C0a — save this step block verbatim to .agent/authored/f106-r13.md
  C0b — mirror it into .agent/last_block.md
  C1  — rewrite .agent/plan.md for round 13 (PLAN13 below)
  C2  — append RECORD13 (booking round 12's PASS) and Done: R-0759
        (this round's own fix) to .agent/live_review.md, two paragraphs
        in order
  C3  — append the two round-12 prose slips (PROSESLIPR12A,
        PROSESLIPR12B) to .agent/prose_slips.md, two paragraphs in order
  C4  — apply the fix to tests/orchestration/test_repair_loop.py
  C5  — rewrite .agent/handoff.md for round 13 handback

Change: exactly tests/orchestration/test_repair_loop.py, plus the five
.agent/** paths named in C0a/C0b/C1/C2/C3/C5. No path under
packages/orchestration/ (this is a test-only fix).

Constraints:
1. C0a/C0b verbatim single-.agent-state-file saves (shutil.copyfile,
   never cp, never retyped), exempt from the 500-line cap.
2. C1 — PLAN13 is a REWRITE of .agent/plan.md, applied via
   shutil.copyfile from .remedy-wt/f106-r13-plan.md (40 lines, < 50,
   holds `## Goal`/`## Next Steps`, sha256
   e2330e056c6a8b439100e95b94651ea27cbe07ad7cdad05f77689762b0f3279d,
   1916 bytes).
3. C2 — TWO paragraphs appended to .agent/live_review.md, never
   retyped: RECORD13 (.remedy-wt/f106-r13-record13.txt, 5004 bytes,
   sha256 0a0f8b1fbf800b23a2cf69230ffe0ffc82791dc73402d699553672074b519e02)
   then Done: R-0759 (.remedy-wt/f106-r13-doner0759.txt, 1243 bytes,
   sha256 a41a36c64ebf32bc74a9a245286aef61797c48aa0d6bdf8aee113764282f756a).
   RE-MEASURE the file's own base length and its OWN trailing-newline
   state before appending — do not trust any number in this block over
   your own reading. At this round's base the file is 1864466 bytes and
   does NOT end in a trailing newline (verified directly), so BOTH
   separators must be "\n\n", not "\n" — round 12's own block got this
   wrong (see PROSESLIPR12A, landing in C3 below) by assuming a trailing
   newline the base did not carry; do not repeat that mistake. Expected
   total: base + 2 + 5004 + 2 + 1243 = base + 6249. If your own
   remeasured base disagrees with 1864466, STOP and report rather than
   proceeding.
4. C3 — TWO paragraphs appended to .agent/prose_slips.md, never
   retyped: PROSESLIPR12A (.remedy-wt/f106-r13-prose1.txt, 815 bytes,
   sha256 6c493c5ae51396f35a3b565328348472a2f6e617441fec84dfba8038c3de2de0)
   then PROSESLIPR12B (.remedy-wt/f106-r13-prose2.txt, 624 bytes, sha256
   0b31ad81ab78b5cbbe4081b6a9fa8d620ff0c728c3f811490e77e53160c39fd0).
   THIS FILE'S OWN CONVENTION DIFFERS FROM live_review.md: every existing
   entry in prose_slips.md, including the appended slice itself, already
   carries its OWN trailing newline (re-verify: the file's current last
   byte is `\n`), so the correct append is base + "\n" + PROSESLIPR12A +
   "\n" + PROSESLIPR12B — single-newline separators here, because the
   entries supply their own closing newline where live_review.md's
   paragraphs do not. Re-measure the base yourself; expected total at
   this round's base (36371 bytes): 36371 + 1 + 815 + 1 + 624 = 37812.
5. C4 — ONE global find-and-replace across the whole file (not a single
   `.replace(x, y, 1)`): the line
       `            def review(self, prompt, *, timeout_sec=120, max_output_chars=50000):`
   (12 leading spaces) occurs EXACTLY 4 times in the file, byte-for-byte
   identical each time (confirmed: the two `IncoherentReviewer` class
   bodies, `BadReviewer`, and `FailNothingReviewer` all share this exact
   signature line), at lines 118, 584, 775 and 794 at this round's base.
   Replace ALL FOUR occurrences with
       `            def review(self, prompt, *, timeout_sec=120, max_output_chars=50000, resume: str | None = None):`
   in one `content.replace(FROM, TO)` call (no count argument — global).
   Verify FROM count 4→0 and TO count 0→4 after. This is the ONLY change
   to the file; no other line is touched.
6. No mutation red-proof is ordered this round: this is a test-only fix
   (no `packages/` or `apps/` path in the change set), and the four
   previously-failing tests going from RED to GREEN, independently
   re-run, is itself the red/green pair the fix needs — there is no
   separate production branch to mutate.
7. No `.agent/**` file other than plan.md, live_review.md,
   prose_slips.md, last_block.md, handoff.md and the one new
   authored/f106-r13.md is touched.

Done when (7 gates, exact commands):
  G1 TRANSPORT — `.agent/authored/f106-r13.md` and `.agent/last_block.md`
     byte-equal (sha256), both equal to this block's own bytes as
     received.
  G2 THE PLAN — `.agent/plan.md` sha256 equals
     e2330e056c6a8b439100e95b94651ea27cbe07ad7cdad05f77689762b0f3279d,
     `wc -l` < 50, holds `## Goal`/`## Next Steps`.
  G3 THE LIVE_REVIEW APPEND — re-measure `.agent/live_review.md`'s
     length and trailing-byte state immediately before C2 (BASE);
     confirm post-C2 length equals BASE + 6249 AND the file's last TWO
     `\n\n`-delimited units equal RECORD13 then Done: R-0759 exactly, in
     that order.
  G4 THE PROSE_SLIPS APPEND — re-measure `.agent/prose_slips.md`'s
     length immediately before C3 (BASE2); confirm post-C3 length equals
     BASE2 + 1441 (1 + 815 + 1 + 624) AND the file's last two
     `\n\n`-delimited units equal PROSESLIPR12A then PROSESLIPR12B
     exactly, in that order.
  G5 THE LEDGER — line-anchored regex counts before and after C2: `^-
     (R-\d+) — ` unmoved at 320; `^Done: (R-\d+) — ` (distinct ids)
     moves 56→57 (`R-0759` added); `^DECISION (F\d+ D\d+) — ` unmoved
     at 20.
  G6 THE CODE AND TESTS — `ast.parse` on the touched file, exit 0;
     `ruff check tests/orchestration/test_repair_loop.py`, exit 0, "All
     checks passed!"; constraint 5's FROM/TO occurrence counts,
     independently re-measured against the real committed file.
     `python3 -m pytest tests/orchestration/test_repair_loop.py -q`,
     REAL exit 0, 131 passed (127 pre-existing + the 4 R-0759 named).
     `python3 -m pytest tests/orchestration/test_pingpong_cli.py
     tests/orchestration/test_repair_loop.py tests/cli/test_scope_plan.py
     tests/cli/test_task_input.py -q`, REAL exit 0, 384 passed.
     `git diff --stat` for every path under `packages/`: EMPTY.
  G7 THE TREE — `git status --porcelain` empty, `git ls-files --others
     --exclude-standard` empty, every commit's insertions via `git diff
     --numstat <sha>^..<sha>` (C0a/C0b exempt as verbatim `.agent/**`
     state-file saves).

Handback: completion report (every gate above, one line each, REAL
numbers only) + rewrite .agent/handoff.md with the standard sections.
─────────────────────────────────────────────────────────────────────────


PLAN13 (exact byte-for-byte content of .remedy-wt/f106-r13-plan.md;
apply via shutil.copyfile, never retype):

# Plan — F106 Session resume instead of rebuild

Branch: feature/f106-session-resume, cut from `main` at `811c2d7e`.
SESSION 4, round 13.

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
| T002b-ii step 2a/2b (Builder side) | done | rounds 11-12 |
| R-0759: `resume`-kwarg gap in `test_repair_loop.py` (4 classes) | done | this round |
| T002b-ii step 2b (Reviewer side): wire the shrink in | open | next |
| T003: measured fixture comparison + docs | open | |

## Next Steps
1. T002b-ii step 2b, Reviewer side: mirror round 12's Builder-side design
   in `compose_reviewer_prompt` — a `resume_hunks_text` param replacing
   whichever of `reviewer_focused_diff`/`reviewer_staged_diff` would
   otherwise fire, fed from `reviewer_resume_ref` (round 9) at the call
   site; state which of the four diff-shaped segment variants the shrink
   applies to (almost certainly only the two `safe_diff`-backed ones);
   add a resume-active fixture to `test_reviewer_prompt_golden.py`.
2. T003 follows once step 2b is closed on both sides.

## Risks
- No adapter's `supports_resume` is true in production yet — only
  `FakeProvider` ever resumes or fails a resume.
- The Reviewer side has FOUR diff-shaped segment variants
  (scoped/unscoped × safe_diff/diff_summary) versus the Builder's one;
  `reviewer_resume_ref` is non-None only `if is_repair`, which already
  excludes the initial-round variants from ever seeing a resume.
- DECISION F106 D1's D1-compatibility reading still governs both sides.
