"""Tests for the build revision a wheel carries (F086 T002, DECISION F086 D2).

The wheel-level proof needs the build backend and lives in the round's gates.
These pin what is reachable without hatchling: the revision comes from the tree
being built, an absent revision writes nothing rather than a guess, and reader
and writer name the same path.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from apps.cli import version_report
from hatch_build import (
    REVISION_WHEEL_NAME,
    build_revision_metadata,
    resolve_source_revision,
)


def _seed_repository(root: Path) -> str:
    """Make `root` a git repository with one commit; return its HEAD sha."""
    root.mkdir(parents=True, exist_ok=True)
    (root / "seed.txt").write_text("seed\n")
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    git = ["git", "-C", str(root), "-c", "user.name=remedy-test",
           "-c", "user.email=t@example.invalid", "-c", "commit.gpgsign=false"]
    subprocess.run([*git, "add", "seed.txt"], check=True)
    subprocess.run([*git, "commit", "-qm", "seed"], check=True)
    head = subprocess.run([*git, "rev-parse", "HEAD"], capture_output=True,
                          text=True, check=True)
    return head.stdout.strip()


@pytest.mark.subprocess
class TestRevisionEmbedding:
    """The embedded revision is the revision of the tree being built, or nothing."""

    def test_a_resolved_revision_is_written_and_mapped(self, tmp_path):
        source = tmp_path / "source"
        head = _seed_repository(source)
        staging = tmp_path / "staging"
        staging.mkdir()
        mapping = build_revision_metadata(source, staging)
        written = staging / REVISION_WHEEL_NAME
        assert mapping == {str(written): REVISION_WHEEL_NAME}
        assert written.read_text() == f"{head}\n"

    def test_no_revision_writes_nothing_and_maps_nothing(self, tmp_path):
        plain = tmp_path / "plain"
        plain.mkdir()
        staging = tmp_path / "staging"
        staging.mkdir()
        assert resolve_source_revision(plain) is None
        assert build_revision_metadata(plain, staging) == {}
        assert list(staging.iterdir()) == []


@pytest.mark.unit
class TestReaderAndWriterAgreeOnOnePath:
    """The path the build writes is the path `remedy --version` reads back."""

    def test_the_reader_carries_hatchlings_extra_metadata_prefix(self):
        # Drop the prefix on either side of this equality and an installed wheel
        # reports `dev` forever while every mock in the suite still passes.
        assert version_report.REVISION_METADATA_FILE == (
            f"extra_metadata/{REVISION_WHEEL_NAME}"
        )
