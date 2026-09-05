# Plan — F259 Vocabulary & concept model v1

Branch: feature/f259-vocabulary, cut from `main` at 25961794 (the merge of pull
request #239). STATUS.md carried no `[~]` line at the cut and F259 is the first
`[ ]` line of the execution order DECISION amend0905-vocab D12 fixes.

## Goal

Write `docs/system/vocabulary.md` as the BINDING vocabulary page: the DECISION
amend0905-vocab D1 table — one row per word, with its meaning, its code
spelling today, its code spelling after F260/F261, its CLI spelling and what it
is NOT — plus the do-not-confuse table, the Mermaid concept diagram, and D2–D10
and F259 D1/D2 as dated DECISION paragraphs. Pin the page with
`tests/docs/test_vocabulary.py` in planned mode against the shipped
`apps/cli/command_catalog.py`, put the same Mermaid block into `README.md`, and
register the page in `docs/README.md`. Explicitly no other code: F259 decides
words, F260 and F261 spend them.

## Current Step

Round 1 — claim F259, cut the branch, re-point this file and `.agent/context.md`
at it, re-head `.agent/live_review.md`, book the reviewer's `Done: R-0797`, and
put the T001 source inventory on disk in `.agent/f259_inventory.md`: per D1
word, the spelling the code really uses today, read from the seven modules
T2_F259.md names and never from memory.

## Next Steps

- Write the page's D1 table from that inventory, one row per word.
- Add the do-not-confuse table, the Mermaid diagram and its short
  REMEDY_EINSTIEG-grade description; that completes T001.
- Write D2–D10 and F259 D1/D2 onto the page and check `T2_F263.md`'s heading
  for a working name (T002).
- Write `tests/docs/test_vocabulary.py` in planned mode with both of the red
  proofs T2_F259.md's T003 names.
- Put the Mermaid block into `README.md` and register the page in
  `docs/README.md` (T004).
- Run the integration gate, then the closure sequence.

## Risks

- The "code spelling today" column is worthless if it is guessed, which is why
  the inventory round comes before any page round.
- `README.md` has a guarded region: its `Accepted in Tier 2 so far:` block is
  scanned for feature ids, and putting an unaccepted id there is what R-0797
  was. The T004 round writes into that file and must not add an id token.
