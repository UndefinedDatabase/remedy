"""Evidence index helpers — one record per exported job evidence bundle.

Writes and reads the EXISTING index at ``<REMEDY_DATA_DIR>/job_evidence_index/``
(one ``<job_id>.json`` per job). No second index format is introduced: this
module only centralizes the record shape and adds the repository/branch/commit
fields review-zip selection needs, while preserving the keys older writers and
``ui_server`` already rely on (``evidence_dir_local``, ``created_at``, ...).

Selection rules (used by the review-zip selector):

* only jobs whose recorded repository matches the current resolved repository;
* prefer the current branch;
* require review-subject alignment — the recorded changed source/test file set
  must be consistent with the current working tree;
* newest matching export wins, by recorded export timestamp, never by raw
  filesystem modification time of an unrelated directory.
"""
from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from packages.orchestration.data_paths import job_evidence_index_dir

SCHEMA_VERSION = "1.1.0"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _git(repo: str | Path, *args: str) -> str:
    try:
        r = subprocess.run(
            ["git", *args], cwd=str(repo), capture_output=True, text=True, timeout=15,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return r.stdout.strip() if r.returncode == 0 else ""


def _git_raw(repo: str | Path, *args: str) -> str:
    """Like ``_git`` but preserves leading whitespace.

    ``git status --porcelain`` encodes the status in the first two columns, so a
    modified-but-unstaged file starts with a space. Stripping the output would
    shift the first line left and silently truncate its path.
    """
    try:
        r = subprocess.run(
            ["git", *args], cwd=str(repo), capture_output=True, text=True, timeout=15,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return r.stdout if r.returncode == 0 else ""


def repo_identity(repo_path: str | Path) -> dict[str, str]:
    """Resolve repository path, branch and commit for an index record."""
    root = _git(repo_path, "rev-parse", "--show-toplevel") or str(Path(repo_path).resolve())
    return {
        "repo_path": str(Path(root).resolve()),
        "branch": _git(root, "rev-parse", "--abbrev-ref", "HEAD"),
        "commit": _git(root, "rev-parse", "HEAD"),
    }


#: Operational noise that is never part of a review subject. Everything else —
#: including ``.jsonl`` fixtures and ``.md`` roadmap files — counts, because an
#: indexed bundle may legitimately cover them.
_NOISE_DIR_PARTS = frozenset({
    ".git", ".data", "__pycache__", ".mypy_cache", ".pytest_cache", ".ruff_cache",
    "node_modules", ".venv", "venv", "dist", "build", "htmlcov", ".tox",
})
_NOISE_PREFIXES = ("remedy-job-evidence", "remedy-review-", "run_transcript")
_NOISE_SUFFIXES = (
    ".pyc", ".pyo", ".zip", ".tar", ".gz", ".log", ".tmp", ".swp",
    ".coverage", ".egg-info",
)


def _normalize_rel(path: str) -> str:
    p = str(path or "").replace("\\", "/").strip()
    while p.startswith("./"):
        p = p[2:]
    return p


def is_review_subject_file(path: str) -> bool:
    """True unless the path is known operational noise, a cache or an archive."""
    p = _normalize_rel(path)
    if not p or p.endswith("/"):
        return False
    parts = p.split("/")
    if any(part in _NOISE_DIR_PARTS or part.endswith(".egg-info") for part in parts):
        return False
    if any(parts[-1].startswith(pref) or p.startswith(pref) for pref in _NOISE_PREFIXES):
        return False
    if p.endswith(_NOISE_SUFFIXES):
        return False
    return True


def dirty_source_test_files(repo_path: str | Path) -> list[str]:
    """Return the current dirty review-subject files.

    Enumerates untracked files individually (``-u``) so a directory is never
    collapsed to ``dir/``, and applies a noise EXCLUDE list rather than a
    hardcoded language-extension allowlist — otherwise ``.jsonl`` fixtures and
    ``docs/roadmap/STATUS.md`` could never align with indexed evidence.
    """
    out = _git_raw(repo_path, "status", "--porcelain", "-u")
    files: list[str] = []
    for line in out.splitlines():
        if not line.strip():
            continue
        # Columns 0-1 are the status code, column 2 is a separator space.
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        path = _normalize_rel(path.strip().strip('"'))
        if is_review_subject_file(path):
            files.append(path)
    return sorted(set(files))


def write_index_record(
    job_id: str,
    evidence_dir: str | Path,
    *,
    repo_path: str | Path = ".",
    job_status: str = "",
    changed_files: list[str] | None = None,
    source_command: str = "",
    index_dir: Path | None = None,
) -> dict[str, Any]:
    """Create or update this job's index record. Never raises on I/O problems."""
    idx = index_dir or job_evidence_index_dir()
    ev = Path(evidence_dir).resolve()
    ident = repo_identity(repo_path)

    record: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "job_id": job_id,
        # Preserved legacy keys (ui_server and older writers read these).
        "evidence_dir_local": str(ev),
        "has_agent_run_trace": (ev / "agent_run_trace.jsonl").exists(),
        "has_job_flow_json": (ev / "job_flow.json").exists(),
        "created_at": _now(),
        "source_command": source_command,
        # Selection fields.
        "evidence_export_path": str(ev),
        "exported_at": _now(),
        "job_status": job_status,
        "changed_files": sorted(changed_files or []),
        **ident,
    }
    try:
        idx.mkdir(parents=True, exist_ok=True)
        (idx / f"{job_id}.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    except OSError:
        pass
    return record


def load_index_records(index_dir: Path | None = None) -> list[dict[str, Any]]:
    """Load every index record, newest export first. Bad files are skipped."""
    idx = index_dir or job_evidence_index_dir()
    if not idx.is_dir():
        return []
    records: list[dict[str, Any]] = []
    for p in sorted(idx.glob("*.json")):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if isinstance(data, dict) and data.get("job_id"):
            records.append(data)
    records.sort(key=lambda r: str(r.get("exported_at") or r.get("created_at") or ""), reverse=True)
    return records


def find_record(job_id: str, index_dir: Path | None = None) -> dict[str, Any] | None:
    for r in load_index_records(index_dir):
        if r.get("job_id") == job_id:
            return r
    return None


# Decides WHICH directory a job's diff is read out of, for every reader of it.
def resolve_job_evidence_dir(job_id: str, index_dir: Path | None = None) -> Path | None:
    """Resolve a job's evidence directory — index record first, then the local default.

    This is what decides which directory the F037 diff viewer and the F033
    decision doors read a diff out of, so both get ONE answer. A second rule
    could disagree with this one, and a decision recorded over hunks nobody was
    shown is exactly the harm the recorder's no-diff refusal exists to prevent.

    It reads ``<job_id>.json`` BY NAME and deliberately does NOT go through
    ``find_record``, which matches on the ``job_id`` key INSIDE the file: a
    record written without that key resolves here and would stop resolving
    through ``find_record``.

    ``packages/orchestration/ui_server.py``'s ``_resolve_evidence_dir`` is now a
    delegation to this function, kept only because callers import that name.
    """
    try:
        idx_file = (index_dir or job_evidence_index_dir()) / f"{job_id}.json"
        if idx_file.exists():
            record = json.loads(idx_file.read_text())
            local_dir = record.get("evidence_dir_local", "")
            if local_dir and Path(local_dir).is_dir():
                return Path(local_dir)
    # ``ImportError`` is retained from the moved original, where the data-paths
    # import sat inside this try; here that import is module level, so the name
    # is now unreachable. It is kept rather than dropped so the move stays
    # behaviour-preserving in both directions.
    except (ImportError, OSError, ValueError, KeyError):
        pass
    # RELATIVE on purpose: this resolves against the current working directory,
    # exactly as it did before the move. It is not an absolute path.
    default = Path(f"remedy-job-evidence-{job_id}")
    if default.is_dir():
        return default
    return None


def _evidence_present(record: dict[str, Any]) -> bool:
    p = record.get("evidence_export_path") or record.get("evidence_dir_local") or ""
    return bool(p) and Path(p).is_dir()


def record_matches_repo(record: dict[str, Any], repo_path: str | Path) -> bool:
    want = repo_identity(repo_path)["repo_path"]
    return str(record.get("repo_path") or "") == want


def record_aligns_with_worktree(record: dict[str, Any], dirty: list[str]) -> bool:
    """Review-subject alignment: the recorded changed files must be part of the
    current dirty source/test set. An empty recorded set cannot be aligned."""
    recorded = {_normalize_rel(f) for f in (record.get("changed_files") or [])}
    if not recorded:
        return False
    return recorded.issubset({_normalize_rel(d) for d in dirty})


def select_evidence(
    repo_path: str | Path,
    *,
    job_id: str = "",
    index_dir: Path | None = None,
) -> dict[str, Any]:
    """Choose the evidence bundle for a review zip.

    With ``job_id`` the requested job is selected exactly, or reported missing —
    a different job is never silently substituted. Without it, only jobs from
    this repository whose recorded changed files align with the current working
    tree are considered; the current branch is preferred; the newest matching
    export wins. Filesystem modification time is never the selector.

    Returns ``{"selected": record|None, "reason": str, "history": [records]}``.
    """
    records = load_index_records(index_dir)

    if job_id:
        rec = next((r for r in records if r.get("job_id") == job_id), None)
        if rec is None:
            return {"selected": None, "reason": f"job_id_not_indexed:{job_id}", "history": []}
        if not _evidence_present(rec):
            return {"selected": None, "reason": f"evidence_missing_for_job:{job_id}", "history": []}
        history = _relevant_history(records, rec, repo_path)
        return {"selected": rec, "reason": "explicit_job_id", "history": history}

    ident = repo_identity(repo_path)
    dirty = dirty_source_test_files(repo_path)

    candidates = [
        r for r in records
        if _evidence_present(r)
        and record_matches_repo(r, repo_path)
        and record_aligns_with_worktree(r, dirty)
    ]
    if not candidates:
        return {"selected": None, "reason": "no_matching_evidence_for_branch_or_worktree", "history": []}

    same_branch = [r for r in candidates if str(r.get("branch") or "") == ident["branch"]]
    pool = same_branch or candidates
    selected = pool[0]  # records are already newest-export-first
    reason = "newest_aligned_evidence_on_current_branch" if same_branch else "newest_aligned_evidence_in_repo"
    history = _relevant_history(records, selected, repo_path)
    return {"selected": selected, "reason": reason, "history": history}


def _relevant_history(
    records: list[dict[str, Any]],
    selected: dict[str, Any],
    repo_path: str | Path,
) -> list[dict[str, Any]]:
    """Earlier jobs that are genuinely related to the selected one.

    Same repository, evidence still present, and a real file-set overlap with the
    current subject. Same-branch jobs come first. An unrelated feature is never
    included merely because it is recent.
    """
    sel_id = selected.get("job_id")
    sel_files = {_normalize_rel(f) for f in (selected.get("changed_files") or [])}
    sel_branch = str(selected.get("branch") or "")

    related: list[dict[str, Any]] = []
    for r in records:
        if r.get("job_id") == sel_id or not _evidence_present(r):
            continue
        if not record_matches_repo(r, repo_path):
            continue
        files = {_normalize_rel(f) for f in (r.get("changed_files") or [])}
        if not files or not (files & sel_files):
            continue  # unrelated feature: no overlap with the current subject
        related.append(r)

    same = [r for r in related if str(r.get("branch") or "") == sel_branch]
    other = [r for r in related if str(r.get("branch") or "") != sel_branch]
    same.sort(key=lambda r: str(r.get("exported_at") or ""), reverse=True)
    other.sort(key=lambda r: str(r.get("exported_at") or ""), reverse=True)
    return same + other
