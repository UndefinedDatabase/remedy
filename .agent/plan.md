# Plan — F106 Session resume instead of rebuild

Branch: feature/f106-session-resume, cut from `main` at `811c2d7e`.
SESSION 5, round 15.

## Goal
Repair rounds stop resending the world: where the provider supports resuming
a session, a repair call resumes the original session and sends only the
findings delta, with an honest automatic fallback to full context when the
session is gone, flagged in evidence. Correctness never depends on resume
working.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| T001, T002a, T002b-i, T002c, T002b-ii (both sides), R-0758, R-0759 | done | rounds 2-14 |
| T003: measured fixture comparison + docs | this round | round 15 |

## Next Steps
1. Once T003 lands, F106 moves to closure per
   docs/roadmap/STATUS_closure_protocol.md: evidence job + fresh review zip,
   the authored STATUS line, PR creation.

## Risks
- No adapter's `supports_resume` is true in production yet — only
  `FakeProvider` ever resumes or fails a resume; T003's fixture chain is
  necessarily `FakeProvider`-driven for the same reason T001-T002 were.
- DECISION F106 D1's D1-compatibility reading governed both sides of the
  shrink; T003 measures the OUTCOME of that decision, not a new one.
