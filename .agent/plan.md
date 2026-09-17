# Plan — F280 CLI vocabulary v2, part two

Branch: feature/f280-cli-vocabulary-v2-part-two, cut from `main` at
`9f1b6d250e68fb5ee3a2dd39d0a8ffef3eef0792`, the merge commit of pull request 251.

## Goal

F280 closed at round 25 (STATUS `[x]`, accepted HEAD `102950eb`, DECISION F280 D11). Pull
request 253 is open; the Open PR Gate found hosted CI red on one node, which this round repairs.

## Current Step

ROUND 26, A POST-CLOSURE CI REPAIR ROUND under AGENTS.md's Open PR Gate exception
(amend0820-gate-autonomy — "Ended RED ... repairing that branch IS this session's work order").
C1 books round 25's PASS (RECORD26) and registers R-0953: round 19's own doc-prose fix for
R-0947 left `tests/orchestration/test_job_fulfillment.py::TestFulfilledDemoGuide::
test_guide_mentions_propose` asserting a string that fix made false, uncaught because round 19's
own gate never re-ran that file. C2 lands the fix and appends `Done: R-0953`. C3 is the handback.

## Next Steps

1. Once this round's push re-triggers CI and it reads green: Phase 1 rule 1 first,
   `.agent/STOP`; then the Open PR Gate merges pull request 253; then Rule A5 claims the next
   feature.

## Risks

- Round 25's STATUS/README/evidence-queue edits are independently verified against the
  closure commit's own content (RECORD26 above); the review package and evidence job the
  STATUS line names were not independently re-read this round, since
  `/home/decodeux/Repos/remedy-history/zips/` sits outside this session's sandboxed working
  directory — the reviewer relies on round 24's own byte-level package verification for that
  machinery's soundness.
- A commit after the closure commit deviates from Rule A4's normal "closure is the branch's
  last commit" rendering; it is justified here by the more specific, later-dated Open PR Gate
  CI-repair authority (amend0820-gate-autonomy), which explicitly allows commits on an open
  PR's branch to repair red CI. It does not reopen or alter the accepted HEAD, the STATUS line
  or any evidence artifact round 25 already produced.
