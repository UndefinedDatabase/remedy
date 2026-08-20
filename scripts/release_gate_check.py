#!/usr/bin/env python3
"""Observe a proposed release and refuse it for every reason it must be refused.

`release_gate.refuse_release` DECIDES; this script OBSERVES. It reads the version
out of the built wheel's own FILENAME, the changelog off disk and the wheel's
size from the file itself, so every value the gate judges comes from the artifact
being released rather than from a second declaration that could drift out of sync
with it (DECISION F086 D2). Remedy deliberately does not upload anything here and
holds no credential: publishing stays a HUMAN command (T2_F086 Orchestrator).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = str(Path(__file__).resolve().parents[1])
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from packages.orchestration.release_gate import ReleaseRequest, refuse_release  # noqa: E402

DEFAULT_CHANGELOG = Path(_REPO_ROOT) / "CHANGELOG.md"
CI_SUCCESS_CONCLUSION = "success"


def version_from_wheel_name(wheel: Path) -> str:
    """Return the distribution version encoded in a wheel's filename.

    A wheel is named `<name>-<version>-<python>-<abi>-<platform>.whl`, so the
    version is its second hyphen-separated field. Reading it HERE ties the gate to
    the artifact under release: a wheel built from some other version cannot pass
    by agreeing with a declaration the build never read.
    """
    fields = wheel.name.split("-")
    if not wheel.name.endswith(".whl") or len(fields) < 5:
        raise ValueError(f"not a wheel filename: {wheel.name}")
    return fields[1]


def observe_release(tag: str, wheel: Path, changelog: Path, ci_status: str) -> ReleaseRequest:
    """Build the request the gate judges out of what is really on disk."""
    return ReleaseRequest(
        tag=tag,
        version=version_from_wheel_name(wheel),
        changelog=changelog.read_text(encoding="utf-8"),
        wheel_bytes=wheel.stat().st_size,
        ci_green=ci_status == CI_SUCCESS_CONCLUSION,
    )


def main(argv: list[str] | None = None) -> int:
    """Print every refusal reason; return 1 when there is one and 0 when there is none."""
    parser = argparse.ArgumentParser(description="Refuse a release that is not fit to ship.")
    parser.add_argument("--tag", required=True, help="the tag being released")
    parser.add_argument("--wheel", required=True, type=Path, help="the built wheel")
    parser.add_argument("--ci-status", required=True, help="the CI run's conclusion")
    parser.add_argument("--changelog", type=Path, default=DEFAULT_CHANGELOG)
    args = parser.parse_args(argv)
    reasons = refuse_release(
        observe_release(args.tag, args.wheel, args.changelog, args.ci_status)
    )
    for reason in reasons:
        print(f"REFUSED: {reason}", file=sys.stderr)
    if not reasons:
        print(f"release {args.tag} may proceed")
    return 1 if reasons else 0


if __name__ == "__main__":
    raise SystemExit(main())
