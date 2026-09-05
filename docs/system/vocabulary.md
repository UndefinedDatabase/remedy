# Vocabulary — the words Remedy uses

> **BINDING.** These are the words. Every feature, every command description in
> `apps/cli/command_catalog.py` and every document under `docs/` uses them with
> the meaning given here, and uses no synonym for a word that already has one.
> The operator decided them on 2026-09-05 in order amend0905-vocab-rebuild,
> DECISION amend0905-vocab D1; F259 wrote them down. To change a word, change
> this page first.

## How to read the table

Two of the columns disagree on purpose. **Code spelling today** is what the
source really says right now — it was read out of the code, not remembered, and
`.agent/f259_inventory.md` holds the per-symbol citations it was taken from,
measured at commit `67598164`. **Code spelling after F260/F261** is a PLAN:
F260 rebuilds the data model and F261 performs the renames, and until they land
the two columns differ wherever the current code carries a word this page
retires. A reader who conflates them will think the page is wrong about the
code; it is not, it is about both the code and the decision.

The last column is the one that does the work. Most of the confusion this page
exists to end was not people failing to define a word — it was two words for one
thing, or one word for two things.

## The words

| Word | Meaning | Code spelling today | Code spelling after F260/F261 | CLI spelling | Is NOT |
|---|---|---|---|---|---|
| **Project** | The frame: one or more repos and every mission inside them. | `project_id` in `packages/core/models.py` and in `packages/orchestration/mission_state.py`, which also defines `mission_dir_for_project` and `project_ids_with_missions`; the store path is `projects_dir` in `packages/orchestration/data_paths.py` | unchanged | the `project` group: `create`, `list`, `show`, `attach-repo`, `attach-job`, `brain`, `context`, `summary`, `current`, `adopt` | — |
| **Order** | Everything the human gives Remedy: the initial text or file behind `remedy do`, and every later message during a run. | no symbol spells it; the same thing is carried under two other names — `parse_job_file`, `plan_job_from_file` and `job_file_sha256` in `packages/orchestration/pingpong_job.py`, and the `--job-file` and `--task-file` options in `apps/cli/command_catalog.py` | `order`; both option spellings are deleted and the argument becomes the positional `<order>`, text or a `.md` path (DECISION F259 D2) | none today; `do <order>` after F261 | the Job — the Order is the input, the Job is Remedy's response |
| **Mission** | What every Order becomes: one persistent record holding the Order, the Contract, the mission Plan and an ordered list of 1..n Jobs. | `Mission`, `MissionJobLink`, the `MISSION_STATUS_` and `MISSION_ROLE_` constants and the `Mission*Error` family, all in `packages/orchestration/mission_state.py` | unchanged as a type; a mission is created for EVERY order, which reverses F056's "a mission is never created automatically" (DECISION amend0905-vocab D2) | the `mission` group: `list`, `show`, `plan`, `contract`, `run`, `continue`, `pause`, `resume`, `achieve`, `abandon`, `start` | a schedule; a job |
| **Contract** | The acceptance criteria of a Mission, compiled to machine-checkable checks — its Definition of Done. One per mission; a job's contract is the derived slice for that job. | nothing in the seven sources spells this concept; its two halves are `PlannedTask.acceptance` in `packages/orchestration/schemas/models.py` and `packages/orchestration/dod_compiler.py`. The catalog's `contract` group today is a DIFFERENT concept wearing the word: the run-permission object, as `contract.inspect`, `contract.check` and `contract.set` | `contract` names the acceptance criteria and nothing else; the run-permission group is deleted and its idea folded into permissions and fences (DECISION amend0905-vocab D4) | `mission contract <id>` and `job contract <id>` after F261 | the run-permission object once called the "run contract" |
| **Job** | The administrative unit under a mission: identity, budget, fences, permissions, decisions, the job Plan with its Tasks, and references to its Runs. | the record and its parts are `Job`, `JobBudgets` and `JobFences` in `packages/core/models.py`; the plan and the state constants are `JobPlan`, `JOB_PLANNED`, `JOB_RUNNING`, `JOB_BLOCKED`, `JOB_COMPLETED`, `JOB_PAUSED` and `JOB_STOPPED` in `packages/orchestration/pingpong_job.py`. Two id shapes are minted from two stores, which `packages/orchestration/data_paths.py` documents in as many words: "Remedy has TWO job stores and they are shaped differently" | one store and one id shape (F260) | the `job` group | the Run |
| **Plan** | The ordered "what will be done" of a level: the mission plan lists the milestones, each of which becomes a job; the job plan lists the tasks. | two dialects side by side. `packages/orchestration/schemas/models.py` defines `FlightPlan`, `FlightPlanClarification`, `PlannerPlan`, `PlannedTask` and `FLIGHT_PLAN_SCHEMA_V`; `packages/orchestration/flight_plan.py` defines `FlightPlanResult` and `map_flight_plan_to_tasks`; and `packages/orchestration/pingpong_job.py` carries `JobPlan` beside them | `flight_plan.py` becomes `job_plan.py` and the noun "flight plan" is deleted from code, catalog, docs and feature files (DECISION amend0905-vocab D6) | `job plan` and `mission plan` are the only two plan commands; today's `plan status` and `plan next` become the hidden group `roadmap` | the Roadmap |
| **Task** | One step in a job plan; the planner chooses how many, bounded by configured maxima that are ceilings, not targets. | four spellings for one idea: `Task` in `packages/core/models.py`; `TaskEntry` in `packages/orchestration/pingpong_job.py`, alongside the `TASK_PENDING` to `TASK_SPLIT` state constants, `max_tasks` and the converters `task_entry_to_planned_task` and `planned_task_to_task_entry`; and `PlannedTask` and `ProposedTask` in `packages/orchestration/schemas/models.py` | one task type (F260) | no group of its own; it appears as `job run <id> --tasks n` and `job context <id> --task <t>` | a Round |
| **Run** | One execution of the ping-pong loop for exactly one Task, owning exactly one evidence folder. | `RunState` in `packages/core/models.py`; `run_id`, `run_job` and the `run_manifest_path`, `run_manifest_created_at` and `run_manifest_episodes` fields in `packages/orchestration/pingpong_job.py`; `runs_dir` in `packages/orchestration/data_paths.py`. The word also names a provider call in one place and a whole execution in another | `run` means the per-task execution and nothing else | `run show <id>` and `run list` after F261; today the verb is scattered across `job run`, `do run`, `mission run`, `loop run` and more | the verb; a dogfood run; the run manifest |
| **Round** | One pass inside a run: build, then tests, then review. Round 2 and later are repairs. | `max_rounds`, `max_rounds_source`, `repair_rounds_allowed`, `repair_rounds_used` and `repair_rounds_source` in `packages/orchestration/pingpong_job.py` | unchanged | none | a Task — a task can take several rounds |
| **Worker** | A model in a role. The roles are Builder, Reviewer, Planner and Teacher, and the list is extensible. | nothing spells the concept itself; the roles appear as the `builder_model` and `reviewer_model` fields in `packages/orchestration/pingpong_job.py` | unchanged as a type, but the report names the ROLE and never says "Worker: fake" for a builder (DECISION amend0905-vocab D1) | the `worker` group: `list`, `show`, `resources`, `unload`, `status`, `doctor` after F261 | — |
| **Decision** | A question Remedy cannot answer for itself, put to the human and answered with one command. | `HumanDecision` in `packages/orchestration/decision_queue.py`; the flight-plan approval path spells the same idea as `flight_plan_approval_open` and `resolve_flight_plan_approval` in `packages/orchestration/flight_plan.py` | the approval stays a Decision; the retired noun leaves its name with DECISION amend0905-vocab D6 | the `decision` group: `list`, `show`, `resolve`, `explain` | a DECISION paragraph in `.agent/decisions.md`, which is Remedy's own build record and not a user concept |
| **Evidence** | What one Run leaves behind: exactly one folder per task run, holding the inputs, the outputs and the proofs. | `build_evidence_bundle` in `packages/orchestration/pingpong_evidence.py`; `stream_evidence` and `job_evidence_dir` in `packages/orchestration/pingpong_job.py`; `mission_evidence_dir` in `packages/orchestration/mission_state.py`; `evidence_exports_dir` in `packages/orchestration/data_paths.py` | unchanged | `job evidence <id>` after F261; today `do evidence` and `do job-evidence` | the run manifest, which is one file inside the folder |
| **Gate** | A check that must pass before the work may proceed; it decides, and it records what it decided from. | `GateResult` in `packages/orchestration/dod_gate.py`, the only type under `packages/` named for the concept itself rather than for one particular gate; nothing in the seven sources spells it | unchanged | none | a Verdict — the gate is the check, the verdict is the Reviewer's judgement |
| **Verdict** | The Reviewer's judgement on one Round. | `Verdict` and `ReviewVerdict` in `packages/orchestration/schemas/models.py`, where `Verdict` is the literal set pass, fail, needs_repair, blocked; the field carrying it is `reviewer_verdict` in `packages/orchestration/pingpong_job.py` | unchanged | none | a Gate's result |
| **Roadmap** | Remedy's own build plan under `docs/roadmap/`; a developer tool, never a user concept. | nothing in the seven sources spells it; the ledger is the file `docs/roadmap/STATUS.md` | unchanged | today's `plan status` and `plan next` become the hidden group `roadmap` (DECISION amend0905-vocab D6) | a mission plan |

