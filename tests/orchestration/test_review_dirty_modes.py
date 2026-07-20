"""F3/F4 (round 19) — a dirty mode change is captured, and the planned mode is bound to the bytes.

F3: a dirty chmod 0644->0755 used to leave current_mode="" so the plan mapped it back to 0644,
losing the mode change under review. F4: the planned regular mode is bound to the OPENED source's
executability, so a plan disagreeing with the source is refused.
"""
from __future__ import annotations

import os
import subprocess

import pytest

from packages.common import secure_fs
from packages.orchestration.archive_plan import (
    MODE_EXECUTABLE,
    MODE_REGULAR,
    build_archive_plan,
)
from packages.orchestration.review_subject import resolve_review_subject


def _sh(r, c):
    subprocess.run(c, shell=True, cwd=r, check=True, capture_output=True)


def _rev(r, ref="HEAD"):
    return subprocess.run(["git", "rev-parse", ref], cwd=r, capture_output=True,
                          text=True).stdout.strip()


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / "repo"
    r.mkdir()
    _sh(r, "git init -q -b main && git config user.email t@t && git config user.name t")
    _sh(r, "echo base > base.txt && git add -A && git commit -qm base")
    base = _rev(r)
    _sh(r, "git checkout -q -b feature")
    return r, base


def _member(plan, path):
    return next((m for m in plan.all_members() if m.archive_path == path), None)


def _plan(r, subject, authority, context):
    return build_archive_plan(repo_root=r, subject=subject, repo_context_rel=context,
                              evidence_root=None, evidence_rel=[],
                              authoritative_paths=set(authority))


class TestDirtyModeCapture:
    def test_a_dirty_chmod_to_executable_plans_0755(self, repo):
        r, base = repo
        _sh(r, "echo '#!/bin/sh' > tool.sh && git add -A && git commit -qm tool")
        base2 = _rev(r)
        # dirty (uncommitted) chmod +x
        os.chmod(str(r / "tool.sh"), 0o755)
        subject = resolve_review_subject(r, base2)
        f = next(f for f in subject.files if f.path == "tool.sh")
        assert f.current_mode == "100755"
        m = _member(_plan(r, subject, {"tool.sh"}, ["tool.sh", "base.txt"]), "tool.sh")
        assert m.mode == MODE_EXECUTABLE

    def test_a_dirty_plain_file_plans_0644(self, repo):
        r, base = repo
        (r / "note.txt").write_text("hi\n")
        subject = resolve_review_subject(r, base)
        f = next(f for f in subject.files if f.path == "note.txt")
        assert f.current_mode == "100644"
        m = _member(_plan(r, subject, {"note.txt"}, ["note.txt", "base.txt"]), "note.txt")
        assert m.mode == MODE_REGULAR


class TestModeBoundToBytes:
    def test_a_0755_plan_over_a_plain_source_is_refused(self, tmp_path):
        (tmp_path / "f.txt").write_text("x")
        os.chmod(str(tmp_path / "f.txt"), 0o644)
        with pytest.raises(RuntimeError) as ei:
            secure_fs.read_verified_relative(str(tmp_path), "f.txt", expected_kind="regular",
                                             expected_mode=0o755, noun="member")
        assert "executable" in str(ei.value)

    def test_a_0644_plan_over_an_executable_source_is_refused(self, tmp_path):
        (tmp_path / "f.txt").write_text("x")
        os.chmod(str(tmp_path / "f.txt"), 0o755)
        with pytest.raises(RuntimeError):
            secure_fs.read_verified_relative(str(tmp_path), "f.txt", expected_kind="regular",
                                             expected_mode=0o644, noun="member")

    def test_a_matching_mode_reads(self, tmp_path):
        (tmp_path / "f.txt").write_text("x")
        os.chmod(str(tmp_path / "f.txt"), 0o644)
        vf = secure_fs.read_verified_relative(str(tmp_path), "f.txt", expected_kind="regular",
                                              expected_mode=0o644, noun="member")
        assert vf.data == b"x"
