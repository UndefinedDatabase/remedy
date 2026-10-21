"""A finished job's certificate: chosen members, a manifest with claims, and a byte budget.

The certificate is one ZIP holding the members that prove a job's outcome (report, token truth,
verdicts, ownership, run manifest) plus a `manifest.json` that names every member by sha256 and size
and states the job's claims. Large members (a diff, a log) are embedded only while the byte budget
allows; otherwise the manifest references them by sha256, size and where to obtain them (DECISION
F060 D1).

It packs and reopens through the review package's `build_review_zip_from_snapshot` and
`verify_review_zip`, so it needs no checkout to be read back. A certificate proves integrity, not
authorship: it carries no signature.
"""
from __future__ import annotations

import hashlib
import json
import os
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from packages.orchestration.review_zip import (
    ReviewZipError,
    build_review_zip_from_snapshot,
    validate_archive_name,
    verify_review_zip,
)

# WHY: the manifest format version; a reader refuses a bundle_v it does not know.
CERTIFICATE_BUNDLE_V = 1
# WHY: names the kind of bundle so a reader never mistakes a review ZIP for a certificate.
CERTIFICATE_KIND = "remedy-job-certificate"
# WHY: the one reserved member name; no source may take it.
CERTIFICATE_MANIFEST_NAME = "manifest.json"
# WHY: every member is a plain readable file; the mode is part of the verified model.
CERTIFICATE_MEMBER_MODE = 0o644
# WHY: the classes a source may declare; anything else is refused by name.
CERTIFICATE_MEMBER_CLASSES = ("report", "token_truth", "verdicts", "ownership", "run_manifest",
                              "diff", "log")
# WHY: the classes that may be left out of the ZIP and referenced when the budget runs short.
CERTIFICATE_REFERENCED_CLASSES = ("diff", "log")
# WHY: the exact claim set, so a certificate never silently gains or loses a claim.
CERTIFICATE_CLAIM_KEYS = ("terminal_state", "dod_summary", "cost", "cost_basis",
                          "decisions_count", "regression_status")
# WHY: the sentence stored in every manifest so no reader mistakes integrity for authorship.
CERTIFICATE_NOT_A_SIGNATURE = (
    "This certificate proves that its members are intact and agree with each other. "
    "It is not a signature: it does not prove who made it.")


# WHY: one named error for every refusal, so callers catch the certificate and nothing broader.
class CertificateError(Exception):
    """The certificate cannot be built safely. Never downgraded to a warning."""


# WHY: one candidate member with its class and, for a referenced one, where to fetch its bytes.
@dataclass(frozen=True)
class CertificateSource:
    path: str
    member_class: str
    data: bytes
    obtain: str = ""


