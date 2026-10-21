"""The certificate verifier: its tamper matrix, its claim checks and its verdict (F060 T002, DECISION F060 D3)."""
from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

import pytest

from packages.core.models import RunState
from packages.orchestration.archive_plan import MAX_GENERATED_MEMBER_BYTES
from packages.orchestration.job_certificate import (
    CERTIFICATE_DEFAULT_MAX_BYTES,
    CERTIFICATE_NOT_A_SIGNATURE,
    CertificateSource,
    build_job_certificate,
    render_certificate_manifest,
)
from packages.orchestration.job_certificate_claims import (
    cost_claims_from_member,
    dod_summary_from_member,
    regression_status_from_member,
)
from packages.orchestration.job_certificate_sources import collect_certificate_inputs
from packages.orchestration.job_certificate_verify import (
    CertificateVerification,
    render_certificate_verdict,
    verify_job_certificate,
)
from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan

STARTED = "2026-10-01T00:00:00+00:00"
CREATED = "2026-10-21T00:00:00Z"
GOOD_ACTUALS = {
    "schema_version": "2.0.0", "provider_call_count": 2, "actual_call_count": 2,
    "unmeasured_call_count": 0, "total_tokens": 10, "actual_sources": ["pingpong_actuals"],
    "started_at": STARTED, "measured_cost_usd": 0.5, "priced_call_count": 2,
    "unpriced_call_count": 0,
}
DIFF_BYTES = b"--- a/x\n+++ b/x\n@@ -1 +1 @@\n-old\n+new\n"
REPORT = b"# Run report\n\n- State: completed\n"
BUDGET = json.dumps({"budget_actuals": GOOD_ACTUALS, "first_running_at": STARTED},
                    indent=2, sort_keys=True).encode() + b"\n"
DOD = json.dumps({"released": True, "checks": [
    {"status": "passed"}, {"status": "passed"}, {"status": "failed"}]}).encode() + b"\n"
VERIFIER = b'{"test_status": "passed"}\n'

# One member of each of the seven classes: path -> (class, bytes).
MEMBERS = {
    "report.md": ("report", REPORT),
    "token/budget_actuals.json": ("token_truth", BUDGET),
    "verdicts/dod_result.json": ("verdicts", DOD),
    "verdicts/final_verifier_report.json": ("verdicts", VERIFIER),
    "ownership/ownership.json": ("ownership", b'{"o": 1}\n'),
    "run_manifest/run_manifest.json": ("run_manifest", b'{"m": 1}\n'),
    "diff/result.diff": ("diff", DIFF_BYTES),
    "logs/run.jsonl": ("log", b'{"e": 1}\n'),
}
# The member each class is tampered through.
TAMPER_PATH = {
    "report": "report.md",
    "token_truth": "token/budget_actuals.json",
    "verdicts": "verdicts/dod_result.json",
    "ownership": "ownership/ownership.json",
    "run_manifest": "run_manifest/run_manifest.json",
    "diff": "diff/result.diff",
    "log": "logs/run.jsonl",
}
COST = cost_claims_from_member(BUDGET)[0]
DOD_SUMMARY = {"released": True, "check_count": 3, "passed_count": 2}


def _sources() -> list[CertificateSource]:
    return [CertificateSource(path, cls, data,
                              obtain="Fetch it." if cls in ("diff", "log") else "")
            for path, (cls, data) in MEMBERS.items()]


def _claims() -> dict:
    cost, basis = cost_claims_from_member(BUDGET)
    return {
        "terminal_state": "completed",
        "dod_summary": dod_summary_from_member(DOD),
        "cost": cost,
        "cost_basis": basis,
        "decisions_count": 2,
        "regression_status": regression_status_from_member(VERIFIER),
    }


def _build(tmp_path: Path, name: str = "cert.zip") -> Path:
    out = tmp_path / name
    build_job_certificate(
        out_path=out, job_id="job-1", project_id="proj", created=CREATED, issue=1,
        sources=_sources(), claims=_claims(), size_budget_bytes=CERTIFICATE_DEFAULT_MAX_BYTES)
    return out


def _write_member(zf: zipfile.ZipFile, name: str, data: bytes) -> None:
    info = zipfile.ZipInfo(filename=name, date_time=(1980, 1, 1, 0, 0, 0))
    info.create_system = 3
    info.external_attr = (0o100000 | 0o644) << 16
    info.compress_type = zipfile.ZIP_DEFLATED
    zf.writestr(info, data)


