# Context — F310 Budgets that fit the provider, and one stop, one question

## Active Branch
`feature/f310-provider-budgets` from `main` at `ee53c20b3` (the merge commit of pull request 368).

## Scope
F310's four slices T001 to T004 as `.agent/plan.md` orders them, with the findings it owns,
R-1370 and R-1371. Steps outside the feature file's slices are out of scope.

## Assumptions
- The product default of the builder, the reviewer and the repair role is `pi` over Ollama, so a
  job run with no provider flag is of the `local` class (DECISION F310 D1).
- The review reports of the operator's lab runs are not read by this feature's sessions; the
  findings' text and the code are the evidence.

## Constraints
- One full pytest suite per feature, in the closure's integration-gate round; every round runs
  its own selection once (operator amendments amend0917-throughput and amend0930-test-load).
- The structure ratchet: every listed function or file a round touches shrinks or stays as long
  as its row, and a row falls in the commit that shrinks it.
- Do not touch: the disk floor, a paid provider's cost cap, the refusal codes of
  `answer_budget_decision` and the public API's version.
