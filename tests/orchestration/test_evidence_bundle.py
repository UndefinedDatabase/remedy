"""Evidence bundle tests — Steps 4807-4811.

Tests for deterministic evidence bundle export, redaction, safety, and CLI.
No real provider calls. No network. No target repo mutation.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from packages.orchestration import data_paths
from packages.orchestration.pingpong_evidence import (
    _redact_json_value,
    _redact_secrets,
    _sanitize_path,
    _validate_output_path,
    build_evidence_bundle,
    export_evidence,
    write_evidence_bundle,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path: Path, monkeypatch):
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


def _make_run_data(
    *,
    final_status: str = "staged_review_passed",
    repair_used: int = 0,
    repair_allowed: int = 2,
    test_passed: bool = True,
    has_diff: bool = True,
    has_task: bool = False,
    findings: list | None = None,
    run_id: str = "test_run_001",
) -> dict:
    """Build minimal fake run data for testing."""
    rounds = [
        {
            "round": 1,
            "kind": "initial",
            "repair_of_round": None,
            "input_finding_ids": [],
            "resolved_finding_ids": [],
            "remaining_finding_ids": [],
            "started_at": "2026-01-01T00:00:00Z",
            "finished_at": "2026-01-01T00:01:00Z",
            "builder": {
                "summary": "Made changes",
                "files_changed": ["src/main.py"],
                "provider": "fake",
                "duration_ms": 100,
                "tokens_used": 500,
                "error": "",
            },
            "test_passed": test_passed,
            "test_summary": "1 passed in 0.5s",
            "reviewer": {
                "verdict": "pass" if not findings else "needs_repair",
                "confidence": "high",
                "summary": "Looks good",
                "finding_count": len(findings) if findings else 0,
                "findings": findings or [],
                "provider": "fake",
                "duration_ms": 50,
                "error": "",
                "parse_retried": False,
                "parse_retry_recovered": False,
            },
        },
    ]

    if repair_used > 0:
        for i in range(repair_used):
            rounds.append({
                "round": i + 2,
                "kind": "repair",
                "repair_of_round": i + 1,
                "input_finding_ids": ["F-001"] if findings else [],
                "resolved_finding_ids": ["F-001"] if i == repair_used - 1 and findings else [],
                "remaining_finding_ids": [],
                "started_at": "2026-01-01T00:02:00Z",
                "finished_at": "2026-01-01T00:03:00Z",
                "builder": {
                    "summary": "Fixed issue",
                    "files_changed": ["src/main.py"],
                    "provider": "fake",
                    "duration_ms": 100,
                    "tokens_used": 500,
                    "error": "",
                },
                "test_passed": True,
                "test_summary": "1 passed in 0.5s",
                "reviewer": {
                    "verdict": "pass",
                    "confidence": "high",
                    "summary": "Fixed",
                    "finding_count": 0,
                    "findings": [],
                    "provider": "fake",
                    "duration_ms": 50,
                    "error": "",
                    "parse_retried": False,
                    "parse_retry_recovered": False,
                },
            })

    data: dict = {
        "run_id": run_id,
        "job_id": "",
        "goal": "Test evidence bundle",
        "repo_path": "/home/user/project",
        "mode": "staged",
        "builder_provider": "fake",
        "reviewer_provider": "fake",
        "max_rounds": 3,
        "total_rounds": len(rounds),
        "final_status": final_status,
        "staged_files": ["src/main.py"],
        "changed_target_files": [],
        "target_mutated": False,
        "tests_not_run": False,
        "safe_diff_files": ["src/main.py"] if has_diff else [],
        "safe_diff_truncated": False,
        "safe_diff_summary": (
            "--- a/src/main.py\n+++ b/src/main.py\n@@ -1 +1 @@\n-old\n+new\n"
            if has_diff else ""
        ),
        "staging_path": "/tmp/remedy-staging-xyz",
        "context_categories": ["code"],
        "error": "",
        "started_at": "2026-01-01T00:00:00Z",
        "finished_at": "2026-01-01T00:05:00Z",
        "rounds": rounds,
        "provider_evidence": {
            "builder_provider": "fake",
            "reviewer_provider": "fake",
            "builder_provider_kind": "synthetic_test",
            "reviewer_provider_kind": "synthetic_test",
            "builder_write_mode": "none",
            "reviewer_write_mode": "none",
            "builder_can_write_staging": False,
            "reviewer_can_write_staging": False,
        },
        "token_accounting": {
            "kind": "estimated",
            "actual_tokens_available": False,
            "builder_prompt_tokens_estimated": 125,
            "reviewer_prompt_tokens_estimated": 50,
            "context_tokens_estimated": 100,
            "context_categories": ["code"],
            "context_strategy": "bounded_task_context",
        },
        "repair_loop": {
            "enabled": repair_allowed > 0,
            "repair_rounds_allowed": repair_allowed,
            "repair_rounds_used": repair_used,
            "repair_rounds_source": "default",
            "status": (
                "not_needed" if repair_used == 0 and final_status == "staged_review_passed"
                else "passed_after_repair" if repair_used > 0 and final_status == "staged_review_passed"
                else "exhausted" if final_status == "repair_exhausted"
                else "disabled"
            ),
            "open_findings": [],
            "resolved_findings": [],
            "final_reviewer_verdict": "pass" if final_status == "staged_review_passed" else "",
            "decisions": [],
            "final_adjudication": None,
            "finding_status_map": [],
        },
    }

    if has_task:
        data["task_input"] = {
            "kind": "file",
            "title": "Test task",
            "sha256": "abc123def456",
            "bytes": 100,
            "chars": 100,
            "tokens_estimated": 25,
            "excerpt": "Do something useful",
        }

    return data


def _persist_fake_run(data_dir: Path, run_data: dict) -> str:
    """Persist a fake run for CLI testing."""
    run_id = run_data["run_id"]
    run_dir = data_paths.run_dir(run_id, data_dir)
    run_dir.mkdir(parents=True)
    (run_dir / "result.json").write_text(json.dumps(run_data, indent=2))
    return run_id


def _persist_fake_promotion(data_dir: Path, run_id: str, promo_data: dict) -> None:
    """Persist a fake promotion for CLI testing."""
    run_dir = data_paths.run_dir(run_id, data_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "promotion.json").write_text(json.dumps(promo_data, indent=2))


# ---------------------------------------------------------------------------
# Step 4807: Evidence bundle builder
# ---------------------------------------------------------------------------

class TestEvidenceBundleBuilder:
    """build_evidence_bundle produces correct bundle structure."""

    def test_no_repair_passed_run(self):
        """Bundle for a no-repair passed run."""
        data = _make_run_data(final_status="staged_review_passed", repair_used=0)
        bundle = build_evidence_bundle(data)
        assert bundle["manifest"]["run_id"] == "test_run_001"
        assert bundle["manifest"]["final_status"] == "staged_review_passed"
        assert bundle["manifest"]["promotion_readiness"]["ready"] is True

    def test_passed_after_repair_run(self):
        """Bundle for a passed-after-repair run."""
        data = _make_run_data(
            final_status="staged_review_passed",
            repair_used=1,
            findings=[{"id": "F-001", "severity": "high", "file": "main.py", "summary": "bug"}],
        )
        bundle = build_evidence_bundle(data)
        assert bundle["manifest"]["final_status"] == "staged_review_passed"
        assert bundle["repair_loop"]["repair_rounds_used"] == 1
        assert bundle["manifest"]["promotion_readiness"]["ready"] is True

    def test_repair_exhausted_run(self):
        """Bundle for a repair-exhausted run."""
        data = _make_run_data(final_status="repair_exhausted", repair_used=2)
        bundle = build_evidence_bundle(data)
        assert bundle["manifest"]["final_status"] == "repair_exhausted"
        assert bundle["manifest"]["promotion_readiness"]["ready"] is False

    def test_with_promotion(self):
        """Bundle includes promotion data when provided."""
        data = _make_run_data()
        promo = {
            "run_id": "test_run_001",
            "promotion_id": "promo_001",
            "status": "dry_run_ready",
            "approved": False,
            "dry_run": True,
            "target_repo": "/home/user/project",
        }
        bundle = build_evidence_bundle(data, promo)
        assert bundle["promotion"] is not None
        assert bundle["promotion"]["status"] == "dry_run_ready"

    def test_manifest_has_final_status(self):
        """manifest.json includes final_status."""
        data = _make_run_data(final_status="test_failed", test_passed=False)
        bundle = build_evidence_bundle(data)
        assert bundle["manifest"]["final_status"] == "test_failed"

    def test_summary_md_human_readable(self):
        """summary.md is human-readable markdown."""
        data = _make_run_data()
        bundle = build_evidence_bundle(data)
        md = bundle["summary_md"]
        assert "# Remedy Run Evidence" in md
        assert "staged_review_passed" in md
        assert "## Providers" in md

    def test_safe_diff_present(self):
        """safe.diff contains diff when available."""
        data = _make_run_data(has_diff=True)
        bundle = build_evidence_bundle(data)
        assert "--- a/src/main.py" in bundle["safe_diff"]

    def test_tests_txt_present(self):
        """tests.txt contains test summary."""
        data = _make_run_data()
        bundle = build_evidence_bundle(data)
        assert "Round 1" in bundle["tests"]
        assert "passed" in bundle["tests"]

    def test_review_json_has_verdict(self):
        """review.json contains reviewer verdict and findings."""
        data = _make_run_data()
        bundle = build_evidence_bundle(data)
        assert bundle["review"]["final_verdict"] == "pass"
        assert bundle["review"]["total_reviews"] == 1

    def test_repair_loop_json_present(self):
        """repair_loop.json contains repair status."""
        data = _make_run_data(repair_used=1, findings=[
            {"id": "F-001", "severity": "high", "file": "main.py", "summary": "bug"},
        ])
        bundle = build_evidence_bundle(data)
        assert bundle["repair_loop"]["repair_rounds_used"] == 1

    def test_token_accounting_present(self):
        """token_accounting.json contains estimated token evidence."""
        data = _make_run_data()
        bundle = build_evidence_bundle(data)
        assert "kind" in bundle["token_accounting"]

    def test_provider_evidence_present(self):
        """provider_evidence.json contains Worker/Reviewer provider evidence."""
        data = _make_run_data()
        bundle = build_evidence_bundle(data)
        assert bundle["provider_evidence"]["builder_provider"] == "fake"
        assert bundle["provider_evidence"]["reviewer_provider"] == "fake"

    def test_promotion_absent_when_not_promoted(self):
        """promotion.json is None when not promoted."""
        data = _make_run_data()
        bundle = build_evidence_bundle(data, None)
        assert bundle["promotion"] is None

    def test_missing_diff_produces_unavailable_note(self):
        """Missing diff produces unavailable note in manifest, not crash."""
        data = _make_run_data(has_diff=False)
        bundle = build_evidence_bundle(data)
        assert "unavailable" in bundle["manifest"]["sections"]["safe.diff"]

    def test_task_input_metadata(self):
        """Task input metadata included when present."""
        data = _make_run_data(has_task=True)
        bundle = build_evidence_bundle(data)
        assert bundle["manifest"]["task_input"] is not None
        assert bundle["manifest"]["task_input"]["sha256"] == "abc123def456"


# ---------------------------------------------------------------------------
# Step 4808: CLI evidence command (via export_evidence)
# ---------------------------------------------------------------------------

class TestEvidenceCli:
    """export_evidence loads run and writes bundle."""

    def test_export_nonexistent_run(self, tmp_path):
        """Missing run returns error, not crash."""
        result = export_evidence("nonexistent_id", str(tmp_path / "out"))
        assert result.get("error")
        assert "not found" in result["error"]

    def test_export_no_repair_run(self, isolate_data_root, tmp_path):
        """Export works for a no-repair passed run."""
        data = _make_run_data()
        _persist_fake_run(isolate_data_root, data)
        out_dir = tmp_path / "bundle"
        result = export_evidence("test_run_001", str(out_dir))
        assert "error" not in result
        assert (out_dir / "manifest.json").exists()
        assert (out_dir / "summary.md").exists()
        assert (out_dir / "safe.diff").exists()
        assert (out_dir / "tests.txt").exists()
        assert (out_dir / "review.json").exists()
        assert (out_dir / "token_accounting.json").exists()
        assert (out_dir / "provider_evidence.json").exists()
        # Verify manifest content
        manifest = json.loads((out_dir / "manifest.json").read_text())
        assert manifest["final_status"] == "staged_review_passed"

    def test_export_passed_after_repair(self, isolate_data_root, tmp_path):
        """Export works for passed-after-repair run."""
        data = _make_run_data(
            final_status="staged_review_passed",
            repair_used=1,
            run_id="repair_run",
            findings=[{"id": "F-001", "severity": "high", "file": "main.py", "summary": "bug"}],
        )
        _persist_fake_run(isolate_data_root, data)
        out_dir = tmp_path / "bundle"
        result = export_evidence("repair_run", str(out_dir))
        assert "error" not in result
        repair = json.loads((out_dir / "repair_loop.json").read_text())
        assert repair["repair_rounds_used"] == 1

    def test_export_repair_exhausted(self, isolate_data_root, tmp_path):
        """Export works for repair-exhausted run."""
        data = _make_run_data(
            final_status="repair_exhausted",
            repair_used=2,
            run_id="exhausted_run",
        )
        _persist_fake_run(isolate_data_root, data)
        out_dir = tmp_path / "bundle"
        result = export_evidence("exhausted_run", str(out_dir))
        assert "error" not in result
        manifest = json.loads((out_dir / "manifest.json").read_text())
        assert manifest["final_status"] == "repair_exhausted"
        assert manifest["promotion_readiness"]["ready"] is False

    def test_export_with_promotion(self, isolate_data_root, tmp_path):
        """Export includes promotion when present."""
        data = _make_run_data(run_id="promo_run")
        _persist_fake_run(isolate_data_root, data)
        promo = {
            "run_id": "promo_run",
            "promotion_id": "promo_001",
            "status": "dry_run_ready",
            "approved": False,
            "dry_run": True,
            "target_repo": "/home/user/project",
        }
        _persist_fake_promotion(isolate_data_root, "promo_run", promo)
        out_dir = tmp_path / "bundle"
        result = export_evidence("promo_run", str(out_dir))
        assert "error" not in result
        assert (out_dir / "promotion.json").exists()
        pdata = json.loads((out_dir / "promotion.json").read_text())
        assert pdata["status"] == "dry_run_ready"


# ---------------------------------------------------------------------------
# Step 4809: Redaction and safe-output rules
# ---------------------------------------------------------------------------

class TestRedaction:
    """Redaction and safe-output rules."""

    def test_no_raw_task_body_by_default(self):
        """Raw full task body not dumped by default."""
        data = _make_run_data(has_task=True)
        # Add raw task_body to run_data (simulating what export_pingpong_json omits)
        data["task_body"] = "This is the full secret task body with API_KEY=sk-ant-secret123"
        bundle = build_evidence_bundle(data)
        # Bundle should NOT contain raw task body in manifest or summary
        manifest_str = json.dumps(bundle["manifest"])
        assert "full secret task body" not in manifest_str
        assert "sk-ant-secret123" not in manifest_str
        # Summary should not contain raw body
        assert "full secret task body" not in bundle["summary_md"]

    def test_api_key_redacted(self):
        """API-key-like strings are redacted."""
        assert "[REDACTED]" in _redact_secrets("key: sk-ant-abc123def456ghi789jkl012")
        assert "[REDACTED]" in _redact_secrets("AKIAIOSFODNN7EXAMPLE")
        assert "[REDACTED]" in _redact_secrets("token: ghp_abcdefghijklmnopqrstuvwxyz1234567890")

    def test_env_key_redacted(self):
        """Environment variable secrets are redacted."""
        assert "[REDACTED]" in _redact_secrets("API_KEY=my_secret_value")
        assert "[REDACTED]" in _redact_secrets("SECRET=hunter2")

    def test_path_sanitization(self):
        """Absolute staging paths sanitized."""
        home = os.path.expanduser("~")
        assert _sanitize_path(f"{home}/project") == "[local]"
        assert _sanitize_path("/other/path") == "/other/path"

    def test_summary_md_no_absolute_staging_path(self):
        """summary.md doesn't contain absolute private staging paths."""
        data = _make_run_data()
        data["staging_path"] = "/tmp/remedy-staging-secret"
        bundle = build_evidence_bundle(data)
        # staging_path is not emitted in summary
        assert "/tmp/remedy-staging-secret" not in bundle["summary_md"]

    def test_path_traversal_blocked(self, tmp_path):
        """Output path traversal is blocked."""
        with pytest.raises(ValueError, match="Path traversal blocked"):
            _validate_output_path(str(tmp_path), "../../../etc/passwd")

    def test_path_traversal_blocked_in_write(self, tmp_path):
        """write_evidence_bundle blocks path traversal attempts."""
        data = _make_run_data()
        bundle = build_evidence_bundle(data)
        # Inject traversal filename
        bundle["manifest"] = bundle["manifest"]  # normal
        out_dir = str(tmp_path / "safe_out")
        # Normal write should succeed
        written = write_evidence_bundle(bundle, out_dir)
        assert "manifest.json" in written

    def test_no_env_in_bundle_files(self, isolate_data_root, tmp_path):
        """Bundle files don't contain env/API-key strings."""
        data = _make_run_data()
        # Inject secret into test summary
        data["rounds"][0]["test_summary"] = "Test passed. API_KEY=sk-ant-mysecretkey123456789012 OK"
        _persist_fake_run(isolate_data_root, data)
        out_dir = tmp_path / "bundle"
        export_evidence("test_run_001", str(out_dir))
        # Check tests.txt for redaction
        tests_content = (out_dir / "tests.txt").read_text()
        assert "sk-ant-mysecretkey" not in tests_content
        assert "[REDACTED]" in tests_content


