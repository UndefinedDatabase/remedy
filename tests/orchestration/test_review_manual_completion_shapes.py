"""F2 (round 29) — manual-only Evidence is a trust boundary: every structured field consumed by
validate_manual_completion and its _verify_* helpers is validated BEFORE any iteration or .get chain.
A valid-JSON document with a wrong nested type appends a bounded ``artifact: field is not a <kind>``
error and invalidates the candidate — it never raises AttributeError/TypeError and never leaves READY
reachable. The mutation matrix replaces every consumed collection/record field with the applicable
wrong types and proves none throws.
"""
from __future__ import annotations

import copy
import importlib.util
import json
import os
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
_b = importlib.util.spec_from_file_location(
    "_brm_mc", REPO_ROOT / "scripts" / "build_review_manifest.py")
_brm = importlib.util.module_from_spec(_b); _b.loader.exec_module(_brm)


def _valid() -> dict:
    """A minimal manual-only completion bundle that triggers the manual-completion path and carries
    every consumed structured field with a correct type."""
    return {
        "manifest.json": {"job_id": "j1", "task_ids": ["T001"], "task_count": 1},
        "final_job_review.json": {
            "job_id": "j1", "completion_mode": "manual_operator_repair",
            "human_final_reviewer_required": True, "completion_provider_call_count": 0,
            "linked_prior_job_ids": ["prior1"],
            "linked_prior_job_summaries": [{"job_id": "prior1", "status": "ok",
                                            "provider_call_count": 0}],
            "per_task_changed_files": {"T001": ["src/a.py"]},
            "actual_changed_files": ["src/a.py"], "expected_changed_files": ["src/a.py"]},
        "current_change_content_proof.json": {
            "file_hashes": {"src/a.py": "0" * 64}, "tombstones": {},
            "base_commit": "a" * 40, "head_commit": "b" * 40},
        "final_verifier_report.json": {
            "authoritative_changed_files": ["src/a.py"],
            "test_status": {"ran": True, "passed": 1, "failed": 0},
            "review_subject_uncovered_files": [], "content_hash_mismatches": [],
            "file_set_alignment_status": "PASS"},
        "change_provenance_gate.json": {
            "covered_files": ["src/a.py"], "hash_mismatches": [], "uncovered_files": []},
        "verification_tests.json": {
            "schema_version": "1.0.0", "verification_type": "explicit_commands",
            "runs": [{"run_id": "vr-0001", "command": "pytest -q", "exit_code": 0, "passed": 1,
                      "failed": 0, "test_files": ["src/a.py"], "stdout_summary": "1 passed"}],
            "command": "pytest -q", "exit_code": 0, "passed": 1, "failed": 0,
            "test_files": ["src/a.py"], "timestamp": "2026-07-19T00:00:00Z"},
        "review_subject.json": {"subject_v": 1, "base_commit": "a" * 40, "head_commit": "b" * 40,
                                "commits": [], "files": []},
        "review_commit_chain.json": {"chain_v": 1, "base_commit": "a" * 40, "head_commit": "b" * 40,
                                     "commits": []},
        "task_runs/T001/manual_repair_provenance.json": {
            "manual_operator_repair": True, "no_provider_calls": True, "job_id": "j1",
            "task_id": "T001", "note": "x", "provenance_sha256": "0" * 64, "diff_sha256": "0" * 64,
            "tracked_diff_sha256": "0" * 64, "changed_files": ["src/a.py"],
            "task_scoped_files": ["src/a.py"], "untracked_file_hashes": []},
        "task_runs/T001/review.json": {"final_verdict": "operator_attested",
                                       "human_final_reviewer_required": True},
        "task_runs/T001/provider_evidence.json": {"execution_mode": "manual_operator_repair",
                                                  "provider_call_count": 0,
                                                  "completion_provider_call_count": 0,
                                                  "prompt_trace_available": False,
                                                  "actual_provider_available": False},
        "task_runs/T001/token_accounting.json": {"task_id": "T001", "kind": "manual",
                                                 "reason": "manual", "provider_call_count": 0,
                                                 "actual_available": False},
        "task_runs/T001/manifest.json": {"evidence_available": True,
                                         "effective_status": "operator_attested_complete"},
        "task_runs/T001/review_scope_packet.json": {"changed_files": ["src/a.py"]},
    }


