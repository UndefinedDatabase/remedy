"""Text about paths that a person may paste: the operator's home folder is written as `~`.

Moved out of `packages/orchestration/self_health.py` (R-1290, DECISION F307 D6), because the crash
report and the command line's crash message use it too.
"""

from __future__ import annotations

import re
from pathlib import Path


# A detail must not leak the operator's home folder into a pasted report.
def home_relative_text(text: str, home: Path | None = None) -> str:
    home_text = str(home if home is not None else Path.home())
    if home_text == "/":
        return text
    return text.replace(home_text, "~")


#: A secret's value after its name, as an error message may carry one: masked, the name kept.
_SECRET_VALUE = re.compile(r"(?i)(key|token|secret|password|api_key)=[^\s,;)\"']+")
#: Another person's home folder, or root's: written `~/`, as the operator's own is. A path under
#: `/mnt/` or `/tmp/` is no home folder and is named as it is (R-1291).
_ANY_HOME = re.compile(r"/home/[^/]+/|/Users/[^/]+/|/root/")


# WHY: `remedy doctor core` and `remedy doctor health` once scrubbed a detail two ways (R-1291).
def report_safe_text(text: object, limit: int | None = None) -> str:
    """TEXT as a report may print it: no home folder and no secret value, cut to LIMIT characters.

    The one scrubber of both doctor commands: the operator's home folder and any other home folder
    are written `~`, the value of a `key=`, `token=`, `secret=`, `password=` or `api_key=` is
    written `***`, and a text longer than LIMIT ends in `...`.
    """
    scrubbed = _SECRET_VALUE.sub(r"\1=***", _ANY_HOME.sub("~/", home_relative_text(str(text))))
    return scrubbed[:limit] + "..." if limit is not None and len(scrubbed) > limit else scrubbed
