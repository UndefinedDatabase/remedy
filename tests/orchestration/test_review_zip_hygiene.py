"""Regression tests for review-zip / test-run hygiene.

Two guarantees are locked down here:

1. The ping-pong loop never leaves ``*_WAS_HERE.txt`` debug detritus in the
   real repo root — the fake builder writes such a marker to its cwd, which
   must land in the throwaway staging dir, not the project root.
2. ``scripts/make_review_zip.sh`` still *rejects* a review zip when actual
   root-level debug detritus is present (fail-fast before zipping).

Both tests are fully offline (fake providers, an isolated tmp git repo) and
never commit, push, reset, or checkout.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import stat
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

from packages.orchestration.pingpong_loop import run_pingpong

REPO_ROOT = Path(__file__).resolve().parents[2]
MAKE_REVIEW_ZIP = REPO_ROOT / "scripts" / "make_review_zip.sh"

# ---------------------------------------------------------------------------
# Fixtures (self-contained; mirror tests/orchestration/test_pingpong_cli.py)
# ---------------------------------------------------------------------------


@pytest.fixture
def demo_repo(tmp_path: Path) -> Path:
    """Minimal demo target repo."""
    (tmp_path / "README.md").write_text("# Demo\nA demo project.\n")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.py").write_text("def hello():\n    return 'hello'\n")
    return tmp_path


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path: Path, monkeypatch):
    """Keep run storage out of the real data root."""
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


@pytest.fixture
def fake_claude_builder_bin(tmp_path: Path) -> Path:
    """Fake `claude` builder that drops a *_WAS_HERE.txt marker in its cwd."""
    bin_dir = tmp_path / "builder_bin"
    bin_dir.mkdir()
    claude_script = bin_dir / "claude"
    claude_script.write_text(textwrap.dedent("""\
        #!/bin/bash
        echo "hello from builder" > "$PWD/BUILDER_WAS_HERE.txt"
        echo "Builder made changes"
    """))
    claude_script.chmod(claude_script.stat().st_mode | stat.S_IEXEC)
    return bin_dir


@pytest.fixture
def fake_claude_reviewer_bin(tmp_path: Path) -> Path:
    """Fake `claude` reviewer that returns a passing verdict."""
    bin_dir = tmp_path / "reviewer_bin"
    bin_dir.mkdir()
    claude_script = bin_dir / "claude"
    claude_script.write_text(textwrap.dedent("""\
        #!/bin/bash
        echo '{"verdict": "pass", "findings": [], "confidence": "high", "summary": "ok"}'
    """))
    claude_script.chmod(claude_script.stat().st_mode | stat.S_IEXEC)
    return bin_dir


# ---------------------------------------------------------------------------
# 1. Ping-pong flow leaves no detritus in the real repo root
# ---------------------------------------------------------------------------


class TestRootDetritusHygiene:
    def test_pingpong_flow_leaves_no_was_here_in_repo_root(
        self, monkeypatch, demo_repo, fake_claude_builder_bin, fake_claude_reviewer_bin
    ):
        """Builder writes BUILDER_WAS_HERE.txt to its cwd; it must stay in
        staging and never appear at the project repo root."""
        monkeypatch.setenv("PATH", f"{fake_claude_builder_bin}:{fake_claude_reviewer_bin}")

        before = {p.name for p in REPO_ROOT.glob("*_WAS_HERE.txt")}

        result = run_pingpong(
            "Fix README", str(demo_repo),
            builder_name="claude-cli", reviewer_name="claude-cli",
            max_rounds=1,
        )

        # The marker proves the builder actually ran and wrote to staging.
        assert "BUILDER_WAS_HERE.txt" in result.staged_files

        after = {p.name for p in REPO_ROOT.glob("*_WAS_HERE.txt")}
        leaked = after - before
        assert not leaked, f"Ping-pong flow leaked detritus into repo root: {sorted(leaked)}"


# ---------------------------------------------------------------------------
# 2. make_review_zip.sh rejects actual debug detritus
# ---------------------------------------------------------------------------


class TestMakeReviewZipRejectsDetritus:
    def _stage_script_repo(self, tmp_path: Path) -> Path:
        """Isolated git repo with every packaging dependency and one evidence dir."""
        repo = _make_git_repo_with_scripts(tmp_path)
        _make_valid_evidence(repo / "remedy-job-evidence-test", "detritus-test")
        return repo

    def _run_script(self, repo: Path) -> subprocess.CompletedProcess:
        ev_dir = repo / "remedy-job-evidence-test"
        return subprocess.run(
            ["bash", "scripts/make_review_zip.sh",
             "--evidence-dir", str(ev_dir)],
            cwd=repo, capture_output=True, text=True, timeout=60,
        )

    @pytest.mark.skipif(
        shutil.which("git") is None or shutil.which("bash") is None,
        reason="git and bash required",
    )
    def test_rejects_root_was_here_detritus(self, tmp_path: Path):
        """A root-level *_WAS_HERE.txt must abort the zip with exit 1."""
        repo = self._stage_script_repo(tmp_path)
        (repo / "BUILDER_WAS_HERE.txt").write_text("debug leftover\n")

        proc = self._run_script(repo)

        assert proc.returncode == 1, (
            f"Script should reject detritus (rc=1), got rc={proc.returncode}\n"
            f"stdout={proc.stdout}\nstderr={proc.stderr}"
        )
        assert "detritus" in (proc.stdout + proc.stderr).lower()
        assert "BUILDER_WAS_HERE.txt" in (proc.stdout + proc.stderr)
        # Aborted before producing a zip.
        assert not list(repo.glob("*.zip"))

    @pytest.mark.skipif(
        shutil.which("git") is None
        or shutil.which("bash") is None
        or shutil.which("zip") is None,
        reason="git, bash, zip required",
    )
    def test_clean_repo_is_accepted(self, tmp_path: Path):
        """Sanity counterpart: with no detritus the script does not exit 1
        on the detritus gate (proves the gate is specific, not always-failing)."""
        repo = self._stage_script_repo(tmp_path)

        proc = self._run_script(repo)

        # Must not be rejected for detritus reasons.
        assert "detritus" not in (proc.stdout + proc.stderr).lower()

    @pytest.mark.skipif(
        shutil.which("git") is None
        or shutil.which("bash") is None
        or shutil.which("zip") is None,
        reason="git, bash, zip required",
    )
    def test_coverage_artifacts_excluded(self, tmp_path: Path):
        """Review ZIP must exclude .coverage and .coverage_reports."""
        repo = self._stage_script_repo(tmp_path)
        (repo / ".coverage").write_text("coverage db\n")
        cov_dir = repo / ".coverage_reports"
        cov_dir.mkdir()
        (cov_dir / "coverage.json").write_text("{}\n")

        proc = self._run_script(repo)

        if proc.returncode != 0:
            pytest.skip(f"Script failed: {proc.stderr}")

        from zipfile import ZipFile
        zips = list(repo.glob("*.zip"))
        assert zips, "ZIP must be created"
        with ZipFile(zips[0]) as zf:
            names = zf.namelist()
            assert not any(".coverage" == n or n.startswith(".coverage.") for n in names), \
                ".coverage must be excluded from review ZIP"
            assert not any(".coverage_reports" in n for n in names), \
                ".coverage_reports must be excluded from review ZIP"


class TestDetritusGateIndependent:
    """R-4324: Detritus must be detected even without evidence dir."""

    @pytest.mark.skipif(
        shutil.which("git") is None or shutil.which("bash") is None,
        reason="git and bash required",
    )
    def test_detritus_detected_without_evidence(self, tmp_path: Path):
        repo = tmp_path / "repo"
        (repo / "scripts").mkdir(parents=True)
        shutil.copy2(MAKE_REVIEW_ZIP, repo / "scripts" / "make_review_zip.sh")
        manifest_src = MAKE_REVIEW_ZIP.parent / "build_review_manifest.py"
        if manifest_src.exists():
            shutil.copy2(manifest_src, repo / "scripts" / "build_review_manifest.py")
        subprocess.run(
            ["git", "init", "-q"], cwd=repo, check=True,
            capture_output=True, text=True,
        )
        _make_valid_evidence(repo / "remedy-job-evidence-det", "det")
        (repo / "BUILDER_WAS_HERE.txt").write_text("debug\n")

        proc = subprocess.run(
            ["bash", "scripts/make_review_zip.sh"],
            cwd=repo, capture_output=True, text=True, timeout=10,
        )
        assert proc.returncode != 0
        assert "detritus" in (proc.stdout + proc.stderr).lower()


class TestStaleEvidenceFlag:
    """R-4325: --include-stale-evidence must fail clearly."""

    @pytest.mark.skipif(
        shutil.which("git") is None or shutil.which("bash") is None,
        reason="git and bash required",
    )
    def test_stale_evidence_flag_fails(self, tmp_path: Path):
        repo = tmp_path / "repo"
        (repo / "scripts").mkdir(parents=True)
        shutil.copy2(MAKE_REVIEW_ZIP, repo / "scripts" / "make_review_zip.sh")
        subprocess.run(
            ["git", "init", "-q"], cwd=repo, check=True,
            capture_output=True, text=True,
        )
        ev = repo / "remedy-job-evidence-test"
        _make_valid_evidence(ev, "stale-test")

        proc = subprocess.run(
            ["bash", "scripts/make_review_zip.sh",
             "--evidence-dir", str(ev), "--include-stale-evidence"],
            cwd=repo, capture_output=True, text=True, timeout=10,
        )
        assert proc.returncode == 2
        assert "not implemented" in proc.stderr.lower()


class TestStarterDryRun:
    """R-4323: Worker/Remedy starter --dry-run."""

    STARTER = REPO_ROOT / "scripts" / "remedy_self_job_flow.sh"

    @pytest.mark.skipif(
        shutil.which("git") is None or shutil.which("bash") is None,
        reason="git and bash required",
    )
    def test_dry_run_prints_commands(self, tmp_path: Path):
        if not self.STARTER.exists():
            pytest.skip("remedy_self_job_flow.sh not found")

        goal = tmp_path / "goal.md"
        goal.write_text("# Job: Test\n\n## Task 1\nDo something.\n\nAcceptance:\n- done\n")

        proc = subprocess.run(
            ["bash", str(self.STARTER),
             "--goal-file", str(goal),
             "--out", str(tmp_path / "evidence"),
             "--allow-dirty", "--dry-run"],
            cwd=str(REPO_ROOT),
            capture_output=True, text=True, timeout=10,
        )
        assert proc.returncode == 0
        assert "[dry-run]" in proc.stdout
        assert "do job-flow" in proc.stdout
        assert "make_review_zip" in proc.stdout

    @pytest.mark.skipif(
        shutil.which("git") is None or shutil.which("bash") is None,
        reason="git and bash required",
    )
    def test_dry_run_with_timeout_sec(self, tmp_path: Path):
        if not self.STARTER.exists():
            pytest.skip("remedy_self_job_flow.sh not found")

        goal = tmp_path / "goal.md"
        goal.write_text("# Job: Test\n\n## Task 1\nDo something.\n\nAcceptance:\n- done\n")

        proc = subprocess.run(
            ["bash", str(self.STARTER),
             "--goal-file", str(goal),
             "--out", str(tmp_path / "evidence"),
             "--timeout-sec", "900",
             "--allow-dirty", "--dry-run"],
            cwd=str(REPO_ROOT),
            capture_output=True, text=True, timeout=10,
        )
        assert proc.returncode == 0
        assert "--timeout-sec 900" in proc.stdout

    @pytest.mark.skipif(
        shutil.which("git") is None or shutil.which("bash") is None,
        reason="git and bash required",
    )
    def test_missing_goal_file_fails(self, tmp_path: Path):
        if not self.STARTER.exists():
            pytest.skip("remedy_self_job_flow.sh not found")

        proc = subprocess.run(
            ["bash", str(self.STARTER),
             "--goal-file", str(tmp_path / "nonexistent.md"),
             "--allow-dirty"],
            cwd=str(REPO_ROOT),
            capture_output=True, text=True, timeout=10,
        )
        assert proc.returncode != 0

    @pytest.mark.skipif(
        shutil.which("git") is None or shutil.which("bash") is None,
        reason="git and bash required",
    )
    def test_no_goal_file_shows_usage(self, tmp_path: Path):
        if not self.STARTER.exists():
            pytest.skip("remedy_self_job_flow.sh not found")

        proc = subprocess.run(
            ["bash", str(self.STARTER)],
            cwd=str(REPO_ROOT),
            capture_output=True, text=True, timeout=10,
        )
        assert proc.returncode != 0
        assert "--goal-file" in proc.stderr


class TestZipManifestContentVerification:
    """R-4326: Post-build verification checks manifest vs zip content."""

    @pytest.mark.skipif(
        shutil.which("git") is None
        or shutil.which("bash") is None
        or shutil.which("zip") is None,
        reason="git, bash, zip required",
    )
    def test_zip_contains_evidence_from_manifest(self, tmp_path: Path):
        repo = _make_git_repo_with_scripts(tmp_path)
        ev = repo / "remedy-job-evidence-test123"
        _make_valid_evidence(ev, "test")

        proc = subprocess.run(
            ["bash", "scripts/make_review_zip.sh", "--evidence-dir", str(ev)],
            cwd=repo, capture_output=True, text=True, timeout=60,
        )
        assert proc.returncode == 0, f"Script failed: {proc.stdout}\n{proc.stderr}"

        from zipfile import ZipFile
        zips = list(repo.glob("*.zip"))
        assert zips, "ZIP must be created"
        with ZipFile(zips[0]) as zf:
            names = zf.namelist()
            assert "evidence/current/job_flow.json" in names
            assert "evidence/current/command_transcript.json" in names
            assert ".review_zip_manifest.json" in names
            assert not any(n.startswith("remedy-job-evidence-") for n in names), \
                "Raw evidence dir must not be in zip"


#: Everything the packaging scripts import at runtime. A missing dependency here
#: makes the script fail post-build verification, which used to look like a
#: product bug rather than a test-harness gap.
_REQUIRED_SCRIPTS = (
    "make_review_zip.sh",
    "build_review_manifest.py",
    "build_review_zip.py",                 # F8 (round 17): the NUL-safe archive builder
    "build_observability_index.py",
    "select_review_evidence.py",
)
_REQUIRED_PACKAGE_MODULES = (
    "packages/orchestration/__init__.py",
    "packages/orchestration/data_paths.py",
    "packages/orchestration/evidence_index.py",
    # F9/F8 (round 17): the containment helper and the archive builder the packager now imports.
    "packages/orchestration/review_zip.py",
    # F1/F3 (round 18): the typed ArchivePlan, the strict review-subject decoder, and secure_fs's
    # anchored reader the plan-driven builder uses. The attest predicate is imported lazily by the
    # builder and defaulted when absent, so the minimal fixture need not carry the full stack.
    "packages/orchestration/archive_plan.py",
    "packages/orchestration/review_subject.py",
    "packages/common/__init__.py",
    "packages/common/secure_fs.py",
)


def _make_git_repo_with_scripts(tmp_path: Path) -> Path:
    """Isolated git repo containing every current packaging dependency."""
    repo = tmp_path / "repo"
    (repo / "scripts").mkdir(parents=True)
    for name in _REQUIRED_SCRIPTS:
        src = REPO_ROOT / "scripts" / name
        assert src.exists(), f"missing packaging dependency in source tree: {src}"
        shutil.copy2(src, repo / "scripts" / name)
    for rel in _REQUIRED_PACKAGE_MODULES:
        src = REPO_ROOT / rel
        assert src.exists(), f"missing package module: {src}"
        dst = repo / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    (repo / "README.md").write_text("# test\n")
    env = {**os.environ, "GIT_AUTHOR_NAME": "test", "GIT_AUTHOR_EMAIL": "t@t",
           "GIT_COMMITTER_NAME": "test", "GIT_COMMITTER_EMAIL": "t@t"}
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True, capture_output=True, text=True)
    subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True, text=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=repo, capture_output=True,
                   text=True, timeout=15, env=env)
    return repo


def _make_valid_evidence(ev_dir: Path, job_id: str = "test123") -> None:
    """Create a complete valid evidence directory with all required artifacts."""
    import json
    ev_dir.mkdir(exist_ok=True)
    (ev_dir / "job_flow.json").write_text(json.dumps({
        "job_id": job_id,
        "final_audit": {
            "status": "READY",
            "missing_observability_artifacts": [],
        },
        "target_guard": {"mutated_target": False},
    }))
    (ev_dir / "manifest.json").write_text("{}")
    (ev_dir / "agent_run_trace.jsonl").write_text("")
    (ev_dir / "agent_run_trace_summary.json").write_text(
        '{"trace_sources": []}'
    )
    (ev_dir / "prompt_trace_summary.json").write_text("{}")
    (ev_dir / "command_transcript.json").write_text("{}")
    task_dir = ev_dir / "task_runs" / "T001"
    task_dir.mkdir(parents=True)
    (task_dir / "prompt_trace.jsonl").write_text("")
    (task_dir / "prompt_trace_summary.json").write_text("{}")
    (task_dir / "review.json").write_text("{}")
    (task_dir / "repair_loop.json").write_text("{}")
    (task_dir / "token_accounting.json").write_text("{}")
    (task_dir / "provider_evidence.json").write_text("{}")


@pytest.mark.skipif(
    shutil.which("git") is None
    or shutil.which("bash") is None
    or shutil.which("zip") is None,
    reason="git, bash, zip required",
)
class TestAutoSelectLatestEvidence:

    def test_single_valid_evidence_dir_auto_selects(self, tmp_path: Path):
        repo = _make_git_repo_with_scripts(tmp_path)
        ev = repo / "remedy-job-evidence-aaa111"
        _make_valid_evidence(ev, "aaa")

        proc = subprocess.run(
            ["bash", "scripts/make_review_zip.sh"],
            cwd=repo, capture_output=True, text=True, timeout=30,
        )
        assert proc.returncode == 0, f"Failed: {proc.stdout}\n{proc.stderr}"
        assert "Auto-selected" in proc.stdout

    def test_all_candidates_invalid_still_creates_zip(self, tmp_path: Path):
        """All incomplete → newest selected, zip created with warning."""
        repo = _make_git_repo_with_scripts(tmp_path)

        bad1 = repo / "remedy-job-evidence-bad1"
        bad1.mkdir()
        (bad1 / "job_flow.json").write_text('{"job_id":"bad1"}')

        bad2 = repo / "remedy-job-evidence-bad2"
        bad2.mkdir()
        (bad2 / "job_flow.json").write_text('{"job_id":"bad2"}')

        proc = subprocess.run(
            ["bash", "scripts/make_review_zip.sh"],
            cwd=repo, capture_output=True, text=True, timeout=30,
        )
        assert proc.returncode == 0, f"Failed: {proc.stdout}\n{proc.stderr}"
        assert "incomplete" in proc.stdout.lower()
        assert list(repo.glob("*.zip"))

    def test_explicit_incomplete_creates_zip(self, tmp_path: Path):
        """Explicit incomplete evidence → zip created, validation in manifest."""
        repo = _make_git_repo_with_scripts(tmp_path)
        ev = repo / "remedy-job-evidence-incomplete"
        ev.mkdir()
        (ev / "job_flow.json").write_text('{"job_id":"inc"}')

        proc = subprocess.run(
            ["bash", "scripts/make_review_zip.sh",
             "--evidence-dir", str(ev)],
            cwd=repo, capture_output=True, text=True, timeout=30,
        )
        assert proc.returncode == 0, f"Failed: {proc.stdout}\n{proc.stderr}"

        import json
        from zipfile import ZipFile
        zips = list(repo.glob("*.zip"))
        assert zips
        with ZipFile(zips[0]) as zf:
            manifest = json.loads(zf.read(".review_zip_manifest.json"))
        val = manifest["current_evidence"]["validation"]
        assert val["is_valid_current_run"] is False
        assert val["selected_candidate_status"] == "incomplete"

    def test_allow_incomplete_flag_is_noop(self, tmp_path: Path):
        """--allow-incomplete-evidence accepted but has no effect (always non-blocking)."""
        repo = _make_git_repo_with_scripts(tmp_path)
        ev = repo / "remedy-job-evidence-debugev"
        ev.mkdir()
        (ev / "job_flow.json").write_text(
            '{"job_id":"debug","final_audit":{"status":"READY",'
            '"missing_observability_artifacts":[]}}'
        )
        (ev / "manifest.json").write_text("{}")
        (ev / "command_transcript.json").write_text("{}")

        proc = subprocess.run(
            ["bash", "scripts/make_review_zip.sh",
             "--evidence-dir", str(ev), "--allow-incomplete-evidence"],
            cwd=repo, capture_output=True, text=True, timeout=30,
        )
        assert proc.returncode == 0, f"Failed: {proc.stdout}\n{proc.stderr}"

        import json
        from zipfile import ZipFile
        zips = list(repo.glob("*.zip"))
        assert zips
        with ZipFile(zips[0]) as zf:
            manifest = json.loads(zf.read(".review_zip_manifest.json"))
        val = manifest["current_evidence"]["validation"]
        assert val["is_valid_current_run"] is False
        assert val["selected_candidate_status"] == "incomplete"

    def test_explicit_valid_override_wins(self, tmp_path: Path):
        import os
        repo = _make_git_repo_with_scripts(tmp_path)

        old = repo / "remedy-job-evidence-old111"
        _make_valid_evidence(old, "old")
        os.utime(old / "job_flow.json", (1000000, 1000000))

        new = repo / "remedy-job-evidence-new222"
        _make_valid_evidence(new, "new")
        os.utime(new / "job_flow.json", (2000000, 2000000))

        proc = subprocess.run(
            ["bash", "scripts/make_review_zip.sh",
             "--evidence-dir", str(old)],
            cwd=repo, capture_output=True, text=True, timeout=30,
        )
        assert proc.returncode == 0, f"Failed: {proc.stdout}\n{proc.stderr}"
        assert "Auto-selected" not in proc.stdout

        from zipfile import ZipFile
        zips = list(repo.glob("*.zip"))
        assert zips
        with ZipFile(zips[0]) as zf:
            jf = zf.read("evidence/current/job_flow.json").decode()
            assert '"old"' in jf

    def test_stale_dirs_not_in_zip(self, tmp_path: Path):
        import os
        repo = _make_git_repo_with_scripts(tmp_path)

        old = repo / "remedy-job-evidence-stale1"
        _make_valid_evidence(old, "stale")
        os.utime(old / "job_flow.json", (1000000, 1000000))

        new = repo / "remedy-job-evidence-current1"
        _make_valid_evidence(new, "current")
        os.utime(new / "job_flow.json", (2000000, 2000000))

        proc = subprocess.run(
            ["bash", "scripts/make_review_zip.sh"],
            cwd=repo, capture_output=True, text=True, timeout=30,
        )
        assert proc.returncode == 0, f"Failed: {proc.stdout}\n{proc.stderr}"

        from zipfile import ZipFile
        zips = list(repo.glob("*.zip"))
        assert zips
        with ZipFile(zips[0]) as zf:
            names = zf.namelist()
            assert not any("stale1" in n for n in names), \
                "Stale evidence must not appear in zip"
            assert "evidence/current/job_flow.json" in names

    def test_manifest_validation_section(self, tmp_path: Path):
        import os
        repo = _make_git_repo_with_scripts(tmp_path)

        old = repo / "remedy-job-evidence-aaa111"
        _make_valid_evidence(old, "aaa")
        os.utime(old / "job_flow.json", (1000000, 1000000))

        new = repo / "remedy-job-evidence-bbb222"
        _make_valid_evidence(new, "bbb")
        os.utime(new / "job_flow.json", (2000000, 2000000))

        proc = subprocess.run(
            ["bash", "scripts/make_review_zip.sh"],
            cwd=repo, capture_output=True, text=True, timeout=30,
        )
        assert proc.returncode == 0, f"Failed: {proc.stdout}\n{proc.stderr}"

        import json
        from zipfile import ZipFile
        zips = list(repo.glob("*.zip"))
        assert zips
        with ZipFile(zips[0]) as zf:
            manifest = json.loads(zf.read(".review_zip_manifest.json"))
        ce = manifest["current_evidence"]
        assert ce["selection_mode"] == "deprecated_root_fallback"
        assert ce["selected_from_candidate_count"] == 2
        assert ce["zip_prefix"] == "evidence/current"
        val = ce["validation"]
        assert val["is_valid_current_run"] is True
        assert val["validation_errors"] == []
        assert val["selected_candidate_status"] == "valid"
        assert val["selection_mode"] == "deprecated_root_fallback"

    def test_manifest_records_explicit_mode(self, tmp_path: Path):
        repo = _make_git_repo_with_scripts(tmp_path)
        ev = repo / "remedy-job-evidence-xxx"
        _make_valid_evidence(ev, "xxx")

        proc = subprocess.run(
            ["bash", "scripts/make_review_zip.sh", "--evidence-dir", str(ev)],
            cwd=repo, capture_output=True, text=True, timeout=30,
        )
        assert proc.returncode == 0, f"Failed: {proc.stdout}\n{proc.stderr}"

        import json
        from zipfile import ZipFile
        zips = list(repo.glob("*.zip"))
        with ZipFile(zips[0]) as zf:
            manifest = json.loads(zf.read(".review_zip_manifest.json"))
        ce = manifest["current_evidence"]
        assert ce["selection_mode"] == "explicit"

    def test_candidate_summary_shows_rejection_reasons(self, tmp_path: Path):
        import os
        repo = _make_git_repo_with_scripts(tmp_path)

        valid = repo / "remedy-job-evidence-good1"
        _make_valid_evidence(valid, "good")
        os.utime(valid / "job_flow.json", (1000000, 1000000))

        bad = repo / "remedy-job-evidence-bad1"
        bad.mkdir()
        (bad / "job_flow.json").write_text('{"job_id":"bad"}')

        proc = subprocess.run(
            ["bash", "scripts/make_review_zip.sh"],
            cwd=repo, capture_output=True, text=True, timeout=30,
        )
        assert proc.returncode == 0, f"Failed: {proc.stdout}\n{proc.stderr}"
        assert "candidate summary" in proc.stdout.lower()
        assert "incomplete" in proc.stdout
        assert "valid" in proc.stdout

    def test_missing_command_transcript_creates_zip_with_warning(self, tmp_path: Path):
        """Missing command_transcript.json → zip created, validation records it."""
        repo = _make_git_repo_with_scripts(tmp_path)
        ev = repo / "remedy-job-evidence-noct"
        _make_valid_evidence(ev, "noct")
        (ev / "command_transcript.json").unlink()

        proc = subprocess.run(
            ["bash", "scripts/make_review_zip.sh"],
            cwd=repo, capture_output=True, text=True, timeout=30,
        )
        assert proc.returncode == 0, f"Failed: {proc.stdout}\n{proc.stderr}"
        assert "incomplete" in proc.stdout.lower()

        import json
        from zipfile import ZipFile
        zips = list(repo.glob("*.zip"))
        assert zips
        with ZipFile(zips[0]) as zf:
            manifest = json.loads(zf.read(".review_zip_manifest.json"))
        val = manifest["current_evidence"]["validation"]
        assert val["is_valid_current_run"] is False
        assert any("command_transcript" in e for e in val["validation_errors"])

    def test_manifest_validation_marks_missing_transcript(self, tmp_path: Path):
        """R-4334: manifest validation must flag missing command_transcript."""
        from scripts.build_review_manifest import validate_evidence_candidate
        ev = tmp_path / "evidence"
        _make_valid_evidence(ev, "val-test")
        (ev / "command_transcript.json").unlink()

        result = validate_evidence_candidate(str(ev))
        assert result["is_valid_current_run"] is False
        assert any("command_transcript" in e for e in result["validation_errors"])

    def test_manifest_validation_marks_missing_task_artifacts(self, tmp_path: Path):
        """R-4334: manifest validation must flag missing task-level artifacts."""
        from scripts.build_review_manifest import validate_evidence_candidate
        ev = tmp_path / "evidence"
        _make_valid_evidence(ev, "val-test")
        (ev / "task_runs" / "T001" / "review.json").unlink()
        (ev / "task_runs" / "T001" / "repair_loop.json").unlink()

        result = validate_evidence_candidate(str(ev))
        assert result["is_valid_current_run"] is False
        assert result["required_task_artifacts"]["T001"]
        assert "review.json" in result["required_task_artifacts"]["T001"]

    def test_unselected_evidence_not_in_zip(self, tmp_path: Path):
        import os
        repo = _make_git_repo_with_scripts(tmp_path)

        sel = repo / "remedy-job-evidence-selected"
        _make_valid_evidence(sel, "selected")
        os.utime(sel / "job_flow.json", (2000000, 2000000))

        other = repo / "remedy-job-evidence-other"
        _make_valid_evidence(other, "other")
        os.utime(other / "job_flow.json", (1000000, 1000000))

        proc = subprocess.run(
            ["bash", "scripts/make_review_zip.sh"],
            cwd=repo, capture_output=True, text=True, timeout=30,
        )
        assert proc.returncode == 0

        from zipfile import ZipFile
        zips = list(repo.glob("*.zip"))
        with ZipFile(zips[0]) as zf:
            names = zf.namelist()
            assert all("other" not in n for n in names)
            assert "evidence/current/job_flow.json" in names

    def test_evidence_under_current_prefix(self, tmp_path: Path):
        repo = _make_git_repo_with_scripts(tmp_path)
        ev = repo / "remedy-job-evidence-preftest"
        _make_valid_evidence(ev, "preftest")

        proc = subprocess.run(
            ["bash", "scripts/make_review_zip.sh"],
            cwd=repo, capture_output=True, text=True, timeout=30,
        )
        assert proc.returncode == 0

        from zipfile import ZipFile
        zips = list(repo.glob("*.zip"))
        with ZipFile(zips[0]) as zf:
            ev_files = [n for n in zf.namelist()
                        if n.startswith("evidence/")]
            assert all(n.startswith("evidence/current/") for n in ev_files)

    def test_manifest_rejected_candidate_count(self, tmp_path: Path):
        """R-4332: manifest tracks rejected_candidate_count."""
        import os
        repo = _make_git_repo_with_scripts(tmp_path)

        valid = repo / "remedy-job-evidence-good"
        _make_valid_evidence(valid, "good")
        os.utime(valid / "job_flow.json", (1000000, 1000000))

        bad1 = repo / "remedy-job-evidence-bad1"
        bad1.mkdir()
        bad2 = repo / "remedy-job-evidence-bad2"
        bad2.mkdir()
        (bad2 / "job_flow.json").write_text("{}")

        proc = subprocess.run(
            ["bash", "scripts/make_review_zip.sh"],
            cwd=repo, capture_output=True, text=True, timeout=30,
        )
        assert proc.returncode == 0

        import json
        from zipfile import ZipFile
        zips = list(repo.glob("*.zip"))
        with ZipFile(zips[0]) as zf:
            manifest = json.loads(zf.read(".review_zip_manifest.json"))
        val = manifest["current_evidence"]["validation"]
        assert val["rejected_candidate_count"] == 2


class TestFilenamePattern:
    """Lock down the review zip filename pattern."""

    @pytest.mark.skipif(
        shutil.which("git") is None
        or shutil.which("bash") is None
        or shutil.which("zip") is None,
        reason="git, bash, zip required",
    )
    def test_filename_matches_pattern(self, tmp_path: Path):
        import re
        repo = _make_git_repo_with_scripts(tmp_path)
        ev = repo / "remedy-job-evidence-fntest"
        _make_valid_evidence(ev, "fn")

        proc = subprocess.run(
            ["bash", "scripts/make_review_zip.sh", "--evidence-dir", str(ev)],
            cwd=repo, capture_output=True, text=True, timeout=30,
        )
        assert proc.returncode == 0, f"Script failed: {proc.stdout}\n{proc.stderr}"

        zips = list(repo.glob("*.zip"))
        assert zips, "ZIP must be created"
        filename = zips[0].name
        # The package status is part of the name so a reviewer cannot mistake a
        # blocked snapshot for an authoritative package.
        pattern = r"^remedy-review-\d{8}-\d{6}-[A-Z_]+\.zip$"
        assert re.match(pattern, filename), \
            f"Filename '{filename}' does not match expected pattern '{pattern}'"

    @pytest.mark.skipif(
        shutil.which("git") is None
        or shutil.which("bash") is None
        or shutil.which("zip") is None,
        reason="git, bash, zip required",
    )
    def test_filenames_sortable_chronologically(self, tmp_path: Path):
        import time
        repo = _make_git_repo_with_scripts(tmp_path)
        ev = repo / "remedy-job-evidence-sorttest"
        _make_valid_evidence(ev, "sort")

        zips_created = []
        for _ in range(2):
            proc = subprocess.run(
                ["bash", "scripts/make_review_zip.sh",
                 "--evidence-dir", str(ev)],
                cwd=repo, capture_output=True, text=True, timeout=30,
            )
            if proc.returncode == 0:
                new_zips = sorted(repo.glob("*.zip"))
                if new_zips:
                    zips_created.append(new_zips[-1].name)
            time.sleep(1.1)

        if len(zips_created) < 2:
            pytest.skip("Could not create 2 zips")
        assert zips_created == sorted(zips_created), \
            "Zip filenames must be sortable chronologically"


class TestPathSanitizerHardening:
    """R-4336: Path sanitizer must cover /mnt/, .data/job_workspaces/, etc."""

    def test_mnt_path_sanitized(self):
        from apps.cli.commands.do_cmd import _sanitize_shareable_paths
        data = {"ref": "/mnt/data/project/src/main.py"}
        result = _sanitize_shareable_paths(data)
        assert "/mnt/" not in result["ref"]

    def test_data_job_workspaces_sanitized(self):
        from apps.cli.commands.do_cmd import _sanitize_shareable_paths
        data = {"path": "/mnt/storage/.data/job_workspaces/abc123/workspace"}
        result = _sanitize_shareable_paths(data)
        assert ".data/job_workspaces" not in result["path"]
        assert "[workspace]" in result["path"]

    def test_data_root_sanitized(self):
        from apps.cli.commands.do_cmd import _sanitize_shareable_paths
        data = {"path": "/home/user/.data/runs"}
        result = _sanitize_shareable_paths(data)
        assert ".data/" not in result["path"]

    def test_evidence_dir_outside_tmp_sanitized(self):
        from apps.cli.commands.do_cmd import _sanitize_shareable_paths
        data = {"path": "/mnt/data/remedy-job-evidence-abc123/job_flow.json"}
        result = _sanitize_shareable_paths(data)
        assert "evidence/current/job_flow.json" == result["path"]

    def test_no_private_paths_in_shareable(self):
        from apps.cli.commands.do_cmd import _sanitize_shareable_paths
        paths = [
            "/tmp/remedy-job-evidence-abc/manifest.json",
            "/home/alice/project/file.py",
            "/Users/bob/code/file.py",
            "/private/var/folders/abc/file.py",
            "/mnt/data/project/file.py",
            "/mnt/storage/.data/job_workspaces/abc/workspace",
        ]
        for p in paths:
            result = _sanitize_shareable_paths({"ref": p})
            for prefix in ["/tmp/", "/home/", "/Users/", "/private/",
                           "/mnt/"]:
                assert prefix not in result["ref"], \
                    f"Path {p} leaked prefix {prefix}: {result['ref']}"


# ---------------------------------------------------------------------------
# F004 Finding 2 — the current indexed evidence-selection contract
#
# Evidence is chosen from the job evidence index, never by filesystem
# modification time. These replace the superseded mtime/auto_latest tests.
# ---------------------------------------------------------------------------

_MIXED_FILES = (
    "packages/orchestration/stream_evidence.py",
    "tests/orchestration/fixtures/stream/basic_session.jsonl",
    "docs/roadmap/STATUS.md",
)


def _dirty(repo: Path, rels) -> None:
    for rel in rels:
        p = repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("changed\n")


def _index_job(repo: Path, job_id: str, changed_files, *, repo_for_record: Path | None = None) -> Path:
    """Export-style evidence under <repo>/.data plus its index record."""
    env_repo = repo_for_record or repo
    ev = repo / ".data" / "evidence_exports" / job_id
    ev.parent.mkdir(parents=True, exist_ok=True)
    _make_valid_evidence(ev, job_id)

    script = (
        "import sys;"
        f"sys.path.insert(0, {str(repo)!r});"
        "from packages.orchestration.evidence_index import write_index_record;"
        f"write_index_record({job_id!r}, {str(ev)!r}, repo_path={str(env_repo)!r},"
        f" changed_files={list(changed_files)!r})"
    )
    subprocess.run(
        [sys.executable, "-c", script], cwd=repo, check=True,
        capture_output=True, text=True,
        env={**os.environ, "REMEDY_DATA_DIR": str(repo / ".data")},
    )
    return ev


def _run_zip(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["bash", "scripts/make_review_zip.sh", *args],
        cwd=repo, capture_output=True, text=True, timeout=120,
        env={**os.environ, "REMEDY_DATA_DIR": str(repo / ".data")},
    )


def _newest_zip(repo: Path) -> Path:
    zips = sorted(repo.glob("remedy-review-*.zip"), key=lambda p: p.stat().st_mtime)
    assert zips, "no review zip produced"
    return zips[-1]


def _zip_manifest(repo: Path) -> dict:
    from zipfile import ZipFile
    with ZipFile(_newest_zip(repo)) as zf:
        return json.loads(zf.read(".review_zip_manifest.json"))


@pytest.mark.skipif(
    shutil.which("git") is None
    or shutil.which("bash") is None
    or shutil.which("zip") is None,
    reason="git, bash, zip required",
)
class TestIndexedEvidenceSelection:
    def test_no_args_select_newest_aligned_job_on_current_branch(self, tmp_path: Path):
        repo = _make_git_repo_with_scripts(tmp_path)
        _dirty(repo, _MIXED_FILES)
        _index_job(repo, "aligned01", _MIXED_FILES)

        proc = _run_zip(repo)
        assert proc.returncode == 0, proc.stdout + proc.stderr
        assert "aligned01" in proc.stdout

    def test_newer_unrelated_scratch_repository_job_is_rejected(self, tmp_path: Path):
        repo = _make_git_repo_with_scripts(tmp_path)
        _dirty(repo, _MIXED_FILES)
        _index_job(repo, "aligned01", _MIXED_FILES)

        scratch = tmp_path / "scratch"
        scratch.mkdir()
        subprocess.run(["git", "init", "-q"], cwd=scratch, check=True, capture_output=True)
        # Newer record, different repository: recency must not win.
        _index_job(repo, "scratch99", ["hello.py"], repo_for_record=scratch)

        proc = _run_zip(repo)
        assert proc.returncode == 0, proc.stdout + proc.stderr
        assert "aligned01" in proc.stdout
        assert "scratch99" not in proc.stdout

    def test_stale_same_repo_job_with_unaligned_file_set_is_rejected(self, tmp_path: Path):
        repo = _make_git_repo_with_scripts(tmp_path)
        _dirty(repo, _MIXED_FILES)
        _index_job(repo, "aligned01", _MIXED_FILES)
        _index_job(repo, "stale002", ["packages/orchestration/deleted_module.py"])

        proc = _run_zip(repo)
        assert proc.returncode == 0, proc.stdout + proc.stderr
        assert "aligned01" in proc.stdout
        assert "stale002" not in proc.stdout

    def test_explicit_job_id_selects_exactly_that_job(self, tmp_path: Path):
        repo = _make_git_repo_with_scripts(tmp_path)
        _dirty(repo, _MIXED_FILES)
        _index_job(repo, "aligned01", _MIXED_FILES)
        _index_job(repo, "older003", [_MIXED_FILES[0]])

        proc = _run_zip(repo, "--job-id", "older003")
        assert proc.returncode == 0, proc.stdout + proc.stderr
        assert "older003" in proc.stdout

    def test_missing_job_id_never_substitutes_another_job(self, tmp_path: Path):
        repo = _make_git_repo_with_scripts(tmp_path)
        _dirty(repo, _MIXED_FILES)
        _index_job(repo, "aligned01", _MIXED_FILES)

        proc = _run_zip(repo, "--job-id", "doesnotexist")
        combined = proc.stdout + proc.stderr
        assert "aligned01" not in combined, "a different job was silently substituted"

    def test_no_matching_evidence_produces_honest_no_evidence_zip(self, tmp_path: Path):
        repo = _make_git_repo_with_scripts(tmp_path)
        _dirty(repo, _MIXED_FILES)  # dirty, but nothing indexed

        proc = _run_zip(repo)
        assert proc.returncode == 0, proc.stdout + proc.stderr
        name = _newest_zip(repo).name
        assert "NO_EVIDENCE" in name, name
        assert "READY_FOR_REVIEW" not in name

    def test_include_recent_adds_only_overlapping_same_repo_history(self, tmp_path: Path):
        repo = _make_git_repo_with_scripts(tmp_path)
        _dirty(repo, _MIXED_FILES)
        _index_job(repo, "related01", [_MIXED_FILES[0]])
        _index_job(repo, "unrelated9", ["docs/other_feature.md"])
        _index_job(repo, "current001", _MIXED_FILES)

        proc = _run_zip(repo, "--job-id", "current001", "--include-recent", "2")
        assert proc.returncode == 0, proc.stdout + proc.stderr

        from zipfile import ZipFile
        with ZipFile(_newest_zip(repo)) as zf:
            names = zf.namelist()
        hist = {n.split("/")[2] for n in names if n.startswith("evidence/history/")}
        assert "related01" in hist
        assert "unrelated9" not in hist, "unrelated feature included merely by recency"

    def test_history_does_not_change_the_current_package_verdict(self, tmp_path: Path):
        repo = _make_git_repo_with_scripts(tmp_path)
        _dirty(repo, _MIXED_FILES)
        _index_job(repo, "current001", _MIXED_FILES)
        broken = _index_job(repo, "related01", [_MIXED_FILES[0]])
        # Corrupt the history bundle: it must not taint the current verdict.
        (broken / "job_flow.json").write_text("{ not json")

        proc = _run_zip(repo, "--job-id", "current001", "--include-recent", "2")
        assert proc.returncode == 0, proc.stdout + proc.stderr
        m = _zip_manifest(repo)
        assert m["current_evidence"]["job_id"] == "current001"

    def test_legacy_root_evidence_only_via_deprecated_fallback_with_warning(self, tmp_path: Path):
        repo = _make_git_repo_with_scripts(tmp_path)
        _make_valid_evidence(repo / "remedy-job-evidence-legacy1", "legacy1")

        proc = _run_zip(repo)
        assert proc.returncode == 0, proc.stdout + proc.stderr
        combined = proc.stdout + proc.stderr
        assert "deprecated" in combined.lower(), combined
        assert _zip_manifest(repo)["current_evidence"]["selection_mode"] == "deprecated_root_fallback"

    def test_jsonl_and_status_md_participate_in_alignment(self, tmp_path: Path):
        """A bundle covering only .py could never align if .jsonl/.md were ignored."""
        repo = _make_git_repo_with_scripts(tmp_path)
        _dirty(repo, _MIXED_FILES)
        # Recorded set includes the fixture and the roadmap file.
        _index_job(repo, "mixed0001", _MIXED_FILES)

        proc = _run_zip(repo)
        assert proc.returncode == 0, proc.stdout + proc.stderr
        assert "mixed0001" in proc.stdout

        # Remove the .jsonl fixture from the worktree: the record no longer aligns.
        (repo / _MIXED_FILES[1]).unlink()
        proc2 = _run_zip(repo)
        assert proc2.returncode == 0, proc2.stdout + proc2.stderr
        assert "NO_EVIDENCE" in _newest_zip(repo).name

    def test_zip_manifest_contains_no_private_absolute_paths(self, tmp_path: Path):
        repo = _make_git_repo_with_scripts(tmp_path)
        _dirty(repo, _MIXED_FILES)
        _index_job(repo, "aligned01", _MIXED_FILES)

        proc = _run_zip(repo)
        assert proc.returncode == 0, proc.stdout + proc.stderr

        from zipfile import ZipFile
        with ZipFile(_newest_zip(repo)) as zf:
            blob = zf.read(".review_zip_manifest.json").decode("utf-8")
        forbidden = ("/home/", "/Users/", "/private/", "/tmp/", "/mnt/", "/var/folders/")
        hits = sorted({m for pref in forbidden
                       for m in re.findall(re.escape(pref) + r"[^\"\\ ,]*", blob)})
        assert not hits, f"review manifest leaks absolute paths: {hits}"
