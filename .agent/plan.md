# Plan — F259 Vocabulary & concept model v1

Branch: feature/f259-vocabulary, cut from `main` at 25961794. Rounds 1 and 2
PASSED the reviewer's gate; the round-2 verdict is booked in
`.agent/live_review.md` by round 3's own C2, which is where a verdict lands
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

Round 3 completes T001 — the do-not-confuse table and the concept model are
appended to the page, the Mermaid block taken byte-for-byte from
`docs/roadmap/features/T2_F259.md` so that round 6's copy in `README.md` cannot
drift from it; the round-2 verdict and one reviewer prose slip are booked.

## Next Steps

- Write DECISION amend0905-vocab D2–D10 and F259 D1/D2 onto the page as dated
  paragraphs, and check `T2_F263.md`'s heading for a working name (T002).
- Write `tests/docs/test_vocabulary.py` in planned mode with both of the red
  proofs T2_F259.md's T003 names.
- Put the Mermaid block into `README.md` and register the page in
  `docs/README.md` (T004).
- Run the integration gate, then the closure sequence.

## Risks

- The Mermaid block now exists in two places and will exist in three; only a
  byte-comparison gate keeps them equal, and every round that touches either
  file re-runs it.
- `README.md` has a guarded region: its `Accepted in Tier 2 so far:` block is
  scanned for feature ids, and putting an unaccepted id there is what R-0797
  was. Round 6 writes into that file and must add no id token.
