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
R11 closes the one shape T001's task slicing names and the corpus never grew —
the huge diff — and records the perf number Acceptance asks for. It changes no
parser behaviour. It also registers `R-0721`: nothing in F037 bounds the work one
diff can cost, and the contract's own `truncated` field is only ever relayed from
an upstream sentinel, never set by this feature.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R10 verdict and R-0721 | ordered | record first; nothing is resolved |
| C3 the huge-diff corpus shape | ordered | structure, numbering, scale, budget |
| C4 the handback | ordered | |

## Next Steps
1. R12 repairs `R-0721`: a line ceiling the parser enforces itself, setting the
   contract's `truncated` flag when it bites, with the ceiling above the 10k
   fixture Acceptance names so that fixture still renders in full.
2. R13 carries the same bound at the endpoint, where the artifact is read whole
   into memory before the parser ever sees it.
3. T002's rendering core and all of T003 stay BLOCKED. `npx vitest`, the `npm`
   script and the direct binary were each refused again while planning R10, for
   the reviewer, as they were for both roles at R8.

## Risks
- A wall-clock assertion is the flakiest thing a suite can hold. R11's ceiling is
  set an order of magnitude above the measured figure so it separates linear from
  quadratic cost and nothing finer; tightening it later would buy noise.
- The binding CSS defines no intraline treatment while Acceptance requires
  intraline emphasis. Inventing a colour early would breach the feature file's
  own banner, so it stays a question for the round that renders spans.
