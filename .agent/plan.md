# Plan — F114 Cost preview per command

Branch: feature/f114-cost-preview-per-command, cut from `main` after
pull request 234 was merged at the Open PR Gate.

## Goal

Expensive actions stop starting silently: commands that will spend real
money show an upfront estimate band with its basis and require
confirmation above a configured threshold in attended mode; unattended
runs rely on budgets, not prompts (docs/roadmap/features/T3_F114.md).

## Current Step

Round 15 books round 14's PASS verdict (RECORD14 - Built State
authored, precondition 4 satisfied) and ends SESSION 3 here, per
amend0827 rule 6's own 4-5-round default (this session ran 5: rounds
10-14). Pure bookkeeping, permitted only inside the closure sequence
(amend0827 rule 1's exception). No code changes.

## Next Steps

- SESSION 4 opens with `remedy integrity check --json` (precondition
  3, not yet run).
- Then the closure commit itself: evidence job, fresh review zip,
  STATUS line, README sync, `scripts/self_use_queue.json`'s
  `consumed_by=F114` edit, the PR (STATUS_closure_protocol.md
  algorithm) - likely its own session or two, per F112's own
  precedent (rounds 20/21/22/29/30/31).
- Preconditions 4 and 6 are SATISFIED; precondition 1 (every step
  PASS) and precondition 2 (integration gate clean, round 11) both
  hold; precondition 5 (clean tree, pushed) holds now.

## Risks

- None new this round. The closure commit is the highest-stakes
  remaining work (STATUS/README edits, a real PR) and deserves a
  fresh session's full context rather than a tired continuation.