# Plan — F274 One world completion, part two

Branch: feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, with `main` merged back in at `f85200e4` to take
operator amendment amend0907-cluster-first.

## Goal

Finish what F272 could not reach inside its own limit: the prototype cluster deletion and the
classic-to-unified record flip DECISION F272 D15 measured as ATOMIC. DECISION
amend0907-cluster-first D1 reorders the slices so the deletion runs FIRST.

## Current Step

Round 11, a DELETION ROUND under operator amendment amend0906-triage-throughput and the first that
deletes COMMANDS rather than read-only views: delete the `feature` command group entirely — the
handler file `apps/cli/commands/feature_cmd.py`, its two catalog entries and their group, its
package wiring, its packaging and allowlist memberships, its boundary-doc row, its two runtime test
classes and its two deletion-map lines. `feature_planner` and `progress_ledger` both reach ZERO
recorded edges. DECISION F274 D6 rules the deletion before a line is cut. Book round 10's PASS
verdict. No cluster module is deleted this round.

## Next Steps

1. `worker_recommend`'s three edges, in `agent_loop.py`, `autonomy_loop.py` and `dashboard.py`.
   These are LIVE RUNTIME CALLS rather than read-only views: the reviewer measured that they feed
   the `token_policy_applied` run-log event and `CycleDecision.selected_worker`, and that
   `selected_worker` is named in `packages/orchestration/event_schemas.py`, so a DECISION naming
   what inherits worker recommendation is authored before the cut and the ruled event vocabulary
   is part of the question.
2. The two carry-overs F260's Design names, each freeing a cockpit section held back so far:
   overnight readiness to `mission readiness`, and the route-policy knobs checked against F110's
   config keys. `mission report` waits for the commit that deletes its current holder, per
   DECISION F274 D2, and that holder is in `worker_facade_cmd.py`.
3. `orchestrator_brain.py`'s four edges, which the reviewer measured as live signal reads in
   `_scrub`, `_review_state`, `_gather_signals` and `consult_local_advisor_for_decision` — a
   surviving module reading cluster modules, so a behaviour change rather than a deletion.
4. The four `worker_facade_cmd.py` edges and `worker_registry`'s remaining pair.
5. Draft DECISION F260 D3, the deletion paragraph. R-0832's fix clause binds it.
6. The cluster deletion itself, one commit per module group, NEVER SPLIT ACROSS SESSIONS.
7. T001 — the `Job.id` flip. Then T002 — the classic runner and the resolver collapse.

## Risks

- The map was blind twice and is now fixed once: R-0834's file-type blindness is closed, R-0832's
  event-name coupling is OPEN. Treat every "zero edges" reading as a claim about the WALKER.
- The open High findings are R-0803, R-0804, R-0806 and R-0807, all F273's rather than this
  feature's, per DECISION F272 D12.
