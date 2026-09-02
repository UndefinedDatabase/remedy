── STEP T002b-ii/2b(Builder) — F106 ──────────────────────────────────────
Goal: Wire T002b-ii step 2b's prompt shrink into the Builder side only
(the Reviewer side is a later round): `compose_builder_prompt` gains a
`resume_hunks_text` parameter that, when non-empty, replaces the full
capped diff in the SAME `builder_staged_diff` segment (same name, same
rank); the call site in `run_pingpong` computes it via round 11's frozen
`render_repair_hunks(select_repair_hunks(...))`, gated on the round-9
hoisted `builder_resume_ref`. An empty render always falls back to the
unconditional full-diff path — never to no diff at all. Also register
R-0759 (new, unrelated defect discovered this round's own diligence).

Bundle:
  C0a — save this step block verbatim to .agent/authored/f106-r12.md
  C0b — mirror it into .agent/last_block.md
  C1  — rewrite .agent/plan.md for round 12 (PLAN12 below)
  C2  — append RECORD12 (booking round 11's PASS) and R-0759 (new
        registration) to .agent/live_review.md, two paragraphs in order
  C3  — apply the four pairs below to packages/orchestration/pingpong_loop.py
  C4  — apply the golden-test changes to
        tests/orchestration/test_builder_prompt_golden.py
  C5  — rewrite .agent/handoff.md for round 12 handback

Change: exactly packages/orchestration/pingpong_loop.py and
tests/orchestration/test_builder_prompt_golden.py, plus the five
.agent/** paths named in C0a/C0b/C1/C2/C5. No path under
packages/orchestration/diff_repair.py (frozen last round, untouched),
no test_reviewer_prompt_golden.py, no test_repair_loop.py (R-0759 is
registered, not fixed, this round).

Constraints:
1. C0a/C0b verbatim single-.agent-state-file saves (shutil.copyfile,
   never cp, never retyped), exempt from the 500-line cap.
2. C1 — PLAN12 is a REWRITE of .agent/plan.md, applied via
   shutil.copyfile from .remedy-wt/f106-r12-plan.md (44 lines, < 50,
   holds `## Goal`/`## Next Steps`, sha256
   dca0031fd5f17e77b41207955ffe510557179c6285ffacfc9d7effc365372274,
   2210 bytes).
3. C2 — TWO paragraphs appended in order to .agent/live_review.md, never
   retyped: RECORD12 (.remedy-wt/f106-r12-record12.txt, 4516 bytes, sha256
   b4f1fa378e05a69d4eb857076dc1f38af8061319827fd9d6244b94c3300c8cca) then
   R-0759 (.remedy-wt/f106-r12-r0759.txt, 2591 bytes, sha256
   c8917e3a818a72cf757eb9efef6ed443a73d2c14cd76432cb30c6491ce811878).
   Re-measure the file's OWN base length before appending (do not trust
   any number in this block over your own reading); if it disagrees with
   1857355, stop and report rather than proceeding. Expected total:
   base + 1 + 4516 + 1 + 2591.
4. C3 — FOUR REWRITE pairs against packages/orchestration/pingpong_loop.py,
   applied IN ORDER (each one changes the file the next one reads), each
   independently verified: FROM exactly 1x pre-commit, 0x post; TO exactly
   0x pre-commit, 1x post; `TO contains FROM: false` for every one (a
   genuine rewrite, not an append). The four pairs, exactly as validated
   by the reviewer in a disposable worktree before this block was
   authored (ast.parse clean, ruff clean, full test suite green — you are
   REPRODUCING this, not discovering it fresh):
     PAIR1-SIGNATURE — `compose_builder_prompt`'s keyword-only parameter
       list gains `resume_hunks_text: str = "",` as the new last entry,
       immediately before `) -> ComposedPrompt:`, right after
       `hunk_ledger: Any = None,`.
     PAIR2-BODY-BRANCH — the existing `if safe_diff and findings:` block
       that builds the `builder_staged_diff` segment becomes an
       `elif safe_diff and findings:` on an UNCHANGED body, with a NEW
       `if resume_hunks_text:` branch immediately above it that appends
       the SAME segment name/rank with `[resume_hunks_text]` as its only
       part — no diff-fence wrapper, no cap, the caller's pre-rendered
       text used exactly as given. A six-line comment above the new
       branch names this round, DECISION F106 D1(b), and states the
       empty-string fallback explicitly.
     PAIR3-CALLSITE — immediately before the existing
       `builder_composed = compose_builder_prompt(...)` call (which
       already exists, unchanged in its own body except gaining
       `resume_hunks_text=builder_resume_hunks_text,` as its new last
       kwarg), insert an eight-line comment plus the
       `builder_resume_hunks_text` computation: empty string by default;
       when `builder_resume_ref and repair_diff` are both truthy, import
       `render_repair_hunks`/`select_repair_hunks` from
       `packages.orchestration.diff_repair` and `parse_diff_line_ranges`
       from `packages.orchestration.review_scope`, then set it to
       `render_repair_hunks(select_repair_hunks(staging,
       parse_diff_line_ranges(repair_diff), max_total_chars=_REPAIR_DIFF_CAP))`.
     PAIR4-BUILD-BUILDER-PROMPT-SHIM — `_build_builder_prompt` (the
       test-only passthrough wrapper) gains the identical
       `resume_hunks_text: str = "",` parameter and forwards it
       unchanged into its own `compose_builder_prompt(...)` call, plus a
       one-clause docstring update naming it alongside `hunk_ledger`.
   Simplest correct application: shutil.copyfile the whole scratch file
   at .remedy-wt/f106-r12-pingpong_loop.py onto
   packages/orchestration/pingpong_loop.py directly (already validated
   end to end — the four pairs above are its exact, complete diff against
   the file's state at this round's base); verify the four pairs' own
   properties AFTER the copy, against the real committed diff, never
   before. sha256 of the target file after copying (re-measure, do not
   trust this number over your own sha256sum):
   4fe8d409f79f84264020c1efeeaf426e3024cf761dcf78e9f9eacfcf07b2bbed,
   205939 bytes.
5. C4 — shutil.copyfile the whole scratch file at
   .remedy-wt/f106-r12-test_builder_prompt_golden.py onto
   tests/orchestration/test_builder_prompt_golden.py. It adds a fifth
   fixture shape ("resumed", mirroring "full" but with
   `resume_hunks_text` set), one new frozen render entry (captured by
   RUNNING the current branch's own `compose_builder_prompt` once and
   writing `repr()` of the reconstructed pre-migration-order render — not
   retyped, and its own provenance is stated inline, distinct from the
   other four which came from commit 54049e6b), and a new
   `TestResumeHunksTextReplacesTheFullDiff` class (4 tests). No existing
   `_FROZEN_RENDERS` entry, `_SHAPES` entry, or test function is edited or
   removed — confirm by diffing the four pre-existing dict values
   byte-for-byte against the pre-commit file. sha256 of the target file
   after copying:
   36180fdd252c0446f8477d153a44cf15355464e38fbbbd8c98f324ea4c3ebbe0.
6. Mutation red-proof for C3 is MANDATORY (production code), disposable
   worktree only (self_drive_protocol.md G5). Recipe: replace
   `if resume_hunks_text:` with `if False:  # MUTATED` inside
   `compose_builder_prompt` and confirm
   `python3 -B -m pytest tests/orchestration/test_builder_prompt_golden.py -q`
   goes RED at exactly 2 failures
   (`test_segments_reassemble_into_the_frozen_render[resumed]`,
   `TestResumeHunksTextReplacesTheFullDiff::test_the_resumed_shapes_diff_segment_is_the_raw_render_unfenced_again`),
   26 passed — the reviewer already ran this exact recipe pre-delegation
   and got this exact split; reproduce it, then revert and confirm 28
   passed again before removing the worktree.
7. R-0759 is REGISTERED this round, not fixed. `tests/orchestration/
   test_repair_loop.py` is named nowhere in this round's Change set and
   stays untouched — confirm with `git diff --stat` after C3/C4, empty
   for that path.
8. No `.agent/**` file other than plan.md, live_review.md, last_block.md,
   handoff.md and the one new authored/f106-r12.md is touched.

Done when (8 gates, exact commands):
  G1 TRANSPORT — `.agent/authored/f106-r12.md` and `.agent/last_block.md`
     byte-equal (sha256), both equal to this block's own bytes as
     received.
  G2 THE PLAN — `.agent/plan.md` sha256 equals
     dca0031fd5f17e77b41207955ffe510557179c6285ffacfc9d7effc365372274,
     `wc -l` < 50, holds `## Goal`/`## Next Steps`.
  G3 THE RECORD APPEND — re-measure `.agent/live_review.md`'s length
     immediately before C2 (BASE), confirm post-C2 length equals
     BASE + 1 + 4516 + 1 + 2591 AND the file's last TWO `\n\n`-delimited
     units equal RECORD12 then R-0759 exactly, in that order.
  G4 THE LEDGER — line-anchored regex counts before C2 and after: `^-
     (R-\d+) — ` registered moves 319→320 (R-0759 added); `^Done: (R-\d+)
     — ` (distinct ids) unmoved at 56; `^DECISION (F\d+ D\d+) — ` unmoved
     at 20.
  G5 THE CODE — `ast.parse` on both touched files, exit 0; `ruff check
     packages/orchestration/pingpong_loop.py
     tests/orchestration/test_builder_prompt_golden.py`, exit 0, "All
     checks passed!"; the four C3 pairs and the C4 whole-file sha256,
     independently re-measured against the real committed files.
  G6 THE TESTS — `python3 -m pytest
     tests/orchestration/test_builder_prompt_golden.py -q`, REAL exit 0,
     28 passed. Then the broadened zero-behavior-change suite:
     `python3 -m pytest tests/orchestration/test_pingpong.py
     tests/orchestration/test_provider_mode.py
     tests/orchestration/test_provider_evidence_integration.py
     tests/orchestration/test_session_resume.py
     tests/orchestration/test_builder_prompt_quality.py
     tests/orchestration/test_builder_prompt_hunk_rejections.py
     tests/orchestration/test_provider_retry.py -q`, REAL exit 0, 240
     passed. `git diff --stat` for `packages/orchestration/diff_repair.py`
     and `tests/orchestration/test_repair_loop.py`: both EMPTY.
  G7 THE MUTATION RED-PROOF — constraint 6's recipe, reported as:
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


PLAN12 (exact byte-for-byte content of .remedy-wt/f106-r12-plan.md;
apply via shutil.copyfile, never retype):

# Plan — F106 Session resume instead of rebuild

Branch: feature/f106-session-resume, cut from `main` at `811c2d7e`.
SESSION 4, round 12.

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
| T002b-ii step 2a: freeze the hunk-rendering convention | done | round 11 |
| T002b-ii step 2b (Builder side): wire the shrink in | done | this round |
| R-0759: `resume`-kwarg gap in `test_repair_loop.py` (4 classes) | open | next |
| T002b-ii step 2b (Reviewer side): wire the shrink in | open | after R-0759 |
| T003: measured fixture comparison + docs | open | |

## Next Steps
1. R-0759: add `resume: str | None = None` to the four affected
   `.review()` signatures in `tests/orchestration/test_repair_loop.py`
   (two separate `IncoherentReviewer` locals, `BadReviewer`,
   `FailNothingReviewer`), an honest ignored no-op, mirroring R-0758's fix.
2. T002b-ii step 2b, Reviewer side: mirror this round's Builder-side design
   in `compose_reviewer_prompt` — a `resume_hunks_text` param replacing
   whichever of `reviewer_focused_diff`/`reviewer_staged_diff` would
   otherwise fire, fed from `reviewer_resume_ref` (round 9) at the call
   site; add a resume-active fixture to `test_reviewer_prompt_golden.py`.
3. T003 follows once step 2b is closed on both sides.

## Risks
- No adapter's `supports_resume` is true in production yet — only
  `FakeProvider` ever resumes or fails a resume.
- The Reviewer side (step 2b) has FOUR diff-shaped segment variants
  (scoped/unscoped × safe_diff/diff_summary) versus the Builder's one;
  round 13's design must state which variants the shrink applies to
  (almost certainly only the two `safe_diff`-backed ones, since
  `reviewer_resume_ref` is non-None only `if is_repair`).
- DECISION F106 D1's D1-compatibility reading still governs both sides.
