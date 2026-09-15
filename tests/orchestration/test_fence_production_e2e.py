"""F017 real production E2E — job_fulfillment, do_continue, CLI fences.

Calls the actual run_job_fulfill() and run_do_continue() entry points and the
fences section of `job show --full` with persisted jobs and fixtures. No mocks
of fence enforcement.
"""
from __future__ import annotations

import json
from uuid import uuid4

import pytest

from packages.core.models import Artifact, ArtifactKind, JobFences, RunState
from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan

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
    job = JobPlan(job_title=name, fences=fences, metadata={"target_repo": str(repo.resolve())})
    save_job_plan(job, root=data_dir)
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
        record = self._run(job.job_id, repo, data_dir)
        assert record.stop_reason == "fence_violation"
        assert record.applied_to_target is False
        assert not record.changed_target_files
        target = repo / "docs" / "CHANGES.md"
        assert not target.exists()

    def test_project_config_deny_blocks_fulfillment(self, env, monkeypatch):
        data_dir, repo = env
        monkeypatch.setenv("REMEDY_SCOPE_DENY", "docs/**")
        job = _make_job(data_dir, repo)
        record = self._run(job.job_id, repo, data_dir)
        assert record.stop_reason == "fence_violation"
        assert record.applied_to_target is False

    def test_env_deny_blocks_fulfillment(self, env, monkeypatch):
        data_dir, repo = env
        monkeypatch.setenv("REMEDY_SCOPE_DENY", "docs/**")
        job = _make_job(data_dir, repo)
        record = self._run(job.job_id, repo, data_dir)
        assert record.stop_reason == "fence_violation"
        assert record.applied_to_target is False
        target = repo / "docs" / "CHANGES.md"
        assert not target.exists()

    def test_fence_artifact_exists_after_violation(self, env):
        data_dir, repo = env
        fences = JobFences(deny=["docs/**"])
        job = _make_job(data_dir, repo, fences=fences)
        self._run(job.job_id, repo, data_dir)
        artifacts = list(data_dir.rglob("fence_violations_*.json"))
        assert len(artifacts) >= 1
        data = json.loads(artifacts[0].read_text())
        assert data["schema"] == "fence_violations/v2"
        assert data["job_id"] == str(job.job_id)
        assert data["applicator"] == "job_fulfillment"

    def test_allowed_write_not_blocked_by_fences(self, env):
        data_dir, repo = env
        job = _make_job(data_dir, repo)
        record = self._run(job.job_id, repo, data_dir)
        assert record.stop_reason != "fence_violation"


# ═══════════════════════════════════════════════════════════════════════════
# do_continue fence enforcement
# ═══════════════════════════════════════════════════════════════════════════


