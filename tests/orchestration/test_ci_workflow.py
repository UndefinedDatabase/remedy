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


def test_hosted_workflow_runs_the_floor_and_a_current_interpreter():
    """F273 T016 (a): `requires-python = ">=3.10"` is only true if 3.10 AND 3.12 run it,
    and the setup step reads the matrix rather than pinning one version beside it."""
    text = workflow_text()
    assert text.count("python-version: ['3.10', '3.12']") == 1
    assert text.count("python-version: ${{ matrix.python-version }}") == 1
    assert text.count("python-version:") == 2
    assert "fail-fast: false" in text


def test_hosted_workflow_matrix_names_exactly_the_floor_and_one_current_python():
    """T2_F279 T004: the matrix runs the oldest supported Python and one newer one, no more,
    and its first entry is the floor `requires-python` promises."""
    import re

    matrix = re.search(r"python-version: \[([^\]]*)\]", workflow_text())
    assert matrix is not None
    versions = [v.strip().strip("'\"") for v in matrix.group(1).split(",")]
    assert len(versions) == 2, versions
    floor = re.search(r'requires-python = ">=([0-9.]+)"',
                      (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert floor is not None and versions[0] == floor.group(1)
    assert tuple(map(int, versions[1].split("."))) > tuple(map(int, versions[0].split(".")))


def test_hosted_workflow_checks_out_the_full_history():
    """A shallow clone hides the deleted modules the event-name coupling ratchet reads (R-0889)."""
    text = workflow_text()
    assert text.count("fetch-depth: 0") == 1
    checkout = text.index("actions/checkout@v4")
    assert checkout < text.index("fetch-depth: 0") < text.index("actions/setup-python@v5")


def test_hosted_workflow_installs_the_hash_pinned_toolchain_before_remedy():
    """DECISION F279 D1: the hashed set installs alone, then Remedy resolving nothing, then a check
    that the pinned set covers the declaration — and no step installs anything unpinned."""
    text = workflow_text()
    pinned = "python3 -m pip install --require-hashes -r constraints.txt"
    remedy = "python3 -m pip install --no-deps -e ."
    check = "python3 -m pip check"
    for step in (pinned, remedy, check):
        assert text.count(step) == 1, step
    assert text.index(pinned) < text.index(remedy) < text.index(check) < text.index("remedy ci run")
    installs = [line.strip() for line in text.splitlines()
                if "pip install" in line and line.strip()[:1] != "#"]
    assert installs == [f"run: {pinned}", f"run: {remedy}"]


def test_hosted_workflow_keys_its_pip_cache_on_the_pinned_set():
    """A cache keyed on anything else would survive a change of the pins it serves."""
    assert workflow_text().count("cache-dependency-path: constraints.txt") == 1
