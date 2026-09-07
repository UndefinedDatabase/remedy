# Plan — F274 One world completion, part two

Branch: feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, with `main` merged back in at `f85200e4` to take
operator amendment amend0907-cluster-first.

## Goal

Finish what F272 could not reach inside its own limit: the prototype cluster deletion and the
classic-to-unified record flip DECISION F272 D15 measured as ATOMIC. DECISION
amend0907-cluster-first D1 reorders the slices so the deletion runs FIRST.

## Current Step

Round 6: cut `context_optimizer`'s last recorded edge by deleting the `context_budget` BRAIN NODE
from the six production files that build, render, weight, colour and describe it, together with
its deletion-map line and the four tests that read it. That takes `context_optimizer` to zero
edges and makes it the fourth module the deletion may take. Book round 5's PASS verdict, register
R-0832 and append round 5's two prose slips. No module is deleted this round.

## Next Steps

1. `worker_recommend`'s three remaining edges, in `agent_loop.py`, `autonomy_loop.py` and
   `dashboard.py`. These are LIVE RUNTIME CALLS rather than read-only views, so a DECISION naming
   what inherits worker recommendation is authored before the cut.
2. The `worker_facade_cmd.py` edges, which carry the `mission report` name collision DECISION
   F274 D2 rules.
3. The remaining edges, of which `packages/orchestration/ui_server.py` holds the most by far.
4. The first carry-over, on the route DECISION F274 D2 fixes: the read-only overnight readiness
   and report views survive as `mission readiness` and `mission report`, the latter only in the
   commit that deletes the cluster-bound command already holding that name.
5. Draft DECISION F260 D3, the deletion paragraph, naming every deleted module and the feature
   that inherited its idea. R-0832's fix clause binds it. Nothing is deleted before it exists.
6. The cluster deletion itself, one commit per module group, NEVER SPLIT ACROSS SESSIONS.
7. T001 — measure the `Job.id` flip with a recording property, rule the cap route, and rule the
   persisted key. Then T002 — the classic runner and the resolver collapse.

## Risks

- Of the catalog's 341 command ids, 311 resolve to an owning handler file and 105 of those sit in
  one of the 21 files that import a cluster module, `mission.run` and `mission.report` among them.
- The open High findings are R-0803, R-0804, R-0806 and R-0807, all F273's rather than this
  feature's, per DECISION F272 D12.
