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
PERMISSION_ACTION_WORDS: dict[str, str] = {
    "read": "read your project's files",
    "write_worktree": "write a job's result into your project's files",
    "commit": "commit in your project's repository",
    "push": "push to your project's remote",
    "dependency_change": "change your project's dependencies",
    "destructive": "delete files or run a migration in your project",
    "expensive": "start work estimated above your cost threshold",
    "external_call": "run a command that reaches the network",
}


# Where each action is asked and what approves one instance (DECISION F141 D6 (1)):
# one entry per action in PERMISSION_ACTIONS order, rendered onto the page's second table.
PERMISSION_SEAMS: dict[str, str] = {
    "read": ("`build_builder_context` in `packages/orchestration/builder_context.py`, before the context "
             "of a builder's call is built; it allows at every level, and the first check of a job's run "
             "records the job's level"),
    "write_worktree": ("`_flag_refusals` in `packages/orchestration/job_apply.py`, through "
                       "`apply_permission_refusals`, when `remedy job apply` or a walk of `remedy do run` "
                       "writes a job's result into your project; approved by `--approve`"),
    "commit": ("the same place, when the apply commits; approved by `--commit`, `--commit-auto` or "
               "`--commit-with-history`"),
    "push": ("the same place, when the apply pushes, and `do_mission_push_refusals` and `do_push_mission` "
             "in `packages/orchestration/do_apply.py` for a walk's push; approved by `--push` or by the "
             "key `apply.push_after_mission`"),
    "dependency_change": ("the apply, when a path it writes is a dependency manifest; approved by your "
                          "answer `approve` to the decision the apply raises"),
    "destructive": ("the apply, when a path it writes lies in a `migrations` folder or a "
                    "`--commit-with-history` branch deletes a file; approved by your answer `approve` to "
                    "the decision the apply raises"),
    "expensive": ("`confirm_cost_preview` in `apps/cli/cost_preview_confirm.py`, for `remedy job resume` "
                  "and `remedy job rerun-subtree` above `cost_preview.confirm_above_usd`; approved by "
                  "`--yes`, `--unattended` or your `y` at its prompt"),
    "external_call": ("`plan_child_spawn` in `packages/orchestration/exec_guard.py`, for every child "
                      "process that keeps the network; it allows at every level"),
}


# Where render_permission_matrix_page's output is committed (DECISION F141 D6 (1));
# tests/docs/test_permission_matrix_page.py holds it equal to the rendering.
PERMISSION_MATRIX_PAGE_PATH = Path("docs/system/permission-matrix-v1.md")

# The three ways a person may approve one asked instance (DECISION F141 D1 (4);
# DECISION F141 D5 (1) adds the prompt: the operator's `y` at a command's own prompt, approving
# this one instance exactly as a flag does, its `ref` the command's name).
APPROVAL_KIND_FLAG = "flag"
APPROVAL_KIND_DECISION = "decision"
APPROVAL_KIND_PROMPT = "prompt"


# One person's approval of ONE instance of an asked action — a command flag or an answered
# decision — never a standing widening of a cell.
@dataclass(frozen=True)
class InstanceApproval:
    kind: str
    ref: str

    def __post_init__(self) -> None:
        if self.kind not in (APPROVAL_KIND_FLAG, APPROVAL_KIND_DECISION, APPROVAL_KIND_PROMPT):
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
    if approval.kind == APPROVAL_KIND_PROMPT:
        return f"your answer at the prompt of {approval.ref}"
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
        words = PERMISSION_ACTION_WORDS[action]
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
            words = PERMISSION_ACTION_WORDS[action]
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
        words = PERMISSION_ACTION_WORDS[action]
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


