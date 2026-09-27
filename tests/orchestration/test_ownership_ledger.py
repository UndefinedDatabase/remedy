"""F035 T001 (first half, DECISION F035 D1) — the ownership ledger's pure pass over the
records that already name who acted: vetoes, veto answers, injections, subtree reruns, plan
and task edits, steering messages and notes, and the pause/resume/stop events of the run log.

Every record is written by the REAL writer that owns its shape — `task_veto`, `task_injection`,
`subtree_rerun`, `plan_editing`, `task_edit_runtime`, `steering` and `RunLogWriter`/
`pause_control` — under `REMEDY_DATA_DIR` set to a tmp path, exactly as their own test modules
do; only a stored record's timestamp is occasionally patched afterward, directly on the file the
real writer produced, to make an ordering assertion deterministic against the real clock.
"""
from __future__ import annotations

import difflib
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import pytest

from packages.core.models import RunState
from packages.orchestration import escalation as esc
from packages.orchestration import ownership as own
from packages.orchestration import pause_control as pc
from packages.orchestration import pingpong_job as pj
from packages.orchestration import plan_editing as pe
from packages.orchestration import steering as st
from packages.orchestration import subtree_rerun as sr
from packages.orchestration import task_edit_runtime as ter
from packages.orchestration import task_injection as ti
from packages.orchestration import task_veto as tv
from packages.orchestration.data_paths import run_log_dir
from packages.orchestration.diff_parser import parse_unified_diff_to_view
from packages.orchestration.hunk_decision_record import record_hunk_decision
from packages.orchestration.hunk_ledger import HUNK_LANDING_UNATTEMPTED
from packages.orchestration.job_plan import (
    APPROVED_PLAN_HASH_KEY,
    AUTO_APPROVAL_MODE,
    announce_plan_approval,
    map_task_plan_to_tasks,
    plan_content_hash,
)
from packages.orchestration.pingpong_job import load_job_plan, save_job_plan
from packages.orchestration.run_log import RunLogWriter
from packages.orchestration.schemas.models import TaskPlan
from packages.orchestration.task_deliverables import record_llm_task_deliverables

JOB = "f035job0000000a"


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path: Path, monkeypatch):
    """REMEDY_DATA_DIR to tmp so every reader/writer here — control files, steering
    records, run-log events and job records alike — resolves to one disposable root."""
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


# ---------------------------------------------------------------------------
# Shared builders
# ---------------------------------------------------------------------------


def _job(*, job_id: str = JOB, tasks: list | None = None, metadata: dict | None = None,
         reruns: list | None = None, task_plan: dict | None = None,
         state: RunState = RunState.RUNNING) -> pj.JobPlan:
    return pj.JobPlan(job_id=job_id, tasks=tasks or [], state=state,
                      metadata=metadata or {}, reruns=reruns or [], task_plan=task_plan)


def _task_entry(task_id: str, *, depends_on: tuple[str, ...] = (),
                status: str = pj.TASK_PENDING) -> pj.TaskEntry:
    """A task carrying flight metadata, shaped like the real mapper's (mirrors
    `test_dag_schedule.flight_task`), but with an explicit id so a test can name it."""
    return pj.TaskEntry(
        task_id=task_id, status=status,
        inputs={"plan": {"planned_id": task_id, "title": task_id, "depends_on": list(depends_on)}})


def _two_task_chain() -> list[pj.TaskEntry]:
    """T1 -> T2: vetoing T1 makes T2 unreachable."""
    return [_task_entry("T1"), _task_entry("T2", depends_on=("T1",))]


def _control_root() -> Path:
    return Path(os.environ["REMEDY_DATA_DIR"]) / "control"


def _veto_path(job_id: str, task_id: str) -> Path:
    digest = hashlib.sha256(task_id.encode("utf-8")).hexdigest()[:32]
    return _control_root() / "jobs" / job_id / tv.VETOED_TASKS_DIRNAME / f"{digest}.json"


def _veto_answer_path(job_id: str, request_id: str) -> Path:
    digest = hashlib.sha256(request_id.encode("utf-8")).hexdigest()[:32]
    return _control_root() / "jobs" / job_id / tv.VETO_ANSWERS_DIRNAME / f"{digest}.json"


def _patch_json(path: Path, **updates) -> None:
    body = json.loads(path.read_text(encoding="utf-8"))
    body.update(updates)
    path.write_text(json.dumps(body), encoding="utf-8")


def _confirmed_injection_record(*, draft_id: str, task_id: str, actor: str = "alice",
                                confirmed_at: str = "2026-01-01T00:00:00+00:00",
                                text: str = "add the thing", drafted_by: str = "alice",
                                basis: str = "frontier_default",
                                confirmed_unseen: bool | None = None) -> dict:
    """Shaped exactly as `confirm_task_injection` writes one (mirrors
    `test_task_injection._confirmed_record`), built directly so this file can plant a
    verbatim newline-and-trailing-space text without fighting `validate_injection_text`,
    which `confirmed_injections` never re-applies to a stored record."""
    record = {
        "draft_id": draft_id,
        "task": {
            "id": task_id, "title": "Add the thing", "goal": "do the thing",
            "acceptance": ["it happens"], "depends_on": [],
            "est_tokens_band": "S", "files_hint": [],
        },
        "placement": {"depends_on": [], "basis": basis, "position": 1,
                      "rationale": "placed at the end"},
        "task_rationale": "because the operator asked",
        "text": text,
        "drafted_by": drafted_by,
        "actor": actor,
        "confirmed_at": confirmed_at,
    }
    if confirmed_unseen is not None:
        record["confirmed_unseen"] = confirmed_unseen
    return record


