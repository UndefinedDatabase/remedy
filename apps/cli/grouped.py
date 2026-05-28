"""
Group-first CLI entry point for Remedy.

Builds an argparse tree from the command catalog and dispatches to
existing handler functions in apps.cli.main.

Usage::

    python -m apps.cli.grouped job create "Build a README"
    python -m apps.cli.grouped brain graph <job_id> --json
    python -m apps.cli.grouped worker list --json

Typing a group name alone shows group help::

    python -m apps.cli.grouped job
    python -m apps.cli.grouped brain
"""

from __future__ import annotations

import argparse
import sys

from apps.cli.command_catalog import (
    CATALOG,
    GROUPS,
    CommandEntry,
    get_commands_for_group,
)
from apps.cli.help_renderer import (
    render_command_help,
    render_error,
    render_group_help,
    render_root_help,
)


# ---------------------------------------------------------------------------
# Dispatch table: catalog command_id -> handler callable
# ---------------------------------------------------------------------------


def _get_dispatch_table() -> dict[str, object]:
    """Lazy import to avoid circular imports and loading all handlers at startup."""
    from apps.cli.main import (
        _cmd_agent_loop,
        _cmd_apply_patch_intent,
        _cmd_approve_patch_intent,
        _cmd_attach_project_job,
        _cmd_attach_project_repo,
        _cmd_attach_repo,
        _cmd_brain,
        _cmd_brain_node,
        _cmd_brain_view,
        _cmd_cockpit,
        _cmd_constitution,
        _cmd_context,
        _cmd_create_job,
        _cmd_create_project,
        _cmd_discover_commands,
        _cmd_list_jobs,
        _cmd_list_patch_intents,
        _cmd_list_projects,
        _cmd_plan_job_local,
        _cmd_reject_patch_intent,
        _cmd_run_contract,
        _cmd_run_next_task_local,
        _cmd_run_tests_local,
        _cmd_set_permission,
        _cmd_show_job,
        _cmd_show_patch_intent,
        _cmd_show_permissions,
        _cmd_show_project,
        _cmd_project_context,
        _cmd_timeline,
        _cmd_token_policy,
        _cmd_trust_report,
        _cmd_workers,
    )

    return {
        # job
        "job.create": lambda args: _cmd_create_job(
            args.prompt,
            project_id=getattr(args, "project", None),
            task_type=getattr(args, "task_type", None),
            task_description=getattr(args, "task_description", None),
        ),
        "job.list": lambda args: _cmd_list_jobs(),
        "job.show": lambda args: _cmd_show_job(args.job_id),
        "job.attach-repo": lambda args: _cmd_attach_repo(args.job_id, args.repo_path),
        "job.permit": lambda args: _cmd_set_permission(args.job_id, args.action, args.permission),
        "job.permissions": lambda args: _cmd_show_permissions(args.job_id),
        "job.run-next": lambda args: _cmd_run_next_task_local(args.job_id),
        "job.plan": lambda args: _cmd_plan_job_local(args.job_id),

        # project
        "project.create": lambda args: _cmd_create_project(
            args.name, getattr(args, "description", None),
        ),
        "project.list": lambda args: _cmd_list_projects(),
        "project.show": lambda args: _cmd_show_project(args.project_id, json_output=args.json),
        "project.attach-repo": lambda args: _cmd_attach_project_repo(args.project_id, args.repo_path),
        "project.attach-job": lambda args: _cmd_attach_project_job(args.project_id, args.job_id),
        "project.context": lambda args: _cmd_project_context(args.project_id, json_output=args.json),

        # patch
        "patch.list": lambda args: _cmd_list_patch_intents(args.job_id),
        "patch.show": lambda args: _cmd_show_patch_intent(args.job_id, args.intent_id),
        "patch.approve": lambda args: _cmd_approve_patch_intent(
            args.job_id, args.intent_id, getattr(args, "reason", None),
        ),
        "patch.reject": lambda args: _cmd_reject_patch_intent(
            args.job_id, args.intent_id, getattr(args, "reason", None),
        ),
        "patch.apply": lambda args: _cmd_apply_patch_intent(
            args.job_id, args.intent_id, json_output=False,
        ),

        # test
        "test.discover": lambda args: _cmd_discover_commands(args.job_id, as_json=args.json),
        "test.run": lambda args: _cmd_run_tests_local(args.job_id),

        # brain
        "brain.graph": lambda args: _cmd_brain(args.job_id, json_output=args.json),
        "brain.node": lambda args: _cmd_brain_node(args.job_id, args.node_id, json_output=args.json),
        "brain.view": lambda args: _cmd_brain_view(args.job_id),
        "brain.context": lambda args: _cmd_context(args.job_id, json_output=args.json),
        "brain.trust": lambda args: _cmd_trust_report(args.job_id),
        "brain.timeline": lambda args: _cmd_timeline(args.job_id),
        "brain.cockpit": lambda args: _cmd_cockpit(args.job_id),
        "brain.constitution": lambda args: _cmd_constitution(args.job_id),

        # policy
        "policy.contract": lambda args: _cmd_run_contract(args.job_id, json_output=args.json),
        "policy.token": lambda args: _cmd_token_policy(args.job_id, json_output=args.json),

        # worker
        "worker.list": lambda args: _cmd_workers(json_output=args.json),

        # dev
        "dev.agent-loop": lambda args: _cmd_agent_loop(args.job_id),
        "dev.smoke-help": lambda args: _dev_smoke_help(),
    }


