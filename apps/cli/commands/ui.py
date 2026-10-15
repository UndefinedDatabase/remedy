"""CLI handler for ``remedy ui``: warning aliases of ``remedy serve start|stop``.

The old React cockpit and its own server were deleted (operator amendment
amend1015-face-migration, DECISION amend1015f D22). Remedy serves no page of its own any more;
its face is the universe's edition, which reads the serve supervisor's public HTTP API.
`remedy ui start` and `remedy ui stop` stay as aliases so old scripts keep working: each prints
one deprecation warning on stderr and then does exactly what `remedy serve start` or
`remedy serve stop` does. A job id given to `ui start` is accepted and ignored, because the
supervisor serves every job of the data root. `ui latest`, `ui status` and `ui open` were removed.
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import argparse


#: The one deprecation sentence each alias prints on stderr before it runs the serve command.
UI_ALIAS_WARNINGS: dict[str, str] = {
    "start": ("warning: `remedy ui start` is deprecated, because the old cockpit was deleted; "
              "it now runs `remedy serve start`. Use `remedy serve start` instead."),
    "stop": ("warning: `remedy ui stop` is deprecated, because the old cockpit was deleted; "
             "it now runs `remedy serve stop`. Use `remedy serve stop` instead."),
}


def _alias(word: str, args: argparse.Namespace) -> None:
    from apps.cli.commands.serve_cmd import COMMAND_HANDLERS as SERVE_HANDLERS

    print(UI_ALIAS_WARNINGS[word], file=sys.stderr)
    sys.stderr.flush()
    SERVE_HANDLERS[f"serve.{word}"](args)


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "ui.start": lambda args: _alias("start", args),
    "ui.stop": lambda args: _alias("stop", args),
}
