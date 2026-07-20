"""F6/F7 (round 12) — workspace inspection is bound to a held handle and executes NO repo code.

Two independent reproductions:

* containment verified a path, closed its descriptors and handed back an ordinary `Path`. Renaming
  the verified directory and dropping a symlink to an outside repository in its place meant the
  inspection ran against that outside repository and observed its HEAD. A `Path` is a name, and a
  name is not a security token.

* `core.fsmonitor = <script>` was EXECUTED by `worktree_identity()`, which then reported
  `status=ok, problems=[]`. A read-only verification command ran arbitrary repository-configured
  code and called the result trustworthy.

So the final workspace descriptor is held open for the whole inspection and git's cwd is bound to
that open description (`/proc/self/fd/N` — no rename can redirect it), and every configured helper
is neutralized for the duration.
"""
from __future__ import annotations

import os
import subprocess

import pytest

from packages.orchestration.run_manifest import (
    GIT_OK,
    inspect_contained_workspace_identity,
    worktree_identity,
)


def _git_repo(path, content="# demo"):
    path.mkdir(parents=True, exist_ok=True)
    subprocess.run(f"git init -q && git config user.email t@t && git config user.name t "
                   f"&& echo '{content}' > README.md && git add -A && git commit -qm init",
                   shell=True, cwd=path, check=True)
    return path


@pytest.fixture
def repo(tmp_path):
    return _git_repo(tmp_path / "repo")


@pytest.fixture
def wt_root(repo):
    root = repo / ".remedy-wt"
    root.mkdir(exist_ok=True)
    return root


def _workspace(repo, wt_root, name="job-x"):
    ws = wt_root / name
    subprocess.run(["git", "worktree", "add", "-q", "--detach", str(ws)], cwd=repo,
                   check=True, capture_output=True)
    return ws


