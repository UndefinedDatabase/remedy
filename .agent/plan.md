# Plan — F037 Rendered diff viewer

Branch: feature/f037-rendered-diff-viewer, cut from `main` at `9dde5495`, the
merge commit of pull request #217 which closed F032.
`.agent/decisions.md` carries the DECISION series, F037 D1 through D4.

## Goal
Changes become readable, not merely present. The server parses a unified diff
into structured JSON — files, hunks, lines, intraline spans — served as a read
endpoint, and the client renders it with a file sidebar, hunk collapse, virtual
scrolling and lazily loaded syntax bundles.
`docs/roadmap/features/T5_F037.md` holds Goal & Done, the task slicing, the
binding CSS and the design amendments A1 through A4.

## Current Step
R10 opens session 3. It books the R9 verdict and repairs `R-0720`, a blindness
the reviewer measured in R9's own conformance guard: the guard's failure message
names declaration ORDER as what keeps ligatures off, and the guard never checks
it, so moving `font-feature-settings` above the `font` shorthand leaves the suite
green while the diff surface composes glyphs.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R9 verdict and R-0720 | ordered | record first, before the repair |
| C3 the ordering assertion | ordered | must go red on the reorder alone |
| C4 the resolution | ordered | written after the repair is proved |
| C5 the handback | ordered | |

## Next Steps
1. R11 closes T001's last named corpus shape, the huge diff. The task slicing
   lists "huge file chunking" and no test in the corpus names one; the parser
   carries no size bound of its own, since `truncated` is only relayed from an
   upstream sentinel.
2. R12 records the same budget where the JSON is actually serialised, at the
   read endpoint.
3. T002's rendering core and all of T003 stay BLOCKED. `npx vitest`, the `npm`
   script and the direct binary were refused again while planning R10, for the
   reviewer, as they were for both roles at R8.

## Risks
- The binding CSS defines no intraline treatment while Acceptance requires
  intraline emphasis. Inventing a colour early would breach the feature file's
  own banner, so it stays a question for the round that renders spans.
- A parse budget is a number from one host. R11 must record it as a measurement
  naming its machine, never as a portable ceiling, or the suite turns flaky on a
  slower runner.
