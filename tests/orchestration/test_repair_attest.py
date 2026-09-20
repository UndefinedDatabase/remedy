"""What stays of the operator repair attestation (F002 T001, F273 finding R-0914).

The writer that recorded a manual operator repair under a job's evidence directory is deleted, so
an operator repair is attested no longer. What survives is the final verifier's acceptance of an
operator-attested task, which the closure evidence producer relies on: its task artifacts are
written here through the surviving producer ``manual_attestation.write_manual_task_evidence``.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from packages.orchestration.manual_attestation import write_manual_task_evidence
from packages.orchestration.pingpong_job import parse_job_file
from packages.orchestration.repair_attest import (
    build_safe_diff_text,
    canonical_provenance_sha256,
    parse_safe_diff_paths,
    sha256_text,
)

_ONE_TASK_JOB = """\
# Job: Operator Repair Test

## Task 1
Fix the broken thing by hand.

Acceptance:
- thing works
"""


@pytest.fixture
def isolate_data_root(tmp_path: Path, monkeypatch):
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


@pytest.fixture
def git_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "main.py").write_text("def hello():\n    return 'hi'\n")

    def _git(*args):
        subprocess.run(["git", *args], cwd=str(repo), check=True,
                       capture_output=True, text=True)

    _git("init", "-q")
    _git("config", "user.email", "t@example.com")
    _git("config", "user.name", "Test")
    _git("add", "-A")
    _git("commit", "-q", "-m", "init")
    # Operator makes a manual repair after the last valid (committed) state.
    (repo / "main.py").write_text("def hello():\n    return 'fixed'\n")
    return repo


def _write_attested_task(evidence_dir: Path, job_id: str, task_id: str, repo: Path,
                         note: str) -> Path:
    """Write one operator-attested task through the surviving producer, hashing the tracked
    diff the way ``job_evidence.create_manual_completion_bundle`` does."""
    tracked = subprocess.run(["git", "diff", "HEAD"], cwd=str(repo), check=True,
                             capture_output=True, text=True).stdout
    safe = build_safe_diff_text(tracked, [])
    tsha, ssha = sha256_text(tracked), sha256_text(safe)
    prov = canonical_provenance_sha256(tsha, [])
    write_manual_task_evidence(
        str(evidence_dir), job_id=job_id, task_id=task_id,
        changed_files=parse_safe_diff_paths(safe), safe_diff_text=safe,
        provenance_sha256=prov, diff_sha256=prov, tracked_diff_sha256=tsha,
        safe_diff_sha256=ssha, timestamp="2026-09-19T00:00:00+00:00", note=note)
    return evidence_dir / "task_runs" / task_id


def test_no_f003_specific_path_in_production_code():
    """Finding 4: no `.agent/F003_*` path remains in generic production code."""
    import re
    prod_files = [
        "packages/orchestration/repair_attest.py",
        "packages/orchestration/job_evidence.py",
        "packages/orchestration/final_verifier.py",
        "packages/orchestration/pingpong_provider.py",
        "scripts/build_review_manifest.py",
    ]
    root = Path(__file__).resolve().parents[2]
    pat = re.compile(r"F003_[A-Za-z0-9_]*")
    for rel in prod_files:
        text = (root / rel).read_text(encoding="utf-8")
        assert not pat.search(text), f"{rel} references an F003-specific path/name"


# -- F002 T003: end-to-end — blocked task -> attested -> verifier PASS -------


def _seed_blocked_task_evidence(base: Path, task_id: str = "T001") -> None:
    """Seed one task's evidence complete except for a blocking review verdict.

    Everything a clean PASS needs is present, but the reviewer verdict is
    ``needs_repair`` with an open finding — so the final verifier is NOT PASS
    until an operator attestation replaces the reviewer verdict. The blocking
    finding lives in the review rounds only (no ``repair_loop`` open findings),
    since operator attestation is what supersedes that review path.
    """
    d = base / "task_runs" / task_id
    d.mkdir(parents=True, exist_ok=True)
    (d / "review_scope_packet.json").write_text(json.dumps({
        "changed_files": ["main.py"],
        "changed_line_ranges": {"main.py": [[1, 2]]},
    }))
    (d / "spec_compliance_check.json").write_text(json.dumps({"verdict": "PASS"}))
    (d / "missing_tests_gate.json").write_text(json.dumps({"gate_status": "PASS"}))
    (d / "review.json").write_text(json.dumps({
        "final_verdict": "needs_repair",
        "verdict": "needs_repair",
        "reviews": [{
            "round": 1,
            "findings": [{
                "id": "F1", "severity": "high", "file": "main.py",
                "summary": "returns the wrong value",
            }],
        }],
    }))
    (d / "repair_loop.json").write_text(json.dumps({"open_findings": []}))
    (d / "tests.txt").write_text("3 passed in 0.1s\n")
    (d / "safe.diff").write_text("--- a/main.py\n+++ b/main.py\n")
    (d / "token_accounting.json").write_text(json.dumps({
        "actual_tokens_available": False,
        "builder_prompt_tokens_estimated": 100,
        "reviewer_prompt_tokens_estimated": 200,
    }))
    (base / "scratch_file_guard.json").write_text(json.dumps({"guard_status": "PASS"}))
    (base / "token_truth.json").write_text(json.dumps({
        "schema_version": "1.0.0",
        "actual_available": False,
        "estimated_prompt_tokens": 300,
        "estimated_total_tokens": 300,
        "measurement_source": "character_heuristic",
        "measurement_confidence": "low",
        "missing_reason": "actual usage unavailable",
        "builder_estimated_total": 100,
        "reviewer_estimated_total": 200,
        "repair_estimated_total": 0,
        "provider_call_count": 2,
    }))
    (base / "execution_config.json").write_text(json.dumps({
        "builder_model": "opus", "builder_actual_model": "opus",
        "reviewer_model": "opus", "reviewer_actual_model": "opus",
        "repair_model": "opus", "repair_actual_model": "opus",
        "actual_config_available": True,
    }))


def test_e2e_blocked_job_attest_verifier_pass(isolate_data_root, git_repo):
    """A blocked task -> operator-attested task artifacts -> verifier PASS."""
    from packages.orchestration.data_paths import jobs_dir
    from packages.orchestration.final_verifier import build_final_verifier_report
    from packages.orchestration.token_truth import build_token_truth

    # 1. Fake blocked job with a failed/blocked task.
    job = parse_job_file(_ONE_TASK_JOB, str(git_repo))
    evidence_dir = jobs_dir() / job.job_id / "evidence"
    _seed_blocked_task_evidence(evidence_dir, "T001")

    # Precondition: the verifier is NOT PASS while the task is blocked.
    before = build_final_verifier_report(str(evidence_dir))
    assert before["verdict"] != "PASS"
    assert before["unresolved_findings"], "task should be blocked before attest"

    # 2. The operator-attested task artifacts replace the reviewer verdict.
    out_dir = _write_attested_task(evidence_dir, job.job_id, "T001", git_repo,
                                   "operator fixed by hand")

    # 3 + 4. Verifier now PASS-equivalent (PASS_WITH_RISKS: human final review
    # mandatory for a fully operator-attested completion) with the badge.
    report = build_final_verifier_report(str(evidence_dir))
    assert report["verdict"] == "PASS_WITH_RISKS"
    assert report["unresolved_findings"] == []
    assert report["operator_attested_tasks"] == ["T001"]
    assert "[OPERATOR ATTESTED]" in report["report_badges"]

    # 5. token_truth: the attested task has no actual provider usage.
    truth = build_token_truth(str(evidence_dir))
    assert truth["per_task"]["T001"]["actual_available"] is False
    assert truth["actual_available"] is False

    # 6. All four attestation artifacts are present and valid JSON.
    for name in (
        "provider_evidence.json",
        "review.json",
        "token_accounting.json",
        "manual_repair_provenance.json",
    ):
        path = out_dir / name
        assert path.exists(), f"missing {name}"
        assert isinstance(json.loads(path.read_text()), dict), f"invalid JSON: {name}"


class TestHunklessDiffEntriesAreVisible:
    """R-1010: an entry with no hunks has no ``+++`` line, and was therefore invisible.

    ``create_manual_completion_bundle`` puts every attestable changed path into a task's
    ``changed_files`` and then checks that ``parse_safe_diff_paths`` reads the same set back
    out of that task's safe diff. An ADDED EMPTY file makes those two disagree: git writes
    only ``diff --git``, ``new file mode`` and ``index`` for it, so the writer's own check
    raised and no review package could be built for any branch holding one. F276's closure
    met it when the operator merged main in with an empty ``__init__.py``.
    """

    ADDED_EMPTY = (
        "diff --git a/packages/providers/claude_planner/__init__.py "
        "b/packages/providers/claude_planner/__init__.py\n"
        "new file mode 100644\n"
        "index 00000000..e69de29b\n"
    )
    MODIFIED = (
        "diff --git a/pkg/a.py b/pkg/a.py\n"
        "index 1111111..2222222 100644\n"
        "--- a/pkg/a.py\n"
        "+++ b/pkg/a.py\n"
        "@@ -1 +1 @@\n-x\n+y\n"
    )
    DELETED = (
        "diff --git a/pkg/gone.py b/pkg/gone.py\n"
        "deleted file mode 100644\n"
        "index 3333333..0000000\n"
        "--- a/pkg/gone.py\n"
        "+++ /dev/null\n"
        "@@ -1 +0,0 @@\n-x\n"
    )
    DELETED_EMPTY = (
        "diff --git a/pkg/gone_empty.py b/pkg/gone_empty.py\n"
        "deleted file mode 100644\n"
        "index e69de29..0000000\n"
    )
    RENAMED = (
        "diff --git a/pkg/old.py b/pkg/new.py\n"
        "similarity index 100%\n"
        "rename from pkg/old.py\n"
        "rename to pkg/new.py\n"
    )

    def test_an_added_empty_file_is_named_by_its_header(self):
        assert parse_safe_diff_paths(self.ADDED_EMPTY) == [
            "packages/providers/claude_planner/__init__.py"]

    def test_a_pure_rename_is_named_by_its_destination(self):
        assert parse_safe_diff_paths(self.RENAMED) == ["pkg/new.py"]

    def test_an_added_empty_file_whose_path_holds_a_space_is_read_whole(self):
        text = ("diff --git a/pkg/with space.py b/pkg/with space.py\n"
                "new file mode 100644\n"
                "index 00000000..e69de29b\n")
        assert parse_safe_diff_paths(text) == ["pkg/with space.py"]

    def test_a_deleted_file_is_still_absent_whether_or_not_it_had_hunks(self):
        # It has no content at head, which is why `+++ /dev/null` is skipped and why
        # the bundle's attestable authority set already excludes it (R-0837).
        assert parse_safe_diff_paths(self.DELETED) == []
        assert parse_safe_diff_paths(self.DELETED_EMPTY) == []

    def test_an_ordinary_modified_file_reads_exactly_as_before(self):
        assert parse_safe_diff_paths(self.MODIFIED) == ["pkg/a.py"]

    def test_a_mixed_diff_names_every_path_that_exists_at_head(self):
        text = self.ADDED_EMPTY + self.MODIFIED + self.DELETED + self.RENAMED
        assert parse_safe_diff_paths(text) == [
            "packages/providers/claude_planner/__init__.py", "pkg/a.py", "pkg/new.py"]

    def test_the_writers_own_round_trip_holds_for_an_added_empty_file(self):
        # This is the exact equality `create_manual_completion_bundle` asserts per task.
        files = ["packages/providers/claude_planner/__init__.py", "pkg/a.py"]
        safe = build_safe_diff_text(self.ADDED_EMPTY + self.MODIFIED, [])
        assert parse_safe_diff_paths(safe) == sorted(files)
