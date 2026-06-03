"""Tests: worker queue, lifecycle, lease, run-once, bounded loop, pause/cancel, stale.

All tests use one-shot mode with temp dirs. No unbounded loops, no background processes.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import pytest

from packages.orchestration.worker_queue import (
    ALLOWED_PROVIDERS,
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
    validate_provider,
)


class TestLifecycleModel:
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


class TestProviderValidation:
    def test_valid_providers(self):
        for p in ("none", "fixture", "ollama"):
            assert validate_provider(p) is None

    def test_invalid_provider(self):
        err = validate_provider("typo")
        assert err is not None
        assert "Unknown" in err

    def test_allowed_set(self):
        assert ALLOWED_PROVIDERS == {"none", "fixture", "ollama"}


class TestLocalQueue:
    def test_enqueue_one_job(self, tmp_path):
        entry = enqueue_job("job-1", tmp_path)
        assert entry.lifecycle_state == "queued"

    def test_list_queued(self, tmp_path):
        enqueue_job("job-a", tmp_path)
        enqueue_job("job-b", tmp_path)
        assert len(list_queued(tmp_path)) == 2

    def test_get_next_returns_first_queued(self, tmp_path):
        enqueue_job("job-a", tmp_path)
        enqueue_job("job-b", tmp_path)
        nxt = get_next_job(tmp_path)
        assert nxt is not None
        assert nxt.job_id == "job-a"

    def test_paused_skipped(self, tmp_path):
        enqueue_job("j1", tmp_path)
        pause_job("j1", tmp_path)
        assert get_next_job(tmp_path) is None

    def test_cancelled_skipped(self, tmp_path):
        enqueue_job("j1", tmp_path)
        cancel_job("j1", tmp_path)
        assert get_next_job(tmp_path) is None

    def test_completed_not_picked(self, tmp_path):
        enqueue_job("j1", tmp_path)
        claim_job("j1", "w1", tmp_path)
        transition_state("j1", "running", tmp_path)
        transition_state("j1", "completed", tmp_path)
        assert get_next_job(tmp_path) is None

    def test_corrupt_queue_safe(self, tmp_path):
        (tmp_path / "queue").mkdir()
        (tmp_path / "queue" / "bad.json").write_text("not json")
        assert len(list_queued(tmp_path)) == 0


class TestWorkerLock:
    def test_claim_job(self, tmp_path):
        enqueue_job("j1", tmp_path)
        lease = claim_job("j1", "wA", tmp_path)
        assert lease is not None
        assert lease.worker_id == "wA"

    def test_second_worker_blocked(self, tmp_path):
        enqueue_job("j1", tmp_path)
        claim_job("j1", "wA", tmp_path)
        assert claim_job("j1", "wB", tmp_path) is None

    def test_lease_released_on_completion(self, tmp_path):
        enqueue_job("j1", tmp_path)
        claim_job("j1", "w1", tmp_path)
        transition_state("j1", "running", tmp_path)
        transition_state("j1", "completed", tmp_path)
        e = [x for x in list_queued(tmp_path) if x.job_id == "j1"][0]
        assert e.worker_id == ""

    def test_release_lease(self, tmp_path):
        enqueue_job("j1", tmp_path)
        claim_job("j1", "w1", tmp_path)
        release_lease("j1", tmp_path)
        e = [x for x in list_queued(tmp_path) if x.job_id == "j1"][0]
        assert e.worker_id == ""


class TestNoFakeCompletion:
    """Provider none must not complete jobs."""

    def test_provider_none_blocks_not_completes(self, tmp_path):
        enqueue_job("j1", tmp_path)
        result = run_worker_once(tmp_path, provider="none")
        assert result.last_lifecycle_state == "blocked"
        assert result.action_taken == "no_work_performed"
        assert result.jobs_processed == 0

    def test_provider_none_why_stopped(self, tmp_path):
        enqueue_job("j1", tmp_path)
        result = run_worker_once(tmp_path, provider="none")
        assert result.why_it_stopped == "no_worker_selected"

    def test_provider_none_suggests_real_provider(self, tmp_path):
        enqueue_job("j1", tmp_path)
        result = run_worker_once(tmp_path, provider="none")
        assert "fixture" in result.next_command or "ollama" in result.next_command

    def test_invalid_provider_no_mutation(self, tmp_path):
        enqueue_job("j1", tmp_path)
        result = run_worker_once(tmp_path, provider="typo")
        assert result.action_taken == "error"
        e = [x for x in list_queued(tmp_path) if x.job_id == "j1"][0]
        assert e.lifecycle_state == "queued"


class TestWorkerRunOnce:
    def test_no_job_idle(self, tmp_path):
        result = run_worker_once(tmp_path)
        assert result.action_taken == "idle"

    def test_approval_stops(self, tmp_path):
        enqueue_job("j1", tmp_path)
        result = run_worker_once(tmp_path, provider="ollama")
        assert result.last_lifecycle_state == "waiting_for_approval"

    def test_json_output_safe(self, tmp_path):
        enqueue_job("j1", tmp_path)
        result = run_worker_once(tmp_path, provider="none")
        data = export_worker_result_json(result)
        assert data["redaction"] == "safe_metadata_only"
        full = json.dumps(data)
        for bad in ("raw_output", "command_output", "traceback", "stderr"):
            assert bad not in full

    def test_specific_job(self, tmp_path):
        result = run_worker_once(tmp_path, job_id="new-job", provider="none")
        assert result.last_job_id == "new-job"
        assert result.last_lifecycle_state == "blocked"


class TestBoundedLoop:
    def test_idle_timeout_stops(self, tmp_path):
        result = run_worker_loop(tmp_path, max_jobs=5, max_seconds=2, idle_timeout=1)
        assert result.why_it_stopped == "idle_timeout"

    def test_no_cpu_spin(self, tmp_path):
        start = time.monotonic()
        run_worker_loop(tmp_path, max_jobs=1, max_seconds=1, idle_timeout=0)
        assert time.monotonic() - start < 5


class TestHeartbeatAndStatus:
    def test_status_after_run(self, tmp_path):
        enqueue_job("j1", tmp_path)
        run_worker_once(tmp_path, provider="none")
        status = get_worker_status(tmp_path)
        assert status.lifecycle_state != "idle"

    def test_idle_status(self, tmp_path):
        status = get_worker_status(tmp_path)
        assert status.lifecycle_state == "idle"

    def test_status_export_safe(self, tmp_path):
        data = export_worker_status_json(get_worker_status(tmp_path))
        assert data["redaction"] == "safe_metadata_only"


class TestPauseAndCancel:
    def test_pause_queued(self, tmp_path):
        enqueue_job("j1", tmp_path)
        assert pause_job("j1", tmp_path).lifecycle_state == "paused"

    def test_paused_not_picked(self, tmp_path):
        enqueue_job("j1", tmp_path)
        pause_job("j1", tmp_path)
        assert get_next_job(tmp_path) is None

    def test_resume_paused(self, tmp_path):
        enqueue_job("j1", tmp_path)
        pause_job("j1", tmp_path)
        assert resume_queued("j1", tmp_path).lifecycle_state == "queued"

    def test_cancel_queued(self, tmp_path):
        enqueue_job("j1", tmp_path)
        assert cancel_job("j1", tmp_path).lifecycle_state == "cancelled"

    def test_cancel_running_marks_cancelling(self, tmp_path):
        enqueue_job("j1", tmp_path)
        claim_job("j1", "w1", tmp_path)
        transition_state("j1", "running", tmp_path)
        assert cancel_job("j1", tmp_path).lifecycle_state == "cancelling"

    def test_cancel_completed_fails(self, tmp_path):
        enqueue_job("j1", tmp_path)
        claim_job("j1", "w1", tmp_path)
        transition_state("j1", "running", tmp_path)
        transition_state("j1", "completed", tmp_path)
        assert cancel_job("j1", tmp_path) is None


class TestStaleRecovery:
    def test_stale_detected(self, tmp_path):
        enqueue_job("j1", tmp_path)
        claim_job("j1", "w1", tmp_path)
        from packages.orchestration.worker_queue import _load_entry, _save_entry
        entry = _load_entry(tmp_path, "j1")
        entry.lease_expires_at = "2020-01-01T00:00:00+00:00"
        _save_entry(tmp_path, entry)
        assert len(detect_stale(tmp_path)) >= 1

    def test_stale_can_be_reclaimed(self, tmp_path):
        enqueue_job("j1", tmp_path)
        claim_job("j1", "w1", tmp_path)
        from packages.orchestration.worker_queue import _load_entry, _save_entry
        entry = _load_entry(tmp_path, "j1")
        entry.lease_expires_at = "2020-01-01T00:00:00+00:00"
        entry.lifecycle_state = "stale"
        _save_entry(tmp_path, entry)
        lease = claim_job("j1", "w2", tmp_path)
        assert lease is not None and lease.worker_id == "w2"


class TestCatalogAndCLI:
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

    def test_worker_run_not_read_only(self):
        from apps.cli.command_catalog import CATALOG
        entry = next(e for e in CATALOG if e.command_id == "worker.run")
        assert entry.action_class != "read_only"

    def test_job_enqueue_not_read_only(self):
        from apps.cli.command_catalog import CATALOG
        entry = next(e for e in CATALOG if e.command_id == "job.enqueue")
        assert entry.action_class != "read_only"

    def test_job_resume_queue_in_catalog(self):
        from apps.cli.command_catalog import CATALOG
        ids = {e.command_id for e in CATALOG}
        assert "job.resume-queue" in ids


class TestNoRawLeaks:
    def test_worker_result_no_raw(self, tmp_path):
        enqueue_job("j1", tmp_path)
        result = run_worker_once(tmp_path, provider="none")
        full = json.dumps(export_worker_result_json(result))
        for bad in ("raw_output", "command_output", "traceback", "stderr", "stdout"):
            assert bad not in full

    def test_queue_entry_no_raw(self, tmp_path):
        entry = enqueue_job("j1", tmp_path)
        full = json.dumps(export_queue_entry_json(entry))
        for bad in ("raw_output", "command_output", "traceback"):
            assert bad not in full


class TestWorkerDocs:
    def test_docs_exist(self):
        assert (Path(__file__).resolve().parents[2] / "docs" / "worker.md").exists()

    def test_docs_mention_commands(self):
        text = (Path(__file__).resolve().parents[2] / "docs" / "worker.md").read_text()
        for cmd in ("remedy worker run", "remedy worker status", "remedy job enqueue", "remedy job pause", "remedy job cancel"):
            assert cmd in text

    def test_docs_no_overnight_autonomy(self):
        text = (Path(__file__).resolve().parents[2] / "docs" / "worker.md").read_text()
        assert "not overnight" in text.lower() or "not autonomy" in text.lower()

    def test_docs_no_browser_actions(self):
        text = (Path(__file__).resolve().parents[2] / "docs" / "worker.md").read_text()
        assert "read-only" in text.lower()


class TestWorkerUI:
    """Worker status visible in UI."""

    def test_worker_status_in_right_panel(self):
        tsx = (Path(__file__).resolve().parents[2] / "apps" / "ui" / "src" / "components" / "panels" / "RightLivePanel.tsx").read_text()
        assert "WorkerStatusMini" in tsx

    def test_worker_status_component_exists(self):
        assert (Path(__file__).resolve().parents[2] / "apps" / "ui" / "src" / "components" / "pipeline" / "WorkerStatusMini.tsx").exists()

    def test_worker_status_no_mutation_buttons(self):
        tsx = (Path(__file__).resolve().parents[2] / "apps" / "ui" / "src" / "components" / "pipeline" / "WorkerStatusMini.tsx").read_text()
        assert "onClick" not in tsx or "clipboard" in tsx
        assert "Start" not in tsx
        assert "Pause" not in tsx or "Paused" in tsx
