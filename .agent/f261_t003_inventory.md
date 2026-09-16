# F261 T003 inventory — the prune to DECISION amend0905-vocab D4

Measured at `80e9cc0f` by the reviewer's research helper of session 38, read-only, and NOT
re-verified by the reviewer: sizes are estimates and every round re-measures its own slice before
it is authored. Written by F261 round 13; the order below is a proposal the rounds follow unless
a measurement contradicts it.

## The catalog at `80e9cc0f`

44 groups and 207 commands. After round 13 the `plan` group is the hidden `roadmap` group. The
groups D4 does not name, with their command counts: context 1, context-pack 1, contract 3,
dashboard 2, guide 1, loop 3, orchestrator 4, policy 3, propose 7, queue 4, readiness 2, repair 6,
repo 2, review 4, rollback 2, token 4. Beyond D4's lists today: `do` continue, evidence,
job-resume, repair-attest, replan, report, run; `job` attach-repo, cancel, create, enqueue,
fulfill, pause, permit, rerun, resume-queue; `mission` ledger; `worker` run.

## Findings of the measurement

1. `do report <run_id>` and `do report list` already are D4's `run show <id>` and `run list`, so
   they are renamed rather than deleted; no `run` group exists yet.
2. `do job-resume` resumes a job plan through `resume_job_plan`, while `job resume` is the F047
   checkpoint resume: two commands, one D4 word.
3. `--builder` and `--reviewer` are the only route into the ping-pong path of `do run` and the
   only provider value `job run` passes to `run_job`; `--builder-provider` is validated there
   and then dropped. Deleting the flags needs `job run` wired to the provider flags (R-0767) and
   the ping-pong path of `do run` deleted with its scope flags (R-0894).
4. `job create`, `job attach-repo` and `job permit` carry sections 3 to 6 of
   `scripts/remedy_smoke.sh` and the fixtures of `tests/test_test_runner.py`,
   `tests/orchestration/test_test_runner.py`, `tests/test_command_discovery.py` and
   `tests/test_cli_main.py`; once `job permit` is gone no CLI word grants a capability that
   `test run` and `patch apply` check.
5. Guards that change as groups go: `tests/cli/test_cli_ux.py` asserts at least 40 groups and
   names `token`, `context-pack` and `contract` as internal; `tests/test_command_catalog.py`
   requires the group `policy` and the commands `job.create`, `job.attach-repo`, `job.permit`,
   `policy.contract` and `policy.token`; every `related=` must resolve.
6. The queue heir T003 names, `mission list --status planned`, does not exist, and `run show`,
   `run list`, `worker doctor` and `job run --tasks` have no owning feature; `job contract` and
   `mission contract` belong to F269, and `--plan-only`, `--force-*` and `--step-by-step` to F268.
7. `packages/orchestration/do_continue.py` has one importer, `_cmd_do_continue`, and holds the
   `do --continue` hints R-0900 names.
8. `flight_plan`, `flight plan` and `FlightPlan` occur in about 97 lines under `apps/cli`, 27
   under `apps/ui`, 236 under `packages`, 469 under `tests` and 22 under `docs`; `JobPlan`
   already names the job record, so `FlightPlan` needs another name; the job record key
   `flight_plan`, the schema tag `flight_plan_v1`, the decision type `flight_plan_approval` and
   the planner prompt text are persisted or frozen names.

## Proposed order

| Round | Commits | Deletion round (amend0906 rule 1) |
|---|---|---|
| A | `orchestrator` · `rollback` · the `loop` command | yes |
| B | the loop modules and the report's loop reference · the `queue` command · `job_queue.py` with the F048 binding, its config keys and `queue_dir`, with a deletion paragraph naming the heirs | yes |
| C | `guide` (with the group-count guard) · `dashboard` · `repo` with its `dev status` block | yes, if their hints are deleted |
| D | `readiness` · `contract` and its hints · `policy` | no |
| E | `context` · `token` with `context-pack` · `review` | no |
| F | `do report` becomes `run show` and `run list` · `do evidence` | no |
| G | `do repair-attest` · `do job-resume` · `do replan` | mostly |
| H | the `do continue` hints, then the command and `do_continue.py`, with R-0900 | no |
| I | `propose` · `repair` | no |
| J | `job run` provider wiring (R-0767) · the ping-pong path of `do run` with its flags (R-0894) | no |
| K | the queue commands of `job` with `worker run` · `mission ledger` | mostly |
| L | `job rerun` · `job fulfill` | yes |
| M | the fixtures and the smoke spine moved off `job create` · `job create`, `job attach-repo`, `job permit` | no |
| N | `teach` becomes `teacher` · the `settings` alias | no |
| O, P | the `flight_plan` rename in two rounds: module, identifiers and schema names; job key, schema tag, decision type, prompt text, prose | no |

Ordering constraints: a hint is re-pointed or deleted in or before the commit that deletes its
command, as DECISION F261 D10 did; `related=` chains are cut in the order guide, repo,
readiness, contract, policy and `do continue` before `repair`; `do replan` goes before the
`flight_plan` rename; fixtures move before `job create` is deleted.

## Rulings the rounds must make

1. Package code orphaned by a command deletion is deleted in the same round when its only
   production importer dies; where it still feeds a cockpit section, a finding is registered.
2. A cockpit route whose payload is a deleted command's output goes with it.
3. `do run` loses only `--builder`, `--reviewer`, the flags only its ping-pong path reads and
   the scope flags; its other flags belong to F268.
4. `job run` passes `--builder-provider` and `--reviewer-provider` to `run_job`, a wiring change
   of a surviving command that needs its own DECISION.
5. `do job-resume` goes with heir `job run`, and the recoverability guard it loses is a finding.
6. `mission ledger` goes with heir the ledger `mission run` prints.
7. `job create`, `job attach-repo`, `job permit` and `job fulfill` go, with findings for the
   capability grant and the repository attach they leave to F269 and F268.
8. Findings are registered for the D4 words no feature owns: `run show` and `run list` if F261
   does not rename `do report` into them, `worker doctor`, `job run --tasks` and
   `mission list --status`.
9. The name that replaces `FlightPlan`, and no reader of the old job key, per DECISION D-A.
10. Whether `teach` becomes `teacher` in words only or also in file and function names.
11. The `settings` alias as an `aliases` field of `GroupDef` with one resolver for every group
    lookup.

## The projection

The proposal is sixteen rounds after round 13, so T003 alone reaches past F261's soft limit of
25 rounds; the session that reaches the limit owes the scope report and executes the
split-and-close default of operator amendment amend0905-throughput.
