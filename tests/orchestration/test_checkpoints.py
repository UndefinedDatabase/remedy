"""F047 T001 — checkpoint writer, loader, hashing and retention.

The five things the order requires proof of:

  * a valid chain loads its newest member;
  * a corrupted NEWEST checkpoint falls back to the previous valid one;
  * all checkpoints corrupted is an honest error, not a silent None;
  * retention keeps the first and the latest;
  * a checkpoint write that fails does not raise out of the cycle.

Nothing here touches the repository's real data root: the autouse fixture
points REMEDY_DATA_DIR at a tmp_path, exactly as the F046 cycle tests do.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

import packages.orchestration.checkpoints as cp
from packages.core.models import Job, RunState, Task
from packages.orchestration.checkpoints import (
    DEFAULT_RETENTION,
    INTENT_CYCLE,
    INTENT_NONE,
    SCHEMA_VERSION,
    AllCheckpointsCorruptError,
    Checkpoint,
    apply_retention,
    build_checkpoint,
    checkpoint_dir,
    checkpoint_paths,
    compute_content_hash,
    load_latest_valid,
    read_checkpoint,
    record_cycle_checkpoint,
    resolve_retention,
    verify_digest_for,
    write_checkpoint,
)

UTC = timezone.utc
T0 = datetime(2026, 7, 26, 12, 0, 0, tzinfo=UTC)
JOB_ID = "11111111-1111-4111-8111-111111111111"


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path: Path, monkeypatch) -> Path:
    """Autouse: every write lands under a throwaway data root."""
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


def make_checkpoint(index: int, *, job_id: str = JOB_ID, head: str = "abc123"
                    ) -> Checkpoint:
    """A record built WITHOUT disk lookups, so index is the only variable."""
    return Checkpoint(
        cycle_index=index,
        job_id=job_id,
        job_snapshot_path=f"jobs/{job_id}.json",
        job_snapshot_sha256="sha256:" + "0" * 64,
        worktree_head=head,
        budget_spent_tokens=100 * index,
        verify_result="passed",
        verify_digest=verify_digest_for("passed", "pytest -q"),
        next_intent={"kind": INTENT_CYCLE, "cycle_index": index + 1},
        created_at=T0.isoformat(),
    )


def write_chain(count: int, *, job_id: str = JOB_ID) -> list[Path]:
    """``count`` valid checkpoints, indices 1..count, retention disabled."""
    return [
        write_checkpoint(job_id, make_checkpoint(i), retention=count + 1)
        for i in range(1, count + 1)
    ]


def corrupt(path: Path) -> None:
    """Edit the body without fixing the hash — the exact tampering the
    content hash exists to catch."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    raw["record"]["worktree_head"] = "tampered"
    path.write_text(json.dumps(raw, indent=2, sort_keys=True), encoding="utf-8")


# ---------------------------------------------------------------------------
# Hashing
# ---------------------------------------------------------------------------


class TestHashing:
    def test_hash_is_stable_across_key_order(self):
        assert compute_content_hash({"a": 1, "b": 2}) == compute_content_hash(
            {"b": 2, "a": 1})

    def test_hash_changes_when_any_field_changes(self):
        one = make_checkpoint(1)
        other = Checkpoint(**{**one.__dict__, "worktree_head": "deadbee"})
        assert one.content_hash != other.content_hash

    def test_written_file_carries_body_and_matching_hash(self):
        path = write_checkpoint(JOB_ID, make_checkpoint(1))
        raw = json.loads(path.read_text(encoding="utf-8"))
        assert set(raw) == {"record", "content_hash"}
        assert raw["content_hash"] == compute_content_hash(raw["record"])
        assert raw["record"]["schema_version"] == SCHEMA_VERSION

    def test_verify_digest_distinguishes_outcome_and_command(self):
        assert verify_digest_for("passed", "a") != verify_digest_for("failed", "a")
        assert verify_digest_for("passed", "a") != verify_digest_for("passed", "b")
        assert verify_digest_for("not_run", None) == verify_digest_for("not_run", None)


# ---------------------------------------------------------------------------
# Writing and locations
# ---------------------------------------------------------------------------


class TestWriting:
    def test_checkpoints_live_beside_the_cycle_records(self):
        from packages.orchestration.long_run_executor import cycle_evidence_dir

        assert checkpoint_dir(JOB_ID).parent == cycle_evidence_dir(JOB_ID).parent
        assert checkpoint_dir(JOB_ID).name == "checkpoints"

    def test_filenames_are_zero_padded_and_indexed_by_cycle(self):
        paths = write_chain(3)
        assert [p.name for p in paths] == [
            "checkpoint_0001.json", "checkpoint_0002.json", "checkpoint_0003.json"]

    def test_rewriting_the_same_cycle_index_replaces_it(self):
        write_checkpoint(JOB_ID, make_checkpoint(1, head="first"))
        write_checkpoint(JOB_ID, make_checkpoint(1, head="second"))
        assert len(checkpoint_paths(JOB_ID)) == 1
        assert load_latest_valid(JOB_ID).worktree_head == "second"

    def test_build_checkpoint_records_the_persisted_snapshot(self):
        from packages.orchestration.storage import save_job

        job = Job(name="cp-job", tasks=[Task(title="t", description="d")])
        save_job(job)
        checkpoint = build_checkpoint(str(job.id), 1, now=T0)
        assert checkpoint.job_snapshot_path == f"jobs/{job.id}.json"
        assert checkpoint.job_snapshot_sha256.startswith("sha256:")
        assert checkpoint.created_at == T0.isoformat()

    def test_build_checkpoint_is_honest_when_no_snapshot_exists(self):
        checkpoint = build_checkpoint(JOB_ID, 1, now=T0)
        assert checkpoint.job_snapshot_path == ""
        assert checkpoint.job_snapshot_sha256 == ""


