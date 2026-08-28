# Plan — F037 Rendered diff viewer

Branch: feature/f037-rendered-diff-viewer, cut from `main` at `9dde5495`, the
merge commit of pull request #217 which closed F032.
`.agent/live_review.md` is the review record and the finding-id ceiling;
`.agent/decisions.md` carries the DECISION series, F037 D1, D2 and D3.

## Goal
Changes become readable, not merely present. The server parses a unified diff
into structured JSON — files, hunks, lines, intraline spans — served as a read
endpoint, and the client renders it with a file sidebar, hunk collapse, virtual
scrolling and lazily loaded syntax bundles.
`docs/roadmap/features/T5_F037.md` holds Goal & Done, the task slicing, the
binding CSS and the design amendments that reconcile it with the source.

## Current Step
T001 is COMPLETE: the parser, the resolver and the two GET routes all landed and
were proved by mutation. R8 prepares T002 rather than starting it. It corrects
the feature file's design authority for the diff surface, which named a section
that does not exist, and it MEASURES whether the frontend test runner can be
executed in this environment at all — the reviewer's three attempts were
refused, and no UI code is ordered until that has an answer, because code that
neither role can execute cannot be verified and must not be certified.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R7 gate, `R-0715`, `R-0719`, the slip | ordered | record first |
| C3 the feature-file amendment and the decision | ordered | authority before builders |
| C4 the handback | ordered | carries the probe's answer first |

## Next Steps
1. Act on the G7 answer. If the runner executes, T002's rendering core lands as
   a pure `.ts` view-model beside its `.test.ts`, which is the only shape this
   package tests: `apps/ui/vitest.config.ts` sets `environment: "node"` and the
   repository has neither jsdom nor a testing library, so no React component is
   rendered in any of its 31 test files. If the runner cannot execute, the
   session hands off asking the operator to grant it, and orders no UI code.
2. T002 the rendering core, then the React components and their CSS module
   against the binding CSS and amendment A4.
3. T003 sidebar, virtual scrolling, lazy languages and the L3 tab.

## Risks
- The frontend runner is unproven here. That is what G7 measures, and it is the
  single largest risk to the rest of this feature.
- `R-0711` carries a `Landed:` line and no `Done:` text because F032's branch
  ended first. It is the terminator case, not a gap for F037 to close.
- No bundle-size budget exists anywhere in `tests/` or `apps/ui/vite.config.ts`,
  so T003 would be creating that ceiling rather than satisfying one.
