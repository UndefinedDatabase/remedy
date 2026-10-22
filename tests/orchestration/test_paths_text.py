"""Tests for packages.orchestration.paths_text — the home folder written as `~` (R-1290)."""

from __future__ import annotations

import pathlib

from packages.orchestration.paths_text import home_relative_text


def test_home_relative_text_replaces_the_home_path(tmp_path):
    assert home_relative_text(f"{tmp_path}/x", tmp_path) == "~/x"


def test_home_relative_text_leaves_text_for_a_root_home():
    assert home_relative_text("/x/y", pathlib.Path("/")) == "/x/y"
