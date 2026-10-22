"""F296 T001b and T001c, DECISION F296 D2 — evidence-triggered tier escalation.

The pure decision is read first, then three runs of the real `run_pingpong` loop: a cheaper builder
whose tests fail twice is followed by round three on the next tier with the reviewer raised; an
unreachable provider never escalates; and with the switch off nothing changes. The test command is
replaced by a script of answers, so no project test and no sandbox runs.
"""
from __future__ import annotations

import pathlib
import warnings
from types import SimpleNamespace

import pytest

from packages.orchestration.config import all_key_specs, get_key_spec
from packages.orchestration.config_keys_model_routing import (
    ESCALATION_AFTER_FAILURES_CONFIG_KEY,
    ESCALATION_ENABLED_CONFIG_KEY,
    ESCALATION_TIERS_CONFIG_KEY,
)
from packages.orchestration.pingpong_call_record import parked_session_refs
from packages.orchestration.pingpong_provider import BuilderOutput, ReviewerOutput
from packages.orchestration.tier_escalation import (
    ESCALATION_REASON_PREFIX,
    ESCALATION_TRIGGERS,
    EscalatedCall,
    EscalatedProvider,
    EscalationPolicy,
    EscalationTiersError,
    TaskTierLadder,
    TierModel,
    escalated_call_of,
    escalation_report_lines,
    escalation_trigger,
    is_escalation_trigger,
    next_model_tier,
    parse_escalation_tiers,
    resolve_escalation_policy,
    round_failure_class,
)
from packages.orchestration.verified_repair import REASON_TEST_FAILURE_UNCHANGED

LADDER = {"cheap": TierModel("fake", "cheap-model"), "mid": TierModel("fake", "mid-model"),
          "top": TierModel("fake", "top-model")}
LADDER_TOML = """
[remedy.model_escalation]
enabled = {enabled}

[remedy.model_escalation.tiers.cheap]
provider = "fake"
model = "cheap-model"

[remedy.model_escalation.tiers.mid]
provider = "fake"
model = "mid-model"

[remedy.model_escalation.tiers.top]
provider = "fake"
model = "top-model"
"""


def _configure_toml(monkeypatch, tmp_path, body: str) -> None:
    """Resolve the configuration from `body` through the real loader, as a project's file."""
    from packages.orchestration.config import load_config

    toml_file = tmp_path / "remedy.toml"
    toml_file.write_text(body, encoding="utf-8")
    loaded = load_config(project_path=toml_file, user_path=pathlib.Path("/nonexistent/user.toml"))
    monkeypatch.setattr("packages.orchestration.config.get_config", lambda: loaded)


def _round(test_passed=None, verdict="pass", summary="", tripped=""):
    return SimpleNamespace(test_passed=test_passed, test_summary=summary, test_tripped_limit=tripped,
                           reviewer_output=SimpleNamespace(verdict=verdict))


def _decision(repair_decision="repair", reason="test_failure_evidence"):
    return SimpleNamespace(repair_decision=repair_decision, reason=reason)


def _ladder(builder=("fake", "cheap-model"), reviewer=("fake", "cheap-model"), *, enabled=True, after=2):
    built: list[tuple[str, str, str]] = []

    def make(name, *, role, model, **options):
        built.append((role, name, model))
        return f"{role}:{model}"

    policy = EscalationPolicy(enabled=enabled, after_failures=after, tiers=LADDER)
    ladder = TaskTierLadder(policy, {"builder": builder, "reviewer": reviewer}, make, "none", {})
    return ladder, built


