# F300 inventory — the structure measure at the claim

Measured on `main` at `b25d87a24` (the merge of pull request 318) by the reviewer's reference
implementation of DECISION F300 D1, run in a disposable worktree against the clean primary
checkout: a Python function from its `def` line to its last line by Python's syntax tree, every
tracked text file by its lines; a function is listed above 100 lines, a file above 1,000.

## Totals

| Scope | Text files | Python functions | Functions above 100 | Files above 1,000 |
|---|---|---|---|---|
| every tracked file | 8770 | 30517 | 185 | 135 |
| `packages/`, `apps/`, `scripts/` | 821 | 4810 | 162 | 40 |

The median function in `packages/`, `apps/` and `scripts/` is 15 lines.
Above 300 lines: 16 functions; above 2,000 lines: 14 files. Python files whose syntax tree could not be read: 0.

By area, functions above 100 lines: `apps/cli/` 20, `packages/` 132, `scripts/` 10; files above 1,000 lines: `apps/cli/` 3, `apps/ui/` 4, `packages/` 31, `scripts/` 2.

`apps/ui/package-lock.json` is written by npm, not by hand. Outside these three folders the
large files are append-only records under `.agent/`, evidence copies under `.data/`, tests and
documents.

## Functions above 100 lines in `packages/`, `apps/` and `scripts/`

