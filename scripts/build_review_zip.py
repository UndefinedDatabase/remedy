#!/usr/bin/env python3
"""F1/F2/F3/F6/F10 (round 18) — the NUL-safe, plan-driven review-ZIP construction stage.

Invoked by `make_review_zip.sh`. It reads the typed ReviewSubject (the authoritative change) and
the repository bundle context list (NUL-delimited, so a newline filename survives), builds ONE
typed ArchivePlanV1 from them, then builds the archive from that plan with anchored no-follow reads
and per-member kind/mode, and finally REOPENS it and verifies the exact member set, types, modes
and hashes. A blocked plan, a containment escape, a missing/extra member or a type/mode mismatch
is a hard failure — nothing rediscovers an authoritative path.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from packages.orchestration.archive_plan import (  # noqa: E402
    ArchivePlanError,
    build_archive_plan,
)
from packages.orchestration.review_zip import (  # noqa: E402
    ReviewZipError,
    build_review_zip_from_plan,
    read_nul_list,
    verify_review_zip,
)


def _load_subject(path: str):
    from packages.orchestration.review_subject import ReviewSubjectV1

    if not path or not os.path.isfile(path):
        return ReviewSubjectV1()
    from packages.orchestration.review_subject import (
        ReviewFileV1, decode_review_subject_from_json,
    )
    try:
        return decode_review_subject_from_json(json.loads(open(path).read()))
    except Exception:
        return ReviewSubjectV1()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--repo-root", required=True)
    ap.add_argument("--repo-files0", required=True, help="NUL-delimited repo context file list")
    ap.add_argument("--evidence-root", default="")
    ap.add_argument("--evidence-files0", default="", help="NUL-delimited evidence file list")
    ap.add_argument("--subject-json", default="", help="review_subject.json (authoritative)")
    ap.add_argument("--manifest-rel", required=True)
    ap.add_argument("--manifest-disk", required=True)
    args = ap.parse_args()

    repo_files = read_nul_list(args.repo_files0)
    evidence_files = read_nul_list(args.evidence_files0) if args.evidence_files0 else []
    evidence_root = args.evidence_root or None
    subject = _load_subject(args.subject_json)

    # The shared authoritative-source predicate. Imported lazily so a minimal packaging
    # environment (no full orchestration stack) can still build a subject-less bundle; when the
    # predicate cannot be loaded there is no authoritative subject to police anyway.
    try:
        from packages.orchestration.repair_attest import is_attestable_source
    except Exception:
        def is_attestable_source(_p):
            return False

    try:
        plan = build_archive_plan(
            repo_root=args.repo_root, subject=subject, repo_context_rel=repo_files,
            evidence_root=evidence_root, evidence_rel=evidence_files,
            is_authoritative_source=is_attestable_source)
        result = build_review_zip_from_plan(
            out_path=args.out, plan=plan, manifest_rel=args.manifest_rel,
            manifest_disk=args.manifest_disk)
        problems = verify_review_zip(args.out, result)
    except (ReviewZipError, ArchivePlanError) as exc:
        print(f"REVIEW_ZIP_ERROR: {exc}", file=sys.stderr)
        return 2

    if problems:
        print("REVIEW_ZIP_VERIFICATION_FAILED:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 3

    authoritative = sum(1 for m in result["model"].values() if m.get("authoritative"))
    symlinks = sum(1 for m in result["model"].values() if m.get("kind") == "symlink")
    print(json.dumps({"member_count": len(result["members"]),
                      "authoritative_count": authoritative,
                      "symlink_count": symlinks,
                      "tombstone_count": len(plan.tombstones)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
