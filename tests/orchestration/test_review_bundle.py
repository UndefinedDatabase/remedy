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
    from packages.orchestration.repair_loop import start_repair_loop_v0
    from packages.orchestration.test_failure_artifact import (
        TestFailureArtifact,
        persist_failure_artifact,
    )

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
        assert f.snapshot_verified is False

    def test_changed_file_safe_snapshot_verified_field(self):
        """snapshot_verified is safe bool only — no blob content (Step 1149)."""
        from packages.orchestration.review_bundle import ChangedFileSafe
        f = ChangedFileSafe(path="src/main.py", status="modified", snapshot_verified=True)
        assert f.snapshot_verified is True

    def test_manifest_defaults(self):
        from packages.orchestration.review_bundle import ReviewBundleManifest
        m = ReviewBundleManifest(job_id="abc")
        assert m.bundle_version == 1
        assert m.included_sections == []

    def test_required_sections_defined(self):
        from packages.orchestration.review_bundle import REQUIRED_SECTIONS
        assert len(REQUIRED_SECTIONS) == 40
        assert "repair_loop_summary.json" in REQUIRED_SECTIONS
        assert "main_builder_adapter_summary.json" in REQUIRED_SECTIONS
        assert "config_summary.json" in REQUIRED_SECTIONS
        assert "managed_execution_summary.json" in REQUIRED_SECTIONS
        assert "snapshot_rollback_summary.json" in REQUIRED_SECTIONS
        assert "overnight_mission_summary.json" in REQUIRED_SECTIONS
        assert "model_route_tournament_summary.json" in REQUIRED_SECTIONS
        assert "token_economy_summary.json" in REQUIRED_SECTIONS
        assert "local_advisor_summary.json" in REQUIRED_SECTIONS
        assert "provider_verification_summary.json" in REQUIRED_SECTIONS
        assert "builder_routing_summary.json" in REQUIRED_SECTIONS
        assert "local_candidate_summary.json" in REQUIRED_SECTIONS
        assert "candidate_quality_summary.json" in REQUIRED_SECTIONS
        assert "external_builder_summary.json" in REQUIRED_SECTIONS
        assert "worker_registry_summary.json" in REQUIRED_SECTIONS
        assert "manifest.json" in REQUIRED_SECTIONS
        assert "snapshot_summary.json" in REQUIRED_SECTIONS
        assert "continuation_summary.json" in REQUIRED_SECTIONS
        assert "overnight_readiness_summary.json" in REQUIRED_SECTIONS
        assert "overnight_run_summary.json" in REQUIRED_SECTIONS
        assert "provider_trust_summary.json" in REQUIRED_SECTIONS
        assert "provider_material_summary.json" in REQUIRED_SECTIONS
        assert "repair_request_summary.json" in REQUIRED_SECTIONS
        assert "self_dogfood_summary.json" in REQUIRED_SECTIONS
        assert "self_execution_summary.json" in REQUIRED_SECTIONS
        assert "orchestrator_decision_summary.json" in REQUIRED_SECTIONS
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
        from packages.orchestration.review_bundle import REQUIRED_SECTIONS, build_review_bundle
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
        from packages.orchestration.review_bundle import REQUIRED_SECTIONS, build_review_bundle
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


# ---------------------------------------------------------------------------
# Step 996: Prompt redaction tests
# ---------------------------------------------------------------------------