class TestTheVocabulary:
    def test_the_step_is_one_tier_up_and_never_down(self):
        assert [next_model_tier(t) for t in ("cheap", "mid", "top")] == ["mid", "top", None]
        with pytest.raises(ValueError):
            next_model_tier("huge")

    def test_provider_unavailable_is_refused_by_name_and_the_four_triggers_are_taken(self):
        assert ESCALATION_TRIGGERS == ("watchdog_tripped", "no_progress", "test_failed", "review_failed")
        assert [is_escalation_trigger(t) for t in ESCALATION_TRIGGERS] == [True] * 4
        assert is_escalation_trigger("provider_unavailable") is False
        assert is_escalation_trigger("provider_timeout") is False

    def test_a_round_names_the_evidence_it_carries(self):
        assert round_failure_class(_round(False)) == "test_failed"
        assert round_failure_class(_round(False, tripped="cpu_seconds")) == "watchdog_tripped"
        assert round_failure_class(_round(False, tripped="sandbox_unavailable")) == "test_failed"
        assert round_failure_class(_round(True, "needs_repair")) == "review_failed"
        assert round_failure_class(_round(None, "fail")) == "review_failed"
        assert round_failure_class(_round(True, "pass")) is None
        assert round_failure_class(_round(None, "pass")) is None

    def test_the_trigger_needs_the_threshold_on_the_current_tier(self):
        red, review, green = _round(False), _round(True, "needs_repair"), _round(True)
        assert escalation_trigger([red], "test_failure_evidence", 2) is None
        assert escalation_trigger([red, red], "test_failure_evidence", 2) == "test_failed"
        assert escalation_trigger([red, review], "reviewer_findings_present", 2) == "review_failed"
        assert escalation_trigger([red, green, red], "test_failure_evidence", 2) is None
        assert escalation_trigger([red, red], "test_failure_evidence", 3) is None
        assert escalation_trigger([red, red], REASON_TEST_FAILURE_UNCHANGED, 3) == "no_progress"
        assert escalation_trigger([red], REASON_TEST_FAILURE_UNCHANGED, 2) is None
        assert escalation_trigger([_round(False, tripped="wall_seconds")], "test_failure_evidence", 2) == (
            "watchdog_tripped")
        assert escalation_trigger([], "test_failure_evidence", 2) is None


class TestTheTiersTable:
    def test_a_well_formed_table_parses(self):
        raw = {tier: {"provider": m.provider, "model": m.model} for tier, m in LADDER.items()}
        assert parse_escalation_tiers(raw) == LADDER

    @pytest.mark.parametrize(("raw", "fault"), [
        ({"huge": {"provider": "fake", "model": "m"}}, "'huge' is not a tier"),
        ({"cheap": "fake"}, "'cheap' must be a table, got str"),
        ({"cheap": {"provider": "fake", "model": "m", "tier": "cheap"}}, "has unknown key 'tier'"),
        ({"cheap": {"provider": "nobody", "model": "m"}}, "names provider 'nobody'"),
        ({"cheap": {"provider": "fake", "model": ""}}, "must set model to a non-empty string"),
        ({"cheap": {"provider": "fake", "model": "m"}, "mid": {"provider": "fake", "model": "m"}},
         "'mid' repeats the model of tier 'cheap'"),
    ])
    def test_a_faulty_table_is_refused_with_the_fault_named(self, raw, fault):
        with pytest.raises(EscalationTiersError, match="^model_escalation.tiers: ") as caught:
            parse_escalation_tiers(raw)
        assert fault in str(caught.value)

    def test_the_policy_reads_the_three_keys(self, monkeypatch, tmp_path):
        _configure_toml(monkeypatch, tmp_path, LADDER_TOML.format(enabled="true"))
        policy = resolve_escalation_policy()
        assert (policy.enabled, policy.after_failures, dict(policy.tiers)) == (True, 2, LADDER)
        assert policy.tier_of("fake", "mid-model") == "mid"
        assert policy.tier_of("fake", "other") is None

    def test_unset_keys_read_off_two_and_no_tiers(self, monkeypatch, tmp_path):
        _configure_toml(monkeypatch, tmp_path, "")
        assert resolve_escalation_policy() == EscalationPolicy(enabled=False, after_failures=2, tiers={})

    def test_a_bad_threshold_and_a_bad_table_each_warn_once_and_escalate_nothing(self, monkeypatch, tmp_path):
        _configure_toml(monkeypatch, tmp_path, """
[remedy.model_escalation]
enabled = true
after_failures = 0

[remedy.model_escalation.tiers.huge]
provider = "fake"
model = "m"
""")
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            policy = resolve_escalation_policy()
        assert (policy.after_failures, dict(policy.tiers)) == (2, {})
        assert [str(w.message) for w in caught] == [
            "model_escalation.after_failures: expected a whole number of at least 1, got 0; using 2",
            "model_escalation.tiers: 'huge' is not a tier; the tiers are cheap, mid, top; no task escalates",
        ]

    def test_the_three_keys_are_registered_after_the_failover_cooldown(self):
        keys = [spec.key for spec in all_key_specs()]
        i = keys.index("model_failover.cooldown_s")
        assert keys[i + 1:i + 4] == [ESCALATION_ENABLED_CONFIG_KEY, ESCALATION_AFTER_FAILURES_CONFIG_KEY,
                                     ESCALATION_TIERS_CONFIG_KEY]
        assert (get_key_spec(ESCALATION_ENABLED_CONFIG_KEY).value_type, get_key_spec(
            ESCALATION_ENABLED_CONFIG_KEY).default) == (bool, False)
        assert get_key_spec(ESCALATION_TIERS_CONFIG_KEY).entry_type is dict


