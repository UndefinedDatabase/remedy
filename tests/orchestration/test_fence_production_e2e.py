"""F017 real production E2E — job_fulfillment, do_continue, CLI fences.

Calls the actual run_job_fulfill(), run_do_continue(), and _cmd_job_fences()
entry points with persisted jobs and fixtures. No mocks of fence enforcement.
"""
from __future__ import annotations

import contextlib
import io
import json
import os
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from packages.core.models import (
    Artifact,
    ArtifactKind,
    Job,
    JobFences,
    RunState,
    Task,
)
from packages.orchestration.storage import save_job


# ═══════════════════════════════════════════════════════════════════════════
# Shared fixtures
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture()
def env(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "src").mkdir()
    (repo / "src" / "main.py").write_text("# main\n")
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    monkeypatch.delenv("REMEDY_SCOPE_ALLOW", raising=False)
    monkeypatch.delenv("REMEDY_SCOPE_DENY", raising=False)
    return data_dir, repo


def _make_job(data_dir, repo, *, fences=None, name="test-job"):
    job = Job(name=name, fences=fences, metadata={"target_repo": str(repo.resolve())})
    save_job(job, root=data_dir)
    return job


# ═══════════════════════════════════════════════════════════════════════════
# job_fulfillment fence enforcement
# ═══════════════════════════════════════════════════════════════════════════


class TestJobFulfillmentFenceEnforcement:
    """run_job_fulfill(): fence violation → staging discarded, nothing applied."""

    def _run(self, job_id, repo, data_dir):
        from packages.orchestration.job_fulfillment import run_job_fulfill
        return run_job_fulfill(str(job_id), repo, data_dir=data_dir)

    def test_per_job_deny_blocks_fulfillment(self, env):
        data_dir, repo = env
        fences = JobFences(deny=["docs/**"])
        job = _make_job(data_dir, repo, fences=fences)
        record = self._run(job.id, repo, data_dir)
        assert record.stop_reason == "fence_violation"
        assert record.staging_promoted is False
        assert not record.changed_target_files
        target = repo / "docs" / "CHANGES.md"
        assert not target.exists()

    def test_project_config_deny_blocks_fulfillment(self, env, monkeypatch):
        data_dir, repo = env
        monkeypatch.setenv("REMEDY_SCOPE_DENY", "docs/**")
        job = _make_job(data_dir, repo)
        record = self._run(job.id, repo, data_dir)
        assert record.stop_reason == "fence_violation"
        assert record.staging_promoted is False

    def test_env_deny_blocks_fulfillment(self, env, monkeypatch):
        data_dir, repo = env
        monkeypatch.setenv("REMEDY_SCOPE_DENY", "docs/**")
        job = _make_job(data_dir, repo)
        record = self._run(job.id, repo, data_dir)
        assert record.stop_reason == "fence_violation"
        assert record.staging_promoted is False
        target = repo / "docs" / "CHANGES.md"
        assert not target.exists()

    def test_fence_artifact_exists_after_violation(self, env):
        data_dir, repo = env
        fences = JobFences(deny=["docs/**"])
        job = _make_job(data_dir, repo, fences=fences)
        self._run(job.id, repo, data_dir)
        artifacts = list(data_dir.rglob("fence_violations_*.json"))
        assert len(artifacts) >= 1
        data = json.loads(artifacts[0].read_text())
        assert data["schema"] == "fence_violations/v2"
        assert data["job_id"] == str(job.id)
        assert data["applicator"] == "job_fulfillment"

    def test_allowed_write_not_blocked_by_fences(self, env):
        data_dir, repo = env
        job = _make_job(data_dir, repo)
        record = self._run(job.id, repo, data_dir)
        assert record.stop_reason != "fence_violation"


# ═══════════════════════════════════════════════════════════════════════════
# do_continue fence enforcement
# ═══════════════════════════════════════════════════════════════════════════


