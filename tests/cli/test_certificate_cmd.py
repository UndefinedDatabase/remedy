"""`remedy job certificate` and `remedy verify` — F060 T003, DECISION F060 D4.

Both commands are driven through the real argv dispatcher over jobs built the way
`tests/orchestration/test_job_certificate_sources.py` builds them. The last test is the standalone
check: the verifier run in a fresh folder, in a subprocess, with no data folder at all.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import zipfile
from pathlib import Path
from uuid import uuid4

import pytest

from packages.core.models import RunState
from packages.orchestration.data_paths import (
    job_dir,
    job_evidence_dir,
    job_evidence_export_dir,
    run_log_dir,
)
from packages.orchestration.job_certificate import (
    CERTIFICATE_DEFAULT_MAX_BYTES,
    CERTIFICATE_NOT_A_SIGNATURE,
)
from packages.orchestration.job_certificate_sources import CERTIFICATE_ISSUES_FILENAME
from packages.orchestration.job_certificate_verify import (
    render_certificate_verdict,
    verify_job_certificate,
)
from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan

REPO_ROOT = Path(__file__).resolve().parents[2]
DIFF_BYTES = b"--- a/x\n+++ b/x\n@@ -1 +1 @@\n-old\n+new\n"
JSON_KEYS = {"schema_version", "ok", "path", "job_id", "issue", "terminal_state", "members",
             "referenced", "size_budget_bytes", "manifest_sha256"}


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "remedy_data"))


def _run(argv: list[str], capsys) -> tuple[int, str]:
    from apps.cli.grouped import main

    try:
        code = main(argv)
    except SystemExit as exc:
        code = exc.code
    return (code or 0), capsys.readouterr().out


def _put(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def _ended_job(state: RunState = RunState.COMPLETED) -> JobPlan:
    job = JobPlan(
        job_title="certificate-cli-job",
        user_prompt="build the thing",
        tasks=[TaskEntry(title="task 0", inputs={"task_type": "documentation"})],
        state=state,
        metadata={"target_repo": "/repo/fixture"},
    )
    job.project_id = "project-fixture"
    job.isolation_mode = "worktree"
    job.result_diff_path = "result.diff"
    job.result_diff_sha256 = hashlib.sha256(DIFF_BYTES).hexdigest()
    job.result_diff_size_bytes = len(DIFF_BYTES)
    save_job_plan(job)
    jid = str(job.job_id)
    evidence, export = job_evidence_dir(jid), job_evidence_export_dir(jid)
    _put(evidence / "report.md", b"# Run report\n\n- State: completed\n")
    _put(evidence / "dod_result.json", json.dumps({
        "released": True, "checks": [{"status": "passed"}, {"status": "failed"}]}).encode())
    _put(export / "final_verifier_report.json", b'{"test_status": "passed"}\n')
    _put(export / "ownership.json", b'{"o": 1}\n')
    _put(job_dir(jid) / "result.diff", DIFF_BYTES)
    _put(run_log_dir(jid) / "run.jsonl", b'{"e": 1}\n')
    return job


def _manifest_of(bundle: Path) -> dict:
    with zipfile.ZipFile(bundle) as zf:
        return json.loads(zf.read("manifest.json"))


def _tampered_copy(bundle: Path, target: Path) -> Path:
    """A copy of `bundle` in which one member's bytes differ and its manifest is untouched."""
    with zipfile.ZipFile(bundle) as src, zipfile.ZipFile(target, "w") as dst:
        for info in src.infolist():
            data = src.read(info.filename)
            if info.filename == "verdicts/final_verifier_report.json":
                data = b'{"test_status": "failed"}\n'
            dst.writestr(info, data)
    return target


def _issue_lines(jid: str) -> list[dict]:
    path = job_dir(jid) / CERTIFICATE_ISSUES_FILENAME
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