def _view(objs: dict, extra_files: dict | None = None) -> "._brm._EvidenceView":  # type: ignore  # noqa: F722
    files = {rel: json.dumps(o).encode() for rel, o in objs.items()}
    files["task_runs/T001/safe.diff"] = b"--- a/src/a.py\n+++ b/src/a.py\n"
    for k, v in (extra_files or {}).items():
        files[k] = v
    return _brm._EvidenceView(files)


# Applicable WRONG-typed values per expected kind (right-typed shapes are excluded — they are not a
# type error). null is a present-but-wrong value for every collection kind.
_WRONG = {
    _brm._MC_LIST: [None, True, False, 0, 1, -1, "", "x", {}, {"x": 1}],
    _brm._MC_DICT: [None, True, False, 0, 1, -1, "", "x", [], [1]],
    _brm._MC_LISTDICT: [None, True, 0, "x", {}, {"x": 1}, [1], [1, {"ok": 1}]],
    _brm._MC_DICTLIST: [None, True, 0, "x", [], [1], {"k": 1}, {"k": "x"}],
}


def _cases():
    for rel, spec in _brm._MC_SHAPES.items():
        # map the basename spec onto the concrete fixture rel(s)
        concrete = [rel] if rel in _valid() else [f"task_runs/T001/{rel}"]
        for cr in concrete:
            if cr not in _valid():
                continue
            for field, kind in spec.items():
                for val in _WRONG[kind]:
                    yield cr, field, kind, val


class TestManualCompletionMutationMatrix:
    def test_manual_path_triggers_on_valid_fixture(self):
        assert _brm._is_manual_completion(_view(_valid())) is True

    def test_every_wrong_typed_field_is_a_controlled_error(self):
        for rel, field, kind, val in _cases():
            objs = copy.deepcopy(_valid())
            objs[rel][field] = val
            ev = _view(objs)
            try:
                vc = _brm.validate_evidence_candidate(ev)
                gm = _brm.evaluate_ready_gate_matrix(ev.gate_loader())
            except Exception as exc:                       # pragma: no cover - the whole point
                raise AssertionError(f"{rel}:{field}={val!r} raised {type(exc).__name__}: {exc}")
            assert vc["is_valid_current_run"] is False, f"{rel}:{field}={val!r} stayed valid"
            assert gm["ok"] is False, f"{rel}:{field}={val!r} left READY reachable"
            assert any(field in e and rel in e for e in vc["validation_errors"]), \
                f"{rel}:{field}={val!r} produced no error naming the artifact+field"

    def test_build_manifest_never_throws_on_malformed_manual_evidence(self):
        for rel, field, val in (
            ("manifest.json", "task_ids", 123),
            ("final_job_review.json", "linked_prior_job_ids", 123),
            ("current_change_content_proof.json", "file_hashes", [{"x": 1}]),
            ("task_runs/T001/manual_repair_provenance.json", "untracked_file_hashes", "x"),
            ("task_runs/T001/manual_repair_provenance.json", "changed_files", 123),
        ):
            objs = copy.deepcopy(_valid())
            objs[rel][field] = val
            d = tempfile.mkdtemp()
            for r, o in objs.items():
                p = os.path.join(d, r)
                os.makedirs(os.path.dirname(p), exist_ok=True)
                with open(p, "w") as fh:
                    json.dump(o, fh)
            with open(os.path.join(d, "task_runs/T001/safe.diff"), "w") as fh:
                fh.write("--- a/src/a.py\n+++ b/src/a.py\n")
            manifest = _brm.build_manifest(d)              # must NOT raise
            assert isinstance(manifest, dict) and "review_subject" in manifest
            assert _brm.validate_evidence_candidate(d)["is_valid_current_run"] is False


