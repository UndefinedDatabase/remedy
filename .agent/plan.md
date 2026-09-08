# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared, with one module group as the atomic unit.

## Current Step

ROUND 3 books round 2's PASS verdict into the record and then WIRES the carried readiness
module. `mission readiness` joins the catalog and `apps/cli/commands/mission_cmd.py`, the
cockpit's readiness section switches its import from the cluster module to the carried one,
and the deletion map loses the one line it recorded for
`packages.orchestration.overnight_readiness` in that same commit. That module ends the round
with ZERO surviving consumer edges, which is what makes it deletable.

## Next Steps

1. The `mission report` carry-over, which DECISION F274 D2 couples to the death of the current
   holder of `mission.report` in `apps/cli/commands/worker_facade_cmd.py`: the carry-over and
   that deletion are ONE commit.
2. The route-policy knobs checked against F110's config keys — R-0831 already records that none
   has an equivalent, so this is a finding update and not a rebuild.
3. `.agent/f275_deletion_order.md`, derived from the map in dependency order, leaf modules
   first, written BEFORE the first `git rm`.
4. The module groups, one commit each, under the four measurements
   amend0906-triage-throughput names for a deletion round.
5. DECISION F260 D3, the deletion paragraph, with R-0832's fix clause binding it and R-0831
   named among the ideas deleted rather than inherited.

## Risks

- 65 findings are open by distinct id, four of them High — R-0803, R-0804, R-0806 and R-0807 —
  all F273's rather than this feature's, per DECISION F272 D12. The integrity gate's
  `high_blockers_open` check is WRONG about them, which is R-0648 and itself open.
- `packages/orchestration/overnight_readiness.py` keeps its own tests and its own cluster
  consumers after this round. It is deletable, not deleted, and only its GROUP commit removes
  it — a half-deleted module is the state operator RULE 1 forbids.
