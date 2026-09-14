# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared. T001 and T002 are DONE, the classic runner's whole
command surface is gone as of round 34, and the record flip landed in round 101.

## Current Step

ROUND 103 IS THE SECOND BRIDGE ROUND, per operator amendment amend0914-f275-sprint rule 3, and
it aims at every bad node round 102's transcript lists. It registers and repairs `R-0885`, the
job save the flip left non-atomic, and `R-0886`, the three readers that treat only `None` as
no project. It repairs the rest in production where the flip broke a contract — the budgets a
mission hands its record, the flight plan's file scope in the job context command, the entry
load of job fulfilment and the three job loads of the test execution service — and in the
runtime smoke harness and the tests where they still seed a classic record. The full suite
runs once; its bad-node set must be a strict subset of round 102's.

## Next Steps

1. MORE BRIDGE ROUNDS only if round 103's transcript does not read exit 0, each strictly
   shrinking the committed bad-node set with no node newly bad.
2. THE CLASSIC STORE: the classic `Job` and `Task` models and `packages/orchestration/storage.py`
   with their remaining readers, the which-store branches of the cockpit and its unreachable
   `_JobPlanAdapter`, the classic-store search inside `resolve_job_id`, and the guard tests
   that still pin the classic models.
3. THE CLOSURE SEQUENCE, with the integration gate's full-suite runs.

## Risks

- THE LIMIT IS LIFTED, not reached: amendment amend0911-f275-to-scope withdraws the 20
  sessions and 60 rounds without a replacement, so this feature closes only at full scope.
- THE BRANCH IS RED until a bridge round's transcript reads exit 0, and hosted CI on the branch
  is expected to be red in that span, per amend0914 rule 3.
- THE BRIDGE IS BOUNDED at eight rounds after the flip commit: a ninth writes an operator
  question and stops, and a round that adds a bad node is FAIL.
- A SERVER-START RACE: a command-channel test read its server's info file before the server
  wrote it once in the reviewer's full run after the flip and passed ten times alone.
- ONE ROUTED LOAD IS REACHED BY NO TEST until `R-0883` is repaired.
- The open set is 89 by distinct id at this round's base and 91 once `R-0885` and `R-0886` are
  registered, with `R-0809`, `R-0880`, `R-0883` and `R-0884` open. Four are High — R-0803,
  R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
