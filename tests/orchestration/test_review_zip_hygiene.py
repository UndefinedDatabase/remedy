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
    "rotate_live_review.py",               # T016 (b): the ledger reader the manifest loads by path
    "build_review_zip.py",                 # F8 (round 17): the NUL-safe archive builder
    "build_observability_index.py",
    "select_review_evidence.py",
    "stage_review_evidence.py",            # F8 (round 19): typed no-follow evidence staging
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
    # F8 (round 19): the typed no-follow evidence inventory the staging CLI drives.
    "packages/orchestration/evidence_inventory.py",
    "packages/common/__init__.py",
    "packages/common/secure_fs.py", "packages/common/strict_json.py", "packages/common/acquisition_budget.py",
)


def _make_git_repo_with_scripts(tmp_path: Path) -> Path:
    """Isolated git repo containing every current packaging dependency."""
    repo = tmp_path / "repo"
    (repo / "scripts").mkdir(parents=True)
    for name in _REQUIRED_SCRIPTS:
        src = REPO_ROOT / "scripts" / name
        assert src.exists(), f"missing packaging dependency in source tree: {src}"
        shutil.copy2(src, repo / "scripts" / name)
    # Round 32 F-fix: copy the COMPLETE packages tree (not a curated subset that breaks whenever a
    # script gains a new import), so every runtime import resolves and the package files an
    # evidence-index test references as source paths are present.
    shutil.copytree(REPO_ROOT / "packages", repo / "packages",
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))

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
    """Root-dir auto-selection is RETIRED — see commits 01e2018 (mtime-based
    root selection replaced by a hard error, "it cannot distinguish features")
    and bd93397 (downgraded to warn-and-ignore so code snapshots still build).
    These tests hold that retirement: `remedy-job-evidence-*` dirs in the repo
    root are ignored with a warning, and only `--evidence-dir` / `--job-id`
    select evidence. The explicit-selection tests below are unchanged.
    """

    def test_single_root_evidence_dir_is_refused(self, tmp_path: Path):
        """DECISION amend0923-selfuse-write D5, 2026-09-23 — REWRITTEN.

        This test formerly asserted the LENIENT behaviour: a root
        `remedy-job-evidence-*` directory was warned about as "IGNORED" and the
        packer went on to build a code snapshot. The operator ruled on
        2026-09-23 that such leftovers must never be packaged NOR tolerated, so
        the same input is now a refusal. The retirement this class holds is
        unchanged and in fact strengthened: root-dir auto-selection is still
        dead, and the directory is now refused rather than silently skipped.
        """
        repo = _make_git_repo_with_scripts(tmp_path)
        ev = repo / "remedy-job-evidence-aaa111"
        _make_valid_evidence(ev, "aaa")

        proc = subprocess.run(
            ["bash", "scripts/make_review_zip.sh"],
            cwd=repo, capture_output=True, text=True, timeout=30,
        )
        out = proc.stdout + proc.stderr
        assert proc.returncode == 1, f"expected a refusal: {out}"
        assert "remedy-job-evidence-aaa111" in out
        assert "Auto-selected" not in proc.stdout
        assert not list(repo.glob("*.zip")), "no archive may be written"

    def test_invalid_root_dirs_are_refused_rather_than_snapshotted(self, tmp_path: Path):
        """DECISION amend0923-selfuse-write D5, 2026-09-23 — REWRITTEN.

        Formerly: "Unusable root dirs never block the snapshot — they are just
        ignored." Now they block it, by name, before anything is read.
        """
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
        out = proc.stdout + proc.stderr
        assert proc.returncode == 1, f"expected a refusal: {out}"
        assert "remedy-job-evidence-bad1" in out
        assert "remedy-job-evidence-bad2" in out
        assert not list(repo.glob("*.zip")), "no archive may be written"

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
        """DECISION amend0923-selfuse-write D5, 2026-09-23 — AMENDED.

        The subject is unchanged: an explicitly selected older bundle beats a
        newer one, because mtime selects nothing. What moved is the newer
        SIBLING, which used to sit beside it in the repository root and is now
        refused there; it lives outside the checkout instead, which is where a
        second bundle can still legitimately be. The root-sibling form of this
        scenario is the deprecated auto-selection D5 kills, and the modern form
        is covered by TestIndexedEvidenceSelection below.
        """
        import os
        repo = _make_git_repo_with_scripts(tmp_path)

        old = repo / "remedy-job-evidence-old111"
        _make_valid_evidence(old, "old")
        os.utime(old / "job_flow.json", (1000000, 1000000))

        new = tmp_path / "elsewhere" / "remedy-job-evidence-new222"
        new.parent.mkdir()
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

    def test_stale_dirs_are_refused_not_merely_left_out(self, tmp_path: Path):
        """DECISION amend0923-selfuse-write D5, 2026-09-23 — REWRITTEN.

        Formerly this asserted that neither root dir rides along and the build
        goes on. Stronger now: unselected root evidence is refused outright, so
        it cannot appear in a package by any route. The property that mtime
        buys nothing survives on the path that still exists — the `.data/`
        evidence index — in TestIndexedEvidenceSelection below.
        """
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
        out = proc.stdout + proc.stderr
        assert proc.returncode == 1, f"expected a refusal: {out}"
        assert "remedy-job-evidence-stale1" in out
        assert "remedy-job-evidence-current1" in out
        assert not list(repo.glob("*.zip"))

    def test_root_dirs_never_reach_a_manifest_because_they_are_refused(
        self, tmp_path: Path
    ):
        """DECISION amend0923-selfuse-write D5, 2026-09-23 — REWRITTEN.

        Formerly: root dirs are ignored and the manifest must not then claim
        evidence the package does not carry. A manifest that could make that
        false claim is no longer reachable from this input, because the build
        stops first. The "manifest never claims absent evidence" property is
        still pinned, on a reachable input, by
        test_a_clean_repo_with_no_evidence_states_no_current_evidence below.
        """
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
        out = proc.stdout + proc.stderr
        assert proc.returncode == 1, f"expected a refusal: {out}"
        assert "remedy-job-evidence-aaa111" in out
        assert not list(repo.glob("*.zip"))

    def test_a_clean_repo_with_no_evidence_states_no_current_evidence(
        self, tmp_path: Path
    ):
        """The manifest must not claim evidence the package does not carry.

        This is the surviving, reachable form of the assertion the test above
        used to make from an input that is now refused.
        """
        repo = _make_git_repo_with_scripts(tmp_path)

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
        assert manifest["current_evidence"] is None
        assert "EVIDENCE_AUTHORITATIVE=false" in proc.stdout
        assert "NO_EVIDENCE" in zips[0].name

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

    def test_refused_root_dirs_are_reported_with_the_places_they_belong(
        self, tmp_path: Path
    ):
        """DECISION amend0923-selfuse-write D5, 2026-09-23 — REWRITTEN.

        Formerly: ignoring is never silent, so the count and both remedies are
        printed. Refusing is never silent either — the refusal names every
        offending directory and says where such files belong, which is strictly
        more than the old warning told the reader.
        """
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
        out = proc.stdout + proc.stderr
        assert proc.returncode == 1, f"expected a refusal: {out}"
        assert "remedy-job-evidence-good1" in out
        assert "remedy-job-evidence-bad1" in out
        assert ".remedy-wt/" in out and ".data/" in out

    def test_missing_command_transcript_creates_zip_with_warning(self, tmp_path: Path):
        """Missing command_transcript.json → zip created, validation records it.

        Selected explicitly: root dirs are no longer picked up on their own.
        """
        repo = _make_git_repo_with_scripts(tmp_path)
        ev = repo / "remedy-job-evidence-noct"
        _make_valid_evidence(ev, "noct")
        (ev / "command_transcript.json").unlink()

        proc = subprocess.run(
            ["bash", "scripts/make_review_zip.sh", "--evidence-dir", str(ev)],
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
        """With an explicit selection, an unselected sibling stays out.

        DECISION amend0923-selfuse-write D5, 2026-09-23 — AMENDED: the sibling
        moved out of the repository root, where it is now refused outright, to
        a directory beside the checkout. The subject is unchanged and in fact
        doubly held: an unselected bundle cannot reach the archive by being
        ignored, and one at the root cannot reach it at all.
        """
        import os
        repo = _make_git_repo_with_scripts(tmp_path)

        sel = repo / "remedy-job-evidence-selected"
        _make_valid_evidence(sel, "selected")
        os.utime(sel / "job_flow.json", (2000000, 2000000))

        other = tmp_path / "elsewhere" / "remedy-job-evidence-other"
        other.parent.mkdir()
        _make_valid_evidence(other, "other")
        os.utime(other / "job_flow.json", (1000000, 1000000))

        proc = subprocess.run(
            ["bash", "scripts/make_review_zip.sh", "--evidence-dir", str(sel)],
            cwd=repo, capture_output=True, text=True, timeout=30,
        )
        assert proc.returncode == 0, f"{proc.stdout}\n{proc.stderr}"

        from zipfile import ZipFile
        zips = list(repo.glob("*.zip"))
        with ZipFile(zips[0]) as zf:
            names = zf.namelist()
            assert all("other" not in n for n in names)
            assert "evidence/current/job_flow.json" in names

    def test_evidence_under_current_prefix(self, tmp_path: Path):
        """DECISION amend0923-selfuse-write D5, 2026-09-23 — AMENDED, and the
        assertion is stronger for it. The bundle is now SELECTED explicitly
        instead of left at the root unselected, so the archive really carries
        evidence and the prefix rule is measured over a non-empty set; the old
        form passed vacuously over zero evidence members.
        """
        repo = _make_git_repo_with_scripts(tmp_path)
        ev = repo / "remedy-job-evidence-preftest"
        _make_valid_evidence(ev, "preftest")

        proc = subprocess.run(
            ["bash", "scripts/make_review_zip.sh", "--evidence-dir", str(ev)],
            cwd=repo, capture_output=True, text=True, timeout=30,
        )
        assert proc.returncode == 0, f"{proc.stdout}\n{proc.stderr}"

        from zipfile import ZipFile
        zips = list(repo.glob("*.zip"))
        with ZipFile(zips[0]) as zf:
            ev_files = [n for n in zf.namelist()
                        if n.startswith("evidence/")]
            assert ev_files, "the archive must actually carry evidence"
            assert all(n.startswith("evidence/current/") for n in ev_files)

    def test_root_dirs_are_not_candidates_and_are_now_refused_outright(
        self, tmp_path: Path
    ):
        """DECISION amend0923-selfuse-write D5, 2026-09-23 — REWRITTEN.

        Root dirs stopped being selection CANDIDATES at 01e2018; they are now
        not tolerated either. Every one of the three is named in the refusal,
        valid and invalid alike, because the gate reads shapes and not contents.
        """
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
        out = proc.stdout + proc.stderr
        assert proc.returncode == 1, f"expected a refusal: {out}"
        for name in ("remedy-job-evidence-good", "remedy-job-evidence-bad1",
                     "remedy-job-evidence-bad2"):
            assert name in out
        assert not list(repo.glob("*.zip"))


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

    def test_legacy_root_evidence_is_refused(self, tmp_path: Path):
        """DECISION amend0923-selfuse-write D5, 2026-09-23 — REWRITTEN.

        The deprecated root fallback was removed at 01e2018 / bd93397 and the
        leftover directory was then merely warned about. It is now refused: it
        was never selected, and it must not sit in the root either.
        """
        repo = _make_git_repo_with_scripts(tmp_path)
        _make_valid_evidence(repo / "remedy-job-evidence-legacy1", "legacy1")

        proc = _run_zip(repo)
        combined = proc.stdout + proc.stderr
        assert proc.returncode == 1, combined
        assert "remedy-job-evidence-legacy1" in combined
        assert not list(repo.glob("*.zip"))

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


# ---------------------------------------------------------------------------
# amendment amend0923-selfuse-write — R-0829 and DECISION D5:
# the packer ships nothing git ignores, and refuses root leftovers outright
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    shutil.which("git") is None
    or shutil.which("bash") is None
    or shutil.which("zip") is None,
    reason="git, bash, zip required",
)
class TestThePackerShipsNothingGitIgnores:
    """R-0829's own FIX clause, which this amendment carries.

    The packer's exclusion list was a hardcoded set of `-prune` paths, so every
    ignored directory the list did not happen to name was packaged. Measured on
    three packages of 2026-09-22 and 2026-09-23: 65 files of F110-era reviewer
    scratch under `remedy-review-r9-scratch/` and `remedy-review-r10-scratch/`
    in each. The list is now backed by `git check-ignore`, which cannot go
    stale the way a list does.
    """

    def _repo_with_an_ignored_directory(self, tmp_path: Path) -> Path:
        repo = _make_git_repo_with_scripts(tmp_path)
        _make_valid_evidence(repo / "remedy-job-evidence-test", "ignored-test")
        (repo / ".gitignore").write_text("secret_scratch/\n")
        scratch = repo / "secret_scratch"
        scratch.mkdir()
        (scratch / "a_note.txt").write_text("scratch nobody should receive\n")
        env = {**os.environ, "GIT_AUTHOR_NAME": "test", "GIT_AUTHOR_EMAIL": "t@t",
               "GIT_COMMITTER_NAME": "test", "GIT_COMMITTER_EMAIL": "t@t"}
        subprocess.run(["git", "add", ".gitignore"], cwd=repo, check=True,
                       capture_output=True, text=True)
        subprocess.run(["git", "commit", "-m", "ignore scratch"], cwd=repo,
                       capture_output=True, text=True, timeout=15, env=env)
        return repo

    def test_no_member_of_the_archive_is_a_path_git_ignores(self, tmp_path: Path):
        repo = self._repo_with_an_ignored_directory(tmp_path)

        proc = subprocess.run(
            ["bash", "scripts/make_review_zip.sh",
             "--evidence-dir", str(repo / "remedy-job-evidence-test")],
            cwd=repo, capture_output=True, text=True, timeout=120,
        )
        assert proc.returncode == 0, f"{proc.stdout}\n{proc.stderr}"

        from zipfile import ZipFile
        zips = list(repo.glob("*.zip"))
        assert zips, "the packer must still build an archive"
        with ZipFile(zips[0]) as zf:
            names = zf.namelist()
        leaked = [n for n in names if n.startswith("secret_scratch/")]
        assert leaked == [], f"the packer shipped git-ignored paths: {leaked}"
        assert any(n.endswith("README.md") for n in names), (
            "the tracked sources must still be packaged — this filter must not "
            "empty the archive"
        )