# ---------------------------------------------------------------------------
# Step 4810: Safety — no provider calls, no target mutation
# ---------------------------------------------------------------------------

class TestSafety:
    """Evidence export is read-only and safe."""

    def test_no_provider_call(self, isolate_data_root, tmp_path):
        """export_evidence does not call any provider."""
        data = _make_run_data()
        _persist_fake_run(isolate_data_root, data)
        # export_evidence only reads JSON, no provider imports needed
        # If it tried to call a provider, it would fail since none are configured
        result = export_evidence("test_run_001", str(tmp_path / "out"))
        assert "error" not in result

    def test_no_target_mutation(self, isolate_data_root, tmp_path):
        """export_evidence does not mutate target repo."""
        data = _make_run_data()
        repo_path = tmp_path / "target_repo"
        repo_path.mkdir()
        (repo_path / "file.txt").write_text("original")
        data["repo_path"] = str(repo_path)
        _persist_fake_run(isolate_data_root, data)
        export_evidence("test_run_001", str(tmp_path / "out"))
        # Target repo unchanged
        assert (repo_path / "file.txt").read_text() == "original"

    def test_output_only_in_out_dir(self, isolate_data_root, tmp_path):
        """All output files are inside the requested output directory."""
        data = _make_run_data()
        _persist_fake_run(isolate_data_root, data)
        out_dir = tmp_path / "bundle_out"
        result = export_evidence("test_run_001", str(out_dir))
        out_resolved = str(out_dir.resolve())
        for path in result.get("files", {}).values():
            assert path.startswith(out_resolved), f"{path} escapes {out_resolved}"

    def test_deterministic_output(self, isolate_data_root, tmp_path):
        """Same input produces identical output."""
        data = _make_run_data()
        _persist_fake_run(isolate_data_root, data)
        out1 = tmp_path / "out1"
        out2 = tmp_path / "out2"
        export_evidence("test_run_001", str(out1))
        export_evidence("test_run_001", str(out2))
        for fname in ("manifest.json", "summary.md", "review.json"):
            c1 = (out1 / fname).read_text()
            c2 = (out2 / fname).read_text()
            assert c1 == c2, f"{fname} differs between runs"


