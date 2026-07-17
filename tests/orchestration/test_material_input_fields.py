"""F14 — one table-driven proof that EVERY material input field moves the job's input identity.

A "material" input is any persisted input that can change which work runs, how many calls run,
what prompts are assembled, what tests run, or what provider options are used. F012's promise is
that changing any of them changes the recorded input identity (``job_input_sha256``) — so a
check-mode diff can never call two genuinely different inputs "the same". This enumerates the
whole set (including the F2 invocation controls: timeout_sec, timeout_profile, max_output_chars,
stream_evidence, max_tasks) and their ``_source`` companions, and asserts each one moves the
hash. A field NOT covered here that becomes material must be added — the test is the checklist.
"""
from __future__ import annotations

import copy
import dataclasses

import pytest

from packages.orchestration.pingpong_job import ExecutionConfig, TaskEntry
from packages.orchestration.run_manifest import (
    build_job_input_definition,
    job_input_sha256,
)


class _Job:
    """The minimal shape ``build_job_input_definition`` reads."""

    def __init__(self):
        self.job_id = "j"
        self.job_title = "demo job"
        self.job_file_sha256 = "f" * 64
        self.isolation_mode = "worktree"
        self.execution_config = ExecutionConfig()
        self.tasks = [
            TaskEntry(task_id="T001", source_heading_number=1, title="a", body="b",
                      acceptance="c"),
        ]


def _sha(job):
    return job_input_sha256(job)


# (label, mutate(job)) — each mutation must change job_input_sha256.
def _mutations():
    def ec(job, **kw):
        job.execution_config = dataclasses.replace(job.execution_config, **kw)

    return [
        # --- provider / model / effort selection ---
        ("builder", lambda j: ec(j, builder="claude")),
        ("builder_source", lambda j: ec(j, builder_source="cli")),
        ("builder_model", lambda j: ec(j, builder_model="opus")),
        ("builder_model_source", lambda j: ec(j, builder_model_source="cli")),
        ("builder_effort", lambda j: ec(j, builder_effort="high")),
        ("builder_effort_source", lambda j: ec(j, builder_effort_source="cli")),
        ("reviewer", lambda j: ec(j, reviewer="claude")),
        ("reviewer_source", lambda j: ec(j, reviewer_source="cli")),
        ("reviewer_model", lambda j: ec(j, reviewer_model="sonnet")),
        ("reviewer_model_source", lambda j: ec(j, reviewer_model_source="cli")),
        ("reviewer_effort", lambda j: ec(j, reviewer_effort="low")),
        ("reviewer_effort_source", lambda j: ec(j, reviewer_effort_source="cli")),
        ("repair_provider", lambda j: ec(j, repair_provider="claude")),
        ("repair_provider_source", lambda j: ec(j, repair_provider_source="cli")),
        ("repair_model", lambda j: ec(j, repair_model="opus")),
        ("repair_model_source", lambda j: ec(j, repair_model_source="cli")),
        ("repair_effort", lambda j: ec(j, repair_effort="high")),
        ("repair_effort_source", lambda j: ec(j, repair_effort_source="cli")),
        # --- loop / repair budget ---
        ("max_rounds", lambda j: ec(j, max_rounds=7)),
        ("max_rounds_source", lambda j: ec(j, max_rounds_source="cli")),
        ("repair_rounds_allowed", lambda j: ec(j, repair_rounds_allowed=5)),
        ("repair_rounds_source", lambda j: ec(j, repair_rounds_source="cli")),
        # --- test command / write mode / context strategy ---
        ("test_command", lambda j: ec(j, test_command="pytest -q")),
        ("test_command_source", lambda j: ec(j, test_command_source="cli")),
        ("claude_cli_write_mode", lambda j: ec(j, claude_cli_write_mode="auto")),
        ("claude_cli_write_mode_source",
         lambda j: ec(j, claude_cli_write_mode_source="cli")),
        ("context_strategy", lambda j: ec(j, context_strategy="whole_job")),
        # --- F2 invocation controls (the reviewed gap) ---
        ("timeout_sec", lambda j: ec(j, timeout_sec=999)),
        ("timeout_sec_source", lambda j: ec(j, timeout_sec_source="invocation")),
        ("timeout_profile", lambda j: ec(j, timeout_profile="slow")),
        ("timeout_profile_source", lambda j: ec(j, timeout_profile_source="invocation")),
        ("max_output_chars", lambda j: ec(j, max_output_chars=1234)),
        ("max_output_chars_source", lambda j: ec(j, max_output_chars_source="invocation")),
        ("stream_evidence", lambda j: ec(j, stream_evidence=True)),
        ("stream_evidence_source", lambda j: ec(j, stream_evidence_source="invocation")),
        ("max_tasks", lambda j: ec(j, max_tasks=3)),
        ("max_tasks_source", lambda j: ec(j, max_tasks_source="invocation")),
        # --- job-level material inputs ---
        ("job_title", lambda j: setattr(j, "job_title", "different")),
        ("job_file_sha256", lambda j: setattr(j, "job_file_sha256", "e" * 64)),
        ("isolation_mode", lambda j: setattr(j, "isolation_mode", "in_place")),
        # --- task material inputs ---
        ("task.title", lambda j: setattr(j.tasks[0], "title", "changed")),
        ("task.body", lambda j: setattr(j.tasks[0], "body", "changed")),
        ("task.acceptance", lambda j: setattr(j.tasks[0], "acceptance", "changed")),
        ("task.source_heading_number",
         lambda j: setattr(j.tasks[0], "source_heading_number", 9)),
        ("task.count", lambda j: j.tasks.append(
            TaskEntry(task_id="T002", source_heading_number=2, title="x", body="y",
                      acceptance="z"))),
    ]


@pytest.mark.parametrize("label,mutate", _mutations(), ids=[m[0] for m in _mutations()])
def test_each_material_field_moves_input_identity(label, mutate):
    base = _Job()
    base_sha = _sha(base)
    mutated = _Job()
    mutate(mutated)
    assert _sha(mutated) != base_sha, f"{label} did not move job_input_sha256"


def test_no_material_field_is_silently_missing_from_definition():
    """Every ExecutionConfig field that is not obviously non-material MUST appear (by key) in
    the exported job-input definition, so a new material field cannot be added without also
    being hashed. This is the guard that the F2 gap (unhashed invocation controls) stays shut."""
    job = _Job()
    exported = build_job_input_definition(job)["execution"]
    ec_fields = {f.name for f in dataclasses.fields(ExecutionConfig)}
    # test_command is exported as a redacted identity object, not the raw string key set.
    missing = {name for name in ec_fields if name not in exported}
    # Only fields intentionally represented differently may be absent by exact key.
    allowed_absent: set[str] = set()
    assert missing <= allowed_absent, (
        f"ExecutionConfig fields not present in the hashed job-input definition: "
        f"{sorted(missing - allowed_absent)}")
