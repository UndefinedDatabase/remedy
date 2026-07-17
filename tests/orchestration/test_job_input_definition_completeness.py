"""F6/F7 (round 9) — the embedded JobInputDefinition is COMPLETE, and redundant facts AGREE.

The definition is what `--check-manifest` reconstructs against, so an absent field is not a
harmless gap: it is a material input Remedy silently stopped comparing. A matching hash proves
the bytes were not tampered with — it says nothing about whether the definition describes the
whole input set. So every required fact must be PRESENT and well-formed, not merely
hash-consistent.

F7: where the same fact is recorded twice (the job file identity, a role's provider/model), the
copies must AGREE. A contradiction is an integrity error, because at most one of them can be the
input that actually ran.
"""
from __future__ import annotations

import copy
import dataclasses

import pytest

import tests.orchestration.test_run_manifest as T
from packages.orchestration import manifest_schema as _S
from packages.orchestration.run_manifest import (
    JOB_INPUT_EXECUTION_FIELDS,
    JOB_INPUT_TOP_FIELDS,
    VALID_ISOLATION_MODES,
    decode_job_input_definition_v1,
    validate_input_snapshot,
)


def _d(**over):
    d = copy.deepcopy(T._job_input())
    d.update(over)
    return d


# --------------------------------------------------------------------------- completeness


class TestRequiredFactsArePresent:
    def test_the_production_definition_is_complete(self):
        decode_job_input_definition_v1(T._job_input())      # the real builder's output

    @pytest.mark.parametrize("field", sorted(JOB_INPUT_TOP_FIELDS))
    def test_every_top_level_field_is_required(self, field):
        d = _d()
        d.pop(field)
        with pytest.raises(_S.SchemaError):
            decode_job_input_definition_v1(d)

    @pytest.mark.parametrize("field", ["job_title_sha256", "job_file_sha256"])
    def test_an_empty_identity_hash_is_not_a_valid_definition(self, field):
        """The bug: an empty required hash passed because the definition's own hash matched."""
        with pytest.raises(_S.SchemaError):
            decode_job_input_definition_v1(_d(**{field: ""}))

    @pytest.mark.parametrize("field", ["job_title_sha256", "job_file_sha256"])
    def test_a_malformed_identity_hash_is_rejected(self, field):
        with pytest.raises(_S.SchemaError):
            decode_job_input_definition_v1(_d(**{field: "NOTAHASH"}))

    def test_isolation_mode_must_come_from_the_real_vocabulary(self):
        with pytest.raises(_S.SchemaError):
            decode_job_input_definition_v1(_d(isolation_mode="teleport"))

    def test_an_empty_isolation_mode_is_rejected(self):
        with pytest.raises(_S.SchemaError):
            decode_job_input_definition_v1(_d(isolation_mode=""))

    def test_the_isolation_vocabulary_matches_production(self):
        """The vocabulary is the JobPlan's real one — not a list invented by the schema."""
        from packages.orchestration.pingpong_job import JobPlan
        assert JobPlan().isolation_mode in VALID_ISOLATION_MODES

    def test_tasks_must_be_a_typed_list_of_objects(self):
        with pytest.raises(_S.SchemaError):
            decode_job_input_definition_v1(_d(tasks=["T001"]))

    def test_a_task_missing_a_content_hash_is_rejected(self):
        d = _d()
        d["tasks"][0].pop("body_sha256")
        with pytest.raises(_S.SchemaError):
            decode_job_input_definition_v1(d)

    @pytest.mark.parametrize("field", sorted(JOB_INPUT_EXECUTION_FIELDS))
    def test_every_material_execution_field_is_required(self, field):
        d = _d()
        d["execution"].pop(field)
        with pytest.raises(_S.SchemaError) as exc:
            decode_job_input_definition_v1(d)
        assert "execution" in str(exc.value)

    def test_an_empty_execution_block_is_rejected_even_with_a_matching_hash(self):
        from packages.orchestration.run_manifest import job_input_definition_sha256
        d = _d(execution={})
        job_input_definition_sha256(d)          # the hash is computable — and irrelevant
        with pytest.raises(_S.SchemaError):
            decode_job_input_definition_v1(d)

    def test_unknown_fields_are_refused(self):
        with pytest.raises(_S.SchemaError):
            decode_job_input_definition_v1(_d(SMUGGLED="x"))

    def test_an_unknown_execution_field_is_refused(self):
        d = _d()
        d["execution"]["SMUGGLED"] = "x"
        with pytest.raises(_S.SchemaError):
            decode_job_input_definition_v1(d)


