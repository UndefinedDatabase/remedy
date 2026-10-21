# Plan — F311 The insight: what runs now, what the worker does, why it hangs

## Goal
A client asks Remedy over HTTP what runs now, looks into one job's worker, and learns why it hangs
and what the operator can do, in closed words (`docs/roadmap/features/T12_F311.md`, DECISIONs
F311 D1 to D6).

## Current Step
Round 5 (session 1), the closure's integration-gate round: book round 4, register R-1389 and add
its test; F311's Built State; the checklist's consolidation pass; the closure's self-use item run
to its approval gate; and the feature's one full suite with its CPU cost.

## Next Steps
1. The evidence round: book round 5, resolve R-1389, register every self-use run defect, the
   evidence bundle and the review package.
2. The closing round: the STATUS line, the README, the self-use queue's `consumed_by`, the PR.

## Risks
- The integrity check fails on High findings F311 does not own (DECISION F310 D7, Q20).
- The self-use run spends real provider calls, within the `self_use` role's budget.
