# Plan — F106 Session resume instead of rebuild

Branch: feature/f106-session-resume, cut from `main` at `811c2d7e`.
SESSION 5, round 18.

## Goal
Repair rounds stop resending the world: where the provider supports resuming
a session, a repair call resumes the original session and sends only the
findings delta, with an honest automatic fallback to full context when the
session is gone, flagged in evidence. Correctness never depends on resume
working.

## Current Step

T001, T002 (both sides) and T003 are ALL DONE. The round 16 integration
gate found R-0760; round 17 repaired it (independently confirmed, full
suite 18736 passed / 0 failed at both the worker's and the reviewer's own
from-scratch runs). This round books both pending verdicts (RECORD16,
RECORD17) and the `Done: R-0760` resolution — pure ledger bookkeeping,
permitted during the closure sequence (amend0827-process-diet rule 1).
Closure precondition 2 (a PASSING dedicated integration gate) is now MET:
round 16's base-side comparison is still valid (zero production change
since, confirmed by round 17's own G7) and round 17's branch-side re-run
is clean.

## Next Steps
1. Feature file Built State section (precondition 4) — describe what
   T001-T003 actually built, citing real files/functions/measured numbers.
2. Resolve the feature file's own job/mission-resume scope note (F075
   candidate routing, R-0201, also carried in `.agent/context.md`) against
   Task slicing — a DECISION, since Acceptance never required it and no
   round ever sliced it in.
3. Self-use track consumption (precondition 6), evidence job, review zip,
   STATUS line, PR — the closure algorithm's remaining steps.

## Risks
- None new this round — pure ledger bookkeeping, zero code/doc change.
