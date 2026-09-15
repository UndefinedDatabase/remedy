# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 1 claims F261, cuts the branch, re-points this file and `.agent/context.md`, re-heads
`.agent/live_review.md`, books F275's round 110 verdict and the resolution of R-0889, registers
F275's closure candidate as R-0890, empties `.agent/candidates.md`, and records DECISION F261 D1,
which re-scopes T001 against the catalog measured at `7cdde89b`. Its code commit lands T001's
first rename, `do job-evidence` to `job evidence`, with a guard that the old id stays deleted.

## Next Steps

1. T001's renames `do job-promote` to `job apply` and `do job-run` to `job run`, one per
   commit, each adding its pair to the rename guard.
2. The deletion of `do job-flow` with its deletion paragraph, in two commits: the command and
   its tests, then the helpers only it used and the script that runs it.
3. The deletions of `do job-plan` and `do plan`, each with its deletion paragraph.
4. T002: `apply` replaces `promote`, and `job show --full` absorbs the read commands and
   `do job-report`.
5. T003, the prune to D4; then T004, descriptions, role labels, help wrapping and the tests.

## Risks

- 90 findings are open by distinct id; four are High, R-0803, R-0804, R-0806 and R-0807, all
  owned by F273. R-0805, R-0806 and R-0809 are named in this feature's Acceptance.
- The canary `tests/cli/test_golden_path.py` names none of T001's commands, so it cannot catch
  a T001 rename; `TestRenamedCommands` in `tests/test_command_catalog.py` and
  `tests/cli/test_advertised_commands.py` are the guards that can.
- A deleted `do` word falls through to `do run` and is read as a goal; DECISION F261 D1
  records why no refusal is added.
