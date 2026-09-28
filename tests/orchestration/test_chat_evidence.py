"""F038 T001 — the grounded chat's node-scope evidence item, composer and collector.

Every fixture below writes its on-disk records through the REAL writers
(`save_job_plan`; a run report at `run_dir(<run id>)/"result.json"`; a `safe.diff`
under `job_evidence_dir(job_id)/"task_runs"/<task id>` with an index record; events as
JSON lines under `run_log_dir(job_id)`), never through a monkeypatched shortcut.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from packages.orchestration.chat_evidence import (
    CHAT_EVIDENCE_TOKEN_CAP,
    CHAT_NOT_RECORDED,
    ChatEvidenceError,
    ChatEvidenceItem,
    ChatEvidenceSet,
    chat_item_problems,
    collect_node_evidence,
    compose_chat_evidence,
    make_chat_item,
    node_evidence_set,
    render_chat_evidence,
)
from packages.orchestration.data_paths import (
    job_evidence_dir,
    job_evidence_index_dir,
    run_dir,
    run_log_dir,
)
from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan


@pytest.fixture(autouse=True)
def _isolated_data_root(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))


# ---------------------------------------------------------------------------
# Fixture helpers — the real writers, never a monkeypatch of this module.
# ---------------------------------------------------------------------------


def _make_job(**task_overrides) -> tuple[JobPlan, str]:
    """A saved job with one task, carrying the minted default id."""
    task = TaskEntry(**task_overrides)
    job = JobPlan(job_title="f038-chat-evidence-job", tasks=[task])
    save_job_plan(job)
    return job, task.task_id


def _write_run_report(run_id: str, rounds: list[dict], *, retries_used: int = 0) -> None:
    d = run_dir(run_id)
    d.mkdir(parents=True, exist_ok=True)
    (d / "result.json").write_text(
        json.dumps({"rounds": rounds, "retries_used": retries_used}), encoding="utf-8"
    )


def _write_diff(job_id: str, task_id: str, diff_text: str) -> None:
    """Write a task run's `safe.diff` and index the job, so `build_diff_view` reads it."""
    ev_dir = job_evidence_dir(job_id)
    task_dir = ev_dir / "task_runs" / task_id
    task_dir.mkdir(parents=True, exist_ok=True)
    (task_dir / "safe.diff").write_text(diff_text, encoding="utf-8")
    idx_dir = job_evidence_index_dir()
    idx_dir.mkdir(parents=True, exist_ok=True)
    (idx_dir / f"{job_id}.json").write_text(
        json.dumps({"evidence_dir_local": str(ev_dir)}), encoding="utf-8"
    )


def _write_events(job_id: str, events: list[dict]) -> None:
    log_dir = run_log_dir(job_id)
    log_dir.mkdir(parents=True, exist_ok=True)
    with (log_dir / "run1.jsonl").open("w", encoding="utf-8") as handle:
        for event in events:
            handle.write(json.dumps(event) + "\n")


_TWO_FILE_DIFF = (
    "diff --git a/a.py b/a.py\n--- a/a.py\n+++ b/a.py\n@@ -1,1 +1,1 @@\n-x\n+y\n"
    "diff --git a/b.py b/b.py\n--- a/b.py\n+++ b/b.py\n@@ -1,1 +1,2 @@\n x\n+z\n"
)


# ---------------------------------------------------------------------------
# S5 THE NODE SCOPE — the eleven-item and the eight-item shapes.
# ---------------------------------------------------------------------------


def test_a_fully_recorded_task_yields_exactly_the_eleven_items_in_order() -> None:
    run_id = "fedcba9876543210"
    job, task_id = _make_job(
        title="Write the README",
        status="completed",
        final_status="succeeded",
        run_id=run_id,
        reviewer_verdict="pass",
        test_passed=True,
        repair_rounds_used=1,
        repair_rounds_allowed=3,
    )
    _write_run_report(run_id, [
        {"round": 1, "kind": "build", "test_passed": True, "reviewer": {"verdict": "pass"}},
        {"round": 2, "kind": "repair", "test_passed": False, "reviewer": {"verdict": "fail"}},
    ])
    _write_diff(job.job_id, task_id, _TWO_FILE_DIFF)
    _write_events(job.job_id, [
        {"event": "task_run_started", "timestamp": "2026-09-28T00:00:00+00:00",
         "task_id": task_id},
        {"event": "task_run_other", "timestamp": "2026-09-28T00:01:00+00:00",
         "task_id": "some-other-task"},
        {"event": "task_run_completed", "timestamp": "2026-09-28T00:02:00+00:00",
         "metadata": {"task_id": task_id}, "message": "done", "outcome": "pass"},
    ])

    items = collect_node_evidence(job, task_id)

    assert [(item.kind, item.ref, item.text) for item in items] == [
        ("node", task_id, f"Task {task_id}: Write the README"),
        ("node", task_id, "Status: completed; final status: succeeded"),
        ("node", task_id, "Reviewer verdict: pass"),
        ("node", task_id, "Tests: passed"),
        ("node", task_id, "Repair rounds used: 1 of 3"),
        ("round", f"{task_id}#1", "Round 1 (build): tests passed; reviewer verdict pass"),
        ("round", f"{task_id}#2", "Round 2 (repair): tests failed; reviewer verdict fail"),
        ("diff", "a.py", "Changed a.py (modified, +1 −1)"),
        ("diff", "b.py", "Changed b.py (modified, +1 −0)"),
        ("event", "task_run_completed@2026-09-28T00:02:00+00:00",
         "2026-09-28T00:02:00+00:00 task_run_completed: done (outcome pass)"),
        ("event", "task_run_started@2026-09-28T00:00:00+00:00",
         "2026-09-28T00:00:00+00:00 task_run_started"),
    ]


