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

Round 9, session 2 — a REPAIR round. Round 8 is booked FAIL: its
`R-0771` fix added a second, correct composition site and turned two
arity guards in `tests/orchestration/test_prompt_trace.py` red, which the
round's gate list never ran. `R-0771` resolves, `R-0772` is registered
for the red suite and repaired by rescoping both guards to the real shape
— one primary composition and one fallback recomposition. On top of that,
`ComposedPrompt` gains a `deduped_names` field so a composed prompt
reports which segments it replaced. The manifest ROW keys stay closed.

## Next Steps

- The config kill switch: a `run_pingpong` parameter forwarded to both
  compose calls as `dedupe_enabled`, proven by a resumed chain in which
  only the flag changed the outcome.
- Surface the deduped names into the prompt trace, answering the
  `schema_v` question on its own evidence. The manifest row keys stay
  closed: the `call_segments` table in `token_ledger.py` mirrors them
  column for column, so widening them is a token-ledger change.
- The measurement fixture on a resumed fixture chain, with the savings
  recorded, plus the docs (T003).
- The integration gate, then the closure sequence.

## Risks

- A suite that no round gate names can go red without anyone seeing it.
  Every block from here names the suites its change set can REACH, not
  only the ones it expects to move.
- The prompt TRACE entry is written before the provider call, so on a
  resume fallback it describes the abandoned resumed composition rather
  than the full one actually sent. The bytes sent and the recorded
  manifest were both repaired by `R-0771`; the trace ordering was not.
- `R-0769` is registered, not fixed: its repair edits `README.md` and a
  docs test, neither of which F109 owns.
