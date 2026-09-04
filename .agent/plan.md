# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1. Round 27 fixed the evidence-packager
contract (R-0792, R-0793); round 28 rebuilt the closure evidence bundle
and review zip, confirmed READY_FOR_REVIEW/true on the real packaged
artifact (RECORD28). Round 29 discovered that PLAN29's own premise was
stale: closure precondition 6 (the self-use item) was ALREADY discharged
at round 21 (commit `1b9ac1ca`, RECORD21) — SU-007 was already planned
and RUN to the approval gate there (job `848fc4c67d7b405b`, blocked,
evidence added to the already-open `R-0784` per §3 item 30) — so PLAN29's
own instruction to run it again was not carried out as new committed
evidence; round 29 halted at C3 per self-drive protocol G8 and declared
the discrepancy instead of landing a misleading duplicate.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion
cascade with full omission disclosure, and a context that cannot fit
raises a task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 29 booked round 28's PASS verdict (C1) and applied PLAN29
byte-exact per constraint 1 (C2), then at C3 found PLAN29's premise
false — precondition 6 needs no run, round 21 already ran and discharged
it. C3 was executed once (job `962cb3c9b96244ed`, same blocked outcome
as R21's job) then NOT committed, to avoid corrupting the record with a
duplicate; `scripts/self_use_queue.json` is untouched, SU-007's
`consumed_by` stays empty pending the closure commit.

## Next Steps

- Round 30: skip the self-use RUN step (already done at R21); go
  straight to the closure commit — STATUS `[x]` line, README capability
  sync, `self_use_queue` SU-007 `consumed_by=F112`, final `.agent/`
  state, PR opened, not merged.
- Round 31: Open PR Gate — hosted CI green, docs gate/canary/touched
  suites pass, planner merges per the standing merge-autonomy rule; hand
  back the built zip's name and SHA-256 to the operator.

## Risks

- `R-0784` (OPEN) already covers this defect class from R21's run; round
  29's redundant run (job `962cb3c9b96244ed`, same signature) was not
  committed — round 30 decides whether a third note is warranted.
- `R-0767` (OPEN, unrelated to F112) carries forward, documented.
