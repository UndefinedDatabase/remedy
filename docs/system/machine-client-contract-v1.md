# Machine client contract v1

> Status (F295, 2026-10-07): built. The binding list for a program that drives Remedy through
> its command line — Luna's runner first (`docs/roadmap/design/luna-control-plane-v1.md`,
> "Gate A" and "Gate B"). `tests/cli/test_machine_client_contract.py` drives the path below end
> to end and fails when this page and that test name different things.

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
header. This is the order file the gate test writes:

```
---
max-cost-usd: 1
---
Add a line saying hello to README.md
```

Remedy refuses an order file before any step, with exit code 2: `order_file_not_found`,
`order_file_unreadable`, `order_file_empty`, `order_file_invalid_header`, and
`order_file_no_cost_cap` when neither the header nor `--max-cost-usd` sets a cost cap. An order
argument that holds whitespace is planned as text, never read as a file.

## The path, step by step

1. **Propose.** `remedy do <order file> --json --no-ui --yes` plans the order and runs its first
   job with the builder and reviewer the client names, and stops before the apply. The gate test
   adds `--no-llm` and the fake providers, and a `--deadline` that has already passed, so the
   budget stops the job and raises one decision. A run that does not finish answers `ok` false
   with `error` `step_failed` and still carries `mission_id` and `job_ids`, and exits 1.
2. **Read.** `remedy status --json` carries the digest under `client`: every project with its
   missions, every job with its state, cost and evidence, every open decision, and the jobs that
   wait for their apply. Read it as often as once a minute.
3. **Answer.** `remedy decision resolve <job> <decision> --reason <option> --json` answers a
   decision. A budget decision is answered `extend` with `--answer <limit>=<value>` for each
   raised limit, or `abandon`. After `extend`, `remedy job run <job> --json` runs the job on with
   the builder and reviewer it started with. An `extend` also answers `no` to the contract
   remainder decision the same budget stop raised, because the job runs on instead of a
   follow-up mission, and names it under `closed_decisions`.
4. **Approve and apply.** `remedy job apply <job> --approve --json` copies the reviewed result
   into the repository. Then `remedy change proof <job> --json` lists that apply under
   `job_applies`.

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

## The interface as data

`remedy client interface --json` prints what a client can rely on, read from the code at the
moment it runs: every command a client uses with its arguments and the exit codes it can reach,
what each exit code means, the envelope every answer wears, the job states, the mission status
words, the contract templates, the budget kinds, and under `digest` the tree of every key the
`client` object of `remedy status --json` can return, under its own `interface_version`, which is
`1.1`. A test reads the keys the digest's code writes and the keys a real run's digest returns,
and fails when either differs from that tree (DECISION F298 D3). Each command also names the
`error` tokens its refusal can carry; a test reads them from the command's code, the way the exit
codes are read, and fails when the code can answer a token the document does not name, or the
document names one the code cannot answer (DECISION F298 D4). Today `remedy status` and
`remedy job apply` name none: an apply that does not land still answers `"ok": true`, which F298
changes. Under `answers` it names, for every command, every top-level key an answer of that
command can carry beside the envelope's own, whether it succeeds or refuses; a test reads them
from the command's code the same way, and a test that runs the path above and each of the other
commands fails when an answer returns a key the document does not name (DECISIONs F298 D5, D6
and D7). `remedy job resume` answers in several shapes, by what it finds, so its list is the
union of all of them. Under `answer_trees` it names the keys under those keys, as trees in the
form of the digest's, for each command whose answers F298 has reached so far, today
`remedy do` and `remedy job run`; a key written `*` stands for keys that are data, such as a job id, and a mission
contract check's `spec` is left open, because its keys are the arguments of the check's kind. A
test holds each tree to the code that builds it, and the run above fails when an answer returns a
key below the top level that the trees do not name (DECISION F298 D8). Inside one major version
it only grows. The product calls this
document the machine client interface, because "contract" names a mission's acceptance criteria
and nothing else (DECISION F298 D2). The tables above are still the ones F295 wrote; F298 renders them from that
document.
