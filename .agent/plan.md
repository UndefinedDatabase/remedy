# Plan — F274 One world completion, part two

Branch: feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, with `main` merged back in at `f85200e4` to take
operator amendment amend0907-cluster-first.

## Goal

Finish what F272 could not reach inside its own limit: the prototype cluster deletion and the
classic-to-unified record flip DECISION F272 D15 measured as ATOMIC. DECISION
amend0907-cluster-first D1 reorders the slices so the deletion runs FIRST.

## Current Step

Round 14, the last two `worker_recommend` edges, in `agent_loop.py` and `autonomy_loop.py`. This is
where DECISION F274 D7 item 4 lands: both loops stop calling `recommend_worker` and take their token
mode from `derive_token_mode`, `CycleDecision.selected_worker` goes, and `token_policy_applied`
loses `estimated_context_tokens`, `remote_model_requires_approval` and `selected_worker` in
`packages/orchestration/event_schemas.py` in the SAME commit as the last emitter that writes them,
with the test and smoke-script pins moved with them. `worker_recommend` then holds NO recorded edge
and becomes deletable. Book round 13's PASS verdict, register R-0836 and append the slip round 13
owed.

## Next Steps

1. Fix R-0836: delete the `agent_loop_cycle_decision` and `agent_loop_stopped` entries of
   `EVENT_METADATA_SCHEMAS` and the ten sites in `tests/orchestration/test_event_ledger.py` that
   pin them. Their sole emitter died with `_cmd_run_loop` in F272 round 19; this is that deletion
   finished, and it is a ruled vocabulary the product no longer speaks.
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