| Lines | File:line | Function |
|---|---|---|
| 1665 | `packages/orchestration/pingpong_job.py:2615` | `run_job` |
| 1318 | `packages/orchestration/pingpong_loop.py:2907` | `run_pingpong` |
| 910 | `packages/orchestration/decision_queue.py:154` | `list_decisions` |
| 718 | `packages/orchestration/job_evidence.py:228` | `export_job_evidence` |
| 455 | `packages/orchestration/ui_server.py:3280` | `_RemedyHandler._handle_command_submission` |
| 438 | `apps/cli/commands/decision.py:245` | `_cmd_decision_resolve` |
| 423 | `packages/orchestration/long_run_executor.py:1394` | `run_cycles` |
| 406 | `packages/orchestration/orchestrator_loop.py:972` | `run_mission` |
| 355 | `apps/cli/commands/worker_facade_cmd.py:190` | `doctor_core_report` |
| 352 | `packages/orchestration/job_apply.py:1659` | `_apply_from_workspace` |
| 334 | `scripts/build_review_manifest.py:3125` | `build_manifest_from_snapshot` |
| 320 | `packages/orchestration/trust_report.py:64` | `summarize_trust_report` |
| 320 | `packages/orchestration/ui_server.py:795` | `_build_dashboard` |
| 317 | `scripts/build_review_zip.py:303` | `main` |
| 312 | `packages/orchestration/test_execution_service.py:596` | `execute_test_run` |
| 303 | `packages/orchestration/run_manifest.py:1951` | `_collect_calls` |
| 300 | `packages/orchestration/repository_snapshot.py:1333` | `revert_repository_apply` |
| 299 | `packages/orchestration/final_verifier.py:779` | `build_final_verifier_report` |
| 282 | `apps/cli/commands/job.py:912` | `_cmd_run_next_task_local` |
| 280 | `packages/orchestration/patch_apply.py:101` | `apply_patch_intent` |
| 279 | `packages/orchestration/repository_snapshot.py:394` | `create_snapshot` |
| 276 | `packages/orchestration/do_sequence.py:360` | `plan_order_job` |
| 275 | `packages/orchestration/diff_parser.py:461` | `parse_unified_diff_to_view` |
| 271 | `apps/cli/commands/job.py:2027` | `_cmd_job_budget` |
| 247 | `packages/orchestration/token_truth.py:283` | `build_token_truth` |
| 236 | `packages/orchestration/job_evidence.py:2757` | `create_manual_completion_bundle` |
| 235 | `apps/cli/commands/job.py:1665` | `_cmd_resume` |
| 235 | `packages/orchestration/run_manifest.py:2999` | `validate_run_manifest` |
| 231 | `packages/orchestration/ui_server.py:2996` | `_RemedyHandler.do_GET` |
| 221 | `scripts/build_review_manifest.py:1895` | `_gate_semantic_problems` |
| 220 | `packages/orchestration/job_apply.py:1389` | `apply_job` |
| 220 | `scripts/build_review_manifest.py:1144` | `validate_manual_completion` |
| 217 | `packages/orchestration/verifier.py:127` | `verify_task_output` |
| 215 | `packages/runtimes/dev_server.py:1824` | `stop_recorded_runtime` |
| 211 | `packages/orchestration/pingpong_loop.py:873` | `compose_builder_prompt` |
| 209 | `packages/orchestration/proof_chain.py:541` | `build_proof_chain` |
| 206 | `apps/cli/commands/runtime_cmd.py:115` | `_serve_supervisor` |
| 205 | `apps/cli/commands/do_cmd.py:737` | `_cmd_job_run` |
| 203 | `apps/cli/grouped.py:67` | `_add_command_args` |
| 199 | `apps/cli/commands/runtime_cmd.py:562` | `_cmd_runtime_probe` |
| 195 | `packages/orchestration/ui_view_model.py:287` | `build_brain_view_model` |
| 192 | `apps/cli/commands/do_cmd.py:250` | `_cmd_do_order` |
| 190 | `packages/orchestration/context_compiler.py:741` | `compile_task_context` |
| 190 | `packages/orchestration/job_apply.py:2355` | `summarize_job_apply` |
| 190 | `packages/orchestration/pingpong_job.py:1783` | `_strict_apply_to_workspace` |
| 186 | `packages/orchestration/client_digest.py:309` | `build_client_digest` |
| 186 | `packages/orchestration/pingpong_job.py:3103` | `run_job._stop_check` |
| 186 | `packages/orchestration/source_apply.py:182` | `apply_structured_patch` |
| 184 | `packages/orchestration/pingpong_loop.py:1476` | `compose_reviewer_prompt` |
| 183 | `packages/orchestration/task_edit_runtime.py:192` | `edit_task_at_runtime` |
| 179 | `apps/cli/commands/status_cmd.py:16` | `_cmd_status` |
| 179 | `scripts/build_review_manifest.py:2822` | `validate_evidence_candidate` |
| 178 | `packages/orchestration/subtree_rerun.py:637` | `prepare_subtree_rerun` |
| 177 | `apps/cli/commands/job.py:1461` | `_cmd_job_resume` |
| 171 | `scripts/build_observability_index.py:139` | `_build_task_section` |
| 168 | `apps/cli/commands/runtime_cmd.py:392` | `_cmd_runtime_serve` |
| 168 | `packages/orchestration/builder_bridge.py:92` | `run_builder_bridge` |
| 160 | `packages/orchestration/artifact_contract_gate.py:234` | `check_worktree_artifacts` |
| 159 | `packages/orchestration/final_job_review.py:93` | `build_final_job_review` |
| 159 | `packages/orchestration/final_verifier.py:341` | `_operator_attested_tasks` |
| 159 | `packages/orchestration/project_context_coverage.py:170` | `derive_project_context_coverage` |
| 159 | `packages/orchestration/run_manifest.py:4176` | `validate_input_snapshot` |
| 159 | `packages/orchestration/self_use_runner.py:276` | `run_next_self_use_item` |
| 158 | `packages/orchestration/file_provenance.py:58` | `build_file_provenance` |
| 158 | `packages/orchestration/public_api.py:861` | `answer_public_api_post` |
| 156 | `packages/orchestration/budget_decision.py:54` | `answer_budget_decision` |
| 155 | `packages/orchestration/task_injection.py:832` | `answer_injection_shortfall` |
| 152 | `scripts/build_observability_index.py:407` | `build_observability_index` |
| 151 | `packages/orchestration/ownership_phrases.py:86` | `ownership_sentence` |
| 150 | `packages/orchestration/project_summary.py:195` | `detect_patterns` |
| 147 | `packages/orchestration/archive_plan.py:257` | `build_archive_plan` |
| 146 | `packages/orchestration/project_constitution.py:144` | `load_project_constitution` |
| 145 | `packages/orchestration/context_coverage.py:160` | `derive_context_coverage` |
| 144 | `apps/cli/commands/dev.py:59` | `_dev_status` |
| 144 | `packages/orchestration/pingpong_job.py:5352` | `_stop_job` |
| 144 | `packages/orchestration/ui_server.py:1549` | `_build_pipeline_section` |
| 143 | `packages/orchestration/pingpong_loop.py:2562` | `_call_with_retry` |
| 143 | `packages/orchestration/token_authority.py:130` | `validate_token_truth` |
| 142 | `packages/orchestration/repository_snapshot.py:1184` | `build_snapshot_truth` |
| 142 | `packages/orchestration/stream_evidence.py:619` | `run_streamed_command` |
| 142 | `packages/orchestration/worktree_resume.py:172` | `prepare_worktree_resume` |
| 141 | `packages/orchestration/job_evidence.py:2054` | `_write_run_manifest_export` |
| 141 | `packages/orchestration/ui_server.py:4472` | `_RemedyHandler._read_command_payload` |
| 140 | `apps/cli/commands/job.py:770` | `_cmd_plan_job_local` |
| 140 | `packages/orchestration/builder_bridge.py:402` | `run_builder_bridge_loop` |
| 140 | `packages/orchestration/change_set.py:52` | `derive_change_set` |
| 139 | `apps/cli/commands/do_cmd.py:444` | `_cmd_do` |
| 139 | `packages/orchestration/pingpong_job.py:860` | `_export_job` |
| 138 | `apps/cli/commands/job.py:1196` | `_cmd_job_run_cycles` |
| 138 | `scripts/build_review_manifest.py:2172` | `validate_verification_tests` |
| 137 | `packages/orchestration/run_manifest.py:2860` | `validate_call_expectation` |
| 136 | `packages/runtimes/runtime_supervisor.py:218` | `Supervisor.run` |
| 135 | `packages/orchestration/run_manifest.py:2723` | `validate_call_ledgers` |
| 134 | `packages/orchestration/project_brain_aggregate.py:63` | `build_project_brain_aggregate` |
| 134 | `packages/orchestration/token_cost_policy.py:102` | `build_token_cost_policy` |
| 133 | `packages/orchestration/pingpong_provider.py:1464` | `ClaudeCliProvider._call_reviewer_structured` |
| 133 | `packages/orchestration/ui_server.py:3933` | `_RemedyHandler._dispatch_decision_resolve` |
| 131 | `packages/orchestration/failure_stats.py:116` | `collect_failures` |
| 131 | `packages/orchestration/pingpong_loop.py:4443` | `_aggregate_usage_actuals` |
| 131 | `packages/orchestration/review_scope.py:403` | `build_review_scope_packet` |
| 131 | `packages/orchestration/run_manifest.py:5952` | `validate_index_and_tree` |
| 130 | `packages/orchestration/budget_guard.py:314` | `evaluate_budget` |
| 129 | `packages/orchestration/test_runner.py:133` | `run_tests_local` |
| 128 | `packages/orchestration/budget_guard.py:818` | `decode_persisted_budget_actuals` |
| 128 | `packages/runtimes/dev_server.py:790` | `classify_state` |
| 127 | `packages/orchestration/pingpong_loop.py:5139` | `export_pingpong_json` |
| 127 | `packages/orchestration/stream_evidence.py:377` | `capture_stream_evidence` |
| 127 | `packages/orchestration/watchdog.py:449` | `act_on_trips` |
| 126 | `packages/orchestration/artifact_contract_gate.py:396` | `build_artifact_contract_gate` |
| 125 | `packages/orchestration/exec_guard.py:413` | `run_guarded` |
| 125 | `packages/orchestration/gauntlet_runner.py:469` | `run_order` |
| 125 | `packages/orchestration/pingpong_loop.py:4820` | `_build_token_accounting` |
| 125 | `packages/orchestration/run_manifest.py:5051` | `write_run_manifest` |
| 124 | `packages/orchestration/pingpong_job.py:5596` | `_write_run_manifest_record` |
| 124 | `packages/orchestration/task_injection.py:1226` | `apply_injection_to_job` |
| 124 | `packages/orchestration/ui_server.py:1900` | `_build_live_state_json` |
| 123 | `packages/orchestration/pingpong_job.py:4494` | `export_job_report` |
| 123 | `packages/orchestration/pingpong_loop.py:4597` | `_build_provider_evidence` |
| 123 | `scripts/build_review_manifest.py:2379` | `evaluate_ready_gate_matrix` |
| 122 | `packages/orchestration/artifact_contract_gate.py:91` | `check_stream_artifacts` |
| 122 | `packages/orchestration/pingpong_job.py:1001` | `_import_job` |
| 121 | `packages/orchestration/project_summary.py:54` | `build_project_summary` |
| 120 | `packages/orchestration/pingpong_job.py:4669` | `format_job_report_text` |
| 120 | `packages/orchestration/scope_fences.py:387` | `_load_fence_spec_effective` |
| 120 | `packages/orchestration/spec_compliance.py:261` | `build_spec_compliance_checklist` |
| 120 | `packages/orchestration/study.py:193` | `run_study` |
| 119 | `packages/orchestration/memory_learn.py:35` | `learn_from_job` |
| 119 | `packages/orchestration/run_contract.py:743` | `evaluate_run_action` |
| 119 | `packages/orchestration/run_manifest.py:510` | `_read_worktree_identity` |
| 118 | `packages/orchestration/continue_from_node.py:39` | `continue_from_node` |
| 118 | `packages/orchestration/pingpong_loop.py:2770` | `_record_call_failure` |
| 118 | `packages/orchestration/task_injection.py:572` | `draft_task_injection` |
| 116 | `packages/orchestration/model_routing.py:959` | `validate_task_class_tier_overrides` |
| 114 | `packages/orchestration/orchestrator_loop.py:1605` | `execute_move` |
| 114 | `packages/orchestration/provider_token_evidence.py:106` | `validate_provider_token_evidence` |
| 113 | `packages/orchestration/job_evidence.py:1003` | `_build_job_agent_run_trace` |
| 113 | `packages/orchestration/repository_snapshot.py:680` | `verify_snapshot` |
| 112 | `apps/cli/commands/patch.py:191` | `_cmd_revert_patch_intent` |
| 112 | `packages/orchestration/pingpong_job.py:1135` | `parse_job_file` |
| 112 | `packages/orchestration/subtree_rerun.py:341` | `plan_subtree_reset` |
| 112 | `packages/orchestration/task_injection.py:1107` | `confirm_task_injection` |
| 112 | `packages/runtimes/dev_server.py:1429` | `DevServer.start` |
| 112 | `scripts/build_review_manifest.py:1030` | `_verify_task_provenance_integrity` |
| 111 | `packages/orchestration/run_manifest.py:6211` | `_verified_episode_export` |
| 111 | `packages/orchestration/run_manifest.py:1278` | `validate_job_input_definition` |
| 111 | `packages/orchestration/ui_view_model.py:629` | `build_next_action` |
| 110 | `packages/orchestration/job_plan.py:587` | `render_plan_md` |
| 110 | `packages/orchestration/run_manifest.py:4741` | `validate_ledger_chain` |
| 109 | `apps/cli/commands/init_cmd.py:62` | `_handle_init` |
| 108 | `packages/orchestration/serve_daemon.py:282` | `run_supervisor` |
| 107 | `packages/orchestration/timeline.py:275` | `_render_task_block` |
| 106 | `packages/orchestration/diff_view_source.py:93` | `build_diff_view` |
| 105 | `packages/orchestration/test_execution_service.py:1034` | `finalize_test_outcome` |
| 104 | `packages/orchestration/autonomy_loop.py:138` | `_decide` |
| 104 | `packages/orchestration/ui_view_model.py:747` | `build_story` |
| 103 | `apps/cli/commands/teacher_cmd.py:122` | `_cmd_teacher_ask` |
| 103 | `packages/orchestration/pingpong_provider.py:1703` | `ClaudeCliProvider._review_impl` |
| 102 | `packages/common/secure_fs.py:389` | `read_verified_file_at` |
| 102 | `packages/orchestration/pingpong_job.py:1505` | `_finalize_job_workspace` |
| 101 | `packages/orchestration/mission_compiler.py:347` | `compile_mission_plan` |
| 101 | `packages/orchestration/run_manifest.py:4638` | `validate_task_lifecycle_chain` |
| 101 | `packages/orchestration/ui_view_model.py:977` | `build_checklist` |

