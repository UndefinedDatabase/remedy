"""
Domain tests: ui_server/test_auth_redaction.py
Migrated from step-numbered test files.
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from uuid import uuid4

from packages.core.models import Job, RunState, Task


def _make_job(**overrides) -> Job:
    defaults = {
        "id": uuid4(),
        "name": "test-job",
        "user_prompt": "test prompt",
        "tasks": [Task(description="task 1", status=RunState.COMPLETED)],
        "state": RunState.COMPLETED,
        "permissions": {"repo_generated_write": "allow", "repo_test_run": "allow"},
        "metadata": {"target_repo": "."},
    }
    defaults.update(overrides)
    return Job(**defaults)


def _get_viewer_html():
    from packages.orchestration.brain_viewer import (
        build_brain_viewer_data,
        write_brain_viewer_files,
    )
    from packages.orchestration.project_brain import build_project_brain

    job = _make_job()
    events = [{"event": "job_created", "run_id": "r1", "job_id": str(job.id),
                "timestamp": "2026-01-01", "outcome": "ok", "metadata": {}}]
    graph = build_project_brain(job, events)
    data = build_brain_viewer_data(job, graph, events)
    with tempfile.TemporaryDirectory() as td:
        out = Path(td)
        html_path = write_brain_viewer_files(data, out)
        return html_path.read_text(), data, out


# ── Step 74.1: Redaction Gate Precision ─────────────────────────────────




class TestRedactionPatterns:
    def test_module_exists(self):
        from packages.orchestration.redaction_patterns import (
            FORBIDDEN_RAW_FIELD_NAMES,
            FORBIDDEN_SECRET_PATTERNS,
        )
        assert len(FORBIDDEN_RAW_FIELD_NAMES) >= 5
        assert len(FORBIDDEN_SECRET_PATTERNS) >= 5

    def test_no_secrets_allowed(self):
        from packages.orchestration.redaction_patterns import find_forbidden_surface_tokens
        # Category words are allowed
        assert find_forbidden_surface_tokens("No secrets or API keys in worker specs.") == []
        assert find_forbidden_surface_tokens("redact secrets") == []
        assert find_forbidden_surface_tokens("environment_secrets") == []

    def test_secret_equals_blocked(self):
        from packages.orchestration.redaction_patterns import find_forbidden_surface_tokens
        findings = find_forbidden_surface_tokens("config: secret=abc123")
        assert len(findings) > 0

    def test_password_equals_blocked(self):
        from packages.orchestration.redaction_patterns import find_forbidden_surface_tokens
        findings = find_forbidden_surface_tokens("db: password=hunter2")
        assert len(findings) > 0

    def test_sk_prefix_blocked(self):
        from packages.orchestration.redaction_patterns import find_forbidden_surface_tokens
        findings = find_forbidden_surface_tokens("key: sk-abc123defg456789")
        assert len(findings) > 0

    def test_ghp_prefix_blocked(self):
        from packages.orchestration.redaction_patterns import find_forbidden_surface_tokens
        findings = find_forbidden_surface_tokens("token: ghp_abcdefghijklmnop")
        assert len(findings) > 0

    def test_raw_field_blocked(self):
        from packages.orchestration.redaction_patterns import find_forbidden_surface_tokens
        findings = find_forbidden_surface_tokens("field: approval_reason")
        assert len(findings) > 0
        findings2 = find_forbidden_surface_tokens("diff_preview data here")
        assert len(findings2) > 0

    def test_traceback_blocked(self):
        from packages.orchestration.redaction_patterns import find_forbidden_surface_tokens
        findings = find_forbidden_surface_tokens("Traceback (most recent call last):")
        assert len(findings) > 0

    def test_viewer_html_passes_precision(self):
        from packages.orchestration.redaction_patterns import find_forbidden_surface_tokens
        html, _, _ = _get_viewer_html()
        findings = find_forbidden_surface_tokens(html)
        assert findings == [], f"Viewer HTML has redaction findings: {findings}"

    def test_clean_text_passes(self):
        from packages.orchestration.redaction_patterns import find_forbidden_surface_tokens
        assert find_forbidden_surface_tokens("Normal text about jobs and tasks") == []
        assert find_forbidden_surface_tokens("No secrets or API keys") == []


# ── Step 75: Interactive Brain Control Surface ──────────────────────────

