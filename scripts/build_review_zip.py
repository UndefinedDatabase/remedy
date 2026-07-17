#!/usr/bin/env python3
"""F8/F10 (round 17) — the NUL-safe review-ZIP construction stage.

Invoked by `make_review_zip.sh` in place of `find | zip -@`. It reads NUL-delimited file lists
(so a filename containing a newline survives), builds the archive with `zipfile` via the typed
builder in `packages.orchestration.review_zip`, then REOPENS it and verifies the exact member set
and hashes. Any containment escape, duplicate, missing or extra member is a hard failure.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from packages.orchestration.review_zip import (  # noqa: E402
    ReviewZipError,
    build_review_zip,
    read_nul_list,
    verify_review_zip,
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--repo-root", required=True)
    ap.add_argument("--repo-files0", required=True, help="NUL-delimited repo file list")
    ap.add_argument("--evidence-root", default="")
    ap.add_argument("--evidence-files0", default="", help="NUL-delimited evidence file list")
    ap.add_argument("--manifest-rel", required=True)
    ap.add_argument("--manifest-disk", required=True)
    args = ap.parse_args()

    repo_files = read_nul_list(args.repo_files0)
    evidence_files = read_nul_list(args.evidence_files0) if args.evidence_files0 else []
    evidence_root = args.evidence_root or None

    try:
        result = build_review_zip(
            out_path=args.out, repo_root=args.repo_root, repo_files=repo_files,
            evidence_root=evidence_root, evidence_files=evidence_files,
            manifest_rel=args.manifest_rel, manifest_disk=args.manifest_disk)
        problems = verify_review_zip(args.out, result)
    except ReviewZipError as exc:
        print(f"REVIEW_ZIP_ERROR: {exc}", file=sys.stderr)
        return 2

    if problems:
        print("REVIEW_ZIP_VERIFICATION_FAILED:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 3

    print(json.dumps({"member_count": len(result["members"]),
                      "symlink_count": len(result["symlinks"])}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
