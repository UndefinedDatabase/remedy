# F272 T002 — the measured `JobPlan.status` -> `JobPlan.state` rename set

> EVIDENCE, not a prediction. Every line below was produced by RUNNING the
> suites against a `JobPlan` whose `status` was replaced by a property that
> logs its caller, per DECISION F272 D7. Line numbers are at `027bdc2c`.

## How the set was measured

1. In a disposable worktree at `027bdc2c` the dataclass field `status: str =
   JOB_PLANNED` was renamed to `state: str = JOB_PLANNED` — annotation and
   default unchanged — and a `status` property installed in its place whose
   getter, setter and `JobPlan(status=...)` constructor path append the
   CALLING frame's `<file>:<line>` to a log inside the worktree.
2. The property runs in two modes. `raise` is the procedure D7 orders: it
   raises after logging. `forward` logs and then forwards to `state`, so a
   single run enumerates EVERY site instead of stopping each test at its
   first one. The forwarding run is an accelerator; the proof is the raising
   run below, which is the one that has to be EXIT 0.
3. Sites the running suite cannot reach were added from a receiver-TYPE
   sweep (`annotation`) and by reading the consumers of each renamed
   production line (`stand-in`). Both classes are listed separately below,
   because nothing catches them if they are wrong.

## The runs

| run | command | exit | reading |
|---|---|---|---|
| probe, raising, nothing renamed | `tests/orchestration/ tests/cli/` | 1 | `766 failed, 13514 passed, 10 skipped, 95 errors` — 40 sites logged before the first raise in each test masked the rest |
| probe, forwarding | `tests/orchestration/ tests/cli/` | 1 | `1 failed, 14374 passed, 10 skipped` — 218 sites logged; the single failure is the lint ceiling, which the scaffolding itself trips |
| probe, forwarding | the rest of `tests/` | 1 | `2 failed, 5355 passed` — 32 sites, one of them new; both failures are red at base and are not rename effects |
| probe, raising, set applied | `tests/orchestration/ tests/cli/` | 1 | `15 failed` — an EMPTY site log with 14 failures in `test_final_audit_evidence.py`, which is what an unfound STAND-IN looks like |
| probe, raising, stand-ins added | `tests/orchestration/ tests/cli/` | 1 | `1 failed, 14374 passed` — empty log, lint ceiling only |
| probe, raising, scaffolding made lint-clean | `tests/orchestration/ tests/cli/` | **0** | `14375 passed, 10 skipped` — EMPTY SITE LOG. This is the convergence. |
| probe, raising | the rest of `tests/` | 1 | `2 failed, 5356 passed` — empty site log; the two failures are the base-red `ui_contracts` tests below |

Two tests are RED AT BASE at `027bdc2c` and were reproduced red in the
unmodified primary checkout before any edit — they are not this round's:
`tests/ui_contracts/test_digest_card_copy.py::TestEveryRunStateIsAccountedFor::test_all_seven_run_states_are_named_by_the_label_map` and
`tests/ui_contracts/test_job_digest_card_contract.py::TestTheTriggerRuleIsPureAndPortless::test_all_seven_run_states_are_accounted_for_in_the_rule`.
They sit outside every suite this round's gates order.

## What did NOT move (DECISION F272 D5)

- The stored JSON key stays `"status"`: `_export_job` emits `"status": job.state`
  and `_import_job` reads `state=data.get("status", JOB_PLANNED)`, so every
  record already on disk still loads.
- The six `JOB_*` constants keep their names, values and type.
- `TaskEntry.status`, `ApplyManifest.status`, a promotion result's `job_status`,
  an episode's `status`, and every name merely CONTAINING `status`
  (`final_status`, `worktree_cleanup_status`, `job_status`) are untouched.

## Totals

| classification | sites |
|---|---|
| `annotation` | 5 |
| `field` | 1 |
| `probe` | 219 |
| `stand-in` | 9 |
| **total** | **234** |

35 files changed. Per file:

| file | sites |
|---|---|
| `apps/cli/commands/do_cmd.py` | 8 |
| `apps/cli/commands/job_stop_cmd.py` | 10 |
| `packages/orchestration/job_evidence.py` | 10 |
| `packages/orchestration/job_promote.py` | 3 |
| `packages/orchestration/pingpong_job.py` | 33 |
| `packages/orchestration/run_manifest.py` | 1 |
| `packages/orchestration/self_use_findings.py` | 1 |
| `packages/orchestration/self_use_runner.py` | 1 |
| `packages/orchestration/ui_server.py` | 1 |
| `tests/cli/test_job_rerun_manifest.py` | 8 |
| `tests/cli/test_job_stop.py` | 5 |
| `tests/orchestration/test_budget_guard.py` | 1 |
| `tests/orchestration/test_episode_snapshot_lifecycle.py` | 6 |
| `tests/orchestration/test_f018_authority_integration.py` | 22 |
| `tests/orchestration/test_f018_package_pipeline_e2e.py` | 4 |
| `tests/orchestration/test_failure_wiring.py` | 2 |
| `tests/orchestration/test_final_audit_evidence.py` | 3 |
| `tests/orchestration/test_job_evidence.py` | 2 |
| `tests/orchestration/test_job_promote.py` | 23 |
| `tests/orchestration/test_job_promote_consistency.py` | 1 |
| `tests/orchestration/test_job_stop_integration.py` | 26 |
| `tests/orchestration/test_job_task_runner.py` | 26 |
| `tests/orchestration/test_job_worktree_handoff.py` | 7 |
| `tests/orchestration/test_job_worktree_integration.py` | 6 |
| `tests/orchestration/test_job_worktree_integrity.py` | 8 |
| `tests/orchestration/test_pingpong_integration.py` | 2 |
| `tests/orchestration/test_predictive_budget.py` | 5 |
| `tests/orchestration/test_run_manifest_episode_graph.py` | 1 |
| `tests/orchestration/test_run_manifest_reference_coverage.py` | 1 |
| `tests/orchestration/test_run_manifest_runtime_truth.py` | 1 |
| `tests/orchestration/test_run_manifest_terminal_consistency.py` | 1 |
| `tests/orchestration/test_run_manifest_zero_call_expectations.py` | 1 |
| `tests/orchestration/test_self_use_findings.py` | 1 |
| `tests/orchestration/test_self_use_runner.py` | 2 |
| `tests/test_do_job_flow.py` | 1 |

