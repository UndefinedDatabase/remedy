# Plan — F115 Prompt breakdown & cost report

Branch: feature/f115-prompt-cost-report, cut from main at 0d6c97aa after
PR #194 merged. Last reviewed SHA: 5c7f5159 (R14 PASS, gated on disk at
R15). Next free finding ID: R-0336. Open findings: 10 — R-0320, R-0322,
R-0323, R-0324, R-0327, R-0328, R-0331, R-0333, R-0334, R-0335. No PR
exists and closure has not started.

## Goal
Costs stop being an opaque total: `remedy stats report` shows WHERE
tokens go — by segment kind, by role, by task class — plus a cost curve
and a prior-period comparison, as markdown and json, every number
traceable to a ledger row, and a period with missing data reported as
missing instead of interpolated (docs/roadmap/features/T2_F115.md).

## Current Step
T003 has begun. The period now has TWO ends: `query_cost` and
`query_segment_shares` both take `until`, `_cost_filters` renders it as a
half-open `ts_utc < until` (DECISION F115 D5), `merge_cost_reports`
carries it, and `_same_question` refuses a pair whose two halves cover
two different periods. Both renderers print it, `COST_REPORT_VERSION` is
2, and the two goldens moved by exactly the lines that surface added. No
CLI is wired; the prior-period comparison has no code yet.

## Next Steps
1. T003b — the prior-period comparison over the half-open period: the
   equal-length window immediately before `since`, and "no comparison
   data" where that window holds nothing — never zeros.
2. T003c — the `remedy stats report` CLI, markdown and `--json`, with its
   catalog entry; `stats_ledger_cmd.UNMEASURED` becomes an import of
   `COST_UNMEASURED_LABEL` so the concept keeps one spelling.
3. T003d — the docs page the new user-visible behaviour needs.
4. Integration gate (docs/agents/integration_gate.md).
5. Closure per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- Per-role has one bucket until `role` stops being hardcoded, and
  per-task-class has no source at all: report "no data", never a bucket.
- R-0322 will meet F115's integration gate as five pre-existing reds.
- The goldens are DATA: no test may regenerate them. A renderer change
  that moves the bytes must move the files in the same, argued commit.

Fortschritt: 84 % (T001 ✅ · T002 ✅ · T003 läuft) — Schätzung
