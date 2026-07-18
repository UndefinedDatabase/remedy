"""F4 (round 22) — the ArchivePlan is the SOLE bundle-policy owner, driven through the real
make_review_zip.sh entry point. Unchanged sensitive context paths get explicit EXCLUDE_SAFE_CONTEXT
records; a FIFO gets an explicit blocked record; no policy path silently disappears."""
from __future__ import annotations

import importlib.util
import json
import os
import zipfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
_e2e = importlib.util.spec_from_file_location(
    "_e2e_bp", REPO_ROOT / "tests" / "orchestration" / "test_review_authoritative_e2e.py")
_E2E = importlib.util.module_from_spec(_e2e)
_e2e.loader.exec_module(_E2E)


def _repo_with_sensitive_context(tmp_path):
    repo = tmp_path / "repo"
    (repo / "scripts").mkdir(parents=True)
    for name in _E2E._REQUIRED_SCRIPTS:
        import shutil
        shutil.copy2(REPO_ROOT / "scripts" / name, repo / "scripts" / name)
    _E2E._git(repo, "init", "-q")
    # base commit: unchanged sensitive CONTEXT files (never part of the reviewed change)
    (repo / "README.md").write_text("# base\n")
    (repo / ".env").write_text("SECRET=1\n")
    (repo / "app.log").write_text("log line\n")
    (repo / "old.zip").write_text("PKzip\n")
    (repo / "id_rsa").write_text("PRIVATE KEY\n")
    _E2E._git(repo, "add", "-A")
    _E2E._git(repo, "commit", "-qm", "base")
    base = _E2E._git(repo, "rev-parse", "HEAD").stdout.strip()
    # feature commit: a normal source file (the reviewed change)
    (repo / "src").mkdir()
    (repo / "src" / "app.py").write_text("x = 1\n")
    _E2E._git(repo, "add", "-A")
    _E2E._git(repo, "commit", "-qm", "feature")
    head = _E2E._git(repo, "rev-parse", "HEAD").stdout.strip()
    return repo, base, head


def _plan_from_zip(repo):
    z = sorted(repo.glob("remedy-review-*.zip"))[-1]
    with zipfile.ZipFile(z) as zf:
        return json.loads(zf.read("evidence/current/review_archive_plan.json")), set(zf.namelist())


class TestRealBundlePolicy:
    def test_unchanged_sensitive_context_paths_are_excluded_with_records(self, tmp_path):
        repo, base, head = _repo_with_sensitive_context(tmp_path)
        ev, _subj, _auth = _E2E._write_evidence(repo, base, head, tmp_path / "evidence")
        proc = _E2E._run(["bash", "scripts/make_review_zip.sh", "--evidence-dir", str(ev)],
                         repo, {"REMEDY_REVIEW_BASE": base, "PYTHONPATH": str(REPO_ROOT)})
        assert proc.returncode == 0, proc.stdout + proc.stderr
        plan, names = _plan_from_zip(repo)
        excluded = {e["path"]: e["disposition"] for e in plan.get("excluded_records", [])}
        for p in (".env", "app.log", "old.zip", "id_rsa"):
            assert excluded.get(p) == "exclude_safe_context", (p, excluded)
            assert p not in names            # never packaged
        # the reviewed source file is a normal member
        assert "src/app.py" in names

    def test_a_fifo_blocks_the_package_with_an_explicit_record(self, tmp_path):
        repo, base, head = _repo_with_sensitive_context(tmp_path)
        ev, _s, _a = _E2E._write_evidence(repo, base, head, tmp_path / "evidence")
        os.mkfifo(str(repo / "pipe.sock"))       # a special file in the discovered tree
        proc = _E2E._run(["bash", "scripts/make_review_zip.sh", "--evidence-dir", str(ev)],
                         repo, {"REMEDY_REVIEW_BASE": base, "PYTHONPATH": str(REPO_ROOT)})
        # a special file cannot be represented — the plan blocks and the build fails closed
        assert proc.returncode != 0, proc.stdout + proc.stderr
        assert "BLOCK_UNSUPPORTED" in (proc.stdout + proc.stderr)
