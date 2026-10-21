"""What running work may DO at each autonomy level, answered by one table (DECISION F141 D1).

F078 answers who may START a job; this module answers what a job already running may then DO —
read, write a job's result into the project, commit, push, change a dependency, delete files or
run a migration, spend above the cost threshold, and reach the network — at each of F078's levels
`L2` to `L5`, through one check every seam calls: :func:`require_permission` (or its plural,
:func:`require_permissions`, for one instance that needs several actions at once).

A cell of :data:`PERMISSION_MATRIX` never REPLACES a gate a seam already has: fences say WHERE a
job may write, the apply's own approval, budgets and the cost threshold's prompt all still apply
at every level, whatever this module answers.
"""

from __future__ import annotations

import json
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING

from packages.common.secure_fs import durable_write_json
from packages.orchestration.autonomy_gate import AUTONOMY_DEFAULT_LEVEL, AUTONOMY_LEVELS, AutonomyConfigError
from packages.orchestration.data_paths import data_class_dir, job_dir, resolve_data_root

if TYPE_CHECKING:  # import-light at runtime: config.py's types are only named here
    from packages.orchestration.config import RemedyConfig


# The eight action classes the matrix covers, and the fixed order every citation,
# every joined reason and every row of the rendered table walks them in.
PERMISSION_ACTIONS: tuple[str, ...] = (
    "read",
    "write_worktree",
    "commit",
    "push",
    "dependency_change",
    "destructive",
    "expensive",
    "external_call",
)

# The three answers one cell of the matrix ever holds.
PERMISSION_ALLOW = "allow"
PERMISSION_ASK = "ask"
PERMISSION_DENY = "deny"

# Every cell value, in the order a reader of a cell expects: allow, then ask, then deny.
PERMISSION_CELLS: tuple[str, ...] = (PERMISSION_ALLOW, PERMISSION_ASK, PERMISSION_DENY)

# The policy table itself (DECISION F141 D1 (2)): one cell per action and level, reviewed as this
# feature's policy core. `push` and `destructive` ask at every level — no level lets Remedy do
# either without a human approving that one instance.
PERMISSION_MATRIX: dict[tuple[str, str], str] = {
    ("read", "L2"): PERMISSION_ALLOW,
    ("read", "L3"): PERMISSION_ALLOW,
    ("read", "L4"): PERMISSION_ALLOW,
    ("read", "L5"): PERMISSION_ALLOW,
    ("write_worktree", "L2"): PERMISSION_ASK,
    ("write_worktree", "L3"): PERMISSION_ASK,
    ("write_worktree", "L4"): PERMISSION_ALLOW,
    ("write_worktree", "L5"): PERMISSION_ALLOW,
    ("commit", "L2"): PERMISSION_ASK,
    ("commit", "L3"): PERMISSION_ASK,
    ("commit", "L4"): PERMISSION_ASK,
    ("commit", "L5"): PERMISSION_ALLOW,
    ("push", "L2"): PERMISSION_ASK,
    ("push", "L3"): PERMISSION_ASK,
    ("push", "L4"): PERMISSION_ASK,
    ("push", "L5"): PERMISSION_ASK,
    ("dependency_change", "L2"): PERMISSION_ASK,
    ("dependency_change", "L3"): PERMISSION_ASK,
    ("dependency_change", "L4"): PERMISSION_ALLOW,
    ("dependency_change", "L5"): PERMISSION_ALLOW,
    ("destructive", "L2"): PERMISSION_ASK,
    ("destructive", "L3"): PERMISSION_ASK,
    ("destructive", "L4"): PERMISSION_ASK,
    ("destructive", "L5"): PERMISSION_ASK,
    ("expensive", "L2"): PERMISSION_ASK,
    ("expensive", "L3"): PERMISSION_ASK,
    ("expensive", "L4"): PERMISSION_ASK,
    ("expensive", "L5"): PERMISSION_ALLOW,
    ("external_call", "L2"): PERMISSION_ALLOW,
    ("external_call", "L3"): PERMISSION_ALLOW,
    ("external_call", "L4"): PERMISSION_ALLOW,
    ("external_call", "L5"): PERMISSION_ALLOW,
}

# The words each action's sentence names (DECISION F141 D1 (4)): what a person reads in place of
# the action's own key.
_ACTION_WORDS: dict[str, str] = {
    "read": "read your project's files",
    "write_worktree": "write a job's result into your project's files",
    "commit": "commit in your project's repository",
    "push": "push to your project's remote",
    "dependency_change": "change your project's dependencies",
    "destructive": "delete files or run a migration in your project",
    "expensive": "start work estimated above your cost threshold",
    "external_call": "run a command that reaches the network",
}

# The two ways a person may approve one asked instance (DECISION F141 D1 (4)).
APPROVAL_KIND_FLAG = "flag"
APPROVAL_KIND_DECISION = "decision"


