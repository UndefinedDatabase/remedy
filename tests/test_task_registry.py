"""
Tests for packages/orchestration/task_registry.py.

Covers:
  - TaskTypeSpec structure (fields, frozen, defaults)
  - get_task_type_spec: known task types produce correct routing
  - get_task_type_spec: unknown task types return conservative fallback
  - get_task_type_spec: repo_route is always fully resolved (no {safe_type})
  - is_known_task_type: known/unknown classification
  - iter_task_type_specs: snapshot includes all route rules in order
  - repo routing matches expected routes for each route class
  - path sanitization in resolved repo_route (unsafe chars replaced)
  - unknown fallback has no repo writes (repo_route=None)
  - registry is the single source of truth for both subsystems

All tests are deterministic — no I/O, no live services.
"""

from __future__ import annotations

import pytest

from packages.orchestration.task_registry import (
    TaskTypeSpec,
    _ROUTE_RULES,  # internal — verifying registry completeness and ordering
    get_task_type_spec,
    is_known_task_type,
    iter_task_type_specs,
)


# ---------------------------------------------------------------------------
# TaskTypeSpec model
# ---------------------------------------------------------------------------


class TestTaskTypeSpec:
    def test_spec_is_frozen(self):
        spec = get_task_type_spec("write_readme")
        with pytest.raises((AttributeError, TypeError)):
            spec.name = "other"  # type: ignore[misc]

    def test_spec_has_all_required_fields(self):
        spec = get_task_type_spec("write_readme")
        assert isinstance(spec.name, str)
        assert isinstance(spec.description, str)
        assert isinstance(spec.allowed_outputs, tuple)
        assert isinstance(spec.repo_route, (str, type(None)))
        assert isinstance(spec.verifier_profile, str)
        assert isinstance(spec.suggested_agent_role, str)
        assert isinstance(spec.capabilities, frozenset)

    def test_known_spec_allowed_outputs_contains_workspace_artifact(self):
        spec = get_task_type_spec("write_readme")
        assert "workspace_artifact" in spec.allowed_outputs

    def test_unknown_spec_allowed_outputs_contains_workspace_artifact(self):
        spec = get_task_type_spec("write_code")
        assert "workspace_artifact" in spec.allowed_outputs


# ---------------------------------------------------------------------------
# get_task_type_spec: known routing
# ---------------------------------------------------------------------------


class TestGetTaskTypeSpecKnown:
    def test_readme_routes_to_readme_md(self):
        spec = get_task_type_spec("readme")
        assert spec.repo_route == "README.md"

    def test_write_readme_routes_to_readme_md(self):
        spec = get_task_type_spec("write_readme")
        assert spec.repo_route == "README.md"

    def test_generate_readme_routes_to_readme_md(self):
        spec = get_task_type_spec("generate_README")
        assert spec.repo_route == "README.md"

    def test_plan_routes_to_docs_remedy(self):
        spec = get_task_type_spec("create_implementation_plan")
        assert spec.repo_route is not None
        assert spec.repo_route.startswith("docs/remedy/")

    def test_spec_routes_to_docs_remedy(self):
        spec = get_task_type_spec("write_spec")
        assert spec.repo_route is not None
        assert spec.repo_route.startswith("docs/remedy/")

    def test_requirement_routes_to_docs_remedy(self):
        spec = get_task_type_spec("analyze_requirements")
        assert spec.repo_route is not None
        assert spec.repo_route.startswith("docs/remedy/")

    def test_acceptance_routes_to_docs_remedy(self):
        spec = get_task_type_spec("define_acceptance_checks")
        assert spec.repo_route is not None
        assert spec.repo_route.startswith("docs/remedy/")

    def test_analysis_routes_to_docs_remedy(self):
        spec = get_task_type_spec("analysis_phase")
        assert spec.repo_route is not None
        assert spec.repo_route.startswith("docs/remedy/")

    def test_changelog_routes_to_docs(self):
        spec = get_task_type_spec("generate_changelog")
        assert spec.repo_route is not None
        assert spec.repo_route.startswith("docs/")
        assert "remedy" not in spec.repo_route

    def test_architecture_routes_to_docs(self):
        spec = get_task_type_spec("architecture_overview")
        assert spec.repo_route is not None
        assert spec.repo_route.startswith("docs/")
        assert "remedy" not in spec.repo_route

    def test_design_routes_to_docs(self):
        spec = get_task_type_spec("system_design")
        assert spec.repo_route is not None
        assert spec.repo_route.startswith("docs/")

    def test_guide_routes_to_docs(self):
        spec = get_task_type_spec("write_user_guide")
        assert spec.repo_route is not None
        assert spec.repo_route.startswith("docs/")

    def test_documentation_routes_to_docs(self):
        spec = get_task_type_spec("write_documentation")
        assert spec.repo_route is not None
        assert spec.repo_route.startswith("docs/")

    def test_doc_routes_to_docs(self):
        spec = get_task_type_spec("write_doc")
        assert spec.repo_route is not None
        assert spec.repo_route.startswith("docs/")

    def test_spec_document_routes_to_docs_remedy_not_docs(self):
        """'spec_document' contains both 'spec' and 'doc'; 'spec' must win."""
        spec = get_task_type_spec("spec_document")
        assert spec.repo_route is not None
        assert spec.repo_route.startswith("docs/remedy/"), (
            f"expected docs/remedy/ but got {spec.repo_route!r} — ordering bug"
        )

    def test_planning_document_routes_to_docs_remedy_not_docs(self):
        """'planning_document' contains both 'plan' and 'doc'; 'plan' must win."""
        spec = get_task_type_spec("planning_document")
        assert spec.repo_route is not None
        assert spec.repo_route.startswith("docs/remedy/"), (
            f"expected docs/remedy/ but got {spec.repo_route!r} — ordering bug"
        )

    def test_name_field_is_queried_task_type(self):
        spec = get_task_type_spec("write_readme")
        assert spec.name == "write_readme"

    def test_known_spec_has_no_unknown_capability(self):
        spec = get_task_type_spec("write_readme")
        assert "unknown_task_type" not in spec.capabilities

    def test_verifier_profile_is_generic_in_v1(self):
        spec = get_task_type_spec("write_readme")
        assert spec.verifier_profile == "generic"

    def test_suggested_agent_role_is_generic_builder_in_v1(self):
        spec = get_task_type_spec("write_readme")
        assert spec.suggested_agent_role == "generic_builder"