class TestTheLadder:
    def test_two_failing_rounds_move_the_builder_up_and_raise_the_reviewer_with_it(self):
        ladder, built = _ladder()
        rounds = [_round(False), _round(False)]
        assert ladder.after_review(_decision(), rounds[:1], rounds_left=2) is None
        step = ladder.after_review(_decision(), rounds, rounds_left=1)
        assert (step.round, step.reason, step.builder_from, step.builder_to, step.reviewer_from,
                step.reviewer_to) == (3, "test_failed", "cheap", "mid", "cheap", "mid")
        assert built == [("builder", "fake", "mid-model"), ("reviewer", "fake", "mid-model")]
        assert _unwrapped(ladder.start_round("cheap-builder", "cheap-reviewer")) == (
            "fake", "mid-model", "builder:mid-model", "fake", "mid-model", "reviewer:mid-model")
        assert ladder.resumes("builder", SimpleNamespace(supports_resume=True)) is False
        assert ladder.start_round("b", "r") is None
        assert ladder.resumes("builder", SimpleNamespace(supports_resume=True)) is True
        assert ladder.reviewer_raised is True

    def test_a_reviewer_already_above_keeps_its_provider_and_its_session(self):
        ladder, built = _ladder(reviewer=("fake", "top-model"))
        step = ladder.after_review(_decision(), [_round(False), _round(False)], rounds_left=1)
        assert (step.reviewer_from, step.reviewer_to) == ("top", "top")
        assert built == [("builder", "fake", "mid-model")]
        assert _unwrapped(ladder.start_round("b", "top-reviewer")) == (
            "fake", "mid-model", "builder:mid-model", "fake", "top-model", "top-reviewer")
        assert ladder.resumes("reviewer", SimpleNamespace(supports_resume=True)) is True
        assert ladder.reviewer_raised is False

    def test_a_no_progress_stop_becomes_the_escalated_round(self):
        ladder, _ = _ladder()
        decision = _decision("stop_exhausted", REASON_TEST_FAILURE_UNCHANGED)
        step = ladder.after_review(decision, [_round(False), _round(False)], rounds_left=1)
        assert step.reason == "no_progress"
        assert (decision.repair_decision, decision.reason) == ("repair", ESCALATION_REASON_PREFIX + "no_progress")

    @pytest.mark.parametrize("decision", [
        _decision("stop_exhausted", "test_failed_repair_budget_insufficient"),
        _decision("stop_exhausted", "repair_budget_exhausted"),
        _decision("pass_no_repair", "reviewer_passed"),
    ])
    def test_a_stop_the_budget_or_the_review_ordered_stands(self, decision):
        ladder, built = _ladder()
        before = (decision.repair_decision, decision.reason)
        assert ladder.after_review(decision, [_round(False), _round(False)], rounds_left=1) is None
        assert (decision.repair_decision, decision.reason) == before
        assert built == []

    @pytest.mark.parametrize(("kwargs", "rounds_left"), [
        ({"enabled": False}, 1),
        ({}, 0),
        ({"builder": ("fake", "top-model"), "reviewer": ("fake", "top-model")}, 1),
        ({"builder": ("claude-cli", "unlisted")}, 1),
        ({"reviewer": ("claude-cli", "unlisted")}, 1),
    ])
    def test_no_escalation_without_the_switch_a_round_a_higher_tier_or_a_known_tier(self, kwargs, rounds_left):
        ladder, built = _ladder(**kwargs)
        assert ladder.after_review(_decision(), [_round(False), _round(False)], rounds_left=rounds_left) is None
        assert built == []
        assert ladder.start_round("b", "r") is None

    def test_counting_starts_again_on_the_new_tier(self):
        ladder, _ = _ladder()
        red = _round(False)
        assert ladder.after_review(_decision(), [red, red], rounds_left=2).builder_to == "mid"
        ladder.start_round("b", "r")
        assert ladder.after_review(_decision(), [red, red, red], rounds_left=1) is None
        assert ladder.after_review(_decision(), [red, red, red, red], rounds_left=1).builder_to == "top"

    def test_a_target_that_cannot_be_built_is_not_taken(self):
        def make(name, *, role, model, **options):
            raise RuntimeError("claude CLI not found on PATH")

        ladder = TaskTierLadder(EscalationPolicy(True, 2, LADDER), {"builder": ("fake", "cheap-model"),
                                                                    "reviewer": ("fake", "mid-model")},
                                make, "none", {})
        decision = _decision("stop_exhausted", REASON_TEST_FAILURE_UNCHANGED)
        with pytest.warns(UserWarning, match="tier escalation to mid not taken: claude CLI not found"):
            assert ladder.after_review(decision, [_round(False), _round(False)], rounds_left=1) is None
        assert decision.repair_decision == "stop_exhausted"
        assert ladder.tiers == {"builder": "cheap", "reviewer": "mid"}


