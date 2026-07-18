"""F3 (round 25) — the metadata scanner walks dictionary KEYS as well as values, and every dynamic
map key must satisfy its typed grammar. A file-hash map keyed by /home/alice/SUPERSECRET, or a
task-map keyed by an out-of-grammar id, blocks before any ZIP is produced.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
_b = importlib.util.spec_from_file_location(
    "_brm_key", REPO_ROOT / "scripts" / "build_review_manifest.py")
_brm = importlib.util.module_from_spec(_b); _b.loader.exec_module(_brm)
_e = importlib.util.spec_from_file_location(
    "_e2e_key", REPO_ROOT / "tests" / "orchestration" / "test_review_authoritative_e2e.py")
_E2E = importlib.util.module_from_spec(_e); _e.loader.exec_module(_E2E)


def _gates():
    return {k: dict(v) for k, v in _E2E._complete_gates().items()}


def _ok(g):
    return _brm.evaluate_ready_gate_matrix(lambda name: g.get(name))["ok"]


def _hash_key(key):
    g = _gates()
    cp = dict(g["change_provenance_gate.json"])
    cp["current_hashes"] = {key: "0" * 64}
    cp["evidence_hashes"] = {key: "0" * 64}
    cp["covered_files"] = [key]
    cp["source_files"] = [key]
    cp["evidence_covered_files"] = [key]
    g["change_provenance_gate.json"] = cp
    return g


UNSAFE_KEYS = [
    "/home/alice/SUPERSECRET",
    "/tmp/private-token",
    "C:\\Users\\alice\\secret",
    "aws_secret_access_key",
    "-----BEGIN PRIVATE KEY-----",
    "col\x00umn",
    "ctrl\x07char",
]


class TestUnsafeMapKeysBlock:
    def test_each_unsafe_hash_key_blocks(self):
        for k in UNSAFE_KEYS:
            assert _ok(_hash_key(k)) is False, k


class TestDynamicKeyGrammar:
    def test_artifact_name_key_with_traversal_blocks(self):
        g = _gates()
        g["artifact_contract_gate.json"]["required_artifacts"] = {"../escape.json": True}
        assert _ok(g) is False

    def test_task_map_bad_grammar_blocks(self):
        g = _gates()
        g["final_verifier_report.json"]["sticky_binding_by_task"] = {"not-a-task": True}
        assert _ok(g) is False

    def test_overlong_key_blocks(self):
        g = _hash_key("a/" + "x" * 400)
        assert _ok(g) is False


def test_clean_keys_still_pass():
    assert _ok(_gates()) is True
