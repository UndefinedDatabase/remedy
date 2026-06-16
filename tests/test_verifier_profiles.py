"""
Tests for packages/orchestration/verifier_profiles.py.

Covers:
  - VerifierProfile: frozen dataclass (immutable), all expected fields
  - get_verifier_profile: returns correct profile, falls back to generic
  - iter_verifier_profiles: includes all expected profile names
  - Profile values: min_proposed_changes, forbidden_phrases, required_sections
    are correct for each named profile

All tests are deterministic — no I/O, no live services.
"""

from __future__ import annotations

import pytest

from packages.orchestration.verifier_profiles import (
    VerifierProfile,
    get_verifier_profile,
    iter_verifier_profiles,
)

# ---------------------------------------------------------------------------
# VerifierProfile: structure and immutability
# ---------------------------------------------------------------------------


class TestVerifierProfileStruct:
    def test_is_frozen_dataclass(self):
        profile = get_verifier_profile("generic")
        with pytest.raises((AttributeError, TypeError)):
            profile.name = "mutated"  # type: ignore[misc]

    def test_has_expected_fields(self):
        profile = get_verifier_profile("generic")
        assert hasattr(profile, "name")
        assert hasattr(profile, "required_sections")
        assert hasattr(profile, "min_proposed_changes")
        assert hasattr(profile, "forbidden_phrases")

    def test_does_not_have_workspace_fields(self):
        """Workspace requirements belong to TaskContract, not VerifierProfile."""
        profile = get_verifier_profile("generic")
        assert not hasattr(profile, "require_workspace_file")
        assert not hasattr(profile, "require_nonempty_workspace_file")

    def test_required_sections_is_tuple(self):
        for profile in iter_verifier_profiles():
            assert isinstance(profile.required_sections, tuple)

    def test_forbidden_phrases_is_tuple(self):
        for profile in iter_verifier_profiles():
            assert isinstance(profile.forbidden_phrases, tuple)

    def test_min_proposed_changes_is_int(self):
        for profile in iter_verifier_profiles():
            assert isinstance(profile.min_proposed_changes, int)
            assert profile.min_proposed_changes >= 1

    def test_no_profile_has_workspace_fields(self):
        """Workspace requirements are owned by TaskContract, not any profile."""
        for profile in iter_verifier_profiles():
            assert not hasattr(profile, "require_workspace_file")
            assert not hasattr(profile, "require_nonempty_workspace_file")


# ---------------------------------------------------------------------------
# get_verifier_profile
# ---------------------------------------------------------------------------


class TestGetVerifierProfile:
    def test_returns_generic_for_generic(self):
        profile = get_verifier_profile("generic")
        assert profile.name == "generic"

    def test_returns_repo_doc(self):
        profile = get_verifier_profile("repo_doc")
        assert profile.name == "repo_doc"

    def test_returns_analysis_doc(self):
        profile = get_verifier_profile("analysis_doc")
        assert profile.name == "analysis_doc"

    def test_returns_implementation_plan(self):
        profile = get_verifier_profile("implementation_plan")
        assert profile.name == "implementation_plan"

    def test_unknown_name_falls_back_to_generic(self):
        profile = get_verifier_profile("nonexistent_profile")
        assert profile.name == "generic"

    def test_none_falls_back_to_generic(self):
        profile = get_verifier_profile(None)
        assert profile.name == "generic"

    def test_fallback_is_permissive(self):
        """Generic fallback has no forbidden phrases so unknown types don't fail."""
        profile = get_verifier_profile("totally_unknown")
        assert profile.forbidden_phrases == ()
        assert profile.min_proposed_changes == 1


# ---------------------------------------------------------------------------
# iter_verifier_profiles
# ---------------------------------------------------------------------------


