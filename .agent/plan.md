# Plan — F037 Rendered diff viewer

Branch: feature/f037-rendered-diff-viewer, cut from `main` at `9dde5495` (the
merge of PR #217, which closed F032). `.agent/decisions.md` holds F037 D1 to D6.

## Goal
Changes become readable, not merely present. The server parses a unified diff
into structured JSON — files, hunks, lines, intraline spans — served as a read
endpoint, and the client renders it with a file sidebar, hunk collapse, virtual
scrolling and lazily loaded syntax bundles.
`docs/roadmap/features/T5_F037.md` holds Goal & Done, the task slicing, the
binding CSS and the design amendments A1 through A4.

## Current Step
R13 repairs `R-0722`. DECISION F037 D5's ceiling bounds body LINES only, so a
diff whose files carry no body lines is bounded by nothing, and every assertion
the R12 suite added follows the constant wherever it goes. The parser gains a
second ceiling on FILE ENTRIES where the collapsed region list becomes `files`;
the two R12 tests whose fixture crosses both ceilings are re-based onto a shape
crossing only the body one; and a recorded payload budget pins what the two
ceilings are for. DECISION F037 D6 records all of it.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R12 verdict, `R-0722`, the slip | ordered | record first |
| C3 DECISION F037 D6 and the file ceiling | ordered | the choice beside what it governs |
| C4 the file-ceiling tests and the budget | ordered | both ceilings, both sides |
| C5 the resolution | ordered | written after the repair is proved |
| C6 the handback | ordered | |

## Next Steps
1. The round after this one carries the other half of `R-0721`:
   `diff_view_source.py` still reads the artifact whole with `read_text` before
   the parser sees it, so the INPUT stays unbounded while the OUTPUT is bounded
   in both dimensions.
2. T002 and T003 are NOT blocked by the refused runner, and the round after that
   states why: `apps/ui/vitest.config.ts` collects `src/**/*.test.ts` in a node
   environment, `tests/orchestration/test_test_runner.py` runs `npx vitest run`
   from pytest and is exit 0 here at `327c1333`, and `tests/ui_contracts/` pins
   the markup vitest never renders.

## Risks
- A ceiling is a behaviour change on a shipped read path. The tests R11 and R12
  added are the regression guard; if one moves that this round did not order
  moved, a ceiling was chosen wrong rather than the test being stale.
- The binding CSS defines no intraline treatment while Acceptance requires it,
  so that stays a question for the round that renders spans.
