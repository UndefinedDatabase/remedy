"""Tests for what `packages/orchestration/do_run.py` still holds, and the `do.run` catalog entry.

Covers:
- `DoRunNextAction`, the `Next:` line contract
- `names_catalog_command`, the tests/ helper the validator moved to (R-0903), against the command catalog (Steps 926-927)
- The run contract defaults (Step 930)
- The `do.run` catalog metadata (Step 929)
- `do_run.py` imports no `source_apply` (Step 933)

The phased `remedy do` v1 flow and its tests were deleted by F268 round 10.
"""

from __future__ import annotations

from packages.orchestration.do_run import DoRunNextAction
from packages.orchestration.pingpong_job import JobPlan
from tests.orchestration.catalog_commands import names_catalog_command

# ---------------------------------------------------------------------------
# Phase model tests (Step 906)
# ---------------------------------------------------------------------------


class TestPhaseModel:

    def test_next_action(self):
        na = DoRunNextAction(label="Approve", command="remedy patch approve x y", reason="needed")
        assert "remedy" in na.command

    def test_contract_defaults(self):
        from packages.orchestration.run_contract import build_default_run_contract
        job = JobPlan(job_title="test")
        c = build_default_run_contract(job)
        assert c.stop_before_apply is True
        assert c.max_loops == 10
        assert c.autonomy_level == 1
        assert c.source == "default_v1"
        assert "plan" in c.allowed_actions
        assert "apply" in c.denied_actions


# ---------------------------------------------------------------------------
# Approval gate enforcement (Step 914 + Step 933 regression)
# ---------------------------------------------------------------------------


class TestApprovalGate:

    def test_no_apply_import_in_do_run(self):
        """Step 933: source_apply not imported in do_run."""
        import inspect

        from packages.orchestration import do_run
        src = inspect.getsource(do_run)
        assert "from packages.orchestration.source_apply import" not in src
        assert "source_apply(" not in src


# ---------------------------------------------------------------------------
# Step 926-927: Full next_safe_action catalog validation
# ---------------------------------------------------------------------------


class TestNextSafeActionValidation:

    def test_validate_real_command(self):
        """remedy patch approve -> patch.approve exists."""
        assert names_catalog_command("remedy patch approve job123 intent456") is True

    def test_validate_job_context(self):
        """remedy job context -> job.context exists."""
        assert names_catalog_command(
            "remedy job context job123 --task T001 --json") is True

    def test_validate_job_show(self):
        """remedy job show -> job.show exists."""
        assert names_catalog_command("remedy job show job123 --json") is True

    def test_validate_do_run(self):
        """remedy do run -> do.run exists."""
        assert names_catalog_command('remedy do run "goal" --json') is True

    def test_reject_fake_subcommand(self):
        """remedy patch does-not-exist -> fails."""
        assert names_catalog_command("remedy patch does-not-exist job123") is False

    def test_reject_group_only(self):
        """remedy patch -> fails (no subcommand)."""
        assert names_catalog_command("remedy patch") is False

    def test_reject_empty(self):
        assert names_catalog_command("") is False

    def test_reject_non_remedy(self):
        assert names_catalog_command("curl http://example.com") is False


# ---------------------------------------------------------------------------
# Step 929: Command catalog metadata truth
# ---------------------------------------------------------------------------


class TestCatalogMetadataTruth:

    def test_do_run_declares_repo_mutation_like_job_apply(self):
        """R-0969: `do "<order>" --apply` writes the repo through `job_apply`, so
        do.run declares may_mutate_repo exactly as job.apply does."""
        from apps.cli.command_catalog import CATALOG
        entry = next(e for e in CATALOG if e.command_id == "do.run")
        job_apply = next(e for e in CATALOG if e.command_id == "job.apply")
        assert entry.may_mutate_repo is True, \
            "do.run --apply writes the repository"
        assert entry.may_mutate_repo == job_apply.may_mutate_repo

    def test_do_run_declares_command_execution_like_job_run(self):
        """R-0965: bare `do "<order>"` runs a job through job.run's runner, so it
        declares the same execution metadata as job.run. Its may_mutate_repo
        follows job.apply instead (R-0969, the test above)."""
        from apps.cli.command_catalog import CATALOG
        entry = next(e for e in CATALOG if e.command_id == "do.run")
        job_run = next(e for e in CATALOG if e.command_id == "job.run")
        assert entry.may_execute_commands is True, \
            "do.run runs a job, which executes commands"
        assert (entry.may_execute_commands, entry.action_class) == (
            job_run.may_execute_commands, job_run.action_class)

    def test_do_run_action_class_not_apply_write(self):
        """do.run action_class should reflect data-only writes."""
        from apps.cli.command_catalog import CATALOG
        entry = next(e for e in CATALOG if e.command_id == "do.run")
        assert entry.action_class != "apply_write", \
            "v1 writes metadata only, not repo files"


