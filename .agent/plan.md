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
R20 closes what R19 left open and starts the last named piece. `DiffView.tsx`
still tells its reader the component is not mounted, two rounds after R18
mounted it, which is `R-0727`. The collapse-threshold count guard counts a bare
substring, so the `2000` this feature needs next would turn it red for breaking
nothing — `R-0728`, measured rather than predicted. The `R-0726` repair landed in
source at R19 and no gate catches the button moving back, so it gets one. Then
the windowing rule of "virtual scrolling >2k lines" is built in `diffViewModel.ts`
where vitest really runs it; no component is wired to it this round.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R19 verdict, two resolutions, two findings | ordered | record first |
| C3 the R-0727 comment repair | ordered | it has been false for two rounds |
| C4 the R-0728 count-anchor repair | ordered | before C6 needs it |
| C5 the R-0726 placement gate | ordered | the repair is real but ungated |
| C6 the windowing rule and its vitest tests | ordered | the last named piece |
| C7 the handback | ordered | |

## Next Steps
1. Wire the window into `DiffView`, with the perf fixture Acceptance requires:
   the 10k-line fixture within budget, and the numbers recorded.
2. The lazy language bundles, unknown languages rendering plain with no bundle
   fetch, which Acceptance also names.
3. A ruling on the sidebar's visual treatment, still owed.

## Risks
- Round 20 of a 25-round soft limit, and this is the last round of session 5 of
  7. If the wiring, the perf fixture and the lazy bundles do not all fit in the
  next session, the one after it owes a scope report rather than more work.
- Nothing in this repository renders a `.tsx` file, so the wiring of step 1 will
  be gated by text and `tsc --noEmit` alone, as every `.tsx` round here has been.
