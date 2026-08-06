"""CLI tests: `remedy plan status` and `remedy plan next` (F080 T001).

The surface, not the parser: the parser's own behaviour is proven in
tests/orchestration/test_roadmap_index.py. What matters here is what an
operator actually sees, that Rule A5 decides which feature is reported,
that grammar violations arrive as `<file>:<line>: <what>` on stderr,
and — the point of the whole group — that these verbs PROPOSE: no job
is created and nothing outside the data root is written.

Every test runs the real grouped CLI in a subprocess against a fixture
repository and a tmp_path data root.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

FEATURE = """# T{tier}_F{fid} — {title}
**Tier {tier} · Depends on: {depends} · Blocks/used by: {blocks}**

## Goal & Done
Fixture feature.
"""

STATUS = """# REMEDY STATUS — Execution-Order Truth

> Grammar: see ROADMAP.md Part C.

## Tier 0 — Foundation

- [x] F001 — First feature (PR #1)
- [ ] F002 — Second feature
- [ ] F003 — Third feature
"""

ROADMAP = """# REMEDY ROADMAP

## PART G — MILESTONES

| # | Name | Features | Proof |
|---|---|---|---|
| M1 | "Solid ground" | Tier 0 | ten clean runs |
"""


def _write_fixture_repo(root: Path) -> Path:
    """A tiny grammar-valid roadmap: F001 done, F002 and F003 open."""
    features = root / "docs" / "roadmap" / "features"
    features.mkdir(parents=True)
    (features / "T0_F001.md").write_text(
        FEATURE.format(tier=0, fid="001", title="First feature", depends="none", blocks="F002"),
        encoding="utf-8")
    (features / "T0_F002.md").write_text(
        FEATURE.format(tier=0, fid="002", title="Second feature", depends="F001", blocks="F003"),
        encoding="utf-8")
    (features / "T0_F003.md").write_text(
        FEATURE.format(tier=0, fid="003", title="Third feature", depends="F002", blocks="nothing yet"),
        encoding="utf-8")
    (root / "docs" / "roadmap" / "STATUS.md").write_text(STATUS, encoding="utf-8")
    (root / "docs" / "roadmap" / "ROADMAP.md").write_text(ROADMAP, encoding="utf-8")
    return root


@pytest.fixture
def fixture_repo(tmp_path: Path) -> tuple[Path, Path]:
    """Returns (repo_root, data_root)."""
    repo = _write_fixture_repo(tmp_path / "repo")
    data_root = tmp_path / "data"
    data_root.mkdir()
    return repo, data_root


def _run(args: list[str], data_root: Path, *, expect_ok: bool = True):
    env = {**os.environ, "REMEDY_DATA_DIR": str(data_root)}
    env.pop("REMEDY_PROJECT", None)
    proc = subprocess.run(
        [sys.executable, "-m", "apps.cli.grouped", *args],
        cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=120, env=env,
    )
    if expect_ok:
        assert proc.returncode == 0, f"{args} failed ({proc.returncode}): {proc.stderr}"
    return proc


def _snapshot(root: Path) -> dict[str, tuple[int, float]]:
    return {str(p.relative_to(root)): (p.stat().st_size, p.stat().st_mtime)
            for p in sorted(root.rglob("*")) if p.is_file()}


# ---------------------------------------------------------------------------
# plan next — the proposal
# ---------------------------------------------------------------------------


class TestPlanNext:
    def test_names_first_unchecked_feature(self, fixture_repo):
        repo, data_root = fixture_repo
        out = _run(["plan", "next", "--repo", str(repo)], data_root).stdout
        assert "F002 — Second feature" in out
        assert "docs/roadmap/features/T0_F002.md" in out

    def test_says_it_started_nothing(self, fixture_repo):
        repo, data_root = fixture_repo
        out = _run(["plan", "next", "--repo", str(repo)], data_root).stdout
        assert "Proposal only — nothing was started." in out

    def test_reports_the_status_line(self, fixture_repo):
        repo, data_root = fixture_repo
        out = _run(["plan", "next", "--repo", str(repo)], data_root).stdout
        assert "docs/roadmap/STATUS.md:8" in out

    def test_json_shape(self, fixture_repo):
        repo, data_root = fixture_repo
        payload = json.loads(_run(["plan", "next", "--repo", str(repo), "--json"], data_root).stdout)
        assert payload["reason"] == "next_unchecked"
        assert payload["feature"]["id"] == "F002"
        assert payload["file"] == "docs/roadmap/features/T0_F002.md"
        assert payload["started"] is False

    def test_in_progress_line_wins_over_first_unchecked(self, fixture_repo):
        """Rule A5: a `[~]` line is the active feature and is reported as such."""
        repo, data_root = fixture_repo
        status = repo / "docs/roadmap/STATUS.md"
        status.write_text(status.read_text(encoding="utf-8").replace(
            "- [ ] F003", "- [~] F003"), encoding="utf-8")
        payload = json.loads(_run(["plan", "next", "--repo", str(repo), "--json"], data_root).stdout)
        assert payload["reason"] == "in_progress"
        assert payload["feature"]["id"] == "F003"

    def test_all_done_reports_no_open_feature(self, fixture_repo):
        repo, data_root = fixture_repo
        status = repo / "docs/roadmap/STATUS.md"
        status.write_text(status.read_text(encoding="utf-8").replace("- [ ] ", "- [x] "),
                          encoding="utf-8")
        out = _run(["plan", "next", "--repo", str(repo)], data_root).stdout
        assert "No open feature" in out


# ---------------------------------------------------------------------------
# plan status — the active feature, its blockers, its milestone
# ---------------------------------------------------------------------------


class TestPlanStatus:
    def test_shows_feature_blockers_and_milestone(self, fixture_repo):
        repo, data_root = fixture_repo
        out = _run(["plan", "status", "--repo", str(repo)], data_root).stdout
        assert "F002 — Second feature" in out
        assert "F001 — First feature" in out
        assert "[done]" in out
        assert "M1 — Solid ground" in out

    def test_reports_roadmap_size(self, fixture_repo):
        repo, data_root = fixture_repo
        out = _run(["plan", "status", "--repo", str(repo)], data_root).stdout
        assert "Roadmap: 3 features · 3 scheduled in STATUS" in out

    def test_active_feature_also_shows_what_is_next(self, fixture_repo):
        repo, data_root = fixture_repo
        status = repo / "docs/roadmap/STATUS.md"
        status.write_text(status.read_text(encoding="utf-8").replace(
            "- [ ] F002", "- [~] F002"), encoding="utf-8")
        out = _run(["plan", "status", "--repo", str(repo)], data_root).stdout
        assert "Active: F002 — Second feature" in out
        assert "Next unchecked: F003 — Third feature" in out

    def test_json_shape(self, fixture_repo):
        repo, data_root = fixture_repo
        payload = json.loads(_run(["plan", "status", "--repo", str(repo), "--json"], data_root).stdout)
        assert payload["feature"]["id"] == "F002"
        assert [b["id"] for b in payload["blockers"]] == ["F001"]
        assert payload["next_unchecked"]["id"] == "F002"
        assert payload["feature_count"] == 3
        assert payload["scheduled_count"] == 3
        assert payload["started"] is False


# ---------------------------------------------------------------------------
# Grammar violations reach the operator
# ---------------------------------------------------------------------------


class TestGrammarErrors:
    def test_broken_feature_file_exits_2_with_file_and_line(self, fixture_repo):
        repo, data_root = fixture_repo
        (repo / "docs/roadmap/features/T0_F003.md").write_text("Third feature\n", encoding="utf-8")
        proc = _run(["plan", "next", "--repo", str(repo)], data_root, expect_ok=False)
        assert proc.returncode == 2
        assert "docs/roadmap/features/T0_F003.md:1: missing title line" in proc.stderr

    def test_broken_status_line_exits_2(self, fixture_repo):
        repo, data_root = fixture_repo
        status = repo / "docs/roadmap/STATUS.md"
        status.write_text(status.read_text(encoding="utf-8").replace("- [ ] F003", "- [?] F003"),
                          encoding="utf-8")
        proc = _run(["plan", "status", "--repo", str(repo)], data_root, expect_ok=False)
        assert proc.returncode == 2
        assert "docs/roadmap/STATUS.md:9: unknown status glyph '?'" in proc.stderr


# ---------------------------------------------------------------------------
# No side effects — the whole point of "proposes, never starts"
# ---------------------------------------------------------------------------


class TestNoSideEffects:
    def test_repo_is_not_modified(self, fixture_repo):
        """One-way mirror: the roadmap markdown is left byte-identical."""
        repo, data_root = fixture_repo
        before = _snapshot(repo)
        _run(["plan", "status", "--repo", str(repo)], data_root)
        _run(["plan", "next", "--repo", str(repo)], data_root)
        assert _snapshot(repo) == before

    def test_only_the_index_is_written_under_the_data_root(self, fixture_repo):
        repo, data_root = fixture_repo
        _run(["plan", "status", "--repo", str(repo)], data_root)
        written = sorted(str(p.relative_to(data_root)) for p in data_root.rglob("*") if p.is_file())
        assert written == ["roadmap/index.json"]

    def test_no_job_is_created(self, fixture_repo):
        repo, data_root = fixture_repo
        _run(["plan", "next", "--repo", str(repo)], data_root)
        _run(["plan", "status", "--repo", str(repo)], data_root)
        assert not (data_root / "jobs").exists()
        assert not (data_root / "runs").exists()

    def test_index_is_rebuilt_on_every_read(self, fixture_repo):
        """No staleness state: an edited STATUS shows up without any refresh verb."""
        repo, data_root = fixture_repo
        _run(["plan", "next", "--repo", str(repo)], data_root)
        status = repo / "docs/roadmap/STATUS.md"
        status.write_text(status.read_text(encoding="utf-8").replace("- [ ] F002", "- [x] F002"),
                          encoding="utf-8")
        payload = json.loads(_run(["plan", "next", "--repo", str(repo), "--json"], data_root).stdout)
        assert payload["feature"]["id"] == "F003"

    def test_index_file_is_outside_the_repo(self, fixture_repo):
        repo, data_root = fixture_repo
        payload = json.loads(_run(["plan", "next", "--repo", str(repo), "--json"], data_root).stdout)
        assert payload["index_file"].startswith(str(data_root))


# ---------------------------------------------------------------------------
# Catalog registration
# ---------------------------------------------------------------------------


class TestCatalogRegistration:
    def test_group_and_commands_registered(self):
        from apps.cli.command_catalog import GROUPS, get_commands_for_group
        assert "plan" in GROUPS
        assert {c.subcommand for c in get_commands_for_group("plan")} == {"status", "next"}

    def test_commands_are_read_only(self):
        from apps.cli.command_catalog import get_commands_for_group
        for command in get_commands_for_group("plan"):
            assert command.action_class == "read_only"
            assert command.may_mutate_repo is False
            assert command.may_execute_commands is False

    def test_handlers_exist(self):
        from apps.cli.commands import collect_all_handlers
        handlers = collect_all_handlers()
        assert "plan.status" in handlers
        assert "plan.next" in handlers

    def test_group_help_lists_both_verbs(self, tmp_path):
        proc = _run(["plan", "--help"], tmp_path)
        assert "status" in proc.stdout
        assert "next" in proc.stdout
