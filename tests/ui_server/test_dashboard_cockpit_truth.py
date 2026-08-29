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

    # Finding R-0738. The apply fold used to answer by MEMBERSHIP, so a task where
    # ONE change of many had applied read "applied" — indistinguishable from a task
    # where all of them had. It now agrees or says "partial", the shape the proof
    # fold beside it has always had. These live in this class so they build their
    # chains through the helpers above rather than through a second idiom.

    def test_all_applied_still_reads_applied(self):
        from packages.orchestration.ui_server import _task_truth_maps
        chain = self._chain([
            self._change("t1", "applied", "verified"),
            self._change("t1", "applied", "verified"),
            self._change("t1", "applied", "verified"),
        ])
        _, apply = _task_truth_maps(chain)
        assert apply["t1"] == "applied", (
            "unanimous applies were right before the agreement fold and must stay "
            "right after it; only the mixed case was ever allowed to move"
        )

    def test_all_reverted_still_reads_reverted(self):
        from packages.orchestration.ui_server import _task_truth_maps
        chain = self._chain([
            self._change("t1", "reverted", "incomplete"),
            self._change("t1", "reverted", "incomplete"),
        ])
        _, apply = _task_truth_maps(chain)
        assert apply["t1"] == "reverted"

    def test_all_not_applied_still_reads_not_applied(self):
        from packages.orchestration.ui_server import _task_truth_maps
        chain = self._chain([
            self._change("t1", "not_applied", "not_applicable"),
            self._change("t1", "not_applied", "not_applicable"),
        ])
        _, apply = _task_truth_maps(chain)
        assert apply["t1"] == "not_applied"

    def test_some_applied_and_some_not_reads_partial_and_never_applied(self):
        # THE DISCRIMINATOR for the whole finding: this exact chain read "applied"
        # before the fold changed shape, which is the state hunk-level approval
        # produces most often of all.
        from packages.orchestration.ui_server import _task_truth_maps
        chain = self._chain([
            self._change("t1", "applied", "verified"),
            self._change("t1", "not_applied", "not_applicable"),
            self._change("t1", "not_applied", "not_applicable"),
        ])
        _, apply = _task_truth_maps(chain)
        assert apply["t1"] == "partial"
        assert apply["t1"] != "applied", (
            "a task with one applied change out of three must never claim the "
            "label a fully applied task carries (finding R-0738)"
        )

    def test_one_applied_and_one_reverted_reads_partial(self):
        from packages.orchestration.ui_server import _task_truth_maps
        chain = self._chain([
            self._change("t1", "applied", "verified"),
            self._change("t1", "reverted", "incomplete"),
        ])
        _, apply = _task_truth_maps(chain)
        assert apply["t1"] == "partial"

    def test_a_missing_apply_state_never_by_itself_produces_applied(self):
        # The getattr default is the empty string, and an absent attribute is not
        # evidence that anything was applied — the reading the old `else` gave and
        # the third arm of the new fold preserves.
        from types import SimpleNamespace

        from packages.orchestration.ui_server import _task_truth_maps
        no_state = SimpleNamespace(task_id="t1", proof_status="verified")
        chain = self._chain([no_state, self._change("t1", "applied", "verified")])
        _, apply = _task_truth_maps(chain)
        assert apply["t1"] == "partial"
        alone = self._chain([SimpleNamespace(task_id="t2", proof_status="verified")])
        _, apply_alone = _task_truth_maps(alone)
        assert apply_alone["t2"] == "not_applied"


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
        for key in ("runs", "passed", "failed", "latest_state"):
            assert key in dash["metrics"]["tests"]

    def test_repair_section_safe_shape(self):
        job = Job(name="t")
        repair = _build_dashboard(job)["repair"]
        assert repair["attempt_count"] == 0
        assert repair["pending_approval_count"] == 0
        assert repair["next_safe_action"] == ""  # no approve affordance without evidence
        assert repair["source"] == "repair_attempts_v1"

    def test_overnight_section_present(self):
        job = Job(name="t")
        dash = _build_dashboard(job)
        assert "overnight" in dash
        ov = dash["overnight"]
        assert "readiness_level" in ov
        assert "can_run_unattended" in ov
        # No fabricated "ready" overnight state without evidence/policy.
        assert ov["can_run_unattended"] in (False, "unknown")

    def test_provider_trust_section_present(self):
        # Read-only Provider Trust Gate summary (Step 1325).
        job = Job(name="t")
        dash = _build_dashboard(job)
        assert "provider_trust" in dash
        pt = dash["provider_trust"]
        assert "report_count" in pt
        assert "rejected" in pt
        assert "pending_provider_repair_approval" in pt
        assert "materialized_count" in pt
        assert "materialization_failed_count" in pt

    def test_provider_verification_section_present(self):
        # Read-only Provider Trust Verification v1 summary (Step 1559).
        job = Job(name="t")
        dash = _build_dashboard(job)
        assert "provider_verification" in dash
        pv = dash["provider_verification"]
        assert "verification_count" in pv
        assert "passed" in pv
        assert "needs_review" in pv
        assert "rejected" in pv
        assert "pending_approval_after_verification" in pv
        # No buttons / mutation surface.
        assert "buttons" not in pv and "actions" not in pv

    def test_builder_routing_section_present(self):
        # Read-only Expensive Builder Routing v0 summary (Step 1595).
        job = Job(name="t")
        dash = _build_dashboard(job)
        assert "builder_routing" in dash
        br = dash["builder_routing"]
        assert "routing_decision_count" in br
        assert "latest_tier" in br
        assert "external_builder_recommended" in br
        assert "next_safe_action_label" in br
        assert "buttons" not in br and "actions" not in br

    def test_local_candidate_section_present(self):
        # Read-only Automated Local Candidate Generator v0 summary (Step 1627).
        job = Job(name="t")
        dash = _build_dashboard(job)
        assert "local_candidate" in dash
        lc = dash["local_candidate"]
        assert "enabled" in lc
        assert "run_count" in lc
        assert "pending_approval_count" in lc
        assert "buttons" not in lc and "actions" not in lc

    def test_candidate_quality_section_present(self):
        # Read-only Local Candidate Quality Evaluation v1 summary (Step 1664).
        job = Job(name="t")
        dash = _build_dashboard(job)
        assert "candidate_quality" in dash
        cq = dash["candidate_quality"]
        assert "evaluation_count" in cq
        assert "latest_outcome" in cq
        assert "pending_with_quality_count" in cq
        assert "buttons" not in cq and "actions" not in cq

    def test_external_builder_section_present(self):
        # Read-only External Builder Sandbox v0 summary (Step 1693).
        job = Job(name="t")
        dash = _build_dashboard(job)
        assert "external_builder" in dash
        eb = dash["external_builder"]
        assert "external_packages" in eb
        assert "external_submissions" in eb
        assert "verified_external_candidates" in eb
        assert eb["live"] is False
        assert "buttons" not in eb and "actions" not in eb

    def test_worker_registry_section_present(self):
        # Read-only Worker Registry + Route Policy v0 summary (Step 1730).
        job = Job(name="t")
        dash = _build_dashboard(job)
        assert "worker_registry" in dash
        wr = dash["worker_registry"]
        assert "available_workers_count" in wr
        assert "selected_workers" in wr
        assert "blocked_workers" in wr
        assert "recommended_next_action" in wr
        assert wr["live"] is False
        assert "buttons" not in wr and "actions" not in wr
        # No execution affordance in the recommended next action.
        assert " run" not in str(wr.get("recommended_next_action", ""))

    def test_repair_request_section_present(self):
        # Read-only Repair Request Builder summary (Step 1381).
        job = Job(name="t")
        dash = _build_dashboard(job)
        assert "repair_request" in dash
        rr = dash["repair_request"]
        assert "request_package_count" in rr
        assert "pending_response_count" in rr

    def test_self_dogfood_section_present(self):
        # Read-only Self-Dogfood summary (Step 1418).
        job = Job(name="t")
        dash = _build_dashboard(job)
        assert "self_dogfood" in dash
        sd = dash["self_dogfood"]
        assert "self_improvement_item_count" in sd
        assert "pending_evaluation_count" in sd

    def test_self_execution_section_present(self):
        # Read-only Self-Dogfood Execution summary (Step 1445).
        job = Job(name="t")
        dash = _build_dashboard(job)
        assert "self_execution" in dash
        se = dash["self_execution"]
        assert "attempt_count" in se
        assert "pending_candidate_count" in se
        assert "pending_approval_count" in se

    def test_orchestrator_section_present(self):
        # Read-only Orchestrator Brain summary (Step 1484).
        job = Job(name="t")
        dash = _build_dashboard(job)
        assert "orchestrator" in dash
        ob = dash["orchestrator"]
        assert "decision_count" in ob
        assert "latest_stop_reason" in ob
        assert "model_routing_tier" in ob

    def test_local_advisor_section_present(self):
        # Read-only Local Model Advisor summary (Step 1520).
        job = Job(name="t")
        dash = _build_dashboard(job)
        assert "local_advisor" in dash
        la = dash["local_advisor"]
        assert "run_count" in la
        assert "enabled" in la
        assert "available" in la
        assert "latest_status" in la
        # No fabricated availability without a real local advisor run.
        assert la["available"] in (False, "unknown")

    def test_overnight_run_section_present(self):
        # Read-only Bounded Overnight Executor run summary (Step 1292).
        job = Job(name="t")
        dash = _build_dashboard(job)
        assert "overnight_run" in dash
        ovr = dash["overnight_run"]
        assert "latest_status" in ovr
        assert "stop_reason" in ovr
        assert "checkpoint_count" in ovr
        # No fabricated running state without a durable run record.
        assert ovr.get("executed_action", "") in ("", "none")

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
