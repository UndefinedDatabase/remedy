"""F048 T001 — the file-based queue entry store and its operations.

What the order requires proof of:

  * ordering: higher priority first, FIFO by ``created_at`` within a priority;
  * the claim marker's lifecycle — created on claim, gone on release/complete/fail;
  * complete and fail transitions, and the refusal to transition an unclaimed entry;
  * a claim survives a process restart, because the state is re-read from disk and
    nothing is cached in the consumer;
  * listing survives corrupt entry files — they are skipped and COUNTED;
  * duplicate goal text is allowed and produces two independent entries.

Every test writes into ``tmp_path``: the queue root is passed explicitly, and the one
test that exercises default resolution points REMEDY_DATA_DIR at a tmp_path too, so the
repository's real data root is never touched.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

from packages.orchestration import job_queue as q
from packages.orchestration.job_queue import (
    CLAIM_SUFFIX,
    ENTRY_SUFFIX,
    STATUS_CLAIMED,
    STATUS_DONE,
    STATUS_FAILED,
    STATUS_QUEUED,
    QueueEntryNotFoundError,
    QueueError,
    claim_holder,
    claim_next,
    complete,
    enqueue,
    fail,
    list_entries,
    list_entries_safe,
    load_entry,
    project_queue_dir,
    release,
)

PROJECT = "proj-alpha"

REPO_ROOT = Path(__file__).resolve().parents[2]


def _in_a_fresh_process(body: str) -> Any:
    """Run *body* in a NEW interpreter and return the JSON it printed.

    Not a thread and not a reimport: a separate process, so nothing this one holds in
    memory can be mistaken for state that survived on disk.
    """
    proc = subprocess.run(
        [sys.executable, "-c", "import json, sys\n" + body],
        cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=60,
    )
    assert proc.returncode == 0, f"child failed: {proc.stderr}"
    return json.loads(proc.stdout.strip().splitlines()[-1])


@pytest.fixture
def root(tmp_path: Path) -> Path:
    """An isolated data root. The queue area lives at <root>/queue/<project_id>."""
    return tmp_path / "remedy_data"


def _entry_path(root: Path, entry_id: str) -> Path:
    return project_queue_dir(PROJECT, root) / f"{entry_id}{ENTRY_SUFFIX}"


def _claim_path(root: Path, entry_id: str) -> Path:
    return project_queue_dir(PROJECT, root) / f"{entry_id}{CLAIM_SUFFIX}"


# ---------------------------------------------------------------------------
# Ordering (A9)
# ---------------------------------------------------------------------------


class TestOrdering:
    def test_higher_priority_is_claimed_first(self, root: Path):
        low = enqueue(PROJECT, "low", 0, root=root)
        high = enqueue(PROJECT, "high", 10, root=root)
        middle = enqueue(PROJECT, "middle", 5, root=root)

        order = [e.id for e in list_entries(PROJECT, root)]
        assert order == [high.id, middle.id, low.id]

    def test_fifo_within_equal_priority(self, root: Path, monkeypatch):
        """Same priority: oldest created_at wins, regardless of insertion accident."""
        stamps = iter([
            "2026-07-27T10:00:03+00:00",
            "2026-07-27T10:00:01+00:00",
            "2026-07-27T10:00:02+00:00",
        ])
        monkeypatch.setattr(q, "utc_now_iso", lambda: next(stamps))

        third = enqueue(PROJECT, "enqueued third in time", 0, root=root)
        first = enqueue(PROJECT, "enqueued first in time", 0, root=root)
        second = enqueue(PROJECT, "enqueued second in time", 0, root=root)

        order = [e.id for e in list_entries(PROJECT, root)]
        assert order == [first.id, second.id, third.id]

    def test_priority_outranks_age(self, root: Path, monkeypatch):
        stamps = iter([
            "2026-07-27T10:00:01+00:00",
            "2026-07-27T10:00:09+00:00",
        ])
        monkeypatch.setattr(q, "utc_now_iso", lambda: next(stamps))

        old_low = enqueue(PROJECT, "old but low", 0, root=root)
        young_high = enqueue(PROJECT, "young but high", 3, root=root)

        assert [e.id for e in list_entries(PROJECT, root)] == [young_high.id, old_low.id]

    def test_claim_next_follows_the_listing_order(self, root: Path):
        enqueue(PROJECT, "low", 0, root=root)
        high = enqueue(PROJECT, "high", 7, root=root)

        claimed = claim_next(PROJECT, "consumer-1", root)
        assert claimed is not None
        assert claimed.id == high.id


# ---------------------------------------------------------------------------
# Claim marker lifecycle
# ---------------------------------------------------------------------------


class TestClaimLifecycle:
    def test_claim_creates_the_marker_and_stamps_the_entry(self, root: Path):
        entry = enqueue(PROJECT, "work", 0, root=root)
        assert not _claim_path(root, entry.id).exists()

        claimed = claim_next(PROJECT, "consumer-1", root)
        assert claimed is not None
        assert claimed.id == entry.id
        assert claimed.status == STATUS_CLAIMED
        assert claimed.claimed_by == "consumer-1"
        assert claimed.claimed_at

        assert _claim_path(root, entry.id).exists()
        assert claim_holder(PROJECT, entry.id, root) == "consumer-1"

    def test_a_claimed_entry_is_not_offered_again(self, root: Path):
        enqueue(PROJECT, "only one", 0, root=root)

        first = claim_next(PROJECT, "consumer-1", root)
        second = claim_next(PROJECT, "consumer-2", root)

        assert first is not None
        assert second is None

    def test_empty_queue_claims_nothing(self, root: Path):
        assert claim_next(PROJECT, "consumer-1", root) is None

    def test_release_returns_the_entry_and_removes_the_marker(self, root: Path):
        entry = enqueue(PROJECT, "work", 0, root=root)
        claimed = claim_next(PROJECT, "consumer-1", root)
        assert claimed is not None

        released = release(claimed, root)
        assert released.status == STATUS_QUEUED
        assert released.claimed_by == ""
        assert released.claimed_at == ""
        assert not _claim_path(root, entry.id).exists()
        assert claim_holder(PROJECT, entry.id, root) == ""

        again = claim_next(PROJECT, "consumer-2", root)
        assert again is not None
        assert again.id == entry.id
        assert again.claimed_by == "consumer-2"

    def test_a_stale_claim_stays_visible(self, root: Path):
        """No takeover here. A consumer that dies leaves an entry that still names it —
        re-offering it is an explicit operator command (T003), not a timeout."""
        entry = enqueue(PROJECT, "work", 0, root=root)
        claim_next(PROJECT, "host-a#111", root)

        # A consumer that never came back leaves both the marker and the record.
        assert claim_holder(PROJECT, entry.id, root) == "host-a#111"
        assert load_entry(PROJECT, entry.id, root).status == STATUS_CLAIMED
        assert claim_next(PROJECT, "host-b#222", root) is None


# ---------------------------------------------------------------------------
# Terminal transitions
# ---------------------------------------------------------------------------


class TestTransitions:
    def test_complete_records_the_job_and_drops_the_marker(self, root: Path):
        entry = enqueue(PROJECT, "work", 0, root=root)
        claimed = claim_next(PROJECT, "consumer-1", root)
        assert claimed is not None

        done = complete(claimed, "job-abc123", root)
        assert done.status == STATUS_DONE
        assert done.result_job_id == "job-abc123"
        assert not _claim_path(root, entry.id).exists()

        # Terminal: it is not queued work any more.
        assert claim_next(PROJECT, "consumer-2", root) is None
        assert load_entry(PROJECT, entry.id, root).status == STATUS_DONE

    def test_fail_records_the_reason_and_drops_the_marker(self, root: Path):
        entry = enqueue(PROJECT, "work", 0, root=root)
        claimed = claim_next(PROJECT, "consumer-1", root)
        assert claimed is not None

        failed = fail(claimed, "provider timed out", root)
        assert failed.status == STATUS_FAILED
        assert failed.failure_reason == "provider timed out"
        assert not _claim_path(root, entry.id).exists()
        assert claim_next(PROJECT, "consumer-2", root) is None

    def test_transition_refuses_an_unclaimed_entry(self, root: Path):
        entry = enqueue(PROJECT, "never claimed", 0, root=root)

        with pytest.raises(QueueError, match="only a claimed entry"):
            complete(entry, "job-abc123", root)
        with pytest.raises(QueueError, match="only a claimed entry"):
            fail(entry, "nope", root)
        with pytest.raises(QueueError, match="only a claimed entry"):
            release(entry, root)

    def test_transition_from_a_stale_snapshot_reads_disk_first(self, root: Path):
        """The caller's object is a snapshot. The file is the truth."""
        entry = enqueue(PROJECT, "work", 0, root=root)
        claimed = claim_next(PROJECT, "consumer-1", root)
        assert claimed is not None
        complete(claimed, "job-first", root)

        # `claimed` still says "claimed" in memory. Disk says done, so this must refuse
        # rather than silently rewrite the terminal state.
        with pytest.raises(QueueError, match="only a claimed entry"):
            fail(claimed, "second opinion", root)
        assert load_entry(PROJECT, entry.id, root).result_job_id == "job-first"

    def test_transition_on_a_vanished_entry_is_an_error(self, root: Path):
        entry = enqueue(PROJECT, "work", 0, root=root)
        claimed = claim_next(PROJECT, "consumer-1", root)
        assert claimed is not None
        _entry_path(root, entry.id).unlink()

        with pytest.raises(QueueEntryNotFoundError):
            complete(claimed, "job-abc123", root)


