"""F6/F7 (round 19) — the symlink read is atomic, and the bundle-safety policy blocks before reads.

F7: a changed sensitive path (.env/key/log/archive/binary) is BLOCK_SENSITIVE — its bytes never
enter the package — decided from the path alone, before any read, separate from authority.
F6: a symlink member's target/containment is validated on the EXACT bytes returned by the
stability-checked no-follow reader, not a separate earlier realpath a swap could invalidate.
"""
from __future__ import annotations

import os
import subprocess

import pytest

from packages.orchestration.archive_plan import (
    DISP_BLOCK_SENSITIVE,
    DISP_INCLUDE,
    DISP_OPERATOR_CONTEXT,
    classify_bundle_path,
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


def _plan(r, subject, authority=None):
    if authority is None:
        authority = {f.path for f in subject.files}
    return build_archive_plan(repo_root=r, subject=subject,
                              repo_context_rel=["base.txt"], evidence_root=None, evidence_rel=[],
                              authoritative_paths=set(authority))


class TestBundleSafetyPolicy:
    @pytest.mark.parametrize("name", [".env", "secret.pem", "id_rsa", "run.log", "bundle.zip",
                                      "credentials.json", "lib.so"])
    def test_a_changed_sensitive_path_blocks(self, name):
        assert classify_bundle_path(name, changed=True, is_authoritative_source=lambda p: True) \
            == DISP_BLOCK_SENSITIVE

    def test_an_unchanged_sensitive_context_blob_is_not_blocked(self):
        # sensitivity only blocks a CHANGED path; an unchanged context blob is simply not reviewed
        assert classify_bundle_path("app.log", changed=False,
                                    is_authoritative_source=lambda p: False) == DISP_INCLUDE

    def test_agent_state_is_operator_context(self):
        assert classify_bundle_path(".agent/plan.md", changed=True,
                                    is_authoritative_source=lambda p: True) \
            == DISP_OPERATOR_CONTEXT

    def test_a_changed_env_is_blocked_in_the_plan_not_packaged(self, repo):
        r, base = repo
        (r / ".env").write_text("SECRET=1")
        _sh(r, "git add -A && git commit -qm env")
        subject = resolve_review_subject(r, base)
        plan = _plan(r, subject)
        assert plan.blocked
        assert any(b.path == ".env" and "sensitive" in b.reason for b in plan.blocked_records)
        assert not any(m.archive_path == ".env" for m in plan.all_members())


class TestSymlinkAtomicContainment:
    def test_an_internal_symlink_is_a_member(self, repo):
        r, base = repo
        (r / "target.txt").write_text("t")
        os.symlink("target.txt", str(r / "link.txt"))
        subject = resolve_review_subject(r, base)
        plan = _plan(r, subject)
        m = next(m for m in plan.all_members() if m.archive_path == "link.txt")
        assert m.kind == "symlink" and m.expected_link_target == "target.txt"

    def test_an_external_symlink_blocks(self, repo):
        r, base = repo
        os.symlink("/etc/passwd", str(r / "evil.txt"))
        subject = resolve_review_subject(r, base)
        plan = _plan(r, subject)
        assert plan.blocked
        assert any("outside the repository" in b.reason for b in plan.blocked_records)

    def test_a_dotdot_escape_symlink_blocks(self, repo):
        r, base = repo
        os.symlink("../../etc/passwd", str(r / "esc.txt"))
        subject = resolve_review_subject(r, base)
        plan = _plan(r, subject)
        assert plan.blocked
