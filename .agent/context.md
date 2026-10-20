# Context — F312 The scope guard knows orders without file names

## Active Branch
`feature/f312-scope-kinds` from `main` at `0eda402fe` (the merge commit of pull request 369).

## Scope
F312's three slices T001 to T003 as `.agent/plan.md` orders them, with the finding it owns,
R-1369. Steps outside the feature file's slices are out of scope.

## Assumptions
- The kind of an order is read from its text alone: a spelled path, then a fence, else open
  (DECISION F312 D1).
- The review reports and job records of the operator's lab runs are not read by this feature's
  sessions; the finding's text and the code are the evidence.

## Constraints
- One full pytest suite per feature, in the closure's integration-gate round; every round runs
  its own selection once (operator amendments amend0917-throughput and amend0930-test-load).
- The structure ratchet: every listed function or file a round touches shrinks or stays as long
  as its row, and a row falls in the commit that shrinks it.
- Do not touch: the fence vocabulary of `order_scope` (amend1016p D1, exec-1017 D2),
  `is_checking_only`, and the refusal of a fenced order's foreign file (R-1363).
