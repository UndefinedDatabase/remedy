# Plan — F274 One world completion, part two

Branch: feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, with `main` merged back in at `f85200e4` to take
operator amendment amend0907-cluster-first.

## Goal

Finish what F272 could not reach inside its own limit: the prototype cluster deletion and the
classic-to-unified record flip DECISION F272 D15 measured as ATOMIC. DECISION
amend0907-cluster-first D1 reorders the slices so the deletion runs FIRST.

## Current Step

Round 13, the FIRST of `worker_recommend`'s three edges. Rule DECISION F274 D7 before a line moves:
worker recommendation dies with the cluster and nothing inherits it, the token mode never belonged
to it and moves to `packages/orchestration/token_policy.py`, and the `token_policy_applied`
vocabulary is ruled down to what a surviving producer measures. Then cut the `dashboard.py` edge —
the one emitting no run-log event — deleting the `worker_recommendation` section with its
contract-test and smoke-script pins. Book round 12's PASS verdict and the slip round 12 owed.

## Next Steps

1. The two remaining `worker_recommend` edges, in `agent_loop.py` and `autonomy_loop.py`. Both emit
   `token_policy_applied`, so this is where DECISION F274 D7 item 4 lands: three keys leave
   `packages/orchestration/event_schemas.py` in the same commit as the last emitter that writes
   them, and `CycleDecision.selected_worker` goes with them.
2. The two carry-overs F260's Design names: overnight readiness to `mission readiness`, and the
   route-policy knobs checked against F110's config keys. `mission report` waits for the commit
   deleting its current holder, per DECISION F274 D2; that holder is in `worker_facade_cmd.py`.
3. `orchestrator_brain.py`'s four edges, measured as live signal reads in `_scrub`, `_review_state`,
   `_gather_signals` and `consult_local_advisor_for_decision` — a surviving module reading cluster
   modules, so a behaviour change rather than a deletion.
4. The four `worker_facade_cmd.py` edges and `worker_registry`'s remaining pair.
5. Draft DECISION F260 D3, the deletion paragraph. R-0832's fix clause binds it.
6. The cluster deletion itself, one commit per module group, NEVER SPLIT ACROSS SESSIONS.
7. T001 — the `Job.id` flip. Then T002 — the classic runner and the resolver collapse.

## Risks

- The map was blind twice and is fixed once: R-0834's file-type blindness is closed, R-0832's
  event-name coupling is OPEN. Treat every "zero edges" reading as a claim about the WALKER.
- The open High findings are R-0803, R-0804, R-0806 and R-0807, all F273's rather than this
  feature's, per DECISION F272 D12.
