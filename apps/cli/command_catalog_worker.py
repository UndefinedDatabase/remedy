"""The `worker` group's entries of the command catalog (F158, DECISION F158 D6).

Moved unchanged out of `apps/cli/command_catalog.py`, whose `_BASE_CATALOG` splices
`WORKER_COMMANDS` in at the group's own place, so the help keeps its order.
"""

from __future__ import annotations

from apps.cli.command_catalog_types import (
    _JSON_OPT,
    ArgDef,
    CommandEntry,
)

WORKER_COMMANDS: tuple[CommandEntry, ...] = (
    # ── worker ───────────────────────────────────────────────────────────
    CommandEntry(
        command_id="worker.list",
        group_id="worker",
        subcommand="list",
        description="List the worker provider specs available for each role: builder, reviewer, planner or teacher.",
        action_class="read_only",
        args=(_JSON_OPT,),
        supports_json=True,
    ),

    CommandEntry(
        command_id="worker.show",
        group_id="worker",
        subcommand="show",
        description="Show the details of a single worker adapter: the model and the roles (builder, reviewer, planner, teacher) it supports.",
        action_class="read_only",
        args=(ArgDef("provider_id", "Provider ID (e.g. ollama)"), _JSON_OPT),
        supports_json=True,
        related=("worker.list",),
    ),

    CommandEntry(
        command_id="worker.resources",
        group_id="worker",
        subcommand="resources",
        description="Show GPU/VRAM and loaded model resources (best-effort).",
        action_class="read_only",
        args=(_JSON_OPT,),
        supports_json=True,
        related=("worker.unload",),
    ),
    CommandEntry(
        command_id="worker.unload",
        group_id="worker",
        subcommand="unload",
        description="Unload local models from VRAM (Ollama).",
        action_class="write_metadata",
        args=(
            ArgDef("--provider", "Provider to unload (default: ollama)", required=False, is_option=True, default="ollama"),
            ArgDef("--model", "Specific model to unload", required=False, is_option=True),
            ArgDef("--all", "Unload all loaded models", required=False, is_option=True),
            _JSON_OPT,
        ),
        supports_json=True,
        related=("worker.resources",),
    ),
    CommandEntry(
        command_id="worker.doctor",
        group_id="worker",
        subcommand="doctor",
        description="Read-only: is each available worker provider's own tooling actually reachable for the roles (builder, reviewer, planner, teacher) it supports?",
        action_class="read_only",
        args=(_JSON_OPT,),
        supports_json=True,
        related=("worker.list", "worker.resources"),
    ),
)
