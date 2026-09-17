"""
Bootcamp-style CLI help renderer using Unicode box drawing.

Produces output visually close to Typer/Rich without adding dependencies.
Deterministic — no terminal probing, fixed width (78 inner).
"""

from __future__ import annotations

import textwrap

BOX_WIDTH = 78  # inner width (between vertical bars)


def _box(title: str, rows: list[tuple[str, str]]) -> str:
    """Render a titled box with aligned two-column rows."""
    lines: list[str] = []
    lines.append(f"\u256d\u2500 {title} " + "\u2500" * (BOX_WIDTH - len(title) - 3) + "\u256e")

    if not rows:
        lines.append("\u2502" + " " * BOX_WIDTH + "\u2502")
    else:
        max_left = max(len(r[0]) for r in rows)
        prefix_width = 2 + max_left + 2
        wrap_width = max(BOX_WIDTH - prefix_width, 1)
        for left, right in rows:
            pad = " " * (max_left - len(left))
            prefix = f"  {left}{pad}  "
            wrapped = textwrap.wrap(right, width=wrap_width) or [""]
            lines.append(f"\u2502{(prefix + wrapped[0]).ljust(BOX_WIDTH)}\u2502")
            for cont in wrapped[1:]:
                lines.append(f"\u2502{(' ' * prefix_width + cont).ljust(BOX_WIDTH)}\u2502")

    lines.append("\u2570" + "\u2500" * BOX_WIDTH + "\u256f")
    return "\n".join(lines)


def render_root_help(
    prog: str,
    description: str,
    groups: list[tuple[str, str]],
    *,
    footer: str = "",
    commands_title: str = "Commands",
) -> str:
    """Render top-level help: usage, description, options box, commands box."""
    parts: list[str] = []
    parts.append(f" Usage: {prog} [OPTIONS] COMMAND [ARGS]...\n")
    parts.append(f" {description}\n")
    parts.append(_box("Options", [
        ("--help", "Show this message and exit."),
        ("--all-commands", "Show all commands (including advanced)."),
    ]))
    parts.append("")
    parts.append(_box(commands_title, groups))
    parts.append("")
    if footer:
        parts.append(footer)
        parts.append("")
    return "\n".join(parts)


def render_group_help(
    prog: str,
    group_name: str,
    description: str,
    commands: list[tuple[str, str]],
    *,
    also: tuple[str, ...] = (),
) -> str:
    """Render group-level help: usage, description, the group's other words, options box,
    commands box."""
    parts: list[str] = []
    parts.append(f" Usage: {prog} {group_name} [OPTIONS] COMMAND [ARGS]...\n")
    parts.append(f" {description}\n")
    if also:
        parts.append(" Also reachable as: " + ", ".join(f"{prog} {word}" for word in also) + "\n")
    parts.append(_box("Options", [("--help", "Show this message and exit.")]))
    parts.append("")
    parts.append(_box("Commands", commands))
    parts.append("")
    parts.append(f" Run '{prog} {group_name} <command> --help' for details.")
    parts.append("")
    return "\n".join(parts)


def render_command_help(
    prog: str,
    group_name: str,
    command_name: str,
    description: str,
    positionals: list[tuple[str, str]],
    options: list[tuple[str, str]],
) -> str:
    """Render command-level help: usage, description, arguments box, options box."""
    # Build usage line with arg names
    usage_args = " ".join(name.upper() for name, _ in positionals)
    opt_hint = " [OPTIONS]" if options else ""
    usage = f" Usage: {prog} {group_name} {command_name}{opt_hint}"
    if usage_args:
        usage += f" {usage_args}"
    usage += "\n"

    parts: list[str] = []
    parts.append(usage)
    parts.append(f" {description}\n")

    if positionals:
        parts.append(_box("Arguments", positionals))
        parts.append("")

    all_opts = list(options) + [("--help", "Show this message and exit.")]
    parts.append(_box("Options", all_opts))
    parts.append("")
    return "\n".join(parts)


def render_error(prog: str, message: str) -> str:
    """Render a clean error message without traceback."""
    return f" Usage: {prog} [OPTIONS] COMMAND [ARGS]...\n\n Error: {message}\n"
