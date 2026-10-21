# Context — F313 Contract 1.22 for the Orb

## Active Branch
`feature/f313-contract-1-22` from `main` at `25ab7c98b` (the merge commit of pull request 371).

## Scope
F313's three slices T001 to T003 as `.agent/plan.md` orders them. F313 owns no open finding at its
claim. Steps outside the feature file's slices are out of scope.

## Assumptions
- Inside one major version the interface only grows: no 1.21 route, key or word is removed or
  renamed (the feature file's Do-not-touch).
- The recorded answers live in this repository; the universe's kit copies them (DECISION F313 D2).

## Constraints
- One full pytest suite per feature, in the closure's integration-gate round; every round runs
  its own selection once (operator amendments amend0917-throughput and amend0930-test-load).
- The structure ratchet: no listed function or file grows; new logic goes into new modules.
