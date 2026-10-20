# Plan — F312 The scope guard knows orders without file names

## Goal
The scope guard tells three kinds of order apart and refuses a plan only for the kind that drew a
fence; an order that names no file gives a plan, not a failure
(`docs/roadmap/features/T2_F312.md`). F312 owns findings R-1369, R-1377 and R-1378.

## Current Step
Round 3 (session 1): book round 2 and R-1378, the DECISION F312 D3 addendum and DECISION F312
D4, the answer path (`scope_question.apply_scope_answer`, called by
`escalation.answer_task_decision`), the question job's prompt traces (R-1378), and their tests.

## Next Steps
1. The closure's integration-gate round: the one full suite, the Built State, the staging
   reclaim, the evidence job and the review package.
2. The closing round: R-1369's, R-1377's and R-1378's resolution lines, STATUS, README, the PR.

## Risks
- The records of the failed lab job were not read (the data root is not readable here); the
  finding's text and the code are the evidence (DECISION F312 D1).
- An answer that names no usable file changes nothing (DECISION F312 D4).
