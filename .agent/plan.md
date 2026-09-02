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

Round 2 — book round 1's PASS verdict and the reviewer's two prose slips
into the record, then land T001b-i: the finalized-call adapter in
`packages/orchestration/session_sent_index.py`. Three functions read a
provider output and decide which session it belongs to, whether it was
proven, and which session a resume fallback must forget. The module stays
pure and still imports nothing from the provider layer.

## Next Steps

- T001b-ii: wire those adapters into `packages/orchestration/pingpong_loop.py`
  at the builder and reviewer finalized-call seams and at both resume
  fallback sites, and persist the index into the job's evidence.
- T002: the composition hook — a segment whose hash the session already
  holds becomes a one-line marker, with non-resume calls bypassing the
  hook entirely, asserted by a byte-equality golden.
- T003: the measurement fixture, the disable flag, and the docs.
- The integration gate, then the closure sequence.

## Risks

- On the loop's fallback path the output object is REPLACED, so the
  failed session's id survives only in the loop's own variable. The
  adapter therefore takes it as an argument; a version reading only the
  output would invalidate nothing exactly when it matters.
- `R-0769` is registered, not fixed: its repair edits `README.md` and a
  docs test, neither of which F109 owns.
