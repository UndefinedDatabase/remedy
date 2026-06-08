"""Root conftest — automatic pytest marker assignment.

Marks are assigned based on file path patterns so individual test files
don't need @pytest.mark decorators for category classification.
"""

import pytest

# Files that spawn subprocesses (CLI runtime, grouped CLI, etc.)
SUBPROCESS_FILES = {
    "test_propose_cli_runtime.py",
    "test_worker_cli_runtime.py",
    "test_runtime_helpers.py",
    "test_pytest_runner.py",
    "test_grouped_cli.py",
    "test_job_commands.py",
    "test_command_catalog.py",  # cli/
    "test_project_summary_cli.py",
    "test_event_ledger.py",
    "test_autonomy.py",
    "test_test_runner.py",  # orchestration/
    "test_small_repo_fixtures.py",
    "test_project_brain.py",  # orchestration/
    "test_project_constitution.py",
    "test_agent_loop_execution.py",
    "test_autonomy_readiness.py",
    "test_context_pack.py",
    "test_memory_gateway.py",
    "test_memory_learn.py",
    "test_remedy_smoke_script.py",
    "test_repair_context_reviewer_memory.py",
    "test_test_runner.py",  # root level
    "test_wrapper_behavior.py",
}

# Real Ollama tests (require running server)
REAL_OLLAMA_FILES = {
    "test_real_ollama_smoke.py",
    "test_real_do_ollama_smoke.py",
    "test_builder_eval.py",  # has skipif for real ollama section
}

# Smoke contract tests
SMOKE_FILES = {
    "test_smoke_scripts.py",
    "test_pytest_runner.py",
    "test_builder_bridge_smoke.py",
}

# Safety/resource tests
SAFETY_FILES = {
    "test_resource_safety.py",
    "test_wrapper_behavior.py",
    "test_runtime_helpers.py",
}

# Architecture guard tests
ARCHITECTURE_FILES = {
    "test_no_step_files.py",
    "test_imports.py",
    "test_reserved_namespaces.py",
    "test_data_paths.py",
}


def pytest_collection_modifyitems(items):
    for item in items:
        filename = item.path.name

        # Directory-based marks
        parts = item.path.parts
        if "ui_contracts" in parts:
            item.add_marker(pytest.mark.ui_contract)
        if "ui_server" in parts:
            item.add_marker(pytest.mark.integration)

        # File-based marks
        if filename in SUBPROCESS_FILES:
            item.add_marker(pytest.mark.subprocess)
        if filename in REAL_OLLAMA_FILES:
            item.add_marker(pytest.mark.real_ollama)
        if filename in SMOKE_FILES:
            item.add_marker(pytest.mark.smoke)
        if filename in SAFETY_FILES:
            item.add_marker(pytest.mark.safety)
        if filename in ARCHITECTURE_FILES:
            item.add_marker(pytest.mark.architecture)

        # Default: if no specific mark, it's unit or integration
        # (integration if it uses orchestration/storage directories)
        if "orchestration" in parts or "storage" in parts:
            if not any(
                item.get_closest_marker(m)
                for m in ("subprocess", "real_ollama", "smoke")
            ):
                item.add_marker(pytest.mark.integration)
