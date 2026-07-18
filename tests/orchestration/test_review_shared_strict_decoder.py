"""F5 (round 26) — ONE shared strict JSON decoder. Both packaging scripts import
packages.common.strict_json; neither carries its own object_pairs_hook copy."""
from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

from packages.common.strict_json import StrictJsonError, strict_loads


class TestSharedDecoder:
    def test_duplicate_key_any_depth_rejected(self):
        with pytest.raises(StrictJsonError):
            strict_loads(b'{"a":1,"a":2}')
        with pytest.raises(StrictJsonError):
            strict_loads(b'{"a":{"b":1,"b":2}}')

    def test_nan_infinity_rejected(self):
        for bad in (b'{"x": NaN}', b'{"x": Infinity}', b'{"x": -Infinity}'):
            with pytest.raises(StrictJsonError):
                strict_loads(bad)

    def test_invalid_utf8_rejected(self):
        with pytest.raises(StrictJsonError):
            strict_loads(b'{"x": "\xff\xfe"}')

    def test_require_object_rejects_non_object(self):
        with pytest.raises(StrictJsonError):
            strict_loads(b'[1, 2, 3]', require_object=True)

    def test_unique_keys_decode(self):
        assert strict_loads(b'{"a":1,"b":{"c":2}}') == {"a": 1, "b": {"c": 2}}


class TestSingleImplementation:
    def _src(self, name):
        return (REPO_ROOT / "scripts" / name).read_text()

    def test_scripts_import_the_shared_decoder(self):
        for name in ("build_review_manifest.py", "build_review_zip.py"):
            src = self._src(name)
            assert "from packages.common.strict_json import" in src, name

    def test_no_private_object_pairs_hook_copy_in_scripts(self):
        # The dependency-free duplicate-key hook lives ONLY in the shared module — the scripts must
        # not re-implement it.
        for name in ("build_review_manifest.py", "build_review_zip.py"):
            src = self._src(name)
            assert "object_pairs_hook" not in src, name
            assert "def _no_dup_pairs" not in src, name
