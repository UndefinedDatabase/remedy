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

Round 8, session 2 — book round 7's PASS verdict, register `R-0771` and
fix it. A resume FALLBACK is not a resumed session, yet the loop re-sent
the prompt composed for the resumed one, markers and all, into a session
that never received the originals, and then recorded that deduped
manifest as what was sent. Both roles recompose at full content inside
the fallback branch and rebind the composed prompt, so the sent bytes,
the stored fallback prompt and the recorded evidence agree. The stale
"no caller exists yet" claim in the transform's docstring is retired in
the same commit.

## Next Steps

- Record the deduped segments in the manifest so evidence shows what the
  model did NOT receive again, and plumb the config kill switch through to
  `dedupe_enabled` (T002c).
- The measurement fixture on a resumed fixture chain, with the savings
  recorded, plus the docs (T003).
- The integration gate, then the closure sequence.

## Risks

- The parse-retry and post-mortem provider calls are still NOT wired into
  the index. That records strictly less than was sent, which errs in the
  safe direction; nothing may assume the index is complete.
- The prompt TRACE entry is written before the provider call, so on a
  fallback it describes the resumed composition rather than the full one
  actually sent. The repair above fixes the sent bytes and the recorded
  manifest; the trace ordering is untouched and belongs with T002c's
  evidence work.
- `R-0769` is registered, not fixed: its repair edits `README.md` and a
  docs test, neither of which F109 owns.
