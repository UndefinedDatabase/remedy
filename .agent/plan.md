# Plan — F111 Diff-only repair

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e,
unmerged, no PR by design. Last reviewed SHA: d457219a (R15 PASS).
Next free finding ID: R-0318. Open findings: 31 — 42 registered minus
11 resolved. None is High.

## Goal
Repairs stop resending whole files: a repair round carries only the
failure-relevant hunks with a configurable context margin, the model
answers with a schema-enforced unified diff that is fence-checked and
applied strictly, and ANY hunk conflict discards the attempt whole
and falls back to today's full-file round with the reason recorded
(docs/roadmap/features/T2_F111.md).

## Current Step
R16 is T003's prompt half and the round that makes F111 real: until
this commit nothing imported the T001/T002 modules.
`run_builder_bridge_loop` maps the patch it just applied to changed
line ranges, selects margin-expanded hunks, carries them in the
repair context, and emits `repair_mode_selected` with counts only.
`diff_mode` and `diff_margin_lines` are keyword arguments per
DECISION F111 D7. T001 and T002 are complete and repaired.

## Next Steps
1. R17 — T003's apply half: route the builder's diff answer through
   `apply_diff_repair`, emit the apply-side mode and token actuals,
   and add the fixture comparison test that records both modes'
   token counts (the feature's DONE condition).
2. Integration gate, then closure.

## Risks
- The full suite is RED at the merge base with five known ids
  (R-0286): the integration gate compares base against branch.
- The prompt side now carries hunk TEXT in the repair context. Only
  counts go into the timeline; any later change that logs the whole
  context would leak source into evidence.
- All-or-nothing rests entirely on source_apply's durable snapshot;
  `apply_diff_repair` adds no rollback of its own.

Fortschritt: ~80 % (T001 ✅ · T002 ✅ · T003 Prompt-Hälfte in dieser Runde ·
T003 Apply-Hälfte offen · R-0316 ✅ · R-0317 ✅) — Schätzung
