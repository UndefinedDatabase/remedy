# Plan — F037 Rendered diff viewer

Branch: feature/f037-rendered-diff-viewer, cut from `main` at `9dde5495`, the
merge commit of pull request #217 which closed F032.
`.agent/live_review.md` is the review record and the finding-id ceiling;
`.agent/decisions.md` carries the DECISION series, F037 D1 onward.

## Goal
Changes become readable, not merely present. The server parses a unified diff
into structured JSON — files, hunks, lines, intraline spans — served as a read
endpoint, and the client renders it with a file sidebar, hunk collapse, virtual
scrolling and lazily loaded syntax bundles.
`docs/roadmap/features/T5_F037.md` holds Goal & Done, the task slicing, the
binding CSS and — from this round — the design amendments that reconcile it
with the source.

## Current Step
R2 books the R1 verdict, registers `R-0715`, records the reviewer's authoring
slip, and lands the DECISIONS the R1 inventory forced together with the
feature-file amendments they rule. The inventory measured that no vocabulary in
this repository carries a `binary` file status and that no per-attempt diff
exists anywhere, so the spec is amended on disk before T001 is planned against
it.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the record, the finding, the slip, both DECISIONS | ordered | record first |
| C3 the feature-file amendments | ordered | the spec moves on disk |
| C4 the handback | ordered | |

## Next Steps
1. T001: the unified-to-JSON parser as a NEW module with its corpus tests, then
   the read endpoint, planned against the amended spec.
2. T002 the rendering core, the binding CSS and the goldens.
3. T003 sidebar, virtual scrolling, lazy languages and the L3 tab.

## Risks
- `R-0715` is open and Low. It is a stale count in a test docstring, turns
  nothing red, and belongs to whoever next edits that file.
- The amended spec drops the endpoint's attempt parameter for v1. If a later
  feature makes per-attempt diffs real, DECISION F037 D2 names how to reverse
  that.