The seven sources the "code spelling today" column was read from are
`packages/core/models.py`, `packages/orchestration/pingpong_job.py`,
`packages/orchestration/schemas/models.py`,
`packages/orchestration/flight_plan.py`,
`packages/orchestration/mission_state.py`,
`packages/orchestration/data_paths.py` and `apps/cli/command_catalog.py`.
Where a cell names a module outside that list —
`packages/orchestration/decision_queue.py`,
`packages/orchestration/pingpong_evidence.py`,
`packages/orchestration/dod_gate.py` and
`packages/orchestration/dod_compiler.py` — it is because DECISION
amend0905-vocab D1 gave that word no table row and told F259 to write one from
the feature that owns the concept; they were found by searching every `.py`
file under `packages/` and under `apps/`.

## Do not confuse these

Most of what this page exists to end was never someone failing to define a word.
It was two words for one thing, or one word for two things.

| Not the same | The difference | Why they get confused |
|---|---|---|
| **Job / Run** | A Job is the administrative unit — identity, budget, fences, permissions, a plan. A Run is one execution of the loop for one Task, owning one evidence folder. One Job has many Runs. | Both carry an id and a status, and the command `job run` reads as though the job were the thing that runs. |
| **Plan / Roadmap** | A Plan is what Remedy will do for a mission or a job. The Roadmap is Remedy's OWN build plan under `docs/roadmap/`, a developer artefact no user ever sees. | The CLI today spells the roadmap mirror `plan status` and `plan next`, which is the sharpest collision in the tree; DECISION amend0905-vocab D6 moves it to the hidden group `roadmap`. |
| **Order / Job** | The Order is what the human gives Remedy. The Job is what Remedy makes of it. Input against response. | The order arrives as a file and the job is parsed straight out of it, so one phrase — "job file" — has been naming both ends at once. |
| **Task / Round** | A Task is one step of a job plan. A Round is one pass inside a single Run of a single Task: build, then tests, then review. A task that fails takes a second Round, never a second Task. | Both are counted and both are capped, and casual prose calls either one a "step". |
| **Contract / permissions** | The Contract is what the mission must ACHIEVE — acceptance criteria compiled to checks. Permissions and fences are what Remedy is ALLOWED TO DO while trying. Goal against boundary. | The catalog's `contract` group today is the permission object, not the acceptance criteria, so the word currently points at the wrong one of the two. |
| **Mission / schedule** | A Mission is one order and everything that came of it. It has no recurrence and no clock. | `remedy loop` and the `overnight` group made recurrence look like a property of a mission; DECISION amend0905-vocab D7 deletes both, and a recurring order becomes an order file started by hand. |
| **Worker / role** | A Worker is a model IN a role. The role is Builder, Reviewer, Planner or Teacher; the worker is whichever model is bound to that role for this task. | Reports have printed "Worker: fake", which names the provider in the place a reader expects the role. |
| **template / order file** | A template is a CONTRACT template — website, api-service, cli-tool, python-library — proposed by the planner or forced with `--contract`. An order file is a Markdown file holding one human's order, started with `remedy do <file>`. | Both are files you keep in the repo and hand to Remedy, and the deleted `loop` tables called order files templates. |

