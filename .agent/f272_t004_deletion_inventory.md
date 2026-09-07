# F272 T004 — the classic job-store deletion inventory

Feature F272 (One world completion), task **T004 — delete the classic runner**.
The reading was taken at commit `230c5f2cda33b720253738671d24d2ce05f3bfc1`, the commit that recorded
DECISION F272 D12, with `git status --porcelain` empty.

This file is produced by running a probe, not by composing a list. The probe is
the `INVPROBE` slice of the round 18 step block, saved verbatim at
`.agent/authored/f272-r18.md`; re-running it against a clean tree at this commit
reproduces every number and every line below.

## What was counted, and why by `ast` rather than by grep

Every tracked `.py` file — enumerated from `git ls-files`, never from a shell
glob, as DECISION F272 D2 requires — is parsed with `ast`. A file counts as a
consumer of the classic job store ONLY when it either

* imports one of the seven names `save_job`, `load_job`, `load_job_safe`,
  `list_jobs`, `list_jobs_safe`, `JobNotFoundError` or `JobStoreError` FROM
  `packages.orchestration.storage`, or
* reads one of those seven names as an attribute off that module object, under
  whatever name the file binds the module to.

A SUBSTRING GREP CANNOT DO THIS AND MISCOUNTS IN BOTH DIRECTIONS. `load_job_plan`
CONTAINS `load_job` as a substring and is the UNIFIED reader — the opposite of
what is being counted here — so a grep for `load_job` would book the new world's
readers as the old world's consumers. Reading the imports and attribute accesses
instead resolves each name to the module it actually comes from. This is the
method DECISION F272 D7 established for the `JobPlan.status` rename set, applied
to the store.

## Bucket counts and total, verbatim from the probe

```
production 72
tests 127
scripts 0
total 199
```

## Per-symbol frequency, verbatim from the probe

A file is counted once per DISTINCT symbol it uses, so these figures sum to more
than the file total.

```
symbol save_job 152
symbol load_job 105
symbol JobNotFoundError 45
symbol list_jobs 6
symbol JobStoreError 6
symbol load_job_safe 5
symbol list_jobs_safe 5
```

## The full production list, verbatim from the probe

Every file under `packages/` and `apps/`, one per line, with the symbols it uses.
Not truncated, not summarised, not re-sorted.

