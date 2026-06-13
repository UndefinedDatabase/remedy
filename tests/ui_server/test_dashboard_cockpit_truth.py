"""Tests for Operator Cockpit dashboard truth (Step 1181).

Covers the new read-only dashboard sections: metrics.tests, metrics.proof,
snapshot, continuation. Verifies payload shape, explicit "unknown" when the
data root is unavailable (never faked zeros), and redaction (no paths, diffs,
or tracebacks in the JSON payload).
"""
from __future__ import annotations

import json
from pathlib import Path

from packages.core.models import Job
from packages.orchestration import ui_server
from packages.orchestration.ui_server import (
    _build_continuation_section,
    _build_dashboard,
    _build_metrics_tests,
    _build_snapshot_section,
    _metrics_proof_from_chain,
)


class TestMetricsTests:
    def test_none_when_no_tests(self):
        m = _build_metrics_tests([])
        assert m == {"runs": 0, "passed": 0, "failed": 0, "latest_state": "none"}

    def test_counts_pass_and_fail(self):
        events = [
            {"event": "test_run_completed", "metadata": {"exit_code": 0}},
            {"event": "test_run_completed", "metadata": {"exit_code": 1}},
            {"event": "test_run_completed", "metadata": {"exit_code": 0}},
        ]
        m = _build_metrics_tests(events)
        assert m["runs"] == 3
        assert m["passed"] == 2
        assert m["failed"] == 1

    def test_latest_state_uses_last_run(self):
        events = [
            {"event": "test_run_completed", "metadata": {"exit_code": 0}},
            {"event": "test_run_completed", "metadata": {"exit_code": 1}},
        ]
        assert _build_metrics_tests(events)["latest_state"] == "fail"

    def test_missing_exit_code_not_counted_as_fail(self):
        # An event without exit_code must not be mislabeled as a failure (R-0071).
        events = [
            {"event": "test_run_completed", "metadata": {"exit_code": 0}},
            {"event": "test_run_completed", "metadata": {}},
        ]
        m = _build_metrics_tests(events)
        assert m["runs"] == 2
        assert m["passed"] == 1
        assert m["failed"] == 0
        assert m["latest_state"] == "none"


class TestUnknownWhenNoDataDir:
    def test_proof_unknown(self):
        # None chain (data root unavailable) -> explicit unknown, never verified.
        m = _metrics_proof_from_chain(None)
        assert m == {"total_changes": "unknown", "verified": "unknown", "state": "unknown"}

    def test_snapshot_unknown(self):
        job = Job(name="t")
        s = _build_snapshot_section(job, None)
        assert s["apply_records"] == "unknown"
        assert s["verified"] == "unknown"
        assert s["reverted"] == "unknown"
        assert s["drift_detected"] == "unknown"
        assert s["source"] == "unavailable"

    def test_continuation_unknown(self):
        job = Job(name="t")
        c = _build_continuation_section(job, [], None)
        assert c == {
            "available": "unknown",
            "last_result": "unknown",
            "last_stop_reason": "unknown",
        }


