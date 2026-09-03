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

Round 14, session 3. Measure the savings from the record itself: one PURE
function reads a run's own prompt-trace entries and reports what the run
did not resend, counting only what it can observe and NAMING the segments
whose full-content size was never recorded rather than guessing them. It
is deliberately not wired into the loop this round. Also book round 13's
PASS and register and repair `R-0779`, the module docstring that still
describes one real-loop class where there are now several.

## Next Steps

- The T003 DOCS: describe the feature's built state and register the doc
  in `docs/README.md` in the same commit.
- The integration gate (docs/agents/integration_gate.md), then the closure
  sequence.

## Risks

- The savings function is landed UNWIRED. Nothing reads it yet, so a later
  round must either wire it or say plainly why it stays a library.
- The open finding set is a SET DIFFERENCE, not a subtraction: two ids
  carry two `Done:` lines each. That is `R-0778`.
- `R-0769` is registered, not fixed: its repair edits `README.md` and a
  docs test, neither of which F109 owns.
