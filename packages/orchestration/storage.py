"""
Job persistence layer.

Jobs are stored as JSON files under <data_dir>/jobs/<job_id>.json.

Storage location resolution order:
1. Explicit root= parameter, if passed.
2. REMEDY_DATA_DIR environment variable, if set.
3. Repository-local default: <repo_root>/.data/jobs

Resolution is delegated to packages.orchestration.data_paths — that module
is the single authoritative reader of REMEDY_DATA_DIR in production Python.

No database. No external dependencies.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from uuid import UUID

from packages.core.models import Job
from packages.orchestration.data_paths import jobs_dir


class JobNotFoundError(Exception):
    """Raised when a requested Job cannot be found in storage."""

    def __init__(self, job_id: UUID | str) -> None:
        super().__init__(f"Job not found: {job_id}")
        self.job_id = job_id


class JobStoreError(Exception):
    """Raised when job storage is corrupt or unreadable."""


# Legacy compat: monkeypatchable in old tests (deprecated, use root= param)
_DATA_DIR: Path | None = None


def _resolve_jobs_dir(root: Path | None = None) -> Path:
    if root is not None:
        return root / "jobs"
    if _DATA_DIR is not None:
        return _DATA_DIR
    return jobs_dir()


def _atomic_write_job(path: Path, data: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    closed = False
    try:
        os.write(fd, data.encode("utf-8"))
        os.fsync(fd)
        os.close(fd)
        closed = True
        os.replace(tmp, str(path))
    except BaseException:
        if not closed:
            try:
                os.close(fd)
            except OSError:
                pass
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def save_job(job: Job, root: Path | None = None) -> None:
    """Persist a Job to disk as JSON (atomic write)."""
    jdir = _resolve_jobs_dir(root)
    jdir.mkdir(parents=True, exist_ok=True)
    path = jdir / f"{job.id}.json"
    _atomic_write_job(path, job.model_dump_json(indent=2))


# Takes BOTH spellings on purpose: ``Job.id`` is a ``UUID`` model field and many
# callers pass ``job.id`` straight in, while a resolver now hands back a ``str``.
def load_job(job_id: UUID | str, root: Path | None = None) -> Job:
    """Load a Job from disk by ID.

    Accepts the id as a ``UUID`` or as a ``str``; the path is built by
    formatting it, which both spellings do identically.

    Raises JobNotFoundError if the job does not exist.
    Raises JobStoreError if the file exists but is corrupt.
    """
    path = _resolve_jobs_dir(root) / f"{job_id}.json"
    if not path.exists():
        raise JobNotFoundError(job_id)
    try:
        return Job.model_validate_json(path.read_text())
    except (ValueError, TypeError, KeyError) as exc:
        raise JobStoreError(f"Corrupt job file for {job_id}: {exc}") from exc
    except OSError as exc:
        raise JobStoreError(f"Cannot read job file for {job_id}: {exc}") from exc


def load_job_safe(job_id: UUID | str, root: Path | None = None) -> tuple[Job | None, bool]:
    """Load a Job, returning (job, degraded).

    Returns (None, True) if corrupt, (None, False) if not found, (job, False) if ok.
    """
    try:
        return (load_job(job_id, root), False)
    except JobNotFoundError:
        return (None, False)
    except JobStoreError:
        return (None, True)


def list_jobs(root: Path | None = None) -> list[Job]:
    """Return all persisted jobs sorted by created_at descending.

    Corrupted or unreadable files are silently skipped.
    Use list_jobs_safe() to detect skipped files.
    """
    result, _, _ = list_jobs_safe(root)
    return result


def list_jobs_safe(root: Path | None = None) -> tuple[list[Job], bool, list[str]]:
    """List jobs with corruption visibility. Returns (jobs, degraded, skipped_files)."""
    jdir = _resolve_jobs_dir(root)
    if not jdir.exists():
        return ([], False, [])
    jobs: list[Job] = []
    skipped: list[str] = []
    for path in jdir.glob("*.json"):
        try:
            jobs.append(Job.model_validate_json(path.read_text()))
        except (ValueError, OSError):
            skipped.append(path.name)
    jobs.sort(key=lambda j: j.created_at, reverse=True)
    return (jobs, len(skipped) > 0, skipped)
