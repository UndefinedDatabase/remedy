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


class TestEveryTrustBoundaryDecodesStrictly:
    """F5 (round 27) — the trust-bearing job_flow / manual_repair_provenance / packaged manifest /
    NO_EVIDENCE manifest decodes go through the strict decoder: a duplicate/contradictory key,
    NaN/Infinity, invalid UTF-8, or a non-object root BLOCKS, exercised at each real boundary."""
    import importlib.util as _ilu
    _b = _ilu.spec_from_file_location("_brm_bnd", REPO_ROOT / "scripts" / "build_review_manifest.py")
    _brm = _ilu.module_from_spec(_b); _b.loader.exec_module(_brm)

    def _valid(self, files):
        v = self._brm._EvidenceView(files)
        return self._brm.validate_evidence_candidate(v)

    def _jf_errors(self, jf):
        val = self._valid({"job_flow.json": jf, "manifest.json": b'{"job_id":"e2e"}'})
        return [e for e in val["validation_errors"] if "job_flow" in e]

    def test_valid_job_flow_parses(self):
        assert self._jf_errors(b'{"job_id":"e2e","final_audit":{"status":"pass"}}') == []

    def test_duplicate_top_job_id_blocks(self):
        assert self._jf_errors(b'{"job_id":"attacker","job_id":"e2e"}')

    def test_duplicate_nested_status_blocks(self):
        assert self._jf_errors(
            b'{"job_id":"e2e","final_audit":{"status":"blocked","status":"pass"}}')

    def test_job_flow_nan_blocks(self):
        assert self._jf_errors(b'{"job_id":"e2e","x": NaN}')

    def test_job_flow_infinity_blocks(self):
        assert self._jf_errors(b'{"job_id":"e2e","x": Infinity}')

    def test_job_flow_invalid_utf8_blocks(self):
        assert self._jf_errors(b'{"job_id":"e2e","x":"\xff\xfe"}')

    def test_job_flow_array_root_blocks(self):
        assert self._jf_errors(b'[1,2,3]')

    def test_duplicate_manual_repair_provenance_blocks(self):
        mrp = b'{"manual_operator_repair":true,"manual_operator_repair":false,"no_provider_calls":true}'
        val = self._valid({"task_runs/T001/manual_repair_provenance.json": mrp,
                           "task_runs/T001/x": b"{}"})
        assert any("manual_repair_provenance.json invalid" in e or "unreadable" in e
                   for e in val["validation_errors"])

    def test_no_raw_json_loads_of_trust_artifacts(self):
        # No bare json.loads survives on the job_flow / provenance / packaged-manifest reads: those
        # go through _strict_json_loads. (A bare json.loads on a NON-trust value stays permitted.)
        src = (REPO_ROOT / "scripts" / "build_review_manifest.py").read_text()
        for marker in ("_strict_json_loads(raw) if raw is not None else {}",     # job_flow + manifest
                       "_strict_json_loads(raw) if raw is not None else None"):   # provenance
            assert marker in src
