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

Round 4 — book round 3's PASS verdict, register `R-0770` (the chain tests
proved the four loop call sites only as a GROUP, because one shared
`fake_session_id` collapsed them to a single observable), and repair it by
giving the chain tests two DISTINCT provider session ids so the Builder
and Reviewer record seams are each pinned alone. No production code
changes this round: the wiring is correct and the defect is in the tests
that failed to prove it.

## Next Steps

- T002: the composition hook — a segment whose hash the session already
  holds becomes a one-line marker, with non-resume calls bypassing the
  hook entirely, asserted by a byte-equality golden. T002 is also where
  the resume-fallback invalidation finally becomes observable, which is
  the half `R-0770` records as still unproven.
- T003: the measurement fixture, the disable flag, and the docs.
- The integration gate, then the closure sequence.

## Risks

- The parse-retry and post-mortem provider calls are still deliberately
  NOT wired into the index. That records strictly less than was sent,
  which errs in the safe direction; T002 must not assume completeness.
- `R-0769` is registered, not fixed: its repair edits `README.md` and a
  docs test, neither of which F109 owns.
