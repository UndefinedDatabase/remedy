"""Build-info embedding for the remedy wheel.

`remedy --version` reports the revision a wheel was built from (DECISION F086 D2).
hatchling prefixes every hook-supplied extra-metadata entry with `extra_metadata/`
inside `.dist-info`, so a hook CANNOT produce `<dist-info>/REVISION`; the wheel
carries `<dist-info>/extra_metadata/REVISION` and `apps/cli/version_report.py` reads
back there. The rule lives in plain functions so the suite can exercise it without
the build backend, and the revision never touches the source tree — a generated
file there survives the build and reports a revision nobody built.

The guard that refused a wheel without the built UI went with the UI (amend1015f
D3, which reverses DECISION F086 D1): there is no `apps/ui/dist` left to carry.
The editable target still embeds nothing: `pip install -e` points at the checkout
and `remedy --version` reports `dev` there.
"""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

try:  # the build backend supplies hatchling; the test environment need not
    from hatchling.builders.hooks.plugin.interface import BuildHookInterface
except ImportError:  # pragma: no cover - only the real wheel build takes this path
    BuildHookInterface = object  # type: ignore[assignment,misc]

REVISION_WHEEL_NAME = "REVISION"
EDITABLE_BUILD_TARGET = "editable"


def build_target_embeds_revision(version: str) -> bool:
    """Return whether build target `version` gets the embedded revision.

    Only the editable target does not: it ships nothing of its own and points at
    the checkout instead.
    """
    return version != EDITABLE_BUILD_TARGET


def resolve_source_revision(root: str | Path) -> str | None:
    """Return the git revision of the tree at `root`, or None when it has none.

    None is not a failure: an sdist unpacked outside version control has no
    revision, and DECISION F086 D2 requires an honest `dev` over an invented sha.
    """
    try:
        completed = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if completed.returncode != 0:
        return None
    return completed.stdout.strip() or None


def build_revision_metadata(root: str | Path, staging: str | Path) -> dict[str, str]:
    """Write the revision under `staging` and return its extra-metadata map.

    The map is EMPTY when no revision resolves, so the wheel carries no REVISION
    member at all and `remedy --version` reports `dev` rather than a guess.
    """
    revision = resolve_source_revision(root)
    if revision is None:
        return {}
    written = Path(staging) / REVISION_WHEEL_NAME
    written.write_text(f"{revision}\n", encoding="utf-8")
    return {str(written): REVISION_WHEEL_NAME}


class RemedyBuildHook(BuildHookInterface):
    """Embed the revision a wheel was built from."""

    PLUGIN_NAME = "remedy-build"

    def initialize(self, version, build_data):
        if not build_target_embeds_revision(version):
            return
        build_data["extra_metadata"].update(
            build_revision_metadata(self.root, tempfile.mkdtemp())
        )
