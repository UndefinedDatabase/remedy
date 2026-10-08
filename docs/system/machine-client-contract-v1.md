# Machine client contract v1

> Status (F295, 2026-10-07; F298, 2026-10-08): built. The binding list for a program that drives
> Remedy through its command line — Luna's runner first
> (`docs/roadmap/design/luna-control-plane-v1.md`, "Gate A" and "Gate B").
> `tests/cli/test_machine_client_contract.py` drives the path below end to end and fails when the
> tables of the path and that test name different things. `tests/cli/test_machine_client_paths.py`
> (F304) drives three more paths the same way: an apply merged with its history and pushed to an
> upstream, an order of two jobs carried to its end, and one order file started twice. The last
> section, "The interface", is generated from the code and names everything a client can rely
> on; the rest of the page is written by hand and walks through the path.

A machine client is a program that never sees a terminal. It writes an order file, starts
Remedy, reads one digest, answers the decisions a run raises, approves the apply and reads the
proof — through the command line's JSON answers alone, with no cockpit, no HTTP and no question
on stdin. The path has four steps: read, propose, approve, apply.

Every command below is run with `--json`. Its standard output is then exactly one JSON object.
A success carries `"ok": true` and `"schema_version": 1`; a refusal carries `"ok": false`,
`"schema_version": 1`, `error` (a fixed token) and `message` (a sentence for a person), and
exits non-zero.

## The order file

An order is a Markdown file whose path ends in `.md` and holds no whitespace. An optional header
sits between two `---` lines and names `project`, `contract`, `max-cost-usd` and any number of
`constraint` lines; the order text follows it. A flag given on the command line wins over the
header. An order that names a project, in its header or with `--project`, runs in that
project's registered repository wherever the client stands; an order that names none runs in
`--repo`, by default the current directory. A client registers such a repository once with
`remedy project register --repo <path> --json`, which answers the project's `project_id` and
`slug` and writes nothing that `git status` shows. This is the order file the gate test
writes:

```
---
max-cost-usd: 1
---
Add a line saying hello to README.md
```

Remedy refuses an order file before any step, with exit code 2: `order_file_not_found`,
`order_file_unreadable`, `order_file_empty`, `order_file_invalid_header`, and
`order_file_no_cost_cap` when neither the header nor `--max-cost-usd` sets a cost cap. An order
that names a project is refused before any step with `project_has_no_repo` and exit code 3
when the project has no registered repository, and with `repo_not_in_project` and exit code 2
when `--repo` names a repository that is not the project's. An order file that a mission which
has not ended already records — a mission that is neither achieved nor abandoned — is refused
before any step with `order_already_running` and exit code 2, and the refusal names that mission
under `mission_id`; `--new-mission` starts another mission for it instead. An order argument that
holds whitespace is planned as text, never read as a file.

## The path, step by step

1. **Propose.** `remedy do <order file> --json --no-ui --yes` plans the order and runs its first
   job with the builder and reviewer the client names, and stops before the apply. The gate test
   adds `--no-llm` and the fake providers, and a `--deadline` that has already passed, so the
   budget stops the job and raises one decision. A run that does not finish answers `ok` false
   with `error` `step_failed` and still carries `mission_id` and `job_ids`, and exits 1.
2. **Read.** `remedy status --json` carries the digest under `client`: every project with its
   missions, every job with its state, cost and evidence, every open decision, and the jobs that
   wait for their apply. Read it as often as once a minute. Each completed job also carries
   `approval_card`, what an operator approves its result on, read from the job's record alone:
   how many files its tasks changed and the first twenty of them by name, the test command the
   job ran with, and each task's title, reviewer's verdict and repair rounds, and whether its
   test ran and passed. Every other job's `approval_card` is null.
3. **Answer.** `remedy decision resolve <job> <decision> --reason <option> --json` answers a
   decision. A budget decision is answered `extend` with `--answer <limit>=<value>` for each
   raised limit, or `abandon`. After `extend`, `remedy job run <job> --json` runs the job on with
   the builder and reviewer it started with. An `extend` also answers `no` to the contract
   remainder decision the same budget stop raised, because the job runs on instead of a
   follow-up mission, and names it under `closed_decisions`. A run that ends `blocked`,
   `failed` or stopped by its budget answers `ok` false with `job_blocked`, `job_failed` or
   `job_stopped_by_budget`, still carries every key of the job's report, and exits 1; a run
   that completes, pauses at the operator's request or at `--tasks`, or stops at the operator's
   request answers as before.
4. **Approve and apply.** `remedy job apply <job> --approve --json` copies the reviewed result
   into the repository. Then `remedy change proof <job> --json` lists that apply under
   `job_applies`. An approved apply that did not land answers `ok` false with one token for
   its first cause — among them `target_dirty`, `target_detached_head`, `merge_conflict`,
   `blocked_paths`, `push_no_upstream` and `push_refused_by_contract`; the interface below
   lists them all — still carries every key of the apply's answer, and exits 1, or 3 when the
   job is absent or not ready to apply; flags that clash exit 2 with `invalid_argument` before
   the job is read. A preview, without `--approve` or with `--dry-run`, answers `ok` true and
   exits 0, whatever it found. A client that does not want a completed job's result declines
   it instead with `remedy job decline <job> --reason <text> --json`: nothing is applied, the
   job no longer waits for its apply, and `remedy job ownership <job>` names the decline as the
   operator's own act. A job that is not completed, or whose result already landed, is
   refused with exit 3. A job of an abandoned mission no longer waits for its apply either.

### Commands

| Command | Step |
|---|---|
| `remedy do` | propose: plan and run an order, stop before the apply |
| `remedy status` | read: the digest under `client` |
| `remedy decision resolve` | answer one decision |
| `remedy job run` | run an answered job on to its end |
| `remedy job apply` | apply a job's reviewed result, only with `--approve` |
| `remedy change proof` | read the proof of what the job changed and applied |

### Flags

