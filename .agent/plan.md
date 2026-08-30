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
