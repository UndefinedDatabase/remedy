"""F5 (round 32) — git status is one typed immutable snapshot. Only OK may mean a clean tree; a
nonzero exit, timeout, missing git executable or malformed output is a distinguished status that blocks
READY, never a fall-open empty list. Dirty and untracked derive from the SAME snapshot."""
from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
_b = importlib.util.spec_from_file_location(
    "_brm_gitsnap", REPO_ROOT / "scripts" / "build_review_manifest.py")
_brm = importlib.util.module_from_spec(_b); _b.loader.exec_module(_brm)


class _R:
    def __init__(self, rc, out="", err=""):
        self.returncode, self.stdout, self.stderr = rc, out, err


class TestGitStatusSnapshot:
    def test_ok_clean(self, monkeypatch):
        monkeypatch.setattr(_brm.subprocess, "run", lambda *a, **k: _R(0, ""))
        s = _brm._git_status_snapshot()
        assert s["status"] == "OK" and s["records"] == []

    def test_ok_dirty_preserves_paths(self, monkeypatch):
        monkeypatch.setattr(_brm.subprocess, "run",
                            lambda *a, **k: _R(0, " M scripts/app.py\0?? new.py\0"))
        s = _brm._git_status_snapshot()
        assert s["status"] == "OK"
        assert s["records"] == [(" M", "scripts/app.py"), ("??", "new.py")]

    def test_nonzero_exit_is_failed(self, monkeypatch):
        monkeypatch.setattr(_brm.subprocess, "run", lambda *a, **k: _R(128, "", "fatal: not a repo"))
        s = _brm._git_status_snapshot()
        assert s["status"] == "FAILED" and s["records"] == [] and s["diagnostic"]

    def test_timeout(self, monkeypatch):
        def boom(*a, **k):
            raise subprocess.TimeoutExpired(cmd="git", timeout=10)
        monkeypatch.setattr(_brm.subprocess, "run", boom)
        assert _brm._git_status_snapshot()["status"] == "TIMED_OUT"

    def test_git_unavailable(self, monkeypatch):
        def boom(*a, **k):
            raise FileNotFoundError("git")
        monkeypatch.setattr(_brm.subprocess, "run", boom)
        assert _brm._git_status_snapshot()["status"] == "UNAVAILABLE"

    def test_malformed_output_blocks(self, monkeypatch):
        # A record with no status columns / no separating space is malformed.
        monkeypatch.setattr(_brm.subprocess, "run", lambda *a, **k: _R(0, "garbage-no-space\0"))
        s = _brm._git_status_snapshot()
        assert s["status"] == "MALFORMED" and s["records"] == []

    def test_strict_parse_raises_on_malformed(self):
        with pytest.raises(ValueError):
            _brm._parse_status_z("XX", strict=True)          # too short, no path


class TestNonOkStatusBlocksReady:
    def test_classify_marks_and_the_flag_is_recorded(self):
        for status in ("FAILED", "TIMED_OUT", "UNAVAILABLE", "MALFORMED"):
            r = _brm._classify_review_subject(
                "feature/x", "abc", [], False, True, git_status=status)
            assert r["kind"] == "git_status_unavailable"
            assert r["git_status"] == status
            assert r["degraded_metadata"] is True

    def test_ok_status_classifies_normally(self):
        r = _brm._classify_review_subject("feature/x", "abc", [], False, True, git_status="OK")
        assert r["kind"] == "feature_branch" and r["git_status"] == "OK"
