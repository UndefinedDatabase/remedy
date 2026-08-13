# Plan — F111 Diff-only repair

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e,
unmerged, no PR by design. Last reviewed SHA: 9a17fad2 (R13 PASS).
Next free finding ID: R-0317. Open findings: 33 — 41 registered minus
8 resolved. None is High.

## Goal
Repairs stop resending whole files: a repair round carries only the
failure-relevant hunks with a configurable context margin, the model
answers with a schema-enforced unified diff that is fence-checked and
applied strictly, and ANY hunk conflict discards the attempt whole
and falls back to today's full-file round with the reason recorded
(docs/roadmap/features/T2_F111.md).

## Current Step
R14 closes R-0313 on the response side: a blank context line whose
single leading space was stripped in transport arrives as "" and makes
an otherwise valid diff REJECT. `normalize_diff_blank_context` restores
the space while the hunk's own line budget says the line is still body,
so the diff reaches the applicator intact. T002 is otherwise complete:
record, split, schema, fence pre-check and the apply-and-fallback seam.

## Next Steps
1. R15 — T003: wire `select_repair_hunks`,
   `changed_line_ranges_from_patch` and `apply_diff_repair` into
   `run_builder_bridge_loop`, emit mode and token evidence per repair
   round, add the fixture token comparison. R15 also fixes R-0316,
   because it is T003 that emits `files_modified` as evidence.
2. Integration gate, then closure.

## Risks
- The full suite is RED at the merge base with five known ids
  (R-0286): the integration gate compares base against branch.
- R-0316 is open: a failed rollback leaves files changed while the
  seam still reports `files_modified=0`. Narrow (OSError during
  restore) but it is the Done criterion's own failure class.
- All-or-nothing rests entirely on source_apply's durable snapshot;
  `apply_diff_repair` adds no rollback of its own.
- A green suite over unreferenced modules is not a working feature.
  R15 is the round that makes F111 real.
