"""Shared display symbols for CLI output across orchestration modules."""

OK   = "\u2713"
FAIL = "\u2715"
WARN = "!"
INFO = "\u25cb"
NEXT = "\u2192"
LINE = "\u2500"


def section(title: str, *, width: int = 50) -> str:
    """Return a section header bar."""
    bar = LINE * max(1, width - len(title) - 1)
    return f"\n{LINE}{LINE} {title} {bar}"
