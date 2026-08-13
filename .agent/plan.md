# Plan — F115 Prompt breakdown & cost report

Branch: feature/f115-prompt-cost-report, cut from main at 0d6c97aa after
PR #194 merged. Last reviewed SHA: b047aa38 (R18 PASS WITH RISKS); R19 is
handed back and awaits its gate. Next free finding ID: R-0339. Open
findings: 12 — R-0320, R-0322, R-0323, R-0324, R-0327, R-0328, R-0331,
R-0333, R-0334, R-0336, R-0337, R-0338 (R-0338 landed in R19, not yet
resolved). No PR exists and closure has not started. `.agent/STOP` is gone.

## Goal
Costs stop being an opaque total: `remedy stats report` shows WHERE
tokens go — by segment kind, by role, by task class — plus a cost curve
and a prior-period comparison, as markdown and json, every number
traceable to a ledger row, and a period with missing data reported as
missing instead of interpolated (docs/roadmap/features/T2_F115.md).

## Current Step
R19 repaired the one false sentence in
`docs/guides/cost-report-user-guide-v0.md`: the per-role limit note is
printed by `remedy stats cache --by role`, not by `remedy stats cost`, and
`remedy stats report` does not print it at all. T003 is otherwise complete.

## Next Steps
1. Reviewer gates R19 and authors `Done: R-0338`.
2. Integration gate (docs/agents/integration_gate.md), full suite
   `-n auto`, R-0322's five pre-existing reds expected.
3. Closure per docs/roadmap/STATUS_closure_protocol.md: evidence job, a
   FRESH review zip, the authored STATUS line committed last, then the PR.

## Risks
- The work tree carries ` M scripts/make_review_zip.sh`, made by no agent
  of this session. It is the durable fix R-0295 names, and DECISION F107
  D3 forbids landing it inside a feature that does not own the packager.
  It is left untouched; every commit stages explicit paths. It will block
  a clean review zip at closure and needs the operator.
- Per-role has one bucket until `role` stops being hardcoded, and
  per-task-class has no source at all: report "no data", never a bucket.
- R-0322 will meet F115's integration gate as five pre-existing reds.
- The goldens are DATA: no test may regenerate them.

Fortschritt: 97 % (T001 ✅ · T002 ✅ · T003 ✅ — Integration-Gate und
Closure offen) — Schätzung
