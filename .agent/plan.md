# Plan — F255 Teacher role

Branch: feature/f255-teacher-role, cut from `main` at b35d350b, the merge commit
of pull request #207. No pull request is open for this branch; on this project
the PR is created by the closure round.
`.agent/live_review.md` is the source of truth for the open set, for the next
free finding id and for the round map; this file repeats none of them.

## Goal
A fourth configured role, `teacher`, that narrates a running mission and answers
operator questions about the operator's own code, and never influences the run.
DONE when passive narration keyed to an enumerated set of ledger events (Stage 1,
deterministic templates, zero tokens) and on-demand Q&A (Stage 2, through the
teacher role's own model) both work, the three grounding sources are never mixed
silently, teacher spend is reported as its own role in the F103 ledger, and the
read-only invariant is proven behaviourally.

## Current Step
R19 is the CLOSURE EVIDENCE round. It persists the R18 verdict, resolves R-0610,
adds the feature file's Built State section — closure precondition 4, measured
absent — and then produces the two artifacts only a worker can make: the evidence
job and a FRESH review zip. It authors no STATUS line.

## Next Steps
1. R20 CLOSES THE FEATURE: the reviewer authors the STATUS `[x]` line from the
   values R19's zip reports, the worker applies it verbatim in the SAME commit as
   the README capability sync (R-0154), writes any closure candidates to
   `.agent/candidates.md`, and opens the pull request. That PR is NOT merged in
   its own session; it merges at the NEXT feature's Open PR Gate, which is the
   operator's manual-review window.

## Risks
- A FAILING ZIP IS A CLOSURE BLOCKER, not a retry. The feature goes `[!]` with a
  stated reason rather than closing without a package.
- THE OPEN SET STAYS LARGE AND THAT IS NOT A BLOCKER: the integrity gate's
  `high_blockers_open` check reports no open blocker or high finding, so every
  open item is a documented Medium or Low risk, which is what closure
  precondition 1 permits.
- R-0607, R-0608 and R-0609 REMAIN OPEN by design. All three are reviewer-process
  defects whose fix edits `docs/agents/`, a path the closure commit's own R-0154
  path set cannot reach; they route to a paydown branch.
