"""Provider Trust Gate + External Repair Intake v0 tests (Steps 1326/1328/1330).

Parser/limits/secret-scan/path-safety/patch-shape/failure-link/trust-decision,
intake orchestration (accepted creates a real pending intent; rejected/needs-review
create none), redaction across surfaces, and architecture guards (no network/
subprocess/provider SDK/apply/test-exec imports).
"""
from __future__ import annotations

import json
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from packages.core.models import Artifact, ArtifactKind, Job, Task
from packages.orchestration.storage import save_job, load_job
from packages.orchestration import provider_trust as PT


@pytest.fixture()
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"; d.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    return d


def _job(data_dir, *, with_failure=True, related_files=None):
    t = Task(description="t")
    arts = []
    fid = ""
    if with_failure:
        fa = Artifact(name="tf", content="x", kind=ArtifactKind.VERIFICATION, task_id=t.id,
                      metadata={"test_failure": True, "failure_kind": "test_failed",
                                "related_task_id": str(t.id), "safe_summary": "boom",
                                "related_files": related_files if related_files is not None else ["src/app.py"]})
        arts.append(fa); fid = str(fa.id)
    job = Job(id=uuid4(), name="ov", tasks=[t], artifacts=arts, metadata={"target_repo": "."})
    save_job(job, root=data_dir)
    return job, fid


def _write(data_dir, name, text):
    p = data_dir / name
    p.write_text(text)
    return str(p)


_GOOD_DIFF = (
    "Fix off-by-one.\n```diff\n--- a/src/app.py\n+++ b/src/app.py\n"
    "@@ -1,2 +1,2 @@\n-x = 1\n+x = 2\n```\n"
)


def _intake(job, data_dir, text, *, fid="", provider="claude", **kw):
    p = _write(data_dir, f"in-{uuid4().hex[:6]}.md", text)
    req = PT.ProviderOutputIntakeRequest(job_id=str(job.id), failure_artifact_id=fid,
                                         provider_name=provider, **kw)
    return PT.intake_provider_repair(req, input_path=p, data_dir=data_dir)


# ---------------------------------------------------------------------------
# Input limits (Step 1308)
# ---------------------------------------------------------------------------


class TestInputLimits:
    def test_oversized_rejected(self, env):
        job, fid = _job(env)
        big = "x" * (PT.MAX_INPUT_BYTES + 10)
        r = _intake(job, env, big, fid=fid)
        assert r.trust_status == PT.TrustStatus.REJECTED
        assert any(f.code == PT.TrustFindingCode.INPUT_TOO_LARGE for f in r.findings)
        assert not r.repair_intent_id

    def test_nul_rejected(self, env):
        job, fid = _job(env)
        p = env / "nul.bin"; p.write_bytes(b"abc\x00def")
        req = PT.ProviderOutputIntakeRequest(job_id=str(job.id), failure_artifact_id=fid)
        r = PT.intake_provider_repair(req, input_path=str(p), data_dir=env)
        assert r.trust_status == PT.TrustStatus.REJECTED
        assert any(f.code == PT.TrustFindingCode.INPUT_NUL_BYTE for f in r.findings)

    def test_binary_rejected(self, env):
        job, fid = _job(env)
        p = env / "b.bin"; p.write_bytes(bytes(range(0, 30)) * 400)
        req = PT.ProviderOutputIntakeRequest(job_id=str(job.id), failure_artifact_id=fid)
        r = PT.intake_provider_repair(req, input_path=str(p), data_dir=env)
        assert r.trust_status == PT.TrustStatus.REJECTED
        assert any(f.code in (PT.TrustFindingCode.INPUT_BINARY, PT.TrustFindingCode.INPUT_NUL_BYTE)
                   for f in r.findings)

    def test_invalid_utf8_safe(self, env):
        job, fid = _job(env)
        p = env / "u.md"; p.write_bytes(b"Fix.\n```diff\n--- a/src/app.py\n+++ b/src/app.py\n@@ -1 +1 @@\n-a\xff\n+b\n```\n")
        req = PT.ProviderOutputIntakeRequest(job_id=str(job.id), failure_artifact_id=fid)
        r = PT.intake_provider_repair(req, input_path=str(p), data_dir=env)
        # decoded with replacement → still processed, no traceback
        assert r.trust_status in (PT.TrustStatus.ACCEPTED, PT.TrustStatus.NEEDS_HUMAN_REVIEW,
                                  PT.TrustStatus.REJECTED)

    def test_missing_file_safe(self, env):
        job, fid = _job(env)
        req = PT.ProviderOutputIntakeRequest(job_id=str(job.id), failure_artifact_id=fid)
        r = PT.intake_provider_repair(req, input_path=str(env / "nope.md"), data_dir=env)
        assert r.trust_status == PT.TrustStatus.REJECTED
        assert any(f.code == PT.TrustFindingCode.INPUT_NOT_FOUND for f in r.findings)


