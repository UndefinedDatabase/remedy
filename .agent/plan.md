# Plan — F111 Diff-only repair

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e.
Next free finding ID: R-0298. Last reviewed SHA: b0ab8e09 (R1 PASS).

## Goal
Repairs stop resending whole files: a repair round carries only the
failure-relevant hunks with a configurable context margin, the model answers
with a schema-enforced unified diff that is fence-checked and applied
strictly, and ANY hunk conflict discards the attempt whole and falls back to
today's full-file round with the reason recorded
(docs/roadmap/features/T2_F111.md).

## Current Step
R2 — record the R1 gate and DECISION F111 D1, amend the feature file with the
seam the DECISION picks, and build T001: the hunk selection helper in the new
`packages/orchestration/diff_repair.py` with unit tests. D1 settles that the
response side attaches to `builder_bridge` (which already applies a parsed
patch through the fenced applicator) and the prompt side to
`repair_context`; `pingpong_loop` is out of scope and the feature file now
says so.

## Next Steps
1. T001 rest — wire the selected hunks into the repair context the bounded
   repair loop feeds to the next build call.
2. T002 — versioned unified-diff response schema, fence pre-check before any
   apply, strict apply with an all-or-nothing conflict fallback.
3. T003 — mode and token evidence per repair round, plus a fixture comparison
   recording both modes' token counts.
4. Integration gate, then closure.

## Risks
- The full suite is RED at the merge base with five known ids (R-0286), so
  the integration gate must compare base against branch, never read absolute
  green.
- `review_scope._parse_diff` and `source_apply._apply_hunks` already exist and
  must be reused, not duplicated — a third `@@` regex in the tree would be a
  finding.
