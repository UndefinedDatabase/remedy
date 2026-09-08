# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared, with one module group as the atomic unit.

## Current Step

ROUND 4 books round 3's PASS verdict, registers R-0840 for the behaviour operator RULE 3
requires a finding for, and lands the SECOND carry-over: `mission report` stops being a facade
over the cluster module `dogfood_run` and becomes the carried report view over a job's
evidence, while the handler holding that name dies in the SAME commit, as DECISION F274 D2
rules. The map is deliberately UNCHANGED — `mission run` keeps the `dogfood_run` edge.

## Next Steps

1. The route-policy knobs checked against F110's config keys — R-0831 already records that none
   has an equivalent, so this is a finding update and not a rebuild. It rides with substantive
   work, because amend0827 rule 1 forbids a round that is only bookkeeping.
2. `.agent/f275_deletion_order.md`, derived from the deletion map in dependency order, leaf
   modules first, written BEFORE the first `git rm`.
3. The module groups, one commit each, in that order, under the four measurements
   amend0906-triage-throughput names for a deletion round, until the map holds zero cluster
   lines and every module F260's Design lists is gone from disk.
4. DECISION F260 D3, the deletion paragraph, with R-0832's fix clause binding it and R-0831 and
   R-0840 named among the ideas deleted rather than inherited.

## Risks

- 66 findings are open by distinct id once R-0840 lands, four of them High — R-0803, R-0804,
  R-0806 and R-0807 — all F273's rather than this feature's, per DECISION F272 D12. The
  integrity gate's `high_blockers_open` check is WRONG about them, which is R-0648 and open.
- `packages/orchestration/overnight_readiness.py` has zero consumer edges and is DELETABLE but
  not deleted; only its group commit removes it. A half-deleted module is the state operator
  RULE 1 forbids.
