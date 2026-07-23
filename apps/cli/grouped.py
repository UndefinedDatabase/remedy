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
    from apps.cli.commands import collect_all_handlers
    return collect_all_handlers()


# ---------------------------------------------------------------------------
# Parser construction
# ---------------------------------------------------------------------------


def _stream_group(parser: argparse.ArgumentParser):
    """F15: the ONE mutually-exclusive group carrying ``--stream-evidence`` /
    ``--no-stream-evidence`` for this parser, so supplying BOTH is a usage error (exit 2)
    instead of silent last-one-wins."""
    grp = getattr(parser, "_remedy_stream_group", None)
    if grp is None:
        grp = parser.add_mutually_exclusive_group()
        parser._remedy_stream_group = grp
    return grp


def _add_command_args(parser: argparse.ArgumentParser, cmd: CommandEntry) -> None:
    """Add arguments from catalog entry to argparse parser."""
    for arg in cmd.args:
        if arg.is_option:
            # A declared boolean flag wins over every name-based rule below: the catalog
            # entry, not the spelling of the option, decides whether it takes a value.
            if arg.is_flag:
                parser.add_argument(arg.name, action="store_true",
                                    dest=arg.name.lstrip("-").replace("-", "_"),
                                    help=arg.help)
            elif arg.name == "--json":
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
            elif arg.name == "--job":
                parser.add_argument("--job", default=None, help=arg.help)
            elif arg.name == "--tags":
                parser.add_argument("--tags", default=None, help=arg.help)
            elif arg.name == "--keyword":
                parser.add_argument("--keyword", default=None, help=arg.help)
            elif arg.name == "--approved":
                parser.add_argument("--approved", action="store_true", help=arg.help)
            elif arg.name == "--approve":
                parser.add_argument("--approve", action="store_true", dest="approve", help=arg.help)
            elif arg.name == "--max-cycles":
                parser.add_argument("--max-cycles", default="3", dest="max_cycles", help=arg.help)
            elif arg.name == "--auto-approve-low-risk":
                parser.add_argument("--auto-approve-low-risk", action="store_true", dest="auto_approve_low_risk", help=arg.help)
            elif arg.name == "--no-tests":
                parser.add_argument("--no-tests", action="store_true", dest="no_tests", help=arg.help)
            elif arg.name == "--autonomy-level":
                parser.add_argument("--autonomy-level", default="1", dest="autonomy_level", help=arg.help)
            elif arg.name == "--path":
                parser.add_argument("--path", default=None, help=arg.help)
            elif arg.name == "--type":
                parser.add_argument("--type", default=None, dest="type", help=arg.help)
            elif arg.name == "--since":
                parser.add_argument("--since", default=None, help=arg.help)
            elif arg.name == "--port":
                parser.add_argument("--port", default=arg.default, help=arg.help)
            elif arg.name == "--host":
                parser.add_argument("--host", default=arg.default, help=arg.help)
            elif arg.name == "--no-open":
                parser.add_argument("--no-open", action="store_true", dest="no_open", help=arg.help)
            elif arg.name == "--info-file":
                parser.add_argument("--info-file", default=None, dest="info_file", help=arg.help)
            elif arg.name == "--out":
                parser.add_argument("--out", default=None, help=arg.help)
            elif arg.name == "--repo":
                parser.add_argument("--repo", default=arg.default, help=arg.help)
            elif arg.name == "--dry-run":
                parser.add_argument("--dry-run", action="store_true", dest="dry_run", help=arg.help)
            elif arg.name == "--fixture-builder":
                parser.add_argument("--fixture-builder", nargs="?", const="true", default="false", dest="fixture_builder", help=arg.help)
            elif arg.name == "--ui":
                parser.add_argument("--ui", action="store_true", dest="ui", help=arg.help)
            elif arg.name == "--fixture-reviewer":
                parser.add_argument("--fixture-reviewer", action="store_true", dest="fixture_reviewer", help=arg.help)
            elif arg.name == "--fixture-demo":
                parser.add_argument("--fixture-demo", action="store_true", dest="fixture_demo", help=arg.help)
            elif arg.name == "--after-task":
                parser.add_argument("--after-task", default=None, dest="after_task", help=arg.help)
            elif arg.name == "--provider":
                parser.add_argument("--provider", default=arg.default, help=arg.help)
            elif arg.name == "--model":
                parser.add_argument("--model", default=None, help=arg.help)
            elif arg.name == "--once":
                parser.add_argument("--once", action="store_true", dest="once", help=arg.help)
            elif arg.name == "--max-jobs":
                parser.add_argument("--max-jobs", default=arg.default, dest="max_jobs", help=arg.help)
            elif arg.name == "--max-seconds":
                parser.add_argument("--max-seconds", default=arg.default, dest="max_seconds", help=arg.help)
            elif arg.name == "--max-steps":
                parser.add_argument("--max-steps", default=arg.default, dest="max_steps", help=arg.help)
            elif arg.name == "--max-tokens":
                parser.add_argument("--max-tokens", default=arg.default, dest="max_tokens", help=arg.help)
            elif arg.name == "--max-runtime-seconds":
                parser.add_argument("--max-runtime-seconds", default=arg.default, dest="max_runtime_seconds", help=arg.help)
            elif arg.name == "--max-wall-minutes":
                parser.add_argument("--max-wall-minutes", default=arg.default, dest="max_wall_minutes", help=arg.help)
            elif arg.name == "--builder-provider":
                parser.add_argument("--builder-provider", default=arg.default, dest="builder_provider", help=arg.help)
            elif arg.name == "--builder-model":
                parser.add_argument("--builder-model", dest="builder_model", default=arg.default, help=arg.help)
            elif arg.name == "--builder-effort":
                parser.add_argument("--builder-effort", dest="builder_effort", default=arg.default, help=arg.help)
            elif arg.name == "--reviewer-provider":
                parser.add_argument("--reviewer-provider", dest="reviewer_provider", default=arg.default, help=arg.help)
            elif arg.name == "--reviewer-model":
                parser.add_argument("--reviewer-model", dest="reviewer_model", default=arg.default, help=arg.help)
            elif arg.name == "--reviewer-effort":
                parser.add_argument("--reviewer-effort", dest="reviewer_effort", default=arg.default, help=arg.help)
            elif arg.name == "--repair-provider":
                parser.add_argument("--repair-provider", dest="repair_provider", default=arg.default, help=arg.help)
            elif arg.name == "--repair-model":
                parser.add_argument("--repair-model", dest="repair_model", default=arg.default, help=arg.help)
            elif arg.name == "--repair-effort":
                parser.add_argument("--repair-effort", dest="repair_effort", default=arg.default, help=arg.help)
            elif arg.name == "--all":
                parser.add_argument("--all", action="store_true", dest="all", help=arg.help)
            elif arg.name == "--no-ui":
                parser.add_argument("--no-ui", action="store_true", dest="no_ui", help=arg.help)
            elif arg.name == "--agent":
                parser.add_argument("--agent", action="store_true", dest="agent", help=arg.help)
            elif arg.name == "--output":
                parser.add_argument("--output", default=None, help=arg.help)
            elif arg.name == "--fixture-patch-intent":
                parser.add_argument("--fixture-patch-intent", nargs="?", const="true", default="false", dest="fixture_patch_intent", help=arg.help)
            elif arg.name == "--collect-only":
                parser.add_argument("--collect-only", action="store_true", dest="collect_only", help=arg.help)
            elif arg.name == "--intent-id":
                parser.add_argument("--intent-id", default=None, dest="intent_id", help=arg.help)
            elif arg.name == "--note":
                parser.add_argument("--note", default=arg.default, dest="note", help=arg.help)
            elif arg.name == "--yes":
                parser.add_argument("--yes", action="store_true", dest="yes", help=arg.help)
            elif arg.name == "--task-scoped":
                parser.add_argument("--task-scoped", action="store_true", dest="task_scoped", help=arg.help)
            elif arg.name == "--allowed-files":
                parser.add_argument("--allowed-files", default=None, dest="allowed_files", help=arg.help)
            elif arg.name == "--expected-files":
                parser.add_argument("--expected-files", default=None, dest="expected_files", help=arg.help)
            elif arg.name == "--linked-prior-job-id":
                parser.add_argument("--linked-prior-job-id", default=None, dest="linked_prior_job_id", help=arg.help)
            elif arg.name == "--verification-command":
                parser.add_argument("--verification-command", action="append", default=None, dest="verification_command", help=arg.help)
            elif arg.name == "--fixture-source-builder":
                parser.add_argument("--fixture-source-builder", nargs="?", const="true",
                                    default="false", dest="fixture_source_builder", help=arg.help)
            elif arg.name == "--markdown":
                parser.add_argument("--markdown", action="store_true", dest="markdown", help=arg.help)
            elif arg.name == "--allow-one-cycle":
                parser.add_argument("--allow-one-cycle", action="store_true", dest="allow_one_cycle", help=arg.help)
            elif arg.name == "--allow-apply":
                parser.add_argument("--allow-apply", action="store_true", dest="allow_apply", help=arg.help)
            elif arg.name == "--allow-repair-propose":
                parser.add_argument("--allow-repair-propose", action="store_true", dest="allow_repair_propose", help=arg.help)
            elif arg.name == "--allow-repair-apply":
                parser.add_argument("--allow-repair-apply", action="store_true", dest="allow_repair_apply", help=arg.help)
            elif arg.name == "--input":
                parser.add_argument("--input", default=None, dest="input", help=arg.help)
            elif arg.name == "--stdin":
                parser.add_argument("--stdin", action="store_true", dest="stdin", help=arg.help)
            elif arg.name == "--failure-artifact-id":
                parser.add_argument("--failure-artifact-id", default=None, dest="failure_artifact_id", help=arg.help)
            elif arg.name == "--target":
                parser.add_argument("--target", default=arg.default, dest="target", help=arg.help)
            elif arg.name == "--new":
                parser.add_argument("--new", action="store_true", dest="new", help=arg.help)
            elif arg.name == "--job-id":
                parser.add_argument("--job-id", default=None, dest="job_id", help=arg.help)
            elif arg.name == "--item-id":
                parser.add_argument("--item-id", default=None, dest="item_id", help=arg.help)
            elif arg.name == "--top":
                parser.add_argument("--top", default=None, dest="top", help=arg.help)
            elif arg.name == "--attempt-id":
                parser.add_argument("--attempt-id", default=None, dest="attempt_id", help=arg.help)
            elif arg.name == "--use-local-advisor":
                parser.add_argument("--use-local-advisor", action="store_true", dest="use_local_advisor", help=arg.help)
            elif arg.name == "--keep-staging":
                parser.add_argument("--keep-staging", action="store_true", dest="keep_staging", help=arg.help)
            elif arg.name == "--builder":
                parser.add_argument("--builder", default=arg.default, help=arg.help)
            elif arg.name == "--reviewer":
                parser.add_argument("--reviewer", default=arg.default, help=arg.help)
            elif arg.name == "--max-rounds":
                parser.add_argument("--max-rounds", default=arg.default, dest="max_rounds", help=arg.help)
            elif arg.name == "--mode":
                parser.add_argument("--mode", default=arg.default, help=arg.help)
            elif arg.name == "--test-command":
                parser.add_argument("--test-command", default=arg.default, dest="test_command", help=arg.help)
            elif arg.name == "--provider-timeout-sec":
                parser.add_argument("--provider-timeout-sec", default=arg.default, dest="provider_timeout_sec", help=arg.help)
            elif arg.name == "--timeout-sec":
                # F1: omission stays None so run_job resolves explicit>persisted>default.
                parser.add_argument("--timeout-sec", default=None, dest="timeout_sec", help=arg.help)
            elif arg.name == "--timeout-profile":
                # F1: omission stays None — never pre-resolved to "normal".
                parser.add_argument("--timeout-profile", default=None, dest="timeout_profile", help=arg.help)
            elif arg.name == "--max-output-chars":
                parser.add_argument("--max-output-chars", default=None, dest="max_output_chars", help=arg.help)
            elif arg.name == "--max-tasks":
                # F1: omission stays None (not "0"), so a persisted cap is not silently cleared.
                parser.add_argument("--max-tasks", default=None, dest="max_tasks", help=arg.help)
            elif arg.name == "--claude-cli-write-mode":
                parser.add_argument("--claude-cli-write-mode", default=arg.default, dest="claude_cli_write_mode", help=arg.help)
            elif arg.name == "--stream-evidence":
                # F1/F15: tri-state AND mutually exclusive — omitted None, --stream-evidence
                # True, --no-stream-evidence False, BOTH is a usage error (exit 2). The pair
                # shares one argparse mutually-exclusive group per command parser.
                _stream_group(parser).add_argument(
                    "--stream-evidence", action="store_const", const=True,
                    default=None, dest="stream_evidence", help=arg.help)
            elif arg.name == "--no-stream-evidence":
                _stream_group(parser).add_argument(
                    "--no-stream-evidence", action="store_const", const=False,
                    dest="stream_evidence", help=arg.help)
            elif arg.name == "--task-file":
                parser.add_argument("--task-file", default="", dest="task_file", help=arg.help)
            elif arg.name == "--task-stdin":
                parser.add_argument("--task-stdin", action="store_true", dest="task_stdin", help=arg.help)
            elif arg.name == "--scope-file":
                parser.add_argument("--scope-file", default="", dest="scope_file", help=arg.help)
            elif arg.name == "--approve-scope":
                parser.add_argument("--approve-scope", action="store_true", dest="approve_scope", help=arg.help)
            elif arg.name == "--repair-rounds":
                parser.add_argument("--repair-rounds", type=int, default=None, dest="repair_rounds", help=arg.help)
            elif arg.name == "--user-requested":
                parser.add_argument("--user-requested", action="store_true", dest="user_requested", help=arg.help)
            elif arg.name == "--prefer-local-for-cheap-tasks":
                parser.add_argument("--prefer-local-for-cheap-tasks", action="store_true",
                                    dest="prefer_local_for_cheap_tasks", help=arg.help)
            elif arg.name == "--prefer-ollama-for-cheap-tasks":
                parser.add_argument("--prefer-ollama-for-cheap-tasks", action="store_true",
                                    dest="prefer_ollama_for_cheap_tasks", help=arg.help)
            elif arg.name == "--require-human-approval-for-expensive":
                parser.add_argument("--require-human-approval-for-expensive", action="store_true",
                                    dest="require_human_approval_for_expensive", help=arg.help)
            # F011 kill switch
            elif arg.name == "--source":
                parser.add_argument("--source", default=arg.default, help=arg.help)
            else:
                parser.add_argument(arg.name, default=arg.default, help=arg.help)
        else:
            if not arg.required:
                parser.add_argument(arg.name, nargs="?", default=arg.default, help=arg.help)
            else:
                parser.add_argument(arg.name, help=arg.help)