# One person's approval of ONE instance of an asked action — a command flag or an answered
# decision — never a standing widening of a cell.
@dataclass(frozen=True)
class InstanceApproval:
    kind: str
    ref: str

    def __post_init__(self) -> None:
        if self.kind not in (APPROVAL_KIND_FLAG, APPROVAL_KIND_DECISION):
            raise ValueError(f"not a known approval kind: {self.kind!r}")
        if not self.ref:
            raise ValueError("an instance approval needs a non-empty ref")


# What a caller asks the matrix about: the job's pinned level, who or what this is for, and,
# when one exists, the approval of this one instance.
@dataclass(frozen=True)
class PermissionRequest:
    level: str
    subject: str
    job_id: str | None = None
    approval: InstanceApproval | None = None


# The matrix's answer: whether the caller may proceed, every action and cell it was asked about
# (in PERMISSION_ACTIONS order, whatever order the caller gave), and the sentence(s) saying why.
@dataclass(frozen=True)
class PermissionVerdict:
    outcome: str
    actions: tuple[str, ...]
    level: str
    cells: tuple[str, ...]
    reason: str


# Raised the moment any one action's cell is `deny` — never lifted by an approval.
class PermissionRefusedError(Exception):
    def __init__(self, *, action: str, level: str, cell: str, reason: str) -> None:
        super().__init__(reason)
        self.action = action
        self.level = level
        self.cell = cell
        self.reason = reason


# Where every satisfied `ask` is audited, under F078's durable "autonomy" data class.
PERMISSION_GRANTS_FILENAME = "permission_grants.jsonl"

# Where a job's pinned level lives, inside that job's own directory (DECISION F141 D2 (2)): a
# job's own folder, never the durable "autonomy" class, so the pin dies with the job it pinned.
JOB_LEVEL_FILENAME = "autonomy_level.json"


# DECISION F141 D1 (3): the one key that can only ever make the `push` cell stricter than the
# table says, never looser.
def push_allowed_by_config(config: RemedyConfig | None = None) -> bool:
    from packages.orchestration.config import ConfigSource, get_config

    cfg = config if config is not None else get_config()
    if cfg.get_source("autonomy.allow_push") == ConfigSource.ENV:
        raise AutonomyConfigError(
            "autonomy.allow_push is set by the environment variable REMEDY_AUTONOMY_ALLOW_PUSH, "
            "and what Remedy may do is changed only by editing a config file. Unset "
            "REMEDY_AUTONOMY_ALLOW_PUSH and set autonomy.allow_push in remedy.toml."
        )
    value = cfg.get("autonomy.allow_push")
    if not isinstance(value, bool):
        raise AutonomyConfigError(f"autonomy.allow_push must be true or false, not {value!r}.")
    return value


# The one cell an action and level resolve to, with the push switch applied; this only ever makes
# a cell STRICTER than the table alone would answer.
def permission_cell(action: str, level: str, *, push_allowed: bool) -> str:
    if action not in PERMISSION_ACTIONS:
        raise ValueError(f"not a known permission action: {action!r}")
    if level not in AUTONOMY_LEVELS:
        raise ValueError(f"not a known autonomy level: {level!r}")
    if action == "push" and not push_allowed:
        return PERMISSION_DENY
    return PERMISSION_MATRIX[(action, level)]


# The level pinned to a job's first context, read back on every later one (DECISION F141 D2
# (2)): a config change mid-run must not change what an already-running job may do.
def pinned_job_level(job_id: str | None, *, root: Path | None = None) -> str:
    if not job_id:
        return AUTONOMY_DEFAULT_LEVEL
    path = job_dir(job_id, root if root is not None else resolve_data_root()) / JOB_LEVEL_FILENAME
    if not path.is_file():
        return AUTONOMY_DEFAULT_LEVEL
    try:
        parsed = json.loads(path.read_text(encoding="utf-8"))
    except ValueError:
        parsed = None
    level = parsed.get("level") if isinstance(parsed, dict) else None
    if not isinstance(level, str) or level not in AUTONOMY_LEVELS:
        raise AutonomyConfigError(
            f"The level recorded for job {job_id} in {path} is not one of L2, L3, L4 or L5."
        )
    return level


# Pins a job's level on its FIRST context, from the policy in force at that moment, so every
# later read of this same job (`pinned_job_level`) answers unchanged (DECISION F141 D2 (2)).
def pin_job_level(
    job_id: str | None, *, config: RemedyConfig | None = None, root: Path | None = None,
    now: datetime | None = None,
) -> str:
    if not job_id:
        return AUTONOMY_DEFAULT_LEVEL
    data_root = root if root is not None else resolve_data_root()
    folder = job_dir(job_id, data_root)
    path = folder / JOB_LEVEL_FILENAME
    if path.is_file():
        return pinned_job_level(job_id, root=data_root)
    from packages.orchestration.autonomy_gate import load_autonomy_policy

    policy = load_autonomy_policy(config, root=data_root, record=False)
    if not folder.is_dir():
        return policy.level
    when = now if now is not None else datetime.now(timezone.utc)
    durable_write_json(path, {
        "level": policy.level, "pinned_at": when.isoformat(), "config_path": policy.config_path,
    })
    return policy.level


