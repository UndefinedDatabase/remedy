"""F3/F4/F7/F8 — worktree-identity safety and the anchored call-artifact trust chain.

* F4: ``WorktreeIdentity.dirty`` is a typed tri-state (True/False/None) computed from real
  changes, not from "did collection have problems".
* F3: untracked files are read through VERIFIED directory fds — a symlink is never followed
  (so a link to a private file cannot leak its content into the digest) and a special file is
  never opened (so it cannot hang); either only marks the identity, never fails open.
* F7: an episode's call artifacts are verified through anchored, symlink-refusing reads; a
  tampered artifact is caught by its sha256.
* F8: the anchored tree reader refuses a symlinked episode/calls component, so the export can
  never read (or copy out) a file from outside the evidence tree.
"""
from __future__ import annotations

import os
import subprocess

import pytest

import tests.orchestration.test_run_manifest as T
from packages.common import secure_fs as _fs
from packages.orchestration.run_manifest import (
    CALLS_SUBDIR,
    MANIFEST_FILENAME,
    MANIFESTS_SUBDIR,
    read_manifest_tree_bytes_anchored,
    validate_index_and_tree,
    worktree_identity,
    write_run_manifest,
)


def _git(path, cmd):
    subprocess.run(cmd, shell=True, cwd=path, check=True, capture_output=True)


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / "repo"
    r.mkdir()
    _git(r, "git init -q && git config user.email t@t && git config user.name t "
            "&& printf one > a.txt && git add -A && git commit -qm init")
    return r


# --------------------------------------------------------------------------- F4


class TestDirtyTristate:
    def test_clean_tree_is_false(self, repo):
        assert worktree_identity(str(repo)).dirty is False

    def test_unstaged_change_is_true(self, repo):
        (repo / "a.txt").write_text("two")
        assert worktree_identity(str(repo)).dirty is True

    def test_untracked_file_is_true(self, repo):
        (repo / "u.txt").write_text("u")
        assert worktree_identity(str(repo)).dirty is True

    def test_non_git_dir_is_none(self, tmp_path):
        d = tmp_path / "plain"
        d.mkdir()
        wi = worktree_identity(str(d))
        assert wi.dirty is None            # unavailable/incomplete => not a boolean claim


# --------------------------------------------------------------------------- F3


class TestUntrackedReaderSafety:
    def test_untracked_symlink_content_is_never_read(self, repo, tmp_path):
        # A private file outside the repo; an untracked symlink points at it.
        secret = tmp_path / "secret"
        secret.write_text("SUPER_SECRET_A")
        link = repo / "link"
        os.symlink(str(secret), str(link))
        dig_a = worktree_identity(str(repo)).digest
        # Change ONLY the secret's CONTENT. If we were following the link, the digest would
        # move. It must not: we hash the link text/type, never the target bytes.
        secret.write_text("TOTALLY_DIFFERENT_CONTENT_B")
        dig_b = worktree_identity(str(repo)).digest
        assert dig_a == dig_b

    def test_special_file_and_symlink_are_never_opened_by_the_reader(self, tmp_path):
        # git does not list special files as untracked, so exercise the FD reader directly:
        # a FIFO must raise (not open → cannot hang), and a symlink must raise carrying only
        # its LINK TEXT, never following it.
        from packages.orchestration.run_manifest import (
            _read_untracked_verified,
            _UntrackedSpecial,
            _UntrackedSymlink,
        )
        os.mkfifo(str(tmp_path / "pipe"))
        outside = tmp_path / "secret"
        outside.write_text("SECRET")
        os.symlink(str(outside), str(tmp_path / "link"))
        root_fd = _fs.anchor_root(str(tmp_path), noun="worktree")
        try:
            with pytest.raises(_UntrackedSpecial):
                _read_untracked_verified(root_fd, "pipe")
            with pytest.raises(_UntrackedSymlink) as exc:
                _read_untracked_verified(root_fd, "link")
            assert "SECRET" not in str(exc.value)   # link text/target path, never file content
        finally:
            os.close(root_fd)

    def test_same_size_in_place_mutation_during_read_is_a_race(self, tmp_path, monkeypatch):
        # F7: a SAME-SIZE in-place rewrite while the reader is hashing must be detected — the
        # bytes are mixed, so the read is refused, never returned as a stable ok read.
        import os as _os

        from packages.orchestration.run_manifest import (
            _read_untracked_verified,
            _UntrackedRace,
        )

        target = tmp_path / "u.txt"
        target.write_bytes(b"A" * (2 << 20))          # 2 MiB, read in >1 chunk
        real_read = _os.read
        flipped = {"done": False}

        def _mutate_mid_read(fd, n):
            data = real_read(fd, n)
            if data and not flipped["done"]:
                flipped["done"] = True
                # same-size in-place overwrite: size stays identical, mtime/ctime change
                with open(target, "r+b") as fh:
                    fh.seek(0)
                    fh.write(b"B" * (2 << 20))
            return data

        monkeypatch.setattr(_os, "read", _mutate_mid_read)
        root_fd = _fs.anchor_root(str(tmp_path), noun="worktree")
        try:
            with pytest.raises(_UntrackedRace):
                _read_untracked_verified(root_fd, "u.txt")
        finally:
            os.close(root_fd)