class TestDoContinueFenceEnforcement:
    """run_do_continue(): fence violation → FENCE_VIOLATION stop, no apply."""

    def _make_continue_job(self, data_dir, repo, *, deny=None, target_path="docs/CHANGES.md"):
        from packages.orchestration.approval_queue import make_intent_id, set_approval_state
        from packages.orchestration.permissions import Capability, set_permission
        from packages.orchestration.run_contract import build_default_run_contract, save_contract
        import dataclasses
        from packages.orchestration.run_contract import ContractAction

        fences = JobFences(deny=deny) if deny else None
        task = Task(description="Continue task")
        content = "Summary:\n  - safe doc\nProposed Changes:\n  - add a line\nNotes:\n  - none\n"
        explanations = [
            {"file": target_path, "action": "create", "risk": "low",
             "reason": "", "summary": "safe doc"}
        ]
        art = Artifact(
            name="build", content=content, kind=ArtifactKind.BUILDER_PROPOSAL,
            task_id=task.id,
            metadata={"patch_intent_explanations": explanations, "patch_intent_approvals": {}},
        )
        job = Job(
            name="cont-job", user_prompt="continue", state=RunState.RUNNING,
            tasks=[task], artifacts=[art], fences=fences,
            metadata={"target_repo": str(repo.resolve())},
        )
        intent_id = make_intent_id(art.id, 0)
        set_permission(job, Capability.repo_generated_write, allow=True)
        set_permission(job, Capability.repo_test_run, allow=True)
        set_approval_state(job, intent_id, "approved", decided_by="human")

        contract = build_default_run_contract(job)
        allowed = list(contract.allowed_actions)
        denied_a = [a for a in contract.denied_actions if a != ContractAction.PATCH_APPLY]
        if ContractAction.PATCH_APPLY not in allowed:
            allowed.append(ContractAction.PATCH_APPLY)
        contract = dataclasses.replace(
            contract,
            allowed_actions=tuple(allowed),
            denied_actions=tuple(denied_a),
            stop_before_apply=False,
            max_test_runs=1,
        )
        save_contract(job, contract)
        save_job(job, root=data_dir)
        return job, intent_id

    def test_denied_intent_produces_fence_violation(self, env):
        data_dir, repo = env
        from packages.orchestration.do_continue import ContinueRequest, ContinueStopReason, run_do_continue
        job, iid = self._make_continue_job(data_dir, repo, deny=["docs/**"])
        result = run_do_continue(ContinueRequest(job_id=str(job.id), intent_id=iid), data_dir=data_dir)
        assert result.stop_reason == ContinueStopReason.FENCE_VIOLATION
        target = repo / "docs" / "CHANGES.md"
        assert not target.exists()

    def test_fence_violation_not_apply_failed(self, env):
        data_dir, repo = env
        from packages.orchestration.do_continue import ContinueRequest, ContinueStopReason, run_do_continue
        job, iid = self._make_continue_job(data_dir, repo, deny=["docs/**"])
        result = run_do_continue(ContinueRequest(job_id=str(job.id), intent_id=iid), data_dir=data_dir)
        assert result.stop_reason == ContinueStopReason.FENCE_VIOLATION
        assert result.stop_reason != ContinueStopReason.APPLY_FAILED

    def test_fence_artifact_written_on_violation(self, env):
        data_dir, repo = env
        from packages.orchestration.do_continue import ContinueRequest, run_do_continue
        job, iid = self._make_continue_job(data_dir, repo, deny=["docs/**"])
        run_do_continue(ContinueRequest(job_id=str(job.id), intent_id=iid), data_dir=data_dir)
        artifacts = list(data_dir.rglob("fence_violations_*.json"))
        assert len(artifacts) >= 1

    def test_env_deny_blocks_continue(self, env, monkeypatch):
        data_dir, repo = env
        monkeypatch.setenv("REMEDY_SCOPE_DENY", "docs/**")
        from packages.orchestration.do_continue import ContinueRequest, ContinueStopReason, run_do_continue
        job, iid = self._make_continue_job(data_dir, repo)
        result = run_do_continue(ContinueRequest(job_id=str(job.id), intent_id=iid), data_dir=data_dir)
        assert result.stop_reason == ContinueStopReason.FENCE_VIOLATION


# ═══════════════════════════════════════════════════════════════════════════
# CLI: remedy job fences
# ═══════════════════════════════════════════════════════════════════════════


