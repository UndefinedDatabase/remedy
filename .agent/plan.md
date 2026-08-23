# Plan — F022 Live cost ticker

Branch: feature/f022-live-cost-ticker, cut from `main` at `c34ef32b`, the merge
commit of pull request #211. `.agent/live_review.md` is the source of truth for
the open set, the round map and the finding-id ceiling.

## Goal
Money is visible while it burns, honestly: the MetricsBar's COST metric renders
from budget tick events {spent, limit, basis} — bar fill against the limit, a
'~' prefix plus tooltip whenever the basis is estimated, warn colour at ≥85% —
and the final figure reconciles with the ledger at terminal. DONE when the
ticker tracks a fixture stream exactly, basis changes flip the prefix and
tooltip live, the warn threshold triggers per tokens, limitless jobs render the
spent-only variant with no fake denominator, and the terminal reconciliation
displays the ledger figure with any delta labelled.

## Current Step
R19 closes F022. It records the R18 verdict, flips the STATUS line to `[x]`
with the evidence job, package and SHA-256 that R18 produced, syncs the README
capability list in that same commit, writes this closure's one candidate to
`.agent/candidates.md`, and opens the pull request without merging it.

## Next Steps
1. The next session's Open PR Gate merges this pull request before any new
   feature is claimed, which is the operator's manual-review window.
2. That session's FIRST reviewed round registers or rules the candidate this
   round records and empties `.agent/candidates.md` in the same round.

## Risks
- The closure PR is created but NOT merged by the round that makes it. Merging
  it here would close the operator's only review window.
- This round's own verdict has no on-disk gate entry by construction (§4 item
  13). It lives in `.agent/handoff.md` and in the pull request, and no repair
  round is opened for that gap.
- Open F022 findings: R-0672 and R-0625 want their next-DECISION and
  next-numeral clauses honoured; R-0431, R-0413 and R-0533 are recorded and
  already paid for; R-0674, R-0675 and R-0676 are registered and repaired by
  none, their subjects being landed append-only text; and R-0445 is a standing
  defect of `docs/agents/integration_gate.md`, routed by the finding itself.
- The two High findings carried forward, R-0495 and R-0574, are inherited from
  the already-closed F085 and F086 and are documented risks, not F022 defects.
- R-0403 is open and this package shows it: `.remedy-wt/` scratch is a large
  share of every review zip built on this machine. It routes to a paydown
  branch and is not an F022 defect.
