"""Tests for packages.orchestration.prompt_budget (F112 T001).

Config-backed tests use the REAL ``load_config`` against a pytest
``tmp_path`` TOML file, patched at
``packages.orchestration.config.get_config`` — the idiom
``tests/orchestration/test_role_config.py`` established for
``resolve_effective_task_class_tiers``, which ``resolve_task_class_cap``
mirrors.
"""

from __future__ import annotations

import pathlib

import pytest

from packages.orchestration.config import get_key_spec, load_config
from packages.orchestration.model_routing import TASK_CLASS_TIERS
from packages.orchestration.prompt_budget import (
    DEFAULT_CAP_CONFIG_KEY,
    DEFAULT_FALLBACK_CAP_TOKENS,
    MIN_TASK_CLASS_CAP_TOKENS,
    PROMPT_BUDGET_ESTIMATE_BASIS_CLASS_DEFAULT,
    TASK_CLASS_CAPS_CONFIG_KEY,
    resolve_task_class_cap,
    validate_prompt_budget_config,
)


def _configure_prompt_budget(
    monkeypatch, tmp_path, *, task_class_caps=None, default_cap=None
):
    """Make prompt_budget's config keys answer given values via REAL TOML.

    Nothing is written to the repository root: a ``remedy.toml`` there
    would change how every test in the suite resolves configuration.
    """
    lines: list[str] = []
    if default_cap is not None:
        lines.append("[remedy.prompt_budget]")
        lines.append(f"default_cap = {default_cap}")
    if task_class_caps:
        lines.append(f"[remedy.{TASK_CLASS_CAPS_CONFIG_KEY}]")
        lines += [f"{task_class} = {cap}" for task_class, cap in task_class_caps.items()]
    toml_file = tmp_path / "remedy.toml"
    toml_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    loaded = load_config(
        project_path=toml_file, user_path=pathlib.Path("/nonexistent/user.toml")
    )
    monkeypatch.setattr("packages.orchestration.config.get_config", lambda: loaded)
    return loaded


class TestSharedVocabulary:
    def test_every_task_class_tiers_member_resolves_a_cap(self, monkeypatch, tmp_path):
        _configure_prompt_budget(monkeypatch, tmp_path)
        for task_class in TASK_CLASS_TIERS:
            resolution = resolve_task_class_cap(task_class)
            assert resolution.task_class == task_class

    def test_a_class_outside_task_class_tiers_is_refused(self, monkeypatch, tmp_path):
        _configure_prompt_budget(monkeypatch, tmp_path)
        with pytest.raises(ValueError, match="shared vocabulary"):
            resolve_task_class_cap("not_a_real_class")


class TestResolutionPrecedence:
    def test_no_config_falls_back_to_the_shipped_default(self, monkeypatch, tmp_path):
        _configure_prompt_budget(monkeypatch, tmp_path)
        resolution = resolve_task_class_cap("format")
        assert resolution.cap_tokens == DEFAULT_FALLBACK_CAP_TOKENS
        assert resolution.source == "shipped_default"

    def test_a_configured_global_default_overrides_the_shipped_one(
        self, monkeypatch, tmp_path
    ):
        _configure_prompt_budget(monkeypatch, tmp_path, default_cap=9000)
        resolution = resolve_task_class_cap("format")
        assert resolution.cap_tokens == 9000
        assert resolution.source == "configured_default"

    def test_a_configured_class_cap_wins_over_the_global_default(
        self, monkeypatch, tmp_path
    ):
        _configure_prompt_budget(
            monkeypatch, tmp_path, default_cap=9000, task_class_caps={"format": 5000}
        )
        resolution = resolve_task_class_cap("format")
        assert resolution.cap_tokens == 5000
        assert resolution.source == "configured_class"

    def test_a_class_cap_for_a_different_class_does_not_leak(self, monkeypatch, tmp_path):
        _configure_prompt_budget(
            monkeypatch, tmp_path, task_class_caps={"architecture": 40000}
        )
        resolution = resolve_task_class_cap("format")
        assert resolution.source == "shipped_default"

    @pytest.mark.parametrize("task_class", sorted(TASK_CLASS_TIERS))
    def test_every_resolution_carries_the_class_default_basis(
        self, monkeypatch, tmp_path, task_class
    ):
        _configure_prompt_budget(monkeypatch, tmp_path)
        resolution = resolve_task_class_cap(task_class)
        assert resolution.estimate_basis == PROMPT_BUDGET_ESTIMATE_BASIS_CLASS_DEFAULT


class TestFloorValidation:
    def test_a_clean_config_has_no_errors(self, monkeypatch, tmp_path):
        loaded = _configure_prompt_budget(
            monkeypatch, tmp_path, default_cap=24000, task_class_caps={"format": 4000}
        )
        assert validate_prompt_budget_config(loaded) == []

    def test_no_prompt_budget_table_at_all_has_no_errors(self, monkeypatch, tmp_path):
        loaded = _configure_prompt_budget(monkeypatch, tmp_path)
        assert validate_prompt_budget_config(loaded) == []

    def test_a_class_cap_below_the_floor_is_an_error(self, monkeypatch, tmp_path):
        loaded = _configure_prompt_budget(
            monkeypatch, tmp_path, task_class_caps={"format": 100}
        )
        errors = validate_prompt_budget_config(loaded)
        assert len(errors) == 1
        assert "format" in errors[0]
        assert str(MIN_TASK_CLASS_CAP_TOKENS) in errors[0]

    def test_a_default_cap_below_the_floor_is_an_error(self, monkeypatch, tmp_path):
        loaded = _configure_prompt_budget(monkeypatch, tmp_path, default_cap=1)
        errors = validate_prompt_budget_config(loaded)
        assert len(errors) == 1
        assert DEFAULT_CAP_CONFIG_KEY in errors[0]

    def test_an_unknown_task_class_is_an_error(self, monkeypatch, tmp_path):
        loaded = _configure_prompt_budget(
            monkeypatch, tmp_path, task_class_caps={"not_a_real_class": 5000}
        )
        errors = validate_prompt_budget_config(loaded)
        assert len(errors) == 1
        assert "not_a_real_class" in errors[0]

    def test_both_kinds_of_violation_are_both_reported(self, monkeypatch, tmp_path):
        loaded = _configure_prompt_budget(
            monkeypatch,
            tmp_path,
            default_cap=1,
            task_class_caps={"not_a_real_class": 5000, "format": 100},
        )
        errors = validate_prompt_budget_config(loaded)
        assert len(errors) == 3


class TestConfigRegistration:
    def test_task_class_caps_key_is_a_table_of_ints(self):
        spec = get_key_spec(TASK_CLASS_CAPS_CONFIG_KEY)
        assert spec is not None
        assert spec.value_type is dict
        assert spec.entry_type is int
        assert spec.default is None

    def test_default_cap_key_is_a_scalar_int(self):
        spec = get_key_spec(DEFAULT_CAP_CONFIG_KEY)
        assert spec is not None
        assert spec.value_type is int
        assert spec.default is None
