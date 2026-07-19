"""F3 (round 28) — a working-tree change is dispositioned as a packaging output ONLY when its path
is a member of the EXACT set of outputs THIS packaging invocation generates (passed from
make_review_zip.sh). An arbitrary leftover/forged root ZIP from another invocation is NOT hidden:
without the current run's set as authority, only its own outputs are excluded and every other change
— including a lookalike root ZIP — stays a dirty source change so a real changed file is never
concealed."""
from __future__ import annotations

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
_b = importlib.util.spec_from_file_location(
    "_brm_dirty", REPO_ROOT / "scripts" / "build_review_manifest.py")
_brm = importlib.util.module_from_spec(_b); _b.loader.exec_module(_brm)
_z = importlib.util.spec_from_file_location(
    "_brz_dirty", REPO_ROOT / "scripts" / "build_review_zip.py")
_brz = importlib.util.module_from_spec(_z); _z.loader.exec_module(_brz)

# The exact outputs a single invocation with STAMP 20260719-131500 generates.
GEN = frozenset({
    ".review_zip_manifest.json",
    "remedy-review-20260719-131500.zip",
})


class TestExactSetMembership:
    def test_no_grammar_predicate_remains(self):
        # F3: the invocation-independent filename grammar is gone — only the passed set classifies.
        assert not hasattr(_brm, "_is_packaging_output")
        assert not hasattr(_brm, "_PKG_ZIP_RE")

    def test_clean_branch_with_only_its_own_outputs_stays_clean(self):
        r = _brm._classify_review_subject(
            "feature/x", "abc123def456",
            ["?? .review_zip_manifest.json",
             "?? remedy-review-20260719-131500.zip"],
            True, True, generated_outputs=GEN)
        assert r["kind"] == "feature_branch"
        assert r["dirty_files"] == []
        assert sorted(r["packaging_generated_outputs"]) == sorted(GEN)

    def test_real_dirty_file_still_dirty(self):
        r = _brm._classify_review_subject(
            "feature/x", "abc", [" M scripts/app.py", "?? .review_zip_manifest.json"],
            True, True, generated_outputs=GEN)
        assert r["kind"] == "dirty_working_tree"
        assert r["dirty_files"] == [" M scripts/app.py"]
        assert r["packaging_generated_outputs"] == [".review_zip_manifest.json"]

    def test_renamed_line_path_extracted(self):
        assert _brm._dirty_line_path("R  old.py -> new.py") == "new.py"


class TestForeignOutputsAreNeverHidden:
    """The Round-28 reproductions: a root ZIP from ANOTHER invocation (a stale stamp, a wild stamp,
    or a forged status suffix) is NOT in the current invocation's generated set, so it stays a dirty
    source change and a co-located real changed file is surfaced with it."""

    def test_stale_and_wild_and_forged_root_zips_stay_dirty(self):
        dirty = [
            "?? remedy-review-20200101-000000-READY_FOR_REVIEW.zip",   # stale stamp
            "?? remedy-review-99999999-999999-CORPUS.zip",             # impossible stamp
            "?? remedy-review-20260719-124709-EVIL.zip",               # forged status
            " M scripts/app.py",                                       # a REAL changed file
            "?? .review_zip_manifest.json",                            # the current run's own output
        ]
        r = _brm._classify_review_subject(
            "feature/x", "abc", dirty, True, True, generated_outputs=GEN)
        assert r["kind"] == "dirty_working_tree"
        assert sorted(_brm._dirty_line_path(x) for x in r["dirty_files"]) == sorted([
            "remedy-review-20200101-000000-READY_FOR_REVIEW.zip",
            "remedy-review-99999999-999999-CORPUS.zip",
            "remedy-review-20260719-124709-EVIL.zip",
            "scripts/app.py"])
        assert r["packaging_generated_outputs"] == [".review_zip_manifest.json"]

    def test_empty_set_classifies_nothing_fail_closed(self):
        # With no current-invocation set (e.g. a stage that cannot know it), NOTHING is hidden.
        dirty = ["?? remedy-review-20260719-131500.zip", "?? .review_zip_manifest.json"]
        r = _brm._classify_review_subject("feature/x", "abc", dirty, True, True)
        assert r["kind"] == "dirty_working_tree"
        assert r["packaging_generated_outputs"] == []
        assert len(r["dirty_files"]) == 2

    def test_nested_same_name_is_not_the_root_output(self):
        # The set holds repo-ROOT paths; a nested file with the same basename is not a member.
        dirty = ["?? tests/fixtures/remedy-review-20260719-131500.zip",
                 "?? docs/.review_zip_manifest.json"]
        r = _brm._classify_review_subject(
            "feature/x", "abc", dirty, True, True, generated_outputs=GEN)
        assert r["kind"] == "dirty_working_tree"
        assert r["packaging_generated_outputs"] == []
        assert len(r["dirty_files"]) == 2


