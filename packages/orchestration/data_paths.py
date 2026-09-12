"""
Data path resolution for Remedy.

This is the single authoritative location in production Python that reads
REMEDY_DATA_DIR.  All other production modules (storage.py, run_log.py,
project_registry.py, workspace.py, apps/cli/main.py) must import helpers
from this module instead of reading the environment variable directly.

Resolution order (via config system):
  1. REMEDY_DATA_DIR environment variable
  2. Project remedy.toml [remedy] data_dir
  3. User ~/.config/remedy/remedy.toml [remedy] data_dir
  4. Repository-local default: <repo_root>/.data

Public API::

    resolve_data_root() -> Path
    jobs_dir(root: Path | None = None) -> Path
    resolve_job_id(raw) -> str               # both job stores; resolve_any_job_id is an alias
    lookup_job_id(raw) -> str                # the same search, raising JobIdError instead of exiting
    mint_job_id() -> str                     # a job id (16-hex, DECISION F260 D2)
    mint_run_id() -> str                     # a run id
    mint_episode_id() -> str                 # a run-episode id
    job_dir(job_id, root: Path | None = None) -> Path
    job_record_path(job_id, root: Path | None = None) -> Path
    job_record_paths(root: Path | None = None) -> list[Path]
    job_evidence_dir(job_id, root: Path | None = None) -> Path
    runs_dir(root: Path | None = None) -> Path               # keyed by RUN id
    run_dir(run_id, root: Path | None = None) -> Path
    job_logs_dir(root: Path | None = None) -> Path           # keyed by JOB id
    run_log_dir(job_id, root: Path | None = None) -> Path
    projects_dir(root: Path | None = None) -> Path
    workspaces_dir(root: Path | None = None) -> Path
    viewers_dir(root: Path | None = None) -> Path
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import NoReturn
from uuid import UUID, uuid4


def resolve_data_root() -> Path:
    """Return the Remedy data root directory.

    Env var checked directly (always fresh) for backward compatibility with
    tests that set REMEDY_DATA_DIR at runtime. TOML config checked via cached
    config system for file-based overrides.
    The returned path is NOT guaranteed to exist — callers must mkdir as needed.
    """
    env = os.environ.get("REMEDY_DATA_DIR")
    if env:
        return Path(env)
    from packages.orchestration.config import get_config

    configured = get_config().get("data_dir")
    if configured:
        return Path(configured)
    # packages/orchestration/data_paths.py → repo root is 3 levels up
    repo_root = Path(__file__).resolve().parents[2]
    return repo_root / ".data"


def jobs_dir(root: Path | None = None) -> Path:
    """Return the jobs storage directory (<root>/jobs)."""
    return (root if root is not None else resolve_data_root()) / "jobs"


def runs_dir(root: Path | None = None) -> Path:
    """Return the run store, keyed by RUN id (<root>/runs)."""
    return (root if root is not None else resolve_data_root()) / "runs"


def job_logs_dir(root: Path | None = None) -> Path:
    """The job-keyed run-log area (<root>/job_logs)."""
    return (root if root is not None else resolve_data_root()) / "job_logs"


# The run-log store, keyed by JOB id and living at ``<data_root>/job_logs/<job_id>/``
# since DECISION F272 D1 moved it out of ``runs/``. It moved because ``runs/`` is
# now keyed by RUN id and nothing else, which is what DECISION F260 D0 required
# before any directory moved; the move was one function body because every one of
# the 74 readers and 35 writers resolves through ``run_log_dir`` rather than
# spelling the path. Whether this log ultimately merges INTO the per-run directory
# is NOT settled — DECISION F272 D1 defers that to T003, where the consumers move.


def run_log_dir(job_id: UUID | str, root: Path | None = None) -> Path:
    """One JOB's run-log directory (<root>/job_logs/<job_id>)."""
    return job_logs_dir(root) / str(job_id)


def projects_dir(root: Path | None = None) -> Path:
    """Return the projects storage directory (<root>/projects)."""
    return (root if root is not None else resolve_data_root()) / "projects"


