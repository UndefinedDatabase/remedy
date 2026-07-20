"""F7 (round 16) — the package ships the canonical patch BYTES its chain hashes.

`review_commit_chain.json` recorded a `patch_sha256` per commit and shipped nothing to hash it
against. So the one field that says what a commit actually DID was the one field a ZIP-only
reviewer — the only kind an external review has — could not check. They could verify the shape of
the history and had to take its content on trust, or clone the repository. A package that requires
the repository is not self-contained evidence.

So every base-exclusive commit gets `review_commit_patches/<full-sha>.patch`, holding exactly the
bytes whose sha256 the chain records, produced by ONE helper so the recorded hash, the packaged
file and the packager's recomputation cannot become three slightly different things.
"""
from __future__ import annotations

import hashlib
import json
import subprocess

import pytest

from packages.orchestration.review_subject import (
    COMMIT_PATCH_DIRNAME,
    ReviewSubjectError,
    commit_patch_bytes,
    commit_patch_filename,
    resolve_review_subject,
)


def _sh(repo, cmd):
    subprocess.run(cmd, shell=True, cwd=repo, check=True, capture_output=True)


def _rev(repo, ref="HEAD"):
    return subprocess.run(["git", "rev-parse", ref], cwd=repo, capture_output=True,
                          text=True).stdout.strip()


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / "repo"
    r.mkdir()
    _sh(r, "git init -q -b main && git config user.email t@t && git config user.name t")
    _sh(r, "echo base > base.txt && git add -A && git commit -qm base")
    base = _rev(r)
    _sh(r, "git checkout -q -b feature")
    _sh(r, "echo one > a.txt && git add -A && git commit -qm first")
    _sh(r, "echo two > b.txt && git add -A && git commit -qm second")
    return r, base


def _export(ev, subject, repo):
    """What the exporter writes."""
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
    return pdir


# --------------------------------------------------------------------------- the bytes


class TestThePatchBytesAreTheHashedBytes:
    def test_a_zip_only_reviewer_can_recompute_every_patch_hash(self, repo, tmp_path):
        """THE point of the finding: no repository needed."""
        r, base = repo
        s = resolve_review_subject(r, base)
        pdir = _export(tmp_path / "ev", s, r)
        for c in s.commits:
            packaged = (pdir / commit_patch_filename(c.commit)).read_bytes()
            assert hashlib.sha256(packaged).hexdigest() == c.patch_sha256

    def test_one_patch_per_commit(self, repo, tmp_path):
        r, base = repo
        s = resolve_review_subject(r, base)
        pdir = _export(tmp_path / "ev", s, r)
        assert len(list(pdir.glob("*.patch"))) == len(s.commits) == 2

    def test_the_filename_is_the_full_commit_sha(self, repo, tmp_path):
        r, base = repo
        s = resolve_review_subject(r, base)
        pdir = _export(tmp_path / "ev", s, r)
        for c in s.commits:
            assert (pdir / f"{c.commit}.patch").is_file()
            assert len(c.commit) == 40

    def test_the_patch_carries_the_real_change(self, repo, tmp_path):
        r, base = repo
        s = resolve_review_subject(r, base)
        pdir = _export(tmp_path / "ev", s, r)
        first = (pdir / commit_patch_filename(s.commits[0].commit)).read_text()
        assert "a.txt" in first and "+one" in first

    def test_a_short_or_bogus_sha_is_refused_as_a_filename(self):
        for bad in ("abc", "", "../escape", "Z" * 40, "/abs/path"):
            with pytest.raises(ReviewSubjectError):
                commit_patch_filename(bad)

    def test_the_bytes_helper_is_deterministic(self, repo):
        r, base = repo
        s = resolve_review_subject(r, base)
        sha = s.commits[0].commit
        assert commit_patch_bytes(r, sha) == commit_patch_bytes(r, sha)

    def test_an_unknown_commit_raises(self, repo):
        r, _base = repo
        with pytest.raises(ReviewSubjectError):
            commit_patch_bytes(r, "d" * 40)

    def test_no_absolute_local_path_enters_the_patch(self, repo, tmp_path):
        """Patch headers are repo-relative; the operator's directory is not evidence."""
        r, base = repo
        s = resolve_review_subject(r, base)
        pdir = _export(tmp_path / "ev", s, r)
        for p in pdir.glob("*.patch"):
            text = p.read_text()
            assert str(tmp_path) not in text
            assert "/home/" not in text


# --------------------------------------------------------------------------- the packager


class TestThePackagerVerifiesThePatches:
    def _verify(self, ev, r, monkeypatch):
        from scripts.build_review_manifest import _verify_commit_chain

        monkeypatch.chdir(r)
        return _verify_commit_chain(str(ev), set())

    def test_a_faithful_package_verifies(self, repo, tmp_path, monkeypatch):
        r, base = repo
        _export(tmp_path / "ev", resolve_review_subject(r, base), r)
        assert self._verify(tmp_path / "ev", r, monkeypatch) == []

    def test_a_missing_patch_blocks(self, repo, tmp_path, monkeypatch):
        r, base = repo
        s = resolve_review_subject(r, base)
        pdir = _export(tmp_path / "ev", s, r)
        (pdir / commit_patch_filename(s.commits[0].commit)).unlink()
        probs = self._verify(tmp_path / "ev", r, monkeypatch)
        assert any("no packaged patch artifact" in p for p in probs), probs

    def test_an_absent_patch_directory_blocks(self, repo, tmp_path, monkeypatch):
        import shutil

        r, base = repo
        s = resolve_review_subject(r, base)
        pdir = _export(tmp_path / "ev", s, r)
        shutil.rmtree(pdir)
        probs = self._verify(tmp_path / "ev", r, monkeypatch)
        assert any("carries no review_commit_patches/" in p for p in probs), probs

    def test_an_extra_patch_blocks(self, repo, tmp_path, monkeypatch):
        r, base = repo
        pdir = _export(tmp_path / "ev", resolve_review_subject(r, base), r)
        (pdir / f"{'e' * 40}.patch").write_bytes(b"invented\n")
        probs = self._verify(tmp_path / "ev", r, monkeypatch)
        assert any("which no chain commit names" in p for p in probs), probs

    def test_a_tampered_patch_blocks(self, repo, tmp_path, monkeypatch):
        r, base = repo
        s = resolve_review_subject(r, base)
        pdir = _export(tmp_path / "ev", s, r)
        p = pdir / commit_patch_filename(s.commits[0].commit)
        p.write_bytes(p.read_bytes() + b"\n# smuggled\n")
        probs = self._verify(tmp_path / "ev", r, monkeypatch)
        assert any("not the repository's patch bytes" in p or "hashes to" in p
                   for p in probs), probs

    def test_a_patch_swapped_between_commits_blocks(self, repo, tmp_path, monkeypatch):
        r, base = repo
        s = resolve_review_subject(r, base)
        pdir = _export(tmp_path / "ev", s, r)
        a = pdir / commit_patch_filename(s.commits[0].commit)
        b = pdir / commit_patch_filename(s.commits[1].commit)
        a_bytes, b_bytes = a.read_bytes(), b.read_bytes()
        a.write_bytes(b_bytes)
        b.write_bytes(a_bytes)
        assert self._verify(tmp_path / "ev", r, monkeypatch)
