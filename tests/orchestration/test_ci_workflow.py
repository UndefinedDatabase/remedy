"""Guards that keep the hosted CI workflow a THIN WRAPPER (T2_F083).

The workflow is read as TEXT and never parsed. PyYAML is in neither
`dependencies` nor the `dev` extra of `pyproject.toml`, so a `yaml.safe_load`
guard would raise ImportError on exactly the clean checkout these guards exist to
protect. Every assertion about stage selection is made against a stage's marker
EXPRESSION, never against its NAME: `ui` is a substring of `apps/ui`, so a
name-based assertion would be red by construction and would say nothing.
"""
from __future__ import annotations

from pathlib import Path

from packages.orchestration.ci_stages import CI_STAGES

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "ci.yml"


def workflow_text() -> str:
    """The hosted workflow as text — the single subject of every guard below."""
    return WORKFLOW_PATH.read_text()


def test_hosted_workflow_file_exists():
    """A hosted CI that is not on disk at the path GitHub reads runs nothing."""
    assert WORKFLOW_PATH.is_file(), WORKFLOW_PATH


def test_hosted_workflow_calls_the_ci_entrypoint():
    """One source of truth for what CI means: the job calls the same entrypoint."""
    assert "remedy ci run" in workflow_text()


def test_hosted_workflow_selects_no_tests_of_its_own():
    """A selection in YAML would give CI a second opinion about what CI means."""
    text = workflow_text()
    for stage in CI_STAGES:
        assert stage.marker_expression not in text, stage.name
    assert "--stage" not in text
    assert "pytest" not in text


def test_hosted_workflow_installs_the_ui_toolchain_before_the_run():
    """DECISION F083 D6 makes the toolchain a precondition, so its step comes first."""
    text = workflow_text()
    assert text.count("npm ci --prefix apps/ui") == 1
    assert text.count("remedy ci run") == 1
    assert text.index("npm ci --prefix apps/ui") < text.index("remedy ci run")


def test_hosted_workflow_never_auto_retries():
    """T2_F083 rules that retries hide rot, so no non-comment line may re-attempt."""
    lines = [line for line in workflow_text().splitlines() if line.strip()[:1] != "#"]
    for token in ("continue-on-error", "retry", "max_attempts"):
        assert [line for line in lines if token in line] == [], token
