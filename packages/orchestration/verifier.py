"""
Task Contract v1 and deterministic workspace verifier.

A task execution is considered complete only after the verifier passes.
The verifier runs deterministic, local-only checks — no LLM calls, no shell execution.

Task Contract v1 checks (all required by default):
  1. task has at least one output_artifact_id
  2. referenced artifact exists in job.artifacts
  3. artifact.task_id matches task.id
  4. artifact metadata contains 'workspace_file' key
  5. workspace file exists on disk
  6. workspace file is not empty
  7. workspace file contains at least one proposed change line (starts with "  - ")

The verifier is pure — it does not mutate job state.
Callers must call finalize_task() in task_runner to apply the result.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from uuid import UUID

from pydantic import BaseModel

from packages.core.models import Job


class TaskContract(BaseModel):
    """Minimal contract describing what a task execution must produce.

    All checks are deterministic and local-only — no LLM or shell execution.
    All fields default to True (all checks required). Step 7 always runs all checks.

    require_artifact:          task must have at least one output_artifact_id, and
                               that artifact must exist in job.artifacts with a
                               matching task_id
    require_workspace_file:    artifact must record a 'workspace_file' path in
                               metadata, and that file must exist and be non-empty
    require_proposed_changes:  workspace file must contain at least one proposed
                               change line (line starting with "  - ")
    """

    require_artifact: bool = True
    require_workspace_file: bool = True
    require_proposed_changes: bool = True


@dataclass
class VerificationCheckResult:
    """Result of a single named verification check."""

    check: str
    passed: bool
    message: str


@dataclass
class VerificationResult:
    """Aggregate result of verifying a task execution against its contract.

    task_id: UUID of the task that was verified.
    passed:  True only if all checks passed.
    checks:  Ordered list of individual check results.
    """

    task_id: UUID
    passed: bool
    checks: list[VerificationCheckResult] = field(default_factory=list)

    @property
    def failures(self) -> list[VerificationCheckResult]:
        """Return only the checks that failed."""
        return [c for c in self.checks if not c.passed]


def verify_task_output(
    job: Job,
    task_id: UUID,
    contract: TaskContract | None = None,
) -> VerificationResult:
    """Run Task Contract v1 checks against the output of an executed task.

    Checks are deterministic and local-only: no LLM calls, no shell execution.
    The 'contract' parameter reserves space for future customization; Step 7
    always runs all checks (all require_* flags default to True).

    Does not mutate job state. Caller must call finalize_task() in task_runner
    to apply the verification result to task and job state.

    Returns a VerificationResult describing which checks passed or failed.
    Early return after any check that would cause a subsequent check to error
    (e.g. if artifact is None, workspace file checks are skipped).
    """
    if contract is None:
        contract = TaskContract()

    checks: list[VerificationCheckResult] = []

    task = next((t for t in job.tasks if t.id == task_id), None)
    if task is None:
        return VerificationResult(
            task_id=task_id,
            passed=False,
            checks=[
                VerificationCheckResult(
                    check="task_exists",
                    passed=False,
                    message=f"task_id={task_id} not found in job.tasks",
                )
            ],
        )

    if contract.require_artifact:
        # Check 1: task has at least one output_artifact_id
        has_artifact_ids = len(task.output_artifact_ids) > 0
        checks.append(
            VerificationCheckResult(
                check="has_output_artifact",
                passed=has_artifact_ids,
                message="OK" if has_artifact_ids else "task has no output_artifact_ids",
            )
        )
        if not has_artifact_ids:
            return VerificationResult(task_id=task_id, passed=False, checks=checks)

        # Check 2: referenced artifact exists
        artifact_id = task.output_artifact_ids[0]
        artifact = next((a for a in job.artifacts if a.id == artifact_id), None)
        artifact_exists = artifact is not None
        checks.append(
            VerificationCheckResult(
                check="artifact_exists",
                passed=artifact_exists,
                message=(
                    "OK"
                    if artifact_exists
                    else f"artifact {artifact_id} not found in job.artifacts"
                ),
            )
        )
        if not artifact_exists:
            return VerificationResult(task_id=task_id, passed=False, checks=checks)

        # Check 3: artifact.task_id matches task.id
        task_id_matches = artifact.task_id == task.id
        checks.append(
            VerificationCheckResult(
                check="artifact_task_id_matches",
                passed=task_id_matches,
                message=(
                    "OK"
                    if task_id_matches
                    else f"artifact.task_id={artifact.task_id} != task.id={task.id}"
                ),
            )
        )
        if not task_id_matches:
            return VerificationResult(task_id=task_id, passed=False, checks=checks)

        if contract.require_workspace_file:
            # Check 4: workspace_file key present in metadata
            has_ws_key = "workspace_file" in artifact.metadata
            checks.append(
                VerificationCheckResult(
                    check="workspace_file_in_metadata",
                    passed=has_ws_key,
                    message=(
                        "OK"
                        if has_ws_key
                        else "artifact metadata missing 'workspace_file' key"
                    ),
                )
            )
            if not has_ws_key:
                return VerificationResult(task_id=task_id, passed=False, checks=checks)

            workspace_file = Path(artifact.metadata["workspace_file"])

            # Check 5: file exists on disk
            file_exists = workspace_file.exists()
            checks.append(
                VerificationCheckResult(
                    check="workspace_file_exists",
                    passed=file_exists,
                    message=(
                        "OK"
                        if file_exists
                        else f"workspace file does not exist: {workspace_file}"
                    ),
                )
            )
            if not file_exists:
                return VerificationResult(task_id=task_id, passed=False, checks=checks)

            # Check 6: file is not empty
            file_not_empty = workspace_file.stat().st_size > 0
            checks.append(
                VerificationCheckResult(
                    check="workspace_file_not_empty",
                    passed=file_not_empty,
                    message=(
                        "OK"
                        if file_not_empty
                        else f"workspace file is empty: {workspace_file}"
                    ),
                )
            )
            if not file_not_empty:
                return VerificationResult(task_id=task_id, passed=False, checks=checks)

            if contract.require_proposed_changes:
                # Check 7: at least one proposed change line in the file
                content = workspace_file.read_text(encoding="utf-8")
                has_change = any(
                    line.startswith("  - ") for line in content.splitlines()
                )
                checks.append(
                    VerificationCheckResult(
                        check="has_proposed_change",
                        passed=has_change,
                        message=(
                            "OK"
                            if has_change
                            else "workspace file contains no proposed change lines"
                        ),
                    )
                )

    passed = all(c.passed for c in checks)
    return VerificationResult(task_id=task_id, passed=passed, checks=checks)
