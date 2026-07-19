"""F6 (round 31) — evaluate_ready_gate_matrix is a TOTAL function. Any missing / malformed / wrongly
typed gate input yields {ok: false, gate_verdicts, blocking_reasons} and NEVER raises; the
closed-schema pass completes before any semantic operation, so no set()/sorted()/membership/arith/.get
runs on an unvalidated value; one malformed gate does not hide the others."""
from __future__ import annotations

import copy
import importlib.util
import json
import os
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
_b = importlib.util.spec_from_file_location(
    "_brm_total", REPO_ROOT / "scripts" / "build_review_manifest.py")
_brm = importlib.util.module_from_spec(_b); _b.loader.exec_module(_brm)
_e = importlib.util.spec_from_file_location(
    "_e2e_total", REPO_ROOT / "tests" / "orchestration" / "test_review_authoritative_e2e.py")
_E2E = importlib.util.module_from_spec(_e); _e.loader.exec_module(_E2E)

_WRONG = [None, True, False, -1, 0, 1, 999, "", "0", "false", [], [1], {}, {"x": 1}]


def _kind(v):
    if v is None:
        return "none"
    if isinstance(v, bool):
        return "bool"
    if isinstance(v, int):
        return "int"
    if isinstance(v, float):
        return "float"
    if isinstance(v, str):
        return "str"
    if isinstance(v, list):
        return "list"
    if isinstance(v, dict):
        return "dict"
    return "other"


def _gates():
    return {k: copy.deepcopy(v) for k, v in _E2E._complete_gates().items()}


def _loader(gates):
    return lambda name: gates.get(name)


def _field_paths(obj, prefix=""):
    """Yield (top_gate_field_path) for every scalar/collection field, one level of nesting deep."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{prefix}.{k}" if prefix else k
            yield p
            if isinstance(v, dict) and prefix == "":       # one level of nesting only (bounded)
                yield from _field_paths(v, p)


def _set_path(d, path, val):
    segs = path.split(".")
    cur = d
    for s in segs[:-1]:
        cur = cur[s]
    cur[segs[-1]] = val


class TestGateMatrixIsTotal:
    def test_baseline_gates_pass(self):
        # Sanity: the unmutated complete gate set evaluates without raising and is ok.
        r = _brm.evaluate_ready_gate_matrix(_loader(_gates()))
        assert isinstance(r, dict) and set(r) == {"ok", "gate_verdicts", "blocking_reasons"}

    def test_recursive_matrix_never_throws(self):
        # TOTALITY: replacing every field (one level deep) in every gate with every applicable wrong
        # value returns a well-formed {ok, gate_verdicts, blocking_reasons} and NEVER raises.
        base = _gates()
        for gate_name, gate in base.items():
            for path in list(_field_paths(gate)):
                for val in _WRONG:
                    gates = _gates()
                    try:
                        _set_path(gates[gate_name], path, val)
                    except (KeyError, TypeError):
                        continue
                    try:
                        r = _brm.evaluate_ready_gate_matrix(_loader(gates))
                    except Exception as exc:               # pragma: no cover - the whole point
                        raise AssertionError(
                            f"{gate_name}.{path}={val!r} raised {type(exc).__name__}: {exc}")
                    assert set(r) == {"ok", "gate_verdicts", "blocking_reasons"}
                    assert isinstance(r["blocking_reasons"], list)

    def test_reviewer_malformed_examples_block_with_named_reason(self):
        # The reviewer's explicit malformed-value class must block, and the reason names the gate.
        cases = [
            ("fresh_evidence_gate.json", "schema_version", []),
            ("change_provenance_gate.json", "covered_files", True),
            ("change_provenance_gate.json", "source_files", 1),
            ("commit_execution_gate.json", "blocked_gates", {}),
            ("artifact_contract_gate.json", "required_artifacts", 1),
            ("final_verifier_report.json", "unresolved_findings", True),
        ]
        for gate_name, field, val in cases:
            gates = _gates()
            gates[gate_name][field] = val
            r = _brm.evaluate_ready_gate_matrix(_loader(gates))
            assert r["ok"] is False, f"{gate_name}.{field}={val!r} did not block"
            assert any(gate_name.replace(".json", "") in x or gate_name in x
                       for x in r["blocking_reasons"]), r["blocking_reasons"]

    def test_each_gate_replaced_by_wrong_root_type_never_throws(self):
        for gate_name in _gates():
            for val in _WRONG:
                gates = _gates()
                gates[gate_name] = val
                r = _brm.evaluate_ready_gate_matrix(_loader(gates))   # must not raise
                assert r["ok"] is False

    def test_loader_that_raises_is_recorded_not_propagated(self):
        gates = _gates()

        def bad_loader(name):
            if name == "final_verifier_report.json":
                raise ValueError("corrupt json")
            return gates.get(name)
        r = _brm.evaluate_ready_gate_matrix(bad_loader)
        assert r["ok"] is False
        assert any("not valid JSON" in x for x in r["blocking_reasons"])

    def test_one_malformed_gate_does_not_hide_another(self):
        gates = _gates()
        gates["fresh_evidence_gate.json"]["covered_files"] = True     # malformed (unknown/typed)
        gates["runtime_integration_gate.json"]["verdict"] = "BLOCKED"  # a distinct real failure
        r = _brm.evaluate_ready_gate_matrix(_loader(gates))
        assert r["ok"] is False
        # The runtime gate's failure is still reported despite the other malformed gate.
        assert any("runtime_integration_gate" in x for x in r["blocking_reasons"])

    def test_build_manifest_returns_valid_json_on_malformed_gate(self):
        # A malformed gate on disk must not throw through build_manifest; it returns a valid manifest.
        d = tempfile.mkdtemp()
        for name, body in _gates().items():
            body2 = copy.deepcopy(body)
            if name == "change_provenance_gate.json":
                body2["covered_files"] = True                # malformed
            with open(os.path.join(d, name), "w") as fh:
                json.dump(body2, fh)
        os.makedirs(os.path.join(d, "task_runs"), exist_ok=True)
        manifest = _brm.build_manifest(d)                    # must not raise
        assert isinstance(manifest, dict) and "ready_gate_matrix" in manifest
        assert manifest["ready_gate_matrix"]["ok"] is False
