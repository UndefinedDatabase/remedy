# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1. Round 30 landed the closure commit
(STATUS [x], README capability sync, self_use_queue SU-007
consumed_by=F112) but halted before the pull request: flipping F112's
STATUS line to [x] moved README's own derived "N of 266 accepted" count
and Tier 3 table Done cell, which round 30's block never named. Round 31
fixes exactly those two numerals, re-confirms the docs gate green, and
opens the pull request.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion
cascade with full omission disclosure, and a context that cannot fit
raises a task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 31 books round 30's PASS-with-declared-deviation verdict, fixes
README.md's stale "69 of 266" -> "70 of 266" line and its Tier 3 table
Done cell "4" -> "5", re-runs the docs gate to confirm green, then opens
the pull request per the AGENTS.md PR workflow. Not merged this round.

## Next Steps

- Round 32: Open PR Gate — hosted CI green, docs gate/canary/touched
  suites pass, planner merges per the standing merge-autonomy rule; hand
  back the built zip's name and SHA-256 to the operator for archiving
  and the formal package review.

## Risks

- R-0784 and R-0767 (both OPEN, unrelated to F112) are documented,
  pre-existing risks; F112's live-review verdict is PASS_WITH_RISKS.
- Hosted CI must read green before the PR is merged; a red hosted run is
  a blocker, not something to route around.