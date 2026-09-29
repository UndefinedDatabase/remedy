"""F041 T002 — the runner of the harness's own verbs (DECISION F041 D3).

The one place a runtime verb runs for a preview. A preview never re-implements the
runtime harness: it runs ``remedy runtime serve``, ``remedy runtime probe`` and
``remedy runtime stop`` as a child process and reads back the one JSON envelope each
already answers under ``--json`` (``apps/cli/commands/runtime_cmd.py``), because that
CLI owns the supervisor's whole lifecycle — its lock, its identity checks, its
handshake — and none of that is this feature's to reach into or duplicate.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from packages.orchestration.preview_control import VerbResult

#: The three verbs a preview ever runs, in the order the harness's own CLI names them.
RUNTIME_VERBS = ("serve", "probe", "stop")

#: The bound on one verb's own child process. Long enough for a slow project's install
#: step or first build; short enough that a hung child cannot hold a preview forever.
VERB_TIMEOUT_SECONDS = 180


def runtime_verb_argv(verb: str, root: Path) -> list[str]:
    """The command line that runs ``verb`` against project ``root``."""
    if verb not in RUNTIME_VERBS:
        raise ValueError(f"unknown runtime verb: {verb!r}")
    return [
        sys.executable, "-m", "apps.cli.main", "runtime", verb, "--repo", str(root),
        "--json",
    ]


def run_runtime_verb(verb: str, root: Path) -> VerbResult:
    """Run one of ``remedy runtime serve``, ``probe`` or ``stop`` against ``root``
    (whichever ``verb`` names) and read back its envelope.

    Runs from the Remedy checkout itself (``parents[2]`` of this module: this file is
    ``packages/orchestration/preview_runner.py``, so its checkout is two directories
    above ``packages``), never from the project ``root`` being served — the CLI being
    invoked is Remedy's own, not the project's.
    """
    argv = runtime_verb_argv(verb, root)
    checkout_root = Path(__file__).resolve().parents[2]
    try:
        result = subprocess.run(
            argv, cwd=checkout_root, capture_output=True, text=True,
            timeout=VERB_TIMEOUT_SECONDS, check=False,
        )
    except subprocess.TimeoutExpired:
        return VerbResult(False, {
            "error": "runtime_error",
            "message": f"runtime {verb} did not answer within {VERB_TIMEOUT_SECONDS} "
                       f"seconds",
        })
    except OSError as exc:
        return VerbResult(False, {
            "error": "runtime_error",
            "message": f"runtime {verb} could not be run: {exc.strerror}",
        })

    try:
        envelope = json.loads(result.stdout)
    except (json.JSONDecodeError, ValueError, TypeError):
        envelope = None
    if not isinstance(envelope, dict) or "ok" not in envelope:
        return VerbResult(False, {
            "error": "runtime_error",
            "message": f"runtime {verb} answered no envelope (exit {result.returncode})",
        })

    ok = bool(envelope.get("ok")) and result.returncode == 0
    return VerbResult(ok, envelope)
