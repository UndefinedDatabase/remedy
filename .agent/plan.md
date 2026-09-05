# Plan — F259 Vocabulary & concept model v1

Branch: feature/f259-vocabulary, cut from `main` at 25961794. Rounds 1 to 3
PASSED the reviewer's gate; the round-3 verdict is booked in
`.agent/live_review.md` by round 4's own C2, which is where a verdict lands
under operator amendment amend0827-process-diet rule 1.

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

Round 4 is T002 — the eleven rulings the page is the user-facing home of are
EXTRACTED from `.agent/decisions.md` and `docs/roadmap/features/T2_F259.md` and
appended to the page, unedited apart from a heading demotion, so the page cannot
disagree with the ledger. `T2_F263.md` needs no edit: its H1 already carries the
final name `absorb`, which the round measures rather than assumes.

## Next Steps

- Write `tests/docs/test_vocabulary.py` in planned mode, with the two red proofs
  T2_F259.md's T003 names: removing a binding word from the page must fail the
  page assertion, and flipping the mode constant to enforced against today's
  catalog must fail the synonym assertion.
- Put the Mermaid block into `README.md`, byte-equal to the page's, and register
  the page in `docs/README.md` (T004).
- Run the integration gate, then the closure sequence.

## Risks

- The Mermaid block will exist in three places once T004 lands; only a
  byte-comparison gate keeps them equal, and every round touching any of the
  three re-runs it.
- `README.md` has a guarded region: its `Accepted in Tier 2 so far:` block is
  scanned for feature ids, and putting an unaccepted id there is what R-0797
  was. The T004 round writes into that file and must add no id token.
