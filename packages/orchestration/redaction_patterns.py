"""
Redaction pattern detection — precise forbidden-token checks for output surfaces.

Distinguishes between:
- Category words (allowed): "No secrets", "redact secrets", "environment_secrets"
- Actual secret patterns (blocked): "sk-...", "password=...", "secret=..."
- Forbidden raw field names (blocked): "approval_reason", "diff_preview", etc.

Public API::

    FORBIDDEN_RAW_FIELD_NAMES: frozenset[str]
    FORBIDDEN_SECRET_PATTERNS: tuple[str, ...]
    find_forbidden_surface_tokens(text: str) -> list[str]
"""

from __future__ import annotations

import re

# ---------------------------------------------------------------------------
# Forbidden raw field names — these should never appear in output surfaces
# ---------------------------------------------------------------------------

FORBIDDEN_RAW_FIELD_NAMES: frozenset[str] = frozenset({
    "approval_reason",
    "diff_preview",
    "command_output",
    "raw_stdout",
    "raw_stderr",
    "raw_command_output",
    "raw_output",
})

# ---------------------------------------------------------------------------
# Forbidden secret patterns — case-insensitive prefix/pattern detection
# ---------------------------------------------------------------------------

FORBIDDEN_SECRET_PATTERNS: tuple[str, ...] = (
    "sk-",
    "ghp_",
    "xoxb-",
    "begin private key",
    "password=",
    "api_key=",
    "secret=",
    "token=",
    "credential=",
)

# Compiled regex for secret patterns — matches value-carrying patterns only
_SECRET_RE = re.compile(
    r"(?i)"
    r"(?:sk-[a-zA-Z0-9_-]{8,})"     # OpenAI-style (keys contain hyphens/underscores)
    r"|(?:ghp_[a-zA-Z0-9]{8,})"     # GitHub PAT
    r"|(?:xoxb-[a-zA-Z0-9_-]+)"     # Slack bot token
    r"|BEGIN\s+PRIVATE\s+KEY"        # PEM headers
    r"|(?:password|api_key|secret|token|credential)\s*=\s*[^\s,;'\"]*"  # key=value leaks (key + value)
)

# Forbidden traceback/exception patterns
_TRACEBACK_RE = re.compile(
    r"Traceback\s*\(most\s+recent",
    re.IGNORECASE,
)


def find_forbidden_surface_tokens(text: str) -> list[str]:
    """Find forbidden tokens in an output surface string.

    Returns a list of human-readable descriptions of what was found.
    Empty list means the text is clean.

    Does NOT reject category words like "No secrets" or "redact secrets".
    Only rejects actual secret-looking patterns and raw field names.
    """
    findings: list[str] = []

    # Check raw field names (exact word boundary match)
    for field in FORBIDDEN_RAW_FIELD_NAMES:
        if field in text:
            findings.append(f"forbidden raw field: {field}")

    # Check secret patterns
    for match in _SECRET_RE.finditer(text):
        findings.append(f"forbidden secret pattern: {match.group()[:40]}")

    # Check traceback patterns
    if _TRACEBACK_RE.search(text):
        findings.append("forbidden traceback pattern")

    return findings
