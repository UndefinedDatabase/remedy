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

Round 1 — claim F109 in the roadmap ledger, discharge the one closure
candidate F108 left open, and land T001a: the PURE per-session sent-hash
index `packages/orchestration/session_sent_index.py` with its unit tests
in `tests/orchestration/test_semantic_dedupe.py`. The module records,
queries, invalidates and serialises; it reads no file and calls no
provider.

## Next Steps

- T001b: persist the index into the job's evidence at the
  `on_call_finalized` seam, and invalidate a session's set whenever a
  resume attempt falls back to full context.
- T002: the composition hook — a segment whose hash the session already
  holds becomes a one-line marker, with non-resume calls bypassing the
  hook entirely, asserted by a byte-equality golden.
- T003: the measurement fixture, the disable flag, and the docs.
- The integration gate, then the closure sequence.

## Risks

- The index must never key on an empty session id: that key would become
  a bucket every sessionless call shares, which is the cross-session leak
  the feature exists to prevent. T001a pins it with a test.
- `R-0769` is registered this round, not fixed: its repair edits
  `README.md` and a docs test, neither of which F109 owns.
