"""F277 T002 — the one shape every ``--json`` command answers in.

Measured before this module existed: of a 56-command output sample taken by the
2026-09-08 orchestrator, 30 carried a version key and 26 carried none, and the
two commands the feature file names by hand answered an invalid argument with a
bare ``Error: ...`` line on stderr and no JSON at all.  A machine consumer
therefore could not tell "this command failed" from "this command is not the
one I thought it was", because failure had no shape.

Two functions, one shape::

    {"schema_version": 1, "ok": true,  ...payload}
    {"schema_version": 1, "ok": false, "error": "<code>", "message": "<text>"}

``schema_version`` is an integer and starts at 1.  It changes only when a
consumer that reads the old shape would break; adding a key does not break such
a consumer, so adding a key does not bump it.

Deliberate absences:
  * Remedy deliberately does not make these functions exit.  Emission and exit
    are separate so a caller can emit and then choose its code, and so a test
    can call them without catching ``SystemExit``.  ``fail()`` (T003) is the
    helper that does both.
  * Remedy deliberately does not let a payload key overwrite ``schema_version``
    or ``ok``.  A command that passes one gets ``ValueError`` at the call site
    rather than a silently reshaped envelope, because the envelope is the one
    thing every consumer is entitled to assume.
  * Remedy deliberately does not sort the payload's own nested values by hand:
    ``json.dumps`` is called with ``sort_keys=True``, which orders every level,
    so two runs of the same command are byte-comparable and a diff of two
    envelopes shows only what really changed.
"""

from __future__ import annotations

import json
import sys
from typing import Any

#: The envelope's version.  Bumped only by a change that breaks a reader of the
#: previous shape — adding a key does not.
SCHEMA_VERSION = 1

#: The two keys the envelope owns.  A payload may not carry either.
RESERVED_KEYS = ("schema_version", "ok")


def build_ok(**payload: Any) -> dict[str, Any]:
    """The success envelope as a dict, for a caller that serialises it itself."""
    _reject_reserved(payload)
    return {"schema_version": SCHEMA_VERSION, "ok": True, **payload}


def build_error(error: str, message: str, **payload: Any) -> dict[str, Any]:
    """The failure envelope as a dict.

    ``error`` is a stable machine token (``invalid_job_id``, ``missing_argument``)
    and ``message`` is the sentence a human reads.  Both are required: a consumer
    that branches on prose is a consumer that breaks on a reworded message.
    """
    _reject_reserved(payload)
    return {
        "schema_version": SCHEMA_VERSION,
        "ok": False,
        "error": error,
        "message": message,
        **payload,
    }


def emit_ok(**payload: Any) -> None:
    """Print the success envelope to stdout.  Does not exit."""
    _write(build_ok(**payload), sys.stdout)


def emit_error(error: str, message: str, **payload: Any) -> None:
    """Print the failure envelope to stdout.  Does not exit.

    stdout rather than stderr on purpose: a machine consumer runs one command
    and reads one stream, and splitting the answer across two by outcome is the
    shape that made the failure case unreadable in the first place.  The exit
    code carries the outcome for a shell; the envelope carries it for a parser.
    """
    _write(build_error(error, message, **payload), sys.stdout)


def _reject_reserved(payload: dict[str, Any]) -> None:
    clash = [k for k in RESERVED_KEYS if k in payload]
    if clash:
        raise ValueError(
            "payload may not carry the envelope's own keys: "
            + ", ".join(clash)
            + " — rename the payload key, or change the envelope deliberately"
        )


def _write(envelope: dict[str, Any], stream: Any) -> None:
    print(json.dumps(envelope, sort_keys=True, default=str), file=stream)