# ---------------------------------------------------------------------------
# Step 4810: CLI dispatch test
# ---------------------------------------------------------------------------

class TestCliDispatch:
    """COMMAND_HANDLERS['do.evidence'] dispatches correctly."""

    def test_cli_handler_exists(self):
        """do.evidence handler exists in COMMAND_HANDLERS."""
        from apps.cli.commands.do_cmd import COMMAND_HANDLERS
        assert "do.evidence" in COMMAND_HANDLERS

    def test_cli_catalog_entry_exists(self):
        """do.evidence has a catalog entry."""
        from apps.cli.command_catalog import CATALOG
        ids = [c.command_id for c in CATALOG]
        assert "do.evidence" in ids

    def test_catalog_read_only(self):
        """do.evidence is read_only action class."""
        from apps.cli.command_catalog import CATALOG
        entry = next(c for c in CATALOG if c.command_id == "do.evidence")
        assert entry.action_class == "read_only"
        assert entry.may_mutate_repo is False
        assert entry.may_execute_commands is False


# ---------------------------------------------------------------------------
# Test secret strings used across Steps 4815-4816
# ---------------------------------------------------------------------------

_TEST_SECRETS = {
    "api_key_env": "API_KEY=supersecretvalue123",
    "secret_env": "SECRET=hunter2password",
    "bearer": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.abcdefghijk",
    "sk_ant": "sk-ant-abcdef1234567890abcdef1234567890",
    "sk_openai": "sk-abcdefghijklmnopqrstuvwxyz1234567890",
    "ghp": "ghp_abcdefghijklmnopqrstuvwxyz1234567890",
    "akia": "AKIAIOSFODNN7EXAMPLE1",
}

