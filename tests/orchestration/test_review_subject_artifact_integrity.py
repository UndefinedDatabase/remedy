"""F4 (round 16) — the packager RECOMPUTES the review subject; it does not read it.

`review_subject.json` is the artifact that says WHAT is under review: which base, which head, and
every file with the proof its status allows. The final package trusted it — the Evidence job's own
account of its own work — so a forged tombstone hash, a rewritten rename origin, or a status
flipped from `added` to `modified` travelled straight into a READY package. The one artifact that
defines the review was the one artifact nobody recomputed.

So the packager resolves the subject again, from the recorded base, and compares it record by
record: path, old_path, status, base_sha256, current_sha256 and file kind.
"""
from __future__ import annotations

import json
import subprocess

import pytest


def _sh(repo, cmd):
    subprocess.run(cmd, shell=True, cwd=repo, check=True, capture_output=True)


def _rev(repo, ref="HEAD"):
    return subprocess.run(["git", "rev-parse", ref], cwd=repo, capture_output=True,
                          text=True).stdout.strip()


@pytest.fixture
def repo(tmp_path):
    """A base plus committed work containing an add, a modify, a delete and a rename."""
    r = tmp_path / "repo"
    r.mkdir()
    _sh(r, "git init -q -b main && git config user.email t@t && git config user.name t")
    _sh(r, "echo keep > keep.py && echo doomed > doomed.py && echo old > old_name.py "
           "&& git add -A && git commit -qm base")
    base = _rev(r)
    _sh(r, "git checkout -q -b feature")
    _sh(r, "echo added > added.py && git add -A && git commit -qm add")
    _sh(r, "echo changed > keep.py && git add -A && git commit -qm modify")
    _sh(r, "git rm -q doomed.py && git commit -qm delete")
    _sh(r, "git mv old_name.py new_name.py && git commit -qm rename")
    return r, base


def _export(ev, subject, repo):
    from packages.orchestration.review_subject import (
        COMMIT_PATCH_DIRNAME,
        commit_patch_bytes,
        commit_patch_filename,
    )
    ev.mkdir(parents=True, exist_ok=True)
    (ev / "review_subject.json").write_text(json.dumps(subject.to_json()))
    (ev / "review_commit_chain.json").write_text(json.dumps({
        "chain_v": 1, "base_commit": subject.base_commit,
        "head_commit": subject.head_commit,
        "commits": [c.to_json() for c in subject.commits]}))
    pdir = ev / COMMIT_PATCH_DIRNAME
    pdir.mkdir(exist_ok=True)
    for c in subject.commits:
        (pdir / commit_patch_filename(c.commit)).write_bytes(commit_patch_bytes(repo, c.commit))


def _verify(ev, r, monkeypatch):
    from scripts.build_review_manifest import _verify_commit_chain

    monkeypatch.chdir(r)
    return _verify_commit_chain(str(ev), set())


def _forge(ev, mutate):
    """Rewrite review_subject.json the way a tamper would — leaving everything else consistent."""
    p = ev / "review_subject.json"
    d = json.loads(p.read_text())
    mutate(d)
    p.write_text(json.dumps(d))


def _rec(d, path):
    return next(f for f in d["files"] if f["path"] == path)


# --------------------------------------------------------------------------- baseline


class TestTheHonestSubjectVerifies:
    def test_a_faithful_subject_passes(self, repo, tmp_path, monkeypatch):
        from packages.orchestration.review_subject import resolve_review_subject

        r, base = repo
        s = resolve_review_subject(r, base)
        _export(tmp_path / "ev", s, r)
        assert _verify(tmp_path / "ev", r, monkeypatch) == []

    def test_the_fixture_really_contains_every_status(self, repo):
        from packages.orchestration.review_subject import resolve_review_subject

        r, base = repo
        got = {f.path: f.status for f in resolve_review_subject(r, base).files}
        assert got["added.py"] == "added"
        assert got["keep.py"] == "modified"
        assert got["doomed.py"] == "deleted"
        assert got["new_name.py"] == "renamed"


# --------------------------------------------------------------------------- the forgeries