class TestPromptRedaction:

    def test_secret_prompt_not_in_bundle(self, tmp_path):
        """Job with secret in prompt — secret must not appear in zip."""
        from packages.orchestration.review_bundle import build_review_bundle
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        old = os.environ.get("REMEDY_DATA_DIR")
        os.environ["REMEDY_DATA_DIR"] = str(data_dir)
        try:
            from packages.core.models import Job, Task
            from packages.orchestration.storage import save_job
            job = Job(name="secret-test", user_prompt="Use API key sk-test-secret-123456 to call endpoint")
            job.tasks = [Task(description="test")]
            save_job(job)

            result = build_review_bundle(str(job.id))
            assert not result.error
            with zipfile.ZipFile(result.output_path) as zf:
                for name in zf.namelist():
                    content = zf.read(name).decode("utf-8", errors="replace")
                    assert "sk-test-secret-123456" not in content, f"Secret in {name}"
        finally:
            _cleanup_env(old)

    def test_password_prompt_not_in_bundle(self, tmp_path):
        from packages.orchestration.review_bundle import build_review_bundle
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        old = os.environ.get("REMEDY_DATA_DIR")
        os.environ["REMEDY_DATA_DIR"] = str(data_dir)
        try:
            from packages.core.models import Job, Task
            from packages.orchestration.storage import save_job
            job = Job(name="pw-test", user_prompt="Set password=hunter2 in config")
            job.tasks = [Task(description="test")]
            save_job(job)

            result = build_review_bundle(str(job.id))
            with zipfile.ZipFile(result.output_path) as zf:
                for name in zf.namelist():
                    content = zf.read(name).decode("utf-8", errors="replace")
                    assert "password=hunter2" not in content, f"Password in {name}"
        finally:
            _cleanup_env(old)

    def test_normal_prompt_has_safe_summary(self, tmp_path):
        from packages.orchestration.review_bundle import build_review_bundle
        job, task, data_dir, old = _make_job(tmp_path)
        try:
            result = build_review_bundle(str(job.id))
            with zipfile.ZipFile(result.output_path) as zf:
                js = json.loads(zf.read("job_summary.json"))
                assert js["user_prompt_present"] is True
                assert js["user_prompt_length"] > 0
                assert js["user_prompt_redacted"] is False
                assert js["user_prompt_safe_summary"] is not None
                assert "user_prompt_preview" not in js
        finally:
            _cleanup_env(old)

    def test_secret_prompt_flags_redacted(self, tmp_path):
        from packages.orchestration.review_bundle import build_review_bundle
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        old = os.environ.get("REMEDY_DATA_DIR")
        os.environ["REMEDY_DATA_DIR"] = str(data_dir)
        try:
            from packages.core.models import Job, Task
            from packages.orchestration.storage import save_job
            job = Job(name="redact-test", user_prompt="key is ghp_abcdef12345678901234")
            job.tasks = [Task(description="test")]
            save_job(job)

            result = build_review_bundle(str(job.id))
            with zipfile.ZipFile(result.output_path) as zf:
                js = json.loads(zf.read("job_summary.json"))
                assert js["user_prompt_redacted"] is True
                assert js["user_prompt_safe_summary"] is None
        finally:
            _cleanup_env(old)


# ---------------------------------------------------------------------------
# Step 997: Redact safe text unit tests
# ---------------------------------------------------------------------------


class TestRedactSafeText:

    def test_clean_text_unchanged(self):
        from packages.orchestration.review_bundle import redact_safe_text
        text, count = redact_safe_text("Build a REST API", max_len=200)
        assert text == "Build a REST API"
        assert count == 0

    def test_api_key_redacted(self):
        from packages.orchestration.review_bundle import redact_safe_text
        text, count = redact_safe_text("key is sk-test12345678", max_len=200)
        assert "sk-test12345678" not in text
        assert "[REDACTED]" in text
        assert count >= 1

    def test_github_pat_redacted(self):
        from packages.orchestration.review_bundle import redact_safe_text
        text, count = redact_safe_text("token ghp_abcdef12345678901234", max_len=200)
        assert "ghp_abcdef" not in text
        assert count >= 1

    def test_password_assignment_redacted(self):
        from packages.orchestration.review_bundle import redact_safe_text
        text, count = redact_safe_text("password= hunter2", max_len=200)
        assert "password=" not in text
        assert count >= 1

    def test_bounded_length(self):
        from packages.orchestration.review_bundle import redact_safe_text
        text, count = redact_safe_text("a" * 500, max_len=100)
        assert len(text) <= 104  # 100 + "..."

    def test_slack_token_redacted(self):
        from packages.orchestration.review_bundle import redact_safe_text
        text, count = redact_safe_text("xoxb-123456-abcdef", max_len=200)
        assert "xoxb-" not in text
        assert count >= 1


# ---------------------------------------------------------------------------
# Step 998: Protected path filtering tests
# ---------------------------------------------------------------------------


