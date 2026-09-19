"""What outlived the fixture fulfillment spine F273 deleted (R-0936).

The filtered staging copy the job runner's non-git fallback uses, the retired
fulfilled-demo page's commands, and the read-only integrity status.
"""
from __future__ import annotations

from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent.parent


# ---------------------------------------------------------------------------
# Docs tests (Step 3327, 3378, 3381, 3396-3398)
# ---------------------------------------------------------------------------


class TestFulfilledDemoGuide:

    def test_guide_exists(self):
        path = _ROOT / "docs" / "system" / "first-fulfilled-job-demo-v0.md"
        assert path.exists()

    def test_guide_mentions_status_report(self):
        path = _ROOT / "docs" / "system" / "first-fulfilled-job-demo-v0.md"
        text = path.read_text()
        assert 'job show "$JOB_ID" --full --json' in text
        assert '# 3. Check final status and read the full report\nremedy job show "$JOB_ID" --full --json' in text

    def test_guide_mentions_propose(self):
        path = _ROOT / "docs" / "system" / "first-fulfilled-job-demo-v0.md"
        text = path.read_text()
        assert (
            '# 4. List proposed next tasks (command deleted F280 round 15 — '
            'DECISION F280 D10; use `remedy decision list` instead)\n'
            'remedy decision list "$JOB_ID" --json'
        ) in text

    def test_guide_no_real_provider_claims(self):
        path = _ROOT / "docs" / "system" / "first-fulfilled-job-demo-v0.md"
        text = path.read_text()
        assert "No real provider" in text

    def test_guide_no_invalid_job_id_syntax(self):
        """R-0196: No --job-id syntax in demo guide."""
        path = _ROOT / "docs" / "system" / "first-fulfilled-job-demo-v0.md"
        text = path.read_text()
        assert "--job-id" not in text

    def test_quickstart_no_invalid_propose_syntax(self):
        """R-0196: No --job-id in propose command in quickstart."""
        path = _ROOT / "docs" / "guides" / "simple-operator-quickstart-v0.md"
        text = path.read_text()
        assert "propose list --job-id" not in text


# ---------------------------------------------------------------------------
# Unit tests: staging workspace (Steps 3524-3527)
# ---------------------------------------------------------------------------


class TestStagingWorkspace:

    def test_filtered_copy_excludes_git(self, tmp_path):
        from packages.orchestration.staging_workspace import create_staging_workspace

        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "README.md").write_text("# Hi")
        (repo / ".git").mkdir()
        (repo / ".git" / "config").write_text("[core]")
        (repo / "__pycache__").mkdir()
        (repo / "__pycache__" / "foo.pyc").write_text("bytecode")

        staging_parent = tmp_path / "staging"
        staging_parent.mkdir()
        ws = create_staging_workspace(repo, staging_parent, "job-123")

        assert (ws.staging_dir / "README.md").exists()
        assert not (ws.staging_dir / ".git").exists()
        assert not (ws.staging_dir / "__pycache__").exists()
        assert ws.files_copied == 1  # only README.md

    def test_filtered_copy_preserves_structure(self, tmp_path):
        from packages.orchestration.staging_workspace import create_staging_workspace

        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "src").mkdir()
        (repo / "src" / "main.py").write_text("x = 1")
        (repo / "docs").mkdir()
        (repo / "docs" / "guide.md").write_text("# Guide")

        staging_parent = tmp_path / "staging"
        staging_parent.mkdir()
        ws = create_staging_workspace(repo, staging_parent, "job-456")

        assert (ws.staging_dir / "src" / "main.py").exists()
        assert (ws.staging_dir / "docs" / "guide.md").exists()


class TestFilteredCopySafety:
    """Filtered copy must exclude .env variants and symlink escapes."""

    def test_env_variants_excluded(self, tmp_path):
        from packages.orchestration.staging_workspace import create_staging_workspace

        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "README.md").write_text("# Test")
        (repo / ".env").write_text("SECRET=bad")
        (repo / ".env.local").write_text("LOCAL=bad")
        (repo / ".env.production").write_text("PROD=bad")
        (repo / ".env-staging").write_text("STAGING=bad")

        staging_parent = tmp_path / "staging"
        ws = create_staging_workspace(repo, staging_parent, "test123")

        staging_files = [f.name for f in ws.staging_dir.rglob("*") if f.is_file()]
        assert ".env" not in staging_files
        assert ".env.local" not in staging_files
        assert ".env.production" not in staging_files
        assert ".env-staging" not in staging_files
        assert "README.md" in staging_files
        assert len(ws.excluded_env_files) == 4

    def test_symlink_escape_excluded(self, tmp_path):
        from packages.orchestration.staging_workspace import create_staging_workspace

        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "README.md").write_text("# Test")

        external = tmp_path / "external_secret.txt"
        external.write_text("SECRET DATA")
        (repo / "escape_link").symlink_to(external)

        staging_parent = tmp_path / "staging"
        ws = create_staging_workspace(repo, staging_parent, "test123")

        staging_files = [f.name for f in ws.staging_dir.rglob("*") if f.is_file()]
        assert "escape_link" not in staging_files
        assert "README.md" in staging_files
        assert len(ws.excluded_symlinks) >= 1