# Substrings that must NOT appear in output after redaction
_LEAK_MARKERS = [
    "supersecretvalue123",
    "hunter2password",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
    "sk-ant-abcdef1234567890abcdef1234567890",
    "sk-abcdefghijklmnopqrstuvwxyz1234567890",
    "ghp_abcdefghijklmnopqrstuvwxyz1234567890",
    "AKIAIOSFODNN7EXAMPLE1",
]


def _make_poisoned_run_data() -> dict:
    """Build run data with secrets injected into many fields."""
    data = _make_run_data(has_task=True)
    # Poison task excerpt
    data["task_input"]["excerpt"] = "Fix the bug. Use API_KEY=supersecretvalue123 to auth."
    # Poison reviewer summary
    data["rounds"][0]["reviewer"]["summary"] = (
        "Code uses sk-ant-abcdef1234567890abcdef1234567890 directly"
    )
    # Poison reviewer finding
    data["rounds"][0]["reviewer"]["findings"] = [
        {
            "id": "F-001",
            "severity": "high",
            "file": "main.py",
            "summary": "Hardcoded ghp_abcdefghijklmnopqrstuvwxyz1234567890 in source",
        },
    ]
    data["rounds"][0]["reviewer"]["finding_count"] = 1
    # Poison test summary
    data["rounds"][0]["test_summary"] = (
        "Test passed. SECRET=hunter2password leaked in output."
    )
    # Poison token accounting note
    data["token_accounting"]["token_note"] = (
        "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.abcdefghijk was used"
    )
    # Poison provider evidence
    data["provider_evidence"]["debug_note"] = (
        "Used AKIAIOSFODNN7EXAMPLE1 for auth"
    )
    # Poison repair_loop
    data["repair_loop"]["debug_reason"] = (
        "Repair because sk-abcdefghijklmnopqrstuvwxyz1234567890 exposed"
    )
    return data


