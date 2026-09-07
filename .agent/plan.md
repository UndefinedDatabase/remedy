# Plan — F274 One world completion, part two

Branch: feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, with `main` merged back in at `f85200e4` to take
operator amendment amend0907-cluster-first.

## Goal

Finish what F272 could not reach inside its own limit: the prototype cluster deletion and the
classic-to-unified record flip DECISION F272 D15 measured as ATOMIC. DECISION
amend0907-cluster-first D1 reorders the slices so the deletion runs FIRST.

## Current Step

Round 2: land the D11c import-reachability test and its allowlist, rule the test's shape and
T003's split boundary as DECISION F274 D1, register R-0830 — the cluster is reachable from all
six D11c entry points, so F260's "already absent from the reachable set" precondition is
unmeetable as written — and book round 1's PASS verdict and the reviewer's two round 1 slips.

## Next Steps

1. The two carry-overs F260's Design names, done BEFORE the first `git rm`: overnight readiness
   and the overnight report become read-only `mission readiness` / `mission report`; every
   user-settable route-policy knob is checked against F110's config keys, existing knob deleted,
   missing knob registered as a finding and never rebuilt.
2. Draft DECISION F260 D3, the deletion paragraph, naming every module and the feature that
   inherited its idea. Nothing is deleted before it exists.
3. The cluster deletion itself, one commit per module group, NEVER SPLIT ACROSS SESSIONS: a
   session that cannot finish it does not start it.
4. T001 — measure the `Job.id` flip with a recording property and rule the cap route. The probe
   also has to rule the persisted key: `Job` stores its identity under the JSON key `"id"`, so
   renaming the field alone makes a stored job load with a FRESH id.
5. T002 — the classic runner and the resolver collapse.

## Risks

- The deletion is far larger than F260's Design lists: 33 production files import the cluster,
  and consumers outside the handler set must be cut before a module can go.
- The open High findings are R-0803, R-0804, R-0806 and R-0807, and all of them are F273's
  rather than this feature's, per DECISION F272 D12. R-0827 was the fifth until operator
  amendment amend0907-cluster-first resolved it.