# ---------------------------------------------------------------------------
# get_task_type_spec: unknown fallback
# ---------------------------------------------------------------------------


class TestGetTaskTypeSpecUnknown:
    def test_write_code_returns_none_repo_route(self):
        spec = get_task_type_spec("write_code")
        assert spec.repo_route is None

    def test_write_tests_returns_none_repo_route(self):
        spec = get_task_type_spec("write_tests")
        assert spec.repo_route is None

    def test_completely_unknown_returns_none_repo_route(self):
        spec = get_task_type_spec("zxqy_totally_unknown_xyz")
        assert spec.repo_route is None

    def test_empty_string_returns_none_repo_route(self):
        spec = get_task_type_spec("")
        assert spec.repo_route is None

    def test_unknown_name_field_is_queried_task_type(self):
        spec = get_task_type_spec("write_code")
        assert spec.name == "write_code"

    def test_unknown_has_unknown_task_type_capability(self):
        spec = get_task_type_spec("write_code")
        assert "unknown_task_type" in spec.capabilities

    def test_unknown_description_signals_fallback(self):
        spec = get_task_type_spec("zxqy_totally_unknown_xyz")
        assert "unknown" in spec.description.lower() or "fallback" in spec.description.lower()

    def test_unknown_verifier_profile_is_generic(self):
        spec = get_task_type_spec("write_code")
        assert spec.verifier_profile == "generic"

    def test_unknown_allowed_outputs_conservative(self):
        spec = get_task_type_spec("write_code")
        assert "workspace_artifact" in spec.allowed_outputs


# ---------------------------------------------------------------------------
# get_task_type_spec: repo_route fully resolved (no {safe_type})
# ---------------------------------------------------------------------------


class TestGetTaskTypeSpecRouteResolution:
    def test_repo_route_contains_no_safe_type_placeholder(self):
        for task_type in ("write_readme", "create_spec", "analyze_requirements",
                          "write_architecture", "write_changelog"):
            spec = get_task_type_spec(task_type)
            if spec.repo_route is not None:
                assert "{safe_type}" not in spec.repo_route, (
                    f"unresolved placeholder in repo_route for {task_type!r}: "
                    f"{spec.repo_route!r}"
                )

    def test_unsafe_chars_in_task_type_are_sanitized(self):
        spec = get_task_type_spec("acceptance checks for release")
        assert spec.repo_route is not None
        assert " " not in spec.repo_route

    def test_traversal_in_task_type_is_sanitized(self):
        # "../evil plan" contains "plan" → docs/remedy/ route; dots/slashes sanitized
        spec = get_task_type_spec("../evil plan")
        if spec.repo_route is not None:
            assert ".." not in spec.repo_route

    def test_readme_route_is_literal(self):
        spec = get_task_type_spec("generate_readme")
        assert spec.repo_route == "README.md"

    def test_docs_remedy_route_ends_with_md(self):
        spec = get_task_type_spec("write_spec")
        assert spec.repo_route is not None
        assert spec.repo_route.endswith(".md")

    def test_docs_route_ends_with_md(self):
        spec = get_task_type_spec("write_architecture")
        assert spec.repo_route is not None
        assert spec.repo_route.endswith(".md")


