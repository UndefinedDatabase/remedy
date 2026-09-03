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

Round 19, session 4. CLOSURE PRECONDITION 6, the self-use item: the queue
holds no pending item, so the generator supplies one from the ledger and
it is planned and RUN to the normal approval gate under the product's own
provider — never promoted, never faked. Its defects are reported in the
handback for the reviewer to author as findings. Also book round 18's
PASS and resolve `R-0783`.

## Next Steps

- The closure sequence (docs/roadmap/STATUS_closure_protocol.md):
  register the self-use defects, the evidence job, a FRESH review zip,
  the authored STATUS line with the README sync in the SAME commit, the
  `consumed_by` edit, and the PR. That round also runs the single
  consolidation pass on the checklist of
  docs/agents/planner_reviewer_prompt.md section 3.

## Risks

- The self-use run uses a local model. If it cannot run, the precondition
  is BLOCKED and reported, never faked.
- SEVEN findings on this branch have been one class: prose TRUE when
  written and falsified by a later round. The consolidation should answer
  the class, not add an eighth id.
- Nothing dedupes in production: every concrete adapter returns
  `supports_resume = False`, so the mechanism is suite-only today.
- The open finding set is a SET DIFFERENCE, not a subtraction: two ids
  carry two `Done:` lines each. That is `R-0778`.
