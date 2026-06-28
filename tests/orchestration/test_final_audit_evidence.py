"""Tests for evidence-derived final audit, path hygiene, and cockpit bridge."""
from __future__ import annotations

from apps.cli.commands.do_cmd import _build_final_audit, _sanitize_shareable_paths


class _FakeTask:
    def __init__(self, task_id: str, status: str, verdict: str = "", error: str = ""):
        self.task_id = task_id
        self.status = status
        self.reviewer_verdict = verdict
        self.safe_diff_files = ["main.py"]
        self.test_passed = True if status == "applied_to_job_workspace" else None
        self.error = error


class _FakeJob:
    def __init__(self, status: str, tasks: list):
        self.status = status
        self.tasks = tasks


class _FakePromo:
    def __init__(self, status: str = "dry_run", blocked_reason: str = ""):
        self.status = status
        self.blocked_reason = blocked_reason


class TestFinalAuditEvidenceDerived:
    def test_ready_when_all_artifacts_present(self, tmp_path):
        (tmp_path / "prompt_trace_summary.json").write_text("{}")
        (tmp_path / "agent_run_trace.jsonl").write_text("{}\n")
        (tmp_path / "agent_run_trace_summary.json").write_text("{}")
        (tmp_path / "job_flow.json").write_text("{}")
        (tmp_path / "manifest.json").write_text("{}")

        job = _FakeJob("completed", [_FakeTask("T001", "applied_to_job_workspace", "pass")])
        promo = _FakePromo("dry_run")
        ts = {"provider_call_count": 2}

        audit = _build_final_audit(job, promo, str(tmp_path), token_summary=ts)
        assert audit["status"] == "READY_FOR_APPROVAL"
        assert audit["prompt_trace_available"] is True
        assert audit["agent_run_trace_available"] is True
        assert audit["job_flow_json_available"] is True
        assert audit["missing_observability_artifacts"] == []

    def test_needs_review_when_prompt_trace_missing(self, tmp_path):
        (tmp_path / "agent_run_trace.jsonl").write_text("{}\n")
        (tmp_path / "agent_run_trace_summary.json").write_text("{}")
        (tmp_path / "job_flow.json").write_text("{}")
        (tmp_path / "manifest.json").write_text("{}")

        job = _FakeJob("completed", [_FakeTask("T001", "applied_to_job_workspace", "pass")])
        promo = _FakePromo("dry_run")
        ts = {"provider_call_count": 2}

        audit = _build_final_audit(job, promo, str(tmp_path), token_summary=ts)
        assert audit["status"] == "NEEDS_REVIEW"
        assert audit["prompt_trace_available"] is False
        assert "prompt_trace" in audit["missing_observability_artifacts"]

    def test_needs_review_when_agent_trace_missing(self, tmp_path):
        (tmp_path / "prompt_trace_summary.json").write_text("{}")
        (tmp_path / "job_flow.json").write_text("{}")
        (tmp_path / "manifest.json").write_text("{}")

        job = _FakeJob("completed", [_FakeTask("T001", "applied_to_job_workspace", "pass")])
        promo = _FakePromo("dry_run")
        ts = {"provider_call_count": 2}

        audit = _build_final_audit(job, promo, str(tmp_path), token_summary=ts)
        assert audit["status"] == "NEEDS_REVIEW"
        assert audit["agent_run_trace_available"] is False
        assert "agent_run_trace" in audit["missing_observability_artifacts"]

    def test_needs_review_when_job_flow_json_missing(self, tmp_path):
        (tmp_path / "prompt_trace_summary.json").write_text("{}")
        (tmp_path / "agent_run_trace.jsonl").write_text("{}\n")
        (tmp_path / "agent_run_trace_summary.json").write_text("{}")
        (tmp_path / "manifest.json").write_text("{}")

        job = _FakeJob("completed", [_FakeTask("T001", "applied_to_job_workspace", "pass")])
        promo = _FakePromo("dry_run")
        ts = {"provider_call_count": 2}

        audit = _build_final_audit(job, promo, str(tmp_path), token_summary=ts)
        assert audit["status"] == "NEEDS_REVIEW"
        assert "job_flow_json" in audit["missing_observability_artifacts"]

    def test_needs_review_when_trace_summary_missing(self, tmp_path):
        (tmp_path / "prompt_trace_summary.json").write_text("{}")
        (tmp_path / "agent_run_trace.jsonl").write_text("{}\n")
        (tmp_path / "job_flow.json").write_text("{}")
        (tmp_path / "manifest.json").write_text("{}")

        job = _FakeJob("completed", [_FakeTask("T001", "applied_to_job_workspace", "pass")])
        promo = _FakePromo("dry_run")
        ts = {"provider_call_count": 2}

        audit = _build_final_audit(job, promo, str(tmp_path), token_summary=ts)
        assert audit["status"] == "NEEDS_REVIEW"
        assert "agent_run_trace_summary" in audit["missing_observability_artifacts"]

    def test_blocked_overrides_missing_artifacts(self, tmp_path):
        job = _FakeJob("blocked", [_FakeTask("T001", "blocked", error="test failed")])
        promo = _FakePromo("blocked", "not_ready")

        audit = _build_final_audit(job, promo, str(tmp_path))
        assert audit["status"] == "BLOCKED"

    def test_token_summary_available_false_when_no_calls(self, tmp_path):
        job = _FakeJob("completed", [_FakeTask("T001", "applied_to_job_workspace")])
        promo = _FakePromo("dry_run")
        ts = {"provider_call_count": 0}

        audit = _build_final_audit(job, promo, str(tmp_path), token_summary=ts)
        assert audit["token_summary_available"] is False

    def test_evidence_bundle_available_true(self, tmp_path):
        (tmp_path / "manifest.json").write_text("{}")
        (tmp_path / "prompt_trace_summary.json").write_text("{}")
        (tmp_path / "agent_run_trace.jsonl").write_text("{}\n")

        job = _FakeJob("completed", [_FakeTask("T001", "applied_to_job_workspace")])
        promo = _FakePromo("dry_run")
        audit = _build_final_audit(job, promo, str(tmp_path), token_summary={"provider_call_count": 1})
        assert audit["evidence_bundle_available"] is True

    def test_explicit_overrides_for_availability(self, tmp_path):
        (tmp_path / "agent_run_trace_summary.json").write_text("{}")
        (tmp_path / "job_flow.json").write_text("{}")
        (tmp_path / "manifest.json").write_text("{}")

        job = _FakeJob("completed", [_FakeTask("T001", "applied_to_job_workspace")])
        promo = _FakePromo("dry_run")
        audit = _build_final_audit(
            job, promo, str(tmp_path),
            prompt_trace_available=True,
            agent_run_trace_available=True,
            job_flow_json_available=True,
            token_summary={"provider_call_count": 1},
        )
        assert audit["status"] == "READY_FOR_APPROVAL"

    def test_needs_review_when_manifest_missing(self, tmp_path):
        (tmp_path / "prompt_trace_summary.json").write_text("{}")
        (tmp_path / "agent_run_trace.jsonl").write_text("{}\n")
        (tmp_path / "agent_run_trace_summary.json").write_text("{}")
        (tmp_path / "job_flow.json").write_text("{}")

        job = _FakeJob("completed", [_FakeTask("T001", "applied_to_job_workspace", "pass")])
        promo = _FakePromo("dry_run")
        ts = {"provider_call_count": 2}

        audit = _build_final_audit(job, promo, str(tmp_path), token_summary=ts)
        assert audit["status"] == "NEEDS_REVIEW"
        assert "manifest" in audit["missing_observability_artifacts"]

    def test_needs_review_when_token_summary_missing(self, tmp_path):
        (tmp_path / "prompt_trace_summary.json").write_text("{}")
        (tmp_path / "agent_run_trace.jsonl").write_text("{}\n")
        (tmp_path / "agent_run_trace_summary.json").write_text("{}")
        (tmp_path / "job_flow.json").write_text("{}")
        (tmp_path / "manifest.json").write_text("{}")

        job = _FakeJob("completed", [_FakeTask("T001", "applied_to_job_workspace", "pass")])
        promo = _FakePromo("dry_run")

        audit = _build_final_audit(job, promo, str(tmp_path))
        assert audit["status"] == "NEEDS_REVIEW"
        assert "token_summary" in audit["missing_observability_artifacts"]

    def test_needs_review_when_token_summary_zero_calls(self, tmp_path):
        (tmp_path / "prompt_trace_summary.json").write_text("{}")
        (tmp_path / "agent_run_trace.jsonl").write_text("{}\n")
        (tmp_path / "agent_run_trace_summary.json").write_text("{}")
        (tmp_path / "job_flow.json").write_text("{}")
        (tmp_path / "manifest.json").write_text("{}")

        job = _FakeJob("completed", [_FakeTask("T001", "applied_to_job_workspace", "pass")])
        promo = _FakePromo("dry_run")
        ts = {"provider_call_count": 0}

        audit = _build_final_audit(job, promo, str(tmp_path), token_summary=ts)
        assert audit["status"] == "NEEDS_REVIEW"
        assert "token_summary" in audit["missing_observability_artifacts"]


