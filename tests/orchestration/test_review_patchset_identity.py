"""F6 (round 32) — the commit-patchset identity is bound to exact ordered (commit, archive path, patch
sha) records derived from review_commit_chain.json. Only members under
evidence/current/review_commit_patches/<sha>.patch count; an ordinary source/test filename that merely
contains 'commit_patch' can never enter the identity; a missing or extra patch blocks."""
from __future__ import annotations

import hashlib
import json

from packages.orchestration.review_subject import commit_patchset_identity

_A = "a" * 40
_B = "b" * 40
PREFIX = "evidence/current"


def _chain(*commits):
    return {"chain_v": 1, "commits": [{"commit": c} for c in commits]}


def _snap(*paths_and_shas, **extra):
    d = {p: s for p, s in paths_and_shas}
    d.update(extra)
    return d


class TestPatchsetIdentity:
    def test_exact_ordered_records(self):
        snap = {f"{PREFIX}/review_commit_patches/{_A}.patch": "11" * 32,
                f"{PREFIX}/review_commit_patches/{_B}.patch": "22" * 32}
        r = commit_patchset_identity(_chain(_A, _B), snap, PREFIX)
        assert r["problems"] == []
        assert r["records"] == [
            {"commit": _A, "path": f"{PREFIX}/review_commit_patches/{_A}.patch", "sha256": "11" * 32},
            {"commit": _B, "path": f"{PREFIX}/review_commit_patches/{_B}.patch", "sha256": "22" * 32}]

    def test_unrelated_commit_patch_named_file_is_excluded(self):
        snap = {f"{PREFIX}/review_commit_patches/{_A}.patch": "11" * 32,
                "tests/orchestration/test_review_commit_patch_artifacts.py": "de" * 32,
                "scripts/commit_patch_helper.py": "ff" * 32}
        r = commit_patchset_identity(_chain(_A), snap, PREFIX)
        assert r["problems"] == []
        assert [rec["path"] for rec in r["records"]] == [f"{PREFIX}/review_commit_patches/{_A}.patch"]
        assert "commit_patch" not in json.dumps(r["records"]).replace(f"{PREFIX}/review_commit_patches", "")

    def test_missing_patch_blocks(self):
        r = commit_patchset_identity(_chain(_A, _B),
                                     {f"{PREFIX}/review_commit_patches/{_A}.patch": "11" * 32}, PREFIX)
        assert any("missing patch" in p for p in r["problems"])

    def test_extra_patch_blocks(self):
        snap = {f"{PREFIX}/review_commit_patches/{_A}.patch": "11" * 32,
                f"{PREFIX}/review_commit_patches/{_B}.patch": "22" * 32}
        r = commit_patchset_identity(_chain(_A), snap, PREFIX)
        assert any("unexpected patch member" in p for p in r["problems"])

    def test_non_sha_commit_id_blocks(self):
        r = commit_patchset_identity(_chain("not-a-sha"), {}, PREFIX)
        assert any("is not a full sha" in p for p in r["problems"])

    def test_identity_is_ordered_not_a_multiset(self):
        # Two commits with swapped hashes must give a DIFFERENT identity (order + commit binding).
        snap1 = {f"{PREFIX}/review_commit_patches/{_A}.patch": "11" * 32,
                 f"{PREFIX}/review_commit_patches/{_B}.patch": "22" * 32}
        snap2 = {f"{PREFIX}/review_commit_patches/{_A}.patch": "22" * 32,
                 f"{PREFIX}/review_commit_patches/{_B}.patch": "11" * 32}
        a = commit_patchset_identity(_chain(_A, _B), snap1, PREFIX)["sha256"]
        b = commit_patchset_identity(_chain(_A, _B), snap2, PREFIX)["sha256"]
        assert a != b