# ---------------------------------------------------------------------------
# Loading — the corruption matrix
# ---------------------------------------------------------------------------


class TestLoadLatestValid:
    def test_valid_chain_returns_the_newest(self):
        write_chain(4)
        loaded = load_latest_valid(JOB_ID)
        assert loaded.cycle_index == 4
        assert loaded.budget_spent_tokens == 400
        assert loaded.next_intent == {"kind": INTENT_CYCLE, "cycle_index": 5}

    def test_corrupted_newest_falls_back_to_the_previous_valid_one(self, caplog):
        paths = write_chain(3)
        corrupt(paths[-1])
        with caplog.at_level("WARNING"):
            loaded = load_latest_valid(JOB_ID)
        assert loaded.cycle_index == 2
        assert "checkpoint_0003.json" in caplog.text

    def test_a_skipped_checkpoint_is_kept_on_disk_for_forensics(self):
        paths = write_chain(3)
        corrupt(paths[-1])
        load_latest_valid(JOB_ID)
        assert paths[-1].exists()

    def test_several_corrupted_newest_are_walked_past(self):
        paths = write_chain(5)
        for path in paths[2:]:
            corrupt(path)
        assert load_latest_valid(JOB_ID).cycle_index == 2

    def test_all_corrupted_is_an_honest_error(self):
        paths = write_chain(3)
        for path in paths:
            corrupt(path)
        with pytest.raises(AllCheckpointsCorruptError) as exc:
            load_latest_valid(JOB_ID)
        assert len(exc.value.paths) == 3
        assert "checkpoint_0003.json" in str(exc.value)

    def test_never_checkpointed_returns_none_not_an_error(self):
        assert load_latest_valid(JOB_ID) is None

    def test_truncated_file_does_not_verify(self, tmp_path):
        path = write_checkpoint(JOB_ID, make_checkpoint(1))
        path.write_text('{"record": {"job_id":', encoding="utf-8")
        assert read_checkpoint(path) is None

    def test_a_body_without_its_hash_does_not_verify(self):
        path = write_checkpoint(JOB_ID, make_checkpoint(1))
        raw = json.loads(path.read_text(encoding="utf-8"))
        path.write_text(json.dumps({"record": raw["record"]}), encoding="utf-8")
        assert read_checkpoint(path) is None

    def test_an_unknown_schema_version_is_refused_even_when_hashed(self):
        body = make_checkpoint(1).to_body()
        body["schema_version"] = SCHEMA_VERSION + 99
        path = checkpoint_dir(JOB_ID) / "checkpoint_0001.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps({"record": body, "content_hash": compute_content_hash(body)}),
            encoding="utf-8")
        assert read_checkpoint(path) is None


# ---------------------------------------------------------------------------
# Retention
# ---------------------------------------------------------------------------


class TestRetention:
    def test_retention_keeps_the_first_and_the_latest(self):
        write_chain(10)
        apply_retention(JOB_ID, keep=3)
        kept = [p.name for p in checkpoint_paths(JOB_ID)]
        assert kept[0] == "checkpoint_0001.json"
        assert kept[-1] == "checkpoint_0010.json"
        assert kept == ["checkpoint_0001.json", "checkpoint_0008.json",
                        "checkpoint_0009.json", "checkpoint_0010.json"]

    def test_retention_is_a_no_op_below_the_limit(self):
        write_chain(3)
        assert apply_retention(JOB_ID, keep=5) == []
        assert len(checkpoint_paths(JOB_ID)) == 3

    def test_a_corrupted_checkpoint_is_never_pruned(self):
        paths = write_chain(10)
        corrupt(paths[4])                       # checkpoint_0005, a prune candidate
        apply_retention(JOB_ID, keep=2)
        assert paths[4].exists()
        assert "checkpoint_0005.json" in [p.name for p in checkpoint_paths(JOB_ID)]

    def test_the_writer_applies_retention_as_it_goes(self):
        for index in range(1, 9):
            write_checkpoint(JOB_ID, make_checkpoint(index), retention=2)
        kept = [p.name for p in checkpoint_paths(JOB_ID)]
        assert kept == ["checkpoint_0001.json", "checkpoint_0007.json",
                        "checkpoint_0008.json"]

    def test_retention_default_and_config_override(self, monkeypatch):
        from packages.orchestration.config import load_config

        assert resolve_retention() == DEFAULT_RETENTION
        monkeypatch.setenv("REMEDY_CYCLES_CHECKPOINT_RETENTION", "2")
        assert resolve_retention(load_config()) == 2

    def test_a_nonsense_retention_value_falls_back_to_the_default(self):
        class _Bad:
            def get(self, _key):
                return "not-a-number"

        assert resolve_retention(_Bad()) == DEFAULT_RETENTION

    def test_the_retention_key_is_registered_in_the_config_catalog(self):
        from packages.orchestration.config import get_key_spec

        spec = get_key_spec(cp.CONFIG_KEY_RETENTION)
        assert spec is not None
        assert spec.value_type is int
        assert spec.default == DEFAULT_RETENTION


