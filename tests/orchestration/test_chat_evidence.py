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
    collect_project_evidence,
    compose_chat_evidence,
    make_chat_item,
    node_evidence_set,
    project_evidence_set,
    render_chat_evidence,
)
from packages.orchestration.data_paths import (
    job_evidence_dir,
    job_evidence_index_dir,
    run_dir,
    run_log_dir,
)
from packages.orchestration.mission_dossier import DossierItem, MissionDossier, save_dossier_state
from packages.orchestration.mission_state import create_mission
from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan
from packages.orchestration.project_registry import RemyProject
from packages.orchestration.token_ledger import (
    COST_BASIS_PROVIDER_REPORTED,
    CallRecord,
    record_call,
)


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


def _write_prompt_trace(run_id: str, lines: list[str]) -> None:
    """Write a task run's `prompt_trace.jsonl` under `run_dir`, one raw line each."""
    d = run_dir(run_id)
    d.mkdir(parents=True, exist_ok=True)
    (d / "prompt_trace.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_status_md(repo_dir: Path, body: str) -> str:
    """Write `docs/roadmap/STATUS.md` under a repository in `tmp_path`."""
    status_path = repo_dir / "docs" / "roadmap" / "STATUS.md"
    status_path.parent.mkdir(parents=True, exist_ok=True)
    status_path.write_text(body, encoding="utf-8")
    return str(repo_dir)


def _make_project(**overrides) -> RemyProject:
    """A project object, never persisted to the registry — `chat_evidence` reads
    only the object it is given, never the registry store."""
    overrides.setdefault("name", "f038-chat-project")
    return RemyProject(**overrides)


def _make_project_job(created_at: str, **overrides) -> JobPlan:
    """A saved job with a controlled `created_at`, so project-scope ordering
    (newest first) is deterministic across a test. Carries a `target_repo` so
    `decision_queue.list_decisions`' stop-reason branch does not also derive a
    `sr:derived_no_repo` decision nobody asked for."""
    defaults = dict(
        job_title="f038-chat-project-job", tasks=[],
        metadata={"target_repo": "/tmp/repo"},
    )
    defaults.update(overrides)
    job = JobPlan(created_at=created_at, **defaults)
    save_job_plan(job)
    return job


# ---------------------------------------------------------------------------
# S5 THE NODE SCOPE — the eleven-item and the eight-item shapes.
# ---------------------------------------------------------------------------


def test_a_fully_recorded_task_yields_exactly_the_twelve_items_in_order() -> None:
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
        ("node", task_id, "Prompt trace: not recorded (trace_missing)"),
        ("diff", "a.py", "Changed a.py (modified, +1 −1)"),
        ("diff", "b.py", "Changed b.py (modified, +1 −0)"),
        ("event", "task_run_completed@2026-09-28T00:02:00+00:00",
         "2026-09-28T00:02:00+00:00 task_run_completed: done (outcome pass)"),
        ("event", "task_run_started@2026-09-28T00:00:00+00:00",
         "2026-09-28T00:00:00+00:00 task_run_started"),
    ]


