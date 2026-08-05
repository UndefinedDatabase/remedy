"""Config resolution: the precedence rule, and the errors around it."""
import pytest

from sampleproj.config import DEFAULTS, ENV_VARS, read_config_file, resolve
from sampleproj.errors import ConfigError


def test_the_built_in_default_is_used_when_nothing_else_supplies_one():
    assert resolve("max_records", env={}) == DEFAULTS["max_records"]


def test_the_environment_beats_the_built_in_default():
    assert resolve("max_records", env={ENV_VARS["max_records"]: "7"}) == 7


def test_an_explicit_argument_beats_the_environment():
    env = {ENV_VARS["max_records"]: "7"}
    assert resolve("max_records", explicit=9, env=env) == 9


def test_a_file_default_is_used_when_the_environment_is_silent(tmp_path):
    conf = tmp_path / "sampleproj.conf"
    conf.write_text("max_records = 5\n", encoding="utf-8")
    assert resolve("max_records", config_path=conf, env={}) == 5


def test_an_empty_environment_value_does_not_count_as_set(tmp_path):
    conf = tmp_path / "sampleproj.conf"
    conf.write_text("max_records = 5\n", encoding="utf-8")
    env = {ENV_VARS["max_records"]: ""}
    assert resolve("max_records", config_path=conf, env=env) == 5


def test_an_unknown_key_is_refused():
    with pytest.raises(ConfigError, match="unknown config key: nope"):
        resolve("nope", env={})


def test_a_non_numeric_value_is_refused():
    with pytest.raises(ConfigError, match="must be a whole number"):
        resolve("max_records", env={ENV_VARS["max_records"]: "lots"})


def test_comments_and_blank_lines_are_ignored(tmp_path):
    conf = tmp_path / "sampleproj.conf"
    conf.write_text("# a comment\n\nretry_attempts = 4\n", encoding="utf-8")
    assert read_config_file(conf) == {"retry_attempts": 4}


def test_a_missing_config_file_reads_as_empty(tmp_path):
    assert read_config_file(tmp_path / "absent.conf") == {}
