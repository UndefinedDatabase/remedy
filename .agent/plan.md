# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 3 books round 2's PASS and R-0891's resolution, registers R-0892 and R-0893, records
DECISION F261 D2, the deletion paragraph of `do job-flow`, and deletes that command in two
commits, each applying a table the round saves under `.agent/authored/`: first the command,
its transcript writer and its tests, with a guard that a deleted id stays deleted; then the
helpers only it used, `scripts/remedy_self_job_flow.sh`, and their tests. The worker runs the
full suite once after the second deletion.

## Next Steps

1. The deletions of `do job-plan` and `do plan`, each with its deletion paragraph and its id
   added to the deleted-command guard.
2. T002: `apply` replaces `promote`, `do promote` joins `job apply`, and `job show --full`
   absorbs the read commands and `do job-report`.
3. T003, the prune to D4; then T004, descriptions, role labels, help wrapping and the tests.

## Risks

- 92 findings are open by distinct id once this round's record lands; four are High, R-0803,
  R-0804, R-0806 and R-0807, all owned by F273.
- After the deletion no command writes the root artifacts that only `do job-flow` wrote and
  the review-package check requires of a provider-run package; R-0892 records it for F268,
  and the closure path, a manual completion bundle, is exempt from them.
- `packages/orchestration/agent_run_trace.py` keeps no production importer; R-0893 records it
  for F271.
