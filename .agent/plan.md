# Plan — F259 Vocabulary & concept model v1

Branch: feature/f259-vocabulary, cut from `main` at 25961794. Rounds 1 to 4
PASSED the reviewer's gate; the round-4 verdict is booked in
`.agent/live_review.md` by round 5's own C2, which is where a verdict lands
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

Round 5 is T003 — `tests/docs/test_vocabulary.py` in planned mode, written to
spec against the imported catalog, with both red proofs run inside a disposable
worktree; the page gains the per-word meaning table the enforced mode reads; and
DECISION F259 D3 records why the enforced synonym scan omits `Worker:`, which is
not a catalog token and whose absence there no repository could ever violate.

## Next Steps

- Put the Mermaid block into `README.md`, byte-equal to the page's, and register
  the page in `docs/README.md` (T004).
- Run the integration gate per docs/agents/integration_gate.md.
- Run the closure sequence per docs/roadmap/STATUS_closure_protocol.md.

## Risks

- The Mermaid block exists in two places and T004 makes it three; only the
  byte-comparison test keeps them equal.
- `README.md` has a guarded region: its `Accepted in Tier 2 so far:` block is
  scanned for feature ids, and putting an unaccepted id there is what R-0797
  was. The T004 round writes into that file and must add no id token; its gates
  read the guarded block's tokens, not only the pin's direction.
- The enforced mode is written but not switched on. If F261 lands the renames
  and forgets the constant, test 6 turns red by itself — that is deliberate.
