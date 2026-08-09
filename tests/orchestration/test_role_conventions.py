"""Tests for the role conventions loaders (F105 T002).

The load-bearing property here is content equality: the conventions segment must
be the reviewed document, byte for byte, so "extraction changed no rules" is
proven rather than asserted. The rest pins the registration contract (name,
rank, cap), the two failure modes, the mapping completeness, and the guards that
keep the cap imported and the module free of a tokenizer or a provider.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from packages.orchestration import role_conventions
from packages.orchestration.prompt_segments import (
    CONVENTIONS_TOKEN_CAP,
    PromptSegmentError,
    PromptSegmentRegistry,
    SegmentStabilityRank,
    compose_prompt_segments,
)
from packages.orchestration.role_conventions import (
    CONVENTIONS_DOC_RELATIVE_PATHS,
    CONVENTIONS_SEGMENT_NAMES,
    ConventionsRole,
    RoleConventionsError,
    register_role_conventions_segment,
    role_conventions_document_path,
    role_conventions_text,
)
from packages.orchestration.token_economy import estimate_text_tokens

ROLES = list(ConventionsRole)


def _register(role: ConventionsRole, repo_root: Path | None = None):
    registry = PromptSegmentRegistry()
    return registry, register_role_conventions_segment(registry, role, repo_root=repo_root)


def _write_repo_root(tmp_path: Path, oversized_role: ConventionsRole | None = None) -> Path:
    """A throwaway repo root carrying both documents at their real relative paths."""
    for role, relative in CONVENTIONS_DOC_RELATIVE_PATHS.items():
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        body = "x" * 8000 if role is oversized_role else "small\n"
        target.write_text(body, encoding="utf-8")
    return tmp_path


# ---------------------------------------------------------------------------
# 1: the content-equality golden — the reason this module exists
# ---------------------------------------------------------------------------


class TestRoleConventionsContentEquality:
    @pytest.mark.parametrize("role", ROLES)
    def test_loaded_text_equals_the_document_byte_for_byte(self, role):
        on_disk = role_conventions_document_path(role).read_text(encoding="utf-8")
        assert role_conventions_text(role) == on_disk

    @pytest.mark.parametrize("role", ROLES)
    def test_document_estimate_is_positive_and_under_the_cap(self, role):
        estimated = estimate_text_tokens(role_conventions_text(role))
        assert estimated > 0, f"{role.value}: ESTIMATE is {estimated}"
        assert estimated <= CONVENTIONS_TOKEN_CAP, (
            f"{role.value}: ESTIMATE {estimated} tokens (chars/4, never a count) "
            f"exceeds the cap {CONVENTIONS_TOKEN_CAP}"
        )


# ---------------------------------------------------------------------------
# 2: the registration contract
# ---------------------------------------------------------------------------


class TestRoleConventionsRegistration:
    @pytest.mark.parametrize("role", ROLES)
    def test_registered_segment_carries_the_documented_name_and_rank(self, role):
        _, segment = _register(role)
        assert segment.name == CONVENTIONS_SEGMENT_NAMES[role]
        assert segment.rank is SegmentStabilityRank.CONVENTIONS

    @pytest.mark.parametrize("role", ROLES)
    def test_registration_mutates_no_text(self, role):
        _, segment = _register(role)
        assert segment.text == role_conventions_text(role)

    @pytest.mark.parametrize("role", ROLES)
    def test_composing_one_conventions_segment_yields_exactly_the_document(self, role):
        registry, _ = _register(role)
        composed = compose_prompt_segments(registry.registered_segments())
        assert composed.text == role_conventions_text(role)

    def test_over_cap_document_raises_prompt_segment_error(self, tmp_path):
        repo_root = _write_repo_root(tmp_path, oversized_role=ConventionsRole.WORKER)
        registry = PromptSegmentRegistry()
        with pytest.raises(PromptSegmentError) as excinfo:
            register_role_conventions_segment(
                registry, ConventionsRole.WORKER, repo_root=repo_root
            )
        assert CONVENTIONS_SEGMENT_NAMES[ConventionsRole.WORKER] in str(excinfo.value)
        assert registry.registered_segments() == ()


# ---------------------------------------------------------------------------
# 3: the failure modes
# ---------------------------------------------------------------------------


class TestRoleConventionsFailures:
    @pytest.mark.parametrize("role", ROLES)
    def test_missing_document_raises_and_names_the_relative_path(self, role, tmp_path):
        with pytest.raises(RoleConventionsError) as excinfo:
            role_conventions_text(role, repo_root=tmp_path)
        assert CONVENTIONS_DOC_RELATIVE_PATHS[role] in str(excinfo.value)

    def test_non_utf8_document_raises_role_conventions_error(self, tmp_path):
        repo_root = _write_repo_root(tmp_path)
        target = repo_root / CONVENTIONS_DOC_RELATIVE_PATHS[ConventionsRole.WORKER]
        target.write_bytes(b"\xff\xfe not utf-8")
        with pytest.raises(RoleConventionsError) as excinfo:
            role_conventions_text(ConventionsRole.WORKER, repo_root=repo_root)
        assert CONVENTIONS_DOC_RELATIVE_PATHS[ConventionsRole.WORKER] in str(excinfo.value)

    def test_role_conventions_error_is_a_prompt_segment_error(self):
        assert issubclass(RoleConventionsError, PromptSegmentError)


# ---------------------------------------------------------------------------
# 4: the mappings cover every role, without aliasing
# ---------------------------------------------------------------------------


class TestRoleConventionsMappings:
    def test_every_role_has_a_path_and_a_segment_name(self):
        assert set(CONVENTIONS_DOC_RELATIVE_PATHS) == set(ROLES)
        assert set(CONVENTIONS_SEGMENT_NAMES) == set(ROLES)

    def test_no_two_roles_share_a_path_or_a_segment_name(self):
        paths = list(CONVENTIONS_DOC_RELATIVE_PATHS.values())
        names = list(CONVENTIONS_SEGMENT_NAMES.values())
        assert len(set(paths)) == len(paths)
        assert len(set(names)) == len(names)

    # These assert the EXPECTED LITERAL per role BECAUSE a test that reads the
    # mapping it is meant to pin can never fail, however wrong that mapping is.
    @pytest.mark.parametrize(
        "role, expected_name",
        [
            (ConventionsRole.WORKER, "worker_conventions"),
            (ConventionsRole.REVIEWER, "reviewer_conventions"),
        ],
    )
    def test_segment_name_mapping_holds_the_expected_literal(self, role, expected_name):
        assert CONVENTIONS_SEGMENT_NAMES[role] == expected_name
        _, segment = _register(role)
        assert segment.name == expected_name

    @pytest.mark.parametrize(
        "role, expected_relative",
        [
            (ConventionsRole.WORKER, "docs/agents/worker_conventions.md"),
            (ConventionsRole.REVIEWER, "docs/agents/reviewer_conventions.md"),
        ],
    )
    def test_document_path_mapping_holds_the_expected_literal(self, role, expected_relative):
        assert CONVENTIONS_DOC_RELATIVE_PATHS[role] == expected_relative


# ---------------------------------------------------------------------------
# 5: architecture guards — the cap stays imported, the module stays dependency-free
# ---------------------------------------------------------------------------


def _module_source() -> str:
    return Path(role_conventions.__file__).read_text(encoding="utf-8")


class TestRoleConventionsArchitectureGuards:
    def test_the_cap_is_imported_not_restated(self):
        assert str(CONVENTIONS_TOKEN_CAP) not in _module_source()

    def test_no_tokenizer_network_or_provider_dependency(self):
        source = _module_source()
        for banned in ("requests", "httpx", "socket", "subprocess", "tiktoken"):
            assert banned not in source, banned


# ---------------------------------------------------------------------------
# 6: rule anchors — neither document was hollowed out while being loaded
# ---------------------------------------------------------------------------


class TestConventionsDocumentRuleAnchors:
    @pytest.mark.parametrize(
        "role, anchors",
        [
            (
                ConventionsRole.WORKER,
                ("## Ground rules", "## Completion report (required fields)"),
            ),
            (
                ConventionsRole.REVIEWER,
                ("## Stance", "## Findings", "## Block conditions"),
            ),
        ],
    )
    def test_document_still_carries_its_headings(self, role, anchors):
        text = role_conventions_text(role)
        for anchor in anchors:
            assert anchor in text, anchor

    def test_reviewer_document_still_lists_six_block_conditions(self):
        text = role_conventions_text(ConventionsRole.REVIEWER)
        section = text.split("## Block conditions", 1)[1].split("\n## ", 1)[0]
        numbered = [line for line in section.split("\n") if re.match(r"^\d+\. ", line)]
        assert len(numbered) == 6, numbered
