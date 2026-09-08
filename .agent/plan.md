# Plan — F274 One world completion, part two

Branch: feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, with `main` merged back in at `f85200e4` to take
operator amendment amend0907-cluster-first.

## Goal

Finish what F272 could not reach inside its own limit: the prototype cluster deletion and the
classic-to-unified record flip DECISION F272 D15 measured as ATOMIC. DECISION
amend0907-cluster-first D1 reorders the slices so the deletion runs FIRST.

## Current Step

Round 9, a DELETION ROUND under operator amendment amend0906-triage-throughput: cut the six
read-only cockpit sections of `packages/orchestration/ui_server.py` whose subject modules owe no
carry-over, with the six deletion-map lines and the six tests those cuts force. DECISION F274 D4
rules the deletion first, and rules why SIX rather than the eight the round 8 handback measured:
`overnight_readiness` and `builder_routing` are the sources of F260's two carry-overs, so their
edges are held until the carry-over lands. Book round 8's PASS verdict and the R-0819 recurrence.
No cluster module is deleted this round.

## Next Steps

1. `worker_recommend`'s three edges, in `agent_loop.py`, `autonomy_loop.py` and `dashboard.py`.
   These are LIVE RUNTIME CALLS rather than read-only views, so a DECISION naming what inherits
   worker recommendation is authored before the cut.
2. The two carry-overs F260's Design names, each with the cockpit section this round held back:
   overnight readiness to `mission readiness`, and the route-policy knobs checked against F110's
   config keys. `mission report` waits for the commit that deletes its current holder, per
   DECISION F274 D2.
3. The `ui_server.py` edges that survive both of the above: `local_model_advisor`,
   `main_builder_adapter`, `managed_builder_execution`, `overnight_executor`, `provider_trust`,
   `provider_trust_verification` and `worker_registry` — each has a second consumer outside
   `ui_server.py`, so cutting its cockpit section alone does not free it.
4. The `worker_facade_cmd.py` edges, which carry the `mission report` name collision, and the two
   `feature_cmd.py` edges, which are live CLI commands.
5. Draft DECISION F260 D3, the deletion paragraph. R-0832's fix clause binds it.
6. The cluster deletion itself, one commit per module group, NEVER SPLIT ACROSS SESSIONS.
7. T001 — the `Job.id` flip. Then T002 — the classic runner and the resolver collapse.

## Risks

- The map was blind twice and is now fixed once: R-0834's file-type blindness is closed, R-0832's
  event-name coupling is OPEN. Treat every "zero edges" reading as a claim about the WALKER.
- The open High findings are R-0803, R-0804, R-0806 and R-0807, all F273's rather than this
  feature's, per DECISION F272 D12.
