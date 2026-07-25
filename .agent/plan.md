# Plan — F014 Repair Round 1 (R-0118..R-0129)

## Goal
Fix 12 review findings from FAIL verdict on F014 Flight Plan.

## Checklist
- [x] STEP A — persist findings
- [ ] STEP B — roll back closure (R-0118)
- [ ] R-0121 — deprecation notes out of docstrings
- [ ] R-0125 — schema tag mismatch
- [ ] R-0122 — parse-failure path: postmortem, not fallback
- [ ] R-0120 — fp: branch in decision resolve + fix next_actions
- [ ] R-0119 — approval gate enforcement at execution entry points
- [ ] R-0124 — --yes auto-approval audit
- [ ] R-0123 + R-0129 — wire dead code (budgets/fences/write_plan_md/replan)
- [ ] R-0126 — repo facts in plan prompt
- [ ] R-0127 — rewrite smoke 12r as real CLI sequence
- [ ] STEP D — verification (all tests green)
- [ ] STEP E — golden-path probe
- [ ] STEP F — handoff

## Current Step
STEP A done. Starting STEP B.
