# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1. Round 27 fixed the evidence-packager
contract (R-0792, R-0793); round 28 rebuilt the closure evidence bundle
and review zip, confirmed READY_FOR_REVIEW/true on the real packaged
artifact; round 29 booked round 28's verdict and discovered closure
precondition 6 (self-use) was already discharged at round 21, so no
further self-use work is owed. All six closure preconditions are now
satisfied. Round 30 is the closure commit and the pull request.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion
cascade with full omission disclosure, and a context that cannot fit
raises a task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 30 books round 29's PASS verdict, then lands the closure commit
per docs/roadmap/STATUS_closure_protocol.md algorithm step 5: the
authored STATUS `[x]` line, the README capability-sync paragraph (same
commit, R-0154 pin), `scripts/self_use_queue.json`'s SU-007
`consumed_by=F112` — nothing else. Then the AGENTS.md PR workflow opens
the pull request; it is NOT merged this round.

## Next Steps

- Round 31: Open PR Gate — hosted CI green, docs gate/canary/touched
  suites pass, planner merges per the standing merge-autonomy rule; hand
  back the built zip's name and SHA-256 to the operator for archiving
  and the formal package review.

## Risks

- `R-0784` and `R-0767` (both OPEN, unrelated to F112) are documented,
  pre-existing risks; F112's live-review verdict is PASS_WITH_RISKS for
  exactly this reason, matching F109's and F110's own closed precedent.
- Hosted CI must read green before the PR is merged; a red hosted run is
  a blocker, not something to route around.