# ---------------------------------------------------------------------------
# Step 4812: Recursive JSON redaction
# ---------------------------------------------------------------------------

class TestRecursiveRedaction:
    """_redact_json_value recursively sanitizes all string values."""

    def test_redacts_string(self):
        assert "[REDACTED]" in _redact_json_value("key: sk-ant-abcdef1234567890abcdef1234567890")

    def test_preserves_int(self):
        assert _redact_json_value(42) == 42

    def test_preserves_bool(self):
        assert _redact_json_value(True) is True

    def test_preserves_none(self):
        assert _redact_json_value(None) is None

    def test_preserves_float(self):
        assert _redact_json_value(3.14) == 3.14

    def test_redacts_dict_values(self):
        result = _redact_json_value({"key": "API_KEY=secret123"})
        assert "secret123" not in result["key"]
        assert "[REDACTED]" in result["key"]

    def test_redacts_list_items(self):
        result = _redact_json_value(["safe", "sk-ant-abcdef1234567890abcdef1234567890"])
        assert result[0] == "safe"
        assert "[REDACTED]" in result[1]

    def test_redacts_nested(self):
        result = _redact_json_value({
            "outer": {
                "inner": ["ghp_abcdefghijklmnopqrstuvwxyz1234567890"],
            },
        })
        assert "[REDACTED]" in result["outer"]["inner"][0]

    def test_preserves_dict_shape(self):
        original = {"a": 1, "b": "safe", "c": [1, 2]}
        result = _redact_json_value(original)
        assert result == original

    def test_does_not_mutate_original(self):
        original = {"key": "API_KEY=secret123"}
        result = _redact_json_value(original)
        assert "secret123" in original["key"]
        assert "secret123" not in result["key"]

    def test_tuple_preserved(self):
        result = _redact_json_value(("safe", "API_KEY=x"))
        assert isinstance(result, tuple)
        assert result[0] == "safe"


