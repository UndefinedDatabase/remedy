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

## The ordinary command and the default harness

```
remedy do "<order>" --apply
```

is the ordinary use: the reviewed change is applied to your files, nothing is committed, and the
walk reports what is now uncommitted. Add `--commit-auto` to commit.

- **Pi is the default execution harness**, with the local Ollama model `muse-glimmer:latest`, for
  the builder, the reviewer and the repair role. Pi supplies the agent loop and the file tools;
  Ollama is the model server and by itself is not a coding harness (a raw Ollama call returns
  text, so `--builder-provider ollama` is refused and names `pi`). Pi runs in Remedy's isolated
  job workspace; the reviewer's Pi has read-only tools. Explicit `--builder-provider claude-cli`
  (or `claude`, `fake`) remains an override. A missing Pi, Ollama or model stops the walk before any
  model call with the action to take, and never falls back to another provider.
- **A dirty working tree is the baseline, for the files the job may change.** At the start Remedy
  captures what you can see of the job's deliverable paths (bytes, executable bit, symlinks,
  deletions), seeds the job workspace from them and measures the proposed change from that state.
  Pi sees only that workspace: every other dirty path (an unrelated source file, an untracked
  `.env`, a private key) is left exactly where it is, is never copied into the workspace or onto a
  job branch, and shows in the report only as a name the run preserved. A sensitive path is also
  never hashed into a Git object. (An ordinary unrelated dirty file is still hashed into the
  repository's own object database by the human-change snapshot that keeps the target's last known
  state under a Remedy checkpoint ref; it is on no job branch and in no evidence.) A sensitive path
  (environment files, credentials files, `.pem`, `.key`, `.p12`, `.pfx`, `.jks`, `.git`) is judged by
  its name alone, never by `.gitignore`; an order that names one as a target is refused before any
  worktree or model call. Nothing is stashed, reset, checked out or committed in your repository. A
  state it cannot represent exactly (unresolved merge conflicts, a submodule or nested repository,
  a very large dirty set) stops the walk before any step and names the cause.
- **Timeouts are ceilings.** An explicit timeout (flag, order file, persisted config) is never
  raised for Pi. The remaining job wall-clock budget and the job deadline cap one Pi call too, and
  the tightest ceiling wins; the call record keeps the configured value, the job ceiling and the
  effective value under `timeout`. Only when nobody set a timeout does Pi get its longer default of
  900 seconds, because its agent loop takes several tool turns.
