# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared. T001 and T002 are DONE.

## Current Step

ROUND 32 opens T003. It rules the inheritance question T003 owes before any command dies —
which live command inherits a bounded-cycles run and a single-pass run — against the shipped
catalog by import, and records it as DECISION F275 D18. It then lands the one half of the
classic runner that no production caller reaches: `run_agent_loop` in
`packages/orchestration/agent_loop.py`, its three private helpers, the tests that exist only
to drive it, and the architecture page's description of it.

## Next Steps

1. Delete the `job.run` and `job.run-next` command surface under the D18 ruling: the catalog
   entries, the dispatch entries, the two `related=` tuples that would otherwise dangle, and
   the advertisements in the eight orchestration modules that print them.
2. Absorb the two handlers under the `job.resume` door, one owner and no copy, and register
   the surfaces D18 names as genuinely lost.
3. The flip DECISION F275 D17 sized, as the one declared-oversize commit AGENTS.md permits
   per feature, re-deriving the site set at its own base.
4. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   ledger rotation, the STATUS line and the PR.

## Risks

- The open set is 87 by distinct id at this round's base `9d1788fe`, over 102 registrations
  against 15 resolutions. This round registers none and resolves none, so it stays 87. Four
  are High — R-0803, R-0804, R-0806 and R-0807 — all F273's rather than this feature's, per
  DECISION F272 D12.
- Step 1 above turns two surviving `related=` tuples dangling the moment the commands die.
  The catalog integrity guard resolves every tuple against the live id set, so that repair
  is not optional and belongs in the same commit as the deletion.