class TestManualCompletionScalarSemantics:
    """F3 (round 31) — scalar typing and cross-artifact binding: booleans-for-integers, wrong enums and
    mismatched counts/task-ids block, and none throws."""

    def _apply(self, rel, field, val):
        objs = copy.deepcopy(_valid())
        objs[rel][field] = val
        return _view(objs)

    def _invalid(self, rel, field, val):
        ev = self._apply(rel, field, val)
        vc = _brm.validate_evidence_candidate(ev)          # must not raise
        assert vc["is_valid_current_run"] is False, f"{rel}.{field}={val!r} stayed valid"
        return vc["validation_errors"]

    def test_task_count_boolean_blocks(self):
        assert any("task_count" in e for e in self._invalid("manifest.json", "task_count", False))

    def test_task_count_wrong_value_blocks(self):
        assert any("task_count" in e for e in self._invalid("manifest.json", "task_count", 999))

    def test_completion_provider_call_count_boolean_blocks(self):
        assert any("completion_provider_call_count" in e for e in
                   self._invalid("final_job_review.json", "completion_provider_call_count", False))

    def test_provider_call_count_boolean_blocks(self):
        assert any("provider_call_count" in e for e in self._invalid(
            "task_runs/T001/provider_evidence.json", "provider_call_count", False))

    def test_actual_provider_available_string_false_blocks(self):
        assert any("actual_provider_available" in e for e in self._invalid(
            "task_runs/T001/provider_evidence.json", "actual_provider_available", "false"))

    def test_prompt_trace_available_true_blocks(self):
        assert any("prompt_trace_available" in e for e in self._invalid(
            "task_runs/T001/provider_evidence.json", "prompt_trace_available", True))

    def test_token_accounting_call_count_boolean_blocks(self):
        assert any("token_accounting.provider_call_count" in e for e in self._invalid(
            "task_runs/T001/token_accounting.json", "provider_call_count", False))

    def test_token_accounting_kind_not_manual_blocks(self):
        assert any("token_accounting" in e for e in self._invalid(
            "task_runs/T001/token_accounting.json", "kind", "actual"))

    def test_no_scalar_mutation_throws(self):
        for rel, field in (("manifest.json", "task_count"),
                           ("final_job_review.json", "completion_provider_call_count"),
                           ("task_runs/T001/provider_evidence.json", "provider_call_count"),
                           ("task_runs/T001/provider_evidence.json", "actual_provider_available"),
                           ("task_runs/T001/provider_evidence.json", "prompt_trace_available"),
                           ("task_runs/T001/token_accounting.json", "provider_call_count")):
            for val in (None, True, False, -1, 0, 1, 999, "", "0", "false", [], [1], {}, {"x": 1}):
                ev = self._apply(rel, field, val)
                _brm.validate_evidence_candidate(ev)       # must not raise


class TestLinkedPriorAndProductionIntegration:
    """F3 (round 32) — the exact linked-prior string-count reproduction blocks, and the canonical
    manual producer has a real (non-test) production caller."""

    def test_linked_prior_string_count_blocks(self):
        objs = copy.deepcopy(_valid())
        objs["final_job_review.json"]["linked_prior_job_summaries"] = [
            {"job_id": "prior1", "status": "ok", "provider_call_count": "0"}]
        objs["final_job_review.json"]["linked_prior_job_ids"] = ["prior1"]
        vc = _brm.validate_evidence_candidate(_view(objs))
        assert vc["is_valid_current_run"] is False
        assert any("provider_call_count is not an integer" in e for e in vc["validation_errors"])

    def test_linked_prior_boolean_count_blocks(self):
        objs = copy.deepcopy(_valid())
        objs["final_job_review.json"]["linked_prior_job_summaries"] = [
            {"job_id": "prior1", "status": "ok", "provider_call_count": True}]
        objs["final_job_review.json"]["linked_prior_job_ids"] = ["prior1"]
        assert _brm.validate_evidence_candidate(_view(objs))["is_valid_current_run"] is False

    def test_linked_prior_null_count_is_allowed(self):
        objs = copy.deepcopy(_valid())
        objs["final_job_review.json"]["linked_prior_job_summaries"] = [
            {"job_id": "prior1", "status": "ok", "provider_call_count": None}]
        objs["final_job_review.json"]["linked_prior_job_ids"] = ["prior1"]
        errs = _brm.validate_evidence_candidate(_view(objs))["validation_errors"]
        assert not any("provider_call_count is not an integer" in e for e in errs)

    def test_write_manual_completion_evidence_has_a_real_production_caller(self):
        # F4 (round 33): a NON-TEST module reaches the canonical producer, verified by repo search
        # (not by inspecting the producer's own source). The execution proof is the e2e test below.
        import subprocess
        out = subprocess.run(
            ["grep", "-rl", "--include=*.py", "write_manual_completion_evidence(",
             str(REPO_ROOT / "packages"), str(REPO_ROOT / "scripts")],
            capture_output=True, text=True).stdout.split()
        # A non-test production file both defines and calls the canonical producer.
        prod = [p for p in out if "/tests/" not in p.replace(os.sep, "/")
                and not p.rsplit("/", 1)[-1].startswith("test_")]
        assert any(p.endswith("job_evidence.py") for p in prod), out
        import inspect

        from packages.orchestration.job_evidence import create_manual_completion_bundle
        assert "write_manual_completion_evidence(" in inspect.getsource(
            create_manual_completion_bundle)


