"""F7 (round 13) — workspace containment rejects LEXICAL `..` escapes.

Round 12 bound the inspection to a held descriptor so a rename could not redirect it. But the
descriptor was obtained by walking components that were never normalized:

    Path("/tmp/root/sub/../../outside").relative_to("/tmp/root")  ->  sub/../../outside

`Path.relative_to` is lexical-but-not-normalizing, so it happily returned a relative path whose
components walk UP. And `..` is neither a symlink nor a non-directory, so every no-follow identity
check passed it — the traversal stepped out of the root one level per component and inspected the
outside repository. Reproduced: `status=ok` and the outside repo's real HEAD.

The fix is the one canonical helper: `secure_fs.lexical_parts()` normalizes first and then asks
whether the result is still under the root, so the escape is refused before a descriptor exists.
`open_verified_dir` refuses `..` on its own as defence in depth. `resolve()` remains the wrong
tool (F010's binding clause: it answers "where does this point", not "did you route me through a
link").
"""
from __future__ import annotations

import os
import pathlib
import subprocess

import pytest

from packages.common import secure_fs as _fs
from packages.orchestration.run_manifest import (
    GIT_UNAVAILABLE,
    UNAVAILABLE,
    _open_contained_workspace_fd,
    inspect_contained_workspace_identity,
)


def _git(path, *args):
    return subprocess.run(["git", *args], cwd=path, capture_output=True, text=True).stdout.strip()


@pytest.fixture
def world(tmp_path):
    """A canonical root with a legitimate nested workspace, and an OUTSIDE repository holding a
    secret the inspection must never read."""
    root = tmp_path / "root"
    (root / "sub").mkdir(parents=True)
    outside = tmp_path / "outside"
    outside.mkdir()
    subprocess.run("git init -q && git config user.email t@t && git config user.name t && "
                   "echo OUTSIDE-SECRET > f.txt && git add -A && git commit -qm outside",
                   shell=True, cwd=outside, check=True)
    inside = root / "nested" / "ws"
    inside.mkdir(parents=True)
    subprocess.run("git init -q && git config user.email t@t && git config user.name t && "
                   "echo fine > g.txt && git add -A && git commit -qm inside",
                   shell=True, cwd=inside, check=True)
    return root, outside, inside


def _fd_count():
    return len(os.listdir("/proc/self/fd"))


# --------------------------------------------------------------------------- the escapes


class TestLexicalTraversalIsRefused:
    def test_the_reproduced_case(self, world):
        """`root/sub/../../outside` — status was ok and the outside HEAD was reported."""
        root, outside, _inside = world
        claimed = str(root / "sub" / ".." / ".." / "outside")
        ident = inspect_contained_workspace_identity(root, claimed)
        assert ident.status == GIT_UNAVAILABLE
        assert ident.head == UNAVAILABLE
        assert ident.head != _git(outside, "rev-parse", "HEAD")

    def test_root_dot_dot_outside_is_refused(self, world):
        root, outside, _inside = world
        ident = inspect_contained_workspace_identity(root, str(root / ".." / "outside"))
        assert ident.status == GIT_UNAVAILABLE
        assert ident.head != _git(outside, "rev-parse", "HEAD")

    def test_multiple_nested_traversal_is_refused(self, world):
        root, outside, _inside = world
        claimed = str(root / "sub" / "a" / "b" / ".." / ".." / ".." / ".." / "outside")
        ident = inspect_contained_workspace_identity(root, claimed)
        assert ident.status == GIT_UNAVAILABLE
        assert ident.head != _git(outside, "rev-parse", "HEAD")

    def test_a_sibling_outside_the_root_is_refused(self, world):
        root, outside, _inside = world
        assert inspect_contained_workspace_identity(root, str(outside)).status == GIT_UNAVAILABLE

    def test_the_root_itself_is_not_a_workspace(self, world):
        root, _outside, _inside = world
        assert inspect_contained_workspace_identity(root, str(root)).status == GIT_UNAVAILABLE

    def test_no_descriptor_is_ever_opened_for_an_escape(self, world):
        """Refused BEFORE anything is opened — not after walking out and back."""
        root, _outside, _inside = world
        assert _open_contained_workspace_fd(root, str(root / "sub" / ".." / ".." / "outside")) \
            is None

    def test_no_outside_head_or_digest_is_read(self, world):
        root, outside, _inside = world
        real_head = _git(outside, "rev-parse", "HEAD")
        ident = inspect_contained_workspace_identity(
            root, str(root / "sub" / ".." / ".." / "outside"))
        assert real_head and real_head not in (ident.head or "")
        assert not ident.digest

    def test_no_outside_helper_marker_executes(self, world, tmp_path):
        """An escape must not run the outside repository's configured helpers either."""
        root, outside, _inside = world
        marker = tmp_path / "helper-ran.marker"
        subprocess.run(["git", "config", "core.fsmonitor",
                        f"sh -c 'touch {marker}; true'"], cwd=outside, check=True)
        inspect_contained_workspace_identity(root, str(root / "sub" / ".." / ".." / "outside"))
        assert not marker.exists(), "an outside configured helper executed"


