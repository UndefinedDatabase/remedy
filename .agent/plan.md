# Plan — F259 Vocabulary & concept model v1

Branch: feature/f259-vocabulary, cut from `main` at 25961794. Rounds 1 to 7
PASSED the reviewer's gate, the last of them the INTEGRATION GATE: the full
suite is green on the branch and at the merge base, with zero branch-only and
zero base-only failures. The round-7 verdict is booked by round 8's own C2.

## Goal

`docs/system/vocabulary.md` is the BINDING vocabulary page: the DECISION
amend0905-vocab D1 table, the do-not-confuse table, the Mermaid concept diagram,
the per-word meaning table, and D2–D10 plus F259 D1/D2 as dated DECISION
paragraphs. `tests/docs/test_vocabulary.py` pins it in planned mode against the
shipped `apps/cli/command_catalog.py`; the same diagram stands in `README.md`,
byte-equal and pinned; the page is registered in `docs/README.md`. No other
code: F259 decides words, F260 and F261 spend them.

## Current Step

Round 8 is CLOSURE PART 1, the content half: the feature file gains its Built
State and loses its registration-only banner; the §3 checklist takes its one
mandated consolidation pass, merging item 32 into item 16 and retiring the
number rather than renumbering, because the append-only review record
cross-references these items by number; the self-use queue is replenished and
its item is run to the approval gate; and the integration-gate verdict is booked.

## Next Steps

- CLOSURE PART 2: the ledger rotation as its own commit; the evidence job; the
  FRESH review zip, whose failure would be a closure blocker; the STATUS `[x]`
  line and the README capability sync in ONE commit with the self-use
  `consumed_by` edit; then the pull request, which is NOT merged in this session
  but at the next feature's Open PR Gate.

## Risks

- The self-use run is a real job execution. If it raises, that is reported and
  the reviewer decides what it means; it is never hidden and never retried into
  silence.
- The consolidation edits the document that governs the reviewer's own work. Its
  gate therefore measures every surviving item's digest, so a merge cannot
  quietly alter a rule it was only supposed to move.