class TestSanitizeShareablePaths:
    def test_sanitizes_staging_paths(self):
        data = {"path": "/tmp/remedy-pingpong-abc123/staging/file.py"}
        result = _sanitize_shareable_paths(data)
        assert "/tmp/remedy-pingpong-" not in result["path"]
        assert "[staging]" in result["path"]

    def test_sanitizes_nested_dicts(self):
        data = {"outer": {"inner": "/tmp/remedy-pingpong-abc/foo"}}
        result = _sanitize_shareable_paths(data)
        assert "/tmp/remedy-pingpong-" not in str(result)

    def test_sanitizes_lists(self):
        data = {"files": ["/tmp/remedy-pingpong-x/a.py", "safe.py"]}
        result = _sanitize_shareable_paths(data)
        assert "/tmp/remedy-pingpong-" not in str(result)
        assert "safe.py" in result["files"]

    def test_sanitizes_home_paths(self):
        data = {"path": "/home/user/repo/file.py"}
        result = _sanitize_shareable_paths(data)
        assert result["path"] == "[local]/repo/file.py"

    def test_sanitizes_users_paths(self):
        data = {"path": "/Users/alice/dev/repo/file.py"}
        result = _sanitize_shareable_paths(data)
        assert result["path"] == "[local]/dev/repo/file.py"

    def test_sanitizes_private_paths(self):
        data = {"path": "/private/var/tmp/file.py"}
        result = _sanitize_shareable_paths(data)
        assert "/private/" not in result["path"]
        assert result["path"].startswith("[local]")

    def test_sanitizes_tmp_paths(self):
        data = {"path": "/tmp/pytest-abc123/file.py"}
        result = _sanitize_shareable_paths(data)
        assert result["path"] == "[tmpdir]/file.py"

    def test_preserves_relative_paths(self):
        data = {"path": "src/main.py"}
        result = _sanitize_shareable_paths(data)
        assert result["path"] == "src/main.py"

    def test_preserves_safe_labels(self):
        data = {"path": "[staging]/file.py"}
        result = _sanitize_shareable_paths(data)
        assert result["path"] == "[staging]/file.py"


