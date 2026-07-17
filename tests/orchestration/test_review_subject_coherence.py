"""F9 (round 19) — the ReviewFile coherence matrix rejects self-contradictory records.

The strict schema closed each field in isolation, so a record could still be internally
incoherent. Each incoherent shape below now produces at least one schema problem.
"""
from __future__ import annotations

from packages.orchestration.review_subject import validate_review_file_schema


def _file(**over):
    d = {
        "path": "a.py", "status": "modified", "kind": "regular",
        "base_sha256": "a" * 64, "current_sha256": "b" * 64,
        "base_kind": "regular", "base_mode": "100644", "current_mode": "100644",
    }
    d.update(over)
    return d


def _problems(**over):
    return validate_review_file_schema(_file(**over))


class TestContentBearingHash:
    def test_modified_regular_without_current_hash_blocks(self):
        assert any("carries no current_sha256" in p
                   for p in _problems(status="modified", current_sha256=None))

    def test_added_regular_without_current_hash_blocks(self):
        assert any("carries no current_sha256" in p
                   for p in _problems(status="added", base_sha256=None, base_kind=None,
                                      base_mode="", current_sha256=None))

    def test_a_directory_with_a_current_hash_blocks(self):
        assert any("carries a current_sha256" in p
                   for p in _problems(status="type_changed", kind="directory",
                                      current_mode="040000", current_sha256="c" * 64))


class TestModeKindAgreement:
    def test_base_symlink_with_regular_mode_blocks(self):
        assert any("base_mode" in p and "does not match base_kind" in p
                   for p in _problems(base_kind="symlink", base_mode="100644"))

    def test_current_mode_disagreeing_with_kind_blocks(self):
        assert any("current_mode" in p and "does not match kind" in p
                   for p in _problems(kind="regular", current_mode="120000",
                                      current_sha256="b" * 64))


class TestStatusPresenceMatrix:
    def test_deleted_without_base_tombstone_blocks(self):
        assert any("no base_sha256 tombstone" in p
                   for p in _problems(status="deleted", kind="deleted", base_sha256=None,
                                      current_sha256=None, current_mode="", base_kind="regular"))

    def test_copied_without_old_path_blocks(self):
        assert any("names no old_path" in p
                   for p in _problems(status="copied"))

    def test_renamed_without_old_path_blocks(self):
        assert any("names no old_path" in p
                   for p in _problems(status="renamed"))

    def test_type_changed_with_same_kind_blocks(self):
        assert any("base and current kind are both" in p
                   for p in _problems(status="type_changed", kind="regular",
                                      base_kind="regular"))

    def test_added_with_a_base_side_blocks(self):
        assert any("added but carries a base" in p
                   for p in _problems(status="added", current_sha256="b" * 64))


class TestCoherentRecordPasses:
    def test_a_well_formed_modified_regular_passes(self):
        assert _problems() == []

    def test_a_well_formed_deletion_passes(self):
        assert _problems(status="deleted", kind="deleted", current_sha256=None,
                         current_mode="", base_kind="regular", base_mode="100644") == []

    def test_a_well_formed_symlink_passes(self):
        assert _problems(kind="symlink", link_target="target.txt", current_mode="120000",
                         base_kind="symlink", base_mode="120000") == []
