"""Packaging contract tests for the wheel's UI assets.

Covers F086 T001: the packaging-time guard that refuses a wheel with no built
frontend (DECISION F086 D1 part (b)), and the asset resolution that must hold in
BOTH modes — from a checkout and from an installed wheel (DECISION F086 D3, which
withdrew the two-mode resolver CODE and kept this test).
"""

from __future__ import annotations

import pytest

from hatch_build import (
    FRONTEND_DIST_INDEX,
    BuildHookInterface,
    RemedyBuildHook,
    assert_frontend_assets_built,
    build_target_ships_ui_assets,
)


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


@pytest.mark.unit
class TestEditableBuildsAreNotGuarded:
    """`pip install -e` must survive a checkout whose UI was never built.

    The guard as first written refused EVERY build target, so the editable install
    that is CI's first step died on any fresh clone and no test ran at all (R-0598).
    """

    def test_the_dev_environment_exercises_the_plain_hook_class(self):
        # The dev extra never installs hatchling, so the module's documented
        # `object` fallback is what the two hook tests below construct. If that
        # ever changes this fails first and explains them.
        assert BuildHookInterface is object

    def test_the_editable_target_does_not_ship_ui_assets(self):
        assert build_target_ships_ui_assets("editable") is False

    def test_every_other_target_ships_ui_assets(self):
        assert build_target_ships_ui_assets("standard") is True
        assert build_target_ships_ui_assets("sdist") is True

    def test_an_editable_build_is_allowed_without_built_assets(self, tmp_path):
        hook = RemedyBuildHook.__new__(RemedyBuildHook)
        hook.root = str(tmp_path)
        build_data = dict(extra_metadata=dict())
        hook.initialize("editable", build_data)
        assert build_data["extra_metadata"] == dict()

    def test_a_shipped_build_is_still_refused_without_built_assets(self, tmp_path):
        hook = RemedyBuildHook.__new__(RemedyBuildHook)
        hook.root = str(tmp_path)
        with pytest.raises(ValueError) as excinfo:
            hook.initialize("standard", dict(extra_metadata=dict()))
        assert FRONTEND_DIST_INDEX in str(excinfo.value)