class TestCockpitBridgeAdapter:
    def test_job_plan_adapter_has_required_fields(self):
        from packages.orchestration.ui_server import _JobPlanAdapter

        class FakeTask:
            task_id = "T001"
            title = "Fix bug"
            status = "applied_to_job_workspace"

        class FakePlan:
            job_id = "abc123"
            job_title = "Test Job"
            status = "completed"
            tasks = [FakeTask()]

        adapter = _JobPlanAdapter(FakePlan())
        assert adapter.id == "abc123"
        assert adapter.name == "Test Job"
        assert len(adapter.tasks) == 1
        assert adapter.tasks[0].id == "T001"
        assert adapter.tasks[0].description == "Fix bug"
        assert adapter.tasks[0].status.value == "completed"
        assert adapter.artifacts == []
        assert adapter._is_job_plan is True

    def test_job_plan_adapter_maps_statuses(self):
        from packages.orchestration.ui_server import _JobPlanAdapter

        class FakeTask:
            task_id = "T001"
            title = "Test"
            status = "blocked"

        class FakePlan:
            job_id = "x"
            job_title = "J"
            status = "blocked"
            tasks = [FakeTask()]

        adapter = _JobPlanAdapter(FakePlan())
        assert adapter.state.value == "blocked"
        assert adapter.tasks[0].status.value == "blocked"

    def test_load_job_accepts_uuid(self):
        from packages.orchestration.ui_server import _load_job
        _, err = _load_job("not-a-valid-id-at-all!!!!")
        assert err is not None

    def test_load_job_returns_not_found_for_missing_plan(self):
        from packages.orchestration.ui_server import _load_job
        _, err = _load_job("deadbeef12345678")
        assert err is not None
        assert err[0] == 404

    def test_evidence_index_resolution(self, tmp_path):
        from packages.orchestration.ui_server import _resolve_evidence_dir
        result = _resolve_evidence_dir("nonexistent_job_id_12345678")
        assert result is None
