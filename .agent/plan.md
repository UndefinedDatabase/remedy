# Plan — F115 Prompt breakdown & cost report

Branch: feature/f115-prompt-cost-report, cut from main at 0d6c97aa after
PR #194 merged. Last reviewed SHA: ddb97945 (R10 PASS). Next free finding
ID: R-0331. Open findings: 7 — R-0320, R-0322, R-0323, R-0324, R-0327,
R-0328, R-0330 (R-0330's fix LANDED at a74e0668 and awaits review). No PR
exists and closure has not started.

## Goal
Costs stop being an opaque total: `remedy stats report` shows WHERE
tokens go — by segment kind, by role, by task class — plus a cost curve
and a prior-period comparison, as markdown and json, every number
traceable to a ledger row, and a period with missing data reported as
missing instead of interpolated (docs/roadmap/features/T2_F115.md).

## Current Step
T001 is DONE and T002 now has both halves: the QUERY (R10) and the
RENDERER (R11). `packages/orchestration/cost_report.py` is a pure
function over the `CostReport` / `SegmentShareReport` pair — markdown for
people, json for the later UI — that opens nothing, computes no price and
renders neither `ledger_path` nor `project_id`, so the same pair yields
the same bytes on any machine. It refuses a pair whose two halves answer
different questions (`since`/`job_id` must match), prints UNMEASURED
rather than a 0, and reports an untraced call as an unattributed count
instead of a zero share. Ten tests pin exactly that. No CLI is wired yet
and no golden file exists yet; the schema, the queries, `calls`, the
writer and the backfill path are all unmoved.

## Next Steps
1. R12 — the golden PAIR on disk over the fixture ledger, following
   gauntlet_matrix.py and the share_ledger fixture at
   tests/orchestration/test_token_ledger.py:1845-1867.
2. T003 — `remedy stats report` CLI, `--until`, prior-period comparison,
   json schema, and the docs page the new user-visible behaviour needs;
   `stats_ledger_cmd.UNMEASURED` becomes an import of
   `COST_UNMEASURED_LABEL` so the concept keeps one spelling.
3. Integration gate (docs/agents/integration_gate.md).
4. Closure per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- Per-role has one bucket until `role` stops being hardcoded, and
  per-task-class has no source at all: report "no data", never a bucket.
- R-0322 will meet F115's integration gate as five pre-existing reds.

Fortschritt: 72 % (T001 ✅ · T002-Query ✅ · T002-Renderer ✅ ·
T002-Goldens · T003 offen) — Schätzung
