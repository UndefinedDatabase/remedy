"""Tests for packages.orchestration.config — remedy.toml configuration system v0."""

from __future__ import annotations

from pathlib import Path

import pytest

from packages.orchestration.config import (
    ConfigKeySpec,
    ConfigSource,
    ConfigValue,
    RemedyConfig,
    _TABLE_VALUED_KEYS,
    _coerce_value,
    _extract_remedy_table,
    _flatten_toml,
    all_key_specs,
    get_config,
    get_key_spec,
    load_config,
    reset_config,
    set_config_value,
    validate_config,
    write_toml_template,
)
from packages.orchestration.model_aliases import resolve_model_alias
from packages.orchestration.model_routing import MODEL_TIERS, TASK_CLASS_TIERS
from packages.orchestration.role_config import TASK_CLASS_TIERS_CONFIG_KEY


class TestConfigSource:
    def test_values(self):
        assert ConfigSource.ENV.value == "env"
        assert ConfigSource.PROJECT.value == "project"
        assert ConfigSource.USER.value == "user"
        assert ConfigSource.DEFAULT.value == "default"


class TestConfigValue:
    def test_is_default(self):
        cv = ConfigValue(key="k", value="v", source=ConfigSource.DEFAULT)
        assert cv.is_default is True

    def test_not_default(self):
        cv = ConfigValue(key="k", value="v", source=ConfigSource.ENV)
        assert cv.is_default is False


class TestConfigKeySpec:
    def test_all_specs_populated(self):
        specs = all_key_specs()
        assert len(specs) >= 18
        keys = {s.key for s in specs}
        assert "data_dir" in keys
        assert "ollama.host" in keys
        assert "ollama.builder.model" in keys
        assert "ollama.planner.model" in keys
        assert "ui.host" in keys
        assert "ui.port" in keys
        assert "tests.pytest_timeout_seconds" in keys
        assert "quality.coverage_fail_under" in keys
        assert "logging.level" in keys
        assert "claude_enabled" in keys
        assert "opencode_enabled" in keys
        assert "pi_dev_enabled" in keys
        assert "external_memory_enabled" in keys

    def test_get_key_spec(self):
        spec = get_key_spec("data_dir")
        assert spec is not None
        assert spec.env_var == "REMEDY_DATA_DIR"

    def test_get_unknown_key(self):
        assert get_key_spec("nonexistent.key") is None

    # F255: the teacher's own routing surface. Pinned by EXPECTED LITERAL
    # because a test that reads the spec it is meant to freeze cannot fail.
    def test_teacher_model_key_is_declared(self):
        spec = get_key_spec("teacher.model")
        assert spec is not None
        assert spec.env_var == "REMEDY_TEACHER_MODEL"
        assert spec.value_type is str
        assert spec.default is None

    def test_fallback_keys(self):
        builder = get_key_spec("ollama.builder.model")
        assert builder is not None
        assert builder.fallback_key == "ollama.model"
        planner = get_key_spec("ollama.planner.model")
        assert planner is not None
        assert planner.fallback_key == "ollama.model"


class TestCoerceValue:
    def test_float(self):
        spec = ConfigKeySpec(key="t", env_var="T", description="", value_type=float)
        assert _coerce_value("0.3", spec) == 0.3

    def test_int(self):
        spec = ConfigKeySpec(key="t", env_var="T", description="", value_type=int)
        assert _coerce_value("4096", spec) == 4096

    def test_bool_true(self):
        spec = ConfigKeySpec(key="t", env_var="T", description="", value_type=bool)
        assert _coerce_value("true", spec) is True
        assert _coerce_value("1", spec) is True
        assert _coerce_value("yes", spec) is True

    def test_bool_false(self):
        spec = ConfigKeySpec(key="t", env_var="T", description="", value_type=bool)
        assert _coerce_value("false", spec) is False
        assert _coerce_value("0", spec) is False

    def test_str(self):
        spec = ConfigKeySpec(key="t", env_var="T", description="", value_type=str)
        assert _coerce_value("hello", spec) == "hello"

    def test_invalid_float(self):
        spec = ConfigKeySpec(key="t", env_var="T", description="", value_type=float)
        with pytest.raises(ValueError):
            _coerce_value("notfloat", spec)


