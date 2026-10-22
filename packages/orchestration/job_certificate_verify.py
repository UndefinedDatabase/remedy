"""Checks a job certificate: its members' integrity first, its claims second (F060, DECISION F060 D3).

`verify_job_certificate` first holds the ZIP to the manifest it carries: the manifest's own shape, then
every embedded member's name, type, mode, size and sha256, through the review package's
`verify_review_zip`. Only when nothing is wrong there does it check the claims: the claimed terminal
state against the report, and the cost, the Definition-of-Done summary and the regression status
against the member each is derived from, so a member doctored together with its hash is still caught.

It needs no Remedy data folder and no checkout: everything it reads is in the bundle. A certificate
proves that its members are intact and agree with each other; it is not a signature and does not
prove who made it.
"""
from __future__ import annotations

import hashlib
import json
import re
import zipfile
import zlib
from dataclasses import dataclass
from pathlib import Path

from packages.orchestration.archive_plan import MAX_GENERATED_MEMBER_BYTES
from packages.orchestration.job_certificate import (
    CERTIFICATE_BUNDLE_V,
    CERTIFICATE_CLAIM_KEYS,
    CERTIFICATE_KIND,
    CERTIFICATE_MANIFEST_NAME,
    CERTIFICATE_MEMBER_CLASSES,
    CERTIFICATE_MEMBER_MODE,
    CERTIFICATE_NOT_A_SIGNATURE,
    CERTIFICATE_REFERENCED_CLASSES,
)
from packages.orchestration.job_certificate_claims import (
    cost_claims_from_member,
    dod_summary_from_member,
    regression_status_from_member,
)
from packages.orchestration.job_certificate_sources import CERTIFICATE_TERMINAL_STATES
from packages.orchestration.review_zip import verify_review_zip

# The keys a version 1 manifest carries (DECISION F060 D1 (2)).
_MANIFEST_KEYS = ("bundle_v", "kind", "job", "project", "created", "issue", "size_budget_bytes",
                  "members", "referenced", "claims", "signature", "not_a_signature")
_SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")
# What opening or reading a damaged archive may raise.
_ZIP_READ_ERRORS = (zipfile.BadZipFile, OSError, zlib.error, NotImplementedError, RuntimeError)
_BUDGET_MEMBER = "token/budget_actuals.json"
_DOD_MEMBER = "verdicts/dod_result.json"
_VERIFIER_MEMBER = "verdicts/final_verifier_report.json"
# Each derived claim: its key, the member it comes from and the function that derives it from the
# member's bytes (None when the member is absent).
_DERIVED_CLAIMS = {
    "cost": (_BUDGET_MEMBER, lambda data: cost_claims_from_member(data)[0]),
    "cost_basis": (_BUDGET_MEMBER, lambda data: cost_claims_from_member(data)[1]),
    "dod_summary": (_DOD_MEMBER, dod_summary_from_member),
    "regression_status": (_VERIFIER_MEMBER, regression_status_from_member),
}


# WHY: one answer for the command and the tests: whether it holds, why not, and what it claims.
@dataclass(frozen=True)
class CertificateVerification:
    ok: bool
    problems: tuple[str, ...]
    # None when no manifest could be read.
    manifest: dict | None


def _is_plain_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _refused(problem: str) -> CertificateVerification:
    return CertificateVerification(ok=False, problems=(problem,), manifest=None)


def _read_manifest_bytes(bundle_path: str | Path) -> tuple[bytes | None, str | None]:
    """The manifest's bytes, or the one sentence that says why they cannot be read."""
    if not zipfile.is_zipfile(bundle_path):
        return None, f"{bundle_path} is not a ZIP archive."
    try:
        with zipfile.ZipFile(bundle_path, "r") as zf:
            try:
                info = zf.getinfo(CERTIFICATE_MANIFEST_NAME)
            except KeyError:
                return None, "The bundle holds no manifest.json."
            if info.file_size > MAX_GENERATED_MEMBER_BYTES:
                return None, (f"manifest.json holds {info.file_size} bytes, more than the "
                              f"{MAX_GENERATED_MEMBER_BYTES} bytes a manifest may hold; it is not read.")
            with zf.open(info) as handle:
                data = handle.read(MAX_GENERATED_MEMBER_BYTES + 1)
    except _ZIP_READ_ERRORS as exc:
        return None, f"{bundle_path} could not be read as a ZIP archive: {exc}"
    if len(data) > MAX_GENERATED_MEMBER_BYTES:
        return None, (f"manifest.json holds more than the {MAX_GENERATED_MEMBER_BYTES} bytes a "
                      f"manifest may hold; it is not read.")
    return data, None


