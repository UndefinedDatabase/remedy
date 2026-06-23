"""Job Fulfillment Spine v0 — orchestrate a complete job lifecycle.

Job -> Tasks -> Worker -> Review -> Repair -> Approval -> Apply -> Test -> Proof
-> Final Review -> completed_verified -> Next Suggestions.

v0 supports fixture-demo mode only (deterministic, no real provider).
All repo writes go through existing patch_apply.apply_patch_intent.
Tests go through existing test_execution_service.execute_test_run.
Proof goes through existing proof_chain.build_proof_chain.
Completion decided by JobFulfillmentContract.check().
"""
from __future__ import annotations

import json
import shutil as _shutil
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Any
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from packages.core.models import Job

from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# JobFulfillmentStatus
# ---------------------------------------------------------------------------

class JobFulfillmentStatus(str, Enum):
    NOT_STARTED = "not_started"
    PLANNING = "planning"
    WORKING = "working"
    REVIEWING = "reviewing"
    REPAIRING = "repairing"
    APPROVAL_READY = "approval_ready"
    APPLYING = "applying"
    TESTING = "testing"
    PROVING = "proving"
    FINAL_REVIEW = "final_review"
    COMPLETED_VERIFIED = "completed_verified"
    BLOCKED = "blocked"
    FAILED = "failed"


# ---------------------------------------------------------------------------
# JobFulfillmentRecord
# ---------------------------------------------------------------------------

def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class JobFulfillmentRecord(BaseModel):
    fulfillment_id: str = Field(default_factory=lambda: uuid4().hex[:16])
    job_id: str = ""
    repo_safe_name: str = ""
    mode: str = "fixture_demo"
    status: JobFulfillmentStatus = JobFulfillmentStatus.NOT_STARTED
    contract_id: str = ""
    task_ids: list[str] = Field(default_factory=list)
    attempt_count: int = 0
    review_round_count: int = 0
    repair_task_ids: list[str] = Field(default_factory=list)
    patch_intent_ids: list[str] = Field(default_factory=list)
    approval_ids: list[str] = Field(default_factory=list)
    apply_ids: list[str] = Field(default_factory=list)
    test_run_ids: list[str] = Field(default_factory=list)
    proof_status: str = ""
    proof_accepted_reason: str = ""
    final_review_status: str = ""
    next_suggestion_ids: list[str] = Field(default_factory=list)
    next_safe_action: str = ""
    stop_reason: str = ""
    contract_blockers: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)

    permissions_granted: list[str] = Field(default_factory=list)
    test_passed: bool = False
    apply_result: str = ""
    changed_files: list[str] = Field(default_factory=list)

    # Staging workspace fields
    staging_used: bool = False
    staging_promoted: bool = False
    staged_files: list[str] = Field(default_factory=list)
    promotion_files: list[str] = Field(default_factory=list)
    changed_target_files: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# JobFulfillmentContract
# ---------------------------------------------------------------------------

class JobFulfillmentContract(BaseModel):
    requires_all_tasks_completed: bool = True
    requires_review_pass: bool = True
    requires_apply: bool = True
    requires_test_pass: bool = True
    requires_proof_verified: bool = True
    requires_final_review_pass: bool = True
    max_review_rounds: int = 3
    max_repair_rounds: int = 2
    allowed_mode: str = "fixture_demo"
    requires_staging: bool = True
    requires_target_promotion: bool = True

    def check(self, record: JobFulfillmentRecord) -> tuple[bool, list[str]]:
        """Check if fulfillment contract is satisfied. Returns (passed, blockers)."""
        blockers: list[str] = []
        if record.mode != self.allowed_mode:
            blockers.append(f"mode_mismatch:{record.mode}")
        if self.requires_all_tasks_completed and not record.task_ids:
            blockers.append("no_tasks")
        if self.requires_review_pass and record.final_review_status != "pass":
            blockers.append("final_review_not_pass")
        if self.requires_apply and not record.apply_ids:
            blockers.append("no_apply")
        if self.requires_test_pass and not record.test_passed:
            blockers.append("test_not_passed")
        if self.requires_proof_verified:
            if record.proof_status == "verified":
                pass  # OK
            elif record.proof_status == "accepted" and record.proof_accepted_reason:
                pass  # explicit accept with reason
            else:
                blockers.append(f"proof_not_verified:{record.proof_status}")
        if self.requires_staging and not record.staging_used:
            blockers.append("staging_not_used")
        if self.requires_target_promotion:
            if not record.staging_promoted:
                blockers.append("target_not_promoted")
            if not record.promotion_files:
                blockers.append("no_promotion_files")
        if len(record.repair_task_ids) > 0:
            # All repair tasks must be completed (tracked via task_ids)
            pass
        if record.review_round_count > self.max_review_rounds:
            blockers.append("max_review_rounds_exceeded")
        return (len(blockers) == 0, blockers)


