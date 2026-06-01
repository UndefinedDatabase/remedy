"""Guard test: no new step-numbered test files allowed."""
from pathlib import Path


def test_no_step_numbered_test_files():
    """Step-numbered test files (test_step*.py) are retired.

    Tests live in domain directories: orchestration/, ui_server/, cli/,
    ui_contracts/, storage/, regression/.  See tests/README.md.
    """
    tests_dir = Path(__file__).resolve().parent
    step_files = (
        list(tests_dir.glob("test_steps_*.py"))
        + list(tests_dir.glob("test_step_*.py"))
    )
    assert step_files == [], (
        f"Step-numbered test files found: {[f.name for f in step_files]}. "
        "New tests must go in domain directories. See tests/README.md."
    )
