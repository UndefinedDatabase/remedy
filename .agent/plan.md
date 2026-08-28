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
R19 closes the two gaps the R18 gate found and then draws the sidebar. The
remainder of `R-0725` is the task-run path's own ending, which no assertion
pins: renaming it alone left the guard green where its two repaired siblings now
go red. `R-0726` is sharper — the "Open diff" button sat inside the "Changed
files" section, which renders only on a non-empty `changedFilesSafe`, and that
list is built from apply EVENTS while the diff is a separate artifact, so the
viewer's only entry point was invisible for a task run holding a diff and no
safe file list. The button moves to popover level, which is where
`component_spec.md:108` lists it. Then `buildDiffFileSummaries`, exported since
R15 and drawn by nothing, becomes the file sidebar.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R18 verdict, R-0725 in part, R-0726 | ordered | record first |
| C3 the R-0725 remainder | ordered | after the record |
| C4 the R-0726 repair | ordered | the entry point becomes reachable |
| C5 the file sidebar and its DOM anchor | ordered | the drawing half |
| C6 the sidebar guard | ordered | nothing here can render a component |
| C7 the handback | ordered | |

## Next Steps
1. Virtual scrolling beyond two thousand lines, which the Design section names
   and which the row list already makes possible.
2. The lazy language bundles, and the perf fixture whose numbers Acceptance
   requires recorded.
3. A ruling on the sidebar's visual treatment: the Design names "paths + stats
   bars", the binding CSS defines neither, so R19 ships semantics only.

## Risks
- Round 19 of a 25-round soft limit, session 5 of 7. Virtual scrolling, the lazy
  bundles, the perf fixture and the sidebar's styling remain.
- Nothing in this repository renders a `.tsx` file, so every guard here reads
  text and `tsc --noEmit` does the rest.