def _dev_smoke_help() -> None:
    """Print smoke test instructions."""
    print("Smoke test:")
    print("  source scripts/remedy_smoke.sh && remedy_smoke")
    print("")
    print("Or run directly:")
    print("  bash scripts/remedy_smoke.sh")


# ---------------------------------------------------------------------------
# Parser construction
# ---------------------------------------------------------------------------


def _add_command_args(parser: argparse.ArgumentParser, cmd: CommandEntry) -> None:
    """Add arguments from catalog entry to argparse parser."""
    for arg in cmd.args:
        if arg.is_option:
            if arg.name == "--json":
                parser.add_argument("--json", action="store_true", dest="json", help=arg.help)
            elif arg.name == "--reason":
                parser.add_argument("--reason", default=None, help=arg.help)
            elif arg.name == "--project":
                parser.add_argument("--project", default=None, help=arg.help)
            elif arg.name == "--task-type":
                parser.add_argument("--task-type", default=None, dest="task_type", help=arg.help)
            elif arg.name == "--task-description":
                parser.add_argument("--task-description", default=None, dest="task_description", help=arg.help)
            elif arg.name == "--description":
                parser.add_argument("--description", default=None, help=arg.help)
            else:
                parser.add_argument(arg.name, default=arg.default, help=arg.help)
        else:
            parser.add_argument(arg.name, help=arg.help)


class _SilentParser(argparse.ArgumentParser):
    """ArgumentParser that raises SystemExit without printing to stderr."""

    def error(self, message: str) -> None:  # type: ignore[override]
        raise SystemExit(2)

    def exit(self, status: int = 0, message: str | None = None) -> None:  # type: ignore[override]
        raise SystemExit(status)


def build_parser() -> argparse.ArgumentParser:
    """Build the full grouped CLI argument parser from the catalog."""
    root = _SilentParser(
        prog="remedy",
        description="Remedy — Human-in-the-loop Project Brain",
        add_help=False,
    )
    root.add_argument("-h", "--help", action="store_true", dest="_help", default=False)
    root.set_defaults(func=None, _group=None, _subcmd=None)

    group_parsers = root.add_subparsers(dest="_group", parser_class=_SilentParser)

    for group_id, group_def in GROUPS.items():
        group_parser = group_parsers.add_parser(
            group_id,
            help=group_def.description,
            add_help=False,
        )
        group_parser.add_argument("-h", "--help", action="store_true", dest="_help", default=False)
        sub = group_parser.add_subparsers(dest="_subcmd", parser_class=_SilentParser)

        for cmd in get_commands_for_group(group_id):
            cmd_parser = sub.add_parser(
                cmd.subcommand,
                help=cmd.description,
                add_help=False,
                description=cmd.description,
            )
            cmd_parser.add_argument("-h", "--help", action="store_true", dest="_help", default=False)
            _add_command_args(cmd_parser, cmd)
            cmd_parser.set_defaults(_command_id=cmd.command_id)

    return root


