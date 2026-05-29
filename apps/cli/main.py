"""
Remedy CLI entrypoint — thin bridge to the grouped CLI.

All command implementations live in apps.cli.commands.*
All CLI parsing and dispatch live in apps.cli.grouped.
This module exists only as the canonical ``python -m apps.cli.main`` entry point.
"""

from __future__ import annotations


def main() -> None:
    """Delegate everything to the grouped CLI entry point."""
    from apps.cli.grouped import main as grouped_main
    grouped_main()


if __name__ == "__main__":
    main()