class TestProtectedPathFiltering:

    def test_env_secret_not_in_bundle(self, tmp_path):
        """Patch intent targeting .env.secret must not appear in bundle."""
        from packages.orchestration.review_bundle import build_review_bundle
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        old = os.environ.get("REMEDY_DATA_DIR")
        os.environ["REMEDY_DATA_DIR"] = str(data_dir)
        try:
            from packages.core.models import Artifact, ArtifactKind, Job, Task
            from packages.orchestration.storage import save_job
            job = Job(name="path-test", user_prompt="test")
            task = Task(description="test")
            job.tasks = [task]
            art = Artifact(
                name="patch",
                content="patch",
                kind=ArtifactKind.BUILDER_PROPOSAL,
                task_id=task.id,
                metadata={
                    "patch_intent_explanations": [
                        {"file": ".env.secret", "action": "modify", "risk": "high",
                         "reason": "update", "summary": "update secret"},
                        {"file": "src/main.py", "action": "modify", "risk": "low",
                         "reason": "fix", "summary": "fix bug"},
                    ],
                    "patch_intent_approvals": {},
                },
            )
            job.artifacts.append(art)
            save_job(job)

            result = build_review_bundle(str(job.id))
            with zipfile.ZipFile(result.output_path) as zf:
                for name in zf.namelist():
                    content = zf.read(name).decode("utf-8", errors="replace")
                    assert ".env.secret" not in content, f".env.secret found in {name}"
                # Safe path still present
                cf = json.loads(zf.read("changed_files_safe.json"))
                paths = [f["path"] for f in cf["files"]]
                assert "src/main.py" in paths
                assert cf["redacted_protected_path_count"] >= 1
        finally:
            _cleanup_env(old)

    def test_credentials_json_not_in_bundle(self, tmp_path):
        from packages.orchestration.review_bundle import build_review_bundle
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        old = os.environ.get("REMEDY_DATA_DIR")
        os.environ["REMEDY_DATA_DIR"] = str(data_dir)
        try:
            from packages.core.models import Artifact, ArtifactKind, Job, Task
            from packages.orchestration.storage import save_job
            job = Job(name="cred-test", user_prompt="test")
            task = Task(description="test")
            job.tasks = [task]
            art = Artifact(
                name="patch",
                content="patch",
                kind=ArtifactKind.BUILDER_PROPOSAL,
                task_id=task.id,
                metadata={
                    "patch_intent_explanations": [
                        {"file": "credentials.json", "action": "create", "risk": "high",
                         "reason": "setup", "summary": "add creds"},
                    ],
                    "patch_intent_approvals": {},
                },
            )
            job.artifacts.append(art)
            save_job(job)

            result = build_review_bundle(str(job.id))
            with zipfile.ZipFile(result.output_path) as zf:
                for name in zf.namelist():
                    content = zf.read(name).decode("utf-8", errors="replace")
                    assert "credentials.json" not in content, f"credentials.json found in {name}"
        finally:
            _cleanup_env(old)

    def test_is_protected_path(self):
        from packages.orchestration.review_bundle import _is_protected_path
        assert _is_protected_path(".env") is True
        assert _is_protected_path(".env.secret") is True
        assert _is_protected_path(".env.staging") is True
        assert _is_protected_path("config/.env.local") is True
        assert _is_protected_path("credentials.json") is True
        assert _is_protected_path("node_modules/foo.js") is True
        assert _is_protected_path("__pycache__/mod.pyc") is True
        assert _is_protected_path(".git/config") is True
        assert _is_protected_path("src/main.py") is False
        assert _is_protected_path("docs/README.md") is False


# ---------------------------------------------------------------------------
# Step 999: Strong safety audit tests
# ---------------------------------------------------------------------------


class TestStrongSafetyAudit:

    def test_secret_in_prompt_flips_safety(self, tmp_path):
        """Bundle with secret prompt must have safety.is_safe=False if secret leaks."""
        from packages.orchestration.review_bundle import build_review_bundle
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        old = os.environ.get("REMEDY_DATA_DIR")
        os.environ["REMEDY_DATA_DIR"] = str(data_dir)
        try:
            from packages.core.models import Job, Task
            from packages.orchestration.storage import save_job
            # The prompt secret should be redacted, so safety should stay safe
            job = Job(name="audit-test", user_prompt="sk-realkey12345678901234")
            job.tasks = [Task(description="test")]
            save_job(job)

            result = build_review_bundle(str(job.id))
            # Since we redact the prompt, the bundle should still be safe
            # But verify the secret is not in the zip
            with zipfile.ZipFile(result.output_path) as zf:
                for name in zf.namelist():
                    content = zf.read(name).decode("utf-8", errors="replace")
                    assert "sk-realkey12345678901234" not in content
        finally:
            _cleanup_env(old)

    def test_clean_bundle_is_safe(self, tmp_path):
        from packages.orchestration.review_bundle import build_review_bundle
        job, task, data_dir, old = _make_job(tmp_path)
        try:
            result = build_review_bundle(str(job.id))
            assert result.safety.is_safe
            assert not result.safety.has_secrets
            assert not result.safety.has_raw_output
            assert not result.safety.has_pycache
            assert not result.safety.has_env_files
            assert not result.safety.has_raw_diffs
        finally:
            _cleanup_env(old)


# ---------------------------------------------------------------------------
# Step 1000: Output path safety tests
# ---------------------------------------------------------------------------


