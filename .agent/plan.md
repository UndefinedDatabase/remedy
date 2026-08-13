# Plan — F115 Prompt breakdown & cost report

Branch: feature/f115-prompt-cost-report, cut from main at 0d6c97aa after
PR #194 merged. Last reviewed SHA: fbaab57f. R20's gate verdict was FAIL, on
the single ground that High finding R-0340 was open; R20's execution was
correct and its evidence is what made the failure legible. Next free finding
ID: R-0342. Open findings: 13 — R-0320, R-0322, R-0323, R-0324, R-0327,
R-0328, R-0331, R-0333, R-0334, R-0336, R-0337, R-0339, R-0341. R-0340 is
landed and awaits the reviewer's `Done:`. No PR exists; closure has not
started. `.agent/STOP` is gone.

## Goal
Costs stop being an opaque total: `remedy stats report` shows WHERE
tokens go — by segment kind, by role, by task class — plus a cost curve
and a prior-period comparison, as markdown and json, every number
traceable to a ledger row, and a period with missing data reported as
missing instead of interpolated (docs/roadmap/features/T2_F115.md).

## Current Step
R21 persisted the R20 verdict with findings R-0340 and R-0341, then repaired
R-0340 with one signature line: the double at `tests/test_run_log_cli.py:78`
now mirrors `plan_job_with_llm`'s keyword-only `on_prompt_composed`. No
assertion moved. The branch side of the gate was re-run against the unmoved
merge base; `comm -13` is EMPTY, so the six branch-only failures are gone and
nothing replaced them. Evidence in `.agent/gate_f115_r21/`.

## Next Steps
1. Reviewer gates R21 and issues the verdict on the repair and the re-run.
2. Closure per docs/roadmap/STATUS_closure_protocol.md: evidence job, a FRESH
   review zip, the authored STATUS line committed last, then the PR.

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
- R-0340's lesson: F115's cover for that call site,
  `tests/orchestration/test_structured_planner_cli.py:302`, asserts the SOURCE
  TEXT of `job.py`, so it can prove the wiring was written and can never prove
  it runs — it cannot catch a stale test double. Any further call-site wiring
  on this branch needs a test that EXECUTES the call.

Fortschritt: 98 % (T001 ✅ · T002 ✅ · T003 ✅ · Integration-Gate rot→repariert — Closure offen) — Schätzung
