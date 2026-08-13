# Plan — F115 Prompt breakdown & cost report

Branch: feature/f115-prompt-cost-report, cut from main at 0d6c97aa after
PR #194 merged. Last reviewed SHA: aa7ad8df (R16 PASS). Next free finding
ID: R-0337. Open findings: 10 — R-0320, R-0322, R-0323, R-0324, R-0327,
R-0328, R-0331, R-0333, R-0334, R-0336. No PR exists and closure has not
started.

## Goal
Costs stop being an opaque total: `remedy stats report` shows WHERE
tokens go — by segment kind, by role, by task class — plus a cost curve
and a prior-period comparison, as markdown and json, every number
traceable to a ledger row, and a period with missing data reported as
missing instead of interpolated (docs/roadmap/features/T2_F115.md).

## Current Step
T003 is wired to a user. `remedy stats report` resolves one project's
ledger, runs the cost and share queries over `[since, until)`, places the
prior window with `prior_report_period` and queries it under the SAME job
filter, then renders markdown or json. `--all-projects` is deliberately
absent: there is no cross-project merge for the segment breakdown, so an
all-projects report would publish one project's breakdown under a
multi-project total. `stats_ledger_cmd.UNMEASURED` is now an import of
`COST_UNMEASURED_LABEL`, so the word has one spelling.

## Next Steps
1. T003d — the docs page the new user-visible behaviour needs, registered
   in the `docs/README.md` index in the same PR.
2. Integration gate (docs/agents/integration_gate.md).
3. Closure per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- Per-role has one bucket until `role` stops being hardcoded, and
  per-task-class has no source at all: report "no data", never a bucket.
- R-0322 will meet F115's integration gate as five pre-existing reds.
- The goldens are DATA: no test may regenerate them. A renderer change
  that moves the bytes must move the files in the same, argued commit.
- The `remedy` binary is refused in this session's sandbox, so CLI wiring
  is proven through the suite and never through a pasted `--help`.

Fortschritt: 93 % (T001 ✅ · T002 ✅ · T003 fast fertig) — Schätzung
