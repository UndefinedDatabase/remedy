"""Operator amendment amend1014-do-golden-path-now D1 — which lane a `remedy do` order walks.

A bounded one-deliverable order walks a bounded lane: deterministic study facts for a tiny
repository, the deterministic one-milestone mission plan, a deterministic DoD, one job and one
task for the one file, and no planning provider call at all; only the builder and the reviewer
are called. Anything else walks the full lane, the scalable mission path, unchanged.

Remedy deliberately does not ask a model whether an order is small, because a classifier call
would be one more provider call spent to decide whether to spend provider calls. The decision is
`select_do_lane`, pure and table-tested, and it takes the full lane whenever a fact is missing
or the scope is not clear.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass

from packages.orchestration.do_context import DoContext
from packages.orchestration.task_deliverables import explicit_order_paths

DO_LANE_BOUNDED = "bounded"
DO_LANE_FULL = "full"

#: A repository holding this many tracked files or fewer is studied without a provider's narration.
DO_TINY_REPO_MAX_FILES = 10

#: An order with no file named is one part when it reads as one or two sentences on one line.
_MAX_PLAIN_ORDER_SENTENCES = 2
_SENTENCE_END_RE = re.compile(r"[.!?](?:\s+|$)")
_LIST_MARKER_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s", re.MULTILINE)


@dataclass(frozen=True)
class DoLaneDecision:
    """The lane an order walks, the sentence saying why, and the one file when the lane has one."""

    lane: str
    reason: str
    deliverable: str = ""

    @property
    def bounded(self) -> bool:
        return self.lane == DO_LANE_BOUNDED


def _plain_one_part_order(order: str) -> bool:
    """One line, no list, no `;`, at most two sentences: the order has one part to do."""
    text = order.strip()
    if "\n" in text or ";" in text or _LIST_MARKER_RE.search(text):
        return False
    return len(_SENTENCE_END_RE.findall(text)) <= _MAX_PLAIN_ORDER_SENTENCES


def select_do_lane(
    order: str,
    *,
    tracked_files: list[str],
    projects: int = 1,
    from_order_file: bool = False,
    force_job: bool = False,
    force_mission: bool = False,
) -> DoLaneDecision:
    """The lane for *order* over a repository holding *tracked_files*; the full lane when unclear.

    Bounded when there is one target repository, no order file, no `--force-mission`, and either
    the order names exactly one file or the repository tracks exactly one file and the order is
    one plain part. `--force-job` selects the bounded lane for a single-repository order text.
    """
    if projects > 1:
        return DoLaneDecision(DO_LANE_FULL, "the order names several projects")
    if force_mission:
        return DoLaneDecision(DO_LANE_FULL, "--force-mission was given")
    if from_order_file:
        return DoLaneDecision(DO_LANE_FULL, "the order is an order file, which may declare several parts")
    named = explicit_order_paths(order)
    if len(named) == 1:
        return DoLaneDecision(DO_LANE_BOUNDED, f"the order names one file, {named[0]}", named[0])
    if force_job:
        return DoLaneDecision(DO_LANE_BOUNDED, "--force-job was given")
    if len(named) > 1:
        return DoLaneDecision(DO_LANE_FULL, f"the order names {len(named)} files")
    if len(tracked_files) == 1 and _plain_one_part_order(order):
        return DoLaneDecision(
            DO_LANE_BOUNDED, f"the repository tracks one file, {tracked_files[0]}, and the order has one part",
            tracked_files[0])
    return DoLaneDecision(DO_LANE_FULL, "the scope of the order is not clearly one file")


def tracked_repo_files(repo_root: str) -> list[str]:
    """The files HEAD tracks in *repo_root*, or [] when there is no commit or git does not answer."""
    try:
        proc = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", "HEAD"],
            cwd=repo_root, capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return []
    return proc.stdout.splitlines() if proc.returncode == 0 else []


def is_tiny_repo(tracked_files: list[str]) -> bool:
    """True when the repository is small enough that its study needs no provider narration."""
    return 0 < len(tracked_files) <= DO_TINY_REPO_MAX_FILES


def settle_do_lane(ctx: DoContext) -> DoLaneDecision:
    """The walk's lane, decided once from its context on first use and kept on it (`lane`, `tiny_repo`)."""
    if ctx.lane is None:
        files = tracked_repo_files(ctx.repo_root)
        ctx.lane = select_do_lane(
            ctx.order, tracked_files=files, projects=len(ctx.projects) or 1,
            from_order_file=bool(ctx.order_source_path),
            force_job=ctx.force_job, force_mission=ctx.force_mission)
        ctx.tiny_repo = is_tiny_repo(files)
    return ctx.lane
