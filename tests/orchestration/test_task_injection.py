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


def _confirmed_record(*, task_id: str = "INJ1", depends_on: tuple[str, ...] = (),
                      actor: str = "alice", draft_id: str = "draftabc00000001",
                      confirmed_at: str = "2026-01-01T00:00:00+00:00",
                      basis: str = "frontier_default") -> dict:
    """A confirmed-injection record shaped exactly as ``confirm_task_injection`` writes one —
    built directly so ``apply_injection_to_job`` (S4) can be tested independent of S3."""
    return {
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
        assert "cannot shrink" in seed["option_labels"][seed["options"].index("shrink_task")]

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
            "confirmed_at": "2026-01-01T00:00:00+00:00", "dod_resync_pending": False,
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