## Files above 1,000 lines in `packages/`, `apps/` and `scripts/`

| Lines | File |
|---|---|
| 6558 | `packages/orchestration/run_manifest.py` |
| 5732 | `packages/orchestration/pingpong_job.py` |
| 5708 | `apps/ui/package-lock.json` |
| 5283 | `packages/orchestration/pingpong_loop.py` |
| 4834 | `packages/orchestration/ui_server.py` |
| 3495 | `scripts/build_review_manifest.py` |
| 3128 | `apps/cli/command_catalog.py` |
| 2992 | `packages/orchestration/job_evidence.py` |
| 2544 | `packages/orchestration/job_apply.py` |
| 2483 | `apps/cli/commands/job.py` |
| 2296 | `packages/orchestration/orchestrator_loop.py` |
| 2134 | `scripts/remedy_smoke.sh` |
| 2052 | `packages/runtimes/dev_server.py` |
| 2024 | `packages/orchestration/pingpong_provider.py` |
| 1908 | `packages/orchestration/config.py` |
| 1879 | `packages/orchestration/token_ledger.py` |
| 1816 | `packages/orchestration/long_run_executor.py` |
| 1650 | `packages/orchestration/brain_detail.py` |
| 1650 | `packages/orchestration/repository_snapshot.py` |
| 1477 | `packages/orchestration/do_sequence.py` |
| 1442 | `packages/orchestration/model_routing.py` |
| 1349 | `packages/orchestration/task_injection.py` |
| 1340 | `apps/ui/src/api/diffViewModel.test.ts` |
| 1248 | `apps/cli/commands/do_cmd.py` |
| 1225 | `apps/ui/src/api/remedyApi.ts` |
| 1205 | `packages/orchestration/decision_queue.py` |
| 1199 | `packages/orchestration/context_compiler.py` |
| 1168 | `packages/orchestration/mission_dossier.py` |
| 1166 | `packages/orchestration/mission_state.py` |
| 1158 | `packages/orchestration/project_brain.py` |
| 1156 | `packages/orchestration/review_subject.py` |
| 1138 | `packages/orchestration/test_execution_service.py` |
| 1136 | `packages/orchestration/public_api.py` |
| 1133 | `packages/orchestration/run_report.py` |
| 1110 | `apps/ui/src/api/remedyApi.test.ts` |
| 1094 | `packages/orchestration/final_verifier.py` |
| 1077 | `packages/orchestration/ui_view_model.py` |
| 1071 | `packages/orchestration/command_discovery.py` |
| 1049 | `packages/orchestration/brain_viewer.py` |
| 1039 | `packages/orchestration/result_tour.py` |
