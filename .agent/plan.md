# Plan — F280 CLI vocabulary v2, part two

Branch: feature/f280-cli-vocabulary-v2-part-two, cut from `main` at
`9f1b6d250e68fb5ee3a2dd39d0a8ffef3eef0792`, the merge commit of pull request 251.

## Goal

Finish what F261 could not reach: the catalog `apps/cli/command_catalog.py` equals DECISION
amend0905-vocab D4 apart from the words D4 gives F268, F269 and F273, and T001's remaining
Acceptance lines hold, per `docs/roadmap/features/T2_F280.md` (T002 moved whole to F281 by
DECISION amend0917-throughput D4).

## Current Step

ROUND 21 books round 20's independently-reviewed PASS (Gate: F280 R20, one prose slip declared,
no new finding) and discharges closure precondition 6: the self-use queue held no pending item,
so `generate_and_append_if_empty` appends the generator's tier-1 item (expected SU-016,
"Address ledger finding R-0445"), which is then run through `run_next_self_use_item` to the
normal approval gate under the configured real provider, in a throwaway worktree, never applied
and its `consumed_by` left empty for the closure commit.

## Next Steps

1. Round 22 books round 21's verdict, registers whatever `describe_self_use_run_defects` found
   against the open ledger (an empty tuple needs no id), and runs precondition 3
   (`remedy integrity check --json` confirmed PASS).
2. Once every precondition holds: the evidence job, the review zip and the STATUS line
   (STATUS_closure_protocol.md algorithm steps 1-4), each its own round.
3. `job attach-repo`/`job permit`/`mission contract`/`job contract` wait for F269
   (DECISION amend0917-throughput D2) — not this feature's to close.

## Risks

- 146 findings registered by distinct id, 14 resolved, 132 open. High: R-0803, R-0804, R-0807,
  none this feature's.
- R-0899 (owned F273), R-0937 (owned F273), R-0938 (owned F280, nothing to fix), R-0941 and
  R-0950 (owned F273) — unchanged.
- THE SELF-USE RUN NEEDS THE LOCAL MODEL SERVER and creates one `remedy/job-*` branch, per
  precedent (F261 R26, F275 R107): item R-0445 blocked at the approval gate both prior times,
  with a defect tuple of length 2.
