# Plan — F115 Prompt breakdown & cost report

Branch: feature/f115-prompt-cost-report, cut from main at 0d6c97aa after
PR #194 merged. Last reviewed SHA: f20f172a (R7 PASS). Next free finding
ID: R-0327. Open findings: 4 — R-0320 (Low, from F111), R-0322 (Medium,
inherited suite red), R-0323 + R-0324 (Low, reviewer arithmetic). R-0325
and R-0326 are resolved.

## Goal
Costs stop being an opaque total: `remedy stats report` shows WHERE
tokens go — by segment kind, by role, by task class — plus a cost curve
and a prior-period comparison, as markdown and json, every number
traceable to a ledger row, and a period with missing data reported as
missing instead of interpolated (docs/roadmap/features/T2_F115.md).

## Current Step
R8 settled T001's persistence shape as DECISION F115 D4 and landed it as
SCHEMA ONLY: `call_segments` is migration step 2, `SCHEMA_VERSION` is 2,
and `calls`, `CallRecord` and `_CALL_COLUMNS` are untouched, so no
existing row can read as ledger drift. Nothing writes to the table yet.

## Next Steps
1. The `call_segments` WRITER — populate from the copied
   `prompt_trace.jsonl` on the backfill path, where the file exists,
   since the live hook runs before the copy.
2. T002 — aggregation queries plus the pure renderer, with goldens.
3. T003 — CLI, prior-period comparison, json schema.
4. Integration gate (docs/agents/integration_gate.md), then closure.

## Risks
- Per-role has one bucket until `role` stops being hardcoded, and
  per-task-class has no source at all: report "no data", never a bucket.
- R-0322 will meet F115's integration gate as five pre-existing reds.

Fortschritt: 50 % (R1 ✅ · T001a ✅ · alle drei Call-Sites ✅ · T001-Shape-Inventar ✅ · T001-Persistenz läuft · T002 · T003 offen) — Schätzung
