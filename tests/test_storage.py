"""
Tests for the Job persistence layer.
"""

from __future__ import annotations

import time
from uuid import uuid4

import pytest

from packages.core.models import Job, RunState
from packages.orchestration.storage import JobNotFoundError, list_jobs, load_job, save_job


@pytest.fixture()
def storage(tmp_path, monkeypatch):
    """Redirect _DATA_DIR to a temp directory for isolation."""
    import packages.orchestration.storage as _storage
    monkeypatch.setattr(_storage, "_DATA_DIR", tmp_path / "jobs")
    return _storage


# ---------------------------------------------------------------------------
# save / load
# ---------------------------------------------------------------------------

def test_save_and_load_roundtrip(storage):
    job = Job(name="test-job", user_prompt="do something", state=RunState.PENDING)
    save_job(job)
    loaded = load_job(job.id)

    assert loaded.id == job.id
    assert loaded.name == job.name
    assert loaded.user_prompt == job.user_prompt
    assert loaded.state == RunState.PENDING
    assert loaded.created_at == job.created_at


def test_load_missing_raises_job_not_found(storage):
    with pytest.raises(JobNotFoundError) as exc_info:
        load_job(uuid4())
    assert "Job not found" in str(exc_info.value)


def test_job_not_found_carries_job_id(storage):
    missing_id = uuid4()
    with pytest.raises(JobNotFoundError) as exc_info:
        load_job(missing_id)
    assert exc_info.value.job_id == missing_id


# ---------------------------------------------------------------------------
# created_at
# ---------------------------------------------------------------------------

def test_created_at_is_set(storage):
    job = Job(name="ts-test")
    assert job.created_at is not None
    # Timezone-aware
    assert job.created_at.tzinfo is not None


# ---------------------------------------------------------------------------
# list_jobs
# ---------------------------------------------------------------------------

def test_list_jobs_empty(storage):
    assert list_jobs() == []


def test_list_jobs_returns_all(storage):
    j1 = Job(name="job-1")
    j2 = Job(name="job-2")
    save_job(j1)
    save_job(j2)
    ids = {j.id for j in list_jobs()}
    assert ids == {j1.id, j2.id}


def test_list_jobs_sorted_newest_first(storage):
    j1 = Job(name="older")
    time.sleep(0.01)  # ensure distinct timestamps
    j2 = Job(name="newer")
    save_job(j1)
    save_job(j2)

    result = list_jobs()
    assert result[0].name == "newer"
    assert result[1].name == "older"
