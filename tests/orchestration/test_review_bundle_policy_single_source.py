"""F5/F6/F7 (round 20/21) — ONE ArchivePlan disposition owner over every repository member.

A CHANGED sensitive path is BLOCK_SENSITIVE (hard block); an UNCHANGED sensitive CONTEXT path is
EXCLUDE_SAFE_CONTEXT (explicit exclusion record, never packaged, never silently absent).
"""
from __future__ import annotations

import pytest

from packages.orchestration.archive_plan import (
    DISP_BLOCK_SENSITIVE,
    DISP_EXCLUDE_SAFE_CONTEXT,
    DISP_INCLUDE,
    build_archive_plan,
    classify_bundle_path,
)
from packages.orchestration.review_subject import ReviewSubjectV1


class TestPolicyDependsOnChanged:
    @pytest.mark.parametrize("path", [".env", "config/.env", "prod.log", "bundle.zip",
                                      "keys/id_rsa", "server.pem", "cert.crt"])
    def test_a_changed_sensitive_path_blocks(self, path):
        assert classify_bundle_path(path, changed=True) == DISP_BLOCK_SENSITIVE

    @pytest.mark.parametrize("path", [".env", "config/.env", "prod.log", "bundle.zip",
                                      "keys/id_rsa", "server.pem", "cert.crt"])
    def test_an_unchanged_sensitive_context_path_is_safely_excluded(self, path):
        assert classify_bundle_path(path, changed=False) == DISP_EXCLUDE_SAFE_CONTEXT

    def test_a_plain_path_includes(self):
        assert classify_bundle_path("src/app.py", changed=False) == DISP_INCLUDE


class TestContextSensitiveIsExcludedInThePlan:
    @pytest.mark.parametrize("name,body", [(".env", "SECRET=1"), ("prod.log", "log"),
                                           ("bundle.zip", "PK"), ("id_rsa", "KEY")])
    def test_a_direct_context_sensitive_file_is_excluded_with_a_record(self, tmp_path, name, body):
        repo = tmp_path / "repo"
        (repo / "sub").mkdir(parents=True)
        (repo / "sub" / name).write_text(body)
        (repo / "keep.py").write_text("x = 1\n")
        rel = f"sub/{name}"
        plan = build_archive_plan(
            repo_root=repo, subject=ReviewSubjectV1(), repo_context_rel=[rel, "keep.py"],
            evidence_root=None, evidence_rel=[], authoritative_paths=set())
        # Not a hard block, but an EXPLICIT exclusion record, and never a member.
        assert not plan.blocked
        assert any(e.path == rel and e.disposition == DISP_EXCLUDE_SAFE_CONTEXT
                   for e in plan.excluded_records)
        assert not any(m.archive_path == rel for m in plan.all_members())
        assert any(m.archive_path == "keep.py" for m in plan.all_members())