# --------------------------------------------------------------------------- F7


class TestAnchoredArtifactTrustChain:
    def _write_episode(self, ev):
        ev.mkdir()
        write_run_manifest(ev, T._mk(episode_id="ep1"), root=ev)

    def test_clean_episode_artifacts_validate(self, tmp_path):
        ev = tmp_path / "ev"
        self._write_episode(ev)
        assert validate_index_and_tree(ev, job_id="j") == []

    def test_tampered_call_artifact_is_caught(self, tmp_path):
        ev = tmp_path / "ev"
        self._write_episode(ev)
        calls_dir = ev / MANIFESTS_SUBDIR / "ep1" / CALLS_SUBDIR
        art = next(calls_dir.iterdir())
        art.write_bytes(b'{"tampered": true}')
        probs = validate_index_and_tree(ev, job_id="j")
        assert any("sha256" in p or "canonical" in p for p in probs), probs

    def test_undeclared_artifact_is_caught(self, tmp_path):
        ev = tmp_path / "ev"
        self._write_episode(ev)
        (ev / MANIFESTS_SUBDIR / "ep1" / CALLS_SUBDIR / "9999-extra.json").write_bytes(b"{}")
        probs = validate_index_and_tree(ev, job_id="j")
        assert any("undeclared" in p for p in probs), probs


# --------------------------------------------------------------------------- F8


class TestAnchoredExportReader:
    def test_symlinked_episode_dir_is_refused_not_followed(self, tmp_path):
        ev = tmp_path / "ev"
        ev.mkdir()
        write_run_manifest(ev, T._mk(episode_id="ep1"), root=ev)
        # An attacker replaces an episode dir with a symlink to an outside tree full of secrets.
        outside = tmp_path / "outside"
        (outside / CALLS_SUBDIR).mkdir(parents=True)
        (outside / MANIFEST_FILENAME).write_text('{"secret": "leak"}')
        ep_dir = ev / MANIFESTS_SUBDIR / "ep1"
        import shutil
        shutil.rmtree(ep_dir)
        os.symlink(str(outside), str(ep_dir))
        files, problems = read_manifest_tree_bytes_anchored(ev)
        # The symlinked episode component is refused; its outside bytes never enter `files`.
        assert not any("leak" in v.decode("utf-8", "replace") for v in files.values())

    def test_missing_episode_manifest_is_a_problem(self, tmp_path):
        ev = tmp_path / "ev"
        ev.mkdir()
        write_run_manifest(ev, T._mk(episode_id="ep1"), root=ev)
        (ev / MANIFESTS_SUBDIR / "ep1" / MANIFEST_FILENAME).unlink()
        files, problems = read_manifest_tree_bytes_anchored(ev)
        assert any("no manifest" in p for p in problems), problems