class TestJobCertificateWrites:
    def test_a_completed_job_writes_a_certificate_that_verifies_intact(self, tmp_path, capsys):
        job = _ended_job()
        jid = str(job.job_id)
        out = tmp_path / "cert.zip"
        code, text = _run(["job", "certificate", jid, "--out", str(out)], capsys)
        assert code == 0
        manifest = _manifest_of(out)
        assert text.splitlines() == [
            f"Certificate written: {out.absolute()}",
            f"Job {jid} ended completed; certificate issue 1.",
            f"Members: {len(manifest['members'])} embedded, {len(manifest['referenced'])} "
            f"referenced (budget {CERTIFICATE_DEFAULT_MAX_BYTES} bytes).",
            CERTIFICATE_NOT_A_SIGNATURE,
        ]
        assert verify_job_certificate(out).ok
        lines = _issue_lines(jid)
        assert len(lines) == 1
        with zipfile.ZipFile(out) as zf:
            manifest_sha = hashlib.sha256(zf.read("manifest.json")).hexdigest()
        assert lines[0]["manifest_sha256"] == manifest_sha
        assert lines[0]["path"] == str(out.absolute())
        assert lines[0]["issue"] == 1

    def test_the_json_answer_carries_exactly_its_keys(self, tmp_path, capsys):
        job = _ended_job()
        jid = str(job.job_id)
        out = tmp_path / "cert.zip"
        code, text = _run(["job", "certificate", jid, "--out", str(out), "--json"], capsys)
        assert code == 0
        body = json.loads(text)
        assert set(body) == JSON_KEYS
        assert body["ok"] is True
        assert body["path"] == str(out.absolute())
        assert body["job_id"] == jid
        assert body["issue"] == 1
        assert body["terminal_state"] == "completed"
        assert body["size_budget_bytes"] == CERTIFICATE_DEFAULT_MAX_BYTES
        manifest = _manifest_of(out)
        assert body["members"] == [m["path"] for m in manifest["members"]]
        assert body["referenced"] == []
        assert body["manifest_sha256"] == _issue_lines(jid)[0]["manifest_sha256"]

    def test_without_out_the_file_is_named_after_the_job_and_the_issue(
            self, tmp_path, monkeypatch, capsys):
        job = _ended_job()
        jid = str(job.job_id)
        here = tmp_path / "here"
        here.mkdir()
        monkeypatch.chdir(here)
        code, _text = _run(["job", "certificate", jid], capsys)
        assert code == 0
        assert (here / f"remedy-certificate-{jid}-1.zip").is_file()
        code, text = _run(["job", "certificate", jid, "--json"], capsys)
        assert code == 0
        assert json.loads(text)["issue"] == 2
        assert (here / f"remedy-certificate-{jid}-2.zip").is_file()
        assert [line["issue"] for line in _issue_lines(jid)] == [1, 2]

    def test_a_relative_out_is_recorded_in_the_issue_record_as_an_absolute_path(
            self, tmp_path, monkeypatch, capsys):
        job = _ended_job()
        jid = str(job.job_id)
        here = tmp_path / "relative_here"
        here.mkdir()
        monkeypatch.chdir(here)
        code, _text = _run(["job", "certificate", jid, "--out", "cert.zip"], capsys)
        assert code == 0
        written = here / "cert.zip"
        assert written.is_file()
        lines = _issue_lines(jid)
        assert len(lines) == 1
        assert os.path.isabs(lines[0]["path"])
        assert lines[0]["path"] == str(written.absolute())


class TestJobCertificateRefusals:
    def test_a_running_job_exits_3_as_not_ready(self, capsys):
        job = _ended_job(RunState.RUNNING)
        code, text = _run(["job", "certificate", str(job.job_id), "--json"], capsys)
        assert code == 3
        body = json.loads(text)
        assert body["ok"] is False
        assert body["error"] == "certificate_not_ready"

    def test_an_id_that_names_no_job_is_refused(self, capsys):
        code, text = _run(["job", "certificate", "../etc", "--json"], capsys)
        assert code == 1
        assert json.loads(text)["error"] == "invalid_job_id"
        unknown = str(uuid4())
        code, text = _run(["job", "certificate", unknown, "--json"], capsys)
        assert code == 3
        assert json.loads(text)["error"] == "certificate_not_ready"

    def test_an_existing_out_is_refused_and_left_unchanged(self, tmp_path, capsys):
        job = _ended_job()
        out = tmp_path / "taken.zip"
        out.write_bytes(b"precious")
        code, text = _run(["job", "certificate", str(job.job_id), "--out", str(out), "--json"],
                          capsys)
        assert code == 1
        assert json.loads(text)["error"] == "certificate_refused"
        assert out.read_bytes() == b"precious"
        assert not (job_dir(str(job.job_id)) / CERTIFICATE_ISSUES_FILENAME).exists()

    @pytest.mark.parametrize("bad", ["abc", "0", "-5", "1.5"])
    def test_a_max_bytes_that_is_not_a_whole_number_of_at_least_one_exits_2(
            self, bad, tmp_path, capsys):
        job = _ended_job()
        out = tmp_path / "never.zip"
        code, text = _run(["job", "certificate", str(job.job_id), "--out", str(out),
                           "--max-bytes", bad, "--json"], capsys)
        assert code == 2
        assert json.loads(text)["error"] == "invalid_max_bytes"
        assert not out.exists()
        assert not (job_dir(str(job.job_id)) / CERTIFICATE_ISSUES_FILENAME).exists()

    def test_a_budget_below_the_diff_lists_the_diff_as_referenced(self, tmp_path, capsys):
        from packages.orchestration.job_certificate_sources import collect_certificate_inputs

        job = _ended_job()
        jid = str(job.job_id)
        always = sum(len(s.data) for s in collect_certificate_inputs(jid).sources
                     if s.member_class not in ("diff", "log"))
        out = tmp_path / "small.zip"
        code, text = _run(["job", "certificate", jid, "--out", str(out),
                           "--max-bytes", str(always), "--json"], capsys)
        assert code == 0
        body = json.loads(text)
        assert body["size_budget_bytes"] == always
        assert "diff/result.diff" in body["referenced"]
        assert "diff/result.diff" not in body["members"]
        assert verify_job_certificate(out).ok