def test_a_task_with_nothing_recorded_yields_exactly_the_nine_items() -> None:
    job, task_id = _make_job()

    items = collect_node_evidence(job, task_id)

    assert [(item.kind, item.ref, item.text) for item in items] == [
        ("node", task_id, f"Task {task_id}: {CHAT_NOT_RECORDED}"),
        ("node", task_id, "Status: pending"),
        ("node", task_id, f"Reviewer verdict: {CHAT_NOT_RECORDED}"),
        ("node", task_id, f"Tests: {CHAT_NOT_RECORDED}"),
        ("node", task_id, "Repair rounds used: 0 of 0"),
        ("node", task_id, "Run rounds: not recorded (no_run_recorded)"),
        ("node", task_id, "Prompt trace: not recorded (no_run_recorded)"),
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
    assert len(evidence_set.items) == 9
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
        "kind 'bogus' is not one of node, round, prompt, diff, event, project, "
        "roadmap, decision, pattern, dossier, ledger, job"
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
        "kind 'bogus' is not one of node, round, prompt, diff, event, project, "
        "roadmap, decision, pattern, dossier, ledger, job",
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


def test_a_malformed_item_and_an_unknown_scope_are_refused() -> None:
    good = make_chat_item("node", "T001", "fine")
    bad = ChatEvidenceItem(kind="bogus", ref="", text="fine")

    with pytest.raises(ChatEvidenceError, match=r"^item 1: kind 'bogus'"):
        compose_chat_evidence("node", "T001", [good, bad])

    with pytest.raises(
        ChatEvidenceError, match=r"^scope 'mission' is not one of node, project$"
    ):
        compose_chat_evidence("mission", "T001", [good])


def test_two_builds_of_the_same_tasks_set_are_equal() -> None:
    job, task_id = _make_job()

    first = node_evidence_set(job, task_id)
    second = node_evidence_set(job, task_id)

    assert first == second
    assert first.scope == "node"
    assert first.subject == task_id
    assert first.omitted == 0


# ---------------------------------------------------------------------------
# S2 THE PROMPT TRACE — metadata only, and the honest absences.
# ---------------------------------------------------------------------------


def test_a_prompt_trace_with_junk_lines_yields_exactly_the_recorded_entries() -> None:
    run_id = "abc123ef01234567"
    job, task_id = _make_job(run_id=run_id)
    builder_entry = {
        "round": 1, "role": "builder", "prompt_kind": "initial",
        "prompt_tokens_estimated": 123, "provider": "anthropic",
        "configured_model": "claude-x",
        "prompt_text_redacted": "the whole composed prompt, never cited",
    }
    reviewer_entry = {
        "round": 2, "role": "reviewer", "prompt_kind": "review",
        "prompt_tokens_estimated": 50, "provider": "ollama",
    }
    _write_prompt_trace(run_id, [
        json.dumps(builder_entry),
        "not json {{{",
        json.dumps([1, 2, 3]),
        "",
        json.dumps(reviewer_entry),
    ])

    items = collect_node_evidence(job, task_id)
    prompt_items = [item for item in items if item.kind == "prompt"]

    assert [(item.ref, item.text) for item in prompt_items] == [
        (f"{task_id}#1/builder",
         "Prompt for round 1, builder (initial): 123 tokens estimated; "
         "provider anthropic; model claude-x"),
        (f"{task_id}#2/reviewer",
         "Prompt for round 2, reviewer (review): 50 tokens estimated; "
         "provider ollama; model not recorded"),
    ]
    assert all("whole composed prompt" not in item.text for item in items)


def test_a_trace_holding_only_a_blank_line_says_trace_empty() -> None:
    run_id = "0123456789abcdef"
    job, task_id = _make_job(run_id=run_id)
    _write_prompt_trace(run_id, [""])

    items = collect_node_evidence(job, task_id)
    trace_items = [item for item in items if "Prompt trace" in item.text]

    assert len(trace_items) == 1
    assert trace_items[0].text == "Prompt trace: not recorded (trace_empty)"


def test_a_run_id_with_a_trailing_newline_is_no_run() -> None:
    job, task_id = _make_job(run_id="abcdef01\n")

    items = collect_node_evidence(job, task_id)
    trace_items = [item for item in items if "Prompt trace" in item.text]

    assert len(trace_items) == 1
    assert trace_items[0].text == "Prompt trace: not recorded (no_run_recorded)"


# ---------------------------------------------------------------------------
# S3 THE PROJECT SCOPE — one registry project's own records.
# ---------------------------------------------------------------------------


def test_a_project_with_nothing_linked_yields_exactly_the_five_items() -> None:
    project = _make_project()
    pid = str(project.id)

    items = collect_project_evidence(project)

    assert [(item.kind, item.ref, item.text) for item in items] == [
        ("project", pid,
         f"Project {project.name}: 0 linked jobs; repository not recorded"),
        ("project", pid, "Roadmap position: not recorded (no repository)"),
        ("project", pid, "Mission dossier: not recorded"),
        ("project", pid, "Token ledger: not recorded"),
        ("project", pid, "Jobs: not recorded for this project"),
    ]


def test_the_roadmap_position_reads_status_by_its_own_grammar(tmp_path: Path) -> None:
    def roadmap_text(name: str, body: str) -> str:
        repo_path = _write_status_md(tmp_path / name, body)
        project = _make_project(canonical_repo_path=repo_path)
        items = collect_project_evidence(project)
        matches = [item for item in items if item.text.startswith("Roadmap")]
        assert len(matches) == 1
        return matches[0].text

    in_progress = roadmap_text("in_progress", (
        "## Tier 1 — Bootstrap\n\n"
        "- [~] F100 — Rework the widget\n"
    ))
    assert in_progress == "Roadmap: F100 — Rework the widget is in progress"

    next_open = roadmap_text("next_open", (
        "## Tier 1 — Bootstrap\n\n"
        "- [x] F100 — Rework the widget\n"
        "- [ ] F101 — Ship the gadget\n"
    ))
    assert next_open == "Roadmap: F101 — Ship the gadget is the next open feature"

    no_open = roadmap_text("no_open", (
        "## Tier 1 — Bootstrap\n\n"
        "- [x] F100 — Rework the widget\n"
        "- [x] F101 — Ship the gadget\n"
    ))
    assert no_open == "Roadmap position: no open feature"

    grammar_error = roadmap_text("dup", (
        "## Tier 1 — Bootstrap\n\n"
        "- [ ] F100 — Rework the widget\n"
        "- [ ] F100 — Rework the widget again\n"
    ))
    assert grammar_error == "Roadmap position: not recorded (RoadmapGrammarError)"


def test_project_scope_filters_to_linked_jobs_and_groups_their_decisions() -> None:
    job_old = _make_project_job("2026-09-01T00:00:00+00:00")
    job_new = _make_project_job("2026-09-02T00:00:00+00:00")
    job_other = _make_project_job("2026-09-03T00:00:00+00:00")

    for job, run_tag in ((job_new, "newrun01"), (job_old, "oldrun01")):
        _write_events(job.job_id, [{
            "event": "test_run_completed",
            "timestamp": "2026-09-28T00:00:00+00:00",
            "metadata": {"status": "failed", "command_safe": "pytest -q",
                         "test_run_id": run_tag},
        }])
    _write_events(job_other.job_id, [{
        "event": "test_run_completed",
        "timestamp": "2026-09-28T00:00:00+00:00",
        "metadata": {"status": "failed", "command_safe": "pytest -q",
                     "test_run_id": "otherun1"},
    }])

    project = _make_project(job_ids=[job_old.job_id, job_new.job_id])

    items = collect_project_evidence(project)

    job_items = [item for item in items if item.kind == "job"]
    assert [item.ref for item in job_items] == [job_new.job_id, job_old.job_id]

    # Each linked job's failing test run derives TWO open decisions —
    # `decision_queue.list_decisions`' stop-reason branch AND its dedicated
    # test-failure branch both fire on the same event — grouped by job, newest
    # job first, in the module's own within-job order.
    decision_items = [item for item in items if item.kind == "decision"]
    assert [item.ref for item in decision_items] == [
        f"{job_new.job_id}/sr:derived_test_fail",
        f"{job_new.job_id}/tf:newrun01",
        f"{job_old.job_id}/sr:derived_test_fail",
        f"{job_old.job_id}/tf:oldrun01",
    ]
    assert decision_items[1].text == (
        f"Open blocker decision on job {job_new.job_id}: Test 'pytest -q' failed."
    )

    pattern_items = [item for item in items if item.kind == "pattern"]
    assert [(item.ref, item.text) for item in pattern_items] == [
        ("test_1",
         "Pattern repeated_test_failure (low): Tests failed 2 times across 2 job(s)"),
    ]

    # S3's order puts the job digests LAST, after the decisions — so the token
    # cap drops the oldest jobs first (DECISION F038 D3).
    kinds_in_order = [item.kind for item in items]
    last_decision_index = max(
        i for i, kind in enumerate(kinds_in_order) if kind == "decision"
    )
    first_job_index = min(
        i for i, kind in enumerate(kinds_in_order) if kind == "job"
    )
    assert last_decision_index < first_job_index


def test_a_missions_dossier_yields_its_goal_next_step_and_open_risks() -> None:
    project = _make_project()
    pid = str(project.id)
    mission = create_mission(pid, "Ship the grounded chat")
    dossier = MissionDossier(
        goal="Ship the grounded chat",
        risks=(
            DossierItem(
                id="r1", text="Provider outages could stall the run", resolved=False
            ),
            DossierItem(id="r2", text="An old risk already closed", resolved=True),
        ),
        next_step="Write the citation check",
    )
    save_dossier_state(pid, mission.id, dossier)

    items = collect_project_evidence(project)
    dossier_items = [item for item in items if item.kind == "dossier"]

    assert [item.text for item in dossier_items] == [
        "Mission goal: Ship the grounded chat",
        "Mission next step: Write the citation check",
        "Mission risk: Provider outages could stall the run",
    ]
    assert all(item.ref == mission.id for item in dossier_items)


def test_the_token_ledger_reads_measured_figures_and_names_the_unmeasured() -> None:
    measured_project = _make_project()
    record_call(
        CallRecord(
            call_id="call-measured-1",
            ts_utc="2026-09-28T00:00:00+00:00",
            tokens_in=100,
            tokens_out=50,
            cost_usd=0.25,
            cost_basis=COST_BASIS_PROVIDER_REPORTED,
        ),
        project_id=str(measured_project.id),
    )
    measured_items = collect_project_evidence(measured_project)
    measured_ledger = [item for item in measured_items if item.kind == "ledger"]
    assert [item.text for item in measured_ledger] == [
        "Token ledger: calls 1; tokens in 100; tokens out 50; cost $0.25"
    ]

    unmeasured_project = _make_project()
    record_call(
        CallRecord(call_id="call-unmeasured-1", ts_utc="2026-09-28T00:00:01+00:00"),
        project_id=str(unmeasured_project.id),
    )
    unmeasured_items = collect_project_evidence(unmeasured_project)
    unmeasured_ledger = [item for item in unmeasured_items if item.kind == "ledger"]
    assert [item.text for item in unmeasured_ledger] == [
        "Token ledger: calls 1; tokens in unmeasured; tokens out unmeasured; "
        "cost unmeasured"
    ]


def test_project_evidence_set_is_deterministic_and_writes_no_file(
    tmp_path: Path,
) -> None:
    project = _make_project()
    before = sorted(p for p in tmp_path.rglob("*") if p.is_file())

    first = project_evidence_set(project)
    second = project_evidence_set(project)

    after = sorted(p for p in tmp_path.rglob("*") if p.is_file())
    assert before == after
    assert first == second
    assert first.scope == "project"
    assert first.subject == str(project.id)
    assert first.omitted == 0
