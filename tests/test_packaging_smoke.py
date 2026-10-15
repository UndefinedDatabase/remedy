"""Packaging contract tests for the wheel's build hook.

The guard that refused a wheel with no built frontend (DECISION F086 D1 part (b)) went with the
frontend (amend1015f D3); what stays is which targets the hook embeds the revision into.
"""

from __future__ import annotations

import pytest

from hatch_build import (
    BuildHookInterface,
    RemedyBuildHook,
    build_target_embeds_revision,
)


@pytest.mark.unit
class TestTheHookTargets:
    """`pip install -e` gets nothing embedded; every shipped target is built without any UI."""

    def test_the_dev_environment_exercises_the_plain_hook_class(self):
        # The dev extra never installs hatchling, so the module's documented
        # `object` fallback is what the two hook tests below construct. If that
        # ever changes this fails first and explains them.
        assert BuildHookInterface is object

    def test_the_editable_target_embeds_no_revision(self):
        assert build_target_embeds_revision("editable") is False

    def test_every_other_target_embeds_the_revision(self):
        assert build_target_embeds_revision("standard") is True
        assert build_target_embeds_revision("sdist") is True

    def test_an_editable_build_adds_no_metadata(self, tmp_path):
        hook = RemedyBuildHook.__new__(RemedyBuildHook)
        hook.root = str(tmp_path)
        build_data = dict(extra_metadata=dict())
        hook.initialize("editable", build_data)
        assert build_data["extra_metadata"] == dict()

    def test_a_shipped_build_needs_no_ui_and_invents_no_revision(self, tmp_path):
        # A folder outside version control: the hook neither refuses nor guesses a sha.
        hook = RemedyBuildHook.__new__(RemedyBuildHook)
        hook.root = str(tmp_path)
        build_data = dict(extra_metadata=dict())
        hook.initialize("standard", build_data)
        assert build_data["extra_metadata"] == dict()
