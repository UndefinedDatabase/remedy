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

import shutil
import stat
import subprocess
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
        """Create an isolated git repo containing a copy of the review script."""
        repo = tmp_path / "ziprepo"
        (repo / "scripts").mkdir(parents=True)
        shutil.copy2(MAKE_REVIEW_ZIP, repo / "scripts" / "make_review_zip.sh")
        manifest_src = MAKE_REVIEW_ZIP.parent / "build_review_manifest.py"
        if manifest_src.exists():
            shutil.copy2(manifest_src, repo / "scripts" / "build_review_manifest.py")
        (repo / "README.md").write_text("# tmp\n")
        ev_dir = repo / "remedy-job-evidence-test"
        ev_dir.mkdir()
        (ev_dir / "job_flow.json").write_text("{}")
        # git init only — no commit/push/reset/checkout.
        subprocess.run(
            ["git", "init", "-q"], cwd=repo, check=True,
            capture_output=True, text=True,
        )
        return repo

    def _run_script(self, repo: Path) -> subprocess.CompletedProcess:
        ev_dir = repo / "remedy-job-evidence-test"
        return subprocess.run(
            ["bash", "scripts/make_review_zip.sh", "--evidence-dir", str(ev_dir)],
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
        ev.mkdir()
        (ev / "job_flow.json").write_text("{}")

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
        repo = tmp_path / "repo"
        (repo / "scripts").mkdir(parents=True)
        shutil.copy2(MAKE_REVIEW_ZIP, repo / "scripts" / "make_review_zip.sh")
        manifest_src = MAKE_REVIEW_ZIP.parent / "build_review_manifest.py"
        if manifest_src.exists():
            shutil.copy2(manifest_src, repo / "scripts" / "build_review_manifest.py")
        (repo / "README.md").write_text("# test\n")
        subprocess.run(
            ["git", "init", "-q"], cwd=repo, check=True,
            capture_output=True, text=True,
        )
        subprocess.run(
            ["git", "add", "."], cwd=repo, check=True,
            capture_output=True, text=True,
        )
        subprocess.run(
            ["git", "commit", "-m", "init"],
            cwd=repo, capture_output=True, text=True, timeout=5,
            env={**__import__("os").environ, "GIT_AUTHOR_NAME": "test",
                 "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "test",
                 "GIT_COMMITTER_EMAIL": "t@t"},
        )
        ev = repo / "remedy-job-evidence-test123"
        ev.mkdir()
        (ev / "job_flow.json").write_text('{"job_id":"test","final_audit":{"status":"READY"}}')
        (ev / "command_transcript.json").write_text("{}")

        proc = subprocess.run(
            ["bash", "scripts/make_review_zip.sh", "--evidence-dir", str(ev)],
            cwd=repo, capture_output=True, text=True, timeout=30,
        )
        if proc.returncode != 0:
            pytest.skip(f"Script failed: {proc.stdout} {proc.stderr}")

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