```
PROD apps/cli/commands/brain.py JobNotFoundError,load_job
PROD apps/cli/commands/change.py JobNotFoundError,load_job
PROD apps/cli/commands/context.py JobNotFoundError,load_job
PROD apps/cli/commands/contract_cmd.py load_job,save_job
PROD apps/cli/commands/dashboard_cmd.py JobNotFoundError,load_job
PROD apps/cli/commands/decision.py JobNotFoundError,load_job,save_job
PROD apps/cli/commands/do_cmd.py JobNotFoundError,load_job,save_job
PROD apps/cli/commands/event.py JobNotFoundError,load_job
PROD apps/cli/commands/feature_cmd.py load_job
PROD apps/cli/commands/file.py JobNotFoundError,load_job
PROD apps/cli/commands/guide.py JobNotFoundError,load_job
PROD apps/cli/commands/job.py JobNotFoundError,load_job,save_job
PROD apps/cli/commands/job_context_cmd.py JobNotFoundError,load_job
PROD apps/cli/commands/job_stop_cmd.py load_job
PROD apps/cli/commands/memory.py JobNotFoundError,load_job,save_job
PROD apps/cli/commands/patch.py JobNotFoundError,load_job,save_job
PROD apps/cli/commands/policy.py JobNotFoundError,load_job
PROD apps/cli/commands/progress_cmd.py JobNotFoundError,load_job
PROD apps/cli/commands/project.py JobNotFoundError,list_jobs,load_job,save_job
PROD apps/cli/commands/propose_cmd.py JobNotFoundError,JobStoreError,load_job
PROD apps/cli/commands/provider_cmd.py JobNotFoundError,load_job
PROD apps/cli/commands/readiness.py JobNotFoundError,load_job
PROD apps/cli/commands/repair_cmd.py JobNotFoundError,JobStoreError,load_job
PROD apps/cli/commands/repo.py JobNotFoundError,load_job
PROD apps/cli/commands/review_cmd.py JobNotFoundError,JobStoreError,load_job,save_job
PROD apps/cli/commands/snapshot_cmds.py JobNotFoundError,load_job
PROD apps/cli/commands/test_cmds.py JobNotFoundError,load_job
PROD apps/cli/commands/worker.py JobNotFoundError,load_job
PROD packages/orchestration/agent_loop.py load_job,save_job
PROD packages/orchestration/autorun.py save_job
PROD packages/orchestration/builder_routing.py JobNotFoundError,load_job
PROD packages/orchestration/candidate_quality.py JobNotFoundError,load_job
PROD packages/orchestration/continue_from_node.py save_job
PROD packages/orchestration/do_continue.py JobNotFoundError,load_job
PROD packages/orchestration/do_run.py save_job
PROD packages/orchestration/dogfood_run.py load_job
PROD packages/orchestration/external_builder_sandbox.py JobNotFoundError,load_job
PROD packages/orchestration/flight_plan.py save_job
PROD packages/orchestration/gauntlet_runner.py load_job_safe
PROD packages/orchestration/handoff.py load_job_safe
PROD packages/orchestration/job_fulfillment.py load_job,save_job
PROD packages/orchestration/local_candidate_generator.py JobNotFoundError,load_job
PROD packages/orchestration/long_run_executor.py save_job
PROD packages/orchestration/loop_run.py list_jobs_safe,save_job
PROD packages/orchestration/mission_state.py JobNotFoundError,JobStoreError,load_job,load_job_safe,save_job
PROD packages/orchestration/orchestrator_brain.py JobNotFoundError,load_job
PROD packages/orchestration/orchestrator_loop.py load_job,save_job
PROD packages/orchestration/overnight_executor.py load_job
PROD packages/orchestration/overnight_mission.py load_job
PROD packages/orchestration/overnight_readiness.py JobNotFoundError,load_job
PROD packages/orchestration/patch_apply.py save_job
PROD packages/orchestration/patch_revert.py save_job
PROD packages/orchestration/project_scope.py list_jobs_safe
PROD packages/orchestration/proposed_tasks.py list_jobs_safe,load_job,load_job_safe,save_job
PROD packages/orchestration/provider_patch_material.py JobNotFoundError,load_job
PROD packages/orchestration/provider_trust.py JobNotFoundError,load_job,save_job
PROD packages/orchestration/provider_trust_verification.py JobNotFoundError,load_job,save_job
PROD packages/orchestration/real_test_execution.py list_jobs,load_job
PROD packages/orchestration/repair_loop.py JobNotFoundError,load_job,save_job
PROD packages/orchestration/repair_loop_v2.py load_job
PROD packages/orchestration/repair_request_builder.py JobNotFoundError,load_job,save_job
PROD packages/orchestration/repository_snapshot.py JobNotFoundError,load_job
PROD packages/orchestration/review_bundle.py load_job
PROD packages/orchestration/self_dogfood.py JobNotFoundError,load_job
PROD packages/orchestration/self_dogfood_execution.py JobNotFoundError,load_job
PROD packages/orchestration/task_execution.py load_job_safe
PROD packages/orchestration/test_execution_service.py JobNotFoundError,load_job,save_job
PROD packages/orchestration/test_failure_artifact.py save_job
PROD packages/orchestration/token_economy.py load_job
PROD packages/orchestration/ui_server.py JobNotFoundError,JobStoreError,list_jobs,load_job,save_job
PROD packages/orchestration/watchdog.py load_job,save_job
PROD packages/orchestration/worker_queue.py JobNotFoundError,JobStoreError,load_job,save_job
```

## The full test list, verbatim from the probe

Every file under `tests/`, in the same form. Not truncated, not summarised.