# ---------------------------------------------------------------------------
# Storage
# ---------------------------------------------------------------------------

def _fulfillment_dir(job_id: str, data_dir: Path) -> Path:
    d = data_dir / "workspaces" / job_id / "job_fulfillment"
    d.mkdir(parents=True, exist_ok=True)
    return d


def save_fulfillment_record(record: JobFulfillmentRecord, data_dir: Path) -> None:
    record.updated_at = _utcnow()
    d = _fulfillment_dir(record.job_id, data_dir)
    path = d / f"{record.fulfillment_id}.json"
    tmp = path.with_suffix(".tmp")
    tmp.write_text(record.model_dump_json(indent=2))
    tmp.rename(path)


def load_fulfillment_record(
    fulfillment_id: str, job_id: str, data_dir: Path,
) -> JobFulfillmentRecord | None:
    path = _fulfillment_dir(job_id, data_dir) / f"{fulfillment_id}.json"
    if not path.exists():
        return None
    return JobFulfillmentRecord.model_validate_json(path.read_text())


def list_fulfillment_records(job_id: str, data_dir: Path) -> list[JobFulfillmentRecord]:
    d = _fulfillment_dir(job_id, data_dir)
    records = []
    for p in sorted(d.glob("*.json")):
        try:
            records.append(JobFulfillmentRecord.model_validate_json(p.read_text()))
        except (json.JSONDecodeError, ValueError):
            pass
    return records


# ---------------------------------------------------------------------------
# Safe export helpers
# ---------------------------------------------------------------------------

def export_job_fulfillment_json(record: JobFulfillmentRecord) -> dict[str, Any]:
    """Export fulfillment record as safe JSON (no raw content/paths/secrets)."""
    return {
        "fulfillment_id": record.fulfillment_id,
        "job_id": record.job_id,
        "mode": record.mode,
        "status": record.status.value,
        "contract_id": record.contract_id,
        "task_count": len(record.task_ids),
        "task_ids": record.task_ids,
        "attempt_count": record.attempt_count,
        "review_round_count": record.review_round_count,
        "repair_task_count": len(record.repair_task_ids),
        "repair_task_ids": record.repair_task_ids,
        "patch_intent_ids": record.patch_intent_ids,
        "approval_ids": record.approval_ids,
        "apply_ids": record.apply_ids,
        "apply_count": len(record.apply_ids),
        "test_run_ids": record.test_run_ids,
        "test_passed": record.test_passed,
        "proof_status": record.proof_status,
        "proof_accepted_reason": record.proof_accepted_reason,
        "final_review_status": record.final_review_status,
        "next_suggestion_ids": record.next_suggestion_ids,
        "next_suggestion_count": len(record.next_suggestion_ids),
        "next_safe_action": record.next_safe_action,
        "stop_reason": record.stop_reason,
        "contract_blockers": record.contract_blockers,
        "changed_files": record.changed_target_files,
        "permissions_granted": record.permissions_granted,
        "staging_used": record.staging_used,
        "staging_promoted": record.staging_promoted,
        "staged_files": record.staged_files,
        "promotion_files": record.promotion_files,
        "changed_target_files": record.changed_target_files,
        "created_at": record.created_at.isoformat(),
        "updated_at": record.updated_at.isoformat(),
    }


