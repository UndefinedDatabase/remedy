# Plan — F115 Prompt breakdown & cost report

Branch: feature/f115-prompt-cost-report, cut from main at 0d6c97aa after
PR #194 merged. Last reviewed SHA: 6752841a (R15 PASS). Next free finding
ID: R-0337. Open findings: 10 — R-0320, R-0322, R-0323, R-0324, R-0327,
R-0328, R-0331, R-0333, R-0334, R-0336. R-0335 was RESOLVED at the R15
gate. No PR exists and closure has not started.

## Goal
Costs stop being an opaque total: `remedy stats report` shows WHERE
tokens go — by segment kind, by role, by task class — plus a cost curve
and a prior-period comparison, as markdown and json, every number
traceable to a ledger row, and a period with missing data reported as
missing instead of interpolated (docs/roadmap/features/T2_F115.md).

## Current Step
T003 is half built. The period has two ends and the comparison now has
its arithmetic: `prior_report_period` places the equal-length window
before `[since, until)`, reusing the current `since` STRING as the prior's
exclusive end so the two windows abut under the same lexicographic
compare (DECISION F115 D6). Four cases yield no window and each states
its reason; a window that exists but is empty says so rather than
rendering zeros. Both renderers print the comparison, `_same_question`
refuses a prior that is not this period's prior, and
`COST_REPORT_VERSION` is 3. No CLI is wired.

## Next Steps
1. T003c — the `remedy stats report` CLI, markdown and `--json`, with its
   catalog entry, `--since`/`--until` validation and the second query the
   comparison needs; `stats_ledger_cmd.UNMEASURED` becomes an import of
   `COST_UNMEASURED_LABEL` so the concept keeps one spelling.
2. T003d — the docs page the new user-visible behaviour needs.
3. Integration gate (docs/agents/integration_gate.md).
4. Closure per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- Per-role has one bucket until `role` stops being hardcoded, and
  per-task-class has no source at all: report "no data", never a bucket.
- R-0322 will meet F115's integration gate as five pre-existing reds.
- The goldens are DATA: no test may regenerate them. A renderer change
  that moves the bytes must move the files in the same, argued commit.

Fortschritt: 88 % (T001 ✅ · T002 ✅ · T003 halb) — Schätzung
