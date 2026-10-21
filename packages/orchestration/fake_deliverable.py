"""The fake builder `--builder-provider fake` selects writes its task's deliverable (amend1015c D6).

Operator order amend1015-final-closure, E5 (R-1325): `remedy do run "pass die readme an"` on a
repository whose one tracked file is `README.md` planned the task "Deliver README.md" correctly,
and the result then changed `docs/README.md`. The cause was the fixture, not the resolver:
`FakeProvider` writes a fixed `docs/README.md` whatever its task names, so every fake run through
the command line showed a person a file the order never named. `DeliverableFakeProvider` is the
same fake, except that a build whose prompt names one repository-relative Markdown file as its
task's deliverable writes that file: the fake's content is a Markdown note, so a source file stays
with the fixed `docs/README.md` (written into `src/main.py`, the note fails its review). A fake given its own files (a test's `builder_files`) and tests that
build a `FakeProvider` themselves keep their fixed files.

Public API::

    DeliverableFakeProvider
    prompt_deliverable_file(prompt) -> str
"""

from __future__ import annotations

import re
from typing import Any

from packages.orchestration.pingpong_provider_fake import FakeProvider

#: The line `task_deliverables.deliverable_task` writes into a task's body, and so into its prompt.
_DELIVERABLE_LINE = re.compile(r"^This task's deliverable: (\S+)[ \t]*$", re.MULTILINE)
#: The deliverables the fake's Markdown note fits.
_MARKDOWN = (".md", ".markdown")
#: `FakeProvider`'s own file when nobody gave it files.
_STOCK_FILES = ["docs/README.md"]


def prompt_deliverable_file(prompt: str) -> str:
    """The one Markdown file the prompt's last deliverable line names, or "" when that deliverable
    is no single repository-relative Markdown file (the order's own text, a check, a source file,
    a sensitive path)."""
    from packages.orchestration.sensitive_paths import sensitive_path_category
    from packages.orchestration.task_deliverables import extract_order_deliverables

    named = _DELIVERABLE_LINE.findall(prompt)
    if not named:
        return ""
    path = named[-1]
    # The extractor answers a text that names no file with the text itself, so the path is a file
    # only when it is also the one file of a longer text.
    if extract_order_deliverables(f"write {path}") != [path]:
        return ""
    if not path.lower().endswith(_MARKDOWN):
        return ""
    return "" if sensitive_path_category(path) else path


class DeliverableFakeProvider(FakeProvider):
    """`FakeProvider` whose build writes the task's one deliverable file when the prompt names one."""

    _deliverable = ""

    def build(self, prompt: str, **kwargs: Any):  # type: ignore[override]
        out = super().build(prompt, **kwargs)
        if self._builder_files != _STOCK_FILES:
            return out
        # A repair round's prompt carries the review, not the task's body, so the round repairs
        # the file the task's own prompt named last.
        self._deliverable = prompt_deliverable_file(prompt) or self._deliverable
        if self._deliverable and not out.error:
            out.files_changed = [self._deliverable]
        return out