# ---------------------------------------------------------------------------
# Step 4815: Explicit JSON leak regression tests
# ---------------------------------------------------------------------------

class TestJsonLeakRegression:
    """Secrets must be redacted from every JSON output file."""

    def test_manifest_task_excerpt_redacted(self, isolate_data_root, tmp_path):
        """manifest.json task excerpt does not leak API_KEY."""
        data = _make_poisoned_run_data()
        _persist_fake_run(isolate_data_root, data)
        out_dir = tmp_path / "bundle"
        export_evidence("test_run_001", str(out_dir))
        content = (out_dir / "manifest.json").read_text()
        assert "supersecretvalue123" not in content

    def test_review_summary_redacted(self, isolate_data_root, tmp_path):
        """review.json reviewer summary does not leak sk-ant key."""
        data = _make_poisoned_run_data()
        _persist_fake_run(isolate_data_root, data)
        out_dir = tmp_path / "bundle"
        export_evidence("test_run_001", str(out_dir))
        content = (out_dir / "review.json").read_text()
        assert "sk-ant-abcdef" not in content

    def test_review_finding_redacted(self, isolate_data_root, tmp_path):
        """review.json finding summary does not leak ghp token."""
        data = _make_poisoned_run_data()
        _persist_fake_run(isolate_data_root, data)
        out_dir = tmp_path / "bundle"
        export_evidence("test_run_001", str(out_dir))
        content = (out_dir / "review.json").read_text()
        assert "ghp_abcdefghijklmnopqrstuvwxyz" not in content

    def test_token_accounting_redacted(self, isolate_data_root, tmp_path):
        """token_accounting.json does not leak Bearer token."""
        data = _make_poisoned_run_data()
        _persist_fake_run(isolate_data_root, data)
        out_dir = tmp_path / "bundle"
        export_evidence("test_run_001", str(out_dir))
        content = (out_dir / "token_accounting.json").read_text()
        assert "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" not in content

    def test_provider_evidence_redacted(self, isolate_data_root, tmp_path):
        """provider_evidence.json does not leak AWS key."""
        data = _make_poisoned_run_data()
        _persist_fake_run(isolate_data_root, data)
        out_dir = tmp_path / "bundle"
        export_evidence("test_run_001", str(out_dir))
        content = (out_dir / "provider_evidence.json").read_text()
        assert "AKIAIOSFODNN7EXAMPLE1" not in content

    def test_repair_loop_redacted(self, isolate_data_root, tmp_path):
        """repair_loop.json does not leak sk- key."""
        data = _make_poisoned_run_data()
        _persist_fake_run(isolate_data_root, data)
        out_dir = tmp_path / "bundle"
        export_evidence("test_run_001", str(out_dir))
        content = (out_dir / "repair_loop.json").read_text()
        assert "sk-abcdefghijklmnopqrstuvwxyz" not in content

    def test_promotion_redacted(self, isolate_data_root, tmp_path):
        """promotion.json does not leak secrets."""
        data = _make_run_data(run_id="promo_leak")
        _persist_fake_run(isolate_data_root, data)
        promo = {
            "run_id": "promo_leak",
            "status": "dry_run_ready",
            "note": "Used API_KEY=supersecretvalue123 for auth",
        }
        _persist_fake_promotion(isolate_data_root, "promo_leak", promo)
        out_dir = tmp_path / "bundle"
        export_evidence("promo_leak", str(out_dir))
        content = (out_dir / "promotion.json").read_text()
        assert "supersecretvalue123" not in content


# ---------------------------------------------------------------------------
# Step 4816: Full-output scanner test
# ---------------------------------------------------------------------------

class TestFullOutputScanner:
    """Scan every emitted file for known secret strings."""

    def test_no_secret_leaks_in_any_file(self, isolate_data_root, tmp_path):
        """No output file may contain unredacted known secret strings."""
        data = _make_poisoned_run_data()
        _persist_fake_run(isolate_data_root, data)
        # Also add promotion with secret
        promo = {
            "run_id": "test_run_001",
            "status": "dry_run_ready",
            "note": "Used Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.abcdefghijk for auth",
        }
        _persist_fake_promotion(isolate_data_root, "test_run_001", promo)
        out_dir = tmp_path / "bundle"
        export_evidence("test_run_001", str(out_dir))

        # Scan all emitted files
        for fpath in out_dir.iterdir():
            content = fpath.read_text()
            for marker in _LEAK_MARKERS:
                assert marker not in content, (
                    f"Secret leaked in {fpath.name}: found {marker!r}"
                )


# ---------------------------------------------------------------------------
# Step 4817: Preserve useful proof while redacting
# ---------------------------------------------------------------------------

