"""
Data path resolution for Remedy.

This is the single authoritative location in production Python that reads
REMEDY_DATA_DIR.  All other production modules (run_log.py,
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
    resolve_job_id(raw) -> str               # the one job store; exits on failure
    lookup_job_id(raw) -> str                # the same search, raising JobIdError instead of exiting
    mint_job_id() -> str                     # a job id (16-hex, DECISION F260 D2)
    mint_run_id() -> str                     # a run id
    mint_episode_id() -> str                 # a run-episode id
    mint_task_id() -> str                    # a task id no job file numbered
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
    EPHEMERAL_CLASSES / DURABLE_CLASSES      # the data-root class registry (F276)
    classify_data_child(name) -> "ephemeral" | "durable" | None
    data_class_dir(name, root: Path | None = None) -> Path
"""

from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, NoReturn
from uuid import UUID, uuid4

# DECISION F276 T001: every top-level child of the data root belongs to exactly one
# class, declared here as DATA, so reclaim (T002) addresses a class directory by its
# name and never by a path it composed itself. tests/test_data_root_classes.py scans
# packages/, apps/ and scripts/ for every child the code creates and reds on one that
# is in neither tuple, or in both. "ping-pong runs" and "task jobs", named by the
# feature file, own no directory in today's code: ping-pong results live in ``runs/``
# and its copy staging in ``/tmp/remedy-pingpong-<run_id>``; ``task_jobs/`` was
# retired by DECISION F260 D-A. A legacy one on disk reports as unclassified.

DataClassKind = Literal["ephemeral", "durable"]


@dataclass(frozen=True)
class DataRootClass:
    """One top-level child of the data root: its name, its writer, its reclaim rule.

    ``prefix`` marks a class whose children are named ``<name>.<suffix>`` rather
    than ``<name>`` itself — ``review_staging.XXXXXX``, minted by ``mktemp -d``.
    """

    name: str
    owner: str
    reclaim_rule: str
    prefix: bool = False


EPHEMERAL_CLASSES: tuple[DataRootClass, ...] = (
    DataRootClass("job_workspaces", "packages.orchestration.pingpong_job",
                  "a staging_<job> copy whose job is terminal"),
    DataRootClass("workspaces", "packages.orchestration.workspace",
                  "a <job> workspace whose job is terminal"),
    DataRootClass("runs", "packages.orchestration.pingpong_loop",
                  "a <run> directory whose job is terminal"),
    DataRootClass("job_logs", "packages.orchestration.run_log",
                  "a <job> run log whose job is terminal"),
    DataRootClass("review_staging", "scripts/make_review_zip.sh",
                  "any review_staging.* directory; the script's EXIT trap missed it",
                  prefix=True),
)

DURABLE_CLASSES: tuple[DataRootClass, ...] = (
    DataRootClass("jobs", "packages.orchestration.pingpong_job", "never; the job record and evidence"),
    DataRootClass("projects", "packages.orchestration.project_registry", "never; project registry, ledgers, locks"),
    DataRootClass("missions", "packages.orchestration.mission_state", "never; mission records"),
    DataRootClass("control", "packages.orchestration.safe_points", "never; stop requests and their archive"),
    DataRootClass("stops", "packages.orchestration.stop_reasons", "never; stop-reason log"),
    DataRootClass("proposed_tasks", "packages.orchestration.proposed_tasks", "never; proposed-task records"),
    DataRootClass("evidence_exports", "packages.orchestration.job_evidence", "F166 retention, not F276"),
    DataRootClass("job_evidence_index", "packages.orchestration.evidence_index", "never; evidence index"),
    DataRootClass("job_apply_records", "packages.orchestration.job_apply", "never; apply audit records"),
    DataRootClass("memory", "packages.memory.local_gateway", "never; memory cards"),
    DataRootClass("viewers", "apps.cli.commands.brain", "never; exported brain viewers"),
    DataRootClass("ui", "apps.cli.commands.ui", "never; UI session registry and do logs"),
    DataRootClass("roadmap", "packages.orchestration.roadmap_index", "never; roadmap index and drafts"),
    DataRootClass("self_dogfood", "packages.orchestration.self_dogfood_execution", "never; self-dogfood attempts"),
    DataRootClass("smoke", "scripts/remedy_smoke.sh", "never; smoke summaries `remedy dev` reads"),
)

_DATA_CLASS_KINDS: dict[str, DataClassKind] = {
    **{c.name: "ephemeral" for c in EPHEMERAL_CLASSES},
    **{c.name: "durable" for c in DURABLE_CLASSES},
}
_PREFIX_CLASS_NAMES = tuple(c.name for c in (*EPHEMERAL_CLASSES, *DURABLE_CLASSES) if c.prefix)


def classify_data_child(name: str) -> DataClassKind | None:
    """The class of one top-level data-root child NAME, or None when unregistered."""
    kind = _DATA_CLASS_KINDS.get(name)
    if kind is not None:
        return kind
    for base in _PREFIX_CLASS_NAMES:
        if name.startswith(base + "."):
            return _DATA_CLASS_KINDS[base]
    return None


def data_class_dir(name: str, root: Path | None = None) -> Path:
    """The directory of one REGISTERED class; an unregistered name raises KeyError."""
    if name not in _DATA_CLASS_KINDS:
        raise KeyError(f"not a registered data-root class: {name!r}")
    return (root if root is not None else resolve_data_root()) / name


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
    return data_class_dir("jobs", root)


def runs_dir(root: Path | None = None) -> Path:
    """Return the run store, keyed by RUN id (<root>/runs)."""
    return data_class_dir("runs", root)


