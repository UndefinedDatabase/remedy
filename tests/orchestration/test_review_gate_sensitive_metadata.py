"""F5 (round 24) — no trusted gate may carry a secret, a local absolute path, or a control
character in ANY textual field. The shared secret/path scanners are applied recursively to every
string value of every READY gate before the ZIP is built, so an unknown-but-allowed metadata field
cannot smuggle a credential, an operator's home path, or a terminal escape into the package.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
_b = importlib.util.spec_from_file_location(
    "_brm_meta", REPO_ROOT / "scripts" / "build_review_manifest.py")
_brm = importlib.util.module_from_spec(_b); _b.loader.exec_module(_brm)
_e = importlib.util.spec_from_file_location(
    "_e2e_meta", REPO_ROOT / "tests" / "orchestration" / "test_review_authoritative_e2e.py")
_E2E = importlib.util.module_from_spec(_e); _e.loader.exec_module(_E2E)


def _gates():
    return {k: dict(v) for k, v in _E2E._complete_gates().items()}


def _ok_with(fname, field, value):
    g = _gates()
    g[fname] = {**g[fname], field: value}
    return _brm.evaluate_ready_gate_matrix(lambda name: g.get(name))["ok"]


UNIX_HOME = "/home/alice/SUPERSECRET"
TMP_TOKEN = "/tmp/private-token"
WIN_HOME = "C:\\Users\\alice\\secret.txt"
PEM = "-----BEGIN RSA PRIVATE KEY-----"
CRED = "aws_secret_access_key=AKIAIOSFODNN7EXAMPLE"
CTRL = "value\x07with\x00control"


class TestSecretsAndPathsBlock:
    def test_unix_home_path_in_issue_blocks(self):
        assert _ok_with("change_provenance_gate.json", "issues", [UNIX_HOME]) is False

    def test_tmp_token_path_blocks(self):
        assert _ok_with("fresh_evidence_gate.json", "issues", [TMP_TOKEN]) is False

    def test_windows_home_path_blocks(self):
        assert _ok_with("artifact_contract_gate.json", "issues", [WIN_HOME]) is False

    def test_pem_marker_blocks(self):
        assert _ok_with("runtime_integration_gate.json", "issues", [PEM]) is False

    def test_credential_key_blocks(self):
        assert _ok_with("commit_execution_gate.json", "issues", [CRED]) is False

    def test_control_character_blocks(self):
        assert _ok_with("fresh_evidence_gate.json", "issues", [CTRL]) is False

    def test_secret_nested_deep_blocks(self):
        # A secret buried inside a nested object/list is still scanned.
        g = _gates()
        g["final_verifier_report.json"] = {
            **g["final_verifier_report.json"],
            "token_measurement_note": PEM}
        assert _brm.evaluate_ready_gate_matrix(lambda n: g.get(n))["ok"] is False


def test_clean_metadata_still_passes():
    # Relative paths and ordinary text are NOT flagged.
    g = _gates()
    g["change_provenance_gate.json"] = {**g["change_provenance_gate.json"],
                                        "issues": []}
    g["runtime_integration_gate.json"]["checks"][0]["source_file"] = "scripts/app.py"
    assert _brm.evaluate_ready_gate_matrix(lambda n: g.get(n))["ok"] is True