def _init_repo(root: Path) -> None:
    import subprocess
    root.mkdir(parents=True, exist_ok=True)
    for args in (["git", "init", "-q"], ["git", "config", "user.email", "op@remedy"],
                 ["git", "config", "user.name", "operator"]):
        subprocess.run(args, cwd=root, check=True, capture_output=True)


def _commit(root: Path, rel: str, text: str, msg: str) -> None:
    import subprocess
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=root, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-qm", msg], cwd=root, check=True, capture_output=True)


def _rev(root: Path, ref: str = "HEAD") -> str:
    import subprocess
    return subprocess.run(["git", "rev-parse", ref], cwd=root, check=True,
                          capture_output=True, text=True).stdout.strip()


class TestManualCompletionRunsEndToEnd:
    """F4 (round 33) — the canonical manual producer is exercised END-TO-END by its real operator
    entry ``job_evidence.create_manual_completion_bundle`` in a temporary repository, and the produced
    bundle passes the coordinator's own READY evaluation: manual-completion clean, final-verifier
    reproducible (VERIFIED_EQUAL), token-truth authority VERIFIED_EQUAL, gate matrix ok."""

    def _make_repo(self, tmp_path):
        repo = tmp_path / "repo"
        _init_repo(repo)
        # Base: four source/test files under a couple of packages.
        _commit(repo, "src_pkg/alpha.py", "def a():\n    return 1\n", "base alpha")
        _commit(repo, "src_pkg/beta.py", "def b():\n    return 2\n", "base beta")
        _commit(repo, "tests_pkg/test_alpha.py", "def test_a():\n    assert True\n", "base ta")
        _commit(repo, "tests_pkg/test_beta.py", "def test_b():\n    assert True\n", "base tb")
        base = _rev(repo)
        # Head: several commits that change every one of those source files.
        _commit(repo, "src_pkg/alpha.py", "def a():\n    return 10\n", "work alpha")
        _commit(repo, "src_pkg/beta.py", "def b():\n    return 20\n", "work beta")
        _commit(repo, "tests_pkg/test_alpha.py",
                "def test_a():\n    assert a_result() == 10\n", "work ta")
        _commit(repo, "tests_pkg/test_beta.py",
                "def test_b():\n    assert b_result() == 20\n", "work tb")
        head = _rev(repo)
        return repo, base, head

    def _bundle(self, evd, repo, base, head):
        from packages.orchestration.job_evidence import create_manual_completion_bundle
        runs = [{"run_id": "vr-0001", "command": "pytest -q tests_pkg", "exit_code": 0,
                 "passed": 2, "failed": 0, "test_files": ["tests_pkg/test_alpha.py",
                 "tests_pkg/test_beta.py"], "stdout_summary": "2 passed"}]
        return create_manual_completion_bundle(
            str(evd), repo_root=str(repo), base_commit=base, head_commit=head,
            job_id="e2ef4bundle0001", job_title="F4 manual e2e", step_range="1-2",
            prior_job_ids=["priore2ef4000001"], verification_runs=runs,
            timestamp="2026-07-19T00:00:00+00:00",
            generated_at="2026-07-19T00:00:00.000000+00:00", num_tasks=2,
            note_prefix="F4 manual e2e")

    def test_end_to_end_bundle_is_ready(self, tmp_path, monkeypatch):
        repo, base, head = self._make_repo(tmp_path)
        evd = tmp_path / "evidence"
        summary = self._bundle(evd, repo, base, head)
        # The coordinator recomputes the commit chain against the packaged repository (CWD).
        monkeypatch.chdir(repo)

        # The canonical producer actually ran: task attestation + regenerated root token truth exist.
        assert (evd / "token_truth.json").is_file()
        assert (evd / "task_runs" / "T001" / "manual_repair_provenance.json").is_file()
        assert (evd / "task_runs" / "T002" / "provider_evidence.json").is_file()

        # The root token truth is the canonical zero-provider manual truth and validates clean.
        from packages.orchestration.token_authority import validate_token_truth
        tt = json.loads((evd / "token_truth.json").read_text(encoding="utf-8"))
        assert validate_token_truth(tt) == []
        assert tt["measurement_source"] == "character_heuristic"
        assert tt["provider_call_count"] == 0

        # The coordinator's own READY evaluation over the produced bytes.
        ev = _brm._view_from_dir(str(evd))
        gm = _brm.evaluate_ready_gate_matrix(ev.gate_loader())
        assert gm["ok"] is True, gm["blocking_reasons"]
        assert _brm.validate_manual_completion(ev) == []
        assert _brm.validate_evidence_candidate(ev)["is_valid_current_run"] is True
        assert _brm._final_verifier_reproducibility(ev)["status"] == "VERIFIED_EQUAL"
        assert _brm._token_truth_authority(ev)["status"] == "VERIFIED_EQUAL"

        assert summary["manual_completion"] is True
        assert summary["verdict"] == "PASS_WITH_RISKS"
        assert sorted(summary["operator_attested_tasks"]) == ["T001", "T002"]

    def test_producer_is_reproducible(self, tmp_path):
        # The same repo bundled twice yields byte-identical final verifier + token truth.
        repo, base, head = self._make_repo(tmp_path)
        evd1, evd2 = tmp_path / "e1", tmp_path / "e2"
        self._bundle(evd1, repo, base, head)
        self._bundle(evd2, repo, base, head)
        for name in ("final_verifier_report.json", "token_truth.json"):
            assert (evd1 / name).read_text() == (evd2 / name).read_text(), name


