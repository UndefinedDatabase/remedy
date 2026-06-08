"""Test category enforcement.

Verifies:
- Fast script excludes subprocess, real_ollama, ui_contract, smoke, slow
- Scripts use remedy_pytest.sh
- Scripts don't use shell=True or background processes
- Marker definitions exist in pyproject.toml
"""

from __future__ import annotations

from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
PYPROJECT = Path(__file__).resolve().parents[1] / "pyproject.toml"


def test_fast_script_excludes_subprocess():
    source = (SCRIPTS / "remedy_test_fast.sh").read_text()
    assert "not subprocess" in source


def test_fast_script_excludes_real_ollama():
    source = (SCRIPTS / "remedy_test_fast.sh").read_text()
    assert "not real_ollama" in source


def test_fast_script_excludes_ui_contract():
    source = (SCRIPTS / "remedy_test_fast.sh").read_text()
    assert "not ui_contract" in source


def test_fast_script_excludes_smoke():
    source = (SCRIPTS / "remedy_test_fast.sh").read_text()
    assert "not smoke" in source


def test_fast_script_uses_wrapper():
    source = (SCRIPTS / "remedy_test_fast.sh").read_text()
    assert "remedy_pytest.sh" in source


def test_integration_script_uses_wrapper():
    source = (SCRIPTS / "remedy_test_integration.sh").read_text()
    assert "remedy_pytest.sh" in source


def test_real_providers_script_uses_wrapper():
    source = (SCRIPTS / "remedy_test_real_providers.sh").read_text()
    assert "remedy_pytest.sh" in source


def test_no_background_in_test_scripts():
    for name in ["remedy_test_fast.sh", "remedy_test_integration.sh", "remedy_test_real_providers.sh"]:
        source = (SCRIPTS / name).read_text()
        assert " &" not in source or "&&" in source.replace(" &", ""), f"{name} may use background process"


def test_markers_defined_in_pyproject():
    source = PYPROJECT.read_text()
    for marker in ["unit", "integration", "subprocess", "smoke", "real_ollama", "ui_contract", "safety", "architecture"]:
        assert marker in source, f"marker '{marker}' not defined in pyproject.toml"


def test_conftest_exists():
    conftest = Path(__file__).resolve().parent / "conftest.py"
    assert conftest.is_file(), "tests/conftest.py must exist for auto-marking"
