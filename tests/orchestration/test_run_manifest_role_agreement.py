"""F9 (round 10) — Builder, Reviewer and Repair must agree with the embedded Execution definition.

The snapshot records each role twice: once as a scalar view (`models["builder"] = "ollama/qwen"`)
and once, field by field, inside the job-input definition. Two records of one fact are only
useful if they are checked against each other — otherwise the manifest is free to say the run
used `ollama/modelB` in one breath and `claude`/`modelA` in the next, and a reader has no way to
know which one produced the evidence.

Before round 10 only Builder and Reviewer MODELS were crosschecked: role providers were never
compared, Repair was never compared at all, and `models` had no schema, so an unknown role could
sit there unnoticed.
"""
from __future__ import annotations

import copy
import dataclasses

import pytest

import tests.orchestration.test_run_manifest as T
from packages.orchestration.run_manifest import (
    OPTIONAL_MODEL_ROLES,
    REQUIRED_MODEL_ROLES,
    validate_input_snapshot,
    validate_models,
)


def _snap(models, **execution):
    ji = copy.deepcopy(T._job_input())
    ji["execution"].update(execution)
    return dataclasses.replace(T._snap(), job_input=ji, models=models)


def _problems(models, **execution):
    return validate_input_snapshot(_snap(models, **execution))


_BASE = {"builder": "fake", "reviewer": "fake"}


# --------------------------------------------------------------------------- agreement


class TestProviderAgreement:
    @pytest.mark.parametrize("role", ["builder", "reviewer"])
    def test_a_contradictory_provider_blocks(self, role):
        probs = _problems({**_BASE, role: "claude"})
        assert any(f"models.{role} provider contradicts" in p for p in probs), probs

    def test_a_contradictory_repair_provider_blocks(self):
        """THE finding: models.repair = ollama/modelB while the definition said claude/modelA."""
        probs = _problems({**_BASE, "repair": "ollama/modelB"},
                          repair_provider="claude", repair_model="modelA")
        assert any("models.repair provider contradicts" in p for p in probs), probs
        assert any("execution.repair_model" in p for p in probs), probs

    def test_agreeing_providers_pass(self):
        assert _problems(_BASE) == []

    def test_an_agreeing_repair_role_passes(self):
        assert _problems({**_BASE, "repair": "claude/modelA"},
                         repair_provider="claude", repair_model="modelA") == []

    def test_repair_provider_falls_back_to_the_builder_provider(self):
        """Production records the builder's provider when only a repair MODEL is pinned, so that
        is exactly what agreement is checked against."""
        assert _problems({**_BASE, "repair": "fake/modelA"}, repair_model="modelA") == []
        probs = _problems({**_BASE, "repair": "claude/modelA"}, repair_model="modelA")
        assert any("models.repair provider contradicts" in p for p in probs), probs


class TestModelAgreement:
    @pytest.mark.parametrize("role", ["builder", "reviewer"])
    def test_a_contradictory_pinned_model_blocks(self, role):
        probs = _problems({**_BASE, role: "fake/other"}, **{f"{role}_model": "qwen3:8b"})
        assert any(f"execution.{role}_model" in p for p in probs), probs

    @pytest.mark.parametrize("role", ["builder", "reviewer"])
    def test_an_agreeing_pinned_model_passes(self, role):
        assert _problems({**_BASE, role: "fake/qwen3:8b"},
                         **{f"{role}_model": "qwen3:8b"}) == []

    def test_an_unset_declared_model_is_not_a_contradiction(self):
        """No declared model means "the provider's default" — there is no second fact to
        contradict, and inventing a failure there would be a false integrity error."""
        assert _problems(_BASE) == []


# --------------------------------------------------------------------------- the exact schema


class TestModelsSchema:
    def test_an_unknown_role_blocks(self):
        probs = _problems({**_BASE, "wizard": "fake"})
        assert any("unknown role 'wizard'" in p for p in probs), probs

    @pytest.mark.parametrize("role", ["builder", "reviewer"])
    def test_a_missing_required_role_blocks(self, role):
        models = {k: v for k, v in _BASE.items() if k != role}
        probs = _problems(models)
        assert any(f"missing the required role {role!r}" in p for p in probs), probs

    def test_the_required_and_optional_roles_are_the_real_vocabulary(self):
        assert set(REQUIRED_MODEL_ROLES) == {"builder", "reviewer"}
        assert set(OPTIONAL_MODEL_ROLES) == {"repair"}

    def test_repair_recorded_but_not_activated_blocks(self):
        probs = _problems({**_BASE, "repair": "fake"})
        assert any("does not activate" in p for p in probs), probs

    def test_repair_activated_but_not_recorded_blocks(self):
        probs = _problems(_BASE, repair_model="modelA")
        assert any("records no repair role" in p for p in probs), probs

    def test_models_must_be_an_object(self):
        assert validate_models(["builder"], {"builder": "fake"}) == ["models is not an object"]


# --------------------------------------------------------------------------- absence semantics


class TestAbsenceIsExplicitAndSymmetric:
    def test_no_execution_config_means_no_models(self):
        """A planning-only job has no resolved execution config, so it declares no providers and
        records no models. The agreement of two absences is itself the check."""
        ji = copy.deepcopy(T._job_input())
        for f in ("builder", "reviewer"):
            ji["execution"][f] = ""
        s = dataclasses.replace(T._snap(), job_input=ji, models={})
        assert validate_input_snapshot(s) == []

    def test_a_model_recorded_for_an_undeclared_role_blocks(self):
        ji = copy.deepcopy(T._job_input())
        ji["execution"]["builder"] = ""
        s = dataclasses.replace(T._snap(), job_input=ji, models=_BASE)
        probs = validate_input_snapshot(s)
        assert any("declares no provider for it" in p for p in probs), probs


# --------------------------------------------------------------------------- production


class TestProductionAgreesWithItself:
    def test_a_real_run_satisfies_every_role_rule(self, data_root, repo):
        from packages.orchestration.pingpong_job import job_evidence_dir
        from packages.orchestration.run_manifest import load_latest_manifest_verified

        job_id, _res = T._run(T._JOB, repo)
        ref = load_latest_manifest_verified(job_evidence_dir(job_id), job_id=job_id)
        snap = ref.episode_snapshot.input
        assert validate_input_snapshot(snap) == []
        assert set(snap.models) == {"builder", "reviewer"}
        assert validate_models(snap.models, snap.job_input["execution"]) == []


data_root = T.data_root
repo = T.repo
