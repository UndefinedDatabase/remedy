"""F027 T002 — the `replan_proposal` decision, its answer as a create-only control fact,
and the follow-up job a replan creates and never runs (DECISION F027 D4).

Graph rows build their plan with ``test_dag_schedule.flight_task``, imported, exactly as
``test_task_veto.py`` does, so this module's unreachable readings and
``dag_schedule.blocked_downstream`` cannot drift apart. Jobs are built directly as
``pingpong_job.JobPlan`` — never a constructed ``HumanDecision`` — over the data root and
the control root the runner tests use.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from packages.core.models import RunState
from packages.orchestration import pingpong_job as pj
from packages.orchestration import task_veto as tv
from packages.orchestration import veto_proposal as vp
from packages.orchestration.decision_evidence import enforce_decision_evidence
from packages.orchestration.pingpong_job import load_job_plan, save_job_plan
from tests.orchestration.test_dag_schedule import flight_task
from tests.orchestration.test_dag_schedule import ids as dag_ids

JOB = "f027job0000000b"


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path: Path, monkeypatch):
    """REMEDY_DATA_DIR to tmp so the ledger reader/writer never touch the real data root."""
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


@pytest.fixture
def control(tmp_path: Path) -> Path:
    """A control root of our own. Nothing here touches the developer's real data dir."""
    return tmp_path / "control"


@pytest.fixture
def jobs_root(tmp_path: Path) -> Path:
    """Where `answer_replan_proposal`'s follow-up job is saved."""
    return tmp_path / "jobs_root"


def _job(tasks: list, *, job_id: str = JOB, repo_path: str = "/repo/original",
        project_id: str = "proj-original") -> pj.JobPlan:
    return pj.JobPlan(job_id=job_id, tasks=tasks, state=RunState.RUNNING,
                      repo_path=repo_path, project_id=project_id)


def _read_events(job_id: str) -> list[dict]:
    from packages.orchestration.data_paths import run_log_dir

    out: list[dict] = []
    job_runs = run_log_dir(job_id)
    if not job_runs.is_dir():
        return out
    for jsonl in sorted(job_runs.glob("*.jsonl")):
        for line in jsonl.read_text(encoding="utf-8").splitlines():
            if line.strip():
                out.append(json.loads(line))
    return out


def _veto_answered_events(job_id: str) -> list[dict]:
    return [e for e in _read_events(job_id) if e["event"] == "veto_proposal_answered"]


# ---------------------------------------------------------------------------
# The decision's shape and its evidence triple
# ---------------------------------------------------------------------------


class TestDecisionShape:
    def test_id_type_severity_summary_payload_and_evidence(self, control):
        tasks = [flight_task("A"), flight_task("B", "A")]
        job = _job(tasks)
        a_id, b_id = dag_ids(tasks, "A", "B")

        result = tv.veto_task_command(
            job, task_id=a_id, reason="known-bad approach", actor="alice",
            control_root_path=control)
        assert result["outcome"] == "vetoed"

        decisions = vp.replan_proposal_decisions(job, control_root_path=control)
        assert len(decisions) == 1
        d = decisions[0]

        assert d.id == f"veto:{result['request_id']}"
        assert d.type == "replan_proposal"
        assert d.status == "open"
        assert d.severity == "blocker"
        title = job.tasks[0].title
        assert d.safe_summary.startswith(
            f"You vetoed {title} — reason: known-bad approach")
        assert d.payload["options"] == ["replan_follow_up", "accept_reduced_scope"]
        assert d.payload["task_id"] == a_id
        assert d.payload["request_id"] == result["request_id"]
        assert d.payload["reason"] == "known-bad approach"
        assert d.payload["unreachable_task_ids"] == [b_id]

        # Must not raise: the emit gate `list_decisions` itself uses.
        enforce_decision_evidence(decisions)


# ---------------------------------------------------------------------------
# One card per veto; none for an inert veto or an answered one
# ---------------------------------------------------------------------------