def _rewrite(src: Path, dst: Path, *, replace=None, remove=(), add=None, edit_manifest=None,
             manifest_bytes: bytes | None = None) -> Path:
    """A copy of a certificate with one change, every member written with the package's metadata."""
    replace, add = replace or {}, add or {}
    with zipfile.ZipFile(src) as zf:
        members = {n: zf.read(n) for n in zf.namelist()}
    if edit_manifest is not None:
        manifest = json.loads(members["manifest.json"])
        edit_manifest(manifest)
        members["manifest.json"] = render_certificate_manifest(manifest)
    if manifest_bytes is not None:
        members["manifest.json"] = manifest_bytes
    members.update(replace)
    for name in remove:
        del members[name]
    members.update(add)
    with zipfile.ZipFile(dst, "w") as zf:
        for name, data in members.items():
            _write_member(zf, name, data)
    return dst


def _doctor(tmp_path: Path, path: str, data: bytes) -> Path:
    """Change one member and rewrite its sha256 and size in the manifest to match."""
    def edit(manifest: dict) -> None:
        for entry in manifest["members"]:
            if entry["path"] == path:
                entry["sha256"] = hashlib.sha256(data).hexdigest()
                entry["size"] = len(data)
    return _rewrite(_build(tmp_path), tmp_path / "doctored.zip", replace={path: data},
                    edit_manifest=edit)


def _same_length_change(data: bytes) -> bytes:
    return data[:-2] + b"X" + data[-1:]


def test_the_fixture_verifies_and_its_verdict_reads_as_written(tmp_path):
    verification = verify_job_certificate(_build(tmp_path))
    assert verification.ok is True
    assert verification.problems == ()
    assert verification.manifest["job"] == "job-1"
    assert render_certificate_verdict(verification) == (
        "Run ended: completed\n"
        "Job job-1 of project proj, certificate issue 1, created 2026-10-21T00:00:00Z.\n"
        "Claims: Definition of Done 2 of 3 checks passed, released yes; cost $0.5000 "
        "(basis: pingpong_actuals); decisions 2; regression status passed.\n"
        "Members: 8 embedded, 0 referenced.\n"
        "Certificate: intact — every member matches its hash and every claim agrees with its "
        "member.\n"
        f"{CERTIFICATE_NOT_A_SIGNATURE}\n")


def test_a_failed_jobs_certificate_made_from_its_record_verifies(tmp_path):
    job = JobPlan(job_title="certificate-job", user_prompt="build the thing",
                  tasks=[TaskEntry(title="task 0", inputs={"task_type": "documentation"})],
                  state=RunState.FAILED, metadata={"target_repo": "/repo/fixture"})
    save_job_plan(job)
    inputs = collect_certificate_inputs(str(job.job_id))
    out = tmp_path / "failed.zip"
    build_job_certificate(
        out_path=out, job_id=inputs.job_id, project_id=inputs.project_id, created=CREATED,
        issue=inputs.issue, sources=inputs.sources, claims=inputs.claims,
        size_budget_bytes=CERTIFICATE_DEFAULT_MAX_BYTES)
    verification = verify_job_certificate(out)
    assert verification.problems == ()
    assert verification.ok is True
    verdict = render_certificate_verdict(verification)
    assert verdict.splitlines()[0] == "Run ended: failed"
    assert "Claims: Definition of Done not recorded; cost not recorded (basis: none); " in verdict


@pytest.mark.parametrize("member_class", list(TAMPER_PATH))
def test_one_members_changed_bytes_are_named(tmp_path, member_class):
    path = TAMPER_PATH[member_class]
    data = MEMBERS[path][1]
    bundle = _rewrite(_build(tmp_path), tmp_path / "bad.zip",
                      replace={path: _same_length_change(data)})
    verification = verify_job_certificate(bundle)
    assert verification.ok is False
    assert verification.problems == (f"member {path!r} hash changed after build",)


@pytest.mark.parametrize("member_class", list(TAMPER_PATH))
def test_a_removed_member_is_named(tmp_path, member_class):
    path = TAMPER_PATH[member_class]
    bundle = _rewrite(_build(tmp_path), tmp_path / "bad.zip", remove=[path])
    verification = verify_job_certificate(bundle)
    assert verification.ok is False
    assert verification.problems == (f"expected member missing from archive: {path!r}",)


def test_an_unlisted_member_is_named(tmp_path):
    bundle = _rewrite(_build(tmp_path), tmp_path / "bad.zip", add={"extra/notes.txt": b"hi\n"})
    verification = verify_job_certificate(bundle)
    assert verification.ok is False
    assert verification.problems == ("unexpected member in archive: 'extra/notes.txt'",)


def test_a_manifest_hash_that_no_longer_matches_its_member_names_the_member(tmp_path):
    def edit(manifest: dict) -> None:
        manifest["members"][0]["sha256"] = "0" * 64
    bundle = _rewrite(_build(tmp_path), tmp_path / "bad.zip", edit_manifest=edit)
    first = json.loads(zipfile.ZipFile(bundle).read("manifest.json"))["members"][0]["path"]
    verification = verify_job_certificate(bundle)
    assert verification.problems == (f"member {first!r} hash changed after build",)