# ---------------------------------------------------------------------------
# Parser (Step 1309)
# ---------------------------------------------------------------------------


class TestParser:
    def test_single_diff_is_patch(self, env):
        cand, raw, findings = PT.parse_candidate(_GOOD_DIFF)
        assert cand.candidate_kind == PT.CandidateKind.PATCH
        assert cand.has_patch and "src/app.py" in cand.target_files
        assert raw  # raw patch captured privately

    def test_multiple_patches_flagged(self, env):
        text = _GOOD_DIFF + "\n" + _GOOD_DIFF
        cand, raw, findings = PT.parse_candidate(text)
        assert any(f.code == PT.TrustFindingCode.MULTIPLE_PATCH_CANDIDATES for f in findings)
        assert not raw

    def test_explanation_needs_review(self, env):
        cand, raw, findings = PT.parse_candidate("You should refactor the parser carefully.")
        assert cand.candidate_kind == PT.CandidateKind.EXPLANATION
        assert any(f.code == PT.TrustFindingCode.REQUIRES_HUMAN_REVIEW for f in findings)

    def test_json_candidate(self, env):
        obj = json.dumps({"summary": "fix", "target_files": ["src/app.py"],
                          "unified_diff": "--- a/src/app.py\n+++ b/src/app.py\n@@ -1 +1 @@\n-a\n+b\n"})
        cand, raw, findings = PT.parse_candidate(obj)
        assert cand.has_patch and cand.patch_format == "unified_diff"

    def test_unknown_unparseable(self, env):
        cand, raw, findings = PT.parse_candidate("???")
        assert any(f.code == PT.TrustFindingCode.PROVIDER_OUTPUT_UNPARSEABLE for f in findings)


# ---------------------------------------------------------------------------
# Validation (Steps 1311-1313)
# ---------------------------------------------------------------------------


class TestValidation:
    def test_secret_blocks(self, env):
        findings = PT.scan_secrets('api_key = "sk-abcdef0123456789abcd"')
        assert any(f.code == PT.TrustFindingCode.RAW_SECRET_DETECTED
                   and f.severity == PT.Severity.BLOCKER for f in findings)

    def test_private_key_blocks(self, env):
        findings = PT.scan_secrets("-----BEGIN RSA PRIVATE KEY-----\nabc\n")
        assert any(f.code == PT.TrustFindingCode.RAW_SECRET_DETECTED for f in findings)

    def test_protected_path_blocks(self, env):
        for bad in [".env", ".git/config", "node_modules/x.js", "secrets/key.txt"]:
            findings = PT.validate_paths([bad])
            assert any(f.severity == PT.Severity.BLOCKER for f in findings), bad

    def test_absolute_and_traversal(self, env):
        assert any(f.code == PT.TrustFindingCode.ABSOLUTE_PATH for f in PT.validate_paths(["/etc/passwd"]))
        assert any(f.code == PT.TrustFindingCode.PATH_TRAVERSAL for f in PT.validate_paths(["../x.py"]))

    def test_lockfile_unsupported(self, env):
        assert any(f.code == PT.TrustFindingCode.UNSUPPORTED_PATCH_OPERATION
                   for f in PT.validate_paths(["package-lock.json"]))

    def test_patch_delete_and_binary(self, env):
        cand = PT.ProviderCandidateRepair(candidate_kind=PT.CandidateKind.PATCH, has_patch=True,
                                          target_files=["src/a.py"])
        del_findings = PT.validate_patch_shape(cand, "--- a/src/a.py\n+++ /dev/null\n")
        assert any(f.code == PT.TrustFindingCode.DELETES_FILE for f in del_findings)
        bin_findings = PT.validate_patch_shape(cand, "GIT binary patch\n")
        assert any(f.code == PT.TrustFindingCode.BINARY_FILE_CHANGE for f in bin_findings)


# ---------------------------------------------------------------------------
# Failure link + decision (Steps 1314-1315)
# ---------------------------------------------------------------------------


