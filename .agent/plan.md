# Plan — F106 Session resume instead of rebuild

Branch: feature/f106-session-resume, cut from `main` at `811c2d7e`.
SESSION 2, round 6.

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
| T002b-i: Reviewer repair call resumes when earned | done | this round |
| T002b-ii: F111 delta prompt shrink | open | next |
| T002c: expired-session fallback-once rule (verbatim) | open | |
| T003: measured fixture comparison + docs | open | |

## Next Steps
1. T002b-i mirrors T002a on the Reviewer side: the repair round's PRIMARY
   `review()` attempt now passes `resume=<prior round's captured Reviewer
   session id>` under the identical three-way guard. The bounded parse
   retry (a different call, same round) is NOT threaded — a declared
   scope line, not an oversight.
2. T002b-ii: the delta-prompt shrink via F111's existing diff-repair hunk
   selection — the repair prompt drops the regions the resumed session
   already holds. Not started.
3. T002c: the fallback-once rule verbatim (Orchestrator brief).
4. T003 follows once T002 is fully closed.

## Risks
- No adapter's `supports_resume` is true in production yet — only
  `FakeProvider`, via its test-only constructor override, ever resumes.
  Neither T002a nor T002b-i changes observable behavior for
  `ClaudeProvider`/`ClaudeCliProvider`, or for a default-constructed
  `FakeProvider`.