class TestVerifyCommand:
    def _bundle(self, tmp_path, capsys) -> Path:
        job = _ended_job()
        out = tmp_path / "cert.zip"
        code, _ = _run(["job", "certificate", str(job.job_id), "--out", str(out)], capsys)
        assert code == 0
        return out

    def test_an_intact_certificate_prints_its_verdict_and_exits_0(self, tmp_path, capsys):
        bundle = self._bundle(tmp_path, capsys)
        code, text = _run(["verify", str(bundle)], capsys)
        assert code == 0
        assert text == render_certificate_verdict(verify_job_certificate(bundle))
        assert text.splitlines()[0] == "Run ended: completed"

    def test_a_changed_member_exits_1_with_the_not_intact_line(self, tmp_path, capsys):
        bundle = self._bundle(tmp_path, capsys)
        bad = _tampered_copy(bundle, tmp_path / "bad.zip")
        code, text = _run(["verify", str(bad)], capsys)
        assert code == 1
        assert text == render_certificate_verdict(verify_job_certificate(bad))
        assert "Certificate: NOT INTACT" in text

    def test_json_answers_intact_problems_and_manifest(self, tmp_path, capsys):
        bundle = self._bundle(tmp_path, capsys)
        code, text = _run(["verify", str(bundle), "--json"], capsys)
        assert code == 0
        body = json.loads(text)
        assert body["ok"] is True
        assert body["intact"] is True
        assert body["problems"] == []
        assert body["manifest"] == _manifest_of(bundle)

        bad = _tampered_copy(bundle, tmp_path / "bad.zip")
        code, text = _run(["verify", str(bad), "--json"], capsys)
        assert code == 1
        body = json.loads(text)
        assert body["ok"] is False
        assert body["error"] == "certificate_not_intact"
        assert body["intact"] is False
        assert body["problems"]
        assert body["manifest"] == _manifest_of(bad)

    def test_a_file_that_is_not_a_zip_exits_1(self, tmp_path, capsys):
        junk = tmp_path / "junk.zip"
        junk.write_bytes(b"not a zip")
        code, text = _run(["verify", str(junk)], capsys)
        assert code == 1
        assert "NOT INTACT" in text


def _verify_in_fresh_folder(bundle: Path, work: Path, data: Path) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(REPO_ROOT)
    env["REMEDY_DATA_DIR"] = str(data)
    return subprocess.run(
        [sys.executable, "-m", "apps.cli.main", "verify", str(bundle)],
        cwd=work, env=env, capture_output=True, text=True, timeout=120, check=False)


def test_the_verifier_runs_in_a_fresh_folder_with_no_data_folder(tmp_path, capsys):
    """THE STANDALONE CHECK: no data folder is read, and none is created."""
    job = _ended_job()
    bundle = tmp_path / "cert.zip"
    code, _ = _run(["job", "certificate", str(job.job_id), "--out", str(bundle)], capsys)
    assert code == 0
    bad = _tampered_copy(bundle, tmp_path / "bad.zip")

    work = tmp_path / "fresh_work"
    work.mkdir()
    data = tmp_path / "no_such_data_folder"
    assert not data.exists()

    done = _verify_in_fresh_folder(bundle, work, data)
    assert done.returncode == 0, done.stderr
    assert done.stdout.splitlines()[0] == "Run ended: completed"
    assert not data.exists()
    assert list(work.iterdir()) == []

    done = _verify_in_fresh_folder(bad, work, data)
    assert done.returncode == 1, done.stderr
    assert "Certificate: NOT INTACT" in done.stdout
    assert not data.exists()
