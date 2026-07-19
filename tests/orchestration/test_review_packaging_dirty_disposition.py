"""F6 (round 26) — the Root Manifest gives the exact generated packaging outputs their own
disposition instead of reporting them as dirty source. A clean branch stays clean during packaging;
a real dirty file still reports dirty; a source lookalike is never hidden."""
from __future__ import annotations

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
_b = importlib.util.spec_from_file_location(
    "_brm_dirty", REPO_ROOT / "scripts" / "build_review_manifest.py")
_brm = importlib.util.module_from_spec(_b); _b.loader.exec_module(_brm)


class TestIsPackagingOutput:
    def test_manifest_and_zip_and_sidecar(self):
        assert _brm._is_packaging_output(".review_zip_manifest.json")
        assert _brm._is_packaging_output("remedy-review-20260101-000000-READY_FOR_REVIEW.zip")
        assert _brm._is_packaging_output("remedy-review-20260101-000000-READY_FOR_REVIEW.zip.sha256")

    def test_source_lookalike_is_not_output(self):
        assert not _brm._is_packaging_output("remedy-review-notes.py")
        assert not _brm._is_packaging_output("scripts/build_review_zip.py")
        assert not _brm._is_packaging_output("review_zip_manifest.json")   # no leading dot


class TestClassification:
    def test_clean_branch_with_only_outputs_stays_clean(self):
        r = _brm._classify_review_subject(
            "feature/x", "abc123def456",
            ["?? .review_zip_manifest.json",
             "?? remedy-review-20260101-000000-READY_FOR_REVIEW.zip",
             "?? remedy-review-20260101-000000-READY_FOR_REVIEW.zip.sha256"],
            True, True)
        assert r["kind"] == "feature_branch"
        assert r["dirty_files"] == []
        assert len(r["packaging_generated_outputs"]) == 3

    def test_real_dirty_file_still_dirty(self):
        r = _brm._classify_review_subject(
            "feature/x", "abc", [" M scripts/app.py", "?? .review_zip_manifest.json"], True, True)
        assert r["kind"] == "dirty_working_tree"
        assert r["dirty_files"] == [" M scripts/app.py"]
        assert r["packaging_generated_outputs"] == [".review_zip_manifest.json"]

    def test_source_lookalike_stays_dirty(self):
        r = _brm._classify_review_subject("feature/x", "abc", ["?? remedy-review-notes.py"], True, True)
        assert r["kind"] == "dirty_working_tree"
        assert r["dirty_files"] == ["?? remedy-review-notes.py"]
        assert r["packaging_generated_outputs"] == []

    def test_renamed_line_path_extracted(self):
        assert _brm._dirty_line_path("R  old.py -> new.py") == "new.py"


class TestExactRootOnlyGrammar:
    """F4 (round 27) — only the current run's EXACT repository-root generated outputs are classified;
    a nested file or a lookalike name is an ordinary repository file and stays in the dirty subject."""

    def test_current_root_outputs_are_generated(self):
        assert _brm._is_packaging_output(
            "remedy-review-20260718-213237-READY_FOR_REVIEW.zip")
        assert _brm._is_packaging_output(
            "remedy-review-20260718-213237-READY_FOR_REVIEW.zip.sha256")
        assert _brm._is_packaging_output(".review_zip_manifest.json")

    def test_nested_and_lookalike_stay_dirty(self):
        for p in ("tests/fixtures/remedy-review-corpus.zip",
                  "tests/remedy-review-20260718-213237-READY_FOR_REVIEW.zip",
                  "docs/.review_zip_manifest.json",
                  "nested/remedy-review-20260718-213237-READY_FOR_REVIEW.zip.sha256",
                  "remedy-review-schema.zip",
                  "remedy-review-foo-READY_FOR_REVIEW.zip"):
            assert not _brm._is_packaging_output(p), p

    def test_dirty_partition_keeps_nested_lookalikes(self):
        dirty = [
            "?? tests/fixtures/remedy-review-corpus.zip",
            "?? remedy-review-schema.zip",
            " M docs/.review_zip_manifest.json",
            "?? remedy-review-20260718-213237-READY_FOR_REVIEW.zip",  # the only real output
            "?? .review_zip_manifest.json",
        ]
        r = _brm._classify_review_subject("feature/x", "abc", dirty, True, True)
        assert r["kind"] == "dirty_working_tree"
        assert sorted(_brm._dirty_line_path(x) for x in r["dirty_files"]) == sorted([
            "tests/fixtures/remedy-review-corpus.zip", "remedy-review-schema.zip",
            "docs/.review_zip_manifest.json"])
        assert sorted(r["packaging_generated_outputs"]) == sorted([
            ".review_zip_manifest.json",
            "remedy-review-20260718-213237-READY_FOR_REVIEW.zip"])