def workspaces_dir(root: Path | None = None) -> Path:
    """Return the workspaces base directory (<root>/workspaces)."""
    return (root if root is not None else resolve_data_root()) / "workspaces"


def viewers_dir(root: Path | None = None) -> Path:
    """Return the brain viewer output directory (<root>/viewers)."""
    return (root if root is not None else resolve_data_root()) / "viewers"


def proposed_tasks_dir(root: Path | None = None) -> Path:
    """Return the proposed tasks storage directory (<root>/proposed_tasks)."""
    return (root if root is not None else resolve_data_root()) / "proposed_tasks"


def evidence_exports_dir(root: Path | None = None) -> Path:
    """Return the hidden evidence-export base directory (<root>/evidence_exports).

    Evidence bundles default here instead of the repository root, so a working
    tree is never littered with ``remedy-job-evidence-*`` directories.
    """
    return (root if root is not None else resolve_data_root()) / "evidence_exports"


def job_evidence_export_dir(job_id: str, root: Path | None = None) -> Path:
    """Return the default export directory for one job's evidence bundle."""
    return evidence_exports_dir(root) / job_id


def job_evidence_index_dir(root: Path | None = None) -> Path:
    """Return the existing job evidence index directory (<root>/job_evidence_index)."""
    return (root if root is not None else resolve_data_root()) / "job_evidence_index"


def queue_dir(root: Path | None = None) -> Path:
    """Return the job-queue area (<root>/queue).

    F048: one directory per project below this, holding one JSON file per queue
    entry plus its claim marker; see ``packages/orchestration/job_queue.py``.
    """
    return (root if root is not None else resolve_data_root()) / "queue"


def missions_dir(root: Path | None = None) -> Path:
    """Return the mission storage area (<root>/missions).

    F056: one directory per project below this, holding one atomic JSON file
    per mission record; see ``packages/orchestration/mission_state.py``.
    """
    return (root if root is not None else resolve_data_root()) / "missions"


def control_dir(root: Path | None = None) -> Path:
    """Return the control area (<root>/control).

    F011: operator control data — a stop request and its archive — lives here, kept apart
    from the evidence a job produces about itself. It is private (0700/0600); see
    ``packages/orchestration/safe_points.py``.
    """
    return (root if root is not None else resolve_data_root()) / "control"


# DECISION F260 D2 (2026-09-06): every Remedy id is ``uuid4().hex[:16]``, but ONE
# SHAPE IS NOT ONE FUNCTION. The same sixteen hex characters already name four
# different kinds of thing, so passing a run id where a job id belongs is not a
# type error and never will be. A name is the weakest distinction Python gives
# away for free, and it is the one thing that makes such a swap greppable, so
# each kind is minted by its own ``def`` below. ``safe_points.new_request_id``
# is the fourth kind and stays where the stop request lives.


def mint_job_id() -> str:
    """Mint the id of one JOB — the administrative unit that hangs under a mission."""
    return uuid4().hex[:16]


def mint_run_id() -> str:
    """Mint the id of one RUN — the evidence case a job points at (DECISION F260 D1)."""
    return uuid4().hex[:16]


def mint_episode_id() -> str:
    """Mint the id of one EPISODE — one execution attempt of a run; a resume gets its own."""
    return uuid4().hex[:16]


# DECISION F260 D1 (2026-09-06): ONE ROOT PER JOB — the record at
# ``<data_root>/jobs/<16hex>/job.json``, that job's evidence at
# ``<data_root>/jobs/<16hex>/evidence/``, and runs keyed by RUN id under
# ``<data_root>/runs/<run_id>/``. That layout was spelled BY HAND at six call
# sites in five modules, which is finding R-0814's root cause: "one spelling per
# concept" failing first inside a file and then across them. ``data_paths``
# already owns every other "where does this live" answer, so it owns these too,
# and each function below is built on the one above it rather than re-deriving
# the root — a layout change then has exactly one place to happen.


