"""F2 (round 17) — ONE lossless, typed merge of committed and dirty file records.

A path can be both committed (base..HEAD) and dirty (HEAD..working-tree). The working tree is the
later truth, so its current side wins — but the previous inline merge rebuilt a bare
`ReviewFileV1(path, status, base_sha256, current_sha256, old_path)` and silently dropped `kind`,
`link_target`, `base_kind` and the modes. So a dirty symlink over a committed regular file came
back a REGULAR file, and the package then hashed it as one — a symlink laundered into a regular
file at exactly the seam F5 exists to keep honest.

`merge_review_file_state` keeps every typed field, from whichever side owns it.
"""
from __future__ import annotations

import os
import subprocess

import pytest

from packages.orchestration.review_subject import (
    KIND_REGULAR,
    KIND_SYMLINK,
    STATUS_DELETED,
    ReviewFileV1,
    merge_review_file_state,
    resolve_review_subject,
)


def _sh(r, c):
    subprocess.run(c, shell=True, cwd=r, check=True, capture_output=True)


def _rev(r, ref="HEAD"):
    return subprocess.run(["git", "rev-parse", ref], cwd=r, capture_output=True,
                          text=True).stdout.strip()


def _file(subject, path):
    return next(f for f in subject.files if f.path == path)


# --------------------------------------------------------------------------- the unit


class TestTheMergeIsLosslessAndTyped:
    def test_a_dirty_symlink_over_a_committed_regular_stays_a_symlink(self):
        """THE finding."""
        committed = ReviewFileV1(path="p", status="modified", base_sha256="a" * 64,
                                 current_sha256="b" * 64, kind=KIND_REGULAR,
                                 base_kind=KIND_REGULAR, base_mode="100644",
                                 current_mode="100644")
        dirty = ReviewFileV1(path="p", status="dirty", current_sha256="c" * 64,
                             kind=KIND_SYMLINK, link_target="target.txt")
        merged = merge_review_file_state(committed, dirty)
        assert merged.kind == KIND_SYMLINK
        assert merged.link_target == "target.txt"
        assert merged.current_sha256 == "c" * 64

    def test_the_committed_base_side_is_preserved(self):
        committed = ReviewFileV1(path="p", status="modified", base_sha256="a" * 64,
                                 base_kind=KIND_REGULAR, base_mode="100644")
        dirty = ReviewFileV1(path="p", status="dirty", current_sha256="c" * 64,
                             kind=KIND_REGULAR)
        merged = merge_review_file_state(committed, dirty)
        assert merged.base_sha256 == "a" * 64
        assert merged.base_kind == KIND_REGULAR
        assert merged.base_mode == "100644"

    def test_a_committed_symlink_over_a_dirty_regular_records_both_kinds(self):
        committed = ReviewFileV1(path="p", status="modified", base_sha256="a" * 64,
                                 kind=KIND_SYMLINK, base_kind=KIND_SYMLINK,
                                 base_mode="120000", link_target="was")
        dirty = ReviewFileV1(path="p", status="dirty", current_sha256="c" * 64,
                             kind=KIND_REGULAR)
        merged = merge_review_file_state(committed, dirty)
        assert merged.kind == KIND_REGULAR          # current side wins
        assert merged.base_kind == KIND_SYMLINK     # base side preserved

    def test_a_dirty_only_record_passes_through_unchanged(self):
        dirty = ReviewFileV1(path="p", status="dirty", current_sha256="c" * 64,
                             kind=KIND_SYMLINK, link_target="t")
        assert merge_review_file_state(None, dirty) is dirty

    def test_a_committed_deletion_is_not_silently_resurrected(self):
        committed = ReviewFileV1(path="p", status=STATUS_DELETED, base_sha256="a" * 64,
                                 base_kind=KIND_REGULAR, base_mode="100644")
        dirty = ReviewFileV1(path="p", status="dirty", current_sha256=None, kind="deleted")
        merged = merge_review_file_state(committed, dirty)
        assert merged.status == STATUS_DELETED
        assert merged.base_sha256 == "a" * 64

    def test_the_dirty_base_is_used_when_committed_has_none(self):
        dirty = ReviewFileV1(path="p", status="dirty", base_sha256="d" * 64,
                             base_kind=KIND_REGULAR, current_sha256="c" * 64, kind=KIND_REGULAR)
        committed = ReviewFileV1(path="p", status="added", base_sha256=None)
        merged = merge_review_file_state(committed, dirty)
        assert merged.base_sha256 == "d" * 64

    def test_no_field_falls_back_to_a_dataclass_default(self):
        """Every typed field is populated from one side or the other — nothing goes silently
        empty just because the merge forgot it (which is the whole bug)."""
        committed = ReviewFileV1(path="p", status="modified", base_sha256="a" * 64,
                                 base_kind=KIND_REGULAR, base_mode="100644", old_path=None)
        dirty = ReviewFileV1(path="p", status="dirty", current_sha256="c" * 64,
                             kind=KIND_SYMLINK, link_target="t", current_mode="120000")
        merged = merge_review_file_state(committed, dirty)
        assert merged.current_mode == "120000"
        assert merged.link_target == "t"
        assert merged.base_mode == "100644"


# --------------------------------------------------------------------------- end to end


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / "repo"
    r.mkdir()
    _sh(r, "git init -q -b main && git config user.email t@t && git config user.name t")
    _sh(r, "echo regular > p.py && git add -A && git commit -qm base")
    base = _rev(r)
    _sh(r, "git checkout -q -b feature")
    _sh(r, "echo committed-change > p.py && git add -A && git commit -qm change")
    return r, base


class TestTheUnionThroughResolve:
    def test_a_committed_file_replaced_by_a_dirty_symlink_stays_a_symlink(self, repo):
        r, base = repo
        (r / "p.py").unlink()
        os.symlink("elsewhere.py", str(r / "p.py"))
        rec = _file(resolve_review_subject(r, base), "p.py")
        assert rec.kind == KIND_SYMLINK
        assert rec.link_target == "elsewhere.py"

    def test_a_committed_then_dirty_edit_keeps_the_base_from_the_review_base(self, repo):
        r, base = repo
        (r / "p.py").write_text("further edit\n")
        rec = _file(resolve_review_subject(r, base), "p.py")
        assert rec.kind == KIND_REGULAR
        assert rec.base_sha256 is not None       # the base..HEAD base, not lost
        assert rec.current_sha256 is not None
