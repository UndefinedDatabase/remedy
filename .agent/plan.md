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
R20 REPAIRS the closure evidence. R19 committed everything correctly and could
not build its artifacts because the reviewer's evidence script parsed node ids
out of `-v` output and one parametrised id in this feature's own suite contains
whitespace. This round registers that as R-0611, records the R19 verdict, and
re-runs the evidence job with ids taken from `--collect-only`, then builds the
review zip.

## Next Steps
1. R21 CLOSES THE FEATURE: the reviewer authors the STATUS `[x]` line from the
   values THIS round's zip reports, the worker applies it verbatim in the SAME
   commit as the README capability sync (R-0154), writes any closure candidates
   to `.agent/candidates.md`, and opens the pull request. That PR is NOT merged
   in its own session; it merges at the NEXT feature's Open PR Gate, which is the
   operator's manual-review window.

## Risks
- A FAILING ZIP IS A CLOSURE BLOCKER, not a retry. The feature goes `[!]` with a
  stated reason rather than closing without a package.
- THE CLOSURE PRECONDITIONS OTHER THAN THE PACKAGE ARE MET AND MEASURED: the
  integrity gate passes with no open blocker or high finding, the Built State
  section landed at R19, the full suite passed the R18 gate with 0 branch-only
  failures, and the tree is clean and pushed.
- R-0607, R-0608, R-0609 AND R-0611 REMAIN OPEN by design: all four are
  reviewer-process defects whose fixes edit `docs/agents/` or the closure
  protocol, paths the closure commit's own R-0154 path set cannot reach.
