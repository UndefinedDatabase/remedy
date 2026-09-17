# Plan — F280 CLI vocabulary v2, part two

Branch: feature/f280-cli-vocabulary-v2-part-two, cut from `main` at
`9f1b6d250e68fb5ee3a2dd39d0a8ffef3eef0792`, the merge commit of pull request 251.

## Goal

Finish what F261 could not reach: the catalog `apps/cli/command_catalog.py` equals DECISION
amend0905-vocab D4 apart from the words D4 gives F268, F269 and F273, and T001's remaining
Acceptance lines hold, per `docs/roadmap/features/T2_F280.md` (T002 moved whole to F281 by
DECISION amend0917-throughput D4).

## Current Step

ROUND 17 books round 16's independently-reviewed PASS (Gate: F280 R16, no new finding) and
resolves R-0942/R-0943, then fixes the one gap the reviewer's own full catalog-vs-D4
measurement found: the `mission` group is advanced-only when DECISION amend0905-vocab D4
names it visible (R-0944), and widens `TestGroupDefIntegrity` to the full D4 partition so no
group's bucket can drift unnoticed again.

## Next Steps

1. `job attach-repo`/`job permit` wait for F269's contract writer (DECISION amend0917-throughput
   D2) — not this feature's to close; `mission contract`/`job contract` likewise F269's.
2. The reviewer's own measurement (round 17) confirms every other part of the catalog — the
   29-group set, the advanced and hidden buckets apart from `mission`, and every command under
   `do`, `job`, `run` and `worker` D4 spells out — already equals D4 exactly.
3. Once round 17 is independently reviewed PASS with no new finding, T001 and the Acceptance
   list both hold; the next round begins F280's closure sequence per
   `docs/roadmap/STATUS_closure_protocol.md` — the integration-gate round (full suite once),
   the self-use precondition, the evidence job and review zip, in that order, each its own
   round rather than compressed into one.
4. Remaining Acceptance lines (`job budget <id> set`, `worker doctor`, `job run --tasks n`)
   are already landed per prior rounds' Built State.

## Risks

- 140 findings registered by distinct id after this round (139 plus R-0944); 9 resolved
  (7 plus R-0942, R-0943); 131 open. High: R-0803, R-0804, R-0807, none this feature's.
- R-0899 (owned F273), R-0937 (owned F273), R-0938 (owned F280, nothing to fix), R-0941
  (owned F273) — unchanged.
- Before closure: the feature file's Built State section (currently absent) must be written,
  the self-use precondition (F257/F258) run, and `remedy integrity check --json` confirmed
  PASS — none of this round's own doing, all named here so the closure round does not
  discover them cold.
