"""Install smoke — the wheel installs and the installed CLI works (F086 T2).

DECISION F086 D4 rules that this module is WRITTEN here and EXECUTED elsewhere:
it self-skips unless `REMEDY_INSTALL_SMOKE` is set, because a self-drive round has
neither network access nor permission to spawn an interpreter it has just
installed. What every ordinary run of this file DOES gate is the opt-in decision
and the pure helpers below. What it does NOT gate is the install itself: a
skipped test is not coverage, and F086's DONE condition stays UNPROVEN until the
variable is set on a host that can honour it.

Remedy deliberately does not build the wheel inside this repository. Hatchling
drops every VCS exclusion when the build root is matched by `.gitignore`, so a
probe rooted in a gitignored scratch directory ships files a real wheel omits
(finding R-0574). `resolve_build_root` is that rule written as code.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

INSTALL_SMOKE_ENV = "REMEDY_INSTALL_SMOKE"
REPO_ROOT = Path(__file__).resolve().parents[1]
DISABLED_VALUES = frozenset({"", "0", "false", "no", "off"})
UNKNOWN_MARKER = "dev"
VERSION_REPORT_FIELDS = ("remedy", "build", "python", "platform")
DECLARED_VERSION_PATTERN = re.compile(r'(?m)^version\s*=\s*"([^"]+)"')


def install_smoke_is_enabled(environ: dict[str, str]) -> bool:
    """Return whether the opt-in variable asks for the real install to run."""
    return environ.get(INSTALL_SMOKE_ENV, "").strip().lower() not in DISABLED_VALUES


def resolve_build_root(repo_root: Path, scratch_root: Path) -> Path:
    """Return the wheel build root, refusing any path inside the repository."""
    repo = repo_root.resolve()
    candidate = scratch_root.resolve()
    if candidate == repo or repo in candidate.parents:
        raise ValueError(f"build root {candidate} lies inside the repository {repo}")
    return candidate


def read_declared_version(pyproject_path: Path) -> str:
    """Return the one version literal `pyproject.toml` declares (DECISION F086 D2)."""
    match = DECLARED_VERSION_PATTERN.search(pyproject_path.read_text(encoding="utf-8"))
    if match is None:
        raise ValueError(f"no version declaration in {pyproject_path}")
    return match.group(1)


def parse_version_report(text: str) -> dict[str, str]:
    """Parse `remedy --version` output into its field mapping."""
    fields: dict[str, str] = {}
    for line in text.splitlines():
        name, _, value = line.partition(" ")
        if name in VERSION_REPORT_FIELDS and value.strip():
            fields[name] = value.strip()
    return fields


def version_report_proves_an_install(report: dict[str, str], expected_version: str) -> bool:
    """Return whether the report came from an INSTALLED wheel rather than a checkout."""
    if sorted(report) != sorted(VERSION_REPORT_FIELDS):
        return False
    if report["remedy"] != expected_version or report["remedy"] == UNKNOWN_MARKER:
        return False
    return report["build"] != UNKNOWN_MARKER


def _report_text(version: str = "0.1.0", build: str = "abc1234") -> str:
    """Render a `remedy --version` report the way `render_version_report` does."""
    return f"remedy   {version}\nbuild    {build}\npython   3.11.2\nplatform Linux-6.1"


@pytest.mark.unit
class TestInstallSmokeOptIn:
    """The gate that keeps this module inert on a host that cannot honour it."""

    def test_an_unset_variable_leaves_the_smoke_disabled(self):
        assert install_smoke_is_enabled({}) is False

    def test_every_documented_disabled_value_leaves_it_disabled(self):
        for raw in sorted(DISABLED_VALUES):
            assert install_smoke_is_enabled({INSTALL_SMOKE_ENV: raw}) is False

    def test_any_other_value_enables_it(self):
        assert install_smoke_is_enabled({INSTALL_SMOKE_ENV: "1"}) is True
        assert install_smoke_is_enabled({INSTALL_SMOKE_ENV: " yes "}) is True


@pytest.mark.unit
class TestBuildRootLiesOutsideTheRepository:
    """Finding R-0574 as an executable rule rather than a comment."""

    def test_a_path_inside_the_repository_is_refused(self, tmp_path):
        with pytest.raises(ValueError) as excinfo:
            resolve_build_root(tmp_path, tmp_path / "scratch" / "build")
        assert "lies inside the repository" in str(excinfo.value)

    def test_the_repository_root_itself_is_refused(self, tmp_path):
        with pytest.raises(ValueError):
            resolve_build_root(tmp_path, tmp_path)

    def test_a_sibling_path_is_accepted(self, tmp_path):
        repo = tmp_path / "repo"
        repo.mkdir()
        outside = tmp_path / "outside"
        outside.mkdir()
        assert resolve_build_root(repo, outside) == outside.resolve()


@pytest.mark.unit
class TestVersionReportReading:
    """The `--version` half of F086's DONE condition, parsed and judged."""

    def test_the_declared_version_is_read_from_pyproject(self, tmp_path):
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text('[project]\nname = "remedy"\nversion = "1.2.3"\n')
        assert read_declared_version(pyproject) == "1.2.3"

    def test_a_pyproject_without_a_version_is_refused(self, tmp_path):
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text('[project]\nname = "remedy"\n')
        with pytest.raises(ValueError):
            read_declared_version(pyproject)

    def test_a_real_report_parses_into_its_four_fields(self):
        assert parse_version_report(_report_text()) == {
            "remedy": "0.1.0", "build": "abc1234",
            "python": "3.11.2", "platform": "Linux-6.1",
        }

    def test_an_installed_report_is_accepted(self):
        assert version_report_proves_an_install(parse_version_report(_report_text()), "0.1.0") is True

    def test_a_checkout_report_is_refused_because_both_fields_read_dev(self):
        report = parse_version_report(_report_text(version="dev", build="dev"))
        assert version_report_proves_an_install(report, "0.1.0") is False

    def test_an_embedded_revision_of_dev_is_refused_on_its_own(self):
        report = parse_version_report(_report_text(build="dev"))
        assert version_report_proves_an_install(report, "0.1.0") is False

    def test_a_version_that_differs_from_the_declaration_is_refused(self):
        report = parse_version_report(_report_text(version="0.9.9"))
        assert version_report_proves_an_install(report, "0.1.0") is False

    def test_a_truncated_report_is_refused(self):
        assert version_report_proves_an_install({"remedy": "0.1.0"}, "0.1.0") is False


