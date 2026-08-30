# Plan — F106 Session resume instead of rebuild

Branch: feature/f106-session-resume, cut from `main` at `811c2d7e`. SESSION 1,
opening the feature.

## Goal
Repair rounds stop resending the world: where the provider supports resuming
a session, a repair call resumes the original session and sends only the
findings delta, with an honest automatic fallback to full context when the
session is gone, flagged in evidence. Correctness never depends on resume
working.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| the F106 claim and the branch | done | this round |
| the shape inventory | done | this round, `.agent/f106_inventory.md` |
| T001 capability + resume param + evidence fields + tests | open | next round |
| T002 repair-path integration + delta shrink + expired fallback | open | gated on T001; F111 already accepted |
| T003 measured fixture comparison + docs | open | |

## Next Steps
1. This round claims F106 and measures the exact call-entry/evidence shape
   T001 builds on, into `.agent/f106_inventory.md` — no code this round.
2. The next round orders T001: `supports_resume` on the provider protocol
   and its three adapters, an additive `resume` kwarg on `build`/`review`,
   `resume_used`/`resume_session_ref` on `BuilderOutput`/`ReviewerOutput`,
   all False/"" by construction — zero behavior change — plus
   `tests/orchestration/test_session_resume.py`.
3. T002 is gated on diff-repair (F111, "Diff-only repair"); F111 is already
   accepted (STATUS.md, 2026-08-13), so that gate is satisfied.

## Risks
- The orchestrator brief demands the fallback-once rule verbatim in the T002
  order — carry it forward, do not soften it.
- Only `ClaudeCliProvider` reports a session id today; T001 keeps
  `supports_resume` False on all three adapters regardless — turning one
  True is T002's call once resume is actually wired to CLI behavior.