class TestOutputPathSafety:

    def test_traversal_rejected(self):
        from packages.orchestration.review_bundle import _is_safe_output_path
        assert _is_safe_output_path("../evil.zip") is False
        assert _is_safe_output_path("/tmp/../../etc/evil.zip") is False

    def test_double_dot_in_filename_allowed(self):
        from packages.orchestration.review_bundle import _is_safe_output_path
        assert _is_safe_output_path("bundle..review.zip") is True
        assert _is_safe_output_path("/tmp/my..file.zip") is True

    def test_git_dir_rejected(self):
        from packages.orchestration.review_bundle import _is_safe_output_path
        assert _is_safe_output_path(".git/out.zip") is False

    def test_env_dir_rejected(self):
        from packages.orchestration.review_bundle import _is_safe_output_path
        assert _is_safe_output_path(".env/out.zip") is False
        assert _is_safe_output_path(".env.local/out.zip") is False

    def test_safe_paths_allowed(self):
        from packages.orchestration.review_bundle import _is_safe_output_path
        assert _is_safe_output_path("/tmp/bundle.zip") is True
        assert _is_safe_output_path("output/review.zip") is True


# ---------------------------------------------------------------------------
# Step 1001: Section availability truth tests
# ---------------------------------------------------------------------------


class TestSectionAvailability:

    def test_failed_section_in_manifest(self, tmp_path):
        """Monkeypatch a builder to fail — manifest should show skipped."""
        from packages.orchestration.review_bundle import (
            _REVIEW_BUNDLE_SECTION_SPECS,
            build_review_bundle,
        )

        def _fail(*a, **kw):
            raise RuntimeError("simulated failure")

        proof_spec = next(s for s in _REVIEW_BUNDLE_SECTION_SPECS if s.filename == "proof_chains.json")
        original_builder = proof_spec.builder

        job, task, data_dir, old = _make_job(tmp_path)
        try:
            proof_spec.builder = _fail
            result = build_review_bundle(str(job.id))
            assert not result.error

            with zipfile.ZipFile(result.output_path) as zf:
                manifest = json.loads(zf.read("manifest.json"))
                assert "proof_chains.json" in manifest["skipped_sections"]

            proof_section = next(
                (s for s in result.sections if s.filename == "proof_chains.json"), None
            )
            assert proof_section is not None
            assert proof_section.status == "degraded"
        finally:
            proof_spec.builder = original_builder
            _cleanup_env(old)

    def test_bundle_still_safe_with_failed_section(self, tmp_path):
        from packages.orchestration.review_bundle import (
            _REVIEW_BUNDLE_SECTION_SPECS,
            build_review_bundle,
        )

        def _fail(*a, **kw):
            raise RuntimeError("simulated failure")

        ctx_spec = next(s for s in _REVIEW_BUNDLE_SECTION_SPECS if s.filename == "context_inspection.json")
        original_builder = ctx_spec.builder

        job, task, data_dir, old = _make_job(tmp_path)
        try:
            ctx_spec.builder = _fail
            result = build_review_bundle(str(job.id))
            assert result.safety.is_safe
            assert Path(result.output_path).exists()
        finally:
            ctx_spec.builder = original_builder
            _cleanup_env(old)


# ---------------------------------------------------------------------------
# Step 1149: Snapshot integration in changed_files_safe
# ---------------------------------------------------------------------------


