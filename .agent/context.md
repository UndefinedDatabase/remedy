# Context — F296 Evidence-triggered tier escalation (routing v2)

## Active Branch
`feature/f296-tier-escalation`, from `main` at `eb7aa432b` (the merge commit of pull request 377,
which carried F307).

## Scope
F296 (Tier 3), as `docs/roadmap/features/T3_F296.md` and DECISION F296 D1 state it: one step up
the model tiers for one task's next repair round, on evidence, with its record and its benchmark.

## Do not touch
F058's trigger and its disclosure; F110's seed table, hard rules and promotion rule; the budget
guards — an escalated round still spends inside the job's budget.

## Active assumptions
- Every behaviour lands with a test that is red without it, proved by the reviewer's mutation.

## Constraints
- One full pytest suite per feature, in the closure's integration-gate round; every round runs
  its own selection once (operator amendments amend0917-throughput and amend0930-test-load).
- The structure ratchet: no listed function or file grows; new logic goes into new modules.
- No file under `.agent/` gains this machine's absolute paths; the commit hook refuses them.

## Steps
The item-status table for each round lives in that round's handback, `.agent/handoff.md`.
