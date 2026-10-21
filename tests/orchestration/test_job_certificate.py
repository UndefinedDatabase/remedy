"""Goldens and the budget, overwrite and refusal tests of the job certificate profile (F060 T001)."""
from __future__ import annotations

import hashlib
import zipfile
from dataclasses import replace

import pytest

import packages.orchestration.job_certificate as jc
from packages.orchestration.job_certificate import (
    CERTIFICATE_BUNDLE_V,
    CERTIFICATE_CLAIM_KEYS,
    CERTIFICATE_KIND,
    CERTIFICATE_NOT_A_SIGNATURE,
    CertificateError,
    CertificateSource,
    build_job_certificate,
    render_certificate_manifest,
)

GOLDEN_MANIFEST = """{
  "bundle_v": 1,
  "claims": {
    "cost": 0.5,
    "cost_basis": "metered",
    "decisions_count": 2,
    "dod_summary": "3 of 3 met",
    "regression_status": "clean",
    "terminal_state": "done"
  },
  "created": "2026-10-21T00:00:00Z",
  "issue": 1,
  "job": "job-fixture",
  "kind": "remedy-job-certificate",
  "members": [
    {
      "class": "diff",
      "path": "changes.diff",
      "sha256": "6e53bf2ad8f234c60294a05a013874a211fe3c03653f48df43ac4ec085ab9a24",
      "size": 12
    },
    {
      "class": "ownership",
      "path": "ownership.json",
      "sha256": "46a6136c3b93aa7fd9f194351bfca93b6e6def0096da2de3c0acebfae9883fc9",
      "size": 20
    },
    {
      "class": "report",
      "path": "report.md",
      "sha256": "92455f427ad655c4a7d21709eb2d121d5567e30736c2614e6dcab1af884c8252",
      "size": 12
    },
    {
      "class": "run_manifest",
      "path": "run_manifest.json",
      "sha256": "664b31aa2f33b922be90d4d4446b75fbada7d2ddee20d29b49713f8c071459ce",
      "size": 11
    },
    {
      "class": "token_truth",
      "path": "token_truth.json",
      "sha256": "27bff4b487e68a6a4b755cf9471e1b26c5356bbd6d034a47f0c67de8ddd6224b",
      "size": 14
    },
    {
      "class": "verdicts",
      "path": "verdicts.json",
      "sha256": "7361566f9b320d9a50b44af43839822e141264e084b4c008993655b7fea46419",
      "size": 20
    }
  ],
  "not_a_signature": "This certificate proves that its members are intact and agree with each other. It is not a signature: it does not prove who made it.",
  "project": "project-fixture",
  "referenced": [],
  "signature": null,
  "size_budget_bytes": 10000
}
"""

OBTAIN = "Read the diff from the job folder."


def _sources():
    return [
        CertificateSource("report.md", "report", b"report body\n"),
        CertificateSource("token_truth.json", "token_truth", b'{"tokens": 3}\n'),
        CertificateSource("verdicts.json", "verdicts", b'{"verdict": "pass"}\n'),
        CertificateSource("ownership.json", "ownership", b'{"owner": "remedy"}\n'),
        CertificateSource("run_manifest.json", "run_manifest", b'{"run": 1}\n'),
        CertificateSource("changes.diff", "diff", b"--- a\n+++ b\n", obtain=OBTAIN),
    ]


def _claims():
    return {"terminal_state": "done", "dod_summary": "3 of 3 met", "cost": 0.5,
            "cost_basis": "metered", "decisions_count": 2, "regression_status": "clean"}


def _build(out_path, **over):
    args = {"out_path": out_path, "job_id": "job-fixture", "project_id": "project-fixture",
            "created": "2026-10-21T00:00:00Z", "issue": 1, "sources": _sources(),
            "claims": _claims(), "size_budget_bytes": 10000}
    args.update(over)
    return build_job_certificate(**args)