class TestForgedRecordsBlock:
    @pytest.fixture(autouse=True)
    def _setup(self, repo, tmp_path):
        from packages.orchestration.review_subject import resolve_review_subject

        self.r, self.base = repo
        self.ev = tmp_path / "ev"
        _export(self.ev, resolve_review_subject(self.r, self.base), self.r)

    def test_a_forged_deletion_base_hash_blocks(self, monkeypatch):
        """The tombstone is the ONLY proof of a deleted file. Forging it is forging the file."""
        _forge(self.ev, lambda d: _rec(d, "doomed.py").__setitem__("base_sha256", "b" * 64))
        assert _verify(self.ev, self.r, monkeypatch)

    def test_a_null_deletion_base_hash_blocks(self, monkeypatch):
        _forge(self.ev, lambda d: _rec(d, "doomed.py").__setitem__("base_sha256", None))
        assert _verify(self.ev, self.r, monkeypatch)

    def test_a_forged_rename_old_path_blocks(self, monkeypatch):
        _forge(self.ev, lambda d: _rec(d, "new_name.py").__setitem__("old_path", "invented.py"))
        assert _verify(self.ev, self.r, monkeypatch)

    def test_a_forged_rename_base_hash_blocks(self, monkeypatch):
        _forge(self.ev, lambda d: _rec(d, "new_name.py").__setitem__("base_sha256", "c" * 64))
        assert _verify(self.ev, self.r, monkeypatch)

    def test_a_forged_rename_current_hash_blocks(self, monkeypatch):
        _forge(self.ev, lambda d: _rec(d, "new_name.py").__setitem__("current_sha256", "d" * 64))
        assert _verify(self.ev, self.r, monkeypatch)

    def test_a_forged_status_blocks(self, monkeypatch):
        _forge(self.ev, lambda d: _rec(d, "added.py").__setitem__("status", "modified"))
        assert _verify(self.ev, self.r, monkeypatch)

    def test_an_unknown_status_blocks(self, monkeypatch):
        _forge(self.ev, lambda d: _rec(d, "keep.py").__setitem__("status", "invented"))
        assert _verify(self.ev, self.r, monkeypatch)

    def test_a_forged_current_hash_blocks(self, monkeypatch):
        _forge(self.ev, lambda d: _rec(d, "keep.py").__setitem__("current_sha256", "e" * 64))
        assert _verify(self.ev, self.r, monkeypatch)

    def test_a_forged_kind_blocks(self, monkeypatch):
        _forge(self.ev, lambda d: _rec(d, "keep.py").__setitem__("kind", "symlink"))
        assert _verify(self.ev, self.r, monkeypatch)

    def test_a_dropped_file_record_blocks(self, monkeypatch):
        _forge(self.ev, lambda d: d.__setitem__(
            "files", [f for f in d["files"] if f["path"] != "added.py"]))
        probs = _verify(self.ev, self.r, monkeypatch)
        assert any("does not record" in p for p in probs), probs

    def test_an_invented_file_record_blocks(self, monkeypatch):
        _forge(self.ev, lambda d: d["files"].append(
            {"path": "ghost.py", "status": "added", "base_sha256": None,
             "current_sha256": "f" * 64, "kind": "regular"}))
        probs = _verify(self.ev, self.r, monkeypatch)
        assert any("does not confirm" in p for p in probs), probs


class TestForgedPatchBytesBlock:
    """Round 40 F2: a packaged patch file whose bytes do not match the canonical
    ``commit_patch_bytes()`` producer is detected and blocks."""

    @pytest.fixture(autouse=True)
    def _setup(self, repo, tmp_path):
        from packages.orchestration.review_subject import resolve_review_subject
        self.r, self.base = repo
        self.ev = tmp_path / "ev"
        self.subject = resolve_review_subject(self.r, self.base)
        _export(self.ev, self.subject, self.r)

    def test_forged_patch_bytes_block(self, monkeypatch):
        from packages.orchestration.review_subject import (
            COMMIT_PATCH_DIRNAME,
            commit_patch_filename,
        )
        from scripts.build_review_manifest import _as_view, _verify_commit_patches
        monkeypatch.chdir(self.r)
        c = self.subject.commits[0]
        patch_path = self.ev / COMMIT_PATCH_DIRNAME / commit_patch_filename(c.commit)
        patch_path.write_bytes(b"From fake Mon Sep 17 00:00:00 2001\nforged patch\n")
        ev = _as_view(str(self.ev))
        probs = _verify_commit_patches(ev, self.subject.commits)
        assert any("not the repository" in p for p in probs), probs

    def test_honest_patches_pass(self, monkeypatch):
        from scripts.build_review_manifest import _as_view, _verify_commit_patches
        monkeypatch.chdir(self.r)
        ev = _as_view(str(self.ev))
        assert _verify_commit_patches(ev, self.subject.commits) == []