def test_a_doctored_report_with_rewritten_hashes_is_caught_by_the_claim_check(tmp_path):
    bundle = _doctor(tmp_path, "report.md", b"# Run report\n\n- State: failed\n")
    verification = verify_job_certificate(bundle)
    assert verification.ok is False
    assert verification.problems == (
        "Member report.md: its State line does not name the claimed terminal state completed.",)


def test_a_doctored_cost_with_rewritten_hashes_is_caught_by_the_claim_check(tmp_path):
    actuals = dict(GOOD_ACTUALS, measured_cost_usd=0.9)
    data = json.dumps({"budget_actuals": actuals, "first_running_at": STARTED}).encode()
    new_cost = cost_claims_from_member(data)[0]
    assert new_cost != COST
    verification = verify_job_certificate(_doctor(tmp_path, "token/budget_actuals.json", data))
    assert verification.ok is False
    assert verification.problems == (
        f"Member token/budget_actuals.json (present) gives the cost {new_cost!r}, but the "
        f"claims say {COST!r}.",)


def _claims_edit(key: str, value):
    def edit(manifest: dict) -> None:
        manifest["claims"][key] = value
    return edit


def _drop_claim(manifest: dict) -> None:
    del manifest["claims"]["cost"]


CLAIM_CASES = [
    pytest.param(
        _claims_edit("dod_summary", {"released": True, "check_count": 9, "passed_count": 9}),
        ("Member verdicts/dod_result.json (present) gives the dod_summary "
         f"{DOD_SUMMARY!r}, but the claims say "
         "{'check_count': 9, 'passed_count': 9, 'released': True}.",),
        id="dod-summary"),
    pytest.param(
        _claims_edit("regression_status", "failed"),
        ("Member verdicts/final_verifier_report.json (present) gives the regression_status "
         "'passed', but the claims say 'failed'.",),
        id="regression-status"),
    pytest.param(
        _claims_edit("cost_basis", []),
        ("Member token/budget_actuals.json (present) gives the cost_basis ['pingpong_actuals'], "
         "but the claims say [].",),
        id="cost-basis"),
    pytest.param(
        _drop_claim,
        ("The claims carry the keys ['cost_basis', 'decisions_count', 'dod_summary', "
         "'regression_status', 'terminal_state'], not ['cost', 'cost_basis', 'decisions_count', "
         "'dod_summary', 'regression_status', 'terminal_state'].",),
        id="claim-removed"),
    pytest.param(
        _claims_edit("terminal_state", "running"),
        ("The claimed terminal state 'running' is not a state in which a job has ended.",
         "Member report.md: its State line does not name the claimed terminal state running."),
        id="terminal-state-running"),
    pytest.param(
        _claims_edit("decisions_count", -1),
        ("The claimed decisions count -1 is not a whole number of zero or more.",),
        id="decisions-negative"),
    pytest.param(
        _claims_edit("decisions_count", True),
        ("The claimed decisions count True is not a whole number of zero or more.",),
        id="decisions-bool"),
]


@pytest.mark.parametrize(("edit", "expected"), CLAIM_CASES)
def test_claims_rewritten_in_the_manifest_are_each_refused_exactly(tmp_path, edit, expected):
    bundle = _rewrite(_build(tmp_path), tmp_path / "bad.zip", edit_manifest=edit)
    verification = verify_job_certificate(bundle)
    assert verification.ok is False
    assert verification.problems == expected


def _edit_key(key: str, value):
    def edit(manifest: dict) -> None:
        manifest[key] = value
    return edit


def _drop_key(manifest: dict) -> None:
    del manifest["job"]


def _malform_member(manifest: dict) -> None:
    manifest["members"][0]["sha256"] = "XYZ"


def _reference_a_report(manifest: dict) -> None:
    manifest["referenced"].append({"path": "report2.md", "class": "report", "sha256": "a" * 64,
                                   "size": 1, "obtain": "Fetch it."})


EMBEDDED_TOTAL = sum(len(data) for _cls, data in MEMBERS.values())


def _missing(path: Path) -> Path:
    return path / "no-such-file.zip"


def _text_file(path: Path) -> Path:
    target = path / "plain.zip"
    target.write_text("not a zip", encoding="utf-8")
    return target


def _without_manifest(path: Path) -> Path:
    target = path / "bare.zip"
    with zipfile.ZipFile(target, "w") as zf:
        _write_member(zf, "report.md", REPORT)
    return target


def _with_manifest_bytes(data: bytes):
    def make(path: Path) -> Path:
        return _rewrite(_build(path), path / "bad.zip", manifest_bytes=data)
    return make


