"""Worker group command handlers."""

from __future__ import annotations

import json as _json
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    import argparse


def _cmd_workers(*, json_output: bool = False) -> None:
    from packages.orchestration.worker_adapters import (
        export_worker_specs_json, list_worker_specs, summarize_worker_specs,
    )

    specs = list_worker_specs()
    if json_output:
        print(_json.dumps(export_worker_specs_json(specs), sort_keys=True))
    else:
        print(summarize_worker_specs(specs))


COMMAND_HANDLERS: dict[str, Callable[["argparse.Namespace"], None]] = {
    "worker.list": lambda args: _cmd_workers(json_output=args.json),
}
