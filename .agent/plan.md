# Plan — F311 The insight: what runs now, what the worker does, why it hangs

## Goal
A client asks Remedy over HTTP what runs now, looks into one job's worker, and learns why it hangs
and what the operator can do, in closed words (`docs/roadmap/features/T12_F311.md`). Accepted
PASS_WITH_RISKS on 2026-10-21.

## Current Step
Round 7 (session 1), the closing round: book round 6, DECISION F311 D7 (no rotation this closure),
accept F311 in STATUS with the README sync and SU-067's `consumed_by`, and open the pull request,
left unmerged.

## Next Steps
1. The next session: Phase 1 rule 1 (`.agent/STOP`), then the Open PR Gate merges F311's pull
   request; then Rule A5 proposes the next feature, F313.

## Risks
- The integrity check fails on High findings F311 does not own (DECISION F310 D7, Q20).