# --------------------------------------------------------------------------- the good path


class TestContainedWorkspacesStillWork:
    def test_a_normal_nested_workspace_passes(self, world):
        root, _outside, inside = world
        ident = inspect_contained_workspace_identity(root, str(inside))
        assert ident.status == "ok"
        assert ident.head == _git(inside, "rev-parse", "HEAD")
        assert len(ident.digest) == 64

    def test_a_name_with_safe_dots_is_not_a_traversal(self, world):
        """`..` is the rule — a component that merely CONTAINS dots is a normal directory."""
        root, _outside, _inside = world
        ws = root / "my.workspace.v2"
        ws.mkdir()
        subprocess.run("git init -q && git config user.email t@t && git config user.name t && "
                       "echo x > a.txt && git add -A && git commit -qm dots",
                       shell=True, cwd=ws, check=True)
        ident = inspect_contained_workspace_identity(root, str(ws))
        assert ident.status == "ok"
        assert ident.head == _git(ws, "rev-parse", "HEAD")

    def test_a_single_dot_component_is_normalized_not_refused(self, world):
        root, _outside, inside = world
        claimed = str(root / "nested" / "." / "ws")
        assert inspect_contained_workspace_identity(root, claimed).status == "ok"


# --------------------------------------------------------------------------- descriptors


class TestNoDescriptorLeak:
    def test_fd_count_is_stable_across_refusals_and_successes(self, world):
        root, _outside, inside = world
        before = _fd_count()
        for _ in range(5):
            inspect_contained_workspace_identity(root, str(root / "sub" / ".." / ".." / "x"))
            inspect_contained_workspace_identity(root, str(inside))
            inspect_contained_workspace_identity(root, str(root / "does-not-exist"))
        assert _fd_count() == before


# --------------------------------------------------------------------------- the helper


class TestTheCanonicalHelperIsTheOneRule:
    def test_lexical_parts_normalizes_before_deciding(self):
        with pytest.raises(Exception):
            _fs.lexical_parts("/tmp/root/sub/../../outside", "/tmp/root")
        assert _fs.lexical_parts("/tmp/root/nested/ws", "/tmp/root") == ["nested", "ws"]

    def test_open_verified_dir_refuses_a_traversal_component(self, tmp_path):
        """Defence in depth: even a caller that forgot to normalize cannot walk up."""
        fd = os.open(str(tmp_path), os.O_RDONLY)
        try:
            for bad in ("..", ".", "", "a/b", "a\0b"):
                with pytest.raises(Exception):
                    _fs.open_verified_dir(bad, dir_fd=fd)
        finally:
            os.close(fd)

    def test_the_absolute_root_bootstrap_still_works(self):
        """`os.sep` is the one documented exception — anchored absolute walks start there."""
        fd = _fs.open_verified_dir(os.sep)
        try:
            assert os.fstat(fd).st_ino == pathlib.Path("/").stat().st_ino
        finally:
            os.close(fd)
