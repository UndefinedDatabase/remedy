# Plan — F040 Completion/return digest

Branch: feature/f040-completion-digest, cut from `main` at `f5b1e6c5`, the merge
commit of pull request 222. SESSION 1, round 2.

## Goal
Coming back is calm: a digest endpoint condenses state, cost with its basis, top
ownership entries, open decisions and ONE primary action into a hero card, shown
at job end or on the first UI open after absence — the "what happened while I
was gone" answer in one glance.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| the two F033 closure candidates | done | round 1; no id spent |
| the F040 claim and the seam inventory | done | round 1, PASS |
| the three spec decisions D2, D3 and D4 | done | this round |
| the one-source urgency in Python and its pin | done | this round |
| R-0751, the stale rule-table comment | done | this round |
| T001 the endpoint composition | open | next round |
| T002 the hero card, triggers and the TS retirement | open | |
| T003 CLI parity and the end-to-end | open | |

## Next Steps
1. This round settles the three questions the inventory raised, amends the
   feature file where they change it, and lands `decision_urgency` in Python as
   the single home of the formula.
2. The round after it builds the digest composition module over
   `build_report_sources` and the inbox read path, with the four state fixtures.
3. The endpoint wiring and its goldens follow, then T002 and T003.

## Risks
- R-0570 (Low) stays OPEN and is not repaired here: its fix edits `README.md` and
  `tests/docs/test_docs_consistency.py`, which F040 does not own.
- Two homes for the urgency formula exist between this round and T002. They are
  pinned equal by a contract test rather than trusted, and D2 schedules the
  retirement of the TypeScript one.
