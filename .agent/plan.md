# Plan — F280 CLI vocabulary v2, part two

Branch: feature/f280-cli-vocabulary-v2-part-two, cut from `main` at
`9f1b6d250e68fb5ee3a2dd39d0a8ffef3eef0792`, the merge commit of pull request 251.

## Goal

Finish what F261 could not reach: the catalog `apps/cli/command_catalog.py` equals DECISION
amend0905-vocab D4 apart from the words D4 gives F268, F269 and F273, and T001's remaining
Acceptance lines hold, per `docs/roadmap/features/T2_F280.md` (T002 moved whole to F281 by
DECISION amend0917-throughput D4).

## Current Step

ROUND 23 books round 22's independently-reviewed PASS (Gate: F280 R22, one prose slip declared
— the reviewer's own stale byte count, nothing on disk affected) and marks `Done: R-0951`. Every
closure precondition now holds: 2 (R18), 3 (R22), 4 (R20), 6 (R21), and 1 (every step PASS,
R-0951 resolved, the standing Highs named). This OPENS the closure sequence
(STATUS_closure_protocol.md): the evidence job is round 24's own work.

## Next Steps

1. Round 24: the evidence job (`packages.orchestration.job_evidence.
   create_manual_completion_bundle`, `review_feature_id="f280"`, `base_commit` the fork point
   `9f1b6d250e68fb5ee3a2dd39d0a8ffef3eef0792`) — its own round, given the algorithm's five named
   packaging pitfalls (STATUS_closure_protocol.md step 1).
2. Round 25: the review zip (`scripts/make_review_zip.sh`), fresh, from a clean tree at the
   evidence job's head.
3. Round 26: the STATUS `[x]` line, README sync, `scripts/self_use_queue.json`'s SU-016
   `consumed_by=F280` in one commit, the ledger rotation
   (`scripts/rotate_live_review.py`), then the PR — not merged this session.
4. `job attach-repo`/`job permit`/`mission contract`/`job contract` wait for F269
   (DECISION amend0917-throughput D2) — not this feature's to close.

## Risks

- 147 findings registered by distinct id, 15 resolved (14 plus R-0951), 132 open. High:
  R-0803, R-0804, R-0807, none this feature's — named in the closure paragraph, not resolved.
- R-0899 (owned F273), R-0937 (owned F273), R-0938 (owned F280, nothing to fix), R-0941 and
  R-0950 (owned F273) — unchanged; re-assigned to F273 in the closure commit per
  amend0911-feedback rule A.
- The evidence job's `base_commit` MUST be the fork point, never a post-merge `merge-base`
  (STATUS_closure_protocol.md step 1(e), the F260 R22 BLOCKED_EVIDENCE lesson) — this branch has
  merged nothing in, so `rev-list --ancestry-path` and plain `rev-list` should already coincide,
  checked directly before authoring round 24's block.
