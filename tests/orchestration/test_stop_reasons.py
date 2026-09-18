"""Tests: builder failure taxonomy and stop reasons."""
from __future__ import annotations

import json

from packages.orchestration.builder_models import BuilderOutput


class TestBridgeStopReasons:
    def _run_bridge(self, tmp_path, monkeypatch, *, patch_text, autonomy=4):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from packages.orchestration.builder_bridge import run_builder_bridge
        from packages.orchestration.pingpong_job import JobPlan

        repo = tmp_path / "repo"
        repo.mkdir(exist_ok=True)
        (repo / "tests").mkdir(exist_ok=True)
        output = BuilderOutput(
            summary="Test", proposed_changes=["Fix"],
            structured_patch_text=patch_text,
        )
        job = JobPlan(job_title="test")
        return run_builder_bridge(
            output, repo, job=job, data_dir=tmp_path / "data",
            autonomy_level=autonomy,
        )

    def test_prose_output_gives_prose_stop_reason(self, tmp_path, monkeypatch):
        result = self._run_bridge(
            tmp_path, monkeypatch,
            patch_text="I think you should change the function.",
        )
        assert result.stop_reason == "provider_output_prose_only"
        assert result.stage == "parse_failed"

    def test_shell_command_gives_unsafe_stop_reason(self, tmp_path, monkeypatch):
        result = self._run_bridge(
            tmp_path, monkeypatch,
            patch_text="rm -rf /tmp/foo",
        )
        assert result.stop_reason == "unsafe_shell_command"

    def test_no_text_gives_no_text_stop_reason(self, tmp_path, monkeypatch):
        result = self._run_bridge(
            tmp_path, monkeypatch, patch_text=None,
        )
        assert result.stop_reason == "no_structured_patch_text"

    def test_path_traversal_gives_validation_stop_reason(self, tmp_path, monkeypatch):
        patch = json.dumps({
            "file_ops": [{"path": "../../etc/passwd", "action": "modify", "content": "x\n"}]
        })
        result = self._run_bridge(tmp_path, monkeypatch, patch_text=patch)
        assert result.stop_reason == "validation_failed"

    def test_approval_pending_gives_approval_stop_reason(self, tmp_path, monkeypatch):
        patch = json.dumps({
            "file_ops": [{"path": "a.py", "action": "create", "content": "x\n"}]
        })
        result = self._run_bridge(
            tmp_path, monkeypatch, patch_text=patch, autonomy=2,
        )
        assert result.stop_reason == "approval_required"
        assert result.stage == "approval_pending"

    def test_test_failure_gives_test_failed_stop_reason(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from packages.orchestration.builder_bridge import run_builder_bridge
        from packages.orchestration.pingpong_job import JobPlan

        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "tests").mkdir()
        (repo / "tests" / "test_fail.py").write_text(
            "def test_always_fail():\n    assert False\n",
        )
        patch = json.dumps({
            "file_ops": [{"path": "app.py", "action": "create", "content": "x = 1\n"}]
        })
        output = BuilderOutput(
            summary="Fix", proposed_changes=["Fix"],
            structured_patch_text=patch,
        )
        job = JobPlan(job_title="test")
        result = run_builder_bridge(
            output, repo, job=job, data_dir=tmp_path / "data",
            autonomy_level=4,
        )
        assert result.stop_reason == "test_failed_after_apply"
        assert result.test_passed is False


class TestLoopStopReasons:
    def test_budget_exhausted_stop_reason(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from packages.orchestration.builder_bridge import run_builder_bridge_loop
        from packages.orchestration.pingpong_job import JobPlan, save_job_plan

        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "app.py").write_text("x = 0\n")
        (repo / "tests").mkdir()
        (repo / "tests" / "test_fail.py").write_text(
            "def test_always_fail():\n    assert False\n",
        )
        cycle_counter = [0]

        def build_fn(ctx):
            cycle_counter[0] += 1
            patch = json.dumps({
                "file_ops": [{"path": "app.py", "action": "modify",
                              "content": f"x = {cycle_counter[0]}\n"}]
            })
            return BuilderOutput(
                summary="Fix", proposed_changes=["Fix"],
                structured_patch_text=patch,
            )

        job = JobPlan(job_title="test")
        save_job_plan(job)
        result = run_builder_bridge_loop(
            build_fn, repo, job=job, data_dir=tmp_path / "data",
            max_cycles=2,
        )
        assert result.stop_reason == "repair_budget_exhausted"
        assert result.success is False
        assert result.cycles_run == 2

    def test_repeated_patch_stop_reason(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        from packages.orchestration.builder_bridge import run_builder_bridge_loop
        from packages.orchestration.pingpong_job import JobPlan, save_job_plan

        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "tests").mkdir()
        (repo / "tests" / "test_fail.py").write_text(
            "def test_always_fail():\n    assert False\n",
        )
        same_patch = json.dumps({
            "file_ops": [{"path": "app.py", "action": "create", "content": "x = 1\n"}]
        })

        def build_fn(ctx):
            return BuilderOutput(
                summary="Fix", proposed_changes=["Fix"],
                structured_patch_text=same_patch,
            )

        job = JobPlan(job_title="test")
        save_job_plan(job)
        result = run_builder_bridge_loop(
            build_fn, repo, job=job, data_dir=tmp_path / "data",
            max_cycles=3,
        )
        assert result.stop_reason == "repeated_patch_detected"
        assert result.cycles_run <= 2


