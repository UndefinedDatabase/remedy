"""F028 T001 — the draft pass of a task injection (DECISION F028 D1): the mandatory verbatim
text, the pure gate and id, the placement, the budget check and its shortfall seed, the fence
flags, the one structured planner call, and the create-only draft file with a time to live.

Every test uses ``tmp_path`` as the control root and a fake ``call_fn`` that answers JSON —
never a real provider.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import pytest

from packages.core.models import JobBudgets, JobFences
from packages.orchestration import pingpong_job as pj
from packages.orchestration import task_injection as ti
from packages.orchestration.budget_guard import BudgetCounters
from packages.orchestration.budget_resolution import PredictiveBudgetConfig
from packages.orchestration.data_paths import job_dod_path
from packages.orchestration.job_plan import APPROVED_PLAN_HASH_KEY, plan_content_hash
from packages.orchestration.mission_compiler import PLAN_VERSION_KEY
from packages.orchestration.plan_editing import EDIT_LOG_KEY, replay_edits
from packages.orchestration.schemas.models import SCHEMA_REGISTRY, PlannedTask, TaskPlan

JOB_ID = "f028job0000000a"
UTC = timezone.utc

CLASS_DEFAULTS = {"low": 8000, "medium": 32000, "high": 120000}


# ---------------------------------------------------------------------------
# Shared builders
# ---------------------------------------------------------------------------


def _secret_shaped_text() -> str:
    """Built at run time from parts, so no secret-shaped literal sits in the source."""
    parts = ["sk", "-", "ant", "-"] + ["a"] * 24
    return "".join(parts)


def _task(task_id: str, files: tuple[str, ...] = ()) -> PlannedTask:
    return PlannedTask(id=task_id, title=f"title {task_id}", goal=f"goal {task_id}",
                       acceptance=[f"do {task_id}"], est_tokens_band="S",
                       files_hint=list(files))


def _plan_dict(tasks: list[PlannedTask]) -> dict:
    return TaskPlan(schema_v="task_plan_v1", tasks=tasks).model_dump()


def _job(*, state: pj.RunState = pj.RunState.RUNNING, tasks: list[PlannedTask] | None = None,
         fences: JobFences | None = None, job_id: str = JOB_ID) -> pj.JobPlan:
    plan_tasks = tasks if tasks is not None else [_task("T1")]
    return pj.JobPlan(job_id=job_id, state=state, task_plan=_plan_dict(plan_tasks),
                      fences=fences)


def _counters(spent: float | None) -> BudgetCounters:
    return BudgetCounters(
        provider_calls=1, measured_call_count=1, unmeasured_call_count=0,
        measured_token_total=1000, actual_sources=("pingpong_actuals",),
        measured_cost_usd=spent, priced_call_count=1)


def _config(price_basis: float | None = 0.01) -> PredictiveBudgetConfig:
    return PredictiveBudgetConfig(price_basis_usd_per_1k_tokens=price_basis,
                                  class_default_tokens=dict(CLASS_DEFAULTS))


def _draft_json(*, title: str = "Add the thing", goal: str = "do the thing",
                acceptance: tuple[str, ...] = ("acceptance one",), est_tokens_band: str = "S",
                files_hint: tuple[str, ...] = (), rationale: str = "because") -> str:
    return json.dumps({
        "schema_v": "task_injection_draft_v1",
        "title": title,
        "goal": goal,
        "acceptance": list(acceptance),
        "est_tokens_band": est_tokens_band,
        "files_hint": list(files_hint),
        "rationale": rationale,
    })


class _FakeCall:
    """A queue of raw replies; each call pops the next and records the prompt it received."""

    def __init__(self, replies: list[str]) -> None:
        self._replies = list(replies)
        self.prompts: list[str] = []
        self.calls = 0

    def __call__(self, prompt: str, attempt: int) -> str:
        self.calls += 1
        self.prompts.append(prompt)
        return self._replies.pop(0)


def _digest_name(draft_id: str) -> str:
    """Mirrors ``task_injection._draft_filename`` exactly: a control file is named by a
    digest of its id, never by the id itself."""
    return f"{hashlib.sha256(draft_id.encode('utf-8')).hexdigest()[:32]}.json"


#: A fixed instant every drafting/confirming helper defaults to, so a confirmation made
#: without an explicit ``now`` never drifts into the real clock and expires the draft.
_FIXED_NOW = datetime(2026, 1, 1, tzinfo=UTC)


def _drafted(tmp_path: Path, *, job: pj.JobPlan | None = None, text: str = "add a widget",
            after: str | None = None, now: datetime = _FIXED_NOW) -> tuple[pj.JobPlan, dict]:
    """A job with one freshly drafted, confirmable injection: ``(job, answer)``."""
    job = job if job is not None else _job()
    call = _FakeCall([_draft_json()])
    answer = ti.draft_task_injection(
        job, text, call_fn=call, budgets=JobBudgets(), counters=_counters(None),
        config=_config(price_basis=None), actor="alice", after=after, now=now,
        control_root_path=tmp_path)
    assert answer["outcome"] == "drafted"
    return job, answer


_NOT_GIVEN = object()  # a sentinel: omit `budget_extend_to_usd` entirely unless asked for


def _confirmed_record(*, task_id: str = "INJ1", depends_on: tuple[str, ...] = (),
                      actor: str = "alice", draft_id: str = "draftabc00000001",
                      confirmed_at: str = "2026-01-01T00:00:00+00:00",
                      basis: str = "frontier_default",
                      budget_extend_to_usd: Any = _NOT_GIVEN,
                      confirmed_unseen: Any = _NOT_GIVEN) -> dict:
    """A confirmed-injection record shaped exactly as ``confirm_task_injection`` writes one —
    built directly so ``apply_injection_to_job`` (S4) can be tested independent of S3.

    ``budget_extend_to_usd`` and ``confirmed_unseen`` are each omitted entirely by default:
    a caller exercising either passes a real value explicitly (DECISION F028 D3 (2), D4 (2)).
    """
    record = {
        "draft_id": draft_id,
        "task": {
            "id": task_id, "title": "Add the thing", "goal": "do the thing",
            "acceptance": ["it happens"], "depends_on": list(depends_on),
            "est_tokens_band": "S", "files_hint": [],
        },
        "placement": {"depends_on": list(depends_on), "basis": basis, "position": 1,
                      "rationale": "placed at the end"},
        "task_rationale": "because the operator asked",
        "text": "add the thing",
        "drafted_by": "alice",
        "actor": actor,
        "confirmed_at": confirmed_at,
    }
    if budget_extend_to_usd is not _NOT_GIVEN:
        record["budget_extend_to_usd"] = budget_extend_to_usd
    if confirmed_unseen is not _NOT_GIVEN:
        record["confirmed_unseen"] = confirmed_unseen
    return record


def _injected_tasks_dir(tmp_path: Path, job_id: str) -> Path:
    return tmp_path / "jobs" / job_id / ti.INJECTED_TASKS_DIRNAME


# ---------------------------------------------------------------------------
# S3 — the text, kept verbatim
# ---------------------------------------------------------------------------


class TestValidateInjectionText:
    @pytest.mark.parametrize("bad", [None, "", "   ", 5])
    def test_text_required(self, bad):
        with pytest.raises(ti.TaskInjectionRefused) as exc:
            ti.validate_injection_text(bad)
        assert exc.value.code == "text_required"

    def test_text_too_long(self):
        with pytest.raises(ti.TaskInjectionRefused) as exc:
            ti.validate_injection_text("x" * (ti.MAX_INJECTION_TEXT_CHARS + 1))
        assert exc.value.code == "text_too_long"

    def test_text_invalid_control_character(self):
        with pytest.raises(ti.TaskInjectionRefused) as exc:
            ti.validate_injection_text("hello\x07world")
        assert exc.value.code == "text_invalid"

    def test_text_invalid_secret_shaped(self):
        with pytest.raises(ti.TaskInjectionRefused) as exc:
            ti.validate_injection_text(_secret_shaped_text())
        assert exc.value.code == "text_invalid"

    def test_newline_and_tab_pass_unchanged(self):
        text = "line one\nline two\twith a tab"
        assert ti.validate_injection_text(text) == text


# ---------------------------------------------------------------------------
# S4 — the gate and the id, pure
# ---------------------------------------------------------------------------


class TestInjectionRefusal:
    @pytest.mark.parametrize(
        "state", [pj.RunState.COMPLETED, pj.RunState.FAILED, pj.RunState.CANCELLED])
    def test_terminal_states_name_a_follow_up_job(self, state):
        refusal = ti.injection_refusal(state, 0)
        assert refusal is not None
        assert refusal.code == "job_terminal"
        assert "follow-up job" in refusal.detail

    @pytest.mark.parametrize(
        "state", [pj.RunState.PAUSED, pj.RunState.BLOCKED, pj.RunState.PLANNED,
                 pj.RunState.RUNNING])
    def test_non_terminal_states_admit_an_injection(self, state):
        assert ti.injection_refusal(state, 0) is None

    def test_plan_full_at_the_cap(self):
        refusal = ti.injection_refusal(pj.RunState.RUNNING, ti.MAX_PLAN_TASKS)
        assert refusal is not None
        assert refusal.code == "plan_full"

    def test_terminal_wins_over_a_full_plan(self):
        refusal = ti.injection_refusal(pj.RunState.COMPLETED, ti.MAX_PLAN_TASKS)
        assert refusal is not None
        assert refusal.code == "job_terminal"


class TestNextInjectedTaskId:
    def test_smallest_free_id(self):
        assert ti.next_injected_task_id([]) == "INJ1"
        assert ti.next_injected_task_id(["INJ1", "INJ2"]) == "INJ3"
        assert ti.next_injected_task_id(["INJ2"]) == "INJ1"


# ---------------------------------------------------------------------------
# S5 — the placement, pure
# ---------------------------------------------------------------------------


class TestPlaceInjectedTask:
    def test_stated_after_a_known_task(self):
        tasks = [_task("T1"), _task("T2")]
        result = ti.place_injected_task(tasks, [], after="T1")
        assert result == {
            "depends_on": ["T1"],
            "basis": "stated",
            "position": 2,
            "rationale": "placed after T1 because you named it",
        }

    def test_unknown_after_names_the_first_ten_and_the_rest(self):
        tasks = [_task(f"T{i}") for i in range(1, 13)]
        with pytest.raises(ti.TaskInjectionRefused) as exc:
            ti.place_injected_task(tasks, [], after="ghost")
        assert exc.value.code == "unknown_task"
        for i in range(1, 11):
            assert f"T{i}" in exc.value.detail
        assert "T11" not in exc.value.detail
        assert "and 2 more" in exc.value.detail

    def test_content_overlap_in_plan_order(self):
        tasks = [_task("T1", files=("b.py",)), _task("T2", files=("a.py",)),
                 _task("T3", files=())]
        result = ti.place_injected_task(tasks, ["a.py", "b.py"], after=None)
        assert result["basis"] == "content_overlap"
        assert result["depends_on"] == ["T1", "T2"]
        assert result["rationale"] == (
            "placed after T1, T2 because they touch the same files: a.py, b.py")

    def test_leading_dot_slash_normalizes(self):
        tasks = [_task("T1", files=("./a.py",))]
        result = ti.place_injected_task(tasks, ["a.py"], after=None)
        assert result["basis"] == "content_overlap"
        assert result["depends_on"] == ["T1"]

    def test_frontier_default_when_nothing_matches(self):
        tasks = [_task("T1", files=("b.py",))]
        result = ti.place_injected_task(tasks, ["z.py"], after=None)
        assert result == {
            "depends_on": [],
            "basis": "frontier_default",
            "position": 1,
            "rationale": (
                "placed at the end of the plan with no dependency, because no planned task "
                "touches its files"),
        }


# ---------------------------------------------------------------------------
# S6 — the budget check and the shortfall seed
# ---------------------------------------------------------------------------


class TestInjectionBudgetCheckAndShortfallSeed:
    def test_band_s_no_shortfall(self):
        check = ti.injection_budget_check(
            JobBudgets(max_cost_usd=1.00), _counters(0.90), band="S", config=_config())
        assert check["plan_band"] == "S"
        assert check["shortfall"] is False

    def test_band_m_shortfall_seed_extend_and_shrink(self):
        check = ti.injection_budget_check(
            JobBudgets(max_cost_usd=1.00), _counters(0.90), band="M", config=_config())
        assert check["shortfall"] is True
        seed = ti.shortfall_decision_seed(check)
        assert seed["extend_to_usd"] == 1.22
        assert seed["shrink_band"] == "S"
        assert seed["options"] == list(ti.SHORTFALL_OPTIONS)
        assert seed["arithmetic"] == check["arithmetic"]

    def test_band_xl_reads_as_unknown_with_class_default_missing_band(self):
        check = ti.injection_budget_check(
            JobBudgets(max_cost_usd=1.00), _counters(0.90), band="XL", config=_config())
        assert check["band"] == "unknown"
        assert check["estimate_basis"] == "class_default_missing_band"

    def test_band_s_shortfall_has_no_smaller_band_to_shrink_to(self):
        check = ti.injection_budget_check(
            JobBudgets(max_cost_usd=1.00), _counters(0.95), band="S", config=_config())
        assert check["shortfall"] is True
        seed = ti.shortfall_decision_seed(check)
        assert seed["shrink_band"] is None
        assert "cannot shrink" in seed["option_labels"]["shrink_task"]

    def test_no_cost_limit_no_shortfall(self):
        check = ti.injection_budget_check(
            JobBudgets(max_cost_usd=None), _counters(0.90), band="M", config=_config())
        assert check["shortfall"] is False

    def test_extend_to_usd_rounds_up_to_the_cent(self):
        # A fractional-cent total distinguishes ROUND_CEILING from ROUND_FLOOR: 1.221
        # ceils to 1.23 and floors to 1.22.
        check = {"plan_band": "M", "spent_cost_usd": 0.901, "expected_cost_usd": 0.32,
                 "arithmetic": "x"}
        seed = ti.shortfall_decision_seed(check)
        assert seed["extend_to_usd"] == 1.23

    def test_question_and_labels_are_exact_sentences_with_a_smaller_band(self):
        # DECISION F028 D3 (3): the labels are a mapping of complete plain sentences.
        check = ti.injection_budget_check(
            JobBudgets(max_cost_usd=1.00), _counters(0.90), band="M", config=_config())
        seed = ti.shortfall_decision_seed(check)
        assert seed["question"] == (
            "Adding this task would go over the job's cost limit. What should happen?")
        assert seed["option_labels"] == {
            "extend_budget": "Raise the job's cost limit to $1.22 and add the task.",
            "shrink_task": (
                "Draft the task again one size smaller, as size S, and check the cost "
                "again."),
            "drop": "Drop this task and add nothing to the job.",
        }

    def test_shrink_label_without_a_smaller_band(self):
        check = ti.injection_budget_check(
            JobBudgets(max_cost_usd=1.00), _counters(0.95), band="S", config=_config())
        seed = ti.shortfall_decision_seed(check)
        assert seed["option_labels"]["shrink_task"] == (
            "The task is already the smallest size, so it cannot shrink.")


# ---------------------------------------------------------------------------
# DECISION F028 D4 (3) — `injection_budget_inputs` / `injection_call_fn`, the shared
# helpers the CLI and round 5's browser command both read.
# ---------------------------------------------------------------------------

_VALID_PERSISTED_ACTUALS_V1 = {
    "schema_version": "1.0.0",
    "provider_call_count": 4,
    "actual_call_count": 3,
    "unmeasured_call_count": 1,
    "total_tokens": 4200,
    "started_at": "2026-07-01T11:00:00+00:00",
    "actual_sources": ["pingpong_live"],
}


class TestInjectionBudgetInputs:
    def test_no_budgets_and_no_actuals_answers_none_and_empty_counters(self):
        job = _job()
        job.budgets = None
        job.budget_actuals = None

        budgets, counters, config = ti.injection_budget_inputs(job)

        assert budgets is None
        # `BudgetCounters()` stamps its own `evaluated_at` at construction, so a
        # field-by-field comparison is used rather than `==` against a fresh instance.
        assert counters.provider_calls == 0
        assert counters.measured_call_count == 0
        assert counters.measured_cost_usd is None
        assert counters.actual_sources == ()
        assert config is not None

    def test_budgets_present_validates_into_jobbudgets(self):
        job = _job()
        job.budgets = {"max_cost_usd": 5.0}
        job.budget_actuals = None

        budgets, _counters_out, _config_out = ti.injection_budget_inputs(job)

        assert budgets == JobBudgets(max_cost_usd=5.0)

    def test_persisted_actuals_decode_into_counters(self):
        job = _job()
        job.budgets = None
        job.budget_actuals = dict(_VALID_PERSISTED_ACTUALS_V1)

        _budgets_out, counters, _config_out = ti.injection_budget_inputs(job)

        assert counters.provider_calls == 4
        assert counters.measured_call_count == 3
        assert counters.actual_sources == ("pingpong_live",)

    def test_config_is_the_repos_predictive_config(self):
        job = _job()
        job.budgets = None
        job.budget_actuals = None
        job.repo_path = ""

        _budgets_out, _counters_out, config = ti.injection_budget_inputs(job)

        assert hasattr(config, "class_default_tokens")

    def test_undecodable_actuals_refuse_budget_unreadable(self):
        job = _job()
        job.budgets = None
        job.budget_actuals = {"schema_version": "1.0.0"}   # missing required fields

        with pytest.raises(ti.TaskInjectionRefused) as exc:
            ti.injection_budget_inputs(job)
        assert exc.value.code == "budget_unreadable"

    def test_unreadable_budgets_refuse_budget_unreadable(self):
        job = _job()
        job.budgets = {"not_a_real_budget_field": 1}
        job.budget_actuals = None

        with pytest.raises(ti.TaskInjectionRefused) as exc:
            ti.injection_budget_inputs(job)
        assert exc.value.code == "budget_unreadable"


class TestInjectionCallFn:
    def test_returns_none_without_ollama(self) -> None:
        """`tests/conftest.py::_no_live_ollama_reach` (autouse) already refuses a live
        Ollama connection for every unmarked test."""
        assert ti.injection_call_fn() is None


# ---------------------------------------------------------------------------
# S7 — the fences
# ---------------------------------------------------------------------------


class TestFenceConflicts:
    def test_deny_glob_is_flagged_with_its_glob(self):
        fences = JobFences(deny=["secrets/**"])
        result = ti.fence_conflicts(["secrets/key.txt", "src/a.py"], fences)
        assert result == [{"path": "secrets/key.txt", "rule": "deny", "glob": "secrets/**"}]

    def test_allow_miss_is_flagged_not_allowed(self):
        fences = JobFences(allow=["src/**"])
        result = ti.fence_conflicts(["docs/readme.md"], fences)
        assert result == [{"path": "docs/readme.md", "rule": "not_allowed", "glob": ""}]

    def test_allowed_path_is_not_flagged(self):
        fences = JobFences(allow=["src/**"])
        assert ti.fence_conflicts(["src/a.py"], fences) == []

    def test_none_fences_never_flag(self):
        assert ti.fence_conflicts(["anything.py"], None) == []


# ---------------------------------------------------------------------------
# S8 — the draft and its file
# ---------------------------------------------------------------------------


class TestDraftTaskInjection:
    def test_drafted_answer_round_trips_through_read_injection_draft(self, tmp_path: Path):
        job = _job()
        call = _FakeCall([_draft_json()])
        now = datetime(2026, 1, 1, tzinfo=UTC)

        answer = ti.draft_task_injection(
            job, "add a widget", call_fn=call, budgets=JobBudgets(), counters=_counters(None),
            config=_config(price_basis=None), actor="alice", now=now,
            control_root_path=tmp_path)

        assert answer["outcome"] == "drafted"
        assert answer["confirm_token"] == answer["draft_id"]
        assert answer["planner_calls"] == 1
        assert call.calls == 1
        assert "add a widget" in call.prompts[0]

        record = ti.read_injection_draft(job.job_id, answer["draft_id"], now=now,
                                         control_root_path=tmp_path)
        expected = dict(answer)
        expected["injection_draft_v"] = 1
        expected["status"] = "confirmable"
        expected["actor"] = "alice"
        expected["after"] = None
        assert record == expected

    def test_planner_calls_two_after_one_invalid_reply(self, tmp_path: Path):
        job = _job()
        call = _FakeCall(["not json", _draft_json()])

        answer = ti.draft_task_injection(
            job, "add a widget", call_fn=call, budgets=JobBudgets(), counters=_counters(None),
            config=_config(price_basis=None), actor="alice", control_root_path=tmp_path)

        assert answer["outcome"] == "drafted"
        assert answer["planner_calls"] == 2
        assert call.calls == 2

    def test_draft_unparseable_after_two_invalid_replies_writes_nothing(self, tmp_path: Path):
        job = _job()
        call = _FakeCall(["not json", "still not json"])

        answer = ti.draft_task_injection(
            job, "add a widget", call_fn=call, budgets=JobBudgets(), counters=_counters(None),
            config=_config(price_basis=None), actor="alice", control_root_path=tmp_path)

        assert answer["outcome"] == "refused"
        assert answer["code"] == "draft_unparseable"
        assert call.calls == 2
        assert not (tmp_path / "jobs").exists()

    def test_planner_unavailable_never_calls_and_writes_nothing(self, tmp_path: Path):
        job = _job()

        answer = ti.draft_task_injection(
            job, "add a widget", call_fn=None, budgets=JobBudgets(), counters=_counters(None),
            config=_config(price_basis=None), actor="alice", control_root_path=tmp_path)

        assert answer == {"outcome": "refused", "code": "planner_unavailable",
                          "detail": answer["detail"]}
        assert not (tmp_path / "jobs").exists()

    def test_unknown_after_refuses_before_any_call_and_writes_nothing(self, tmp_path: Path):
        job = _job()
        call = _FakeCall([_draft_json()])

        answer = ti.draft_task_injection(
            job, "add a widget", call_fn=call, budgets=JobBudgets(), counters=_counters(None),
            config=_config(price_basis=None), actor="alice", after="ghost",
            control_root_path=tmp_path)

        assert answer["outcome"] == "refused"
        assert answer["code"] == "unknown_task"
        assert call.calls == 0
        assert not (tmp_path / "jobs").exists()

    def test_shortfall_answer_has_no_token_and_needs_decision_status(self, tmp_path: Path):
        job = _job()
        call = _FakeCall([_draft_json(est_tokens_band="M")])
        now = datetime(2026, 1, 1, tzinfo=UTC)

        answer = ti.draft_task_injection(
            job, "add a widget", call_fn=call, budgets=JobBudgets(max_cost_usd=1.00),
            counters=_counters(0.90), config=_config(), actor="alice", now=now,
            control_root_path=tmp_path)

        assert answer["outcome"] == "shortfall"
        assert answer["confirm_token"] is None
        assert answer["decision_seed"]["shrink_band"] == "S"

        record = ti.read_injection_draft(job.job_id, answer["draft_id"], now=now,
                                         control_root_path=tmp_path)
        assert record["status"] == "needs_decision"

    def test_read_injection_draft_expiry_boundary(self, tmp_path: Path):
        job = _job()
        call = _FakeCall([_draft_json()])
        drafted_at = datetime(2026, 1, 1, tzinfo=UTC)

        answer = ti.draft_task_injection(
            job, "add a widget", call_fn=call, budgets=JobBudgets(), counters=_counters(None),
            config=_config(price_basis=None), actor="alice", now=drafted_at,
            control_root_path=tmp_path)
        draft_id = answer["draft_id"]

        almost_expired = drafted_at + timedelta(seconds=899)
        record = ti.read_injection_draft(job.job_id, draft_id, now=almost_expired,
                                         control_root_path=tmp_path)
        assert record["draft_id"] == draft_id

        at_expiry = drafted_at + timedelta(seconds=900)
        with pytest.raises(ti.TaskInjectionRefused) as exc:
            ti.read_injection_draft(job.job_id, draft_id, now=at_expiry,
                                    control_root_path=tmp_path)
        assert exc.value.code == "draft_expired"

        drafts_dir = tmp_path / "jobs" / job.job_id / "injection_drafts"
        assert len(list(drafts_dir.iterdir())) == 1

    def test_draft_unknown_for_missing_id_and_for_path_escape(self, tmp_path: Path):
        job = _job()

        with pytest.raises(ti.TaskInjectionRefused) as exc:
            ti.read_injection_draft(job.job_id, "deadbeefdeadbeef", control_root_path=tmp_path)
        assert exc.value.code == "draft_unknown"

        with pytest.raises(ti.TaskInjectionRefused) as exc:
            ti.read_injection_draft(job.job_id, "../x", control_root_path=tmp_path)
        assert exc.value.code == "draft_unknown"

    def test_task_injection_error_for_a_corrupt_file(self, tmp_path: Path):
        job = _job()
        call = _FakeCall([_draft_json()])

        answer = ti.draft_task_injection(
            job, "add a widget", call_fn=call, budgets=JobBudgets(), counters=_counters(None),
            config=_config(price_basis=None), actor="alice", control_root_path=tmp_path)
        draft_id = answer["draft_id"]

        drafts_dir = tmp_path / "jobs" / job.job_id / "injection_drafts"
        [entry] = list(drafts_dir.iterdir())
        entry.write_bytes(b"not json")

        with pytest.raises(ti.TaskInjectionError):
            ti.read_injection_draft(job.job_id, draft_id, control_root_path=tmp_path)

    def test_schema_not_registered(self):
        assert ti.INJECTION_DRAFT_SCHEMA_V not in SCHEMA_REGISTRY


# ---------------------------------------------------------------------------
# R-1076 — a record whose `expires_at` cannot be trusted must never read as still live
# ---------------------------------------------------------------------------


class TestReadInjectionDraftUntrustedExpiry:
    def _drafted_with_expiry(self, tmp_path: Path, mutate) -> tuple[str, str]:
        job, answer = _drafted(tmp_path)
        draft_id = answer["draft_id"]
        path = tmp_path / "jobs" / job.job_id / "injection_drafts" / _digest_name(draft_id)
        record = json.loads(path.read_text(encoding="utf-8"))
        mutate(record)
        path.write_text(json.dumps(record), encoding="utf-8")
        return job.job_id, draft_id

    def test_missing_expires_at_raises(self, tmp_path):
        job_id, draft_id = self._drafted_with_expiry(tmp_path, lambda r: r.pop("expires_at"))
        with pytest.raises(ti.TaskInjectionError):
            ti.read_injection_draft(job_id, draft_id, control_root_path=tmp_path)

    def test_non_string_expires_at_raises(self, tmp_path):
        job_id, draft_id = self._drafted_with_expiry(
            tmp_path, lambda r: r.__setitem__("expires_at", 12345))
        with pytest.raises(ti.TaskInjectionError):
            ti.read_injection_draft(job_id, draft_id, control_root_path=tmp_path)

    def test_unparseable_expires_at_raises(self, tmp_path):
        job_id, draft_id = self._drafted_with_expiry(
            tmp_path, lambda r: r.__setitem__("expires_at", "not-a-timestamp"))
        with pytest.raises(ti.TaskInjectionError):
            ti.read_injection_draft(job_id, draft_id, control_root_path=tmp_path)

    def test_expires_at_without_a_time_zone_raises(self, tmp_path):
        job_id, draft_id = self._drafted_with_expiry(
            tmp_path, lambda r: r.__setitem__("expires_at", "2026-01-01T00:00:00"))
        with pytest.raises(ti.TaskInjectionError):
            ti.read_injection_draft(job_id, draft_id, control_root_path=tmp_path)


# ---------------------------------------------------------------------------
# S3/T002 — `confirmed_injections`
# ---------------------------------------------------------------------------


class TestConfirmedInjections:
    def test_no_control_area_answers_empty(self, tmp_path):
        assert ti.confirmed_injections("nope", control_root_path=tmp_path) == ()

    def test_ordered_by_confirmed_at_then_draft_id(self, tmp_path):
        job_id = "f028job0000000o"
        later = _confirmed_record(task_id="INJ1", draft_id="zzzzzzzzzzzzzzzz",
                                  confirmed_at="2026-01-02T00:00:00+00:00")
        earlier = _confirmed_record(task_id="INJ2", draft_id="aaaaaaaaaaaaaaaa",
                                    confirmed_at="2026-01-01T00:00:00+00:00")
        assert ti._publish_confirmed_injection(
            job_id, later["draft_id"], later, control_root_path=tmp_path)
        assert ti._publish_confirmed_injection(
            job_id, earlier["draft_id"], earlier, control_root_path=tmp_path)

        records = ti.confirmed_injections(job_id, control_root_path=tmp_path)
        assert [r["draft_id"] for r in records] == ["aaaaaaaaaaaaaaaa", "zzzzzzzzzzzzzzzz"]

    def test_a_corrupt_file_raises(self, tmp_path):
        job_id = "f028job0000000p"
        d = _injected_tasks_dir(tmp_path, job_id)
        d.mkdir(parents=True)
        (d / "deadbeefdeadbeefdeadbeefdeadbeef.json").write_text("not json")
        with pytest.raises(ti.TaskInjectionError):
            ti.confirmed_injections(job_id, control_root_path=tmp_path)


# ---------------------------------------------------------------------------
# S3/T002 — `confirm_task_injection`
# ---------------------------------------------------------------------------


class TestConfirmTaskInjection:
    def test_a_terminal_job_answers_job_terminal_and_writes_nothing(self, tmp_path):
        job, answer = _drafted(tmp_path)
        job.state = pj.RunState.COMPLETED

        result = ti.confirm_task_injection(
            job, answer["confirm_token"], actor="bob", now=_FIXED_NOW,
            control_root_path=tmp_path)

        assert result["outcome"] == "refused" and result["code"] == "job_terminal"
        assert not _injected_tasks_dir(tmp_path, job.job_id).exists()

    def test_an_unknown_token_answers_draft_unknown(self, tmp_path):
        job = _job()
        result = ti.confirm_task_injection(
            job, "deadbeefdeadbeef", actor="bob", control_root_path=tmp_path)
        assert result["outcome"] == "refused" and result["code"] == "draft_unknown"
        assert not _injected_tasks_dir(tmp_path, job.job_id).exists()

    def test_an_expired_draft_answers_draft_expired(self, tmp_path):
        now = datetime(2026, 1, 1, tzinfo=UTC)
        job, answer = _drafted(tmp_path, now=now)
        later = now + timedelta(seconds=ti.INJECTION_DRAFT_TTL_SECONDS)

        result = ti.confirm_task_injection(
            job, answer["confirm_token"], actor="bob", now=later, control_root_path=tmp_path)

        assert result["outcome"] == "refused" and result["code"] == "draft_expired"
        assert not _injected_tasks_dir(tmp_path, job.job_id).exists()

    def test_a_record_naming_another_job_answers_draft_unknown(self, tmp_path):
        job, answer = _drafted(tmp_path)
        path = (tmp_path / "jobs" / job.job_id / "injection_drafts"
               / _digest_name(answer["draft_id"]))
        record = json.loads(path.read_text(encoding="utf-8"))
        record["job_id"] = "some-other-job"
        path.write_text(json.dumps(record), encoding="utf-8")

        result = ti.confirm_task_injection(
            job, answer["confirm_token"], actor="bob", now=_FIXED_NOW,
            control_root_path=tmp_path)

        assert result["outcome"] == "refused" and result["code"] == "draft_unknown"
        assert not _injected_tasks_dir(tmp_path, job.job_id).exists()

    def test_a_shortfall_draft_answers_draft_needs_decision(self, tmp_path):
        job = _job()
        call = _FakeCall([_draft_json(est_tokens_band="M")])
        now = datetime(2026, 1, 1, tzinfo=UTC)
        answer = ti.draft_task_injection(
            job, "add a widget", call_fn=call, budgets=JobBudgets(max_cost_usd=1.00),
            counters=_counters(0.90), config=_config(), actor="alice", now=now,
            control_root_path=tmp_path)
        assert answer["outcome"] == "shortfall"

        result = ti.confirm_task_injection(
            job, answer["draft_id"], actor="bob", now=now, control_root_path=tmp_path)

        assert result["outcome"] == "refused" and result["code"] == "draft_needs_decision"
        assert not _injected_tasks_dir(tmp_path, job.job_id).exists()

    def test_confirming_twice_answers_already_confirmed_the_second_time(self, tmp_path):
        job, answer = _drafted(tmp_path)

        first = ti.confirm_task_injection(
            job, answer["confirm_token"], actor="bob", now=_FIXED_NOW,
            control_root_path=tmp_path)
        assert first["outcome"] == "confirmed"

        second = ti.confirm_task_injection(
            job, answer["confirm_token"], actor="bob", now=_FIXED_NOW,
            control_root_path=tmp_path)
        assert second["outcome"] == "refused" and second["code"] == "already_confirmed"
        assert len(list(_injected_tasks_dir(tmp_path, job.job_id).iterdir())) == 1

    def test_task_plan_unreadable_answers_no_task_plan(self, tmp_path):
        job, answer = _drafted(tmp_path)
        job.task_plan = None

        result = ti.confirm_task_injection(
            job, answer["confirm_token"], actor="bob", now=_FIXED_NOW,
            control_root_path=tmp_path)

        assert result["outcome"] == "refused" and result["code"] == "no_task_plan"
        assert not _injected_tasks_dir(tmp_path, job.job_id).exists()

    def test_two_drafts_of_one_plan_the_second_confirmed_after_is_stale(self, tmp_path):
        job = _job()
        now = datetime(2026, 1, 1, tzinfo=UTC)
        call = _FakeCall([_draft_json(), _draft_json()])
        first_answer = ti.draft_task_injection(
            job, "add widget one", call_fn=call, budgets=JobBudgets(),
            counters=_counters(None), config=_config(price_basis=None), actor="alice",
            now=now, control_root_path=tmp_path)
        second_answer = ti.draft_task_injection(
            job, "add widget two", call_fn=call, budgets=JobBudgets(),
            counters=_counters(None), config=_config(price_basis=None), actor="alice",
            now=now, control_root_path=tmp_path)
        assert first_answer["task"]["id"] == second_answer["task"]["id"] == "INJ1"

        first = ti.confirm_task_injection(
            job, first_answer["confirm_token"], actor="bob", now=now,
            control_root_path=tmp_path)
        assert first["outcome"] == "confirmed"

        second = ti.confirm_task_injection(
            job, second_answer["confirm_token"], actor="bob", now=now,
            control_root_path=tmp_path)
        assert second["outcome"] == "refused" and second["code"] == "draft_stale"
        assert len(list(_injected_tasks_dir(tmp_path, job.job_id).iterdir())) == 1

    def test_a_depends_on_id_no_longer_in_the_plan_is_stale(self, tmp_path):
        job = _job(tasks=[_task("T1"), _task("T2")])
        job, answer = _drafted(job=job, tmp_path=tmp_path, after="T2")
        assert answer["placement"]["depends_on"] == ["T2"]

        # T2 leaves the plan before this draft is confirmed.
        job.task_plan = _plan_dict([_task("T1")])

        result = ti.confirm_task_injection(
            job, answer["confirm_token"], actor="bob", now=_FIXED_NOW,
            control_root_path=tmp_path)

        assert result["outcome"] == "refused" and result["code"] == "draft_stale"
        assert not _injected_tasks_dir(tmp_path, job.job_id).exists()

    def test_plan_full_counted_over_confirmed_injections(self, tmp_path):
        tasks = [_task(f"T{i}") for i in range(1, ti.MAX_PLAN_TASKS)]     # 24 tasks
        job = _job(tasks=tasks)
        prior = _confirmed_record(task_id="INJZ", draft_id="priorid00000001")
        assert ti._publish_confirmed_injection(
            job.job_id, prior["draft_id"], prior, control_root_path=tmp_path)

        job, answer = _drafted(tmp_path, job=job)          # a fresh, non-colliding id

        result = ti.confirm_task_injection(
            job, answer["confirm_token"], actor="bob", now=_FIXED_NOW,
            control_root_path=tmp_path)

        assert result["outcome"] == "refused" and result["code"] == "plan_full"
        assert len(list(_injected_tasks_dir(tmp_path, job.job_id).iterdir())) == 1

    def test_confirmed_answer_reads_back_through_confirmed_injections(self, tmp_path):
        job, answer = _drafted(tmp_path)

        result = ti.confirm_task_injection(
            job, answer["confirm_token"], actor="bob", now=_FIXED_NOW,
            control_root_path=tmp_path)

        assert result == {
            "outcome": "confirmed", "job_id": job.job_id, "draft_id": answer["draft_id"],
            "task_id": answer["task"]["id"], "placement": answer["placement"],
            "confirmed_at": result["confirmed_at"],
        }
        [record] = ti.confirmed_injections(job.job_id, control_root_path=tmp_path)
        assert record["draft_id"] == answer["draft_id"]
        assert record["task"] == answer["task"]
        assert record["placement"] == answer["placement"]
        assert record["task_rationale"] == answer["task_rationale"]
        assert record["text"] == answer["text"]
        assert record["drafted_by"] == "alice"
        assert record["actor"] == "bob"
        assert record["confirmed_at"] == result["confirmed_at"]

    def test_unseen_true_is_stored_on_disk(self, tmp_path):
        job, answer = _drafted(tmp_path)

        result = ti.confirm_task_injection(
            job, answer["confirm_token"], actor="bob", unseen=True, now=_FIXED_NOW,
            control_root_path=tmp_path)

        assert result["outcome"] == "confirmed"
        [record] = ti.confirmed_injections(job.job_id, control_root_path=tmp_path)
        assert record["confirmed_unseen"] is True

    def test_unseen_defaults_to_false(self, tmp_path):
        job, answer = _drafted(tmp_path)

        result = ti.confirm_task_injection(
            job, answer["confirm_token"], actor="bob", now=_FIXED_NOW,
            control_root_path=tmp_path)

        assert result["outcome"] == "confirmed"
        [record] = ti.confirmed_injections(job.job_id, control_root_path=tmp_path)
        assert record["confirmed_unseen"] is False


# ---------------------------------------------------------------------------
# S4/T002 — `apply_injection_to_job`
# ---------------------------------------------------------------------------


class TestApplyInjectionToJob:
    def test_appends_provenance_bumps_version_and_reseals_an_approved_hash(self):
        job = _job(tasks=[_task("T1")])
        body = dict(job.task_plan)
        body["_approval"] = "approved"
        body[PLAN_VERSION_KEY] = 3
        body[APPROVED_PLAN_HASH_KEY] = plan_content_hash(body)
        old_hash = body[APPROVED_PLAN_HASH_KEY]
        job.task_plan = body

        record = _confirmed_record(depends_on=["T1"])
        result = ti.apply_injection_to_job(job, record)

        new_task = next(
            t for t in job.tasks
            if (t.inputs.get("plan") or {}).get("planned_id") == "INJ1")
        assert result == {"task_id": new_task.task_id, "planned_id": "INJ1",
                          "folded_at": result["folded_at"]}
        plan_info = new_task.inputs["plan"]
        assert plan_info["origin"] == ti.ORIGIN_HUMAN_INJECTED
        assert plan_info["plan_rationale"] == "placed at the end"
        assert plan_info["task_rationale"] == "because the operator asked"
        assert plan_info["injection_draft_id"] == "draftabc00000001"

        assert job.task_plan[PLAN_VERSION_KEY] == 4
        assert job.task_plan[APPROVED_PLAN_HASH_KEY] == plan_content_hash(job.task_plan)
        assert job.task_plan[APPROVED_PLAN_HASH_KEY] != old_hash

        [entry] = job.task_plan[EDIT_LOG_KEY]
        assert entry["command"] == "plan_add_task"
        assert entry["actor"] == "alice"
        assert entry["args"] == {"task": record["task"]}
        assert entry["injection"] == {
            "draft_id": "draftabc00000001", "task_id": new_task.task_id, "planned_id": "INJ1",
            "origin": ti.ORIGIN_HUMAN_INJECTED, "basis": "frontier_default",
            "plan_rationale": "placed at the end", "text": "add the thing",
            "confirmed_at": "2026-01-01T00:00:00+00:00",
            # DECISION F028 D4 (2): unconditional, unlike `budget_extend_to_usd` below —
            # `_confirmed_record()` carries no `confirmed_unseen` key, so this reads its
            # `.get(..., False)` default.
            "confirmed_unseen": False,
            "dod_resync_pending": False,
        }

    def test_an_unapproved_plan_keeps_no_approval_hash(self):
        job = _job(tasks=[_task("T1")])
        body = dict(job.task_plan)
        body["_approval"] = "pending"
        job.task_plan = body

        ti.apply_injection_to_job(job, _confirmed_record())

        assert APPROVED_PLAN_HASH_KEY not in job.task_plan

    def test_dod_resync_pending_true_with_a_dod_file_present(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _job(tasks=[_task("T1")], job_id="f028job0000000q")
        dod_path = job_dod_path(job.job_id)
        dod_path.parent.mkdir(parents=True, exist_ok=True)
        dod_path.write_text("{}")

        ti.apply_injection_to_job(job, _confirmed_record())

        [entry] = job.task_plan[EDIT_LOG_KEY]
        assert entry["injection"]["dod_resync_pending"] is True

    def test_dod_resync_pending_false_without_a_dod_file(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _job(tasks=[_task("T1")], job_id="f028job0000000r")

        ti.apply_injection_to_job(job, _confirmed_record())

        [entry] = job.task_plan[EDIT_LOG_KEY]
        assert entry["injection"]["dod_resync_pending"] is False

    def test_replay_edits_reproduces_the_new_plans_tasks(self):
        job = _job(tasks=[_task("T1"), _task("T2")])
        original = TaskPlan.model_validate(
            {k: v for k, v in job.task_plan.items() if not k.startswith("_")})

        ti.apply_injection_to_job(job, _confirmed_record(depends_on=["T1"]))

        replayed = replay_edits(original, job.task_plan[EDIT_LOG_KEY])
        assert [t.id for t in replayed.tasks] == ["T1", "T2", "INJ1"]
        assert replayed.tasks[-1].depends_on == ["T1"]

    def test_a_missing_dependency_raises_injection_invalid_and_leaves_the_job_unchanged(self):
        job = _job(tasks=[_task("T1")])
        before_plan = dict(job.task_plan)
        before_tasks = list(job.tasks)

        with pytest.raises(ti.TaskInjectionRefused) as exc:
            ti.apply_injection_to_job(job, _confirmed_record(depends_on=["GHOST"]))

        assert exc.value.code == "injection_invalid"
        assert job.task_plan == before_plan
        assert job.tasks == before_tasks

    @pytest.mark.parametrize(
        "field", ["task", "placement", "task_rationale", "draft_id", "actor", "text",
                 "confirmed_at"])
    def test_a_field_missing_from_the_record_raises_and_leaves_the_job_unchanged(self, field):
        job = _job(tasks=[_task("T1")])
        job.budgets = {"max_cost_usd": 1.00}
        before_plan = dict(job.task_plan)
        before_tasks = list(job.tasks)
        before_budgets = dict(job.budgets)
        record = _confirmed_record()
        del record[field]

        with pytest.raises(Exception):                      # noqa: BLE001 — any read failure
            ti.apply_injection_to_job(job, record)

        assert job.task_plan == before_plan
        assert job.tasks == before_tasks
        assert job.budgets == before_budgets


# ---------------------------------------------------------------------------
# R-1077 — every field `apply_injection_to_job` reads must exist, with its type, before a
# confirmed injection is trusted (`confirmed_injections`)
# ---------------------------------------------------------------------------


class TestConfirmedRecordFieldValidation:
    def _publish(self, tmp_path: Path, record: dict, *, job_id: str = "f028job0000000s") -> str:
        raw_id = record.get("draft_id")
        name_id = raw_id if isinstance(raw_id, str) and raw_id else "fallbackid00000"
        assert ti._publish_confirmed_injection(
            job_id, name_id, record, control_root_path=tmp_path)
        return job_id

    @pytest.mark.parametrize(
        "field", ["draft_id", "task_rationale", "text", "actor", "confirmed_at"])
    def test_missing_string_field_raises(self, tmp_path, field):
        record = _confirmed_record()
        del record[field]
        job_id = self._publish(tmp_path, record)
        with pytest.raises(ti.TaskInjectionError):
            ti.confirmed_injections(job_id, control_root_path=tmp_path)

    @pytest.mark.parametrize(
        "field", ["draft_id", "task_rationale", "text", "actor", "confirmed_at"])
    def test_wrong_type_string_field_raises(self, tmp_path, field):
        record = _confirmed_record()
        record[field] = 5
        job_id = self._publish(tmp_path, record)
        with pytest.raises(ti.TaskInjectionError):
            ti.confirmed_injections(job_id, control_root_path=tmp_path)

    def test_missing_task_raises(self, tmp_path):
        record = _confirmed_record()
        del record["task"]
        job_id = self._publish(tmp_path, record)
        with pytest.raises(ti.TaskInjectionError):
            ti.confirmed_injections(job_id, control_root_path=tmp_path)

    def test_task_wrong_type_raises(self, tmp_path):
        record = _confirmed_record()
        record["task"] = "not a dict"
        job_id = self._publish(tmp_path, record)
        with pytest.raises(ti.TaskInjectionError):
            ti.confirmed_injections(job_id, control_root_path=tmp_path)

    def test_missing_placement_raises(self, tmp_path):
        record = _confirmed_record()
        del record["placement"]
        job_id = self._publish(tmp_path, record)
        with pytest.raises(ti.TaskInjectionError):
            ti.confirmed_injections(job_id, control_root_path=tmp_path)

    def test_placement_wrong_type_raises(self, tmp_path):
        record = _confirmed_record()
        record["placement"] = "not a dict"
        job_id = self._publish(tmp_path, record)
        with pytest.raises(ti.TaskInjectionError):
            ti.confirmed_injections(job_id, control_root_path=tmp_path)

    def test_placement_missing_rationale_raises(self, tmp_path):
        record = _confirmed_record()
        del record["placement"]["rationale"]
        job_id = self._publish(tmp_path, record)
        with pytest.raises(ti.TaskInjectionError):
            ti.confirmed_injections(job_id, control_root_path=tmp_path)

    def test_placement_wrong_type_rationale_raises(self, tmp_path):
        record = _confirmed_record()
        record["placement"]["rationale"] = 5
        job_id = self._publish(tmp_path, record)
        with pytest.raises(ti.TaskInjectionError):
            ti.confirmed_injections(job_id, control_root_path=tmp_path)

    def test_placement_missing_basis_raises(self, tmp_path):
        record = _confirmed_record()
        del record["placement"]["basis"]
        job_id = self._publish(tmp_path, record)
        with pytest.raises(ti.TaskInjectionError):
            ti.confirmed_injections(job_id, control_root_path=tmp_path)

    def test_placement_wrong_type_basis_raises(self, tmp_path):
        record = _confirmed_record()
        record["placement"]["basis"] = 5
        job_id = self._publish(tmp_path, record)
        with pytest.raises(ti.TaskInjectionError):
            ti.confirmed_injections(job_id, control_root_path=tmp_path)

    def test_absent_budget_extend_to_usd_is_valid(self, tmp_path):
        record = _confirmed_record()
        job_id = self._publish(tmp_path, record)
        [got] = ti.confirmed_injections(job_id, control_root_path=tmp_path)
        assert "budget_extend_to_usd" not in got

    def test_budget_extend_to_usd_none_is_valid(self, tmp_path):
        record = _confirmed_record(budget_extend_to_usd=None)
        job_id = self._publish(tmp_path, record)
        [got] = ti.confirmed_injections(job_id, control_root_path=tmp_path)
        assert got["budget_extend_to_usd"] is None

    def test_budget_extend_to_usd_valid_number_is_accepted(self, tmp_path):
        record = _confirmed_record(budget_extend_to_usd=1.5)
        job_id = self._publish(tmp_path, record)
        [got] = ti.confirmed_injections(job_id, control_root_path=tmp_path)
        assert got["budget_extend_to_usd"] == 1.5

    @pytest.mark.parametrize("bad", [0, -1.0, True, "1.22"])
    def test_budget_extend_to_usd_invalid_value_raises(self, tmp_path, bad):
        record = _confirmed_record(budget_extend_to_usd=bad)
        job_id = self._publish(tmp_path, record)
        with pytest.raises(ti.TaskInjectionError):
            ti.confirmed_injections(job_id, control_root_path=tmp_path)

    def test_absent_confirmed_unseen_is_valid(self, tmp_path):
        record = _confirmed_record()
        job_id = self._publish(tmp_path, record)
        [got] = ti.confirmed_injections(job_id, control_root_path=tmp_path)
        assert "confirmed_unseen" not in got

    @pytest.mark.parametrize("value", [True, False])
    def test_confirmed_unseen_bool_is_valid(self, tmp_path, value):
        record = _confirmed_record(confirmed_unseen=value)
        job_id = self._publish(tmp_path, record)
        [got] = ti.confirmed_injections(job_id, control_root_path=tmp_path)
        assert got["confirmed_unseen"] is value

    @pytest.mark.parametrize("bad", [1, 0, "true", None])
    def test_confirmed_unseen_mistyped_raises(self, tmp_path, bad):
        record = _confirmed_record(confirmed_unseen=bad)
        job_id = self._publish(tmp_path, record)
        with pytest.raises(ti.TaskInjectionError):
            ti.confirmed_injections(job_id, control_root_path=tmp_path)


# ---------------------------------------------------------------------------
# DECISION F028 D3 (2) — the extension: raised, never created, never lowered
# ---------------------------------------------------------------------------


class TestApplyInjectionToJobBudgetExtension:
    def test_raises_a_lower_limit_to_the_extension(self):
        job = _job(tasks=[_task("T1")])
        job.budgets = {"max_cost_usd": 1.00}

        ti.apply_injection_to_job(job, _confirmed_record(budget_extend_to_usd=1.22))

        assert job.budgets["max_cost_usd"] == 1.22
        [entry] = job.task_plan[EDIT_LOG_KEY]
        assert entry["injection"]["budget_extend_to_usd"] == 1.22

    def test_never_lowers_an_already_higher_limit(self):
        job = _job(tasks=[_task("T1")])
        job.budgets = {"max_cost_usd": 2.00}

        ti.apply_injection_to_job(job, _confirmed_record(budget_extend_to_usd=1.22))

        assert job.budgets["max_cost_usd"] == 2.00

    def test_never_creates_a_limit_on_a_job_without_one(self):
        job = _job(tasks=[_task("T1")])
        assert job.budgets is None

        ti.apply_injection_to_job(job, _confirmed_record(budget_extend_to_usd=1.22))

        assert job.budgets is None

    def test_no_extension_named_leaves_the_limit_and_the_injection_block_untouched(self):
        job = _job(tasks=[_task("T1")])
        job.budgets = {"max_cost_usd": 1.00}

        ti.apply_injection_to_job(job, _confirmed_record())

        assert job.budgets == {"max_cost_usd": 1.00}
        [entry] = job.task_plan[EDIT_LOG_KEY]
        assert "budget_extend_to_usd" not in entry["injection"]


class TestApplyInjectionToJobConfirmedUnseen:
    """DECISION F028 D4 (2): the injection block always carries `confirmed_unseen`."""

    def test_unseen_true_is_logged_in_the_injection_block(self):
        job = _job(tasks=[_task("T1")])

        ti.apply_injection_to_job(job, _confirmed_record(confirmed_unseen=True))

        [entry] = job.task_plan[EDIT_LOG_KEY]
        assert entry["injection"]["confirmed_unseen"] is True

    def test_absent_confirmed_unseen_logs_false(self):
        job = _job(tasks=[_task("T1")])

        ti.apply_injection_to_job(job, _confirmed_record())

        [entry] = job.task_plan[EDIT_LOG_KEY]
        assert entry["injection"]["confirmed_unseen"] is False


# ---------------------------------------------------------------------------
# DECISION F028 D3 (1) — `answer_injection_shortfall`
# ---------------------------------------------------------------------------


def _drafted_shortfall(tmp_path: Path, *, job: pj.JobPlan | None = None, band: str = "M",
                       counters: BudgetCounters | None = None,
                       now: datetime = _FIXED_NOW) -> tuple[pj.JobPlan, dict]:
    """A job with one freshly drafted injection whose check shortfalls: ``(job, answer)``."""
    job = job if job is not None else _job()
    call = _FakeCall([_draft_json(est_tokens_band=band)])
    answer = ti.draft_task_injection(
        job, "add a widget", call_fn=call, budgets=JobBudgets(max_cost_usd=1.00),
        counters=counters if counters is not None else _counters(0.90), config=_config(),
        actor="alice", now=now, control_root_path=tmp_path)
    assert answer["outcome"] == "shortfall"
    return job, answer


class TestAnswerInjectionShortfall:
    def test_a_terminal_job_answers_job_terminal_and_writes_nothing(self, tmp_path):
        job, answer = _drafted_shortfall(tmp_path)
        job.state = pj.RunState.COMPLETED

        result = ti.answer_injection_shortfall(
            job, answer["draft_id"], "drop", actor="bob",
            budgets=JobBudgets(max_cost_usd=1.00), counters=_counters(0.90), config=_config(),
            now=_FIXED_NOW, control_root_path=tmp_path)

        assert result["outcome"] == "refused" and result["code"] == "job_terminal"
        assert not (tmp_path / "jobs" / job.job_id / ti.INJECTION_ANSWERS_DIRNAME).exists()

    def test_an_unknown_draft_answers_draft_unknown(self, tmp_path):
        job = _job()
        result = ti.answer_injection_shortfall(
            job, "deadbeefdeadbeef", "drop", actor="bob", budgets=JobBudgets(),
            counters=_counters(None), config=_config(price_basis=None),
            control_root_path=tmp_path)
        assert result["outcome"] == "refused" and result["code"] == "draft_unknown"

    def test_a_confirmable_draft_answers_draft_not_in_shortfall(self, tmp_path):
        job, answer = _drafted(tmp_path)
        result = ti.answer_injection_shortfall(
            job, answer["draft_id"], "drop", actor="bob", budgets=JobBudgets(),
            counters=_counters(None), config=_config(price_basis=None), now=_FIXED_NOW,
            control_root_path=tmp_path)
        assert result["outcome"] == "refused" and result["code"] == "draft_not_in_shortfall"

    def test_an_unknown_option_answers_unknown_option(self, tmp_path):
        job, answer = _drafted_shortfall(tmp_path)
        result = ti.answer_injection_shortfall(
            job, answer["draft_id"], "explode", actor="bob",
            budgets=JobBudgets(max_cost_usd=1.00), counters=_counters(0.90), config=_config(),
            now=_FIXED_NOW, control_root_path=tmp_path)
        assert result["outcome"] == "refused" and result["code"] == "unknown_option"

    def test_cannot_shrink_when_already_the_smallest_size(self, tmp_path):
        job, answer = _drafted_shortfall(tmp_path, band="S", counters=_counters(0.95))
        result = ti.answer_injection_shortfall(
            job, answer["draft_id"], "shrink_task", actor="bob",
            budgets=JobBudgets(max_cost_usd=1.00), counters=_counters(0.95), config=_config(),
            now=_FIXED_NOW, control_root_path=tmp_path)
        assert result["outcome"] == "refused" and result["code"] == "cannot_shrink"

    def test_drop_answers_dropped_and_writes_one_answer_file(self, tmp_path):
        job, answer = _drafted_shortfall(tmp_path)
        result = ti.answer_injection_shortfall(
            job, answer["draft_id"], "drop", actor="bob",
            budgets=JobBudgets(max_cost_usd=1.00), counters=_counters(0.90), config=_config(),
            now=_FIXED_NOW, control_root_path=tmp_path)

        assert result == {"outcome": "dropped", "job_id": job.job_id,
                          "draft_id": answer["draft_id"], "answered_at": result["answered_at"]}
        answers_dir = tmp_path / "jobs" / job.job_id / ti.INJECTION_ANSWERS_DIRNAME
        assert len(list(answers_dir.iterdir())) == 1

    def test_a_second_answer_is_refused_already_answered(self, tmp_path):
        job, answer = _drafted_shortfall(tmp_path)
        first = ti.answer_injection_shortfall(
            job, answer["draft_id"], "drop", actor="bob",
            budgets=JobBudgets(max_cost_usd=1.00), counters=_counters(0.90), config=_config(),
            now=_FIXED_NOW, control_root_path=tmp_path)
        assert first["outcome"] == "dropped"

        second = ti.answer_injection_shortfall(
            job, answer["draft_id"], "shrink_task", actor="bob",
            budgets=JobBudgets(max_cost_usd=1.00), counters=_counters(0.90), config=_config(),
            now=_FIXED_NOW, control_root_path=tmp_path)
        assert second["outcome"] == "refused" and second["code"] == "already_answered"

    def test_shrink_task_from_m_to_s_answers_a_confirmable_derived_draft(self, tmp_path):
        job, answer = _drafted_shortfall(tmp_path, band="M", counters=_counters(0.90))

        result = ti.answer_injection_shortfall(
            job, answer["draft_id"], "shrink_task", actor="bob",
            budgets=JobBudgets(max_cost_usd=1.00), counters=_counters(0.90), config=_config(),
            now=_FIXED_NOW, control_root_path=tmp_path)

        assert result["outcome"] == "drafted"
        assert result["task"]["est_tokens_band"] == "S"
        assert result["confirm_token"] == result["draft_id"]
        assert result["derived_from"] == answer["draft_id"]
        assert result["answer"] == "shrink_task"
        assert result["budget_extend_to_usd"] is None
        assert result["budget_check"]["shortfall"] is False

        record = ti.read_injection_draft(job.job_id, result["draft_id"], now=_FIXED_NOW,
                                         control_root_path=tmp_path)
        assert record["status"] == "confirmable"
        assert record["derived_from"] == answer["draft_id"]

    def test_shrink_task_from_l_to_m_is_still_a_shortfall(self, tmp_path):
        job, answer = _drafted_shortfall(tmp_path, band="L", counters=_counters(0.90))

        result = ti.answer_injection_shortfall(
            job, answer["draft_id"], "shrink_task", actor="bob",
            budgets=JobBudgets(max_cost_usd=1.00), counters=_counters(0.90), config=_config(),
            now=_FIXED_NOW, control_root_path=tmp_path)

        assert result["outcome"] == "shortfall"
        assert result["task"]["est_tokens_band"] == "M"
        assert result["confirm_token"] is None
        assert result["decision_seed"] is not None
        assert result["budget_check"]["shortfall"] is True

        record = ti.read_injection_draft(job.job_id, result["draft_id"], now=_FIXED_NOW,
                                         control_root_path=tmp_path)
        assert record["status"] == "needs_decision"

    def test_extend_budget_answers_a_confirmable_draft_with_no_shortfall(self, tmp_path):
        job, answer = _drafted_shortfall(tmp_path, band="M", counters=_counters(0.90))

        result = ti.answer_injection_shortfall(
            job, answer["draft_id"], "extend_budget", actor="bob",
            budgets=JobBudgets(max_cost_usd=1.00), counters=_counters(0.90), config=_config(),
            now=_FIXED_NOW, control_root_path=tmp_path)

        assert result["outcome"] == "drafted"
        assert result["budget_extend_to_usd"] == 1.22
        assert result["budget_check"]["shortfall"] is False
        assert result["task"]["est_tokens_band"] == "M"
        assert result["confirm_token"] == result["draft_id"]

        record = ti.read_injection_draft(job.job_id, result["draft_id"], now=_FIXED_NOW,
                                         control_root_path=tmp_path)
        assert record["status"] == "confirmable"
        assert record["budget_extend_to_usd"] == 1.22

    def test_extend_budget_recomputes_the_larger_amount_when_spend_grew(self, tmp_path):
        """DECISION F028 D4 (4): spend grew from $0.90 (draft time) to $0.98 (answer time)
        at band M — the seed said $1.22; the re-check says $1.30, and $1.30 wins."""
        job, answer = _drafted_shortfall(tmp_path, band="M", counters=_counters(0.90))
        assert answer["decision_seed"]["extend_to_usd"] == 1.22

        result = ti.answer_injection_shortfall(
            job, answer["draft_id"], "extend_budget", actor="bob",
            budgets=JobBudgets(max_cost_usd=1.00), counters=_counters(0.98), config=_config(),
            now=_FIXED_NOW, control_root_path=tmp_path)

        assert result["outcome"] == "drafted"
        assert result["budget_extend_to_usd"] == 1.30
        assert result["budget_check"]["shortfall"] is False

    def test_extend_budget_keeps_the_seeds_amount_when_it_is_larger(self, tmp_path):
        """Spend at answer time ($0.50) is LOWER than at draft time ($0.90) — the re-check's
        own sum ($0.82) is smaller than the seed's $1.22, so the seed's amount wins."""
        job, answer = _drafted_shortfall(tmp_path, band="M", counters=_counters(0.90))
        assert answer["decision_seed"]["extend_to_usd"] == 1.22

        result = ti.answer_injection_shortfall(
            job, answer["draft_id"], "extend_budget", actor="bob",
            budgets=JobBudgets(max_cost_usd=1.00), counters=_counters(0.50), config=_config(),
            now=_FIXED_NOW, control_root_path=tmp_path)

        assert result["outcome"] == "drafted"
        assert result["budget_extend_to_usd"] == 1.22

    def test_the_old_shortfall_draft_still_refuses_confirmation(self, tmp_path):
        job, answer = _drafted_shortfall(tmp_path, band="M", counters=_counters(0.90))
        ti.answer_injection_shortfall(
            job, answer["draft_id"], "extend_budget", actor="bob",
            budgets=JobBudgets(max_cost_usd=1.00), counters=_counters(0.90), config=_config(),
            now=_FIXED_NOW, control_root_path=tmp_path)

        result = ti.confirm_task_injection(
            job, answer["draft_id"], actor="bob", now=_FIXED_NOW, control_root_path=tmp_path)
        assert result["outcome"] == "refused" and result["code"] == "draft_needs_decision"
