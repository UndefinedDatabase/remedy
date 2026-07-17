"""F7 (round 15) — the packaged commit history is machine-verifiable, not prose.

The operator's handoff used to say "there were six commits" in a table a reader had to take on
trust. A reader could not check that the packaged history starts after the declared base, ends at
the reviewed HEAD, forms one connected path, or carries no unrelated commit swept in from
somewhere else.

So the chain is an artifact — `review_commit_chain.json` — that the package builder RECOMPUTES
from the repository and holds the artifact to.

`--ancestry-path` is what keeps it honest: a commit merely reachable from HEAD by some other route
is not part of the path from the base to HEAD, and must not appear in a package's history.
"""
from __future__ import annotations

import subprocess

import pytest

from packages.orchestration.review_subject import (
    ReviewSubjectError,
    resolve_commit_chain,
    resolve_review_subject,
    validate_commit_chain,
)


def _sh(repo, cmd):
    subprocess.run(cmd, shell=True, cwd=repo, check=True, capture_output=True)


def _rev(repo, ref="HEAD"):
    return subprocess.run(["git", "rev-parse", ref], cwd=repo, capture_output=True,
                          text=True).stdout.strip()


@pytest.fixture
def repo(tmp_path):
    """base -> c1 -> c2 -> c3 on a feature branch, plus an unrelated branch."""
    r = tmp_path / "repo"
    r.mkdir()
    _sh(r, "git init -q -b main && git config user.email t@t && git config user.name t")
    _sh(r, "echo base > base.txt && git add -A && git commit -qm base")
    base = _rev(r)
    _sh(r, "git checkout -q -b other && echo u > other.txt && git add -A && git commit -qm other")
    _sh(r, f"git checkout -q {base} && git checkout -q -b feature")
    _sh(r, "echo one > a.txt && git add -A && git commit -qm 'first'")
    _sh(r, "echo two > b.txt && git add -A && git commit -qm 'second'")
    _sh(r, "echo three > c.txt && git add -A && git commit -qm 'third'")
    return r, base


# --------------------------------------------------------------------------- the chain


class TestTheChainIsRecomputable:
    def test_it_starts_after_the_declared_base(self, repo):
        r, base = repo
        chain = resolve_commit_chain(r, base, _rev(r))
        assert base not in [c.commit for c in chain], "the base itself is not part of the change"
        assert base in chain[0].parents

    def test_it_ends_at_the_packaged_head(self, repo):
        r, base = repo
        chain = resolve_commit_chain(r, base, _rev(r))
        assert chain[-1].commit == _rev(r)

    def test_it_is_ordered_oldest_first_and_connected(self, repo):
        r, base = repo
        chain = resolve_commit_chain(r, base, _rev(r))
        assert [c.subject for c in chain] == ["first", "second", "third"]
        for prev, nxt in zip(chain, chain[1:]):
            assert prev.commit in nxt.parents

    def test_every_commit_carries_verifiable_metadata(self, repo):
        r, base = repo
        for c in resolve_commit_chain(r, base, _rev(r)):
            assert len(c.commit) == 40 and len(c.tree) == 40
            assert len(c.patch_sha256) == 64
            assert c.parents and all(len(p) == 40 for p in c.parents)
            assert c.changed_files

    def test_the_changed_file_union_is_the_committed_subject(self, repo):
        r, base = repo
        s = resolve_review_subject(r, base)
        union = {f for c in s.commits for f in c.changed_files}
        assert union == set(s.paths())

    def test_an_unrelated_branch_commit_never_appears(self, repo):
        r, base = repo
        chain = resolve_commit_chain(r, base, _rev(r))
        assert all("other" not in c.subject for c in chain)
        assert not any("other.txt" in c.changed_files for c in chain)

    def test_a_patch_hash_changes_when_the_patch_does(self, repo, tmp_path):
        r, base = repo
        first = resolve_commit_chain(r, base, _rev(r))[0].patch_sha256
        r2 = tmp_path / "repo2"
        r2.mkdir()
        _sh(r2, "git init -q -b main && git config user.email t@t && git config user.name t")
        _sh(r2, "echo base > base.txt && git add -A && git commit -qm base")
        b2 = _rev(r2)
        _sh(r2, "git checkout -q -b feature && echo DIFFERENT > a.txt "
                "&& git add -A && git commit -qm 'first'")
        assert resolve_commit_chain(r2, b2, _rev(r2))[0].patch_sha256 != first


# --------------------------------------------------------------------------- validation


class TestTheChainValidates:
    def test_a_real_chain_passes(self, repo):
        r, base = repo
        assert validate_commit_chain(resolve_review_subject(r, base)) == []

    def test_a_chain_that_does_not_end_at_head_blocks(self, repo):
        import dataclasses
        r, base = repo
        s = resolve_review_subject(r, base)
        truncated = dataclasses.replace(s, commits=s.commits[:-1])
        assert any("ends at" in p for p in validate_commit_chain(truncated))

    def test_a_chain_with_a_broken_link_blocks(self, repo):
        import dataclasses
        r, base = repo
        s = resolve_review_subject(r, base)
        forged = dataclasses.replace(
            s, commits=(s.commits[0], dataclasses.replace(s.commits[1], parents=("f" * 40,)),
                        s.commits[2]))
        assert any("does not descend" in p for p in validate_commit_chain(forged))

    def test_a_chain_not_starting_after_the_base_blocks(self, repo):
        import dataclasses
        r, base = repo
        s = resolve_review_subject(r, base)
        forged = dataclasses.replace(s, commits=s.commits[1:])
        assert any("does not descend from the declared base" in p
                   for p in validate_commit_chain(forged))

    def test_a_declared_base_with_no_commits_blocks(self, repo):
        import dataclasses
        r, base = repo
        s = resolve_review_subject(r, base)
        forged = dataclasses.replace(s, commits=())
        assert validate_commit_chain(forged)

    def test_an_undeclared_subject_has_no_chain_to_validate(self, repo):
        r, _base = repo
        assert validate_commit_chain(resolve_review_subject(r, "")) == []


