# Plan — F280 CLI vocabulary v2, part two

Branch: feature/f280-cli-vocabulary-v2-part-two, cut from `main` at
`9f1b6d250e68fb5ee3a2dd39d0a8ffef3eef0792`, the merge commit of pull request 251.

## Goal

Finish what F261 could not reach: the catalog `apps/cli/command_catalog.py` equals DECISION
amend0905-vocab D4 apart from the words D4 gives F268, F269 and F273, and T001's remaining
Acceptance lines hold, per `docs/roadmap/features/T2_F280.md` (T002 moved whole to F281 by
DECISION amend0917-throughput D4).

## Current Step

ROUND 19 books round 18's PASS (the closure suite ran once, honestly, per amend0917-throughput
rule 1) and is this feature's FIRST closure repair round: five defect clusters the closure
suite surfaced (R-0945 through R-0949), all traced to earlier F280 rounds' own residue — a
stale gauntlet-manifest digest (round 14), a duplicate stale hint string and seven dead doc
advertisements (round 15's `propose` deletion), and two test files still naming the deleted
surface — are fixed in one round, dry-run-verified before authoring. R-0950 (four bad nodes
that reproduce in no isolated re-run) is registered but not repaired: investigated and found
unconnected to any F280 change.

## Next Steps

1. Round 20 re-verifies round 19's fix, resolves R-0945 through R-0949, and re-runs exactly
   the 51 previously-bad nodes (never the full suite — reserved for the closure round alone)
   to confirm the bad set shrank to R-0950's four with none newly bad, per the
   amend0917-throughput rule 2 shrinking rule (repair round 1 of at most 3).
2. Once confirmed: precondition 4 (Built State section), precondition 6 (self-use item) and
   precondition 3 (`remedy integrity check --json`) each their own round, then the evidence
   job, review zip and STATUS line (STATUS_closure_protocol.md algorithm), each its own round.
3. `job attach-repo`/`job permit`/`mission contract`/`job contract` wait for F269
   (DECISION amend0917-throughput D2) — not this feature's to close.

## Risks

- 146 findings registered by distinct id after this round (140 plus R-0945 through R-0950);
  9 resolved (unchanged this round — the five repaired findings resolve next round); 137 open.
  High: R-0803, R-0804, R-0807, none this feature's.
- R-0899 (owned F273), R-0937 (owned F273), R-0938 (owned F280, nothing to fix), R-0941 and
  now R-0950 (owned F273) — unchanged/new.
- R-0950's four flaky nodes stay in the closure suite's own committed transcript regardless of
  this round's fix (that file is never rewritten); the closure paragraph names them explicitly
  as investigated-and-unconnected, per amend0917-throughput rule 2's own honesty requirement.
