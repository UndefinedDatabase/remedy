"""Root conftest — automatic pytest marker assignment.

Marks are assigned based on file path patterns so individual test files
don't need @pytest.mark decorators for category classification.
"""

import pytest


@pytest.fixture(autouse=True)
def _reset_config_cache():
    """Keep the process-global config cache from leaking between tests.

    ``get_config()`` memoises a ``RemedyConfig`` in a module-level global, and
    ``load_config()`` resolves ``data_dir`` from ``REMEDY_DATA_DIR`` (and from a
    cwd-relative ``remedy.toml``). A test that sets ``REMEDY_DATA_DIR`` via
    ``monkeypatch`` therefore bakes its temp path into the cache; monkeypatch
    restores the environment afterwards but cannot undo the cache. Every later
    test in the same xdist worker then reads a stale ``data_dir``:
    ``resolve_data_root()`` finds no env var, falls through to the cached
    config, and returns the previous test's temp directory.

    Measured effect before this fixture: running
    ``test_job_rerun_manifest.py::TestCurrentTargetDrift`` first made every
    ``test_grouped_cli.py::TestGroupedExecution`` JSON test fail with
    "Job not found" — ``save_job()`` wrote to the leaked temp root while the
    CLI subprocess resolved the real one. Order-dependent, so it surfaced as
    flake under ``-n auto``.

    Resetting on both sides makes each test start from a cold cache.
    """
    from packages.orchestration.config import reset_config
    reset_config()
    yield
    reset_config()


@pytest.fixture(autouse=True)
def _restore_cwd():
    """Undo a working-directory change that a test forgot to reverse.

    Several tests ``os.chdir`` into a temp directory. When one of them fails
    early — or simply never restores — the process keeps that directory, and
    every later test in the same xdist worker that reads a repo file by a
    RELATIVE path breaks:

        FileNotFoundError: 'scripts/remedy_smoke.sh'
        FileNotFoundError: 'packages/orchestration/ui_server.py'

    Whether a victim runs before or after the offender depends on the xdist
    schedule, so it presents as flake. Restoring the directory after every test
    keeps one test's chdir from becoming another test's missing file.
    """
    import os
    before = os.getcwd()
    yield
    if os.getcwd() != before:
        os.chdir(before)


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
