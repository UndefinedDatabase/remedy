"""Guards that keep the hosted release gate manual, thin and publish-free (T2_F086).

The workflow is read as TEXT and never parsed. PyYAML is in neither
`dependencies` nor the `dev` extra of `pyproject.toml`, so a `yaml.safe_load`
guard would raise ImportError on exactly the clean checkout these guards exist to
protect — the reasoning `test_ci_workflow.py` already records for `ci.yml`.
"""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "release.yml"
RUNNER_PATH = "scripts/release_gate_check.py"


def workflow_text() -> str:
    """The hosted release workflow as text — the single subject of every guard."""
    return WORKFLOW_PATH.read_text()


def executable_lines() -> list[str]:
    """Every line of the workflow that is not a comment."""
    return [line for line in workflow_text().splitlines() if line.strip()[:1] != "#"]


def test_release_workflow_file_exists():
    """A gate that is not at the path GitHub reads gates nothing."""
    assert WORKFLOW_PATH.is_file(), WORKFLOW_PATH


def test_release_workflow_calls_the_gate_runner_exactly_once():
    """One owner of the rules: the workflow decides nothing of its own."""
    called = [line for line in executable_lines() if RUNNER_PATH in line]
    assert len(called) == 1, called


def test_release_workflow_is_triggered_by_hand_only():
    """Cutting a release is a human decision, so no event may fire this job."""
    text = workflow_text()
    assert any("workflow_dispatch:" in line for line in executable_lines())
    for event in ("\n  push:", "\n  pull_request:", "\n  schedule:", "\n  release:"):
        assert event not in text, event


def test_release_workflow_publishes_nothing():
    """T2_F086's Do-not-touch keeps the final upload a HUMAN command."""
    text = workflow_text().lower()
    for forbidden in ("twine", "pypi", "gh release create", "upload-artifact", "secrets."):
        assert forbidden not in text, forbidden


def test_release_workflow_never_auto_retries():
    """T2_F083 rules that retries hide rot; the release gate inherits that."""
    for token in ("continue-on-error", "retry", "max_attempts"):
        assert [line for line in executable_lines() if token in line] == [], token


def test_release_workflow_passes_the_tag_through_the_environment():
    """A tag interpolated into a shell line would be a command-injection seam."""
    assert any('--tag "$TAG"' in line for line in executable_lines())
    carriers = [line for line in executable_lines() if "inputs.tag" in line]
    assert carriers, "the workflow never reads its own tag input"
    for line in carriers:
        assert line.strip().startswith("TAG:"), line


def test_release_workflow_refuses_when_no_ci_run_is_found():
    """An absent CI answer must not read as a green one."""
    assert any("missing" in line for line in executable_lines())