class TestSnapshotIntegration:
    """Review bundle surfaces snapshot_verified in changed_files_safe (Step 1149)."""

    def test_snapshot_verified_in_changed_files(self, tmp_path):
        """snapshot_verified=True from apply record appears in changed_files output."""
        from packages.core.models import Artifact, ArtifactKind
        from packages.orchestration.approval_queue import make_intent_id
        from packages.orchestration.review_bundle import _build_changed_files_safe

        job, task, data_dir, old = _make_job(tmp_path)
        try:
            art = Artifact(
                name="patch", content="", kind=ArtifactKind.PATCH_INTENT, task_id=task.id,
                metadata={
                    "patch_intent_explanations": [
                        {"file": "src/main.py", "action": "modify", "risk": "low",
                         "reason": "", "summary": ""}
                    ],
                    "patch_intent_approvals": {},
                },
            )
            iid = make_intent_id(art.id, 0)
            art.metadata["patch_intent_apply_records"] = {
                iid: {"state": "applied", "snapshot_verified": True}
            }
            job.artifacts.append(art)
            result = _build_changed_files_safe(job, [])
            file_entry = next((f for f in result["files"] if f["path"] == "src/main.py"), None)
            assert file_entry is not None
            assert file_entry["snapshot_verified"] is True
        finally:
            _cleanup_env(old)

    def test_unverified_snapshot_in_changed_files(self, tmp_path):
        """snapshot_verified=False when no apply record exists."""
        from packages.core.models import Artifact, ArtifactKind
        from packages.orchestration.review_bundle import _build_changed_files_safe

        job, task, data_dir, old = _make_job(tmp_path)
        try:
            art = Artifact(
                name="patch", content="", kind=ArtifactKind.PATCH_INTENT, task_id=task.id,
                metadata={
                    "patch_intent_explanations": [
                        {"file": "src/lib.py", "action": "modify", "risk": "low",
                         "reason": "", "summary": ""}
                    ],
                    "patch_intent_approvals": {},
                },
            )
            job.artifacts.append(art)
            result = _build_changed_files_safe(job, [])
            file_entry = next((f for f in result["files"] if f["path"] == "src/lib.py"), None)
            assert file_entry is not None
            assert file_entry["snapshot_verified"] is False
        finally:
            _cleanup_env(old)

    def test_no_blob_content_in_changed_files(self, tmp_path):
        """changed_files_safe output contains only safe metadata, no blob content (Step 1149)."""
        import json

        from packages.core.models import Artifact, ArtifactKind
        from packages.orchestration.approval_queue import make_intent_id
        from packages.orchestration.review_bundle import _build_changed_files_safe

        job, task, data_dir, old = _make_job(tmp_path)
        try:
            art = Artifact(
                name="patch", content="", kind=ArtifactKind.PATCH_INTENT, task_id=task.id,
                metadata={
                    "patch_intent_explanations": [
                        {"file": "src/safe.py", "action": "create", "risk": "low",
                         "reason": "", "summary": ""}
                    ],
                    "patch_intent_approvals": {},
                },
            )
            iid = make_intent_id(art.id, 0)
            art.metadata["patch_intent_apply_records"] = {
                iid: {"state": "applied", "snapshot_verified": True}
            }
            job.artifacts.append(art)
            result = _build_changed_files_safe(job, [])
            raw = json.dumps(result)
            for forbidden in ("blob_", "bin", "recovery", "traceback", "Traceback", "diff --git"):
                assert forbidden not in raw, f"Forbidden term in changed_files: {forbidden}"
        finally:
            _cleanup_env(old)


# ---------------------------------------------------------------------------
# Snapshot summary section (Step 1160)
# ---------------------------------------------------------------------------


class TestSnapshotSummarySection:
    """snapshot_summary.json — safe aggregate counts, no blobs/paths."""

    def _add_durable_snapshot(self, data_dir, job_id, *, state="applied"):
        from packages.orchestration.repository_snapshot import (
            DurableApplyRecord,
            create_snapshot,
            save_durable_apply_record,
            verify_snapshot,
        )
        repo = data_dir.parent / "repo"
        repo.mkdir(exist_ok=True)
        (repo / "f.py").write_text("before\n")
        snap = create_snapshot(job_id, "intent-1", ["f.py"], repo, data_dir)
        verify_snapshot(snap.snapshot_id, job_id, data_dir)
        rec = DurableApplyRecord(
            apply_id="apply-1", job_id=job_id, intent_id="intent-1",
            snapshot_id=snap.snapshot_id, state=state, target_paths=["f.py"],
            applied_at="2026-06-12T10:00:00+00:00",
            before_proof={}, after_proof={}, snapshot_verified=True,
        )
        save_durable_apply_record(rec, job_id, data_dir)
        return snap.snapshot_id

    def _read_section(self, zip_path, name):
        import json as _json
        import zipfile
        with zipfile.ZipFile(zip_path) as zf:
            return _json.loads(zf.read(name))

    def test_snapshot_summary_present_and_counted(self, tmp_path):
        from packages.orchestration.review_bundle import build_review_bundle
        job, task, data_dir, old = _make_job(tmp_path)
        try:
            self._add_durable_snapshot(data_dir, str(job.id))
            result = build_review_bundle(str(job.id))
            assert any(s.filename == "snapshot_summary.json" and s.status == "included"
                       for s in result.sections)
            summary = self._read_section(result.output_path, "snapshot_summary.json")
            assert summary["snapshot_count"] == 1
            assert summary["verified_count"] == 1
            assert summary["active_apply_count"] == 1
            assert summary["reverted_count"] == 0
        finally:
            _cleanup_env(old)

    def test_snapshot_summary_reverted(self, tmp_path):
        from packages.orchestration.review_bundle import build_review_bundle
        job, task, data_dir, old = _make_job(tmp_path)
        try:
            self._add_durable_snapshot(data_dir, str(job.id), state="reverted")
            result = build_review_bundle(str(job.id))
            summary = self._read_section(result.output_path, "snapshot_summary.json")
            assert summary["reverted_count"] == 1
            assert summary["active_apply_count"] == 0
        finally:
            _cleanup_env(old)

    def test_snapshot_summary_no_blob_or_path_leak(self, tmp_path):
        from packages.orchestration.review_bundle import build_review_bundle
        job, task, data_dir, old = _make_job(tmp_path)
        try:
            self._add_durable_snapshot(data_dir, str(job.id))
            result = build_review_bundle(str(job.id))
            import zipfile
            with zipfile.ZipFile(result.output_path) as zf:
                raw = zf.read("snapshot_summary.json").decode()
            assert "blob_" not in raw
            assert str(data_dir) not in raw
            assert "manifest.json" not in raw
            assert result.safety.is_safe
        finally:
            _cleanup_env(old)

    def test_snapshot_summary_empty_job(self, tmp_path):
        from packages.orchestration.review_bundle import build_review_bundle
        job, task, data_dir, old = _make_job(tmp_path)
        try:
            result = build_review_bundle(str(job.id))
            summary = self._read_section(result.output_path, "snapshot_summary.json")
            assert summary["snapshot_count"] == 0
            assert summary["applies"] == []
        finally:
            _cleanup_env(old)