def job_logs_dir(root: Path | None = None) -> Path:
    """The job-keyed run-log area (<root>/job_logs)."""
    return data_class_dir("job_logs", root)


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
    return data_class_dir("projects", root)


def workspaces_dir(root: Path | None = None) -> Path:
    """Return the workspaces base directory (<root>/workspaces)."""
    return data_class_dir("workspaces", root)


def viewers_dir(root: Path | None = None) -> Path:
    """Return the brain viewer output directory (<root>/viewers)."""
    return data_class_dir("viewers", root)


def proposed_tasks_dir(root: Path | None = None) -> Path:
    """Return the proposed tasks storage directory (<root>/proposed_tasks)."""
    return data_class_dir("proposed_tasks", root)


def evidence_exports_dir(root: Path | None = None) -> Path:
    """Return the hidden evidence-export base directory (<root>/evidence_exports).

    Evidence bundles default here instead of the repository root, so a working
    tree is never littered with ``remedy-job-evidence-*`` directories.
    """
    return data_class_dir("evidence_exports", root)


def job_evidence_export_dir(job_id: str, root: Path | None = None) -> Path:
    """Return the default export directory for one job's evidence bundle."""
    return evidence_exports_dir(root) / job_id


def job_evidence_index_dir(root: Path | None = None) -> Path:
    """Return the existing job evidence index directory (<root>/job_evidence_index)."""
    return data_class_dir("job_evidence_index", root)


def missions_dir(root: Path | None = None) -> Path:
    """Return the mission storage area (<root>/missions).

    F056: one directory per project below this, holding one atomic JSON file
    per mission record; see ``packages/orchestration/mission_state.py``.
    """
    return data_class_dir("missions", root)


def control_dir(root: Path | None = None) -> Path:
    """Return the control area (<root>/control).

    F011: operator control data — a stop request and its archive — lives here, kept apart
    from the evidence a job produces about itself. It is private (0700/0600); see
    ``packages/orchestration/safe_points.py``.
    """
    return data_class_dir("control", root)


# DECISION F260 D2 (2026-09-06): every Remedy id is ``uuid4().hex[:16]``, but ONE
# SHAPE IS NOT ONE FUNCTION. The same sixteen hex characters already name five
# different kinds of thing, so passing a run id where a job id belongs is not a
# type error and never will be. A name is the weakest distinction Python gives
# away for free, and it is the one thing that makes such a swap greppable, so
# each kind is minted by its own ``def`` below. ``safe_points.new_request_id``
# is the fifth kind and stays where the stop request lives.


def mint_job_id() -> str:
    """Mint the id of one JOB — the administrative unit that hangs under a mission."""
    return uuid4().hex[:16]


def mint_run_id() -> str:
    """Mint the id of one RUN — the evidence case a job points at (DECISION F260 D1)."""
    return uuid4().hex[:16]


def mint_episode_id() -> str:
    """Mint the id of one EPISODE — one execution attempt of a run; a resume gets its own."""
    return uuid4().hex[:16]


def mint_task_id() -> str:
    """Mint the id of one TASK that no job file numbered — a task built by code, not parsed."""
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


def _task_job_id_matches(prefix: str) -> list[str]:
    """Every id in the job store starting with ``prefix``.

    One directory per job under ``<data_root>/jobs/``, holding a ``job.json``, so
    the id is the directory name. A directory without a ``job.json`` is not a job —
    a half-created or hand-made directory must not be resolvable as one — and a
    plain file in ``jobs/`` is not a job either.
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
    """A well-formed prefix that matches no job."""


class JobIdAmbiguous(JobIdError):
    """A prefix that matches more than one job; ``matches`` lists them, sorted."""

    def __init__(self, raw: str, matches: list[str]) -> None:
        self.raw = raw
        self.matches = sorted(matches)
        super().__init__(
            f"ambiguous job id prefix {raw!r} matches {len(self.matches)} jobs"
        )


# UUID(...) was the id-shape check while every job id was a UUID, and it refuses the sixteen-hex id mint_job_id mints.
_JOB_ID_HEX16_RE = re.compile(r"[0-9a-f]{16}")


def normalize_job_id(raw: str) -> str:
    """Check a job id's SHAPE and return its canonical spelling, or RAISE.

    A string ``UUID(...)`` accepts comes back as ``str(UUID(raw))``; sixteen
    lowercase hex characters, the shape :func:`mint_job_id` mints, come back
    unchanged; anything else raises :class:`JobIdInvalid`. It reads no disk and
    resolves no prefix — :func:`lookup_job_id` is the function that does.
    """
    try:
        return str(UUID(raw))
    except ValueError:
        pass
    if _JOB_ID_HEX16_RE.fullmatch(raw):
        return raw
    raise JobIdInvalid(f"invalid job ID: {raw!r}")


def lookup_job_id(raw: str) -> str:
    """Resolve a full job id or a short hex prefix against the job store, or RAISE.

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

    matches = sorted(_task_job_id_matches(raw))
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        raise JobIdAmbiguous(raw, matches)
    raise JobIdNotFound(f"no job matches prefix {raw!r}")


def resolve_job_id(raw: str) -> str:
    """Resolve a full job id or a short hex prefix against the job store.

    Every job is one record at ``<data_root>/jobs/<id>/job.json``, so a prefix
    resolves to the one directory holding a ``job.json`` whose name starts with it.
    The job's run log lives under ``<data_root>/job_logs/<job-id>/``, so
    ``timeline.load_run_events`` reaches it by the id returned here.

    Returns a ``str``. A full UUID comes back in the form ``str(UUID(...))``
    produces, without touching the disk; a prefix comes back as the matching
    directory name.

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
    except JobIdError:
        print(f"Error: No job matches {raw!r}. Try: remedy job list.", file=sys.stderr)
        sys.exit(1)

