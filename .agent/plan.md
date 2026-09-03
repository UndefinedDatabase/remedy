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

Round 11, session 3. Book round 10's PASS, register `R-0773` and `R-0774`,
and fix both. `R-0773` is three docstring passages in `pingpong_loop.py`
that still call F109's config plumbing absent after round 10 landed it.
`R-0774` is the prompt TRACE describing the abandoned resumed composition
on a resume fallback rather than the full-content call that actually
reached the provider; the fix appends a second trace in each role's
fallback branch, so one trace exists per real provider invocation.

## Next Steps

- Surface the deduped names as a first-class `deduped_segment_names` field
  on `PromptTraceEntry`, derived from `composed_prompt.deduped_names` at
  the same seam `segment_manifest` already uses. The manifest ROW KEYS
  STAY CLOSED: `token_ledger.py`'s `call_segments` table mirrors them
  column for column, so widening a row is a token-ledger change.
- The measurement fixture on a resumed fixture chain with the savings
  recorded, plus the docs (T003).
- The integration gate, then the closure sequence.

## Risks

- A suite that no round gate names can go red without anyone seeing it.
  That is what `R-0772` was. Every block from here names the suites its
  change set can REACH, not only the ones it expects to move.
- `R-0769` is registered, not fixed: its repair edits `README.md` and a
  docs test, neither of which F109 owns.