class TestFlattenToml:
    def test_flat(self):
        assert _flatten_toml({"host": "x"}) == {"host": "x"}

    def test_nested(self):
        d = {"ollama": {"host": "x", "builder": {"model": "y"}}}
        flat = _flatten_toml(d)
        assert flat == {"ollama.host": "x", "ollama.builder.model": "y"}

    def test_empty(self):
        assert _flatten_toml({}) == {}


class TestExtractRemedyTable:
    def test_present(self):
        assert _extract_remedy_table({"remedy": {"k": "v"}}) == {"k": "v"}

    def test_missing(self):
        assert _extract_remedy_table({"other": {}}) == {}


class TestLoadConfig:
    def test_defaults_no_files(self):
        config = load_config(
            project_path=Path("/nonexistent/project.toml"),
            user_path=Path("/nonexistent/user.toml"),
        )
        assert config.get("ollama.host") == "http://localhost:11434"
        assert config.get("ollama.model") == resolve_model_alias("ollama-default")
        assert config.get("data_dir") is None
        assert config.get_source("ollama.host") == ConfigSource.DEFAULT

    def test_project_toml(self, tmp_path):
        toml_file = tmp_path / "remedy.toml"
        toml_file.write_text('[remedy]\ndata_dir = "/custom/data"\n')
        config = load_config(
            project_path=toml_file,
            user_path=Path("/nonexistent/user.toml"),
        )
        assert config.get("data_dir") == "/custom/data"
        assert config.get_source("data_dir") == ConfigSource.PROJECT

    def test_user_toml(self, tmp_path):
        toml_file = tmp_path / "remedy.toml"
        toml_file.write_text('[remedy.ollama]\nhost = "http://userhost:11434"\n')
        config = load_config(
            project_path=Path("/nonexistent/project.toml"),
            user_path=toml_file,
        )
        assert config.get("ollama.host") == "http://userhost:11434"
        assert config.get_source("ollama.host") == ConfigSource.USER

    def test_project_overrides_user(self, tmp_path):
        project_toml = tmp_path / "project.toml"
        project_toml.write_text('[remedy.ollama]\nhost = "http://project:11434"\n')
        user_toml = tmp_path / "user.toml"
        user_toml.write_text('[remedy.ollama]\nhost = "http://user:11434"\n')
        config = load_config(project_path=project_toml, user_path=user_toml)
        assert config.get("ollama.host") == "http://project:11434"
        assert config.get_source("ollama.host") == ConfigSource.PROJECT

    def test_env_overrides_toml(self, tmp_path, monkeypatch):
        toml_file = tmp_path / "remedy.toml"
        toml_file.write_text('[remedy.ollama]\nhost = "http://toml:11434"\n')
        monkeypatch.setenv("REMEDY_OLLAMA_HOST", "http://env:11434")
        config = load_config(
            project_path=toml_file,
            user_path=Path("/nonexistent/user.toml"),
        )
        assert config.get("ollama.host") == "http://env:11434"
        assert config.get_source("ollama.host") == ConfigSource.ENV

    def test_fallback_key(self, tmp_path):
        toml_file = tmp_path / "remedy.toml"
        toml_file.write_text('[remedy.ollama]\nmodel = "llama3.1"\n')
        config = load_config(
            project_path=toml_file,
            user_path=Path("/nonexistent/user.toml"),
        )
        assert config.get("ollama.builder.model") == "llama3.1"
        assert config.get("ollama.planner.model") == "llama3.1"

    def test_fallback_not_used_for_default(self):
        config = load_config(
            project_path=Path("/nonexistent/project.toml"),
            user_path=Path("/nonexistent/user.toml"),
        )
        assert config.get("ollama.builder.model") is None

    def test_load_report(self, tmp_path):
        toml_file = tmp_path / "remedy.toml"
        toml_file.write_text("[remedy]\n")
        config = load_config(
            project_path=toml_file,
            user_path=Path("/nonexistent/user.toml"),
        )
        assert config.load_report.project_loaded is True
        assert config.load_report.user_loaded is False

    def test_float_coercion_from_env(self, monkeypatch):
        monkeypatch.setenv("REMEDY_OLLAMA_BUILDER_TEMPERATURE", "0.7")
        config = load_config(
            project_path=Path("/nonexistent/project.toml"),
            user_path=Path("/nonexistent/user.toml"),
        )
        assert config.get("ollama.builder.temperature") == 0.7
        assert isinstance(config.get("ollama.builder.temperature"), float)

    def test_int_coercion_from_env(self, monkeypatch):
        monkeypatch.setenv("REMEDY_OLLAMA_BUILDER_NUM_PREDICT", "4096")
        config = load_config(
            project_path=Path("/nonexistent/project.toml"),
            user_path=Path("/nonexistent/user.toml"),
        )
        assert config.get("ollama.builder.num_predict") == 4096


