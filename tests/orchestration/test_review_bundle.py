"""Tests for Review Bundle v1 — safe state package for reviewers.

Covers:
- Step 977: ReviewBundleResult, ReviewBundleSection, BundleSafetyReport models
- Step 978-983: Section builders (job summary, events, changed files, repair, context, trust, proof)
- Step 985: Review zip script hygiene
- Step 986: Bundle safety (no raw content, no caches, no secrets)
- Step 988: Bundle determinism (stable section names, repeatable)
"""

from __future__ import annotations

import json
import os
import zipfile
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_job(tmp_path):
    """Create minimal job in tmp data dir."""
    data_dir = tmp_path / "data"
    data_dir.mkdir(exist_ok=True)
    old = os.environ.get("REMEDY_DATA_DIR")
    os.environ["REMEDY_DATA_DIR"] = str(data_dir)

    from packages.core.models import Job, Task
    from packages.orchestration.storage import save_job

    job = Job(name="bundle-test-job", user_prompt="test bundle generation")
    task = Task(description="initial task")
    job.tasks = [task]
    save_job(job)
    return job, task, data_dir, old


def _make_job_with_failure(tmp_path):
    """Create job with failure artifact and repair loop result."""
    job, task, data_dir, old = _make_job(tmp_path)
    from packages.orchestration.test_failure_artifact import (
        TestFailureArtifact,
        persist_failure_artifact,
    )
    from packages.orchestration.repair_loop import start_repair_loop_v0

    failure = TestFailureArtifact(
        artifact_id="temp",
        job_id=str(job.id),
        task_id=str(task.id),
        failure_kind="test_failed",
        safe_summary="3 tests failed in test_example.py",
    )
    art = persist_failure_artifact(job, failure)
    result = start_repair_loop_v0(
        str(job.id), str(art.id), create_patch_intent=True,
    )
    return job, result, data_dir, old


def _cleanup_env(old):
    if old:
        os.environ["REMEDY_DATA_DIR"] = old
    else:
        os.environ.pop("REMEDY_DATA_DIR", None)


# ---------------------------------------------------------------------------
# Step 977: Model tests
# ---------------------------------------------------------------------------


class TestReviewBundleModel:

    def test_result_defaults(self):
        from packages.orchestration.review_bundle import ReviewBundleResult
        r = ReviewBundleResult()
        assert r.bundle_version == 1
        assert r.sections == []
        assert r.safety.is_safe

    def test_section_defaults(self):
        from packages.orchestration.review_bundle import ReviewBundleSection
        s = ReviewBundleSection("test.json")
        assert s.status == "included"
        assert s.byte_count == 0

    def test_safety_report_flags(self):
        from packages.orchestration.review_bundle import BundleSafetyReport
        s = BundleSafetyReport()
        assert s.is_safe
        s.has_raw_artifacts = True
        assert not s.is_safe

    def test_changed_file_safe(self):
        from packages.orchestration.review_bundle import ChangedFileSafe
        f = ChangedFileSafe(path="src/main.py", status="modified")
        assert f.path == "src/main.py"
        assert f.tested_after_change is False

    def test_manifest_defaults(self):
        from packages.orchestration.review_bundle import ReviewBundleManifest
        m = ReviewBundleManifest(job_id="abc")
        assert m.bundle_version == 1
        assert m.included_sections == []

    def test_required_sections_defined(self):
        from packages.orchestration.review_bundle import REQUIRED_SECTIONS
        assert len(REQUIRED_SECTIONS) == 10
        assert "manifest.json" in REQUIRED_SECTIONS
        assert "bundle_readme.md" in REQUIRED_SECTIONS


# ---------------------------------------------------------------------------
# Step 978-983: Section builder tests
# ---------------------------------------------------------------------------


