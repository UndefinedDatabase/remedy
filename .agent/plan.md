# Plan — F037 Rendered diff viewer

Branch: feature/f037-rendered-diff-viewer, cut from `main` at `9dde5495` (the
merge of PR #217, which closed F032). `.agent/decisions.md` holds F037 D1 to D11.

## Goal
Changes become readable, not merely present. The server parses a unified diff
into structured JSON — files, hunks, lines, intraline spans — served as a read
endpoint, and the client renders it with a file sidebar, hunk collapse and
virtual scrolling. `docs/roadmap/features/T5_F037.md` holds Goal & Done, the task
slicing, the binding CSS and the design amendments A1 through A6, the last of
which records what this feature deliberately no longer ships.

## Current Step
R26 is the EVIDENCE-AND-ZIP round, the second of F037's closure sequence. The
integration gate PASSED at R25: branch and merge base each showed one failure,
both serial-pass flakes, with no branch-only failure reaching feature code. This
round books the R25 verdict, appends the feature file's Built State section so
closure precondition 4 holds, then builds the `f037-closure` evidence bundle and
a FRESH review package from the clean tree at the Built State commit. Nothing
under `apps/`, `packages/` or `tests/` is touched.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R25 verdict | ordered | record first |
| C3 the Built State section | ordered | closure precondition 4 |
| the evidence job and the review zip | ordered | from the clean tree at C3 |
| C4 the handback | ordered | carries package, hash and path |

## Next Steps
1. The STATUS round: the `[x]` line for F037, the README capability paragraph,
   the README accepted count with its `Next:` clause and the README tier row —
   all four in the SAME commit — then the closure PR, which is not merged here.
2. The split-off scope of amendment A6 wants its own STATUS line. That remains a
   PROPOSAL to the operator and is executed by no session.

## Risks
- A failing zip build is a closure BLOCKER, not a deviation. If it packages
  BLOCKED_EVIDENCE, the round stops and hands back with the raw error.
- `R-0714` stays open and is carried into closure as a documented Medium risk:
  it is a defect in a ui_server test, out of F037's scope, and fixing it here
  would be scope drift.
