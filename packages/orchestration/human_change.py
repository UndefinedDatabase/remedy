"""F263 T001 — the human change record.

A human who edits the target repository while a job runs is not drift. DECISION D-E of
`docs/roadmap/features/T2_F263.md` makes the edit the authority: it is detected, certified
into the job's evidence, and never overwritten or discarded. This module is the detection
and the certification. It measures the target checkout against the job's LAST KNOWN STATE —
one tree object taken through a private index, so the user's own index is never touched — and
writes a HUMAN CHANGE RECORD under the job's evidence before anything else happens.

It re-bases nothing (DECISION F263 D1). `absorb` takes the re-base step as an argument and
calls it only after the record is on disk, and it catches nothing: a re-base that raises
leaves the record behind and the error loud.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from packages.common.secure_fs import durable_write, durable_write_json

SCHEMA = "remedy.human_change_record.v1"
RECORD_DIRNAME = "human_changes"
#: The checkpoint-ref name that keeps the last known tree alive, beside `job-initial`.
LAST_KNOWN_REF_NAME = "target-last-known"
#: Paths per `git diff` call, so a large change never overruns the argument list.
_DIFF_CHUNK = 200


class HumanChangeError(RuntimeError):
    """The target's state could not be read, or a record could not be certified."""


@dataclass(frozen=True)
class TargetState:
    """The target checkout at one moment: its complete tree and the commit it sat on."""
    tree: str
    head: str
    captured_at: str

    def to_dict(self) -> dict[str, str]:
        return {"tree": self.tree, "head": self.head, "captured_at": self.captured_at}

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> TargetState | None:
        if not data or not data.get("tree"):
            return None
        return cls(tree=str(data["tree"]), head=str(data.get("head", "")),
                   captured_at=str(data.get("captured_at", "")))


@dataclass(frozen=True)
class FileChange:
    path: str
    status: str  # git's letter: A, M, D or T


@dataclass(frozen=True)
class HumanChange:
    before: TargetState
    after: TargetState
    files: tuple[FileChange, ...]
    ignored_operational: tuple[str, ...]
    ignored_noise: tuple[str, ...]


@dataclass(frozen=True)
class AbsorbOutcome:
    status: str  # "unchanged" | "absorbed"
    change: HumanChange | None = None
    record_path: Path | None = None


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _git_text(repo: str | Path, *args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=str(repo), capture_output=True, text=True,
                          timeout=60)
    if proc.returncode != 0:
        raise HumanChangeError(f"git {args[0]} failed: {proc.stderr.strip()[:200]}")
    return proc.stdout


def capture_target_state(repo_path: str | Path) -> TargetState:
    """The target's complete current state, untracked files included; writes no ref."""
    from packages.orchestration import worktrees as W

    try:
        tree = W.write_tree_at(repo_path)
    except W.WorktreeError as exc:
        raise HumanChangeError(str(exc)) from exc
    head = _git_text(repo_path, "rev-parse", "HEAD").strip()
    return TargetState(tree=tree, head=head, captured_at=_now())


def _classify(repo_path: Path, rel: str) -> str:
    # The run guard's own rules (pingpong_loop), so a file that guard ignores is never a
    # human change here either: one definition of "not the user's source".
    from packages.orchestration.pingpong_loop import (
        _is_operational_artifact,
        _is_remedy_data_path,
        _is_target_noise,
    )

    if _is_operational_artifact(rel) or _is_remedy_data_path(repo_path, rel):
        return "operational"
    if _is_target_noise(rel):
        return "noise"
    return "content"


def detect_human_change(repo_path: str | Path, last_known: TargetState) -> HumanChange | None:
    """The change since ``last_known``, or None when the target's content has not moved.

    A difference made only of Remedy's own artifacts or of tool-cache noise is not a human
    change and answers None.
    """
    after = capture_target_state(repo_path)
    if after.tree == last_known.tree:
        return None
    raw = _git_text(repo_path, "diff", "--name-status", "-z", "--no-renames",
                    last_known.tree, after.tree)
    fields = [f for f in raw.split("\0") if f]
    files: list[FileChange] = []
    operational: list[str] = []
    noise: list[str] = []
    for status, rel in zip(fields[0::2], fields[1::2]):
        kind = _classify(Path(repo_path), rel)
        if kind == "operational":
            operational.append(rel)
        elif kind == "noise":
            noise.append(rel)
        else:
            files.append(FileChange(path=rel, status=status))
    if not files:
        return None
    return HumanChange(before=last_known, after=after,
                       files=tuple(sorted(files, key=lambda f: f.path)),
                       ignored_operational=tuple(sorted(operational)),
                       ignored_noise=tuple(sorted(noise)))


