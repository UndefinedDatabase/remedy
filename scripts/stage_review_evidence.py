#!/usr/bin/env python3
"""F8 (round 19) — the typed, no-follow Evidence staging CLI used by make_review_zip.sh.

Replaces the `find "$EVIDENCE_DIR" -type f | cp` staging (which SKIPS symlinks and FOLLOWS them
into outside bytes) with an anchored no-follow copy, and replaces the `find "$STAGING" -type f`
listing with a typed walk. A symlink/FIFO/device anywhere in the evidence tree fails the build
closed — it is never skipped and never followed.

  stage --src SRC --dest DEST_DIR            copy every regular file, no-follow, into DEST_DIR
  list  --root ROOT --nul-out F --text-out F  emit the regular-file inventory of ROOT
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from packages.orchestration.evidence_inventory import (  # noqa: E402
    EvidenceInventoryError,
    list_regular_tree,
    stage_evidence_tree,
)


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    ps = sub.add_parser("stage")
    ps.add_argument("--src", required=True)
    ps.add_argument("--dest", required=True)

    pl = sub.add_parser("list")
    pl.add_argument("--root", required=True)
    pl.add_argument("--nul-out", required=True)
    pl.add_argument("--text-out", default="")

    args = ap.parse_args()
    try:
        if args.cmd == "stage":
            staged = stage_evidence_tree(args.src, args.dest)
            print(len(staged))
        else:
            rels = list_regular_tree(args.root)
            with open(args.nul_out, "wb") as fh:
                fh.write(b"".join((r + "\0").encode() for r in rels))
            if args.text_out:
                with open(args.text_out, "w") as fh:
                    fh.write("".join(r + "\n" for r in rels))
    except EvidenceInventoryError as exc:
        print(f"EVIDENCE_INVENTORY_ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
