"""Contract tests for smoke scripts.

Verifies:
- Backend smoke shell delegates to Python supervisor
- Python supervisors use smoke_runner (Popen + isolation)
- No shell=True in supervisors or runner
- No || true in shell scripts
- Shell scripts don't run pytest directly (use remedy_pytest.sh)
"""

from __future__ import annotations

from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"


def test_backend_smoke_sh_delegates_to_python():
    source = (SCRIPTS / "remedy_backend_basis_smoke.sh").read_text()
    assert "remedy_backend_basis_smoke.py" in source
    # Should not chain pytest directly
    assert "python3 -m pytest" not in source


def test_backend_smoke_py_uses_smoke_runner():
    source = (SCRIPTS / "remedy_backend_basis_smoke.py").read_text()
    assert "from smoke_runner import run_phase" in source
    assert "shell=True" not in source


def test_runtime_wrapper_smoke_sh_delegates_to_python():
    source = (SCRIPTS / "remedy_runtime_wrapper_smoke.sh").read_text()
    assert "remedy_runtime_wrapper_smoke.py" in source
    assert "python3 -m pytest" not in source


def test_runtime_wrapper_smoke_py_uses_smoke_runner():
    source = (SCRIPTS / "remedy_runtime_wrapper_smoke.py").read_text()
    assert "from smoke_runner import run_phase" in source
    assert "shell=True" not in source


def test_smoke_runner_no_shell_true():
    source = (SCRIPTS / "smoke_runner.py").read_text()
    # Verify no subprocess call uses shell=True (check Popen/run calls)
    import re
    # Match shell=True that appears as a keyword argument (not in strings/comments)
    calls = re.findall(r"(?:Popen|subprocess\.run)\([^)]*shell\s*=\s*True", source)
    assert not calls, f"smoke_runner.py uses shell=True in subprocess call: {calls}"


def test_smoke_runner_uses_start_new_session():
    source = (SCRIPTS / "smoke_runner.py").read_text()
    assert "start_new_session=True" in source


def test_smoke_runner_uses_temp_files():
    source = (SCRIPTS / "smoke_runner.py").read_text()
    assert "NamedTemporaryFile" in source


def test_process_isolation_smoke_sh_delegates_to_python():
    source = (SCRIPTS / "remedy_process_isolation_smoke.sh").read_text()
    assert "remedy_process_isolation_smoke.py" in source
    assert "python3 -m pytest" not in source


def test_process_isolation_smoke_py_uses_smoke_runner():
    source = (SCRIPTS / "remedy_process_isolation_smoke.py").read_text()
    assert "from smoke_runner import run_phase" in source
    assert "shell=True" not in source


def test_backend_smoke_no_helper_tests():
    source = (SCRIPTS / "remedy_backend_basis_smoke.py").read_text()
    assert "test_runtime_helpers" not in source


def test_no_or_true_in_smoke_scripts():
    for name in [
        "remedy_backend_basis_smoke.sh",
        "remedy_runtime_wrapper_smoke.sh",
        "remedy_process_isolation_smoke.sh",
    ]:
        source = (SCRIPTS / name).read_text()
        assert "|| true" not in source, f"{name} contains || true"