def job_dir(job_id: str, root: Path | None = None) -> Path:
    """The one directory holding everything about one JOB."""
    return jobs_dir(root) / job_id


def job_record_path(job_id: str, root: Path | None = None) -> Path:
    """The job's own record — its plan, status and tasks as one JSON file.

    ``pingpong_job._persist_job`` WRITES HERE: F260 T002 moved the ping-pong
    record onto this path, so the record and that job's evidence now hang off
    the one ``job_dir`` above. ``pingpong_job.load_job_plan`` reads it back.
    """
    return job_dir(job_id, root) / "job.json"


# The SHAPE of the job store — one directory per job, the record inside it named
# ``job.json`` — is a layout fact, and DECISION F260 D1 puts every layout fact in this
# module, so a caller that globbed for itself would be the second place a layout change
# has to happen.


def job_record_paths(root: Path | None = None) -> list[Path]:
    """Every persisted job record under ``root``, sorted by path.

    The plural of ``job_record_path`` above. Returns ``[]`` when the jobs directory
    does not exist, so no caller has to decide whether "no jobs" and "no store"
    differ.
    """
    jdir = jobs_dir(root)
    if not jdir.is_dir():
        return []
    return sorted(jdir.glob("*/job.json"))


def job_evidence_dir(job_id: str, root: Path | None = None) -> Path:
    """The job's own evidence — artifacts, streams and post-mortems, beside its record."""
    return job_dir(job_id, root) / "evidence"


def run_dir(run_id: str, root: Path | None = None) -> Path:
    """One RUN's log directory, keyed by RUN id and never by job id (DECISION F260 D1)."""
    return runs_dir(root) / run_id


_SHORT_HEX_RE = re.compile(r"[0-9a-fA-F]{4,32}")


def _classic_job_id_matches(prefix: str) -> list[str]:
    """Every id in the CLASSIC job store starting with ``prefix``.

    One ``<uuid>.json`` file per job, so the id is the file stem.
    """
    jdir = jobs_dir()
    if not jdir.exists():
        return []
    lower = prefix.lower()
    return [
        p.stem for p in jdir.glob("*.json")
        if p.stem.lower().startswith(lower)
    ]


def _task_job_id_matches(prefix: str) -> list[str]:
    """Every id in the TASK-JOB store starting with ``prefix``.

    Since F260 T002 both stores live under ``<data_root>/jobs/``: the classic
    one as ``<uuid>.json`` FILES, this one as ``<16hex>/`` DIRECTORIES holding
    a ``job.json``. The ``is_dir()`` test plus the ``job.json`` check is what
    keeps the two populations apart — a classic ``<uuid>.json`` file is not a
    directory and never reaches this reading, and the sibling
    :func:`_classic_job_id_matches` globs ``*.json`` and so never sees a
    ping-pong directory.

    One directory per job, so the id is the directory name. A directory
    without a ``job.json`` is not a job — a half-created or hand-made
    directory must not be resolvable as one.
    """
    tdir = jobs_dir()
    if not tdir.exists():
        return []
    lower = prefix.lower()
    return [
        p.name for p in tdir.iterdir()
        if p.is_dir()
        and p.name.lower().startswith(lower)
        and (p / "job.json").is_file()
    ]


def _exit_ambiguous(raw: str, matches: list[str]) -> NoReturn:
    print(f"Error: ambiguous job id prefix '{raw}' matches "
          f"{len(matches)} jobs:", file=sys.stderr)
    for m in sorted(matches):
        print(f"  {m[:8]}", file=sys.stderr)
    sys.exit(2)


class JobIdError(ValueError):
    """A job id string that does not name exactly one job.

    It is a ``ValueError`` ON PURPOSE. The CLI handlers parsed a job id with
    ``UUID(...)``, which raises ``ValueError``, and they guard that parse with
    ``except ValueError`` or wider; several of those guards select a documented
    path of their own — a JSON error payload, a ``job_not_found`` document —
    instead of ending the process. A handler that routes its parse through
    :func:`lookup_job_id` therefore keeps that path, which a ``SystemExit`` from
    :func:`resolve_job_id` would escape.
    """