def test_a_task_with_nothing_recorded_yields_exactly_the_eight_items() -> None:
    job, task_id = _make_job()

    items = collect_node_evidence(job, task_id)

    assert [(item.kind, item.ref, item.text) for item in items] == [
        ("node", task_id, f"Task {task_id}: {CHAT_NOT_RECORDED}"),
        ("node", task_id, "Status: pending"),
        ("node", task_id, f"Reviewer verdict: {CHAT_NOT_RECORDED}"),
        ("node", task_id, f"Tests: {CHAT_NOT_RECORDED}"),
        ("node", task_id, "Repair rounds used: 0 of 0"),
        ("node", task_id, "Run rounds: not recorded (no_run_recorded)"),
        ("node", task_id, "Diff: not recorded (evidence_dir_unavailable)"),
        ("node", task_id, "Run log: not recorded for this task"),
    ]


def test_status_detail_failed_test_error_and_tripped_limit_each_appear() -> None:
    job, task_id = _make_job(
        status="failed",
        final_status="errored",
        final_status_detail="provider unavailable",
        test_passed=False,
        error="boom",
        tripped_limit="wall_clock",
    )

    items = collect_node_evidence(job, task_id)
    texts = [item.text for item in items]

    assert "Status: failed; final status: errored (provider unavailable)" in texts
    assert "Tests: failed" in texts
    assert "Error: boom" in texts
    assert "Tripped limit: wall_clock" in texts


def test_an_unknown_id_a_prefix_and_the_empty_string_are_refused() -> None:
    job, task_id = _make_job()

    for bad_id in ("not-a-real-task-id", task_id[:8], ""):
        with pytest.raises(ChatEvidenceError, match="is not a task of job"):
            collect_node_evidence(job, bad_id)


def test_an_event_with_no_name_gives_no_item() -> None:
    job, task_id = _make_job()
    _write_events(job.job_id, [
        {"event": "", "timestamp": "2026-09-28T00:00:00+00:00", "task_id": task_id},
        {"timestamp": "2026-09-28T00:00:01+00:00", "task_id": task_id},
        {"event": "task_run_started", "timestamp": "2026-09-28T00:00:02+00:00",
         "task_id": task_id},
    ])

    items = collect_node_evidence(job, task_id)
    event_items = [item for item in items if item.kind == "event"]

    assert len(event_items) == 1
    assert event_items[0].ref == "task_run_started@2026-09-28T00:00:02+00:00"


def test_node_evidence_set_composes_the_collected_items() -> None:
    job, task_id = _make_job()

    evidence_set = node_evidence_set(job, task_id)

    assert evidence_set.scope == "node"
    assert evidence_set.subject == task_id
    assert len(evidence_set.items) == 8
    assert evidence_set.omitted == 0


def test_building_a_set_writes_no_file(tmp_path: Path) -> None:
    job, task_id = _make_job()
    before = sorted(p for p in tmp_path.rglob("*") if p.is_file())

    node_evidence_set(job, task_id)

    after = sorted(p for p in tmp_path.rglob("*") if p.is_file())
    assert before == after


# ---------------------------------------------------------------------------
# S3 THE ITEM — make_chat_item, chat_item_problems, render_*.
# ---------------------------------------------------------------------------


def test_make_chat_item_redacts_before_folding_and_cutting() -> None:
    secret_text = "the key is sk-ant-api03-abcdefghijklmnopqrst right here"
    redacted = make_chat_item("node", "T001", secret_text)
    assert "sk-ant" not in redacted.text

    broken_line = "first line\r\nsecond line\nthird"
    folded = make_chat_item("node", "T001", broken_line)
    assert "\n" not in folded.text
    assert "\r" not in folded.text
    assert folded.text == "first line second line third"

    long_text = "x" * 1000
    cut = make_chat_item("node", "T001", long_text)
    assert len(cut.text) == 400
    assert cut.text.endswith("…")
    assert cut.text[:-1] == "x" * 399

    exact_text = "y" * 400
    whole = make_chat_item("node", "T001", exact_text)
    assert whole.text == exact_text
    assert len(whole.text) == 400


