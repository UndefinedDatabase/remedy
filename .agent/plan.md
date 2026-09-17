# Plan — F280 CLI vocabulary v2, part two

Branch: feature/f280-cli-vocabulary-v2-part-two, cut from `main` at
`9f1b6d250e68fb5ee3a2dd39d0a8ffef3eef0792`, the merge commit of pull request 251.

## Goal

Finish what F261 could not reach: the catalog `apps/cli/command_catalog.py` equals DECISION
amend0905-vocab D4 apart from the words D4 gives F268, F269 and F273, and T001's remaining
Acceptance lines hold, per `docs/roadmap/features/T2_F280.md` (T002 moved whole to F281 by
DECISION amend0917-throughput D4).

## Current Step

ROUND 22 books round 21's independently-reviewed PASS (Gate: F280 R21, R-0951 registered — an
undisclosed second self-use job the round's own evidence never named, substance unaffected),
lands R-0951's fix (a disclosure file naming both jobs, marked `Landed: R-0951`), and discharges
closure precondition 3: `run_integrity_checks()` confirmed PASS (vacuously, per the already-open
R-0648) with no relevant untracked files.

## Next Steps

1. Round 23 books round 22's verdict and marks `Done: R-0951` (the reviewer's own text,
   replacing the worker's `Landed:` line).
2. Once every precondition holds: the evidence job, the review zip and the STATUS line
   (STATUS_closure_protocol.md algorithm steps 1-4), each its own round.
3. `job attach-repo`/`job permit`/`mission contract`/`job contract` wait for F269
   (DECISION amend0917-throughput D2) — not this feature's to close.

## Risks

- 147 findings registered by distinct id (146 plus R-0951), 14 resolved, 133 open. High:
  R-0803, R-0804, R-0807, none this feature's.
- R-0899 (owned F273), R-0937 (owned F273), R-0938 (owned F280, nothing to fix), R-0941 and
  R-0950 (owned F273) — unchanged.
- Precondition 3's own check is known-vacuous for the `high_blockers_open` clause (R-0648, open,
  unowned by this feature): `remedy integrity check --json` reports PASS regardless of the three
  standing High findings, exactly as it did for every closure since the ledger took its current
  form (F261 R25, F272, F275).
