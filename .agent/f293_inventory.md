# F293 T001 — Test load inventory

One full-suite measurement run, taken 2026-09-30 as F293's one full-suite run permitted by
operator amendment amend0917-throughput (taken at T001, not at closure, because T001 is the task
that needs the data). Source commands are named under each section heading. The full command
output that every reading below is drawn from is committed verbatim at
`.agent/authored/f293-r1-durations.txt` (the `--durations=0` run) and the readings below quote the
test load record at `~/.remedy-loop/test_load.jsonl`, written automatically by
`tests/conftest.py`/`tests/load_governor.py`.

## 1. Cost of collection

Command: `python3 -m pytest --collect-only -q`, timed with
`bash -c 'time python3 -m pytest --collect-only -q; echo REAL_EXIT=$?'`.

- Collected: **21102 tests** (pytest's own summary line: "21102 tests collected in 4.64s").
- pytest's own internal collection time: **4.64s**.
- Wall-clock around the whole process (`time`'s `real`): **5.965s** (`user` 5.790s, `sys` 0.171s —
  the gap against pytest's own 4.64s is Python/import startup outside pytest's own collection
  phase).
- Exit code: 0.
- This collected count (21102) matches the `collected` field the full run below wrote into the
  test load record, so collection is stable between the two invocations.

## 2. CPU share per test file

Command used to produce the raw numbers: `python3 -m pytest -n auto -q --durations=0`, output
captured verbatim at `.agent/authored/f293-r1-durations.txt`; the ranking below groups every
`<seconds>s <phase> <nodeid>` line of that file by the nodeid's file (the part before `::`) and
sums the seconds per file, ranked descending. 10814 duration lines were parsed across 575 distinct
files; the file below shows the top 30.

**Approximation caveat, stated explicitly as ordered:** this is NOT true per-process CPU time. It
is the sum of wall-clock durations `pytest --durations` reports for `setup`, `call` and
`teardown` phases of each test, and the run itself executed under `-n auto` (6-worker cap,
amend0930-test-load), so several tests' wall-clock windows overlapped inside the same wall-clock
second; pytest-xdist reports no per-worker CPU figure per test, only wall time per phase. A file's
summed seconds therefore over-counts true CPU seconds whenever its tests ran concurrently with
each other or with other files' tests on different workers, and under-counts nothing (each phase
of each test is counted exactly once). The test load record's own reading for this run is the
authoritative total, not this table: `collected` 21102, `wall_seconds` 355.02, `cpu_seconds`
1246.09, `workers` 6 (from `~/.remedy-loop/test_load.jsonl`'s newest line at the time of this run).
This table is a relative ranking of files against each other, not an absolute CPU budget.

### CPU share per test file (top 30)

| Rank | File | Summed durations (s) | Duration-line count |
|---|---|---|---|
| 1 | `tests/cli/test_worker_facade_cmd.py` | 125.54 | 40 |
| 2 | `tests/orchestration/test_job_task_runner.py` | 89.92 | 158 |
| 3 | `tests/runtimes/test_supervisor_portability.py` | 84.06 | 161 |
| 4 | `tests/cli/test_mission_cmd.py` | 60.79 | 178 |
| 5 | `tests/cli/test_do_sequence_cli.py` | 58.62 | 88 |
| 6 | `tests/cli/test_golden_path.py` | 52.56 | 41 |
| 7 | `tests/runtimes/test_runtime_lifecycle_safety.py` | 44.25 | 50 |
| 8 | `tests/runtimes/test_runtime_cli_process_boundary.py` | 34.40 | 45 |
| 9 | `tests/orchestration/test_review_zip_hygiene.py` | 31.66 | 78 |
| 10 | `tests/orchestration/test_run_manifest_cross_episode_concurrency.py` | 31.12 | 22 |
| 11 | `tests/orchestration/test_job_budgets.py` | 30.28 | 15 |
| 12 | `tests/cli/test_do_commit_flags.py` | 27.82 | 50 |
| 13 | `tests/orchestration/test_review_gate_totality.py` | 27.36 | 7 |
| 14 | `tests/cli/test_scoped_listings.py` | 20.72 | 7 |
| 15 | `tests/test_grouped_cli.py` | 20.52 | 299 |
| 16 | `tests/cli/test_test_run_runtime.py` | 19.21 | 20 |
| 17 | `tests/orchestration/test_persisted_call_ownership.py` | 17.74 | 50 |
| 18 | `tests/runtimes/test_runtime_state_machine.py` | 17.46 | 29 |
| 19 | `tests/orchestration/test_job_apply_commit.py` | 17.01 | 69 |
| 20 | `tests/orchestration/test_exec_guard.py` | 16.75 | 29 |
| 21 | `tests/orchestration/test_ci_budgets.py` | 16.69 | 4 |
| 22 | `tests/ui_server/test_preview_end_to_end.py` | 16.09 | 2 |
| 23 | `tests/orchestration/test_disk_floor.py` | 16.07 | 17 |
| 24 | `tests/orchestration/test_job_evidence.py` | 16.07 | 68 |
| 25 | `tests/orchestration/test_mission_e2e.py` | 15.22 | 24 |
| 26 | `tests/ui_server/test_pause_e2e_live.py` | 14.75 | 4 |
| 27 | `tests/orchestration/test_orchestrator_loop.py` | 14.64 | 239 |
| 28 | `tests/orchestration/test_job_apply.py` | 14.51 | 57 |
| 29 | `tests/orchestration/test_job_stop_integration.py` | 14.30 | 26 |
| 30 | `tests/ui_server/test_multi_project_live.py` | 14.10 | 10 |

## 3. The 100 slowest tests

Same source command and file as section 2. "Sort all reported durations descending, take the top
100" is read literally: every `setup`/`call`/`teardown` line is its own entry in the sort, so a
single slow test can, in principle, contribute more than one row (none does in this top 100 — the
slowest entries are dominated by `call` phases, with only two `setup` phases appearing, both well
down the list).

### The 100 slowest individual test entries

| Rank | Seconds | Phase | Node id |
|---|---|---|---|
| 1 | 30.03 | call | `tests/orchestration/test_job_budgets.py::TestOnProviderAttemptCallback::test_callback_fires_on_retry` |
| 2 | 25.71 | call | `tests/orchestration/test_review_gate_totality.py::TestGateMatrixIsTotal::test_recursive_matrix_never_throws` |
| 3 | 19.66 | call | `tests/orchestration/test_job_task_runner.py::TestProviderOverrideToFake::test_cli_handler_provider_override` |
| 4 | 16.08 | call | `tests/ui_server/test_preview_end_to_end.py::TestPreviewEndToEnd::test_the_preview_flow_runs_end_to_end_on_a_real_fixture_app` |
| 5 | 15.31 | call | `tests/runtimes/test_runtime_lifecycle_safety.py::TestHonestStop::test_the_text_summary_of_a_failed_stop_is_explicit` |
| 6 | 15.30 | call | `tests/runtimes/test_runtime_lifecycle_safety.py::TestHonestStop::test_a_survivor_keeps_a_retryable_state` |
| 7 | 12.77 | call | `tests/orchestration/test_job_task_runner.py::TestCommandPathExplicitOverrides::test_provider_override_to_fake` |
| 8 | 12.42 | call | `tests/runtimes/test_runtime_cli_process_boundary.py::TestReadinessLogTail::test_the_readiness_failure_returns_the_line_the_child_really_printed` |
| 9 | 10.11 | call | `tests/orchestration/test_run_manifest_cross_episode_concurrency.py::TestTwoEpisodeIdsCannotClaimOneOrdinal::test_three_parallel_append_writers_leave_one_contiguous_chain` |
| 10 | 10.11 | call | `tests/orchestration/test_run_manifest_cross_episode_concurrency.py::TestTwoEpisodeIdsCannotClaimOneOrdinal::test_the_reproduced_race` |
| 11 | 10.04 | call | `tests/orchestration/test_run_manifest_cross_episode_concurrency.py::TestTwoEpisodeIdsCannotClaimOneOrdinal::test_the_loser_publishes_nothing_at_all` |
| 12 | 8.39 | call | `tests/orchestration/test_ci_stage_coverage.py::test_every_collected_test_is_selected_by_a_stage` |
| 13 | 7.90 | call | `tests/ui_server/test_pause_e2e_live.py::TestTaskScopeE2ELive::test_pause_relaunch_through_the_cli_matches_an_unpaused_control` |
| 14 | 7.81 | call | `tests/runtimes/test_supervisor_portability.py::TestEmergencyNoteLifecycle::test_the_note_lives_with_its_survivor_and_dies_with_the_record` |
| 15 | 7.62 | call | `tests/runtimes/test_supervisor_portability.py::TestPersistentLogPumpHealth::test_a_survivor_never_loses_its_last_durable_identity` |
| 16 | 7.50 | call | `tests/orchestration/test_ci_budgets.py::test_this_repositorys_shell_sustains_60fps_at_200_nodes` |
| 17 | 7.20 | call | `tests/cli/test_scoped_listings.py::TestScopedListingsCLI::test_full_isolation_and_flags` |
| 18 | 7.13 | call | `tests/runtimes/test_runtime_lifecycle_safety.py::TestHonestStop::test_a_readiness_failure_reports_survivors_instead_of_lying` |
| 19 | 7.08 | call | `tests/runtimes/test_supervisor_portability.py::TestPersistentLogPumpHealth::test_a_pump_failure_whose_cleanup_leaves_a_survivor_is_retained` |
| 20 | 6.83 | call | `tests/ui_server/test_pause_e2e_live.py::TestJobScopeE2ELive::test_pause_relaunch_through_the_cli_matches_an_unpaused_control` |
| 21 | 6.72 | call | `tests/cli/test_pytest_runner.py::test_runner_failing_pytest` |
| 22 | 6.34 | call | `tests/orchestration/test_ci_stage_selection.py::test_no_test_in_this_repository_escapes_the_marker_selected_stages` |
| 23 | 6.09 | call | `tests/orchestration/test_run_manifest_strict_boundaries.py::TestNoRawJsonLoadsOnManifestBytes::test_run_manifest_json_loads_only_inside_strict_json_loads` |
| 24 | 6.04 | call | `tests/runtimes/test_runtime_state_machine.py::TestRollbackSurvivors::test_a_state_write_failure_with_a_survivor_is_not_called_atomic` |
| 25 | 5.84 | call | `tests/cli/test_worker_facade_cmd.py::TestDoctorCoreDeadModels::test_dead_list_count_label_matches_what_it_counts` |
| 26 | 5.76 | call | `tests/cli/test_worker_facade_cmd.py::TestDoctorCoreReportFunction::test_report_as_json_matches_the_commands_own_json_output_in_the_same_run` |
| 27 | 5.67 | call | `tests/cli/test_worker_facade_cmd.py::TestDoctorCoreDeadModels::test_dead_id_leaves_ready_and_blockers_untouched` |
| 28 | 5.50 | call | `tests/orchestration/test_ci_budgets.py::test_this_repositorys_shell_paints_within_its_budget` |
| 29 | 5.32 | call | `tests/cli/test_test_run_runtime.py::TestTimeoutRun::test_timeout_json` |
| 30 | 5.32 | call | `tests/cli/test_test_run_runtime.py::TestTimeoutRun::test_timeout_status` |
| 31 | 4.96 | setup | `tests/orchestration/test_event_names.py::TestTheEventVocabularyIsDeclared::test_every_written_event_name_is_declared` |
| 32 | 4.84 | call | `tests/cli/test_quick_start.py::test_every_quick_start_line_exits_0_and_leaves_the_target_as_line_one_left_it` |
| 33 | 4.69 | call | `tests/orchestration/test_disk_floor.py::TestDoctorReadsTheInjectedProbe::test_the_section_states_both_numbers` |
| 34 | 4.61 | call | `tests/orchestration/test_event_name_coupling.py::TestEventNameCouplingRatchet::test_no_declared_entry_is_stale` |
| 35 | 4.59 | call | `tests/test_timeline.py::TestTheRunLogSeamHasOneIdSpelling::test_no_call_site_wraps_the_run_log_id_in_a_uuid` |
| 36 | 4.55 | call | `tests/orchestration/test_event_name_coupling.py::TestEventNameCouplingRatchet::test_every_dead_coupling_is_declared` |
| 37 | 4.42 | call | `tests/cli/test_scoped_listings.py::TestScopedListingsCLI::test_status_scoped` |
| 38 | 4.19 | call | `tests/runtimes/test_apps_ui_probe.py::TestRealViteAcrossTheCliBoundary::test_vite_survives_the_serve_cli_and_is_probed_and_stopped_separately` |
| 39 | 4.17 | call | `tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes` |
| 40 | 4.17 | call | `tests/ui_server/test_explanation_layer_live.py::test_the_explanation_layer_works_on_the_real_shell` |
| 41 | 4.03 | call | `tests/runtimes/test_supervisor_portability.py::TestPersistentLogPumpHealth::test_a_healthy_long_running_pump_stays_healthy` |
| 42 | 3.90 | call | `tests/cli/test_project_current.py::TestWorkspaceKeyGuard::test_no_forbidden_imports` |
| 43 | 3.87 | call | `tests/orchestration/test_review_zip_hygiene.py::TestFilenamePattern::test_filenames_sortable_chronologically` |
| 44 | 3.86 | call | `tests/ui_server/test_story_export_file_live.py::test_the_exported_demo_story_plays_from_file_with_no_request` |
| 45 | 3.83 | call | `tests/cli/test_scoped_listings.py::TestStatsFailuresScopedCLI::test_stats_failures_scoped_by_project` |
| 46 | 3.76 | call | `tests/runtimes/test_runtime_cli_process_boundary.py::TestServeSurvivesTheCli::test_serve_cli_exits_successfully_and_the_runtime_survives` |
| 47 | 3.73 | call | `tests/orchestration/test_job_stop_integration.py::TestALiveRunnerStopsCleanly::test_a_three_task_job_stopped_after_task_one_exits_clean_with_no_leftovers` |
| 48 | 3.72 | call | `tests/orchestration/test_one_job_store.py::TestTheClassicStoreIsGone::test_no_python_file_imports_a_classic_model` |
| 49 | 3.69 | call | `tests/runtimes/test_supervisor_portability.py::TestPostHandshakeTerminalState::test_a_stop_that_lands_while_the_supervisor_is_still_exiting_still_succeeds` |
| 50 | 3.68 | call | `tests/cli/test_do_sequence_cli.py::test_force_job_on_an_order_naming_ten_files_yields_one_job_of_ten_tasks` |
| 51 | 3.62 | call | `tests/orchestration/test_ci_budgets.py::test_this_repositorys_ui_bundle_is_within_its_size_cap` |
| 52 | 3.50 | call | `tests/ui_server/test_dashboard_contract.py::TestJobSummaryCommandContract::test_typescript_compiles` |
| 53 | 3.50 | call | `tests/runtimes/test_runtime_cli_process_boundary.py::TestServeSurvivesTheCli::test_the_log_stays_bounded_under_heavy_output` |
| 54 | 3.48 | call | `tests/ui_contracts/test_humanize_catalog.py::TestDerivation::test_the_emitter_walk_finds_call_sites` |
| 55 | 3.42 | call | `tests/orchestration/test_self_use_runner.py::TestThreeConsecutiveItemsOnAnEmptyLedger::test_three_closures_the_first_run_to_completion` |
| 56 | 3.36 | call | `tests/cli/test_worker_facade_cmd.py::TestDoctorCoreReportFunction::test_a_dead_builtin_default_is_actionable_with_its_id_and_repair_path` |
| 57 | 3.34 | call | `tests/cli/test_worker_facade_cmd.py::TestDoctorCoreFromAnotherDirectory::test_lanes_resolve_outside_the_checkout` |
| 58 | 3.32 | call | `tests/cli/test_worker_facade_cmd.py::TestDoctorCoreDeadModels::test_config_extension_id_says_it_came_from_config` |
| 59 | 3.29 | call | `tests/cli/test_worker_facade_cmd.py::TestDoctorCoreEnvironment::test_an_unknown_variable_is_named_with_its_closest_registered_match` |
| 60 | 3.28 | call | `tests/cli/test_worker_facade_cmd.py::TestDoctorCoreDeadModels::test_text_output_shows_warnings_without_claiming_not_ready` |
| 61 | 3.28 | setup | `tests/ui_server/test_explanation_layer_live.py::test_the_explanation_layer_works_on_the_real_shell` |
| 62 | 3.25 | setup | `tests/ui_server/test_story_export_file_live.py::test_the_exported_demo_story_plays_from_file_with_no_request` |
| 63 | 3.24 | call | `tests/cli/test_golden_path.py::TestStatus::test_status_shows_multiple_jobs` |
| 64 | 3.23 | call | `tests/cli/test_worker_facade_cmd.py::TestDoctorCoreDataReclaimable::test_a_preview_at_the_threshold_warns_with_the_total_and_both_commands` |
| 65 | 3.21 | call | `tests/cli/test_golden_path.py::TestShortIdResolution::test_ambiguous_short_id_exits_2` |
| 66 | 3.07 | call | `tests/cli/test_worker_facade_cmd.py::TestDoctorCoreDataReclaimable::test_a_preview_under_the_threshold_warns_about_nothing` |
| 67 | 3.06 | call | `tests/runtimes/test_runtime_cli_process_boundary.py::TestSeparateProbeAndStop::test_repeated_serve_probe_stop_cycles_leave_nothing_behind` |
| 68 | 3.04 | call | `tests/orchestration/test_exec_guard.py::test_a_pump_blocked_by_an_escapee_still_returns_the_bytes_it_already_read` |
| 69 | 3.04 | call | `tests/orchestration/test_exec_guard.py::test_wall_timeout_bounds_the_call_when_a_descendant_escapes_the_group` |
| 70 | 3.03 | call | `tests/orchestration/test_self_use_generator.py::TestDoctorWarningTierRealChain::test_a_real_dead_builtin_default_becomes_a_tier_3_item` |
| 71 | 3.00 | call | `tests/cli/test_worker_facade_cmd.py::TestDoctorCoreReportFunction::test_every_warnings_as_json_key_list_is_exactly_three_keys` |
| 72 | 3.00 | call | `tests/cli/test_do_sequence_cli.py::test_a_two_milestone_do_in_a_repo_with_a_passing_suite_meets_both_planner_criteria` |
| 73 | 2.95 | call | `tests/orchestration/test_dead_command_check.py::TestDeadCommandIds::test_the_real_catalog_has_no_dead_commands` |
| 74 | 2.94 | call | `tests/orchestration/test_disk_floor.py::TestDoctorReadsTheInjectedProbe::test_no_configured_floor_is_met_and_keeps_ready` |
| 75 | 2.93 | call | `tests/orchestration/test_disk_floor.py::TestDoctorReadsTheInjectedProbe::test_text_mode_prints_both_numbers_and_the_verdict` |
| 76 | 2.92 | call | `tests/cli/test_worker_facade_cmd.py::TestDoctorCoreDataReclaimable::test_the_threshold_is_read_from_the_config_key` |
| 77 | 2.92 | call | `tests/cli/test_worker_facade_cmd.py::TestDoctorCoreReportFunction::test_a_dead_configured_id_and_an_unknown_variable_are_not_actionable` |
| 78 | 2.92 | call | `tests/cli/test_worker_facade_cmd.py::TestDoctorCoreReportFunction::test_actionable_warnings_answers_exactly_the_actionable_ones_in_order` |
| 79 | 2.92 | call | `tests/orchestration/test_disk_floor.py::TestDoctorReadsTheInjectedProbe::test_a_floor_that_is_not_met_blocks_ready` |
| 80 | 2.90 | call | `tests/cli/test_worker_facade_cmd.py::TestDoctorCoreDeadModels::test_summary_is_materially_shorter_than_detail` |
| 81 | 2.89 | call | `tests/cli/test_worker_facade_cmd.py::TestShippedDefaultsAreNotOnTheShippedDeadList::test_doctor_core_emits_no_dead_builtin_warning` |
| 82 | 2.89 | call | `tests/cli/test_worker_facade_cmd.py::TestDoctorCoreDeadModels::test_missing_replacement_is_not_repeated_after_the_reason` |
| 83 | 2.87 | call | `tests/cli/test_worker_facade_cmd.py::TestDoctorCoreDeadModels::test_text_mode_prints_the_summary_and_not_the_recorded_reason` |
| 84 | 2.86 | call | `tests/cli/test_worker_facade_cmd.py::TestDoctorCoreDeadModels::test_provenance_survives_in_the_compact_text_rendering` |
| 85 | 2.85 | call | `tests/cli/test_worker_facade_cmd.py::TestDoctorCore::test_core_text_output` |
| 86 | 2.85 | call | `tests/cli/test_worker_facade_cmd.py::TestDoctorCoreSafeErr::test_mnt_tmp_users_redacted` |
| 87 | 2.85 | call | `tests/cli/test_worker_facade_cmd.py::TestDoctorCoreDeadModels::test_warnings_key_present_and_is_a_list` |
| 88 | 2.84 | call | `tests/cli/test_worker_facade_cmd.py::TestDoctorCoreSafeErr::test_private_paths_redacted` |
| 89 | 2.84 | call | `tests/cli/test_worker_facade_cmd.py::TestDoctorCoreFromAnotherDirectory::test_lane_detail_stays_installation_relative` |
| 90 | 2.83 | call | `tests/cli/test_worker_facade_cmd.py::TestDoctorCore::test_core_error_messages_safe` |
| 91 | 2.83 | call | `tests/regression/test_resource_safety.py::TestWrapperPathForcedTimeout::test_subsequent_wrapper_succeeds_after_timeout` |
| 92 | 2.83 | call | `tests/cli/test_worker_facade_cmd.py::TestDoctorCoreDeadCommands::test_text_mode_lists_the_planted_command_in_the_section` |
| 93 | 2.83 | call | `tests/cli/test_worker_facade_cmd.py::TestDoctorCoreDeadModels::test_warning_states_operator_maintained_provenance` |
| 94 | 2.82 | call | `tests/cli/test_worker_facade_cmd.py::TestDoctorCoreDeadModels::test_known_replacement_is_named` |
| 95 | 2.82 | call | `tests/cli/test_worker_facade_cmd.py::TestDoctorCoreSafeErr::test_secrets_redacted` |
| 96 | 2.82 | call | `tests/cli/test_worker_facade_cmd.py::TestDoctorCoreDeadModels::test_unreadable_dead_list_is_a_failing_check_and_a_blocker` |
| 97 | 2.82 | call | `tests/cli/test_worker_facade_cmd.py::TestDoctorCoreDeadModels::test_dead_configured_id_names_the_config_key` |
| 98 | 2.82 | call | `tests/cli/test_worker_facade_cmd.py::TestDoctorCoreDeadCommands::test_json_mode_carries_the_key_empty` |
| 99 | 2.82 | call | `tests/cli/test_worker_facade_cmd.py::TestDoctorCoreEnvironment::test_text_mode_prints_the_compact_line` |
| 100 | 2.81 | call | `tests/cli/test_worker_facade_cmd.py::TestDoctorCoreDeadCommands::test_text_mode_shows_the_section_empty` |

## 4. Tests that start a child process

Commands:
`git grep -lE 'subprocess\.(run|Popen|check_call|check_output)|os\.(fork|spawn|exec)' tests/`
(file list) and
`git grep -cE 'subprocess\.(run|Popen|check_call|check_output)|os\.(fork|spawn|exec)' tests/`
(per-file call-site counts, summed in Python since a shell `awk` pipe was avoided per the sandbox
note).

- **206 files** under `tests/` contain at least one process-spawning call matching the pattern.
- **623 total call sites** across those 206 files (summed from the per-file `git grep -c` counts).
- This is a static grep over source text, not a dynamic trace: a file can match without every
  matched call site executing in a given run (guarded by a skip, a fixture condition, or a
  conditional branch), and a helper function called from many test files is counted once per
  file that contains the call site itself, not once per file that merely imports the helper.

## 5. UI builds and Chrome starts

Command: `git grep -n "npm run build\|vite build\|remote-debugging-pipe\|launch_chrome\|webdriver" tests/`,
followed by manual reading of each hit to separate an actual invocation from a docstring mention,
a banned-word assertion, or a mocked seam.

**UI builds (real `vite build` subprocess invocations), 5 call sites across 3 files, all 5 actually
executed in this run** (confirmed against `.agent/authored/f293-r1-durations.txt`, each showing a
multi-second, non-zero `call` duration rather than an instant skip):
- `tests/orchestration/test_ci_budgets.py` — 3 call sites (lines 173, 239, 345):
  `test_this_repositorys_ui_bundle_is_within_its_size_cap` (3.62s),
  `test_this_repositorys_shell_paints_within_its_budget` (5.50s),
  `test_this_repositorys_shell_sustains_60fps_at_200_nodes` (7.50s).
- `tests/ui_server/test_explanation_layer_live.py` — 1 call site (line 93), feeding
  `test_the_explanation_layer_works_on_the_real_shell` (4.17s call + 3.28s setup).
- `tests/ui_server/test_story_export_file_live.py` — 1 call site (line 204), a module-scoped
  fixture (`story_player_dir`) feeding
  `test_the_exported_demo_story_plays_from_file_with_no_request` (3.86s call + 3.25s setup).

**Real Chrome/CDP starts (`ChromePipe(...)` instantiated with the real `CHROME_BIN`), 4 call sites,
all 4 executed in this run** (the same four tests named above that build the UI also drive Chrome
over `--remote-debugging-pipe`, i.e. `test_this_repositorys_shell_paints_within_its_budget`,
`test_this_repositorys_shell_sustains_60fps_at_200_nodes`,
`test_the_explanation_layer_works_on_the_real_shell`,
`test_the_exported_demo_story_plays_from_file_with_no_request`; the size-cap test builds the UI but
never drives Chrome). One further `ChromePipe(...)` call site in
`tests/ui_server/test_story_export_file_live.py` (line 329, `test_chrome_timeout_message_names_log`)
passes a `fake_chrome` stand-in script, not a real Chrome binary — **not counted** as a Chrome start.

**Mentions that are NOT a build or a Chrome start** (read and excluded): `tests/cli/test_product_spine.py`
(asserts the strings are absent from some generated text), `tests/orchestration/test_story_export.py`
(asserts an error message contains the string), `tests/ui_contracts/test_diff_view_render.py`
(docstring recording a historical manual build at a past commit), `tests/orchestration/test_product_smoke.py`
(a banned-import-name check that includes `"webdriver"` in its ban list), `tests/ui_server/test_dashboard_contract.py`
(patches the build seam, `exec_guard.run_guarded_runtime_build_command`, specifically to avoid
spending a real `npm install`/`npm run build` inside the suite — its own docstring states this).

## 6. Processes alive after the run

Commands: `ps aux` (the sandbox's `ps -eo pid,ppid,etime,cmd` form required interactive approval
and was refused by the harness, so `ps aux`, which carries an equivalent `PID`/`START`/`TIME`/`COMMAND`
set, was used instead), taken once after the full suite run's `REAL_EXIT=0`; suspect PIDs were then
traced to their parent via `/proc/<pid>/status` (`PPid:`) and `/proc/<pid>/cmdline`/`cwd` to
establish ownership, since `ps` alone does not show ancestry beyond one hop clearly in this output
width.

No process leaked by Remedy's own test suite was found in this snapshot. Two clusters of long
wall-clock-adjacent but OWNED-ELSEWHERE processes were investigated and ruled out:

- Three `node node_modules/vite/bin/vite.js --host 127.0.0.1 --port <18430|18431|18432>` processes
  and a `chromium_headless_shell` (ms-playwright cache) process tree (a zygote, a gpu-process, two
  utility processes and a renderer, all carrying `--remote-debugging-pipe`), all started at 19:56-
  19:57 local time, the same wall-clock minute the test load record's run finished
  (`utc: 2026-09-30T17:56:04Z` = 19:56:04 CEST). Traced via `/proc/<pid>/status` `PPid:` up the
  chain: the vite processes' ancestor is `node .../@playwright/test/cli.js test`, itself a child of
  `npx playwright test` run from `/home/decodeux/Repos/luna-meta/luna-chat` — a different repository
  entirely, launched by a separate, unattended Claude Code agent process
  (`/opt/luna/bin/improve-run.sh claude`, the "Luna workspace" `improve run`). This is a sibling
  automated session on the same shared machine, not a Remedy test leak; it merely started in the
  same minute by coincidence.
- A `timeout 1800 .venv/bin/pytest -q --ignore=tests/test_remedy_questions.py -p no:cacheprovider`
  process (PID 1225120) whose `cwd` (`/proc/1225120/cwd`) resolves to `/home/decodeux/Repos/luna-meta/luna`
  — again a different repository, not this one.
- Every `google-chrome`/`chrome` process remaining in the snapshot was checked for
  `--remote-debugging-pipe`: only the two processes already attributed to the `luna-chat` Playwright
  tree above carry that flag. None of the Remedy-repo tests' own `ChromePipe`-launched Chrome
  instances (the four real Chrome starts named in section 5) are still present — they exited
  cleanly.
- No process anywhere in the snapshot has a command line referencing a `/tmp/pytest-of-*` path.

**R-1118 cross-check** (the finding this section exists to re-check): R-1118 names a specific
leaked-process shape produced by `tests/runtimes/test_dev_server.py`'s
`test_readiness_timeout_stops_the_tree_and_leaves_no_state` — a Remedy dev-server process tree left
behind after a readiness timeout. **Negative result: that pattern does not reappear in this
snapshot.** No process whose command line names `remedy`, a Remedy dev-server entry point, or a
path under this repository's own runtime state directories was found alive and unaccounted for
after the run. This does not by itself resolve R-1118 (a single clean run is not proof the shape
never recurs), but it gives T001's own inventory the negative reading its task description orders;
the next round (T003, per `docs/roadmap/features/T2_F293.md`) is where "a test run that leaves a
process behind fails" becomes an enforced rule.
