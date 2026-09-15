# Plan — F261 CLI vocabulary v2 (rename & prune)

Branch: feature/f261-cli-vocabulary-v2, cut from `main` at
`7cdde89b5d0dc8ef1fb96980105870e956699873`, the merge commit of pull request 250.

## Goal

The catalog `apps/cli/command_catalog.py` equals DECISION amend0905-vocab D4: one name per
command, and every retired word deleted rather than aliased, per
`docs/roadmap/features/T2_F261.md`.

## Current Step

ROUND 2 books round 1's PASS, registers R-0891, and lands T001's next two renames as two
commits, each applying an edit table the round saves under `.agent/authored/`: `do job-promote`
to `job apply`, then `do job-run` to `job run`. The second commit also makes the F114 paragraph
of `README.md` and two catalog test names say `job resume`, the repair R-0891 records.

## Next Steps

1. The deletion of `do job-flow` with its deletion paragraph, in two commits: the command and
   its tests, then the helpers only it used and the script that runs it.
2. The deletions of `do job-plan` and `do plan`, each with its deletion paragraph.
3. T002: `apply` replaces `promote`, `do promote` joins `job apply`, and `job show --full`
   absorbs the read commands and `do job-report`.
4. T003, the prune to D4; then T004, descriptions, role labels, help wrapping and the tests.

## Risks

- 91 findings are open by distinct id once R-0891 is registered; four are High, R-0803,
  R-0804, R-0806 and R-0807, all owned by F273.
- The canary `tests/cli/test_golden_path.py` names none of T001's commands; the rename guard
  `TestRenamedCommands` in `tests/test_command_catalog.py` and
  `tests/cli/test_advertised_commands.py` are the guards that can catch a T001 rename.
- `job apply` and `job run` keep the flags their old commands had; D4's shorter flag lists,
  such as `run <id> [--tasks n]`, are separate flag renames.