## The concept model

```mermaid
flowchart TD
    Order["Order (text or .md file)"] --> Mission["Mission (contract, plan)"]
    Mission --> Job["Job 1..n (budget, fences, plan)"]
    Job --> Task["Task 1..n"]
    Task --> Run["Run (one evidence folder per task)"]
    Run --> R1["Round 1 (build · review)"]
    R1 --> R2["Round 2+ (repair)"]
```

In words, for a first read. You give Remedy an **Order** — a sentence, or a
Markdown file. Remedy turns it into a **Mission**, the record of that order,
which holds the **Contract**: the acceptance criteria the finished work must
meet. The mission is carried out by one or more **Jobs**, and each job has its
own budget, its fences and its own **Plan** — and that plan is a list of
**Tasks**. Each task is executed by exactly one **Run**, which owns exactly one
evidence folder. Inside a run the work happens in **Rounds**: round 1 builds and
reviews, and every later round repairs.

Everything above the Run is bookkeeping. The Run is where a model actually
writes code, and the evidence folder it leaves behind is what you read
afterwards to see what happened.

## The rulings

The words on this page were not derived; they were decided. The eleven rulings
below are the decisions themselves, copied here unedited so that a reader of the
page never has to go looking for the reasoning — each one names its date, the
operator order it came from, and how to reverse it.

