"""F5 (round 26): the ONE dependency-free strict JSON decoder for every Root-of-Trust artifact.

Both `scripts/build_review_manifest.py` and `scripts/build_review_zip.py` — and every gate / subject
/ proof / chain / inventory decode on the trust path — import THIS implementation, so there is a
single place that decides what "unambiguous JSON" means. It rejects:

* duplicate keys at ANY depth (the stdlib silently keeps the last of duplicate keys, so two different
  byte strings would decode to one object);
* the non-standard ``NaN`` / ``Infinity`` / ``-Infinity`` constants (Python extensions, not JSON);
* invalid UTF-8 (surfaced as StrictJsonError, never a raw UnicodeDecodeError);
* a non-object payload when ``require_object`` is set.

It is intentionally dependency-free (only the stdlib ``json``) so the standalone review-packaging
scripts stay importable in the minimal isolated environments the archive-mechanics tests use.
"""
from __future__ import annotations

import json
from typing import Any


class StrictJsonError(ValueError):
    """A trust-path artifact was absent-of-ambiguity's opposite: duplicate-keyed, non-standard,
    non-UTF-8, or not the object it had to be."""


def _no_duplicate_keys(pairs):
    seen: set = set()
    out: dict = {}
    for k, v in pairs:
        if k in seen:
            raise StrictJsonError(f"duplicate JSON key {k!r}")
        seen.add(k)
        out[k] = v
    return out


def _reject_constant(name: str):
    raise StrictJsonError(f"non-standard JSON constant {name!r}")


def strict_loads(raw: bytes | bytearray | str, *, where: str = "artifact",
                 require_object: bool = False) -> Any:
    """Decode ``raw`` strictly. Raises :class:`StrictJsonError` on any ambiguity."""
    if isinstance(raw, (bytes, bytearray)):
        try:
            text = bytes(raw).decode("utf-8")
        except UnicodeDecodeError as exc:
            raise StrictJsonError(f"unreadable {where}: not valid UTF-8 ({exc.reason})") from None
    else:
        text = raw
    try:
        data = json.loads(text, object_pairs_hook=_no_duplicate_keys,
                          parse_constant=_reject_constant)
    except StrictJsonError:
        raise
    except ValueError as exc:
        raise StrictJsonError(f"unreadable {where}: {exc}") from None
    if require_object and not isinstance(data, dict):
        raise StrictJsonError(f"{where} is not a JSON object")
    return data
