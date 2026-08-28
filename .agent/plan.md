# Plan — F037 Rendered diff viewer

Branch: feature/f037-rendered-diff-viewer, cut from `main` at `9dde5495` (the
merge of PR #217, which closed F032). `.agent/decisions.md` holds F037 D1 to D11.

## Goal
Changes become readable, not merely present. The server parses a unified diff
into structured JSON — files, hunks, lines, intraline spans — served as a read
endpoint, and the client renders it with a file sidebar, hunk collapse and
virtual scrolling. `docs/roadmap/features/T5_F037.md` holds Goal & Done, the task
slicing, the binding CSS, the design amendments A1 through A6 and the Built State
section recording what actually shipped.

## Current Step
R27 is the CLOSURE round, the last of F037's closure sequence and the last round
of this branch. Every closure precondition is met: the integration gate PASSED at
R25 with no branch-only failure reaching feature code, the R26 package is
READY_FOR_REVIEW at accepted head `5e557a1c`, the integrity gate passes with zero
failures, and F037 carries no open finding of its own. This round books the R26
verdict, flips the STATUS line to `[x]`, syncs the four README pins in that same
commit, and opens the PR — which is NOT merged here.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R26 verdict | ordered | record first |
| C3 STATUS, README and the handback | ordered | one commit, last on the branch |
| the closure PR | ordered | created, never merged |

## Next Steps
1. A fresh session claims the next feature by Rule A5 — `F033 Hunk-level diff
   approval` — and its Open PR Gate merges this feature's PR first.
2. The split-off scope of amendment A6 wants its own STATUS line before F033.
   That remains a PROPOSAL to the operator and is executed by no session.

## Risks
- `R-0714` closes OPEN as a documented Medium risk: a ui_server test runs a real
  frontend build from inside the suite, which F037 does not own and did not
  cause. Closure precondition 1 admits exactly this case.
- The STATUS and README edits must land in ONE commit or the ledger pins in
  `tests/docs/` go red; the reviewer measured that red as the control.