def _content_diff(repo_path: str | Path, change: HumanChange) -> bytes:
    paths = [f.path for f in change.files]
    out = b""
    for start in range(0, len(paths), _DIFF_CHUNK):
        chunk = [f":(literal){p}" for p in paths[start:start + _DIFF_CHUNK]]
        proc = subprocess.run(
            ["git", "diff", "--binary", "--no-color", "--no-ext-diff", "--no-renames",
             "--src-prefix=a/", "--dst-prefix=b/", change.before.tree, change.after.tree,
             "--", *chunk],
            cwd=str(repo_path), capture_output=True, timeout=120,
        )
        if proc.returncode != 0:
            raise HumanChangeError(f"git diff failed: {proc.stderr.decode(errors='replace')[:200]}")
        out += proc.stdout
    return out


def _seal(body: dict[str, Any]) -> str:
    unsealed = {k: v for k, v in body.items() if k != "record_sha256"}
    return hashlib.sha256(json.dumps(unsealed, sort_keys=True).encode("utf-8")).hexdigest()


def record_id_for(change: HumanChange) -> str:
    """One id per transition, so detecting the same change twice certifies it once."""
    return f"hcr-{change.before.tree[:12]}-{change.after.tree[:12]}"


def write_human_change_record(
    job_id: str, repo_path: str | Path, change: HumanChange, *, detected_by: str,
    root: Path | None = None,
) -> Path:
    """Certify ``change`` into the job's evidence and return the record's path.

    The diff is written first and the record, which carries the diff's digest and its own
    seal, second. A record that already exists for this transition is returned untouched.
    """
    from packages.orchestration.data_paths import job_evidence_dir

    folder = job_evidence_dir(job_id, root) / RECORD_DIRNAME
    record_id = record_id_for(change)
    path = folder / f"{record_id}.json"
    if path.exists():
        return path
    folder.mkdir(parents=True, exist_ok=True)
    diff = _content_diff(repo_path, change)
    durable_write(folder / f"{record_id}.diff", diff)
    body: dict[str, Any] = {
        "schema": SCHEMA,
        "record_id": record_id,
        "job_id": job_id,
        "detected_by": detected_by,
        "detected_at": change.after.captured_at,
        "repo_path": str(repo_path),
        "before": change.before.to_dict(),
        "after": change.after.to_dict(),
        "files": [{"path": f.path, "status": f.status} for f in change.files],
        "ignored": {"operational": list(change.ignored_operational),
                    "noise": list(change.ignored_noise)},
        "diff": {"path": f"{record_id}.diff",
                 "sha256": hashlib.sha256(diff).hexdigest(),
                 "size_bytes": len(diff)},
    }
    body["record_sha256"] = _seal(body)
    durable_write_json(path, body)
    return path


def verify_human_change_record(path: Path) -> list[str]:
    """Every reason the record at ``path`` is not intact; empty when it is."""
    try:
        body = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"unreadable: {exc}"]
    problems: list[str] = []
    if body.get("schema") != SCHEMA:
        problems.append(f"schema is {body.get('schema')!r}, not {SCHEMA!r}")
    if body.get("record_sha256") != _seal(body):
        problems.append("record_sha256 does not match the record")
    diff_meta = body.get("diff") or {}
    diff_path = Path(path).parent / str(diff_meta.get("path", ""))
    try:
        diff = diff_path.read_bytes()
    except OSError:
        problems.append(f"diff {diff_meta.get('path')!r} is missing")
    else:
        if hashlib.sha256(diff).hexdigest() != diff_meta.get("sha256"):
            problems.append("diff sha256 does not match the record")
    return problems