class _ScriptedProvider:
    """A builder or reviewer whose answers are fixed; it records each call's resume argument."""

    def __init__(self, name: str, model: str, *, supports_resume: bool = False, build_error: str = "") -> None:
        self.name, self.model = name, model
        self.supports_resume = supports_resume
        self.build_error = build_error
        self.resumes: list[str | None] = []

    def _actuals(self):
        return {"session_id": f"{self.model}-session"} if self.supports_resume else None

    def build(self, prompt, *, timeout_sec=120, max_output_chars=50000, resume=None):
        self.resumes.append(resume)
        return BuilderOutput(summary="ok", provider=self.name, error=self.build_error,
                             usage_actuals=self._actuals())

    def review(self, prompt, *, timeout_sec=120, max_output_chars=50000, resume=None):
        self.resumes.append(resume)
        return ReviewerOutput(verdict="pass", provider=self.name, summary="ok", confidence="high",
                              usage_actuals=self._actuals())


class TestARealRun:
    """T001c: the loop calls the ladder; `create_provider` on `pingpong_loop` hands out one
    scripted provider per (role, model), and `_run_test_command` answers from a script."""

    def _run(self, monkeypatch, tmp_path, *, enabled="true", tests=("FAILED a", "FAILED b", None),
             supports_resume=False, build_error="", reviewer_model="cheap-model"):
        import packages.orchestration.pingpong_loop as loop

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        monkeypatch.setattr("packages.orchestration.pingpong_provider_call._time.sleep", lambda seconds: None)
        _configure_toml(monkeypatch, tmp_path, LADDER_TOML.format(enabled=enabled))
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "README.md").write_text("# Demo\n")
        made: list[_ScriptedProvider] = []

        def create_provider(name, *, model=""):
            provider = _ScriptedProvider(name, model, supports_resume=supports_resume,
                                         build_error=build_error if model == "cheap-model" else "")
            made.append(provider)
            return provider

        answers = iter(tests)

        def run_test_command(command, staging, *, timeout_sec=120):
            failure = next(answers)
            return (True, "exit=0", "") if failure is None else (False, f"exit=1\n{failure}", "")

        monkeypatch.setattr(loop, "create_provider", create_provider)
        monkeypatch.setattr(loop, "_run_test_command", run_test_command)
        result = loop.run_pingpong("Fix README", str(repo), builder_name="fake", builder_model="cheap-model",
                                   reviewer_name="fake", reviewer_model=reviewer_model, test_command="scripted",
                                   repair_rounds=2)
        return result, made, loop.export_pingpong_json(result)

    def test_a_builder_failing_its_tests_twice_runs_round_three_one_tier_up_with_the_reviewer(
            self, monkeypatch, tmp_path):
        result, made, record = self._run(monkeypatch, tmp_path)
        assert result.final_status == "staged_review_passed"
        assert [rd.test_passed for rd in result.rounds] == [False, False, True]
        assert [(p.model, len(p.resumes)) for p in made] == [
            ("cheap-model", 2), ("cheap-model", 2), ("mid-model", 1), ("mid-model", 1)]
        traced = [(t.role, t.provider, t.configured_model) for t in result.prompt_traces]
        assert traced == [("builder", "fake", "cheap-model"), ("reviewer", "fake", "cheap-model")] * 2 + [
            ("builder", "fake", "mid-model"), ("reviewer", "fake", "mid-model")]
        assert result.repair_decisions[1]["reason"] == "test_failure_evidence"
        assert result.task_actor_binding["sticky_across_rounds"] is False

    def test_the_same_failure_twice_escalates_instead_of_stopping(self, monkeypatch, tmp_path):
        result, made, _ = self._run(monkeypatch, tmp_path, tests=("FAILED a", "FAILED a", None))
        assert result.final_status == "staged_review_passed"
        assert result.repair_decisions[1]["repair_decision"] == "repair"
        assert result.repair_decisions[1]["reason"] == ESCALATION_REASON_PREFIX + "no_progress"
        assert [p.model for p in made] == ["cheap-model", "cheap-model", "mid-model", "mid-model"]

    def test_the_escalated_round_never_resumes_the_cheaper_session(self, monkeypatch, tmp_path):
        result, made, _ = self._run(monkeypatch, tmp_path, supports_resume=True)
        cheap_builder, cheap_reviewer, mid_builder, mid_reviewer = made
        assert cheap_builder.resumes == [None, "cheap-model-session"]
        assert cheap_reviewer.resumes == [None, "cheap-model-session"]
        assert mid_builder.resumes == [None]
        assert mid_reviewer.resumes == [None]

    def test_a_reviewer_on_the_next_tier_already_keeps_its_session_while_the_builder_moves(
            self, monkeypatch, tmp_path):
        result, made, _ = self._run(monkeypatch, tmp_path, supports_resume=True, reviewer_model="mid-model")
        assert result.final_status == "staged_review_passed"
        cheap_builder, reviewer, mid_builder = made
        assert (cheap_builder.model, reviewer.model, mid_builder.model) == ("cheap-model", "mid-model", "mid-model")
        assert reviewer.resumes == [None, "mid-model-session", "mid-model-session"]
        assert mid_builder.resumes == [None]
        assert result.task_actor_binding["sticky_across_rounds"] is False

    def test_with_the_switch_off_nothing_escalates_and_nothing_changes(self, monkeypatch, tmp_path):
        result, made, _ = self._run(monkeypatch, tmp_path, enabled="false", tests=("FAILED a", "FAILED a"))
        assert result.final_status == "repair_exhausted"
        assert result.repair_decisions[1]["reason"] == REASON_TEST_FAILURE_UNCHANGED
        assert [p.model for p in made] == ["cheap-model", "cheap-model"]
        assert result.task_actor_binding["sticky_across_rounds"] is True

    def test_an_unreachable_provider_never_escalates(self, monkeypatch, tmp_path):
        result, made, _ = self._run(monkeypatch, tmp_path, tests=(),
                                    build_error="provider_unavailable: the endpoint refused the connection")
        assert result.final_status == "provider_unavailable"
        assert {p.model for p in made} == {"cheap-model"}