def _with_manifest_edit(edit):
    def make(path: Path) -> Path:
        return _rewrite(_build(path), path / "bad.zip", edit_manifest=edit)
    return make


def _oversized_manifest(path: Path) -> Path:
    target = path / "huge.zip"
    with zipfile.ZipFile(target, "w") as zf:
        _write_member(zf, "manifest.json", b" " * (MAX_GENERATED_MEMBER_BYTES + 1))
    return target


REFUSALS = [
    pytest.param(_text_file, lambda p: (f"{p / 'plain.zip'} is not a ZIP archive.",), True,
                 id="not-a-zip"),
    pytest.param(_missing, lambda p: (f"{p / 'no-such-file.zip'} is not a ZIP archive.",), True,
                 id="missing-file"),
    pytest.param(_without_manifest, lambda p: ("The bundle holds no manifest.json.",), True,
                 id="no-manifest"),
    pytest.param(_oversized_manifest,
                 lambda p: (f"manifest.json holds {MAX_GENERATED_MEMBER_BYTES + 1} bytes, more "
                            f"than the {MAX_GENERATED_MEMBER_BYTES} bytes a manifest may hold; "
                            f"it is not read.",), True, id="manifest-too-large"),
    pytest.param(_with_manifest_bytes(b"[1, 2]"),
                 lambda p: ("manifest.json is not a JSON object.",), True, id="manifest-a-list"),
    pytest.param(_with_manifest_bytes(b"\xff\xfe"),
                 lambda p: ("manifest.json is not a JSON object.",), True,
                 id="manifest-not-utf8"),
    pytest.param(_with_manifest_edit(_edit_key("bundle_v", 2)),
                 lambda p: ("manifest.json names bundle_v 2; this Remedy reads bundle_v 1.",),
                 False, id="bundle-v-2"),
    pytest.param(_with_manifest_edit(_edit_key("kind", "remedy-review-zip")),
                 lambda p: ("manifest.json names kind 'remedy-review-zip', not "
                            "remedy-job-certificate.",), False, id="another-kind"),
    pytest.param(_with_manifest_edit(_edit_key("signature", "abc")),
                 lambda p: ("manifest.json carries a signature, which version 1 reserves and "
                            "leaves empty.",), False, id="signature"),
    pytest.param(_with_manifest_edit(_drop_key),
                 lambda p: ("manifest.json lacks the key 'job'.",), False, id="missing-key"),
    pytest.param(_with_manifest_edit(_malform_member),
                 lambda p: ("manifest.json members entry 0 is malformed.",), False,
                 id="malformed-member-entry"),
    pytest.param(_with_manifest_edit(_reference_a_report),
                 lambda p: ("Referenced member 'report2.md' is of class 'report', which a "
                            "certificate always embeds.",), False, id="referenced-report"),
    pytest.param(_with_manifest_edit(_edit_key("size_budget_bytes", 1)),
                 lambda p: (f"The embedded members hold {EMBEDDED_TOTAL} bytes, more than the "
                            f"manifest's budget of 1 bytes.",), False, id="budget-too-small"),
]


@pytest.mark.parametrize(("make", "expected", "no_manifest"), REFUSALS)
def test_a_refused_bundle_gets_exactly_its_sentence(tmp_path, make, expected, no_manifest):
    verification = verify_job_certificate(make(tmp_path))
    assert verification.ok is False
    assert verification.problems == expected(tmp_path)
    assert (verification.manifest is None) is no_manifest


def test_a_broken_certificates_verdict_lists_every_problem_and_ends_with_the_not_a_signature_line(
        tmp_path):
    bundle = _rewrite(_build(tmp_path), tmp_path / "bad.zip",
                      replace={"ownership/ownership.json": b'{"o": 2}\n'},
                      remove=["logs/run.jsonl"])
    verification = verify_job_certificate(bundle)
    assert isinstance(verification, CertificateVerification)
    assert len(verification.problems) == 2
    lines = render_certificate_verdict(verification).splitlines()
    assert lines[0] == "Run ended: completed"
    assert lines[-1] == CERTIFICATE_NOT_A_SIGNATURE
    assert lines[-4] == "Certificate: NOT INTACT — 2 problem(s):"
    assert lines[-3:-1] == [f"  - {problem}" for problem in verification.problems]
    assert render_certificate_verdict(verification).endswith("\n")


def test_the_verdict_of_a_bundle_with_no_manifest_says_so(tmp_path):
    verification = verify_job_certificate(_text_file(tmp_path))
    assert render_certificate_verdict(verification) == (
        "Run ended: unknown — the certificate's manifest could not be read.\n"
        f"Certificate: NOT INTACT — 1 problem(s):\n"
        f"  - {tmp_path / 'plain.zip'} is not a ZIP archive.\n"
        f"{CERTIFICATE_NOT_A_SIGNATURE}\n")
