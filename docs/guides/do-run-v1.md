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
| `run` | Runs the first job on the chosen builder and reviewer; in a walk of two or more jobs the rest wait until the job before them is applied and committed. Under a commit flag no job waits: each job but the last is run, applied and committed (or merged) before the next job's worktree is cut. |
| `ui` | Opens the cockpit for the job that ran as a detached process, unless `--no-ui`. |
| `apply` | Stops before apply and prints the apply command for each job that ran, unless `--apply` or a commit flag, which applies them; with a push, it then pushes the mission once. |

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
cost, landed, push, next
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
- `landed` holds one `{job_id, sha, branch}` per commit or merge a commit flag
  landed, in job order; `[]` without one.
- `push` is the mission's one push — `{pushed, sha, remote, ref, error, source,
  open_blocking_criteria}`, `remote` being the remote's name, never its URL — or
  `null` when the walk asked none.
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
- `--commit "<message>"`, `--commit-auto`, `--commit-with-history` — the commit
  flags (DECISION F270 D4): each implies `--apply` and is passed to every job's
  `remedy job apply --approve`. `--commit` and `--commit-auto` land one commit of
  exactly the job's copied files on your current branch, as you;
  `--commit-with-history` merges the job's per-task commits with `--no-ff`. In a
  mission of several jobs, `--commit`'s line gains ` (job <k> of <n>)` and
  `--commit-auto` writes each first line from the job's title first, then the
  mission's goal. Only one may be given, and none with `--plan-only`
- `--push` — only with a commit flag. Push is a mission-level act: `do` never
  passes it to a job's apply, and pushes the last commit it landed ONCE, after
  the last job, to the branch's configured upstream, never forced. A push is
  held only by a blocking contract criterion that is `unmet`; each one still
  `open`, which no check has evaluated yet, is named in the output and in
  `push`. In a walk of one job an `unmet` criterion refuses before anything is
  applied; in a walk of several the commits land and the push is refused. A
  refused or failed push leaves every commit where it landed and exits 1

## Refused before any step

A lone `--push`, two commit flags, an empty or multi-line `--commit` message, a
commit flag with `--plan-only`, and — with a commit flag — a dirty tree, a
detached `HEAD` or the target's own merge, rebase, cherry-pick or revert in
progress, and — with a push — a branch with no upstream (the sentence names the
`git push --set-upstream` command that sets one) each exit 2 with "Nothing was
run." before the first step, so a long run is never spent on a commit or a push
that cannot happen.

## Remedy never commits by itself

Remedy never commits on your branch without a commit flag. `--apply` alone
copies files and commits nothing, and a walk that stops keeps what it had
committed and pushes nothing. The config key `apply.push_after_mission` makes a
run with a commit flag push exactly as `--push` would; set without a commit flag,
`do` commits and pushes nothing and says so in one sentence on stderr, so
`--json` stays clean.

## Next-line commands

`DoRunNextAction` in `packages/orchestration/do_run.py` is the label, command
and reason of one next action, which `packages/orchestration/repair_loop.py`
builds its results with. The check that a `remedy <group> <subcommand> ...`
command names a real `<group>.<subcommand>` entry of the command catalog is the
test helper `names_catalog_command` in `tests/orchestration/catalog_commands.py`
(R-0903).

## Source Files

- `packages/orchestration/do_sequence.py` — the steps, `DO_SEQUENCE` and the walker
- `apps/cli/commands/do_cmd.py` — CLI wiring and the output
- `packages/orchestration/do_run.py` — `DoRunNextAction`
- `tests/cli/test_do_sequence_cli.py`, `tests/cli/test_do_flags.py` — the sequence through the CLI
- `tests/orchestration/test_do_run.py` — the Next-line validator and the `do.run` catalog metadata

## See also

- [do-continue-v1](do-continue-v1.md) — the one apply+test+proof cycle F261 round 21 deleted.
