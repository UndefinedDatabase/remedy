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

Round 18, session 4. CLOSURE PREPARATION. Give the feature file the
BUILT STATE section closure precondition 4 requires; book round 17's
PASS, which is the integration gate — branch 18937 passed and base 18799
passed, both exit 0, with ZERO branch-only failures; resolve `R-0782`;
and register and repair `R-0783`, the sixth and last site the
stale-prose sweep has found.

## Next Steps

- The self-use item closure precondition 6 requires: the queue holds no
  pending item, so `generate_and_append_if_empty` supplies one from the
  ledger, and it is planned, RUN to the normal approval gate, and its
  defects registered before the close.
- The closure sequence proper: evidence job, a FRESH review zip, the
  authored STATUS line with the README sync in the SAME commit, the PR.

## Risks

- Six findings on this branch have been one class: prose that was TRUE
  when written and was falsified by a later round. The closure
  consolidation should answer the class, not add a seventh id.
- Nothing dedupes in production: every concrete adapter returns
  `supports_resume = False`, so the mechanism is suite-only today.
  `docs/system/semantic-dedupe-v1.md` states this plainly.
- The open finding set is a SET DIFFERENCE, not a subtraction: two ids
  carry two `Done:` lines each. That is `R-0778`.
- `R-0769` is registered, not fixed: its repair edits `README.md` and a
  docs test, neither of which F109 owns.
