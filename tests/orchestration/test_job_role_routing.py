"""F110 T001b — unit tests for ``default_role_provider_name``.

The function under test is the seam that ended ``run_job``'s literal ``"fake"``
default (finding R-0768). It is PURE: these tests construct no job, open no
network connection and build no provider.

Every expectation about the uninjected case is stated against
``role_config.resolve_role_config(role).provider`` rather than against the
literal name that resolver happens to return today, so the tests pin the SEAM
and not the current product default. A test that asserted ``"ollama"`` would go
red the day the default legitimately changes; these go red only if the two
mechanisms drift apart again, which is the defect.
"""

import pytest

from packages.orchestration import role_config
from packages.orchestration.pingpong_job import default_role_provider_name


class _NamedProvider:
    """An injected provider object that carries a usable ``name``."""

    def __init__(self, name):
        self.name = name


class _NamelessProvider:
    """An injected object with no ``name`` attribute at all."""


class TestNoInjectedProvider:
    """With nothing injected the answer comes from role_config, not a literal."""

    @pytest.mark.parametrize("role", ["builder", "reviewer"])
    def test_resolves_through_role_config(self, role):
        expected = role_config.resolve_role_config(role).provider
        assert default_role_provider_name(role) == expected

    @pytest.mark.parametrize("role", ["builder", "reviewer"])
    def test_explicit_none_is_the_same_as_omitting_it(self, role):
        expected = role_config.resolve_role_config(role).provider
        assert default_role_provider_name(role, None) == expected

    def test_the_two_roles_agree_with_their_own_role_config_entries(self):
        builder = default_role_provider_name("builder")
        reviewer = default_role_provider_name("reviewer")
        assert builder == role_config.resolve_role_config("builder").provider
        assert reviewer == role_config.resolve_role_config("reviewer").provider

    def test_the_answer_is_a_non_empty_provider_name(self):
        resolved = default_role_provider_name("builder")
        assert isinstance(resolved, str)
        assert resolved


class TestInjectedProvider:
    """An injected provider object is what will really run, so it wins."""

    def test_injected_fake_provider_resolves_to_fake(self):
        assert default_role_provider_name("builder", _NamedProvider("fake")) == "fake"

    def test_injected_name_wins_over_the_role_config_answer(self):
        injected = _NamedProvider("a-provider-role-config-would-never-return")
        assert default_role_provider_name("builder", injected) == injected.name
        assert injected.name != role_config.resolve_role_config("builder").provider

    @pytest.mark.parametrize("role", ["builder", "reviewer"])
    def test_injection_is_honoured_for_either_role(self, role):
        assert default_role_provider_name(role, _NamedProvider("fake")) == "fake"


class TestUnusableInjectedName:
    """An object with no usable name falls back to the role_config answer."""

    @pytest.mark.parametrize(
        "injected",
        [_NamelessProvider(), _NamedProvider(None), _NamedProvider(""),
         _NamedProvider(object())],
        ids=["no-attribute", "name-is-none", "name-is-empty", "name-not-a-str"],
    )
    def test_falls_back_to_role_config(self, injected):
        expected = role_config.resolve_role_config("builder").provider
        assert default_role_provider_name("builder", injected) == expected