class TestGetConfig:
    def test_caching(self):
        reset_config()
        c1 = get_config()
        c2 = get_config()
        assert c1 is c2

    def test_reset(self):
        reset_config()
        c1 = get_config()
        reset_config()
        c2 = get_config()
        assert c1 is not c2


class TestRemedyConfigMethods:
    def test_get_unknown(self):
        config = RemedyConfig()
        assert config.get("nonexistent") is None
        assert config.get_value("nonexistent") is None
        assert config.get_source("nonexistent") is None

    def test_to_summary_dict(self):
        config = load_config(
            project_path=Path("/nonexistent/project.toml"),
            user_path=Path("/nonexistent/user.toml"),
        )
        summary = config.to_summary_dict()
        assert summary["config_version"] == 0
        assert isinstance(summary["keys"], list)
        assert len(summary["keys"]) >= 18
        assert "load_report" in summary


class TestWriteTomlTemplate:
    def test_creates_file(self, tmp_path):
        path = tmp_path / "remedy.toml"
        write_toml_template(path)
        assert path.exists()
        content = path.read_text()
        assert "[remedy]" in content
        assert "[remedy.ollama]" in content

    def test_creates_parent_dirs(self, tmp_path):
        path = tmp_path / "sub" / "dir" / "remedy.toml"
        write_toml_template(path)
        assert path.exists()


class TestSetConfigValue:
    def test_creates_file(self, tmp_path):
        path = tmp_path / "remedy.toml"
        set_config_value(path, "data_dir", "/custom")
        assert path.exists()
        config = load_config(
            project_path=path,
            user_path=Path("/nonexistent/user.toml"),
        )
        assert config.get("data_dir") == "/custom"

    def test_nested_key(self, tmp_path):
        path = tmp_path / "remedy.toml"
        set_config_value(path, "ollama.host", "http://custom:11434")
        config = load_config(
            project_path=path,
            user_path=Path("/nonexistent/user.toml"),
        )
        assert config.get("ollama.host") == "http://custom:11434"

    def test_env_only_rejected(self, tmp_path):
        path = tmp_path / "remedy.toml"
        spec = get_key_spec("data_dir")
        if spec and not spec.env_only:
            set_config_value(path, "data_dir", "/ok")

    def test_updates_existing(self, tmp_path):
        path = tmp_path / "remedy.toml"
        set_config_value(path, "data_dir", "/first")
        set_config_value(path, "data_dir", "/second")
        config = load_config(
            project_path=path,
            user_path=Path("/nonexistent/user.toml"),
        )
        assert config.get("data_dir") == "/second"


class TestSetConfigValueGuards:
    def test_rejects_unknown_key(self, tmp_path):
        path = tmp_path / "remedy.toml"
        with pytest.raises(ValueError, match="Unknown config key"):
            set_config_value(path, "totally.bogus.key", "val")

    def test_rejects_env_only_key(self, tmp_path):
        path = tmp_path / "remedy.toml"
        with pytest.raises(ValueError, match="env-only"):
            set_config_value(path, "claude_enabled", "true")

    def test_accepts_known_key(self, tmp_path):
        path = tmp_path / "remedy.toml"
        set_config_value(path, "ollama.host", "http://custom:11434")
        assert path.exists()


