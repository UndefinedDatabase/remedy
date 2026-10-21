"""One job's change as a client shows it before apply: per file, git's own unified diff (amend1015c D5).

Operator order amend1015-final-closure, E3: a client must show the real change before a person
says "apply". `remedy client diff <job> --json` and `GET /api/v1/jobs/{job}/diff` answer it from
git, never from a diff engine of Remedy's own: a result not yet applied (or declined, or refused
by a conflict) is `git diff <the job's base commit> <the job branch's head>` in the job's own
repository, and one applied with a commit (`commit`, `commit_auto`, `commit_with_history`) is the
commit its apply landed, `git diff <commit>^1 <commit>`; a plain apply commits nothing and copied
exactly the job branch's change, so its diff is that change.

The answer, beside the envelope's own keys::

    {"job": str, "state": "prepared"|"applied"|"declined"|"failed"|"conflict",
     "files": [{"path", "change": "added"|"modified"|"deleted"|"renamed",
                "added": int, "removed": int, "patch": str, "truncated": bool}],
     "truncated": bool}

A job that has not ended, or that waits for an answer to a question (its story reads `waiting`),
is refused `diff_not_ready`. `patch` is cut at a line boundary after `FILE_PATCH_LIMIT` bytes (the file's `truncated` is
true), the patches together stop at `TOTAL_PATCH_LIMIT` bytes and the list at `FILE_LIMIT` files
(the answer's `truncated` is true). A binary file counts 0 lines and carries git's own one-line
patch. A path `sensitive_paths` names keeps its counts but never its patch, so a credential's
content cannot leave the machine. This module reads git and the job's records; it changes nothing.

Public API::

    DIFF_STATES
    job_client_diff(job_id, plan) -> dict   # raises ClientDiffRefusal
"""

from __future__ import annotations

import subprocess
from typing import Any

#: The closed list of the answer's `state`.
DIFF_STATES: tuple[str, ...] = ("prepared", "applied", "declined", "failed", "conflict")
#: The closed list of a file's `change`.
DIFF_CHANGES: tuple[str, ...] = ("added", "modified", "deleted", "renamed")
#: The refusal tokens of the read, beside the job-id refusals every job route shares.
DIFF_REFUSALS: tuple[str, ...] = ("diff_not_ready", "diff_unavailable")

FILE_PATCH_LIMIT = 64 * 1024
TOTAL_PATCH_LIMIT = 512 * 1024
FILE_LIMIT = 300

#: git's name-status letters, by the answer's `change` word.
_CHANGE_BY_LETTER = {"A": "added", "M": "modified", "D": "deleted", "R": "renamed", "T": "modified",
                     "C": "added"}
#: The job states whose job has ended without a result to apply.
_FAILED_STATES = frozenset({"failed", "blocked", "stopped", "cancelled"})
#: The reason prefixes an apply refusal writes when the target moved under the result.
_CONFLICT_REASONS = ("baseline_check_failed", "baseline_check_before_apply_failed",
                     "human_change_conflict", "merge_conflict", "target_changed")


class ClientDiffRefusal(Exception):
    """The job has no change to show (yet); `token` is one of `DIFF_REFUSALS`."""

    def __init__(self, token: str, message: str) -> None:
        super().__init__(message)
        self.token = token


def _git(repo: str, *args: str) -> bytes:
    return subprocess.run(
        ["git", "-C", repo, "-c", "core.quotePath=false", *args],
        capture_output=True, timeout=30, check=True).stdout


def _latest_apply_record(job_id: str) -> dict[str, Any] | None:
    """The newest apply record of JOB_ID that was a real, approved apply, read raw, or None."""
    import json

    from packages.orchestration.job_apply import _job_apply_records_dir

    folder = _job_apply_records_dir() / job_id
    records = []
    for path in folder.glob("*.json") if folder.is_dir() else ():
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if isinstance(record, dict) and record.get("approved") and not record.get("dry_run"):
            records.append(record)
    records.sort(key=lambda r: (str(r.get("finished_at") or ""), str(r.get("job_apply_id") or "")))
    applied = [r for r in records if r.get("status") == "applied"]
    return (applied or records or [None])[-1]


def _asks_a_question(plan: Any) -> bool:
    """Whether PLAN has an open decision, so its story reads `waiting`: a job its budget stopped
    with a question has not ended (found by the kit's recording, which first read `failed`)."""
    from packages.orchestration.client_story import job_story_open_decision
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.timeline import load_run_events

    return job_story_open_decision(plan, load_run_events(resolve_data_root(), str(plan.job_id))) is not None


