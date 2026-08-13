# Plan — F111 Diff-only repair

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e,
unmerged. Last reviewed SHA: 8644def9 (R10 PASS). Next free finding
ID: R-0315. Open findings: 33, measured on disk as 39 registered
minus 6 resolved; one High (R-0312, fixed in R11, awaiting the
reviewer's Done text). Earlier states carried 30, which was stale.

## Goal
Repairs stop resending whole files: a repair round carries only the
failure-relevant hunks with a configurable context margin, the model
answers with a schema-enforced unified diff that is fence-checked and
applied strictly, and ANY hunk conflict discards the attempt whole
and falls back to today's full-file round with the reason recorded
(docs/roadmap/features/T2_F111.md).

## Current Step
R11 closed the header half of the applier's placement defect: a hunk
whose OLD COUNT is 0 is a pure insertion whose content belongs AFTER
the line its header names, but `_apply_hunks` subtracted 1 from every
header, so such hunks landed one line early and `@@ -0,0 +1 @@`
spliced at index -1, turning a prepend into an append (R-0312,
DECISION F111 D5). R10 had fixed the in-body half (R-0311). T002
otherwise stands at record, validation, fence pre-check, split and
conversion — all on disk, all still WITHOUT a call site.

## Next Steps
1. R12 — the apply half of T002: run a converted patch through
   `apply_structured_patch`, and on ANY hunk conflict discard the
   attempt whole, record `fallback_reason`, report mode
   `full_fallback`, and prove every touched file byte-identical to
   its pre-attempt state.
2. T003 — wire `changed_line_ranges_from_patch` and the response
   channel into `run_builder_bridge_loop`, emit mode and token
   evidence per repair round, add the fixture token comparison.
3. Integration gate, then closure.

## Risks
- The full suite is RED at the merge base with five known ids
  (R-0286): the integration gate compares base against branch.
- R-0313 is open by decision: a blank context line stripped to ""
  makes a diff REJECT where the pre-R10 applier applied it. Safe
  direction, but the normalisation belongs on the response side and
  T002/T003 must carry it.
- `review_scope` is the only module that reads hunk headers or
  splits a diff by path; `source_apply._apply_hunks` is the only
  applier. Neither may be duplicated.
- A green suite over unreferenced modules is not a working feature.
  T003 is the round that makes F111 real.
