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
    task_jobs_dir(root: Path | None = None) -> Path
    resolve_job_id(raw) -> UUID              # the classic store
    resolve_any_job_id(raw) -> str           # both stores
    mint_job_id() -> str                     # a job id (16-hex, DECISION F260 D2)
    mint_run_id() -> str                     # a run id
    mint_episode_id() -> str                 # a run-episode id
    runs_dir(root: Path | None = None) -> Path
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


def task_jobs_dir(root: Path | None = None) -> Path:
    """Return the ping-pong task-job storage directory (<root>/task_jobs).

    Remedy has TWO job stores and they are shaped differently. The classic
    store above holds one ``<uuid>.json`` file per job. This one holds one
    DIRECTORY per job, named by a 16-hex id (``uuid4().hex[:16]``), containing
    ``job.json`` and the run's artifacts; ``packages.orchestration.pingpong_job``
    writes it and ``remedy do job-run`` fills it.

    Named here, beside the store it is a sibling of, so the two spellings of
    "where the task jobs live" cannot drift apart.
    """
    return (root if root is not None else resolve_data_root()) / "task_jobs"


def runs_dir(root: Path | None = None) -> Path:
    """Return the run-log base directory (<root>/runs)."""
    return (root if root is not None else resolve_data_root()) / "runs"


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

    One directory per job, so the id is the directory name. A directory
    without a ``job.json`` is not a job — a half-created or hand-made
    directory must not be resolvable as one.
    """
    tdir = task_jobs_dir()
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


def resolve_job_id(raw: str) -> UUID:
    """Parse a full UUID or resolve a short hex prefix to a unique job UUID.

    Searches the CLASSIC job store only, and its return type says so: a
    task-job id is sixteen hex characters and ``UUID()`` rejects it. Callers
    that must reach both stores use :func:`resolve_any_job_id`.

    Exits with code 1 on invalid input, code 2 on ambiguous prefix.
    """
    try:
        return UUID(raw)
    except ValueError:
        pass

    if not _SHORT_HEX_RE.fullmatch(raw):
        print(f"Error: invalid job ID: {raw!r}", file=sys.stderr)
        sys.exit(1)

    matches = _classic_job_id_matches(raw)
    if len(matches) == 1:
        return UUID(matches[0])
    if len(matches) > 1:
        _exit_ambiguous(raw, matches)

    print(f"Error: no job matches prefix {raw!r}", file=sys.stderr)
    sys.exit(1)


def resolve_any_job_id(raw: str) -> str:
    """Resolve a job id across BOTH job stores, and return it as a string.

    Remedy runs jobs into two stores. ``<data_root>/jobs/<uuid>.json`` is the
    classic one; ``<data_root>/task_jobs/<16-hex>/job.json`` is the one
    ``remedy do job-run`` writes. Both file their run logs the same way, under
    ``<data_root>/runs/<job-id>/``, so ``timeline.load_run_events`` reaches
    either — but :func:`resolve_job_id` searches only the classic store and
    returns a ``UUID``, which a 16-hex task-job id can never be.

    That is why `remedy teach narrate <task-job-id>` answered "no job matches
    prefix" for a job whose run log was sitting on disk the whole time
    (operator dogfooding, 2026-08-25). The teacher was built against the
    classic store and could not see a job-based run at all.

    The return type is ``str`` rather than ``UUID`` because the two stores mint
    different id shapes and only one of them is a UUID. Callers print it or
    join it onto a path; nothing needs the parsed form.

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
