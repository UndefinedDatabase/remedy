# Plan — F274 One world completion, part two

Branch: feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, with `main` merged back in at `f85200e4` to take
operator amendment amend0907-cluster-first.

## Goal

Finish what F272 could not reach inside its own limit: the prototype cluster deletion and the
classic-to-unified record flip DECISION F272 D15 measured as ATOMIC. DECISION
amend0907-cluster-first D1 reorders the slices so the deletion runs FIRST.

## Current Step

Round 7, the repair round for round 6's FAIL on gate G6. Cut the `context_budget` half of
`scripts/remedy_smoke.sh` section 12ai, which round 6 left importing two deleted symbols, and then
widen the deletion map's walker so a consumer that embeds first-party python in a non-python file
under a consumer root can no longer hide from it. Recording the edge that walk newly sees returns
`context_optimizer` to ONE consumer, so it is NOT deletable and round 6's zero-edge reading is
corrected on disk. Book round 6's FAIL verdict, register R-0833 and R-0834, and mark both Landed.

## Next Steps

1. Cut section 12ah of `scripts/remedy_smoke.sh`, the last recorded consumer of
   `context_optimizer`, in the round that takes that module to zero for real.
2. `worker_recommend`'s three remaining edges, in `agent_loop.py`, `autonomy_loop.py` and
   `dashboard.py`. These are LIVE RUNTIME CALLS rather than read-only views, so a DECISION naming
   what inherits worker recommendation is authored before the cut.
3. The `worker_facade_cmd.py` edges, which carry the `mission report` name collision DECISION
   F274 D2 rules.
4. The remaining edges, of which `packages/orchestration/ui_server.py` holds the most by far.
5. The first carry-over, on the route DECISION F274 D2 fixes: the read-only overnight readiness
   and report views survive as `mission readiness` and `mission report`.
6. Draft DECISION F260 D3, the deletion paragraph. R-0832's and R-0834's fix clauses bind it.
7. The cluster deletion itself, one commit per module group, NEVER SPLIT ACROSS SESSIONS.
8. T001 — the `Job.id` flip. Then T002 — the classic runner and the resolver collapse.

## Risks

- The map is now proven blind twice: to event-name coupling (R-0832) and, until this round, to
  embedded python (R-0834). Treat every "zero edges" reading as a claim about the WALKER.
- The open High findings are R-0803, R-0804, R-0806 and R-0807, all F273's rather than this
  feature's, per DECISION F272 D12.