def _head(path):
    return subprocess.run(["git", "-C", str(path), "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()


# --------------------------------------------------------------------------- F6


class TestContainmentStaysBoundThroughInspection:
    def test_a_swap_after_containment_cannot_read_the_outside_repository(
            self, repo, wt_root, tmp_path):
        """THE finding: verify, rename, symlink an outside repo into place, inspect — and the
        outside HEAD came back."""
        outside = _git_repo(tmp_path / "outside", content="SECRET-OUTSIDE")
        ws = _workspace(repo, wt_root)
        os.rename(str(ws), str(wt_root / "moved"))
        os.symlink(str(outside), str(ws))

        wid = inspect_contained_workspace_identity(wt_root, ws)
        assert wid.status != GIT_OK
        assert wid.head != _head(outside), "the inspection read the outside repository"
        assert not wid.digest, "an escaping workspace must never be digested"

    def test_a_swapped_workspace_executes_no_outside_configuration(
            self, repo, wt_root, tmp_path):
        outside = _git_repo(tmp_path / "outside2")
        marker = tmp_path / "outside_helper_ran"
        subprocess.run(["git", "config", "core.fsmonitor", f"sh -c 'touch {marker}; exit 1'"],
                       cwd=outside, check=True)
        ws = _workspace(repo, wt_root)
        os.rename(str(ws), str(wt_root / "moved2"))
        os.symlink(str(outside), str(ws))

        inspect_contained_workspace_identity(wt_root, ws)
        assert not marker.exists(), "an outside repository's configured helper was executed"

    def test_a_contained_workspace_still_inspects_normally(self, repo, wt_root):
        ws = _workspace(repo, wt_root)
        (ws / "untracked.txt").write_text("work")
        wid = inspect_contained_workspace_identity(wt_root, ws)
        assert wid.status == GIT_OK
        assert wid.dirty is True
        assert len(wid.digest) == 64

    def test_the_held_handle_and_by_name_identities_agree(self, repo, wt_root):
        """Binding the inspection must not change what it measures."""
        ws = _workspace(repo, wt_root)
        (ws / "f.txt").write_text("data")
        assert inspect_contained_workspace_identity(wt_root, ws).digest == \
            worktree_identity(str(ws)).digest

    def test_a_workspace_outside_the_root_is_refused(self, repo, wt_root, tmp_path):
        outside = _git_repo(tmp_path / "elsewhere")
        wid = inspect_contained_workspace_identity(wt_root, outside)
        assert wid.status != GIT_OK
        assert not wid.digest


# --------------------------------------------------------------------------- F7


class TestNoConfiguredHelperEverRuns:
    def _canary(self, ws, marker, key, value=None):
        subprocess.run(["git", "config", key, value or f"sh -c 'touch {marker}; exit 1'"],
                       cwd=ws, check=True)

    def test_core_fsmonitor_never_runs(self, repo, wt_root, tmp_path):
        """THE finding: the fsmonitor script ran and the identity still said ok/problems=[]."""
        marker = tmp_path / "fsmonitor_ran"
        ws = _workspace(repo, wt_root)
        self._canary(ws, marker, "core.fsmonitor")
        inspect_contained_workspace_identity(wt_root, ws)
        assert not marker.exists()

    def test_a_clean_filter_never_runs(self, repo, wt_root, tmp_path):
        marker = tmp_path / "clean_ran"
        ws = _workspace(repo, wt_root)
        (ws / ".gitattributes").write_text("* filter=canary\n")
        (ws / "content.txt").write_text("data")
        self._canary(ws, marker, "filter.canary.clean", f"sh -c 'touch {marker}; cat'")
        inspect_contained_workspace_identity(wt_root, ws)
        assert not marker.exists()

    def test_a_smudge_filter_never_runs(self, repo, wt_root, tmp_path):
        marker = tmp_path / "smudge_ran"
        ws = _workspace(repo, wt_root)
        (ws / ".gitattributes").write_text("* filter=canary\n")
        (ws / "content.txt").write_text("data")
        self._canary(ws, marker, "filter.canary.smudge", f"sh -c 'touch {marker}; cat'")
        inspect_contained_workspace_identity(wt_root, ws)
        assert not marker.exists()

    def test_a_filter_process_never_runs(self, repo, wt_root, tmp_path):
        marker = tmp_path / "process_ran"
        ws = _workspace(repo, wt_root)
        (ws / ".gitattributes").write_text("* filter=canary\n")
        (ws / "content.txt").write_text("data")
        self._canary(ws, marker, "filter.canary.process", f"sh -c 'touch {marker}; exit 1'")
        subprocess.run(["git", "config", "filter.canary.required", "true"], cwd=ws, check=True)
        inspect_contained_workspace_identity(wt_root, ws)
        assert not marker.exists()

    def test_a_required_but_disabled_filter_cannot_fake_success(self, repo, wt_root, tmp_path):
        """A configured helper must never be able to turn an inspection into a lie in EITHER
        direction — neither by running, nor by making a failure look like a success."""
        marker = tmp_path / "req_ran"
        ws = _workspace(repo, wt_root)
        (ws / ".gitattributes").write_text("* filter=canary\n")
        (ws / "content.txt").write_text("data")
        self._canary(ws, marker, "filter.canary.clean", f"sh -c 'touch {marker}; exit 3'")
        subprocess.run(["git", "config", "filter.canary.required", "true"], cwd=ws, check=True)
        wid = inspect_contained_workspace_identity(wt_root, ws)
        assert not marker.exists()
        assert wid.status == GIT_OK and len(wid.digest) == 64

    def test_an_external_diff_helper_never_runs(self, repo, wt_root, tmp_path):
        marker = tmp_path / "diff_ran"
        ws = _workspace(repo, wt_root)
        (ws / ".gitattributes").write_text("* diff=canary\n")
        (ws / "content.txt").write_text("data")
        subprocess.run(["git", "config", "diff.canary.command",
                        f"sh -c 'touch {marker}'"], cwd=ws, check=True)
        inspect_contained_workspace_identity(wt_root, ws)
        assert not marker.exists()

    def test_a_textconv_helper_never_runs(self, repo, wt_root, tmp_path):
        marker = tmp_path / "textconv_ran"
        ws = _workspace(repo, wt_root)
        (ws / ".gitattributes").write_text("* diff=canary\n")
        (ws / "content.txt").write_text("data")
        subprocess.run(["git", "config", "diff.canary.textconv",
                        f"sh -c 'touch {marker}; cat'"], cwd=ws, check=True)
        inspect_contained_workspace_identity(wt_root, ws)
        assert not marker.exists()

    def test_the_identity_stays_deterministic_with_helpers_configured(self, repo, wt_root,
                                                                      tmp_path):
        marker = tmp_path / "any_ran"
        ws = _workspace(repo, wt_root)
        (ws / ".gitattributes").write_text("* filter=canary\n")
        (ws / "content.txt").write_text("data")
        self._canary(ws, marker, "filter.canary.clean", f"sh -c 'touch {marker}; cat'")
        first = inspect_contained_workspace_identity(wt_root, ws)
        second = inspect_contained_workspace_identity(wt_root, ws)
        assert first.digest == second.digest
        assert not marker.exists()