# WHY: one rendering of the manifest, so the bytes in the ZIP and the golden agree.
def render_certificate_manifest(manifest: dict) -> bytes:
    return (json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode(
        "utf-8")


# WHY: the budget rule in one place: always-embedded first, then diff and log while they fit.
def plan_certificate_members(
        sources: Sequence[CertificateSource], size_budget_bytes: int,
) -> tuple[tuple[CertificateSource, ...], tuple[CertificateSource, ...]]:
    ordered = sorted(sources, key=lambda s: s.path)
    embedded = [s for s in ordered if s.member_class not in CERTIFICATE_REFERENCED_CLASSES]
    total = sum(len(s.data) for s in embedded)
    if total > size_budget_bytes:
        raise CertificateError(
            f"The certificate's always-embedded members hold {total} bytes, more than its "
            f"budget of {size_budget_bytes} bytes.")
    referenced: list[CertificateSource] = []
    for s in ordered:
        if s.member_class not in CERTIFICATE_REFERENCED_CLASSES:
            continue
        if total + len(s.data) <= size_budget_bytes:
            embedded.append(s)
            total += len(s.data)
        else:
            referenced.append(s)
    embedded.sort(key=lambda s: s.path)
    return tuple(embedded), tuple(referenced)


def _is_plain_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _check_inputs(job_id, created, issue, size_budget_bytes, sources, claims) -> None:
    if not job_id:
        raise CertificateError(f"job_id must not be empty: {job_id!r}")
    if not created:
        raise CertificateError(f"created must not be empty: {created!r}")
    if not _is_plain_int(issue) or issue < 1:
        raise CertificateError(f"issue must be an int of at least 1: {issue!r}")
    if not _is_plain_int(size_budget_bytes) or size_budget_bytes < 1:
        raise CertificateError(
            f"size_budget_bytes must be an int of at least 1: {size_budget_bytes!r}")
    if not sources:
        raise CertificateError("a certificate needs at least one source")
    seen: set[str] = set()
    for s in sources:
        try:
            validate_archive_name(s.path)
        except ReviewZipError as exc:
            raise CertificateError(f"source path {s.path!r} is not a safe name: {exc}") from None
        if s.path == CERTIFICATE_MANIFEST_NAME:
            raise CertificateError(f"source path {s.path!r} is reserved for the manifest")
        if s.path in seen:
            raise CertificateError(f"source path {s.path!r} is repeated")
        seen.add(s.path)
        if s.member_class not in CERTIFICATE_MEMBER_CLASSES:
            raise CertificateError(
                f"source {s.path!r} has an unknown class {s.member_class!r}")
        if not isinstance(s.data, bytes):
            raise CertificateError(f"source {s.path!r} data must be bytes, not "
                                   f"{type(s.data).__name__}")
        if s.member_class in CERTIFICATE_REFERENCED_CLASSES and not s.obtain:
            raise CertificateError(
                f"source {s.path!r} of class {s.member_class!r} needs an obtain sentence")
    keys = set(claims)
    want = set(CERTIFICATE_CLAIM_KEYS)
    if keys != want:
        raise CertificateError(
            f"claims must carry exactly the claim keys; missing {sorted(want - keys)}, "
            f"extra {sorted(keys - want)}")
    try:
        json.dumps(dict(claims))
    except (TypeError, ValueError) as exc:
        raise CertificateError(f"claims cannot be written as JSON: {exc}") from None


def _overwrite_sentence(out_path) -> str:
    return f"A certificate already exists at {out_path}; Remedy never overwrites one."


# WHY: the one entry point that turns a finished job's sources and claims into a verified ZIP.
def build_job_certificate(*, out_path: str | Path, job_id: str, project_id: str, created: str,
                          issue: int, sources: Sequence[CertificateSource],
                          claims: Mapping[str, object], size_budget_bytes: int) -> dict:
    _check_inputs(job_id, created, issue, size_budget_bytes, sources, claims)

    if os.path.lexists(out_path):
        raise CertificateError(_overwrite_sentence(out_path))
    final = Path(out_path)
    if not final.parent.is_dir():
        raise CertificateError(f"The folder for the certificate does not exist: {final.parent}")

    embedded, referenced = plan_certificate_members(sources, size_budget_bytes)
    manifest = {
        "bundle_v": CERTIFICATE_BUNDLE_V,
        "kind": CERTIFICATE_KIND,
        "job": job_id,
        "project": project_id,
        "created": created,
        "issue": issue,
        "size_budget_bytes": size_budget_bytes,
        "members": [{"path": s.path, "class": s.member_class,
                     "sha256": hashlib.sha256(s.data).hexdigest(), "size": len(s.data)}
                    for s in embedded],
        "referenced": [{"path": s.path, "class": s.member_class,
                        "sha256": hashlib.sha256(s.data).hexdigest(), "size": len(s.data),
                        "obtain": s.obtain} for s in referenced],
        "claims": dict(claims),
        "signature": None,
        "not_a_signature": CERTIFICATE_NOT_A_SIGNATURE,
    }

    generated = {s.path: (s.data, CERTIFICATE_MEMBER_MODE) for s in embedded}
    generated[CERTIFICATE_MANIFEST_NAME] = (render_certificate_manifest(manifest),
                                            CERTIFICATE_MEMBER_MODE)
    tmp = final.parent / f".{final.name}.{os.getpid()}.part"
    try:
        try:
            result = build_review_zip_from_snapshot(out_path=tmp, snapshot={},
                                                    generated_members=generated)
        except ReviewZipError as exc:
            raise CertificateError(f"the certificate could not be packed: {exc}") from None
        problems = verify_review_zip(tmp, result)
        if problems:
            raise CertificateError(f"the certificate failed its reopen check: {problems[0]}")
        try:
            os.link(tmp, final)
        except FileExistsError:
            raise CertificateError(_overwrite_sentence(out_path)) from None
    finally:
        if os.path.lexists(tmp):
            os.unlink(tmp)
    return {"path": final, "manifest": manifest, "members": result["members"]}
