"""
Verifier Profile registry for Remedy.

A VerifierProfile describes the semantic quality checks applied to a task's
artifact content during verification.  Profiles are deterministic and local-only
— no shell execution, no LLM calls.

Profiles are selected via the TaskTypeSpec.verifier_profile field, which is
resolved through get_task_type_spec() in task_registry.py.

v1 profiles:
  generic              — baseline check; applies to unknown/unclassified tasks
  repo_doc             — documentation written to the user's repo (README, guides, etc.)
  analysis_doc         — structured analysis/spec/requirement/acceptance documents
  implementation_plan  — planning documents that must carry explicit risk entries

Public API:
  get_verifier_profile(name)   → VerifierProfile  (falls back to generic for unknown names)
  iter_verifier_profiles()     → tuple[VerifierProfile, ...]
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class VerifierProfile:
    """Quality-check profile applied to a task artifact during verification.

    All checks are deterministic and local-only — no shell commands, no LLM calls.

    VerifierProfile owns content-level semantic checks only:
      - required_sections: structure of artifact.content
      - min_proposed_changes: output quantity threshold
      - forbidden_phrases: vagueness / incompleteness signals

    Workspace-file requirements (file exists, non-empty, etc.) are owned by
    TaskContract in verifier.py — they are structural/materialization concerns,
    not content-quality concerns.

    name:
        Stable identifier used by TaskTypeSpec.verifier_profile.
    required_sections:
        Section header strings that must appear somewhere in artifact.content.
        Each entry is checked as a substring match (e.g. "Summary:" matches
        the line "Summary: my summary").
    min_proposed_changes:
        Minimum number of "  - " lines in the Proposed Changes section of
        artifact.content.  1 for most profiles; 2 for stricter analysis types.
    forbidden_phrases:
        Phrases that must NOT appear in artifact.content (case-insensitive).
        Intended to catch vague or incomplete builder output.
    """

    name: str
    required_sections: tuple[str, ...]
    min_proposed_changes: int = 1
    forbidden_phrases: tuple[str, ...] = ()


# ---------------------------------------------------------------------------
# Profile definitions
# ---------------------------------------------------------------------------

_PROFILES: dict[str, VerifierProfile] = {
    "generic": VerifierProfile(
        name="generic",
        required_sections=("Summary:", "Proposed Changes:"),
        min_proposed_changes=1,
        forbidden_phrases=(),
    ),
    "repo_doc": VerifierProfile(
        name="repo_doc",
        required_sections=("Summary:", "Proposed Changes:"),
        min_proposed_changes=1,
        forbidden_phrases=("TODO", "TBD"),
    ),
    "analysis_doc": VerifierProfile(
        name="analysis_doc",
        required_sections=("Summary:", "Proposed Changes:"),
        min_proposed_changes=2,
        forbidden_phrases=("maybe", "probably", "some files", "TODO"),
    ),
    "implementation_plan": VerifierProfile(
        name="implementation_plan",
        required_sections=("Summary:", "Proposed Changes:", "Risks:"),
        min_proposed_changes=2,
        # TODO is intentionally NOT forbidden for implementation plans.
        # Plans may legitimately reference follow-up TODO items or open questions.
        # Vagueness is guarded by "some files", "maybe", and "probably" instead.
        forbidden_phrases=("some files", "maybe", "probably"),
    ),
}

_GENERIC = _PROFILES["generic"]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def get_verifier_profile(name: str | None) -> VerifierProfile:
    """Return the VerifierProfile for the given name.

    Falls back to the generic profile if name is None or not found.
    The generic fallback is intentionally permissive — unknown task types
    should not fail on profile-specific content requirements.
    """
    if name is None:
        return _GENERIC
    return _PROFILES.get(name, _GENERIC)


def iter_verifier_profiles() -> tuple[VerifierProfile, ...]:
    """Return a snapshot of all registered profiles in definition order."""
    return tuple(_PROFILES.values())
