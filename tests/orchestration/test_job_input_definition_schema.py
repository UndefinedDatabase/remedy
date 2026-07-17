"""F7 — JobInputDefinitionV1 is an EXACT, complete schema (a matching hash is not enough)."""
from __future__ import annotations

import dataclasses

import pytest

import tests.orchestration.test_run_manifest as T
from packages.orchestration.manifest_schema import SchemaError
from packages.orchestration.pingpong_job import ExecutionConfig
from packages.orchestration.run_manifest import (
    JOB_INPUT_EXECUTION_FIELDS,
    build_job_input_definition,
    decode_job_input_definition_v1,
    job_input_definition_sha256,
    validate_run_manifest,
)


class TestExactSchema:
    def test_the_production_definition_decodes(self):
        decode_job_input_definition_v1(T._job_input())

    def test_minimal_definition_is_rejected_even_with_a_matching_hash(self):
        minimal = {"job_input_v": 1, "tasks": [], "execution": {}}
        with pytest.raises(SchemaError):
            decode_job_input_definition_v1(minimal)
        # ...and it is rejected through the manifest even though the hash matches its bytes
        snap = T._snap(job_input=minimal)
        m = dataclasses.replace(
            T._mk(episode_id="ep1"),
            episode_snapshot=T._wrap(snap, episode_id="ep1"),
            job_input_sha256=job_input_definition_sha256(minimal))
        assert validate_run_manifest(m), "a minimal definition passed with a matching hash"

    def test_unknown_top_level_field_is_rejected(self):
        d = T._job_input(); d["EXTRA"] = "x"
        with pytest.raises(SchemaError, match="unknown field"):
            decode_job_input_definition_v1(d)

    def test_unknown_execution_field_is_rejected(self):
        d = T._job_input(); d["execution"]["EXTRA"] = "x"
        with pytest.raises(SchemaError, match="unknown field"):
            decode_job_input_definition_v1(d)

    def test_missing_material_execution_field_is_rejected(self):
        d = T._job_input(); d["execution"].pop("timeout_sec")
        with pytest.raises(SchemaError, match="missing material field"):
            decode_job_input_definition_v1(d)

    def test_wrong_material_execution_type_is_rejected(self):
        d = T._job_input(); d["execution"]["timeout_sec"] = "120"
        with pytest.raises(SchemaError):
            decode_job_input_definition_v1(d)

    def test_wrong_boolean_execution_type_is_rejected(self):
        d = T._job_input(); d["execution"]["stream_evidence"] = "false"
        with pytest.raises(SchemaError):
            decode_job_input_definition_v1(d)

    def test_unknown_task_field_is_rejected(self):
        d = T._job_input(); d["tasks"][0]["EXTRA"] = 1
        with pytest.raises(SchemaError):
            decode_job_input_definition_v1(d)

    def test_unknown_test_command_field_is_rejected(self):
        d = T._job_input(); d["execution"]["test_command"]["EXTRA"] = "x"
        with pytest.raises(SchemaError):
            decode_job_input_definition_v1(d)


class TestExecutionConfigLockstepGuard:
    def test_every_execution_config_field_is_in_the_hashed_definition(self):
        """F7: a future MATERIAL ExecutionConfig field cannot be added without updating the
        F012 hashed definition — this guard fails loudly if the two drift apart."""
        ec_fields = {f.name for f in dataclasses.fields(ExecutionConfig)}
        missing = sorted(ec_fields - set(JOB_INPUT_EXECUTION_FIELDS))
        assert missing == [], (
            f"ExecutionConfig fields absent from the hashed JobInputDefinition: {missing}")

    def test_the_schema_declares_nothing_the_builder_does_not_emit(self):
        emitted = set(build_job_input_definition(_Job())["execution"])
        assert set(JOB_INPUT_EXECUTION_FIELDS) == emitted


class _Job:
    job_id = "j"
    job_title = "t"
    job_file_sha256 = "f" * 64
    isolation_mode = "worktree"
    execution_config = ExecutionConfig()

    def __init__(self):
        from packages.orchestration.pingpong_job import TaskEntry
        self.tasks = [TaskEntry(task_id="T001", source_heading_number=1, title="a",
                                body="b", acceptance="c")]
