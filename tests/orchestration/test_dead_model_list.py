"""Tests for packages.orchestration.dead_model_list — the known-dead model list.

Covers the shipped data file (scripts/dead_models.json), the loader's refusal to
turn an unreadable file into an empty answer, the EXTEND-never-replace merge with
the ``doctor.dead_models`` config key, and the F254 fixture acceptance: a dead
list holding one of Remedy's own built-in default ids is detected.

Pure in-process assertions — no network, no provider probe, and no dependence on
the operator's real remedy.toml: every config-reading test resolves its config
from paths under tmp_path and clears the global cache afterwards.
"""
from __future__ import annotations

import json

import pytest

from packages.orchestration import config
from packages.orchestration.dead_model_list import (
    DEAD_MODEL_CONFIG_KEY,
    DEAD_MODEL_SCHEMA_VERSION,
    DeadModelEntry,
    DeadModelListError,
    dead_model_ids,
    default_dead_list_path,
    load_dead_models,
)
from packages.orchestration.model_aliases import builtin_model_ids


def _write_dead_list(path, entries, *, schema_version=DEAD_MODEL_SCHEMA_VERSION):
    """A fixture dead list on disk, so a test never edits the shipped one."""
    path.write_text(json.dumps({
        "schema_version": schema_version,
        "description": "test fixture",
        "dead_models": entries,
    }), encoding="utf-8")
    return path


@pytest.fixture
def dead_model_config(tmp_path, monkeypatch):
    """Resolve config from EMPTY tmp_path files, so the operator's own
    remedy.toml can never decide the outcome of a test.

    Yields a callable that sets (or clears) the ``doctor.dead_models``
    extension and reloads the cached config. The cache is cleared on teardown,
    so nothing global survives the test.
    """
    project_toml = tmp_path / "project_remedy.toml"
    user_toml = tmp_path / "user_remedy.toml"

    def _apply(extension=None):
        if extension is None:
            monkeypatch.delenv("REMEDY_DOCTOR_DEAD_MODELS", raising=False)
        else:
            monkeypatch.setenv("REMEDY_DOCTOR_DEAD_MODELS", ",".join(extension))
        monkeypatch.setattr(
            config, "_CACHED_CONFIG",
            config.load_config(project_path=project_toml, user_path=user_toml))

    _apply(None)
    yield _apply
    config.reset_config()


class TestShippedDeadList:
    def test_the_shipped_file_is_where_the_loader_looks(self):
        assert default_dead_list_path().is_file()

    def test_the_shipped_file_parses(self):
        entries = load_dead_models()
        assert entries
        assert all(isinstance(entry, DeadModelEntry) for entry in entries)

    def test_every_entry_has_a_non_empty_id_and_reason(self):
        for entry in load_dead_models():
            assert entry.id.strip()
            assert entry.reason.strip()

    def test_superseded_by_is_a_string_and_may_be_empty(self):
        # An empty replacement is honest data: F232 chooses successors, and a
        # guessed model id would be fabricated.
        for entry in load_dead_models():
            assert isinstance(entry.superseded_by, str)

    def test_ids_are_unique(self):
        ids = [entry.id for entry in load_dead_models()]
        assert len(set(ids)) == len(ids)

    def test_schema_version_is_the_one_the_loader_expects(self):
        body = json.loads(default_dead_list_path().read_text(encoding="utf-8"))
        assert body["schema_version"] == DEAD_MODEL_SCHEMA_VERSION

    def test_the_file_describes_itself(self):
        body = json.loads(default_dead_list_path().read_text(encoding="utf-8"))
        assert body["description"].strip()


class TestLoaderRefusesToGuess:
    def test_a_missing_file_raises_and_names_the_path(self, tmp_path):
        missing = tmp_path / "nope" / "dead_models.json"
        with pytest.raises(DeadModelListError) as excinfo:
            load_dead_models(missing)
        assert str(missing) in str(excinfo.value)

    def test_invalid_json_raises(self, tmp_path):
        broken = tmp_path / "dead_models.json"
        broken.write_text("{ not json", encoding="utf-8")
        with pytest.raises(DeadModelListError):
            load_dead_models(broken)

    def test_a_json_array_is_not_a_dead_list(self, tmp_path):
        wrong_shape = tmp_path / "dead_models.json"
        wrong_shape.write_text("[]", encoding="utf-8")
        with pytest.raises(DeadModelListError):
            load_dead_models(wrong_shape)

    def test_an_unsupported_schema_version_raises(self, tmp_path):
        future = _write_dead_list(
            tmp_path / "dead_models.json", [],
            schema_version=DEAD_MODEL_SCHEMA_VERSION + 1)
        with pytest.raises(DeadModelListError):
            load_dead_models(future)

    def test_dead_models_must_be_a_list(self, tmp_path):
        path = tmp_path / "dead_models.json"
        path.write_text(json.dumps({
            "schema_version": DEAD_MODEL_SCHEMA_VERSION,
            "dead_models": {"id": "x"},
        }), encoding="utf-8")
        with pytest.raises(DeadModelListError):
            load_dead_models(path)

    def test_a_blank_reason_raises(self, tmp_path):
        path = _write_dead_list(tmp_path / "dead_models.json", [
            {"id": "some-model", "reason": "   ", "superseded_by": ""},
        ])
        with pytest.raises(DeadModelListError):
            load_dead_models(path)

    def test_duplicate_ids_raise(self, tmp_path):
        path = _write_dead_list(tmp_path / "dead_models.json", [
            {"id": "some-model", "reason": "retired", "superseded_by": ""},
            {"id": "some-model", "reason": "retired twice", "superseded_by": ""},
        ])
        with pytest.raises(DeadModelListError):
            load_dead_models(path)

    def test_an_unreadable_list_never_becomes_an_empty_answer(self, tmp_path):
        # "No dead models" and "I could not read the list" are opposite
        # answers; dead_model_ids() must raise rather than report frozenset().
        broken = tmp_path / "dead_models.json"
        broken.write_text("{ not json", encoding="utf-8")
        with pytest.raises(DeadModelListError):
            dead_model_ids(broken)