class TestCLIJobFences:
    """_cmd_job_fences(): human + JSON output against real persisted jobs."""

    def _run_cli(self, job_id_str, *, json_output=False):
        from apps.cli.commands.job import _cmd_job_fences
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            _cmd_job_fences(job_id_str, json_output=json_output)
        return buf.getvalue()

    def test_human_output_shows_builtin_rules(self, env):
        data_dir, repo = env
        job = _make_job(data_dir, repo)
        output = self._run_cli(str(job.id))
        assert "Builtin rules:" in output
        assert ".git/" in output

    def test_json_output_has_builtin_rules(self, env):
        data_dir, repo = env
        job = _make_job(data_dir, repo)
        output = self._run_cli(str(job.id), json_output=True)
        data = json.loads(output)
        assert "builtin_rules" in data
        assert any(r["pattern"] == ".git/" for r in data["builtin_rules"])

    def test_per_job_rules_appear(self, env):
        data_dir, repo = env
        fences = JobFences(allow=["src/**"], deny=["tests/**"])
        job = _make_job(data_dir, repo, fences=fences)
        output = self._run_cli(str(job.id), json_output=True)
        data = json.loads(output)
        assert any(r["pattern"] == "src/**" for r in data["allow_rules"])
        assert any(r["pattern"] == "tests/**" for r in data["deny_rules"])
        assert any(r["source"] == "per_job" for r in data["allow_rules"])

    def test_env_rules_appear(self, env, monkeypatch):
        data_dir, repo = env
        monkeypatch.setenv("REMEDY_SCOPE_DENY", "secret/**")
        job = _make_job(data_dir, repo)
        output = self._run_cli(str(job.id), json_output=True)
        data = json.loads(output)
        assert any(r["pattern"] == "secret/**" for r in data["deny_rules"])
        assert any(r["source"] == "environment" for r in data["deny_rules"])

    def test_project_config_rules_appear(self, env):
        data_dir, repo = env
        config = repo / "remedy.toml"
        config.write_text('[remedy.scope]\ndeny = ["vendor/**"]\n')
        job = _make_job(data_dir, repo)
        output = self._run_cli(str(job.id), json_output=True)
        data = json.loads(output)
        assert any(r["pattern"] == "vendor/**" for r in data["deny_rules"])
        assert any(r["source"] == "project" for r in data["deny_rules"])

    def test_dynamic_builtin_rule_present(self, env):
        data_dir, repo = env
        job = _make_job(data_dir, repo)
        output = self._run_cli(str(job.id), json_output=True)
        data = json.loads(output)
        builtins = [r["pattern"] for r in data["builtin_rules"]]
        assert ".git/" in builtins
        assert any(r["source"] in ("builtin", "dynamic_builtin") for r in data["builtin_rules"])

    def test_unknown_job_exits(self, env):
        with pytest.raises(SystemExit) as exc_info:
            self._run_cli(str(uuid4()))
        assert exc_info.value.code == 1

    def test_missing_target_repo_exits(self, env):
        data_dir, repo = env
        job = Job(name="no-repo")
        save_job(job, root=data_dir)
        with pytest.raises(SystemExit) as exc_info:
            self._run_cli(str(job.id))
        assert exc_info.value.code == 2

    def test_malformed_config_exits(self, env):
        data_dir, repo = env
        config = repo / "remedy.toml"
        config.write_text('[remedy.scope]\ndeny = 42\n')
        job = _make_job(data_dir, repo)
        with pytest.raises(SystemExit) as exc_info:
            self._run_cli(str(job.id))
        assert exc_info.value.code == 3

    def test_allow_list_provenance_in_output(self, env):
        data_dir, repo = env
        fences = JobFences(allow=["src/**", "lib/**"])
        job = _make_job(data_dir, repo, fences=fences)
        output = self._run_cli(str(job.id), json_output=True)
        data = json.loads(output)
        assert len(data["allow_rules"]) == 2
        for r in data["allow_rules"]:
            assert r["source"] == "per_job"

    def test_cli_result_matches_enforce_result(self, env):
        from packages.orchestration.scope_fences import resolve_fence_spec_effective
        data_dir, repo = env
        fences = JobFences(allow=["src/**"], deny=["build/**"])
        job = _make_job(data_dir, repo, fences=fences)
        cli_out = self._run_cli(str(job.id), json_output=True)
        cli_data = json.loads(cli_out)
        eff = resolve_fence_spec_effective(
            repo, job_fences={"allow": fences.allow, "deny": fences.deny})
        assert cli_data["source"] == eff.source
        assert len(cli_data["allow_rules"]) == len(eff.allow_rules)
        assert len(cli_data["deny_rules"]) == len(eff.deny_rules)
        assert len(cli_data["builtin_rules"]) == len(eff.builtin_rules)
