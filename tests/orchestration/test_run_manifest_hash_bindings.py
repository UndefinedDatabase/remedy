"""F5/F6/F7/F8/F9/F10 — the hash bindings and the strict semantic schema."""
from __future__ import annotations

import dataclasses

import pytest

import tests.orchestration.test_run_manifest as T
from packages.orchestration.call_identity import CallIdentity, prepare_call_input
from packages.orchestration.run_manifest import (
    CallCoverage,
    FinalizedCall,
    validate_input_snapshot,
    validate_run_manifest,
)


def _mk(**over):
    return dataclasses.replace(T._mk(episode_id="ep1"), **over)


# --------------------------------------------------------------------------- F6


class TestJobInputHashBinding:
    def test_tampered_hash_blocks(self):
        m = _mk(job_input_sha256="0" * 64)
        assert any("job_input_sha256 does not match" in p for p in validate_run_manifest(m))

    @pytest.mark.parametrize("mutate", [
        lambda d: d.__setitem__("job_title_sha256", "b" * 64),
        lambda d: d.__setitem__("isolation_mode", "in_place"),
        lambda d: d["tasks"][0].__setitem__("body_sha256", "c" * 64),
        lambda d: d["tasks"].append({"order": 1, "task_id": "T002",
                                     "source_heading_number": 2, "title_sha256": "d" * 64,
                                     "body_sha256": "d" * 64, "acceptance_sha256": "d" * 64}),
        lambda d: d["execution"].__setitem__("max_rounds", 9),
    ])
    def test_mutating_the_definition_without_the_hash_blocks(self, mutate):
        ji = T._job_input()
        mutate(ji)
        snap = T._snap(job_input=ji)
        # keep the ORIGINAL (now stale) hash
        m = dataclasses.replace(T._mk(episode_id="ep1"),
                                episode_snapshot=T._wrap(snap, episode_id="ep1"))
        assert any("job_input_sha256 does not match" in p for p in validate_run_manifest(m))

    def test_invalid_definition_blocks(self):
        ji = T._job_input()
        ji["execution"]["builder_source"] = "wat"
        m = dataclasses.replace(T._mk(episode_id="ep1"),
                                episode_snapshot=T._wrap(T._snap(job_input=ji),
                                                         episode_id="ep1"))
        assert any("invalid source" in p for p in validate_run_manifest(m))


# --------------------------------------------------------------------------- F7


class TestPreparedInputBinding:
    def test_fingerprint_mismatch_blocks(self):
        c = T._call()
        bad = dataclasses.replace(c, fingerprint="0" * 64)
        m = _mk(calls=(bad,))
        assert any("fingerprint" in p for p in validate_run_manifest(m))

    def test_tampered_prepared_component_blocks(self):
        c = T._call()
        pi = dict(c.prepared_input)
        pi["model"] = "sneaky"                 # fingerprint no longer recomputes
        m = _mk(calls=(dataclasses.replace(c, prepared_input=pi),))
        assert any("does not match its recorded components" in p
                   for p in validate_run_manifest(m))

    def test_malformed_prompt_hash_blocks(self):
        c = T._call()
        pi = dict(c.prepared_input)
        pi["prompt_sha256"] = "nope"
        m = _mk(calls=(dataclasses.replace(c, prepared_input=pi),))
        assert any("prompt_sha256" in p for p in validate_run_manifest(m))

    def test_unsupported_mode_blocks(self):
        prepared = prepare_call_input(prompt="p", model="m", mode="wat", options={})
        c = dataclasses.replace(T._call(), fingerprint=prepared.fingerprint,
                                prepared_input=prepared.to_json())
        assert any("transport mode" in p for p in validate_run_manifest(_mk(calls=(c,))))


# --------------------------------------------------------------------------- F8/F9


