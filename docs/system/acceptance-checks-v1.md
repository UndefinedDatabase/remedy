# Acceptance checks v1: a project's own test command

> Status (F299, 2026-10-09): built. DECISIONs F299 D1 and D2 in `.agent/decisions.md` hold the
> rules this page states; the feature is `docs/roadmap/features/T7_F299.md`.

A mission's contract holds its acceptance criteria, and each criterion carries one check. When a
criterion names no test of its own, its check is the project's own test command: the check kind
`project_tests`. This page says where that command comes from, where it runs, and what a
criterion reads when the project has no test command at all.

## Where the command comes from
The check looks for the command when it runs, in the job's worktree, so a job that adds a
project's first tests is judged by them. It takes the first of these that exists:

1. The `command` list in the `[tests]` table of the project's own `.remedy/config.toml`, the file
   that also holds its `[runtime]` table:

       [tests]
       command = ["make", "test"]

   The command is a list of words, never a shell line. Its first word must be on the closed list
   of programs Remedy may start, `_EXECUTION_SAFE_EXECUTABLES` in
   `packages/orchestration/test_runner.py`; any other is refused as `executable_not_allowed`, and
   nothing runs. A `[tests]` table whose `command` is not a non-empty list of words is refused as
   `test_command_invalid`.
2. `npm test`, when the project's `package.json` has a `test` script other than the placeholder
   that `npm init` writes.
3. Python's test runner on the `tests` folder, when that folder exists:
   `python -m pytest -p no:cacheprovider tests -q`, under the project's own interpreter.

A project whose tests run any other way names its command in `.remedy/config.toml`.

## Where it runs
In the job's worktree, with the project's own environment. A job's worktree holds neither the
project's virtual environment nor its `node_modules`, because git ignores both, so the check
looks in the worktree first and then at the same place in the repository's own checkout:

- a virtual environment is a `.venv` or `venv` folder that holds `pyvenv.cfg` and `bin/python`;
  its `bin` folder goes first on the check's `PATH`, `VIRTUAL_ENV` names it, and its
  `bin/python` is the interpreter of the third source;
- a `node_modules/.bin` folder goes on `PATH` after it.

With neither, the check runs with Remedy's own environment and interpreter, as every check did
before. Remedy's own repository has no `.remedy/config.toml`, no `package.json` at its root and no
virtual environment folder, so its checks run the same command as before, under the same
interpreter.

## A project with no test command
When none of the three sources names a command, nothing runs, and the criterion reads
`unchecked`: no check ran, because the project names no test command. That state is neither met
nor unmet:

- the gate lists the check under `not_run`, never as red, so it holds no job;
- the mission's blockers leave the criterion out, so it holds neither `remedy mission achieve`
  nor the contract's remainder, and `remedy do run --json` does not list it under
  `unmet_blocking_criteria`;
- the approval card recommends `review`, never `apply` and never `hold`;
- a push is not refused, because a push is refused only for an `unmet` blocking criterion; the
  push names the criterion instead, under `push_unchecked_criteria` in `remedy job apply --json`
  and under `unchecked_blocking_criteria` in the `push` object of `remedy do run --json`.

A check that found a command and failed makes its criterion `unmet`, and so does a configured
command that cannot run: a project that names a command is judged by it.

## Where it is said
Each of these says "no check ran, because the project names no test command" for an `unchecked`
criterion or for its check: the `Contract:` line that `remedy do run` prints, the tables of
`remedy mission contract` and `remedy job contract`, the definition-of-done section of
`remedy job show --full`, the run report, the guided tour, and the push sentence of `remedy do run`
and `remedy job apply`. The approval card carries the state word `unchecked`.

## Tests
`tests/orchestration/test_project_tests.py` holds the order of the sources and the lookup of the
environment. `tests/orchestration/test_dod_runners.py` runs a Python project with a module that
only its own virtual environment holds, and a Node project through `npm test`.
`tests/cli/test_do_project_targets.py` drives `remedy do run` with the fake providers through to the
push on four scratch projects: a Python project with its own virtual environment, a Node project
whose tests run with `npm test`, a project with no tests, and a Python project whose test fails.
