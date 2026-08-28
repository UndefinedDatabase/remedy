# Plan — F037 Rendered diff viewer

Branch: feature/f037-rendered-diff-viewer, cut from `main` at `9dde5495` (the
merge of PR #217, which closed F032). `.agent/decisions.md` holds F037 D1 to D9.

## Goal
Changes become readable, not merely present. The server parses a unified diff
into structured JSON — files, hunks, lines, intraline spans — served as a read
endpoint, and the client renders it with a file sidebar, hunk collapse, virtual
scrolling and lazily loaded syntax bundles.
`docs/roadmap/features/T5_F037.md` holds Goal & Done, the task slicing, the
binding CSS and the design amendments A1 through A5.

## Current Step
R18 makes the viewer real. `DiffView` has been on disk since R16 and mounted by
nothing; this round opens the door to it. `DetailPopover` grows the "Open diff"
button `component_spec.md` names, emitting `onOpenDiff(taskId)`; `RemedyShell`
holds which task run is open, reads its envelope through the door R17 built, and
draws `DiffView` behind it. A response arriving after the selection changed is
discarded rather than shown under the wrong task. The round also repairs finding
`R-0725`, the reviewer's own: two presence assertions in R17's cross-language
guard searched the whole module where they meant one function, so renaming the
job path alone, or replacing the reader call while keeping its import, left the
guard green.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R17 verdict and finding R-0725 | ordered | findings persist first |
| C3 the R-0725 repair | ordered | after the record, before the new work |
| C4 the entry point in DetailPopover | ordered | the button the spec names |
| C5 the mount in RemedyShell | ordered | state, read, drawing |
| C6 the mount guard | ordered | nothing here can render a component |
| C7 the handback | ordered | |

## Next Steps
1. The file sidebar over `buildDiffFileSummaries`, which the model already
   exports and nothing yet draws.
2. Virtual scrolling beyond two thousand lines, the lazy language bundles, and
   the perf fixture whose numbers Acceptance requires recorded.

## Risks
- Round 18 of a 25-round soft limit, session 5 of 7. The sidebar, the virtual
  scrolling, the lazy bundles and the perf fixture remain, so a round closing
  none of them is the one to stop and re-scope after.
- Nothing in this repository renders a `.tsx` file. This round's wiring is
  covered by `tsc --noEmit` and by text guards, and by nothing else — which is
  why the guard scopes to function bodies rather than to files.
