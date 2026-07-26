# Handoff — F034 Bundled clarification (integration gate)

Branch: feature/f034-bundled-clarification
Review range: 0891b8d..HEAD (integration-gate round; state files only)
Full-suite comparison: branch 0891b8d vs base 34878f3 (main after PR #150)
Open findings: 0. Next expected action: reviewer integration-gate verdict.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| Persist round-1 PASS + open the gate | done | commit 25351cf |
| Full suite, branch | done | 161 failed / 13935 passed, 180.61s |
| Full suite, base worktree | done | 197 failed / 13820 passed, 193.31s |
| Attribution of every branch-only failure | done | 7/7 pre-existing flake |
| Canary | done | 42 passed |
| Production code changes | none | no branch-only failure was F034-attributable |

## Commits this round

### 25351cf chore(f034): persist round 1 reviewer verdict; open integration gate
| File | + | - |
|------|---|---|
| .agent/live_review.md | 9 | 3 |
| .agent/plan.md | 4 | 3 |

### (this handback) chore(f034): record integration-gate evidence
| File | + | - |
|------|---|---|
| .agent/handoff.md | rewritten | |
| .agent/live_review.md | gate verdict appended | |
| .agent/plan.md | checklist + current step | |

Prior round for reference (34878f3..0891b8d): 4648d69 claim, f5aef15 T001,
2a365d7 T002, 01f546e T003, 3a8652f T004, 0891b8d handoff. Per-file tables
for those are in the round-1 handoff (git history at 0891b8d).

## Raw suite evidence

### Branch (0891b8d)

    $ python3 -m pytest -n auto -q
    ...
    FAILED tests/cli/test_runtime_cmd.py::TestProbe::test_a_probe_timeout_exits_4
    FAILED tests/ui_contracts/test_graph_architecture.py::TestExplainableEdges::test_legacy_edge_component_under_legacy
    FAILED tests/test_test_runner.py::TestCliRunTestsLocal::test_permission_missing_exits_1
    FAILED tests/ui_contracts/test_graph_architecture.py::TestSemanticZoomDirection::test_renderer_zoom_direction_in_legacy_source
    FAILED tests/ui_contracts/test_timeline_guard.py::TestOrchestratorLoopContract::test_orchestrator_loop_doc_exists
    FAILED tests/ui_contracts/test_ux_quality.py::TestUXAntiRegression::test_legacy_graph_files_under_legacy
    FAILED tests/ui_contracts/test_ux_quality.py::TestScreenSpaceLabels::test_legacy_graph_nodes_under_legacy
    FAILED tests/ui_server/test_dashboard_contract.py::TestAgentStateFilesCurrentBranch::test_context_md_references_current_branch
    FAILED tests/test_test_runner.py::TestCliRunTestsLocal::test_no_target_repo_exits_1
    FAILED tests/ui_server/test_dashboard_contract.py::TestLiveReviewAndAgentStateRefs::test_context_md_no_stale_steps
    FAILED tests/test_agent_tooling.py::test_claude_agent_is_read_only_reviewer
    FAILED tests/cli/test_scoped_listings.py::TestScopedListingsCLI::test_legacy_job_hidden_and_unscoped_label
    FAILED tests/ui_server/test_dashboard_contract.py::TestLiveReviewAndAgentStateRefs::test_live_review_has_steps_section
    FAILED tests/runtimes/test_supervisor_portability.py::TestRuntimeArtifactsArePrivate::test_the_spec_is_private_and_removed_once_the_supervisor_has_read_it
    FAILED tests/runtimes/test_runtime_state_machine.py::TestSpecFingerprint::test_a_changed_config_blocks_a_second_serve[changed1]
    FAILED tests/runtimes/test_supervisor_portability.py::TestShareableRedaction::test_a_real_served_state_shares_nothing_private
    FAILED tests/runtimes/test_supervisor_portability.py::TestShareableRedaction::test_embedded_private_paths_are_removed_everywhere
    FAILED tests/runtimes/test_supervisor_portability.py::TestShareableRedaction::test_the_redaction_walks_dictionaries_and_lists_recursively
    FAILED tests/runtimes/test_supervisor_portability.py::TestDeniedCwdPortability::test_a_wrong_readable_cwd_is_still_a_mismatch
    FAILED tests/cli/test_scoped_listings.py::TestScopedListingsCLI::test_orphaned_label_on_deleted_project
    FAILED tests/orchestration/test_job_worktree_handoff.py::TestJobPlanResumeCli::test_the_cli_resumes_a_16_char_jobplan_id
    FAILED tests/runtimes/test_supervisor_portability.py::TestCrossPlatformRedaction::test_windows_forward_slash_paths_are_redacted
    FAILED tests/runtimes/test_supervisor_portability.py::TestCrossPlatformRedaction::test_unc_paths_are_redacted_in_both_slash_styles
    FAILED tests/cli/test_scoped_listings.py::TestScopedListingsCLI::test_status_scoped
    FAILED tests/cli/test_scoped_listings.py::TestStatsFailuresScopedCLI::test_stats_failures_scoped_by_project
    ERROR tests/runtimes/test_supervisor_portability.py::TestHardStopFallbackRevalidation::test_a_stale_supervisor_identity_is_never_signalled[pid disappeared and was replaced-check2]
    161 failed, 13935 passed, 8 skipped, 1 error in 180.61s (0:03:00)

    real 3m1.113s   user 10m57.305s   sys 2m22.673s   exit 0

### Base (34878f3, read-only worktree /tmp/remedy-base-34878f3)

    $ python3 -m pytest -n auto -q
    ...
    FAILED tests/ui_contracts/test_ux_quality.py::TestUXAntiRegression::test_legacy_graph_files_under_legacy
    FAILED tests/ui_contracts/test_ux_quality.py::TestScreenSpaceLabels::test_legacy_graph_nodes_under_legacy
    FAILED tests/test_test_runner.py::TestCliRunTestsLocal::test_no_target_repo_exits_1
    FAILED tests/ui_server/test_dashboard_contract.py::TestAgentStateFilesCurrentBranch::test_context_md_references_current_branch
    FAILED tests/ui_server/test_dashboard_contract.py::TestLiveReviewAndAgentStateRefs::test_live_review_has_steps_section
    FAILED tests/ui_server/test_dashboard_contract.py::TestLiveReviewAndAgentStateRefs::test_context_md_no_stale_steps
    FAILED tests/ui_server/test_dashboard_contract.py::TestJobSummaryCommandContract::test_typescript_compiles
    FAILED tests/ui_server/test_live_state.py::TestUIServerIntegration::test_server_starts_and_writes_info
    FAILED tests/ui_server/test_live_state.py::TestUIServerIntegration::test_app_shell_served_without_token
    FAILED tests/ui_server/test_live_state.py::TestUIServerIntegration::test_api_invalid_token_403
    FAILED tests/ui_server/test_live_state.py::TestUIServerIntegration::test_api_valid_token_returns_dashboard
    FAILED tests/ui_server/test_live_state.py::TestUIServerIntegration::test_put_rejected
    FAILED tests/ui_server/test_live_state.py::TestUIServerIntegration::test_dashboard_no_raw_leaks
    FAILED tests/ui_server/test_live_state.py::TestUIServerIntegration::test_brain_endpoint
    FAILED tests/ui_server/test_live_state.py::TestUIServerIntegration::test_readiness_endpoint
    FAILED tests/runtimes/test_supervisor_portability.py::TestShareableRedaction::test_a_real_served_state_shares_nothing_private
    FAILED tests/runtimes/test_supervisor_portability.py::TestShareableRedaction::test_embedded_private_paths_are_removed_everywhere
    FAILED tests/runtimes/test_supervisor_portability.py::TestShareableRedaction::test_the_redaction_walks_dictionaries_and_lists_recursively
    FAILED tests/runtimes/test_runtime_cli_process_boundary.py::TestSupervisorFailures::test_an_application_that_dies_before_readiness_is_a_start_failure
    FAILED tests/runtimes/test_runtime_cli_process_boundary.py::TestSupervisorFailures::test_a_readiness_timeout_leaves_no_runtime
    FAILED tests/orchestration/test_job_worktree_handoff.py::TestJobPlanResumeCli::test_the_cli_resumes_a_16_char_jobplan_id
    FAILED tests/cli/test_scoped_listings.py::TestScopedListingsCLI::test_full_isolation_and_flags
    FAILED tests/runtimes/test_supervisor_portability.py::TestCrossPlatformRedaction::test_windows_forward_slash_paths_are_redacted
    FAILED tests/runtimes/test_supervisor_portability.py::TestCrossPlatformRedaction::test_unc_paths_are_redacted_in_both_slash_styles
    FAILED tests/runtimes/test_supervisor_portability.py::TestServeIsSupervisorFirst::test_a_second_serve_succeeds_when_the_app_cwd_cannot_be_read
    FAILED tests/cli/test_scoped_listings.py::TestScopedListingsCLI::test_legacy_job_hidden_and_unscoped_label
    FAILED tests/cli/test_scoped_listings.py::TestScopedListingsCLI::test_orphaned_label_on_deleted_project
    FAILED tests/cli/test_scoped_listings.py::TestScopedListingsCLI::test_status_scoped
    FAILED tests/cli/test_scoped_listings.py::TestStatsFailuresScopedCLI::test_stats_failures_scoped_by_project
    197 failed, 13820 passed, 15 skipped in 193.31s (0:03:13)

    real 3m13.826s   user 12m29.163s   sys 1m44.785s   exit 0

## Failure-set diff

| Set | Count |
|-----|-------|
| Branch failures (unique ids) | 161 |
| Base failures (unique ids) | 197 |
| Shared | 154 |
| Branch-only | 7 |
| Base-only | 43 |

The branch has 36 FEWER failures than base. Both directions are the same
pre-existing xdist nondeterminism; neither is a property of F034.

## Attribution — all 7 branch-only failures

Serial re-run of all seven together:

    $ python3 -m pytest -p no:randomly -q <the 7 node ids>
    .......                                                                  [100%]
    7 passed in 4.53s
    exit=0

| # | Branch-only failure | Verdict | Evidence |
|---|---------------------|---------|----------|
| 1 | tests/cli/test_runtime_cmd.py::TestProbe::test_a_probe_timeout_exits_4 | pre-existing flake | passes serially; **reproduced verbatim on the BASE worktree** under xdist (repeat run 2) |
| 2 | tests/cli/test_runtime_cmd.py::TestProbe::test_a_second_probe_runs_cleanly | pre-existing flake | passes serially; **reproduced verbatim on BASE** (repeat run 2) |
| 3 | tests/runtimes/test_apps_ui_probe.py::TestRealViteProbe::test_a_one_shot_probe_leaves_no_process_and_no_state | pre-existing flake | passes serially; same file failed on BASE repeat run 1 (TestRealViteAcrossTheCliBoundary) |
| 4 | tests/runtimes/test_runtime_state_machine.py::TestSpecFingerprint::test_a_changed_config_blocks_a_second_serve[changed1] | pre-existing flake | passes serially; same file produced 3 failures on BASE repeat run 2 |
| 5 | tests/runtimes/test_supervisor_portability.py::TestDeniedCwdPortability::test_a_wrong_readable_cwd_is_still_a_mismatch | pre-existing flake | passes serially; file fails 8× on the base full run, 5–6× per base repeat |
| 6 | tests/runtimes/test_supervisor_portability.py::TestRuntimeArtifactsArePrivate::test_the_spec_is_private_and_removed_once_the_supervisor_has_read_it | pre-existing flake | as above (file: branch 9, base 8) |
| 7 | tests/runtimes/test_supervisor_portability.py::TestSupervisorFinalizationAndGroups::test_every_supervisor_failure_path_uses_the_common_finalizer | pre-existing flake | as above |

Base-worktree xdist repeats (the decisive check):

    === BASE xdist run 1 ===  15 failed, 139 passed, 2 errors in 13.08s
    === BASE xdist run 2 ===  12 failed, 142 passed, 1 error in 14.69s
      FAILED tests/cli/test_runtime_cmd.py::TestProbe::test_a_probe_timeout_exits_4
      FAILED tests/cli/test_runtime_cmd.py::TestProbe::test_a_second_probe_runs_cleanly
      FAILED tests/runtimes/test_runtime_state_machine.py::TestProcessGroupIdentity::...
      FAILED tests/runtimes/test_runtime_state_machine.py::TestLifecycleStateMachine::...
      FAILED tests/runtimes/test_runtime_state_machine.py::TestTypedState::...

Coupling check — none of the four affected files references any module
F034 touched:

    $ grep -l "flight_plan\|decision_queue\|clarification\|assumptions" \
        tests/cli/test_runtime_cmd.py tests/runtimes/test_apps_ui_probe.py \
        tests/runtimes/test_runtime_state_machine.py \
        tests/runtimes/test_supervisor_portability.py
    (no matches)

These are real-process supervisor/probe tests (spawn, port bind, process
groups, readiness timeouts) — the classic xdist-contention failure class,
already on the F135/F052 backlog.

**Verdict: zero regressions attributable to F034. No production code changed
this round.**

## Canary

    $ python3 -m pytest tests/cli/test_golden_path.py -q
    ..........................................                               [100%]
    42 passed in 18.80s
    exit=0

## Notes

- Wall clock 3m01s (branch) / 3m13s (base), both under the ~5 min
  threshold — no perf pass needed.
- Base worktree /tmp/remedy-base-34878f3 created and removed; `git
  worktree list` shows only the main checkout.
- The suite is RED on base by 197 tests. That is pre-existing and outside
  this feature's scope; it is why the gate is a differential comparison
  rather than an absolute green.
