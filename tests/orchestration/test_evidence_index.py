"""Tests for the evidence storage / index / review-zip selection hygiene fix.

Covers: hidden default export location, explicit --out, index updates, no repo
root pollution, index-driven selection (never by mtime), explicit --job-id,
NO_EVIDENCE honesty, history separation, and the deprecated root-style fallback.

Also covers `resolve_job_evidence_dir`, the ONE rule that decides which
directory a job's diff is read out of: the by-name index read, the `is_dir()`
check that stops a named-but-absent directory being returned, resolution of a
record written WITHOUT a `job_id` key, a malformed record falling through
rather than raising, the CWD-relative `remedy-job-evidence-<job_id>` fallback in
both directions, and that `ui_server._resolve_evidence_dir` now answers exactly
the same value.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from packages.orchestration.data_paths import (
    evidence_exports_dir,
    job_evidence_export_dir,
    job_evidence_index_dir,
    resolve_data_root,
)
from packages.orchestration.evidence_index import (
    find_record,
    load_index_records,
    record_aligns_with_worktree,
    resolve_job_evidence_dir,
    select_evidence,
    write_index_record,
)


@pytest.fixture
def isolate_data_root(tmp_path, monkeypatch):
    d = tmp_path / "remedy_data"
    d.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    return d


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=str(repo), check=True, capture_output=True, text=True)


def _repo(path: Path, dirty: list[str] | None = None) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    (path / "README.md").write_text("base\n")
    _git(path, "init", "-q")
    _git(path, "config", "user.email", "t@e.com")
    _git(path, "config", "user.name", "T")
    _git(path, "add", "-A")
    _git(path, "commit", "-q", "-m", "base")
    for rel in dirty or []:
        p = path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("x = 1\n")
    return path


def _evidence(dirpath: Path) -> Path:
    dirpath.mkdir(parents=True, exist_ok=True)
    (dirpath / "manifest.json").write_text("{}")
    return dirpath


# ---------------------------------------------------------------------------
# Hidden default location
# ---------------------------------------------------------------------------

class TestHiddenExportLocation:
    def test_default_paths_live_under_data_root(self, isolate_data_root):
        assert evidence_exports_dir() == isolate_data_root / "evidence_exports"
        assert job_evidence_export_dir("abc123") == isolate_data_root / "evidence_exports" / "abc123"
        assert job_evidence_index_dir() == isolate_data_root / "job_evidence_index"
        assert resolve_data_root() == isolate_data_root

    def test_default_export_dir_is_not_in_repo_root(self, isolate_data_root, tmp_path):
        out = job_evidence_export_dir("job1")
        assert "remedy-job-evidence-" not in str(out)
        assert str(out).startswith(str(isolate_data_root))


class TestJobEvidenceCliDefaults:
    def _plan(self, repo: Path):
        from packages.orchestration.pingpong_job import parse_job_file
        return parse_job_file("# Job: t\n\n## Task 1\nDo a thing.\n", str(repo))

    def test_default_out_goes_to_hidden_dir_and_indexes(self, isolate_data_root, tmp_path, capsys):
        repo = _repo(tmp_path / "repo", dirty=["pkg/mod.py"])
        job = self._plan(repo)
        from apps.cli.commands.do_cmd import _cmd_do_job_evidence

        _cmd_do_job_evidence(job.job_id, json_output=True)
        capsys.readouterr()

        expected = job_evidence_export_dir(job.job_id)
        assert expected.is_dir(), "evidence must default to the hidden data-dir location"
        # No repo-root pollution FROM THIS EXPORT. The bare glob also caught
        # legacy dirs an operator left in the checkout years ago, which says
        # nothing about the command under test.
        assert not [d for d in Path.cwd().glob("remedy-job-evidence-*")
                    if job.job_id in d.name]

        rec = find_record(job.job_id)
        assert rec is not None
        assert rec["job_id"] == job.job_id
        assert rec["evidence_export_path"] == str(expected.resolve())
        assert rec["repo_path"] == str(repo.resolve())
        assert rec["branch"]
        assert rec["commit"]
        assert rec["exported_at"]
        assert "job_status" in rec
        # Legacy keys preserved (ui_server reads these).
        assert rec["evidence_dir_local"] == str(expected.resolve())
        assert "created_at" in rec

    def test_explicit_out_still_supported(self, isolate_data_root, tmp_path, capsys):
        repo = _repo(tmp_path / "repo2", dirty=["pkg/mod.py"])
        job = self._plan(repo)
        from apps.cli.commands.do_cmd import _cmd_do_job_evidence

        custom = tmp_path / "custom_out"
        _cmd_do_job_evidence(job.job_id, out=str(custom), json_output=True)
        capsys.readouterr()
        assert custom.is_dir()
        rec = find_record(job.job_id)
        assert rec["evidence_export_path"] == str(custom.resolve())


# ---------------------------------------------------------------------------
# Index + selection
# ---------------------------------------------------------------------------

class TestIndexRecords:
    def test_write_and_load_records_newest_first(self, isolate_data_root, tmp_path):
        repo = _repo(tmp_path / "r")
        write_index_record("old", _evidence(tmp_path / "e_old"), repo_path=repo)
        write_index_record("new", _evidence(tmp_path / "e_new"), repo_path=repo)
        recs = load_index_records()
        assert {r["job_id"] for r in recs} == {"old", "new"}
        assert recs[0]["exported_at"] >= recs[1]["exported_at"]

    def test_alignment_requires_recorded_files_within_worktree(self):
        rec = {"changed_files": ["a.py", "b.py"]}
        assert record_aligns_with_worktree(rec, ["a.py", "b.py", "c.py"]) is True
        assert record_aligns_with_worktree(rec, ["a.py"]) is False
        assert record_aligns_with_worktree({"changed_files": []}, ["a.py"]) is False


class TestSelection:
    def test_no_matching_evidence_reports_none(self, isolate_data_root, tmp_path):
        repo = _repo(tmp_path / "repo")
        result = select_evidence(repo)
        assert result["selected"] is None
        assert "no_matching_evidence" in result["reason"]

    def test_prefers_aligned_repo_evidence_over_newer_unrelated_scratch_job(
        self, isolate_data_root, tmp_path,
    ):
        """The newest job is a scratch/runtime job in a DIFFERENT repository.
        It must never be selected for this working tree."""
        repo = _repo(tmp_path / "main_repo", dirty=["pkg/f004.py", "tests/test_f004.py"])
        scratch = _repo(tmp_path / "scratch_repo", dirty=["hello.py"])

        write_index_record(
            "f004job", _evidence(tmp_path / "ev_f004"), repo_path=repo,
            changed_files=["pkg/f004.py", "tests/test_f004.py"],
        )
        # Written later => newer exported_at, but belongs to another repo.
        write_index_record(
            "scratchjob", _evidence(tmp_path / "ev_scratch"), repo_path=scratch,
            changed_files=["hello.py"],
        )

        result = select_evidence(repo)
        assert result["selected"]["job_id"] == "f004job"
        assert result["reason"].startswith("newest_aligned_evidence")

    def test_unaligned_same_repo_evidence_is_not_selected(self, isolate_data_root, tmp_path):
        repo = _repo(tmp_path / "repo", dirty=["pkg/a.py"])
        # Recorded file set is not part of the current dirty set.
        write_index_record(
            "stale", _evidence(tmp_path / "ev_stale"), repo_path=repo,
            changed_files=["pkg/gone.py"],
        )
        assert select_evidence(repo)["selected"] is None

    def test_explicit_job_id_selects_exactly_that_job(self, isolate_data_root, tmp_path):
        repo = _repo(tmp_path / "repo", dirty=["pkg/a.py"])
        write_index_record("wanted", _evidence(tmp_path / "ev_w"), repo_path=repo,
                           changed_files=["pkg/a.py"])
        write_index_record("other", _evidence(tmp_path / "ev_o"), repo_path=repo,
                           changed_files=["pkg/a.py"])
        result = select_evidence(repo, job_id="wanted")
        assert result["selected"]["job_id"] == "wanted"
        assert result["reason"] == "explicit_job_id"

    def test_explicit_job_id_never_substitutes_another_job(self, isolate_data_root, tmp_path):
        repo = _repo(tmp_path / "repo", dirty=["pkg/a.py"])
        write_index_record("present", _evidence(tmp_path / "ev_p"), repo_path=repo,
                           changed_files=["pkg/a.py"])
        result = select_evidence(repo, job_id="missing")
        assert result["selected"] is None
        assert result["reason"].startswith("job_id_not_indexed")

    def test_history_excludes_current_and_is_separate(self, isolate_data_root, tmp_path):
        repo = _repo(tmp_path / "repo", dirty=["pkg/a.py"])
        for jid in ("j1", "j2", "j3"):
            write_index_record(jid, _evidence(tmp_path / f"ev_{jid}"), repo_path=repo,
                               changed_files=["pkg/a.py"])
        result = select_evidence(repo, job_id="j2")
        assert result["selected"]["job_id"] == "j2"
        hist_ids = [r["job_id"] for r in result["history"]]
        assert "j2" not in hist_ids
        assert set(hist_ids) == {"j1", "j3"}


class TestSelectorScript:
    def _run(self, repo: Path, *args: str) -> dict[str, str]:
        root = Path(__file__).resolve().parents[2]
        r = subprocess.run(
            ["python3", str(root / "scripts" / "select_review_evidence.py"),
             "--repo", str(repo), *args],
            capture_output=True, text=True, check=True,
        )
        out: dict[str, str] = {}
        for line in r.stdout.splitlines():
            if "=" in line:
                k, v = line.split("=", 1)
                out[k] = v
        return out

    def test_script_reports_none_without_evidence(self, isolate_data_root, tmp_path):
        repo = _repo(tmp_path / "repo")
        out = self._run(repo)
        assert out["STATUS"] == "none"
        assert out["HISTORY"] == ""

    def test_script_include_recent_limits_history(self, isolate_data_root, tmp_path):
        repo = _repo(tmp_path / "repo", dirty=["pkg/a.py"])
        for jid in ("h1", "h2", "h3", "cur"):
            write_index_record(jid, _evidence(tmp_path / f"ev_{jid}"), repo_path=repo,
                               changed_files=["pkg/a.py"])
        out = self._run(repo, "--job-id", "cur", "--include-recent", "2")
        assert out["STATUS"] == "selected"
        assert out["JOB_ID"] == "cur"
        entries = [e for e in out["HISTORY"].split(",") if e]
        assert len(entries) == 2
        assert all(not e.startswith("cur:") for e in entries)


class TestLegacyRootFallback:
    def test_root_style_evidence_is_ignored_with_a_warning(self):
        """The shell warns about root-directory evidence and never selects it.

        The fallback itself is gone: 01e2018 replaced mtime-based root
        selection with a hard error ("cannot distinguish features"), bd93397
        downgraded that to warn-and-ignore so code snapshots still build.
        """
        script = (Path(__file__).resolve().parents[2] / "scripts" / "make_review_zip.sh").read_text()
        assert "deprecated remedy-job-evidence-* dir(s) in repo root — IGNORED." in script
        assert "Auto-selection from root dirs is disabled" in script
        assert "To use one: --evidence-dir <path>." in script
        # And the honest NO_EVIDENCE message is present.
        assert "No matching review evidence exists for the current branch/worktree." in script
        assert "This is a code snapshot, not a final review package." in script

    def test_zip_supports_job_id_and_include_recent(self):
        script = (Path(__file__).resolve().parents[2] / "scripts" / "make_review_zip.sh").read_text()
        assert "--job-id)" in script
        assert "--include-recent)" in script
        assert "evidence/history/$h_job" in script
        assert "refusing to substitute another job" in script


class TestDirtyFileEnumeration:
    def test_manifest_lists_untracked_files_individually(self):
        """`git status --porcelain` collapses untracked directories to `dir/`,
        which can never match a covered file. The manifest must pass `-u`."""
        import sys
        root = Path(__file__).resolve().parents[2]
        sys.path.insert(0, str(root / "scripts"))
        import inspect

        import build_review_manifest as brm
        # Round 32 F5: the single git-status acquisition lives in _git_status_snapshot
        # (NUL-safe porcelain=v1 -z); -u still enumerates untracked files individually there.
        src = inspect.getsource(brm._git_status_snapshot)
        assert '"-u"' in src, "_git_status_snapshot must enumerate untracked files individually"

    def test_untracked_dir_is_expanded(self, tmp_path, monkeypatch):
        repo = _repo(tmp_path / "r")
        (repo / "pkg").mkdir()
        (repo / "pkg" / "a.py").write_text("x = 1\n")
        (repo / "pkg" / "b.py").write_text("y = 2\n")
        out = subprocess.run(
            ["git", "status", "--porcelain", "-u"], cwd=repo,
            capture_output=True, text=True, check=True,
        ).stdout
        assert "pkg/a.py" in out and "pkg/b.py" in out
        assert "pkg/\n" not in out


# ---------------------------------------------------------------------------
# Finding 8 — the dirty set is not a hardcoded language-extension allowlist
# ---------------------------------------------------------------------------

_MIXED = [
    "packages/orchestration/stream_evidence.py",
    "tests/orchestration/fixtures/stream/basic_session.jsonl",
    "docs/roadmap/STATUS.md",
]


class TestDirtySubjectFiles:
    def test_mixed_extension_files_are_all_subject_files(self):
        from packages.orchestration.evidence_index import is_review_subject_file
        for rel in _MIXED:
            assert is_review_subject_file(rel) is True

    def test_operational_noise_is_excluded(self):
        from packages.orchestration.evidence_index import is_review_subject_file
        for rel in (
            ".data/evidence_exports/x/manifest.json",
            "remedy-review-20260101-000000-READY_FOR_REVIEW.zip",
            "remedy-job-evidence-abc/manifest.json",
            "packages/__pycache__/x.pyc",
            "build/out.tar.gz",
            "tests/orchestration/fixtures/",   # collapsed dir entry
        ):
            assert is_review_subject_file(rel) is False, rel

    def test_dirty_enumeration_includes_jsonl_and_md(self, tmp_path):
        from packages.orchestration.evidence_index import dirty_source_test_files
        repo = _repo(tmp_path / "r", dirty=_MIXED)
        dirty = dirty_source_test_files(repo)
        for rel in _MIXED:
            assert rel in dirty, f"{rel} missing from dirty subject files"


class TestNoArgSelectionWithMixedFiles:
    def test_selects_matching_f004_job_for_mixed_file_set(self, isolate_data_root, tmp_path):
        repo = _repo(tmp_path / "f004_repo", dirty=_MIXED)
        scratch = _repo(tmp_path / "scratch", dirty=["hello.py"])

        write_index_record("f004job", _evidence(tmp_path / "ev_f004"), repo_path=repo,
                           changed_files=list(_MIXED))
        # Newer, but a different repository (tiny runtime smoke).
        write_index_record("smokejob", _evidence(tmp_path / "ev_smoke"), repo_path=scratch,
                           changed_files=["hello.py"])
        # Same repo, but its file set no longer aligns with the working tree.
        write_index_record("stalejob", _evidence(tmp_path / "ev_stale"), repo_path=repo,
                           changed_files=["packages/orchestration/gone.py"])

        result = select_evidence(repo)
        assert result["selected"]["job_id"] == "f004job"

    def test_history_requires_file_set_overlap(self, isolate_data_root, tmp_path):
        repo = _repo(tmp_path / "repo", dirty=_MIXED)
        write_index_record("related", _evidence(tmp_path / "ev_rel"), repo_path=repo,
                           changed_files=[_MIXED[0]])
        write_index_record("unrelated", _evidence(tmp_path / "ev_unrel"), repo_path=repo,
                           changed_files=["packages/orchestration/other_feature.py"])
        write_index_record("current", _evidence(tmp_path / "ev_cur"), repo_path=repo,
                           changed_files=list(_MIXED))

        result = select_evidence(repo, job_id="current")
        hist = [r["job_id"] for r in result["history"]]
        assert "related" in hist
        assert "unrelated" not in hist, "an unrelated feature was included merely by recency"


class TestPorcelainParsing:
    """The status columns must never be confused with the path.

    ``git status --porcelain`` puts the status in columns 0-1, so an unstaged
    modification starts with a space. Stripping the command output shifts the
    first line left and silently truncates its path (``.agent/x`` -> ``agent/x``),
    which then fails to match anything in the working tree.
    """

    def test_leading_dot_survives_on_the_first_modified_entry(self, tmp_path):
        from packages.orchestration.evidence_index import dirty_source_test_files

        repo = tmp_path / "dotrepo"
        (repo / ".agent").mkdir(parents=True)
        (repo / "src").mkdir()
        _git(repo, "init", "-q")
        _git(repo, "config", "user.email", "t@e.com")
        _git(repo, "config", "user.name", "T")
        (repo / ".agent" / "decisions.md").write_text("v1\n")
        (repo / "src" / "a.py").write_text("x = 1\n")
        _git(repo, "add", "-A")
        _git(repo, "commit", "-q", "-m", "init")

        # Unstaged modification -> porcelain line is " M .agent/decisions.md"
        (repo / ".agent" / "decisions.md").write_text("v2\n")

        dirty = dirty_source_test_files(repo)
        assert ".agent/decisions.md" in dirty
        assert "agent/decisions.md" not in dirty
        for rel in dirty:
            assert (repo / rel).exists(), f"enumerated a path that does not exist: {rel}"

    def test_every_enumerated_path_exists_in_this_repo(self):
        import pathlib

        from packages.orchestration.evidence_index import dirty_source_test_files

        root = pathlib.Path(__file__).resolve().parents[2]
        for rel in dirty_source_test_files(root):
            assert (root / rel).exists(), f"enumerated a nonexistent path: {rel}"


# ---------------------------------------------------------------------------
# resolve_job_evidence_dir — the ONE evidence-directory rule (F033 R13)
# ---------------------------------------------------------------------------

def _index_file(index_dir: Path, job_id: str, body: str) -> Path:
    index_dir.mkdir(parents=True, exist_ok=True)
    f = index_dir / f"{job_id}.json"
    f.write_text(body, encoding="utf-8")
    return f


class TestResolveJobEvidenceDir:
    """Every test here passes ``index_dir`` explicitly and chdirs into
    ``tmp_path``, so the CWD-relative fallback can never resolve against this
    repository's own working tree."""

    def test_record_naming_an_existing_directory_resolves_to_it(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        idx = tmp_path / "index"
        ev = _evidence(tmp_path / "ev_here")
        _index_file(idx, "j1", json.dumps({"job_id": "j1", "evidence_dir_local": str(ev)}))
        assert resolve_job_evidence_dir("j1", index_dir=idx) == Path(str(ev))

    def test_record_naming_an_absent_directory_answers_none(self, tmp_path, monkeypatch):
        """The discriminator for the ``is_dir()`` check: a NAMED but absent
        directory must fall through, never be handed back."""
        monkeypatch.chdir(tmp_path)
        idx = tmp_path / "index"
        gone = tmp_path / "never_created"
        _index_file(idx, "j2", json.dumps({"job_id": "j2", "evidence_dir_local": str(gone)}))
        assert resolve_job_evidence_dir("j2", index_dir=idx) is None

    def test_record_without_a_job_id_key_still_resolves(self, tmp_path, monkeypatch):
        """THE DISCRIMINATOR FOR THE WHOLE MOVE: this passes under the by-name
        read of ``<job_id>.json`` and fails under any re-expression through
        ``find_record``, which matches the ``job_id`` key INSIDE the file."""
        monkeypatch.chdir(tmp_path)
        idx = tmp_path / "index"
        ev = _evidence(tmp_path / "ev_nokey")
        _index_file(idx, "j3", json.dumps({"evidence_dir_local": str(ev)}))
        assert resolve_job_evidence_dir("j3", index_dir=idx) == Path(str(ev))

    def test_malformed_record_falls_through_instead_of_raising(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        idx = tmp_path / "index"
        _index_file(idx, "j4", "this is not json {{{")
        assert resolve_job_evidence_dir("j4", index_dir=idx) is None

    def test_relative_fallback_resolves_against_the_cwd(self, tmp_path, monkeypatch):
        """No index record at all: the fallback is RELATIVE and resolves against
        the current working directory."""
        monkeypatch.chdir(tmp_path)
        idx = tmp_path / "index"
        _evidence(tmp_path / "remedy-job-evidence-j5")
        assert resolve_job_evidence_dir("j5", index_dir=idx) == Path("remedy-job-evidence-j5")

    def test_no_record_and_no_fallback_directory_answers_none(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        idx = tmp_path / "index"
        assert resolve_job_evidence_dir("j6", index_dir=idx) is None


class TestUiServerDelegatesToTheSameRule:
    def test_ui_server_resolver_answers_the_same_directory(
        self, isolate_data_root, tmp_path, monkeypatch,
    ):
        """The F037 viewer's resolver and the shared rule must agree over a case
        that is NOT None — one answer, not two."""
        from packages.orchestration.ui_server import _resolve_evidence_dir

        monkeypatch.chdir(tmp_path)
        ev = _evidence(tmp_path / "ev_shared")
        _index_file(job_evidence_index_dir(), "jdel",
                    json.dumps({"job_id": "jdel", "evidence_dir_local": str(ev)}))

        shared = resolve_job_evidence_dir("jdel")
        via_ui = _resolve_evidence_dir("jdel")
        assert shared is not None
        assert via_ui == shared == Path(str(ev))
