"""Repo group command handlers."""

from __future__ import annotations

import json as _json
import sys
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    import argparse


def _cmd_repo_status(
    path: str | None = None,
    *,
    json_output: bool = False,
) -> None:
    from packages.orchestration.git_status import (
        export_git_status_json,
        read_git_status,
        summarize_git_status,
    )

    repo_path = path or "."
    status = read_git_status(repo_path)

    if json_output:
        print(_json.dumps(export_git_status_json(status), sort_keys=True))
    else:
        print(summarize_git_status(status))


COMMAND_HANDLERS: dict[str, Callable[["argparse.Namespace"], None]] = {
    "repo.status": lambda args: _cmd_repo_status(
        getattr(args, "path", None),
        json_output=getattr(args, "json", False),
    ),
}
