# F301 inventory — what a mission knows about its finished jobs, at the claim

Read on `main` at `fdbf0802e` (the merge of pull request 319, F300) by a read-only research pass
and checked by the reviewer at the cited symbols. No behaviour was changed to take it. "The page"
is `docs/system/structure-ledger-v1.md`; "the data root" is what
`data_paths.resolve_data_root` answers.

## 1. Where a job's findings live
| Record | Path under the data root | Writer | A finding |
|---|---|---|---|
| A task run's rounds | `runs/<run_id>/result.json` | `pingpong_loop._persist_run`, from `export_pingpong_json` | each `rounds[]` entry's `reviewer.findings[]`: `id`, `severity`, `file`, `summary` (`ReviewFinding` in `pingpong_provider.py`, strict schema `schemas/models.py`) |
| The task's evidence copy | `task_runs/<task_id>/review.json` and `repair_loop.json` inside the job's evidence export (`evidence_exports/<job_id>/` by default) | `pingpong_evidence.write_evidence_bundle`, called from `job_evidence._write_task_run_evidence` | `repair_loop.json` holds `open_findings`, `resolved_findings` and `finding_status_map` |
| The final job review | `jobs/<job_id>/final_job_review.json` | `run_job` in `pingpong_job.py`, ONLY when the job ends `completed`; shape from `final_job_review.build_final_job_review` | `{id, severity ('critical' or 'repairable'), category, message, task_id}`; ids are positional (`F-TASK-001`, `F-TESTS-001`, ...) |
| The job flow | `job_flow.json` in the evidence export | `job_evidence._write_job_flow_artifacts` | none; it holds the final audit status and missing observability artifacts |
| The final verifier | `final_verifier_report.json` in the evidence export | `final_verifier.write_final_verifier_report` | derived: it folds the final job review's findings in, so it is not a source |
| The job record | `jobs/<job_id>/job.json` | `save_job_plan` | none on `TaskEntry`: `reviewer_verdict`, `final_status`, `test_passed`, `repair_rounds_used` |

- A finding carries no status of its own. The only resolution Remedy computes is between the
  rounds of ONE run: `resolved_finding_ids` is the previous round's ids minus this round's, and
  `remaining_finding_ids` their intersection (`pingpong_loop`, the repair loop over
  `prev_ids`).
- Finding ids are chosen by the reviewer model for each run, and the final review's are
  positional, so no id is stable across jobs. Remedy mints its own only for hygiene
  (`HYG-<rule>-<path>`, from `round_hygiene_findings`) and for an empty change (`EMPTY-change`).
- A reviewer `pass` that still carries findings is refused as incoherent
  (`validate_reviewer_output`), so a task that passed has no reviewer finding left in its last
  round.
- `collect_blocked_task_findings(job, full=...)` in `pingpong_job.py` already reads the last
  round's findings of every BLOCKED task from its run record, and never raises.
- The final job review is built with `test_evidence={}` and `gate_verdicts=[]`, so in practice
  its findings are `task_verdict` findings: a task whose verdict or final status is not passing.

What "still open after its job" can mean today, and what this feature takes:
1. the findings of a completed job's `final_job_review.json`;
2. the last-round reviewer findings of each blocked task, as `collect_blocked_task_findings`
   reads them;
3. `repair_loop.json`'s `open_findings`, a copy of 2 inside the evidence folder.
Nothing links a finding to a later job, and nothing marks one resolved across jobs. The repository's
own `.agent/live_review.md` is the build process's ledger, not the product's.

## 2. Missions
- A mission is one JSON file, `missions/<project_id>/<mission_id>.json` (`mission_state.Mission`,
  `MISSION_SCHEMA_VERSION` 1; `from_json` refuses any other version). Keys: `schema_version`, `id`,
  `project_id`, `goal`, `status` (`active`, `paused`, `achieved`, `abandoned`), `job_links`,
  `dossier_ref`, `created_at`, and three written only when set: `mission_plan`, `order`,
  `contract`. Those three were added without a version bump.
- A job belongs to a mission by a `MissionJobLink` `{job_id, role, created_at}`, the role being
  `initial` or `follow_up` (`MISSION_ROLES`). The mission stores no job state; it is read live
  (`mission_job_state_label`). The job carries `mission_id` and `mission_role` in its free
  `metadata` dict.
- Job states are `RunState`'s: pending, planned, running, paused, completed, failed, cancelled,
  blocked, stopped. `JOB_TERMINAL_STATES` in `pingpong_job.py` and `TERMINAL_JOB_STATES` in the
  loop are completed, failed and cancelled. Nothing counts a mission's completed jobs today.
- The mission's plan (`mission_plan_schema.MissionPlan`) is a graph of at most 12 milestones,
  each with draft jobs that are "an OUTLINE, never a runnable job"; done milestones are kept
  under `_milestones_done`. The plan lists no real upcoming job.
- There is no mission budget record; each job carries its own `budgets`. The loop's only mission
  bound is `orchestrator.max_iterations` (default 10).

## 3. The orchestrator loop (`packages/orchestration/orchestrator_loop.py`)
- `run_mission` (406 lines, on the page with its boundary) runs one model call per iteration,
  evaluates the move (`evaluate_move`, `evaluate_dispatch`) and executes it (`execute_move`, 114
  lines, on the page WITHOUT a boundary).
- The model chooses the next job: a `dispatch_job` move names `{milestone_id, step}`. The guards
  refuse an unknown or done milestone, unmet dependencies, a milestone with a job in flight, one
  whose job completed with a released gate, and a handback with era defects.