class _UsageError(SystemExit):
    """F15: a usage error that CARRIES its message, so the conflict can be explained instead of
    exiting silently (e.g. `--stream-evidence` together with `--no-stream-evidence`)."""

    def __init__(self, message: str) -> None:
        super().__init__(2)
        self.message = message


class _SilentParser(argparse.ArgumentParser):
    """ArgumentParser that raises SystemExit without printing to stderr — but keeps the message
    so the caller can render it (F15)."""

    def error(self, message: str) -> None:  # type: ignore[override]
        raise _UsageError(message)

    def exit(self, status: int = 0, message: str | None = None) -> None:  # type: ignore[override]
        raise SystemExit(status)


_DEFAULT_COMMAND: dict[str, str] = {"ui": "start", "do": "run", "init": "run"}
_ALWAYS_INJECT: set[str] = {"init"}


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

_QUICK_START = """\
 Quick start:
   1. remedy do run "<goal>" --repo . --builder claude-cli --reviewer claude-cli --json | tee /tmp/remedy-run.json
   2. RUN_ID=$(python3 -c "import json; print(json.load(open('/tmp/remedy-run.json'))['run_id'])")
   3. remedy do report $RUN_ID --json
   4. remedy do promote $RUN_ID --repo . --dry-run --json
   5. remedy do promote $RUN_ID --repo . --approve

 Show all commands:  remedy --all-commands"""


