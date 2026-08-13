# Plan — F115 Prompt breakdown & cost report

Branch: feature/f115-prompt-cost-report, cut from main at 0d6c97aa after
PR #194 merged. Last reviewed SHA: ce812bc0 (R19 PASS; R-0338 resolved). R20
is the integration gate: it RAN, its raw evidence is committed, and it is
handed back awaiting its verdict. Next free finding ID: R-0340. Open
findings: 12 — R-0320, R-0322, R-0323, R-0324, R-0327, R-0328, R-0331,
R-0333, R-0334, R-0336, R-0337, R-0339 (R-0338 resolved, R-0339 added).
No PR exists and closure has not started. `.agent/STOP` is gone.

## Goal
Costs stop being an opaque total: `remedy stats report` shows WHERE
tokens go — by segment kind, by role, by task class — plus a cost curve
and a prior-period comparison, as markdown and json, every number
traceable to a ledger row, and a period with missing data reported as
missing instead of interpolated (docs/roadmap/features/T2_F115.md).

## Current Step
R20 ran the integration gate per docs/agents/integration_gate.md and
committed `.agent/gate_f115_r20/`. It found a BLOCKER: six branch-only
failures in `tests/test_run_log_cli.py::TestPlanJobLocalRunLog`, serial-fail
on the branch and serial-pass at the merge base. Commit cb17024a added
`on_prompt_composed=` to the call at `apps/cli/commands/job.py:288` while the
stub at `tests/test_run_log_cli.py:78` still takes two positional parameters.
Per step 4 the round stopped and handed back; no fix was attempted.

## Next Steps
1. Reviewer gates R20 and issues the gate verdict.
2. Repair round for the blocker: widen the stub at
   `tests/test_run_log_cli.py:78` to accept the keyword. One test file.
3. Re-run the gate after the repair, then closure per
   docs/roadmap/STATUS_closure_protocol.md: evidence job, a FRESH review
   zip, the authored STATUS line committed last, then the PR.

## Risks
- The work tree carries ` M scripts/make_review_zip.sh`, made by no agent
  of this session. DECISION F115 D7 (which the R20 block called D4 — that
  ID was already taken) leaves it untouched now and stashes it in the
  closure round only. Every commit stages explicit paths.
- Per-role has one bucket until `role` stops being hardcoded, and
  per-task-class has no source at all: report "no data", never a bucket.
- R-0322 met the gate as five pre-existing reds, in both failed lists and
  in neither comm output, exactly as predicted.
- The goldens are DATA: no test may regenerate them.

Fortschritt: 98 % (T001 ✅ · T002 ✅ · T003 ✅ · Integration-Gate gelaufen — Closure offen) — Schätzung
