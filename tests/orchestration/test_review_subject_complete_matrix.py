"""F8 (round 20) — the complete ReviewFile state matrix. Every impossible shape fails strict decode.
"""
from __future__ import annotations

from packages.orchestration.review_subject import validate_review_file_schema


def _f(**over):
    d = {"path": "a.py", "status": "modified", "kind": "regular",
         "base_sha256": "a" * 64, "current_sha256": "b" * 64,
         "base_kind": "regular", "base_mode": "100644", "current_mode": "100644"}
    d.update(over)
    return d


def _probs(**over):
    return validate_review_file_schema(_f(**over))


class TestAdded:
    def test_added_without_current_mode_blocks(self):
        assert any("no current_mode" in p for p in _probs(
            status="added", base_sha256=None, base_kind=None, base_mode="", current_mode=""))

    def test_added_with_old_path_blocks(self):
        assert any("added but names an old_path" in p for p in _probs(
            status="added", base_sha256=None, base_kind=None, base_mode="", old_path="x.py"))


class TestModified:
    def test_modified_without_base_kind_blocks(self):
        assert any("no base_kind" in p for p in _probs(base_kind=None))

    def test_modified_without_base_mode_blocks(self):
        assert any("no base_mode" in p for p in _probs(base_mode=""))


class TestDirtyDeletion:
    def test_dirty_kind_deleted_must_be_normalized(self):
        assert any("not normalized" in p for p in _probs(
            status="dirty", kind="deleted", current_sha256=None, current_mode=""))


class TestDeleted:
    def test_deleted_without_base_kind_blocks(self):
        assert any("no base_kind" in p for p in _probs(
            status="deleted", kind="deleted", current_sha256=None, current_mode="",
            base_kind=None))

    def test_a_clean_deletion_passes(self):
        assert _probs(status="deleted", kind="deleted", current_sha256=None, current_mode="") == []


class TestRenameCopy:
    def test_rename_without_old_path_blocks(self):
        assert any("names no old_path" in p for p in _probs(status="renamed"))

    def test_rename_with_identical_old_path_blocks(self):
        assert any("old_path equals the current path" in p for p in _probs(
            status="renamed", old_path="a.py"))

    def test_copy_without_base_facts_blocks(self):
        assert any("no base_kind" in p for p in _probs(
            status="copied", old_path="src.py", base_kind=None))

    def test_a_clean_rename_passes(self):
        assert _probs(status="renamed", old_path="old.py") == []


class TestTypeChanged:
    def test_type_changed_with_no_change_blocks(self):
        assert any("no mode change" in p for p in _probs(
            status="type_changed", kind="regular", base_kind="regular",
            base_mode="100644", current_mode="100644"))

    def test_type_changed_by_mode_passes(self):
        assert _probs(status="type_changed", kind="regular", base_kind="regular",
                      base_mode="100644", current_mode="100755") == []