class TestDemoDocsCommands:
    """Demo docs commands must match actual CLI support."""

    def test_job_create_no_json_flag(self):
        """job create does not support --json — docs must not claim it."""
        docs = (_ROOT / "docs" / "system" / "first-fulfilled-job-demo-v0.md").read_text()
        # Should NOT have 'job create' with --json
        create_lines = [l for l in docs.splitlines() if "job create" in l and "remedy" in l]
        for line in create_lines:
            assert "--json" not in line, f"job create should not use --json: {line}"

    def test_demo_docs_command_shapes(self):
        """All remedy commands in demo docs must be valid shapes."""
        docs = (_ROOT / "docs" / "system" / "first-fulfilled-job-demo-v0.md").read_text()
        cmd_lines = [l.strip() for l in docs.splitlines()
                     if l.strip().startswith("remedy ") or l.strip().startswith("JOB_ID=$(remedy ")]
        assert len(cmd_lines) >= 4, f"Expected >=4 commands, got {len(cmd_lines)}"
        for line in cmd_lines:
            # No --json on job create
            if "job create" in line:
                assert "--json" not in line, f"job create must not use --json: {line}"


# ---------------------------------------------------------------------------
# v0.6 — Review bundle side-effect + public truth (Steps 3696-3714)
# ---------------------------------------------------------------------------


class TestIntegrityReadOnlyV07:
    """_integrity_status() and _build_integrity_summary() must be truly read-only.

    No subprocess. No run_integrity_checks(). No .agent file reads.
    """

    def test_integrity_status_no_run_integrity_checks(self, monkeypatch):
        """run_integrity_checks must not be called at all."""
        import packages.orchestration.integrity_gate as ig

        def bomb(**kwargs):
            raise AssertionError("run_integrity_checks must not be called from readiness")

        monkeypatch.setattr(ig, "run_integrity_checks", bomb)

        from packages.orchestration.mission_readiness import _integrity_status
        result = _integrity_status()
        assert result == "unknown"

    def test_integrity_status_no_subprocess(self, monkeypatch):
        """No subprocess.run from _integrity_status."""
        import subprocess as sp

        original_run = sp.run

        def bomb(*args, **kwargs):
            raise AssertionError(f"subprocess.run called: {args}")

        monkeypatch.setattr(sp, "run", bomb)

        from packages.orchestration.mission_readiness import _integrity_status
        result = _integrity_status()
        assert result == "unknown"

    def test_no_agent_dependency(self, tmp_path, monkeypatch):
        """Read-only integrity works without .agent directory."""
        monkeypatch.chdir(tmp_path)

        from packages.orchestration.integrity_gate import export_readonly_integrity_status
        result = export_readonly_integrity_status()
        assert result["status"] == "unknown"
        assert result["passed"] is None

        from packages.orchestration.mission_readiness import _integrity_status
        assert _integrity_status() == "unknown"


class TestDocsCommandShapesV06:
    """Docs must not contain invalid job create --json."""

    def test_no_job_create_json_in_quickstart(self):
        path = _ROOT / "docs" / "guides" / "simple-operator-quickstart-v0.md"
        if not path.exists():
            return
        content = path.read_text()
        assert "job create" not in content or "--json" not in content.split("job create")[1].split("\n")[0], \
            "simple-operator-quickstart must not use 'job create --json'"

    def test_no_job_create_json_in_any_doc(self):
        docs_dir = _ROOT / "docs"
        if not docs_dir.exists():
            return
        for md in docs_dir.glob("*.md"):
            content = md.read_text()
            for i, line in enumerate(content.splitlines(), 1):
                if "job create" in line and "--json" in line:
                    raise AssertionError(
                        f"{md.name}:{i} contains invalid 'job create --json'"
                    )
