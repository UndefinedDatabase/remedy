# Plan — F037 Rendered diff viewer

Branch: feature/f037-rendered-diff-viewer, cut from `main` at `9dde5495`, the
merge commit of pull request #217 which closed F032.
`.agent/live_review.md` is the review record and the finding-id ceiling;
`.agent/decisions.md` carries the DECISION series, F037 D1 and D2.

## Goal
Changes become readable, not merely present. The server parses a unified diff
into structured JSON — files, hunks, lines, intraline spans — served as a read
endpoint, and the client renders it with a file sidebar, hunk collapse, virtual
scrolling and lazily loaded syntax bundles.
`docs/roadmap/features/T5_F037.md` holds Goal & Done, the task slicing, the
binding CSS and the design amendments that reconcile it with the source.

## Current Step
R3 opens T001 with the parser itself: a new self-contained module that turns a
unified diff into the versioned view JSON, plus the corpus that pins one shape
per row of the feature file's list. It reads the THREE diff shapes this
repository really produces — difflib output, git hunks, and untracked-file
markers — rather than the single git-style shape the contract assumed. The
round also books the R2 verdict and the reviewer's authoring slip.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R2 gate and the reviewer's slip | ordered | the record moves first |
| C3 the parser module | ordered | production code, spec-driven |
| C4 the corpus tests | ordered | one shape per row, plus red-proofs |
| C5 the handback | ordered | |

## Next Steps
1. Intraline spans over the parsed lines, with the word-diff fixture the
   feature file's Acceptance names.
2. The read endpoint, keyed on task run and job per DECISION F037 D2, with the
   route guards the R1 inventory measured.
3. T002 the rendering core, the binding CSS and the goldens; then T003 sidebar,
   virtual scrolling, lazy languages and the L3 tab.

## Risks
- `R-0715` is open and Low. It is a stale count in a test docstring, turns
  nothing red, and belongs to whoever next edits that file.
- The parser is new surface with no consumer yet. Until the endpoint lands it
  is proved only by its own corpus, so the corpus carries the whole weight and
  the round orders mutation red-proofs against it.