def _entry_is_wellformed(entry: object, *, referenced: bool) -> bool:
    if not isinstance(entry, dict):
        return False
    if not isinstance(entry.get("path"), str):
        return False
    if entry.get("class") not in CERTIFICATE_MEMBER_CLASSES:
        return False
    sha = entry.get("sha256")
    if not isinstance(sha, str) or _SHA256_PATTERN.fullmatch(sha) is None:
        return False
    size = entry.get("size")
    if not isinstance(size, int) or not _is_plain_int(size) or size < 0:
        return False
    return not referenced or isinstance(entry.get("obtain"), str)


def _manifest_problems(manifest: dict) -> list[str]:
    problems: list[str] = []
    if "bundle_v" in manifest:
        version = manifest["bundle_v"]
        if not (_is_plain_int(version) and version == CERTIFICATE_BUNDLE_V):
            problems.append(f"manifest.json names bundle_v {version!r}; this Remedy reads "
                            f"bundle_v {CERTIFICATE_BUNDLE_V}.")
    if "kind" in manifest and manifest["kind"] != CERTIFICATE_KIND:
        problems.append(f"manifest.json names kind {manifest['kind']!r}, not {CERTIFICATE_KIND}.")
    if manifest.get("signature") is not None:
        problems.append("manifest.json carries a signature, which version 1 reserves and leaves "
                        "empty.")
    for key in _MANIFEST_KEYS:
        if key not in manifest:
            problems.append(f"manifest.json lacks the key {key!r}.")
    for field, referenced in (("members", False), ("referenced", True)):
        entries = manifest.get(field)
        if field not in manifest:
            continue
        if not isinstance(entries, list):
            problems.append(f"manifest.json {field} entry 0 is malformed.")
            continue
        for index, entry in enumerate(entries):
            if not _entry_is_wellformed(entry, referenced=referenced):
                problems.append(f"manifest.json {field} entry {index} is malformed.")
                continue
            if referenced and entry["class"] not in CERTIFICATE_REFERENCED_CLASSES:
                problems.append(f"Referenced member {entry['path']!r} is of class "
                                f"{entry['class']!r}, which a certificate always embeds.")
    return problems


def _integrity_problems(bundle_path: str | Path, manifest: dict, manifest_bytes: bytes) -> list[str]:
    model = {entry["path"]: {"kind": "regular", "mode": CERTIFICATE_MEMBER_MODE,
                             "sha256": entry["sha256"], "size": entry["size"]}
             for entry in manifest["members"]}
    model[CERTIFICATE_MANIFEST_NAME] = {
        "kind": "regular", "mode": CERTIFICATE_MEMBER_MODE,
        "sha256": hashlib.sha256(manifest_bytes).hexdigest(), "size": len(manifest_bytes)}
    try:
        problems = list(verify_review_zip(bundle_path, {"model": model}))
    except _ZIP_READ_ERRORS as exc:
        return [f"{bundle_path} could not be read as a ZIP archive: {exc}"]
    budget = manifest["size_budget_bytes"]
    total = sum(entry["size"] for entry in manifest["members"])
    if _is_plain_int(budget) and total > budget:
        problems.append(f"The embedded members hold {total} bytes, more than the manifest's "
                        f"budget of {budget} bytes.")
    return problems


def _member_bytes(zf: zipfile.ZipFile, path: str) -> bytes | None:
    try:
        return zf.read(path)
    except KeyError:
        return None