class TestBuildReviewBundle:

    def test_basic_bundle_builds(self, tmp_path):
        from packages.orchestration.review_bundle import build_review_bundle
        job, task, data_dir, old = _make_job(tmp_path)
        try:
            result = build_review_bundle(str(job.id))
            assert not result.error
            assert result.file_count >= 8
            assert result.byte_count > 0
            assert Path(result.output_path).exists()
        finally:
            _cleanup_env(old)

    def test_bundle_with_repair_data(self, tmp_path):
        from packages.orchestration.review_bundle import build_review_bundle
        job, repair_result, data_dir, old = _make_job_with_failure(tmp_path)
        try:
            result = build_review_bundle(str(job.id))
            assert not result.error
            assert result.file_count >= 8
        finally:
            _cleanup_env(old)

    def test_bundle_output_is_zip(self, tmp_path):
        from packages.orchestration.review_bundle import build_review_bundle
        job, task, data_dir, old = _make_job(tmp_path)
        try:
            result = build_review_bundle(str(job.id))
            assert result.output_path.endswith(".zip")
            assert zipfile.is_zipfile(result.output_path)
        finally:
            _cleanup_env(old)

    def test_bundle_custom_output_path(self, tmp_path):
        from packages.orchestration.review_bundle import build_review_bundle
        job, task, data_dir, old = _make_job(tmp_path)
        custom_path = str(tmp_path / "custom-bundle.zip")
        try:
            result = build_review_bundle(str(job.id), output_path=custom_path)
            assert not result.error
            assert result.output_path == custom_path
            assert Path(custom_path).exists()
        finally:
            _cleanup_env(old)

    def test_bundle_job_not_found(self, tmp_path):
        from packages.orchestration.review_bundle import build_review_bundle
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        old = os.environ.get("REMEDY_DATA_DIR")
        os.environ["REMEDY_DATA_DIR"] = str(data_dir)
        try:
            result = build_review_bundle("00000000-0000-0000-0000-000000000000")
            assert result.error
            assert "not found" in result.error.lower()
        finally:
            _cleanup_env(old)

    def test_bundle_unsafe_output_path(self, tmp_path):
        from packages.orchestration.review_bundle import build_review_bundle
        job, task, data_dir, old = _make_job(tmp_path)
        try:
            result = build_review_bundle(str(job.id), output_path="../../../etc/evil.zip")
            assert result.error
            assert "traversal" in result.error.lower() or "unsafe" in result.error.lower()
        finally:
            _cleanup_env(old)


# ---------------------------------------------------------------------------
# Step 986: Bundle safety tests
# ---------------------------------------------------------------------------


class TestBundleSafety:

    def test_bundle_contains_required_sections(self, tmp_path):
        from packages.orchestration.review_bundle import build_review_bundle, REQUIRED_SECTIONS
        job, task, data_dir, old = _make_job(tmp_path)
        try:
            result = build_review_bundle(str(job.id))
            with zipfile.ZipFile(result.output_path) as zf:
                names = set(zf.namelist())
                for section in REQUIRED_SECTIONS:
                    assert section in names, f"Missing required section: {section}"
        finally:
            _cleanup_env(old)

    def test_bundle_excludes_raw_artifact_body(self, tmp_path):
        from packages.orchestration.review_bundle import build_review_bundle
        job, repair_result, data_dir, old = _make_job_with_failure(tmp_path)
        try:
            result = build_review_bundle(str(job.id))
            with zipfile.ZipFile(result.output_path) as zf:
                for name in zf.namelist():
                    content = zf.read(name).decode("utf-8", errors="replace")
                    assert "Traceback (most recent call last)" not in content, (
                        f"Raw traceback found in {name}"
                    )
        finally:
            _cleanup_env(old)

    def test_bundle_excludes_pycache(self, tmp_path):
        from packages.orchestration.review_bundle import build_review_bundle
        job, task, data_dir, old = _make_job(tmp_path)
        try:
            result = build_review_bundle(str(job.id))
            with zipfile.ZipFile(result.output_path) as zf:
                for name in zf.namelist():
                    assert "__pycache__" not in name
                    assert name.endswith(".pyc") is False
        finally:
            _cleanup_env(old)

    def test_bundle_excludes_env_files(self, tmp_path):
        from packages.orchestration.review_bundle import build_review_bundle
        job, task, data_dir, old = _make_job(tmp_path)
        try:
            result = build_review_bundle(str(job.id))
            with zipfile.ZipFile(result.output_path) as zf:
                for name in zf.namelist():
                    assert ".env" not in name
        finally:
            _cleanup_env(old)

    def test_bundle_excludes_data_dir(self, tmp_path):
        from packages.orchestration.review_bundle import build_review_bundle
        job, task, data_dir, old = _make_job(tmp_path)
        try:
            result = build_review_bundle(str(job.id))
            with zipfile.ZipFile(result.output_path) as zf:
                for name in zf.namelist():
                    assert not name.startswith(".data/")
                    assert not name.startswith(".git/")
        finally:
            _cleanup_env(old)

    def test_bundle_no_source_file_contents(self, tmp_path):
        from packages.orchestration.review_bundle import build_review_bundle
        job, task, data_dir, old = _make_job(tmp_path)
        try:
            result = build_review_bundle(str(job.id))
            with zipfile.ZipFile(result.output_path) as zf:
                for name in zf.namelist():
                    assert not name.endswith(".py"), f"Source file {name} in bundle"
                    assert not name.endswith(".ts"), f"Source file {name} in bundle"
                    assert not name.endswith(".js"), f"Source file {name} in bundle"
        finally:
            _cleanup_env(old)

    def test_bundle_json_sections_parse(self, tmp_path):
        from packages.orchestration.review_bundle import build_review_bundle
        job, task, data_dir, old = _make_job(tmp_path)
        try:
            result = build_review_bundle(str(job.id))
            with zipfile.ZipFile(result.output_path) as zf:
                for name in zf.namelist():
                    if name.endswith(".json"):
                        content = zf.read(name).decode("utf-8")
                        data = json.loads(content)
                        assert isinstance(data, (dict, list))
        finally:
            _cleanup_env(old)

    def test_safety_report_clean(self, tmp_path):
        from packages.orchestration.review_bundle import build_review_bundle
        job, task, data_dir, old = _make_job(tmp_path)
        try:
            result = build_review_bundle(str(job.id))
            assert result.safety.is_safe
            assert not result.safety.has_raw_artifacts
            assert not result.safety.has_pycache
            assert not result.safety.has_env_files
        finally:
            _cleanup_env(old)


