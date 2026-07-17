"""F11 — ONE uniform size-limit contract: the writer never creates what the exporter refuses."""
from __future__ import annotations

import dataclasses

import pytest

import tests.orchestration.test_run_manifest as T
from packages.orchestration import manifest_schema as S
from packages.orchestration.run_manifest import (
    ManifestError,
    build_verified_manifest_tree,
    decode_run_manifest_v1,
    validate_run_manifest,
    write_run_manifest,
)


def _call_with_options(nbytes):
    """A call whose prepared_input options blob is ~nbytes (fingerprint stays bound)."""
    from packages.orchestration.call_identity import prepare_call_input
    prepared = prepare_call_input(prompt="p", model="fake", mode="fake",
                                  options={"pad": "x" * nbytes})
    pi = prepared.to_json()
    pi["pad"] = "x" * nbytes                 # unknown key → rejected by the decoder, so instead
    pi.pop("pad")
    return dataclasses.replace(T._call(), fingerprint=prepared.fingerprint,
                               prepared_input=pi)


class TestExportAndWriterAgree:
    def test_export_ceilings_are_the_shared_limits(self):
        from packages.orchestration import run_manifest as RM
        # F11: the export ceilings are not a second contract — they ARE the shared limits.
        assert RM.MANIFEST_MAX_FILE_BYTES == S.MAX_EPISODE_MANIFEST_BYTES
        assert RM.MANIFEST_MAX_TREE_BYTES == S.MAX_TREE_BYTES

    def test_a_written_record_is_always_exportable(self, tmp_path):
        ev = tmp_path / "ev"
        ev.mkdir()
        write_run_manifest(ev, T._mk(episode_id="ep1"), root=ev)
        files, problems = build_verified_manifest_tree(ev, job_id="j")
        assert problems == [], "the writer produced a record the exporter refuses"
        assert files


class TestPreparedInputBound:
    def test_oversized_prepared_input_is_rejected_before_write(self, tmp_path):
        big = dict(T._call().prepared_input)
        big["model"] = "m" * (S.MAX_PREPARED_INPUT_BYTES + 10)
        m = dataclasses.replace(T._mk(episode_id="ep1"),
                                calls=(dataclasses.replace(T._call(), prepared_input=big),))
        assert validate_run_manifest(m, published=False), "oversized prepared_input accepted"
        ev = tmp_path / "ev"
        ev.mkdir()
        with pytest.raises(ManifestError):
            write_run_manifest(ev, m, root=ev)


class TestDecoderBounds:
    def test_oversized_manifest_bytes_are_refused_before_parsing(self):
        with pytest.raises(ManifestError):
            decode_run_manifest_v1(b"x" * (S.MAX_EPISODE_MANIFEST_BYTES + 1))

    def test_limit_minus_one_is_accepted_by_the_byte_bound(self):
        # exactly at/below the limit the bound itself does not object (content still decides)
        S.bounded_bytes(b"x" * (S.MAX_INDEX_BYTES - 1), S.MAX_INDEX_BYTES, "index")
        S.bounded_bytes(b"x" * S.MAX_INDEX_BYTES, S.MAX_INDEX_BYTES, "index")
        with pytest.raises(S.SchemaError):
            S.bounded_bytes(b"x" * (S.MAX_INDEX_BYTES + 1), S.MAX_INDEX_BYTES, "index")

    def test_too_many_list_entries_are_refused(self):
        with pytest.raises(S.SchemaError):
            S.req_list({"a": list(range(S.MAX_EPISODES + 1))}, "a", "x",
                       max_len=S.MAX_EPISODES)

    def test_deep_string_is_bounded(self):
        with pytest.raises(S.SchemaError):
            S.req_str({"a": "x" * (S.MAX_SHORT_TEXT + 1)}, "a", "x")