class TestDoContinueFenceEnforcement:
    """run_do_continue(): fence violation → FENCE_VIOLATION stop, no apply."""

    def _make_continue_job(self, data_dir, repo, *, deny=None, target_path="docs/CHANGES.md"):
        import dataclasses

        from packages.orchestration.approval_queue import make_intent_id, set_approval_state
        from packages.orchestration.permissions import Capability, set_permission
        from packages.orchestration.run_contract import ContractAction, build_default_run_contract, save_contract

        fences = JobFences(deny=deny) if deny else None
        task = TaskEntry(title="Continue task")
        content = "Summary:\n  - safe doc\nProposed Changes:\n  - add a line\nNotes:\n  - none\n"
        explanations = [
            {"file": target_path, "action": "create", "risk": "low",
             "reason": "", "summary": "safe doc"}
        ]
        art = Artifact(
            name="build", content=content, kind=ArtifactKind.BUILDER_PROPOSAL,
            task_id=str(task.task_id),
            metadata={"patch_intent_explanations": explanations, "patch_intent_approvals": {}},
        )
        job = JobPlan(
            job_title="cont-job", user_prompt="continue", state=RunState.RUNNING,
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
        save_job_plan(job, root=data_dir)
        return job, intent_id

    def test_denied_intent_produces_fence_violation(self, env):
        data_dir, repo = env
        from packages.orchestration.do_continue import ContinueRequest, ContinueStopReason, run_do_continue
        job, iid = self._make_continue_job(data_dir, repo, deny=["docs/**"])
        result = run_do_continue(ContinueRequest(job_id=str(job.job_id), intent_id=iid), data_dir=data_dir)
        assert result.stop_reason == ContinueStopReason.FENCE_VIOLATION
        target = repo / "docs" / "CHANGES.md"
        assert not target.exists()

    def test_fence_violation_not_apply_failed(self, env):
        data_dir, repo = env
        from packages.orchestration.do_continue import ContinueRequest, ContinueStopReason, run_do_continue
        job, iid = self._make_continue_job(data_dir, repo, deny=["docs/**"])
        result = run_do_continue(ContinueRequest(job_id=str(job.job_id), intent_id=iid), data_dir=data_dir)
        assert result.stop_reason == ContinueStopReason.FENCE_VIOLATION
        assert result.stop_reason != ContinueStopReason.APPLY_FAILED

    def test_fence_artifact_written_on_violation(self, env):
        data_dir, repo = env
        from packages.orchestration.do_continue import ContinueRequest, run_do_continue
        job, iid = self._make_continue_job(data_dir, repo, deny=["docs/**"])
        run_do_continue(ContinueRequest(job_id=str(job.job_id), intent_id=iid), data_dir=data_dir)
        artifacts = list(data_dir.rglob("fence_violations_*.json"))
        assert len(artifacts) >= 1

    def test_env_deny_blocks_continue(self, env, monkeypatch):
        data_dir, repo = env
        monkeypatch.setenv("REMEDY_SCOPE_DENY", "docs/**")
        from packages.orchestration.do_continue import ContinueRequest, ContinueStopReason, run_do_continue
        job, iid = self._make_continue_job(data_dir, repo)
        result = run_do_continue(ContinueRequest(job_id=str(job.job_id), intent_id=iid), data_dir=data_dir)
        assert result.stop_reason == ContinueStopReason.FENCE_VIOLATION


# ═══════════════════════════════════════════════════════════════════════════
# CLI: the fences section of remedy job show <id> --full
# ═══════════════════════════════════════════════════════════════════════════


class TestCLIJobFences:
    """The ``fences`` section of `job show --full` (formerly `job fences`): text + JSON on real jobs."""

    def _show(self, capsys, job_id_str):
        from apps.cli.grouped import main
        main(["job", "show", job_id_str, "--full"])
        shown = capsys.readouterr()
        text = shown.err.split("--- Fences ---\n", 1)[1].split("\n\n--- ", 1)[0]
        return json.loads(shown.out)["sections"]["fences"], text

    def _data(self, capsys, job_id_str):
        section, _text = self._show(capsys, job_id_str)
        assert section["ok"] is True, section
        return section["data"]

    def test_human_output_shows_builtin_rules(self, env, capsys):
        data_dir, repo = env
        job = _make_job(data_dir, repo)
        _section, output = self._show(capsys, str(job.job_id))
        assert "Builtin rules:" in output
        assert ".git/" in output

    def test_json_output_has_builtin_rules(self, env, capsys):
        data_dir, repo = env
        job = _make_job(data_dir, repo)
        data = self._data(capsys, str(job.job_id))
        assert data["job_id"] == str(job.job_id)
        assert "builtin_rules" in data
        assert any(r["pattern"] == ".git/" for r in data["builtin_rules"])

    def test_per_job_rules_appear(self, env, capsys):
        data_dir, repo = env
        fences = JobFences(allow=["src/**"], deny=["tests/**"])
        job = _make_job(data_dir, repo, fences=fences)
        data = self._data(capsys, str(job.job_id))
        assert any(r["pattern"] == "src/**" for r in data["allow_rules"])
        assert any(r["pattern"] == "tests/**" for r in data["deny_rules"])
        assert any(r["source"] == "per_job" for r in data["allow_rules"])

    def test_env_rules_appear(self, env, monkeypatch, capsys):
        data_dir, repo = env
        monkeypatch.setenv("REMEDY_SCOPE_DENY", "secret/**")
        job = _make_job(data_dir, repo)
        data = self._data(capsys, str(job.job_id))
        assert any(r["pattern"] == "secret/**" for r in data["deny_rules"])
        assert any(r["source"] == "environment" for r in data["deny_rules"])

    def test_project_config_rules_appear(self, env, capsys):
        data_dir, repo = env
        config = repo / "remedy.toml"
        config.write_text('[remedy.scope]\ndeny = ["vendor/**"]\n')
        job = _make_job(data_dir, repo)
        data = self._data(capsys, str(job.job_id))
        assert any(r["pattern"] == "vendor/**" for r in data["deny_rules"])
        assert any(r["source"] == "project" for r in data["deny_rules"])

    def test_dynamic_builtin_rule_present(self, env, capsys):
        data_dir, repo = env
        job = _make_job(data_dir, repo)
        data = self._data(capsys, str(job.job_id))
        builtins = [r["pattern"] for r in data["builtin_rules"]]
        assert ".git/" in builtins
        assert any(r["source"] in ("builtin", "dynamic_builtin") for r in data["builtin_rules"])

    def test_unknown_job_exits(self, env, capsys):
        with pytest.raises(SystemExit) as exc_info:
            self._show(capsys, str(uuid4()))
        assert exc_info.value.code == 1

    def test_missing_target_repo_is_a_no_target_repo_error(self, env, capsys):
        data_dir, repo = env
        job = JobPlan(job_title="no-repo")
        save_job_plan(job, root=data_dir)
        section, text = self._show(capsys, str(job.job_id))
        message = f"Job {str(job.job_id)[:8]} has no target_repo attached"
        assert section == {"ok": False, "error": {"code": "no_target_repo", "message": message}}
        assert text == f"  Error: no_target_repo: {message}"

    def test_a_target_repo_that_is_gone_is_a_target_repo_missing_error(self, env, capsys):
        data_dir, repo = env
        gone = repo.parent / "gone"
        job = _make_job(data_dir, gone)
        section, _text = self._show(capsys, str(job.job_id))
        message = f"Target repo does not exist: {gone.resolve()}"
        assert section == {"ok": False, "error": {"code": "target_repo_missing", "message": message}}

    def test_malformed_config_is_a_fence_config_error(self, env, capsys):
        data_dir, repo = env
        config = repo / "remedy.toml"
        config.write_text('[remedy.scope]\ndeny = 42\n')
        job = _make_job(data_dir, repo)
        section, _text = self._show(capsys, str(job.job_id))
        assert section["ok"] is False
        assert section["error"]["code"] == "fence_config_error"
        assert section["error"]["message"].startswith("Fence config error: ")

    def test_a_builtin_resolution_failure_is_its_own_error(self, env, capsys, monkeypatch):
        from packages.orchestration import scope_fences
        data_dir, repo = env
        job = _make_job(data_dir, repo)

        def cannot_resolve(worktree_root):
            raise RuntimeError("data root unresolvable")

        monkeypatch.setattr(scope_fences, "resolve_effective_builtins", cannot_resolve)
        section, _text = self._show(capsys, str(job.job_id))
        message = "Builtin resolution failed: data root unresolvable"
        assert section == {"ok": False, "error": {"code": "builtin_resolution_failed", "message": message}}

    def test_allow_list_provenance_in_output(self, env, capsys):
        data_dir, repo = env
        fences = JobFences(allow=["src/**", "lib/**"])
        job = _make_job(data_dir, repo, fences=fences)
        data = self._data(capsys, str(job.job_id))
        assert len(data["allow_rules"]) == 2
        for r in data["allow_rules"]:
            assert r["source"] == "per_job"

    def test_cli_result_matches_enforce_result(self, env, capsys):
        from packages.orchestration.scope_fences import resolve_fence_spec_effective
        data_dir, repo = env
        fences = JobFences(allow=["src/**"], deny=["build/**"])
        job = _make_job(data_dir, repo, fences=fences)
        cli_data = self._data(capsys, str(job.job_id))
        eff = resolve_fence_spec_effective(
            repo, job_fences={"allow": fences.allow, "deny": fences.deny})
        assert cli_data["source"] == eff.source
        assert len(cli_data["allow_rules"]) == len(eff.allow_rules)
        assert len(cli_data["deny_rules"]) == len(eff.deny_rules)
        assert len(cli_data["builtin_rules"]) == len(eff.builtin_rules)