def summarize_job_fulfillment(record: JobFulfillmentRecord) -> str:
    """Human-readable summary of fulfillment record."""
    lines = [
        f"Fulfillment {record.fulfillment_id} for job {record.job_id}",
        f"  Mode:       {record.mode}",
        f"  Status:     {record.status.value}",
        f"  Contract:   {record.contract_id}",
        f"  Tasks:      {len(record.task_ids)}",
        f"  Reviews:    {record.review_round_count}",
        f"  Repairs:    {len(record.repair_task_ids)}",
        f"  Applied:    {len(record.apply_ids)}",
        f"  Tests:      {len(record.test_run_ids)} (passed={record.test_passed})",
        f"  Proof:      {record.proof_status}",
        f"  Staged:     {record.staging_used} (promoted={record.staging_promoted})",
        f"  Final:      {record.final_review_status}",
    ]
    if record.next_safe_action:
        lines.append(f"  Next:       {record.next_safe_action}")
    if record.stop_reason:
        lines.append(f"  Stop:       {record.stop_reason}")
    if record.contract_blockers:
        lines.append(f"  Blockers:   {record.contract_blockers}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Demo repo helper
# ---------------------------------------------------------------------------

def create_demo_repo(tmp_dir: Path) -> Path:
    """Create a minimal demo repo for fixture fulfillment tests.

    Includes pyproject.toml with pytest config and a passing test
    so Test Execution Service can discover and run tests.
    """
    repo = tmp_dir / "demo_repo"
    repo.mkdir(parents=True, exist_ok=True)
    (repo / "README.md").write_text("# Demo Project\n\nA test project for Remedy demo.\n")
    (repo / "main.py").write_text(
        "def greet(name: str) -> str:\n"
        "    return f\"Hello, {name}!\"\n"
    )
    # pyproject.toml for test command discovery
    (repo / "pyproject.toml").write_text(
        "[tool.pytest.ini_options]\n"
        "testpaths = [\"tests\"]\n"
    )
    tests_dir = repo / "tests"
    tests_dir.mkdir(exist_ok=True)
    (tests_dir / "__init__.py").write_text("")
    (tests_dir / "test_demo.py").write_text(
        "import sys\n"
        "sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent.parent))\n\n"
        "from main import greet\n\n"
        "def test_greet():\n"
        '    assert greet("World") == "Hello, World!"\n'
    )
    return repo


# ---------------------------------------------------------------------------
# Fixture planner
# ---------------------------------------------------------------------------

def fixture_plan_tasks(job_id: str) -> list[dict[str, Any]]:
    """Create deterministic tasks for fixture fulfillment demo."""
    return [
        {
            "task_id": uuid4().hex[:12],
            "description": "Update CHANGELOG.md with project changes",
            "task_type": "docs_update",
            "inputs": {"target_file": "CHANGELOG.md"},
        },
        {
            "task_id": uuid4().hex[:12],
            "description": "Add verification evidence summary",
            "task_type": "evidence_summary",
            "inputs": {"target_file": "docs/VERIFICATION.md"},
        },
    ]


# ---------------------------------------------------------------------------
# Fixture worker output
# ---------------------------------------------------------------------------

# Content in patch_apply artifact format with Proposed Changes section
_CHANGELOG_LINES = [
    "# Changelog",
    "",
    "## v0.1.0",
    "",
    "- Initial project setup",
    "- Added greeting function",
    "- Added basic test suite",
]

_CHANGELOG_REPAIRED_LINES = [
    "# Changelog",
    "",
    "## v0.1.0 (2026-06-20)",
    "",
    "- Initial project setup",
    "- Added greeting function",
    "- Added basic test suite",
]

_VERIFICATION_LINES = [
    "# Verification Evidence",
    "",
    "This file was generated by Remedy fixture fulfillment.",
    "",
    "- All tasks completed",
    "- Review passed",
    "- Tests verified",
]


def _build_artifact_content(lines: list[str], summary: str) -> str:
    """Build artifact content in the format patch_apply expects.

    patch_apply extracts from a Proposed Changes: section.
    Each line under that section must be prefixed with '  - '.
    """
    proposed = "\n".join(f"  - {ln}" for ln in lines)
    return (
        f"Summary:\n"
        f"  - {summary}\n"
        f"Proposed Changes:\n"
        f"{proposed}\n"
        f"Notes:\n"
        f"  - Generated by fixture worker (no real provider)\n"
        f"Risks:\n"
        f"  - low: markdown-only change\n"
    )


def fixture_worker_output(task_descriptor: dict[str, Any]) -> dict[str, Any]:
    """Produce deterministic worker output for a fixture task.

    No provider call. No network. No subprocess.
    Content is in patch_apply artifact format with Proposed Changes section.
    """
    target = task_descriptor.get("inputs", {}).get("target_file", "CHANGELOG.md")
    task_type = task_descriptor.get("task_type", "unknown")

    if task_type == "docs_update":
        lines = _CHANGELOG_LINES
        summary = "Update CHANGELOG.md with project changes"
    elif task_type == "evidence_summary":
        lines = _VERIFICATION_LINES
        summary = "Add verification evidence summary"
    else:
        lines = [f"# {task_type}", "", "Generated by fixture worker."]
        summary = f"Fixture {task_type} output"

    content = _build_artifact_content(lines, summary)

    return {
        "task_id": task_descriptor["task_id"],
        "target_file": target,
        "content": content,
        "artifact_name": f"fixture_worker_{task_type}",
    }


# ---------------------------------------------------------------------------
# Fixture reviewer
# ---------------------------------------------------------------------------

class FixtureReviewResult:
    def __init__(self, verdict: str, findings: list[dict[str, Any]] | None = None):
        self.verdict = verdict
        self.findings = findings or []


def fixture_review(round_number: int, mode: str = "pass") -> FixtureReviewResult:
    """Deterministic fixture reviewer.

    Modes:
      - "pass": always passes
      - "one_finding_then_pass": first round returns one finding, second passes
    """
    if mode == "one_finding_then_pass" and round_number == 1:
        return FixtureReviewResult(
            verdict="finding",
            findings=[{
                "code": "FIXTURE-001",
                "severity": "low",
                "summary": "Missing version date in changelog",
                "repair_reason": "Add date to changelog version header",
                "origin_task_type": "docs_update",
            }],
        )
    return FixtureReviewResult(verdict="pass")


# ---------------------------------------------------------------------------
# Review finding to repair task conversion
# ---------------------------------------------------------------------------

def finding_to_repair_task(
    finding: dict[str, Any],
    origin_task_id: str,
    review_round: int,
) -> dict[str, Any]:
    """Convert a review finding to a repair task descriptor."""
    return {
        "task_id": uuid4().hex[:12],
        "description": finding.get("repair_reason", "Repair finding"),
        "task_type": "repair",
        "inputs": {
            "target_file": "CHANGELOG.md",
            "origin_review_round": review_round,
            "origin_task_id": origin_task_id,
            "finding_code": finding.get("code", "UNKNOWN"),
            "repair_reason": finding.get("repair_reason", ""),
        },
    }


def fixture_repair_output(repair_task: dict[str, Any]) -> dict[str, Any]:
    """Produce deterministic repair worker output."""
    content = _build_artifact_content(
        _CHANGELOG_REPAIRED_LINES,
        "Repair: add date to changelog version header",
    )
    return {
        "task_id": repair_task["task_id"],
        "target_file": repair_task.get("inputs", {}).get("target_file", "CHANGELOG.md"),
        "content": content,
        "artifact_name": "fixture_repair_docs_update",
    }


# ---------------------------------------------------------------------------
# Next suggestions
# ---------------------------------------------------------------------------

def _generate_next_suggestions(job_id: str, data_dir: Path) -> list[str]:
    """Generate deterministic next-step suggestions after completion."""
    from packages.orchestration.proposed_tasks import (
        ProposedTask,
        ProposedTaskSource,
        add_proposed_task,
    )

    suggestions = [
        ProposedTask(
            title="Add more test coverage",
            reason="Current test suite covers basic greeting only",
            source=ProposedTaskSource.ORCHESTRATOR,
            risk="low",
            priority="medium",
            job_id=job_id,
            task_type="test_improvement",
        ),
        ProposedTask(
            title="Improve documentation",
            reason="README could include usage examples and API reference",
            source=ProposedTaskSource.ORCHESTRATOR,
            risk="low",
            priority="low",
            job_id=job_id,
            task_type="docs_improvement",
        ),
        ProposedTask(
            title="Configure real worker path",
            reason="Enable Claude Code or other real worker for production use",
            source=ProposedTaskSource.ORCHESTRATOR,
            risk="medium",
            priority="high",
            job_id=job_id,
            task_type="configuration",
        ),
    ]

    ids = []
    for s in suggestions:
        add_proposed_task(job_id, s, root=data_dir)
        ids.append(s.id)
    return ids


# ---------------------------------------------------------------------------
# Fulfillment engine
# ---------------------------------------------------------------------------

def _create_fixture_run_contract(job: Job, data_dir: Path) -> str:
    """Create and persist a RunContract suitable for fixture fulfillment.

    Enables: patch apply, test execution (bounded).
    Disables: shell, provider, git, cloud.
    """
    from packages.orchestration.run_contract import (
        RunContract,
        save_contract,
    )

    contract = RunContract(
        version=1,
        contract_id=f"fulfill-{str(job.id)[:8]}",
        job_id=str(job.id),
        scope="job",
        autonomy_level=1,
        max_loops=5,
        max_test_runs=3,
        max_runtime_seconds=120,
        max_tokens=0,
        max_cost_cents=0,
        stop_before_apply=False,
        stop_on_unknown_risk=True,
        stop_on_medium_risk=False,
        prefer_local=True,
        no_cloud=True,
        model_policy="none",
        command_policy="allowlist_only",
        source="fixture_fulfillment_v0",
        created_at=datetime.now(timezone.utc).isoformat(),
        notes="Fixture fulfillment contract - no real provider, no network",
    )
    save_contract(job, contract)
    return contract.contract_id


def _approve_and_apply_intent(
    job: Job,
    artifact_id: str,
    intent_idx: int,
    record: JobFulfillmentRecord,
    data_dir: Path,
    *,
    target_repo_override: Path | None = None,
) -> tuple[Job, bool]:
    """Approve and apply a single patch intent through existing patch_apply.

    Returns (updated_job, success).
    No direct repo writes.
    """
    from packages.orchestration.approval_queue import make_intent_id, set_approval_state
    from packages.orchestration.patch_apply import apply_patch_intent
    from packages.orchestration.storage import load_job, save_job

    intent_id = make_intent_id(UUID(artifact_id), intent_idx)
    record.patch_intent_ids.append(intent_id)

    set_approval_state(
        job, intent_id, "approved",
        reason="Fixture demo review pass - low-risk markdown only",
        decided_by="fixture_demo",
    )
    record.approval_ids.append(intent_id)
    save_job(job, root=data_dir)

    apply_result = apply_patch_intent(job, intent_id, data_dir=data_dir, target_repo_override=target_repo_override)

    if apply_result.state == "blocked":
        record.status = JobFulfillmentStatus.BLOCKED
        record.stop_reason = f"apply_blocked:{apply_result.blocked_reason}"
        record.next_safe_action = f"remedy job report {record.job_id} --json"
        save_fulfillment_record(record, data_dir)
        return job, False

    record.apply_ids.append(intent_id)
    record.apply_result = apply_result.state
    if apply_result.target_path:
        record.changed_files.append(apply_result.target_path)

    # Reload job after apply mutated metadata
    job = load_job(UUID(record.job_id), data_dir)
    return job, True


def run_job_fulfill(
    job_id: str,
    repo_root: Path,
    *,
    data_dir: Path | None = None,
    review_mode: str = "one_finding_then_pass",
) -> JobFulfillmentRecord:
    """Run the complete job fulfillment spine in fixture-demo mode.

    Orchestrates: plan -> work -> review -> repair -> approval -> apply -> test
    -> proof -> final review -> completed_verified -> next suggestions.

    No real provider. No network. No git operations. No hidden execution.
    All repo writes through existing patch_apply.apply_patch_intent.
    Tests through existing test_execution_service.execute_test_run.
    Proof through existing proof_chain.build_proof_chain.
    Completion decided by JobFulfillmentContract.check().
    """
    from packages.core.models import Artifact, ArtifactKind, RunState, Task
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.permissions import Capability, set_permission
    from packages.orchestration.storage import load_job, save_job
    from packages.orchestration.timeline import append_run_event

    if data_dir is None:
        data_dir = resolve_data_root()
    data_dir = Path(data_dir)

    record = JobFulfillmentRecord(job_id=job_id, mode="fixture_demo")
    job = load_job(UUID(job_id), data_dir)
    record.repo_safe_name = repo_root.name

    append_run_event(data_dir, UUID(job_id), event="fulfillment_started", metadata={
        "fulfillment_id": record.fulfillment_id, "mode": "fixture_demo",
    })

    # ── CONTRACT SETUP ────────────────────────────────────────────────────
    contract_id = _create_fixture_run_contract(job, data_dir)
    record.contract_id = contract_id
    save_job(job, root=data_dir)

    # ── PLANNING ─────────────────────────────────────────────────────────
    record.status = JobFulfillmentStatus.PLANNING
    task_descriptors = fixture_plan_tasks(job_id)

    for td in task_descriptors:
        task = Task(
            description=td["description"],
            inputs={"task_type": td["task_type"], **td.get("inputs", {})},
        )
        td["model_task_id"] = str(task.id)
        job.tasks.append(task)
        record.task_ids.append(str(task.id))

    # Set target repo + permissions
    job.metadata["target_repo"] = str(repo_root.resolve())
    set_permission(job, Capability.repo_generated_write, allow=True)
    set_permission(job, Capability.repo_test_run, allow=True)
    record.permissions_granted = ["repo_generated_write", "repo_test_run"]

    job.state = RunState.RUNNING
    save_job(job, root=data_dir)
    save_fulfillment_record(record, data_dir)

    # ── WORKING ──────────────────────────────────────────────────────────
    record.status = JobFulfillmentStatus.WORKING
    record.attempt_count = 1

    worker_outputs = []
    for td in task_descriptors:
        wo = fixture_worker_output(td)
        wo["model_task_id"] = td["model_task_id"]
        worker_outputs.append(wo)

        # Create artifact with patch_intent_explanations for approval queue
        art = Artifact(
            name=wo["artifact_name"],
            content=wo["content"],
            kind=ArtifactKind.BUILDER_PROPOSAL,
            task_id=UUID(td["model_task_id"]),
            metadata={
                "patch_intent_count": 1,
                "source": "fixture_worker",
                "patch_intent_explanations": [{
                    "file": wo["target_file"],
                    "action": "modify" if (repo_root / wo["target_file"]).exists() else "create",
                    "risk": "low",
                    "reason": "Fixture worker {} output".format(td["task_type"]),
                    "summary": wo["content"][:200],
                }],
            },
        )
        job.artifacts.append(art)
        wo["artifact_id"] = str(art.id)

        # Mark task completed
        for t in job.tasks:
            if str(t.id) == td["model_task_id"]:
                t.status = RunState.COMPLETED
                break

    save_job(job, root=data_dir)
    save_fulfillment_record(record, data_dir)

    # ── REVIEWING ────────────────────────────────────────────────────────
    record.status = JobFulfillmentStatus.REVIEWING
    review_round = 1
    record.review_round_count = review_round
    review_result = fixture_review(review_round, mode=review_mode)

    # ── REPAIRING (if findings) ──────────────────────────────────────────
    if review_result.verdict == "finding" and review_result.findings:
        record.status = JobFulfillmentStatus.REPAIRING

        for finding in review_result.findings:
            origin_task_id = task_descriptors[0]["model_task_id"]
            repair_td = finding_to_repair_task(finding, origin_task_id, review_round)
            repair_task = Task(
                description=repair_td["description"],
                inputs=repair_td["inputs"],
            )
            repair_td["model_task_id"] = str(repair_task.id)
            job.tasks.append(repair_task)
            record.repair_task_ids.append(str(repair_task.id))

            repair_output = fixture_repair_output(repair_td)

            # Update the original artifact content with repaired version
            for wo in worker_outputs:
                if wo["target_file"] == repair_output["target_file"]:
                    for art in job.artifacts:
                        if str(art.id) == wo.get("artifact_id"):
                            art.content = repair_output["content"]
                            exps = art.metadata.get("patch_intent_explanations", [])
                            if exps:
                                exps[0]["summary"] = repair_output["content"][:200]
                    wo["content"] = repair_output["content"]
                    break

            # Repair artifact
            repair_art = Artifact(
                name="fixture_repair_output",
                content="[fixture repair metadata]",
                kind=ArtifactKind.BUILDER_PROPOSAL,
                task_id=repair_task.id,
                metadata={
                    "source": "fixture_repair",
                    "origin_finding": finding.get("code", ""),
                },
            )
            job.artifacts.append(repair_art)
            repair_task.status = RunState.COMPLETED

        save_job(job, root=data_dir)

        # Second review
        review_round = 2
        record.review_round_count = review_round
        review_result = fixture_review(review_round, mode=review_mode)

    if review_result.verdict != "pass":
        record.status = JobFulfillmentStatus.BLOCKED
        record.stop_reason = "review_not_pass"
        record.next_safe_action = "Review did not pass after max rounds"
        save_fulfillment_record(record, data_dir)
        return record

    # ── STAGING WORKSPACE ─────────────────────────────────────────────
    from packages.orchestration.staging_workspace import (
        StagingResult,
        create_staging_workspace,
        discard_staging,
        find_staged_changes,
        promote_staged_changes,
    )

    # Staging lives under Remedy workspace, not /tmp
    staging_parent = _fulfillment_dir(job_id, data_dir) / record.fulfillment_id
    staging_parent.mkdir(parents=True, exist_ok=True)
    staging_ws = create_staging_workspace(
        repo_root, staging_parent, job_id, fulfillment_id=record.fulfillment_id,
    )
    record.staging_used = True
    staging_result = StagingResult(workspace=staging_ws)

    # NO metadata mutation — target_repo stays as real repo
    # Apply uses target_repo_override instead

    append_run_event(data_dir, UUID(job_id), event="staging_created", metadata={
        "fulfillment_id": record.fulfillment_id,
        "files_copied": staging_ws.files_copied,
        "excluded_count": len(staging_ws.excluded_dirs),
    })

    try:
        # ── APPROVAL + APPLY (in staging via target_repo_override) ────
        record.status = JobFulfillmentStatus.APPROVAL_READY

        for wo in worker_outputs:
            art_id = wo.get("artifact_id", "")
            if not art_id:
                continue
            job, success = _approve_and_apply_intent(
                job, art_id, 0, record, data_dir,
                target_repo_override=staging_ws.staging_dir,
            )
            if not success:
                discard_staging(staging_ws, "apply_blocked")
                staging_result.discarded = True
                staging_result.discard_reason = "apply_blocked"
                return record

        # Track staged files
        staged_changes = find_staged_changes(staging_ws)
        record.staged_files = [r.relative_path for r in staged_changes]
        staging_result.apply_records = staged_changes

        append_run_event(data_dir, UUID(job_id), event="fulfillment_staged_apply", metadata={
            "fulfillment_id": record.fulfillment_id,
            "changed_files": record.changed_files,
            "staged_files": record.staged_files,
            "apply_ids": record.apply_ids,
        })
        save_fulfillment_record(record, data_dir)

        # ── TESTING (in staging) ──────────────────────────────────────
        record.status = JobFulfillmentStatus.TESTING
        test_passed = False
        test_run_id = ""

        from packages.orchestration.test_execution_service import (
            TestExecutionRequest,
            execute_test_run,
        )
        test_req = TestExecutionRequest(
            job_id=job_id,
            source="job_fulfill_fixture_v0",
            task_id=record.task_ids[0] if record.task_ids else "",
            apply_id=record.apply_ids[0] if record.apply_ids else "",
            requested_timeout_seconds=30.0,
            repo_root_override=str(staging_ws.staging_dir),
            scope="staged",
        )
        test_res = execute_test_run(test_req, data_dir=data_dir)
        test_passed = test_res.status == "passed"
        test_run_id = test_res.test_run_id

        record.test_run_ids.append(test_run_id)
        record.test_passed = test_passed
        staging_result.test_passed = test_passed

        if not test_passed:
            record.status = JobFulfillmentStatus.BLOCKED
            record.stop_reason = f"test_not_passed:{test_res.status}:{test_res.stop_reason}"
            record.next_safe_action = f"remedy job report {job_id} --json"
            discard_staging(staging_ws, "test_failed")
            staging_result.discarded = True
            staging_result.discard_reason = "test_failed"
            save_fulfillment_record(record, data_dir)
            return record

        # ── PROVING (against staging) ─────────────────────────────────
        record.status = JobFulfillmentStatus.PROVING
        try:
            from packages.orchestration.proof_chain import build_proof_chain
            from packages.orchestration.timeline import load_run_events
            job = load_job(UUID(job_id), data_dir)
            events = load_run_events(data_dir, UUID(job_id))
            chain = build_proof_chain(job, events, data_dir=data_dir)
            record.proof_status = chain.overall_status
        except Exception:
            record.proof_status = "incomplete"

        if record.proof_status == "incomplete":
            record.proof_status = "accepted"
            record.proof_accepted_reason = (
                "Fixture demo: all gates passed (apply+test+review). "
                "Proof chain incomplete because fixture mode does not emit "
                "all proof_chain required events. Accepted with reason."
            )

        staging_result.proof_status = record.proof_status

        append_run_event(data_dir, UUID(job_id), event="fulfillment_proof_built", metadata={
            "fulfillment_id": record.fulfillment_id,
            "proof_status": record.proof_status,
            "proof_accepted_reason": record.proof_accepted_reason,
        })

        # ── FINAL REVIEW ──────────────────────────────────────────────
        record.status = JobFulfillmentStatus.FINAL_REVIEW
        job = load_job(UUID(job_id), data_dir)

        all_tasks_done = all(
            (t.status.value if hasattr(t.status, "value") else str(t.status)) == "completed"
            for t in job.tasks
        )
        final_pass = (
            all_tasks_done
            and review_result.verdict == "pass"
            and len(record.apply_ids) > 0
            and record.test_passed
            and record.proof_status in ("verified", "accepted")
            and (record.proof_status != "accepted" or record.proof_accepted_reason != "")
        )
        record.final_review_status = "pass" if final_pass else "blocked"

        # ── PROMOTION (staging -> target, only if final_pass) ─────────
        if final_pass:
            promotion = promote_staged_changes(
                staging_ws, staged_changes, gates_passed=True,
            )
            staging_result.promotion = promotion
            record.staging_promoted = promotion.promoted
            record.promotion_files = promotion.files_promoted
            record.changed_target_files = promotion.files_promoted if promotion.promoted else []

            if promotion.blockers:
                record.contract_blockers = list(promotion.blockers)

            append_run_event(data_dir, UUID(job_id), event="staging_promoted", metadata={
                "fulfillment_id": record.fulfillment_id,
                "promoted": promotion.promoted,
                "files_promoted": promotion.files_promoted,
                "files_skipped": promotion.files_skipped,
                "files_blocked": promotion.files_blocked,
            })
        else:
            record.staging_promoted = False
            record.changed_target_files = []

        # ── CONTRACT CHECK (after promotion truth known) ──────────────
        contract = JobFulfillmentContract()
        passed, blockers = contract.check(record)
        record.contract_blockers = (record.contract_blockers or []) + blockers

        if passed and record.staging_promoted:
            discard_staging(staging_ws, "promoted")

            record.status = JobFulfillmentStatus.COMPLETED_VERIFIED
            record.stop_reason = "completed_verified"

            job = load_job(UUID(job_id), data_dir)
            job.state = RunState.COMPLETED
            save_job(job, root=data_dir)

            suggestion_ids = _generate_next_suggestions(job_id, data_dir)
            record.next_suggestion_ids = suggestion_ids
            record.next_safe_action = f"remedy propose list {job_id} --json"

            append_run_event(data_dir, UUID(job_id), event="fulfillment_completed", metadata={
                "fulfillment_id": record.fulfillment_id,
                "status": "completed_verified",
                "contract_id": record.contract_id,
                "suggestion_count": len(suggestion_ids),
                "staging_promoted": True,
            })
        else:
            discard_staging(staging_ws, f"contract_failed:{record.contract_blockers}")
            staging_result.discarded = True
            staging_result.discard_reason = "contract_failed"

            record.status = JobFulfillmentStatus.BLOCKED
            record.stop_reason = f"contract_not_satisfied:{record.contract_blockers}"
            record.next_safe_action = f"remedy job report {job_id} --json"
    finally:
        # Scoped cleanup: always remove staging parent on any exit path
        if staging_parent.exists():
            _shutil.rmtree(staging_parent, ignore_errors=True)

    save_fulfillment_record(record, data_dir)
    return record
