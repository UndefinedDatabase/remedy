# Plan — F037 Rendered diff viewer

Branch: feature/f037-rendered-diff-viewer, cut from `main` at `9dde5495`, the
merge commit of pull request #217 which closed F032.
`.agent/live_review.md` is the review record and the finding-id ceiling;
`.agent/decisions.md` carries the DECISION series.

## Goal
Changes become readable, not merely present. The server parses a unified diff
into structured JSON — files, hunks, lines, intraline spans — served as a read
endpoint per task and attempt, and the client renders it with a file sidebar,
hunk collapse, virtual scrolling and lazily loaded syntax bundles.
`docs/roadmap/features/T5_F037.md` holds Goal & Done, the task slicing, the
binding CSS and the orchestrator brief.

## Current Step
R1 claims F037 in the roadmap ledger, cuts the branch, resets this record set
for the new feature, books the F032 R19 verdict, and puts the F037 source
inventory on disk. The inventory is the round's substance: `review_scope.py`
already parses unified diffs and `review_subject.py` already names a
file-status vocabulary, while the feature file specifies a contract matching
neither exactly, so what already exists is measured before T001 is planned.

| Item | Status | Reason |
|------|--------|--------|
| C0a/C0b save and mirror the block | ordered | |
| C1 plan and context for F037 | ordered | first substantive commit |
| C2 STATUS claim, open to active | ordered | |
| C3 ledger reset and the F032 R19 gate | ordered | findings carried forward |
| C4 the F037 source inventory | ordered | Q1-Q8, each measured |
| C5 the handback | ordered | |

## Next Steps
1. Book R1's verdict and plan T001 against the inventory — the parser seam, the
   status vocabulary and the route the read endpoint attaches to.
2. T001: the unified-to-JSON parser, its corpus tests and the read endpoint.
3. T002 the rendering core, then T003 sidebar, virtual scrolling, lazy
   languages and the L3 tab.

## Risks
- The feature file's contract names a `binary` file status that
  `review_subject.py`'s vocabulary does not carry, and that vocabulary carries
  `copied` and `type_changed` which the contract omits. If the inventory
  confirms this, the reviewer rules a DECISION under §4 item 7 rather than
  widening scope silently.
- `.agent/live_review.md` is append-only below `## Findings`. R1 rewrites the
  header region and appends the F032 R19 gate entry, and G5 proves both.
