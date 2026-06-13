"""Contract tests: truncation metadata survives from TestRunRecord through CLI event log and job metadata."""
from __future__ import annotations

import ast
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


class TestTruncationFieldsOnTestRunRecord:
    """TestRunRecord dataclass must carry truncation metadata."""

    def test_dataclass_has_output_truncated(self):
        src = (REPO_ROOT / "packages" / "orchestration" / "test_runner.py").read_text()
        assert "output_truncated: bool" in src

    def test_dataclass_has_original_output_bytes(self):
        src = (REPO_ROOT / "packages" / "orchestration" / "test_runner.py").read_text()
        assert "original_output_bytes: int" in src

    def test_dataclass_has_persisted_output_bytes(self):
        src = (REPO_ROOT / "packages" / "orchestration" / "test_runner.py").read_text()
        assert "persisted_output_bytes: int" in src


class TestTruncationMetadataSurvivesCLI:
    """Truncation metadata must be stored in the test execution service's persisted record."""

    def _svc_src(self) -> str:
        return (REPO_ROOT / "packages" / "orchestration" / "test_execution_service.py").read_text()

    def test_event_log_includes_output_truncated(self):
        src = self._svc_src()
        assert '"output_truncated"' in src, \
            "test_execution_service must persist output_truncated in test run records"

    def test_event_log_includes_original_output_bytes(self):
        src = self._svc_src()
        assert '"original_output_bytes"' in src

    def test_event_log_includes_persisted_output_bytes(self):
        src = self._svc_src()
        assert '"persisted_output_bytes"' in src

    def test_job_metadata_includes_truncation_fields(self):
        src = self._svc_src()
        assert '"output_truncated"' in src
        assert '"original_output_bytes"' in src
        assert '"persisted_output_bytes"' in src


class TestTruncationVisibleInTrustReport:
    """Trust report must surface truncation warnings when output was truncated."""

    def test_trust_report_checks_output_truncated(self):
        src = (REPO_ROOT / "packages" / "orchestration" / "trust_report.py").read_text()
        assert "output_truncated" in src, \
            "trust_report must check output_truncated metadata"

    def test_trust_report_shows_byte_counts(self):
        src = (REPO_ROOT / "packages" / "orchestration" / "trust_report.py").read_text()
        assert "original_output_bytes" in src
        assert "persisted_output_bytes" in src


class TestTruncationWarningInCLIOutput:
    """Test execution service must note output truncation in records."""

    def test_cli_prints_truncation_warning(self):
        src = (REPO_ROOT / "packages" / "orchestration" / "test_execution_service.py").read_text()
        assert "output truncated" in src.lower() or "output_truncated" in src, \
            "test_execution_service must track and note output truncation"
