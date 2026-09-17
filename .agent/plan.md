# Plan — F280 CLI vocabulary v2, part two

Branch: feature/f280-cli-vocabulary-v2-part-two, cut from `main` at
`9f1b6d250e68fb5ee3a2dd39d0a8ffef3eef0792`, the merge commit of pull request 251.

## Goal

Finish what F261 could not reach: the catalog `apps/cli/command_catalog.py` equals DECISION
amend0905-vocab D4 apart from the words D4 gives F268, F269 and F273, and T001's remaining
Acceptance lines hold, per `docs/roadmap/features/T2_F280.md` (T002 moved whole to F281 by
DECISION amend0917-throughput D4).

## Current Step

ROUND 18 books round 17's independently-reviewed PASS (Gate: F280 R17, no new finding — the
reviewer's own catalog-vs-D4 measurement now holds exactly) and runs the closure sequence's
integration-gate round per operator amendment amend0917-throughput rule 1: the full suite,
exactly once, by the worker, in the primary checkout, its transcript committed as
`.agent/authored/f280-closure-suite.txt`.

## Next Steps

1. If the closure suite is green: write T2_F280.md's Built State section (precondition 4),
   run the self-use precondition (F257/F258 — one pending queue item planned and run through
   the normal approval gate, its findings registered, `consumed_by` set to F280) and confirm
   `remedy integrity check --json` PASS (preconditions 3 and 6), each its own round.
2. If the closure suite is red: repair rounds follow the shrinking rule (amend0917-throughput
   rule 2) — each must strictly shrink the bad node set, at most three rounds, before an
   `xfail` mark and a follow-up feature registration.
3. Once every precondition holds: the evidence job, the review zip (STATUS_closure_protocol.md
   algorithm steps 1-2) and the STATUS line (step 4), each its own round — closure is not
   compressed into one.
4. `job attach-repo`/`job permit`/`mission contract`/`job contract` wait for F269
   (DECISION amend0917-throughput D2) — not this feature's to close.

## Risks

- 140 findings registered by distinct id, 9 resolved, 131 open. High: R-0803, R-0804,
  R-0807, none this feature's.
- R-0899 (owned F273), R-0937 (owned F273), R-0938 (owned F280, nothing to fix), R-0941
  (owned F273) — unchanged.
- The closure suite has not run yet this feature; any bad node it surfaces that pre-dates
  this branch (present on `main`'s merge base) is not this feature's to repair, per
  amend0917-throughput rule 2 — the repair round checks the merge-base's own hosted CI
  record before assuming ownership.
