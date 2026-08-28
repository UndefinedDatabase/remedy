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
R22 builds the last named piece, lazy language bundles, in the layer vitest
executes. Acceptance states one property in so many words — an unknown language
renders plain WITHOUT a bundle fetch — so the loader takes its importer as an
ARGUMENT, the way `loadDiffEnvelope` takes its fetcher, and a counting importer
in the test proves the count is zero rather than merely that the answer is
plain. No component is wired this round. Three comments R21's own code falsified
are repaired first: `R-0729`, a docstring telling future rounds that a
TypeScript red-proof cannot be ordered, which DECISION F037 D10 disproved, and
`R-0730`, two stale sentences in the model.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R21 verdict and two findings | ordered | record first |
| C3 the three comment repairs | ordered | one misleads future rounds |
| C4 the language rule and its tests | ordered | |
| C5 the lazy loader and its tests | ordered | the Acceptance property |
| C6 the guards | ordered | after the code they read |
| C7 the handback | ordered | |

## Next Steps
1. Wire highlighting into `DiffView`, and the 10k-line perf fixture measured END
   TO END with its numbers recorded, which Acceptance requires.
2. A ruling on the sidebar's visual treatment, still owed.
3. Then T003 is complete and the closure sequence can begin.

## Risks
- Round 22 of a 25-round soft limit, and session 6 of 7. Three named pieces
  remain across two Next Steps. If they do not fit by round 25, the session that
  reaches it owes a SCOPE REPORT rather than more work.
- Nothing here renders a `.tsx` file, so the wiring of step 1 will be gated by
  text and `tsc --noEmit` alone, as every `.tsx` round of this feature has been.