def _claim_problems(bundle_path: str | Path, manifest: dict) -> list[str]:
    claims = manifest["claims"]
    keys = set(claims) if isinstance(claims, dict) else set()
    if keys != set(CERTIFICATE_CLAIM_KEYS):
        return [f"The claims carry the keys {sorted(keys)}, not {sorted(CERTIFICATE_CLAIM_KEYS)}."]
    problems: list[str] = []
    state = claims["terminal_state"]
    if state not in CERTIFICATE_TERMINAL_STATES:
        problems.append(f"The claimed terminal state {state!r} is not a state in which a job has "
                        f"ended.")
    report_path = next((e["path"] for e in manifest["members"] if e["class"] == "report"), None)
    try:
        with zipfile.ZipFile(bundle_path, "r") as zf:
            if report_path is None:
                problems.append("The bundle holds no report to check the claimed terminal state "
                                "against.")
            else:
                text = (_member_bytes(zf, report_path) or b"").decode("utf-8", errors="replace")
                if f"- State: {state}" not in text.splitlines():
                    problems.append(f"Member {report_path}: its State line does not name the "
                                    f"claimed terminal state {state}.")
            for key, (path, derive) in _DERIVED_CLAIMS.items():
                data = _member_bytes(zf, path)
                derived = derive(data)
                if derived != claims[key]:
                    present = "present" if data is not None else "absent"
                    problems.append(f"Member {path} ({present}) gives the {key} {derived!r}, but "
                                    f"the claims say {claims[key]!r}.")
    except _ZIP_READ_ERRORS as exc:
        problems.append(f"{bundle_path} could not be read as a ZIP archive: {exc}")
    count = claims["decisions_count"]
    if not _is_plain_int(count) or count < 0:
        problems.append(f"The claimed decisions count {count!r} is not a whole number of zero or "
                        f"more.")
    return problems


# WHY: the one check of a certificate, so the command and the tests ask the same question.
def verify_job_certificate(bundle_path: str | Path) -> CertificateVerification:
    data, why_not = _read_manifest_bytes(bundle_path)
    if data is None:
        return _refused(why_not or f"{bundle_path} is not a ZIP archive.")
    try:
        manifest = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        manifest = None
    if not isinstance(manifest, dict):
        return _refused("manifest.json is not a JSON object.")

    problems = _manifest_problems(manifest)
    if not problems:
        problems = _integrity_problems(bundle_path, manifest, data)
    if not problems:
        problems = _claim_problems(bundle_path, manifest)
    return CertificateVerification(ok=not problems, problems=tuple(problems), manifest=manifest)


def _text_or_repr(value: object) -> str:
    return value if isinstance(value, str) else repr(value)


def _dod_text(dod: object) -> str:
    if dod is None:
        return "not recorded"
    if (isinstance(dod, dict) and set(dod) == {"released", "check_count", "passed_count"}
            and _is_plain_int(dod["check_count"]) and _is_plain_int(dod["passed_count"])):
        return (f"{dod['passed_count']} of {dod['check_count']} checks passed, released "
                f"{'yes' if dod['released'] else 'no'}")
    return repr(dod)


def _basis_text(basis: object) -> str:
    if isinstance(basis, list) and all(isinstance(item, str) for item in basis):
        return ", ".join(basis) if basis else "none"
    return repr(basis)


def _optional_text(value: object) -> str:
    return "not recorded" if value is None else _text_or_repr(value)


def _count_of(entries: object) -> int:
    return len(entries) if isinstance(entries, list) else 0


# WHY: the verdict says how the run ended before it says whether the file is sound, so an intact
# certificate of a failed run never reads as a success.
def render_certificate_verdict(verification: CertificateVerification) -> str:
    manifest = verification.manifest
    lines: list[str] = []
    if manifest is None:
        lines.append("Run ended: unknown — the certificate's manifest could not be read.")
    else:
        claims = manifest.get("claims")
        claims = claims if isinstance(claims, dict) else {}
        lines.append(f"Run ended: {_text_or_repr(claims.get('terminal_state'))}")
        project = manifest.get("project")
        lines.append(f"Job {manifest.get('job')} of project {project or '(none)'}, certificate "
                     f"issue {manifest.get('issue')}, created {manifest.get('created')}.")
        lines.append(
            f"Claims: Definition of Done {_dod_text(claims.get('dod_summary'))}; "
            f"cost {_optional_text(claims.get('cost'))} "
            f"(basis: {_basis_text(claims.get('cost_basis'))}); "
            f"decisions {claims.get('decisions_count')!r}; "
            f"regression status {_optional_text(claims.get('regression_status'))}.")
        lines.append(f"Members: {_count_of(manifest.get('members'))} embedded, "
                     f"{_count_of(manifest.get('referenced'))} referenced.")
    if verification.ok:
        lines.append("Certificate: intact — every member matches its hash and every claim agrees "
                     "with its member.")
    else:
        lines.append(f"Certificate: NOT INTACT — {len(verification.problems)} problem(s):")
        lines.extend(f"  - {problem}" for problem in verification.problems)
    lines.append(CERTIFICATE_NOT_A_SIGNATURE)
    return "\n".join(lines) + "\n"
