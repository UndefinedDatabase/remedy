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
R16 finishes T002. `DiffView.tsx` draws the rows `diffViewModel.ts` builds —
file rows, hunk heads that collapse on click, line rows against the binding CSS
— and the last named piece of T002 is ruled rather than deferred: Acceptance
requires intraline emphasis, the three binding authorities say nothing about it,
and DECISION F037 D9 settles it as the binding CSS's own two hues at a higher
alpha, so no new hue and no new token enters the sheet. Amendment A5 records
that in the feature file. The component is deliberately not mounted yet.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R15 verdict and the type-gate slip | ordered | record first |
| C3 DECISION F037 D9 and amendment A5 | ordered | the ruling before what it governs |
| C4 the intraline segmentation and its tests | ordered | the last decidable rule |
| C5/C6 the stylesheet and the component | ordered | the drawing half |
| C7 the render guard | ordered | nothing here can render it |
| C8 the handback | ordered | |

## Next Steps
1. T003 mounts what T002 built: the entry point `component_spec.md` names —
   `onOpenDiff(taskId)` from `DetailPopover` — the fetch through `remedyApi.ts`
   calling `readDiffEnvelope`, and the file sidebar over
   `buildDiffFileSummaries`.
2. T003 then carries virtual scrolling beyond two thousand lines and the lazy
   language bundles, which are its last two named pieces.

## Risks
- Round 16 of a 25-round soft limit. T003 is three or four rounds of work, so
  the feature fits only if T003's rounds each close a named piece; the session
  that reaches round 21 with T003 unfinished owes a scope report instead.
- Nothing in this repository can execute a `.tsx` file. `tsc --noEmit` type-
  checks it through `tests/ui_server/test_dashboard_contract.py` and
  `tests/ui_contracts/` reads it as text, and those two are the whole of the
  gate; a rendering defect that both admit is invisible until the L3 tab exists.
