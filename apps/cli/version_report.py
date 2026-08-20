"""`remedy --version` — the version and build info a release is checked against.

WHY here: DECISION F086 D2 keeps `pyproject.toml` as the single place a version
NUMBER is written and reads it back through package metadata, so no second
literal exists to drift out of sync. In a checkout the distribution is often not
installed and no revision was embedded at build time; this module then reports
`dev` rather than inventing a sha, which D2 makes a requirement and not a
fallback — a version command that reports a fabricated revision is worse than
one that admits it is looking at a working tree.

Remedy deliberately does not generate a `_version.py` at build time: a stale
generated file in a checkout outranks the metadata and reports a version nobody built.
"""

from __future__ import annotations

import platform
import sys
from importlib.metadata import PackageNotFoundError, distribution

DISTRIBUTION_NAME = "remedy"
# hatchling prefixes every hook-supplied extra-metadata entry with
# `extra_metadata/` inside `.dist-info`, so a real wheel answers here and returns
# None for a bare `REVISION` — measured on a built wheel, not inferred.
# `hatch_build.py` writes the other half of this pair.
REVISION_METADATA_FILE = "extra_metadata/REVISION"
UNKNOWN_MARKER = "dev"


def resolve_distribution_version() -> str:
    """Return the installed distribution's version, or `dev` in a checkout."""
    try:
        return distribution(DISTRIBUTION_NAME).version
    except PackageNotFoundError:
        return UNKNOWN_MARKER


def resolve_build_revision() -> str:
    """Return the revision embedded at build time, or `dev` when none was."""
    try:
        embedded = distribution(DISTRIBUTION_NAME).read_text(REVISION_METADATA_FILE)
    except PackageNotFoundError:
        return UNKNOWN_MARKER
    if embedded is None or not embedded.strip():
        return UNKNOWN_MARKER
    return embedded.strip()


def render_version_report() -> str:
    """Render the `remedy --version` report as the release gate reads it."""
    return "\n".join(
        [
            f"remedy   {resolve_distribution_version()}",
            f"build    {resolve_build_revision()}",
            f"python   {platform.python_version()}",
            f"platform {platform.platform()}",
        ]
    )


def handle_version_flag(argv: list[str] | None) -> bool:
    """Print the version report if argv asks for it; return whether it did.

    Called before the help pre-scan so `remedy --version` answers from anywhere
    in the command tree and is never swallowed by `--help` or by argparse.
    """
    raw = sys.argv[1:] if argv is None else argv
    if "--version" not in raw:
        return False
    print(render_version_report())
    return True
