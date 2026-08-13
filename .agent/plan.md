# Plan — F115 Prompt breakdown & cost report

Branch: feature/f115-prompt-cost-report, cut from main at 0d6c97aa after
PR #194 merged. Last reviewed SHA: a228feb9 (R12 PASS). Next free finding
ID: R-0334. Open findings: 8 — R-0320, R-0322, R-0323, R-0324, R-0327,
R-0328, R-0331, R-0333. R-0329, R-0330 and R-0332 were each RESOLVED at
their gates. No PR exists and closure has not started.

## Goal
Costs stop being an opaque total: `remedy stats report` shows WHERE
tokens go — by segment kind, by role, by task class — plus a cost curve
and a prior-period comparison, as markdown and json, every number
traceable to a ledger row, and a period with missing data reported as
missing instead of interpolated (docs/roadmap/features/T2_F115.md).

## Current Step
T001 and T002 are both DONE. The QUERY, the RENDERER and the GOLDEN PAIR
are all on disk: `tests/orchestration/fixtures/cost_report/golden/` holds
the markdown and the json the renderer produces over a ledger the REAL
`backfill_ledger` wrote from real evidence files, so a change to those
bytes must be argued for instead of re-blessed. `_same_question` refuses
a pair whose two halves read DIFFERENT ledgers, not only one whose
filters disagree (R-0332, fixed and reviewed). Fifteen tests pin it. No
CLI is wired; the schema, `calls`, the writer and the backfill path are
unmoved.

## Next Steps
1. T003 — the `remedy stats report` CLI with `--until`, the prior-period
   comparison and the json schema, plus the docs page the new
   user-visible behaviour needs; `stats_ledger_cmd.UNMEASURED` becomes an
   import of `COST_UNMEASURED_LABEL` so the concept keeps one spelling.
2. Integration gate (docs/agents/integration_gate.md).
3. Closure per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- Per-role has one bucket until `role` stops being hardcoded, and
  per-task-class has no source at all: report "no data", never a bucket.
- R-0322 will meet F115's integration gate as five pre-existing reds.
- The goldens are DATA: no test may regenerate them. A renderer change
  that moves the bytes must move the files in the same, argued commit.

Fortschritt: 80 % (T001 ✅ · T002 ✅ · T003 offen) — Schätzung
