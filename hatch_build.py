"""Packaging-time guard: refuse to build a wheel with no built UI assets.

WHY: `artifacts = ["apps/ui/dist/**"]` in pyproject.toml carries the built UI into
the wheel, but it is silent when that directory is absent — measured at 419fb683,
a build with the carry applied and no `apps/ui/dist` present exits 0 and ships a
414-member wheel with zero UI files. That is exactly the "empty UI directory
shipped silently" DECISION F086 D1 part (b) forbids, and this hook is that guard.

Remedy deliberately keeps the rule in a plain function rather than only in the
hook class: the test suite must be able to exercise it without the build backend
installed, and the class below is a thin adapter that hatchling loads.
"""

from __future__ import annotations

from pathlib import Path

try:  # the build backend supplies hatchling; the test environment need not
    from hatchling.builders.hooks.plugin.interface import BuildHookInterface
except ImportError:  # pragma: no cover - only the real wheel build takes this path
    BuildHookInterface = object  # type: ignore[assignment,misc]

FRONTEND_DIST_INDEX = "apps/ui/dist/index.html"


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


class FrontendAssetsBuildHook(BuildHookInterface):
    """Fail the wheel build when the built frontend entry point is missing."""

    PLUGIN_NAME = "remedy-frontend-assets"

    def initialize(self, version, build_data):
        assert_frontend_assets_built(self.root)