def _state_and_range(plan: Any) -> tuple[str, str, str]:
    """(state, from-commit, to-commit) of PLAN's change; raises `diff_not_ready` while it runs."""
    from packages.orchestration.job_apply import job_result_decline

    state = str(getattr(plan.state, "value", plan.state))
    base, head = str(plan.worktree_base_commit or ""), str(plan.worktree_head or plan.worktree_branch or "")
    if state != "completed" and _asks_a_question(plan):
        raise ClientDiffRefusal("diff_not_ready",
                                f"job {plan.job_id} waits for an answer; its change is shown once it ends")
    if state in _FAILED_STATES:
        return "failed", base, head
    if state != "completed":
        raise ClientDiffRefusal("diff_not_ready",
                                f"job {plan.job_id} is {state}; its change is shown once it ends")
    record = _latest_apply_record(str(plan.job_id))
    if record is not None and record.get("status") == "applied":
        # A plain apply copies the result into the working tree and commits nothing; its change
        # is then the job branch's, which is exactly what it copied.
        commit = str(record.get("commit_sha") or "")
        return ("applied", f"{commit}^1", commit) if commit else ("applied", base, head)
    if job_result_decline(plan) is not None:
        return "declined", base, head
    if record is not None and (record.get("merge_conflicts") or str(
            record.get("blocked_reason") or "").startswith(_CONFLICT_REASONS)):
        return "conflict", base, head
    return "prepared", base, head


def _entries(repo: str, start: str, end: str) -> list[tuple[str, str, str]]:
    """(change, path, old path or "") per changed file, in git's order."""
    fields = _git(repo, "diff", "--no-color", "-M", "--name-status", "-z", start, end).decode(
        "utf-8", "replace").split("\0")
    rows, index = [], 0
    while index < len(fields) and fields[index]:
        letter = fields[index][0]
        if letter in ("R", "C"):
            rows.append((_CHANGE_BY_LETTER[letter], fields[index + 2], fields[index + 1]))
            index += 3
        else:
            rows.append((_CHANGE_BY_LETTER.get(letter, "modified"), fields[index + 1], ""))
            index += 2
    return rows


def _cut(text: str, limit: int) -> tuple[str, bool]:
    """TEXT cut at the last line boundary within LIMIT bytes, and whether anything was cut."""
    data = text.encode("utf-8")
    if len(data) <= limit:
        return text, False
    kept = data[:limit]
    return kept[: kept.rfind(b"\n") + 1].decode("utf-8", "ignore"), True


def _file_row(repo: str, start: str, end: str, entry: tuple[str, str, str],
              budget: int) -> dict[str, Any]:
    from packages.orchestration.sensitive_paths import sensitive_path_category

    change, path, old = entry
    spec = [path, old] if old else [path]
    numstat = _git(repo, "diff", "-M", "--numstat", start, end, "--", *spec).decode(
        "utf-8", "replace").split("\t")
    added, removed = (int(n) if n.isdigit() else 0 for n in (numstat + ["", ""])[:2])
    if sensitive_path_category(path) or (old and sensitive_path_category(old)):
        return {"path": path, "change": change, "added": added, "removed": removed,
                "patch": "", "truncated": True}
    patch = _git(repo, "diff", "--no-color", "--no-ext-diff", "--no-textconv", "-M",
                 "--src-prefix=a/", "--dst-prefix=b/", start, end, "--", *spec).decode(
        "utf-8", "replace")
    patch, truncated = _cut(patch, min(FILE_PATCH_LIMIT, budget))
    return {"path": path, "change": change, "added": added, "removed": removed,
            "patch": patch, "truncated": truncated}


def job_client_diff(job_id: str, plan: Any) -> dict[str, Any]:
    """The diff answer of the resolved job JOB_ID whose record is PLAN (see the module's text).

    Raises `ClientDiffRefusal` `diff_not_ready` while the job has not ended, and
    `diff_unavailable` when its commits cannot be read from git any more."""
    state, start, end = _state_and_range(plan)
    repo = str(plan.repo_path or "")
    if state == "failed" and (not start or not end):
        return {"job": job_id, "state": state, "files": [], "truncated": False}
    if not repo or not start or not end:
        raise ClientDiffRefusal("diff_unavailable",
                                f"job {job_id} records no commits its change can be read from")
    try:
        entries = _entries(repo, start, end)
        files, budget = [], TOTAL_PATCH_LIMIT
        for entry in entries[:FILE_LIMIT]:
            row = _file_row(repo, start, end, entry, max(budget, 0))
            budget -= len(row["patch"].encode("utf-8"))
            files.append(row)
    except (OSError, subprocess.SubprocessError) as exc:
        raise ClientDiffRefusal(
            "diff_unavailable",
            f"job {job_id}'s change cannot be read from git any more ({type(exc).__name__})") from exc
    truncated = len(entries) > FILE_LIMIT or any(row["truncated"] for row in files)
    return {"job": job_id, "state": state, "files": files, "truncated": truncated}
