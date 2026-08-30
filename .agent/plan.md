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