class TestMixedCompletionIdentityBlocks:
    """Round 40 F1: a bundle with ANY manual claim that does NOT satisfy the full manual-completion
    contract blocks with a mixed-identity error. This prevents masquerading."""

    def test_pe_manual_but_fjr_not_manual_blocks(self):
        objs = copy.deepcopy(_valid())
        objs["final_job_review.json"]["completion_mode"] = "provider_backed"
        ev = _view(objs)
        assert _brm._has_any_manual_claim(ev) is True
        assert _brm._is_manual_completion(ev) is False
        vc = _brm.validate_evidence_candidate(ev)
        assert vc["is_valid_current_run"] is False
        assert any("mixed completion identity" in e for e in vc["validation_errors"])

    def test_task_manifest_manual_but_fjr_not_manual_blocks(self):
        objs = copy.deepcopy(_valid())
        objs["final_job_review.json"]["completion_mode"] = "provider_backed"
        objs["task_runs/T001/provider_evidence.json"]["execution_mode"] = "provider_backed"
        ev = _view(objs)
        assert _brm._has_any_manual_claim(ev) is True
        assert _brm._is_manual_completion(ev) is False
        vc = _brm.validate_evidence_candidate(ev)
        assert vc["is_valid_current_run"] is False
        assert any("mixed completion identity" in e for e in vc["validation_errors"])

    def test_fvr_manual_but_fjr_not_manual_blocks(self):
        objs = copy.deepcopy(_valid())
        objs["final_job_review.json"]["completion_mode"] = "provider_backed"
        objs["task_runs/T001/provider_evidence.json"]["execution_mode"] = "provider_backed"
        objs["task_runs/T001/manifest.json"]["effective_status"] = "complete"
        objs["task_runs/T001/manifest.json"]["completion_mode"] = "provider_backed"
        objs["final_verifier_report.json"]["manual_completion"] = True
        ev = _view(objs)
        assert _brm._has_any_manual_claim(ev) is True
        assert _brm._is_manual_completion(ev) is False
        vc = _brm.validate_evidence_candidate(ev)
        assert vc["is_valid_current_run"] is False
        assert any("mixed completion identity" in e for e in vc["validation_errors"])

    def test_execution_config_operator_but_fjr_not_manual_blocks(self):
        objs = copy.deepcopy(_valid())
        objs["final_job_review.json"]["completion_mode"] = "provider_backed"
        objs["task_runs/T001/provider_evidence.json"]["execution_mode"] = "provider_backed"
        objs["task_runs/T001/manifest.json"]["effective_status"] = "complete"
        objs["task_runs/T001/manifest.json"]["completion_mode"] = "provider_backed"
        objs["execution_config.json"] = {"builder_model": "operator", "reviewer_model": "operator"}
        ev = _view(objs)
        assert _brm._has_any_manual_claim(ev) is True
        assert _brm._is_manual_completion(ev) is False
        vc = _brm.validate_evidence_candidate(ev)
        assert vc["is_valid_current_run"] is False
        assert any("mixed completion identity" in e for e in vc["validation_errors"])

    def test_fully_consistent_manual_bundle_has_no_mixed_identity_error(self):
        ev = _view(_valid())
        assert _brm._has_any_manual_claim(ev) is True
        assert _brm._is_manual_completion(ev) is True
        vc = _brm.validate_evidence_candidate(ev)
        assert not any("mixed completion identity" in e for e in vc["validation_errors"])
