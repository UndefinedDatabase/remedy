"""Operator amendment amend1014-do-golden-path-now D3 — whether `remedy do` may ask a person about a plan.

Remedy deliberately keeps this decision in the CLI and out of `packages/`: reading a terminal
(`input`, `isatty`) is the CLI's act, and the packages stay free of interactive constructs
(tests/test_no_interactive_guard.py). A walk asks only when both stdin and stderr are a terminal.
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from typing import Any


def interactive_plan_confirmer() -> Callable[[Any], bool] | None:
    """The confirmer when a person is at the terminal (stdin and stderr are both a TTY); else None."""
    from packages.orchestration.do_plan_confirm import make_plan_confirmer

    return make_plan_confirmer(ask=input) if sys.stdin.isatty() and sys.stderr.isatty() else None
