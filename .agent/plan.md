# Plan — Steps 5121-5140: Audit + Zip Truth Closure v1

## Goal
Fix 6 acceptance gaps (R-4308 through R-4313) to make final audit fail-closed,
evidence index truthful, stdout JSON shareable, and review zip complete.

## Current Step
Step 5121: Implement R-4308 (test fix), R-4309 (plan.md step range), R-4310 (fail-closed audit)

## Next Steps
- R-4311: Fix evidence index ordering
- R-4312: Separate local/shareable fields in stdout JSON
- R-4313: Review zip observability manifest
- Tests + verification
- Handoff

## Constraints
No auto-approval, no target mutation, no git ops, no UI mutation,
no external providers, no fake events, no hiding missing data, no MemPalace.