#: The bundle's integrity artifact for the records it carries (DECISION F263 D2). A failure in it
#: BLOCKS the final verifier, like a lost post-mortem: a package must not look clean while a
#: human change it carries cannot be proved intact.
INTEGRITY_FILE = "human_change_integrity.json"


def export_human_change_records(
    job_id: str, out_dir: Path, *, root: Path | None = None,
) -> tuple[dict[str, Any], list[str]]:
    """Copy the job's records into ``out_dir/human_changes/`` and verify every COPY.

    Returns the integrity artifact and the bundle-relative paths written. A job with no
    records exports none and is intact.
    """
    from packages.orchestration.data_paths import job_evidence_dir

    source = job_evidence_dir(job_id, root) / RECORD_DIRNAME
    records: list[str] = []
    failures: list[str] = []
    written: list[str] = []
    for record in sorted(source.glob("hcr-*.json")) if source.is_dir() else []:
        record_id = record.stem
        records.append(record_id)
        dest = Path(out_dir) / RECORD_DIRNAME
        dest.mkdir(parents=True, exist_ok=True)
        for name in (record.name, f"{record_id}.diff"):
            try:
                (dest / name).write_bytes((source / name).read_bytes())
            except OSError as exc:
                failures.append(f"{record_id}: {name} could not be copied: {exc}")
                continue
            written.append(f"{RECORD_DIRNAME}/{name}")
        failures.extend(f"{record_id}: {p}" for p in verify_human_change_record(dest / record.name))
    integrity = {"schema_version": "1.0.0", "ok": not failures, "records": records,
                 "failures": failures}
    return integrity, written


@dataclass(frozen=True)
class JobAbsorbOutcome:
    job_id: str
    status: str  # "absorbed" | "unchanged" | "skipped_running" | "skipped_no_state"
    record_path: Path | None = None
    files: tuple[FileChange, ...] = ()


def absorb_job(job: Any, *, detected_by: str, root: Path | None = None) -> JobAbsorbOutcome:
    """Absorb the target's human change into ONE job: certify it, then re-base the job.

    The one implementation behind `remedy absorb` and, from T003, the run's own safe points
    (T2_F263.md, Design). The re-base is a state operation: the job's checkpoint ref and its
    `target_last_known` move to the tree the human left, and the job record is persisted. No
    file in the repository is written. A job holding no last known state — made before F263,
    or a non-git copy job — has nothing to measure against and is skipped, not failed.
    """
    from packages.orchestration import worktrees as W
    from packages.orchestration.pingpong_job import job_worktree_id, save_job_plan

    last_known = TargetState.from_dict(job.target_last_known)
    if last_known is None:
        return JobAbsorbOutcome(job_id=job.job_id, status="skipped_no_state")

    def rebase(change: HumanChange) -> None:
        ref = job.target_last_known.get("ref") or W.checkpoint_ref(
            job_worktree_id(job.job_id), LAST_KNOWN_REF_NAME)
        W.set_checkpoint_ref(job.repo_path, ref, change.after.tree)
        job.target_last_known = {**change.after.to_dict(), "ref": ref}
        save_job_plan(job, root)

    outcome = absorb(job.job_id, job.repo_path, last_known, detected_by=detected_by,
                     rebase=rebase, root=root)
    if outcome.change is None:
        return JobAbsorbOutcome(job_id=job.job_id, status="unchanged")
    return JobAbsorbOutcome(job_id=job.job_id, status="absorbed",
                            record_path=outcome.record_path, files=outcome.change.files)


def absorb(
    job_id: str, repo_path: str | Path, last_known: TargetState, *, detected_by: str,
    rebase: Callable[[HumanChange], None], root: Path | None = None,
) -> AbsorbOutcome:
    """Detect, certify, then re-base — in that order, and the record first.

    ``rebase`` runs only after the record is durable and is never wrapped: whatever it
    raises reaches the caller, and the record stays (T2_F263.md, Design).
    """
    change = detect_human_change(repo_path, last_known)
    if change is None:
        return AbsorbOutcome(status="unchanged")
    record = write_human_change_record(job_id, repo_path, change, detected_by=detected_by,
                                       root=root)
    rebase(change)
    return AbsorbOutcome(status="absorbed", change=change, record_path=record)
