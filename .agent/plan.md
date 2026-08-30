# Plan — F106 Session resume instead of rebuild

Branch: feature/f106-session-resume, cut from `main` at `811c2d7e`.
SESSION 1, round 2.

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
| T001a: Protocol + evidence fields + FakeProvider | done | this round |
| T001b: ClaudeProvider + ClaudeCliProvider, same surface | open | next round |
| T001c: `tests/orchestration/test_session_resume.py` | open | round 4, once all 3 adapters conform |
| T002 repair-path integration + delta shrink + expired fallback | open | gated on T001; F111 already accepted |
| T003 measured fixture comparison + docs | open | |

## Next Steps
1. This round adds `supports_resume`, the `resume` kwarg, and the two
   evidence fields to the Protocol and to `FakeProvider` only.
2. The next round does the identical mechanical addition to
   `ClaudeProvider` and `ClaudeCliProvider` — no new design, same shape.
3. Round 4 writes the dedicated test file once all three adapters share the
   same surface, closing T001.

## Risks
- None new this round. Carried from round 1: only `ClaudeCliProvider`
  reports a session id today; no adapter's `supports_resume` turns True
  until T002 wires real resume behavior.