@pytest.mark.skipif(
    shutil.which("git") is None or shutil.which("bash") is None,
    reason="git and bash required",
)
class TestThePackerRefusesRootLeftovers:
    """DECISION amend0923-selfuse-write D5, 2026-09-23.

    The operator ruled that reviewer scratch, deprecated evidence directories
    and stray archives must never be packaged NOR tolerated at the repository
    root. The detritus gate, which already refused `*_WAS_HERE.txt`, now
    refuses those three shapes as well, with the same print-and-exit-1
    behaviour and before anything is read.
    """

    def _repo(self, tmp_path: Path) -> Path:
        repo = _make_git_repo_with_scripts(tmp_path)
        _make_valid_evidence(repo / "remedy-job-evidence-test", "refusal-test")
        return repo

    def _run(self, repo: Path, review_dir: Path) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["bash", "scripts/make_review_zip.sh",
             "--evidence-dir", str(repo / "remedy-job-evidence-test")],
            cwd=repo, capture_output=True, text=True, timeout=60,
            env={**os.environ, "REMEDY_REVIEW_DIR": str(review_dir)},
        )

    def test_a_scratch_dir_and_a_stray_zip_are_both_refused_by_name(
        self, tmp_path: Path
    ):
        repo = self._repo(tmp_path)
        (repo / "remedy-review-x-scratch").mkdir()
        (repo / "foo.zip").write_bytes(b"not a package\n")
        review_dir = tmp_path / "packages_out"

        proc = self._run(repo, review_dir)

        out = proc.stdout + proc.stderr
        assert proc.returncode == 1, f"expected a refusal, got {proc.returncode}\n{out}"
        assert "remedy-review-x-scratch" in out
        assert "foo.zip" in out
        assert not list(review_dir.glob("*.zip")), "nothing may be written"

    def test_a_root_evidence_dir_is_refused_rather_than_ignored(self, tmp_path: Path):
        """The old behaviour warned "IGNORED" and packaged a code snapshot."""
        repo = self._repo(tmp_path)
        (repo / "remedy-job-evidence-aaa111").mkdir()
        review_dir = tmp_path / "packages_out"

        proc = self._run(repo, review_dir)

        out = proc.stdout + proc.stderr
        assert proc.returncode == 1, f"expected a refusal, got {proc.returncode}\n{out}"
        assert "remedy-job-evidence-aaa111" in out
        assert not list(review_dir.glob("*.zip"))

    def test_the_packages_own_output_directory_is_not_its_own_detritus(
        self, tmp_path: Path
    ):
        """REMEDY_REVIEW_DIR="." is what tests/conftest.py sets, so a build
        that writes its archive INTO the repository root must not then refuse
        the archive it just wrote. Only the configured output directory is
        spared, and only for the `*.zip` shape."""
        repo = self._repo(tmp_path)

        first = subprocess.run(
            ["bash", "scripts/make_review_zip.sh",
             "--evidence-dir", str(repo / "remedy-job-evidence-test")],
            cwd=repo, capture_output=True, text=True, timeout=60,
            env={**os.environ, "REMEDY_REVIEW_DIR": "."},
        )
        assert first.returncode == 0, f"{first.stdout}\n{first.stderr}"
        assert list(repo.glob("*.zip")), "the archive must land in the root"

        second = subprocess.run(
            ["bash", "scripts/make_review_zip.sh",
             "--evidence-dir", str(repo / "remedy-job-evidence-test")],
            cwd=repo, capture_output=True, text=True, timeout=60,
            env={**os.environ, "REMEDY_REVIEW_DIR": "."},
        )
        assert second.returncode == 0, (
            "the packer's own output must not be read as detritus\n"
            f"{second.stdout}\n{second.stderr}"
        )
