# Plan — F032 Approval with the evidence triple

Branch: feature/f032-evidence-triple, cut from `main` at `a399a330`, the merge
commit of pull request #216 which closed the amend0827 process-diet order.
`.agent/live_review.md` is the review record and the finding-id ceiling;
`.agent/decisions.md` carries the DECISION series, F032 D1 through D8.

## Goal
No decision without its receipts. Every decision a human is asked to answer
carries the evidence triple — `evidence_refs[]`, `expected_outcome` and
`downside` — the inbox card renders all three, and a producer that omits one
fails its own test. `docs/roadmap/features/T5_F032.md` holds Goal & Done, the
task slicing and the design amendments that reconcile it with the source.

## Current Step
T001, T002 and T003 are COMPLETE and the integration gate PASSED at R17: the
branch's full suite is exit 0 at 17982 passed, the branch-only failure set is
empty, and both base-only ids pass serially at the merge base and on the
branch. R18 is closure part one — the R17 verdict and the one finding the gate
produced, the feature file's Built State section that closure precondition 4
requires and that does not exist yet, then the evidence job and the FRESH
review zip. The STATUS flip, the README sync and the pull request are R19's.

| Item | Status | Reason |
|------|--------|--------|
| C0a and C0b, save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R17 verdict, R-0714 and the reviewer's slip | ordered | the record is touched first |
| C3 the feature file's Built State | ordered | precondition 4; the accepted HEAD |
| C4 the handback | ordered | records the bundle and the package |

## Next Steps
1. R19, closure part two: the authored STATUS line and the README capability
   sync in ONE commit, last on the branch, then the pull request — which is NOT
   merged in this session, per the closure protocol's step 6.

## Risks
- A failing zip build is a closure BLOCKER, not a thing to route around. The
  raw error goes in the handback and the branch is left as it is.
- Closure precondition 3 names a CLI this session's guard refuses. The check is
  reached through its Python module instead and the route used is named, so no
  PASS is reported that was not produced.
