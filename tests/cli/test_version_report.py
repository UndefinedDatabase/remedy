"""Tests for `remedy --version` (F086 T002, DECISION F086 D2).

Both modes are pinned: an INSTALLED distribution reports its version and the
revision embedded at build time, and a CHECKOUT reports `dev` for what it cannot
prove. The checkout half matters most — D2 makes honest `dev` a requirement, so
a regression that invented a revision must turn a test red.
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError
from types import SimpleNamespace

import pytest

from apps.cli import version_report
from apps.cli.grouped import main


def _install(monkeypatch, version: str, revision: str | None) -> None:
    """Make the distribution look installed, carrying `revision` (or none)."""
    dist = SimpleNamespace(
        version=version,
        read_text=lambda name: revision if name == version_report.REVISION_METADATA_FILE else None,
    )
    monkeypatch.setattr(version_report, "distribution", lambda name: dist)


def _uninstall(monkeypatch) -> None:
    """Make the distribution look absent, as it is in a bare checkout."""

    def _raise(name: str):
        raise PackageNotFoundError(name)

    monkeypatch.setattr(version_report, "distribution", _raise)


@pytest.mark.unit
class TestInstalledMode:
    def test_embedded_revision_is_reported(self, monkeypatch):
        _install(monkeypatch, "1.2.3", "abc1234\n")
        assert version_report.resolve_build_revision() == "abc1234"

    def test_report_carries_version_and_revision(self, monkeypatch):
        _install(monkeypatch, "1.2.3", "abc1234")
        report = version_report.render_version_report()
        assert "remedy   1.2.3" in report
        assert "build    abc1234" in report


@pytest.mark.unit
class TestCheckoutMode:
    def test_uninstalled_version_is_dev(self, monkeypatch):
        _uninstall(monkeypatch)
        assert version_report.resolve_distribution_version() == version_report.UNKNOWN_MARKER

    def test_uninstalled_revision_is_dev(self, monkeypatch):
        _uninstall(monkeypatch)
        assert version_report.resolve_build_revision() == version_report.UNKNOWN_MARKER

    def test_installed_without_embedded_revision_is_dev(self, monkeypatch):
        _install(monkeypatch, "1.2.3", None)
        assert version_report.resolve_build_revision() == version_report.UNKNOWN_MARKER

    def test_blank_embedded_revision_is_dev(self, monkeypatch):
        _install(monkeypatch, "1.2.3", "   \n")
        assert version_report.resolve_build_revision() == version_report.UNKNOWN_MARKER


@pytest.mark.unit
class TestVersionFlag:
    def test_version_flag_prints_the_report_and_returns(self, capsys):
        main(["--version"])
        out = capsys.readouterr().out
        assert out.startswith("remedy   ")
        assert "python   " in out
        assert "platform " in out

    def test_version_flag_wins_over_help(self, capsys):
        main(["--version", "--help"])
        out = capsys.readouterr().out
        assert out.startswith("remedy   ")
        assert "Usage" not in out
