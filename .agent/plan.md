# Plan — F255 Teacher role

Branch: feature/f255-teacher-role, cut from `main` at b35d350b, the merge commit
of pull request #207. The closure pull request is created by THIS round and is
NOT merged in this session; it merges at the next feature's Open PR Gate.
`.agent/live_review.md` is the source of truth for the open set, for the next
free finding id and for the round map; this file repeats none of them.

## Goal
A fourth configured role, `teacher`, that narrates a running mission and answers
operator questions about the operator's own code, and never influences the run.
DONE when passive narration keyed to an enumerated set of ledger events (Stage 1,
deterministic templates, zero tokens) and on-demand Q&A (Stage 2, through the
teacher role's own model) both work, the three grounding sources are never mixed
silently, teacher spend is reported as its own role in the F103 ledger, and the
read-only invariant is proven behaviourally. ALL FOUR HOLD and are reviewed.

## Current Step
R21 CLOSES F255. It records the R20 verdict, writes the STATUS `[x]` line with
the package and `accepted HEAD` values R20 produced, syncs the README count, tier
table and accepted list in the SAME commit, empties the closure-candidate
carrier, and opens the pull request.

## Next Steps
1. The next session's FIRST action is Phase 1 rule 1, the `.agent/STOP` re-read,
   and its SECOND is the Open PR Gate, which merges this feature's pull request
   before any new branch is cut. Rule A5 then selects F008 — SSE event stream —
   as the next feature, it being the first `[ ]` in STATUS order.

## Risks
- FOUR FINDINGS REMAIN OPEN and none is a code defect: R-0607, R-0608, R-0609 and
  R-0611 are all reviewer-process defects whose fixes edit `docs/agents/` or the
  closure protocol, paths the closure commit's own R-0154 path set cannot reach.
  They route to a paydown branch and are named in the pull request.
- THE PACKAGE PACKAGES `.remedy-wt/` SCRATCH, which is the already-registered
  R-0403 and not a new condition of this closure.
