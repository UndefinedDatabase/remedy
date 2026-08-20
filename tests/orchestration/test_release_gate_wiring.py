"""The release gate is WIRED to this repository's own values (T2_F086 T003).

`test_release_gate.py` proves the gate's DECISIONS against seeded requests. These
prove the other half: that those decisions are reached over the real changelog,
the real declared version and a real wheel's real size. A gate nothing calls
refuses nothing, which is the state R13 left behind on purpose.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from packages.orchestration.release_gate import changelog_section, refuse_release
from scripts.release_gate_check import main, observe_release, version_from_wheel_name

REPO_ROOT = Path(__file__).resolve().parents[2]
CHANGELOG_PATH = REPO_ROOT / "CHANGELOG.md"
PYPROJECT_PATH = REPO_ROOT / "pyproject.toml"
ABSENT_VERSION = "0.0.0"


def declared_version() -> str:
    """The version `pyproject.toml` declares — the one place it is written (D2)."""
    found = re.search(r'^version = "([^"]+)"', PYPROJECT_PATH.read_text(), re.MULTILINE)
    assert found is not None, "pyproject.toml declares no version"
    return found.group(1)


def build_wheel(directory: Path, version: str, size: int) -> Path:
    """A file named like a real wheel of `version` and exactly `size` bytes long."""
    wheel = directory / f"remedy-{version}-py3-none-any.whl"
    wheel.write_bytes(b"x" * size)
    return wheel


@pytest.mark.unit
class TestTheRealChangelogCoversTheRealVersion:
    def test_the_declared_version_has_a_non_empty_section(self):
        assert CHANGELOG_PATH.is_file(), CHANGELOG_PATH
        version = declared_version()
        body = changelog_section(CHANGELOG_PATH.read_text(), version)
        assert body is not None, f"CHANGELOG.md has no section for {version}"
        assert body.strip(), f"the CHANGELOG.md section for {version} is empty"

    def test_this_repository_is_refused_for_no_reason_at_all(self, tmp_path):
        version = declared_version()
        request = observe_release(
            f"v{version}", build_wheel(tmp_path, version, 1024), CHANGELOG_PATH, "success"
        )
        assert refuse_release(request) == ()


@pytest.mark.unit
class TestTheCallerObservesTheArtifact:
    def test_the_version_comes_from_the_wheel_filename(self, tmp_path):
        assert version_from_wheel_name(build_wheel(tmp_path, "9.9.9", 3)) == "9.9.9"

    def test_a_file_that_is_not_a_wheel_is_refused_rather_than_guessed(self, tmp_path):
        with pytest.raises(ValueError):
            version_from_wheel_name(tmp_path / "remedy-1.2.3.tar.gz")

    def test_the_wheel_size_is_read_from_the_file_not_declared(self, tmp_path):
        request = observe_release(
            "v1.2.3", build_wheel(tmp_path, "1.2.3", 4321), CHANGELOG_PATH, "success"
        )
        assert request.wheel_bytes == 4321


@pytest.mark.unit
class TestTheCallerExitsNonZeroSoAWorkflowStops:
    def _run(self, tmp_path, version, tag, ci_status):
        wheel = build_wheel(tmp_path, version, 1024)
        return main(["--tag", tag, "--wheel", str(wheel), "--ci-status", ci_status])

    def test_a_sound_release_exits_zero(self, tmp_path):
        version = declared_version()
        assert self._run(tmp_path, version, f"v{version}", "success") == 0

    def test_red_ci_exits_non_zero(self, tmp_path):
        version = declared_version()
        assert self._run(tmp_path, version, f"v{version}", "failure") == 1

    def test_a_version_with_no_changelog_section_exits_non_zero(self, tmp_path):
        assert self._run(tmp_path, ABSENT_VERSION, f"v{ABSENT_VERSION}", "success") == 1

    def test_every_reason_is_printed_not_only_the_first(self, tmp_path, capsys):
        assert self._run(tmp_path, ABSENT_VERSION, "v9.9.9", "failure") == 1
        assert capsys.readouterr().err.count("REFUSED: ") == 3