# ---------------------------------------------------------------------------
# Steps 2296-2365: Structured error reporting tests
# ---------------------------------------------------------------------------


class TestStructuredErrorModel:
    """ReviewBundleSectionError serialization and redaction."""

    def test_section_error_to_dict(self):
        from packages.orchestration.review_bundle import ReviewBundleSectionError
        err = ReviewBundleSectionError(
            section_name="test.json",
            error_type="ValueError",
            error_category="validation_error",
            safe_message="bad input",
        )
        d = err.to_dict()
        assert d["section_name"] == "test.json"
        assert d["error_type"] == "ValueError"
        assert d["error_category"] == "validation_error"
        assert d["safe_message"] == "bad input"
        assert d["is_bug"] is False
        assert d["occurred_at"]

    def test_section_error_categories(self):
        from packages.orchestration.review_bundle import SECTION_ERROR_CATEGORIES
        assert "section_builder_error" in SECTION_ERROR_CATEGORIES
        assert "import_error" in SECTION_ERROR_CATEGORIES
        assert "io_error" in SECTION_ERROR_CATEGORIES
        assert "unknown_error" in SECTION_ERROR_CATEGORIES

    def test_categorize_import_error(self):
        from packages.orchestration.review_bundle import _categorize_exception
        assert _categorize_exception(ImportError("no module")) == "import_error"

    def test_categorize_value_error(self):
        from packages.orchestration.review_bundle import _categorize_exception
        assert _categorize_exception(ValueError("bad")) == "validation_error"

    def test_categorize_os_error(self):
        from packages.orchestration.review_bundle import _categorize_exception
        assert _categorize_exception(OSError("disk")) == "io_error"

    def test_categorize_permission_error(self):
        from packages.orchestration.review_bundle import _categorize_exception
        assert _categorize_exception(PermissionError("denied")) == "permission_error"

    def test_categorize_runtime_error(self):
        from packages.orchestration.review_bundle import _categorize_exception
        assert _categorize_exception(RuntimeError("boom")) == "section_builder_error"


class TestSafeExceptionMessage:
    """_safe_exception_message redaction and truncation."""

    def test_clean_message(self):
        from packages.orchestration.review_bundle import _safe_exception_message
        msg = _safe_exception_message(ValueError("missing field"))
        assert msg == "missing field"

    def test_secret_redacted(self):
        from packages.orchestration.review_bundle import _safe_exception_message
        msg = _safe_exception_message(RuntimeError("key sk-test12345678 invalid"))
        assert "sk-test12345678" not in msg
        assert "[REDACTED]" in msg

    def test_private_path_redacted(self):
        from packages.orchestration.review_bundle import _safe_exception_message
        msg = _safe_exception_message(FileNotFoundError("/home/user/secret/file.txt"))
        assert "/home/user" not in msg
        assert "[PRIVATE_PATH]" in msg

    def test_truncation(self):
        from packages.orchestration.review_bundle import _safe_exception_message
        msg = _safe_exception_message(RuntimeError("x" * 500))
        assert len(msg) <= 244  # 240 + "..."

    def test_empty_message(self):
        from packages.orchestration.review_bundle import _safe_exception_message
        msg = _safe_exception_message(RuntimeError(""))
        assert msg == ""

    def test_no_traceback(self):
        from packages.orchestration.review_bundle import _safe_exception_message
        try:
            raise ValueError("test error")
        except ValueError as exc:
            msg = _safe_exception_message(exc)
        assert "Traceback" not in msg
        assert "test error" in msg

    def test_exception_type_not_in_message(self):
        from packages.orchestration.review_bundle import _safe_exception_message
        msg = _safe_exception_message(ValueError("bad"))
        assert "ValueError" not in msg


