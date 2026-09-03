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

Round 21, session 4 — THE CLOSURE ROUND, and the last on this branch.
The authored STATUS line flips F109 to accepted with the README
capability sync in the SAME commit, `consumed_by` is set to `F109` on
`SU-005`, and the PR is created but NOT merged: it merges at the next
feature's start through the Open PR Gate, and that gap is the operator's
manual-review window.

## Next Steps

- The operator merges the PR, or the next feature's first session merges
  it at the Open PR Gate.
- Nothing else is owed by this branch.

## Risks

- Three findings from the self-use run are carried as documented Low
  risks, not repaired: `R-0784`, `R-0785` and `R-0786`. Two of them are
  F258's generator and one is F257's queue file, so none is F109's code.
- Nothing dedupes in production: every concrete adapter returns
  `supports_resume = False`, so the mechanism is suite-only today.
  `docs/system/semantic-dedupe-v1.md` states this as its first limit.
- The open finding set is a SET DIFFERENCE, not a subtraction: two ids
  carry two `Done:` lines each. That is `R-0778`.