# ---------------------------------------------------------------------------
# Restart safety
# ---------------------------------------------------------------------------


class TestRestartSafety:
    def test_claim_survives_a_process_restart(self, root: Path):
        """A restart keeps nothing in memory. A SECOND interpreter, started after the
        claim, must see the same claim — and must not be able to steal it."""
        entry = enqueue(PROJECT, "durable work", 4, root=root)
        claimed = claim_next(PROJECT, "host-a#4242", root)
        assert claimed is not None

        observed = _in_a_fresh_process(f"""
from packages.orchestration import job_queue as q
root = {str(root)!r}
after = q.load_entry({PROJECT!r}, {entry.id!r}, root)
print(json.dumps({{
    "status": after.status,
    "claimed_by": after.claimed_by,
    "claimed_at": after.claimed_at,
    "priority": after.priority,
    "goal": after.goal,
    "holder": q.claim_holder({PROJECT!r}, {entry.id!r}, root),
    "stolen": q.claim_next({PROJECT!r}, "host-b#7", root) is not None,
}}))
""")

        assert observed["status"] == STATUS_CLAIMED
        assert observed["claimed_by"] == "host-a#4242"
        assert observed["claimed_at"] == claimed.claimed_at
        assert observed["priority"] == 4
        assert observed["goal"] == "durable work"
        assert observed["holder"] == "host-a#4242"
        assert observed["stolen"] is False

    def test_the_queue_is_readable_from_a_bare_data_root(self, root: Path, monkeypatch):
        """Default resolution: no explicit root, REMEDY_DATA_DIR only."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
        entry = enqueue(PROJECT, "resolved by env", 0)

        assert _entry_path(root, entry.id).exists()
        assert [e.id for e in list_entries(PROJECT)] == [entry.id]


# ---------------------------------------------------------------------------
# Honest listing
# ---------------------------------------------------------------------------


class TestCorruptEntries:
    def test_corrupt_entries_are_skipped_and_counted(self, root: Path):
        good_a = enqueue(PROJECT, "good a", 0, root=root)
        broken = enqueue(PROJECT, "to be broken", 0, root=root)
        good_b = enqueue(PROJECT, "good b", 0, root=root)

        _entry_path(root, broken.id).write_text("{ this is not json", encoding="utf-8")

        entries, degraded, skipped = list_entries_safe(PROJECT, root)
        assert [e.id for e in entries] == [good_a.id, good_b.id]
        assert degraded is True
        assert skipped == [f"{broken.id}{ENTRY_SUFFIX}"]

    def test_an_unknown_record_version_is_skipped_not_guessed(self, root: Path):
        good = enqueue(PROJECT, "good", 0, root=root)
        alien = enqueue(PROJECT, "from the future", 0, root=root)

        payload = json.loads(_entry_path(root, alien.id).read_text(encoding="utf-8"))
        payload["queue_entry_v"] = 999
        _entry_path(root, alien.id).write_text(json.dumps(payload), encoding="utf-8")

        entries, degraded, skipped = list_entries_safe(PROJECT, root)
        assert [e.id for e in entries] == [good.id]
        assert degraded is True
        assert skipped == [f"{alien.id}{ENTRY_SUFFIX}"]

    def test_a_corrupt_entry_does_not_block_claiming(self, root: Path):
        broken = enqueue(PROJECT, "to be broken", 9, root=root)
        good = enqueue(PROJECT, "still claimable", 0, root=root)
        _entry_path(root, broken.id).write_text("", encoding="utf-8")

        claimed = claim_next(PROJECT, "consumer-1", root)
        assert claimed is not None
        assert claimed.id == good.id

    def test_a_missing_queue_lists_empty_and_honest(self, root: Path):
        entries, degraded, skipped = list_entries_safe("proj-never-used", root)
        assert entries == []
        assert degraded is False
        assert skipped == []


# ---------------------------------------------------------------------------
# Enqueue contract
# ---------------------------------------------------------------------------


class TestEnqueue:
    def test_duplicate_goal_text_is_allowed(self, root: Path):
        """Deduplication is a human judgment, not the queue's (A9)."""
        first = enqueue(PROJECT, "same exact goal", 0, root=root)
        second = enqueue(PROJECT, "same exact goal", 0, root=root)

        assert first.id != second.id
        entries = list_entries(PROJECT, root)
        assert len(entries) == 2
        assert {e.goal for e in entries} == {"same exact goal"}

        one = claim_next(PROJECT, "consumer-1", root)
        two = claim_next(PROJECT, "consumer-2", root)
        assert one is not None and two is not None
        assert {one.id, two.id} == {first.id, second.id}

    def test_a_goal_file_reference_is_accepted(self, root: Path):
        entry = enqueue(PROJECT, goal_path="/work/goals/f048.md", root=root)
        assert entry.goal == ""
        assert entry.goal_path == "/work/goals/f048.md"
        assert load_entry(PROJECT, entry.id, root).goal_path == "/work/goals/f048.md"

    def test_goal_text_and_goal_path_are_exclusive(self, root: Path):
        with pytest.raises(QueueError, match="exactly one"):
            enqueue(PROJECT, "text", 0, goal_path="/work/goals/f048.md", root=root)
        with pytest.raises(QueueError, match="exactly one"):
            enqueue(PROJECT, "", 0, root=root)

    def test_entries_are_scoped_to_their_project(self, root: Path):
        mine = enqueue(PROJECT, "mine", 0, root=root)
        enqueue("proj-beta", "theirs", 0, root=root)

        assert [e.id for e in list_entries(PROJECT, root)] == [mine.id]
        claimed = claim_next(PROJECT, "consumer-1", root)
        assert claimed is not None
        assert claimed.id == mine.id
        assert claim_next(PROJECT, "consumer-1", root) is None

    def test_an_unsafe_project_id_never_becomes_a_path(self, root: Path):
        for bad in ("../escape", "a/b", "", "."):
            with pytest.raises(QueueError, match="invalid project id"):
                enqueue(bad, "work", 0, root=root)

    def test_a_non_integer_priority_is_refused(self, root: Path):
        with pytest.raises(QueueError, match="invalid priority"):
            enqueue(PROJECT, "work", "high", root=root)  # type: ignore[arg-type]
