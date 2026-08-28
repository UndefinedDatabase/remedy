# Plan — F037 Rendered diff viewer

Branch: feature/f037-rendered-diff-viewer, cut from `main` at `9dde5495`, the
merge commit of pull request #217 which closed F032.
`.agent/live_review.md` is the review record and the finding-id ceiling;
`.agent/decisions.md` carries the DECISION series, F037 D1 and D2.

## Goal
Changes become readable, not merely present. The server parses a unified diff
into structured JSON — files, hunks, lines, intraline spans — served as a read
endpoint, and the client renders it with a file sidebar, hunk collapse, virtual
scrolling and lazily loaded syntax bundles.
`docs/roadmap/features/T5_F037.md` holds Goal & Done, the task slicing, the
binding CSS and the design amendments that reconcile it with the source.

## Current Step
R4 closes T001's parser half. It registers `R-0716` — the parser splits one
file into two entries for the `workspace.diff` shape, whose emitter writes the
header pair itself and then hands the same pair to `difflib` — repairs it in
the commit after the registration, and adds the intraline spans the contract's
line shape carries. The repair is proved by its own red before it lands.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R3 gate and the `R-0716` registration | ordered | findings persist first |
| C3 the `R-0716` repair and its regression test | ordered | red proved before green |
| C4 intraline spans and their tests | ordered | the contract's line shape |
| C5 the handback | ordered | |

## Next Steps
1. The read endpoint, keyed on task run and job per DECISION F037 D2, against
   the route guards the R1 inventory measured.
2. T002 the rendering core, the binding CSS and the goldens.
3. T003 sidebar, virtual scrolling, lazy languages and the L3 tab.

## Risks
- `R-0715` is open and Low; it is a stale count in a test docstring and belongs
  to whoever next edits that file.
- The parser still has no consumer, so its corpus carries the whole weight.
  Every round that touches it orders mutation red-proofs for that reason.
