# Plan — F312 The scope guard knows orders without file names

## Goal
The scope guard tells three kinds of order apart and refuses a plan only for the kind that drew a
fence; an order that names no file gives a plan, not a failure
(`docs/roadmap/features/T2_F312.md`). F312 owns findings R-1369 and R-1377 to R-1380.

## Current Step
Round 4 (session 1): book round 3, register R-1379 and R-1380, and repair both: an answered scope
question clears its job's two string fields to `""`, and each guard of `apply_scope_answer` gets
a test of its own.

## Next Steps
1. The closure's integration-gate round: the Built State, the consolidation pass, the self-use
   item, the one full suite.
2. The evidence job and the review package; then the closing round: the resolution lines, STATUS,
   README, the PR.

## Risks
- The records of the failed lab job were not read (the data root is not readable here); the
  finding's text and the code are the evidence (DECISION F312 D1).
- An answer that names no usable file changes nothing (DECISION F312 D4).