class TestPublishedCallsAndIdentities:
    def test_published_call_without_artifact_blocks(self):
        m = _mk()                                    # calls have no artifact bound yet
        assert any("has no artifact ref" in p
                   for p in validate_run_manifest(m, published=True))

    def test_unbound_call_is_allowed_pre_publication(self):
        assert not any("artifact" in p
                       for p in validate_run_manifest(_mk(), published=False))

    @pytest.mark.parametrize("field,value", [
        ("role", "../evil"), ("kind", "a/b"), ("task_id", "../x"),
        ("run_id", "a/b"), ("job_id", ".."),
    ])
    def test_unsafe_identity_blocks(self, field, value):
        c = T._call()
        ident = dataclasses.replace(c.identity, **{field: value})
        m = _mk(calls=(dataclasses.replace(c, identity=ident),))
        assert validate_run_manifest(m), f"{field}={value!r} was accepted"


# --------------------------------------------------------------------------- F10


class TestCoverageEnum:
    def test_garbage_status_blocks(self):
        m = _mk(coverage=CallCoverage(status="garbage"))
        assert any("invalid coverage status" in p for p in validate_run_manifest(m))

    def test_complete_with_problems_blocks(self):
        m = _mk(coverage=CallCoverage(status="complete", problems=("x",)))
        assert any("complete yet declares problems" in p for p in validate_run_manifest(m))

    def test_incomplete_without_problems_blocks(self):
        m = _mk(coverage=CallCoverage(status="incomplete", problems=()))
        assert any("incomplete yet declares no problem" in p
                   for p in validate_run_manifest(m))


# --------------------------------------------------------------------------- F5


class TestSnapshotSafety:
    def test_clean_snapshot_passes(self):
        assert validate_input_snapshot(T._snap()) == []

    def test_dirty_contradiction_blocks(self):
        s = T._snap(remedy_dirty=True)            # worktree.dirty is False
        assert any("remedy_dirty contradicts" in p for p in validate_input_snapshot(s))

    def test_remedy_sha_head_contradiction_blocks(self):
        s = T._snap(remedy_git_sha="9" * 40)
        assert any("remedy_git_sha contradicts" in p for p in validate_input_snapshot(s))

    def test_target_head_contradiction_blocks(self):
        s = T._snap(target_head="9" * 40)
        assert any("target_head contradicts" in p for p in validate_input_snapshot(s))

    def test_target_tree_digest_contradiction_blocks(self):
        s = T._snap(target_tree="9" * 64)
        assert any("target_tree contradicts" in p for p in validate_input_snapshot(s))

    def test_empty_worktree_status_blocks(self):
        s = T._snap(remedy_worktree={"head": "a" * 40, "digest": "aa" * 32,
                                     "problems": [], "dirty": False})
        assert any("status" in p for p in validate_input_snapshot(s))

    def test_raw_secret_config_value_blocks(self):
        s = T._snap(config=[{"key": "api_token", "value": "sk-ant-SUPERSECRETKEY123456",
                             "source": "env"}])
        assert any("secret" in p for p in validate_input_snapshot(s))

    def test_raw_secret_environment_value_blocks(self):
        s = T._snap(environment=[{"key": "REMEDY_API_TOKEN",
                                  "value": "sk-ant-SUPERSECRETKEY123456"}])
        assert any("secret" in p or "redacted" in p for p in validate_input_snapshot(s))

    def test_absolute_path_config_value_blocks(self):
        s = T._snap(config=[{"key": "path", "value": "/home/alice/private", "source": "env"}])
        assert any("local path" in p for p in validate_input_snapshot(s))

    def test_absolute_path_provider_version_blocks(self):
        s = T._snap(provider_versions={"fake": "/home/alice/bin/thing 1.0"})
        assert any("local path" in p for p in validate_input_snapshot(s))

    def test_redacted_values_are_safe(self):
        s = T._snap(config=[{"key": "api_token", "value": "[REDACTED]", "source": "env"}],
                    environment=[{"key": "REMEDY_DATA_DIR", "value": "[runtime-data]/."}])
        assert validate_input_snapshot(s) == []