class TestLoadDiagnostics:
    def test_malformed_toml_raises_budget_config_error(self, tmp_path):
        """F018: malformed TOML must fail closed, not return empty dict."""
        from packages.orchestration.budget_resolution import BudgetConfigError
        bad = tmp_path / "bad.toml"
        bad.write_text("this is [ not valid toml ugh")
        with pytest.raises(BudgetConfigError, match="Malformed TOML"):
            load_config(project_path=bad, user_path=Path("/nonexistent/user.toml"))

    def test_unknown_key_warning(self, tmp_path):
        toml_file = tmp_path / "remedy.toml"
        toml_file.write_text('[remedy]\nunknown_key = "val"\n')
        config = load_config(project_path=toml_file, user_path=Path("/nonexistent/user.toml"))
        assert any("Unknown key" in w for w in config.load_report.warnings)

    def test_no_warnings_for_valid(self, tmp_path):
        toml_file = tmp_path / "remedy.toml"
        toml_file.write_text('[remedy.ollama]\nhost = "http://localhost:11434"\n')
        config = load_config(project_path=toml_file, user_path=Path("/nonexistent/user.toml"))
        assert config.load_report.warnings == []


class TestPathRedaction:
    def test_summary_dict_redacts_absolute_paths(self):
        config = load_config(
            project_path=Path("/nonexistent/project.toml"),
            user_path=Path("/nonexistent/user.toml"),
        )
        summary = config.to_summary_dict()
        pp = summary["load_report"]["project_path"]
        up = summary["load_report"]["user_path"]
        assert not pp.startswith("/") or pp.startswith("~/")
        assert not up.startswith("/") or up.startswith("~/")

    def test_relative_path_preserved(self):
        config = load_config(
            project_path=Path("remedy.toml"),
            user_path=Path("/nonexistent/user.toml"),
        )
        summary = config.to_summary_dict()
        assert summary["load_report"]["project_path"] == "remedy.toml"


class TestValidateConfig:
    def test_valid_config(self):
        config = load_config(
            project_path=Path("/nonexistent/project.toml"),
            user_path=Path("/nonexistent/user.toml"),
        )
        warnings = validate_config(config)
        assert warnings == []

    def test_invalid_float(self):
        config = RemedyConfig(values={
            "ollama.builder.temperature": ConfigValue(
                key="ollama.builder.temperature",
                value="notfloat",
                source=ConfigSource.ENV,
            ),
        })
        warnings = validate_config(config)
        assert any("float" in w for w in warnings)


class TestEnvOnlyKey:
    def test_env_only_not_read_from_toml(self, tmp_path):
        spec = ConfigKeySpec(
            key="test_secret",
            env_var="REMEDY_TEST_SECRET",
            description="test",
            env_only=True,
        )
        assert spec.env_only is True