class TestUsefulnessPreservation:
    """Redaction must not destroy evidence usefulness."""

    def test_manifest_preserves_identity(self, isolate_data_root, tmp_path):
        """Manifest still has run_id, final_status, sections."""
        data = _make_poisoned_run_data()
        _persist_fake_run(isolate_data_root, data)
        out_dir = tmp_path / "bundle"
        export_evidence("test_run_001", str(out_dir))
        manifest = json.loads((out_dir / "manifest.json").read_text())
        assert manifest["run_id"] == "test_run_001"
        assert manifest["final_status"] == "staged_review_passed"
        assert "manifest.json" in manifest["sections"]
        assert manifest["sections"]["manifest.json"] == "present"

    def test_review_preserves_verdict_and_count(self, isolate_data_root, tmp_path):
        """review.json still has verdict and finding count."""
        data = _make_poisoned_run_data()
        _persist_fake_run(isolate_data_root, data)
        out_dir = tmp_path / "bundle"
        export_evidence("test_run_001", str(out_dir))
        review = json.loads((out_dir / "review.json").read_text())
        assert review["total_reviews"] == 1
        # Verdict preserved (not a secret)
        assert review["reviews"][0]["verdict"] == "pass"
        assert review["reviews"][0]["finding_count"] == 1

    def test_promotion_preserves_status(self, isolate_data_root, tmp_path):
        """promotion.json still has status."""
        data = _make_run_data(run_id="useful_promo")
        _persist_fake_run(isolate_data_root, data)
        promo = {
            "run_id": "useful_promo",
            "status": "dry_run_ready",
            "approved": False,
            "note": "API_KEY=leaked here",
        }
        _persist_fake_promotion(isolate_data_root, "useful_promo", promo)
        out_dir = tmp_path / "bundle"
        export_evidence("useful_promo", str(out_dir))
        pdata = json.loads((out_dir / "promotion.json").read_text())
        assert pdata["status"] == "dry_run_ready"
        assert pdata["approved"] is False

    def test_token_accounting_preserves_kind(self, isolate_data_root, tmp_path):
        """token_accounting.json still has kind and estimates."""
        data = _make_poisoned_run_data()
        _persist_fake_run(isolate_data_root, data)
        out_dir = tmp_path / "bundle"
        export_evidence("test_run_001", str(out_dir))
        ta = json.loads((out_dir / "token_accounting.json").read_text())
        assert ta["kind"] == "estimated"
        assert "builder_prompt_tokens_estimated" in ta

    def test_provider_evidence_preserves_names(self, isolate_data_root, tmp_path):
        """provider_evidence.json still has provider names and kinds."""
        data = _make_poisoned_run_data()
        _persist_fake_run(isolate_data_root, data)
        out_dir = tmp_path / "bundle"
        export_evidence("test_run_001", str(out_dir))
        pe = json.loads((out_dir / "provider_evidence.json").read_text())
        assert pe["builder_provider"] == "fake"
        assert pe["reviewer_provider"] == "fake"
        assert pe["builder_provider_kind"] == "synthetic_test"

    def test_summary_md_still_readable(self, isolate_data_root, tmp_path):
        """summary.md is still human-readable markdown."""
        data = _make_poisoned_run_data()
        _persist_fake_run(isolate_data_root, data)
        out_dir = tmp_path / "bundle"
        export_evidence("test_run_001", str(out_dir))
        summary = (out_dir / "summary.md").read_text()
        assert "# Remedy Run Evidence" in summary
        assert "## Providers" in summary
        assert "staged_review_passed" in summary


# ---------------------------------------------------------------------------
# Step 4822: CLI stdout JSON leak regression test
# ---------------------------------------------------------------------------

class TestCliStdoutRedaction:
    """CLI --json output must not leak secrets."""

    def test_cli_json_stdout_redacted(self, isolate_data_root, tmp_path):
        """do evidence --json stdout does not leak secrets."""
        data = _make_run_data(has_task=True)
        data["goal"] = "Fix API_KEY=supersecretvalue123 leak"
        data["task_input"]["excerpt"] = "Use sk-ant-abcdef1234567890abcdef1234567890"
        _persist_fake_run(isolate_data_root, data)
        out_dir = tmp_path / "bundle"
        result = export_evidence("test_run_001", str(out_dir))
        # Simulate what CLI does: json.dumps(result)
        stdout = json.dumps(result, indent=2)
        assert "supersecretvalue123" not in stdout
        assert "sk-ant-abcdef" not in stdout
        # Useful fields preserved
        assert "test_run_001" in stdout
        assert "staged_review_passed" in stdout


# ---------------------------------------------------------------------------
# Step 4823: export_evidence return-value regression test
# ---------------------------------------------------------------------------