def _fixture_git_repo(root: Path) -> Path:
    """Create the minimal committed git repository `remedy init` expects."""
    root.mkdir(parents=True)
    env = {
        **os.environ,
        "GIT_AUTHOR_NAME": "smoke", "GIT_AUTHOR_EMAIL": "smoke@example.invalid",
        "GIT_COMMITTER_NAME": "smoke", "GIT_COMMITTER_EMAIL": "smoke@example.invalid",
    }
    subprocess.run(["git", "init", "-q", str(root)], check=True, capture_output=True)
    subprocess.run(
        ["git", "-C", str(root), "commit", "--allow-empty", "-m", "init", "-q"],
        check=True, capture_output=True, env=env,
    )
    return root


@pytest.mark.smoke
@pytest.mark.slow
@pytest.mark.subprocess
@pytest.mark.skipif(
    not install_smoke_is_enabled(dict(os.environ)),
    reason=f"install smoke is opt-in: set {INSTALL_SMOKE_ENV}=1 on a host with network access",
)
def test_the_wheel_installs_and_the_installed_cli_runs_the_golden_path(tmp_path):
    """Build outside the repo, install into a fresh venv, drive the installed CLI."""
    build_root = resolve_build_root(REPO_ROOT, tmp_path / "build")
    subprocess.run(
        ["git", "clone", "--quiet", "--depth", "1", f"file://{REPO_ROOT}", str(build_root)],
        check=True, capture_output=True, timeout=300,
    )
    shutil.copytree(REPO_ROOT / "apps" / "ui" / "dist", build_root / "apps" / "ui" / "dist")

    venv = tmp_path / "venv"
    subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True, capture_output=True, timeout=300)
    subprocess.run(
        [str(venv / "bin" / "python"), "-m", "pip", "install", "--quiet", str(build_root)],
        check=True, capture_output=True, timeout=1800,
    )

    remedy = venv / "bin" / "remedy"
    assert remedy.exists(), "the console entrypoint is not on the fresh venv's PATH"
    assert next(venv.glob("lib/python*/site-packages/apps/ui/dist/index.html"), None) is not None, (
        "the installed wheel carries no built UI assets"
    )

    version = subprocess.run([str(remedy), "--version"], check=True, capture_output=True, text=True, timeout=120)
    expected = read_declared_version(REPO_ROOT / "pyproject.toml")
    report = parse_version_report(version.stdout)
    assert version_report_proves_an_install(report, expected) is True, report

    project = _fixture_git_repo(tmp_path / "project")
    env = {**os.environ, "REMEDY_DATA_DIR": str(tmp_path / "data")}
    init = subprocess.run(
        [str(remedy), "init"], cwd=str(project), env=env,
        capture_output=True, text=True, timeout=300, stdin=subprocess.DEVNULL,
    )
    assert init.returncode == 0, init.stderr
    do = subprocess.run(
        [str(remedy), "do", "install smoke mission", "--no-llm"], cwd=str(project), env=env,
        capture_output=True, text=True, timeout=600, stdin=subprocess.DEVNULL,
    )
    assert do.returncode == 0, do.stderr
