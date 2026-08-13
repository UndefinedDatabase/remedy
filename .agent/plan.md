# Plan — F111 Diff-only repair

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e,
unmerged, no PR by design. Last reviewed SHA: c0ed5dd1 (R16 PASS).
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
R17 is T003's apply half. `run_builder_bridge` takes a decoded
`DiffRepairResponse` and routes it through `apply_diff_repair`
instead of `apply_structured_patch`, keeping Stage 1's conversion,
the approval gate and the test stage on one implementation
(DECISION F111 D8). A conflict returns stage `diff_fallback`, the
loop records the reason and puts the next cycle back on the
full-file path. R16's prompt half is complete and gated.

## Next Steps
1. R18 — the measurement: record payload character counts per repair
   round and add the fixture comparison test that shows the diff path
   costs a fraction of the full-file path (DECISION F111 D9 — chars,
   never fabricated token numbers). That is the feature's DONE line.
2. Integration gate, then closure.

## Risks
- The full suite is RED at the merge base with five known ids
  (R-0286): the integration gate compares base against branch.
- `builder_bridge.py` now imports four diff-repair symbols at module
  level; an import cycle would surface as collection errors across
  the nine test files that import it, so that fallout check is a
  standing gate, not a one-off.
- All-or-nothing rests entirely on source_apply's durable snapshot;
  `apply_diff_repair` adds no rollback of its own, and R-0316's fix
  means a failed rollback is now reported rather than hidden.

Fortschritt: ~86 % (T001 ✅ · T002 ✅ · T003 Prompt-Hälfte ✅ · T003
Apply-Hälfte in dieser Runde · Messung offen) — Schätzung
