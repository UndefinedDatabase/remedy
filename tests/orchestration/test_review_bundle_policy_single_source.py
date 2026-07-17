"""F6/F7 (round 20) — one bundle policy governs EVERY repository member, including context.

A `.env`, log, archive or key handed to build_archive_plan as CONTEXT (never in the subject) is
blocked by the same policy — it is never read or packaged.
"""
from __future__ import annotations

import pytest

from packages.orchestration.archive_plan import (
    DISP_BLOCK_SENSITIVE,
    DISP_INCLUDE,
    build_archive_plan,
    classify_bundle_path,
)
from packages.orchestration.review_subject import ReviewSubjectV1


class TestPolicyIsSourceIndependentOfChanged:
    @pytest.mark.parametrize("path", [".env", "config/.env", "prod.log", "bundle.zip",
                                      "keys/id_rsa", "server.pem", "cert.crt"])
    def test_a_sensitive_context_path_blocks(self, path):
        assert classify_bundle_path(path, changed=False) == DISP_BLOCK_SENSITIVE

    def test_a_plain_path_includes(self):
        assert classify_bundle_path("src/app.py", changed=False) == DISP_INCLUDE


class TestContextSensitiveIsBlockedInThePlan:
    @pytest.mark.parametrize("name,body", [(".env", "SECRET=1"), ("prod.log", "log"),
                                           ("bundle.zip", "PK"), ("id_rsa", "KEY")])
    def test_a_direct_context_sensitive_file_never_enters(self, tmp_path, name, body):
        repo = tmp_path / "repo"
        (repo / "sub").mkdir(parents=True)
        (repo / "sub" / name).write_text(body)
        (repo / "keep.py").write_text("x = 1\n")
        rel = f"sub/{name}"
        plan = build_archive_plan(
            repo_root=repo, subject=ReviewSubjectV1(), repo_context_rel=[rel, "keep.py"],
            evidence_root=None, evidence_rel=[], authoritative_paths=set())
        assert plan.blocked
        assert any(b.path == rel and "sensitive" in b.reason for b in plan.blocked_records)
        assert not any(m.archive_path == rel for m in plan.all_members())
