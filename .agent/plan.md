# Plan — F115 Prompt breakdown & cost report

Branch: feature/f115-prompt-cost-report, cut from main at 0d6c97aa after
PR #194 merged. Last reviewed SHA: ddb97945 (R10 PASS). Next free finding
ID: R-0331. Open findings: 7 — R-0320, R-0322, R-0323, R-0324, R-0327,
R-0328, R-0330. R-0329 was RESOLVED at the R10 gate. No PR exists and
closure has not started. `.agent/STOP` is present and the session ended
at it (guardrail G6, docs/agents/self_drive_protocol.md).

## Goal
Costs stop being an opaque total: `remedy stats report` shows WHERE
tokens go — by segment kind, by role, by task class — plus a cost curve
and a prior-period comparison, as markdown and json, every number
traceable to a ledger row, and a period with missing data reported as
missing instead of interpolated (docs/roadmap/features/T2_F115.md).

## Current Step
T001 is DONE and T002's QUERY half is done. R10 added
`query_segment_shares` beside `query_cost`: it joins `calls` to
`call_segments` under the shared `_cost_filters` clause, reports each
segment kind's share in a pinned order (`tokens_estimated` DESC, then
`segment_name` ASC), and counts attributed and unattributed calls
separately so a call the tracer never covered stays an absence rather
than a zero share. The same commit's guard (`_MANIFEST_KEY_TYPES`) keeps
a wrongly TYPED manifest value out of those sums — R-0329, now closed.
The schema, `calls`, `CallRecord`, the writer and the backfill path are
all unmoved.

## Next Steps
1. R11 — the pure renderer over `query_segment_shares` and `query_cost`,
   markdown and json, with the golden PAIR on disk following
   `packages/orchestration/gauntlet_matrix.py`; fix R-0330 in the same
   region.
2. T003 — `remedy stats report` CLI, `--until`, prior-period comparison,
   json schema, and the docs page the new user-visible behaviour needs.
3. Integration gate (docs/agents/integration_gate.md).
4. Closure per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- Per-role has one bucket until `role` stops being hardcoded, and
  per-task-class has no source at all: report "no data", never a bucket.
- R-0322 will meet F115's integration gate as five pre-existing reds.

Fortschritt: 66 % (T001 ✅ · T002-Query ✅ · T002-Renderer · T003 offen) — Schätzung