They are copies, and the copy is not the original. DECISION amend0905-vocab D2
through D10 live in `.agent/decisions.md`; DECISION F259 D1 and D2 live in
`docs/roadmap/features/T2_F259.md`. Those files are where the rulings were made
and where a reversal is performed — deleting a paragraph here would change
nothing. Because they are verbatim copies of Remedy's own build record, some of
them talk about Remedy's internals — feature ids, finding ids, module paths — in
a way the rest of this page does not; that is the price of not paraphrasing a
decision, and it is worth paying, because a paraphrased ruling is a second
source of truth.

### DECISION amend0905-vocab D2 (2026-09-05, operator order amend0905-vocab-rebuild) — everything is a mission

No job exists without a mission. The contract has exactly one home, the mission.
`remedy do` decides from the order whether the mission gets one job or several —
the planner's shape decision; `--force-job` forces exactly one job, `--force-mission`
forces at least two. The F056 rule "a mission is never created automatically"
(T1_F056.md Goal & Done, Acceptance, and the negative tests named in its Built State)
is REVERSED by this ruling; the explicit mission start (`mission start "<goal>"`)
remains available. F260 builds the unified record; F268 builds the shape decision.
Reverse by deleting this paragraph.

### DECISION amend0905-vocab D3 (2026-09-05, operator order amend0905-vocab-rebuild) — cleanliness before compatibility, deletion before archive

Restates amend0831 D-A (hard breaks allowed while Remedy is deployed nowhere; no
migration shims) and D-B (old commands are deleted, not aliased; dependents converted
in the same move) and adds: there is NO `attic/`, NO deprecated alias, NO
compatibility reader. Deleted code is recovered from git if ever needed. The only
trace of a deletion is one dated DECISION paragraph naming the deleted modules and,
per module, the feature that inherited its idea, so no later session rebuilds it.
Reverse by deleting this paragraph.

### DECISION amend0905-vocab D4 (2026-09-05, operator order amend0905-vocab-rebuild) — the CLI tree after F261 (binding, complete)