def _part_files(folder):
    return sorted(p.name for p in folder.iterdir() if p.name.endswith(".part"))


def test_golden_manifest_and_members(tmp_path):
    out = tmp_path / "cert.zip"
    answer = _build(out)
    with zipfile.ZipFile(out) as zf:
        names = zf.namelist()
        manifest_bytes = zf.read("manifest.json")
        assert manifest_bytes.decode("utf-8") == GOLDEN_MANIFEST
        assert manifest_bytes == render_certificate_manifest(answer["manifest"])
        sources = {s.path: s for s in _sources()}
        assert sorted(names) == sorted([*sources, "manifest.json"])
        assert names == sorted(names)
        for row in answer["manifest"]["members"]:
            data = zf.read(row["path"])
            assert data == sources[row["path"]].data
            assert row["sha256"] == hashlib.sha256(data).hexdigest()
    assert answer["path"] == out
    assert answer["members"] == sorted([*sources, "manifest.json"])


def test_two_builds_are_byte_identical(tmp_path):
    _build(tmp_path / "a.zip")
    _build(tmp_path / "b.zip")
    assert (tmp_path / "a.zip").read_bytes() == (tmp_path / "b.zip").read_bytes()


def test_budget_references_large_diff_and_embeds_later_small_log(tmp_path):
    big = b"x" * 50_000
    sources = [s for s in _sources() if s.member_class != "diff"]
    sources.append(CertificateSource("a-big.diff", "diff", big, obtain=OBTAIN))
    sources.append(CertificateSource("z-small.log", "log", b"log line\n", obtain=OBTAIN))
    out = tmp_path / "cert.zip"
    answer = _build(out, sources=sources, size_budget_bytes=2000)
    manifest = answer["manifest"]
    assert manifest["referenced"] == [{
        "path": "a-big.diff", "class": "diff", "sha256": hashlib.sha256(big).hexdigest(),
        "size": 50_000, "obtain": OBTAIN}]
    with zipfile.ZipFile(out) as zf:
        assert "a-big.diff" not in zf.namelist()
        assert zf.read("z-small.log") == b"log line\n"
    assert "z-small.log" in [row["path"] for row in manifest["members"]]
    assert sum(row["size"] for row in manifest["members"]) <= 2000


def test_always_embedded_members_over_budget_are_refused(tmp_path):
    out = tmp_path / "cert.zip"
    total = sum(len(s.data) for s in _sources() if s.member_class != "diff")
    with pytest.raises(CertificateError) as exc:
        _build(out, size_budget_bytes=total - 1)
    assert str(exc.value) == (
        f"The certificate's always-embedded members hold {total} bytes, more than its budget "
        f"of {total - 1} bytes.")
    assert not out.exists()
    assert _part_files(tmp_path) == []


def test_existing_out_path_is_never_overwritten(tmp_path):
    out = tmp_path / "cert.zip"
    out.write_bytes(b"precious")
    with pytest.raises(CertificateError) as exc:
        _build(out)
    assert str(exc.value) == f"A certificate already exists at {out}; Remedy never overwrites one."
    assert out.read_bytes() == b"precious"
    assert _part_files(tmp_path) == []


def _with_source(index, **changes):
    sources = _sources()
    sources[index] = replace(sources[index], **changes)
    return {"sources": sources}


def _claims_without(key):
    claims = _claims()
    del claims[key]
    return {"claims": claims}


_CIRCULAR: list = []
_CIRCULAR.append(_CIRCULAR)   # json.dumps raises ValueError on a circular reference