def _lowest_allowing_level(action: str) -> str | None:
    """The lowest level whose matrix cell for ACTION is `allow`, or None when no level does."""
    for level in AUTONOMY_LEVELS:
        if PERMISSION_MATRIX[(action, level)] == PERMISSION_ALLOW:
            return level
    return None


def _approved_by(approval: InstanceApproval) -> str:
    """The phrase naming who approved an instance, for the allow-sentence of an asked action."""
    if approval.kind == APPROVAL_KIND_FLAG:
        return f"your flag {approval.ref}"
    return f"your answer to decision {approval.ref}"


def _append_grant(
    *, action: str, level: str, cell: str, approval: InstanceApproval, job_id: str | None,
    subject: str, root: Path | None, when: datetime,
) -> None:
    """One audited line for one satisfied `ask`, creating the folder (DECISION F141 D1 (5))."""
    folder = data_class_dir("autonomy", root if root is not None else resolve_data_root())
    folder.mkdir(parents=True, exist_ok=True)
    line = {
        "at": when.isoformat(),
        "action": action,
        "level": level,
        "cell": cell,
        "approval_kind": approval.kind,
        "approval_ref": approval.ref,
        "job_id": job_id,
        "subject": subject,
    }
    with (folder / PERMISSION_GRANTS_FILENAME).open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(line) + "\n")


# The one check every seam calls for SEVERAL actions of one instance at once (DECISION F141 D1
# (7), the conjunction): every cell must pass, a `deny` among them refusing first.
def require_permissions(
    actions: Sequence[str],
    request: PermissionRequest,
    *,
    config: RemedyConfig | None = None,
    root: Path | None = None,
    now: datetime | None = None,
) -> PermissionVerdict:
    if not actions:
        raise ValueError("require_permissions needs at least one action")
    if len(set(actions)) != len(actions):
        raise ValueError(f"a permission action was repeated: {tuple(actions)!r}")
    unknown_actions = [action for action in actions if action not in PERMISSION_ACTIONS]
    if unknown_actions:
        raise ValueError(f"not a known permission action: {unknown_actions[0]!r}")
    if request.level not in AUTONOMY_LEVELS:
        raise ValueError(f"not a known autonomy level: {request.level!r}")

    level = request.level
    ordered = tuple(action for action in PERMISSION_ACTIONS if action in actions)

    push_allowed = push_allowed_by_config(config) if "push" in ordered else True
    cells = tuple(permission_cell(action, level, push_allowed=push_allowed) for action in ordered)
    citations = tuple(f"({action}, {level}) = {cell}" for action, cell in zip(ordered, cells))

    for action, cell, citation in zip(ordered, cells, citations):
        if cell != PERMISSION_DENY:
            continue
        words = _ACTION_WORDS[action]
        if action == "push" and not push_allowed:
            reason = (
                f"Remedy may not {words} ({citation}): autonomy.allow_push is false in your "
                "configuration, at every autonomy level."
            )
        else:
            reason = f"Autonomy level {level} does not let Remedy {words} ({citation})."
        raise PermissionRefusedError(action=action, level=level, cell=cell, reason=reason)

    asking = [
        (action, cell, citation) for action, cell, citation in zip(ordered, cells, citations)
        if cell == PERMISSION_ASK
    ]
    if asking and request.approval is None:
        sentences = []
        for action, _cell, citation in asking:
            words = _ACTION_WORDS[action]
            first = _lowest_allowing_level(action)
            lift = (
                f"raise the level to {first} with its decision record" if first is not None
                else "no level lets Remedy do it without asking"
            )
            sentences.append(
                f"Autonomy level {level} asks before Remedy may {words} ({citation}): approve "
                f"this instance, or {lift}."
            )
        return PermissionVerdict(
            outcome=PERMISSION_ASK, actions=ordered, level=level, cells=citations,
            reason=" ".join(sentences),
        )

    when = now if now is not None else datetime.now(timezone.utc)
    sentences = []
    for action, cell, citation in zip(ordered, cells, citations):
        words = _ACTION_WORDS[action]
        if cell == PERMISSION_ALLOW:
            sentences.append(
                f"Autonomy level {level} lets Remedy {words} without asking ({citation})."
            )
            continue
        approval = request.approval
        sentences.append(
            f"Autonomy level {level} asks before Remedy may {words} ({citation}), and this "
            f"instance was approved by {_approved_by(approval)}."
        )
        _append_grant(
            action=action, level=level, cell=cell, approval=approval, job_id=request.job_id,
            subject=request.subject, root=root, when=when,
        )

    return PermissionVerdict(
        outcome=PERMISSION_ALLOW, actions=ordered, level=level, cells=citations,
        reason=" ".join(sentences),
    )


# The one check every seam calls for a SINGLE action of one instance (DECISION F141 D1 (1)).
def require_permission(
    action: str,
    request: PermissionRequest,
    *,
    config: RemedyConfig | None = None,
    root: Path | None = None,
    now: datetime | None = None,
) -> PermissionVerdict:
    return require_permissions((action,), request, config=config, root=root, now=now)
