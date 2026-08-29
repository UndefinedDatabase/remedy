# Plan — F040 Completion/return digest

Branch: feature/f040-completion-digest, cut from `main` at `f5b1e6c5`, the merge
commit of pull request 222. SESSION 1, opening the feature.

## Goal
Coming back is calm: a digest endpoint condenses state, cost with its basis, top
ownership entries, open decisions and ONE primary action into a hero card, shown
at job end or on the first UI open after absence — the "what happened while I
was gone" answer in one glance.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| the two F033 closure candidates | done | this round; no id spent |
| the F040 claim and the branch | done | this round |
| the seam inventory | done | this round, `.agent/f040_inventory.md` |
| T001 the endpoint composition | open | next round, ordered from the inventory |
| T002 the hero card and its triggers | open | |
| T003 CLI parity and the end-to-end | open | |

## Next Steps
1. This round claims F040, discharges the two candidates the F033 closure gate
   raised, and measures the four read paths the digest composes over.
2. The round after it orders T001 — the endpoint, the next-action rule-table
   import and the fixture goldens — from what the inventory measured.
3. The ownership seam is unbuilt: F035 is `[ ]` in the ledger. The inventory
   measures that directly, and the T001 order carries the decision that settles
   what the digest does about it.

## Risks
- R-0570 (Low) stays OPEN and is deliberately NOT repaired here. Its fix edits
  `README.md` and `tests/docs/test_docs_consistency.py`, neither of which F040
  owns, and AGENTS.md forbids mixing an unrelated fix into a feature branch.
- F040's Design section names an ownership source that does not exist on disk.
  Building T001 against it verbatim would compose over nothing.
