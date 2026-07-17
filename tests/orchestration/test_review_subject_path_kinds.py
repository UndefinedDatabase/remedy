"""F5 (round 16) — a typed file-kind contract: inspect, never follow.

Round 15 hashed every dirty path with `read_bytes()`. That FOLLOWS symlinks, so:

    repo/link.txt -> /tmp/outside.txt

put the OUTSIDE file's bytes into `current_change_content_proof.json`, while the ZIP collector
(`find -type f`) never packaged the link at all. The proof described a file the package did not
contain, with content read from outside the repository entirely — and both halves were silent.

`is_file()` and `read_bytes()` answer "what does this point AT". A review needs "what IS this".
So every working-tree path is inspected with `lstat`, its kind is recorded, and each kind carries
exactly the one proof it honestly can — or is refused.
"""
from __future__ import annotations

import os
import subprocess

import pytest

from packages.orchestration.review_subject import (
    KIND_DIRECTORY,
    KIND_REGULAR,
    KIND_SPECIAL,
    KIND_SYMLINK,
    inspect_path_kind,
    resolve_review_subject,
    symlink_escapes_repository,
    validate_subject_path_kinds,
)


def _sh(repo, cmd):
    subprocess.run(cmd, shell=True, cwd=repo, check=True, capture_output=True)


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / "repo"
    (r / "sub").mkdir(parents=True)
    _sh(r, "git init -q -b main && git config user.email t@t && git config user.name t")
    _sh(r, "echo x > tracked.txt && git add -A && git commit -qm init")
    outside = tmp_path / "outside.txt"
    outside.write_text("SECRET-OUTSIDE-CONTENT\n")
    return r, outside


def _file(subject, path):
    return next(f for f in subject.files if f.path == path)


# --------------------------------------------------------------------------- the reproduction


class TestTheSymlinkIsNotItsTarget:
    def test_the_reproduced_case(self, repo):
        """A dirty absolute symlink is recorded as a LINK and its target is never read."""
        import hashlib

        r, outside = repo
        os.symlink(str(outside), str(r / "link.txt"))
        s = resolve_review_subject(r)
        rec = _file(s, "link.txt")
        assert rec.kind == KIND_SYMLINK
        assert rec.link_target == str(outside)
        outside_hash = hashlib.sha256(outside.read_bytes()).hexdigest()
        assert rec.current_sha256 != outside_hash, "the target's bytes were hashed"
        assert rec.current_sha256 == hashlib.sha256(
            str(outside).encode("utf-8")).hexdigest(), "a link's content is its target text"

    def test_an_absolute_symlink_blocks_ready_packaging(self, repo):
        r, outside = repo
        os.symlink(str(outside), str(r / "link.txt"))
        s = resolve_review_subject(r)
        probs = validate_subject_path_kinds(s, r)
        assert any("outside the repository" in p for p in probs), probs

    def test_the_outside_content_never_enters_the_proof(self, repo):
        r, outside = repo
        os.symlink(str(outside), str(r / "link.txt"))
        s = resolve_review_subject(r)
        blob = str(s.to_json())
        assert "SECRET-OUTSIDE-CONTENT" not in blob

    def test_an_escaping_relative_symlink_blocks(self, repo):
        r, _outside = repo
        os.symlink("../../outside.txt", str(r / "sub" / "esc.txt"))
        s = resolve_review_subject(r)
        assert any("outside the repository" in p
                   for p in validate_subject_path_kinds(s, r)), s.to_json()

    def test_a_home_symlink_blocks(self, repo):
        r, _o = repo
        os.symlink("~/secrets.txt", str(r / "home.txt"))
        s = resolve_review_subject(r)
        assert any("outside the repository" in p for p in validate_subject_path_kinds(s, r))

    def test_a_contained_relative_symlink_is_deterministic_and_allowed(self, repo):
        """The safe case gets an explicit, reproducible metadata proof."""
        import hashlib

        r, _o = repo
        os.symlink("tracked.txt", str(r / "inside.txt"))
        s = resolve_review_subject(r)
        rec = _file(s, "inside.txt")
        assert rec.kind == KIND_SYMLINK and rec.link_target == "tracked.txt"
        assert rec.current_sha256 == hashlib.sha256(b"tracked.txt").hexdigest()
        assert validate_subject_path_kinds(s, r) == []
        again = resolve_review_subject(r)
        assert _file(again, "inside.txt").current_sha256 == rec.current_sha256

    def test_a_broken_symlink_is_still_a_symlink_not_a_deletion(self, repo):
        r, _o = repo
        os.symlink("nowhere-at-all.txt", str(r / "broken.txt"))
        s = resolve_review_subject(r)
        assert _file(s, "broken.txt").kind == KIND_SYMLINK


