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
R5 closes the parser's verification gaps and ends the session. It books R4,
resolves `R-0716`, and registers and repairs two defects the R4 red-proofs
exposed: `R-0717`, the intraline side mapping is pinned only for `replace`
opcodes, and `R-0718`, the similarity guard cannot fire for a multi-word line
because separator tokens floor its ratio. Both repairs are proved by the reds
their own fixtures now cause.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R4 gate, the resolution and both registrations | ordered | record first |
| C3 the `R-0717` discriminating fixtures | ordered | must kill both mutations |
| C4 the `R-0718` repair and its test | ordered | ratio over significant tokens |
| C5 the handback | ordered | last round of the session |

## Next Steps
1. The read endpoint, keyed on task run and job per DECISION F037 D2, against
   the route guards the R1 inventory measured. That is what T001 still owes.
2. T002 the rendering core, the binding CSS and the goldens.
3. T003 sidebar, virtual scrolling, lazy languages and the L3 tab.

## Risks
- `R-0715` is open and Low; it is a stale count in a test docstring and belongs
  to whoever next edits that file.
- The parser still has no consumer, so its corpus carries the whole weight.
  Every round that touches it orders mutation red-proofs for that reason, and
  R4 is the round that proved why: a red-proof reported green is how both of
  this round's findings were found.
