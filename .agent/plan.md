# Plan — F312 The scope guard knows orders without file names

## Goal
The scope guard tells three kinds of order apart and refuses a plan only for the kind that drew a
fence; an order that names no file gives a plan, not a failure
(`docs/roadmap/features/T2_F312.md`). F312 owns findings R-1369 and R-1377.

## Current Step
Round 2 (session 1): book round 1 and R-1377, DECISION F312 D3, move `do_job_task_listing` to
`do_summary.py` (structure step), T002's second attempt and question in `scope_question.py`
with the walk stopping on it, R-1377's comment, and T003, the three lab orders as a fixture
walked through the real `milestones` shape.

## Next Steps
1. Round 3: DECISION F312 D4, what answering the question does (the named files become the
   job's tasks, and the job can run), with its tests.
2. The closure: the one full suite, the evidence, R-1369's and R-1377's resolution lines,
   STATUS, the PR.

## Risks
- The records of the failed lab job were not read (the data root is not readable here); the
  finding's text and the code are the evidence (DECISION F312 D1).
- `do_sequence.py` stands near the file limit and `plan_order_job` is listed: new logic goes to
  new modules.