class TestCardPresence:
    def test_one_card_per_veto(self, control):
        tasks = [flight_task("A"), flight_task("B"), flight_task("C", "A"),
                 flight_task("D", "B")]
        job = _job(tasks)
        a_id, b_id = dag_ids(tasks, "A", "B")
        r1 = tv.veto_task_command(job, task_id=a_id, reason="reason one", actor="alice",
                                  control_root_path=control)
        r2 = tv.veto_task_command(job, task_id=b_id, reason="reason two", actor="alice",
                                  control_root_path=control)
        assert r1["outcome"] == r2["outcome"] == "vetoed"

        decisions = vp.replan_proposal_decisions(job, control_root_path=control)
        assert {d.payload["request_id"] for d in decisions} == {
            r1["request_id"], r2["request_id"]}

    def test_no_card_for_an_inert_veto(self, control):
        """The task moved on to a status the veto no longer holds (e.g. applied):
        `_qualifying_entries` drops it, exactly as the fold would leave it inert."""
        tasks = [flight_task("A")]
        job = _job(tasks)
        a_id = dag_ids(tasks, "A")[0]
        result = tv.veto_task_command(job, task_id=a_id, reason="x", actor="a",
                                      control_root_path=control)
        assert result["outcome"] == "vetoed"
        job.tasks[0].status = pj.TASK_APPLIED

        assert vp.replan_proposal_decisions(job, control_root_path=control) == []

    def test_no_card_for_an_answered_veto(self, control, jobs_root):
        tasks = [flight_task("A")]
        job = _job(tasks)
        a_id = dag_ids(tasks, "A")[0]
        result = tv.veto_task_command(job, task_id=a_id, reason="x", actor="a",
                                      control_root_path=control)
        decision_id = f"veto:{result['request_id']}"
        answer = vp.answer_replan_proposal(job, decision_id, tv.ACCEPT_REDUCED_SCOPE,
                                           actor="a", control_root_path=control,
                                           root=jobs_root)
        assert answer["outcome"] == "answered"

        assert vp.replan_proposal_decisions(job, control_root_path=control) == []


# ---------------------------------------------------------------------------
# Refusals — each in its order, nothing written
# ---------------------------------------------------------------------------


class TestRefusals:
    def test_an_id_not_naming_veto_is_unknown_decision(self, control, jobs_root):
        tasks = [flight_task("A")]
        job = _job(tasks)
        result = vp.answer_replan_proposal(
            job, "bogus:xyz", tv.ACCEPT_REDUCED_SCOPE, actor="a",
            control_root_path=control, root=jobs_root)
        assert result == {
            "outcome": "refused", "code": "unknown_decision",
            "detail": "'bogus:xyz' does not name a veto of this job",
            "decision_id": "bogus:xyz",
        }
        assert not (control / "jobs").exists()
        assert not jobs_root.exists()

    def test_a_veto_prefixed_id_naming_no_entry_is_unknown_decision(self, control, jobs_root):
        tasks = [flight_task("A")]
        job = _job(tasks)
        result = vp.answer_replan_proposal(
            job, "veto:doesnotexist", tv.ACCEPT_REDUCED_SCOPE, actor="a",
            control_root_path=control, root=jobs_root)
        assert result["outcome"] == "refused"
        assert result["code"] == "unknown_decision"
        assert not (control / "jobs").exists()
        assert not jobs_root.exists()

    def test_an_option_outside_the_two_is_invalid_option(self, control, jobs_root):
        tasks = [flight_task("A")]
        job = _job(tasks)
        a_id = dag_ids(tasks, "A")[0]
        result = tv.veto_task_command(job, task_id=a_id, reason="x", actor="a",
                                      control_root_path=control)
        decision_id = f"veto:{result['request_id']}"

        refusal = vp.answer_replan_proposal(
            job, decision_id, "bogus_option", actor="a",
            control_root_path=control, root=jobs_root)
        assert refusal["outcome"] == "refused"
        assert refusal["code"] == "invalid_option"
        assert tv.veto_answers(job.job_id, control_root_path=control) == {}
        assert not jobs_root.exists()
        assert _veto_answered_events(job.job_id) == []


# ---------------------------------------------------------------------------
# An accept: the answer file, one event, no job
# ---------------------------------------------------------------------------


