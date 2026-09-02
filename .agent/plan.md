# Plan — F106 Session resume instead of rebuild

Branch: feature/f106-session-resume, cut from `main` at `811c2d7e`.
SESSION 5, round 17.

## Goal
Repair rounds stop resending the world: where the provider supports resuming
a session, a repair call resumes the original session and sends only the
findings delta, with an honest automatic fallback to full context when the
session is gone, flagged in evidence. Correctness never depends on resume
working.

## Current Step

T001, T002 (both sides) and T003 are ALL DONE. The round 16 integration
gate found R-0760 (Medium, OPEN): 5 fake provider/reviewer classes across
3 test files never got the additive `resume` no-op parameter. This round
REPAIRS R-0760 — the same additive fix shape already used twice
(R-0758, R-0759 — both CLOSED).

## Next Steps
1. This round: apply the additive `resume: str | None = None` parameter to
   the 7 named signatures (5 classes, 2 of them carrying both `build` and
   `review`) across `test_structured_outputs.py`, `test_worktree_isolation.py`
   and `test_worktree_persistence.py`; confirm 0 failures.
2. Next: re-run the FULL integration gate (branch only — the base side is
   unaffected by a test-only fix) to confirm the gate is clean; only then
   does F106 move on to the feature file's Built State section
   (precondition 4) and the rest of the closure sequence.

## Risks
- This is a test-only fix (zero behavior change to any production code) —
  confirm via `git diff --stat -- packages/` staying empty this round.
