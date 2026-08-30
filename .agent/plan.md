# Plan — F106 Session resume instead of rebuild

Branch: feature/f106-session-resume, cut from `main` at `811c2d7e`.
SESSION 1, round 3.

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
| T001b: ClaudeProvider + ClaudeCliProvider, same surface | done | this round |
| T001c: `tests/orchestration/test_session_resume.py` | open | next round, closes T001 |
| T002 repair-path integration + delta shrink + expired fallback | open | gated on T001; F111 already accepted |
| T003 measured fixture comparison + docs | open | |

## Next Steps
1. This round applies the identical mechanical addition from round 2 to
   the two remaining adapters — no new design.
2. The next round writes `tests/orchestration/test_session_resume.py`
   covering all three adapters' `supports_resume`/`resume`/evidence-field
   shape, closing T001, then T002 (repair-path integration) can start.

## Risks
- None new. Carried forward: no adapter's `supports_resume` turns True
  until T002 wires real resume behavior.