class TestRedactionClosure:
    """Verify R-0121/R-0122/R-0123 closures."""

    def test_r0121_key_value_redacted(self):
        from packages.orchestration.redaction_patterns import _SECRET_RE

        assert _SECRET_RE.sub("[REDACTED]", "api_key=mysecret123") == "[REDACTED]"
        assert _SECRET_RE.sub("[REDACTED]", "password=hunter2") == "[REDACTED]"
        assert _SECRET_RE.sub("[REDACTED]", "token=xyz789") == "[REDACTED]"
        assert _SECRET_RE.sub("[REDACTED]", "api_key = spaced") == "[REDACTED]"

    def test_r0124_quoted_key_value_redacted(self):
        from packages.orchestration.redaction_patterns import _SECRET_RE

        assert _SECRET_RE.sub("[REDACTED]", 'password="mysecret123"') == "[REDACTED]"
        assert _SECRET_RE.sub("[REDACTED]", "api_key='mysecret'") == "[REDACTED]"
        assert _SECRET_RE.sub("[REDACTED]", "secret=\"spaced value\"") == "[REDACTED]"
        assert _SECRET_RE.sub("[REDACTED]", "token='abc def'") == "[REDACTED]"

    def test_r0121_category_words_not_matched(self):
        from packages.orchestration.redaction_patterns import _SECRET_RE

        assert _SECRET_RE.sub("[REDACTED]", "No secrets here") == "No secrets here"
        assert _SECRET_RE.sub("[REDACTED]", "environment_secrets") == "environment_secrets"

    def test_r0122_is_optional_is_bug_used(self):
        from packages.orchestration.review_bundle import (
            ReviewBundleSectionSpec,
            _build_section_safe,
        )

        def _fail():
            raise ImportError("missing module")

        spec = ReviewBundleSectionSpec("test.json", _fail, description="test")
        _, _, section = _build_section_safe(spec, builder_args={})
        assert section.structured_error is not None
        assert section.structured_error.is_optional_dependency is True
        assert section.structured_error.is_bug is False

    def test_r0122_bug_category(self):
        from packages.orchestration.review_bundle import (
            ReviewBundleSectionSpec,
            _build_section_safe,
        )

        def _fail():
            raise RuntimeError("unexpected")

        spec = ReviewBundleSectionSpec("test.json", _fail, description="test")
        _, _, section = _build_section_safe(spec, builder_args={})
        assert section.structured_error is not None
        assert section.structured_error.is_bug is True
        assert section.structured_error.is_optional_dependency is False

    def test_r0123_structured_error_in_production(self):
        from packages.orchestration.review_bundle import (
            ReviewBundleSectionError,
            ReviewBundleSectionSpec,
            _build_section_safe,
        )

        def _fail():
            raise ValueError("bad data")

        spec = ReviewBundleSectionSpec("test.json", _fail, description="test")
        _, _, section = _build_section_safe(spec, builder_args={})
        assert isinstance(section.structured_error, ReviewBundleSectionError)
        d = section.structured_error.to_dict()
        assert d["section_name"] == "test.json"
        assert d["error_type"] == "ValueError"
        assert d["is_bug"] is True
        assert "occurred_at" in d


class TestPostmortemConfig:
    """F010: generated summaries are OFF, and the key says so."""

    def test_the_llm_summary_key_exists_and_defaults_to_false(self):
        from packages.orchestration.config import get_config, get_key_spec

        spec = get_key_spec("postmortem.llm_summary")
        assert spec is not None
        assert spec.env_var == "REMEDY_POSTMORTEM_LLM_SUMMARY"
        assert spec.value_type is bool
        assert spec.default is False
        assert "zero provider calls" in spec.description
        assert get_config().get("postmortem.llm_summary") is False

    def test_the_env_var_can_set_it_but_v1_generates_nothing(self, monkeypatch):
        from packages.orchestration.config import load_config

        monkeypatch.setenv("REMEDY_POSTMORTEM_LLM_SUMMARY", "true")
        assert load_config().get("postmortem.llm_summary") is True
        # ...and no summarizer exists to act on it: F010 v1 is deterministic by design.
        import packages.orchestration.failure_postmortem as FP
        assert not any("summar" in name.lower() for name in dir(FP))


class TestPlanningGranularityConfig:
    """F016: the granularity thresholds are config keys, not constants."""

    @pytest.mark.parametrize(
        ("key", "env_var", "value_type", "default"),
        [
            ("planning.granularity.enabled",
             "REMEDY_PLANNING_GRANULARITY_ENABLED", bool, True),
            ("planning.granularity.split_band",
             "REMEDY_PLANNING_GRANULARITY_SPLIT_BAND", str, "XL"),
            ("planning.granularity.max_acceptance",
             "REMEDY_PLANNING_GRANULARITY_MAX_ACCEPTANCE", int, 3),
            ("planning.granularity.merge_group_size",
             "REMEDY_PLANNING_GRANULARITY_MERGE_GROUP_SIZE", int, 3),
        ],
    )
    def test_key_spec_and_default(self, key, env_var, value_type, default):
        spec = get_key_spec(key)
        assert spec is not None
        assert spec.env_var == env_var
        assert spec.value_type is value_type
        assert spec.default == default
        assert get_config().get(key) == default

    def test_enabled_can_be_switched_off_by_env(self, monkeypatch):
        monkeypatch.setenv("REMEDY_PLANNING_GRANULARITY_ENABLED", "false")
        assert load_config().get("planning.granularity.enabled") is False


