"""Tests for safe change-set test evidence association."""

from __future__ import annotations

from packages.core.models import Artifact, ArtifactKind, Job, Task
from packages.orchestration.approval_queue import make_intent_id
from packages.orchestration.change_set import derive_change_set


def _job_with_intents(count: int = 1):
    task = Task(description="Task")
    artifact = Artifact(
        name="patch-intent",
        content="",
        kind=ArtifactKind.PATCH_INTENT,
        task_id=task.id,
        metadata={
            "patch_intent_explanations": [
                {"file": f"src/file_{idx}.py", "action": "modify", "risk": "medium"}
                for idx in range(count)
            ],
            "patch_intent_approvals": {},
        },
    )
    approvals = {}
    intent_ids = []
    for idx in range(count):
        iid = make_intent_id(artifact.id, idx)
        intent_ids.append(iid)
        approvals[iid] = {"state": "approved", "decided_at": "", "decided_by": ""}
    artifact.metadata["patch_intent_approvals"] = approvals
    job = Job(name="job", user_prompt="prompt")
    job.tasks = [task]
    job.artifacts = [artifact]
    return job, intent_ids, task


def test_change_set_does_not_attach_latest_global_test_to_every_change():
    job, intent_ids, _task = _job_with_intents(2)
    events = [
        {"event": "patch_intent_applied", "timestamp": "2026-01-01T00:00:00Z", "metadata": {"intent_id": intent_ids[0], "outcome": "applied"}},
        {"event": "patch_intent_applied", "timestamp": "2026-01-01T00:00:00Z", "metadata": {"intent_id": intent_ids[1], "outcome": "applied"}},
        {"event": "test_run_completed", "timestamp": "2026-01-01T00:01:00Z", "metadata": {"status": "passed", "exit_code": 0}},
    ]

    changes = derive_change_set(job, events)

    assert len(changes) == 2
    assert all(change.test == {"ran": False, "linked": False} for change in changes)


def test_change_set_links_intent_test_only_to_matching_change():
    job, intent_ids, _task = _job_with_intents(2)
    events = [
        {"event": "patch_intent_applied", "timestamp": "2026-01-01T00:00:00Z", "metadata": {"intent_id": intent_ids[0], "outcome": "applied"}},
        {"event": "patch_intent_applied", "timestamp": "2026-01-01T00:00:00Z", "metadata": {"intent_id": intent_ids[1], "outcome": "applied"}},
        {"event": "test_run_completed", "metadata": {"intent_id": intent_ids[0], "status": "passed", "exit_code": 0}},
    ]

    changes = derive_change_set(job, events)
    by_id = {change.intent_id: change for change in changes}

    assert by_id[intent_ids[0]].test["linked"] is True
    assert by_id[intent_ids[0]].test["status"] == "passed"
    assert by_id[intent_ids[1]].test == {"ran": False, "linked": False}


def test_change_set_links_sole_change_generic_only_after_apply():
    job, intent_ids, _task = _job_with_intents(1)
    events = [
        {"event": "patch_intent_applied", "timestamp": "2026-01-01T00:00:00Z", "metadata": {"intent_id": intent_ids[0], "outcome": "applied"}},
        {"event": "test_run_completed", "timestamp": "2026-01-01T00:01:00Z", "metadata": {"status": "passed", "exit_code": 0}},
    ]

    changes = derive_change_set(job, events)

    assert changes[0].test["linked"] is True
    assert changes[0].test["link"] == "sole_change"


def test_change_set_does_not_link_sole_change_generic_before_apply():
    job, intent_ids, _task = _job_with_intents(1)
    events = [
        {"event": "patch_intent_applied", "timestamp": "2026-01-01T00:01:00Z", "metadata": {"intent_id": intent_ids[0], "outcome": "applied"}},
        {"event": "test_run_completed", "timestamp": "2026-01-01T00:00:00Z", "metadata": {"status": "passed", "exit_code": 0}},
    ]

    changes = derive_change_set(job, events)

    assert changes[0].test == {"ran": False, "linked": False}
