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
