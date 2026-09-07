# Plan — F274 One world completion, part two

Branch: feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, with `main` merged back in at `f85200e4` to take
operator amendment amend0907-cluster-first.

## Goal

Finish what F272 could not reach inside its own limit: the prototype cluster deletion and the
classic-to-unified record flip DECISION F272 D15 measured as ATOMIC. DECISION
amend0907-cluster-first D1 reorders the slices so the deletion runs FIRST.

## Current Step

Round 4: cut three of the deletion map's forty-two edges. `apps/cli/commands/context.py` and
`apps/cli/commands/worker.py` each host both surviving and cluster-bound commands; move the
cluster-bound handlers into three new files that are themselves cluster-bound, so their imports
die with the cluster instead of blocking it. Book round 3's PASS verdict. Nothing is deleted and
no command id changes.

## Next Steps

1. The remaining edge cuts the map records, module group by module group. The two modules with no
   edge at all, `review_bundle` and `self_repair_proposal`, are deletable whenever the deletion
   itself may start.
2. The first carry-over, on the route DECISION F274 D2 fixes: the read-only overnight readiness
   and report views survive as `mission readiness` and `mission report`, the latter only in the
   commit that deletes the cluster-bound command already holding that name.
3. Draft DECISION F260 D3, the deletion paragraph, naming every deleted module and the feature
   that inherited its idea. Nothing is deleted before it exists.
4. The cluster deletion itself, one commit per module group, NEVER SPLIT ACROSS SESSIONS.
5. T001 — measure the `Job.id` flip with a recording property, rule the cap route, and rule the
   persisted key: `Job` stores its identity under the JSON key `"id"`, so renaming the field
   alone makes a stored job load with a FRESH id.
6. T002 — the classic runner and the resolver collapse.

## Risks

- The deletion reaches further than F260's Design describes: of the catalog's 341 command ids,
  311 resolve to an owning handler file and 105 of those sit in one of the 21 files that import a
  cluster module, `mission.run` and `mission.report` among them.
- The open High findings are R-0803, R-0804, R-0806 and R-0807, all F273's rather than this
  feature's, per DECISION F272 D12.
