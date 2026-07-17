"""F4 — the strict raw-JSON decoder layer. No Boolean/integer coercion, no silent defaults."""
from __future__ import annotations

import pytest

import tests.orchestration.test_run_manifest as T
from packages.orchestration.manifest_schema import SchemaError
from packages.orchestration.run_manifest import (
    ManifestError,
    decode_episode_snapshot_v1,
    decode_finalized_call_v1,
    decode_index_v1,
    decode_input_snapshot_v1,
    decode_prepared_call_input_v1,
    decode_run_manifest_v1,
)


class TestNoBooleanCoercion:
    def test_string_false_is_rejected_for_call_ok(self):
        d = T._call().to_json()
        d["ok"] = "false"                      # a JSON STRING, not a boolean
        with pytest.raises(SchemaError):
            decode_finalized_call_v1(d)

    def test_int_is_rejected_for_call_ok(self):
        d = T._call().to_json()
        d["ok"] = 0
        with pytest.raises(SchemaError):
            decode_finalized_call_v1(d)

    def test_string_false_is_rejected_for_remedy_dirty(self):
        d = T._snap().to_json()
        d["remedy_dirty"] = "false"
        with pytest.raises(SchemaError):
            decode_input_snapshot_v1(d)

    def test_real_booleans_decode(self):
        snap = decode_input_snapshot_v1(T._snap().to_json())
        assert snap.remedy_dirty is False
        call = decode_finalized_call_v1(T._call().to_json())
        assert call.ok is True


class TestNoIntegerCoercion:
    def test_string_integer_is_rejected(self):
        d = T._call().to_json()
        d["identity"]["sequence"] = "1"
        with pytest.raises(SchemaError):
            decode_finalized_call_v1(d)

    def test_boolean_is_rejected_where_an_integer_is_required(self):
        d = T._call().to_json()
        d["identity"]["round"] = True          # bool is an int subclass — must still be refused
        with pytest.raises(SchemaError):
            decode_finalized_call_v1(d)

    def test_string_prompt_len_is_rejected(self):
        d = T._call().to_json()["prepared_input"]
        d["prompt_len_bytes"] = "12"
        with pytest.raises(SchemaError):
            decode_prepared_call_input_v1(d)


class TestNoSilentDefaults:
    def test_missing_required_field_is_rejected(self):
        d = T._call().to_json()
        d.pop("ok")
        with pytest.raises(SchemaError):
            decode_finalized_call_v1(d)

    def test_unknown_field_is_rejected(self):
        d = T._call().to_json()
        d["surprise"] = 1
        with pytest.raises(SchemaError):
            decode_finalized_call_v1(d)

    def test_snapshot_wrapper_missing_input_key_is_rejected(self):
        d = T._wrap(episode_id="ep").to_json()
        d.pop("input")
        with pytest.raises(SchemaError):
            decode_episode_snapshot_v1(d)


class TestManifestAndIndexDecoding:
    def test_valid_manifest_round_trips(self):
        m = T._mk(episode_id="ep1")
        again = decode_run_manifest_v1(m.to_json())
        assert again.episode_id == "ep1" and again.calls[0].ok is True

    def test_malformed_manifest_bytes_raise_manifest_error(self):
        with pytest.raises(ManifestError):
            decode_run_manifest_v1(b"{bad")

    def test_unsupported_index_version_is_rejected(self):
        with pytest.raises(ManifestError):
            decode_index_v1({"index_v": 99, "latest_episode_id": "e", "episodes": []})

    def test_malformed_index_bytes_raise_manifest_error(self):
        with pytest.raises(ManifestError):
            decode_index_v1(b"{bad")