class TestAccept:
    def test_writes_the_answer_file_one_event_and_no_job(self, control, jobs_root):
        tasks = [flight_task("A"), flight_task("B", "A")]
        job = _job(tasks)
        a_id = dag_ids(tasks, "A")[0]
        result = tv.veto_task_command(job, task_id=a_id, reason="x", actor="alice",
                                      control_root_path=control)
        decision_id = f"veto:{result['request_id']}"

        answer = vp.answer_replan_proposal(
            job, decision_id, tv.ACCEPT_REDUCED_SCOPE, actor="alice",
            control_root_path=control, root=jobs_root)
        assert answer == {
            "outcome": "answered", "decision_id": decision_id,
            "option": tv.ACCEPT_REDUCED_SCOPE, "follow_up_job_id": "",
        }

        stored = tv.veto_answers(job.job_id, control_root_path=control)
        assert stored[result["request_id"]].option == tv.ACCEPT_REDUCED_SCOPE
        assert stored[result["request_id"]].follow_up_job_id == ""

        assert len(_veto_answered_events(job.job_id)) == 1
        assert not jobs_root.exists()


# ---------------------------------------------------------------------------
# A replan: the answer file, one event, exactly one new job
# ---------------------------------------------------------------------------


class TestReplan:
    def test_creates_exactly_one_new_job_and_leaves_the_original_untouched(
            self, control, jobs_root):
        tasks = [flight_task("A"), flight_task("B", "A"), flight_task("C", "A")]
        job = _job(tasks, repo_path="/repo/x", project_id="proj-9")
        original_path = save_job_plan(job, jobs_root)
        before = original_path.read_bytes()

        a_id, b_id, c_id = dag_ids(tasks, "A", "B", "C")
        result = tv.veto_task_command(job, task_id=a_id, reason="known-bad approach",
                                      actor="alice", control_root_path=control)
        decision_id = f"veto:{result['request_id']}"

        answer = vp.answer_replan_proposal(
            job, decision_id, tv.REPLAN_FOLLOW_UP, actor="alice",
            control_root_path=control, root=jobs_root)
        assert answer["outcome"] == "answered"
        assert answer["option"] == tv.REPLAN_FOLLOW_UP
        follow_up_id = answer["follow_up_job_id"]
        assert follow_up_id

        follow_up = load_job_plan(follow_up_id, jobs_root)
        assert follow_up is not None
        assert follow_up.state == RunState.PENDING
        assert follow_up.tasks == []
        assert follow_up.repo_path == "/repo/x"
        assert follow_up.project_id == "proj-9"
        assert job.tasks[0].title in follow_up.user_prompt          # the vetoed task's goal
        assert "known-bad approach" in follow_up.user_prompt        # the reason, verbatim
        assert job.tasks[1].title in follow_up.user_prompt          # unreachable B's goal
        assert job.tasks[2].title in follow_up.user_prompt          # unreachable C's goal
        assert follow_up.metadata["replan_of"] == {
            "job_id": job.job_id, "task_id": a_id, "request_id": result["request_id"],
        }

        assert original_path.read_bytes() == before

        assert len(_veto_answered_events(job.job_id)) == 1

        # Exactly one new job directory exists under jobs_root: the follow-up.
        job_dirs = sorted(p.name for p in (jobs_root / "jobs").iterdir())
        assert job_dirs == sorted([job.job_id, follow_up_id])


# ---------------------------------------------------------------------------
# A repeated answer: already_answered, no second job or event
# ---------------------------------------------------------------------------


class TestRepeatedAnswer:
    def test_already_answered_writes_nothing_new(self, control, jobs_root):
        tasks = [flight_task("A"), flight_task("B", "A")]
        job = _job(tasks)
        a_id = dag_ids(tasks, "A")[0]
        result = tv.veto_task_command(job, task_id=a_id, reason="x", actor="alice",
                                      control_root_path=control)
        decision_id = f"veto:{result['request_id']}"

        first = vp.answer_replan_proposal(
            job, decision_id, tv.REPLAN_FOLLOW_UP, actor="alice",
            control_root_path=control, root=jobs_root)
        assert first["outcome"] == "answered"

        second = vp.answer_replan_proposal(
            job, decision_id, tv.ACCEPT_REDUCED_SCOPE, actor="bob",
            control_root_path=control, root=jobs_root)
        assert second == {
            "outcome": "refused", "code": "already_answered", "decision_id": decision_id,
            "option": first["option"], "follow_up_job_id": first["follow_up_job_id"],
        }

        assert len(_veto_answered_events(job.job_id)) == 1
        # The original job was never saved under `jobs_root` in this test — only the
        # follow-up is, and exactly once (no second job from the second answer).
        job_dirs = sorted(p.name for p in (jobs_root / "jobs").iterdir())
        assert job_dirs == [first["follow_up_job_id"]]


