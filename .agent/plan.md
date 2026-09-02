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

Round 5, the last of session 1 — book round 4's PASS verdict, correct a
false load-bearing clause in `R-0770` and resolve that finding, and land
T002a: the pure dedupe DECISION in
`packages/orchestration/session_sent_index.py` —
`DEDUPE_MIN_SEGMENT_CHARS`, `should_dedupe_segment` and
`dedupe_marker_for_segment`. No prompt is rewritten yet and the loop is
not touched.

## Next Steps

- T002b: the composition hook in `packages/orchestration/pingpong_loop.py`
  that calls the decision, replaces a deduped segment's text with its
  marker while leaving rank and order untouched, and bypasses non-resume
  calls entirely under a byte-equality golden.
- T002c: record the deduped segments in the manifest so evidence shows
  what the model did NOT receive again, and plumb the config kill switch.
- T003: the measurement fixture and the docs.
- The integration gate, then the closure sequence.

## Risks

- The parse-retry and post-mortem provider calls are still NOT wired into
  the index. That records strictly less than was sent, which errs in the
  safe direction; T002b must not assume the index is complete.
- `R-0769` is registered, not fixed: its repair edits `README.md` and a
  docs test, neither of which F109 owns.