class TestConfigExtendsNeverReplaces:
    def test_the_config_key_is_registered(self):
        spec = config.get_key_spec(DEAD_MODEL_CONFIG_KEY)
        assert spec is not None
        assert spec.value_type is list
        assert spec.default is None

    def test_without_an_extension_the_merge_is_the_shipped_list(
            self, tmp_path, dead_model_config):
        dead_model_config(None)
        shipped = _write_dead_list(tmp_path / "dead_models.json", [
            {"id": "shipped-one", "reason": "retired", "superseded_by": ""},
            {"id": "shipped-two", "reason": "retired", "superseded_by": ""},
        ])
        assert dead_model_ids(shipped) == frozenset({"shipped-one", "shipped-two"})

    def test_an_extension_returns_the_union(self, tmp_path, dead_model_config):
        dead_model_config(["operator-one", "operator-two"])
        shipped = _write_dead_list(tmp_path / "dead_models.json", [
            {"id": "shipped-one", "reason": "retired", "superseded_by": ""},
            {"id": "shipped-two", "reason": "retired", "superseded_by": ""},
        ])
        merged = dead_model_ids(shipped)
        assert merged == frozenset({
            "shipped-one", "shipped-two", "operator-one", "operator-two"})

    def test_an_extension_drops_no_shipped_id(self, tmp_path, dead_model_config):
        shipped = _write_dead_list(tmp_path / "dead_models.json", [
            {"id": "shipped-one", "reason": "retired", "superseded_by": ""},
            {"id": "shipped-two", "reason": "retired", "superseded_by": ""},
        ])
        dead_model_config(None)
        before = dead_model_ids(shipped)
        dead_model_config(["operator-one"])
        after = dead_model_ids(shipped)
        # Extension is strictly additive: config cannot configure a shipped
        # entry away, so `before` stays a subset of `after`.
        assert before <= after
        assert after - before == frozenset({"operator-one"})

    def test_the_real_shipped_ids_survive_an_extension(self, dead_model_config):
        dead_model_config(None)
        shipped = frozenset(entry.id for entry in load_dead_models())
        dead_model_config(["operator-only-id"])
        assert shipped <= dead_model_ids()


class TestFixtureAcceptance:
    """The F254 Acceptance bullet: a dead id in a fixture is detected."""

    def test_a_fixture_dead_list_flags_a_builtin_default(
            self, tmp_path, dead_model_config):
        dead_model_config(None)
        # Taken from the alias table rather than typed, so this still means
        # something after F232 changes which ids Remedy ships.
        expected = builtin_model_ids()[0]
        fixture = _write_dead_list(tmp_path / "dead_models.json", [
            {"id": expected, "reason": "fixture: superseded",
             "superseded_by": ""},
        ])
        flagged = frozenset(builtin_model_ids()) & dead_model_ids(fixture)
        assert flagged == frozenset({expected})

    def test_a_fixture_of_unrelated_ids_flags_nothing(
            self, tmp_path, dead_model_config):
        dead_model_config(None)
        fixture = _write_dead_list(tmp_path / "dead_models.json", [
            {"id": "not-a-model-remedy-ships", "reason": "fixture",
             "superseded_by": ""},
        ])
        assert not frozenset(builtin_model_ids()) & dead_model_ids(fixture)

    def test_the_flagged_entry_carries_its_reason(self, tmp_path):
        expected = builtin_model_ids()[0]
        fixture = _write_dead_list(tmp_path / "dead_models.json", [
            {"id": expected, "reason": "fixture: superseded",
             "superseded_by": "some-successor"},
        ])
        entry = next(e for e in load_dead_models(fixture) if e.id == expected)
        # R5's doctor output has to name WHY an id is dead, not just that it is.
        assert entry.reason == "fixture: superseded"
        assert entry.superseded_by == "some-successor"
