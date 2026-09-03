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

Round 13, session 3. Surface the deduped names into the prompt TRACE:
`PromptTraceEntry` gains `deduped_segment_names`, derived from the composed
prompt at the same seam `segment_manifest` already uses, so the evidence
records what the model did NOT receive again. Round 12 made the trace
honest about WHICH call it describes, which is what this field needed to
inherit. Also book round 12's PASS, register `R-0777` and `R-0778`, and
repair the stale comment `R-0777` names.

## Next Steps

- The measurement fixture on a resumed fixture chain with the savings
  recorded, plus the docs (T003) — the last build slice of the feature.
- The integration gate, then the closure sequence.

## Risks

- A positional selector over source text or over a trace list breaks
  silently whenever a correct change adds a site. `R-0775` was that class;
  prefer selecting by a declared property.
- The open finding set is a SET DIFFERENCE, not a subtraction: two ids
  carry two `Done:` lines each, so line counts overstate what is resolved.
  That is `R-0778`.
- `R-0769` is registered, not fixed: its repair edits `README.md` and a
  docs test, neither of which F109 owns.
