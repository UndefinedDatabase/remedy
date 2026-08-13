# Plan — F115 Prompt breakdown & cost report

Branch: feature/f115-prompt-cost-report, cut from main at 0d6c97aa after PR
#194 merged. Last reviewed SHA: 7bc57cd1. R21's verdict is PASS; the
integration gate is green. Next free finding ID: R-0343. Open findings: 14 —
R-0320, R-0322/23/24, R-0327/28, R-0331, R-0333/34, R-0336/37, R-0339,
R-0341/42 — all Medium/Low. No PR exists.

## Goal
Costs stop being an opaque total: `remedy stats report` shows WHERE tokens go
— by segment kind, by role, by task class — plus a cost curve and a
prior-period comparison, as markdown and json, every number traceable to a
ledger row, missing data reported as missing (docs/roadmap/features/T2_F115.md).

## Current Step
R24 HALTED at ITEM B, a THIRD time, on stop-on-false-claim. Only C0
(d4a27801) landed; ITEM A was blocked too. Two ITEM B claims are refuted
mechanically; 38 of 41 checked claims verified TRUE:
1. "the catalog entry's description says why where `remedy stats --help` will
   print it". FALSE. `help_renderer._box` truncates each Commands row to 78
   columns, so that command prints only "Cost report over ONE project's
   ledger: the cost table, whe…". The command that prints the --all-projects
   rationale in full is `remedy stats report --help` (`render_command_help`).
2. "…and one that existed but held no calls: … `_PRIOR_REASON_EMPTY_PERIOD`".
   FALSE. That constant reads "this period ends at or before it starts",
   returned when `length <= timedelta(0)`. `prior_report_period` is PURE (no
   ledger), so no reason of its means "we looked and found nothing" — that
   fact lives in `cost_report.COST_EMPTY_COMPARISON`.
ITEM A blocked as a consequence: R-0343's text certifies the R24 rewrite as
carrying "no claim the reviewer had not re-verified mechanically" — claim 1
refutes that, so committing it would put a false certification in the ledger.

## Next Steps
1. Reviewer re-authors ITEM B with claims 1 and 2 corrected, AND amends
   R-0343 to drop the self-certification and register the new instance.
2. Closure per docs/roadmap/STATUS_closure_protocol.md: evidence job, a FRESH
   review zip, the authored STATUS line committed last, then the PR.

## Risks
- The work tree carries ` M scripts/make_review_zip.sh`, made by no agent of
  this session. DECISION F115 D7 leaves it untouched until closure stashes it.
- The repo already carries five unrelated stashes, so a "stash list non-empty"
  gate cannot fail; the closure gate must match the new entry's message.
- The goldens are DATA: no test may regenerate them.
- Three rounds lost to one defect class: a PROPERTY attributed to a NAME the
  reviewer never ran a command against. R24 dropped line numbers but kept the
  attributions.

Fortschritt: 98 % (T001 ✅ · T002 ✅ · T003 ✅ · Integration-Gate ✅ — Closure offen) — Schätzung