class JobIdInvalid(JobIdError):
    """The string is neither a full UUID nor a short hex prefix."""


class JobIdNotFound(JobIdError):
    """A well-formed prefix that matches no job in either store."""


class JobIdAmbiguous(JobIdError):
    """A prefix that matches more than one job; ``matches`` lists them, sorted."""

    def __init__(self, raw: str, matches: list[str]) -> None:
        self.raw = raw
        self.matches = sorted(matches)
        super().__init__(
            f"ambiguous job id prefix {raw!r} matches {len(self.matches)} jobs"
        )


def lookup_job_id(raw: str) -> str:
    """Resolve a full job id or a short hex prefix across BOTH job stores, or RAISE.

    The search :func:`resolve_job_id` documents, and the same return values, but a
    failure raises a :class:`JobIdError` instead of ending the process:
    :class:`JobIdInvalid` for a string that is neither a UUID nor a hex prefix,
    :class:`JobIdNotFound` for a prefix no job matches, :class:`JobIdAmbiguous`
    for a prefix more than one job matches. A full UUID returns without touching
    the disk. READ-ONLY, like :func:`resolve_job_id`.
    """
    try:
        return str(UUID(raw))
    except ValueError:
        pass

    if not _SHORT_HEX_RE.fullmatch(raw):
        raise JobIdInvalid(f"invalid job ID: {raw!r}")

    matches = sorted(set(_classic_job_id_matches(raw)) | set(_task_job_id_matches(raw)))
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        raise JobIdAmbiguous(raw, matches)
    raise JobIdNotFound(f"no job matches prefix {raw!r}")


def resolve_job_id(raw: str) -> str:
    """Resolve a full job id or a short hex prefix across BOTH job stores.

    Remedy runs jobs into two stores. ``<data_root>/jobs/<uuid>.json`` is the
    classic one; ``<data_root>/jobs/<16hex>/job.json`` is the one
    ``remedy do job-run`` writes. Since F260 T002 both stores share the one
    ``jobs/`` directory and are told apart by FILE versus DIRECTORY: the classic
    id is a ``.json`` file's stem, the ping-pong id is a directory holding a
    ``job.json``. Both file their run logs the same way, under
    ``<data_root>/job_logs/<job-id>/``, so ``timeline.load_run_events`` reaches
    either. This function searches both stores. Until F275 T003 it searched the
    classic store alone, where a 16-hex ping-pong id can never match — which is
    why `remedy teach narrate <task-job-id>` answered "no job matches prefix"
    for a job whose run log was sitting on disk the whole time (operator
    dogfooding, 2026-08-25). The two searches are unioned and deduplicated, so
    an id that is present in both stores is one match rather than a false
    ambiguity.

    Returns a ``str`` because the two stores mint different id shapes and only
    one of them is a UUID. A full UUID comes back in the form ``str(UUID(...))``
    produces; a prefix comes back as the matching file stem or directory name.

    READ-ONLY: this opens directories and stats files, and writes nothing —
    which is what lets the teacher, whose whole stance is passivity, use it.

    Exits with code 1 on invalid input or no match, code 2 on an ambiguous
    prefix.

    The search itself is :func:`lookup_job_id`; this function is its EXITING
    form, for a command that has no failure path of its own. A handler that
    guards its parse calls :func:`lookup_job_id` and catches the ``ValueError``.
    """
    try:
        return lookup_job_id(raw)
    except JobIdAmbiguous as exc:
        _exit_ambiguous(raw, exc.matches)
    except JobIdError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


# ``resolve_any_job_id`` is an ALIAS of ``resolve_job_id``, not a copy: F275 T003
# collapsed the two resolvers, which had differed in one statement, and an alias is
# one function under two names, so the two cannot drift apart again. The name is
# kept because the callers under ``apps/cli/`` read it as saying they need both job
# stores. ``tests/test_data_paths.py`` pins the identity.
resolve_any_job_id = resolve_job_id
