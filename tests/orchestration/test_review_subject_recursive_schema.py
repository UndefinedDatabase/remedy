"""F4/F5 (round 18) — the ReviewSubject schema is exact RECURSIVELY.

Round 17 validated the top-level fields and each file's path/status/kind/hashes, but not the
embedded commit list, and not the round-17 typed file fields (base_kind, base_mode, current_mode).
So `commits: [{"EXTRA_SECRET": "/home/alice/..."}]` and `base_kind: "SECRET-/home/alice"`,
`base_mode: "999999"`, `current_mode: "evil-mode"` were all accepted. A packager that accepts a
known field with an arbitrary string would ship an injected secret untouched.
"""
from __future__ import annotations

import pytest

from packages.orchestration.review_subject import (
    ReviewSubjectError,
    decode_review_subject_from_json,
    validate_review_commit_schema,
    validate_review_file_schema,
    validate_review_subject_schema,
)


def _commit(**kw):
    base = {"commit": "a" * 40, "parents": ["b" * 40], "tree": "c" * 40, "subject": "msg",
            "changed_files": ["x.py"], "patch_sha256": "d" * 64}
    base.update(kw)
    return base


def _file(**kw):
    base = {"path": "f.py", "status": "modified", "base_sha256": "a" * 64,
            "current_sha256": "b" * 64, "kind": "regular"}
    base.update(kw)
    return base


def _subject(files=None, commits=None, **kw):
    base = {"subject_v": 1, "base_commit": "c" * 40, "head_commit": "d" * 40,
            "base_is_ancestor": True, "commits": commits or [], "files": files or [_file()]}
    base.update(kw)
    return base


# --------------------------------------------------------------------------- commits (F4)


class TestCommitSchema:
    def test_a_clean_commit_passes(self):
        assert validate_review_commit_schema(_commit()) == []

    def test_the_reproduced_unknown_field_blocks(self):
        probs = validate_review_commit_schema(_commit(EXTRA_SECRET="/home/alice/SUPERSECRET"))
        assert any("unknown field" in p for p in probs)

    def test_a_short_or_nonhex_commit_sha_blocks(self):
        assert validate_review_commit_schema(_commit(commit="abc"))
        assert validate_review_commit_schema(_commit(tree="ZZ" * 20))

    def test_a_bad_parent_blocks(self):
        assert validate_review_commit_schema(_commit(parents=["short"]))

    def test_a_subject_with_a_local_path_or_secret_blocks(self):
        assert validate_review_commit_schema(_commit(subject="see /home/alice/id_rsa"))

    def test_a_subject_with_a_control_char_blocks(self):
        assert validate_review_commit_schema(_commit(subject="line\x00null"))

    def test_unsorted_or_duplicate_changed_files_block(self):
        assert validate_review_commit_schema(_commit(changed_files=["b.py", "a.py"]))
        assert validate_review_commit_schema(_commit(changed_files=["a.py", "a.py"]))

    def test_a_bad_patch_sha_blocks(self):
        assert validate_review_commit_schema(_commit(patch_sha256="nope"))


# --------------------------------------------------------------------------- files (F4)


class TestFileMetadataSchema:
    def test_the_reproduced_bad_base_kind_blocks(self):
        assert any("base_kind" in p
                   for p in validate_review_file_schema(_file(base_kind="SECRET-/home/alice")))

    def test_the_reproduced_bad_base_mode_blocks(self):
        assert any("base_mode" in p
                   for p in validate_review_file_schema(_file(base_mode="999999")))

    def test_the_reproduced_bad_current_mode_blocks(self):
        assert any("current_mode" in p
                   for p in validate_review_file_schema(_file(current_mode="evil-mode")))

    def test_a_secret_in_metadata_blocks(self):
        # A closed base_kind value cannot carry a secret; the scanner catches the case where a
        # closed field is bypassed (e.g. a control character riding in a valid-looking mode is
        # already blocked by the mode enum). Here we prove the scanner fires on a subject-carried
        # secret in the one place a free string lives: the commit subject.
        assert validate_review_commit_schema(_commit(subject="token=/home/alice/id_rsa"))
        # ...and a legitimate typed record passes untouched.
        assert validate_review_file_schema(
            _file(base_mode="100644", base_kind="regular")) == []

    def test_a_symlink_current_mode_on_a_regular_blocks(self):
        assert any("symlink current_mode" in p
                   for p in validate_review_file_schema(_file(kind="regular",
                                                              current_mode="120000")))

    def test_an_added_file_with_a_base_hash_blocks(self):
        assert any("added but carries a base_sha256" in p
                   for p in validate_review_file_schema(
                       _file(status="added", base_sha256="a" * 64)))

    def test_a_valid_metadata_record_passes(self):
        assert validate_review_file_schema(
            _file(base_kind="regular", base_mode="100644", current_mode="100644")) == []


# --------------------------------------------------------------------------- subject + shas


class TestSubjectShaAndDecode:
    def test_a_non_full_base_sha_blocks(self):
        assert any("base_commit" in p
                   for p in validate_review_subject_schema(_subject(base_commit="abc123")))

    def test_the_legacy_empty_form_passes(self):
        s = {"subject_v": 1, "base_commit": "", "head_commit": "", "base_is_ancestor": False,
             "commits": [], "files": []}
        assert validate_review_subject_schema(s) == []

    def test_a_duplicate_path_blocks(self):
        assert any("more than once" in p
                   for p in validate_review_subject_schema(
                       _subject(files=[_file(), _file()])))

    def test_the_strict_decoder_refuses_a_bad_subject(self):
        with pytest.raises(ReviewSubjectError):
            decode_review_subject_from_json(_subject(commits=[_commit(EXTRA="x")]))

    def test_the_strict_decoder_round_trips_a_clean_subject(self):
        s = decode_review_subject_from_json(_subject(
            commits=[_commit()],
            files=[_file(base_kind="regular", base_mode="100644", current_mode="100644")]))
        assert s.base_commit == "c" * 40
        assert len(s.commits) == 1 and len(s.files) == 1
        assert s.files[0].base_mode == "100644"
