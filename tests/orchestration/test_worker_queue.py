"""Tests: worker queue, lifecycle, lease, run-once, bounded loop, pause/cancel, stale.

All tests use one-shot mode with temp dirs. No unbounded loops, no background processes.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import pytest

from packages.orchestration.worker_queue import (
    LIFECYCLE_STATES,
    QueueEntry,
    WorkerLease,
    WorkerResult,
    WorkerStatus,
    cancel_job,
    claim_job,
    detect_stale,
    enqueue_job,
    export_queue_entry_json,
    export_worker_result_json,
    export_worker_status_json,
    get_next_job,
    get_worker_status,
    is_valid_transition,
    list_queued,
    pause_job,
    release_lease,
    resume_queued,
    run_worker_loop,
    run_worker_once,
    transition_state,
)


class TestLifecycleModel:
    """Step 436: Job lifecycle states and transitions."""

    def test_all_states_defined(self):
        assert len(LIFECYCLE_STATES) >= 10

    def test_valid_transition_queued_to_claimed(self):
        assert is_valid_transition("queued", "claimed")

    def test_invalid_transition_completed_to_running(self):
        assert not is_valid_transition("completed", "running")

    def test_cancelled_has_no_transitions(self):
        assert not is_valid_transition("cancelled", "queued")

    def test_running_to_waiting_for_approval(self):
        assert is_valid_transition("running", "waiting_for_approval")

    def test_paused_to_queued(self):
        assert is_valid_transition("paused", "queued")

    def test_stale_to_queued(self):
        assert is_valid_transition("stale", "queued")


class TestLocalQueue:
    """Step 437: Enqueue, list, get next."""

    def test_enqueue_one_job(self, tmp_path):
        entry = enqueue_job("job-1", tmp_path)
        assert entry.lifecycle_state == "queued"
        assert entry.job_id == "job-1"

    def test_list_queued(self, tmp_path):
        enqueue_job("job-a", tmp_path)
        enqueue_job("job-b", tmp_path)
        entries = list_queued(tmp_path)
        assert len(entries) == 2

    def test_get_next_returns_first_queued(self, tmp_path):
        enqueue_job("job-a", tmp_path)
        enqueue_job("job-b", tmp_path)
        nxt = get_next_job(tmp_path)
        assert nxt is not None
        assert nxt.job_id == "job-a"

    def test_paused_skipped(self, tmp_path):
        enqueue_job("job-1", tmp_path)
        pause_job("job-1", tmp_path)
        assert get_next_job(tmp_path) is None

    def test_cancelled_skipped(self, tmp_path):
        enqueue_job("job-1", tmp_path)
        cancel_job("job-1", tmp_path)
        assert get_next_job(tmp_path) is None

    def test_completed_not_picked(self, tmp_path):
        enqueue_job("job-1", tmp_path)
        claim_job("job-1", "w1", tmp_path)
        transition_state("job-1", "running", tmp_path)
        transition_state("job-1", "completed", tmp_path)
        assert get_next_job(tmp_path) is None

    def test_corrupt_queue_safe(self, tmp_path):
        (tmp_path / "queue").mkdir()
        (tmp_path / "queue" / "bad.json").write_text("not json")
        entries = list_queued(tmp_path)
        assert len(entries) == 0


class TestWorkerLock:
    """Step 438: Claim, lease, release."""

    def test_claim_job(self, tmp_path):
        enqueue_job("job-1", tmp_path)
        lease = claim_job("job-1", "worker-A", tmp_path)
        assert lease is not None
        assert lease.worker_id == "worker-A"

    def test_second_worker_blocked(self, tmp_path):
        enqueue_job("job-1", tmp_path)
        claim_job("job-1", "worker-A", tmp_path)
        lease2 = claim_job("job-1", "worker-B", tmp_path)
        assert lease2 is None

    def test_lease_released_on_completion(self, tmp_path):
        enqueue_job("job-1", tmp_path)
        claim_job("job-1", "w1", tmp_path)
        transition_state("job-1", "running", tmp_path)
        transition_state("job-1", "completed", tmp_path)
        entries = list_queued(tmp_path)
        completed = [e for e in entries if e.job_id == "job-1"]
        assert completed[0].worker_id == ""

    def test_release_lease(self, tmp_path):
        enqueue_job("job-1", tmp_path)
        claim_job("job-1", "w1", tmp_path)
        release_lease("job-1", tmp_path)
        entries = list_queued(tmp_path)
        e = [x for x in entries if x.job_id == "job-1"][0]
        assert e.worker_id == ""


class TestWorkerRunOnce:
    """Step 439: One-shot worker."""

    def test_no_job_idle(self, tmp_path):
        result = run_worker_once(tmp_path)
        assert result.action_taken == "idle"
        assert result.why_it_stopped == "no_queued_jobs"

    def test_fixture_job_completes(self, tmp_path):
        enqueue_job("job-1", tmp_path)
        result = run_worker_once(tmp_path, provider="fixture")
        assert result.jobs_processed == 1
        assert result.last_lifecycle_state == "completed"

    def test_approval_stops(self, tmp_path):
        enqueue_job("job-1", tmp_path)
        result = run_worker_once(tmp_path, provider="ollama")
        assert result.last_lifecycle_state == "waiting_for_approval"
        assert result.why_it_stopped == "approval_required"

    def test_json_output_safe(self, tmp_path):
        enqueue_job("job-1", tmp_path)
        result = run_worker_once(tmp_path, provider="fixture")
        data = export_worker_result_json(result)
        assert data["redaction"] == "safe_metadata_only"
        full = json.dumps(data)
        for bad in ("raw_output", "command_output", "traceback", "stderr"):
            assert bad not in full

    def test_specific_job(self, tmp_path):
        result = run_worker_once(tmp_path, job_id="new-job", provider="none")
        assert result.last_job_id == "new-job"
        assert result.jobs_processed == 1


class TestBoundedLoop:
    """Step 440: Bounded worker loop."""

    def test_max_jobs_stops(self, tmp_path):
        enqueue_job("j1", tmp_path)
        enqueue_job("j2", tmp_path)
        result = run_worker_loop(tmp_path, max_jobs=1, provider="fixture")
        assert result.jobs_processed == 1

    def test_idle_timeout_stops(self, tmp_path):
        result = run_worker_loop(tmp_path, max_jobs=5, max_seconds=2, idle_timeout=1)
        assert result.why_it_stopped == "idle_timeout"

    def test_no_cpu_spin(self, tmp_path):
        start = time.monotonic()
        run_worker_loop(tmp_path, max_jobs=1, max_seconds=1, idle_timeout=0)
        elapsed = time.monotonic() - start
        assert elapsed < 5


class TestHeartbeatAndStatus:
    """Step 441: Worker status."""

    def test_status_after_run(self, tmp_path):
        enqueue_job("job-1", tmp_path)
        run_worker_once(tmp_path, provider="fixture")
        status = get_worker_status(tmp_path)
        assert status.processed_job_count >= 1

    def test_idle_status(self, tmp_path):
        status = get_worker_status(tmp_path)
        assert status.lifecycle_state == "idle"

    def test_status_export_safe(self, tmp_path):
        status = get_worker_status(tmp_path)
        data = export_worker_status_json(status)
        assert data["redaction"] == "safe_metadata_only"


class TestPauseAndCancel:
    """Step 442: Pause and cancel."""

    def test_pause_queued_job(self, tmp_path):
        enqueue_job("j1", tmp_path)
        entry = pause_job("j1", tmp_path)
        assert entry.lifecycle_state == "paused"

    def test_paused_not_picked(self, tmp_path):
        enqueue_job("j1", tmp_path)
        pause_job("j1", tmp_path)
        assert get_next_job(tmp_path) is None

    def test_resume_paused(self, tmp_path):
        enqueue_job("j1", tmp_path)
        pause_job("j1", tmp_path)
        entry = resume_queued("j1", tmp_path)
        assert entry.lifecycle_state == "queued"

    def test_cancel_queued(self, tmp_path):
        enqueue_job("j1", tmp_path)
        entry = cancel_job("j1", tmp_path)
        assert entry.lifecycle_state == "cancelled"

    def test_cancel_running_marks_cancelling(self, tmp_path):
        enqueue_job("j1", tmp_path)
        claim_job("j1", "w1", tmp_path)
        transition_state("j1", "running", tmp_path)
        entry = cancel_job("j1", tmp_path)
        assert entry.lifecycle_state == "cancelling"

    def test_cancel_completed_fails(self, tmp_path):
        enqueue_job("j1", tmp_path)
        claim_job("j1", "w1", tmp_path)
        transition_state("j1", "running", tmp_path)
        transition_state("j1", "completed", tmp_path)
        entry = cancel_job("j1", tmp_path)
        assert entry is None


class TestStaleRecovery:
    """Step 445: Stale worker detection and recovery."""

    def test_stale_detected(self, tmp_path):
        enqueue_job("j1", tmp_path)
        claim_job("j1", "w1", tmp_path)
        entry = list_queued(tmp_path)[0]
        entry.lease_expires_at = "2020-01-01T00:00:00+00:00"
        from packages.orchestration.worker_queue import _save_entry
        _save_entry(tmp_path, entry)
        stale = detect_stale(tmp_path)
        assert len(stale) >= 1
        assert stale[0].lifecycle_state == "stale"

    def test_stale_can_be_reclaimed(self, tmp_path):
        enqueue_job("j1", tmp_path)
        claim_job("j1", "w1", tmp_path)
        entry = list_queued(tmp_path)[0]
        entry.lease_expires_at = "2020-01-01T00:00:00+00:00"
        entry.lifecycle_state = "stale"
        from packages.orchestration.worker_queue import _save_entry
        _save_entry(tmp_path, entry)
        lease = claim_job("j1", "w2", tmp_path)
        assert lease is not None
        assert lease.worker_id == "w2"


class TestCatalogAndCLI:
    """Step 446: Commands in catalog."""

    def test_worker_run_in_catalog(self):
        from apps.cli.command_catalog import CATALOG
        ids = {e.command_id for e in CATALOG}
        assert "worker.run" in ids

    def test_worker_status_in_catalog(self):
        from apps.cli.command_catalog import CATALOG
        ids = {e.command_id for e in CATALOG}
        assert "worker.status" in ids

    def test_job_enqueue_in_catalog(self):
        from apps.cli.command_catalog import CATALOG
        ids = {e.command_id for e in CATALOG}
        assert "job.enqueue" in ids

    def test_job_pause_in_catalog(self):
        from apps.cli.command_catalog import CATALOG
        ids = {e.command_id for e in CATALOG}
        assert "job.pause" in ids

    def test_job_cancel_in_catalog(self):
        from apps.cli.command_catalog import CATALOG
        ids = {e.command_id for e in CATALOG}
        assert "job.cancel" in ids


class TestNoRawLeaks:
    """Worker outputs must not leak raw content."""

    def test_worker_result_no_raw(self, tmp_path):
        enqueue_job("j1", tmp_path)
        result = run_worker_once(tmp_path, provider="fixture")
        data = export_worker_result_json(result)
        full = json.dumps(data)
        for bad in ("raw_output", "command_output", "traceback", "stderr", "stdout"):
            assert bad not in full

    def test_queue_entry_no_raw(self, tmp_path):
        entry = enqueue_job("j1", tmp_path)
        data = export_queue_entry_json(entry)
        full = json.dumps(data)
        for bad in ("raw_output", "command_output", "traceback"):
            assert bad not in full


class TestWorkerDocs:
    """Step 448: Worker docs exist and are accurate."""

    def test_docs_exist(self):
        assert (Path(__file__).resolve().parents[2] / "docs" / "worker.md").exists()

    def test_docs_mention_commands(self):
        text = (Path(__file__).resolve().parents[2] / "docs" / "worker.md").read_text()
        assert "remedy worker run" in text
        assert "remedy worker status" in text
        assert "remedy job enqueue" in text
        assert "remedy job pause" in text
        assert "remedy job cancel" in text

    def test_docs_no_overnight_autonomy(self):
        text = (Path(__file__).resolve().parents[2] / "docs" / "worker.md").read_text()
        assert "not overnight" in text.lower() or "not autonomy" in text.lower()

    def test_docs_no_browser_actions(self):
        text = (Path(__file__).resolve().parents[2] / "docs" / "worker.md").read_text()
        assert "read-only" in text.lower()