## The sites

| file | line | form | enclosing scope | classification |
|---|---|---|---|---|
| `apps/cli/commands/do_cmd.py` | 1352 | attribute | `def _cmd_do_job_plan` | `annotation` |
| `apps/cli/commands/do_cmd.py` | 1618 | attribute | `def _cmd_do_job_resume` | `probe` |
| `apps/cli/commands/do_cmd.py` | 1892 | attribute | `def _build_final_audit` | `probe` |
| `apps/cli/commands/do_cmd.py` | 1939 | attribute | `def _build_final_audit` | `annotation` |
| `apps/cli/commands/do_cmd.py` | 1958 | attribute | `def _build_final_audit` | `probe` |
| `apps/cli/commands/do_cmd.py` | 2141 | getattr literal | `def _index_job_evidence` | `probe` |
| `apps/cli/commands/do_cmd.py` | 2431 | attribute | `def _build_agent_run_trace` | `probe` |
| `apps/cli/commands/do_cmd.py` | 2885 | attribute | `def _cmd_do_job_flow` | `probe` |
| `apps/cli/commands/job_stop_cmd.py` | 29 | stand-in / generated | `class _CoreJobAdapter` | `stand-in` |
| `apps/cli/commands/job_stop_cmd.py` | 32 | stand-in / generated | `def __init__` | `stand-in` |
| `apps/cli/commands/job_stop_cmd.py` | 67 | attribute | `def _print_status` | `probe` |
| `apps/cli/commands/job_stop_cmd.py` | 68 | attribute | `def _print_status` | `probe` |
| `apps/cli/commands/job_stop_cmd.py` | 74 | attribute | `def _print_status` | `probe` |
| `apps/cli/commands/job_stop_cmd.py` | 133 | attribute | `def _cmd_job_stop` | `probe` |
| `apps/cli/commands/job_stop_cmd.py` | 144 | attribute | `def _cmd_job_stop` | `probe` |
| `apps/cli/commands/job_stop_cmd.py` | 160 | attribute | `def _cmd_job_stop` | `probe` |
| `apps/cli/commands/job_stop_cmd.py` | 163 | attribute | `def _cmd_job_stop` | `probe` |
| `apps/cli/commands/job_stop_cmd.py` | 185 | attribute | `def _cmd_job_stop` | `probe` |
| `packages/orchestration/job_evidence.py` | 918 | attribute | `def _build_job_manifest` | `probe` |
| `packages/orchestration/job_evidence.py` | 939 | attribute | `def _build_job_summary_md` | `probe` |
| `packages/orchestration/job_evidence.py` | 967 | attribute | `def _build_job_summary_md` | `probe` |
| `packages/orchestration/job_evidence.py` | 1029 | attribute | `def _build_job_report_safe` | `probe` |
| `packages/orchestration/job_evidence.py` | 1080 | attribute | `def _build_job_timeline` | `probe` |
| `packages/orchestration/job_evidence.py` | 1100 | attribute | `def _check_sequencing` | `probe` |
| `packages/orchestration/job_evidence.py` | 2184 | getattr literal | `def _crosscheck_job_episodes_vs_index` | `probe` |
| `packages/orchestration/job_evidence.py` | 2198 | getattr literal | `def _crosscheck_terminal_jobplan_manifest` | `probe` |
| `packages/orchestration/job_evidence.py` | 2286 | getattr literal | `def _write_run_manifest_export` | `probe` |
| `packages/orchestration/job_evidence.py` | 2311 | attribute | `def _write_run_manifest_export` | `probe` |
| `packages/orchestration/job_promote.py` | 691 | attribute | `def promote_job` | `probe` |
| `packages/orchestration/job_promote.py` | 720 | attribute | `def promote_job` | `probe` |
| `packages/orchestration/job_promote.py` | 721 | attribute | `def promote_job` | `probe` |
| `packages/orchestration/pingpong_job.py` | 305 | dataclass field | `class JobPlan` | `field` |
| `packages/orchestration/pingpong_job.py` | 667 | attribute | `def _export_job` | `probe` |
| `packages/orchestration/pingpong_job.py` | 789 | JobPlan(status=) keyword | `def _import_job` | `probe` |
| `packages/orchestration/pingpong_job.py` | 963 | JobPlan(status=) keyword | `def parse_job_file` | `probe` |
| `packages/orchestration/pingpong_job.py` | 1014 | JobPlan(status=) keyword | `def plan_job_from_file` | `probe` |
| `packages/orchestration/pingpong_job.py` | 1250 | attribute | `def _finalize_job_workspace` | `probe` |
| `packages/orchestration/pingpong_job.py` | 1258 | attribute | `def _finalize_job_workspace` | `probe` |
| `packages/orchestration/pingpong_job.py` | 1284 | attribute | `def _finalize_job_workspace` | `probe` |
| `packages/orchestration/pingpong_job.py` | 1906 | JobPlan(status=) keyword | `def run_job` | `probe` |
| `packages/orchestration/pingpong_job.py` | 1913 | attribute | `def run_job` | `probe` |
| `packages/orchestration/pingpong_job.py` | 1938 | attribute | `def run_job` | `probe` |
| `packages/orchestration/pingpong_job.py` | 2096 | attribute | `def run_job` | `probe` |
| `packages/orchestration/pingpong_job.py` | 2102 | attribute | `def run_job` | `probe` |
| `packages/orchestration/pingpong_job.py` | 2117 | attribute | `def run_job` | `probe` |
| `packages/orchestration/pingpong_job.py` | 2369 | attribute | `def run_job` | `probe` |
| `packages/orchestration/pingpong_job.py` | 2410 | attribute | `def run_job` | `probe` |
| `packages/orchestration/pingpong_job.py` | 2416 | attribute | `def run_job` | `probe` |
| `packages/orchestration/pingpong_job.py` | 2597 | attribute | `def run_job` | `annotation` |
| `packages/orchestration/pingpong_job.py` | 2721 | attribute | `def run_job` | `annotation` |
| `packages/orchestration/pingpong_job.py` | 2734 | attribute | `def run_job` | `probe` |
| `packages/orchestration/pingpong_job.py` | 2784 | attribute | `def run_job` | `probe` |
| `packages/orchestration/pingpong_job.py` | 2790 | attribute | `def run_job` | `probe` |
| `packages/orchestration/pingpong_job.py` | 2822 | attribute | `def resume_job_plan` | `probe` |
| `packages/orchestration/pingpong_job.py` | 2843 | attribute | `def _block_job` | `probe` |
| `packages/orchestration/pingpong_job.py` | 2968 | attribute | `def export_job_report` | `probe` |
| `packages/orchestration/pingpong_job.py` | 3026 | attribute | `def format_job_report_text` | `probe` |
| `packages/orchestration/pingpong_job.py` | 3071 | attribute | `def format_job_report_text` | `probe` |
| `packages/orchestration/pingpong_job.py` | 3088 | attribute | `def format_job_report_text` | `probe` |
| `packages/orchestration/pingpong_job.py` | 3112 | attribute | `def _suggest_next_command` | `probe` |
| `packages/orchestration/pingpong_job.py` | 3114 | attribute | `def _suggest_next_command` | `probe` |
| `packages/orchestration/pingpong_job.py` | 3116 | attribute | `def _suggest_next_command` | `probe` |
| `packages/orchestration/pingpong_job.py` | 3118 | attribute | `def _suggest_next_command` | `probe` |
| `packages/orchestration/pingpong_job.py` | 3401 | attribute | `def _stop_job` | `probe` |
| `packages/orchestration/run_manifest.py` | 6509 | getattr literal | `def _job_is_resumable` | `probe` |
| `packages/orchestration/self_use_findings.py` | 51 | attribute | `def describe_self_use_run_defects` | `probe` |
| `packages/orchestration/self_use_runner.py` | 127 | attribute | `def run_next_self_use_item` | `probe` |
| `packages/orchestration/ui_server.py` | 148 | attribute | `def __init__` | `annotation` |
| `tests/cli/test_job_rerun_manifest.py` | 213 | attribute | `def test_stop_resume_complete_two_episodes_no_conflict` | `probe` |
| `tests/cli/test_job_rerun_manifest.py` | 221 | attribute | `def test_stop_resume_complete_two_episodes_no_conflict` | `probe` |
| `tests/cli/test_job_rerun_manifest.py` | 260 | attribute | `def test_manifest_write_failure_leaves_the_stop_request_pending` | `probe` |
| `tests/cli/test_job_rerun_manifest.py` | 272 | attribute | `def test_manifest_write_failure_leaves_the_stop_request_pending` | `probe` |
| `tests/cli/test_job_rerun_manifest.py` | 296 | attribute | `def test_pre_f012_completed_job_is_legacy_not_corrupt` | `probe` |
| `tests/cli/test_job_rerun_manifest.py` | 313 | attribute | `def test_marked_completed_job_without_manifest_is_blocking` | `probe` |
| `tests/cli/test_job_rerun_manifest.py` | 583 | attribute | `def test_completed_resume_episode_has_only_its_own_calls` | `probe` |
| `tests/cli/test_job_rerun_manifest.py` | 592 | attribute | `def test_completed_resume_episode_has_only_its_own_calls` | `probe` |
| `tests/cli/test_job_stop.py` | 91 | attribute | `def test_stopping_an_already_stopped_job_creates_no_new_trap_request` | `probe` |
| `tests/cli/test_job_stop.py` | 105 | attribute | `def test_the_human_already_stopped_message_is_honest` | `probe` |
| `tests/cli/test_job_stop.py` | 142 | attribute | `def test_status_distinguishes_none_pending_and_consumed` | `probe` |
| `tests/cli/test_job_stop.py` | 152 | attribute | `def test_status_shows_the_archived_history_of_a_resumed_job` | `probe` |
| `tests/cli/test_job_stop.py` | 197 | attribute | `def test_a_completed_job_is_not_told_that_work_will_stop` | `probe` |
| `tests/orchestration/test_budget_guard.py` | 781 | JobPlan(status=) keyword | `def _drive` | `probe` |
| `tests/orchestration/test_episode_snapshot_lifecycle.py` | 85 | attribute | `def test_failed_snapshot_capture_blocks_before_any_provider_call` | `probe` |
| `tests/orchestration/test_episode_snapshot_lifecycle.py` | 86 | attribute | `def test_failed_snapshot_capture_blocks_before_any_provider_call` | `probe` |
| `tests/orchestration/test_episode_snapshot_lifecycle.py` | 91 | attribute | `def test_failed_snapshot_capture_blocks_before_any_provider_call` | `probe` |
| `tests/orchestration/test_episode_snapshot_lifecycle.py` | 119 | attribute | `def test_failed_workspace_tree_capture_is_a_snapshot_failure` | `probe` |
| `tests/orchestration/test_episode_snapshot_lifecycle.py` | 143 | attribute | `def test_stopped_manifest_snapshot_and_calls_share_one_episode` | `probe` |
| `tests/orchestration/test_episode_snapshot_lifecycle.py` | 164 | attribute | `def test_pre_work_stop_uses_one_coherent_episode` | `probe` |
| `tests/orchestration/test_f018_authority_integration.py` | 839 | attribute | `def test_zero_limit_blocks` | `probe` |
| `tests/orchestration/test_f018_authority_integration.py` | 847 | attribute | `def test_negative_limit_blocks` | `probe` |
| `tests/orchestration/test_f018_authority_integration.py` | 855 | attribute | `def test_boolean_limit_blocks` | `probe` |
| `tests/orchestration/test_f018_authority_integration.py` | 863 | attribute | `def test_string_limit_blocks` | `probe` |
| `tests/orchestration/test_f018_authority_integration.py` | 871 | attribute | `def test_float_limit_blocks` | `probe` |
| `tests/orchestration/test_f018_authority_integration.py` | 879 | attribute | `def test_unknown_field_blocks` | `probe` |
| `tests/orchestration/test_f018_authority_integration.py` | 887 | attribute | `def test_naive_deadline_blocks` | `probe` |
| `tests/orchestration/test_f018_authority_integration.py` | 1021 | JobPlan(status=) keyword | `def test_jobplan_budget_stop_creates_decision` | `probe` |
| `tests/orchestration/test_f018_authority_integration.py` | 1064 | JobPlan(status=) keyword | `def test_repeated_list_no_duplicates` | `probe` |
| `tests/orchestration/test_f018_authority_integration.py` | 1096 | JobPlan(status=) keyword | `def test_stopped_job_refuses_budget_flags` | `probe` |
| `tests/orchestration/test_f018_authority_integration.py` | 1102 | attribute | `def test_stopped_job_refuses_budget_flags` | `probe` |
| `tests/orchestration/test_f018_authority_integration.py` | 1113 | JobPlan(status=) keyword | `def test_run_job_rejects_budget_on_stopped` | `probe` |
| `tests/orchestration/test_f018_authority_integration.py` | 1128 | JobPlan(status=) keyword | `def test_run_job_accepts_budget_on_non_stopped` | `probe` |
| `tests/orchestration/test_f018_authority_integration.py` | 1475 | attribute | `def test_valid_schema_version_passes` | `probe` |
| `tests/orchestration/test_f018_authority_integration.py` | 1525 | attribute | `def test_zero_count_no_sources_passes` | `probe` |
| `tests/orchestration/test_f018_authority_integration.py` | 1534 | attribute | `def test_unparseable_value_blocks` | `probe` |
| `tests/orchestration/test_f018_authority_integration.py` | 1537 | attribute | `def test_unparseable_value_blocks` | `probe` |
| `tests/orchestration/test_f018_authority_integration.py` | 1543 | attribute | `def test_naive_datetime_blocks` | `probe` |
| `tests/orchestration/test_f018_authority_integration.py` | 1546 | attribute | `def test_naive_datetime_blocks` | `probe` |
| `tests/orchestration/test_f018_authority_integration.py` | 1552 | attribute | `def test_valid_iso_utc_passes` | `probe` |
| `tests/orchestration/test_f018_authority_integration.py` | 1555 | attribute | `def test_valid_iso_utc_passes` | `probe` |
| `tests/orchestration/test_f018_authority_integration.py` | 1689 | attribute | `def test_three_calls_then_stop` | `probe` |
| `tests/orchestration/test_f018_package_pipeline_e2e.py` | 461 | JobPlan(status=) keyword | `def test_stopped_job_with_pending_stop_blocks` | `probe` |
| `tests/orchestration/test_f018_package_pipeline_e2e.py` | 487 | JobPlan(status=) keyword | `def test_stopped_job_without_pending_stop_proceeds` | `probe` |
| `tests/orchestration/test_f018_package_pipeline_e2e.py` | 514 | JobPlan(status=) keyword | `def test_corrupt_budget_does_not_stamp_first_running_at` | `probe` |
| `tests/orchestration/test_f018_package_pipeline_e2e.py` | 531 | attribute | `def test_corrupt_budget_does_not_stamp_first_running_at` | `probe` |
| `tests/orchestration/test_failure_wiring.py` | 504 | attribute | `def test_a_workspace_acquisition_failure_emits_one_job_postmortem` | `probe` |
| `tests/orchestration/test_failure_wiring.py` | 836 | attribute | `def test_a_failed_job_record_survives_reload_and_blocks_the_package` | `probe` |
| `tests/orchestration/test_final_audit_evidence.py` | 18 | stand-in / generated | `def __init__` | `stand-in` |
| `tests/orchestration/test_final_audit_evidence.py` | 252 | stand-in / generated | `class FakePlan` | `stand-in` |
| `tests/orchestration/test_final_audit_evidence.py` | 276 | stand-in / generated | `class FakePlan` | `stand-in` |
| `tests/orchestration/test_job_evidence.py` | 260 | attribute | `def test_does_not_mutate_job_state` | `probe` |
| `tests/orchestration/test_job_evidence.py` | 267 | attribute | `def test_does_not_mutate_job_state` | `probe` |
| `tests/orchestration/test_job_promote.py` | 200 | JobPlan(status=) keyword | `def test_missing_run_id_blocks` | `probe` |
| `tests/orchestration/test_job_promote.py` | 226 | JobPlan(status=) keyword | `def test_bad_reviewer_verdict_blocks` | `probe` |
| `tests/orchestration/test_job_promote.py` | 252 | JobPlan(status=) keyword | `def test_failed_tests_block` | `probe` |
| `tests/orchestration/test_job_promote.py` | 279 | JobPlan(status=) keyword | `def test_target_mutation_blocks` | `probe` |
| `tests/orchestration/test_job_promote.py` | 307 | JobPlan(status=) keyword | `def test_traversal_path_blocks` | `probe` |
| `tests/orchestration/test_job_promote.py` | 338 | JobPlan(status=) keyword | `def test_env_file_blocks` | `probe` |
| `tests/orchestration/test_job_promote.py` | 448 | JobPlan(status=) keyword | `def test_approve_blocks_traversal` | `probe` |
| `tests/orchestration/test_job_promote.py` | 478 | JobPlan(status=) keyword | `def test_approve_blocks_sensitive_paths` | `probe` |
| `tests/orchestration/test_job_promote.py` | 704 | JobPlan(status=) keyword | `def test_workspace_source_symlink_blocks` | `probe` |
| `tests/orchestration/test_job_promote.py` | 748 | JobPlan(status=) keyword | `def test_workspace_parent_symlink_blocks` | `probe` |
| `tests/orchestration/test_job_promote.py` | 794 | JobPlan(status=) keyword | `def test_target_dest_symlink_escape_blocks` | `probe` |
| `tests/orchestration/test_job_promote.py` | 839 | JobPlan(status=) keyword | `def test_no_apply_manifest_blocks` | `probe` |
| `tests/orchestration/test_job_promote.py` | 873 | JobPlan(status=) keyword | `def test_empty_apply_manifest_blocks` | `probe` |
| `tests/orchestration/test_job_promote.py` | 911 | JobPlan(status=) keyword | `def test_pending_apply_manifest_blocks` | `probe` |
| `tests/orchestration/test_job_promote.py` | 1128 | JobPlan(status=) keyword | `def _make_baselined_job` | `probe` |
| `tests/orchestration/test_job_promote.py` | 1180 | JobPlan(status=) keyword | `def _make_new_file_job` | `probe` |
| `tests/orchestration/test_job_promote.py` | 1345 | JobPlan(status=) keyword | `def test_legacy_new_file_allows` | `probe` |
| `tests/orchestration/test_job_promote.py` | 1388 | JobPlan(status=) keyword | `def test_legacy_existing_file_blocks` | `probe` |
| `tests/orchestration/test_job_promote.py` | 1625 | JobPlan(status=) keyword | `def test_dest_parent_symlink_blocks_promote` | `probe` |
| `tests/orchestration/test_job_promote.py` | 1695 | JobPlan(status=) keyword | `def test_dest_becomes_symlink_after_plan` | `probe` |
| `tests/orchestration/test_job_promote.py` | 1936 | JobPlan(status=) keyword | `def test_dest_parent_symlink_via_grouped_cli` | `probe` |
| `tests/orchestration/test_job_promote.py` | 2017 | JobPlan(status=) keyword | `def _make_two_file_baselined_job` | `probe` |
| `tests/orchestration/test_job_promote.py` | 2227 | JobPlan(status=) keyword | `def _make_partially_blocked_job` | `probe` |
| `tests/orchestration/test_job_promote_consistency.py` | 89 | attribute | `def _run_job` | `probe` |
| `tests/orchestration/test_job_stop_integration.py` | 175 | attribute | `def test_a_stop_requested_while_the_job_is_idle_costs_zero_provider_calls` | `probe` |
| `tests/orchestration/test_job_stop_integration.py` | 195 | attribute | `def test_the_stopped_job_reloads_from_disk_as_stopped` | `probe` |
| `tests/orchestration/test_job_stop_integration.py` | 214 | attribute | `def test_a_stop_during_the_builder_call_lets_that_call_finish_and_starts_no_reviewer` | `probe` |
| `tests/orchestration/test_job_stop_integration.py` | 231 | attribute | `def test_a_stop_during_the_reviewer_call_starts_no_repair_round` | `probe` |
| `tests/orchestration/test_job_stop_integration.py` | 245 | attribute | `def test_a_stop_before_the_parse_retry_leaves_the_malformed_response_alone` | `probe` |
| `tests/orchestration/test_job_stop_integration.py` | 261 | attribute | `def test_a_stop_is_never_dressed_up_as_a_failure` | `probe` |
| `tests/orchestration/test_job_stop_integration.py` | 285 | attribute | `def test_an_applied_task_stays_applied_and_the_next_one_never_starts` | `probe` |
| `tests/orchestration/test_job_stop_integration.py` | 299 | attribute | `def test_a_stopped_job_resumes_at_the_first_pending_task` | `probe` |
| `tests/orchestration/test_job_stop_integration.py` | 306 | attribute | `def test_a_stopped_job_resumes_at_the_first_pending_task` | `probe` |
| `tests/orchestration/test_job_stop_integration.py` | 320 | attribute | `def test_stop_resume_stop_is_two_distinct_episodes` | `probe` |
| `tests/orchestration/test_job_stop_integration.py` | 328 | attribute | `def test_stop_resume_stop_is_two_distinct_episodes` | `probe` |
| `tests/orchestration/test_job_stop_integration.py` | 360 | attribute | `def test_an_unwritable_stop_postmortem_blocks_instead_of_faking_a_clean_stop` | `probe` |
| `tests/orchestration/test_job_stop_integration.py` | 457 | stand-in / generated | `module level` | `probe` |
| `tests/orchestration/test_job_stop_integration.py` | 622 | attribute | `def test_a_pending_stop_is_honoured_before_the_workspace_is_even_acquired` | `probe` |
| `tests/orchestration/test_job_stop_integration.py` | 647 | attribute | `def _fail_on_the_stopped_write` | `probe` |
| `tests/orchestration/test_job_stop_integration.py` | 660 | attribute | `def test_a_failing_job_persist_leaves_the_request_pending` | `probe` |
| `tests/orchestration/test_job_stop_integration.py` | 669 | attribute | `def test_a_failing_job_persist_leaves_the_request_pending` | `probe` |
| `tests/orchestration/test_job_stop_integration.py` | 697 | attribute | `def test_an_archive_failure_creates_no_consumed_episode` | `probe` |
| `tests/orchestration/test_job_stop_integration.py` | 715 | attribute | `def test_an_archive_failure_creates_no_consumed_episode` | `probe` |
| `tests/orchestration/test_job_stop_integration.py` | 749 | attribute | `def _persist_then_crash` | `probe` |
| `tests/orchestration/test_job_stop_integration.py` | 767 | attribute | `def test_every_crash_window_converges_to_exactly_one_episode` | `probe` |
| `tests/orchestration/test_job_stop_integration.py` | 773 | attribute | `def test_every_crash_window_converges_to_exactly_one_episode` | `probe` |
| `tests/orchestration/test_job_stop_integration.py` | 792 | attribute | `def test_a_failed_acknowledgement_leaves_a_stopped_job_and_no_duplicates` | `probe` |
| `tests/orchestration/test_job_stop_integration.py` | 798 | attribute | `def test_a_failed_acknowledgement_leaves_a_stopped_job_and_no_duplicates` | `probe` |
| `tests/orchestration/test_job_stop_integration.py` | 836 | attribute | `def test_an_ordinary_run_json_has_no_stop_block` | `probe` |
| `tests/orchestration/test_job_stop_integration.py` | 856 | attribute | `def test_a_planted_control_file_cannot_leak_a_secret_into_event_or_postmortem` | `probe` |
| `tests/orchestration/test_job_task_runner.py` | 400 | attribute | `def test_failed_task_blocks_job` | `probe` |
| `tests/orchestration/test_job_task_runner.py` | 795 | attribute | `def test_two_task_success` | `probe` |
| `tests/orchestration/test_job_task_runner.py` | 958 | attribute | `def test_parses_two_tasks` | `probe` |
| `tests/orchestration/test_job_task_runner.py` | 978 | attribute | `def test_no_tasks_blocks` | `probe` |
| `tests/orchestration/test_job_task_runner.py` | 991 | attribute | `def test_plan_file_not_found` | `probe` |
| `tests/orchestration/test_job_task_runner.py` | 995 | attribute | `def test_no_provider_call` | `probe` |
| `tests/orchestration/test_job_task_runner.py` | 1227 | attribute | `def test_target_mutation_blocks_job` | `probe` |
| `tests/orchestration/test_job_task_runner.py` | 1273 | attribute | `def test_max_tasks_gives_paused` | `probe` |
| `tests/orchestration/test_job_task_runner.py` | 1280 | attribute | `def test_paused_not_running` | `probe` |
| `tests/orchestration/test_job_task_runner.py` | 1299 | attribute | `def test_continuation_after_pause` | `probe` |
| `tests/orchestration/test_job_task_runner.py` | 1309 | attribute | `def test_continuation_after_pause` | `probe` |
| `tests/orchestration/test_job_task_runner.py` | 1316 | attribute | `def test_full_run_gives_completed` | `probe` |
| `tests/orchestration/test_job_task_runner.py` | 1569 | attribute | `def test_test_failed_but_final_pass_blocks` | `probe` |
| `tests/orchestration/test_job_task_runner.py` | 1574 | attribute | `def test_reviewer_fail_but_final_pass_blocks` | `probe` |
| `tests/orchestration/test_job_task_runner.py` | 1582 | attribute | `def test_reviewer_pass_with_findings_blocks` | `probe` |
| `tests/orchestration/test_job_task_runner.py` | 1587 | attribute | `def test_target_mutated_but_final_pass_blocks` | `probe` |
| `tests/orchestration/test_job_task_runner.py` | 1656 | attribute | `def test_pause_preserves_config` | `probe` |
| `tests/orchestration/test_job_task_runner.py` | 1682 | attribute | `def test_continuation_restores_config` | `probe` |
| `tests/orchestration/test_job_task_runner.py` | 1906 | attribute | `def test_max_rounds_persisted_on_pause` | `probe` |
| `tests/orchestration/test_job_task_runner.py` | 1925 | attribute | `def test_max_rounds_restored_on_continuation` | `probe` |
| `tests/orchestration/test_job_task_runner.py` | 1989 | attribute | `def test_provider_persisted_on_pause` | `probe` |
| `tests/orchestration/test_job_task_runner.py` | 2565 | attribute | `def test_missing_reviewer_blocks_job` | `probe` |
| `tests/orchestration/test_job_task_runner.py` | 2811 | attribute | `def test_mutation_before_apply_blocks_job` | `probe` |
| `tests/orchestration/test_job_task_runner.py` | 3068 | attribute | `def test_post_apply_mutation_blocks` | `probe` |
| `tests/orchestration/test_job_task_runner.py` | 3103 | attribute | `def test_target_mutated_result_blocks_at_gate` | `probe` |
| `tests/orchestration/test_job_task_runner.py` | 3488 | attribute | `def test_a_splittable_task_is_replaced_by_its_children` | `probe` |
| `tests/orchestration/test_job_worktree_handoff.py` | 117 | attribute | `def test_dry_run_is_ready_not_workspace_missing` | `probe` |
| `tests/orchestration/test_job_worktree_handoff.py` | 347 | attribute | `def _crashed_job` | `probe` |
| `tests/orchestration/test_job_worktree_handoff.py` | 373 | attribute | `def test_resume_uses_the_16_char_jobplan_id_and_the_same_worktree` | `probe` |
| `tests/orchestration/test_job_worktree_handoff.py` | 431 | attribute | `def test_a_crash_before_any_change_still_resumes_cleanly` | `probe` |
| `tests/orchestration/test_job_worktree_handoff.py` | 451 | attribute | `def test_a_second_crash_during_the_resumed_attempt_is_still_recoverable` | `probe` |
| `tests/orchestration/test_job_worktree_handoff.py` | 461 | attribute | `def test_a_completed_clean_job_is_not_rematerialized_by_resume` | `probe` |
| `tests/orchestration/test_job_worktree_handoff.py` | 506 | attribute | `def test_plan_run_report_evidence_promote_dry_run` | `probe` |
| `tests/orchestration/test_job_worktree_integration.py` | 124 | attribute | `def test_git_job_runs_in_worktree_mode_never_copy` | `probe` |
| `tests/orchestration/test_job_worktree_integration.py` | 140 | attribute | `def test_no_full_repository_copy_is_made_for_a_git_target` | `probe` |
| `tests/orchestration/test_job_worktree_integration.py` | 161 | attribute | `def test_task_two_sees_task_ones_accepted_change` | `probe` |
| `tests/orchestration/test_job_worktree_integration.py` | 232 | attribute | `def test_a_blocked_job_retains_the_worktree_and_releases_the_lock` | `probe` |
| `tests/orchestration/test_job_worktree_integration.py` | 261 | attribute | `def test_paused_job_is_resumable_and_second_run_reuses_the_worktree` | `probe` |
| `tests/orchestration/test_job_worktree_integration.py` | 270 | attribute | `def test_paused_job_is_resumable_and_second_run_reuses_the_worktree` | `probe` |
| `tests/orchestration/test_job_worktree_integrity.py` | 124 | attribute | `def _crashed_two_task_job` | `probe` |
| `tests/orchestration/test_job_worktree_integrity.py` | 136 | attribute | `def _crashed_two_task_job` | `probe` |
| `tests/orchestration/test_job_worktree_integrity.py` | 168 | attribute | `def test_resume_after_gc_reviews_pre_crash_and_post_resume_files` | `probe` |
| `tests/orchestration/test_job_worktree_integrity.py` | 189 | attribute | `def test_a_deleted_checkpoint_ref_blocks_instead_of_re_snapshotting` | `probe` |
| `tests/orchestration/test_job_worktree_integrity.py` | 210 | attribute | `def test_a_ref_pointing_at_the_wrong_tree_blocks` | `probe` |
| `tests/orchestration/test_job_worktree_integrity.py` | 215 | attribute | `def test_a_completed_job_drops_its_checkpoint_refs` | `probe` |
| `tests/orchestration/test_job_worktree_integrity.py` | 274 | attribute | `def test_an_unexpected_final_file_blocks_completion` | `probe` |
| `tests/orchestration/test_job_worktree_integrity.py` | 414 | attribute | `def test_0644_to_0755_survives_promotion` | `probe` |
| `tests/orchestration/test_pingpong_integration.py` | 145 | attribute | `def test_final_job_review_persisted` | `probe` |
| `tests/orchestration/test_pingpong_integration.py` | 239 | stand-in / generated | `class FakeJob` | `stand-in` |
| `tests/orchestration/test_predictive_budget.py` | 744 | attribute | `def test_a_predictive_stop_reaches_the_stopped_state` | `probe` |
| `tests/orchestration/test_predictive_budget.py` | 766 | attribute | `def test_a_reactive_cost_stop_reaches_the_stopped_state` | `probe` |
| `tests/orchestration/test_predictive_budget.py` | 785 | attribute | `def test_without_a_cost_limit_nothing_is_predicted` | `probe` |
| `tests/orchestration/test_predictive_budget.py` | 801 | attribute | `def test_with_no_price_basis_configured_nothing_is_predicted` | `probe` |
| `tests/orchestration/test_predictive_budget.py` | 909 | attribute | `def test_the_helper_reproduces_every_live_dispatch_selection` | `probe` |
| `tests/orchestration/test_run_manifest_episode_graph.py` | 219 | stand-in / generated | `def _job` | `stand-in` |
| `tests/orchestration/test_run_manifest_reference_coverage.py` | 145 | attribute | `def test_a_real_zero_call_job_publishes_complete_coverage` | `probe` |
| `tests/orchestration/test_run_manifest_runtime_truth.py` | 94 | attribute | `def test_persisted_invocation_controls_are_executed_and_recorded` | `probe` |
| `tests/orchestration/test_run_manifest_terminal_consistency.py` | 17 | stand-in / generated | `def __init__` | `stand-in` |
| `tests/orchestration/test_run_manifest_zero_call_expectations.py` | 213 | attribute | `def test_a_pre_work_stop_is_a_valid_zero_call_reference` | `probe` |
| `tests/orchestration/test_self_use_findings.py` | 61 | attribute | `def test_a_blocked_run_surfaces_the_jobs_own_error_text` | `probe` |
| `tests/orchestration/test_self_use_runner.py` | 99 | attribute | `def test_it_runs_the_planned_item_to_completion` | `probe` |
| `tests/orchestration/test_self_use_runner.py` | 281 | attribute | `def test_a_generated_item_plans_and_runs` | `probe` |
| `tests/test_do_job_flow.py` | 1197 | stand-in / generated | `def __init__` | `stand-in` |

