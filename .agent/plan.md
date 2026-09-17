# Plan — F280 CLI vocabulary v2, part two

Branch: feature/f280-cli-vocabulary-v2-part-two, cut from `main` at
`9f1b6d250e68fb5ee3a2dd39d0a8ffef3eef0792`, the merge commit of pull request 251.

## Goal

Finish what F261 could not reach: the catalog `apps/cli/command_catalog.py` equals DECISION
amend0905-vocab D4 apart from the words D4 gives F268, F269 and F273, and T001's remaining
Acceptance lines hold, per `docs/roadmap/features/T2_F280.md` (T002 moved whole to F281 by
DECISION amend0917-throughput D4).

## Current Step

ROUND 16 books round 15's independently-reviewed FAIL (Gate: F280 R15, two new findings:
R-0942 HIGH — a broken smoke script the deletion left unparseable — and R-0943 MEDIUM — an
uncaught crash in `decision.py`'s new `proposal:` approve branch) and repairs both in the
same round: delete the now-purposeless `scripts/remedy_runtime_cli_smoke.py`, remove its
Phase 1 from `scripts/remedy_backend_basis_smoke.py`, add a parse-guard test over every
`scripts/*.py` file, guard the `approve` action against a non-materializable task, and
restore the CLI round-trip test coverage round 15's own repair commit deleted.

## Next Steps

1. `job attach-repo`/`job permit` wait for F269's contract writer (DECISION amend0917-throughput
   D2) — not this feature's to close.
2. Once round 16 is independently reviewed PASS, book its verdict and R-0942/R-0943's
   resolution in round 17's C1.
3. Remaining Acceptance lines: `job budget <id> set`, `worker doctor`, `job run --tasks n` are
   already landed per prior rounds' Built State; confirm the catalog-vs-D4 diff at closure.
4. If T001 and the Acceptance list both hold after round 16's repair is confirmed, the next
   round is F280's closure sequence (integration gate, full suite, STATUS flip).

## Risks

- 139 findings open by distinct id after this round (137 plus R-0942, R-0943, both owned
  F280 and repaired this same round — resolution booked next round once re-reviewed); High:
  R-0803, R-0804, R-0807, R-0942, none but R-0942 this feature's own to close going forward.
- R-0899 (owned F273), R-0937 (owned F273), R-0938 (owned F280, nothing to fix), R-0941
  (owned F273) — unchanged.
- The two round-15 defects both trace to a gate whose own wording checked the SHAPE of a
  change (a grep for a string, a passing pytest count) rather than its TRUTH (does the file
  parse, does the branch handle every reachable state) — the parse-guard test this round adds
  is aimed at the first of those two classes; the second stays a standing reviewer discipline.