class TestDecision:
    def test_blocker_rejects(self, env):
        cand = PT.ProviderCandidateRepair(candidate_kind=PT.CandidateKind.PATCH, has_patch=True)
        d = PT.decide_trust(cand, [PT._finding(PT.TrustFindingCode.RAW_SECRET_DETECTED, PT.Severity.BLOCKER, "x")])
        assert d.trust_status == PT.TrustStatus.REJECTED

    def test_no_patch_needs_review(self, env):
        cand = PT.ProviderCandidateRepair(candidate_kind=PT.CandidateKind.EXPLANATION, has_patch=False)
        assert PT.decide_trust(cand, []).trust_status == PT.TrustStatus.NEEDS_HUMAN_REVIEW

    def test_low_only_accepts(self, env):
        cand = PT.ProviderCandidateRepair(candidate_kind=PT.CandidateKind.PATCH, has_patch=True)
        d = PT.decide_trust(cand, [PT._finding(PT.TrustFindingCode.NO_REPAIR_ATTEMPT_LINK, PT.Severity.LOW, "x")])
        assert d.trust_status == PT.TrustStatus.ACCEPTED

    def test_missing_failure_artifact_high(self, env):
        job, _ = _job(env, with_failure=False)
        cand = PT.ProviderCandidateRepair(candidate_kind=PT.CandidateKind.PATCH, has_patch=True,
                                          target_files=["src/app.py"])
        findings, _ = PT.validate_failure_link(job, cand, str(uuid4()), "")
        assert any(f.code == PT.TrustFindingCode.NO_FAILURE_LINK and f.severity == PT.Severity.HIGH
                   for f in findings)


# ---------------------------------------------------------------------------
# Intake orchestration (Steps 1316-1317)
# ---------------------------------------------------------------------------


class TestIntake:
    def test_accepted_creates_pending_intent(self, env):
        from packages.orchestration.approval_queue import get_patch_intent, APPROVAL_PENDING
        job, fid = _job(env)
        r = _intake(job, env, _GOOD_DIFF, fid=fid)
        assert r.trust_status == PT.TrustStatus.ACCEPTED
        assert r.repair_intent_id
        assert r.next_safe_action == f"remedy patch approve {job.id} {r.repair_intent_id} --json"
        reloaded = load_job(UUID(str(job.id)), env)
        intent = get_patch_intent(reloaded, r.repair_intent_id)
        assert intent is not None and intent["state"] == APPROVAL_PENDING  # not auto-approved

    def test_secret_rejected_no_intent(self, env):
        job, fid = _job(env)
        text = ("Fix.\n```diff\n--- a/src/app.py\n+++ b/src/app.py\n@@ -1 +1,2 @@\n a\n"
                '+token = "ghp_abcdefghijklmnopqrstuvwxyz0123"\n```\n')
        r = _intake(job, env, text, fid=fid)
        assert r.trust_status == PT.TrustStatus.REJECTED
        assert not r.repair_intent_id

    def test_protected_rejected_no_intent(self, env):
        job, fid = _job(env)
        text = "```diff\n--- a/.env\n+++ b/.env\n@@ -1 +1 @@\n-A=1\n+A=2\n```\n"
        r = _intake(job, env, text, fid=fid)
        assert r.trust_status == PT.TrustStatus.REJECTED
        assert not r.repair_intent_id

    def test_unparseable_no_intent(self, env):
        job, fid = _job(env)
        r = _intake(job, env, "???", fid=fid)
        assert r.trust_status in (PT.TrustStatus.REJECTED, PT.TrustStatus.NEEDS_HUMAN_REVIEW)
        assert not r.repair_intent_id

    def test_missing_job_safe(self, env):
        req = PT.ProviderOutputIntakeRequest(job_id=str(uuid4()))
        r = PT.intake_provider_repair(req, input_path=_write(env, "x.md", _GOOD_DIFF), data_dir=env)
        assert r.trust_status == PT.TrustStatus.REJECTED
        assert not r.repair_intent_id

    def test_candidate_summary_scrubbed(self, env):
        # R-0083: provider free-text fields are scrubbed of secrets/abs paths before
        # being persisted/shown publicly.
        job, fid = _job(env)
        obj = json.dumps({
            "summary": "uses token sk-abcdef0123456789abcd at /home/u/.ssh/id_rsa",
            "target_files": ["src/app.py"],
            "unified_diff": "--- a/src/app.py\n+++ b/src/app.py\n@@ -1 +1 @@\n-a\n+b\n",
            "rationale": "see /etc/passwd",
        })
        r = _intake(job, env, obj, fid=fid)
        rep = PT.get_trust_report(load_job(UUID(str(job.id)), env), r.trust_report_id)
        blob = json.dumps(rep)
        assert "sk-abcdef0123456789abcd" not in blob
        assert "/home/" not in blob and "/etc/passwd" not in blob and "id_rsa" not in blob

    def test_quarantine_private_and_hashed(self, env):
        job, fid = _job(env)
        r = _intake(job, env, _GOOD_DIFF, fid=fid)
        qdir = env / "workspaces" / str(job.id) / "provider_quarantine" / r.quarantine_id
        assert (qdir / "raw_input.txt").exists()
        # raw lives only in quarantine, never in the persisted report
        rep = PT.get_trust_report(load_job(UUID(str(job.id)), env), r.trust_report_id)
        assert "x = 2" not in json.dumps(rep)


