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
from dataclasses import dataclass, replace
from pathlib import PurePosixPath

from packages.orchestration.do_context import DoContext
from packages.orchestration.do_scope import order_scope_files, resolve_order_path
from packages.orchestration.order_intent import (
    FILE_ROLE_CONTEXT,
    FILE_ROLE_MENTIONED,
    FILE_ROLE_OPTIONAL,
    FILE_ROLE_PROTECTED,
    FILE_ROLE_REQUIRED,
    ORDER_INTENT_CHANGE,
    ORDER_INTENT_NO_WORK,
    ORDER_INTENT_PLAN_ONLY,
    ORDER_INTENT_VERIFY_ONLY,
    independent_parts,
    order_file_roles,
    order_intent,
)
from packages.orchestration.order_scope import (
    MAX_SIMPLE_ACTIONS,
    is_scope_fence,
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

#: A small change spread over a few named files is still ONE bounded job and one task: the files a
#: rename, a fix and its call site, or a value and its two readers touch belong to one change, and a
#: planner asked to split them made two jobs that could not see each other (lab order of 2026-10-17).
#: More files than this is no longer "small" by its file count alone and gets a plan.
MAX_BOUNDED_FILES = 3

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
#: Wording that reaches past the files an order names (exec-1017c, R-1341): "in src/a.js and everywhere
#: else" names one file and asks for the project. A floor like the risk words, never a classifier; no
#: negation ("keine anderen Dateien", "nothing elsewhere") and no in-file phrase ("all occurrences").
_WIDER_SCOPE = re.compile(
    r"\b(?:everywhere|throughout\s+the\s+(?:code\s*base|project|repo\w*)|"
    r"across\s+the\s+(?:code\s*base|project|repo\w*)|in\s+(?:all|every)\s+(?:other\s+)?files?|"
    r"(?:the\s+)?(?:whole|entire)\s+(?:code\s*base|project|repo\w*)|überall|"
    r"in\s+allen\s+(?:anderen\s+)?dateien|im\s+(?:ganzen|gesamten)\s+(?:projekt|repo\w*|code))\b",
    re.IGNORECASE)
#: Wording that asks for a new file; without it a named file the repository does not track is a question.
_CREATES = re.compile(r"\b(?:create|add|write|generate|new|introduce|erstell\w*|schreib\w*|"
                      r"neu\w*|ergänz\w*|füg\w*|lege)\b", re.IGNORECASE)


@dataclass(frozen=True)
class DoLaneDecision:
    """The lane an order walks, the sentence saying why, and the one file when the lane has one.

    *risk* is the deterministic fact that took a one-file order off the bounded lane; *with_tests*
    says the order itself asks for a test beside the one file (a deliverable, never a check).
    *also* names the further files of a small change over several named files, in the order's
    own order; they belong to the same one task as *deliverable*. exec-1018: *intent* is what the
    order asks for at all (`order_intent`); *optional*, *context* and *protected* are the named files
    the order allows, only refers to, or forbids to change; *parts* groups the changed files into
    the order's independent parts, one task each, when there is more than one.
    """

    lane: str
    reason: str
    deliverable: str = ""
    risk: str = ""
    with_tests: bool = False
    also: tuple[str, ...] = ()
    intent: str = ORDER_INTENT_CHANGE
    optional: tuple[str, ...] = ()
    context: tuple[str, ...] = ()
    protected: tuple[str, ...] = ()
    parts: tuple[tuple[str, ...], ...] = ()
    #: exec-1018b (R-1358): targets whose role the order's words did not make sure; never held to change.
    mentioned: tuple[str, ...] = ()

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


def _order_targets(order: str, tracked_files: list[str], roles: dict[str, str] | None = None) -> list[str]:
    """The files an order's work is about: the files its deliverables name, else the files its scope
    fence names, else the tracked document its words name.

    A file in a test run ("run pytest tests/x.py") or in a header constraint is never a target, and a
    test file the order asks for beside its work is a companion, never a target of its own.
    """
    scope = split_order_scope(order)
    named = explicit_order_paths(" ".join(scope.deliverables))
    # exec-1018 (R-1348): a file named only as context, or that the order forbids to change, is no
    # target; a file the order merely allows is one only when it names no file to change.
    roles = roles if roles is not None else order_file_roles(order)
    required = [path for path in named if roles.get(path, FILE_ROLE_REQUIRED) == FILE_ROLE_REQUIRED]
    required += [path for path in named if roles.get(path) == FILE_ROLE_MENTIONED]     # sure ones first
    named = required or [path for path in named if roles.get(path) == FILE_ROLE_OPTIONAL]
    if not named:
        named = explicit_order_paths(" ".join(s for s in scope.constraints if is_scope_fence(s)))
    # A test file is a companion by its PATH, whatever words ask for it (lab orders of 2026-10-17:
    # "Schreibe dazu einen Regressionstest in test/format.test.js" escaped every phrase pattern and
    # the order fell to the planner). Only an order about test files alone keeps them as targets.
    if any(not is_test_path(path) for path in named):
        named = [path for path in named if not is_test_path(path)]
    if not named:
        # "Fix the typo in the readme": a tracked document whose name the order uses as a word. Only
        # documents, only long stems and only one match: "app" or "main" are words, not files.
        by_word = [t for t in order_scope_files(" ".join(scope.deliverables), tracked_files)
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
    are a few plain actions on one file, or on up to `MAX_BOUNDED_FILES` named files of one small
    change, that the repository proves (or, for a new file, that the order says to create) and no
    fact marks the change risky. A bare file name two nested files
    share, or a named file nothing tracks that the order does not create, is a question (hold),
    never a guess. A test the order asks for beside the file is part of the one job. `--force-job`
    selects the bounded lane for a single-repository order and says what routing alone chose, except
    over a hold: which file is meant stays a question that no flag answers.
    Where the order came from plays no part.
    """
    if projects > 1:
        return DoLaneDecision(DO_LANE_FULL, "the order names several projects")
    if force_mission:
        return DoLaneDecision(DO_LANE_FULL, "--force-mission was given")
    auto = _routed_lane(order, tracked_files, infer_single_file=not force_job)
    if force_job and not auto.bounded and not auto.hold:   # an override never settles a question
        return replace(auto, lane=DO_LANE_BOUNDED,
                       reason=f"--force-job was given (routing alone chose the {auto.lane} lane: {auto.reason})")
    return auto


def _routed_lane(order: str, tracked_files: list[str], *, infer_single_file: bool) -> DoLaneDecision:
    intent = order_intent(order)
    if intent == ORDER_INTENT_VERIFY_ONLY:
        # exec-1018 (R-1349): one job with no build task; its DoD runs the project's tests, no model runs.
        return DoLaneDecision(DO_LANE_BOUNDED, "the order asks only for its checks to run and for no "
                              "change: one job without a build task runs the project's tests",
                              intent=intent)
    if intent == ORDER_INTENT_NO_WORK:
        return DoLaneDecision(DO_LANE_HOLD, "the order asks for no change, no plan and no check; "
                              "what should be done?", intent=intent)
    decided = _routed_change(order, tracked_files, infer_single_file=infer_single_file)
    if intent == ORDER_INTENT_PLAN_ONLY and not decided.hold:
        return replace(decided, intent=intent, reason=f"{decided.reason}; the order asks for a plan only, "
                                                      "so nothing is run")
    return decided


def _routed_change(order: str, tracked_files: list[str], *, infer_single_file: bool) -> DoLaneDecision:
    scope = split_order_scope(order)
    roles = order_file_roles(order)
    targets = _order_targets(order, tracked_files, roles)
    named_tests = [p for p in explicit_order_paths(" ".join(scope.deliverables))
                   if is_test_path(p) and p not in targets]
    with_tests = requests_test_files(order) or bool(named_tests)
    if len(targets) > MAX_BOUNDED_FILES:
        return DoLaneDecision(DO_LANE_FULL, f"the order names {len(targets)} files, more than the "
                              f"{MAX_BOUNDED_FILES} one bounded job changes")
    if not targets:
        if infer_single_file and len(tracked_files) == 1 and scope.single:
            return DoLaneDecision(
                DO_LANE_BOUNDED, f"the repository tracks one file, {tracked_files[0]}, and the order "
                "has one part", tracked_files[0], with_tests=with_tests)
        return DoLaneDecision(DO_LANE_FULL, "the scope of the order is not clearly one file")
    files: list[str] = []
    for target in targets:
        resolved, question = _resolved_target(order, target, tracked_files)
        if question:
            return DoLaneDecision(DO_LANE_HOLD, question)
        files.append(resolved)
    deliverable, also = files[0], tuple(dict.fromkeys(f for f in files[1:] if f != files[0]))
    named = f"one file, {deliverable}" if not also else f"{1 + len(also)} files, {', '.join((deliverable, *also))}"
    if risk := order_risk(order, [deliverable, *also]):
        return DoLaneDecision(DO_LANE_FULL, f"the order names {named}, but it is high-risk: {risk}",
                              risk=risk, with_tests=with_tests)
    # One named file (and its tests) is one job whatever the order's wording: how many sentences
    # it has or which verbs they use no longer sends it to the planner (lab orders of 2026-10-17,
    # where each new phrasing missed a pattern and the local planner's plan then failed outright).
    # A few named files of one small change are the same one job. Only many explicit actions ("add a
    # section, write a changelog entry, add a CI workflow") still go to the planner: they likely
    # need files the order does not name.
    if wider := _WIDER_SCOPE.search(order):
        return DoLaneDecision(DO_LANE_FULL, f"the order names {named}, but reaches beyond {'them' if also else 'it'} "
                              f"({wider.group(0)!r})", with_tests=with_tests)
    if scope.actions > MAX_SIMPLE_ACTIONS:
        return DoLaneDecision(DO_LANE_FULL, f"the order names {named}, but asks for "
                              f"{scope.actions} separate actions")
    # exec-1017c (R-1341): several named files are one bounded job by their count, not because the
    # order asks for one thing; the reason says which, and every named file must change (R-1342).
    # exec-1018 (R-1350): parts that refer to nothing of each other are one task each; a requested
    # test keeps the change one task, since no fact says which part it tests.
    resolved = dict(zip(targets, files))
    sure = [path for path in targets if roles.get(path) != FILE_ROLE_MENTIONED] or list(targets)
    # R-1358: a file the words do not clearly ask to change is never a part, so never a task of its own.
    parts = [] if with_tests else [[resolved[path] for path in part] for part in independent_parts(order, sure)]
    unsure = [resolved[path] for path in targets if roles.get(path) == FILE_ROLE_MENTIONED]
    held = (f"each of which must change but {', '.join(unsure)}, which its words do not clearly ask to change"
            if unsure else "each of which must change")
    asks = ("asks for one thing" if not also else
            f"they are {len(parts)} independent parts of one bounded job, one task each, {held}"
            if len(parts) > 1 else f"they are one bounded job of at most {MAX_BOUNDED_FILES} files, {held}")
    roles_of = {role: tuple(dict.fromkeys(resolve_order_path(path, tracked_files) or path for path, named_role
                                          in roles.items() if named_role == role and path not in resolved))
                for role in (FILE_ROLE_OPTIONAL, FILE_ROLE_CONTEXT, FILE_ROLE_PROTECTED)}
    return DoLaneDecision(DO_LANE_BOUNDED, f"the order names {named}, and {asks}"
                          + (" and a test for it" if with_tests else ""),
                          deliverable, with_tests=with_tests, also=also, optional=roles_of[FILE_ROLE_OPTIONAL],
                          context=roles_of[FILE_ROLE_CONTEXT], protected=roles_of[FILE_ROLE_PROTECTED],
                          parts=tuple(tuple(part) for part in parts) if len(parts) > 1 else (),
                          mentioned=tuple(unsure))


def _resolved_target(order: str, target: str, tracked_files: list[str]) -> tuple[str, str]:
    """``(path, question)``: the tracked file *target* means, or the question a hold asks instead."""
    resolved = resolve_order_path(target, tracked_files)
    if resolved is None and tracked_files and "/" not in target:
        sharing = [t for t in tracked_files if PurePosixPath(t).name == target]
        if len(sharing) > 1:
            return "", (f"{target} matches {len(sharing)} tracked files "
                        f"({', '.join(sharing[:4])}); which one is meant?")
    if resolved is None and tracked_files and not _CREATES.search(order):
        return "", f"{target} is not tracked and the order does not say to create it; which existing file is meant?"
    return resolved or target, ""


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
        # exec-1018 (R-1349): an order whose own words ask for a plan only walks as `--plan-only`.
        ctx.plan_only = ctx.plan_only or ctx.lane.intent == ORDER_INTENT_PLAN_ONLY
    return ctx.lane
