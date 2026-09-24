"""F264 T002 — a steering message is consumed at the run's next safe point, never mid-call.

T5_F264.md's Acceptance, as fixtures: a message sent during round N changes round N+1's
builder prompt — proved by comparing that prompt with and without the message — while round
N's prompt, already sent, is untouched; the message's consumption round is recorded; and a
run with no job never reads a message. Scripted providers only: no model is ever called.
"""
from __future__ import annotations

import pytest

from packages.orchestration import steering as ST
from packages.orchestration.pingpong_loop import compose_builder_prompt, run_pingpong
from packages.orchestration.pingpong_provider import FakeProvider
from packages.orchestration.prompt_segments import SegmentStabilityRank
from packages.orchestration.timeline import load_run_events

JOB = "fedcba9876543210"
TASK = "task-1"
MESSAGE = "Use pnpm, never npm."


def _repo(tmp_path):
    repo = tmp_path / "repo"
    (repo / "docs").mkdir(parents=True)
    (repo / "README.md").write_text("# Demo\n")
    (repo / "docs" / "README.md").write_text("# Docs\n")
    return repo


class _Recording(FakeProvider):
    """FakeProvider fails round 1 and passes round 2; this records every builder prompt and,
    when told to, sends a steering message WHILE round 1's builder call is in flight."""

    def __init__(self, *, send_mid_call: bool):
        super().__init__()
        self.builder_prompts: list[str] = []
        self.send_mid_call = send_mid_call

    def build(self, prompt, **kw):
        self.builder_prompts.append(prompt)
        if self.send_mid_call and len(self.builder_prompts) == 1:
            ST.record_steering_message(JOB, MESSAGE, job_state="running", channel="cli")
        return super().build(prompt, **kw)


def _run(tmp_path, monkeypatch, *, send_mid_call: bool, job_id: str = JOB) -> _Recording:
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    prov = _Recording(send_mid_call=send_mid_call)
    run_pingpong("Fix README", str(_repo(tmp_path)), builder_provider=prov,
                 reviewer_provider=prov, max_rounds=3, repair_rounds=2,
                 job_id=job_id, task_id=TASK)
    return prov


def test_a_message_sent_during_round_one_changes_round_two_and_only_round_two(tmp_path, monkeypatch):
    without = _run(tmp_path / "a", monkeypatch, send_mid_call=False).builder_prompts
    with_msg = _run(tmp_path / "b", monkeypatch, send_mid_call=True).builder_prompts
    assert len(without) == len(with_msg) == 2
    # Round 1's prompt was composed before the message existed: it is byte-identical.
    assert with_msg[0] == without[0]
    assert MESSAGE not in with_msg[0]
    # Round 2's prompt differs by exactly the steering segment and the blank line that
    # separates it from the directive, and carries the text verbatim.
    segment = ST.render_steering_segment([{"text": MESSAGE}])
    assert MESSAGE not in without[1]
    assert f"- {MESSAGE}\n" in with_msg[1]
    assert with_msg[1].count(segment + "\n") == 1
    assert with_msg[1].replace(segment + "\n", "", 1) == without[1]


def test_the_consumption_round_is_the_round_after_the_call_it_arrived_in(tmp_path, monkeypatch):
    _run(tmp_path, monkeypatch, send_mid_call=True)
    root = tmp_path / "data"
    marker = ST.list_steering_consumptions(JOB, root)["sm-0001"]
    assert (marker["task_id"], marker["round_number"]) == (TASK, 2)
    events = [e for e in load_run_events(root, JOB) if e.get("event") == "steering_message_consumed"]
    assert [(e["metadata"]["message_id"], e["metadata"]["round_number"]) for e in events] == [
        ("sm-0001", 2)]


def test_a_message_waiting_before_the_run_steers_its_first_round(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    ST.record_steering_message(JOB, MESSAGE, job_state="running", channel="cockpit")
    prov = _Recording(send_mid_call=False)
    run_pingpong("Fix README", str(_repo(tmp_path)), builder_provider=prov,
                 reviewer_provider=prov, max_rounds=3, repair_rounds=2, job_id=JOB, task_id=TASK)
    # Consumed once, in round 1, and carried in every later round of the job.
    assert all(f"- {MESSAGE}\n" in p for p in prov.builder_prompts)
    assert ST.list_steering_consumptions(JOB, tmp_path / "data")["sm-0001"]["round_number"] == 1


def test_a_run_with_no_job_never_reads_a_message(tmp_path, monkeypatch):
    prov = _run(tmp_path, monkeypatch, send_mid_call=True, job_id="")
    assert all(MESSAGE not in p for p in prov.builder_prompts)
    assert ST.list_steering_consumptions(JOB, tmp_path / "data") == {}


def test_a_tampered_message_stops_the_run_loudly(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    ST.record_steering_message(JOB, MESSAGE, job_state="running", channel="cli")
    path = ST.steering_dir(JOB, tmp_path / "data") / "sm-0001.json"
    path.write_text(path.read_text(encoding="utf-8").replace("pnpm", "yarn"), encoding="utf-8")
    prov = _Recording(send_mid_call=False)
    with pytest.raises(ST.SteeringError, match="not intact"):
        run_pingpong("Fix README", str(_repo(tmp_path)), builder_provider=prov,
                     reviewer_provider=prov, job_id=JOB, task_id=TASK)
    assert prov.builder_prompts == []


class TestTheSegment:
    def test_it_sits_directly_before_the_directive_at_steering_rank(self):
        composed = compose_builder_prompt("goal", "ctx", steering_text="STEER\n")
        names = [row.name for row in composed.manifest]
        assert names[-2:] == ["builder_steering", "builder_directive"]
        [row] = [r for r in composed.manifest if r.name == "builder_steering"]
        assert row.rank == SegmentStabilityRank.STEERING

    def test_it_is_absent_without_steering_text(self):
        composed = compose_builder_prompt("goal", "ctx")
        assert "builder_steering" not in [row.name for row in composed.manifest]
