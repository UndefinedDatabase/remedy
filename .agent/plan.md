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

Round 7, session 2 — book round 6's PASS verdict, then give the transform
`_dedupe_resumed_segments` its callers. `compose_builder_prompt` and
`compose_reviewer_prompt` each gain a keyword-only `dedupe_sent_hashes`
that defaults to None and bypasses entirely, plus a `dedupe_enabled` kill
switch; the two call sites in `run_pingpong` pass the session's sent
hashes only when a resume ref is actually set, so a non-resuming call has
no value it could dedupe with. The byte-equality golden for the
non-resume path is this round's first acceptance item.

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
- A deduped call records the MARKER's hash as sent, which is honest but
  not useful. T002c's manifest annotation is what makes the evidence
  readable; until then the marker hashes are harmless noise in the index.
- `R-0769` is registered, not fixed: its repair edits `README.md` and a
  docs test, neither of which F109 owns.
