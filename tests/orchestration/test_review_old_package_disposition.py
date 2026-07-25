"""F5 (round 23) — a prior review package (and its .sha256 sidecar) is classified in the ArchivePlan,
not silently removed by the shell."""
from __future__ import annotations

import importlib.util
import json
import shutil
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
_e = importlib.util.spec_from_file_location("_e2e_op", REPO_ROOT / "tests" / "orchestration" / "test_review_authoritative_e2e.py")
_E2E = importlib.util.module_from_spec(_e); _e.loader.exec_module(_E2E)

from packages.orchestration.archive_plan import (  # noqa: E402
    DISP_EXCLUDE_SAFE_CONTEXT,
    classify_bundle_path,
)


def test_classify_marks_prior_packages_exclude_safe_context():
    assert classify_bundle_path("remedy-review-old.zip", changed=False) == DISP_EXCLUDE_SAFE_CONTEXT
    assert classify_bundle_path("remedy-review-old.zip.sha256", changed=False) \
        == DISP_EXCLUDE_SAFE_CONTEXT


def _repo_with_old_package(tmp_path):
    repo = tmp_path / "repo"
    (repo / "scripts").mkdir(parents=True)
    for name in _E2E._REQUIRED_SCRIPTS:
        shutil.copy2(REPO_ROOT / "scripts" / name, repo / "scripts" / name)
    _E2E._git(repo, "init", "-q")
    (repo / "README.md").write_text("# base\n")
    (repo / "remedy-review-old.zip").write_text("PRIOR PACKAGE BYTES\n")
    (repo / "remedy-review-old.zip.sha256").write_text("deadbeef  remedy-review-old.zip\n")
    _E2E._git(repo, "add", "-A")
    _E2E._git(repo, "commit", "-qm", "base")
    base = _E2E._git(repo, "rev-parse", "HEAD").stdout.strip()
    (repo / "src").mkdir()
    (repo / "src" / "app.py").write_text("x = 1\n")
    _E2E._git(repo, "add", "-A")
    _E2E._git(repo, "commit", "-qm", "feature")
    head = _E2E._git(repo, "rev-parse", "HEAD").stdout.strip()
    return repo, base, head


def test_a_committed_prior_package_gets_an_exclusion_record_and_is_not_packaged(tmp_path):
    repo, base, head = _repo_with_old_package(tmp_path)
    ev, _s, _a = _E2E._write_evidence(repo, base, head, tmp_path / "evidence")
    proc = _E2E._run(["bash", "scripts/make_review_zip.sh", "--evidence-dir", str(ev)],
                     repo, {"REMEDY_REVIEW_BASE": base, "PYTHONPATH": str(REPO_ROOT)})
    assert proc.returncode == 0, proc.stdout + proc.stderr
    # the BUILT package carries a status suffix; the committed decoy is `remedy-review-old.zip`
    built = [p for p in repo.glob("remedy-review-2*.zip") if "REVIEW" in p.name or "EVIDENCE" in p.name]
    z = sorted(built)[-1]
    with zipfile.ZipFile(z) as zf:
        names = set(zf.namelist())
        plan = json.loads(zf.read("evidence/current/review_archive_plan.json"))
    excluded = {e["path"]: e["disposition"] for e in plan.get("excluded_records", [])}
    for p in ("remedy-review-old.zip", "remedy-review-old.zip.sha256"):
        assert excluded.get(p) == "exclude_safe_context", (p, excluded)
        assert p not in names            # a prior package never recurses into the new one