def _print_root_help(*, show_all: bool = False) -> None:
    """Print Bootcamp-style root help and exit 0."""
    if show_all:
        groups = [(gid, gdef.description) for gid, gdef in GROUPS.items()]
        title = "All Commands"
    else:
        groups = [
            (gid, gdef.description)
            for gid, gdef in GROUPS.items()
            if gdef.user_facing
        ]
        title = "Commands"
    print(render_root_help(
        "remedy", "Remedy \u2014 Human-in-the-loop Project Brain", groups,
        footer=_QUICK_START,
        commands_title=title,
    ))


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
    """Pre-scan argv for --help/--all-commands before argparse touches it.

    Returns True if help was printed (caller should return).
    This avoids argparse's SystemExit on missing required args when --help is present.
    """
    raw = argv if argv is not None else sys.argv[1:]
    has_help = "-h" in raw or "--help" in raw
    has_all = "--all-commands" in raw

    if not has_help and not has_all:
        return False

    # --all-commands alone or with --help
    if has_all:
        _print_root_help(show_all=True)
        return True

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


def _wants_json(raw: list[str]) -> bool:
    return "--json" in (raw or [])


def main(argv: list[str] | None = None) -> None:
    """Entry point for the grouped CLI."""
    # Pre-scan for --help to avoid argparse SystemExit on missing required args
    if _pre_scan_help(argv):
        return

    parser = build_parser()

    raw = argv if argv is not None else sys.argv[1:]
    if raw and raw[0] in _DEFAULT_COMMAND:
        subcmds = {c.subcommand for c in get_commands_for_group(raw[0])}
        has_subcmd = len(raw) >= 2 and raw[1] in subcmds
        if not has_subcmd and (
            raw[0] in _ALWAYS_INJECT
            or (len(raw) >= 2 and not raw[1].startswith("-"))
        ):
            default_sub = _DEFAULT_COMMAND[raw[0]]
            raw = [raw[0], default_sub] + raw[1:]
            argv = raw

    # Intercept argparse errors for clean output
    try:
        args, unknown = parser.parse_known_args(argv)
    except SystemExit as exc:
        raw = argv if argv is not None else sys.argv[1:]
        # F15: a conflicting/invalid option combination EXPLAINS itself (both stream flags →
        # exit 2 with the reason), instead of silently falling through to generic help.
        msg = getattr(exc, "message", "")
        if msg and ("not allowed with" in msg or "mutually exclusive" in msg):
            where = f"remedy {raw[0]} {raw[1]}" if len(raw) >= 2 else "remedy"
            if _wants_json(raw):
                import json as _json
                print(_json.dumps({"ok": False, "error": "conflicting_options",
                                   "message": msg}, indent=2))
            else:
                print(render_error(where, msg), file=sys.stderr)
            sys.exit(2)
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

    # --all-commands handled by pre-scan, but catch edge cases
    if getattr(args, "_group", None) == "--all-commands":
        _print_root_help(show_all=True)
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
        print("Error: unknown command", file=sys.stderr)
        sys.exit(1)

    dispatch = _get_dispatch_table()
    handler = dispatch.get(command_id)
    if handler is None:
        print(f"Error: no handler for {command_id}", file=sys.stderr)
        sys.exit(1)

    handler(args)


if __name__ == "__main__":
    main()
