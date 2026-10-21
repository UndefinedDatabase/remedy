#!/usr/bin/env python3
"""Create the evidence job for F303 round 8, the closure's evidence round.

Adapted from F060's `.agent/authored/f060-r6-create_f060_evidence.py`, which packaged READY; this
copy differs from it in its docstring, base commit, evidence directory, job id, job title, feature
id, run_id and TEST_FILES. F303's branch carries no merge, so its first-parent count equals its
plain count, and the guard holds as written. TEST_FILES are F060's set plus the eight test files
F303's rounds added or changed that F060's set lacks. The base is `2621bbe2e`, `main` when F303's
branch was made and the merge of F060's pull request. The deselection is F060's.
The closure's one full suite, `.agent/authored/f303-closure-suite.txt`, ran on the tree that ships.
Everything else is F060's and load-bearing.
Round 8 differs from round 7's `.agent/authored/f303-r7-create_f303_evidence.py` in this
paragraph, its evidence directory, its job id and title, and one thing more (DECISION F303 D6):
its collect-only and its test run get `REMEDY_DATA_DIR` set to a fresh, empty folder,
`.remedy-wt/f303-r8-evidence-data`, so the data root guard of `tests/conftest.py` watches a
root only the run writes, not the operator's, which the operator's own service writes at any
time (R-1411). The recorded command text is unchanged.
Run from the repository root at the accepted head: `python3 <this file> [<evidence dir>]`; the
optional argument overrides the evidence directory for a reviewer's dry run.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = "2621bbe2ebf62c394750fee8b06cbdfd357d7f77"
EVIDENCE_DIR = sys.argv[1] if len(sys.argv) > 1 else ".remedy-wt/f303-r8-evidence"
TEST_FILES = sorted([
    "tests/cli/test_advertised_commands.py",
    "tests/cli/test_certificate_cmd.py",
    "tests/cli/test_cli_ux.py",
    "tests/cli/test_client_changes_cmd.py",
    "tests/cli/test_client_insight_cmd.py",
    "tests/cli/test_client_interface.py",
    "tests/cli/test_client_mcp_cmd.py",
    "tests/cli/test_client_order_cmd.py",
    "tests/cli/test_client_run_cmd.py",
    "tests/cli/test_command_catalog.py",
    "tests/cli/test_config_cmd.py",
    "tests/cli/test_cost_preview_confirm.py",
    "tests/cli/test_decision_answers.py",
    "tests/cli/test_decision_cmd.py",
    "tests/cli/test_do_bounded_lane.py",
    "tests/cli/test_do_commit_flags.py",
    "tests/cli/test_do_flags.py",
    "tests/cli/test_do_order_budget.py",
    "tests/cli/test_do_order_file.py",
    "tests/cli/test_do_project_repo.py",
    "tests/cli/test_do_scale_walk.py",
    "tests/cli/test_do_sequence_cli.py",
    "tests/cli/test_do_several_projects.py",
    "tests/cli/test_exit_codes.py",
    "tests/cli/test_golden_path.py",
    "tests/cli/test_job_commands.py",
    "tests/cli/test_job_pause.py",
    "tests/cli/test_job_refusal_envelope.py",
    "tests/cli/test_job_rerun_manifest.py",
    "tests/cli/test_job_rerun_read_only_workspace.py",
    "tests/cli/test_job_rerun_subtree.py",
    "tests/cli/test_job_rerun_workspace_identity.py",
    "tests/cli/test_job_rerun_workspace_security.py",
    "tests/cli/test_job_rerun_workspace_traversal.py",
    "tests/cli/test_job_run_end_states.py",
    "tests/cli/test_job_run_invocation_truth.py",
    "tests/cli/test_job_run_session_resume.py",
    "tests/cli/test_job_show.py",
    "tests/cli/test_job_steer.py",
    "tests/cli/test_job_stop.py",
    "tests/cli/test_json_contract.py",
    "tests/cli/test_json_envelope.py",
    "tests/cli/test_machine_client_contract.py",
    "tests/cli/test_machine_client_paths.py",
    "tests/cli/test_mission_cmd.py",
    "tests/cli/test_plan_approval.py",
    "tests/cli/test_quick_start.py",
    "tests/cli/test_rehearsal.py",
    "tests/cli/test_serve_client_parity.py",
    "tests/cli/test_serve_client_scope.py",
    "tests/cli/test_status_cmd.py",
    "tests/conftest.py",
    "tests/docs/test_bootstrap_reads_decisions_by_part.py",
    "tests/docs/test_docs_consistency.py",
    "tests/docs/test_environment_guide.py",
    "tests/docs/test_named_source_paths.py",
    "tests/docs/test_operator_questions_shape.py",
    "tests/docs/test_permission_matrix_page.py",
    "tests/docs/test_retired_promote_word.py",
    "tests/docs/test_toolchain_refresh_order.py",
    "tests/docs/test_vocabulary.py",
    "tests/orchestration/test_agent_state_and_readiness.py",
    "tests/orchestration/test_api_clients.py",
    "tests/orchestration/test_api_release_matrix.py",
    "tests/orchestration/test_apply_permissions.py",
    "tests/orchestration/test_autonomy_gate.py",
    "tests/orchestration/test_autonomy_levels.py",
    "tests/orchestration/test_autonomy_seams.py",
    "tests/orchestration/test_block_lint.py",
    "tests/orchestration/test_budget_clock.py",
    "tests/orchestration/test_budget_decision.py",
    "tests/orchestration/test_budget_guard.py",
    "tests/orchestration/test_budget_profiles.py",
    "tests/orchestration/test_budget_stop.py",
    "tests/orchestration/test_budget_stop_integration.py",
    "tests/orchestration/test_builder_context.py",
    "tests/orchestration/test_call_modes_agree.py",
    "tests/orchestration/test_ci_workflow.py",
    "tests/orchestration/test_claude_cli_resume.py",
    "tests/orchestration/test_client_changes.py",
    "tests/orchestration/test_client_diff.py",
    "tests/orchestration/test_client_digest.py",
    "tests/orchestration/test_client_story.py",
    "tests/orchestration/test_client_story_words.py",
    "tests/orchestration/test_closure_suite_cost.py",
    "tests/orchestration/test_config.py",
    "tests/orchestration/test_crash_report.py",
    "tests/orchestration/test_data_reclaim.py",
    "tests/orchestration/test_dead_command_check.py",
    "tests/orchestration/test_decision_evidence.py",
    "tests/orchestration/test_decision_queue.py",
    "tests/orchestration/test_disk_floor.py",
    "tests/orchestration/test_do_lane.py",
    "tests/orchestration/test_do_scope.py",
    "tests/orchestration/test_do_sequence.py",
    "tests/orchestration/test_do_sequence_order_digest.py",
    "tests/orchestration/test_do_sequence_scope_order.py",
    "tests/orchestration/test_do_then_story.py",
    "tests/orchestration/test_dod_runners.py",
    "tests/orchestration/test_durable_write_guard.py",
    "tests/orchestration/test_env_registry.py",
    "tests/orchestration/test_episode_snapshot_full_validity.py",
    "tests/orchestration/test_episode_snapshot_lifecycle.py",
    "tests/orchestration/test_escalation.py",
    "tests/orchestration/test_event_names.py",
    "tests/orchestration/test_evidence_bundle.py",
    "tests/orchestration/test_exec_guard.py",
    "tests/orchestration/test_execution_config.py",
    "tests/orchestration/test_execution_options.py",
    "tests/orchestration/test_f018_authority_integration.py",
    "tests/orchestration/test_f018_package_pipeline_e2e.py",
    "tests/orchestration/test_failure_postmortem.py",
    "tests/orchestration/test_failure_wiring.py",
    "tests/orchestration/test_handoff.py",
    "tests/orchestration/test_import_reachability.py",
    "tests/orchestration/test_integrity_gate.py",
    "tests/orchestration/test_job_administrative_fields.py",
    "tests/orchestration/test_job_apply.py",
    "tests/orchestration/test_job_apply_consistency.py",
    "tests/orchestration/test_job_budgets.py",
    "tests/orchestration/test_job_burn.py",
    "tests/orchestration/test_job_certificate.py",
    "tests/orchestration/test_job_certificate_claims.py",
    "tests/orchestration/test_job_certificate_sources.py",
    "tests/orchestration/test_job_certificate_verify.py",
    "tests/orchestration/test_job_evidence.py",
    "tests/orchestration/test_job_input_definition_completeness.py",
    "tests/orchestration/test_job_input_definition_schema.py",
    "tests/orchestration/test_job_insight.py",
    "tests/orchestration/test_job_plan.py",
    "tests/orchestration/test_job_run_refs.py",
    "tests/orchestration/test_job_stop_integration.py",
    "tests/orchestration/test_job_task_runner.py",
    "tests/orchestration/test_job_worktree_handoff.py",
    "tests/orchestration/test_job_worktree_integrity.py",
    "tests/orchestration/test_lab_stop_20261020.py",
    "tests/orchestration/test_legacy_manifest_presence.py",
    "tests/orchestration/test_lessons.py",
    "tests/orchestration/test_live_review_rotation.py",
    "tests/orchestration/test_long_run_executor.py",
    "tests/orchestration/test_manual_completion_bundle.py",
    "tests/orchestration/test_material_input_fields.py",
    "tests/orchestration/test_mcp_server.py",
    "tests/orchestration/test_mcp_tools.py",
    "tests/orchestration/test_mission_compiler.py",
    "tests/orchestration/test_mission_contract.py",
    "tests/orchestration/test_mission_projects.py",
    "tests/orchestration/test_mission_state.py",
    "tests/orchestration/test_mission_upkeep.py",
    "tests/orchestration/test_model_routing.py",
    "tests/orchestration/test_orchestrator_dispatch.py",
    "tests/orchestration/test_orchestrator_loop.py",
    "tests/orchestration/test_order_file.py",
    "tests/orchestration/test_order_intent.py",
    "tests/orchestration/test_order_jobs.py",
    "tests/orchestration/test_order_ledger.py",
    "tests/orchestration/test_order_scope.py",
    "tests/orchestration/test_order_shape_repair.py",
    "tests/orchestration/test_ownership_phrases.py",
    "tests/orchestration/test_pause_manifest.py",
    "tests/orchestration/test_pause_resume.py",
    "tests/orchestration/test_permission_levels.py",
    "tests/orchestration/test_permission_matrix.py",
    "tests/orchestration/test_permission_matrix_guards.py",
    "tests/orchestration/test_persisted_call_episode_membership.py",
    "tests/orchestration/test_persisted_call_ownership.py",
    "tests/orchestration/test_persisted_episode_snapshot_schema.py",
    "tests/orchestration/test_persisted_run_call_schema.py",
    "tests/orchestration/test_pi_events.py",
    "tests/orchestration/test_pi_loop_limits.py",
    "tests/orchestration/test_pi_provider.py",
    "tests/orchestration/test_pi_timeouts.py",
    "tests/orchestration/test_pi_turn_counts.py",
    "tests/orchestration/test_pingpong_cli.py",
    "tests/orchestration/test_predictive_budget.py",
    "tests/orchestration/test_product_smoke.py",
    "tests/orchestration/test_project_brain.py",
    "tests/orchestration/test_project_tests.py",
    "tests/orchestration/test_prompt_trace.py",
    "tests/orchestration/test_public_api_gate_paths.py",
    "tests/orchestration/test_record_client_answers.py",
    "tests/orchestration/test_repo_mission.py",
    "tests/orchestration/test_resume_cli.py",
    "tests/orchestration/test_resume_kill.py",
    "tests/orchestration/test_review_commit_chain.py",
    "tests/orchestration/test_review_complete_acceptance_commands.py",
    "tests/orchestration/test_review_gate_sensitive_metadata.py",
    "tests/orchestration/test_review_subject_strict_schema.py",
    "tests/orchestration/test_round13_evidence_alignment.py",
    "tests/orchestration/test_run_manifest.py",
    "tests/orchestration/test_run_manifest_aggregate_limits.py",
    "tests/orchestration/test_run_manifest_call_expectation_lifecycle.py",
    "tests/orchestration/test_run_manifest_call_ledger_trust.py",
    "tests/orchestration/test_run_manifest_call_ref_canonical_numbers.py",
    "tests/orchestration/test_run_manifest_call_ref_grammar.py",
    "tests/orchestration/test_run_manifest_call_task_binding.py",
    "tests/orchestration/test_run_manifest_canonical_bytes.py",
    "tests/orchestration/test_run_manifest_chain_append.py",
    "tests/orchestration/test_run_manifest_cross_episode_concurrency.py",
    "tests/orchestration/test_run_manifest_episode_graph.py",
    "tests/orchestration/test_run_manifest_exact_ledger_set.py",
    "tests/orchestration/test_run_manifest_export_allowlist.py",
    "tests/orchestration/test_run_manifest_external_schema.py",
    "tests/orchestration/test_run_manifest_hash_bindings.py",
    "tests/orchestration/test_run_manifest_idempotent_chain_integrity.py",
    "tests/orchestration/test_run_manifest_immutable_artifacts.py",
    "tests/orchestration/test_run_manifest_index_canonical.py",
    "tests/orchestration/test_run_manifest_integrity.py",
    "tests/orchestration/test_run_manifest_ledger_chain_continuity.py",
    "tests/orchestration/test_run_manifest_ledger_identity_safety.py",
    "tests/orchestration/test_run_manifest_ledger_ref_uniqueness.py",
    "tests/orchestration/test_run_manifest_ledger_semantics.py",
    "tests/orchestration/test_run_manifest_logical_identity.py",
    "tests/orchestration/test_run_manifest_prework_resume.py",
    "tests/orchestration/test_run_manifest_publication_races.py",
    "tests/orchestration/test_run_manifest_recovery.py",
    "tests/orchestration/test_run_manifest_reference_coverage.py",
    "tests/orchestration/test_run_manifest_role_agreement.py",
    "tests/orchestration/test_run_manifest_root_containment.py",
    "tests/orchestration/test_run_manifest_runtime_truth.py",
    "tests/orchestration/test_run_manifest_schema.py",
    "tests/orchestration/test_run_manifest_security.py",
    "tests/orchestration/test_run_manifest_size_limits.py",
    "tests/orchestration/test_run_manifest_snapshot_phase_requirements.py",
    "tests/orchestration/test_run_manifest_staging_cleanup.py",
    "tests/orchestration/test_run_manifest_standard_json.py",
    "tests/orchestration/test_run_manifest_strict_boundaries.py",
    "tests/orchestration/test_run_manifest_task_history_chain.py",
    "tests/orchestration/test_run_manifest_task_lifecycle_binding.py",
    "tests/orchestration/test_run_manifest_terminal_consistency.py",
    "tests/orchestration/test_run_manifest_terminal_ledger_finality.py",
    "tests/orchestration/test_run_manifest_writer_postconditions.py",
    "tests/orchestration/test_run_manifest_zero_call_expectations.py",
    "tests/orchestration/test_run_report.py",
    "tests/orchestration/test_run_task_list.py",
    "tests/orchestration/test_scope_question.py",
    "tests/orchestration/test_self_use_findings.py",
    "tests/orchestration/test_self_use_generator.py",
    "tests/orchestration/test_self_use_queue.py",
    "tests/orchestration/test_self_use_runner.py",
    "tests/orchestration/test_serve_daemon.py",
    "tests/orchestration/test_serve_runs.py",
    "tests/orchestration/test_steering.py",
    "tests/orchestration/test_steering_consumption.py",
    "tests/orchestration/test_steering_mission.py",
    "tests/orchestration/test_steering_notes.py",
    "tests/orchestration/test_stream_evidence.py",
    "tests/orchestration/test_stream_evidence_integration.py",
    "tests/orchestration/test_structure_measure.py",
    "tests/orchestration/test_task_deliverables.py",
    "tests/orchestration/test_task_edit_runtime.py",
    "tests/orchestration/test_task_expectation_episode_context.py",
    "tests/orchestration/test_task_expectation_status_truth.py",
    "tests/orchestration/test_task_injection_runner.py",
    "tests/orchestration/test_task_veto.py",
    "tests/orchestration/test_task_veto_runner.py",
    "tests/orchestration/test_test_runner.py",
    "tests/orchestration/test_token_ledger.py",
    "tests/orchestration/test_tool_sandbox.py",
    "tests/orchestration/test_veto_proposal.py",
    "tests/orchestration/test_watchdog.py",
    "tests/orchestration/test_worker_pulse.py",
    "tests/regression/test_f293_acceptance.py",
    "tests/regression/test_f294_acceptance.py",
    "tests/regression/test_lab_orders_20261020.py",
    "tests/regression/test_named_bugs.py",
    "tests/regression/test_readme_order_20261017.py",
    "tests/regression/test_resource_safety.py",
    "tests/regression/test_test_load_governor.py",
    "tests/runtimes/test_dev_server.py",
    "tests/runtimes/test_dev_server_ports.py",
    "tests/test_agent_tooling.py",
    "tests/test_ble001_ratchet.py",
    "tests/test_cli_main.py",
    "tests/test_command_catalog.py",
    "tests/test_data_paths.py",
    "tests/test_data_root_isolation.py",
    "tests/test_grouped_cli.py",
    "tests/test_no_orphan_modules.py",
    "tests/test_parametrize_ids_stable.py",
    "tests/test_project_constitution.py",
    "tests/test_remedy_smoke_script.py",
    "tests/test_reserved_namespaces.py",
    "tests/test_structure_ratchet.py",
    "tests/test_subprocess_timeouts.py",
    "tests/test_timeline.py",
    "tests/ui_server/test_command_channel.py",
    "tests/ui_server/test_pause_e2e_live.py",
    "tests/ui_server/test_public_api.py",
    "tests/ui_server/test_public_api_client_scope.py",
    "tests/ui_server/test_public_api_lifecycle.py",
])
#: `not legacy` deselects the standing D3 quarantine; the names after it deselect the test
#: functions whose parameter ids the packaging scan reads as a local path or a secret, the ones the
#: reviewer's precheck at `358617a72` found among these files, as F306's evidence did, and the
#: three F311's precheck at `f3dd90844` found among the files its rounds added.
_UNSAFE_ID_FUNCTIONS = (
    "test_a_budget_answer_above_a_ceiling_is_refused_naming_its_limit",
    "test_a_budget_answer_inside_the_ceilings_or_outside_the_policy_is_passed_on",
    "test_a_malformed_job_id_is_a_usage_error",
    "test_a_missing_or_broken_sandbox_refuses_and_runs_nothing",
    "test_a_nonce_that_cannot_be_a_filename_is_400_on_its_own_field",
    "test_a_path_value_that_begins_with_a_dash_is_400_and_runs_nothing",
    "test_a_private_path_never_survives",
    "test_a_real_path_is_still_redacted",
    "test_a_secret_never_reaches_the_record",
    "test_absolute_and_traversing_refs_are_rejected",
    "test_an_absolute_path_never_reaches_the_record",
    "test_an_invalid_identity_field_is_rejected",
    "test_an_undeclared_key_a_repeated_key_or_a_bad_value_is_400",
    "test_an_unknown_full_id_or_a_value_that_is_no_id_is_run_not_found",
    "test_an_unknown_or_path_shaped_id_is_order_not_found",
    "test_an_unsafe_call_id_blocks",
    "test_an_unsafe_episode_id_blocks",
    "test_an_unsupported_status_blocks",
    "test_it_now_blocks",
    "test_kind_is_a_closed_enum",
    "test_other_multi_segment_tokens_are_still_paths",
    "test_read_order_record_refuses_a_malformed_or_unknown_id",
    "test_real_paths_still_flagged",
    "test_role_is_a_closed_enum",
    "test_secret_shapes_redacted",
    "test_sk_key_at_token_boundary_redacted",
    "test_the_api_port_answers_every_cockpit_only_path_404",
    "test_the_call_identity_validator_uses_the_same_grammar",
    "test_the_rest_of_the_grammar_blocks",
    "test_unsafe_identity_blocks",
)
DESELECT = " and ".join(["not legacy", *(f"not {n}" for n in _UNSAFE_ID_FUNCTIONS)])


def git(*args: str) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout.strip()


def test_output_lines(text: str) -> list[str]:
    """The lines of a pytest output, so a guard line the run printed is shown in the log."""
    return [line.strip() for line in text.splitlines() if line.strip()]


def main() -> int:
    repo_root = Path(".").resolve()
    sys.path.insert(0, str(repo_root / "scripts"))
    from build_review_manifest import _unsafe_text, validate_evidence_candidate, validate_verification_tests

    head_commit = git("rev-parse", "HEAD")
    ancestry = git("rev-list", "--count", "--ancestry-path", f"{BASE}..{head_commit}")
    plain = git("rev-list", "--count", "--first-parent", f"{BASE}..{head_commit}")
    print(f"head {head_commit}\nancestry-path count {ancestry}\nfirst-parent count {plain}")
    if ancestry != plain:
        print("ERROR: the two counts differ, so the base is wrong (pitfall (e)); stopping")
        return 1

    data_root = (repo_root / ".remedy-wt" / "f303-r8-evidence-data").resolve()
    if data_root.exists():
        shutil.rmtree(data_root)
    data_root.mkdir(parents=True)
    run_env = dict(os.environ, REMEDY_DATA_DIR=str(data_root))
    print("data root for the run: .remedy-wt/f303-r8-evidence-data (fresh, empty)")
    collect = subprocess.run(["python3", "-m", "pytest", "--collect-only", "-q", "-k", DESELECT, *TEST_FILES],
                             cwd=repo_root, capture_output=True, text=True, check=False, env=run_env)
    node_ids = [ln.strip() for ln in collect.stdout.split("\n") if ln.startswith("tests/") and "::" in ln]
    collected = re.search(r"(\d+)/(\d+) tests? collected \((\d+) deselected\)", collect.stdout)
    if collected:
        selected, total, deselected = (int(collected.group(i)) for i in (1, 2, 3))
    else:
        plain_count = re.search(r"(\d+) tests? collected", collect.stdout)
        selected = total = int(plain_count.group(1)) if plain_count else -1
        deselected = 0
    if selected != len(node_ids) or not node_ids or selected + deselected != total:
        print(f"ERROR: collect-only count mismatch: {selected}/{total} ({deselected}) vs {len(node_ids)}")
        return 1
    print(f"collected node ids {len(node_ids)}, deselected {deselected}")

    unsafe = [(nid, _unsafe_text(nid)) for nid in node_ids if _unsafe_text(nid) is not None]
    print(f"red control: unsafe among the real ids {len(unsafe)} {unsafe[:3]}")
    print(f"red control: planted id -> {_unsafe_text('tests/x.py::test_a[/home/someone/secret]')}")
    if unsafe:
        return 1

    run = subprocess.run(["python3", "-m", "pytest", "-v", "-k", DESELECT, *TEST_FILES], cwd=repo_root,
                         capture_output=True, text=True, check=False, env=run_env)
    guard = [line for line in test_output_lines(run.stdout) if line.startswith(("R-0803:", "R-1139"))
             or "process(es) behind" in line]
    print(f"guard lines {guard}")
    test_output = run.stdout
    counts = {"passed": 0, "failed": 0, "skipped": 0}
    for line in test_output.split("\n")[-15:]:
        for word in counts:
            found = re.search(rf"(\d+) {word}", line)
            if found:
                counts[word] = int(found.group(1))
    output_hash = hashlib.sha256(test_output.encode()).hexdigest()
    print(f"pytest exit {run.returncode}, {counts}, output_hash {output_hash}")

    verification_runs = [{
        "run_id": "vr-1303",
        "command": f"python3 -m pytest -v -k '{DESELECT}' {' '.join(TEST_FILES)}",
        "exit_code": run.returncode,
        "passed": counts["passed"],
        "failed": counts["failed"],
        "skipped": counts["skipped"],
        "selected": len(node_ids),
        "deselected": deselected,
        "test_files": TEST_FILES,
        "node_ids": node_ids,
        "output_hash": output_hash,
        "duration_seconds": 0.0,
        "stdout_summary": f"{counts['passed']} passed",
        "head_sha": head_commit,
    }]

    from packages.orchestration.job_evidence import create_manual_completion_bundle

    evidence_dir = Path(EVIDENCE_DIR).resolve()
    if evidence_dir.exists():
        shutil.rmtree(evidence_dir)
    evidence_dir.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc)
    summary = create_manual_completion_bundle(
        str(evidence_dir),
        repo_root=".",
        base_commit=BASE,
        head_commit=head_commit,
        job_id="f303r8e1001",
        job_title="F303 round 8 evidence job",
        step_range="T001-T003",
        prior_job_ids=[],
        verification_runs=verification_runs,
        timestamp=now.isoformat(timespec="seconds"),
        generated_at=now.isoformat(timespec="microseconds"),
        review_feature_id="f303",
    )

    vt_path = evidence_dir / "verification_tests.json"
    problems, vt_passed = validate_verification_tests(json.loads(vt_path.read_text(encoding="utf-8")))
    print(f"validate_verification_tests problems {problems} passed {vt_passed}")
    validation = validate_evidence_candidate(str(evidence_dir))
    print(f"is_valid_current_run {validation['is_valid_current_run']}")
    print(f"validation_errors {validation['validation_errors']}")
    print("gates written:", sorted(p.name for p in evidence_dir.glob("*_gate.json"))
          + sorted(p.name for p in evidence_dir.glob("final_verifier_report.json")))
    print(json.dumps(summary, indent=2))
    return 0 if not problems and validation["is_valid_current_run"] and run.returncode == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