- What the loop knows of finished jobs: per milestone, the latest job's state, gate and handback
  (`collect_milestone_evidence`), and the open decisions of all linked jobs. It never reads a
  reviewer finding or `final_job_review.json`.
- The dispatch branch of `execute_move` creates the job through `dispatch or continue_mission`,
  applies the audited unattended approval (`_auto_approve_if_gated`), attaches the milestone's
  DoD, its contract slice, the repository grant and the milestone key, RUNS the job
  (`execute_dispatched_job`, which calls `run_cycles` unattended with the job's own budgets), and
  records the contract results.

## 4. `remedy mission continue`
- `_cmd_mission_continue` in `apps/cli/commands/mission_cmd.py` resolves the project and the
  mission and calls `mission_state.continue_mission(project_id, mission_id, next_step)`; it
  prints the job, its role and the injected verify task, and never runs the job.
- `continue_mission` takes the operator's step as text, builds ONE work task
  (`build_follow_up_task`, "deliberately ONE task"), injects and asserts the verify-first task
  when there is a previous job, saves a `PLANNED` `JobPlan` with `mission_id` and `mission_role`
  in its metadata, and links it. It reads only the latest link.
- The loop's dispatch uses the same function, so both ways of adding a job to a mission meet in
  one place. Two other places link jobs: `do_sequence._step_shape` and a mission made from a
  decision (`apps/cli/commands/decision.py`).

## 5. What a person and a client see of a mission
- `remedy mission show` (`_cmd_mission_show`) prints the chain (`render_mission_chain`: index,
  job, role, live state), watchdog trips when paused, and the loop's ledger; `--json` answers the
  mission export with each link's `job_state`, the trips and the ledger.
- The client digest (`client_digest.build_client_digest`, 186 lines, on the page) gives each
  mission as `_mission_entry`: `mission_id`, `status`, `goal`, `job_ids`, `order_source_path`,
  `order_source_sha256`. The public HTTP API's `GET /api/v1/digest` answers that digest;
  `public_api.py` has no route of its own for missions.
- None of these says anything about findings across jobs or counts a mission's jobs.

## 6. The structure ledger and what this feature would touch
| On the page | Lines at `fdbf0802e` | Boundary on the page |
|---|---|---|
| `run_mission` | 406 | yes: the safe point, the context, the call and its refusals, the streak counters |
| `execute_move` | 114 | none |
| `orchestrator_loop.py` | 2296 | yes: protocol, context and milestones, ledger, move evaluation, constants first |
| `mission_state.py` | 1166 | none |
| `config.py` | 1908 | none |
| `build_client_digest` | 186 | none |
| `run_job` and `pingpong_job.py` | 1652 and 5719 | yes; `run_job` stays in its file |

`mission_cmd.py` (720 lines), `client_digest.py` (494) and `data_paths.py` (515) are not on the
page. The ratchet `tests/test_structure_ratchet.py` requires each row to equal its measure, so a
listed function or file can only shrink: a new line in one of them is red unless as many leave it
in the same commit.

## 7. "Replaced and not deleted"
- No plan, task, milestone or DoD record has a field saying what it replaces or deletes.
- `contract_hygiene.find_replaced_files(root, added)` names an added file that sits beside the file
  it replaces, by name (`_new`, `_old`, `_copy`, `_backup`, `_bak`, `_v<n>`, `new_`, `old_`,
  `.bak`, `.orig`; `replaced_originals`). The round hygiene rule turns each into a reviewer
  finding `HYG-replaced-<path>` of severity high in every round (`ROUND_HYGIENE_RULES`), and it is
  a blocking contract hygiene criterion (DECISION F269 D5).
- Nothing records a replacement whose deletion must wait.

## 8. Settings
- Every setting is a `ConfigKeySpec` in `_CONFIG_KEY_SPECS` (`config.py`), read by `get_config`,
  shown by `remedy config`, and rendered into `docs/guides/environment.md`, which
  `tests/docs/test_environment_guide.py` holds equal to the registry. The nearest model is
  `orchestrator.max_iterations` (int, default 10, `REMEDY_ORCHESTRATOR_MAX_ITERATIONS`).
- A project's own data lives under `projects/<project_id>/`; `bench_history.jsonl`
  (`bench_history.bench_history_path_for`) is an append-only JSON-lines file there.
- A project's repository is `RemyProject.canonical_repo_path`, else an entry of `repo_paths`
  (`project_registry.load_project`).

## 9. Fixtures that build a mission without a model
- `tests/orchestration/test_mission_e2e.py`: `data_root` and `mission` fixtures, a scripted
  orchestrator replaying move JSON, `_no_execution`, and `_finish_job_with_dod_met`, which marks a
  job and its tasks completed and releases its gate; it makes three jobs over two `run_mission`
  calls.
- `tests/orchestration/test_orchestrator_loop.py`: `_scripted`, the `dispatched` fixture with a
  fake dispatch, `_FakeCycleRun` and `_executed`, and a real `run_cycles` over one-task steps.
- `tests/orchestration/test_mission_state.py`: `_mission_with_a_green_first_job`, completed
  `JobPlan`s linked to a mission and followed by `continue_mission`.
- `tests/orchestration/test_pingpong_integration.py`: a real `run_job` with `FakeProvider`, which
  writes a real `final_job_review.json` without a network.
No fixture has six jobs, a planted open finding or a planted oversized file.
