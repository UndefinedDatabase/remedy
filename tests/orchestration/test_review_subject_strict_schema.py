"""F7 (round 17) — strict external schema for review_subject.json.

The final packager ignored unknown fields, `subject_v`, `link_target` rules and the embedded
commit list. A packager that ignores unknown fields is one that would ship an injected
`secret`/`path` field untouched. The schema is now exact: closed field sets, closed enums, safe
paths, lowercase hashes, `link_target` required for symlinks and forbidden elsewhere.
"""
from __future__ import annotations

from packages.orchestration.review_subject import (
    validate_review_file_schema,
    validate_review_subject_schema,
)


def _file(**kw):
    # A complete `modified` record per the round-20 state matrix (base + current facts present).
    base = {"path": "a.py", "status": "modified", "base_sha256": "a" * 64,
            "current_sha256": "b" * 64, "kind": "regular",
            "base_kind": "regular", "base_mode": "100644", "current_mode": "100644"}
    base.update(kw)
    return base


def _subject(files=None, **kw):
    base = {"subject_v": 1, "base_commit": "c" * 40, "head_commit": "d" * 40,
            "base_is_ancestor": True, "commits": [], "files": files or [_file()]}
    base.update(kw)
    return base


# --------------------------------------------------------------------------- file schema


class TestReviewFileSchema:
    def test_a_clean_record_passes(self):
        assert validate_review_file_schema(_file()) == []

    def test_an_unknown_file_field_blocks(self):
        assert any("unknown field" in p
                   for p in validate_review_file_schema(_file(secret="/home/alice")))

    def test_a_missing_required_field_blocks(self):
        d = _file()
        del d["kind"]
        assert any("missing required field 'kind'" in p
                   for p in validate_review_file_schema(d))

    def test_an_unsafe_path_blocks(self):
        for bad in ("/abs.py", "../escape.py", "a//b.py"):
            assert any("not a safe relative path" in p
                       for p in validate_review_file_schema(_file(path=bad))), bad

    def test_an_unsupported_status_blocks(self):
        assert any("not a supported status" in p
                   for p in validate_review_file_schema(_file(status="invented")))

    def test_an_unsupported_kind_blocks(self):
        assert any("not a supported kind" in p
                   for p in validate_review_file_schema(_file(kind="invented")))

    def test_a_non_hex_hash_blocks(self):
        assert any("sha256" in p
                   for p in validate_review_file_schema(_file(base_sha256="ZZZ")))

    def test_a_symlink_without_link_target_blocks(self):
        assert any("no link_target" in p
                   for p in validate_review_file_schema(_file(kind="symlink")))

    def test_a_symlink_with_link_target_passes(self):
        assert validate_review_file_schema(
            _file(kind="symlink", link_target="target.txt",
                  base_kind="symlink", base_mode="120000", current_mode="120000")) == []

    def test_a_regular_file_with_link_target_blocks(self):
        assert any("carries a link_target" in p
                   for p in validate_review_file_schema(
                       _file(kind="regular", link_target="x")))

    def test_an_unsafe_old_path_blocks(self):
        assert any("old_path" in p
                   for p in validate_review_file_schema(
                       _file(status="renamed", old_path="../evil")))


# --------------------------------------------------------------------------- subject schema


class TestReviewSubjectSchema:
    def test_a_clean_subject_passes(self):
        assert validate_review_subject_schema(_subject()) == []

    def test_an_unknown_top_level_field_blocks(self):
        assert any("unknown field" in p
                   for p in validate_review_subject_schema(_subject(injected="/home/alice")))

    def test_a_wrong_subject_version_blocks(self):
        assert any("subject_v" in p
                   for p in validate_review_subject_schema(_subject(subject_v=99)))

    def test_a_non_boolean_ancestor_blocks(self):
        assert any("base_is_ancestor" in p
                   for p in validate_review_subject_schema(_subject(base_is_ancestor="yes")))

    def test_a_bad_file_inside_blocks(self):
        assert any("file[0]" in p
                   for p in validate_review_subject_schema(
                       _subject(files=[_file(kind="invented")])))

    def test_a_secret_canary_field_is_refused(self):
        """The point of strictness: an injected path/secret field cannot ride along."""
        s = _subject()
        s["files"][0]["EXTRA_SECRET"] = "/home/alice/id_rsa"
        assert validate_review_subject_schema(s)
