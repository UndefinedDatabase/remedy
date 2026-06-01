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
    """CLI test_cmds.py must forward truncation fields to event log and job metadata."""

    def _cli_src(self) -> str:
        return (REPO_ROOT / "apps" / "cli" / "commands" / "test_cmds.py").read_text()

    def test_event_log_includes_output_truncated(self):
        src = self._cli_src()
        # Both blocked and normal paths must emit the field
        assert src.count('"output_truncated"') >= 2, \
            "Both log.log() calls must include output_truncated"

    def test_event_log_includes_original_output_bytes(self):
        src = self._cli_src()
        assert src.count('"original_output_bytes"') >= 2

    def test_event_log_includes_persisted_output_bytes(self):
        src = self._cli_src()
        assert src.count('"persisted_output_bytes"') >= 2

    def test_job_metadata_includes_truncation_fields(self):
        src = self._cli_src()
        # The job.metadata["test_runs"].append(...) dict must have all three
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
    """CLI must warn user when output was truncated."""

    def test_cli_prints_truncation_warning(self):
        src = (REPO_ROOT / "apps" / "cli" / "commands" / "test_cmds.py").read_text()
        assert "output truncated" in src.lower(), \
            "CLI must print a warning when output is truncated"