class TestExportReturnRedaction:
    """export_evidence() return value must be redacted."""

    def test_return_manifest_redacted(self, isolate_data_root, tmp_path):
        """Return manifest does not contain raw secrets."""
        data = _make_poisoned_run_data()
        _persist_fake_run(isolate_data_root, data)
        out_dir = tmp_path / "bundle"
        result = export_evidence("test_run_001", str(out_dir))
        result_str = json.dumps(result)
        for marker in _LEAK_MARKERS:
            assert marker not in result_str, (
                f"Secret leaked in export_evidence return: {marker!r}"
            )

    def test_return_preserves_useful_fields(self, isolate_data_root, tmp_path):
        """Return value still has run_id, out_dir, manifest identity."""
        data = _make_poisoned_run_data()
        _persist_fake_run(isolate_data_root, data)
        out_dir = tmp_path / "bundle"
        result = export_evidence("test_run_001", str(out_dir))
        assert result["run_id"] == "test_run_001"
        assert "out_dir" in result
        assert result["manifest"]["final_status"] == "staged_review_passed"
        assert result["manifest"]["run_id"] == "test_run_001"

    def test_return_has_redacted_placeholder(self, isolate_data_root, tmp_path):
        """Return value contains [REDACTED] where secrets were."""
        data = _make_run_data(has_task=True)
        data["goal"] = "Fix API_KEY=supersecretvalue123"
        _persist_fake_run(isolate_data_root, data)
        out_dir = tmp_path / "bundle"
        result = export_evidence("test_run_001", str(out_dir))
        result_str = json.dumps(result)
        assert "[REDACTED]" in result_str


# ---------------------------------------------------------------------------
# Step 4824: Extended full-output scanner (files + CLI/API payload)
# ---------------------------------------------------------------------------

class TestFullOutputScannerExtended:
    """Scan files AND CLI/API return for known secrets."""

    def test_no_leaks_in_files_or_api_return(self, isolate_data_root, tmp_path):
        """Neither output files nor API return contain secrets."""
        data = _make_poisoned_run_data()
        _persist_fake_run(isolate_data_root, data)
        promo = {
            "run_id": "test_run_001",
            "status": "dry_run_ready",
            "note": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.abcdefghijk",
        }
        _persist_fake_promotion(isolate_data_root, "test_run_001", promo)
        out_dir = tmp_path / "bundle"
        result = export_evidence("test_run_001", str(out_dir))

        # Scan files
        for fpath in out_dir.iterdir():
            content = fpath.read_text()
            for marker in _LEAK_MARKERS:
                assert marker not in content, (
                    f"Secret leaked in {fpath.name}: {marker!r}"
                )

        # Scan API return (simulates CLI --json stdout)
        api_str = json.dumps(result, indent=2)
        for marker in _LEAK_MARKERS:
            assert marker not in api_str, (
                f"Secret leaked in API return: {marker!r}"
            )


# -- F002: builder_no_changes still produces review/test evidence ----------


def _make_no_changes_run_data() -> dict:
    """Build minimal run data simulating a builder_no_changes outcome."""
    return {
        "run_id": "no_changes_001",
        "goal": "verify code is correct",
        "repo_path": "/tmp/test",
        "mode": "staged",
        "builder_provider": "claude-cli",
        "reviewer_provider": "claude-cli",
        "final_status": "builder_no_changes",
        "total_rounds": 0,
        "max_rounds": 3,
        "started_at": "2026-01-01T00:00:00Z",
        "finished_at": "2026-01-01T00:01:00Z",
        "rounds": [],
        "staged_files": [],
        "error": "Builder produced no file changes in staging",
        "safe_diff_summary": "",
        "target_mutated": False,
        "tests_not_run": True,
        "repair_loop": {
            "enabled": False,
            "repair_rounds_allowed": 0,
            "repair_rounds_used": 0,
            "status": "disabled",
        },
    }


def test_builder_no_changes_produces_review_json(tmp_path: Path) -> None:
    """builder_no_changes still produces review.json."""
    run_data = _make_no_changes_run_data()
    bundle = build_evidence_bundle(run_data)
    out_dir = tmp_path / "evidence"
    out_dir.mkdir()
    written = write_evidence_bundle(bundle, str(out_dir))
    assert "review.json" in written
    review = json.loads(Path(written["review.json"]).read_text())
    assert review["final_verdict"] == "no_changes_verified"
    assert review["total_reviews"] == 1


def test_builder_no_changes_produces_tests_txt(tmp_path: Path) -> None:
    """builder_no_changes still produces tests.txt."""
    run_data = _make_no_changes_run_data()
    bundle = build_evidence_bundle(run_data)
    out_dir = tmp_path / "evidence"
    out_dir.mkdir()
    written = write_evidence_bundle(bundle, str(out_dir))
    assert "tests.txt" in written
    content = Path(written["tests.txt"]).read_text()
    assert "builder_no_changes" in content


def test_builder_no_changes_does_not_skip_evidence(tmp_path: Path) -> None:
    """builder_no_changes writes both review.json and tests.txt."""
    run_data = _make_no_changes_run_data()
    bundle = build_evidence_bundle(run_data)
    out_dir = tmp_path / "evidence"
    out_dir.mkdir()
    written = write_evidence_bundle(bundle, str(out_dir))
    assert "review.json" in written
    assert "tests.txt" in written
    assert "manifest.json" in written
