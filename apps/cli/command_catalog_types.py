"""The command catalog's types and its shared argument shorthands (F301, DECISION F301 D2).

Moved unchanged out of `apps/cli/command_catalog.py`, which imports every name back by name, so
`from apps.cli.command_catalog import ArgDef` keeps working. A group of the catalog whose entries
live in a module of their own imports from here, which is what lets a group's data leave the
catalog without an import cycle.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from apps.cli.exit_codes import EXIT_CODE_FLOOR

# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------

ActionClass = Literal[
    "read_only",
    "write_metadata",
    "approval_gate",
    "apply_write",
    "test_execution",
    "dev_helper",
    "local_state_change",
    "controlled_builder_execution",
]

#: The product path that reaches a command group (DECISION amend0905-vocab D11 (a)).
Reach = Literal[
    "golden-path",
    "job-path",
    "mission-path",
    "self-use",
    "teacher",
    "cockpit",
    "self-build",
]


@dataclass(frozen=True)
class GroupDef:
    """A top-level command group (e.g. 'job', 'brain')."""

    id: str
    label: str
    description: str
    user_facing: bool = True
    #: A hidden group appears in no help at all, neither `remedy --help` nor
    #: `remedy --all-commands`, and stays callable: its own help and its commands
    #: still work (DECISION amend0905-vocab D4).
    hidden: bool = False
    #: Further words that reach this same group (DECISION amend0831 D-D): one
    #: `GroupDef` and one set of commands, never a duplicated definition.
    #: `resolve_group` maps each of them to `id` for every group lookup.
    aliases: tuple[str, ...] = ()
    #: The owning feature id, e.g. "F261", and the path that reaches the group
    #: (DECISION amend0905-vocab D11 (a)). Defaulted so that a group missing
    #: either is refused by the catalog ownership test, not by a TypeError.
    feature: str = ""
    reach: Reach | None = None


@dataclass(frozen=True)
class ArgDef:
    """A single CLI argument or option."""

    name: str
    help: str
    required: bool = True
    is_option: bool = False
    default: str | None = None
    #: A boolean flag takes NO value (`--status`), a valued option does (`--status pending`).
    #: Declared per ARGUMENT, because the same option name means different things to
    #: different commands: `job stop --status` is a flag, `propose list --status pending`
    #: is not. F011 briefly special-cased the NAME in the parser and broke `propose list`.
    is_flag: bool = False
    #: A repeatable option collects every occurrence into a list
    #: (`--answer q1=a --answer q2=b`) instead of last-one-wins.
    is_repeatable: bool = False


@dataclass(frozen=True)
class CommandEntry:
    """One entry in the command catalog."""

    command_id: str
    group_id: str
    subcommand: str
    description: str
    action_class: ActionClass
    args: tuple[ArgDef, ...] = ()
    supports_json: bool = False
    requires_permission: bool = False
    may_mutate_repo: bool = False
    may_execute_commands: bool = False
    #: True marks a command whose real-money spend requires an upfront
    #: estimate and, above a configured threshold, operator confirmation
    #: before it runs (F114). Explicit and reviewable per command - never
    #: derived from another flag such as may_execute_commands.
    is_expensive: bool = False
    related: tuple[str, ...] = ()
    #: The codes this command's handler can exit with (DECISION F283 D12 (4)),
    #: ascending, always the floor plus whatever it reaches above it.
    #: `tests/cli/test_exit_codes.py` asserts this against a static reading.
    exit_codes: tuple[int, ...] = EXIT_CODE_FLOOR


# ---------------------------------------------------------------------------
# Argument shorthands
# ---------------------------------------------------------------------------

_JOB_ID = ArgDef("job_id", "UUID of the job (under its mission)")
_PROJECT_ID = ArgDef("project_id", "UUID or name of the project (its repo)")
_INTENT_ID = ArgDef("intent_id", "Intent ID (integer)")
_JSON_OPT = ArgDef("--json", "Output as JSON", required=False, is_option=True, default="false")
#: F107: names ONE task of a job — its planned id (`T001`) or a prefix of its
#: task UUID. A valued option, never a flag, and never defaulted to a guess.
_TASK_OPT = ArgDef(
    "--task", "Task to select from the job plan: planned id (T001) or task-id prefix",
    required=False, is_option=True)
_REASON_OPT = ArgDef("--reason", "Reason text", required=False, is_option=True)
#: F015 T002: every job plan edit names the version it was made against, as
#: `remedy job plan-show` prints it, so an edit made on an older reading is refused.
_PLAN_VERSION_OPT = ArgDef(
    "--plan-version", "The version `remedy job plan-show` prints for the job plan and its tasks; "
    "an edit made against an older one is refused (required)", required=False, is_option=True)
_PLAN_TASK_ID = ArgDef("task_id", "The task's id, as `remedy job plan-show` prints it")
_ANSWER_OPT = ArgDef(
    "--answer",
    'Answer one bundled clarification (--answer q1="use PostgreSQL") or raise a '
    "budget decision's limit (--answer max_cost_usd=2.5); repeatable",
    required=False, is_option=True, is_repeatable=True)
_APPLY_ID_OPT = ArgDef("--apply-id", "Explicit apply_id (overrides intent_id lookup)", required=False, is_option=True)
#: F033: names ONE task run whose diff to decide hunks over. Deliberately NOT
#: `_TASK_OPT`, which promises "planned id (T001) or task-id prefix":
#: `diff_view_source.build_diff_view` does no prefix resolution at all — it
#: requires exact membership in the real `task_runs/` listing — and promising a
#: prefix match the code does not perform is worse than a second option name.
_TASK_RUN_OPT = ArgDef(
    "--task-run",
    "Task run to decide over, exactly as it is named under task_runs/ (T001); "
    "omit it to decide over the job-level diff",
    required=False, is_option=True)
#: DECISION F295 D14: the same option for `patch.hunks`, which shows a diff
#: rather than deciding over one, so its help says so.
_TASK_RUN_SHOW_OPT = ArgDef(
    "--task-run",
    "Task run whose hunks to show, exactly as it is named under task_runs/ (T001); "
    "omit it for the job-level diff",
    required=False, is_option=True)
#: F033: repeatable, one hunk id per occurrence.
_APPROVE_HUNK_OPT = ArgDef(
    "--approve-hunk", "Approve one hunk by id (repeatable)",
    required=False, is_option=True, is_repeatable=True)
#: F033: repeatable. The reason is kept VERBATIM — T003 quotes it into the next
#: repair prompt — so the shape is shown rather than described away.
_REJECT_HUNK_OPT = ArgDef(
    "--reject-hunk",
    'Reject one hunk with a reason: --reject-hunk <hunk-id>=<reason>, '
    'e.g. --reject-hunk h3="renames a public name" (repeatable)',
    required=False, is_option=True, is_repeatable=True)
#: F056: the plan-approval opt-in. Its ABSENCE is the default — approving
#: without it creates no mission, which is the whole point of the opt-in.
_AS_MISSION_FLAG = ArgDef(
    "--as-mission",
    "When approving: also create a mission for this goal and link this job as its initial job",
    required=False, is_option=True, is_flag=True)
_PROJECT_SCOPE_OPT = ArgDef("--project", "Scope to a project's repo (slug or UUID)", required=False, is_option=True)
_ALL_PROJECTS_FLAG = ArgDef("--all-projects", "Show jobs from all projects", required=False, is_option=True, is_flag=True)
