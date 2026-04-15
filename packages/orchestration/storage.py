"""
Simple Job persistence layer.

Jobs are stored as JSON files under .data/jobs/<job_id>.json,
relative to the current working directory.

No database. No external dependencies.
"""

from __future__ import annotations

from pathlib import Path
from uuid import UUID

from packages.core.models import Job

_DATA_DIR = Path(".data/jobs")


def save_job(job: Job) -> None:
    """Persist a Job to disk as JSON."""
    _DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = _DATA_DIR / f"{job.id}.json"
    path.write_text(job.model_dump_json(indent=2))


def load_job(job_id: UUID) -> Job:
    """Load a Job from disk by ID.

    Raises FileNotFoundError if the job does not exist.
    """
    path = _DATA_DIR / f"{job_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"Job not found: {job_id}")
    return Job.model_validate_json(path.read_text())
