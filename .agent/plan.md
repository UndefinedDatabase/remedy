# Plan — F259 Vocabulary & concept model v1

Branch: feature/f259-vocabulary, cut from `main` at 25961794. Rounds 1 to 5
PASSED the reviewer's gate; the round-5 verdict is booked in
`.agent/live_review.md` by round 6's own C2, which is where a verdict lands
under operator amendment amend0827-process-diet rule 1.

## Goal

Write `docs/system/vocabulary.md` as the BINDING vocabulary page: the DECISION
amend0905-vocab D1 table, the do-not-confuse table, the Mermaid concept diagram,
and D2–D10 and F259 D1/D2 as dated DECISION paragraphs. Pin the page with
`tests/docs/test_vocabulary.py` in planned mode against the shipped
`apps/cli/command_catalog.py`, put the same Mermaid block into `README.md`, and
register the page in `docs/README.md`. Explicitly no other code: F259 decides
words, F260 and F261 spend them.

## Current Step

Round 6 is T004, the last build round — the diagram into `README.md` under the
one-sentence description, byte-equal to the page's; the page registered in the
Quick-Find and System tables of `docs/README.md`; and the test extended with the
pin that keeps the two diagram copies equal, proved red by mutating README alone.

## Next Steps

- Run the integration gate per docs/agents/integration_gate.md: the full suite,
  a regression there is a normal repair round.
- Run the closure sequence per docs/roadmap/STATUS_closure_protocol.md: the
  evidence job, a FRESH review zip, the ledger rotation, the reviewer-authored
  STATUS line committed last, and the pull request — which is NOT merged in this
  session but at the next feature's Open PR Gate.

## Risks

- The Mermaid block now exists in three files. The new pin covers README against
  the page, and an existing test covers the page against the feature file, so
  every pair is pinned; a fourth copy would need a fourth pin.
- `README.md`'s `Accepted in Tier N so far:` blocks are scanned for feature ids
  and an unaccepted id there is what R-0797 was. This round inserts far above
  them, adds no id token, and gates the tokens themselves rather than only the
  test's direction.
