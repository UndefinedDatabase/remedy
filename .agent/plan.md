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
R9 lands the half of T002 this environment can actually verify: the diff surface
stylesheet, transcribed from the feature file's binding CSS, and a Python
conformance guard over it in `tests/ui_contracts/`, which is how this repository
already pins frontend CSS. The rendering core stays unwritten because the
frontend test runner is REFUSED here for both roles, measured at R8 — code that
neither role can execute must not be certified.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit, repairs its own cap |
| C2 the R8 gate and the slip | ordered | record first |
| C3 DECISION F037 D4 and the stylesheet | ordered | the choice beside what it governs |
| C4 the conformance guard | ordered | must go red when the sheet drifts |
| C5 the handback | ordered | last round of the session |

## Next Steps
1. UNBLOCK THE RUNNER. `npx vitest run --root apps/ui`, `npm --prefix apps/ui
   run test:unit` and the direct binary were all refused at R8. Until one is
   permitted, no `.ts`, `.tsx` or React component of T002 can be verified, and
   none is ordered.
2. T002's rendering core as a pure `.ts` view-model beside its `.test.ts`, the
   only shape this package tests: `apps/ui/vitest.config.ts` sets
   `environment: "node"` and there is no jsdom and no testing library.
3. T003 sidebar, virtual scrolling, lazy languages and the L3 tab.

## Risks
- The binding CSS defines no intraline treatment, and Acceptance requires
  intraline emphasis. That is a design question for the round that renders
  spans; inventing a colour early would breach the feature file's own banner.
- `R-0711` carries a `Landed:` line and no `Done:` text because F032's branch
  ended first. It is the terminator case, not a gap for F037 to close.
- No bundle-size budget exists in `tests/` or `apps/ui/vite.config.ts`, so T003
  would be creating that ceiling rather than satisfying one.
