"""Packaging contract tests for the wheel's UI assets.

Covers F086 T001: the packaging-time guard that refuses a wheel with no built
frontend (DECISION F086 D1 part (b)), and the asset resolution that must hold in
BOTH modes — from a checkout and from an installed wheel (DECISION F086 D3, which
withdrew the two-mode resolver CODE and kept this test).
"""

from __future__ import annotations

from pathlib import Path

import pytest

import packages.orchestration.ui_server as ui_server
from hatch_build import FRONTEND_DIST_INDEX, assert_frontend_assets_built


def _wheel_root_layout(root: Path, *, with_index: bool) -> Path:
    """Lay out a wheel root: apps/ is a sibling of packages/, module three deep."""
    module = root / "packages" / "orchestration" / "ui_server.py"
    module.parent.mkdir(parents=True, exist_ok=True)
    module.write_text("# stand-in for the installed module\n")
    dist = root / "apps" / "ui" / "dist"
    dist.mkdir(parents=True, exist_ok=True)
    if with_index:
        (dist / "index.html").write_text("<html></html>")
    return module


@pytest.mark.unit
class TestFrontendDistResolution:
    """`_get_frontend_dist` resolves in both install modes (DECISION F086 D3)."""

    def test_installed_wheel_mode_resolves_under_the_wheel_root(self, tmp_path, monkeypatch):
        module = _wheel_root_layout(tmp_path, with_index=True)
        monkeypatch.setattr(ui_server, "__file__", str(module))
        assert ui_server._get_frontend_dist() == tmp_path / "apps" / "ui" / "dist"

    def test_checkout_mode_resolves_under_the_repository_root(self, tmp_path, monkeypatch):
        # A checkout has the SAME geometry as a wheel root: three parents up from
        # the module file, apps/ is a sibling of packages/. That identity is why
        # DECISION F086 D3 withdrew the dual-mode resolver and kept this test.
        checkout = tmp_path / "checkout"
        module = _wheel_root_layout(checkout, with_index=True)
        monkeypatch.setattr(ui_server, "__file__", str(module))
        assert ui_server._get_frontend_dist() == checkout / "apps" / "ui" / "dist"

    def test_missing_index_resolves_to_none_in_either_mode(self, tmp_path, monkeypatch):
        module = _wheel_root_layout(tmp_path, with_index=False)
        monkeypatch.setattr(ui_server, "__file__", str(module))
        assert ui_server._get_frontend_dist() is None


@pytest.mark.unit
class TestFrontendAssetsBuildGuard:
    """The packaging-time guard refuses a wheel with no built UI."""

    def test_present_assets_return_the_index_path(self, tmp_path):
        index = tmp_path / FRONTEND_DIST_INDEX
        index.parent.mkdir(parents=True)
        index.write_text("<html></html>")
        assert assert_frontend_assets_built(tmp_path) == index

    def test_absent_assets_raise_and_name_the_missing_path(self, tmp_path):
        with pytest.raises(ValueError) as excinfo:
            assert_frontend_assets_built(tmp_path)
        assert FRONTEND_DIST_INDEX in str(excinfo.value)

    def test_a_directory_without_the_index_is_still_refused(self, tmp_path):
        (tmp_path / "apps" / "ui" / "dist").mkdir(parents=True)
        with pytest.raises(ValueError):
            assert_frontend_assets_built(tmp_path)