class TestTaskTruthMaps:
    """Per-task proof/apply truth is authoritative, never event/count-derived."""

    def _change(self, task_id, apply_state, proof_status):
        from packages.orchestration.proof_chain import ProofChange
        return ProofChange(
            target_path="a.py", intent_id="i", task_id=task_id, task_title="t",
            artifact_id="art", patch_intent_id="pi", approval_state="approved",
            apply_state=apply_state, test_state="passed", test_link="task_linked",
            proof_status=proof_status, safe_summary="", next_safe_action="",
        )

    def _chain(self, changes):
        from types import SimpleNamespace
        return SimpleNamespace(changes=changes)

    def test_none_chain_empty_maps(self):
        from packages.orchestration.ui_server import _task_truth_maps
        assert _task_truth_maps(None) == ({}, {})

    def test_verified_only_when_all_verified(self):
        from packages.orchestration.ui_server import _task_truth_maps
        chain = self._chain([
            self._change("t1", "applied", "verified"),
            self._change("t1", "applied", "verified"),
            self._change("t2", "applied", "incomplete"),
        ])
        proof, apply = _task_truth_maps(chain)
        assert proof["t1"] == "verified"
        assert proof["t2"] == "incomplete"
        assert apply["t1"] == "applied"

    def test_failed_change_makes_task_failed(self):
        from packages.orchestration.ui_server import _task_truth_maps
        chain = self._chain([
            self._change("t1", "applied", "verified"),
            self._change("t1", "applied", "failed"),
        ])
        proof, _ = _task_truth_maps(chain)
        assert proof["t1"] == "failed"

    def test_reverted_apply_state(self):
        from packages.orchestration.ui_server import _task_truth_maps
        chain = self._chain([self._change("t1", "reverted", "incomplete")])
        _, apply = _task_truth_maps(chain)
        assert apply["t1"] == "reverted"

    def test_proof_not_verified_from_event_presence(self):
        # A proof_collected event must NOT make a task "verified" — only the
        # authoritative chain does (R-0076). With no data root the per-task proof
        # is "unknown", never "verified".
        job = Job(name="t", tasks=[__import__("packages.core.models", fromlist=["Task"]).Task(description="x")])
        import packages.orchestration.ui_server as us
        # Force the unknown path (no data root): proof chain is None.
        orig = us._resolve_dashboard_data_dir
        us._resolve_dashboard_data_dir = lambda: None
        try:
            dash = us._build_dashboard(job)
        finally:
            us._resolve_dashboard_data_dir = orig
        for t in dash["tasks"]:
            assert t["proof_status"] != "verified"
            assert t["apply_status"] != "applied"


class TestContinuationLastResult:
    def test_last_result_from_stopped_event(self, tmp_path: Path):
        job = Job(name="t")
        events = [
            {"event": "do_continue_stopped",
             "metadata": {"stop_reason": "completed_verified"}},
        ]
        c = _build_continuation_section(job, events, tmp_path)
        assert c["last_result"] == "completed_verified"
        assert c["last_stop_reason"] == "completed_verified"
        assert c["available"] is False  # no approved intents on empty job

    def test_non_result_stop_reason_maps_to_none(self, tmp_path: Path):
        job = Job(name="t")
        events = [
            {"event": "do_continue_stopped",
             "metadata": {"stop_reason": "lease_unavailable"}},
        ]
        c = _build_continuation_section(job, events, tmp_path)
        assert c["last_result"] == "none"
        assert c["last_stop_reason"] == "lease_unavailable"

    def test_no_stopped_event(self, tmp_path: Path):
        job = Job(name="t")
        c = _build_continuation_section(job, [], tmp_path)
        assert c["last_result"] == "none"
        assert c["last_stop_reason"] == "none"


class TestDashboardShape:
    def test_payload_has_cockpit_sections(self):
        job = Job(name="t")
        dash = _build_dashboard(job)
        assert "tests" in dash["metrics"]
        assert "proof" in dash["metrics"]
        assert "snapshot" in dash
        assert "continuation" in dash
        assert "repair" in dash

    def test_repair_section_safe_shape(self):
        job = Job(name="t")
        repair = _build_dashboard(job)["repair"]
        assert repair["attempt_count"] == 0
        assert repair["pending_approval_count"] == 0
        assert repair["next_safe_action"] == ""  # no approve affordance without evidence
        assert repair["source"] == "repair_attempts_v1"
        for key in ("runs", "passed", "failed", "latest_state"):
            assert key in dash["metrics"]["tests"]

    def test_unknown_when_data_dir_unavailable(self, monkeypatch):
        monkeypatch.setattr(ui_server, "_resolve_dashboard_data_dir", lambda: None)
        job = Job(name="t")
        dash = _build_dashboard(job)
        assert dash["snapshot"]["source"] == "unavailable"
        assert dash["continuation"]["available"] == "unknown"
        assert dash["metrics"]["proof"]["state"] == "unknown"

    def test_redaction_no_paths_diffs_tracebacks(self):
        job = Job(name="t")
        payload = json.dumps(_build_dashboard(job), default=str)
        assert "/home/" not in payload
        assert "Traceback" not in payload
        assert "diff --git" not in payload
