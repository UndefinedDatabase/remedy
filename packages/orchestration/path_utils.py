"""
Shared path-component sanitization for Remedy.

This is the single canonical location for the sanitize_path_component function.
Previously, identical copies existed in task_registry.py, task_runner.py, and
patch_intent.py.  All call sites now import from this module.

Public API::

    sanitize_path_component(value: str) -> str
"""

from __future__ import annotations

import re

_SAFE_PATH_RE = re.compile(r"[^a-zA-Z0-9_-]")
_MAX_PATH_COMPONENT_LENGTH = 48


def sanitize_path_component(value: str) -> str:
    """Sanitize a string for safe use as a single filesystem path component.

    Replaces any character that is not alphanumeric, underscore, or hyphen
    with an underscore.  Truncates to 48 characters.  Strips leading and
    trailing underscores.  Returns "unknown" if the result is empty after
    sanitization.

    This neutralizes path traversal sequences ("../", "/") because "." and "/"
    are both replaced with "_".  Callers must still pass the result as a single
    component (not a full path) to remain safe.

    Examples::

        sanitize_path_component("write_readme")   -> "write_readme"
        sanitize_path_component("my-task")        -> "my-task"
        sanitize_path_component("../escape")      -> "_escape"   (stripped)
        sanitize_path_component("a" * 60)         -> "a" * 48
        sanitize_path_component("...")            -> "unknown"
        sanitize_path_component("")               -> "unknown"
    """
    sanitized = _SAFE_PATH_RE.sub("_", value)
    sanitized = sanitized[:_MAX_PATH_COMPONENT_LENGTH].strip("_")
    return sanitized or "unknown"