def _unwrapped(fresh):
    """`start_round`'s six values with each `EscalatedProvider` replaced by the provider it wraps."""
    return tuple(value._inner if isinstance(value, EscalatedProvider) else value for value in fresh)


class TestTheRecord:
    """T002a, DECISION F296 D3: what an escalated call leaves in the run's record, its cost booking,
    a relaunch's session guard, the run report and the job's event stream."""

    _run = TestARealRun._run

    def test_every_escalated_call_carries_its_tier_its_reason_and_its_round(self, monkeypatch, tmp_path):
        result, _, record = self._run(monkeypatch, tmp_path)
        entries = [(r.get("builder", {}).get("escalation"), r.get("reviewer", {}).get("escalation"))
                   for r in record["rounds"]]
        mid = {"escalated_from": "cheap", "tier": "mid", "reason": "test_failed", "round": 3,
               "provider": "fake", "model": "mid-model"}
        assert entries == [(None, None), (None, None), (mid, mid)]
        assert list(record["rounds"][2]["builder"])[-1] == "escalation"
        assert escalated_call_of(result.rounds[2].builder_output) == EscalatedCall(**mid)
        assert escalated_call_of(result.rounds[0].builder_output) is None

    def test_the_cost_booking_names_the_model_that_served_each_call(self, monkeypatch, tmp_path):
        _, _, record = self._run(monkeypatch, tmp_path)
        booked = [(a["role"], a["model"]) for a in record["provider_evidence"]["provider_attempts"]]
        assert booked == [("builder", "cheap-model"), ("reviewer", "cheap-model")] * 2 + [
            ("builder", "mid-model"), ("reviewer", "mid-model")]

    def test_a_relaunch_never_offers_an_escalated_models_session(self, monkeypatch, tmp_path):
        _, _, record = self._run(monkeypatch, tmp_path, supports_resume=True)
        assert parked_session_refs(record) == {}
        (tmp_path / "kept").mkdir()
        _, _, kept = self._run(monkeypatch, tmp_path / "kept", supports_resume=True, reviewer_model="mid-model")
        assert parked_session_refs(kept) == {"reviewer": "mid-model-session"}

    def test_the_report_has_one_line_per_escalation(self, monkeypatch, tmp_path):
        _, _, record = self._run(monkeypatch, tmp_path)
        assert escalation_report_lines(record) == [
            "Escalation: from round 3 the builder ran on the mid tier instead of cheap, because its tests kept "
            "failing; the reviewer was raised to mid with it."]
        (tmp_path / "kept").mkdir()
        _, _, kept = self._run(monkeypatch, tmp_path / "kept", tests=("FAILED a", "FAILED a", None),
                               reviewer_model="mid-model")
        assert escalation_report_lines(kept) == [
            "Escalation: from round 3 the builder ran on the mid tier instead of cheap, because its tests failed "
            "twice with the same failure; the reviewer kept its tier."]
        assert escalation_report_lines({"rounds": [{"builder": {"session_id": ""}}]}) == []

    def test_run_show_prints_the_line_after_the_reviewer(self, monkeypatch, tmp_path, capsys):
        from apps.cli.commands.run_report_cmd import _cmd_run_show

        result, _, record = self._run(monkeypatch, tmp_path)
        _cmd_run_show(result.run_id, json_output=False)
        lines = capsys.readouterr().out.splitlines()
        reviewer_at = next(i for i, line in enumerate(lines) if line.startswith("Reviewer:"))
        assert lines[reviewer_at + 1] == escalation_report_lines(record)[0]

    def test_the_job_event_stream_carries_worker_escalated_before_the_round(self, monkeypatch, tmp_path):
        from packages.orchestration.pingpong_job import _log_task_rounds

        result, _, _ = self._run(monkeypatch, tmp_path)
        events: list[tuple[str, dict]] = []
        log = SimpleNamespace(log=lambda event, **fields: events.append((event, fields)))
        _log_task_rounds(log, SimpleNamespace(task_id="T001"), result, "attempt-1")
        names = [name for name, _ in events]
        assert names.count("worker.escalated") == 1
        at = names.index("worker.escalated")
        assert names[at:at + 4] == ["worker.escalated", "task_round_repaired", "task_round_tested",
                                    "task_round_completed"]
        assert events[at + 1][1]["round_number"] == 3
        assert events[at][1] == {"task_id": "T001", "attempt_id": "attempt-1", "escalated_from": "cheap",
                                 "tier": "mid", "reason": "test_failed", "round": 3, "provider": "fake",
                                 "model": "mid-model"}

    def test_the_event_comes_once_per_escalation_not_once_per_escalated_round(self):
        from packages.orchestration.pingpong_job import _log_task_rounds

        call = EscalatedCall("cheap", "mid", "test_failed", 3, "fake", "mid-model")

        def served(number, stamped):
            out = BuilderOutput(summary="ok", provider="fake")
            if stamped:
                out.tier_escalation = call
            return SimpleNamespace(round_number=number, kind="repair", test_passed=False, builder_output=out,
                                   reviewer_output=SimpleNamespace(verdict="pass"))

        events: list[str] = []
        log = SimpleNamespace(log=lambda event, **fields: events.append(event))
        rounds = [served(2, False), served(3, True), served(4, True)]
        _log_task_rounds(log, SimpleNamespace(task_id="T001"), SimpleNamespace(rounds=rounds), "attempt-1")
        assert events.count("worker.escalated") == 1
        assert events.index("worker.escalated") == 3

    def test_an_escalated_provider_hands_every_other_attribute_to_its_provider(self):
        inner = _ScriptedProvider("fake", "mid-model", supports_resume=True)
        call = EscalatedCall("cheap", "mid", "test_failed", 3, "fake", "mid-model")
        wrapped = EscalatedProvider(inner, call)
        assert (wrapped.name, wrapped.model, wrapped.supports_resume) == ("fake", "mid-model", True)
        assert escalated_call_of(wrapped.build("p")) is call
        assert escalated_call_of(wrapped.review("p")) is call
        assert inner.resumes == [None, None]
        assert escalated_call_of(SimpleNamespace(tier_escalation="a test double's attribute")) is None
        with pytest.raises(AttributeError):
            wrapped._private
