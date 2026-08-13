# Plan — F111 Diff-only repair

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e,
unmerged. Last reviewed SHA: 33f408b2 (R9 PASS). Next free finding
ID: R-0312. Open findings: 30, one High (R-0311, fixed in R10,
awaiting the reviewer's Done text), the rest Low or Medium.

## Goal
Repairs stop resending whole files: a repair round carries only the
failure-relevant hunks with a configurable context margin, the model
answers with a schema-enforced unified diff that is fence-checked and
applied strictly, and ANY hunk conflict discards the attempt whole
and falls back to today's full-file round with the reason recorded
(docs/roadmap/features/T2_F111.md).

## Current Step
R10 fixed `source_apply._apply_hunks`, which inserted every added
line at the hunk's START instead of at its position, so any hunk
whose additions were not on its first line silently reordered the
file it applied to (finding R-0311, DECISION F111 D4). The applier
now splices each hunk's new block over the exact original range it
consumed. T002 otherwise stands at record, validation, fence
pre-check, split and conversion — all on disk in
`diff_repair_response.py` and `review_scope.split_diff_by_path`, and
all still WITHOUT a call site.

## Next Steps
1. R11 — the apply half of T002: run a converted patch through
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
- R-0311 was live for the whole life of the structured unified-diff
  path. Any earlier evidence claiming a clean diff apply predates
  this fix and cannot be trusted about line ORDER.
- `review_scope` is now the only module that reads hunk headers or
  splits a diff by path; `source_apply._apply_hunks` is the only
  applier. Neither may be duplicated.
- A green suite over unreferenced modules is not a working feature.
  T003 is the round that makes F111 real.
