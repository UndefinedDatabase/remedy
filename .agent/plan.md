# Plan — F111 Diff-only repair

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e,
unmerged, no PR by design. Last reviewed SHA: 06e85a11 (R11 PASS).
Next free finding ID: R-0316. Open findings: 33, measured on disk as
40 registered minus 7 resolved. None is High.

## Goal
Repairs stop resending whole files: a repair round carries only the
failure-relevant hunks with a configurable context margin, the model
answers with a schema-enforced unified diff that is fence-checked and
applied strictly, and ANY hunk conflict discards the attempt whole
and falls back to today's full-file round with the reason recorded
(docs/roadmap/features/T2_F111.md).

## Current Step
R12 is the session-closing gate round: it records the R11 verdict,
resolves R-0312 and registers R-0315. Both halves of the applier's
placement defect are now closed — R-0311 fixed WHERE an added line
lands inside its hunk, R-0312 fixed WHERE the hunk itself starts.
T002 otherwise stands at record, validation, fence pre-check, split
and conversion — all on disk, all still WITHOUT a call site.

## Next Steps
1. R13 — the apply half of T002. Settle R-0315 FIRST: the feature
   file allows new-file creation inside a diff, the applicator
   rejects any diff whose target file does not exist. Then run a
   converted patch through `apply_structured_patch`, and on ANY hunk
   conflict discard the attempt whole, record `fallback_reason`,
   report mode `full_fallback`, and prove every touched file
   byte-identical to its pre-attempt state.
2. T003 — wire `changed_line_ranges_from_patch` and the response
   channel into `run_builder_bridge_loop`, emit mode and token
   evidence per repair round, add the fixture token comparison.
3. Integration gate, then closure.

## Risks
- The full suite is RED at the merge base with five known ids
  (R-0286): the integration gate compares base against branch.
- R-0313 is open by decision: a blank context line stripped to ""
  makes a diff REJECT where the pre-R10 applier applied it. Safe
  direction; the normalisation belongs on the response side.
- `source_apply._apply_hunks` is the only applier and `review_scope`
  the only diff reader. Neither may be duplicated.
- A green suite over unreferenced modules is not a working feature.
  T003 is the round that makes F111 real.
