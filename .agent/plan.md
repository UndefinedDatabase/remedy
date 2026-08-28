# Plan — F037 Rendered diff viewer

Branch: feature/f037-rendered-diff-viewer, cut from `main` at `9dde5495` (the
merge of PR #217, which closed F032). `.agent/decisions.md` holds F037 D1 to D7.

## Goal
Changes become readable, not merely present. The server parses a unified diff
into structured JSON — files, hunks, lines, intraline spans — served as a read
endpoint, and the client renders it with a file sidebar, hunk collapse, virtual
scrolling and lazily loaded syntax bundles.
`docs/roadmap/features/T5_F037.md` holds Goal & Done, the task slicing, the
binding CSS and the design amendments A1 through A4.

## Current Step
R14 closes the remaining half of `R-0721`. DECISION F037 D5 and D6 bound what
the parser BUILDS; neither bounds what `diff_view_source.py` READS, and a diff
of one enormous line with no newline reaches neither ceiling while still costing
the whole read. The read is bounded at `DIFF_VIEW_MAX_ARTIFACT_BYTES`, cut back
to the last newline so no partial line and no split character reaches the
parser, and the envelope's `truncated` becomes an OR over both sources.
DECISION F037 D7 records the value and how to reverse it.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R13 verdict | ordered | record first |
| C3 DECISION F037 D7 and the read bound | ordered | the choice beside what it governs |
| C4 the read-bound tests | ordered | both sides, and the two cut hazards |
| C5 the resolution | ordered | written after the repair is proved |
| C6 the handback | ordered | |

## Next Steps
1. T002 is NOT blocked by the refused runner and the round after this one says
   so in a DECISION and starts the rendering core. `apps/ui/vitest.config.ts`
   collects `src/**/*.test.ts` in a node environment,
   `tests/orchestration/test_test_runner.py` runs `npx vitest run` from pytest
   and is exit 0 here at `922f3223`, and `tests/ui_contracts/` pins the markup
   vitest never renders. Logic goes in `apps/ui/src/api/`, where vitest reaches
   it; markup is pinned from pytest.
2. T003 — sidebar, virtual scrolling, lazy language bundles, the L3 tab —
   follows the rendering core and is the feature's last slice.

## Risks
- The feature is at round 14 against a soft limit of 25, with T002 and T003 both
  still to build. If the rendering core does not start within two rounds, the
  next handback carries a scope report rather than another step.
- The binding CSS defines no intraline treatment while Acceptance requires it,
  so that stays a question for the round that renders spans.