# ---------------------------------------------------------------------------
# Write failure must not escape the cycle
# ---------------------------------------------------------------------------


class TestWriteFailureIsContained:
    def test_record_cycle_checkpoint_returns_the_reason_instead_of_raising(
            self, monkeypatch):
        def boom(*_a, **_kw):
            raise OSError("disk full")

        monkeypatch.setattr(cp, "_atomic_write", boom)
        path, reason = record_cycle_checkpoint(JOB_ID, 1)
        assert path is None
        assert "disk full" in reason

    def test_the_failure_is_logged_loudly(self, monkeypatch, caplog):
        monkeypatch.setattr(cp, "_atomic_write", lambda *_a, **_k: (_ for _ in ()).throw(
            OSError("disk full")))
        with caplog.at_level("WARNING"):
            record_cycle_checkpoint(JOB_ID, 1)
        assert "checkpoint write FAILED" in caplog.text
        assert "the run continues" in caplog.text

    def test_a_successful_write_reports_no_error(self):
        path, reason = record_cycle_checkpoint(JOB_ID, 1)
        assert reason == ""
        assert path is not None and path.exists()


# ---------------------------------------------------------------------------
# The cycle boundary in long_run_executor
# ---------------------------------------------------------------------------


def _job(task_count: int = 2) -> Job:
    return Job(
        name="cp-loop-job",
        tasks=[Task(title=f"t{i}", description="d") for i in range(task_count)],
    )


def _run_one_cycle(job: Job, **kwargs):
    """One cycle with a task step that completes exactly one task."""
    from packages.orchestration.long_run_executor import CycleLimits, TaskAttempt, run_cycles

    def step(j: Job, _provider):
        pending = [t for t in j.tasks if t.status == RunState.PENDING]
        if not pending:
            return TaskAttempt()
        pending[0].status = RunState.COMPLETED
        return TaskAttempt(task_id=pending[0].id, executed=True, verified=True)

    return run_cycles(job, CycleLimits(max_cycles=1), lambda _ctx: None,
                      task_step=step, clock=lambda: T0, **kwargs)


class TestCycleBoundaryWiring:
    def test_a_cycle_writes_its_checkpoint(self):
        job = _job()
        _run_one_cycle(job)
        loaded = load_latest_valid(str(job.id))
        assert loaded is not None
        assert loaded.cycle_index == 1
        assert loaded.budget_spent_tokens == 0

    def test_the_checkpoint_names_the_task_that_would_run_next(self):
        job = _job(task_count=2)
        _run_one_cycle(job)
        loaded = load_latest_valid(str(job.id))
        remaining = [t for t in job.tasks if t.status == RunState.PENDING]
        assert loaded.next_intent["kind"] == INTENT_CYCLE
        assert loaded.next_intent["task_id"] == str(remaining[0].id)
        assert loaded.next_intent["cycle_index"] == 2

    def test_nothing_left_to_run_is_recorded_as_such(self):
        job = _job(task_count=1)
        _run_one_cycle(job)
        assert load_latest_valid(str(job.id)).next_intent == {"kind": INTENT_NONE}

    def test_the_checkpoint_references_the_persisted_snapshot(self):
        job = _job()
        _run_one_cycle(job)
        loaded = load_latest_valid(str(job.id))
        assert loaded.job_snapshot_path == f"jobs/{job.id}.json"
        assert loaded.job_snapshot_sha256.startswith("sha256:")

    def test_a_failed_checkpoint_write_does_not_break_the_cycle(self, monkeypatch):
        monkeypatch.setattr(cp, "_atomic_write", lambda *_a, **_k: (_ for _ in ()).throw(
            OSError("disk full")))
        job = _job()
        result = _run_one_cycle(job)
        assert result.cycles_run == 1
        assert "disk full" in job.metadata["checkpoint_error"]
        assert checkpoint_paths(str(job.id)) == []

    def test_checkpointing_can_be_switched_off(self):
        job = _job()
        _run_one_cycle(job, record_checkpoint=False)
        assert checkpoint_paths(str(job.id)) == []

    def test_the_default_single_pass_still_writes_exactly_one_checkpoint(self):
        from packages.orchestration.long_run_executor import CYCLE_SAFETY_CAP

        assert CYCLE_SAFETY_CAP == 1        # the rollout default is untouched
        job = _job(task_count=3)
        _run_one_cycle(job)
        assert [p.name for p in checkpoint_paths(str(job.id))] == [
            "checkpoint_0001.json"]
