"""F8/F10 (round 17) — the ZIP is built from an exact, path-safe file model.

`find -print | sort | zip -@` is newline-delimited end to end, so a filename containing a newline
is silently truncated or dropped — the typed subject is NUL-safe, the archive that represents it is
not. The `zipfile` builder takes an EXPLICIT list of validated relative POSIX paths, preserves
hostile-but-legal names exactly, refuses names that change WHERE a member lands, and then reopens
the archive to verify its member set and hashes exactly (F10).
"""
from __future__ import annotations

import zipfile

import pytest

from packages.orchestration.review_zip import (
    ReviewZipError,
    build_review_zip,
    read_nul_list,
    validate_archive_name,
    verify_review_zip,
)


# --------------------------------------------------------------------------- names


class TestArchiveNameValidation:
    @pytest.mark.parametrize("name", [
        "a\nb.py", "-leading.py", 'q"uote.py', "ünïcode.py", "a\tb.py",
        "dir/sub/file.py", "normal.py",
    ])
    def test_hostile_but_legal_names_are_accepted(self, name):
        validate_archive_name(name)          # must not raise

    @pytest.mark.parametrize("name", [
        "", "/abs.py", "a/../b.py", "a//b.py", "a/./b.py", "back\\slash.py", "a\0b.py",
        "..", ".",
    ])
    def test_names_that_move_the_member_are_refused(self, name):
        with pytest.raises(ReviewZipError):
            validate_archive_name(name)


# --------------------------------------------------------------------------- building


class TestTheBuilderPreservesHostileNames:
    def _build(self, tmp_path, names):
        root = tmp_path / "root"
        root.mkdir()
        for n in names:
            p = root / n
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(f"body of {n}".encode())
        manifest = tmp_path / ".review_zip_manifest.json"
        manifest.write_text("{}")
        out = tmp_path / "out.zip"
        result = build_review_zip(
            out_path=out, repo_root=root, repo_files=list(names),
            evidence_root=None, evidence_files=[],
            manifest_rel=".review_zip_manifest.json", manifest_disk=manifest)
        return out, result

    def test_a_newline_filename_appears_exactly_once(self, tmp_path):
        out, _ = self._build(tmp_path, ["with\nnewline.py"])
        with zipfile.ZipFile(out) as zf:
            assert zf.namelist().count("with\nnewline.py") == 1

    def test_a_leading_dash_filename_is_included(self, tmp_path):
        out, _ = self._build(tmp_path, ["-dashed.py"])
        with zipfile.ZipFile(out) as zf:
            assert "-dashed.py" in zf.namelist()

    def test_quote_and_unicode_names_survive(self, tmp_path):
        out, _ = self._build(tmp_path, ['q"uote.py', "ünïcode.py"])
        with zipfile.ZipFile(out) as zf:
            names = zf.namelist()
            assert 'q"uote.py' in names and "ünïcode.py" in names

    def test_a_duplicate_normalized_archive_path_blocks(self, tmp_path):
        root = tmp_path / "root"
        root.mkdir()
        (root / "a.py").write_text("x")
        manifest = tmp_path / ".review_zip_manifest.json"
        manifest.write_text("{}")
        with pytest.raises(ReviewZipError):
            build_review_zip(
                out_path=tmp_path / "o.zip", repo_root=root,
                repo_files=["a.py", "a.py"], evidence_root=None, evidence_files=[],
                manifest_rel=".review_zip_manifest.json", manifest_disk=manifest)

    def test_a_hostile_traversal_archive_name_blocks(self, tmp_path):
        root = tmp_path / "root"
        root.mkdir()
        manifest = tmp_path / ".review_zip_manifest.json"
        manifest.write_text("{}")
        with pytest.raises(ReviewZipError):
            build_review_zip(
                out_path=tmp_path / "o.zip", repo_root=root,
                repo_files=["../escape.py"], evidence_root=None, evidence_files=[],
                manifest_rel=".review_zip_manifest.json", manifest_disk=manifest)


# --------------------------------------------------------------------------- symlink policy


class TestSymlinkMembersAreMetadata:
    def test_a_repo_symlink_is_recorded_as_its_target_text(self, tmp_path):
        import os

        root = tmp_path / "root"
        root.mkdir()
        (root / "real.py").write_text("real")
        os.symlink("real.py", str(root / "link.py"))
        manifest = tmp_path / ".review_zip_manifest.json"
        manifest.write_text("{}")
        out = tmp_path / "o.zip"
        result = build_review_zip(
            out_path=out, repo_root=root, repo_files=["real.py", "link.py"],
            evidence_root=None, evidence_files=[],
            manifest_rel=".review_zip_manifest.json", manifest_disk=manifest)
        assert result["symlinks"]["link.py"] == "real.py"
        with zipfile.ZipFile(out) as zf:
            assert zf.read("link.py").decode() == "real.py"     # target text, not followed


# --------------------------------------------------------------------------- post-build (F10)


class TestPostBuildVerification:
    def _build(self, tmp_path):
        root = tmp_path / "root"
        root.mkdir()
        (root / "a.py").write_text("aaa")
        (root / "b.py").write_text("bbb")
        manifest = tmp_path / ".review_zip_manifest.json"
        manifest.write_text("{}")
        out = tmp_path / "o.zip"
        result = build_review_zip(
            out_path=out, repo_root=root, repo_files=["a.py", "b.py"],
            evidence_root=None, evidence_files=[],
            manifest_rel=".review_zip_manifest.json", manifest_disk=manifest)
        return out, result

    def test_a_faithful_archive_verifies(self, tmp_path):
        out, result = self._build(tmp_path)
        assert verify_review_zip(out, result) == []

    def test_a_missing_member_is_detected(self, tmp_path):
        out, result = self._build(tmp_path)
        # rebuild the zip without a.py, then verify against the full model
        with zipfile.ZipFile(out, "w") as zf:
            zf.writestr("b.py", "bbb")
            zf.writestr(".review_zip_manifest.json", "{}")
        probs = verify_review_zip(out, result)
        assert any("missing from archive" in p for p in probs), probs

    def test_an_extra_member_is_detected(self, tmp_path):
        out, result = self._build(tmp_path)
        with zipfile.ZipFile(out, "a") as zf:
            zf.writestr("smuggled.py", "surprise")
        probs = verify_review_zip(out, result)
        assert any("unexpected member" in p for p in probs), probs

    def test_a_tampered_member_hash_is_detected(self, tmp_path):
        out, result = self._build(tmp_path)
        # rewrite a.py's content
        buf = {}
        with zipfile.ZipFile(out) as zf:
            for n in zf.namelist():
                buf[n] = zf.read(n)
        buf["a.py"] = b"TAMPERED"
        with zipfile.ZipFile(out, "w") as zf:
            for n, data in buf.items():
                zf.writestr(n, data)
        probs = verify_review_zip(out, result)
        assert any("hash changed" in p for p in probs), probs


# --------------------------------------------------------------------------- NUL lists


class TestNulListReading:
    def test_a_nul_delimited_list_preserves_newline_names(self, tmp_path):
        p = tmp_path / "list0"
        p.write_bytes(b"with\nnewline.py\0normal.py\0")
        assert read_nul_list(p) == ["with\nnewline.py", "normal.py"]

    def test_an_empty_list_is_empty(self, tmp_path):
        p = tmp_path / "empty0"
        p.write_bytes(b"")
        assert read_nul_list(p) == []
