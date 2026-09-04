# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1. Round 27 fixed the evidence-packager
contract (R-0792, R-0793); round 28 rebuilt the closure evidence bundle
and review zip, confirmed READY_FOR_REVIEW/true on the real packaged
artifact (RECORD28, this round). Closure preconditions 1-5 are now
satisfied; precondition 6 (the self-use item) is the last one — SU-007
is already pending in scripts/self_use_queue.json (consumed_by=""), so
this round plans and RUNS it for real through the shipped generator/
runner, mirroring F109 R19 and F110 R16's precedent exactly.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion
cascade with full omission disclosure, and a context that cannot fit
raises a task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 29 books round 28's PASS verdict, then runs SU-007 (an "Address
ledger finding R-0418" job) through
`packages.orchestration.self_use_runner.run_next_self_use_item` to the
normal approval gate — never promoted, `consumed_by` stays empty this
round. The run's defects (if any) and `consumed_by=F112` land in round
30, together with the closure commit.

## Next Steps

- Round 30: register any self-use-run defects as normal R-id findings,
  author the STATUS `[x]` line from round 28's evidence values, closure
  commit (STATUS, README capability sync, `self_use_queue` SU-007
  `consumed_by=F112`, final `.agent/` state), PR opened, not merged.
- Round 31: Open PR Gate — hosted CI green, docs gate/canary/touched
  suites pass, planner merges per the standing merge-autonomy rule;
  hand back the built zip's name and SHA-256 to the operator.

## Risks

- The self-use run may land `blocked` at its own approval gate (F109's
  SU-005 and F110's SU-006 both did) — a normal outcome per
  `self_use_runner`'s own docstring, not a failure of this round; its
  defects route to round 30's findings.
- R-0784 and R-0767 (both OPEN, unrelated to F112) carry forward as
  documented risks per precondition 1's "Resolved or documented risk".