## The `annotation` sites — no test executes these

The probe never reached them, so the suite cannot catch a mistake here. Each
was read in its source before renaming and its receiver is a JobPlan by
construction, not by spelling:

| site | why it is a JobPlan |
|---|---|
| `apps/cli/commands/do_cmd.py:1352` | inside `_cmd_do_job_plan`, on the job `plan_job_from_file` just returned |
| `apps/cli/commands/do_cmd.py:1939` | inside `_build_final_audit`, the SAME parameter the probe named at 1892 and 1958 |
| `packages/orchestration/pingpong_job.py:2597` | inside `run_job`, an exception path on the job that function owns |
| `packages/orchestration/pingpong_job.py:2721` | inside `run_job`, the budget-exhausted path on the same job |
| `packages/orchestration/ui_server.py:148` | `_JobPlanAdapter.__init__`; its only production construction site is `_JobPlanAdapter(plan)` at `ui_server.py:259`, where `plan` is `load_job_plan(...)` |

## The `stand-in` sites — no type analysis can find these

A structural double carries its own `status`; renaming the production line it
feeds without renaming the double leaves the double silently wrong:

| file | what it is |
|---|---|
| `apps/cli/commands/job_stop_cmd.py` | _CoreJobAdapter — presents a Core Job as the interface `_cmd_job_stop` expects |
| `tests/orchestration/test_final_audit_evidence.py` | _FakeJob and two FakePlan classes — doubles for `_build_final_audit` and `_JobPlanAdapter` |
| `tests/orchestration/test_pingpong_integration.py` | FakeJob — double for the JobPlan `_build_final_audit` reads |
| `tests/orchestration/test_run_manifest_episode_graph.py` | _J — double for `_crosscheck_job_episodes_vs_index` |
| `tests/orchestration/test_run_manifest_terminal_consistency.py` | _Job — double for `_crosscheck_terminal_jobplan_manifest` |
| `tests/test_do_job_flow.py` | _FakeJob — double for `_build_final_audit` |

`tests/test_do_job_flow.py` and `tests/orchestration/test_final_audit_evidence.py`
were found only because the suites were run: the first lives OUTSIDE the two
suites this round's gate orders and was caught by running the rest of the tree,
the second by the 14 failures its doubles produced once the production reads
moved. Neither is reachable from any static rule over receiver names or types.

## Method note for T003 and T004

The site list of a polymorphic attribute is not derivable from the source. It is
derivable from a RUN. The cost was six full suite passes; the alternative,
measured in round 9, was a change set that was wrong in both directions while
its own gate read green.
