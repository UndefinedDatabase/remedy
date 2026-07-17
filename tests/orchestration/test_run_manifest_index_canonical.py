"""F2 (round 9) — the Index is CANONICAL RAW BYTES, not "some JSON that parses".

`run_manifest_index.json` is a trust anchor: it names the latest episode and the canonical
episode order. Accepting whatever happens to parse means the bytes an operator hashes, copies or
diffs are not the bytes Remedy trusted. So at EVERY entry point the stored bytes must literally
equal `canonical_index_bytes(decode_index_v1(bytes))`: strict duplicate-key decode, size limit
BEFORE decode, exact schema, no unknown fields.
"""
from __future__ import annotations

import dataclasses

import json

import pytest

import tests.orchestration.test_run_manifest as T
from packages.orchestration.run_manifest import (
    MANIFEST_INDEX_FILENAME,
    ManifestError,
    build_verified_manifest_tree,
    canonical_index_bytes,
    decode_index_v1,
    load_index_verified,
    load_latest_manifest_verified,
    read_index,
    require_canonical_index_bytes,
    validate_index_and_tree,
    write_run_manifest,
)


@pytest.fixture
def ev(tmp_path):
    d = tmp_path / "ev"
    d.mkdir()
    write_run_manifest(d, dataclasses.replace(
        T._mk(episode_id="ep1", status="stopped"), stop_request_id="stop-ep1"),
        root=tmp_path)
    return d


def _stored(ev):
    return (ev / MANIFEST_INDEX_FILENAME).read_bytes()


def _decoded(ev):
    return decode_index_v1(_stored(ev))


# --------------------------------------------------------------------------- the writer


class TestWriterEmitsCanonicalIndex:
    def test_stored_index_is_exactly_its_canonical_encoding(self, ev):
        raw = _stored(ev)
        assert raw == canonical_index_bytes(decode_index_v1(raw))

    def test_a_second_episode_keeps_the_index_canonical(self, ev, tmp_path):
        import dataclasses
        write_run_manifest(ev, dataclasses.replace(
            T._mk(episode_id="ep2", status="stopped", calls=(T._call(run="r-ep2"),)),
            stop_request_id="stop-ep2", episode_ordinal=2, previous_episode_id="ep1",
            prior_episode_ids=("ep1",), created_at="2026-07-15T00:02:00+00:00"), root=tmp_path)
        raw = _stored(ev)
        assert raw == canonical_index_bytes(decode_index_v1(raw))


# --------------------------------------------------------------------------- the readers


class TestEveryReaderRequiresCanonicalIndexBytes:
    """The rule is applied at EVERY entry point — one permissive reader would be the hole."""

    def _tamper(self, ev, mutate):
        idx = json.loads(_stored(ev).decode())
        (ev / MANIFEST_INDEX_FILENAME).write_bytes(mutate(idx))

    def test_pretty_printed_index_is_rejected_by_load_index_verified(self, ev):
        # SAME decoded content, different bytes — a re-serialization by a well-meaning tool.
        self._tamper(ev, lambda i: json.dumps(i, indent=4).encode())
        with pytest.raises(ManifestError) as exc:
            load_index_verified(ev)
        assert "canonical" in str(exc.value)

    def test_pretty_printed_index_is_rejected_by_validate_index_and_tree(self, ev):
        self._tamper(ev, lambda i: json.dumps(i, indent=4).encode())
        assert validate_index_and_tree(ev, job_id="j") != []

    def test_pretty_printed_index_is_rejected_by_the_tree_builder(self, ev):
        self._tamper(ev, lambda i: json.dumps(i, indent=4).encode())
        _files, problems = build_verified_manifest_tree(ev, job_id="j")
        assert problems != []

    def test_pretty_printed_index_is_rejected_by_the_canonical_loader(self, ev):
        self._tamper(ev, lambda i: json.dumps(i, indent=4).encode())
        with pytest.raises(ManifestError):
            load_latest_manifest_verified(ev, job_id="j")

    def test_pretty_printed_index_is_rejected_by_the_cli_reader(self, ev):
        self._tamper(ev, lambda i: json.dumps(i, indent=4).encode())
        with pytest.raises(ManifestError):
            read_index(ev)

    def test_unknown_field_is_rejected_even_when_canonically_encoded(self, ev):
        def _add(i):
            i["EXTRA"] = "smuggled"
            return canonical_index_bytes(i)          # canonical bytes, unknown field
        self._tamper(ev, _add)
        with pytest.raises(ManifestError):
            load_index_verified(ev)

    def test_duplicate_keys_are_rejected(self, ev):
        raw = _stored(ev).decode().rstrip("\n")
        assert raw.endswith("}")
        dup = raw[:-1] + ',\n  "latest_episode_id": "evil"\n}\n'
        (ev / MANIFEST_INDEX_FILENAME).write_bytes(dup.encode())
        with pytest.raises(ManifestError):
            load_index_verified(ev)

    def test_key_reordering_is_rejected(self, ev):
        # canonical order is sorted; reversing it parses identically but is NOT canonical
        self._tamper(ev, lambda i: (json.dumps(dict(reversed(list(i.items()))), indent=2)
                                    + "\n").encode())
        with pytest.raises(ManifestError):
            load_index_verified(ev)

    def test_the_size_limit_applies_BEFORE_the_decode(self, ev):
        """An oversized index must be refused on its size, not parsed first — a reader that
        decodes 500 MB to decide it is too big is the denial-of-service."""
        from packages.orchestration import manifest_schema as _S
        (ev / MANIFEST_INDEX_FILENAME).write_bytes(
            b"[" + b"0," * _S.MAX_INDEX_BYTES + b"0]")
        with pytest.raises(ManifestError) as exc:
            load_index_verified(ev)
        assert "byte" in str(exc.value) or "large" in str(exc.value)

    def test_missing_index_is_missing_not_malformed(self, ev):
        """Absence is distinguishable from corruption: `read_index` returns the empty index."""
        (ev / MANIFEST_INDEX_FILENAME).unlink()
        assert read_index(ev)["episodes"] == []


# --------------------------------------------------------------------------- the primitive


class TestRequireCanonicalIndexBytes:
    def test_accepts_the_canonical_encoding(self):
        idx = {"index_v": 1, "episodes": [], "latest_episode_id": ""}
        require_canonical_index_bytes(canonical_index_bytes(idx), idx)

    def test_rejects_anything_else(self):
        idx = {"index_v": 1, "episodes": [], "latest_episode_id": ""}
        with pytest.raises(ManifestError):
            require_canonical_index_bytes(json.dumps(idx).encode(), idx)