# ---------------------------------------------------------------------------
# The repair of a follow-up job whose save failed
# ---------------------------------------------------------------------------


class TestFollowUpRepair:
    def test_a_repeated_answer_repairs_a_follow_up_job_whose_save_failed(
            self, control, jobs_root, monkeypatch):
        tasks = [flight_task("A"), flight_task("B", "A")]
        job = _job(tasks)
        a_id = dag_ids(tasks, "A")[0]
        result = tv.veto_task_command(job, task_id=a_id, reason="x", actor="alice",
                                      control_root_path=control)
        decision_id = f"veto:{result['request_id']}"

        def _boom(*_a, **_kw):
            raise OSError("simulated save failure")

        monkeypatch.setattr(pj, "save_job_plan", _boom)
        with pytest.raises(OSError):
            vp.answer_replan_proposal(
                job, decision_id, tv.REPLAN_FOLLOW_UP, actor="alice",
                control_root_path=control, root=jobs_root)
        monkeypatch.undo()

        # The answer WAS published — record_veto_answer runs before the save — so the
        # follow-up id is already known, but its job.json was never written.
        stored = tv.veto_answers(job.job_id, control_root_path=control)
        follow_up_id = stored[result["request_id"]].follow_up_job_id
        assert follow_up_id
        assert load_job_plan(follow_up_id, jobs_root) is None

        second = vp.answer_replan_proposal(
            job, decision_id, tv.REPLAN_FOLLOW_UP, actor="bob",
            control_root_path=control, root=jobs_root)
        assert second["outcome"] == "refused"
        assert second["code"] == "already_answered"
        assert second["follow_up_job_id"] == follow_up_id
        assert load_job_plan(follow_up_id, jobs_root) is not None


# ---------------------------------------------------------------------------
# Two concurrent answers converge
# ---------------------------------------------------------------------------


class TestConcurrentAnswers:
    def test_two_concurrent_answers_converge_on_the_winner(
            self, control, jobs_root, monkeypatch):
        tasks = [flight_task("A"), flight_task("B", "A")]
        job = _job(tasks)
        a_id = dag_ids(tasks, "A")[0]
        result = tv.veto_task_command(job, task_id=a_id, reason="x", actor="alice",
                                      control_root_path=control)
        decision_id = f"veto:{result['request_id']}"

        winner: dict[str, object] = {}
        real_write = tv._fs.write_file_atomically

        def _slip_in_first(dir_fd, name, data, **kw):
            if "answer" not in winner:
                winner["answer"] = None                    # re-entry guard
                monkeypatch.undo()
                winner["answer"] = vp.answer_replan_proposal(
                    job, decision_id, tv.ACCEPT_REDUCED_SCOPE, actor="carol",
                    control_root_path=control, root=jobs_root)
            return real_write(dir_fd, name, data, **kw)

        monkeypatch.setattr(
            "packages.orchestration.task_veto._fs.write_file_atomically", _slip_in_first)

        got = vp.answer_replan_proposal(
            job, decision_id, tv.REPLAN_FOLLOW_UP, actor="dave",
            control_root_path=control, root=jobs_root)

        assert got["option"] == winner["answer"]["option"] == tv.ACCEPT_REDUCED_SCOPE
        assert got["follow_up_job_id"] == winner["answer"]["follow_up_job_id"] == ""
        # The winner accepted the reduced scope, so no follow-up job exists at all —
        # including no orphan under the LOSER's own minted (and discarded) id.
        assert not jobs_root.exists()
