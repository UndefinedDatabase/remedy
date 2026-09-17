# Plan — F280 CLI vocabulary v2, part two

Branch: feature/f280-cli-vocabulary-v2-part-two, cut from `main` at
`9f1b6d250e68fb5ee3a2dd39d0a8ffef3eef0792`, the merge commit of pull request 251.

## Goal

Finish what F261 could not reach: the catalog `apps/cli/command_catalog.py` equals DECISION
amend0905-vocab D4 apart from the words D4 gives F268, F269 and F273, and T001's remaining
Acceptance lines hold, per `docs/roadmap/features/T2_F280.md` (T002 moved whole to F281 by
DECISION amend0917-throughput D4).

## Current Step

ROUND 20 books round 19's independently-reviewed PASS (Gate: F280 R19, no new finding),
resolves R-0945 through R-0949 (the closure suite's five F280-owned defects, all confirmed
repaired), and writes `T2_F280.md`'s Built State section — closure precondition 4.

## Next Steps

1. Precondition 6: the self-use precondition (one pending `scripts/self_use_queue.json` item
   planned, run through `self_use_job`/`self_use_runner` to the normal approval gate, its
   findings registered, `consumed_by` set to F280) — its own round.
2. Precondition 3: `remedy integrity check --json` confirmed PASS — its own round or folded
   into the evidence-job round.
3. Once every precondition holds: the evidence job, the review zip and the STATUS line
   (STATUS_closure_protocol.md algorithm steps 1-4), each its own round.
4. `job attach-repo`/`job permit`/`mission contract`/`job contract` wait for F269
   (DECISION amend0917-throughput D2) — not this feature's to close.

## Risks

- 146 findings registered by distinct id, 14 resolved (9 plus R-0945 through R-0949), 132
  open. High: R-0803, R-0804, R-0807, none this feature's.
- R-0899 (owned F273), R-0937 (owned F273), R-0938 (owned F280, nothing to fix), R-0941 and
  R-0950 (owned F273) — unchanged.
- The self-use precondition (next round) runs a real job through the normal approval gate —
  the first round since R14 that is not a mechanical fix, so it gets its own round rather
  than riding with anything else.