# ---------------------------------------------------------------------------
# Redaction (Step 1326)
# ---------------------------------------------------------------------------


class TestRedaction:
    def test_no_raw_leak_across_surfaces(self, env):
        job, fid = _job(env)
        text = (
            "Here is the fix.\n```diff\n--- a/src/app.py\n+++ b/src/app.py\n"
            "@@ -1,3 +1,4 @@\n value = 1\n"
            '+api_key = "sk-secretsecretsecret01"\n'
            "+password = hunter2hunter2\n"
            "+path = /home/victim/.ssh/id_rsa\n"
            "+# Traceback (most recent call last)\n```\n"
        )
        r = _intake(job, env, text, fid=fid)
        reloaded = load_job(UUID(str(job.id)), env)
        rep = PT.get_trust_report(reloaded, r.trust_report_id)
        from packages.orchestration.progress_ledger import extract_provider_trust_items
        from packages.orchestration.review_bundle import _build_provider_trust_summary
        from packages.orchestration.ui_server import _build_provider_trust_section
        items = extract_provider_trust_items(PT.load_trust_reports(reloaded))
        blobs = [
            json.dumps(PT.export_intake_result_json(r)),
            json.dumps(rep),
            json.dumps([{"id": i.item_id, "s": i.safe_summary, "n": i.next_action} for i in items]),
            json.dumps(_build_provider_trust_summary(reloaded)),
            json.dumps(_build_provider_trust_section(reloaded)),
            json.dumps([a.metadata for a in reloaded.artifacts], default=str),
        ]
        for b in blobs:
            assert "sk-secretsecretsecret01" not in b
            assert "hunter2hunter2" not in b
            assert "/home/" not in b
            assert "id_rsa" not in b
            assert "Traceback" not in b
            assert "value = 1" not in b  # no raw source line
            assert "diff --git" not in b


# ---------------------------------------------------------------------------
# Architecture guards (Step 1328)
# ---------------------------------------------------------------------------


class TestArchitectureGuards:
    SRC = Path("packages/orchestration/provider_trust.py").read_text()

    def _imports(self):
        return [ln for ln in self.SRC.splitlines()
                if ln.strip().startswith(("import ", "from "))]

    def test_no_network_or_subprocess(self):
        for ln in self._imports():
            for bad in ("subprocess", "socket", "requests", "httpx", "urllib", "http.client", "aiohttp"):
                assert bad not in ln
        assert "import subprocess" not in self.SRC
        assert "shell=True" not in self.SRC

    def test_no_provider_sdk(self):
        for ln in self._imports():
            low = ln.lower()
            for bad in ("ollama", "anthropic", "openai", "claude", "litellm"):
                assert bad not in low

    def test_no_apply_or_test_exec_imports(self):
        for ln in self._imports():
            assert "patch_apply" not in ln
            assert "source_apply" not in ln
            assert "test_execution_service" not in ln
            assert "do_continue" not in ln

    def test_accepted_intent_resolvable(self, env):
        from packages.orchestration.approval_queue import get_patch_intent
        job, fid = _job(env)
        r = _intake(job, env, _GOOD_DIFF, fid=fid)
        reloaded = load_job(UUID(str(job.id)), env)
        assert get_patch_intent(reloaded, r.repair_intent_id) is not None

    def test_next_action_catalog_backed(self, env):
        from packages.orchestration.do_run import validate_next_safe_action_command
        job, fid = _job(env)
        r = _intake(job, env, _GOOD_DIFF, fid=fid)
        assert validate_next_safe_action_command(r.next_safe_action)