REFUSALS = [
    pytest.param({"job_id": ""}, "job_id", id="empty-job-id"),
    pytest.param({"created": ""}, "created", id="empty-created"),
    pytest.param({"issue": True}, "issue", id="issue-is-a-bool"),
    pytest.param({"issue": 0}, "issue", id="issue-below-one"),
    pytest.param({"issue": "1"}, "issue", id="issue-is-a-string"),
    pytest.param({"size_budget_bytes": 0}, "size_budget_bytes", id="budget-below-one"),
    pytest.param({"size_budget_bytes": 1.5}, "size_budget_bytes", id="budget-is-a-float"),
    pytest.param({"sources": []}, "at least one source", id="no-sources"),
    pytest.param(_with_source(0, path="../report.md"), "'../report.md'", id="unsafe-path"),
    pytest.param(_with_source(0, path="manifest.json"), "reserved", id="manifest-name-taken"),
    pytest.param(_with_source(0, path="ownership.json"), "repeated", id="repeated-path"),
    pytest.param(_with_source(0, member_class="poem"), "'poem'", id="unknown-class"),
    pytest.param(_with_source(0, data="text"), "bytes", id="data-not-bytes"),
    pytest.param(_with_source(5, obtain=""), "obtain", id="diff-without-obtain"),
    pytest.param(_claims_without("cost"), "['cost']", id="claim-missing"),
    pytest.param({"claims": {**_claims(), "extra": 1}}, "['extra']", id="claim-extra"),
    pytest.param({"claims": {**_claims(), "cost": object()}}, "JSON", id="claims-not-json"),
    pytest.param({"claims": {**_claims(), "cost": _CIRCULAR}}, "JSON", id="claims-circular"),
]


@pytest.mark.parametrize("over, fragment", REFUSALS)
def test_refusals_name_the_offending_value(tmp_path, over, fragment):
    out = tmp_path / "cert.zip"
    with pytest.raises(CertificateError) as exc:
        _build(out, **over)
    assert fragment in str(exc.value)
    assert not out.exists()
    assert _part_files(tmp_path) == []


def test_missing_parent_folder_is_refused(tmp_path):
    out = tmp_path / "nowhere" / "cert.zip"
    with pytest.raises(CertificateError):
        _build(out)
    assert not out.exists()


def test_a_reopen_problem_is_refused_and_leaves_nothing(tmp_path, monkeypatch):
    monkeypatch.setattr(jc, "verify_review_zip", lambda path, expected: ["member 'x' changed"])
    out = tmp_path / "cert.zip"
    with pytest.raises(CertificateError) as exc:
        _build(out)
    assert "member 'x' changed" in str(exc.value)
    assert not out.exists()
    assert _part_files(tmp_path) == []


def test_signature_is_none_and_the_constants_are_stated(tmp_path):
    manifest = _build(tmp_path / "cert.zip", issue=7)["manifest"]
    assert manifest["signature"] is None
    assert manifest["not_a_signature"] == CERTIFICATE_NOT_A_SIGNATURE
    assert manifest["kind"] == CERTIFICATE_KIND
    assert manifest["bundle_v"] == CERTIFICATE_BUNDLE_V
    assert manifest["issue"] == 7
    assert set(manifest["claims"]) == set(CERTIFICATE_CLAIM_KEYS)


def test_a_budget_that_exactly_fits_embeds_the_diff(tmp_path):
    always = sum(len(s.data) for s in _sources() if s.member_class != "diff")
    diff = next(s for s in _sources() if s.member_class == "diff")
    manifest = _build(tmp_path / "cert.zip", size_budget_bytes=always + len(diff.data))["manifest"]
    assert diff.path in [row["path"] for row in manifest["members"]]
    assert manifest["referenced"] == []


def test_an_existing_out_path_is_refused_before_anything_is_packed(tmp_path, monkeypatch):
    def _must_not_pack(*args, **kwargs):
        pytest.fail("the packer was called although the certificate already exists")

    monkeypatch.setattr(jc, "build_review_zip_from_snapshot", _must_not_pack)
    out = tmp_path / "cert.zip"
    out.write_bytes(b"precious")
    with pytest.raises(CertificateError) as exc:
        _build(out)
    assert str(exc.value) == f"A certificate already exists at {out}; Remedy never overwrites one."
    assert out.read_bytes() == b"precious"
