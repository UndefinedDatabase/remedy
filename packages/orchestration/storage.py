"""
Job persistence layer.

Jobs are stored as JSON files under <data_dir>/<job_id>.json.

Storage location resolution order:
1. REMEDY_DATA_DIR environment variable, if set.
2. Repository-local default: <repo_root>/.data/jobs

No database. No external dependencies.
"""

from __future__ import annotations

import os
from pathlib import Path
from uuid import UUID

from packages.core.models import Job


class JobNotFoundError(Exception):
    """Raised when a requested Job cannot be found in storage."""

    def __init__(self, job_id: UUID) -> None:
        super().__init__(f"Job not found: {job_id}")
        self.job_id = job_id


def _resolve_data_dir() -> Path:
    """Resolve the storage directory.

    Checks REMEDY_DATA_DIR env var first; falls back to <repo_root>/.data/jobs.
    """
    env = os.environ.get("REMEDY_DATA_DIR")
    if env:
        return Path(env)
    # packages/orchestration/storage.py → repo root is 3 levels up
    repo_root = Path(__file__).resolve().parent.parent.parent
    return repo_root / ".data" / "jobs"


_DATA_DIR: Path = _resolve_data_dir()


def save_job(job: Job) -> None:
    """Persist a Job to disk as JSON."""
    _DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = _DATA_DIR / f"{job.id}.json"
    path.write_text(job.model_dump_json(indent=2))


def load_job(job_id: UUID) -> Job:
    """Load a Job from disk by ID.

    Raises JobNotFoundError if the job does not exist.
    """
    path = _DATA_DIR / f"{job_id}.json"
    if not path.exists():
        raise JobNotFoundError(job_id)
    return Job.model_validate_json(path.read_text())


def list_jobs() -> list[Job]:
    """Return all persisted jobs sorted by created_at descending (newest first).

    Corrupted or unreadable files are silently skipped.
    """
    if not _DATA_DIR.exists():
        return []
    jobs: list[Job] = []
    for path in _DATA_DIR.glob("*.json"):
        try:
            jobs.append(Job.model_validate_json(path.read_text()))
        except Exception:
            pass  # skip corrupted files; will be surfaced in a later step
    return sorted(jobs, key=lambda j: j.created_at, reverse=True)
