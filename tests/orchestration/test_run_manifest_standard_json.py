"""F9 (round 9) — STANDARD JSON only, in both directions.

`NaN`, `Infinity` and `-Infinity` are Python extensions, not JSON: Python emits them as bare
words that a conforming parser rejects. A record carrying one is unreadable by anyone else — and
a non-finite float has no business in an input identity or a hash. So Remedy neither writes them
nor accepts them, and invalid UTF-8 surfaces as a bounded `ManifestError` rather than a raw
`UnicodeDecodeError` escaping to the caller.
"""
from __future__ import annotations

import json
import math

import pytest

import packages.common.secure_fs as _fs
import tests.orchestration.test_run_manifest as T
from packages.orchestration import manifest_schema as _S
from packages.orchestration.run_manifest import (
    MANIFEST_FILENAME,
    MANIFEST_INDEX_FILENAME,
    MANIFESTS_SUBDIR,
    ManifestError,
    decode_index_v1,
    decode_run_manifest_v1,
    load_index_verified,
    load_latest_manifest_verified,
    read_run_manifest,
    strict_json_loads,
    write_run_manifest,
)

# --------------------------------------------------------------------------- writing


class TestTheSerializerRefusesNonStandardJson:
    @pytest.mark.parametrize("bad", [float("nan"), float("inf"), float("-inf")])
    def test_non_finite_floats_are_refused_at_serialization(self, bad):
        """`json.dumps` would happily emit `NaN` — a bare word no conforming reader accepts."""
        with pytest.raises(ValueError):
            _fs.json_bytes({"x": bad})

    def test_a_nested_non_finite_float_is_refused(self):
        with pytest.raises(ValueError):
            _fs.json_bytes({"a": {"b": [1, float("inf")]}})

    def test_ordinary_payloads_still_serialize(self):
        raw = _fs.json_bytes({"b": 1, "a": 2.5})
        assert json.loads(raw) == {"b": 1, "a": 2.5}
        assert raw.endswith(b"\n")


# --------------------------------------------------------------------------- reading


class TestTheStrictParserRefusesNonStandardJson:
    @pytest.mark.parametrize("word", ["NaN", "Infinity", "-Infinity"])
    def test_the_json_constants_are_rejected(self, word):
        with pytest.raises((ManifestError, _S.SchemaError)):
            strict_json_loads(('{"x": ' + word + '}').encode())

    def test_plain_json_loads_would_have_accepted_them(self):
        """Proof the guard is doing real work: the stdlib default accepts what we refuse."""
        assert math.isnan(json.loads('{"x": NaN}')["x"])

    def test_duplicate_keys_are_still_rejected(self):
        with pytest.raises((ManifestError, _S.SchemaError)):
            strict_json_loads(b'{"x": 1, "x": 2}')

    def test_invalid_utf8_is_a_bounded_manifest_error(self):
        """A raw UnicodeDecodeError escaping the decoder is a crash, not a verdict."""
        with pytest.raises(ManifestError) as exc:
            strict_json_loads(b'{"x": "\xff\xfe"}')
        assert "UTF-8" in str(exc.value)

    def test_ordinary_json_still_parses(self):
        assert strict_json_loads(b'{"x": [1, 2.5, null, true]}') == {"x": [1, 2.5, None, True]}


# --------------------------------------------------------------------------- on disk


class TestStoredRecordsWithNonStandardJsonAreRejected:
    @pytest.fixture
    def ev(self, tmp_path):
        d = tmp_path / "ev"
        d.mkdir()
        write_run_manifest(d, T._mk(episode_id="ep1"), root=tmp_path)
        return d

    def _poison(self, path, word="Infinity"):
        raw = path.read_text().rstrip("\n")
        assert raw.endswith("}")
        path.write_text(raw[:-1] + f',\n  "poison": {word}\n}}\n')

    def test_a_poisoned_episode_record_is_rejected(self, ev):
        self._poison(ev / MANIFESTS_SUBDIR / "ep1" / MANIFEST_FILENAME)
        with pytest.raises(ManifestError):
            read_run_manifest(ev / MANIFESTS_SUBDIR / "ep1" / MANIFEST_FILENAME)

    def test_a_poisoned_mirror_is_rejected_by_the_canonical_loader(self, ev):
        self._poison(ev / MANIFEST_FILENAME)
        with pytest.raises(ManifestError):
            load_latest_manifest_verified(ev, job_id="j")

    def test_a_poisoned_index_is_rejected(self, ev):
        self._poison(ev / MANIFEST_INDEX_FILENAME)
        with pytest.raises(ManifestError):
            load_index_verified(ev)

    def test_invalid_utf8_on_disk_is_a_manifest_error(self, ev):
        (ev / MANIFEST_FILENAME).write_bytes(b'{"job_id": "\xff"}')
        with pytest.raises(ManifestError):
            load_latest_manifest_verified(ev, job_id="j")

    def test_decoders_report_manifest_errors_not_raw_parser_errors(self):
        for decode, arg in ((decode_run_manifest_v1, b'{"job_id": NaN}'),
                            (decode_index_v1, b'{"index_v": Infinity}')):
            with pytest.raises((ManifestError, _S.SchemaError)):
                decode(arg)


# --------------------------------------------------------------------------- end to end


class TestRealRunsEmitStandardJson:
    def test_every_stored_manifest_byte_parses_under_a_strict_conforming_reader(
            self, data_root, repo):
        """A conforming reader with NO Python extensions enabled must read everything Remedy
        published — that is what "standard JSON" means operationally."""
        from packages.orchestration.pingpong_job import job_evidence_dir

        job_id, _res = T._run(T._JOB, repo)
        ev = job_evidence_dir(job_id)
        seen = 0
        for path in sorted(ev.rglob("*.json")):
            raw = path.read_bytes()
            json.loads(raw.decode("utf-8"),
                       parse_constant=lambda w: pytest.fail(f"{path} carries {w}"))
            seen += 1
        assert seen >= 3          # mirror + index + at least one episode record


data_root = T.data_root
repo = T.repo
