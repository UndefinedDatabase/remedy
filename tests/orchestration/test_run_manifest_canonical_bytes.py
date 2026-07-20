"""F11/F13 — raw canonical byte equality and duplicate-key rejection at every stored member."""
from __future__ import annotations

import json

import pytest

import tests.orchestration.test_run_manifest as T
from packages.orchestration.manifest_schema import SchemaError
from packages.orchestration.run_manifest import (
    MANIFEST_FILENAME,
    MANIFESTS_SUBDIR,
    ManifestError,
    decode_run_manifest_v1,
    read_run_manifest,
    require_canonical_bytes,
    strict_json_loads,
    validate_index_and_tree,
    write_run_manifest,
)


def _tree(ev):
    ev.mkdir()
    write_run_manifest(ev, T._mk(episode_id="ep1"), root=ev)
    return ev / MANIFESTS_SUBDIR / "ep1" / MANIFEST_FILENAME


class TestDuplicateKeys:
    def test_duplicate_json_key_is_rejected(self):
        with pytest.raises(SchemaError, match="duplicate JSON key"):
            strict_json_loads('{"a": 1, "a": 2}')

    def test_duplicate_key_in_a_stored_episode_blocks(self, tmp_path):
        ev = tmp_path / "ev"
        ep = _tree(ev)
        raw = ep.read_text()
        ep.write_text(raw.rstrip()[:-1] + ', "job_id": "sneaky"}')
        assert any("duplicate" in p.lower() or "unreadable" in p.lower()
                   for p in validate_index_and_tree(ev, job_id="j"))


class TestCanonicalByteEquality:
    def test_canonical_bytes_accept_the_writer_output(self, tmp_path):
        ep = _tree(tmp_path / "ev")
        raw = ep.read_bytes()
        require_canonical_bytes(raw, decode_run_manifest_v1(raw), where="episode")

    def test_pretty_printed_noncanonical_bytes_are_rejected(self, tmp_path):
        ev = tmp_path / "ev"
        ep = _tree(ev)
        obj = json.loads(ep.read_text())
        ep.write_text(json.dumps(obj, indent=4))      # same object, noncanonical bytes
        with pytest.raises(ManifestError, match="canonical"):
            read_run_manifest(ep)
        assert validate_index_and_tree(ev, job_id="j")

    def test_wrong_boolean_type_in_an_episode_blocks(self, tmp_path):
        ev = tmp_path / "ev"
        ep = _tree(ev)
        obj = json.loads(ep.read_text())
        obj["calls"][0]["ok"] = "false"               # a JSON STRING, not a boolean
        ep.write_text(json.dumps(obj, sort_keys=True, separators=(",", ":")))
        with pytest.raises(ManifestError):
            read_run_manifest(ep)
        assert validate_index_and_tree(ev, job_id="j")

    def test_wrong_boolean_type_in_the_root_mirror_blocks(self, tmp_path):
        ev = tmp_path / "ev"
        _tree(ev)
        mirror = ev / MANIFEST_FILENAME
        obj = json.loads(mirror.read_text())
        obj["calls"][0]["ok"] = "false"
        mirror.write_text(json.dumps(obj, sort_keys=True, separators=(",", ":")))
        probs = validate_index_and_tree(ev, job_id="j")
        assert any("mirror" in p for p in probs), probs

    def test_unknown_snapshot_field_in_the_root_mirror_blocks(self, tmp_path):
        ev = tmp_path / "ev"
        _tree(ev)
        mirror = ev / MANIFEST_FILENAME
        obj = json.loads(mirror.read_text())
        obj["episode_snapshot"]["input"]["EXTRA_SECRET"] = "CANARY-SUPERSECRET-/home/alice"
        mirror.write_text(json.dumps(obj, sort_keys=True, separators=(",", ":")))
        probs = validate_index_and_tree(ev, job_id="j")
        assert any("mirror" in p for p in probs), probs

    def test_mirror_bytes_must_equal_the_latest_episode_bytes(self, tmp_path):
        ev = tmp_path / "ev"
        ep = _tree(ev)
        mirror = ev / MANIFEST_FILENAME
        assert mirror.read_bytes() == ep.read_bytes()     # byte-for-byte by construction
