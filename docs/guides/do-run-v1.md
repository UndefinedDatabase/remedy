# remedy do — the one-command start

> How `remedy do "<order>"` plans and runs what you ask, and stops before apply.

## Overview

`remedy do "<order>"` walks one fixed sequence of steps, read as data from
`DO_SEQUENCE` in `packages/orchestration/do_sequence.py`. Every `remedy do`,
with or without the word `run`, walks it (DECISION F268 D16); there is no
second route under `do`.

```
remedy do "add a hello() function" --repo . --json
remedy do run "add a hello() function" --repo . --json
```

## The steps, in order

| Step | What it does |
|------|--------------|
| `init` | Registers the repository as a project if it is not one (or selects `--project`), and adds the ignore entries; writes no file into the repository. |
| `study` | Studies the repository once, and only when it holds a commit with a tracked file; skipped when already studied. |
| `plan` | Creates the mission record for the order, records the order, writes the contract template forced by `--contract` or proposed from the order onto it, and plans it. |
| `shape` | Reads the shape from the plan — one job, or milestones — or from `--force-job` / `--force-mission`, and plans the jobs, each linked to the mission. |
| `run` | Runs the first job on the chosen builder and reviewer; in a walk of two or more jobs the rest wait until the job before them is applied and committed. |
| `ui` | Opens the cockpit for the job that ran as a detached process, unless `--no-ui`. |
| `apply` | Stops before apply and prints the apply command for each job that ran, unless `--apply`, which applies them. |

A step that stops or fails ends the walk; the steps after it are not called.

## Stop before apply

Without `--apply` the walk ends at `apply` with the repository untouched and a
`Next:` line per job that ran, of the form
`remedy job apply <job_id> --repo <repo> --approve`. With `--apply` each job that
ran is applied in run order, as `remedy job apply --approve` does, and the walk
fails at the first job that is not applied, naming it and why.

## --plan-only and --step-by-step

- `--plan-only` ends the walk after `shape`: `run` reports stopped, no job is
  run, and a `remedy job run <job_id>` line is printed per planned job.
- `--step-by-step` halts after every step that did work, and inside `run`
  before each job: it prints what happened and what comes next, and reads one
  line. Enter continues; `q` or end of input stops the walk and asks every job
  of the walk to stop.

## JSON output

`--json` prints one object with these keys:

```
mission_id, job_ids, waiting_job_ids, contract, unmet_blocking_criteria,
stopped_before_apply, shape, shape_source, mission_plan_path, jobs, steps,
cost, next
```

- `contract` is the mission's contract body as its record holds it, or `null`
  when the mission has none (DECISION F269 D4 (6)).
- `unmet_blocking_criteria` lists the ids of the contract's blocking criteria
  not met after the walk, in contract order, or `[]` without a contract
  (DECISION F269 D6 (4)); the text output prints them on one `Contract:` line
  with each one's status.
- `jobs` lists every job's tasks with their deliverables.
- `steps` holds one `{name, status, detail}` per step the walk reached.
- `cost` carries the measured tokens per role and cost, read back from the ledger.
- `next` holds the `Next:` lines.

## Flags

Read from the `do.run` catalog entry in `apps/cli/command_catalog.py`:

- `--repo` — target repository path (default `.`)
- `--project` — select a registered project by slug or id instead of the repository's own
- `--json` — the JSON output above
- `--builder-provider`, `--reviewer-provider` — claude, claude-cli, fake or ollama
- `--builder-model`, `--reviewer-model` — model for the role on every task `do` runs
- `--planner-model` — model for every planner call of the plan and shape steps
- `--yes` — approve the job's plan of tasks unattended
- `--no-ui` — do not open the cockpit
- `--max-total-tokens`, `--max-provider-calls`, `--max-wall-clock-minutes`,
  `--max-cost-usd`, `--deadline` — the job's budgets
- `--no-llm` — heuristic intake, no LLM provider call
- `--force-job`, `--force-mission` — override the planner's shape; not together
- `--step-by-step`, `--plan-only` — above
- `--apply` — apply each job that ran instead of stopping before apply
- `--contract <name>` — force one of the templates under `docs/contracts/`
  (api-service, cli-tool, python-library, website) instead of the one proposed
  from the order; a name that is not a template exits 2 before any step
- `--commit`, `--commit-auto`, `--commit-with-history`, `--push` — not yet
  available: each exits 2 before any step, naming the feature that brings it
  (F270)

## Next-line commands

`validate_next_safe_action_command` in `packages/orchestration/do_run.py`
checks that a `remedy <group> <subcommand> ...` command names a real
`<group>.<subcommand>` entry of the command catalog; `DoRunNextAction` in the
same module is the label, command and reason of one next action, which
`packages/orchestration/repair_loop.py` builds its results with.

## Source Files

- `packages/orchestration/do_sequence.py` — the steps, `DO_SEQUENCE` and the walker
- `apps/cli/commands/do_cmd.py` — CLI wiring and the output
- `packages/orchestration/do_run.py` — `DoRunNextAction` and `validate_next_safe_action_command`
- `tests/cli/test_do_sequence_cli.py`, `tests/cli/test_do_flags.py` — the sequence through the CLI
- `tests/orchestration/test_do_run.py` — the Next-line validator and the `do.run` catalog metadata

## See also

- [do-continue-v1](do-continue-v1.md) — the one apply+test+proof cycle F261 round 21 deleted.
