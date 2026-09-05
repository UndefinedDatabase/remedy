# Plan — F259 Vocabulary & concept model v1

Branch: feature/f259-vocabulary, cut from `main` at 25961794. Round 1 PASSED the
reviewer's gate; its verdict is booked in `.agent/live_review.md` by round 2's
own C2, which is where a verdict lands under operator amendment
amend0827-process-diet rule 1.

## Goal

Write `docs/system/vocabulary.md` as the BINDING vocabulary page: the DECISION
amend0905-vocab D1 table — one row per word, with its meaning, its code spelling
today, its code spelling after F260/F261, its CLI spelling and what it is NOT —
plus the do-not-confuse table, the Mermaid concept diagram, and D2–D10 and F259
D1/D2 as dated DECISION paragraphs. Pin the page with
`tests/docs/test_vocabulary.py` in planned mode against the shipped
`apps/cli/command_catalog.py`, put the same Mermaid block into `README.md`, and
register the page in `docs/README.md`. Explicitly no other code: F259 decides
words, F260 and F261 spend them.

## Current Step

Round 2 — create `docs/system/vocabulary.md` with its binding preamble and the
D1 table, every "code spelling today" cell taken from `.agent/f259_inventory.md`
and from nothing else; book the round-1 verdict and two reviewer prose slips;
repair the blank line the round-1 preamble slice cost the review record.

## Next Steps

- Add the do-not-confuse table, the Mermaid diagram and its short
  REMEDY_EINSTIEG-grade description; that completes T001.
- Write D2–D10 and F259 D1/D2 onto the page and check `T2_F263.md`'s heading for
  a working name (T002).
- Write `tests/docs/test_vocabulary.py` in planned mode with both of the red
  proofs T2_F259.md's T003 names.
- Put the Mermaid block into `README.md` and register the page in
  `docs/README.md` (T004).
- Run the integration gate, then the closure sequence.

## Risks

- The page's middle two columns say different things ON PURPOSE — today's
  spelling and the spelling after F260/F261 — and a reader who conflates them
  will think the page is wrong. The preamble says so before the table.
- `README.md` has a guarded region: its `Accepted in Tier 2 so far:` block is
  scanned for feature ids, and putting an unaccepted id there is what R-0797
  was. Round 6 writes into that file and must add no id token.
