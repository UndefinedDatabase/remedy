# F205 inventory — what a mission writes, and where, before it spans several repositories

Read at `c72d2a7ec` (the merge of pull request 321) from the code, for DECISION F205 D1 and the
amendment section of `docs/roadmap/features/T13_F205.md`, which orders the first round to measure
the mission's records against the data root's classes before it writes the slice list.

## The data root's classes
`packages/orchestration/data_paths.py` names every top-level child of the data root:
`EPHEMERAL_CLASSES` holds `job_workspaces` and `review_staging`; `DURABLE_CLASSES` holds `jobs`,
`workspaces`, `runs`, `job_logs`, `projects`, `missions`, `control`, `stops`, `proposed_tasks`,
`evidence_exports`, `job_evidence_index`, `job_apply_records`, `memory`, `viewers`, `ui`,
`roadmap`, `self_dogfood`, `smoke`, `serve` and `api`. `tests/test_data_root_classes.py` fails on
any new child no class holds.

## The records of one mission today

| Record | Where | Class | Keyed by | Writer |
|---|---|---|---|---|
| the mission record | `missions/<project id>/<mission id>.json` | `missions` | one project | `save_mission` (`mission_state.py`) |
| the loop's ledger | `missions/<project id>/<mission id>/evidence/` + `LEDGER_FILENAME` | `missions` | one project | `ledger_path` (`orchestrator_loop.py`) |
| the dossier, the rendered plan, the handoff report | the same evidence folder | `missions` | one project | `mission_dossier.py`, `mission_compiler.py`, `handoff.py` |
| the upkeep ledger | `projects/<project id>/upkeep_ledger.jsonl`, one `mission_id` per line | `projects` | one project | `append_upkeep_line` (`mission_upkeep.py`) |
| each job's record and evidence | `jobs/<job id>/job.json`, `jobs/<job id>/evidence/` | `jobs` | the job | `save_job_plan` (`pingpong_job.py`) |
| a follow-up's verify record | `jobs/<job id>/evidence/mission_verify.json` | `jobs` | the job | `write_mission_verify_record` |
| the token ledger | `projects/<project id>/ledger.sqlite` | `projects` | the job's project | `token_ledger.py` |
| memory cards | `memory/<project id>/memory.jsonl` | `memory` | the job's project | `packages/memory/local_gateway.py` |
| the job's worktree | one folder per job under `<repository>/.remedy-wt/` | outside the data root | the job's repository | `worktrees.create` |

## What already holds for several repositories
- A job record names its own `project_id` and `repo_path` (`JobPlan` in `pingpong_job.py`), and
  every record keyed by a job or by a job's project stays strictly in that project.
- Mission ids are `uuid4().hex`, and `mission_for_job` and `running_mission_for_order_file` already
  scan the mission area of every project, so a mission is found from any of its jobs.

## What assumes one repository
- `Mission.project_id` is one value and `MissionJobLink` names no project (`mission_state.py`).
- The order file's `project` header key is single-valued (`order_file.py`, `OrderFile.project`).
- `remedy do` resolves one project and one `repo_root` (`_step_init` in `do_sequence.py`), plans
  every job against them (`_step_shape`), and pushes once to that root (`do_push_mission`).
- The loop runs a mission under one project id (`run_mission` in `orchestrator_loop.py`), and a job
  it makes through `continue_mission` carries no `repo_path`, only `metadata["target_repo"]` from
  `grant_contract_job_repository` (`mission_contract.py`), so the public API's apply refuses it as
  `api_job_repository_unknown` (`_job_apply_argv` in `public_api.py`).
- The upkeep cadence and plan measure `project_repository(project_id)`, one repository
  (`mission_upkeep.py`).
- The client digest lists a mission under one project, and a job entry names no repository
  (`_mission_entry` and `build_client_digest` in `client_digest.py`).

## What the structure page holds
`mission_state.py` (1166 lines), `do_sequence.py`, `apps/cli/commands/do_cmd.py`,
`orchestrator_loop.py`, `job_apply.py`, `pingpong_job.py` and `public_api.py` are rows of "Files
above 1,000 lines" and may not grow; `plan_order_job`, `_cmd_do_order`, `_cmd_do`, `run_mission`
and `build_client_digest` are rows of "Functions above 100 lines". `mission_upkeep.py`,
`client_digest.py`, `orchestrator_dispatch.py`, `order_file.py` and `project_registry.py` are not.

## The fixtures that exist
`tests/cli/test_do_project_repo.py` builds two git repositories `a` and `b`, each registered by
`remedy init`, with a tripwire on model calls; `tests/cli/test_scoped_listings.py` holds the F148
two-project isolation tests. No shared fixture spans two repositories.
