"""
Smoke tests for the Job persistence layer.
"""

from __future__ import annotations

import pytest
from uuid import uuid4

from packages.core.models import Job, RunState
from packages.orchestration.storage import save_job, load_job


def test_save_and_load_job(tmp_path, monkeypatch):
    """Jobs saved to disk can be loaded back with identical fields."""
    import packages.orchestration.storage as storage
    monkeypatch.setattr(storage, "_DATA_DIR", tmp_path / "jobs")

    job = Job(name="test-job", user_prompt="do something", state=RunState.PENDING)
    save_job(job)
    loaded = load_job(job.id)

    assert loaded.id == job.id
    assert loaded.name == job.name
    assert loaded.user_prompt == job.user_prompt
    assert loaded.state == RunState.PENDING


def test_load_missing_job_raises(tmp_path, monkeypatch):
    """Loading a non-existent job raises FileNotFoundError."""
    import packages.orchestration.storage as storage
    monkeypatch.setattr(storage, "_DATA_DIR", tmp_path / "jobs")

    with pytest.raises(FileNotFoundError):
        load_job(uuid4())
