# Plan — F037 Rendered diff viewer

Branch: feature/f037-rendered-diff-viewer, cut from `main` at `9dde5495`, the
merge commit of pull request #217 which closed F032.
`.agent/decisions.md` carries the DECISION series, F037 D1 through D5.

## Goal
Changes become readable, not merely present. The server parses a unified diff
into structured JSON — files, hunks, lines, intraline spans — served as a read
endpoint, and the client renders it with a file sidebar, hunk collapse, virtual
scrolling and lazily loaded syntax bundles.
`docs/roadmap/features/T5_F037.md` holds Goal & Done, the task slicing, the
binding CSS and the design amendments A1 through A4.

## Current Step
R12 repairs `R-0721`: the parser bounds its own output at
`DIFF_VIEW_MAX_BODY_LINES` and sets the contract's `truncated` flag when the bound
bites, so that flag becomes something F037 decides rather than only a relay of an
upstream sentinel. The ceiling is twice the 10k fixture Acceptance names, so that
fixture still renders in full. DECISION F037 D5 records the value and how to
reverse it.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R11 verdict and the timing slip | ordered | record first |
| C3 DECISION F037 D5 and the ceiling | ordered | the choice beside what it governs |
| C4 the boundary tests | ordered | both sides of the ceiling, or an off-by-one hides |
| C5 the resolution | ordered | written after the repair is proved |
| C6 the handback | ordered | |

## Next Steps
1. R13 carries the other half of `R-0721`: `diff_view_source.py` reads the whole
   artifact with `read_text` before the parser ever sees it, so the input is
   still unbounded even once the output is not.
2. T002's rendering core and all of T003 stay BLOCKED. `npx vitest`, the `npm`
   script and the direct binary were each refused again while planning R10, for
   the reviewer, as they were for both roles at R8.

## Risks
- A ceiling is a behaviour change on a shipped read path. The four tests R11 added
  are the regression guard and constraint 5 forbids touching them; if one of them
  moves, the ceiling was chosen wrong rather than the test being stale.
- The binding CSS defines no intraline treatment while Acceptance requires
  intraline emphasis. Inventing a colour early would breach the feature file's
  own banner, so it stays a question for the round that renders spans.