- **Harness invocations and model turns are different counts.** One Pi process (a harness
  invocation, what the token ledger records as one call) runs several model turns. The text report
  and `--json` print both, for example `(1 harness invocation, 8 model turns)`; the turns are
  counted from Pi's own event stream, and a role without a Pi record says `model turns not
  reported`. A failed Pi invocation that produced no assistant message is one invocation and zero
  turns.
- **Concurrent edits still block.** If a file the job changed was edited, or HEAD moved, after
  the start state was captured, the apply stops with `target_changed_during_run`, names the paths
  and overwrites nothing.
- **`--commit-auto` commits only the files the job changed.** Other uncommitted files stay
  uncommitted and byte-identical, and the report names them. If the committed file already held
  your uncommitted edits, the report says so: the commit contains them too.
- Nothing is applied without `--apply` or a commit flag.

## Two lanes

An ordinary, bounded request needs nothing but the order:

```
remedy do "Add one concise project-description paragraph below the heading in README.md. Change no other files." --repo .
```

`remedy do` reads the order and the repository and picks a lane without asking a model. A
**bounded** order, one repository and exactly one file (named in the order, or the only file the
repository tracks) with one plain part, walks the bounded lane: a deterministic scan of a tiny
repository, the one-milestone plan, one job and one task for that file, and **no planning
provider call**. Only the builder and the reviewer are called, in Remedy's isolated workspace,
and the walk stops before apply. Anything else, several files, several projects, an order file or
`--force-mission`, or any order whose scope is not clearly one file, walks the **full lane**,
which plans milestones, jobs and tasks with the planner and keeps an approval boundary: on a
terminal Remedy shows the plan and asks whether to run it; with no terminal it stops and names
`--run-unattended`. `--run-unattended` runs a generated plan without asking and takes the
documented default for every open question; it never applies, commits, pushes, merges or
deploys, because the target repository only changes with `--apply` or a commit flag.
`--force-job` also selects the bounded lane. A planner that names a file the order did not ask
for is not believed: the walk keeps the deterministic plan of the order's own deliverables
(operator amendment amend1014-do-golden-path-now D1, D6).

## While it works

Unless `--json`, `remedy do` says what it is doing on stderr as it goes: each step before it
starts (with the provider of a step that calls one), a heartbeat at least every ten seconds
while a step stays blocked, and each step's end with its elapsed time. `remedy do` opens no
browser page: the old cockpit was deleted (operator amendment amend1015-face-migration). To
watch or read a job, start the serve supervisor with `remedy serve start` and read the job's
story with `remedy client story <job id>`, or through the public API at
`GET /api/v1/jobs/{job}/story`; the walk's `Next:` lines name both. `--json` keeps stdout one
document and stderr silent (D4, D5).

## The steps, in order

| Step | What it does |
|------|--------------|
| `init` | Registers the repository as a project if it is not one (or selects `--project`), and adds the ignore entries; writes no file into the repository. |
| `study` | Studies the repository once, and only when it holds a commit with a tracked file; skipped when already studied. A tiny repository of a bounded order is studied from facts alone. |
| `plan` | Finds the repository's one mission, creating it on the repository's first order, adds the order to it as a batch, writes the contract template forced by `--contract` or proposed from the order onto it, and plans it. |
| `shape` | Reads the shape from the plan — one job, or milestones — or from `--force-job` / `--force-mission`, and plans the jobs, each linked to the mission and to the milestone it serves: the one whose outline it came from, or the plan's only milestone. Its gate evaluates that milestone's planner criterion, and never holds the job on it (R-0977, 2026-09-19). |
| `run` | Runs the first job on the chosen builder and reviewer; in a walk of two or more jobs the rest wait until the job before them is applied and committed. Under a commit flag no job waits: each job but the last is run, applied and committed (or merged) before the next job's worktree is cut. |
| `apply` | Stops before apply and prints the apply command for each job that ran, unless `--apply` or a commit flag, which applies them; with a push, it then pushes the mission once. |

A step that stops or fails ends the walk; the steps after it are not called.

## Stop before apply

Without `--apply` the walk ends at `apply` with the repository untouched and a
`Next:` line per job that ran, of the form
`remedy job apply <job_id> --repo <repo> --approve`. With `--apply` each job that
ran is applied in run order, as `remedy job apply --approve` does, and the walk
fails at the first job that is not applied, naming it and why.

## Tokens and cost after a run

When the walk ends it prints one `Tokens <role>:` line per role, that is per kind of worker
(the builder writes the change, the reviewer checks it). Each line gives the input tokens (text
sent to the model), the output tokens (text the model wrote) and the cache-read tokens (input
the provider served from its cache), all read from the project's call ledger, the record of
every provider call. It also gives the harness invocations (how many times Remedy started the
worker program) and the model turns (how many times the model answered inside one invocation).
A figure no call reported says "not reported", never 0.

The `Cost:` line shows no dollar figure by default. It reads `Cost: not shown — tokens only (…)`
when a cost was measured, and `Cost: not reported by the provider` when none was. A project that
wants dollars sets this in its `.remedy/config.toml`:

```toml
[cockpit]
show_cost_usd = true
```

The key defaults to `false`. With it set, the `Cost:` line shows the measured
dollar figure. The `--json` output always carries `cost.cost_usd`, because it is for programs,
not people (operator amendment amend1015).

## --plan-only and --step-by-step

- `--plan-only` ends the walk after `shape`: `run` reports stopped, no job is
  run, and a `remedy job run <job_id>` line is printed per planned job.
- `--step-by-step` halts after every step that did work, and inside `run`
  before each job: it prints what happened and what comes next, and reads one
  line. Enter continues; `q` or end of input stops the walk and asks every job
  of the walk to stop.

## --rehearse

`--rehearse` plans the order exactly as `remedy do` does and stops where
`--plan-only` stops: `run` reports stopped with a detail that begins
`--rehearse: no job was run and nothing was written to the repository`. No
builder or reviewer is built, nothing is applied, and the repository is not
touched. A job whose plan of tasks waits for approval keeps waiting: its
`Next:` lines name `remedy decision resolve <job_id> plan:approval --reason approve`
and then `remedy job run <job_id>`. `--rehearse` is refused before any step,
with exit 2 and the error `invalid_argument`, when it is given with `--run-unattended`,
`--apply`, `--commit`, `--commit-auto`, `--commit-with-history` or `--push`
(DECISION F055 D1).

### What a rehearsal records

For every job it plans, a rehearsal writes `rehearsal.json` and its readable
summary `rehearsal.md` into the job's own evidence folder, and the `run`
step's detail names each summary. The summary says what the planning cost,
as the job's prompt trace records it and without a dollar figure that was
never measured; what each task would cost, as a band from the shared
estimator or "not available"; the plan's risks and normalization; every
check of the job's definition of done and which were not compiled; and which
files of the plan the run could write and which the fences would block, or
that the plan declared no scope. The job keeps the repository's commit at
the rehearsal (DECISION F055 D2).

### Running a rehearsed plan for real

A rehearsed job is an ordinary planned job. To run it, answer its approval
with `remedy decision resolve <job_id> plan:approval --reason approve` and
then run `remedy job run <job_id>`; neither plans the job again. When the
repository's commit has moved since the rehearsal, both commands print a
warning that the plan may be stale and go on; the person decides. `remedy job
run` refuses a job whose plan of tasks still waits for approval
(`plan_awaiting_approval`, exit 3) or was rejected (`plan_rejected`, exit 3).
While a rehearsed job waits, `remedy status` shows `(rehearsed)` after its
name (DECISION F055 D3).

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
- `--builder-provider` — `pi` (the default), claude, claude-cli or fake; `ollama` is refused
- `--reviewer-provider` — `pi` (the default), claude, claude-cli, fake or ollama
- `--builder-model`, `--reviewer-model` — model for the role on every task `do` runs
- `--planner-model` — model for every planner call of the plan and shape steps
- `--planner-provider` — which service makes those planner calls: `ollama`
  or `claude-cli`; a name that is neither exits 2 before any step. Omitted,
  the configured `planner` role answers, and its default is `ollama`
  (operator amendment amend0920-selfuse-real, DECISION D1). The planner the
  walk actually used is the one its prompt traces and the mission plan
  record name.
- `--run-unattended` — run a generated plan of tasks without interactive confirmation; every open question takes its documented default; never implies `--apply`, a commit or a push
- `--no-ui` — deprecated and inert: the old cockpit was deleted, so it opens nothing; still
  accepted so existing scripts keep working
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
  held only by a blocking contract criterion that is `unmet` — a planner
  criterion the repository's test suite does not pass is one; each one still
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
and reason of one next action; the repair loop that built its results with it
was deleted by F273 (R-0923), so no production module imports it now. The check that a `remedy <group> <subcommand> ...`
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
