"""Runtime integration gate — verify gate writers are wired into the pipeline.

Deterministic, read-only orchestration logic: no provider calls, no target-repo
mutation, no job state mutation. Uses static analysis (source-text search) to
confirm that the evidence-pipeline module actually *calls* each gate writer,
and binds to executed test records when verification data is provided.

Public API:
    build_runtime_integration_gate(repo_root, checks=None, verification_data=None, feature_id=None) -> dict
    write_runtime_integration_gate(evidence_dir, repo_root, written=None, verification_data=None, feature_id=None) -> None
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.1.0"

_JOB_EVIDENCE = "packages/orchestration/job_evidence.py"

# Each check: the evidence pipeline must reference the given pattern in the
# named source file. ``call_exists`` asserts a writer function is invoked;
# ``artifact_written`` asserts an artifact filename is registered.
_PINGPONG_JOB = "packages/orchestration/pingpong_job.py"
_BUDGET_GUARD = "packages/orchestration/budget_guard.py"
_BUDGET_RES = "packages/orchestration/budget_resolution.py"
_RUN_CONTRACT = "packages/orchestration/run_contract.py"
_DECISION_Q = "packages/orchestration/decision_queue.py"
_RUN_MANIFEST = "packages/orchestration/run_manifest.py"
_CONFIG = "packages/orchestration/config.py"
_DO_CMD = "apps/cli/commands/do_cmd.py"

_F018_TEST = "tests/orchestration/test_f018_authority_integration.py"
_F146_REGISTRY = "packages/orchestration/project_registry.py"
_F146_CLI = "apps/cli/commands/project.py"
_F146_RESOLUTION_TEST = "tests/orchestration/test_project_resolution.py"
_F146_CLI_TEST = "tests/cli/test_project_current.py"
_F146_REGISTRY_TEST = "tests/test_project_registry.py"

INTEGRATION_CHECKS: tuple[dict[str, str], ...] = (
    # Gate-writer meta-checks
    {
        "check_id": "job_evidence_calls_fresh_evidence_gate",
        "source_file": _JOB_EVIDENCE,
        "check_type": "call_exists",
        "pattern": "write_fresh_evidence_gate",
    },
    {
        "check_id": "job_evidence_calls_artifact_contract_gate",
        "source_file": _JOB_EVIDENCE,
        "check_type": "call_exists",
        "pattern": "write_artifact_contract_gate",
    },
    {
        "check_id": "job_evidence_calls_runtime_integration_gate",
        "source_file": _JOB_EVIDENCE,
        "check_type": "call_exists",
        "pattern": "write_runtime_integration_gate",
    },
    {
        "check_id": "job_evidence_calls_change_provenance_gate",
        "source_file": _JOB_EVIDENCE,
        "check_type": "call_exists",
        "pattern": "write_change_provenance_gate",
    },
    {
        "check_id": "job_evidence_calls_commit_execution_gate",
        "source_file": _JOB_EVIDENCE,
        "check_type": "call_exists",
        "pattern": "write_commit_execution_gate",
    },
    # F018: budget system production-path integration checks
    {
        "check_id": "f018_run_job_calls_collect_counters",
        "source_file": _PINGPONG_JOB,
        "check_type": "call_exists",
        "pattern": "collect_counters_from_actuals",
    },
    {
        "check_id": "f018_run_job_persists_budget_actuals",
        "source_file": _PINGPONG_JOB,
        "check_type": "call_exists",
        "pattern": "_persist_budget_actuals",
    },
    {
        "check_id": "f018_run_job_uses_first_running_at",
        "source_file": _PINGPONG_JOB,
        "check_type": "call_exists",
        "pattern": "first_running_at",
    },
    {
        "check_id": "f018_config_fail_closed_budgets",
        "source_file": _CONFIG,
        "check_type": "call_exists",
        "pattern": "fail_closed_for_budgets",
    },
    {
        "check_id": "f018_budget_resolution_project_root",
        "source_file": _BUDGET_RES,
        "check_type": "call_exists",
        "pattern": "project_root",
    },
    {
        "check_id": "f018_run_manifest_decode_budgets",
        "source_file": _RUN_MANIFEST,
        "check_type": "call_exists",
        "pattern": "_decode_budgets_field",
    },
    {
        "check_id": "f018_run_contract_reconcile_budgets",
        "source_file": _RUN_CONTRACT,
        "check_type": "call_exists",
        "pattern": "_reconcile_budget_fields",
    },
    {
        "check_id": "f018_decision_queue_budget_actions",
        "source_file": _DECISION_Q,
        "check_type": "call_exists",
        "pattern": "\"extend\", \"abandon\"",
    },
    {
        "check_id": "f018_do_job_plan_budget_flags",
        "source_file": _DO_CMD,
        "check_type": "call_exists",
        "pattern": "resolve_job_budgets",
    },
    {
        "check_id": "f018_budget_guard_counter_validation",
        "source_file": _BUDGET_GUARD,
        "check_type": "call_exists",
        "pattern": "BudgetCounterError",
    },
    # F146: project identity production-path integration checks
    {
        "check_id": "f146_registry_atomic_save",
        "source_file": _F146_REGISTRY,
        "check_type": "call_exists",
        "pattern": "os.replace",
    },
    {
        "check_id": "f146_registry_read_only_resolution",
        "source_file": _F146_REGISTRY,
        "check_type": "call_exists",
        "pattern": "_find_project_by_repo_readonly",
    },
    {
        "check_id": "f146_registry_ambiguous_error",
        "source_file": _F146_REGISTRY,
        "check_type": "call_exists",
        "pattern": "AmbiguousProjectError",
    },
    {
        "check_id": "f146_registry_invalid_selector",
        "source_file": _F146_REGISTRY,
        "check_type": "call_exists",
        "pattern": "InvalidProjectSelectorError",
    },
    {
        "check_id": "f146_registry_register_primitive",
        "source_file": _F146_REGISTRY,
        "check_type": "call_exists",
        "pattern": "register_project_repo",
    },
    {
        "check_id": "f146_cli_select_project",
        "source_file": _F146_CLI,
        "check_type": "call_exists",
        "pattern": "select_project",
    },
    {
        "check_id": "f146_cli_not_a_git_repo_error",
        "source_file": _F146_CLI,
        "check_type": "call_exists",
        "pattern": "NotAGitRepoError",
    },
    {
        "check_id": "f146_cli_attach_canonical",
        "source_file": _F146_CLI,
        "check_type": "call_exists",
        "pattern": "attach_repo_canonical",
    },
    {
        "check_id": "f146_registry_not_a_git_repo_error",
        "source_file": _F146_REGISTRY,
        "check_type": "call_exists",
        "pattern": "NotAGitRepoError",
    },
    {
        "check_id": "f146_registry_attach_canonical",
        "source_file": _F146_REGISTRY,
        "check_type": "call_exists",
        "pattern": "attach_repo_canonical",
    },
    {
        "check_id": "f146_registry_slug_validation",
        "source_file": _F146_REGISTRY,
        "check_type": "call_exists",
        "pattern": "_validate_slug",
    },
    {
        "check_id": "f146_registry_lookup_readonly",
        "source_file": _F146_REGISTRY,
        "check_type": "call_exists",
        "pattern": "_lookup_by_slug_or_uuid_readonly",
    },
    {
        "check_id": "f146_registry_migrate_legacy",
        "source_file": _F146_REGISTRY,
        "check_type": "call_exists",
        "pattern": "migrate_legacy_projects",
    },
)

TEST_EXECUTION_BINDINGS: tuple[dict[str, Any], ...] = (
    {
        "check_id": "f018_test_authority_integration_execution",
        "check_type": "test_execution_binding",
        "test_file": _F018_TEST,
        "min_passed": 70,
        "critical_node_ids": [
            "TestStoppedJobBudgetOverrideBlocked::test_run_job_rejects_budget_on_stopped",
            "TestClosedSourceVocabulary::test_unknown_source_rejected",
            "TestClosedSourceVocabulary::test_valid_sources_accepted",
            "TestStrictActualsRejectCoercion",
            "TestCorruptPersistedBudgetsBlock",
            "TestPersistedActualsSchemaVersion",
            "TestPersistedActualsMissingSources",
            "TestCorruptFirstRunningAt",
        ],
    },
    {
        "check_id": "f018_test_budget_guard_execution",
        "check_type": "test_execution_binding",
        "test_file": "tests/orchestration/test_budget_guard.py",
        "min_passed": 45,
        "critical_node_ids": [
            "TestBudgetCounters::test_rejects_inconsistent_call_counts",
            "TestBudgetCounters::test_rejects_negative_provider_calls",
        ],
    },
    {
        "check_id": "f018_test_job_budgets_execution",
        "check_type": "test_execution_binding",
        "test_file": "tests/orchestration/test_job_budgets.py",
        "min_passed": 65,
    },
    {
        "check_id": "f018_test_budget_stop_integration_execution",
        "check_type": "test_execution_binding",
        "test_file": "tests/orchestration/test_budget_stop_integration.py",
        "min_passed": 30,
    },
    # F146: project identity test execution bindings
    {
        "check_id": "f146_test_resolution_execution",
        "check_type": "test_execution_binding",
        "test_file": _F146_RESOLUTION_TEST,
        "min_passed": 50,
        "critical_node_ids": [
            "TestReadOnlyResolution::test_resolve_does_not_write",
            "TestReadOnlyResolution::test_resolve_legacy_project_does_not_write",
            "TestAmbiguousProjectError::test_duplicate_slug_raises",
            "TestSelectProject::test_empty_flag_raises_invalid",
            "TestSelectProject::test_empty_env_raises_invalid",
            "TestAtomicSave::test_save_uses_atomic_replace",
            "TestRegisterProjectRepo::test_creates_with_slug_and_canonical",
            "TestRegisterProjectRepo::test_same_repo_returns_existing",
            "TestRegisterProjectRepo::test_create_project_assigns_slug_immediately",
            "TestManagedWorktreeParent::test_worktree_path_without_git_returns_none",
            "TestSelectProject::test_env_uuid",
            "TestSelectProject::test_env_slug",
            "TestSelectProject::test_env_beats_cwd",
            "TestSelectProject::test_flag_beats_env_and_cwd",
        ],
    },
    {
        "check_id": "f146_test_cli_execution",
        "check_type": "test_execution_binding",
        "test_file": _F146_CLI_TEST,
        "min_passed": 10,
        "critical_node_ids": [
            "TestProjectCurrentCommand::test_json_output_exact_schema",
            "TestProjectCurrentCommand::test_project_flag_overrides_cwd",
            "TestProjectCurrentCommand::test_env_source_in_json",
            "TestProjectCurrentCommand::test_job_count_uses_job_ids_len",
            "TestProjectAttachCommand::test_attach_rejects_non_git",
            "TestProjectAttachCommand::test_attach_json_output",
            "TestProjectAttachCommand::test_attach_same_path_idempotent",
            "TestProjectAttachCommand::test_attach_with_project_flag",
            "TestWorkspaceKeyGuard::test_no_forbidden_imports",
        ],
    },
    {
        "check_id": "f146_test_registry_execution",
        "check_type": "test_execution_binding",
        "test_file": _F146_REGISTRY_TEST,
        "min_passed": 40,
        "critical_node_ids": [
            "TestSaveLoadRoundtrip::test_roundtrip",
            "TestReadOnlyProofs::test_load_readonly_no_write",
            "TestReadOnlyProofs::test_list_readonly_no_write",
            "TestAttachRepo::test_attach_sets_canonical",
            "TestProjectNotFoundError::test_load_missing",
        ],
    },
)


def _read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except (OSError, ValueError):
        return None


def _select_checks_for_feature(
    feature_id: str | None,
) -> tuple[list[dict], list[dict]]:
    """Select integration checks and test bindings by feature.

    Returns (static_checks, test_bindings). When feature_id is None, returns
    all (historical behavior). When set, returns generic pipeline checks plus
    feature-specific checks only — other features' checks are excluded.
    """
    if feature_id is None:
        return (
            [dict(c) for c in INTEGRATION_CHECKS],
            [dict(b) for b in TEST_EXECUTION_BINDINGS],
        )

    prefix = feature_id.lower() + "_"

    static = []
    for c in INTEGRATION_CHECKS:
        cid = c["check_id"]
        is_feature_specific = len(cid) > 4 and cid[0] == "f" and cid[1:4].isdigit()
        if not is_feature_specific or cid.startswith(prefix):
            static.append(dict(c))

    bindings = []
    for b in TEST_EXECUTION_BINDINGS:
        if b["check_id"].startswith(prefix):
            bindings.append(dict(b))

    return static, bindings


def build_runtime_integration_gate(
    repo_root: str,
    checks: list[dict[str, str]] | None = None,
    verification_data: dict[str, Any] | None = None,
    feature_id: str | None = None,
) -> dict[str, Any]:
    """Verify integration via source-text checks and test execution bindings.

    ``checks`` overrides ``INTEGRATION_CHECKS`` when provided. For each
    ``call_exists`` check, the named ``source_file`` is read and searched for
    ``pattern``. ``test_execution_binding`` checks validate against
    ``verification_data`` (the verification_tests.json payload).

    ``feature_id`` (e.g. ``"f146"``) selects only generic pipeline checks
    plus feature-specific checks.  When None, all checks run (historical).

    Gate never passes with zero checks.
    """
    root = Path(repo_root) if repo_root else Path(".")

    if checks is not None:
        active = list(checks)
        selected_bindings = None
    else:
        active, selected_bindings = _select_checks_for_feature(feature_id)

    results: list[dict[str, Any]] = []
    issues: list[str] = []

    for check in active:
        check_id = str(check.get("check_id", ""))
        source_file = str(check.get("source_file", ""))
        check_type = str(check.get("check_type", "call_exists"))
        pattern = str(check.get("pattern", ""))

        text = _read_text(root / source_file)
        found = bool(pattern) and text is not None and pattern in text
        file_missing = text is None

        results.append({
            "check_id": check_id,
            "source_file": source_file,
            "check_type": check_type,
            "pattern": pattern,
            "found": found,
            "file_missing": file_missing,
        })

        if not found:
            if file_missing:
                issues.append(f"{check_id}: source file {source_file!r} not found")
            else:
                issues.append(
                    f"{check_id}: pattern {pattern!r} not found in {source_file!r}"
                )

    if checks is None:
        _bind_test_execution(
            results, issues, verification_data,
            bindings_override=selected_bindings,
        )

    if not results:
        return {
            "schema_version": SCHEMA_VERSION,
            "verdict": "BLOCKED",
            "checks": [],
            "checks_total": 0,
            "checks_passed": 0,
            "issues": ["gate has zero checks"],
        }

    all_passed = all(r["found"] for r in results)
    verdict = "PASS" if all_passed else "BLOCKED"

    gate: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "verdict": verdict,
        "checks": results,
        "checks_total": len(results),
        "checks_passed": sum(1 for r in results if r["found"]),
        "issues": issues,
    }
    if feature_id is not None:
        gate["feature_id"] = feature_id
    return gate


def _bind_test_execution(
    results: list[dict[str, Any]],
    issues: list[str],
    verification_data: dict[str, Any] | None,
    bindings_override: list[dict[str, Any]] | None = None,
) -> None:
    """Validate test execution bindings against verification run data.

    Uses ``bindings_override`` when provided, otherwise ``TEST_EXECUTION_BINDINGS``.
    """
    runs = []
    if isinstance(verification_data, dict):
        runs = verification_data.get("runs") or []

    active_bindings = bindings_override if bindings_override is not None else TEST_EXECUTION_BINDINGS
    for binding in active_bindings:
        check_id = binding["check_id"]
        test_file = binding["test_file"]
        min_passed = int(binding.get("min_passed", 1))

        bound_run = None
        for run in runs:
            run_files = run.get("test_files") or []
            if test_file not in run_files:
                continue
            if run.get("exit_code", -1) != 0:
                continue
            if (run.get("passed") or 0) < min_passed:
                continue
            bound_run = {
                "run_id": run.get("run_id", ""),
                "command": run.get("command", ""),
                "exit_code": run.get("exit_code", -1),
                "passed": run.get("passed", 0),
                "failed": run.get("failed", 0),
                "skipped": run.get("skipped", 0),
                "selected": run.get("selected", 0),
                "node_ids": run.get("node_ids", []),
                "output_hash": run.get("output_hash", ""),
                "head_sha": run.get("head_sha", ""),
            }
            break

        found = bound_run is not None
        critical = binding.get("critical_node_ids") or []
        missing_critical: list[str] = []
        if found and critical and bound_run is not None:
            run_nodes = bound_run.get("node_ids") or []
            for crit in critical:
                if not any(crit in nid for nid in run_nodes):
                    missing_critical.append(crit)
            if missing_critical:
                found = False

        entry: dict[str, Any] = {
            "check_id": check_id,
            "check_type": "test_execution_binding",
            "test_file": test_file,
            "min_passed": min_passed,
            "found": found,
        }
        if critical:
            entry["critical_node_ids"] = critical
        if bound_run is not None:
            entry["bound_run"] = bound_run
        results.append(entry)

        if missing_critical:
            issues.append(
                f"{check_id}: critical node(s) missing from execution: "
                f"{missing_critical}")
        elif not found:
            issues.append(
                f"{check_id}: no passing execution for {test_file!r} "
                f"(need >= {min_passed} passed, exit_code 0)"
            )


def write_runtime_integration_gate(
    evidence_dir: str,
    repo_root: str,
    written: dict[str, str] | None = None,
    verification_data: dict[str, Any] | None = None,
    feature_id: str | None = None,
) -> None:
    """Build and write ``runtime_integration_gate.json`` into ``evidence_dir``.

    Registers the written path in ``written`` when provided. No-op when
    ``evidence_dir`` is empty.
    """
    if not evidence_dir:
        return

    gate = build_runtime_integration_gate(
        repo_root, verification_data=verification_data,
        feature_id=feature_id,
    )

    out_dir = Path(evidence_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "runtime_integration_gate.json"
    json_path.write_text(json.dumps(gate, indent=2) + "\n", encoding="utf-8")

    if written is not None:
        written["runtime_integration_gate.json"] = str(json_path)
