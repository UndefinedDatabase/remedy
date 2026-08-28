# Plan — F037 Rendered diff viewer

Branch: feature/f037-rendered-diff-viewer, cut from `main` at `9dde5495` (the
merge of PR #217, which closed F032). `.agent/decisions.md` holds F037 D1 to D8.

## Goal
Changes become readable, not merely present. The server parses a unified diff
into structured JSON — files, hunks, lines, intraline spans — served as a read
endpoint, and the client renders it with a file sidebar, hunk collapse, virtual
scrolling and lazily loaded syntax bundles.
`docs/roadmap/features/T5_F037.md` holds Goal & Done, the task slicing, the
binding CSS and the design amendments A1 through A4.

## Current Step
R15 starts T002 and corrects the premise that stopped it. DECISION F037 D8
records that the frontend runner IS reachable here — through
`tests/orchestration/test_test_runner.py`, which runs `npx vitest run` from
pytest — and that the build pattern is this repository's own: decidable rules in
`apps/ui/src/api/` where vitest reaches them, markup and stylesheets pinned from
`tests/ui_contracts/`. The round lands `diffViewModel.ts`, its vitest tests and
a structural guard, and repairs two shipped comments that assert otherwise
(`R-0723`, `R-0724`).

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R14 verdict and two registrations | ordered | record first |
| C3 DECISION F037 D8 and both comment repairs | ordered | the choice beside what it governs |
| C4/C5 the view model and its vitest tests | ordered | the decidable half of the core |
| C6 the structural guard | ordered | what vitest cannot see about itself |
| C7 the resolutions | ordered | written after the repairs are proved |
| C8 the handback | ordered | |

## Next Steps
1. The round after this one renders: the `DiffView` component over these row
   models, the hunk-head and line markup against the binding CSS, and the entry
   point `component_spec.md` names — `onOpenDiff(taskId)` from `DetailPopover`.
   Its behaviour is pinned by `tests/ui_contracts/`, its rules by vitest here.
2. T003 — the sidebar over `buildDiffFileSummaries`, virtual scrolling beyond
   two thousand lines, lazy language bundles, the L3 tab — is the last slice.

## Risks
- Round 15 of a 25-round soft limit with T002 and T003 both unfinished. If the
  component does not land next round, the handback after it carries a scope
  report proposing a split rather than another step.
- The binding CSS defines no intraline treatment while Acceptance requires it,
  so that stays a question for the round that renders spans.
