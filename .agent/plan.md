# Plan — F259 Vocabulary & concept model v1

Branch: feature/f259-vocabulary, cut from `main` at 25961794. Rounds 1 to 8
PASSED the reviewer's gate. Round 7 was the integration gate: the full suite is
green on the branch and at the merge base, with zero branch-only and zero
base-only failures. Round 8 was closure part 1.

## Goal

`docs/system/vocabulary.md` is the BINDING vocabulary page: the DECISION
amend0905-vocab D1 table, the do-not-confuse table, the Mermaid concept diagram,
the per-word meaning table, and D2–D10 plus F259 D1/D2 as dated DECISION
paragraphs. `tests/docs/test_vocabulary.py` pins it in planned mode against the
shipped `apps/cli/command_catalog.py`; the same diagram stands in `README.md`,
byte-equal and pinned; the page is registered in `docs/README.md`. No other
code: F259 decides words, F260 and F261 spend them.

## Current Step

Round 9 is CLOSURE PART 2, the evidence half: the round-8 verdict is booked
together with the three ledger obligations the closure creates — a new finding
for the contradiction round 8's own consolidation left in the frozen paragraph,
a recurrence under the existing R-0784 rather than a second id for the self-use
run's two defect strings, and the `Done: R-0418` that SU-010's acceptance owes;
then that contradiction is repaired, the ledger is rotated, and the evidence
bundle and the FRESH review zip are built from a clean tree.

## Next Steps

- CLOSURE PART 3: the reviewer authors the STATUS `[x]` line from this round's
  measured evidence job id, package name, SHA-256, package path and accepted
  HEAD; the worker applies it with the README capability sync and the self-use
  `consumed_by` edit in ONE commit, which is the last on the branch; then the
  pull request, which is NOT merged this session but at the next feature's Open
  PR Gate.

## Risks

- A failing zip build is a closure BLOCKER, not a nuisance: it is reported raw
  and the feature does not close until it is fixed.
- The rotation rewrites the ledger. It verifies every moved record by sha256
  before and after and refuses on mismatch; a refusal stops the rotation and is
  reported, never forced.