# ---------------------------------------------------------------------------
# Step 985: Review zip script hygiene
# ---------------------------------------------------------------------------


class TestReviewZipHygiene:

    def test_make_review_zip_excludes_pycache(self):
        script = Path("scripts/make_review_zip.sh")
        if not script.exists():
            pytest.skip("make_review_zip.sh not found")
        text = script.read_text()
        assert "__pycache__" in text, "Script should exclude __pycache__"
        assert "*.pyc" in text, "Script should exclude *.pyc"

    def test_make_review_zip_excludes_data(self):
        script = Path("scripts/make_review_zip.sh")
        if not script.exists():
            pytest.skip("make_review_zip.sh not found")
        text = script.read_text()
        assert ".data" in text

    def test_make_review_zip_excludes_secrets(self):
        script = Path("scripts/make_review_zip.sh")
        if not script.exists():
            pytest.skip("make_review_zip.sh not found")
        text = script.read_text()
        assert ".env" in text
        assert "secret" in text.lower()


# ---------------------------------------------------------------------------
# Step 988: Bundle determinism tests
# ---------------------------------------------------------------------------


class TestBundleDeterminism:

    def test_manifest_has_stable_keys(self, tmp_path):
        from packages.orchestration.review_bundle import build_review_bundle
        job, task, data_dir, old = _make_job(tmp_path)
        try:
            result = build_review_bundle(str(job.id))
            with zipfile.ZipFile(result.output_path) as zf:
                manifest = json.loads(zf.read("manifest.json"))
                assert "bundle_version" in manifest
                assert "job_id" in manifest
                assert "generated_at" in manifest
                assert "included_sections" in manifest
        finally:
            _cleanup_env(old)

    def test_section_filenames_stable(self, tmp_path):
        from packages.orchestration.review_bundle import build_review_bundle, REQUIRED_SECTIONS
        job, task, data_dir, old = _make_job(tmp_path)
        try:
            result = build_review_bundle(str(job.id))
            section_names = [s.filename for s in result.sections]
            for req in REQUIRED_SECTIONS:
                assert req in section_names, f"Missing section: {req}"
        finally:
            _cleanup_env(old)

    def test_repeated_bundle_same_sections(self, tmp_path):
        from packages.orchestration.review_bundle import build_review_bundle
        job, task, data_dir, old = _make_job(tmp_path)
        try:
            out1 = str(tmp_path / "b1.zip")
            out2 = str(tmp_path / "b2.zip")
            r1 = build_review_bundle(str(job.id), output_path=out1)
            r2 = build_review_bundle(str(job.id), output_path=out2)
            names1 = sorted(s.filename for s in r1.sections)
            names2 = sorted(s.filename for s in r2.sections)
            assert names1 == names2
        finally:
            _cleanup_env(old)

    def test_no_random_filenames_in_zip(self, tmp_path):
        from packages.orchestration.review_bundle import build_review_bundle
        job, task, data_dir, old = _make_job(tmp_path)
        try:
            result = build_review_bundle(str(job.id))
            with zipfile.ZipFile(result.output_path) as zf:
                for name in zf.namelist():
                    assert len(name) < 100, f"Suspiciously long filename: {name}"
                    assert name.endswith(".json") or name.endswith(".md"), (
                        f"Unexpected file type: {name}"
                    )
        finally:
            _cleanup_env(old)


# ---------------------------------------------------------------------------
# Export / summary tests
# ---------------------------------------------------------------------------


class TestBundleExport:

    def test_export_json(self, tmp_path):
        from packages.orchestration.review_bundle import (
            build_review_bundle,
            export_review_bundle_json,
        )
        job, task, data_dir, old = _make_job(tmp_path)
        try:
            result = build_review_bundle(str(job.id))
            data = export_review_bundle_json(result)
            assert data["bundle_version"] == 1
            assert data["job_id"] == str(job.id)
            assert data["file_count"] >= 8
            assert data["safety"]["is_safe"]
            text = json.dumps(data)
            assert "Traceback" not in text
        finally:
            _cleanup_env(old)

    def test_summarize(self, tmp_path):
        from packages.orchestration.review_bundle import (
            build_review_bundle,
            summarize_review_bundle,
        )
        job, task, data_dir, old = _make_job(tmp_path)
        try:
            result = build_review_bundle(str(job.id))
            text = summarize_review_bundle(result)
            assert "Review Bundle" in text
            assert "Sections" in text
        finally:
            _cleanup_env(old)