# --------------------------------------------------------------------------- other kinds


class TestSpecialAndRegularKinds:
    def test_a_regular_dirty_file_hashes_its_own_bytes(self, repo):
        import hashlib

        r, _o = repo
        (r / "new.py").write_text("fresh = 1\n")
        s = resolve_review_subject(r)
        rec = _file(s, "new.py")
        assert rec.kind == KIND_REGULAR
        assert rec.current_sha256 == hashlib.sha256(b"fresh = 1\n").hexdigest()
        assert validate_subject_path_kinds(s, r) == []

    def test_a_tracked_file_replaced_by_a_fifo_blocks(self, repo):
        """The reachable special-file case: git reports it as a modification to a tracked path,
        so it DOES enter the subject — with nothing to hash and nothing to package."""
        r, _o = repo
        (r / "tracked.txt").unlink()
        os.mkfifo(str(r / "tracked.txt"))
        s = resolve_review_subject(r)
        rec = _file(s, "tracked.txt")
        assert rec.kind == KIND_SPECIAL and rec.current_sha256 is None
        assert any("carries no content proof" in p
                   for p in validate_subject_path_kinds(s, r))

    def test_an_untracked_fifo_is_not_reported_by_git_at_all(self, repo):
        """Honest boundary: `git status -u` does not list a bare FIFO, so it never reaches the
        subject through this door. Recorded rather than asserted the other way round — a test
        claiming we block it here would be claiming a rule that never runs."""
        r, _o = repo
        os.mkfifo(str(r / "pipe"))
        assert "pipe" not in resolve_review_subject(r).paths()

    def test_a_directory_kind_blocks(self, repo):
        """No git path produces it today; the policy is still closed, and proven closed."""
        from packages.orchestration.review_subject import ReviewFileV1, ReviewSubjectV1

        r, _o = repo
        subj = ReviewSubjectV1(files=(ReviewFileV1(path="sub", status="dirty",
                                                   kind=KIND_DIRECTORY),))
        assert any("carries no content proof" in p
                   for p in validate_subject_path_kinds(subj, r))

    def test_an_unsupported_kind_blocks(self, repo):
        from packages.orchestration.review_subject import ReviewFileV1, ReviewSubjectV1

        r, _o = repo
        subj = ReviewSubjectV1(files=(ReviewFileV1(path="x", status="dirty", kind="invented"),))
        assert any("unsupported kind" in p for p in validate_subject_path_kinds(subj, r))

    def test_a_deleted_tracked_file_is_a_tombstone_not_a_special(self, repo):
        r, _o = repo
        (r / "tracked.txt").unlink()
        s = resolve_review_subject(r)
        rec = _file(s, "tracked.txt")
        assert rec.status == "deleted" and rec.current_sha256 is None
        assert validate_subject_path_kinds(s, r) == []

    def test_inspect_path_kind_never_follows(self, repo):
        r, outside = repo
        os.symlink(str(outside), str(r / "l.txt"))
        kind, target = inspect_path_kind(r / "l.txt")
        assert (kind, target) == (KIND_SYMLINK, str(outside))
        assert inspect_path_kind(r / "tracked.txt") == (KIND_REGULAR, None)
        assert inspect_path_kind(r / "sub") == (KIND_DIRECTORY, None)
        assert inspect_path_kind(r / "does-not-exist")[0] == "deleted"


# --------------------------------------------------------------------------- the rule


class TestTheEscapeRuleIsLexical:
    @pytest.mark.parametrize("target", [
        "/etc/passwd", "~/secret", "../outside", "../../outside", "sub/../../outside", "",
    ])
    def test_escaping_targets(self, tmp_path, target):
        assert symlink_escapes_repository(tmp_path, "link.txt", target)

    @pytest.mark.parametrize("target", ["tracked.txt", "./tracked.txt", "sub/inner.txt"])
    def test_contained_targets(self, tmp_path, target):
        assert not symlink_escapes_repository(tmp_path, "link.txt", target)

    def test_a_nested_link_resolves_relative_to_its_own_directory(self, tmp_path):
        """`sub/link -> ../tracked.txt` stays inside; `sub/link -> ../../x` does not."""
        assert not symlink_escapes_repository(tmp_path, "sub/link", "../tracked.txt")
        assert symlink_escapes_repository(tmp_path, "sub/link", "../../x")

    def test_the_rule_never_touches_the_filesystem(self, tmp_path):
        """It decides on the recorded TEXT — resolving would read the outside path this exists
        to avoid, and would answer the wrong question anyway (F010's binding clause)."""
        assert symlink_escapes_repository(tmp_path, "l", "/does/not/exist/anywhere")