# ---------------------------------------------------------------------------
# Help rendering from catalog
# ---------------------------------------------------------------------------

def _print_root_help() -> None:
    """Print Bootcamp-style root help and exit 0."""
    groups = [(gid, gdef.description) for gid, gdef in GROUPS.items()]
    print(render_root_help("remedy", "Remedy \u2014 Human-in-the-loop Project Brain", groups))


def _print_group_help(group_id: str) -> None:
    """Print Bootcamp-style group help and exit 0."""
    group_def = GROUPS[group_id]
    cmds = get_commands_for_group(group_id)
    commands = [(c.subcommand, c.description) for c in cmds]
    print(render_group_help("remedy", group_id, group_def.description, commands))


def _print_command_help(group_id: str, cmd: CommandEntry) -> None:
    """Print Bootcamp-style command help and exit 0."""
    positionals = [(a.name, a.help) for a in cmd.args if not a.is_option]
    options = [(a.name, a.help) for a in cmd.args if a.is_option]
    print(render_command_help("remedy", group_id, cmd.subcommand, cmd.description, positionals, options))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def _pre_scan_help(argv: list[str] | None) -> bool:
    """Pre-scan argv for --help before argparse touches it.

    Returns True if help was printed (caller should return).
    This avoids argparse's SystemExit on missing required args when --help is present.
    """
    raw = argv if argv is not None else sys.argv[1:]
    has_help = "-h" in raw or "--help" in raw

    if not has_help:
        return False

    # Strip -h/--help for position analysis
    tokens = [t for t in raw if t not in ("-h", "--help")]

    if not tokens:
        _print_root_help()
        return True

    group_id = tokens[0]
    if group_id not in GROUPS:
        _print_root_help()
        return True

    if len(tokens) < 2:
        _print_group_help(group_id)
        return True

    subcmd = tokens[1]
    cmds = get_commands_for_group(group_id)
    cmd = next((c for c in cmds if c.subcommand == subcmd), None)
    if cmd is None:
        _print_group_help(group_id)
        return True

    _print_command_help(group_id, cmd)
    return True


def main(argv: list[str] | None = None) -> None:
    """Entry point for the grouped CLI."""
    # Pre-scan for --help to avoid argparse SystemExit on missing required args
    if _pre_scan_help(argv):
        return

    parser = build_parser()

    # Intercept argparse errors for clean output
    try:
        args, unknown = parser.parse_known_args(argv)
    except SystemExit:
        raw = argv if argv is not None else sys.argv[1:]
        if not raw:
            _print_root_help()
            return
        if raw[0] not in GROUPS:
            print(render_error("remedy", f"Unknown command '{raw[0]}'."), file=sys.stderr)
            sys.exit(2)
        if len(raw) >= 2:
            subcmds = {c.subcommand for c in get_commands_for_group(raw[0])}
            if raw[1] not in subcmds and not raw[1].startswith("-"):
                print(render_error(f"remedy {raw[0]}", f"Unknown command '{raw[1]}'."), file=sys.stderr)
                sys.exit(2)
            # Missing required args for a valid command — show command help
            if raw[1] in subcmds:
                cmd = next(c for c in get_commands_for_group(raw[0]) if c.subcommand == raw[1])
                _print_command_help(raw[0], cmd)
                sys.exit(2)
        _print_group_help(raw[0])
        return

    # No group specified -> show top-level help
    if args._group is None:
        _print_root_help()
        return

    # Group specified but no subcommand -> show group help
    if args._subcmd is None:
        _print_group_help(args._group)
        return

    # Handle unknown args after successful parse
    if unknown:
        print(render_error(f"remedy {args._group} {args._subcmd}", f"Unrecognized arguments: {' '.join(unknown)}"), file=sys.stderr)
        sys.exit(2)

    command_id = getattr(args, "_command_id", None)
    if command_id is None:
        print(f"Error: unknown command", file=sys.stderr)
        sys.exit(1)

    dispatch = _get_dispatch_table()
    handler = dispatch.get(command_id)
    if handler is None:
        print(f"Error: no handler for {command_id}", file=sys.stderr)
        sys.exit(1)

    handler(args)


if __name__ == "__main__":
    main()