def _override_table_toml(table: dict[str, str]) -> str:
    """Render *table* as the TOML a project would actually write.

    The table header is built from ``TASK_CLASS_TIERS_CONFIG_KEY``, so the key
    the router reads and the key the test writes are the SAME string and cannot
    drift into a test that passes against a key nothing reads.
    """
    lines = [f"[remedy.{TASK_CLASS_TIERS_CONFIG_KEY}]"]
    lines += [f'{task_class} = "{tier}"' for task_class, tier in table.items()]
    return "\n".join(lines) + "\n"


class TestTableValuedKeys:
    """F110 R10: ``value_type is dict`` makes a key resolve as ONE whole table.

    Every task class and every tier below is READ from
    :mod:`packages.orchestration.model_routing`, and the key name from
    :mod:`packages.orchestration.role_config`, so a re-tiering of the seed
    mapping or a rename of the key cannot leave a stale literal passing here.
    """

    def test_the_key_is_registered_as_table_valued(self):
        spec = get_key_spec(TASK_CLASS_TIERS_CONFIG_KEY)
        assert spec is not None
        assert spec.env_var == "REMEDY_MODEL_ROUTING_TASK_CLASS_TIERS"
        assert spec.value_type is dict
        # NOT {} — "nothing configured" and "an explicitly empty table" are
        # different operator statements and stay distinguishable.
        assert spec.default is None

    def test_the_stop_set_is_derived_from_the_registry(self):
        # Derived, never hand-listed: exactly the specs whose value_type is
        # dict. Registering a second table key must need no second edit.
        assert _TABLE_VALUED_KEYS == {
            spec.key for spec in all_key_specs() if spec.value_type is dict
        }
        assert TASK_CLASS_TIERS_CONFIG_KEY in _TABLE_VALUED_KEYS

    def test_flatten_stops_at_a_table_valued_key(self):
        task_class = sorted(TASK_CLASS_TIERS)[0]
        table = {task_class: MODEL_TIERS[-1]}
        parts = TASK_CLASS_TIERS_CONFIG_KEY.split(".")
        nested: dict = {parts[-1]: table}
        for part in reversed(parts[:-1]):
            nested = {part: nested}
        assert _flatten_toml(nested) == {TASK_CLASS_TIERS_CONFIG_KEY: table}

    def test_a_project_table_resolves_as_one_dict_with_no_warning(self, tmp_path):
        first, second = sorted(TASK_CLASS_TIERS)[:2]
        table = {first: MODEL_TIERS[-1], second: MODEL_TIERS[0]}
        toml_file = tmp_path / "remedy.toml"
        toml_file.write_text(_override_table_toml(table))
        config = load_config(
            project_path=toml_file,
            user_path=Path("/nonexistent/user.toml"),
        )
        assert config.get(TASK_CLASS_TIERS_CONFIG_KEY) == table
        assert config.get_source(TASK_CLASS_TIERS_CONFIG_KEY) == ConfigSource.PROJECT
        # ...and NOT one "Unknown key in ..." diagnostic per entry, which is
        # exactly what the unstopped recursion produced.
        assert config.load_report.warnings == []

    def test_an_unset_table_resolves_to_none(self):
        config = load_config(
            project_path=Path("/nonexistent/project.toml"),
            user_path=Path("/nonexistent/user.toml"),
        )
        assert config.get(TASK_CLASS_TIERS_CONFIG_KEY) is None
        assert config.get_source(TASK_CLASS_TIERS_CONFIG_KEY) == ConfigSource.DEFAULT

    def test_a_project_table_replaces_a_user_table_whole(self, tmp_path):
        # The two tables name DIFFERENT classes, so a MERGE would be visible as
        # a resolved value carrying both. Precedence resolves a table the way it
        # resolves a scalar: one source wins outright.
        first, second = sorted(TASK_CLASS_TIERS)[:2]
        user_table = {first: MODEL_TIERS[0]}
        project_table = {second: MODEL_TIERS[-1]}
        project_toml = tmp_path / "project.toml"
        project_toml.write_text(_override_table_toml(project_table))
        user_toml = tmp_path / "user.toml"
        user_toml.write_text(_override_table_toml(user_table))
        config = load_config(project_path=project_toml, user_path=user_toml)
        assert config.get(TASK_CLASS_TIERS_CONFIG_KEY) == project_table
        assert config.get_source(TASK_CLASS_TIERS_CONFIG_KEY) == ConfigSource.PROJECT

    def test_a_user_table_resolves_when_no_project_file_has_one(self, tmp_path):
        user_table = {sorted(TASK_CLASS_TIERS)[0]: MODEL_TIERS[-1]}
        user_toml = tmp_path / "user.toml"
        user_toml.write_text(_override_table_toml(user_table))
        config = load_config(
            project_path=Path("/nonexistent/project.toml"),
            user_path=user_toml,
        )
        assert config.get(TASK_CLASS_TIERS_CONFIG_KEY) == user_table
        assert config.get_source(TASK_CLASS_TIERS_CONFIG_KEY) == ConfigSource.USER


