"""Secret, absolute-path and traceback masking for strings Remedy surfaces publicly.

WHY THIS IS HERE. These three patterns and the two helpers over them were written for
the Provider Trust Gate, in a module F275 round 22 deleted at `0242c0a3` (R-0083: never
echo a secret value or an absolute path out of untrusted provider text). Seven modules that
have nothing to do with provider trust came to import them anyway, because masking a
public-facing string is a repository-wide obligation rather than a trust-gate one. F275
round 21 deletes the trust gate, so the helpers move here BYTE-IDENTICALLY — one
implementation, no copy, no shim — and the former host's importers repoint at this
module. DECISION F275 D10 records the move and why this file rather than an existing one.

NOT `packages/common/path_redaction.py`, and the distinction is load-bearing. That module
reduces every absolute path and `file:` URI to its bare file name, for shareable runtime
state and post-mortems; it is about PATHS and it rewrites all of them. This module masks
SECRET-LIKE material, a narrow set of home-ish absolute paths and stack traces, and it
replaces them with `[redacted-...]` markers rather than shortening them. Both would have
carried a module-level constant spelled `ABS_PATH_RE` over two different regexes with two
different jobs, which is exactly the synonym drift AGENTS.md's Code Discoverability
Conventions forbid.

Remedy deliberately does not re-export these under public names: the leading underscore is
the original spelling, every call site already uses it, and renaming five names across
seven modules is the mass rename those same conventions forbid as its own activity.
"""
from __future__ import annotations

import re

_SECRET_PATTERNS = [
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bsk-[A-Za-z0-9]{16,}\b"),
    re.compile(r"\bghp_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bBearer\s+[A-Za-z0-9._\-]{12,}"),
    re.compile(r"(?i)\b(api[_-]?key|secret|token|password|passwd|pwd)\b\s*[:=]\s*\S{6,}"),
    re.compile(r"(?i)\bAWS_SECRET_ACCESS_KEY\b\s*[:=]\s*\S+"),
]
_ABS_PATH_RE = re.compile(r"(?:^|[\s\"'=(])(/(?:home|Users|root|etc|var|opt|private)/[^\s\"':]+)")
_TRACEBACK_RE = re.compile(r"Traceback \(most recent call last\)")


def _scrub_public(text: str) -> str:
    """Mask secret-like material and absolute paths in a public-facing string."""
    scrubbed = text
    for pat in _SECRET_PATTERNS:
        scrubbed = pat.sub("[redacted-secret]", scrubbed)
    scrubbed = _ABS_PATH_RE.sub(lambda m: m.group(0).replace(m.group(1), "[redacted-path]"), scrubbed)
    scrubbed = _TRACEBACK_RE.sub("[redacted-trace]", scrubbed)
    return scrubbed


def _safe_path_label(path: str) -> str:
    """A repo-relative-ish, length-bounded label. Never an absolute path."""
    p = (path or "").replace("\\", "/")
    if p.startswith("/"):
        p = p.rsplit("/", 1)[-1]
    return p[:80]
