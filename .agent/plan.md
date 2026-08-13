# Plan — F115 Prompt breakdown & cost report

Branch: feature/f115-prompt-cost-report, cut from main at 0d6c97aa after
PR #194 merged. Last reviewed SHA: 8615259b (R8 PASS). Next free finding
ID: R-0329. Open findings: 6 — R-0320, R-0322, R-0323, R-0324, R-0327,
R-0328. No PR exists yet; closure has not started.

## Goal
Costs stop being an opaque total: `remedy stats report` shows WHERE
tokens go — by segment kind, by role, by task class — plus a cost curve
and a prior-period comparison, as markdown and json, every number
traceable to a ledger row, and a period with missing data reported as
missing instead of interpolated (docs/roadmap/features/T2_F115.md).

## Current Step
T001 is DONE, schema and writer both. R8 landed `call_segments` as
migration step 2; R9 filled it: `segment_rows_from_trace_file` reads the
copied `prompt_trace.jsonl`, `record_call_segments` writes it, and
`backfill_ledger` wires the two. `BackfillResult`'s four counters are
unmoved and `calls`, `CallRecord` and `_CALL_COLUMNS` are untouched. The
live hook stays deliberately unwired — it fires before the exporter
copies the trace, so backfill is the only path where the file exists.

## Next Steps
1. T002 — aggregation queries over `calls` joined to `call_segments`,
   plus the pure renderer with markdown/json goldens, following
   `gauntlet_matrix.py` and the fixture-ledger pattern at
   `tests/cli/test_stats_cost.py:49-128`.
2. T003 — `remedy stats report` CLI, prior-period comparison, json schema.
3. Integration gate (docs/agents/integration_gate.md).
4. Closure per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- Per-role has one bucket until `role` stops being hardcoded, and
  per-task-class has no source at all: report "no data", never a bucket.
- R-0322 will meet F115's integration gate as five pre-existing reds.

Fortschritt: 58 % (T001-Schema ✅ · T001-Writer ✅ · T002 · T003 offen) — Schätzung
