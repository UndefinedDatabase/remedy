# Plan — F106 Session resume instead of rebuild

Branch: feature/f106-session-resume, cut from `main` at `811c2d7e`.
SESSION 2, round 8.

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
| T002c-i: Builder fallback-once on a failed resume | done | round 7 |
| T002c-ii: Reviewer fallback-once mirror | done | this round |
| T002b-ii: F111 delta prompt shrink | open | next |
| T003: measured fixture comparison + docs | open | |

## Next Steps
1. T002b-ii: the delta-prompt shrink via F111's existing diff-repair hunk
   selection. Needs its own research pass into the hunk-selection code
   before design — not started.
2. T003 follows once T002 is fully closed (after T002b-ii lands).

## Risks
- No adapter's `supports_resume` is true in production yet — only
  `FakeProvider`, via its test-only constructor overrides, ever resumes
  or fails a resume. None of T002a/b-i/c-i/c-ii changes observable
  behavior for `ClaudeProvider`/`ClaudeCliProvider`, or for a
  default-constructed `FakeProvider`.