# ---------------------------------------------------------------------------
# Step 930: Contract consolidation
# ---------------------------------------------------------------------------


class TestContractConsolidation:

    def test_contract_has_source(self):
        from packages.orchestration.run_contract import build_default_run_contract
        c = build_default_run_contract(JobPlan(job_title="test"))
        assert c.source == "default_v1"

    def test_contract_has_allowed_actions(self):
        from packages.orchestration.run_contract import build_default_run_contract
        c = build_default_run_contract(JobPlan(job_title="test"))
        assert len(c.allowed_actions) > 0
        assert "plan" in c.allowed_actions

    def test_contract_has_denied_actions(self):
        from packages.orchestration.run_contract import build_default_run_contract
        c = build_default_run_contract(JobPlan(job_title="test"))
        assert len(c.denied_actions) > 0
        assert "apply" in c.denied_actions


# ---------------------------------------------------------------------------
# amend0920-selfuse-real Part A: the `--planner-provider` flag and its route
# ---------------------------------------------------------------------------


class TestPlannerProviderFlag:
    """`do.run` declares the flag, and the flag reaches the Claude planner factory."""

    def _do_run_args(self):
        from apps.cli.command_catalog import CATALOG
        entry = next(e for e in CATALOG if e.command_id == "do.run")
        return {arg.name: arg for arg in entry.args}

    def test_do_run_declares_planner_provider(self):
        arg = self._do_run_args()["--planner-provider"]
        assert arg.is_option is True
        assert arg.is_flag is False, "it takes a value, it is not a boolean flag"
        assert arg.required is False
        assert arg.default is None, "default None means the configured planner role"

    def test_the_declared_choices_are_the_factory_s_own(self):
        """The help text names every planner the factory accepts, and no other."""
        from packages.orchestration.intake import PLANNER_PROVIDERS

        assert PLANNER_PROVIDERS == ("ollama", "claude-cli")
        help_text = self._do_run_args()["--planner-provider"].help
        for planner in PLANNER_PROVIDERS:
            assert planner in help_text, f"{planner} is not offered in the help"

    def test_planner_provider_sits_beside_planner_model(self):
        from apps.cli.command_catalog import CATALOG
        entry = next(e for e in CATALOG if e.command_id == "do.run")
        names = [a.name for a in entry.args]
        assert names.index("--planner-provider") == names.index("--planner-model") + 1

    def test_claude_cli_reaches_the_claude_planner_factory(self, monkeypatch):
        """`--planner-provider claude-cli` builds the Claude planner, not the Ollama one."""
        built: list[str] = []

        class _FakeClaudePlanner:
            def __init__(self, model=None, **kwargs):
                built.append("claude-cli")
                self.model = model or "claude-test"

            def raw_call(self, prompt, *, schema, system=None):
                return "{}"

        monkeypatch.setattr(
            "packages.providers.claude_planner.provider.ClaudeCliPlanner",
            _FakeClaudePlanner,
        )
        monkeypatch.setattr("shutil.which", lambda name: f"/usr/bin/{name}")

        def _ollama_tripwire(*args, **kwargs):
            raise AssertionError("the Ollama planner must not be built for claude-cli")

        monkeypatch.setattr(
            "packages.providers.ollama_planner.provider.OllamaPlanner",
            _ollama_tripwire,
        )

        from packages.orchestration.intake import make_structured_call_fn
        from packages.orchestration.schemas import JobIntake

        call_fn = make_structured_call_fn(JobIntake, provider="claude-cli")
        assert call_fn is not None
        assert built == ["claude-cli"]
        assert getattr(call_fn, "resolved_model", None) == "claude-test"

    def test_an_absent_claude_cli_answers_none_and_never_falls_back(self, monkeypatch):
        monkeypatch.setattr("shutil.which", lambda name: None)

        def _ollama_tripwire(*args, **kwargs):
            raise AssertionError("an unreachable claude-cli must not fall back to Ollama")

        monkeypatch.setattr(
            "packages.providers.ollama_planner.provider.OllamaPlanner",
            _ollama_tripwire,
        )

        from packages.orchestration.intake import make_structured_call_fn
        from packages.orchestration.schemas import JobIntake

        assert make_structured_call_fn(JobIntake, provider="claude-cli") is None

    def test_an_unknown_planner_is_refused(self):
        import pytest

        from packages.orchestration.intake import make_structured_call_fn
        from packages.orchestration.schemas import JobIntake

        with pytest.raises(ValueError, match="Unknown planner provider"):
            make_structured_call_fn(JobIntake, provider="gpt-cli")

    def test_the_do_context_carries_the_planner_provider(self):
        from packages.orchestration.do_sequence import DoContext

        assert DoContext(order="x").planner_provider is None
        assert DoContext(order="x", planner_provider="claude-cli").planner_provider == "claude-cli"
