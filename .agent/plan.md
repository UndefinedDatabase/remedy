# Plan — amend0825-dogfood-findings

Branch: feature/amend0825-dogfood-findings, cut from `main` at `6325ac2f`, the
merge commit of pull request #213. Operator collection order amend0825, no
self-drive loop; the operator prompt carries the authorization for every
decision named below.

## Goal
Six findings from the first operator dogfooding run (project ~/demo-remedy,
jobs edbbc42bba4c4b00 and e984ec1943bb422f) are triaged by ONE rule: a finding
is repaired in code only when the repair is surgical AND a regression test
proves it; everything larger becomes a dated "Operator finding (2026-08-25,
dogfooding)" paragraph in the owning file under docs/roadmap/features/.
Findings are NOT written to `.agent/candidates.md` — that would block feature
claims — and no new STATUS line is registered unless no existing feature file
can carry the finding.

## Current Step
C1 — Finding 1: `remedy do run` with budget flags crashes with
StopControlError "invalid job id ''" before the first model call. The
budget-aware stop check on the job-less ping-pong path calls `should_stop("")`,
whose operator-stop layer is addressed by job id. Fix: consult the budget
guard directly on this path; `validate_job_id` is NOT weakened.

## Next Steps
1. C2 — Finding 5: `doctor core` resolves the two test lanes relative to the
   process working directory; make the resolution installation-relative.
2. C3 — Finding 6: repoint `claude-flagship`/`claude-workhorse` onto live ids
   per the operator decision, and print the effective model on the bare
   `do run` path.
3. C4 — Finding 2: extend job-id resolution to the task-job store so the
   teacher can read job-based runs.
4. C5 — Finding 3: record the ledger gap in docs/roadmap/features/T2_F103.md.
5. C6 — Finding 4: record the promotion dead-end in
   docs/roadmap/features/T0_F017.md.
6. Verification battery, pull request, hosted CI green, self-merge.

## Risks
- `.agent/STOP` is on disk, untracked, from the stopped F031 R10 round. It
  governs the self-drive loop, not this order; it is never deleted here.
- Finding 3 is a design gap, not wiring: job runs mirror into the F103 ledger
  only through `export_job_evidence`, so a run that never exports records
  nothing. It is recorded, not repaired.
- Finding 4's guardrail is correct and stays untouched; only the missing
  partial-promotion path and the missing next-step line are recorded.
