# Plan — F106 Session resume instead of rebuild

Branch: feature/f106-session-resume, cut from `main` at `811c2d7e`.
SESSION 1, round 4.

## Goal
Repair rounds stop resending the world: where the provider supports resuming
a session, a repair call resumes the original session and sends only the
findings delta, with an honest automatic fallback to full context when the
session is gone, flagged in evidence. Correctness never depends on resume
working.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| the F106 claim, branch, shape inventory | done | round 1 |
| T001a: Protocol + evidence fields + FakeProvider | done | round 2 |
| T001b: ClaudeProvider + ClaudeCliProvider, same surface | done | round 3 |
| T001c: `tests/orchestration/test_session_resume.py` | done | this round — T001 CLOSED |
| T002 repair-path integration + delta shrink + expired fallback | open | next session; gated on T001 (done) and F111 (accepted) |
| T003 measured fixture comparison + docs | open | |

## Next Steps
1. T001 is complete: all three adapters share the `supports_resume`/
   `resume`/evidence-field surface, dedicated tests exist and pass, zero
   behavior change proved by property test and by the existing suite.
2. Next session opens T002: thread `resume`/session-id through the repair
   path in `packages/orchestration/pingpong_loop.py`, shrink the repair
   prompt via the existing diff-repair (F111) hunk selection, and
   implement the fallback-once rule verbatim per the Orchestrator brief.
3. T003 (measured fixture comparison + docs) follows T002.

## Risks
- None new. No adapter's `supports_resume` turns True until T002 actually
  wires resume behavior end to end — T001 only builds the honest surface.
