# Plan — F274 One world completion, part two

Branch: feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, with `main` merged back in at `f85200e4` to take
operator amendment amend0907-cluster-first.

## Goal

Finish what F272 could not reach inside its own limit: the prototype cluster deletion and the
classic-to-unified record flip DECISION F272 D15 measured as ATOMIC. DECISION
amend0907-cluster-first D1 reorders the slices so the deletion runs FIRST.

## Current Step

Round 15, the R-0836 fix: delete the `agent_loop_cycle_decision` and `agent_loop_stopped` entries of
`EVENT_METADATA_SCHEMAS` and the sites in `tests/orchestration/test_event_ledger.py` that pin them.
Their sole emitter died with `_cmd_run_loop` in F272 round 19, so the registry has been describing
two events the product does not write; this finishes that deletion. Book round 14's PASS verdict and
a RECURRENCE of R-0819 for a per-pair count two of that block's pairs could not meet, and resolve
R-0836 in this same round. No cluster module and no edge moves.

## Next Steps

1. The two carry-overs F260's Design names: overnight readiness to `mission readiness`, and the
   route-policy knobs checked against F110's config keys. `mission report` waits for the commit
   deleting its current holder, per DECISION F274 D2; that holder is in `worker_facade_cmd.py`.
2. `orchestrator_brain.py`'s four edges, measured as live signal reads in `_scrub`, `_review_state`,
   `_gather_signals` and `consult_local_advisor_for_decision` — a surviving module reading cluster
   modules, so a behaviour change rather than a deletion.
3. The four `worker_facade_cmd.py` edges and `worker_registry`'s remaining pair.
4. Draft DECISION F260 D3, the deletion paragraph. R-0832's fix clause binds it, and it must name
   the event-name couplings the import map cannot see.
5. The cluster deletion itself, one commit per module group, NEVER SPLIT ACROSS SESSIONS.
   `worker_recommend` is already edge-free and goes with that round.
6. T001 — the `Job.id` flip. Then T002 — the classic runner and the resolver collapse.

## Risks

- The map was blind twice and is fixed once: R-0834's file-type blindness is closed, R-0832's
  event-name coupling is OPEN. Treat every "zero edges" reading as a claim about the WALKER.
- The open High findings are R-0803, R-0804, R-0806 and R-0807, all F273's rather than this
  feature's, per DECISION F272 D12.