class TestSectionRegistry:
    """_REVIEW_BUNDLE_SECTION_SPECS registry tests."""

    def test_spec_count_matches_required(self):
        from packages.orchestration.review_bundle import (
            _REVIEW_BUNDLE_SECTION_SPECS,
            REQUIRED_SECTIONS,
        )
        spec_filenames = {s.filename for s in _REVIEW_BUNDLE_SECTION_SPECS}
        required_filenames = set(REQUIRED_SECTIONS)
        non_generated = {"manifest.json", "bundle_readme.md"}
        assert spec_filenames == required_filenames - non_generated

    def test_deterministic_order(self):
        from packages.orchestration.review_bundle import _REVIEW_BUNDLE_SECTION_SPECS
        names = [s.filename for s in _REVIEW_BUNDLE_SECTION_SPECS]
        assert names == [s.filename for s in _REVIEW_BUNDLE_SECTION_SPECS]

    def test_all_specs_have_builders(self):
        from packages.orchestration.review_bundle import _REVIEW_BUNDLE_SECTION_SPECS
        for spec in _REVIEW_BUNDLE_SECTION_SPECS:
            assert callable(spec.builder), f"{spec.filename} has no callable builder"

    def test_all_specs_have_filenames(self):
        from packages.orchestration.review_bundle import _REVIEW_BUNDLE_SECTION_SPECS
        for spec in _REVIEW_BUNDLE_SECTION_SPECS:
            assert spec.filename.endswith(".json"), f"Non-JSON spec: {spec.filename}"


class TestBuildSectionSafe:
    """_build_section_safe wrapper tests."""

    def test_success_produces_included(self):
        from packages.orchestration.review_bundle import (
            ReviewBundleSectionSpec,
            _build_section_safe,
        )
        spec = ReviewBundleSectionSpec("test.json", lambda: {"ok": True})
        filename, content, section = _build_section_safe(spec, builder_args={})
        assert section.status == "included"
        assert content is not None
        assert b'"ok"' in content

    def test_failure_produces_degraded(self):
        from packages.orchestration.review_bundle import (
            ReviewBundleSectionSpec,
            _build_section_safe,
        )
        def _boom():
            raise RuntimeError("test boom")
        spec = ReviewBundleSectionSpec("test.json", _boom)
        filename, content, section = _build_section_safe(spec, builder_args={})
        assert section.status == "degraded"
        assert section.error_type == "RuntimeError"
        assert section.error_category == "section_builder_error"
        assert "test boom" in section.error_message
        assert content is not None
        data = json.loads(content)
        assert data["status"] == "degraded"
        assert data["error_type"] == "RuntimeError"

    def test_failure_no_traceback_in_content(self):
        from packages.orchestration.review_bundle import (
            ReviewBundleSectionSpec,
            _build_section_safe,
        )
        def _boom():
            raise ValueError("bad value")
        spec = ReviewBundleSectionSpec("test.json", _boom)
        _, content, _ = _build_section_safe(spec, builder_args={})
        assert b"Traceback" not in content

    def test_failure_no_secret_in_content(self):
        from packages.orchestration.review_bundle import (
            ReviewBundleSectionSpec,
            _build_section_safe,
        )
        def _boom():
            raise RuntimeError("key sk-secret12345678 failed")
        spec = ReviewBundleSectionSpec("test.json", _boom)
        _, content, _ = _build_section_safe(spec, builder_args={})
        assert b"sk-secret12345678" not in content

    def test_args_passed_to_builder(self):
        from packages.orchestration.review_bundle import (
            ReviewBundleSectionSpec,
            _build_section_safe,
        )
        def _builder(x, y):
            return {"sum": x + y}
        spec = ReviewBundleSectionSpec("test.json", _builder, args=("a", "b"))
        _, content, section = _build_section_safe(spec, builder_args={"a": 3, "b": 4})
        assert section.status == "included"
        data = json.loads(content)
        assert data["sum"] == 7

    def test_import_error_is_optional(self):
        from packages.orchestration.review_bundle import (
            ReviewBundleSectionSpec,
            _build_section_safe,
        )
        def _boom():
            raise ImportError("no module")
        spec = ReviewBundleSectionSpec("test.json", _boom)
        _, _, section = _build_section_safe(spec, builder_args={})
        assert section.error_category == "import_error"

    def test_log_warning_on_failure(self, caplog):
        import logging

        from packages.orchestration.review_bundle import (
            ReviewBundleSectionSpec,
            _build_section_safe,
        )
        def _boom():
            raise RuntimeError("logged failure")
        spec = ReviewBundleSectionSpec("logged.json", _boom)
        with caplog.at_level(logging.WARNING, logger="packages.orchestration.review_bundle"):
            _build_section_safe(spec, builder_args={})
        assert any("logged.json" in r.message and "logged failure" in r.message for r in caplog.records)


