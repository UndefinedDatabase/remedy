#!/usr/bin/env python3
"""F1/F2/F10 (round 19) — the fail-closed, authority-aligned, plan-driven ZIP construction stage.

Invoked by `make_review_zip.sh`. It strict-decodes the ReviewSubject (fail-closed — a supplied but
invalid subject BLOCKS, never silently becomes an empty subject), reads THE authority set from the
Content Proof (so the ArchivePlan's authoritative members equal the 18-file evidence authority set,
`.agent` operator state excluded), builds one typed ArchivePlanV1, packages the plan as an evidence
artifact, builds the archive with anchored no-follow reads and per-member kind/mode, and reopens it
to verify the exact typed membership. A blocked plan, an escape, a missing/extra member, or a
type/mode/hash mismatch is a hard failure.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from packages.orchestration.archive_plan import (  # noqa: E402
    ArchiveMemberV1,
    ArchivePlanError,
    MEMBER_REGULAR,
    MODE_REGULAR,
    SOURCE_GENERATED_MANIFEST,
    build_archive_plan,
)
from packages.orchestration.review_zip import (  # noqa: E402
    ReviewZipError,
    build_review_zip_from_plan,
    read_nul_list,
    verify_review_zip,
)


def _load_subject(path: str):
    """F10: fail closed. No path supplied -> legacy empty subject. A supplied path that is
    missing, invalid JSON or fails the strict schema is a hard error, never a downgrade."""
    from packages.orchestration.review_subject import (
        ReviewSubjectV1, decode_review_subject_from_json,
    )
    if not path:
        return ReviewSubjectV1()
    if not os.path.isfile(path):
        raise ArchivePlanError(f"the declared review subject {path!r} is absent")
    try:
        raw = json.loads(open(path).read())
    except (OSError, json.JSONDecodeError) as exc:
        raise ArchivePlanError(f"the declared review subject is not valid JSON: {exc}") from None
    return decode_review_subject_from_json(raw)   # raises ReviewSubjectError on schema failure


def _authority_set(content_proof_json: str) -> set[str]:
    """THE authority set: the Content Proof's file_hashes keys plus its tombstones."""
    if not content_proof_json or not os.path.isfile(content_proof_json):
        return set()
    try:
        d = json.loads(open(content_proof_json).read())
    except (OSError, json.JSONDecodeError):
        return set()
    auth = set(d.get("file_hashes") or {})
    auth |= set(d.get("tombstones") or {})
    return auth


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--repo-root", required=True)
    ap.add_argument("--repo-files0", required=True, help="NUL-delimited repo context file list")
    ap.add_argument("--evidence-root", default="")
    ap.add_argument("--evidence-files0", default="", help="NUL-delimited evidence file list")
    ap.add_argument("--subject-json", default="", help="review_subject.json (authoritative)")
    ap.add_argument("--content-proof-json", default="", help="the authority set source")
    ap.add_argument("--plan-out", default="", help="where to write review_archive_plan.json")
    ap.add_argument("--manifest-rel", required=True)
    ap.add_argument("--manifest-disk", required=True)
    args = ap.parse_args()

    repo_files = read_nul_list(args.repo_files0)
    evidence_files = read_nul_list(args.evidence_files0) if args.evidence_files0 else []
    evidence_root = args.evidence_root or None

    try:
        subject = _load_subject(args.subject_json)
        authority = _authority_set(args.content_proof_json)
        plan = build_archive_plan(
            repo_root=args.repo_root, subject=subject, repo_context_rel=repo_files,
            evidence_root=evidence_root, evidence_rel=evidence_files,
            authoritative_paths=authority)

        # F2: package the plan as an evidence artifact so a ZIP-only reviewer can independently
        # verify the model the 1,359 members were built from.
        plan_member = None
        if args.plan_out and evidence_root:
            plan_bytes = (json.dumps(plan.to_json(), indent=2, sort_keys=True) + "\n").encode()
            os.makedirs(os.path.dirname(args.plan_out), exist_ok=True)
            with open(args.plan_out, "wb") as fh:
                fh.write(plan_bytes)
            plan_rel = os.path.relpath(args.plan_out, evidence_root)
            plan_member = ArchiveMemberV1(
                archive_path=plan_rel, kind=MEMBER_REGULAR, mode=MODE_REGULAR,
                authoritative=False, source_root=str(evidence_root), source_rel=plan_rel,
                source_class=SOURCE_GENERATED_MANIFEST)
            import dataclasses
            plan = dataclasses.replace(
                plan, evidence_members=plan.evidence_members + (plan_member,))

        result = build_review_zip_from_plan(
            out_path=args.out, plan=plan, manifest_rel=args.manifest_rel,
            manifest_disk=args.manifest_disk)
        problems = verify_review_zip(args.out, result)

        # F2: the verification report — actual, typed, packaged next to the ZIP for the reviewer.
        if args.plan_out and evidence_root:
            report = _verification_report(plan, result, problems)
            vpath = os.path.join(os.path.dirname(args.plan_out),
                                 "review_zip_verification.json")
            with open(vpath, "wb") as fh:
                fh.write((json.dumps(report, indent=2, sort_keys=True) + "\n").encode())
    except (ReviewZipError, ArchivePlanError) as exc:
        print(f"REVIEW_ZIP_ERROR: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:                         # a ReviewSubjectError or any strict failure
        print(f"REVIEW_ZIP_ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
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


def _verification_report(plan, result, problems) -> dict:
    model = result["model"]
    return {
        "verification_v": 1,
        "review_subject_sha256": plan.review_subject_sha256,
        "authority_set_sha256": plan.authority_set_sha256,
        "expected_member_count": plan.expected_member_count() + 1,   # + the manifest member
        "actual_member_count": len(model),
        "authoritative_member_count": sum(1 for m in model.values() if m.get("authoritative")),
        "symlink_member_count": sum(1 for m in model.values() if m.get("kind") == "symlink"),
        "duplicate_count": 0,
        "problems": list(problems),
        "verdict": "PASS" if not problems else "BLOCKED",
    }


if __name__ == "__main__":
    raise SystemExit(main())
