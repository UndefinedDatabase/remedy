# Plan — F106 Session resume instead of rebuild

Branch: feature/f106-session-resume, cut from `main` at `811c2d7e`.
SESSION 6, round 19.

## Goal
Repair rounds stop resending the world: where the provider supports resuming
a session, a repair call resumes the original session and sends only the
findings delta, with an honest automatic fallback to full context when the
session is gone, flagged in evidence. Correctness never depends on resume
working.

## Current Step
Closure preconditions 1-2 are MET (round 18). This round adds precondition
4: the feature file's Built State section, describing what T001-T003 built
with real file/function citations and the T003 measured byte-reduction
numbers. It also registers DECISION F106 D2, resolving the feature file's
own Scope note (job/mission resume-from-persisted-state, F075 candidate
routing R-0201) against Task slicing: closing on T001-T003 alone, with the
job/mission-resume half carried forward as a closure-commit candidate
rather than built now or silently dropped.

## Next Steps
1. The closure commit (when reached) adds ONE entry to
   `.agent/candidates.md` per DECISION F106 D2's own text — do not lose
   this obligation between now and then.
2. Precondition 3 (`remedy integrity check --json` / no relevant untracked
   files) and precondition 6 (self-use track consumption) are still open.
3. Evidence job, review zip, STATUS line, PR — the closure algorithm's
   remaining steps.

## Risks
- None new this round — docs/ledger-only change, zero code touched.
