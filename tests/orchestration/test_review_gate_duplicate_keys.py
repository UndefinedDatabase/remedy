"""F5 (round 25) — the staged gate loaders reject duplicate JSON keys at ANY depth. The stdlib
keeps the last of duplicate keys, so {"verdict":"BLOCKED","verdict":"PASS"} would decode to PASS and
two different byte strings would collapse to one object. The shared strict decoder refuses it.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
_b = importlib.util.spec_from_file_location(
    "_brm_dup", REPO_ROOT / "scripts" / "build_review_manifest.py")
_brm = importlib.util.module_from_spec(_b); _b.loader.exec_module(_brm)


class TestStrictDecoderRejectsDuplicates:
    def test_top_level_duplicate_raises(self):
        raw = b'{"schema_version":"1.0.0","verdict":"BLOCKED","verdict":"PASS"}'
        try:
            _brm._strict_json_loads(raw)
            assert False, "duplicate top-level key was accepted"
        except Exception:
            pass

    def test_nested_duplicate_raises(self):
        raw = (b'{"schema_version":"1.0.0","verdict":"PASS",'
               b'"evidence_validity":{"has_job_id":true,"has_job_id":false}}')
        try:
            _brm._strict_json_loads(raw)
            assert False, "duplicate nested key was accepted"
        except Exception:
            pass

    def test_unique_keys_decode(self):
        raw = b'{"a":1,"b":{"c":2,"d":3}}'
        assert _brm._strict_json_loads(raw) == {"a": 1, "b": {"c": 2, "d": 3}}


class TestGateMatrixBlocksDuplicateKeyedGate:
    def _view(self, dup_name, dup_bytes):
        good = {
            "final_verifier_report.json": b'{"schema_version":"1.0.0","verdict":"PASS"}',
        }

        def load(name):
            if name == dup_name:
                return _brm._strict_json_loads(dup_bytes)
            b = good.get(name)
            return _brm._strict_json_loads(b) if b is not None else None
        return load

    def test_duplicate_verdict_gate_blocks_the_matrix(self):
        loader = self._view("final_verifier_report.json",
                            b'{"schema_version":"1.0.0","verdict":"BLOCKED","verdict":"PASS"}')
        r = _brm.evaluate_ready_gate_matrix(loader)
        assert r["ok"] is False
        assert any("valid" in x.lower() or "duplicate" in x.lower()
                   for x in r["blocking_reasons"])
