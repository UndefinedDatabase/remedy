# Plan — F014 Repair Round 1 (R-0118..R-0129)

## Goal
Fix 12 review findings from FAIL verdict on F014 Flight Plan.

## Checklist
- [x] STEP A — persist findings
- [x] STEP B — roll back closure (R-0118)
- [x] R-0121 — deprecation notes out of docstrings
- [x] R-0125 — schema tag mismatch
- [x] R-0122 — parse-failure path: postmortem, not fallback
- [x] R-0120 — fp: branch in decision resolve + fix next_actions
- [x] R-0119 — approval gate enforcement at execution entry points
- [x] R-0124 — --yes auto-approval audit
- [x] R-0129 — replan re-arms _approval
- [x] R-0126 — repo facts in plan prompt
- [ ] R-0123 — wire dead code (budgets/fences/write_plan_md/replan)
- [ ] R-0127 — rewrite smoke 12r as real CLI sequence
- [ ] R-0128 — complete handback
- [ ] STEP D — verification (all tests green)
- [ ] STEP E — golden-path probe
- [ ] STEP F — handoff

## Current Step
Committing R-0119..R-0126 batch. Next: R-0123, R-0127.
