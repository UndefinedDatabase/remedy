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
    resolve_job_id(raw) -> str               # the classic store
    resolve_any_job_id(raw) -> str           # both stores
    mint_job_id() -> str                     # a job id (16-hex, DECISION F260 D2)
    mint_run_id() -> str                     # a run id
    mint_episode_id() -> str                 # a run-episode id
    job_dir(job_id, root: Path | None = None) -> Path
    job_record_path(job_id, root: Path | None = None) -> Path
    job_evidence_dir(job_id, root: Path | None = None) -> Path
    run_dir(run_id, root: Path | None = None) -> Path
    runs_dir(root: Path | None = None) -> Path
    pingpong_runs_dir(root: Path | None = None) -> Path    # the LIVE run store
    pingpong_run_dir(run_id, root: Path | None = None) -> Path
    projects_dir(root: Path | None = None) -> Path
    workspaces_dir(root: Path | None = None) -> Path
    viewers_dir(root: Path | None = None) -> Path
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
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
    """Return the run-log base directory (<root>/runs)."""
    return (root if root is not None else resolve_data_root()) / "runs"


# The LIVE run-log store, named as it is TODAY: ``<data_root>/runs/<job_id>/``,
# keyed by JOB id. ``run_dir`` below is the TARGET spelling and is keyed by RUN
# id: DECISION F260 D1 re-keys this directory by run id, so the two are NOT the
# same function and are not merged here. Giving the live layout ONE spelling is
# what turns D1's re-key into a change to the body below instead of a sweep of
# every caller — the same move rounds 11 and 12 made for the ping-pong run store.


def run_log_dir(job_id: UUID | str, root: Path | None = None) -> Path:
    """One JOB's run-log directory as it is today (<root>/runs/<job_id>)."""
    return runs_dir(root) / str(job_id)


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


def job_evidence_dir(job_id: str, root: Path | None = None) -> Path:
    """The job's own evidence — artifacts, streams and post-mortems, beside its record."""
    return job_dir(job_id, root) / "evidence"


def run_dir(run_id: str, root: Path | None = None) -> Path:
    """One RUN's log directory, keyed by RUN id and never by job id (DECISION F260 D1)."""
    return runs_dir(root) / run_id


# The LIVE ping-pong run store, named as it is TODAY: ``<data_root>/pingpong_runs/``.
# ``run_dir`` above is the TARGET spelling and this pair is the LIVE one — exactly
# the relationship ``job_dir`` and ``task_job_dir`` had before F260 round 9
# collapsed them. DECISION F260 D1 says a run belongs at
# ``<data_root>/runs/<run_id>/``, and until round 11 the live store was spelled by
# ``pingpong_loop._pingpong_runs_dir`` with thirty-nine references hanging off it.
# Giving it ONE spelling here is what turns D1's collapse into a change to the two
# function bodies below instead of a sweep of every caller; that collapse is F260
# T002's remaining work.


def pingpong_runs_dir(root: Path | None = None) -> Path:
    """The ping-pong run store as it is today (<root>/pingpong_runs)."""
    return (root if root is not None else resolve_data_root()) / "pingpong_runs"


def pingpong_run_dir(run_id: str, root: Path | None = None) -> Path:
    """One ping-pong RUN's directory, keyed by run id, under the live run store."""
    return pingpong_runs_dir(root) / run_id


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


def _exit_ambiguous(raw: str, matches: list[str]) -> None:
    print(f"Error: ambiguous job id prefix '{raw}' matches "
          f"{len(matches)} jobs:", file=sys.stderr)
    for m in sorted(matches):
        print(f"  {m[:8]}", file=sys.stderr)
    sys.exit(2)


def resolve_job_id(raw: str) -> str:
    """Parse a full UUID or resolve a short hex prefix to a unique job id.

    Searches the CLASSIC job store ONLY — that restriction is now carried by
    the SEARCH, not by the return type, since a ``str`` could hold either id
    shape. Callers that must reach both stores use :func:`resolve_any_job_id`.

    Returns the canonical id as a string: lowercase, hyphenated, the form
    ``str(UUID(...))`` produces. F260 T004 is where this function and
    :func:`resolve_any_job_id` become one.

    Exits with code 1 on invalid input, code 2 on ambiguous prefix.
    """
    try:
        return str(UUID(raw))
    except ValueError:
        pass

    if not _SHORT_HEX_RE.fullmatch(raw):
        print(f"Error: invalid job ID: {raw!r}", file=sys.stderr)
        sys.exit(1)

    matches = _classic_job_id_matches(raw)
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        _exit_ambiguous(raw, matches)

    print(f"Error: no job matches prefix {raw!r}", file=sys.stderr)
    sys.exit(1)


def resolve_any_job_id(raw: str) -> str:
    """Resolve a job id across BOTH job stores, and return it as a string.

    Remedy runs jobs into two stores. ``<data_root>/jobs/<uuid>.json`` is the
    classic one; ``<data_root>/jobs/<16hex>/job.json`` is the one
    ``remedy do job-run`` writes. Since F260 T002 both stores share the one
    ``jobs/`` directory and are told apart by FILE versus DIRECTORY: the classic
    id is a ``.json`` file's stem, the ping-pong id is a directory holding a
    ``job.json``. Both file their run logs the same way, under
    ``<data_root>/runs/<job-id>/``, so ``timeline.load_run_events`` reaches
    either — but :func:`resolve_job_id` SEARCHES only the classic store, where a
    16-hex task-job id can never match. Both now return a ``str``; F260 T004 is
    where the two become one.

    That is why `remedy teach narrate <task-job-id>` answered "no job matches
    prefix" for a job whose run log was sitting on disk the whole time
    (operator dogfooding, 2026-08-25). The teacher was built against the
    classic store and could not see a job-based run at all.

    The return type is ``str`` because the two stores mint different id shapes
    and only one of them is a UUID. Callers print it or join it onto a path;
    nothing needs the parsed form.

    READ-ONLY: this opens directories and stats files, and writes nothing —
    which is what lets the teacher, whose whole stance is passivity, use it.

    Exits with code 1 on invalid input or no match, code 2 on an ambiguous
    prefix — the same codes, and the same messages, :func:`resolve_job_id`
    uses, so no caller gains a new exit path by switching.
    """
    try:
        return str(UUID(raw))
    except ValueError:
        pass

    if not _SHORT_HEX_RE.fullmatch(raw):
        print(f"Error: invalid job ID: {raw!r}", file=sys.stderr)
        sys.exit(1)

    # A single id could in principle live in both stores; dedupe so that is a
    # match rather than a false ambiguity.
    matches = sorted(set(_classic_job_id_matches(raw)) | set(_task_job_id_matches(raw)))
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        _exit_ambiguous(raw, matches)

    print(f"Error: no job matches prefix {raw!r}", file=sys.stderr)
    sys.exit(1)
