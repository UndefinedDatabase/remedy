# Plan — F111 Diff-only repair

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e,
unmerged. Last reviewed SHA: 456a25e9 (R8 PASS). Next free finding
ID: R-0309. Open findings: 28, none above Medium.

## Goal
Repairs stop resending whole files: a repair round carries only the
failure-relevant hunks with a configurable context margin, the model
answers with a schema-enforced unified diff that is fence-checked and
applied strictly, and ANY hunk conflict discards the attempt whole
and falls back to today's full-file round with the reason recorded
(docs/roadmap/features/T2_F111.md).

## Current Step
T002 is all but the apply, and still has NO CALL SITE. On disk in
`diff_repair_response.py`: the versioned `{format, version, diff,
files}` record, its parse, the validation that cross-checks the
declared `files` list against the paths the diff really touches,
`precheck_diff_repair_fences` — the non-raising fence decision that
rejects an out-of-fence path before the applicator — and now
`diff_repair_response_to_patch`, which converts a validated response
into the `StructuredPatch` the existing applicator already takes.
The per-path split it needs is `review_scope.split_diff_by_path`,
placed inside the module that owns hunk-header reading so no second
walk exists. Nothing imports any of it: T001 and T002 are seams.

## Next Steps
1. R10 — the apply half: run the converted patch through
   `apply_structured_patch` with its snapshot and approval gates, and
   on ANY hunk conflict discard the attempt whole, record
   `fallback_reason`, report mode `full_fallback`, and prove every
   touched file byte-identical to its pre-attempt state.
2. T003 — wire `changed_line_ranges_from_patch` and the response
   channel into `run_builder_bridge_loop`, emit mode and token
   evidence per repair round, add the fixture token comparison.
3. Integration gate, then closure.

## Risks
- The full suite is RED at the merge base with five known ids
  (R-0286): the integration gate compares base against branch.
- `source_apply._apply_hunks` is the strict applier and must be
  reused, never duplicated. `review_scope` is now the only module
  that reads hunk headers OR splits a diff by path.
- A green suite over unreferenced modules is not a working feature.
  T003 is the round that makes F111 real, and until it lands the
  Fortschritt figure is about code written, not behaviour shipped.