class TestGeneratedOutputAuthorityIsNotCallerSupplied:
    """F3 (round 29) — the disposition is bound to the packaging-output SHAPE and the invocation's own
    DERIVED outputs, never an arbitrary path a caller names. A declared source path cannot hide."""

    def test_injected_source_path_cannot_hide_a_dirty_source_file(self):
        # The external reproduction: a caller declares a real source file as a generated output.
        r = _brm._classify_review_subject(
            "feature/x", "abc", [" M scripts/security_fix.py"], True, True,
            generated_outputs={"scripts/security_fix.py"})
        assert r["kind"] == "dirty_working_tree"
        assert _brm._dirty_line_path(r["dirty_files"][0]) == "scripts/security_fix.py"
        assert r["packaging_generated_outputs"] == []

    def test_root_source_lookalike_declaration_is_rejected(self):
        r = _brm._classify_review_subject(
            "feature/x", "abc", [" M security_fix.py"], True, True,
            generated_outputs={"security_fix.py"})
        assert r["packaging_generated_outputs"] == []
        assert len(r["dirty_files"]) == 1

    def test_eligibility_predicate(self):
        ok = _brm._eligible_generated_output
        assert ok(".review_zip_manifest.json")
        assert ok("remedy-review-20260719-131500.zip")
        assert ok("remedy-review-20260719-131500-READY_FOR_REVIEW.zip")
        assert ok("remedy-review-20260719-131500.zip.sha256")
        for bad in ("scripts/security_fix.py", "security_fix.py", "review_zip_manifest.json",
                    "tests/fixtures/remedy-review-20260719-131500.zip", "remedy-review-x.zip",
                    "docs/.review_zip_manifest.json", ""):
            assert not ok(bad), bad


class TestGeneratedOutputDerivedInternally:
    """The coordinator derives the set from its OWN --out/--manifest-rel, so a direct Python builder
    invocation has the same safety as the shell wrapper, and two invocations do not share identity."""

    def test_derive_from_concrete_outputs(self):
        gen = _brz._derive_generated_outputs(
            _brm, "/repo", "/repo/remedy-review-20260719-131500.zip", ".review_zip_manifest.json")
        assert gen == frozenset({"remedy-review-20260719-131500.zip", ".review_zip_manifest.json"})

    def test_derive_rejects_outside_root_and_source_like(self):
        gen = _brz._derive_generated_outputs(
            _brm, "/repo", "/repo/scripts/app.py", "/repo/nested/.review_zip_manifest.json")
        assert gen == frozenset()

    def test_two_invocations_do_not_share_identity(self):
        a = _brz._derive_generated_outputs(
            _brm, "/repo", "remedy-review-20260719-131500.zip", ".review_zip_manifest.json")
        b = _brz._derive_generated_outputs(
            _brm, "/repo", "remedy-review-20260719-140000.zip", ".review_zip_manifest.json")
        # Invocation B's ZIP is not in A's set, so B's output stays dirty under A's classification.
        dirty = ["?? remedy-review-20260719-140000.zip"]
        r = _brm._classify_review_subject("feature/x", "abc", dirty, True, True, generated_outputs=a)
        assert r["packaging_generated_outputs"] == []
        assert len(r["dirty_files"]) == 1
        assert "remedy-review-20260719-140000.zip" in b
