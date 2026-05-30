"""CLI handler for ``remedy ui`` — localhost UI server."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    import argparse


def _cmd_ui(
    job_id_str: str,
    *,
    port: int = 8787,
    host: str = "127.0.0.1",
    open_browser: bool = False,
    info_file: str | None = None,
) -> None:
    from packages.orchestration.ui_server import start_ui_server

    start_ui_server(
        job_id_str,
        host=host,
        port=port,
        open_browser=open_browser,
        info_file=info_file,
    )


COMMAND_HANDLERS: dict[str, Callable[["argparse.Namespace"], None]] = {
    "ui.start": lambda args: _cmd_ui(
        args.job_id,
        port=int(getattr(args, "port", None) or 8787),
        host=getattr(args, "host", None) or "127.0.0.1",
        open_browser=str(getattr(args, "open", "false")).lower() == "true",
        info_file=getattr(args, "info_file", None) or None,
    ),
}