class TestDegradedSectionSummary:
    """Top-level degraded section count and summary fields."""

    def test_clean_bundle_zero_degraded(self, tmp_path):
        from packages.orchestration.review_bundle import build_review_bundle
        job, task, data_dir, old = _make_job(tmp_path)
        try:
            result = build_review_bundle(str(job.id))
            assert result.degraded_section_count == 0
            assert result.degraded_sections == []
            assert result.section_error_summary == []
            assert result.diagnostics_version == 1
        finally:
            _cleanup_env(old)

    def test_failed_section_increments_degraded(self, tmp_path):
        from packages.orchestration.review_bundle import (
            _REVIEW_BUNDLE_SECTION_SPECS,
            build_review_bundle,
        )
        def _fail(*a, **kw):
            raise RuntimeError("injected")
        proof_spec = next(s for s in _REVIEW_BUNDLE_SECTION_SPECS if s.filename == "proof_chains.json")
        original = proof_spec.builder
        job, task, data_dir, old = _make_job(tmp_path)
        try:
            proof_spec.builder = _fail
            result = build_review_bundle(str(job.id))
            assert result.degraded_section_count >= 1
            assert "proof_chains.json" in result.degraded_sections
            assert any(e["section_name"] == "proof_chains.json" for e in result.section_error_summary)
        finally:
            proof_spec.builder = original
            _cleanup_env(old)

    def test_export_json_includes_diagnostics(self, tmp_path):
        from packages.orchestration.review_bundle import (
            build_review_bundle,
            export_review_bundle_json,
        )
        job, task, data_dir, old = _make_job(tmp_path)
        try:
            result = build_review_bundle(str(job.id))
            data = export_review_bundle_json(result)
            assert data["diagnostics_version"] == 1
            assert data["degraded_section_count"] == 0
            assert data["degraded_sections"] == []
            assert data["section_error_summary"] == []
        finally:
            _cleanup_env(old)

    def test_manifest_includes_diagnostics(self, tmp_path):
        from packages.orchestration.review_bundle import build_review_bundle
        job, task, data_dir, old = _make_job(tmp_path)
        try:
            result = build_review_bundle(str(job.id))
            with zipfile.ZipFile(result.output_path) as zf:
                manifest = json.loads(zf.read("manifest.json"))
            assert manifest["diagnostics_version"] == 1
            assert manifest["degraded_section_count"] == 0
        finally:
            _cleanup_env(old)

    def test_degraded_section_in_zip_has_structured_data(self, tmp_path):
        from packages.orchestration.review_bundle import (
            _REVIEW_BUNDLE_SECTION_SPECS,
            build_review_bundle,
        )
        def _fail(*a, **kw):
            raise ValueError("bad data")
        event_spec = next(s for s in _REVIEW_BUNDLE_SECTION_SPECS if s.filename == "event_summary.json")
        original = event_spec.builder
        job, task, data_dir, old = _make_job(tmp_path)
        try:
            event_spec.builder = _fail
            result = build_review_bundle(str(job.id))
            with zipfile.ZipFile(result.output_path) as zf:
                data = json.loads(zf.read("event_summary.json"))
            assert data["status"] == "degraded"
            assert data["error_type"] == "ValueError"
            assert data["error_category"] == "validation_error"
            assert "bad data" in data["error_message"]
        finally:
            event_spec.builder = original
            _cleanup_env(old)

    def test_summarize_shows_degraded(self, tmp_path):
        from packages.orchestration.review_bundle import (
            _REVIEW_BUNDLE_SECTION_SPECS,
            build_review_bundle,
            summarize_review_bundle,
        )
        def _fail(*a, **kw):
            raise RuntimeError("broken")
        spec = next(s for s in _REVIEW_BUNDLE_SECTION_SPECS if s.filename == "command_summary.json")
        original = spec.builder
        job, task, data_dir, old = _make_job(tmp_path)
        try:
            spec.builder = _fail
            result = build_review_bundle(str(job.id))
            text = summarize_review_bundle(result)
            assert "Degraded sections: " in text
            assert "command_summary.json" in text
        finally:
            spec.builder = original
            _cleanup_env(old)