Measured 2026-09-05 at `b2ee0a84`: `apps/cli/command_catalog.py` carries 60 groups
and 342 commands; `GroupDef` has the fields `id`, `label`, `description`,
`user_facing`, and 17 groups are `user_facing=True`. After F261 the tree is:

Visible in `remedy --help`, in this order: do, mission, job, run, decision, status,
stats, teach, memory, ui, config (with the `settings` alias of amend0831 D-D), doctor,
project, init, worker, runtime.

Advanced (only with `--all-commands`): brain, event, patch, test, blocker, change,
file, snapshot, self, ci, integrity, dev.

Hidden (in no help at all, callable): roadmap.

Every group not named above is deleted by F261. That includes: queue, loop,
overnight, provider, external-builder, local-advisor, local-candidate,
candidate-quality, builder-routing, route-policy, tournament, context, context-pack,
token, contract (the run-permission group; the word is freed for D1's Contract),
policy, approval, readiness, progress, feature, propose, review, repair, builder,
execution, dogfood, self-repair, orchestrator, rollback, guide, dashboard, plan
(renamed to the hidden roadmap). The catalog group `repo` (`repo status`, `repo
commit-readiness`) appears in neither list of the ruling and therefore falls under
"every group not named here is deleted"; the session recorded this as a finding in
`.agent/live_review.md` so the operator sees it at the next relay.

Clarification 2026-09-05: repo is deleted; see R-0800.

The commands per surviving group:

- `do <order>` where `<order>` is a text or a path to a `.md` file. Flags:
  `--apply`, `--with-history`, `--step-by-step`, `--plan-only`, `--force-job`,
  `--force-mission`, `--contract <template>`, `--no-ui`, `--project`, `--repo`, the
  budget flags, the role flags (`--builder-model`, `--reviewer-model`,
  `--planner-model`, and the `--*-provider` triplet), `--yes`, `--json`. Nothing
  else under `do`.
- `mission list | show <id> [--full] | plan <id> | contract <id> | run <id> |
  continue <id> "<next step>" | pause | resume | achieve | abandon | watchdog |
  handoff | report | readiness | start "<goal>"`. `mission list` IS the operator's
  list of orders; `show` prints the order text and every amendment.
- `job list | show <id> [--full] | run <id> [--tasks n] | plan <id> | contract <id> |
  stop <id> | resume <id> | checkpoints <id> | apply <id> [--approve]
  [--with-history] [--skip-blocked] | evidence <id> | context <id> --task <t> |
  budget <id> [set …]`. Permissions, fences, assumptions, digest, summary, status,
  report, dod are sections of `job show --full`; they are not commands.
- `run show <id> | list`.
- `worker list | show | resources | unload | status | doctor`.
- All other surviving groups keep their commands minus anything that imports a
  deleted module.

Reverse by deleting this paragraph.

### DECISION amend0905-vocab D5 (2026-09-05, operator order amend0905-vocab-rebuild) — apply replaces promote everywhere

`apply` replaces `promote` everywhere: CLI (`do promote`, `do job-promote` → `job
apply`), code identifiers, docs, and evidence file names where a rename does not
break an accepted evidence chain. Accepted `[x]` evidence is history and stays
byte-identical. The word `promote` in its OTHER senses — a memory card promoted
between scopes (F125, F211), a model promoted into a task class (F110,
docs/agents/model_routing_policy.md), a non-blocking check promoted to blocking by
config (F130, F132–F134, F156, F170), a finding promoted into a checklist — is not
the job-result verb and is not renamed; the sweep of this amendment applied the
ruling by SENSE and recorded the kept occurrences in `.agent/live_review.md`.
Reverse by deleting this paragraph.

### DECISION amend0905-vocab D6 (2026-09-05, operator order amend0905-vocab-rebuild) — plan words

`job plan` and `mission plan` are the only two plan commands.
`packages/orchestration/flight_plan.py` becomes `job_plan.py`; the noun "flight
plan" is deleted from code, catalog, docs and feature files (accepted `[x]` feature
files carry a vocabulary note instead of an edit, per D5's history rule). The
roadmap mirror (today `remedy plan status|next`, F080) becomes the hidden group
`roadmap` with the same two subcommands. Reverse by deleting this paragraph.

### DECISION amend0905-vocab D7 (2026-09-05, operator order amend0905-vocab-rebuild) — templates

`remedy loop` (F045's `loop.list`, `loop.validate`, `loop.run` and the `[[loop]]`
tables of `remedy.toml`) is deleted by F261. A recurring order is an order file kept
in the repo and started with `remedy do <file.md>`. The word "template" is reserved
for contract templates (D9). A scheduler that fires order files on a schedule is a
later feature; nothing here builds it and nothing here registers it. Reverse by
deleting this paragraph.

### DECISION amend0905-vocab D8 (2026-09-05, operator order amend0905-vocab-rebuild) — remedy do is THE easy start and the operator's standing test path

In order: `init` if the repo is not registered; `study` (F266) exactly once if the
repo is non-empty and never studied (afterwards only by hand); the planner produces
mission plan + contract + job plans; the shape decision (one job or several); the
runs start; the cockpit opens in the browser (unless `--no-ui`); it stops before
applying unless `--apply`. `--step-by-step` halts at every safe point, prints what
just happened and what comes next, waits for Enter (`q` stops). `--plan-only` stops
after planning. `do` never runs a model call while waiting for a keypress. F268
builds this. Reverse by deleting this paragraph.

### DECISION amend0905-vocab D9 (2026-09-05, operator order amend0905-vocab-rebuild) — contract and templates

The contract is compiled from the order by the planner; today's F014 acceptance
criteria (`PlannedTask.acceptance`) and the F061 DoD compiler
(`packages/orchestration/dod_compiler.py`) are its two halves. Four templates ship
first: website, api-service, cli-tool, python-library; the planner proposes one from
the order, `--contract <name>` forces one. Every later operator message (the F264
channel) is an amendment to the contract: recorded on the mission, DoD recompiled,
acknowledged with what was understood and from which round it applies. At budget end
with blocking criteria open, Remedy proposes a remainder contract ("these two
criteria are unmet — start a follow-up mission?") as a decision the operator answers
with one word. The old overnight Mission Contract prototype
(`packages/orchestration/overnight_mission.py`, `overnight contract-create |
contract-show | contract-readiness`) is superseded by this and deleted (F260). F269
builds the contract. Reverse by deleting this paragraph.

### DECISION amend0905-vocab D10 (2026-09-05, operator order amend0905-vocab-rebuild) — history apply

Every passed task lands as one commit on the job worktree branch `remedy/<job id>`
(the branch `packages/orchestration/worktrees.py` already creates with
`git worktree add -b`; message: task title + contract state). `job apply --approve`
copies files as today; `job apply --approve --with-history` merges those commits
into the operator's current branch instead. Remedy never commits on the operator's
branch by itself; `--with-history` is an operator command. Non-git targets (staging
copies) support copy only. F270 builds this. Reverse by deleting this paragraph.

### DECISION F259 D1 (2026-09-05, operator order amend0905-vocab-rebuild) — F263's command is `absorb`
The candidates were `absorb`, `sync`, `refresh`. `sync` claims a two-way
operation the feature does not perform (nothing flows from Remedy INTO the
human's edit); `refresh` describes the effect on a view, not on the evidence
chain. `absorb` says what happens: the human change is taken into the run as a
certified fact. F263 ships `remedy absorb`; T2_F263.md carries the final name.
Reverse by deleting this paragraph.

### DECISION F259 D2 (2026-09-05, operator order amend0905-vocab-rebuild) — `task-file` and `job-file` collapse into `order`
Today `remedy do --task-file` (`packages/orchestration/pingpong_loop.load_task_file`)
and the "job file" `packages/orchestration/pingpong_job.parse_job_file` parses are
two spellings of the same thing: a Markdown file a human hands Remedy. Under D1 that
thing is an Order. Both words are deleted; the file is "an order file" and the
argument is `remedy do <order>` where `<order>` is text or a `.md` path (D4). F261
performs the rename. Reverse by deleting this paragraph.