```
TEST tests/cli/test_builder_routing_cli.py load_job,save_job
TEST tests/cli/test_decision_answers.py load_job,save_job
TEST tests/cli/test_do_continue_cli.py save_job
TEST tests/cli/test_external_builder_cli.py save_job
TEST tests/cli/test_file_provenance_cli.py save_job
TEST tests/cli/test_golden_path.py save_job
TEST tests/cli/test_job_commands.py save_job
TEST tests/cli/test_job_context_cmd.py save_job
TEST tests/cli/test_job_digest_cli.py save_job
TEST tests/cli/test_job_report.py save_job
TEST tests/cli/test_local_candidate_cli.py load_job,save_job
TEST tests/cli/test_loop_cmd.py list_jobs_safe,load_job
TEST tests/cli/test_main_builder_adapter_cli.py save_job
TEST tests/cli/test_open_decisions_view.py save_job
TEST tests/cli/test_orchestrator_brain_cli.py save_job
TEST tests/cli/test_overnight_cli.py save_job
TEST tests/cli/test_overnight_executor_cli.py save_job
TEST tests/cli/test_patch_cmd.py load_job,save_job
TEST tests/cli/test_plan_approval.py list_jobs,load_job,save_job
TEST tests/cli/test_product_spine.py save_job
TEST tests/cli/test_progress_feature_runtime.py save_job
TEST tests/cli/test_propose_cli.py load_job,save_job
TEST tests/cli/test_provider_material_cli.py save_job
TEST tests/cli/test_provider_trust_cli.py save_job
TEST tests/cli/test_provider_verification_cli.py save_job
TEST tests/cli/test_real_test_execution_cli.py save_job
TEST tests/cli/test_repair_loop_v2_cli.py save_job
TEST tests/cli/test_repair_request_cli.py save_job
TEST tests/cli/test_repair_runtime.py load_job,save_job
TEST tests/cli/test_repair_v1_cli.py save_job
TEST tests/cli/test_review_bundle_runtime.py save_job
TEST tests/cli/test_self_dogfood_cli.py load_job,save_job
TEST tests/cli/test_self_dogfood_execution_cli.py save_job
TEST tests/orchestration/test_approval_queue.py list_jobs,load_job,save_job
TEST tests/orchestration/test_autonomy.py save_job
TEST tests/orchestration/test_autorun.py save_job
TEST tests/orchestration/test_builder_routing.py load_job,save_job
TEST tests/orchestration/test_builder_visibility.py save_job
TEST tests/orchestration/test_candidate_quality.py save_job
TEST tests/orchestration/test_checkpoints.py save_job
TEST tests/orchestration/test_command_discovery.py save_job
TEST tests/orchestration/test_diff_repair_apply.py save_job
TEST tests/orchestration/test_do_continue.py load_job,save_job
TEST tests/orchestration/test_do_run.py load_job
TEST tests/orchestration/test_dod_gate.py load_job,save_job
TEST tests/orchestration/test_escalation.py load_job,save_job
TEST tests/orchestration/test_event_ledger.py save_job
TEST tests/orchestration/test_external_builder_sandbox.py load_job,save_job
TEST tests/orchestration/test_fence_production_e2e.py save_job
TEST tests/orchestration/test_handoff.py save_job
TEST tests/orchestration/test_job_fulfillment.py load_job,save_job
TEST tests/orchestration/test_local_candidate_generator.py save_job
TEST tests/orchestration/test_long_run_executor.py save_job
TEST tests/orchestration/test_loop_run.py load_job,save_job
TEST tests/orchestration/test_main_builder_adapter.py save_job
TEST tests/orchestration/test_mission_compiler.py list_jobs_safe
TEST tests/orchestration/test_mission_e2e.py load_job,save_job
TEST tests/orchestration/test_mission_state.py load_job,save_job
TEST tests/orchestration/test_model_route_tournament_integration.py save_job
TEST tests/orchestration/test_orchestrator_brain.py load_job,save_job
TEST tests/orchestration/test_overnight_executor.py load_job,save_job
TEST tests/orchestration/test_overnight_mission.py save_job
TEST tests/orchestration/test_overnight_readiness.py load_job,save_job
TEST tests/orchestration/test_project_brain.py load_job,save_job
TEST tests/orchestration/test_proposed_tasks.py load_job,save_job
TEST tests/orchestration/test_provider_patch_material.py load_job,save_job
TEST tests/orchestration/test_provider_trust.py load_job,save_job
TEST tests/orchestration/test_provider_trust_verification.py load_job,save_job
TEST tests/orchestration/test_queue_executor_binding.py load_job
TEST tests/orchestration/test_real_test_execution.py save_job
TEST tests/orchestration/test_repair_apply_cycle.py load_job,save_job
TEST tests/orchestration/test_repair_loop_hardened.py save_job
TEST tests/orchestration/test_repair_loop_v1.py load_job,save_job
TEST tests/orchestration/test_repair_loop_v2.py save_job
TEST tests/orchestration/test_repair_request_builder.py load_job,save_job
TEST tests/orchestration/test_repository_snapshot.py save_job
TEST tests/orchestration/test_resume_cli.py save_job
TEST tests/orchestration/test_resume_kill.py load_job
TEST tests/orchestration/test_review_bundle.py save_job
TEST tests/orchestration/test_self_dogfood.py load_job,save_job
TEST tests/orchestration/test_self_dogfood_execution.py load_job,save_job
TEST tests/orchestration/test_source_apply.py load_job,save_job
TEST tests/orchestration/test_source_apply_transaction.py save_job
TEST tests/orchestration/test_stop_reasons.py save_job
TEST tests/orchestration/test_structured_planner_cli.py save_job
TEST tests/orchestration/test_task_execution.py save_job
TEST tests/orchestration/test_test_failure_repair.py load_job,save_job
TEST tests/orchestration/test_token_economy.py save_job
TEST tests/orchestration/test_token_economy_integration.py save_job
TEST tests/orchestration/test_watchdog.py load_job,save_job
TEST tests/orchestration/test_worker_execution.py load_job,save_job
TEST tests/orchestration/test_worktree_lifecycle.py save_job
TEST tests/orchestration/test_worktree_resume_cli.py save_job
TEST tests/regression/test_named_bugs.py save_job
TEST tests/storage/test_persistence.py save_job
TEST tests/test_agent_loop.py save_job
TEST tests/test_agent_loop_execution.py save_job
TEST tests/test_autonomy_readiness.py save_job
TEST tests/test_brain_detail.py save_job
TEST tests/test_brain_smoke.py save_job
TEST tests/test_brain_viewer.py save_job
TEST tests/test_cli_main.py load_job,save_job
TEST tests/test_cockpit.py save_job
TEST tests/test_context_coverage.py save_job
TEST tests/test_context_pack.py save_job
TEST tests/test_execution_foundation.py save_job
TEST tests/test_grouped_cli.py save_job
TEST tests/test_memory_learn.py save_job
TEST tests/test_patch_apply.py load_job,save_job
TEST tests/test_patch_intent_approval.py load_job,save_job
TEST tests/test_project_brain.py save_job
TEST tests/test_project_constitution.py save_job
TEST tests/test_project_context_coverage.py save_job
TEST tests/test_run_log_cli.py load_job,save_job
TEST tests/test_storage.py JobNotFoundError,list_jobs,load_job,save_job
TEST tests/test_timeline.py save_job
TEST tests/test_trust_report.py save_job
TEST tests/ui_contracts/test_responsive.py save_job
TEST tests/ui_contracts/test_ux_quality.py save_job
TEST tests/ui_server/test_command_channel.py load_job,save_job
TEST tests/ui_server/test_command_dispatch.py load_job,save_job
TEST tests/ui_server/test_dashboard_contract.py save_job
TEST tests/ui_server/test_decisions_endpoint.py save_job
TEST tests/ui_server/test_diff_endpoint.py save_job
TEST tests/ui_server/test_digest_route.py save_job
TEST tests/ui_server/test_live_state.py save_job
TEST tests/ui_server/test_server_concurrency.py save_job
```

## Scripts

The probe reports `scripts 0`: no file under `scripts/` references a classic job
store symbol, so `scripts/` carries no share of this deletion.

## This is a measurement, not a plan

Nothing above stages anything. It records WHAT REFERENCES THE CLASSIC JOB STORE
at the commit named in the title, and it exists so that T004 is staged from a
number somebody measured rather than from an estimate — a 199-file blast radius
does not fit in one commit under the DECISION F104 D1 cap of 500 insertions, and
a round that discovered that halfway through would already have made the mess.
The division of T004 into rounds, the order those rounds take, and which files
travel together in a commit are the NEXT BLOCK'S JOB and are deliberately not
decided here. DECISION F260 D5's one binding constraint on that staging already
stands: the resolver collapse lands in the SAME commit range as the store
deletion, because it is a behaviour change to a shared error path and is harmless
only once the store is gone.
