# Closure Candidates — carrier of record

> Written at closure per docs/roadmap/STATUS_closure_protocol.md
> ("Closure-candidate findings", disk-vehicle rule, operator ruling
> 2026-08-01). Read at Window-1 session bootstrap
> (docs/agents/planner_reviewer_prompt.md §1). One entry per
> candidate: description · source feature · date. Any entry present
> at feature-claim time is a block condition.

- A stop reason no code can ever emit. `STOP_REASONS` in
  `packages/orchestration/builder_bridge.py` declares
  `stale_diff_context`, and a repo-wide grep over every `.py` file
  finds that string in exactly one place: the frozenset itself. Nothing
  raises it, nothing tests it, nothing reads it. It predates this
  branch — it is present at the merge base 4e0b762e — so it is NOT an
  F111 defect and was deliberately not fixed here, because AGENTS.md
  bars mixing an unrelated fix into a feature branch. It is recorded
  because F111 is the feature that put a stale-diff CONCEPT into the
  codebase (`out_of_bounds` in `diff_repair.py` is how a stale diff
  actually becomes visible), so the next reader will reasonably expect
  the two to be connected and find that one of them is dead. Either
  wire it to the condition it names or delete it. · source F111 ·
  2026-08-13
