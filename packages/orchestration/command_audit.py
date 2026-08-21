"""The per-job command audit record — DECISION F009 D6, with D14's three halves.

Every attempt at the single write door leaves a line here, accepted or refused, so that
"wrong or missing auth is audited as rejected" is a property of the door rather than a
promise. The record is one JSON object per line in `commands_audit.jsonl`, inside the job's
private control directory, appended and never rewritten.

This module owns the record and nothing else: it decides no status code, refuses no request
and never reads a request. `packages/orchestration/ui_server.py` decides; this writes down
what was decided.
"""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Any

from packages.common import secure_fs as _fs
from packages.orchestration import safe_points

__all__ = [
    "AUDIT_FILENAME",
    "AUDIT_FILE_MODE",
    "AUDIT_FIELD_ORDER",
    "OUTCOMES",
    "args_fingerprint",
    "audit_command_attempt",
]

#: DECISION F009 D6 fixes the name; T5_F035 and T9_F167 already plan to READ it.
AUDIT_FILENAME = "commands_audit.jsonl"

#: The mode the job control directory's other files already use.
AUDIT_FILE_MODE = 0o600

#: DECISION F009 D6 fixes this ORDER, and two later features depend on it. The line is
#: built key by key in this sequence rather than sorted, so a reader sees the same shape
#: on every line.
AUDIT_FIELD_ORDER = ("ts", "token_fp", "command", "args_hash", "nonce", "outcome")

#: DECISION F009 D14's closed vocabulary. Each token names the CHECK that refused, never
#: the client's message, so a wording change cannot drift the vocabulary. `accepted` and
#: `replayed` are the two NO caller writes yet: DECISION F009 D17 lands the vocabulary one
#: round ahead of the dispatch that writes them, so the round retiring the 501 seam changes
#: the door alone. `replayed` is deliberately distinct from `accepted` (finding R-0636): a
#: replay REPEATS an acceptance rather than being one, and T5_F035 and T9_F167 both read
#: this file to count what the door did, so one token for both would make them
#: indistinguishable to the two features that care.
OUTCOMES = (
    "rejected_token",
    "rejected_csrf",
    "rejected_job",
    "rejected_shape",
    "rejected_command",
    "rejected_rate",
    "not_implemented",
    "accepted",
    "replayed",
)


# `token_fp` arrives already fingerprinted, from `ui_server.token_fingerprint` (DECISION
# F009 D7) — that is where a reader looking for the hashing will find it. This module never
# sees, accepts or writes a raw token, which is why no fingerprinting happens here.
def args_fingerprint(args: Any) -> str:
    """A stable, non-reversible handle for one command's arguments (DECISION F009 D14).

    The raw `args` are NEVER written: they are client-supplied and may name paths or ids
    that the redaction denylist would have to reason about. The hash answers the only
    question this record asks of them — whether two attempts carried the same arguments.

    `secure_fs.json_bytes` sorts keys, which is what makes two clients that spell the same
    object in different orders hash the same. The `ah:` prefix mirrors `tf:` so the two
    digests are told apart at a glance on a line.
    """
    return "ah:" + hashlib.sha256(_fs.json_bytes(args)).hexdigest()[:16]


def audit_command_attempt(job_id: Any, *, token_fp: str, command: Any, args: Any,
                          nonce: Any, outcome: str, create: bool,
                          control_root_path: Path | None = None) -> bool:
    """Append ONE attempt to the job's audit log. True when a record was written.

    `create` is DECISION F009 D14's first clause. An attempt whose bearer or CSRF check
    failed is audited only into a control directory that ALREADY exists (`create=False`)
    and writes nothing when there is none: creating one would let a caller who has
    presented nothing steer directory litter on this host. An attempt past both credential
    checks is audited with `create=True`.

    Nothing here raises for a caller's benefit. A `job_id` that does not validate writes
    nothing and returns False rather than raising, so the door never has to pre-validate a
    path segment it took from a URL. A missing `nonce` is written as the empty string, so
    the field is present on every line and a reader never has to handle its absence.
    """
    try:
        jid = safe_points.validate_job_id(str(job_id or ""))
    except safe_points.StopControlError:
        return False

    record = {
        "ts": safe_points.utc_now_iso(),
        "token_fp": str(token_fp or ""),
        "command": str(command or ""),
        "args_hash": args_fingerprint(args if args is not None else {}),
        "nonce": str(nonce or ""),
        "outcome": str(outcome or ""),
    }
    ordered = {key: record[key] for key in AUDIT_FIELD_ORDER}
    # One record is one LINE, so the object is serialised without indentation. `json_bytes`
    # already ends its output in exactly the one newline `append_line_at` requires.
    line = _fs.json_bytes(ordered, indent=None, sort_keys=False)

    job_fd = safe_points.open_job_control_fd(jid, control_root_path, create=create)
    if job_fd is None:
        return False                      # create=False and no such directory: D14, clause 1
    try:
        _fs.append_line_at(job_fd, AUDIT_FILENAME, line,
                           file_mode=AUDIT_FILE_MODE,
                           error_cls=safe_points.StopControlError,
                           noun="command audit record")
    finally:
        os.close(job_fd)
    return True