# --------------------------------------------------------------------------- safety


class TestTestCommandIsStoredSafely:
    def test_the_test_command_is_a_redacted_identity_object(self):
        d = _d()
        d["execution"]["test_command"] = "pytest -q"        # raw string, not an identity
        with pytest.raises(_S.SchemaError):
            decode_job_input_definition_v1(d)

    def test_a_leaked_secret_in_the_redacted_command_is_refused(self):
        d = _d()
        d["execution"]["test_command"]["redacted"] = "TOKEN=ghp_averyrealtokenvalue pytest"
        with pytest.raises(_S.SchemaError):
            decode_job_input_definition_v1(d)

    def test_a_leaked_local_path_is_refused(self):
        d = _d()
        d["execution"]["test_command"]["redacted"] = "/home/someone/secret/run.sh"
        with pytest.raises(_S.SchemaError):
            decode_job_input_definition_v1(d)

    def test_a_missing_command_hash_is_refused(self):
        d = _d()
        d["execution"]["test_command"]["sha256"] = ""
        with pytest.raises(_S.SchemaError):
            decode_job_input_definition_v1(d)


# --------------------------------------------------------------------------- F7 crosschecks


class TestRedundantFactsMustAgree:
    def test_the_clean_snapshot_agrees_with_itself(self):
        assert validate_input_snapshot(T._snap()) == []

    def test_a_contradictory_job_file_identity_is_an_integrity_error(self):
        """The snapshot records the job file's hash; so does the definition. If they disagree,
        at most one of them is the file that ran — that is corruption, not a warning."""
        s = dataclasses.replace(T._snap(), job_file_sha256="a" * 64)   # definition says "f"*64
        probs = validate_input_snapshot(s)
        assert any("job_file_sha256" in p for p in probs), probs

    @pytest.mark.parametrize("role", ["builder", "reviewer"])
    def test_a_contradictory_role_provider_is_an_integrity_error(self, role):
        s = dataclasses.replace(T._snap(),
                                models={**T._snap().models, role: "some-other-provider"})
        probs = validate_input_snapshot(s)
        assert any(f"models.{role} provider" in p for p in probs), probs

    @pytest.mark.parametrize("role", ["builder", "reviewer"])
    def test_a_contradictory_role_model_is_an_integrity_error(self, role):
        """A PINNED model recorded two ways must agree."""
        ji = copy.deepcopy(T._job_input())
        ji["execution"][f"{role}_model"] = "qwen3:8b"
        s = dataclasses.replace(T._snap(), job_input=ji,
                                models={**T._snap().models, role: "fake/some-other-model"})
        probs = validate_input_snapshot(s)
        assert any(f"execution.{role}_model" in p for p in probs), probs

    @pytest.mark.parametrize("role", ["builder", "reviewer"])
    def test_an_agreeing_pinned_model_is_accepted(self, role):
        ji = copy.deepcopy(T._job_input())
        ji["execution"][f"{role}_model"] = "qwen3:8b"
        s = dataclasses.replace(T._snap(), job_input=ji,
                                models={**T._snap().models, role: "fake/qwen3:8b"})
        assert validate_input_snapshot(s) == []

    def test_an_unset_declared_model_is_not_a_contradiction(self):
        """No declared model means "the provider default" — there is no second fact to
        contradict, and inventing a failure there would be a false integrity error."""
        assert validate_input_snapshot(T._snap()) == []

    def test_agreement_holds_on_a_real_run(self, data_root, repo):
        """Production must satisfy its own crosschecks — the rule is not test-only."""
        from packages.orchestration.pingpong_job import job_evidence_dir
        from packages.orchestration.run_manifest import load_latest_manifest_verified

        job_id, _res = T._run(T._JOB, repo)
        ref = load_latest_manifest_verified(job_evidence_dir(job_id), job_id=job_id)
        snap = ref.episode_snapshot.input
        assert validate_input_snapshot(snap) == []
        assert snap.job_file_sha256 == snap.job_input["job_file_sha256"]


data_root = T.data_root
repo = T.repo
