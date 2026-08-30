# Plan — F106 Session resume instead of rebuild

Branch: feature/f106-session-resume, cut from `main` at `811c2d7e`.
SESSION 3, round 10.

## Goal
Repair rounds stop resending the world: where the provider supports resuming
a session, a repair call resumes the original session and sends only the
findings delta, with an honest automatic fallback to full context when the
session is gone, flagged in evidence. Correctness never depends on resume
working.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| T001 (a/b/c): capability surface, all 3 adapters, tests | done | rounds 2-4 |
| T002a: Builder repair call resumes when earned | done | round 5 |
| T002b-i: Reviewer repair call resumes when earned | done | round 6 |
| T002c (i+ii): fallback-once, both sides | done | rounds 7-8 |
| T002b-ii step 1: hoist resume-ref before prompt build | done | round 9 |
| R-0758: fix `test_provider_retry.py`'s `resume`-kwarg gap | done | this round |
| T002b-ii step 2: the actual delta-prompt shrink | open | next |
| T003: measured fixture comparison + docs | open | |

## Next Steps
1. T002b-ii step 2: per DECISION F106 D1, reuse `parse_diff_line_ranges`/
   `select_repair_hunks` gated on the hoisted resume-ref to shrink the
   repair-diff prompt segment when a session is being resumed; invent and
   freeze a hunk-rendering convention (none exists to borrow); reconcile
   against the prompt-golden test files only if their segment set changes.
2. T003 follows once T002 is fully closed (after T002b-ii step 2 lands).

## Risks
- No adapter's `supports_resume` is true in production yet — only
  `FakeProvider`, via its test-only constructor overrides, ever resumes
  or fails a resume. This round's fix touches only four test-only
  provider subclasses in `test_provider_retry.py`, adding an accepted,
  honestly-forwarded `resume` kwarg that changes no test's assertions.
- DECISION F106 D1's D1-compatibility reading (reusing F111's pure hunk
  functions for prompt content, never the diff-apply channel) governs
  step 2's design; step 2 must not widen it further without a new DECISION.
