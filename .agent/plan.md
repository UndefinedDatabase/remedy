# Plan — F111 Diff-only repair

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e,
unmerged, no PR by design. Last reviewed SHA: 48c6340e (R14 PASS).
Next free finding ID: R-0318. Open findings: 33 — 42 registered minus
9 resolved. None is High.

## Goal
Repairs stop resending whole files: a repair round carries only the
failure-relevant hunks with a configurable context margin, the model
answers with a schema-enforced unified diff that is fence-checked and
applied strictly, and ANY hunk conflict discards the attempt whole
and falls back to today's full-file round with the reason recorded
(docs/roadmap/features/T2_F111.md).

## Current Step
R15 closes the two reviewer-caused spec defects in T002 so T003 starts
from a clean seam. R-0317: a "" is hunk body only when the next
non-blank line is body too, so a blank line separating two file
sections stops becoming a context line. R-0316: a failed rollback no
longer reports a clean tree — the seam carries `rollback_incomplete`
and stops zeroing `files_modified` when the applicator says restore
failed. T002 is otherwise complete.

## Next Steps
1. R16 — T003: wire `select_repair_hunks`,
   `changed_line_ranges_from_patch` and `apply_diff_repair` into
   `run_builder_bridge_loop`, emit mode and token evidence per repair
   round, add the fixture token comparison. NOTHING imports the three
   T001/T002 modules yet; R16 is the round that makes F111 real.
2. Integration gate, then closure.

## Risks
- The full suite is RED at the merge base with five known ids
  (R-0286): the integration gate compares base against branch.
- Two rounds running, the defect came from the reviewer's authored
  algorithm, not the worker's execution. Any further algorithm spec
  is measured against this repository's own fixtures BEFORE emission,
  not only against a hand-built example.
- All-or-nothing rests entirely on source_apply's durable snapshot;
  `apply_diff_repair` adds no rollback of its own.