def _plan_task(tid: str, deps: list[str] | None = None) -> dict:
    return {
        "id": tid, "title": f"Build {tid}", "goal": f"goal of {tid}",
        "acceptance": [f"{tid} works"], "depends_on": deps or [],
        "est_tokens_band": "S", "files_hint": [],
    }


def _save_plan_job(tasks: list[dict], *, approval: str = "pending",
                   state: RunState = RunState.PLANNED, job_id: str = JOB) -> str:
    plan = TaskPlan.model_validate({"schema_v": "task_plan_v1", "tasks": tasks})
    body = plan.model_dump()
    body["_approval"] = approval
    body["_normalization"] = []
    if approval == "approved":
        body[APPROVED_PLAN_HASH_KEY] = plan_content_hash(body)
    mapped = map_task_plan_to_tasks(plan)
    record_llm_task_deliverables(mapped)
    job = pj.JobPlan(job_id=job_id, job_title="t", task_plan=body, tasks=mapped, state=state)
    save_job_plan(job, None)
    return job.job_id


def _task_id_of(job_id: str, planned_id: str) -> str:
    job = load_job_plan(job_id, None)
    for t in job.tasks:
        if (t.inputs.get("plan") or {}).get("planned_id") == planned_id:
            return t.task_id
    raise AssertionError(f"no task for planned id {planned_id!r}")


#: A twenty-line original with two well-separated edits, RESTATED from
#: ``test_hunk_decision_record.py``'s own recipe rather than imported — a test file reaching
#: into another test file's helpers couples two suites that have no reason to move together.
_HUNK_ORIGINAL = "\n".join(f"line {number:02d}" for number in range(1, 21)) + "\n"


def _hunk_diff(*replacements: tuple[str, str], path: str = "f.txt") -> str:
    text = _HUNK_ORIGINAL
    for old, new in replacements:
        text = text.replace(old + "\n", new + "\n")
    return "".join(difflib.unified_diff(
        _HUNK_ORIGINAL.splitlines(True), text.splitlines(True),
        fromfile=f"a/{path}", tofile=f"b/{path}"))


_HUNK_DIFF = _hunk_diff(("line 03", "line 03 CHANGED"), ("line 15", "line 15 CHANGED"))
_HUNK_IDS = [h["id"] for h in parse_unified_diff_to_view(_HUNK_DIFF)["files"][0]["hunks"]]