class TestIterVerifierProfiles:
    def test_includes_all_expected_names(self):
        names = {p.name for p in iter_verifier_profiles()}
        assert "generic" in names
        assert "repo_doc" in names
        assert "analysis_doc" in names
        assert "implementation_plan" in names

    def test_returns_tuple(self):
        result = iter_verifier_profiles()
        assert isinstance(result, tuple)

    def test_all_entries_are_verifier_profiles(self):
        for p in iter_verifier_profiles():
            assert isinstance(p, VerifierProfile)

    def test_no_duplicates(self):
        names = [p.name for p in iter_verifier_profiles()]
        assert len(names) == len(set(names))


# ---------------------------------------------------------------------------
# Profile content: generic
# ---------------------------------------------------------------------------


class TestGenericProfile:
    def setup_method(self):
        self.profile = get_verifier_profile("generic")

    def test_requires_summary_section(self):
        assert "Summary:" in self.profile.required_sections

    def test_requires_proposed_changes_section(self):
        assert "Proposed Changes:" in self.profile.required_sections

    def test_min_proposed_changes_is_1(self):
        assert self.profile.min_proposed_changes == 1

    def test_no_forbidden_phrases(self):
        assert self.profile.forbidden_phrases == ()


# ---------------------------------------------------------------------------
# Profile content: repo_doc
# ---------------------------------------------------------------------------


class TestRepoDocProfile:
    def setup_method(self):
        self.profile = get_verifier_profile("repo_doc")

    def test_requires_summary_section(self):
        assert "Summary:" in self.profile.required_sections

    def test_requires_proposed_changes_section(self):
        assert "Proposed Changes:" in self.profile.required_sections

    def test_does_not_require_risks_section(self):
        assert "Risks:" not in self.profile.required_sections

    def test_min_proposed_changes_is_1(self):
        assert self.profile.min_proposed_changes == 1

    def test_forbids_TODO(self):
        assert "TODO" in self.profile.forbidden_phrases

    def test_forbids_TBD(self):
        assert "TBD" in self.profile.forbidden_phrases


# ---------------------------------------------------------------------------
# Profile content: analysis_doc
# ---------------------------------------------------------------------------


class TestAnalysisDocProfile:
    def setup_method(self):
        self.profile = get_verifier_profile("analysis_doc")

    def test_requires_summary_section(self):
        assert "Summary:" in self.profile.required_sections

    def test_requires_proposed_changes_section(self):
        assert "Proposed Changes:" in self.profile.required_sections

    def test_min_proposed_changes_is_2(self):
        assert self.profile.min_proposed_changes == 2

    def test_forbids_maybe(self):
        assert "maybe" in self.profile.forbidden_phrases

    def test_forbids_probably(self):
        assert "probably" in self.profile.forbidden_phrases

    def test_forbids_some_files(self):
        assert "some files" in self.profile.forbidden_phrases

    def test_forbids_TODO(self):
        assert "TODO" in self.profile.forbidden_phrases


# ---------------------------------------------------------------------------
# Profile content: implementation_plan
# ---------------------------------------------------------------------------


class TestImplementationPlanProfile:
    def setup_method(self):
        self.profile = get_verifier_profile("implementation_plan")

    def test_requires_summary_section(self):
        assert "Summary:" in self.profile.required_sections

    def test_requires_proposed_changes_section(self):
        assert "Proposed Changes:" in self.profile.required_sections

    def test_requires_risks_section(self):
        assert "Risks:" in self.profile.required_sections

    def test_min_proposed_changes_is_2(self):
        assert self.profile.min_proposed_changes == 2

    def test_forbids_some_files(self):
        assert "some files" in self.profile.forbidden_phrases

    def test_forbids_maybe(self):
        assert "maybe" in self.profile.forbidden_phrases

    def test_forbids_probably(self):
        assert "probably" in self.profile.forbidden_phrases

    def test_does_not_forbid_TODO(self):
        """implementation_plan intentionally does not forbid TODO.

        Plans may legitimately reference follow-up TODO items or open questions.
        Vagueness is guarded by 'some files', 'maybe', and 'probably' instead.
        """
        assert "TODO" not in self.profile.forbidden_phrases
        assert "todo" not in [p.lower() for p in self.profile.forbidden_phrases]
