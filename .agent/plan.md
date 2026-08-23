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
R15 runs the integration gate over the whole suite, branch against base, and
records the R14 verdict with two recurrences. It builds nothing: T001, T002 and
T003 are all complete, and what remains unmeasured is whether this branch broke
anything outside its own scoped gates.

## Next Steps
1. R16 closure, per docs/roadmap/STATUS_closure_protocol.md — evidence job, a
   FRESH review zip, the authored STATUS line, and the PR created last.

## Risks
- A branch-only failure that reproduces serially and touches feature code is a
  BLOCKER, not a note. It ends R15 and buys its own reviewer-gated repair round
  before closure can start.
- The base worktree needs `apps/ui/node_modules` copied with its symlinks
  PRESERVED. Dereferencing them is what turned a parity restore into 7 base-only
  failures at F085 R23, and the copy call's default is the dereferencing one.
- Open F022 findings: R-0672 and R-0625 want their next-DECISION and
  next-numeral clauses honoured, and R-0672 gained a third instance at R14;
  R-0431, R-0413 and R-0533 are reviewer-block defects already recorded and
  already paid for.
- The two High findings carried forward, R-0495 and R-0574, are inherited from
  the already-closed F085 and F086 and are documented risks, not F022 defects.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
- R-0665 is open and this feature needs its route: every UI feature is told to
  record visual deviations in an `assumption_log` that does not exist. F022
  records them as DECISIONs in `.agent/decisions.md`, a route rather than a fix.
