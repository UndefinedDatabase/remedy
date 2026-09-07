# Plan — F274 One world completion, part two

Branch: feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, the merge commit of pull request 244. F272 closed
at the scope DECISION F272 D16 fixed; this feature owns the remainder.

## Goal

Finish what F272 could not reach inside its own limit: the classic-to-unified record flip
DECISION F272 D15 measured as ATOMIC, and the prototype cluster deletion. T001 moves no
production line — it replaces D15's receiver-name BOUND with a measured site set and rules how
an atomic change lands under a per-commit cap that forbids it.

## Current Step

Round 1: claim F274 in the ledger, cut the branch, re-point this file and `.agent/context.md`,
re-head `.agent/live_review.md` and book F272's round 31 verdict into it, run the DECISION F272
D7 raising-property probe over `Job.id` in a disposable worktree, commit the measured site set
as `.agent/f274_id_probe_inventory.md`, and record the route as DECISION F274 D1.

## Next Steps

1. Rule the persisted-key question the probe exposed, before any consumer moves: `Job` stores
   its identity under the JSON key `"id"`, so renaming the field alone makes a stored job load
   with a FRESH id. DECISION F272 D5 answered the same question for `status` by ruling the
   stored key does not move.
2. T002 — the classic runner and the resolver collapse, on the route DECISION F274 D1 fixes.
3. T003 — the reachability test, the two carry-overs, DECISION F260 D3, then the cluster
   deletion, one commit per module group. NEVER SPLIT INSIDE T003.

## Risks

- The flip is atomic by construction and far over the DECISION F104 D1 cap of 500 insertions.
  D1 rules the route, and that ruling bounds every later commit's size.
- Five open High findings — R-0803, R-0804, R-0806, R-0807 and R-0827 — are F273's and not
  this feature's, per DECISION F272 D12.
