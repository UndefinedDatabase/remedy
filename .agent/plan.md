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

Round 20, session 4. CLOSURE, steps 1 and 2: the evidence job and a FRESH
review zip, plus the integrity check. Register the three findings the
round 19 self-use run exposed, all three as documented Low risks carried
into closure — two of them are F258's generator, not F109's code. The
STATUS line and the PR are round 21, because the closure commit must
FOLLOW a READY package.

## Next Steps

- Round 21, the closure commit: the authored STATUS line with the README
  capability sync in the SAME commit, `consumed_by` set to F109 on
  `SU-005`, the final `.agent/` state, then the PR. That round also runs
  the single consolidation pass on the checklist of
  docs/agents/planner_reviewer_prompt.md section 3.

## Risks

- A failing zip build is a CLOSURE BLOCKER, never something to work
  around; `PACKAGE_STATUS` is the reading, not the exit code.
- SEVEN findings on this branch were one class: prose TRUE when written
  and falsified by a later round. The consolidation should answer the
  class, not add an eighth id.
- Nothing dedupes in production: every concrete adapter returns
  `supports_resume = False`, so the mechanism is suite-only today.
- The open finding set is a SET DIFFERENCE, not a subtraction: two ids
  carry two `Done:` lines each. That is `R-0778`.
