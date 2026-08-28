# Plan — F037 Rendered diff viewer

Branch: feature/f037-rendered-diff-viewer, cut from `main` at `9dde5495` (the
merge of PR #217, which closed F032). `.agent/decisions.md` holds F037 D1 to D10.

## Goal
Changes become readable, not merely present. The server parses a unified diff
into structured JSON — files, hunks, lines, intraline spans — served as a read
endpoint, and the client renders it with a file sidebar, hunk collapse, virtual
scrolling and lazily loaded syntax bundles.
`docs/roadmap/features/T5_F037.md` holds Goal & Done, the task slicing, the
binding CSS and the design amendments A1 through A5.

## Current Step
R21 gives `computeDiffRowWindow` its caller. The division a viewport forces —
scroll offset and panel height into row indices — goes into `diffViewModel.ts`
as `diffRowWindowForViewport`, so the rule stays where vitest executes it and
`DiffView` keeps deriving nothing. The trap it exists to resolve is an
unmeasured panel: `clientHeight` is 0 on first render, 0 divides to a visible
count of 0, and an empty window draws no rows, so the panel never scrolls and
never gets measured. R20's five reported stale comments are repaired, closing
`R-0727`.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R20 verdict and two resolutions | ordered | record first |
| C3 DECISION F037 D10 | ordered | it licenses this round's own red-proofs |
| C4 the five staleness repairs | ordered | closes `R-0727` |
| C5 the viewport rule and its vitest tests | ordered | before its caller |
| C6 the wiring | ordered | the window becomes real |
| C7 the guards over the wiring | ordered | after the code they read |
| C8 the handback | ordered | |

## Next Steps
1. The lazy language bundles, unknown languages rendering plain with no bundle
   fetch, which Acceptance names.
2. The 10k-line perf fixture measured END TO END and its numbers recorded; S3 of
   this round bounds the window's row count but times nothing.
3. A ruling on the sidebar's visual treatment, still owed.

## Risks
- Round 21 of a 25-round soft limit, session 6 of 7. Two named pieces remain
  after this round. If both do not fit in session 7, that session owes a SCOPE
  REPORT rather than more work.
- Nothing here renders a `.tsx` file, so S4 is gated by text and `tsc --noEmit`
  alone, as every `.tsx` round of this feature has been.
