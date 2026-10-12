"""The `project` group's entries of the command catalog (F206, DECISION F206 D4).

Moved unchanged out of `apps/cli/command_catalog.py`, whose `_BASE_CATALOG` splices
`PROJECT_COMMANDS` in at the group's own place, so the help keeps its order.
"""

from __future__ import annotations

from apps.cli.command_catalog_types import (
    _JOB_ID,
    _JSON_OPT,
    _PROJECT_ID,
    ArgDef,
    CommandEntry,
)

PROJECT_COMMANDS: tuple[CommandEntry, ...] = (
    # ── project ──────────────────────────────────────────────────────────
    CommandEntry(
        command_id="project.create",
        group_id="project",
        subcommand="create",
        description="Create a new project for a repo.",
        action_class="write_metadata",
        args=(
            ArgDef("name", "Project name (its repo)"),
            ArgDef("--description", "Project description (its repo)", required=False, is_option=True),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("project.show",),
    ),
    CommandEntry(
        command_id="project.list",
        group_id="project",
        subcommand="list",
        description="List all projects.",
        action_class="read_only",
        args=(_JSON_OPT,),
        supports_json=True,
    ),
    CommandEntry(
        command_id="project.show",
        group_id="project",
        subcommand="show",
        description="Show the project's repo details.",
        action_class="read_only",
        args=(_PROJECT_ID, _JSON_OPT),
        supports_json=True,
        related=("project.list", "project.context"),
    ),
    CommandEntry(
        command_id="project.attach-repo",
        group_id="project",
        subcommand="attach-repo",
        description="Attach a repository path to a project.",
        action_class="write_metadata",
        args=(_PROJECT_ID, ArgDef("repo_path", "Path to the repository"), _JSON_OPT),
        supports_json=True,
    ),
    CommandEntry(
        command_id="project.attach-job",
        group_id="project",
        subcommand="attach-job",
        description="Link a job to a project's repo, under its mission.",
        action_class="write_metadata",
        args=(_PROJECT_ID, _JOB_ID, _JSON_OPT),
        supports_json=True,
    ),
    CommandEntry(
        command_id="project.brain",
        group_id="project",
        subcommand="brain",
        description="Show the aggregate brain graph of the project's repo, across all jobs.",
        action_class="read_only",
        args=(_PROJECT_ID, _JSON_OPT),
        supports_json=True,
        related=("brain.graph", "project.show"),
    ),
    CommandEntry(
        command_id="project.context",
        group_id="project",
        subcommand="context",
        description="Show the project's repo context and constitution.",
        action_class="read_only",
        args=(_PROJECT_ID, _JSON_OPT),
        supports_json=True,
        related=("project.show",),
    ),

    CommandEntry(
        command_id="project.summary",
        group_id="project",
        subcommand="summary",
        description="Show the project's repo-level summary with patterns and suggestions.",
        action_class="read_only",
        args=(_PROJECT_ID, _JSON_OPT),
        supports_json=True,
        related=("project.show", "project.brain"),
    ),
    CommandEntry(
        command_id="project.current",
        group_id="project",
        subcommand="current",
        description="Show the project's repo, resolved from the current directory.",
        action_class="read_only",
        args=(
            ArgDef("--project", "Project's repo, slug or UUID", required=False, is_option=True),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("project.show", "project.list"),
        exit_codes=(0, 1, 2, 3),
    ),
    CommandEntry(
        command_id="project.attach",
        group_id="project",
        subcommand="attach",
        description="Attach a repository path to the current project.",
        action_class="write_metadata",
        args=(
            ArgDef("--project", "Project's repo, slug or UUID", required=False, is_option=True),
            ArgDef("--repo", "Path to the repository", required=True, is_option=True),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("project.current",),
        exit_codes=(0, 1, 2, 3),
    ),
    CommandEntry(
        command_id="project.adopt",
        group_id="project",
        subcommand="adopt",
        description="Adopt a single unscoped job into the current project's repo, under its mission.",
        action_class="write_metadata",
        args=(
            _JOB_ID,
            ArgDef("--project", "Project's repo, slug or UUID", required=False, is_option=True),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("project.attach-job", "job.list"),
        exit_codes=(0, 1, 2, 3),
    ),
    CommandEntry(
        command_id="project.register",
        group_id="project",
        subcommand="register",
        description="Register a repository as a project's repo, writing nothing its git status shows; a repo already registered answers its project.",
        action_class="write_metadata",
        args=(
            ArgDef("--repo", "Path to the repository", required=True, is_option=True),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("do.run", "project.show"),
        exit_codes=(0, 1, 2, 4),
    ),
)
