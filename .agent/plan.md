# Plan — F115 Prompt breakdown & cost report

Branch: feature/f115-prompt-cost-report, cut from main at 0d6c97aa after
PR #194 merged. Last reviewed SHA: 7bc57cd1. R21's verdict is PASS; the
integration gate is green. Next free finding ID: R-0343. Open findings: 14 —
R-0320, R-0322, R-0323, R-0324, R-0327, R-0328, R-0331, R-0333, R-0334,
R-0336, R-0337, R-0339, R-0341, R-0342 — all Medium/Low. No PR exists.

## Goal
Costs stop being an opaque total: `remedy stats report` shows WHERE
tokens go — by segment kind, by role, by task class — plus a cost curve
and a prior-period comparison, as markdown and json, every number
traceable to a ledger row, and a period with missing data reported as
missing instead of interpolated (docs/roadmap/features/T2_F115.md).

## Current Step
R23 HALTED at ITEM B (the Built State), a second time, on stop-on-false-claim.
ITEM A landed: R-0342 is registered. The R23 Built State text carries two
claims that do not hold against source, so it was NOT written to
docs/roadmap/features/T2_F115.md:
1. "`prior_report_period` needs BOTH bounds (`token_ledger.py:1160-1161`)" —
   the both-bounds guard is at 1158-1159; 1160-1161 are `try:` and the first
   `_parse_period_bound` call.
2. "Three vocabulary decisions are load-bearing and pinned by tests" —
   only `COST_UNMEASURED_LABEL` is. `"(unlabelled)"` and `"(unnamed)"`, and
   their constant names, appear NOWHERE under `tests/` in any form.
51 of 54 checked claims verified TRUE. Third, minor: `_cmd_stats_report` is
cited as 509-568; its AST span is 509-566 (567-568 blank).

## Next Steps
1. Reviewer re-authors the Built State with those two claims corrected, then
   re-orders the closure from that item. ITEM A must NOT be re-applied.
2. Closure per docs/roadmap/STATUS_closure_protocol.md: evidence job, a FRESH
   review zip, the authored STATUS line committed last, then the PR.

## Risks
- The work tree carries ` M scripts/make_review_zip.sh`, made by no agent
  of this session. DECISION F115 D7 leaves it untouched until the closure
  round stashes it. Every commit stages explicit paths.
- Per-role has one bucket until `role` stops being hardcoded, and
  per-task-class has no source at all: the USER GUIDE states both limits;
  `remedy stats report` prints neither.
- The goldens are DATA: no test may regenerate them.
- R-0342's lesson: authored prose that attributes an OUTPUT to a COMMAND, or
  a PROPERTY to a symbol, must ship with a per-claim verification naming the
  enclosing function. Two rounds have now been spent on the same defect class.

Fortschritt: 98 % (T001 ✅ · T002 ✅ · T003 ✅ · Integration-Gate ✅ — Closure offen) — Schätzung