def test_chat_item_problems_reads_each_of_its_lines() -> None:
    assert chat_item_problems("not an item") == ["not a ChatEvidenceItem"]
    assert chat_item_problems(42) == ["not a ChatEvidenceItem"]

    bad_kind = ChatEvidenceItem(kind="bogus", ref="T001", text="fine")
    assert chat_item_problems(bad_kind) == [
        "kind 'bogus' is not one of node, round, diff, event"
    ]

    bad_ref = ChatEvidenceItem(kind="node", ref="", text="fine")
    assert chat_item_problems(bad_ref) == ["ref is not a non-empty string"]

    empty_text = ChatEvidenceItem(kind="node", ref="T001", text="   ")
    assert chat_item_problems(empty_text) == ["text is not a non-empty string"]

    line_break_text = ChatEvidenceItem(kind="node", ref="T001", text="a\nb")
    assert chat_item_problems(line_break_text) == ["text holds a line break"]

    too_long_text = ChatEvidenceItem(kind="node", ref="T001", text="z" * 401)
    assert chat_item_problems(too_long_text) == [
        "text is longer than 400 characters"
    ]

    sound = ChatEvidenceItem(kind="node", ref="T001", text="fine")
    assert chat_item_problems(sound) == []

    multi_problem = ChatEvidenceItem(kind="bogus", ref="", text="fine")
    assert chat_item_problems(multi_problem) == [
        "kind 'bogus' is not one of node, round, diff, event",
        "ref is not a non-empty string",
    ]


def test_render_chat_evidence_of_two_items() -> None:
    evidence_set = ChatEvidenceSet(
        scope="node",
        subject="T001",
        items=(
            ChatEvidenceItem(kind="node", ref="T001", text="a"),
            ChatEvidenceItem(kind="diff", ref="x.py", text="b"),
        ),
        omitted=0,
        tokens_estimated=9,
    )

    assert render_chat_evidence(evidence_set) == "[1] node:T001 — a\n[2] diff:x.py — b"
    assert render_chat_evidence(
        ChatEvidenceSet(scope="node", subject="T001", items=(), omitted=0, tokens_estimated=0)
    ) == ""


# ---------------------------------------------------------------------------
# S4 THE COMPOSER — the cap, malformed items and the unknown scope.
# ---------------------------------------------------------------------------


def test_the_cap_keeps_a_strict_ordered_prefix_and_counts_the_rest_omitted() -> None:
    items = [
        make_chat_item("node", f"T{n:03d}", "x" * 100) for n in range(200)
    ]

    evidence_set = compose_chat_evidence("node", "T001", items)

    assert len(evidence_set.items) < len(items)
    assert evidence_set.items == tuple(items[: len(evidence_set.items)])
    assert evidence_set.omitted == len(items) - len(evidence_set.items)
    assert evidence_set.omitted > 0
    rendered = render_chat_evidence(evidence_set)
    assert evidence_set.tokens_estimated > 0

    from packages.orchestration.token_economy import estimate_text_tokens

    assert estimate_text_tokens(rendered) == evidence_set.tokens_estimated
    assert estimate_text_tokens(rendered) <= CHAT_EVIDENCE_TOKEN_CAP
    next_index = len(evidence_set.items)
    next_candidate = "\n".join(
        f"[{i + 1}] {it.kind}:{it.ref} — {it.text}"
        for i, it in enumerate(items[: next_index + 1])
    )
    assert estimate_text_tokens(next_candidate) > CHAT_EVIDENCE_TOKEN_CAP


def test_a_cap_of_one_keeps_nothing() -> None:
    items = [
        make_chat_item("node", "T001", "a"),
        make_chat_item("diff", "x.py", "b"),
    ]

    evidence_set = compose_chat_evidence("node", "T001", items, token_cap=1)

    assert evidence_set.items == ()
    assert evidence_set.omitted == 2
    assert evidence_set.tokens_estimated == 0


def test_a_malformed_item_and_the_scope_project_are_refused() -> None:
    good = make_chat_item("node", "T001", "fine")
    bad = ChatEvidenceItem(kind="bogus", ref="", text="fine")

    with pytest.raises(ChatEvidenceError, match=r"^item 1: kind 'bogus'"):
        compose_chat_evidence("node", "T001", [good, bad])

    with pytest.raises(ChatEvidenceError, match="scope 'project' is not one of node"):
        compose_chat_evidence("project", "T001", [good])


def test_two_builds_of_the_same_tasks_set_are_equal() -> None:
    job, task_id = _make_job()

    first = node_evidence_set(job, task_id)
    second = node_evidence_set(job, task_id)

    assert first == second
    assert first.scope == "node"
    assert first.subject == task_id
    assert first.omitted == 0
