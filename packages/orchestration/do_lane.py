"""Operator amendment amend1014-do-golden-path-now D1 — which lane a `remedy do` order walks.

A bounded one-deliverable order walks a bounded lane: deterministic study facts for a tiny
repository, the deterministic one-milestone mission plan, a deterministic DoD, one job and one
task for the one file, and no planning provider call at all; only the builder and the reviewer
are called. Anything else walks the full lane, the scalable mission path, unchanged.

Remedy deliberately does not ask a model whether an order is small, because a classifier call
would be one more provider call spent to decide whether to spend provider calls. The decision is
`select_do_lane`, pure and table-tested, and it takes the full lane whenever a fact is missing
or the scope is not clear.

DECISION amend1016p D1: the TRANSPORT never decides. An order typed on the command line, read from
an order file or posted to the HTTP API (which writes an order file) gets the same lane for the
same words over the same repository. The decision reads the order's DELIVERABLES, never its
constraints (`order_scope`): "change only README.md", "run npm test" and "apply nothing" bind the
work and are enforced by Remedy's own guards, so they neither make an order complex nor count as
parts. A named file alone is not enough: the deliverables must also be one plain part.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import PurePosixPath

from packages.orchestration.do_context import DoContext
from packages.orchestration.do_scope import order_scope_files, resolve_order_path
from packages.orchestration.order_scope import (
    is_test_path,
    requests_test_files,
    split_order_scope,
)
from packages.orchestration.task_deliverables import explicit_order_paths

DO_LANE_BOUNDED = "bounded"
DO_LANE_FULL = "full"
#: The order cannot safely be placed: the walk stops before planning anything and asks (never guesses).
DO_LANE_HOLD = "hold"

#: A repository holding this many tracked files or fewer is studied without a provider's narration.
DO_TINY_REPO_MAX_FILES = 10

#: Documentation targets: a word like "authentication" in an order about a doc is no risk to code.
_DOC_SUFFIXES = frozenset({".md", ".rst", ".txt", ".adoc"})
#: A document is named by a word of the order only when its stem is at least this long.
_MIN_WORD_STEM_CHARS = 4
#: Path facts that make a change risky whatever the order says: security, persistence, deployment.
_RISKY_PATH = re.compile(
    r"(?:^|/)(?:auth\w*|login\w*|security\w*|crypto\w*|passw\w*|secrets?|permissions?|sessions?|"
    r"payments?|billing|migrations?|alembic|schema\w*|database|db|deploy\w*|infra\w*|terraform|"
    r"helm|k8s|\.github/workflows)(?:[./_-]|/|$)|(?:^|/)(?:Dockerfile|docker-compose[^/]*)$|\.(?:sql|tf)$",
    re.IGNORECASE)
#: Words of an order that name security, data or deployment risk, or a change as wide as the system.
_RISKY_WORDS = re.compile(
    r"\b(?:authenticat\w*|authoriz\w*|authoris\w*|oauth|password\w*|credential\w*|secrets?|encrypt\w*|"
    r"decrypt\w*|permissions?|privileges?|security|vulnerab\w*|authentifizier\w*|autorisier\w*|"
    r"passwort\w*|passwörter|sicherheit\w*|verschlüssel\w*|berechtigung\w*|"
    r"schema|migrations?|drop\s+(?:all\s+)?tables?|data\s+loss|datenverlust|datenbank\w*|"
    r"deploy\w*|production|produktion\w*|breaking\s+changes?|"
    r"rewrite|re-?architect\w*|overhaul|from\s+scratch|neu\s+schreiben|komplett\s+neu)\b"
    r"|\b(?:migrat\w*|migrier\w*)\b.{0,60}\b(?:all|every|entire|whole|alle\w*|sämtliche\w*|gesamte\w*)\b",
    re.IGNORECASE)
#: Wording that asks for a new file; without it a named file the repository does not track is a question.
_CREATES = re.compile(r"\b(?:create|add|write|generate|new|introduce|erstell\w*|schreib\w*|"
                      r"neu\w*|ergänz\w*|füg\w*|lege)\b", re.IGNORECASE)


@dataclass(frozen=True)
class DoLaneDecision:
    """The lane an order walks, the sentence saying why, and the one file when the lane has one.

    *risk* is the deterministic fact that took a one-file order off the bounded lane; *with_tests*
    says the order itself asks for a test beside the one file (a deliverable, never a check).
    """

    lane: str
    reason: str
    deliverable: str = ""
    risk: str = ""
    with_tests: bool = False

    @property
    def bounded(self) -> bool:
        return self.lane == DO_LANE_BOUNDED

    @property
    def hold(self) -> bool:
        return self.lane == DO_LANE_HOLD


def order_risk(order: str, targets: list[str]) -> str:
    """The sentence naming why a one-file order is high-risk (security, persistence, deployment,
    an order-wide rewrite), or "" when no fact says so. A documentation target is never risky."""
    code = [t for t in targets if PurePosixPath(t).suffix.lower() not in _DOC_SUFFIXES]
    if targets and not code:
        return ""
    if path := next((t for t in code if _RISKY_PATH.search(t)), ""):
        return f"{path} is a security, persistence or deployment path"
    body = " ".join(split_order_scope(order).deliverables)
    if word := _RISKY_WORDS.search(body):
        return f"the order speaks of {word.group().strip()!r}"
    return ""


def _order_targets(order: str, tracked_files: list[str]) -> list[str]:
    """The files an order's work is about: the files it names, else the tracked file its words name.

    A test file the order asks for beside its work is a companion, never a target of its own.
    """
    named = explicit_order_paths(order)
    if requests_test_files(order):
        named = [path for path in named if not is_test_path(path)]
    if not named:
        # "Fix the typo in the readme": a tracked document whose name the order uses as a word. Only
        # documents, only long stems and only one match: "app" or "main" are words, not files.
        by_word = [t for t in order_scope_files(order, tracked_files)
                   if PurePosixPath(t).suffix.lower() in _DOC_SUFFIXES
                   and len(PurePosixPath(t).stem) >= _MIN_WORD_STEM_CHARS]
        named = by_word if len(by_word) == 1 else []
    return named


def select_do_lane(
    order: str,
    *,
    tracked_files: list[str],
    projects: int = 1,
    force_job: bool = False,
    force_mission: bool = False,
) -> DoLaneDecision:
    """The lane for *order* over a repository holding *tracked_files*; the full lane when unclear.

    Bounded when there is one target repository, no `--force-mission`, and the order's deliverables
    are a few plain actions on exactly one file that the repository proves (or, for a new file, that
    the order says to create) and no fact marks the change risky. A bare file name two nested files
    share, or a named file nothing tracks that the order does not create, is a question (hold),
    never a guess. A test the order asks for beside the file is part of the one job. `--force-job`
    selects the bounded lane for a single-repository order and says what routing alone chose.
    Where the order came from plays no part.
    """
    if projects > 1:
        return DoLaneDecision(DO_LANE_FULL, "the order names several projects")
    if force_mission:
        return DoLaneDecision(DO_LANE_FULL, "--force-mission was given")
    auto = _routed_lane(order, tracked_files, infer_single_file=not force_job)
    if force_job and not auto.bounded:
        return DoLaneDecision(DO_LANE_BOUNDED, f"--force-job was given (routing alone chose the "
                              f"{auto.lane} lane: {auto.reason})", auto.deliverable, auto.risk,
                              auto.with_tests)
    return auto


def _routed_lane(order: str, tracked_files: list[str], *, infer_single_file: bool) -> DoLaneDecision:
    scope = split_order_scope(order)
    with_tests = requests_test_files(order)
    targets = _order_targets(order, tracked_files)
    if len(targets) > 1:
        return DoLaneDecision(DO_LANE_FULL, f"the order names {len(targets)} files")
    if not targets:
        if infer_single_file and len(tracked_files) == 1 and scope.single:
            return DoLaneDecision(
                DO_LANE_BOUNDED, f"the repository tracks one file, {tracked_files[0]}, and the order "
                "has one part", tracked_files[0], with_tests=with_tests)
        return DoLaneDecision(DO_LANE_FULL, "the scope of the order is not clearly one file")
    [target] = targets
    resolved = resolve_order_path(target, tracked_files)
    if resolved is None and tracked_files and "/" not in target:
        sharing = [t for t in tracked_files if PurePosixPath(t).name == target]
        if len(sharing) > 1:
            return DoLaneDecision(DO_LANE_HOLD, f"{target} matches {len(sharing)} tracked files "
                                  f"({', '.join(sharing[:4])}); which one is meant?")
    if resolved is None and tracked_files and not _CREATES.search(order):
        return DoLaneDecision(DO_LANE_HOLD, f"{target} is not tracked and the order does not say to "
                              "create it; which existing file is meant?")
    deliverable = resolved or target
    if risk := order_risk(order, [deliverable]):
        return DoLaneDecision(DO_LANE_FULL, f"the order names one file, {deliverable}, but it is "
                              f"high-risk: {risk}", risk=risk, with_tests=with_tests)
    if not scope.simple:
        return DoLaneDecision(DO_LANE_FULL, f"the order names one file, {deliverable}, but asks for "
                              "several things")
    return DoLaneDecision(DO_LANE_BOUNDED, f"the order names one file, {deliverable}, and asks for "
                          "one thing" + (" and a test for it" if with_tests else ""),
                          deliverable, with_tests=with_tests)


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
            force_job=ctx.force_job, force_mission=ctx.force_mission)
        ctx.tiny_repo = is_tiny_repo(files)
    return ctx.lane
