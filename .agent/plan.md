# Plan — F115 Prompt breakdown & cost report

Branch: feature/f115-prompt-cost-report, cut from main at 0d6c97aa after
PR #194 merged. Last reviewed SHA: a46d65a1 (R11 PASS). Next free finding
ID: R-0333. Open findings: 8 — R-0320, R-0322, R-0323, R-0324, R-0327,
R-0328, R-0331, R-0332 (R-0332's fix LANDED at cfeecdf7 and awaits
review). No PR exists and closure has not started.

## Goal
Costs stop being an opaque total: `remedy stats report` shows WHERE
tokens go — by segment kind, by role, by task class — plus a cost curve
and a prior-period comparison, as markdown and json, every number
traceable to a ledger row, and a period with missing data reported as
missing instead of interpolated (docs/roadmap/features/T2_F115.md).

## Current Step
T002 is DONE in all three halves: the QUERY (R10), the RENDERER (R11) and
the GOLDENS (R12). `tests/orchestration/fixtures/cost_report/golden/`
holds the markdown and the json the renderer produces over a ledger the
REAL `backfill_ledger` wrote from real evidence files — four calls over
three days, two traced and two not, one of them measured — so a change to
the bytes now has to be argued for instead of re-blessed. `_same_question`
also refuses a pair whose two halves read DIFFERENT ledgers, not only one
whose filters disagree (R-0332). Fifteen tests pin all of it. No CLI is
wired, and the schema, the queries, `calls`, the writer and the backfill
path are all unmoved.

## Next Steps
1. T003 — `remedy stats report` CLI, `--until`, the prior-period
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
