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

ROUND 102 IS THE FIRST BRIDGE ROUND, per operator amendment amend0914-f275-sprint rule 3. It
removes the lint rows and the guard and pin failures the flip left: `ruff`'s own fixer sorts
the import blocks and drops the unused imports in the files the flip changed, the three
routed-handler tests of `tests/test_data_paths.py` build a unified record with a classic-shaped
id, the job digest's golden normalizer reads the unified record's id, two guard tests about
the classic pydantic models import those models again, and the command door's import guard
rules `save_job_plan` where it ruled `save_job`. The full suite runs once and its bad-node set
must be a strict subset of round 101's committed transcript.

## Next Steps

1. MORE BRIDGE ROUNDS on the real tree, each strictly shrinking the committed bad-node set with
   no node newly bad: production code that hands a `JobPlan` a `JobBudgets` model where the
   record holds its serialized dict, and the `job resume` tests of `tests/cli/test_plan_approval.py`;
   what is left of the classic runner under `job resume`, whose kill-and-resume fixture still
   builds a classic job; the scoped job listings; and the single failures left in the job
   context command, the golden path, the runtime smokes, the repair loop, the proposed-task
   store, the cockpit adapter and the task runner — until a round's transcript reads exit 0.
2. THE CLASSIC STORE, with the which-store branches and adapters the flip leaves unreached.
3. THE CLOSURE SEQUENCE.

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
- The open set is 89 by distinct id, with `R-0809`, `R-0880`, `R-0883` and `R-0884` open.
  Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