# Renders docs/system/permission-matrix-v1.md whole from the constants above, so a row can
# never drift from the page describing it (DECISION F141 D6 (1)): delete a row and both lose it.
def render_permission_matrix_page() -> str:
    cells = "\n".join(
        f"| `{action}` | {PERMISSION_ACTION_WORDS[action]} | "
        + " | ".join(PERMISSION_MATRIX[(action, level)] for level in AUTONOMY_LEVELS) + " |"
        for action in PERMISSION_ACTIONS
    )
    seams = "\n".join(
        f"| `{action}` | {PERMISSION_SEAMS[action]} |" for action in PERMISSION_ACTIONS
    )
    template = """# Permission matrix (v1)

> GENERATED from `PERMISSION_MATRIX`, `PERMISSION_ACTION_WORDS` and `PERMISSION_SEAMS` in
> `packages/orchestration/permission_matrix.py` by `render_permission_matrix_page()`. Do not edit it
> by hand: `tests/docs/test_permission_matrix_page.py` fails whenever the constants and this file
> differ. Regenerate it from the repository root with
> `python3 -c "from packages.orchestration.permission_matrix import write_permission_matrix_page; write_permission_matrix_page()"`.

The permission matrix says what the work Remedy runs may DO at each autonomy level; the autonomy
level itself (`docs/system/autonomy-levels-v1.md`) says who may START that work. Every place that
acts asks one check, `require_permission`, and every answer names its cell as
`(action, level) = cell` (F141, DECISIONs F141 D1 to D6).

## The table

| Action | What it means | L2 | L3 | L4 | L5 |
|---|---|---|---|---|---|
{cells}

`allow` means the matrix asks nothing more of this one instance. `ask` means the action goes ahead
only with your approval of this one instance: the flag of your own command that names it, your `y`
at the command's own prompt, or your answer `approve` to the decision the apply raises for a
dependency change or a deletion. `deny` means refused, with or without an approval; only a change
of the configuration lifts it. An instance that needs several actions needs every one of their
cells.

A cell never replaces a gate a place already has: the scope fences still say where a job may
write, an apply still needs `--approve`, and budgets and the cost threshold's prompt still apply at
every level.

## The push switch

`autonomy.allow_push`, true by default, set in `remedy.toml` and refused from the environment,
turns every `push` cell into `deny` when it is false, at every level. It can only make the table
stricter.

## Where each action is asked

| Action | Where it is asked, and what approves one instance |
|---|---|
{seams}

## The record of approvals

Every `ask` that an approval satisfied leaves one line in
`<data root>/autonomy/permission_grants.jsonl`, with `at`, `action`, `level`, `cell`,
`approval_kind` (`flag`, `prompt` or `decision`), `approval_ref`, `job_id` and `subject`.

## The level a job runs at

A job keeps the level in force at its first context: the first `read` check of its run writes
`autonomy_level.json` into the job's folder, and every later check reads it back, so a level
changed while a job runs never reaches that job. A job without that file reads `L2`, and so does
work that belongs to no job.

## What the matrix does not replace

- The worker's writes inside a job's own workspace are not an action of the matrix: the workspace
  is the job, and the scope fences say where in it the job may write.
- `packages/orchestration/permissions.py` grants a job the capabilities its own steps need inside
  its workspace. It is a layer below the matrix, like the fences, and the matrix still answers for
  everything that reaches your project.
- The integer `autonomy_level` of the builder bridge and the 0 to 7 readiness scale are other
  scales, not the levels `L2` to `L5`.
- Remedy deliberately has no switch that turns the matrix off: the only way past an `ask` is your
  approval of the one instance, and the only way past a `deny` is the configuration.
"""
    return template.replace("{cells}", cells).replace("{seams}", seams)


# Writes the rendered page under ROOT (the repository root by default) and answers its path,
# mirroring write_environment_guide (DECISION F141 D6 (1)).
def write_permission_matrix_page(root: Path | None = None) -> Path:
    base = root if root is not None else Path(__file__).resolve().parents[2]
    path = base / PERMISSION_MATRIX_PAGE_PATH
    path.write_text(render_permission_matrix_page(), encoding="utf-8")
    return path
