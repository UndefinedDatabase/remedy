# Plan — F109 Semantic dedupe

Branch: feature/f109-semantic-dedupe, cut from `main` at
`5e18a8536afa086b591b5a2e13009d68d6227432` (pull request 231 merged).

## Goal

Within a RESUMED session only, stop resending context the model has
already provably received: segments whose hash already went to that exact
session are replaced by short reference markers. Everywhere else full
content wins, because only a resumed session guarantees the model still
holds the prior content. The scope rule of the whole feature is "resumed
session only, proven sends only".

## Current Step

Round 12, session 3, a REPAIR round. Round 11 landed the correct fix for
`R-0774` on the Builder side and ended RED: two test selectors assumed one
Builder trace per role per round, and a second, honest trace falsified
them. Repair both by the property they meant to assert rather than the
position they used, book round 11's FAIL, register `R-0775` and `R-0776`,
and record that `R-0774`'s Reviewer half was false — that role already
recorded two traces before the round began. No production file changes.

## Next Steps

- Surface the deduped names as a first-class `deduped_segment_names` field
  on `PromptTraceEntry`, derived from `composed_prompt.deduped_names` at
  the same seam `segment_manifest` already uses. The manifest ROW KEYS
  STAY CLOSED: `token_ledger.py`'s `call_segments` table mirrors them
  column for column, so widening a row is a token-ledger change.
- The measurement fixture on a resumed fixture chain with the savings
  recorded, plus the docs (T003).
- The integration gate, then the closure sequence.

## Risks

- A positional selector over source text or over a trace list breaks
  silently whenever a correct change adds a site. `R-0775` is that class;
  prefer selecting by a declared property.
- `R-0769` is registered, not fixed: its repair edits `README.md` and a
  docs test, neither of which F109 owns.
