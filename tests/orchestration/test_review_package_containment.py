"""F9 (round 17) — containment by PATH COMPONENTS, not a string prefix.

`ev_resolved.startswith(root_resolved)` accepts `/tmp/x/repo-evil/evidence` as inside
`/tmp/x/repo` — a sibling whose name merely begins with the root's. `contained` uses
`os.path.commonpath` and resolves symlinks first, so a sibling, a different tree, or a symlinked
descendant that escapes the root is refused.
"""
from __future__ import annotations

import os

import pytest

from packages.orchestration.review_zip import contained


@pytest.fixture
def tree(tmp_path):
    (tmp_path / "repo" / "sub").mkdir(parents=True)
    (tmp_path / "repo-evil").mkdir()
    (tmp_path / "elsewhere").mkdir()
    return tmp_path


class TestContainment:
    def test_the_reproduced_sibling_prefix_is_not_contained(self, tree):
        assert contained(tree / "repo", tree / "repo-evil" / "evidence") is False

    def test_a_real_descendant_is_contained(self, tree):
        assert contained(tree / "repo", tree / "repo" / "sub" / "x") is True

    def test_the_exact_root_is_contained(self, tree):
        assert contained(tree / "repo", tree / "repo") is True

    def test_an_unrelated_tree_is_not_contained(self, tree):
        assert contained(tree / "repo", tree / "elsewhere" / "x") is False

    def test_a_symlinked_descendant_escaping_the_root_is_refused(self, tree):
        outside = tree / "outside"
        outside.mkdir()
        (outside / "secret.txt").write_text("s")
        link = tree / "repo" / "escape"
        os.symlink(str(outside), str(link))
        # A path THROUGH the symlink resolves outside the root — refused.
        assert contained(tree / "repo", link / "secret.txt") is False

    def test_a_prefix_that_is_a_parent_is_not_contained(self, tree):
        assert contained(tree / "repo" / "sub", tree / "repo") is False


class TestThePackagerUsesComponentContainment:
    def test_build_manifest_containment_uses_contained(self):
        """The packager's containment block imports and uses `contained`, not startswith."""
        import inspect

        import scripts.build_review_manifest as brm

        src = inspect.getsource(brm.build_manifest)
        assert "contained(" in src
        # the raw sibling-vulnerable pattern must be gone from the containment block
        assert "ev_resolved.startswith(root_resolved)" not in src
        assert "cwd_resolved.startswith(root_resolved)" not in src