| Flag | Command | Meaning |
|---|---|---|
| `--json` | every command | one JSON object on standard output |
| `--no-ui` | `remedy do` | do not open the cockpit |
| `--yes` | `remedy do` | approve the plan of tasks unattended; every open question takes its documented default |
| `--no-llm` | `remedy do` | plan without a model call (the gate test's choice) |
| `--builder-provider` | `remedy do` | the builder, here `fake` |
| `--reviewer-provider` | `remedy do` | the reviewer, here `fake` |
| `--deadline` | `remedy do` | the job's deadline, UTC, ISO 8601 |
| `--reason` | `remedy decision resolve` | the option chosen, here `extend` |
| `--answer` | `remedy decision resolve` | one raised limit, `<limit>=<value>`, repeatable |
| `--approve` | `remedy job apply` | the approval; without it nothing is applied |

### JSON keys

| Key | Where | Meaning |
|---|---|---|
| `ok` | every answer | true for a success, false for a refusal |
| `mission_id` | `remedy do`; digest missions and jobs | the mission the order started |
| `job_ids` | `remedy do`; digest missions | the jobs of that mission |
| `client` | `remedy status` | the digest for a machine client |
| `version` | digest | the digest's version, 1 |
| `projects` | digest | every registered project |
| `missions` | digest projects | each project's missions |
| `order_source_path` | digest missions | the order file a mission was started from |
| `jobs` | digest | every job |
| `job_id` | digest jobs and decisions; `remedy change proof` | the job |
| `state` | digest jobs | the job's state: `stopped`, `completed` and the others |
| `cost` | digest jobs | `value_usd` and its `basis`, measured, never guessed |
| `evidence` | digest jobs | the job's evidence references |
| `run_manifest_path` | digest job evidence | the run manifest the job's runs wrote |
| `waits_for_apply` | digest jobs | true while a completed job's result is not applied |
| `awaiting_apply` | digest | the jobs that wait for their apply |
| `decisions` | digest | every open decision of every job |
| `decision_id` | digest decisions; `remedy decision resolve` | what `remedy decision resolve` names |
| `type` | digest decisions | the kind of decision, `token_budget` for a budget stop |
| `options` | digest decisions | the answers it accepts, `extend` and `abandon` for a budget stop |
| `outcome` | `remedy decision resolve` | what the answer did, `extended` for an extend |
| `closed_decisions` | `remedy decision resolve` | the decisions an `extend` answered with it: the contract remainder decision of the same budget stop |
| `budgets` | `remedy decision resolve` | the job's limits after the answer, the order file's cap among them |
| `max_cost_usd` | `budgets` | the cost cap in USD |
| `next_command` | `remedy decision resolve` | the command that runs the job on |
| `status` | `remedy job apply`; proof `job_applies` | `applied` when the result landed |
| `files_applied` | `remedy job apply`; proof `job_applies` | the repository paths the apply wrote |
| `job_apply_id` | `remedy job apply`; proof `job_applies` | the apply's own id |
| `job_applies` | `remedy change proof` | every apply of the job, oldest first, never called verified |
| `overall_status` | `remedy change proof` | the verdict over the job's patch intents |

### Exit codes

| Code | Meaning |
|---|---|
| `0` | the command did what was asked |
| `1` | a refusal, or a run that did not finish; the JSON object says which |

## Decisions and the command that answers each

| Kind (`type`) | Answered by |
|---|---|
| `task_plan_approval` | `remedy decision resolve <job> plan:approval --reason approve` or `reject`, with `--answer <question>=<text>` for its bundled questions |
| `task_decision` | `remedy decision resolve <job> <decision> --reason <answer>` |
| `token_budget` | `remedy decision resolve <job> <decision> --reason extend --answer <limit>=<value>`, or `--reason abandon` |
| `proposal` | `remedy decision resolve <job> <decision> --reason approve`, `reject` or `defer` |
| `replan_proposal` | `remedy decision resolve <job> <decision> --reason replan_follow_up` or `accept_reduced_scope` |
| `stop_reason` | `remedy decision resolve <job> <decision>` |
| `patch_approval` | `remedy patch approve <job> <intent>` or `remedy patch reject <job> <intent>` |
| `test_failure`, `memory_review` | notices with no answer; `remedy decision resolve` refuses them as `decision_not_resolvable` |

A hunk decision is not raised by a run: a client chooses to decide over the hunks of a job's
diff. For a job `remedy do` ran, `remedy job evidence <job> --json` first exports the job's
evidence; then `remedy patch hunks <job> --json` reads the hunk ids and the decision recorded
for them, and `remedy patch approve-hunks <job> --approve-hunk <id> --reject-hunk <id>=<reason>
--json` records a decision.

## What Remedy never does on a machine order

- It never applies without `--approve`, and never commits or pushes without their own flags.
- It never starts an order file that carries no cost cap.
- It never asks a question on stdin when `--yes` is given: the builder's and the reviewer's
  child processes read end of file, and the gate test fails on any read of stdin.
- It never resumes a job its budget stopped until that budget decision is answered:
  `remedy job resume` refuses it with exit code 3 and `budget_decision_open`.

<!-- BEGIN GENERATED by render_client_interface_markdown() -->
## The interface

> GENERATED from `build_client_interface()` in `apps/cli/client_interface.py` by
> `render_client_interface_markdown()`. Do not edit this section by hand:
> `tests/cli/test_client_interface.py` fails whenever the interface and this section differ.
> Regenerate it from the repository root with
> `python3 -c "from apps.cli.client_interface import write_client_interface_page; write_client_interface_page()"`.

`remedy client interface --json` prints this interface as data, read from the code. Inside
one major version it only grows. Under a key, `*` stands for keys that are data, such as a
path, a job id or a job state. A key whose keys are not fixed is marked so, and a key that
repeats the object that holds it holds that object's keys again, to any depth.

Interface version: `1.1`.

### Envelope

Schema version: `1`.
Reserved keys: `schema_version`, `ok`.
Refusal keys: `error`, `message`.

### Exit codes of every command

| Code | Name | Meaning |
|---|---|---|
| `0` | `ok` | The command did what it was asked, including finding nothing to do or honouring a pending stop request. |
| `1` | `failed` | The command ran and did not do what was asked — a refusal, a failed operation, a red check, drift found; the general failure and the code of every refusal no narrower meaning claims. |
| `2` | `usage` | The invocation itself is wrong — an unknown command, or a missing, invalid, unrecognised or conflicting argument — and nothing was attempted. |
| `3` | `not_ready` | The invocation is well formed, but what it names is absent or not in a state the command can act on. |
| `4` | `environment` | The machine lacks a prerequisite the command cannot supply, such as a git repository. |

### Words

Job states: `pending`, `planned`, `running`, `paused`, `completed`, `failed`, `cancelled`, `blocked`, `stopped`.
Mission statuses: `active`, `paused`, `achieved`, `abandoned`.
Contract templates: `api-service`, `cli-tool`, `python-library`, `website`.
Budget kinds: `max_total_tokens`, `max_provider_calls`, `max_wall_clock_minutes`, `max_cost_usd`, `deadline`, `min_free_disk_bytes`.

### Operations

#### `remedy project register`

Command id: `project.register`.
Description: Register a repository as a project's repo, writing nothing its git status shows; a repo already registered answers its project.

| Argument | Option | Required | Takes a value | Repeatable | Help |
|---|---|---|---|---|---|
| `--repo` | yes | yes | yes | no | Path to the repository |
| `--json` | yes | no | no | no | Output as JSON |

Exit codes: `0`, `1`, `2`, `4`.
Refusal tokens: `not_a_git_repo`.
Answer keys: `created`, `project_id`, `repo_path`, `slug`.
Keys under the answer keys: none.

#### `remedy do run`

Command id: `do.run`.
Description: Plan and run what you ask: study the repo, plan a mission of jobs and their tasks, run the first job, and stop before apply unless --apply.

| Argument | Option | Required | Takes a value | Repeatable | Help |
|---|---|---|---|---|---|
| `goal` | no | no | yes | no | What you ask, as text, or one path ending in .md to an order file |
| `--repo` | yes | no | yes | no | Path to target repository (default: the registered repository of the project --project or the order file names, else the current directory) |
| `--project` | yes | no | yes | no | Select a registered project by slug or id instead of the repository's own |
| `--json` | yes | no | no | no | Output JSON |
| `--builder-provider` | yes | no | yes | no | Builder provider for `do`: claude, claude-cli, fake or ollama (default: the builder role config) |
| `--reviewer-provider` | yes | no | yes | no | Reviewer provider for `do`: claude, claude-cli, fake or ollama (default: the reviewer role config) |
| `--builder-model` | yes | no | yes | no | Model for the builder role on every task `do` runs (default: the builder role config) |
| `--reviewer-model` | yes | no | yes | no | Model for the reviewer role on every task `do` runs (default: the reviewer role config) |
| `--planner-model` | yes | no | yes | no | Model for every planner call of the plan and shape steps (default: the planner's configured model) |
| `--planner-provider` | yes | no | yes | no | Which service plans: ollama or claude-cli (default: the configured planner role) |
| `--yes` | yes | no | no | no | Approve the job's plan of tasks unattended: audited, every open question takes its documented default |
| `--no-ui` | yes | no | no | no | Do not open the cockpit |
| `--max-total-tokens` | yes | no | yes | no | Maximum total tokens for this job (F018 budget) |
| `--max-provider-calls` | yes | no | yes | no | Maximum provider calls for this job (F018 budget) |
| `--max-wall-clock-minutes` | yes | no | yes | no | Maximum wall-clock minutes for this job (F018 budget) |
| `--max-cost-usd` | yes | no | yes | no | Maximum cost in USD for this job (F104 budget) |
| `--deadline` | yes | no | yes | no | UTC deadline for this job as ISO 8601 string (F018 budget) |
| `--no-llm` | yes | no | no | no | Force heuristic intake (no LLM provider call) |
| `--force-job` | yes | no | no | no | One job for what you ask, its tasks under the mission, whatever shape the planner chose |
| `--force-mission` | yes | no | no | no | Two or more jobs under the mission, one per milestone outline or deliverable, whatever shape the planner chose |
| `--new-mission` | yes | no | no | no | Start a new mission for an order file that a mission which has not ended already records; without it such an order file is refused before any step, naming that mission |
| `--step-by-step` | yes | no | no | no | Halt after each step that did work: print what happened and what comes next; Enter continues, q stops |
| `--plan-only` | yes | no | no | no | Stop after the shape step: nothing is executed, and the output lists every deliverable |
| `--apply` | yes | no | no | no | Apply each job of the mission to the repository, one after another, as `remedy job apply --approve` does; stops at the first that is not applied |
| `--contract` | yes | no | yes | no | Force this contract template as the floor of the mission's acceptance criteria, instead of the one Remedy proposes: api-service, cli-tool, python-library or website |
| `--commit` | yes | no | yes | no | Implies --apply: apply each job as `remedy job apply --approve --commit` does, landing one commit of exactly its copied files on your current branch, as you, with this one line as its first line, followed by the job's number when the mission has several jobs; each job runs only after the one before it is committed. Refused before any step with --plan-only, another commit flag, a dirty tree or a detached HEAD |
| `--commit-auto` | yes | no | no | no | As --commit, with a first line Remedy writes from the job's title or the mission's goal |
| `--commit-with-history` | yes | no | no | no | Implies --apply: merge each job's commits, one per applied task step, onto your current branch with git merge --no-ff instead of copying, as `remedy job apply --approve --commit-with-history` does; each job runs only after the one before it is merged |
| `--push` | yes | no | no | no | With a commit flag only: push your branch to its configured upstream once, after the mission's last job, never forced; refused alone and, before any step, without an upstream; refused while any blocking criteria of the mission contract are unmet, naming those still open. The config key apply.push_after_mission does the same |

Exit codes: `0`, `1`, `2`, `3`.
Refusal tokens: `invalid_argument`, `invalid_budget`, `order_already_running`, `order_file_empty`, `order_file_invalid_header`, `order_file_no_cost_cap`, `order_file_not_found`, `order_file_unreadable`, `project_has_no_repo`, `repo_not_in_project`, `step_failed`, `unsupported_contract_template`, `unsupported_provider`.
Answer keys: `contract`, `cost`, `failed_step`, `job_ids`, `jobs`, `landed`, `mission_id`, `mission_plan_path`, `next`, `push`, `shape`, `shape_source`, `steps`, `stopped_before_apply`, `unmet_blocking_criteria`, `waiting_job_ids`.
Keys under the answer keys: see below.

- `contract`: `amendments`, `criteria`, `schema`, `template`
  - `amendments`: `acknowledged_in`, `applies_from`, `criteria`, `id`, `received_at`, `text`, `understood`
  - `criteria`: `blocking`, `check`, `evidence_ref`, `id`, `milestones`, `origin`, `status`, `text`
    - `check`: `acceptance_refs`, `blocking`, `description`, `id`, `kind`, `source`, `spec` (keys not fixed)
- `cost`: `cost_usd`, `job_ids`, `mirror_errors`, `mirror_failed_job_ids`, `roles`
  - `mirror_errors`: `*`
  - `roles`: `cache_read`, `calls`, `cost_usd`, `role`, `tokens_in`, `tokens_out`
- `jobs`: `job_id`, `tasks`
  - `tasks`: `deliverable`, `title`
- `landed`: `branch`, `job_id`, `sha`
- `push`: `error`, `open_blocking_criteria`, `pushed`, `ref`, `remote`, `sha`, `source`
- `steps`: `detail`, `name`, `status`

#### `remedy status run`

Command id: `status.run`.
Description: Show project status overview, across its repos and missions.

| Argument | Option | Required | Takes a value | Repeatable | Help |
|---|---|---|---|---|---|
| `--project` | yes | no | yes | no | Scope to a project's repo (slug or UUID) |
| `--all-projects` | yes | no | no | no | Show jobs from all projects |
| `--json` | yes | no | no | no | Output as JSON |

Exit codes: `0`, `1`, `2`.
Refusal tokens: none.
Answer keys: `client`, `decisions_open`, `degraded`, `jobs`, `project`, `runtime`, `runtime_warning`, `scope`, `skipped_files`, `stops_pending`.
Keys under the answer keys: see below.

- `client`: `awaiting_apply`, `decisions`, `degraded`, `jobs`, `projects`, `read_at`, `skipped_files`, `supervisor`, `version`
  - `decisions`: `age_seconds`, `clarifications`, `created_at`, `decision_id`, `default`, `job_id`, `options`, `project_id`, `question`, `severity`, `type`
    - `clarifications`: `default`, `id`, `question`
  - `jobs`: `approval_card`, `cost`, `evidence`, `job_id`, `mission_id`, `project_id`, `state`, `title`, `waits_for_apply`
    - `approval_card`: `changed_file_count`, `changed_files`, `tasks`, `test_command`
      - `tasks`: `repair_rounds_used`, `reviewer_verdict`, `task_id`, `test_passed`, `test_ran`, `title`
    - `cost`: `basis`, `value_usd`
    - `evidence`: `evidence_dir`, `postmortem_path`, `result_diff_path`, `result_diff_sha256`, `run_ids`, `run_manifest_path`
  - `projects`: `cost_today`, `missions`, `project_id`, `slug`
    - `cost_today`: `basis`, `calls`, `day`, `value_usd`
    - `missions`: `goal`, `job_ids`, `mission_id`, `order_source_path`, `order_source_sha256`, `status`
  - `supervisor`: `answers`
- `jobs`: `*`
  - `*`: `job_id`, `name`, `short_id`, `state`

#### `remedy decision resolve`

Command id: `decision.resolve`.
Description: Resolve a decision (if backed by a resolvable record).

| Argument | Option | Required | Takes a value | Repeatable | Help |
|---|---|---|---|---|---|
| `job_id` | no | yes | yes | no | UUID of the job (under its mission) |
| `decision_id` | no | yes | yes | no | ID of the decision to answer or resolve |
| `--reason` | yes | no | yes | no | Reason text |
| `--answer` | yes | no | yes | yes | Answer one bundled clarification (--answer q1="use PostgreSQL") or raise a budget decision's limit (--answer max_cost_usd=2.5); repeatable |
| `--as-mission` | yes | no | no | no | When approving: also create a mission for this goal and link this job as its initial job |
| `--json` | yes | no | no | no | Output as JSON |

Exit codes: `0`, `1`, `2`.
Refusal tokens: `ambiguous_job_id`, `answer_parse_error`, `budget_limit_not_raisable`, `budget_limit_not_raised`, `clarifications_already_resolved`, `decision_already_answered`, `decision_not_found`, `decision_not_resolvable`, `follow_up_mission_error`, `invalid_argument`, `invalid_budget`, `invalid_job_id`, `job_not_found`, `missing_argument`, `mission_already_linked`, `mission_error`, `no_pending_plan_approval`, `no_project`, `option_not_applicable`, `proposed_task_invalid_state`, `proposed_task_not_found`, `proposed_task_operation_failed`, `stop_reason_not_found`.
Answer keys: `answer`, `answers`, `assumption_log`, `budgets`, `closed_decisions`, `cross_references`, `decision_id`, `follow_up_job_id`, `follow_up_mission`, `job_id`, `matches`, `mission_id`, `next_command`, `next_step`, `option`, `outcome`, `raised`, `reason_code`, `state`, `stop_id`, `task_id`.
Keys under the answer keys: see below.

- `answers`: `answer`, `id`, `source`
- `budgets`: `deadline`, `max_cost_usd`, `max_provider_calls`, `max_total_tokens`, `max_wall_clock_minutes`, `min_free_disk_bytes`
- `raised`: `deadline`, `max_cost_usd`, `max_provider_calls`, `max_total_tokens`, `max_wall_clock_minutes`, `min_free_disk_bytes`

#### `remedy job run`

Command id: `job.run`.
Description: Run pending job tasks sequentially through Builder/Reviewer/Repair.

| Argument | Option | Required | Takes a value | Repeatable | Help |
|---|---|---|---|---|---|
| `job_id` | no | yes | yes | no | Job ID (under its mission) |
| `--max-rounds` | yes | no | yes | no | Max ping-pong rounds per task's run (default: 3, persisted on continuation) |
| `--repair-rounds` | yes | no | yes | no | Max repair attempts per task's run (default: 2, 0=disabled, persisted on continuation) |
| `--test-command` | yes | no | yes | no | Test command to execute in staging (persisted on continuation) |
| `--claude-cli-write-mode` | yes | no | yes | no | Claude CLI write mode for the BUILDER: none, allowed-tools, dangerous-skip (default: allowed-tools, persisted on continuation). The reviewer never writes |
| `--stream-evidence` | yes | no | no | no | Opt-in F004 raw stream evidence: use Claude CLI stream-json and write redacted raw_stream.jsonl + run_events.jsonl. Omitted keeps the persisted/default mode |
| `--no-stream-evidence` | yes | no | no | no | Explicitly disable this run's raw stream evidence (overrides a persisted true). Omitted keeps the persisted/default mode |
| `--tasks` | yes | no | yes | no | Max tasks to execute (omitted keeps persisted; 0=all) |
| `--timeout-sec` | yes | no | yes | no | Raw per-call timeout in seconds (omitted keeps persisted/default) |
| `--max-output-chars` | yes | no | yes | no | Max provider output chars (omitted keeps persisted/default) |
| `--builder-provider` | yes | no | yes | no | Builder provider: claude, claude-cli, fake or ollama (persisted on continuation) |
| `--builder-model` | yes | no | yes | no | Model for builder role |
| `--builder-effort` | yes | no | yes | no | Effort level for builder role |
| `--reviewer-provider` | yes | no | yes | no | Reviewer provider: claude, claude-cli, fake or ollama (persisted on continuation) |
| `--reviewer-model` | yes | no | yes | no | Model for reviewer role |
| `--reviewer-effort` | yes | no | yes | no | Effort level for reviewer role |
| `--repair-provider` | yes | no | yes | no | Provider for repair role |
| `--repair-model` | yes | no | yes | no | Model for repair role |
| `--repair-effort` | yes | no | yes | no | Effort level for repair role |
| `--timeout-profile` | yes | no | yes | no | Timeout profile: fast, normal, patient (default: normal unless raw timeout is explicitly set) |
| `--max-total-tokens` | yes | no | yes | no | Maximum total tokens (F018 budget override) |
| `--max-provider-calls` | yes | no | yes | no | Maximum provider calls (F018 budget override) |
| `--max-wall-clock-minutes` | yes | no | yes | no | Maximum wall-clock minutes (F018 budget override) |
| `--max-cost-usd` | yes | no | yes | no | Maximum cost in USD (F104 budget override) |
| `--deadline` | yes | no | yes | no | UTC deadline as ISO 8601 string (F018 budget override) |
| `--json` | yes | no | no | no | Output as JSON |

Exit codes: `0`, `1`, `2`.
Refusal tokens: `invalid_argument`, `invalid_budget`, `job_blocked`, `job_failed`, `job_not_resumable`, `job_not_started`, `job_stopped`, `job_stopped_by_budget`, `serve_unreachable`.
Answer keys: `context_strategy`, `cost_mirror`, `created_at`, `execution_config`, `finished_at`, `handoff_available`, `has_workspace_changes`, `isolation_mode`, `job_id`, `job_title`, `job_workspace_path`, `next_command`, `pending_tasks`, `postmortem`, `repair_rounds_allowed`, `repair_rounds_source`, `repo_path`, `result_diff`, `status`, `target_guard`, `tasks`, `warning`, `worktree`.
Keys under the answer keys: see below.

- `context_strategy`: `full_job_history_in_prompt`, `full_repo_in_prompt`, `previous_task_summary_limit`, `strategy`
- `cost_mirror`: `error`, `ledger_mirrored`, `out_dir`
- `execution_config`: `builder`, `builder_effort`, `builder_effort_source`, `builder_model`, `builder_model_source`, `builder_source`, `claude_cli_write_mode`, `claude_cli_write_mode_source`, `context_strategy`, `max_output_chars`, `max_output_chars_source`, `max_rounds`, `max_rounds_source`, `max_tasks`, `max_tasks_source`, `repair_effort`, `repair_effort_source`, `repair_model`, `repair_model_source`, `repair_provider`, `repair_provider_source`, `repair_rounds_allowed`, `repair_rounds_source`, `reviewer`, `reviewer_effort`, `reviewer_effort_source`, `reviewer_model`, `reviewer_model_source`, `reviewer_source`, `stream_evidence`, `stream_evidence_source`, `test_command`, `test_command_present`, `test_command_source`, `timeout_profile`, `timeout_profile_source`, `timeout_sec`, `timeout_sec_source`
- `postmortem`: `error`, `path`
- `result_diff`: `path`, `sha256`, `size_bytes`
- `target_guard`: `changed_target_files`, `ignored_operational_artifacts`, `ignored_target_noise_files`, `target_content_mutated`, `target_mutated`, `target_noise_changed`, `target_operational_artifacts_changed`
- `tasks`: `apply_manifest`, `error`, `final_status`, `proof_summary`, `repair_rounds_allowed`, `repair_rounds_used`, `reviewer_verdict`, `run_id`, `safe_diff_files`, `source_heading_number`, `status`, `steering_not_consumed`, `task_id`, `test_passed`, `title`, `veto`
  - `apply_manifest`: `applied_file_proofs`, `applied_files`, `duplicate_files`, `missing_files`, `run_id`, `status`, `task_id`, `unexpected_files`, `unsupported_files`
    - `applied_file_proofs`: `baseline_mode`, `baseline_sha256`, `existed_before_job`, `final_mode`, `final_workspace_sha256`, `path`, `run_id`, `task_id`
  - `proof_summary`: `applied_files`, `final_status`, `repair_rounds_allowed`, `repair_rounds_used`, `reviewer_verdict`, `run_id`, `task_id`, `test_passed`, `title`, `tokens_estimated`
  - `steering_not_consumed`: `message_id`, `received_at`, `text`
  - `veto`: `actor`, `reason`, `requested_at`, `unreachable_task_ids`
- `worktree`: `base_commit`, `branch`, `cleanup_status`, `head`, `path`, `workspace_expected_present`

#### `remedy job resume`

Command id: `job.resume`.
Description: Resume a job. Without --checkpoint: continue from the newest valid cycle checkpoint (F047) — a pending stop request is consumed first, worktree drift refuses, the plan-approval gate (approving the job's tasks) still applies. With --checkpoint <id>: resume from that safe event-replay checkpoint.

| Argument | Option | Required | Takes a value | Repeatable | Help |
|---|---|---|---|---|---|
| `job_id` | no | yes | yes | no | UUID of the job (under its mission) |
| `--checkpoint` | yes | no | yes | no | Event-replay checkpoint ID to resume from |
| `--dry-run` | yes | no | no | no | Preview resume without executing |
| `--cycles` | yes | no | yes | no | Maximum cycles for the resumed run's tasks (capped by the rollout default) |
| `--unattended` | yes | no | no | no | Run without a human present: a task decision that carries a safe default is auto-answered from it and recorded in the escalation assumption log. A question with no safe default still waits. |
| `--yes` | yes | no | no | no | Skip the cost-preview confirmation prompt above the configured threshold (F114). Never bypasses budget limits or the escalation log. |
| `--json` | yes | no | no | no | Output as JSON |

Exit codes: `0`, `1`, `2`, `3`.
Refusal tokens: `ambiguous_job_id`, `budget_decision_open`, `builder_error`, `builder_unavailable`, `checkpoint_not_found`, `checkpoint_not_resumable`, `checkpoints_corrupt`, `configuration_error`, `confirmation_required`, `invalid_argument`, `invalid_budget`, `invalid_builder_output`, `invalid_job_id`, `job_blocked`, `job_failed`, `job_not_found`, `job_not_resumable`, `job_not_started`, `job_stopped`, `job_stopped_by_budget`, `missing_dependency`, `permission_denied`, `plan_awaiting_approval`, `plan_rejected`, `resume_blocked`, `serve_unreachable`, `verification_failed`, `worktree_drift`.
Answer keys: `action`, `awaiting_checks`, `blocked_reason`, `budget_stop`, `can_resume`, `checkpoint_id`, `checkpoint_index`, `checkpoint_kind`, `context_strategy`, `cost_mirror`, `created_at`, `cycles`, `cycles_run`, `decision_id`, `dry_run`, `elapsed_ms`, `execution_config`, `failures`, `file`, `finished_at`, `handoff_available`, `has_workspace_changes`, `isolation_mode`, `job_id`, `job_status`, `job_title`, `job_workspace_path`, `log`, `matches`, `model`, `next_command`, `open_decision_ids`, `outcome`, `output_truncated`, `patch_intents`, `pending_tasks`, `persisted_output_bytes`, `plan_approval_gate`, `postmortem`, `reason`, `redaction`, `remaining`, `repair_rounds_allowed`, `repair_rounds_source`, `repo`, `repo_path`, `required_approvals`, `required_capabilities`, `result_diff`, `resume_mode`, `resumed`, `safety_summary`, `stage`, `state`, `status`, `stop_reason`, `stop_request`, `target_guard`, `task_id`, `task_type`, `tasks`, `terminal_status`, `test_run_id`, `tests_passed`, `verified`, `warning`, `worktree`, `worktree_head`, `worktrees`, `would_run`, `would_run_stage`.
Keys under the answer keys: see below.

- `budget_stop`: `decision_id`, `stopped`
- `context_strategy`: `full_job_history_in_prompt`, `full_repo_in_prompt`, `previous_task_summary_limit`, `strategy`
- `cost_mirror`: `error`, `ledger_mirrored`, `out_dir`
- `cycles`: `awaiting_downstream_task_ids`, `awaiting_task_ids`, `cycle_index`, `ended_at`, `errors`, `executed_task_ids`, `healed_after_repair`, `healed_without_changes`, `open_decision_ids`, `paused_downstream_task_ids`, `paused_task_ids`, `repair_rounds_used`, `repair_summary`, `skipped_blocked_task_ids`, `started_at`, `tasks_attempted`, `tasks_completed`, `tasks_escalated`, `tasks_failed`, `tokens_so_far`, `verify_command`, `verify_failure_class`, `verify_result`
- `execution_config`: `builder`, `builder_effort`, `builder_effort_source`, `builder_model`, `builder_model_source`, `builder_source`, `claude_cli_write_mode`, `claude_cli_write_mode_source`, `context_strategy`, `max_output_chars`, `max_output_chars_source`, `max_rounds`, `max_rounds_source`, `max_tasks`, `max_tasks_source`, `repair_effort`, `repair_effort_source`, `repair_model`, `repair_model_source`, `repair_provider`, `repair_provider_source`, `repair_rounds_allowed`, `repair_rounds_source`, `reviewer`, `reviewer_effort`, `reviewer_effort_source`, `reviewer_model`, `reviewer_model_source`, `reviewer_source`, `stream_evidence`, `stream_evidence_source`, `test_command`, `test_command_present`, `test_command_source`, `timeout_profile`, `timeout_profile_source`, `timeout_sec`, `timeout_sec_source`
- `failures`: `check`, `message`
- `postmortem`: `error`, `path`
- `result_diff`: `path`, `sha256`, `size_bytes`
- `stop_request`: `pending`, `reason`
- `target_guard`: `changed_target_files`, `ignored_operational_artifacts`, `ignored_target_noise_files`, `target_content_mutated`, `target_mutated`, `target_noise_changed`, `target_operational_artifacts_changed`
- `tasks`: `apply_manifest`, `error`, `final_status`, `proof_summary`, `repair_rounds_allowed`, `repair_rounds_used`, `reviewer_verdict`, `run_id`, `safe_diff_files`, `source_heading_number`, `status`, `steering_not_consumed`, `task_id`, `test_passed`, `title`, `veto`
  - `apply_manifest`: `applied_file_proofs`, `applied_files`, `duplicate_files`, `missing_files`, `run_id`, `status`, `task_id`, `unexpected_files`, `unsupported_files`
    - `applied_file_proofs`: `baseline_mode`, `baseline_sha256`, `existed_before_job`, `final_mode`, `final_workspace_sha256`, `path`, `run_id`, `task_id`
  - `proof_summary`: `applied_files`, `final_status`, `repair_rounds_allowed`, `repair_rounds_used`, `reviewer_verdict`, `run_id`, `task_id`, `test_passed`, `title`, `tokens_estimated`
  - `steering_not_consumed`: `message_id`, `received_at`, `text`
  - `veto`: `actor`, `reason`, `requested_at`, `unreachable_task_ids`
- `worktree`: `base_commit`, `branch`, `cleanup_status`, `head`, `path`, `workspace_expected_present`
- `worktree_head`: `checkpoint_head`, `live_head`, `outcome`
- `worktrees`: `applicable`, `base_commit`, `blocked`, `blocked_reason`, `branch`, `branch_kept`, `cleanup_status`, `head`, `notes`, `prepared`, `recovered`, `result_diff_sha256`, `result_diff_size_bytes`, `run_id`, `worktree_path`

#### `remedy job apply`

Command id: `job.apply`.
Description: Review and apply job workspace changes to target repo, under its mission. Preview by default; --approve applies.

| Argument | Option | Required | Takes a value | Repeatable | Help |
|---|---|---|---|---|---|
| `job_id` | no | yes | yes | no | Job ID (under its mission) |
| `--repo` | yes | no | yes | no | Path to target repository |
| `--approve` | yes | no | no | no | Apply changes (without this flag, preview only) |
| `--dry-run` | yes | no | no | no | Preview only, no target mutation |
| `--test-command` | yes | no | yes | no | Post-apply test command |
| `--skip-blocked` | yes | no | no | no | Apply the non-blocked files and deliberately leave the protected ones not applied (they are named, never written) |
| `--commit-with-history` | yes | no | no | no | Merge the job's commits, one per applied task step, onto your current branch with git merge --no-ff instead of copying files, as you and under your hooks; needs --approve (without it, preview only) and refuses a dirty tree, a detached HEAD, a staging job and a conflict, changing nothing |
| `--commit` | yes | no | yes | no | Copy the files, then land one commit of exactly those files on your current branch, as you and under your hooks, with this one line as its first line; needs --approve and a clean tree, and changes nothing when refused |
| `--commit-auto` | yes | no | no | no | As --commit, with a first line Remedy writes from the mission's goal or the job's title, and a body listing the title of each task step of the job |
| `--push` | yes | no | no | no | After --commit, --commit-auto or --commit-with-history lands, push that branch to its configured upstream, never forced; refused alone, without an upstream, or while any blocking criteria of the mission contract are unmet, and naming those still open, which no check has evaluated yet |
| `--json` | yes | no | no | no | Output as JSON |

Exit codes: `0`, `1`, `2`, `3`.
Refusal tokens: `apply_failed`, `blocked_paths`, `commit_refused`, `history_merge_refused`, `invalid_argument`, `job_not_found`, `job_not_ready`, `merge_conflict`, `post_test_failed`, `push_failed`, `push_no_upstream`, `push_refused`, `push_refused_by_contract`, `target_changed`, `target_detached_head`, `target_dirty`.
Answer keys: `approved`, `blocked_reason`, `blocked_reasons`, `commit_message_mode`, `commit_sha`, `commit_with_history`, `context_strategy`, `dry_run`, `execution_config`, `file_readiness`, `files_applied`, `files_blocked`, `files_planned`, `files_skipped`, `finished_at`, `history_commits`, `job_apply_id`, `job_id`, `job_status`, `job_title`, `job_workspace_path`, `merge_commit`, `merge_conflicts`, `merged_branch`, `missing_source_files`, `modes_applied`, `post_test_command_present`, `post_test_passed`, `post_test_summary`, `push`, `push_error`, `push_open_criteria`, `push_ref`, `push_remote`, `pushed`, `reviewed_task_files`, `skip_blocked`, `source_changed_files`, `started_at`, `status`, `target_branch`, `target_clean`, `target_guard_ok`, `target_repo`, `task_summaries`, `temporary_worktree_cleanup`, `unexpected_source_files`.
Keys under the answer keys: see below.

- `execution_config`: `builder`, `builder_effort`, `builder_effort_source`, `builder_model`, `builder_model_source`, `builder_source`, `claude_cli_write_mode`, `claude_cli_write_mode_source`, `context_strategy`, `max_output_chars`, `max_output_chars_source`, `max_rounds`, `max_rounds_source`, `max_tasks`, `max_tasks_source`, `repair_effort`, `repair_effort_source`, `repair_model`, `repair_model_source`, `repair_provider`, `repair_provider_source`, `repair_rounds_allowed`, `repair_rounds_source`, `reviewer`, `reviewer_effort`, `reviewer_effort_source`, `reviewer_model`, `reviewer_model_source`, `reviewer_source`, `stream_evidence`, `stream_evidence_source`, `test_command`, `test_command_present`, `test_command_source`, `timeout_profile`, `timeout_profile_source`, `timeout_sec`, `timeout_sec_source`
- `file_readiness`: `baseline_status`, `kind`, `path`, `workspace_status`
- `modes_applied`: `*`
- `task_summaries`: `applied_files`, `repair_rounds_allowed`, `repair_rounds_used`, `reviewer_verdict`, `run_id`, `status`, `task_id`, `test_passed`, `title`
- `temporary_worktree_cleanup`: `cleanup_error`, `cleanup_status`, `temporary_registration_removed`, `temporary_worktree_removed`

#### `remedy job decline`

Command id: `job.decline`.
Description: Decline a completed job's result under its mission, with your reason: nothing is applied, the job no longer waits for its apply, and the decline is kept on the job and named in its ownership record (F304).

| Argument | Option | Required | Takes a value | Repeatable | Help |
|---|---|---|---|---|---|
| `job_id` | no | yes | yes | no | UUID of the job (under its mission) |
| `--reason` | yes | yes | yes | no | Why you decline the result, in your own words; kept with the decline |
| `--json` | yes | no | no | no | Output as JSON |

Exit codes: `0`, `1`, `2`, `3`.
Refusal tokens: `ambiguous_job_id`, `invalid_job_id`, `job_already_applied`, `job_not_declinable`, `job_not_found`, `missing_argument`.
Answer keys: `already_declined`, `declined_at`, `job_id`, `matches`, `reason`, `source`.
Keys under the answer keys: none.

#### `remedy change proof`

Command id: `change.proof`.
Description: Show proof chain — why changes happened and verification status.

| Argument | Option | Required | Takes a value | Repeatable | Help |
|---|---|---|---|---|---|
| `job_id` | no | yes | yes | no | UUID of the job (under its mission) |
| `--path` | yes | no | yes | no | Filter to a specific file path |
| `--json` | yes | no | no | no | Output as JSON |

Exit codes: `0`, `1`, `2`.
Refusal tokens: `ambiguous_job_id`, `invalid_job_id`, `invalid_path`, `job_not_found`.
Answer keys: `changes`, `generated_at`, `goal`, `job_applies`, `job_id`, `matches`, `missing_links`, `next_safe_action`, `next_safe_action_obj`, `overall_status`, `path_filter`, `version`.
Keys under the answer keys: see below.

- `changes`: `apply_state`, `approval_state`, `artifact_id`, `intent_id`, `missing_links`, `next_safe_action`, `next_safe_action_obj`, `proof_status`, `safe_summary`, `target_path`, `task_id`, `task_title`, `test_link`, `test_state`
  - `next_safe_action_obj`: `available`, `command`, `label`, `reason`
- `job_applies`: `approved`, `commit_sha`, `dry_run`, `files_applied`, `finished_at`, `job_apply_id`, `post_test_passed`, `pushed`, `status`
- `next_safe_action_obj`: `available`, `command`, `label`, `reason`

#### `remedy job evidence`

Command id: `job.evidence`.
Description: Export a self-contained evidence bundle for an entire job (under its mission).

| Argument | Option | Required | Takes a value | Repeatable | Help |
|---|---|---|---|---|---|
| `job_id` | no | yes | yes | no | Job ID (under its mission) |
| `--out` | yes | no | yes | no | Output directory for bundle files |
| `--verification-command` | yes | no | yes | yes | Explicit verification command to execute and record (repeatable) into the evidence bundle. Each execution is stored as a verification run covering the test files it names |
| `--json` | yes | no | no | no | Output as JSON |

Exit codes: `0`, `1`, `2`.
Refusal tokens: `job_not_found`, `unsafe_task_id`.
Answer keys: `files`, `job_id`, `manifest`, `out_dir`.
Keys under the answer keys: see below.

- `files`: `*`
- `manifest`: `bundle_generated_at`, `bundle_type`, `bundle_version`, `context_strategy`, `created_at`, `error`, `execution_config`, `finished_at`, `job_file_sha256`, `job_id`, `job_title`, `job_workspace_path`, `repo_identity`, `status`, `target_guard`, `task_count`, `task_ids`, `task_run_ids`, `task_statuses`
  - `execution_config`: `builder`, `builder_effort`, `builder_effort_source`, `builder_model`, `builder_model_source`, `builder_source`, `claude_cli_write_mode`, `claude_cli_write_mode_source`, `context_strategy`, `max_output_chars`, `max_output_chars_source`, `max_rounds`, `max_rounds_source`, `max_tasks`, `max_tasks_source`, `repair_effort`, `repair_effort_source`, `repair_model`, `repair_model_source`, `repair_provider`, `repair_provider_source`, `repair_rounds_allowed`, `repair_rounds_source`, `reviewer`, `reviewer_effort`, `reviewer_effort_source`, `reviewer_model`, `reviewer_model_source`, `reviewer_source`, `stream_evidence`, `stream_evidence_source`, `test_command`, `test_command_present`, `test_command_source`, `timeout_profile`, `timeout_profile_source`, `timeout_sec`, `timeout_sec_source`
  - `target_guard`: `changed_target_files`, `ignored_operational_artifacts`, `ignored_target_noise_files`, `target_content_mutated`, `target_mutated`, `target_noise_changed`, `target_operational_artifacts_changed`
  - `task_run_ids`: `*`
  - `task_statuses`: `*`

#### `remedy patch hunks`

Command id: `patch.hunks`.
Description: Show the hunks of a job's diff, or of one of its tasks, with their ids and the answer recorded for them.

| Argument | Option | Required | Takes a value | Repeatable | Help |
|---|---|---|---|---|---|
| `job_id` | no | yes | yes | no | UUID of the job (under its mission) |
| `--task-run` | yes | no | yes | no | Task run whose hunks to show, exactly as it is named under task_runs/ (T001); omit it for the job-level diff |
| `--json` | yes | no | no | no | Output as JSON |

Exit codes: `0`, `1`, `2`.
Refusal tokens: `ambiguous_job_id`, `invalid_job_id`, `job_not_found`.
Answer keys: `decision`, `job_id`, `matches`, `view`.
Keys under the answer keys: see below.

- `decision`: `attempt_key`, `decided_at`, `hunks`
  - `hunks`: `id`, `reason`, `state`
- `view`: `available`, `files`, `reason`, `scope`, `source`, `task_id`, `task_run_ids`, `truncated`, `version`
  - `files`: `hunks`, `note`, `old_path`, `path`, `stats`, `status`
    - `hunks`: `header`, `id`, `lines`, `new_start`, `old_start`
      - `lines`: `content`, `intraline`, `kind`, `new_ln`, `old_ln`
    - `stats`: `added`, `deleted`

#### `remedy patch approve-hunks`

Command id: `patch.approve-hunks`.
Description: Record a hunk-level approve-or-reject answer over one of a job's tasks.

| Argument | Option | Required | Takes a value | Repeatable | Help |
|---|---|---|---|---|---|
| `job_id` | no | yes | yes | no | UUID of the job (under its mission) |
| `--task-run` | yes | no | yes | no | Task run to decide over, exactly as it is named under task_runs/ (T001); omit it to decide over the job-level diff |
| `--approve-hunk` | yes | no | yes | yes | Approve one hunk by id (repeatable) |
| `--reject-hunk` | yes | no | yes | yes | Reject one hunk with a reason: --reject-hunk <hunk-id>=<reason>, e.g. --reject-hunk h3="renames a public name" (repeatable) |
| `--json` | yes | no | no | no | Output as JSON |

Exit codes: `0`, `1`, `2`.
Refusal tokens: `ambiguous_job_id`, `duplicate_hunk`, `empty_decision`, `invalid_job_id`, `job_not_found`, `missing_reason`, `no_diff_available`, `overlapping_sets`, `unknown_hunk`, `untrustworthy_view`.
Answer keys: `attempt`, `decided_at`, `hunk_ids`, `hunks`, `matches`, `task_id`.
Keys under the answer keys: see below.

- `hunks`: `id`, `landing`, `reason`, `state`

#### `remedy patch approve`

Command id: `patch.approve`.
Description: Approve a patch intent for application.

| Argument | Option | Required | Takes a value | Repeatable | Help |
|---|---|---|---|---|---|
| `job_id` | no | yes | yes | no | UUID of the job (under its mission) |
| `intent_id` | no | yes | yes | no | Intent ID (integer) |
| `--reason` | yes | no | yes | no | Reason text |
| `--json` | yes | no | no | no | Output as JSON |

Exit codes: `0`, `1`, `2`.
Refusal tokens: `ambiguous_job_id`, `invalid_job_id`, `job_not_found`, `patch_intent_not_found`.
Answer keys: `intent_id`, `matches`, `reason_recorded`, `risk`, `state`, `target_path`.
Keys under the answer keys: none.

#### `remedy patch reject`

Command id: `patch.reject`.
Description: Reject a patch intent.

| Argument | Option | Required | Takes a value | Repeatable | Help |
|---|---|---|---|---|---|
| `job_id` | no | yes | yes | no | UUID of the job (under its mission) |
| `intent_id` | no | yes | yes | no | Intent ID (integer) |
| `--reason` | yes | no | yes | no | Reason text |
| `--json` | yes | no | no | no | Output as JSON |

Exit codes: `0`, `1`, `2`.
Refusal tokens: `ambiguous_job_id`, `invalid_job_id`, `job_not_found`, `patch_intent_not_found`.
Answer keys: `intent_id`, `matches`, `reason_recorded`, `risk`, `state`, `target_path`.
Keys under the answer keys: none.

#### `remedy mission abandon`

Command id: `mission.abandon`.
Description: Mark a mission abandoned — the goal is dropped; its jobs and their run evidence stay.

| Argument | Option | Required | Takes a value | Repeatable | Help |
|---|---|---|---|---|---|
| `mission_id` | no | yes | yes | no | Mission id (or a unique prefix) that owns the jobs |
| `--project` | yes | no | yes | no | Scope to a project's repo (slug or UUID) |
| `--json` | yes | no | no | no | Output as JSON |

Exit codes: `0`, `1`, `2`, `3`.
Refusal tokens: `mission_error`, `mission_not_found`, `no_project`.
Answer keys: `mission`, `unmet_blocking_criteria`, `version`.
Keys under the answer keys: see below.

- `mission`: `contract`, `created_at`, `dossier_ref`, `goal`, `id`, `job_links`, `mission_plan`, `order`, `project_id`, `schema_version`, `status`
  - `contract`: `amendments`, `criteria`, `schema`, `template`
    - `amendments`: `acknowledged_in`, `applies_from`, `criteria`, `id`, `received_at`, `text`, `understood`
    - `criteria`: `blocking`, `check`, `evidence_ref`, `id`, `milestones`, `origin`, `status`, `text`
      - `check`: `acceptance_refs`, `blocking`, `description`, `id`, `kind`, `source`, `spec` (keys not fixed)
  - `job_links`: `created_at`, `job_id`, `job_state`, `role`
  - `mission_plan`: `_milestones_done`, `_version`, `_versions` (repeats the object that holds it), `assumptions`, `compiled`, `milestones`, `origin`, `risks`, `schema_v`
    - `milestones`: `depends_on`, `dod_ref`, `goal`, `id`, `jobs_draft`, `rationale`
      - `jobs_draft`: `est_band`, `goal`, `title`
  - `order`: `source_path`, `source_sha256`, `text`

#### `remedy client interface`

Command id: `client.interface`.
Description: Show what a program that drives Remedy can rely on: its commands, arguments, exit codes, state words, templates and budget kinds (read-only).

| Argument | Option | Required | Takes a value | Repeatable | Help |
|---|---|---|---|---|---|
| `--json` | yes | no | no | no | Output as JSON |

Exit codes: `0`, `1`, `2`.
Refusal tokens: none.
Answer keys: `answer_trees`, `answers`, `budget_kinds`, `contract_templates`, `digest`, `envelope`, `exit_codes`, `interface_version`, `job_states`, `mission_statuses`, `operations`.
Keys under the answer keys: see below.

- `answer_trees`: `*`
  - `*`: `*`
    - `*`: `*` (repeats the object that holds it)
- `answers`: `*`
- `digest`: `*` (repeats the object that holds it)
- `envelope`: `error_keys`, `reserved_keys`, `schema_version`
- `exit_codes`: `code`, `meaning`, `name`
- `operations`: `arguments`, `command`, `command_id`, `description`, `exit_codes`, `refusal_tokens`
  - `arguments`: `help`, `name`, `option`, `repeatable`, `required`, `takes_value`

### Digest

The keys of the `client` object of `remedy status --json`.

Keys: `awaiting_apply`, `decisions`, `degraded`, `jobs`, `projects`, `read_at`, `skipped_files`, `supervisor`, `version`.

- `decisions`: `age_seconds`, `clarifications`, `created_at`, `decision_id`, `default`, `job_id`, `options`, `project_id`, `question`, `severity`, `type`
  - `clarifications`: `default`, `id`, `question`
- `jobs`: `approval_card`, `cost`, `evidence`, `job_id`, `mission_id`, `project_id`, `state`, `title`, `waits_for_apply`
  - `approval_card`: `changed_file_count`, `changed_files`, `tasks`, `test_command`
    - `tasks`: `repair_rounds_used`, `reviewer_verdict`, `task_id`, `test_passed`, `test_ran`, `title`
  - `cost`: `basis`, `value_usd`
  - `evidence`: `evidence_dir`, `postmortem_path`, `result_diff_path`, `result_diff_sha256`, `run_ids`, `run_manifest_path`
- `projects`: `cost_today`, `missions`, `project_id`, `slug`
  - `cost_today`: `basis`, `calls`, `day`, `value_usd`
  - `missions`: `goal`, `job_ids`, `mission_id`, `order_source_path`, `order_source_sha256`, `status`
- `supervisor`: `answers`
<!-- END GENERATED by render_client_interface_markdown() -->
