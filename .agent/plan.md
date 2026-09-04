# Plan — F114 Cost preview per command

Branch: feature/f114-cost-preview-per-command, cut from `main` after
pull request 234 was merged at the Open PR Gate.

## Goal

Expensive actions stop starting silently: commands that will spend real
money show an upfront estimate band with its basis and require
confirmation above a configured threshold in attended mode; unattended
runs rely on budgets, not prompts (docs/roadmap/features/T3_F114.md).

## Current Step

Round 16 opens SESSION 4. It books round 15's PASS verdict (RECORD15 —
the session-ending handback itself, reviewed and reproduced
independently at session start) into the ledger, then runs closure
precondition 3 (`remedy integrity check --json`) for the first time
this feature. No code changes.

## Next Steps

- The closure commit itself: evidence job, fresh review zip, STATUS
  line, README sync, `scripts/self_use_queue.json`'s `consumed_by=F114`
  edit, the PR (STATUS_closure_protocol.md algorithm) — its own round
  or two, per F258's own precedent (rounds 9-11).
- Preconditions 1, 2, 4, 5 and 6 hold; precondition 3 is confirmed this
  round (see Done when).

## Risks

- None new this round. The closure commit remains the highest-stakes
  remaining work.