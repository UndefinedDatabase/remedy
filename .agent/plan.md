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
R23 fixes `R-0731`, a defect the round that shipped it could not see and its
whole green suite did not catch: the language mapping is a plain object literal,
so an extension naming an INHERITED property resolves off `Object.prototype`
instead of to plain, and `src/x.constructor` really does reach the bundle
importer that Acceptance says must not be called. The fix closes both halves —
a null-prototype map AND an own-property read — because either alone is undone
silently by a later refactor. Then `R-0730`'s remaining three comments are
repaired, one of them a sentence the reviewer's own R21 spec introduced.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R22 verdict, two resolutions, one finding | ordered | record first |
| C3 the `R-0731` fix and its tests | ordered | a measured defect |
| C4 the structural guard | ordered | after the code it reads |
| C5 the three comment repairs | ordered | closes `R-0730` |
| C6 the handback | ordered | |

## Next Steps
1. Wire highlighting into `DiffView` through `loadDiffLanguageBundle`.
2. The 10k-line perf fixture measured END TO END with its numbers recorded,
   which Acceptance requires and nothing has yet measured.
3. A ruling on the sidebar's visual treatment, still owed.

## Risks
- Round 23 of a 25-round soft limit, session 6 of 7. THREE named pieces remain
  and only two rounds are left inside the limit, so the session that reaches
  round 25 owes a SCOPE REPORT rather than more work — most likely proposing
  that the highlighting wiring and the perf fixture become their own STATUS
  line.
- Nothing here renders a `.tsx` file, so step 1 will be gated by text and
  `tsc --noEmit` alone, as every `.tsx` round of this feature has been.
