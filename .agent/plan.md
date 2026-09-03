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

Round 6, session 2 — book round 5's PASS verdict, then land the first
half of T002b: the pure composition transform `_dedupe_resumed_segments`
in `packages/orchestration/pingpong_loop.py`, which rewrites an
already-sent segment's TEXT to its marker while leaving that segment's
NAME, RANK and POSITION alone, and reports which names it replaced. No
call site is added: `compose_builder_prompt` and `compose_reviewer_prompt`
are not touched, so every prompt this repository composes stays
byte-identical to the one before this round.

## Next Steps

- Wire the transform into `compose_builder_prompt` and
  `compose_reviewer_prompt` behind a parameter that defaults to no dedupe,
  and pass the session's sent hashes at the two loop call sites only when
  a resume ref is actually set. The non-resume byte-equality golden is
  that round's first acceptance item.
- Record the deduped segments in the manifest so evidence shows what the
  model did NOT receive again, and plumb the config kill switch through
  to `enabled` (T002c).
- The measurement fixture and the docs (T003).
- The integration gate, then the closure sequence.

## Risks

- The parse-retry and post-mortem provider calls are still NOT wired into
  the index. That records strictly less than was sent, which errs in the
  safe direction; the wiring step must not assume the index is complete.
- `tests/orchestration/test_builder_prompt_golden.py` pins frozen renders
  and an exact ten-name manifest tuple. This round adds no call site, so
  it cannot reach them; the wiring step must gate on that suite.
- `R-0769` is registered, not fixed: its repair edits `README.md` and a
  docs test, neither of which F109 owns.