class TestDashboardStopReason:
    def test_stop_reason_in_live_state(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.builder_bridge import run_builder_bridge
        from packages.orchestration.pingpong_job import JobPlan, save_job_plan
        from packages.orchestration.ui_server import _build_live_state_json

        job = JobPlan(job_title="test")
        save_job_plan(job)

        output = BuilderOutput(
            summary="Fix", proposed_changes=["Fix"],
            structured_patch_text="I think we should modify the code.",
        )
        run_builder_bridge(output, tmp_path, job=job, data_dir=tmp_path, autonomy_level=2)

        state = _build_live_state_json(job)
        assert "stop_reason" in state
        assert state["stop_reason"] == "provider_output_prose_only"

    def test_stop_reason_empty_on_success(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.builder_bridge import run_builder_bridge
        from packages.orchestration.pingpong_job import JobPlan, save_job_plan
        from packages.orchestration.ui_server import _build_live_state_json

        job = JobPlan(job_title="test")
        save_job_plan(job)

        (tmp_path / "tests").mkdir(exist_ok=True)
        (tmp_path / "tests" / "test_x.py").write_text(
            "def test_ok():\n    assert True\n"
        )
        patch = json.dumps({
            "file_ops": [{"path": "x.py", "action": "create", "content": "x = 1\n"}]
        })
        output = BuilderOutput(
            summary="Fix", proposed_changes=["Fix"],
            structured_patch_text=patch,
        )
        run_builder_bridge(output, tmp_path, job=job, data_dir=tmp_path, autonomy_level=4)

        state = _build_live_state_json(job)
        assert state["stop_reason"] == ""


# ---------------------------------------------------------------------------
# R-0811: the no-repo tip names the real job and a real path, never a placeholder;
# since DECISION F269 D7 it names `job contract`, where a job's repository comes from
# ---------------------------------------------------------------------------

_PLACEHOLDER_RE = r"<[a-z_]+>"


def test_the_no_repo_tip_names_the_job_and_its_projects_repository(tmp_path, monkeypatch):
    import re

    from packages.orchestration.pingpong_job import JobPlan
    from packages.orchestration.project_registry import RemyProject, save_project
    from packages.orchestration.stop_reasons import derive_stop_reasons

    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    repo = tmp_path / "the-repo"
    repo.mkdir()
    project = RemyProject(name="the-repo", canonical_repo_path=str(repo))
    save_project(project)
    job = JobPlan(job_title="no repo yet", project_id=str(project.id))

    [tip] = next(r for r in derive_stop_reasons(job, [])
                 if r.id == "derived_no_repo").next_actions

    assert tip == (f"remedy job contract {job.job_id} — a job gets its repository and "
                   f"grants from its mission's contract; its project's repository is {repo}")
    for action in _every_next_action(job, []):
        assert not re.search(_PLACEHOLDER_RE, action), action
        assert str(job.job_id) in action, action


def test_the_no_repo_tip_without_a_project_names_where_the_repository_comes_from(
        tmp_path, monkeypatch):
    import re

    from packages.orchestration.pingpong_job import JobPlan
    from packages.orchestration.stop_reasons import derive_stop_reasons

    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    job = JobPlan(job_title="no project")

    [tip] = next(r for r in derive_stop_reasons(job, [])
                 if r.id == "derived_no_repo").next_actions

    assert tip == (f"remedy job contract {job.job_id} — a job gets its repository and "
                   f"grants from its mission's contract")
    for action in _every_next_action(job, []):
        assert not re.search(_PLACEHOLDER_RE, action), action
        assert str(job.job_id) in action, action


def _every_next_action(job, events) -> list[str]:
    from packages.orchestration.stop_reasons import derive_stop_reasons

    return [a for r in derive_stop_reasons(job, events) for a in r.next_actions]


def test_every_derived_next_action_names_the_real_job_and_no_placeholder(tmp_path, monkeypatch):
    """R-0811: all four derived stop reasons at once — no `<…>` anywhere, the real ids everywhere."""
    import re

    from packages.orchestration.pingpong_job import JobPlan
    from packages.orchestration.stop_reasons import derive_stop_reasons

    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    job = JobPlan(job_title="every stop at once")
    events = [
        {"event": "test_run_completed", "metadata": {"status": "failed"}},
        {"event": "patch_intent_created", "metadata": {"intent_id": "intent-a1"}},
        {"event": "patch_intent_created", "metadata": {}},
        {"event": "git_status_read", "metadata": {"dirty": True}},
    ]

    reasons = {r.id: r for r in derive_stop_reasons(job, events)}

    assert sorted(reasons) == ["derived_dirty_repo", "derived_no_repo",
                               "derived_not_approved", "derived_test_fail"]
    actions = _every_next_action(job, events)
    assert len(actions) == 6
    for action in actions:
        assert not re.search(_PLACEHOLDER_RE, action), action
        assert str(job.job_id) in action, action
    assert f"remedy test run {job.job_id}" in reasons["derived_test_fail"].next_actions
    assert reasons["derived_not_approved"].next_actions == (
        f"remedy patch approve {job.job_id} intent-a1",
        f"remedy patch list {job.job_id} names the intent ids to approve",
    )
