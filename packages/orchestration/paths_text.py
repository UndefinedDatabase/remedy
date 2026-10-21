"""Text about paths that a person may paste: the operator's home folder is written as `~`.

Moved out of `packages/orchestration/self_health.py` (R-1290, DECISION F307 D6), because the crash
report and the command line's crash message use it too.
"""

from __future__ import annotations

from pathlib import Path


# A detail must not leak the operator's home folder into a pasted report.
def home_relative_text(text: str, home: Path | None = None) -> str:
    home_text = str(home if home is not None else Path.home())
    if home_text == "/":
        return text
    return text.replace(home_text, "~")