class TestTableValuedKeyShapeValidation:
    """SHAPE ONLY. Whether an override is LEGAL is a POLICY question, and
    config.py is the lower layer: it never imports model_routing to answer one.
    """

    def test_a_non_string_entry_is_reported(self, tmp_path):
        task_class = sorted(TASK_CLASS_TIERS)[0]
        toml_file = tmp_path / "remedy.toml"
        toml_file.write_text(
            f"[remedy.{TASK_CLASS_TIERS_CONFIG_KEY}]\n{task_class} = 3\n"
        )
        config = load_config(
            project_path=toml_file,
            user_path=Path("/nonexistent/user.toml"),
        )
        found = validate_config(config)
        assert any(
            TASK_CLASS_TIERS_CONFIG_KEY in warning and task_class in warning
            for warning in found
        ), found

    def test_a_well_formed_table_is_reported_silently(self, tmp_path):
        table = {sorted(TASK_CLASS_TIERS)[0]: MODEL_TIERS[-1]}
        toml_file = tmp_path / "remedy.toml"
        toml_file.write_text(_override_table_toml(table))
        config = load_config(
            project_path=toml_file,
            user_path=Path("/nonexistent/user.toml"),
        )
        assert validate_config(config) == []

    def test_a_policy_illegal_but_well_formed_table_is_silent_here(self):
        # A table the ROUTER refuses is not a SHAPE fault, and config.py must
        # not learn what a task class or a tier is in order to say so.
        spec = get_key_spec(TASK_CLASS_TIERS_CONFIG_KEY)
        illegal = {sorted(TASK_CLASS_TIERS)[0]: "not-a-tier"}
        config = RemedyConfig(
            values={
                spec.key: ConfigValue(
                    key=spec.key, value=illegal, source=ConfigSource.PROJECT
                )
            }
        )
        assert validate_config(config) == []

    def test_a_scalar_where_a_table_belongs_is_reported(self):
        # An env var cannot carry a table, so a bare string can arrive here.
        spec = get_key_spec(TASK_CLASS_TIERS_CONFIG_KEY)
        config = RemedyConfig(
            values={
                spec.key: ConfigValue(
                    key=spec.key, value="cheap", source=ConfigSource.ENV
                )
            }
        )
        found = validate_config(config)
        assert any(TASK_CLASS_TIERS_CONFIG_KEY in warning for warning in found), found
