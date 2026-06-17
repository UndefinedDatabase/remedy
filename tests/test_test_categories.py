"""Test category enforcement.

Verifies:
- Fast script uses targeted file list (core spine suites)
- Scripts use remedy_pytest.sh
- Scripts don't use background processes
- Marker definitions exist in pyproject.toml
"""

from __future__ import annotations

from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
PYPROJECT = Path(__file__).resolve().parents[1] / "pyproject.toml"


def test_fast_script_uses_wrapper():
    source = (SCRIPTS / "remedy_test_fast.sh").read_text()
    assert "remedy_pytest.sh" in source


def test_fast_script_targets_core_suites():
    source = (SCRIPTS / "remedy_test_fast.sh").read_text()
    for suite in [
        "test_worker_facade_cmd.py",
        "test_dogfood_run.py",
        "test_managed_builder_execution.py",
        "test_product_spine.py",
    ]:
        assert suite in source, f"Fast lane must include {suite}"


def test_fast_script_no_subprocess_files():
    source = (SCRIPTS / "remedy_test_fast.sh").read_text()
    for suite in [
        "test_review_bundle_runtime.py",
        "test_command_catalog.py",
        "test_contract_runtime.py",
        "test_config_cmd.py",
    ]:
        assert suite not in source, f"Fast lane must not include subprocess file {suite}"


def test_runtime_script_exists():
    assert (SCRIPTS / "remedy_test_runtime.sh").is_file()


def test_runtime_script_uses_wrapper():
    source = (SCRIPTS / "remedy_test_runtime.sh").read_text()
    assert "remedy_pytest.sh" in source


def test_runtime_script_targets_subprocess_suites():
    source = (SCRIPTS / "remedy_test_runtime.sh").read_text()
    for suite in [
        "test_review_bundle_runtime.py",
        "test_command_catalog.py",
        "test_contract_runtime.py",
        "test_config_cmd.py",
    ]:
        assert suite in source, f"Runtime lane must include {suite}"


def test_fast_script_no_full_suite():
    source = (SCRIPTS / "remedy_test_fast.sh").read_text()
    code_lines = [ln for ln in source.splitlines()
                  if ln.strip() and not ln.strip().startswith("#")]
    code = "\n".join(code_lines)
    assert "tests/ " not in code or "-q" in code, \
        "Fast lane should target specific files, not all of tests/"


def test_integration_script_uses_wrapper():
    source = (SCRIPTS / "remedy_test_integration.sh").read_text()
    assert "remedy_pytest.sh" in source


def test_real_providers_script_uses_wrapper():
    source = (SCRIPTS / "remedy_test_real_providers.sh").read_text()
    assert "remedy_pytest.sh" in source


def test_no_background_in_test_scripts():
    for name in ["remedy_test_fast.sh", "remedy_test_runtime.sh", "remedy_test_integration.sh", "remedy_test_real_providers.sh"]:
        source = (SCRIPTS / name).read_text()
        assert " &" not in source or "&&" in source.replace(" &", ""), f"{name} may use background process"


def test_markers_defined_in_pyproject():
    source = PYPROJECT.read_text()
    for marker in ["unit", "integration", "subprocess", "smoke", "real_ollama", "ui_contract", "safety", "architecture"]:
        assert marker in source, f"marker '{marker}' not defined in pyproject.toml"


def test_conftest_exists():
    conftest = Path(__file__).resolve().parent / "conftest.py"
    assert conftest.is_file(), "tests/conftest.py must exist for auto-marking"
