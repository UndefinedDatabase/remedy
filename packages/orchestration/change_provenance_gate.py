"""Change provenance gate — verify dirty source files are backed by evidence.

Deterministic, read-only orchestration logic: no provider calls, no target-repo
mutation, no job state mutation. Given the same evidence directory and dirty
file list, the same gate is produced every time.

Every dirty/staged *source* file in the repo must be accounted for by the job's
evidence: it must appear in ``workspace.diff``, in ``workspace_apply.json``'s
applied files, or in a per-task ``task_runs/<id>/safe.diff``. A dirty source
file with no such backing is an unexplained change and blocks the run.

Public API:
    build_change_provenance_gate(evidence_dir, dirty_files, current_job_id) -> dict
    write_change_provenance_gate(evidence_dir, dirty_files, current_job_id, written) -> None
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.0.0"

# Directory components that never carry job source changes.
_EXCLUDE_DIRS = frozenset({
    "remedy-job-evidence",
    "__pycache__",
    ".git",
    ".agent",
    "node_modules",
    ".data",
    ".mypy_cache",
    ".pytest_cache",
    ".venv",
    "venv",
    "dist",
    "build",
    "egg-info",
})

_EXCLUDE_DIRS_BARE = frozenset(d.lstrip(".") for d in _EXCLUDE_DIRS)

# File suffixes that are build/output artifacts, not source.
_EXCLUDE_SUFFIXES = (
    ".pyc",
    ".pyo",
    ".egg",
    ".whl",
    ".zip",
    ".tar",
    ".gz",
    ".log",
    ".tmp",
)

# Path substrings that mark generated/review scratch, not source.
_EXCLUDE_SUBSTRINGS = (
    "remedy-review-",
    "remedy-job-evidence",
    "run_transcript",
    ".coverage",
    "htmlcov/",
)

# Diff header lines that name a changed file, e.g. ``+++ b/pkg/mod.py``.
_DIFF_PATH_RE = re.compile(r"^[+-]{3}\s+[ab]/(.+)$")


def _normalize(path: str) -> str:
    p = path.replace("\\", "/").strip()
    while p.startswith("./"):
        p = p[2:]
    return p


def _is_source_file(path: str) -> bool:
    """True when ``path`` is a source file (not a build/scratch artifact)."""
    norm = _normalize(path)
    if not norm:
        return False
    parts = norm.split("/")
    if any(
        part in _EXCLUDE_DIRS
        or part.lstrip(".") in _EXCLUDE_DIRS_BARE
        or part.endswith(".egg-info")
        for part in parts
    ):
        return False
    if norm.endswith(_EXCLUDE_SUFFIXES):
        return False
    if any(sub in norm for sub in _EXCLUDE_SUBSTRINGS):
        return False
    return True


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except (OSError, ValueError):
        return ""


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except (OSError, ValueError):
        return None


def _files_from_diff(diff_text: str) -> set[str]:
    files: set[str] = set()
    for line in diff_text.splitlines():
        m = _DIFF_PATH_RE.match(line)
        if not m:
            continue
        path = m.group(1).strip()
        if not path or path == "/dev/null":
            continue
        files.add(_normalize(path))
    return files


def _files_from_apply_json(data: Any) -> set[str]:
    files: set[str] = set()
    if not isinstance(data, list):
        return files
    for entry in data:
        if not isinstance(entry, dict):
            continue
        manifest = entry.get("apply_manifest")
        if isinstance(manifest, dict):
            for f in manifest.get("applied_files") or []:
                files.add(_normalize(str(f)))
    return files


def _hashes_from_apply_json(data: Any) -> dict[str, str]:
    """Extract per-file SHA256 from workspace_apply.json applied_file_proofs.

    Supports two shapes:
    - dict: ``{"path.py": {"final_workspace_sha256": "..."}}``
    - list: ``[{"path": "path.py", "final_workspace_sha256": "..."}]``
    """
    hashes: dict[str, str] = {}
    if not isinstance(data, list):
        return hashes
    for entry in data:
        if not isinstance(entry, dict):
            continue
        proofs = entry.get("applied_file_proofs")
        if proofs is None:
            manifest = entry.get("apply_manifest")
            if isinstance(manifest, dict):
                proofs = manifest.get("applied_file_proofs")
        if proofs is None:
            continue
        if isinstance(proofs, dict):
            for fpath, proof in proofs.items():
                if isinstance(proof, dict):
                    sha = proof.get("final_workspace_sha256") or proof.get("sha256") or ""
                    if sha:
                        hashes[_normalize(str(fpath))] = str(sha)
                elif isinstance(proof, str) and proof:
                    hashes[_normalize(str(fpath))] = proof
        elif isinstance(proofs, list):
            for proof in proofs:
                if not isinstance(proof, dict):
                    continue
                fpath = proof.get("path", "")
                sha = proof.get("final_workspace_sha256") or proof.get("sha256") or ""
                if fpath and sha:
                    hashes[_normalize(str(fpath))] = str(sha)
    return hashes


def _sha256_file(path: Path) -> str:
    """Return hex SHA256 of file contents, or "" on error."""
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return ""


def _compute_current_hashes(
    source_files: list[str], repo_root: str,
) -> dict[str, str]:
    """SHA256 every source file relative to repo_root."""
    root = Path(repo_root)
    out: dict[str, str] = {}
    for f in source_files:
        h = _sha256_file(root / f)
        if h:
            out[f] = h
    return out


def _collect_evidence_files(
    evidence_dir: str,
) -> tuple[set[str], list[str], dict[str, str], list[dict[str, str]]]:
    """Return evidence-covered paths, sources, hashes, and stale apply proofs."""
    covered: set[str] = set()
    sources: list[str] = []
    evidence_hashes: dict[str, str] = {}
    stale_apply_proofs: list[dict[str, str]] = []
    if not evidence_dir:
        return covered, sources, evidence_hashes, stale_apply_proofs
    base = Path(evidence_dir)

    ws_diff = base / "workspace.diff"
    if ws_diff.exists():
        covered |= _files_from_diff(_read_text(ws_diff))
        sources.append("workspace.diff")

    apply_hashes: dict[str, str] = {}
    apply_json = base / "workspace_apply.json"
    if apply_json.exists():
        apply_data = _read_json(apply_json)
        covered |= _files_from_apply_json(apply_data)
        apply_hashes = _hashes_from_apply_json(apply_data)
        evidence_hashes.update(apply_hashes)
        sources.append("workspace_apply.json")

    content_proof = base / "current_change_content_proof.json"
    if content_proof.exists():
        proof_data = _read_json(content_proof)
        if isinstance(proof_data, dict):
            for fpath, sha in (proof_data.get("file_hashes") or {}).items():
                norm = _normalize(str(fpath))
                old_hash = apply_hashes.get(norm, "")
                if old_hash and old_hash != str(sha):
                    stale_apply_proofs.append({
                        "file": norm,
                        "apply_sha256": old_hash,
                        "current_proof_sha256": str(sha),
                        "superseded_by": "current_change_content_proof.json",
                    })
                evidence_hashes[norm] = str(sha)
            sources.append("current_change_content_proof.json")

    task_runs = base / "task_runs"
    if task_runs.is_dir():
        for safe_diff in sorted(task_runs.glob("*/safe.diff")):
            covered |= _files_from_diff(_read_text(safe_diff))
            sources.append(f"task_runs/{safe_diff.parent.name}/safe.diff")

    return covered, sources, evidence_hashes, stale_apply_proofs


def _is_covered(source_file: str, covered: set[str]) -> bool:
    norm = _normalize(source_file)
    if norm in covered:
        return True
    # Tolerate path-prefix differences between git-relative and diff-relative
    # spellings of the same file.
    return any(
        c == norm or c.endswith("/" + norm) or norm.endswith("/" + c)
        for c in covered
    )


def build_change_provenance_gate(
    evidence_dir: str,
    dirty_files: list[str],
    current_job_id: str,
    repo_root: str = "",
) -> dict[str, Any]:
    """Check that every dirty source file is backed by job evidence.

    Filters ``dirty_files`` down to source files, collects the files covered by
    the job's evidence (``workspace.diff``, ``workspace_apply.json``, per-task
    ``safe.diff``), and flags any source file with no evidence backing.

    When ``repo_root`` is provided, also verifies content hashes: each covered
    source file's current SHA256 must match the evidence proof hash.  A path
    match with a hash mismatch blocks the gate.
    """
    incoming = [str(f) for f in (dirty_files or [])]

    source_files = sorted({_normalize(f) for f in incoming if _is_source_file(f)})
    excluded_files = sorted({_normalize(f) for f in incoming if not _is_source_file(f)})

    covered, sources, evidence_hashes, stale_apply_proofs = _collect_evidence_files(
        evidence_dir,
    )

    covered_files = [f for f in source_files if _is_covered(f, covered)]
    uncovered_files = [f for f in source_files if not _is_covered(f, covered)]

    issues = [
        f"dirty source file {f!r} has no evidence backing"
        for f in uncovered_files
    ]

    hash_mismatches: list[dict[str, str]] = []
    current_hashes: dict[str, str] = {}
    content_hash_verified = False

    if repo_root and source_files:
        content_hash_verified = True
        current_hashes = _compute_current_hashes(source_files, repo_root)
        for f in covered_files:
            ev_hash = evidence_hashes.get(f, "")
            cur_hash = current_hashes.get(f, "")
            if ev_hash and cur_hash and ev_hash != cur_hash:
                hash_mismatches.append({
                    "file": f,
                    "evidence_sha256": ev_hash,
                    "current_sha256": cur_hash,
                })
                issues.append(
                    f"content hash mismatch for {f!r}: "
                    f"evidence={ev_hash[:16]}… current={cur_hash[:16]}…"
                )

    has_blocking = bool(uncovered_files) or bool(hash_mismatches)
    verdict = "BLOCKED" if has_blocking else "PASS"

    result: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "verdict": verdict,
        "current_job_id": current_job_id,
        "dirty_files": [_normalize(f) for f in incoming],
        "source_files": source_files,
        "excluded_files": excluded_files,
        "evidence_sources": sources,
        "evidence_covered_files": sorted(covered),
        "covered_files": covered_files,
        "uncovered_files": uncovered_files,
        "content_hash_verified": content_hash_verified,
        "current_hashes": current_hashes,
        "evidence_hashes": evidence_hashes,
        "hash_mismatches": hash_mismatches,
        "stale_apply_proofs": stale_apply_proofs,
        "issues": issues,
    }
    return result


def write_change_provenance_gate(
    evidence_dir: str,
    dirty_files: list[str],
    current_job_id: str,
    written: dict[str, str] | None = None,
    repo_root: str = "",
) -> None:
    """Build and write ``change_provenance_gate.json`` into ``evidence_dir``.

    Registers the written path in ``written`` when provided. No-op when
    ``evidence_dir`` is empty.
    """
    if not evidence_dir:
        return

    gate = build_change_provenance_gate(
        evidence_dir, dirty_files, current_job_id, repo_root=repo_root,
    )

    out_dir = Path(evidence_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "change_provenance_gate.json"
    json_path.write_text(json.dumps(gate, indent=2) + "\n", encoding="utf-8")

    if written is not None:
        written["change_provenance_gate.json"] = str(json_path)