def _rewrite_run_log_timestamps(job_id: str, *, event: str, timestamps: list[str]) -> None:
    """Overwrite the `timestamp` of every `event`-named line, IN FILE ORDER, with
    `timestamps` — a `_patch_json`-style direct edit on the run log's own JSONL file, so an
    ordering/count assertion does not depend on how fast consecutive real-clock writes land."""
    root = Path(os.environ["REMEDY_DATA_DIR"])
    files = sorted(run_log_dir(job_id, root).glob("*.jsonl"))
    path = files[-1]
    remaining = list(timestamps)
    out_lines = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        if record.get("event") == event and remaining:
            record["timestamp"] = remaining.pop(0)
        out_lines.append(json.dumps(record))
    path.write_text("\n".join(out_lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# The empty job
# ---------------------------------------------------------------------------


class TestEmptyJob:
    def test_no_action_answers_empty_entries_and_the_schema(self):
        job = _job()
        ledger = own.build_ownership_ledger(job)
        assert ledger == {"schema": own.OWNERSHIP_SCHEMA, "job_id": JOB, "entries": []}


# ---------------------------------------------------------------------------
# (a) VETO
# ---------------------------------------------------------------------------


class TestVeto:
    def test_folded_and_control_only_entries_in_one_ledger(self):
        """T1 vetoed and folded (makes T2 unreachable); T3, independent, vetoed but never
        folded — the control-only path, whose unreachable set `_task_veto_report_map`'s own
        computation (minus the OTHER vetoed ids) must answer empty for an isolated task."""
        job = _job(tasks=[*_two_task_chain(), _task_entry("T3")])
        veto1, created1 = tv.record_task_veto(job.job_id, "T1", "risky change", "alice",
                                               pj.TASK_PENDING)
        assert created1
        blocked = pj._fold_task_vetoes(job, None, None)
        assert blocked is False
        veto3, created3 = tv.record_task_veto(job.job_id, "T3", "also risky", "bob",
                                               pj.TASK_PENDING)
        assert created3
        # T3 is deliberately left unfolded: it stays a control-only entry.

        ledger = own.build_ownership_ledger(job)
        entries = {e["task_id"]: e for e in ledger["entries"] if e["action"] == "task_vetoed"}
        assert set(entries) == {"T1", "T3"}

        folded = entries["T1"]
        assert folded["record_ref"] == f"veto:{veto1.request_id}"
        assert folded["ts"] == veto1.requested_at
        assert folded["text"] == "risky change"
        assert folded["actor"] == own.ownership_actor("alice")
        assert folded["consequence"] == {"kind": "unreachable", "task_ids": ["T2"], "ref": ""}
        assert folded["detail"] == {"status_at_veto": pj.TASK_PENDING}

        control_only = entries["T3"]
        assert control_only["record_ref"] == f"veto:{veto3.request_id}"
        assert control_only["text"] == "also risky"
        assert control_only["actor"] == own.ownership_actor("bob")
        assert control_only["consequence"] == {"kind": "unreachable", "task_ids": [], "ref": ""}

    def test_inert_veto_reads_kind_inert_with_the_status_as_ref(self):
        job = _job(tasks=_two_task_chain())
        tv.record_task_veto(job.job_id, "GHOST", "no such task", "alice", pj.TASK_PENDING)
        blocked = pj._fold_task_vetoes(job, None, None)
        assert blocked is False

        ledger = own.build_ownership_ledger(job)
        [entry] = [e for e in ledger["entries"] if e["action"] == "task_vetoed"]
        assert entry["task_id"] == "GHOST"
        assert entry["consequence"] == {"kind": "inert", "task_ids": [], "ref": "unknown"}

    def test_an_unreadable_control_file_raises_ownershiperror(self):
        job = _job(tasks=_two_task_chain())
        tv.record_task_veto(job.job_id, "T1", "risky", "alice", pj.TASK_PENDING)
        path = _veto_path(job.job_id, "T1")
        path.write_text("not json", encoding="utf-8")

        with pytest.raises(tv.TaskVetoError):
            tv.vetoed_tasks(job.job_id)
        with pytest.raises(own.OwnershipError):
            own.build_ownership_ledger(job)


# ---------------------------------------------------------------------------
# (b) VETO ANSWER
# ---------------------------------------------------------------------------


class TestVetoAnswer:
    def test_entry_shape(self):
        job = _job()
        answer, created = tv.record_veto_answer(
            job.job_id, "req-answer-1", "T1", tv.REPLAN_FOLLOW_UP, "alice", "f035job0000000f")
        assert created

        ledger = own.build_ownership_ledger(job)
        [entry] = [e for e in ledger["entries"] if e["action"] == "veto_answered"]
        assert entry["record_ref"] == f"veto_answer:{answer.request_id}"
        assert entry["ts"] == answer.answered_at
        assert entry["task_id"] == "T1"
        assert entry["text"] == tv.REPLAN_FOLLOW_UP
        assert entry["actor"] == own.ownership_actor("alice")
        assert entry["consequence"] == {
            "kind": tv.REPLAN_FOLLOW_UP, "task_ids": [], "ref": "f035job0000000f"}
        assert entry["detail"] == {}


# ---------------------------------------------------------------------------
# (c) INJECTION
# ---------------------------------------------------------------------------


class TestInjection:
    def test_applied_with_yes_is_auto_approved_and_verbatim_text_survives(self):
        job_id = _save_plan_job([_plan_task("T1")], approval="approved",
                                state=RunState.RUNNING)
        job = load_job_plan(job_id, None)
        record = _confirmed_injection_record(
            draft_id="draft0000000001", task_id="INJ1",
            text="add the thing\nplease  ", confirmed_unseen=True)
        ti._publish_confirmed_injection(job.job_id, record["draft_id"], record,
                                        control_root_path=None)

        blocked = pj._fold_task_injections(job, None)
        assert blocked is False

        ledger = own.build_ownership_ledger(job)
        [entry] = [e for e in ledger["entries"] if e["action"] == "task_injected"]
        assert entry["record_ref"] == "injection:draft0000000001"
        assert entry["text"] == "add the thing\nplease  "
        assert entry["actor"]["auto_approved"] is True
        assert entry["actor"]["recorded_as"] == "alice"
        assert entry["consequence"]["kind"] == "task_added"
        assert entry["task_id"] == entry["consequence"]["task_ids"][0]
        assert entry["detail"] == {
            "drafted_by": "alice", "planned_id": "INJ1", "placement_basis": "frontier_default"}

        # The injection's own `_edits` entry (carrying `injection`) must not surface as a
        # `plan_edited`/`task_edited` entry (it belongs to class (c) alone).
        assert not any(e["record_ref"].startswith("plan_edit:") for e in ledger["entries"])

    def test_applied_without_yes_is_not_auto_approved(self):
        job_id = _save_plan_job([_plan_task("T1")], approval="approved",
                                state=RunState.RUNNING)
        job = load_job_plan(job_id, None)
        record = _confirmed_injection_record(draft_id="draft0000000002", task_id="INJ2")
        ti._publish_confirmed_injection(job.job_id, record["draft_id"], record,
                                        control_root_path=None)
        pj._fold_task_injections(job, None)

        ledger = own.build_ownership_ledger(job)
        [entry] = [e for e in ledger["entries"] if e["action"] == "task_injected"]
        assert entry["actor"]["auto_approved"] is False

    def test_inert_injection_reads_kind_inert(self):
        # INJ_DUP names a task id already in the plan — `apply_injection_to_job` refuses it,
        # which the fold records INERT rather than raising.
        job_id = _save_plan_job([_plan_task("T1")], approval="approved",
                                state=RunState.RUNNING)
        job = load_job_plan(job_id, None)
        record = _confirmed_injection_record(draft_id="draft0000000003", task_id="T1")
        ti._publish_confirmed_injection(job.job_id, record["draft_id"], record,
                                        control_root_path=None)
        pj._fold_task_injections(job, None)

        ledger = own.build_ownership_ledger(job)
        [entry] = [e for e in ledger["entries"] if e["action"] == "task_injected"]
        assert entry["task_id"] == ""
        assert entry["consequence"]["kind"] == "inert"

    def test_not_yet_folded_injection_reads_kind_not_folded(self):
        job = _job()
        record = _confirmed_injection_record(draft_id="draft0000000004", task_id="INJ4")
        ti._publish_confirmed_injection(job.job_id, record["draft_id"], record,
                                        control_root_path=None)
        # Deliberately never folded.

        ledger = own.build_ownership_ledger(job)
        [entry] = [e for e in ledger["entries"] if e["action"] == "task_injected"]
        assert entry["task_id"] == ""
        assert entry["consequence"] == {"kind": "not_folded", "task_ids": [], "ref": ""}


# ---------------------------------------------------------------------------
# (d) RERUN
# ---------------------------------------------------------------------------


class TestRerun:
    def test_entry_shape(self):
        job = _job(tasks=[_task_entry("T1")])
        reset = {
            "root_task_id": "T1", "subtree": ["T1"],
            "base_commit": "a" * 40, "reset_commit": "b" * 40,
            "paths": ["src/x.py"], "exact": True, "proof": {}, "pre_task_tree_equal": True,
        }
        from datetime import datetime, timezone
        now = datetime(2026, 1, 1, tzinfo=timezone.utc)
        record = sr.fold_subtree_rerun(
            job, reset, rerun_id="rr-0001", model_override="claude-opus-x", actor="alice",
            now=now, moved_streams={})

        ledger = own.build_ownership_ledger(job)
        [entry] = [e for e in ledger["entries"] if e["action"] == "subtree_rerun"]
        assert entry["record_ref"] == "rerun:rr-0001"
        assert entry["ts"] == record["at"]
        assert entry["task_id"] == "T1"
        assert entry["text"] == ""
        assert entry["actor"] == own.ownership_actor("alice")
        assert entry["consequence"] == {
            "kind": "subtree_reset", "task_ids": ["T1"], "ref": ""}
        assert entry["detail"] == {"model_override": "claude-opus-x"}


# ---------------------------------------------------------------------------
# (e) EDITS
# ---------------------------------------------------------------------------


class TestEdits:
    def test_plan_edit_is_plan_edited(self):
        job_id = _save_plan_job([_plan_task("T1")], approval="pending",
                                state=RunState.PLANNED)
        pe.edit_plan(job_id, "plan_edit_task", {"task_id": "T1", "fields": {"title": "New"}},
                     expected_version=1, actor="alice", root=None)

        job = load_job_plan(job_id, None)
        ledger = own.build_ownership_ledger(job)
        [entry] = [e for e in ledger["entries"] if e["action"] == "plan_edited"]
        assert entry["record_ref"] == "plan_edit:v2"
        assert entry["task_id"] == "T1"
        assert entry["text"] == ""
        assert entry["actor"] == own.ownership_actor("alice")
        assert entry["consequence"] == {
            "kind": "plan_version", "task_ids": ["T1"], "ref": "v2"}
        assert entry["detail"]["command"] == "plan_edit_task"

    def test_runtime_edit_is_task_edited(self):
        job_id = _save_plan_job([_plan_task("T1")], approval="approved",
                                state=RunState.PLANNED)
        task_id = _task_id_of(job_id, "T1")
        ter.edit_task_at_runtime(
            job_id, task_id, {"title": "Renamed", "goal": "new goal"},
            expected_spec_version=1, actor="alice", root=None)

        job = load_job_plan(job_id, None)
        ledger = own.build_ownership_ledger(job)
        [entry] = [e for e in ledger["entries"] if e["action"] == "task_edited"]
        assert entry["record_ref"] == "plan_edit:v2"
        assert entry["task_id"] == task_id
        assert entry["consequence"] == {
            "kind": "plan_version", "task_ids": [task_id], "ref": "v2"}
        assert entry["detail"]["command"] == "plan_edit_task"


# ---------------------------------------------------------------------------
# (f) STEERING
# ---------------------------------------------------------------------------


class TestSteering:
    def test_consumed_note_names_its_task_and_round(self):
        job = _job()
        st.record_steering_message(job.job_id, "resize the widget", job_state="running",
                                   channel="cli", task_id="T1")
        st.consume_pending_steering(job.job_id, task_id="T1", round_number=3)

        ledger = own.build_ownership_ledger(job)
        [entry] = [e for e in ledger["entries"] if e["action"] == "note_sent"]
        assert entry["task_id"] == "T1"
        assert entry["text"] == "resize the widget"
        assert entry["actor"] == own.ownership_actor("cli")
        assert entry["consequence"] == {"kind": "consumed", "task_ids": ["T1"], "ref": "round 3"}

    def test_unconsumed_job_wide_message_reads_steering_sent_not_consumed(self):
        job = _job()
        st.record_steering_message(job.job_id, "job-wide correction", job_state="running",
                                   channel="cockpit")

        ledger = own.build_ownership_ledger(job)
        [entry] = [e for e in ledger["entries"] if e["action"] == "steering_sent"]
        assert entry["task_id"] == ""
        assert entry["actor"]["door"] == "browser"
        assert entry["consequence"] == {"kind": "not_consumed", "task_ids": [], "ref": ""}

    def test_a_tampered_steering_record_raises_ownershiperror(self):
        job = _job()
        record = st.record_steering_message(job.job_id, "note", job_state="running",
                                            channel="cli", task_id="T1")
        from packages.orchestration.data_paths import job_evidence_dir

        path = job_evidence_dir(job.job_id) / "steering" / f"{record['message_id']}.json"
        _patch_json(path, text="tampered")

        with pytest.raises(st.SteeringError):
            st.list_steering_messages(job.job_id)
        with pytest.raises(own.OwnershipError):
            own.build_ownership_ledger(job)


# ---------------------------------------------------------------------------
# (g) RUN LOG — job_paused, task_paused, job_resumed, task_resumed, job_stopped
# ---------------------------------------------------------------------------


class TestRunLog:
    def test_job_paused_entry(self):
        job = _job()
        writer = RunLogWriter(job.job_id)
        writer.log("job_paused", outcome="paused", scope="job", request_id="req-p1",
                  reason="operator asked", source="cli", withheld_task_ids=["T1", "T2"],
                  pending_task_count=2)

        ledger = own.build_ownership_ledger(job)
        [entry] = [e for e in ledger["entries"] if e["action"] == "job_paused"]
        assert entry["record_ref"] == "job_paused:req-p1"
        assert entry["task_id"] == ""
        assert entry["text"] == "operator asked"
        assert entry["actor"] == own.ownership_actor("cli")
        assert entry["consequence"] == {
            "kind": "withheld", "task_ids": ["T1", "T2"], "ref": ""}

    def test_task_paused_entry(self):
        job = _job(tasks=[_task_entry("T1")])
        result = pc.pause_job_command(job, task_id="T1", reason="fix it", source="cli")
        assert result["outcome"] == "paused"

        ledger = own.build_ownership_ledger(job)
        [entry] = [e for e in ledger["entries"] if e["action"] == "task_paused"]
        assert entry["task_id"] == "T1"
        assert entry["text"] == "fix it"
        assert entry["actor"] == own.ownership_actor("cli")
        assert entry["consequence"] == {"kind": "withheld", "task_ids": ["T1"], "ref": ""}

    def test_job_resumed_entry_actor_has_no_door_and_names_the_pause_source_in_detail(self):
        job = _job()
        writer = RunLogWriter(job.job_id)
        writer.log("job_resumed", outcome="resumed", scope="job", request_id="req-p1",
                  reason="operator asked", source="cli", requested_at="2026-01-01T00:00:00+00:00",
                  paused_at="2026-01-01T00:00:01+00:00", paused_task_ids=["T1"],
                  withheld_task_ids=["T1", "T2"], resumed_at="2026-01-01T00:05:00+00:00")

        ledger = own.build_ownership_ledger(job)
        [entry] = [e for e in ledger["entries"] if e["action"] == "job_resumed"]
        assert entry["task_id"] == ""
        assert entry["text"] == ""
        assert entry["actor"]["door"] == ""
        assert entry["actor"]["recorded_as"] == ""
        assert entry["consequence"] == {
            "kind": "released", "task_ids": ["T1", "T2"], "ref": ""}
        assert entry["detail"] == {"paused_by": "cli"}

    def test_task_resumed_entry(self):
        job = _job(tasks=[_task_entry("T1")])
        pc.pause_job_command(job, task_id="T1", reason="fix it", source="cli")
        result = pc.unpause_job_command(job, task_id="T1", source="cli")
        assert result["outcome"] == "released"

        ledger = own.build_ownership_ledger(job)
        [entry] = [e for e in ledger["entries"] if e["action"] == "task_resumed"]
        assert entry["task_id"] == "T1"
        assert entry["actor"]["door"] == ""
        assert entry["actor"]["recorded_as"] == ""
        assert entry["consequence"] == {"kind": "released", "task_ids": ["T1"], "ref": ""}
        assert entry["detail"] == {"paused_by": "cli"}

    def test_job_stopped_entry(self):
        job = _job()
        writer = RunLogWriter(job.job_id)
        writer.log("job_stopped", task_id=None, outcome="stopped", request_id="req-s1",
                  reason="operator stop", source="cli",
                  requested_at="2026-01-01T00:00:00+00:00",
                  consumed_at="2026-01-01T00:00:05+00:00", completed_task_count=0,
                  pending_task_count=1, postmortem_ref="evidence/postmortem.json")

        ledger = own.build_ownership_ledger(job)
        [entry] = [e for e in ledger["entries"] if e["action"] == "job_stopped"]
        assert entry["record_ref"] == "job_stopped:req-s1"
        assert entry["ts"] == "2026-01-01T00:00:00+00:00"
        assert entry["task_id"] == ""
        assert entry["text"] == "operator stop"
        assert entry["actor"] == own.ownership_actor("cli")
        assert entry["consequence"] == {
            "kind": "stopped", "task_ids": [], "ref": "evidence/postmortem.json"}

    def test_a_pause_event_written_twice_for_one_request_id_yields_one_entry(self):
        job = _job()
        writer = RunLogWriter(job.job_id)
        for _ in range(2):
            writer.log("job_paused", outcome="paused", scope="job", request_id="req-dup",
                      reason="operator asked", source="cli", withheld_task_ids=[],
                      pending_task_count=0)

        ledger = own.build_ownership_ledger(job)
        entries = [e for e in ledger["entries"] if e["action"] == "job_paused"]
        assert len(entries) == 1


# ---------------------------------------------------------------------------
# (h) HUNK DECISIONS — round 2, S1
# ---------------------------------------------------------------------------


class TestHunkDecisions:
    #: An operator's reason with surrounding whitespace, so "verbatim" is a testable claim.
    _REASON = "  the second edit is out of scope  "

    def test_approved_entry_and_no_entry_for_the_pending_row(self):
        job = _job()
        now = datetime(2026, 1, 1, 12, 0, 0)
        record_hunk_decision(job, task_id="T1", attempt=2, attempt_diff_text=_HUNK_DIFF,
                             approved=[_HUNK_IDS[0]], rejected=(), now=now)

        ledger = own.build_ownership_ledger(job)
        entries = [e for e in ledger["entries"]
                  if e["action"] in ("hunk_approved", "hunk_rejected")]
        [entry] = entries
        assert entry["action"] == "hunk_approved"
        assert entry["record_ref"] == f"hunk:T1:2:{_HUNK_IDS[0]}"
        assert entry["ts"] == now.isoformat()
        assert entry["task_id"] == "T1"
        assert entry["text"] == ""
        assert entry["actor"] == own.ownership_actor("")
        assert entry["consequence"] == {
            "kind": "landing", "task_ids": ["T1"], "ref": HUNK_LANDING_UNATTEMPTED}
        assert entry["detail"] == {"attempt": "2", "hunk_id": _HUNK_IDS[0]}

    def test_rejected_entry_reason_verbatim_its_landing_and_no_door(self):
        job = _job()
        now = datetime(2026, 1, 1, 12, 0, 0)
        record_hunk_decision(job, task_id="T2", attempt=1, attempt_diff_text=_HUNK_DIFF,
                             approved=(), rejected=[(_HUNK_IDS[0], self._REASON)], now=now)

        ledger = own.build_ownership_ledger(job)
        [entry] = [e for e in ledger["entries"] if e["action"] == "hunk_rejected"]
        assert entry["record_ref"] == f"hunk:T2:1:{_HUNK_IDS[0]}"
        assert entry["text"] == self._REASON
        assert entry["actor"]["door"] == ""
        assert entry["consequence"] == {
            "kind": "landing", "task_ids": ["T2"], "ref": HUNK_LANDING_UNATTEMPTED}


# ---------------------------------------------------------------------------
# (i) DECISION ANSWERS — round 2, S2
# ---------------------------------------------------------------------------


class TestDecisionAnswers:
    def test_human_and_default_answers_and_no_entry_for_an_open_one(self):
        job = _job()
        now = datetime(2026, 1, 1, tzinfo=timezone.utc)
        human_rec = esc.enqueue_task_decision(job, task_id="T1", question="which way?",
                                              options=["a", "b"], safe_default="a", now=now)
        esc.answer_task_decision(job, human_rec["decision_id"], answer="b", now=now)
        default_rec = esc.enqueue_task_decision(job, task_id="T2", question="proceed?",
                                                safe_default="yes", now=now)
        esc.auto_apply_safe_default(job, default_rec, now=now)
        esc.enqueue_task_decision(job, task_id="T3", question="still open?", now=now)

        ledger = own.build_ownership_ledger(job)
        entries = {e["task_id"]: e for e in ledger["entries"]
                  if e["action"] == "decision_answered"}
        assert set(entries) == {"T1", "T2"}

        human = entries["T1"]
        assert human["record_ref"] == f"decision:{human_rec['decision_id']}"
        assert human["text"] == "b"
        assert human["actor"]["kind"] == "operator"
        assert human["actor"]["recorded_as"] == "human"
        assert human["consequence"] == {
            "kind": "answer_to_task", "task_ids": ["T1"], "ref": ""}
        assert human["detail"] == {"question": "which way?"}

        default = entries["T2"]
        assert default["text"] == "yes"
        assert default["actor"]["kind"] == "default_policy"
        assert default["actor"]["recorded_as"] == "default"


# ---------------------------------------------------------------------------
# (j) CLARIFICATIONS — round 2, S3
# ---------------------------------------------------------------------------


class TestClarifications:
    def test_human_default_and_planner_and_none_for_unresolved(self):
        job = _job(task_plan={"clarifications_resolved": [
            {"id": "q1", "question": "Which auth?", "default_answer": "oauth",
             "answer": "saml", "answered_by": "human"},
            {"id": "q2", "question": "Which db?", "default_answer": "postgres",
             "answer": "postgres", "answered_by": "default"},
            {"id": "q3", "question": "Which cache?", "default_answer": "redis",
             "answer": "memcached", "answered_by": ""},
            {"id": "q4", "question": "Which queue?", "default_answer": "", "answer": "",
             "answered_by": ""},
        ]})

        ledger = own.build_ownership_ledger(job)
        entries = {e["record_ref"]: e for e in ledger["entries"]
                  if e["action"] == "clarification_answered"}
        assert set(entries) == {"clarification:q1", "clarification:q2", "clarification:q3"}

        human = entries["clarification:q1"]
        assert human["ts"] == ""
        assert human["actor"]["kind"] == "operator"
        assert human["text"] == "saml"
        assert human["consequence"] == {"kind": "plan_input", "task_ids": [], "ref": ""}
        assert human["detail"] == {"question": "Which auth?", "default_answer": "oauth"}

        default = entries["clarification:q2"]
        assert default["actor"]["kind"] == "default_policy"
        assert default["text"] == "postgres"

        planner = entries["clarification:q3"]
        assert planner["actor"]["kind"] == "remedy"
        assert planner["text"] == "memcached"


# ---------------------------------------------------------------------------
# (k) PLAN APPROVAL — round 2, S4
# ---------------------------------------------------------------------------


class TestPlanApproval:
    def test_human_mode_event(self):
        job = _job(tasks=_two_task_chain())
        announce_plan_approval(job, mode="human")

        ledger = own.build_ownership_ledger(job)
        [entry] = [e for e in ledger["entries"] if e["action"] == "plan_approved"]
        assert entry["record_ref"] == f"plan_approved:{entry['ts']}"
        assert entry["task_id"] == ""
        assert entry["text"] == ""
        assert entry["actor"] == own.ownership_actor("")
        assert entry["consequence"] == {
            "kind": "plan_approved", "task_ids": ["T1", "T2"], "ref": ""}
        assert entry["detail"] == {"approval_mode": "human"}

    def test_auto_yes_mode_event_is_auto_approved_with_the_audits_reason_as_text(self):
        job = _job(tasks=_two_task_chain(),
                  task_plan={"_approval": "approved",
                            "_approval_audit": {"mode": AUTO_APPROVAL_MODE,
                                                "reason": "auto-approved via --yes"}})
        announce_plan_approval(job, mode=AUTO_APPROVAL_MODE)

        ledger = own.build_ownership_ledger(job)
        [entry] = [e for e in ledger["entries"] if e["action"] == "plan_approved"]
        assert entry["actor"]["auto_approved"] is True
        assert entry["actor"]["recorded_as"] == AUTO_APPROVAL_MODE
        assert entry["text"] == "auto-approved via --yes"

    def test_two_events_with_no_request_id_yield_two_entries(self):
        job = _job(tasks=_two_task_chain())
        announce_plan_approval(job, mode="human")
        announce_plan_approval(job, mode="human")
        _rewrite_run_log_timestamps(
            job.job_id, event="plan_approved",
            timestamps=["2026-01-01T00:00:00+00:00", "2026-01-01T00:00:01+00:00"])

        ledger = own.build_ownership_ledger(job)
        entries = [e for e in ledger["entries"] if e["action"] == "plan_approved"]
        assert len(entries) == 2
        assert {e["record_ref"] for e in entries} == {
            "plan_approved:2026-01-01T00:00:00+00:00",
            "plan_approved:2026-01-01T00:00:01+00:00"}

    def test_a_rejected_plans_entry(self):
        job = _job(task_plan={"_approval": "rejected"})
        ledger = own.build_ownership_ledger(job)
        [entry] = [e for e in ledger["entries"] if e["action"] == "plan_rejected"]
        assert entry["record_ref"] == "plan_rejected"
        assert entry["ts"] == ""
        assert entry["actor"] == own.ownership_actor("")
        assert entry["consequence"] == {"kind": "plan_rejected", "task_ids": [], "ref": ""}

    def test_a_body_approval_with_no_event_yields_plan_approved_body(self):
        job = _job(task_plan={"_approval": "approved"})
        ledger = own.build_ownership_ledger(job)
        [entry] = [e for e in ledger["entries"] if e["action"] == "plan_approved"]
        assert entry["record_ref"] == "plan_approved:body"
        assert entry["ts"] == ""
        assert entry["actor"] == own.ownership_actor("")
        assert entry["text"] == ""


# ---------------------------------------------------------------------------
# S2 — the actor's door mapping
# ---------------------------------------------------------------------------


class TestActorDoorMapping:
    @pytest.mark.parametrize("recorded_as,door", [
        ("cli", "cli"),
        ("tf:0123456789abcdef", "browser"),
        ("cockpit", "browser"),
        ("ui", "browser"),
        ("batch", ""),
    ])
    def test_door_mapping(self, recorded_as, door):
        assert own.ownership_actor(recorded_as)["door"] == door

    def test_an_unknown_kind_raises(self):
        with pytest.raises(own.OwnershipError):
            own.ownership_actor("alice", kind="astronaut")


# ---------------------------------------------------------------------------
# S5 — token numbering and sort order
# ---------------------------------------------------------------------------


class TestTokenNumbering:
    def test_fingerprints_numbered_by_first_appearance_not_text_order(self):
        job = _job()
        tv.record_veto_answer(job.job_id, "req-z", "T1", tv.REPLAN_FOLLOW_UP,
                              "tf:zzzzzzzzzzzzzzzz", "")
        tv.record_veto_answer(job.job_id, "req-a", "T2", tv.ACCEPT_REDUCED_SCOPE,
                              "tf:aaaaaaaaaaaaaaaa", "")
        tv.record_veto_answer(job.job_id, "req-c", "T3", tv.REPLAN_FOLLOW_UP, "cli", "")
        # Fix the timestamps directly on the written files: the order below (z before a) is
        # what "by first appearance, not text order" is testing, and it must not depend on
        # how fast three real-clock calls happen to land.
        _patch_json(_veto_answer_path(job.job_id, "req-z"),
                   answered_at="2026-01-01T00:00:01+00:00")
        _patch_json(_veto_answer_path(job.job_id, "req-a"),
                   answered_at="2026-01-01T00:00:02+00:00")
        _patch_json(_veto_answer_path(job.job_id, "req-c"),
                   answered_at="2026-01-01T00:00:03+00:00")

        ledger = own.build_ownership_ledger(job)
        by_actor = {e["actor"]["recorded_as"]: e["actor"]["token_number"]
                   for e in ledger["entries"]}
        assert by_actor["tf:zzzzzzzzzzzzzzzz"] == 1
        assert by_actor["tf:aaaaaaaaaaaaaaaa"] == 2
        assert by_actor["cli"] == 0


class TestSortOrder:
    def test_an_entry_with_empty_ts_sorts_after_every_dated_one(self):
        job = _job()
        tv.record_veto_answer(job.job_id, "req-dated", "T1", tv.REPLAN_FOLLOW_UP, "alice", "")
        tv.record_veto_answer(job.job_id, "req-timeless", "T2", tv.ACCEPT_REDUCED_SCOPE,
                              "bob", "")
        _patch_json(_veto_answer_path(job.job_id, "req-dated"),
                   answered_at="2026-01-01T00:00:00+00:00")
        _patch_json(_veto_answer_path(job.job_id, "req-timeless"), answered_at="")

        ledger = own.build_ownership_ledger(job)
        refs = [e["record_ref"] for e in ledger["entries"]]
        assert refs[-1] == "veto_answer:req-timeless"
        assert refs[0] == "veto_answer:req-dated"


# ---------------------------------------------------------------------------
# S3 — ownership_entry_problems, direct
# ---------------------------------------------------------------------------


class TestOwnershipEntryProblems:
    def _sound_entry(self) -> dict:
        return {
            "record_ref": "veto:req-1", "ts": "2026-01-01T00:00:00+00:00",
            "actor": own.ownership_actor("alice"), "action": "task_vetoed", "task_id": "T1",
            "text": "reason", "consequence": {"kind": "unreachable", "task_ids": [], "ref": ""},
            "detail": {},
        }

    def test_a_sound_entry_answers_empty(self):
        assert own.ownership_entry_problems(self._sound_entry()) == []

    def test_a_missing_key_is_reported(self):
        entry = self._sound_entry()
        del entry["text"]
        problems = own.ownership_entry_problems(entry)
        assert any("text" in p for p in problems)

    def test_an_actor_kind_outside_actor_kinds_is_reported(self):
        entry = self._sound_entry()
        entry["actor"] = {**entry["actor"], "kind": "astronaut"}
        problems = own.ownership_entry_problems(entry)
        assert any("kind" in p for p in problems)


# ---------------------------------------------------------------------------
# S5 — idempotence
# ---------------------------------------------------------------------------


class TestIdempotence:
    def test_two_builds_over_the_same_records_are_equal(self):
        job = _job(tasks=_two_task_chain())
        tv.record_task_veto(job.job_id, "T1", "risky", "alice", pj.TASK_PENDING)
        pj._fold_task_vetoes(job, None, None)
        tv.record_veto_answer(job.job_id, "req-1", "T1", tv.REPLAN_FOLLOW_UP, "alice", "")
        st.record_steering_message(job.job_id, "note", job_state="running", channel="cli",
                                   task_id="T1")

        first = own.build_ownership_ledger(job)
        second = own.build_ownership_ledger(job)
        assert first == second