# --------------------------------------------------------------------------- packaging


class TestThePackagerVerifiesTheArtifact:
    def _write(self, ev, subject):
        import json
        ev.mkdir(parents=True, exist_ok=True)
        (ev / "review_subject.json").write_text(json.dumps(subject.to_json()))
        (ev / "review_commit_chain.json").write_text(json.dumps({
            "chain_v": 1, "base_commit": subject.base_commit,
            "head_commit": subject.head_commit,
            "commits": [c.to_json() for c in subject.commits]}))

    def test_a_faithful_artifact_verifies(self, repo, tmp_path, monkeypatch):
        from scripts.build_review_manifest import _verify_commit_chain
        r, base = repo
        s = resolve_review_subject(r, base)
        ev = tmp_path / "ev"
        self._write(ev, s)
        monkeypatch.chdir(r)
        assert _verify_commit_chain(str(ev), set(s.paths())) == []

    def test_a_tampered_commit_chain_is_rejected(self, repo, tmp_path, monkeypatch):
        """The point of an artifact: it can be checked, so it can be caught."""
        import dataclasses

        from scripts.build_review_manifest import _verify_commit_chain
        r, base = repo
        s = resolve_review_subject(r, base)
        forged = dataclasses.replace(s, commits=(
            dataclasses.replace(s.commits[0], patch_sha256="0" * 64),) + s.commits[1:])
        ev = tmp_path / "ev2"
        self._write(ev, forged)
        monkeypatch.chdir(r)
        probs = _verify_commit_chain(str(ev), set(s.paths()))
        assert any("patch_sha256 does not match" in p for p in probs), probs

    def test_a_dropped_commit_is_rejected(self, repo, tmp_path, monkeypatch):
        import dataclasses

        from scripts.build_review_manifest import _verify_commit_chain
        r, base = repo
        s = resolve_review_subject(r, base)
        ev = tmp_path / "ev3"
        self._write(ev, dataclasses.replace(s, commits=s.commits[:2]))
        monkeypatch.chdir(r)
        probs = _verify_commit_chain(str(ev), set(s.paths()))
        assert any("ancestry path has" in p for p in probs), probs

    def test_a_subject_claiming_an_uncommitted_change_is_rejected(self, repo, tmp_path,
                                                                  monkeypatch):
        """The direction that matters: the subject cannot claim a committed change that no
        packaged commit made."""
        import dataclasses

        from packages.orchestration.review_subject import ReviewFileV1
        from scripts.build_review_manifest import _verify_commit_chain
        r, base = repo
        s = resolve_review_subject(r, base)
        forged = dataclasses.replace(s, files=s.files + (
            ReviewFileV1(path="never_committed.py", status="modified",
                         base_sha256="a" * 64, current_sha256="b" * 64),))
        ev = tmp_path / "ev4"
        self._write(ev, forged)
        monkeypatch.chdir(r)
        probs = _verify_commit_chain(str(ev), set(forged.paths()))
        assert any("no packaged commit made" in p for p in probs), probs

    def test_a_file_changed_then_reverted_inside_the_range_is_not_a_stray(self, tmp_path,
                                                                         monkeypatch):
        """Honest history: the commits touched it, the NET delta does not contain it. Requiring
        the commit union to EQUAL the subject flagged exactly this, wrongly."""
        from scripts.build_review_manifest import _verify_commit_chain
        r = tmp_path / "reverted"
        r.mkdir()
        _sh(r, "git init -q -b main && git config user.email t@t && git config user.name t")
        _sh(r, "echo original > flip.py && echo keep > keep.py && git add -A "
               "&& git commit -qm base")
        base = _rev(r)
        _sh(r, "git checkout -q -b feature")
        _sh(r, "echo edited > flip.py && git add -A && git commit -qm 'edit flip'")
        _sh(r, "echo real > keep.py && git add -A && git commit -qm 'edit keep'")
        _sh(r, "echo original > flip.py && git add -A && git commit -qm 'revert flip'")
        s = resolve_review_subject(r, base)
        assert s.paths() == ["keep.py"], "the net subject excludes the reverted file"
        assert any("flip.py" in c.changed_files for c in s.commits), "but commits touched it"
        ev = tmp_path / "ev5"
        self._write(ev, s)
        monkeypatch.chdir(r)
        assert _verify_commit_chain(str(ev), set(s.paths())) == []

    def test_an_undeclared_subject_is_not_verified(self, tmp_path, monkeypatch, repo):
        from scripts.build_review_manifest import _verify_commit_chain
        r, _base = repo
        monkeypatch.chdir(r)
        assert _verify_commit_chain(str(tmp_path / "empty"), set()) == []


# --------------------------------------------------------------------------- errors


class TestUnreadableChainsAreErrors:
    def test_an_invalid_base_cannot_produce_a_chain(self, repo):
        r, _base = repo
        with pytest.raises(ReviewSubjectError):
            resolve_commit_chain(r, "NO_SUCH_BASE", _rev(r))
