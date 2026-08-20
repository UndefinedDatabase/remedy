"""Packaging-time guard and build-info embedding for the remedy wheel.

THE GUARD: `artifacts = ["apps/ui/dist/**"]` carries the built UI but is SILENT
when that directory is absent — measured at 419fb683, such a build exits 0 and
ships zero UI files, which DECISION F086 D1 part (b) forbids.

THE EMBEDDING: `remedy --version` reports the revision a wheel was built from
(DECISION F086 D2). hatchling prefixes every hook-supplied extra-metadata entry
with `extra_metadata/` inside `.dist-info`, so a hook CANNOT produce
`<dist-info>/REVISION`; the wheel carries `<dist-info>/extra_metadata/REVISION`
and `apps/cli/version_report.py` reads back there. ONE hook class, because
`load_plugin_from_script` refuses a script defining two subclasses. Both rules
live in plain functions so the suite can exercise them without the build backend,
and the revision never touches the source tree — a generated file there survives
the build and reports a revision nobody built.
"""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

try:  # the build backend supplies hatchling; the test environment need not
    from hatchling.builders.hooks.plugin.interface import BuildHookInterface
except ImportError:  # pragma: no cover - only the real wheel build takes this path
    BuildHookInterface = object  # type: ignore[assignment,misc]

FRONTEND_DIST_INDEX = "apps/ui/dist/index.html"
REVISION_WHEEL_NAME = "REVISION"


def assert_frontend_assets_built(root: str | Path) -> Path:
    """Return the frontend entry point under `root`, or raise ValueError if absent."""
    index = Path(root) / FRONTEND_DIST_INDEX
    if not index.is_file():
        raise ValueError(
            f"remedy: refusing to build a wheel without built UI assets. "
            f"{FRONTEND_DIST_INDEX} is missing under {root}. Build the frontend "
            f"first (npm --prefix apps/ui run build); a wheel built without it "
            f"installs a CLI whose UI cannot serve."
        )
    return index


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
    """Refuse a wheel with no built UI, and embed the revision it was built from."""

    PLUGIN_NAME = "remedy-build"

    def initialize(self, version, build_data):
        assert_frontend_assets_built(self.root)
        build_data["extra_metadata"].update(
            build_revision_metadata(self.root, tempfile.mkdtemp())
        )
