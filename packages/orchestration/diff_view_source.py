"""Resolve an evidence directory to the unified-diff artifact the F037 viewer renders.

WHY this module exists BESIDE ``diff_parser.py`` rather than inside it: that module turns
diff TEXT into the contract-v1 view and touches no filesystem whatsoever — it is pure and
total by contract. This is the other half of the same job. It decides WHICH artifact to
read for a requested scope, reads it, and hands the text over to the parser.

It performs no HTTP and imports nothing from ``ui_server.py``, deliberately: the endpoint
layer stays a thin caller that maps this envelope to a response, and this half stays
testable with no server running and no port bound. F037 R7 wires the two GET routes onto
``build_diff_view``; nothing calls it before then.

Every absence is NAMED rather than raised. ``build_diff_view`` returns an envelope whose
``reason`` carries exactly one of the three ``DIFF_REASON_*`` values below, because this
feeds a VIEWER: a viewer that 500s on a job that never wrote a diff is worse than one that
says, in the data, that there is none.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from packages.orchestration.diff_parser import DIFF_VIEW_VERSION, parse_unified_diff_to_view

#: The two scopes a caller can ask for. The scope is what was ASKED FOR, so it is recorded
#: on the envelope before anything can fail.
DIFF_SCOPE_JOB = "job"
DIFF_SCOPE_TASK_RUN = "task_run"

#: Artifact names, quoted from their producers so a grep for the literal lands on both
#: ends: ``job_evidence`` writes ``workspace.diff`` at the evidence root, and
#: ``pingpong_loop._compute_safe_diff`` writes ``safe.diff`` inside each task run.
DIFF_JOB_ARTIFACT_NAME = "workspace.diff"
DIFF_TASK_RUN_ARTIFACT_NAME = "safe.diff"
DIFF_TASK_RUNS_DIR_NAME = "task_runs"

#: The three named absences. ``DIFF_REASON_NO_EVIDENCE_DIR``'s VALUE repeats the string
#: ``packages/orchestration/ui_server.py`` already uses for the same condition in its
#: ``_empty_prompt_trace("evidence_dir_unavailable")`` call — one spelling per concept, per
#: the AGENTS.md "Code Discoverability Conventions".
DIFF_REASON_NO_EVIDENCE_DIR = "evidence_dir_unavailable"
DIFF_REASON_ARTIFACT_MISSING = "diff_artifact_missing"
DIFF_REASON_UNKNOWN_TASK_RUN = "unknown_task_run"

#: Filters the LISTING of ``task_runs/`` — it never validates a caller's argument. Same
#: shape as ``final_verifier._task_ids`` applies to that same directory; re-declared here
#: rather than imported because that name is private to that module.
SAFE_TASK_RUN_ID_RE = re.compile(r"^T\d{3,}$")


def list_task_run_ids(evidence_dir: Path | None) -> list[str]:
    """Return the sorted ids of the task runs that really exist under ``evidence_dir``.

    WHY this is a listing and not a validator: the set it returns is the ONLY set of task
    ids ``build_diff_view`` will serve, so an id that is not a directory here cannot be
    reached at all. Returns ``[]`` when ``evidence_dir`` is None, is not a directory, or
    holds no ``task_runs`` directory — three absences that are the same answer to a
    caller: there is nothing to list.
    """
    if evidence_dir is None:
        return []
    try:
        runs = Path(evidence_dir) / DIFF_TASK_RUNS_DIR_NAME
        children = list(runs.iterdir()) if runs.is_dir() else []
    except (OSError, TypeError, ValueError):
        return []
    return sorted(
        child.name
        for child in children
        if child.is_dir() and SAFE_TASK_RUN_ID_RE.fullmatch(child.name)
    )


def build_diff_view(evidence_dir: Path | None, task_id: str | None = None) -> dict[str, Any]:
    """Return the F037 diff envelope for one job, or for one task run of it.

    The envelope always carries ``version``, ``scope``, ``task_id``, ``source``,
    ``available``, ``reason``, ``truncated``, ``files`` and ``task_run_ids``. It NEVER
    raises: every failure arrives as ``available`` False plus exactly one
    ``DIFF_REASON_*`` value in ``reason``.
    """
    # WHY the scope is set first: it is what the caller ASKED FOR, not what was found, so
    # an envelope describing a failure still says which question produced it.
    scope = DIFF_SCOPE_TASK_RUN if task_id is not None else DIFF_SCOPE_JOB
    view: dict[str, Any] = {
        "version": DIFF_VIEW_VERSION,
        "scope": scope,
        "task_id": task_id,
        "source": None,
        "available": False,
        "reason": None,
        "truncated": False,
        "files": [],
        "task_run_ids": [],
    }

    # WHY the coercion is guarded: the docstring promises this function never raises, and a
    # caller handing over something that is not a path deserves the same named absence as a
    # caller whose evidence directory is simply gone.
    try:
        root = Path(evidence_dir) if evidence_dir is not None else None
        root_is_dir = root is not None and root.is_dir()
    except (OSError, TypeError, ValueError):
        root, root_is_dir = None, False

    if root is None or not root_is_dir:
        view["reason"] = DIFF_REASON_NO_EVIDENCE_DIR
        return view

    # WHY this is always present: a caller that asked for the wrong run can see the real set
    # without a second request.
    task_run_ids = list_task_run_ids(root)
    view["task_run_ids"] = task_run_ids

    # WHY membership in the REAL listing rather than a pattern match over the argument: a
    # name that is not already a directory under task_runs/ cannot be reached, so "..", an
    # absolute path and every other traversal are refused BY CONSTRUCTION here. Remedy
    # deliberately does NOT use path_utils.sanitize_path_component for this: sanitizing
    # rewrites an unsafe id into a DIFFERENT valid one and would then serve the wrong task
    # run's diff, where refusing serves none.
    if task_id is not None and task_id not in task_run_ids:
        view["reason"] = DIFF_REASON_UNKNOWN_TASK_RUN
        return view

    if task_id is not None:
        relative_source = f"{DIFF_TASK_RUNS_DIR_NAME}/{task_id}/{DIFF_TASK_RUN_ARTIFACT_NAME}"
        artifact = root / DIFF_TASK_RUNS_DIR_NAME / task_id / DIFF_TASK_RUN_ARTIFACT_NAME
    else:
        relative_source = DIFF_JOB_ARTIFACT_NAME
        artifact = root / DIFF_JOB_ARTIFACT_NAME
    # WHY source is set BEFORE the read: an absence still tells the caller what was looked
    # for, which is the difference between a debuggable empty panel and a mystery.
    view["source"] = relative_source

    # WHY one absence flag rather than two branches: "the path is not a file" and "the bytes
    # would not decode" are the same answer to a viewer — there is no readable diff here —
    # and folding them keeps a single place that can set DIFF_REASON_ARTIFACT_MISSING.
    diff_text: str | None = None
    if artifact.is_file():
        try:
            diff_text = artifact.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            diff_text = None
    if diff_text is None:
        view["reason"] = DIFF_REASON_ARTIFACT_MISSING
        return view

    # WHY an EMPTY artifact is AVAILABLE with zero files: "nothing changed" and "no diff was
    # written" are different answers and this module must not merge them. A job that touched
    # nothing has a readable, empty diff; a job whose diff was never written has none.
    parsed = parse_unified_diff_to_view(diff_text)
    view["version"] = parsed["version"]
    view["files"] = parsed["files"]
    view["truncated"] = parsed["truncated"]
    view["available"] = True
    return view
