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

Round 3 — book round 2's PASS verdict and one reviewer prose slip, then
land T001b-ii: wire the finalized-call adapters into
`packages/orchestration/pingpong_loop.py` at the builder and reviewer
finalized-call seams and at both resume-fallback sites, carry the result
on `PingPongResult.session_sent_evidence`, and prove it with the first
chain tests in this feature that drive the real loop. Every loop edit is
additive; no existing statement moves.

## Next Steps

- T002: the composition hook — a segment whose hash the session already
  holds becomes a one-line marker, with non-resume calls bypassing the
  hook entirely, asserted by a byte-equality golden.
- T003: the measurement fixture, the disable flag, and the docs.
- The integration gate, then the closure sequence.

## Risks

- The loop is production code every job runs. The wiring is additive and
  the round gates the three suites that cover it, but a regression here
  would reach real runs rather than only this feature.
- The parse-retry and post-mortem provider calls are deliberately NOT
  wired. That records strictly less than was sent, which errs in the safe
  direction; T002 must not assume the index is complete.
- `R-0769` is registered, not fixed: its repair edits `README.md` and a
  docs test, neither of which F109 owns.
