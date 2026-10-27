"""Operator amendment amend1027-green-builds E1: a job's evidence files, read over HTTP.

Universe asked to show why a job ended as it did without a shell on the workstation:
`GET /api/v1/jobs/{job}/evidence` and its twin `remedy client evidence <job> --json` answer the
files of the job's evidence folder (`data_paths.job_evidence_dir`: the scope decision, the DoD and
its result, the builder's Bash calls and test runs, each task run's isolation records and raw
streams), each with its path in the folder, its size in bytes and its text cut to its last
20,000 characters. Only the server's token and a client granted `host_tools` read them: the
streams carry the commands a builder ran on the host.

Remedy deliberately does not answer the job's worktree or record here: the diff route answers the
change, the story route the record's reading.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

#: The keys `remedy client evidence <job> --json` answers beside the envelope's own.
JOB_EVIDENCE_ANSWER_KEYS: tuple[str, ...] = ("files", "files_omitted", "job_id")
#: How many characters of one file's text are answered: its last ones.
MAX_EVIDENCE_FILE_CHARS = 20_000
#: How many files are answered, the first in path order; the rest are counted in `files_omitted`.
MAX_EVIDENCE_FILES = 400
#: The refusal of a client token not granted `host_tools`.
EVIDENCE_REFUSED_WORDS = ("a client token reads a job's evidence only when it is granted host_tools "
                          "(remedy client grant-host-tools)")


def job_evidence_files(job_id: str) -> dict[str, Any]:
    """`{job_id, files, files_omitted}`: each file under the job's evidence folder as `{name, size,
    content, truncated}`, `name` relative to the folder; links are never followed."""
    from packages.orchestration.data_paths import job_evidence_dir

    root = Path(job_evidence_dir(job_id))
    found = sorted(path for path in root.rglob("*") if path.is_file() and not path.is_symlink()) \
        if root.is_dir() else []
    files = []
    for path in found[:MAX_EVIDENCE_FILES]:
        try:
            raw = path.read_bytes()
        except OSError:
            continue
        text = raw.decode("utf-8", errors="replace")
        files.append({"name": path.relative_to(root).as_posix(), "size": len(raw),
                      "content": text[-MAX_EVIDENCE_FILE_CHARS:],
                      "truncated": len(text) > MAX_EVIDENCE_FILE_CHARS})
    return {"job_id": job_id, "files": files, "files_omitted": max(0, len(found) - MAX_EVIDENCE_FILES)}


def client_evidence_answer(*, job: str) -> dict[str, Any]:
    """The answer `GET /api/v1/jobs/{job}/evidence` sends: what `remedy client evidence <job> --json`
    prints, for a value that names one job; its refusal otherwise (the job resolved as the twin does)."""
    from apps.cli.json_envelope import build_ok
    from packages.orchestration.public_api import _resolved_job_plan

    resolved, refusal = _resolved_job_plan(job)
    if resolved is None:
        return refusal or {}
    return build_ok(**job_evidence_files(resolved[0]))