# ---------------------------------------------------------------------------
# is_known_task_type
# ---------------------------------------------------------------------------


class TestIsKnownTaskType:
    def test_readme_is_known(self):
        assert is_known_task_type("write_readme") is True

    def test_spec_is_known(self):
        assert is_known_task_type("write_spec") is True

    def test_plan_is_known(self):
        assert is_known_task_type("create_implementation_plan") is True

    def test_write_code_is_unknown(self):
        assert is_known_task_type("write_code") is False

    def test_write_tests_is_unknown(self):
        assert is_known_task_type("write_tests") is False

    def test_empty_string_is_unknown(self):
        assert is_known_task_type("") is False

    def test_completely_novel_type_is_unknown(self):
        assert is_known_task_type("zxqy_totally_unknown_xyz") is False

    def test_is_known_matches_get_spec_has_repo_route(self):
        """is_known_task_type must agree with get_task_type_spec().repo_route != None."""
        for task_type in ("write_readme", "create_spec", "write_code", "implement_feature"):
            known = is_known_task_type(task_type)
            spec = get_task_type_spec(task_type)
            # known ↔ has repo_route
            assert known == (spec.repo_route is not None), (
                f"is_known_task_type({task_type!r})={known} but "
                f"get_task_type_spec().repo_route={spec.repo_route!r}"
            )


# ---------------------------------------------------------------------------
# iter_task_type_specs
# ---------------------------------------------------------------------------


class TestIterTaskTypeSpecs:
    def test_returns_tuple(self):
        result = iter_task_type_specs()
        assert isinstance(result, tuple)

    def test_length_matches_route_rules(self):
        result = iter_task_type_specs()
        assert len(result) == len(_ROUTE_RULES)

    def test_all_items_are_task_type_specs(self):
        for spec in iter_task_type_specs():
            assert isinstance(spec, TaskTypeSpec)

    def test_names_match_route_rule_keywords(self):
        keywords = [kw for kw, _, _ in _ROUTE_RULES]
        spec_names = [spec.name for spec in iter_task_type_specs()]
        assert spec_names == keywords

    def test_no_safe_type_placeholder_in_repo_routes(self):
        for spec in iter_task_type_specs():
            if spec.repo_route is not None:
                assert "{safe_type}" not in spec.repo_route

    def test_readme_spec_has_correct_route(self):
        specs = {s.name: s for s in iter_task_type_specs()}
        assert specs["readme"].repo_route == "README.md"

    def test_plan_spec_routes_to_docs_remedy(self):
        specs = {s.name: s for s in iter_task_type_specs()}
        assert specs["plan"].repo_route is not None
        assert specs["plan"].repo_route.startswith("docs/remedy/")

    def test_doc_spec_routes_to_docs(self):
        specs = {s.name: s for s in iter_task_type_specs()}
        assert specs["doc"].repo_route is not None
        assert specs["doc"].repo_route.startswith("docs/")
        assert "remedy" not in specs["doc"].repo_route

    def test_all_known_specs_have_no_unknown_capability(self):
        for spec in iter_task_type_specs():
            assert "unknown_task_type" not in spec.capabilities

    def test_documentation_appears_before_doc_in_order(self):
        """'documentation' must precede 'doc' — substring ordering."""
        names = [s.name for s in iter_task_type_specs()]
        assert names.index("documentation") < names.index("doc"), (
            "ordering bug: 'documentation' must appear before 'doc'"
        )

    def test_plan_appears_before_doc_in_order(self):
        """'plan' must precede 'doc' — docs/remedy/ before docs/ catch-all."""
        names = [s.name for s in iter_task_type_specs()]
        assert names.index("plan") < names.index("doc"), (
            "ordering bug: 'plan' must appear before 'doc'"
        )

    def test_snapshot_is_independent_tuple(self):
        """iter_task_type_specs returns a new tuple each call."""
        first = iter_task_type_specs()
        second = iter_task_type_specs()
        assert first == second  # same content
        assert first is not second  # not the same object
