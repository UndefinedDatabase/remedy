"""The release gate: every reason a release must be refused (T2_F086 T003).

This module DECIDES and RUNS NOTHING. It takes a description of a proposed
release and returns the reasons to refuse it, so each refusal the feature's
Acceptance names is testable without a tag, a wheel or a CI run existing. The
caller — a manual-trigger workflow, not yet written — supplies the real values,
reads the repository's `CHANGELOG.md` and stops on a non-empty result. Until that
caller exists this gate refuses nothing, because nothing calls it. It is
deliberately NOT an entry in `ci_stages.CI_STAGES`, which is pytest-selection
data; this gate selects no tests. Publishing stays a HUMAN command, which
T2_F086's Orchestrator brief requires: nothing here uploads or holds a credential.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

#: Measured, not guessed: a wheel built at F086 R12 carrying a stand-in
#: `index.html` is 2040197 B, one carrying the built `apps/ui/dist` was 2155470 B
#: at F086 R7. The budget is 8 MiB, about four times that: it admits a real UI
#: bundle's growth while still refusing what it exists to catch — a wheel that
#: swallowed `node_modules`, `.git` or the test corpus.
WHEEL_SIZE_BUDGET_BYTES = 8 * 1024 * 1024


@dataclass(frozen=True)
class ReleaseRequest:
    """A proposed release, as the caller observed it."""

    tag: str
    version: str
    changelog: str
    wheel_bytes: int
    ci_green: bool


def normalise_tag(tag: str) -> str:
    """Return `tag` without a leading `v`, which is how tags are written here."""
    return tag[1:] if tag.startswith("v") else tag


def changelog_section(changelog: str, version: str) -> str | None:
    """Return the body of `version`'s changelog section, or None if it has none.

    A section runs from its own `## [<version>]` heading to the next heading
    starting `## `, or to the end of the file. An empty body is NOT the same as a
    missing section: the caller refuses on both but must be able to say which.
    """
    heading = re.compile(rf"^## \[{re.escape(version)}\][^\n]*\n", re.MULTILINE)
    found = heading.search(changelog)
    if found is None:
        return None
    rest = changelog[found.end():]
    following = re.search(r"^## ", rest, re.MULTILINE)
    return rest if following is None else rest[: following.start()]


def refuse_release(request: ReleaseRequest) -> tuple[str, ...]:
    """Every reason to refuse `request`; an EMPTY tuple means it may proceed.

    Every rule is evaluated, so the result names ALL the reasons rather than the
    first — a release broken four ways should have to be fixed once.
    """
    reasons: list[str] = []
    if not request.ci_green:
        reasons.append("CI is not green for this commit")
    if normalise_tag(request.tag) != request.version:
        reasons.append(
            f"tag {request.tag!r} does not match distribution version {request.version!r}"
        )
    body = changelog_section(request.changelog, request.version)
    if body is None:
        reasons.append(f"CHANGELOG.md has no section for version {request.version!r}")
    elif not body.strip():
        reasons.append(f"the CHANGELOG.md section for {request.version!r} is empty")
    if request.wheel_bytes > WHEEL_SIZE_BUDGET_BYTES:
        reasons.append(
            f"wheel is {request.wheel_bytes} B, over the "
            f"{WHEEL_SIZE_BUDGET_BYTES} B budget"
        )
    return tuple(reasons)
