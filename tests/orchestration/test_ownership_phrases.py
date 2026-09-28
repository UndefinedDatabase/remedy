"""F035 T002/T003 (DECISION F035 D3, D4) — the phrase catalog, and the view built over it:
one sentence per ledger entry, in the one "you did X" dialect, worded nowhere else.

THE GOLDEN covers one entry per action named in S3, plus one entry per consequence kind of
the two actions (`task_vetoed`, `task_injected`) whose sentence branches on it, plus one entry
per named `plan_edited` command S1's round 4 table adds — a hand-built ledger, never one built
through `build_ownership_ledger`, because the claim under test is the CATALOG's own wording,
not the reader that assembles a ledger from real records. It stands BESIDE, never in place of,
the inline assertions below of every S1 actor phrase, the reason clause's absence for an empty
reason, a multi-line note kept verbatim, a title shown and one not known, `OwnershipError` for
an unknown action, every S1 plain-verb plan-edit sentence, the unknown-command fallback, and
`ownership_view`'s own shape and error form — exactly the coverage the block orders, none of it
duplicated in prose the golden already carries byte for byte.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from packages.orchestration.ownership import OwnershipError
from packages.orchestration.ownership_phrases import (
    ownership_actor_phrase,
    ownership_sentence,
    ownership_sentences,
    ownership_view,
)

GOLDEN_PATH = (
    Path(__file__).resolve().parent / "fixtures" / "ownership" / "golden" / "sentences.txt"
)

#: Titles for the golden ledger's task ids — deliberately NOT every id below carries one
#: (a raw downstream/subtree id list is never looked up here at all; see S3).
TITLES = {
    "T1": "Task One",
    "T2": "Task Two",
    "T3": "Task Three",
    "T4": "Task Four",
    "T5": "Task Five",
    "T6": "Task Six",
    "T7": "Task Seven",
    "T8": "Task Eight",
    "T9": "Task Nine",
    "T-new": "Add caching",
}


def _actor(*, kind: str = "operator", door: str = "", recorded_as: str = "",
          token_number: int = 0, auto_approved: bool = False) -> dict[str, Any]:
    return {
        "kind": kind, "door": door, "recorded_as": recorded_as,
        "token_number": token_number, "auto_approved": auto_approved,
    }


def _entry(action: str, *, record_ref: str, actor: dict[str, Any], task_id: str = "",
          text: str = "", consequence: dict[str, Any] | None = None,
          detail: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "record_ref": record_ref,
        "ts": "",
        "actor": actor,
        "action": action,
        "task_id": task_id,
        "text": text,
        "consequence": consequence or {"kind": "", "task_ids": [], "ref": ""},
        "detail": detail or {},
    }


def _golden_ledger() -> dict[str, Any]:
    """One entry per action of S3, plus one per consequence kind of `task_vetoed` and
    `task_injected` (+3), plus one per named `plan_edited` command S1's round 4 table adds
    (+6), plus one `task_vetoed` `unreachable` veto with no downstream id (R-1084's repair,
    +1) — 29 entries, in this fixed order."""
    entries = [
        _entry("task_vetoed", record_ref="veto:1",
              actor=_actor(recorded_as="alice"), task_id="T1",
              text="known-bad approach",
              consequence={"kind": "unreachable", "task_ids": ["T2", "T3"], "ref": ""}),
        _entry("task_vetoed", record_ref="veto:2",
              actor=_actor(door="cli", recorded_as="cli"), task_id="T4",
              consequence={"kind": "inert", "task_ids": [], "ref": "already applied"}),
        _entry("task_vetoed", record_ref="veto:3",
              actor=_actor(recorded_as="carol"), task_id="T5",
              text="not needed anymore",
              consequence={"kind": "unreachable", "task_ids": [], "ref": ""}),
        _entry("veto_answered", record_ref="veto_answer:1",
              actor=_actor(recorded_as="human"), task_id="T1",
              text="accept_reduced_scope",
              consequence={"kind": "accept_reduced_scope", "task_ids": [], "ref": "job-999"}),
        _entry("task_injected", record_ref="injection:1",
              actor=_actor(auto_approved=True),
              text="Add a caching layer",
              consequence={"kind": "task_added", "task_ids": ["T-new"], "ref": ""}),
        _entry("task_injected", record_ref="injection:2",
              actor=_actor(),
              text="Refactor the client",
              consequence={"kind": "inert", "task_ids": [], "ref": "duplicate of T-new"}),
        _entry("task_injected", record_ref="injection:3",
              actor=_actor(kind="remedy", recorded_as="planner"),
              text="Add integration tests",
              consequence={"kind": "not_folded", "task_ids": [], "ref": ""}),
        _entry("subtree_rerun", record_ref="rerun:1",
              actor=_actor(door="browser", recorded_as="tf:abc123", token_number=1),
              task_id="T1",
              consequence={"kind": "subtree_reset", "task_ids": ["T1", "T2", "T3"], "ref": ""},
              detail={"model_override": "gpt-5-nano"}),
        _entry("plan_edited", record_ref="plan_edit:v7",
              actor=_actor(door="browser", recorded_as="tf:abc123", token_number=1),
              task_id="T2",
              consequence={"kind": "plan_version", "task_ids": ["T2"], "ref": "v7"},
              detail={"command": "task edit T2 --acceptance add", "args": {"task_id": "T2"}}),
        _entry("plan_edited", record_ref="plan_edit:v9",
              actor=_actor(), task_id="T1",
              consequence={"kind": "plan_version", "task_ids": ["T1"], "ref": "v9"},
              detail={"command": "plan_edit_task"}),
        _entry("plan_edited", record_ref="plan_edit:v10",
              actor=_actor(), task_id="T2",
              consequence={"kind": "plan_version", "task_ids": ["T2"], "ref": "v10"},
              detail={"command": "plan_edit_acceptance"}),
        _entry("plan_edited", record_ref="plan_edit:v11",
              actor=_actor(), task_id="T3",
              consequence={"kind": "plan_version", "task_ids": ["T3"], "ref": "v11"},
              detail={"command": "plan_delete_task"}),
        _entry("plan_edited", record_ref="plan_edit:v12",
              actor=_actor(), task_id="T4",
              consequence={"kind": "plan_version", "task_ids": ["T4"], "ref": "v12"},
              detail={"command": "plan_split_task"}),
        _entry("plan_edited", record_ref="plan_edit:v13",
              actor=_actor(),
              consequence={"kind": "plan_version", "task_ids": [], "ref": "v13"},
              detail={"command": "plan_merge_tasks"}),
        _entry("plan_edited", record_ref="plan_edit:v14",
              actor=_actor(),
              consequence={"kind": "plan_version", "task_ids": [], "ref": "v14"},
              detail={"command": "plan_reorder"}),
        _entry("task_edited", record_ref="plan_edit:v8",
              actor=_actor(),
              task_id="T3",
              consequence={"kind": "plan_version", "task_ids": ["T3"], "ref": "v8"},
              detail={"command": "task edit T3 --files add src/x.py", "runtime": True}),
        _entry("steering_sent", record_ref="steering:1",
              actor=_actor(door="browser", recorded_as="cockpit"),
              text="Focus on the auth flow first",
              consequence={"kind": "consumed", "task_ids": ["T4"], "ref": "round 3"}),
        _entry("note_sent", record_ref="steering:2",
              actor=_actor(door="cli", recorded_as="cli"), task_id="T5",
              text="Watch out for flaky retries",
              consequence={"kind": "not_consumed", "task_ids": [], "ref": ""}),
        _entry("job_paused", record_ref="job_paused:1",
              actor=_actor(recorded_as="human"),
              text="waiting for budget approval",
              consequence={"kind": "withheld", "task_ids": ["T6", "T7"], "ref": ""}),
        _entry("task_paused", record_ref="task_paused:1",
              actor=_actor(recorded_as="bob"), task_id="T6",
              text="needs a design review",
              consequence={"kind": "withheld", "task_ids": ["T6"], "ref": ""}),
        _entry("job_resumed", record_ref="job_resumed:1", actor=_actor()),
        _entry("task_resumed", record_ref="task_resumed:1",
              actor=_actor(door="cli", recorded_as="cli"), task_id="T7"),
        _entry("job_stopped", record_ref="job_stopped:1",
              actor=_actor(recorded_as="alice"),
              text="budget exhausted",
              consequence={"kind": "stopped", "task_ids": [], "ref": ""}),
        _entry("hunk_approved", record_ref="hunk:1:h1",
              actor=_actor(), task_id="T8",
              consequence={"kind": "landing", "task_ids": ["T8"], "ref": "applied"},
              detail={"attempt": "1", "hunk_id": "h1"}),
        _entry("hunk_rejected", record_ref="hunk:1:h2",
              actor=_actor(), task_id="T9",
              text="breaks the API contract",
              consequence={"kind": "landing", "task_ids": ["T9"], "ref": ""},
              detail={"attempt": "1", "hunk_id": "h2"}),
        _entry("decision_answered", record_ref="decision:1",
              actor=_actor(kind="default_policy", recorded_as="default"), task_id="T2",
              text="postgres",
              consequence={"kind": "answer_to_task", "task_ids": ["T2"], "ref": ""},
              detail={"question": "Which database?"}),
        _entry("clarification_answered", record_ref="clarification:1",
              actor=_actor(kind="remedy", recorded_as="planner"),
              text="Auth0",
              consequence={"kind": "plan_input", "task_ids": [], "ref": ""},
              detail={"question": "Which auth provider?"}),
        _entry("plan_approved", record_ref="plan_approved:1",
              actor=_actor(auto_approved=True, recorded_as="auto_yes"),
              consequence={"kind": "plan_approved", "task_ids": [], "ref": ""}),
        _entry("plan_rejected", record_ref="plan_rejected",
              actor=_actor(recorded_as="human"),
              consequence={"kind": "plan_rejected", "task_ids": [], "ref": ""}),
    ]
    return {"schema": "remedy.ownership.v1", "job_id": "golden-job", "entries": entries}


def test_the_golden_ledger_covers_every_action_and_consequence_kind():
    """29 entries: one per S3 action (19), plus one per extra consequence kind of
    `task_vetoed` (+1) and `task_injected` (+2), plus one per named `plan_edited` command
    S1's round 4 table adds (+6), plus one `task_vetoed` `unreachable` veto with no
    downstream id, R-1084's repair (+1)."""
    ledger = _golden_ledger()
    assert len(ledger["entries"]) == 29
    actions = {e["action"] for e in ledger["entries"]}
    assert len(actions) == 19


def test_the_golden_ledger_s_sentences_match_byte_for_byte():
    ledger = _golden_ledger()
    rendered = "\n".join(ownership_sentences(ledger, titles=TITLES)) + "\n"
    golden_bytes = GOLDEN_PATH.read_bytes()
    assert rendered.encode("utf-8") == golden_bytes


# ---------------------------------------------------------------------------
# S1 — every actor phrase
# ---------------------------------------------------------------------------


def test_an_unattended_action_is_auto_approved_via_yes():
    assert (ownership_actor_phrase(_actor(auto_approved=True))
            == "You (auto-approved via --yes)")


def test_an_unattended_action_wins_over_every_other_field():
    """`auto_approved` is checked FIRST: it wins even over a `remedy`/`default_policy`
    kind or a browser door with a token number."""
    actor = _actor(kind="remedy", door="browser", recorded_as="tf:zzz",
                  token_number=9, auto_approved=True)
    assert ownership_actor_phrase(actor) == "You (auto-approved via --yes)"


def test_the_default_policy_phrase():
    assert (ownership_actor_phrase(_actor(kind="default_policy", recorded_as="default"))
            == "The default policy (you accepted at plan approval)")


def test_the_remedy_phrase_names_the_recorded_role():
    assert (ownership_actor_phrase(_actor(kind="remedy", recorded_as="planner"))
            == "Remedy's planner (under this job's configuration)")


def test_a_browser_actor_with_a_token_number_is_named_by_it():
    actor = _actor(door="browser", recorded_as="tf:abc123", token_number=3)
    assert ownership_actor_phrase(actor) == "You (browser, token #3)"


def test_a_browser_actor_without_a_token_number_carries_no_hash():
    actor = _actor(door="browser", recorded_as="cockpit", token_number=0)
    assert ownership_actor_phrase(actor) == "You (browser)"


def test_a_cli_actor():
    assert ownership_actor_phrase(_actor(door="cli", recorded_as="cli")) == "You (command line)"


def test_an_empty_recorded_as_is_plain_you():
    assert ownership_actor_phrase(_actor(recorded_as="")) == "You"


def test_a_human_recorded_as_is_plain_you():
    assert ownership_actor_phrase(_actor(recorded_as="human")) == "You"


def test_any_other_recorded_as_is_kept_verbatim():
    assert ownership_actor_phrase(_actor(recorded_as="alice")) == "You (recorded as alice)"


# ---------------------------------------------------------------------------
# The reason clause, a multi-line note, titles, and the unknown-action error
# ---------------------------------------------------------------------------


def test_an_empty_reason_adds_no_reason_clause():
    entry = _entry("task_paused", record_ref="p1", actor=_actor(), task_id="T1", text="",
                   consequence={"kind": "withheld", "task_ids": ["T1"], "ref": ""})
    assert ownership_sentence(entry, titles=TITLES) == "You paused task T1 (Task One)."


def test_an_unreachable_veto_with_no_ids_adds_no_downstream_clause():
    """R-1084's repair: a veto whose consequence names no unreachable task reads only the
    base sentence, nothing appended after the reason clause — not "0 downstream tasks
    could not run: .\""""
    entry = _entry("task_vetoed", record_ref="veto:3", actor=_actor(recorded_as="carol"),
                   task_id="T5", text="not needed anymore",
                   consequence={"kind": "unreachable", "task_ids": [], "ref": ""})
    assert (ownership_sentence(entry, titles=TITLES)
            == "You (recorded as carol) vetoed task T5 (Task Five) — reason: “not needed anymore”.")


def test_a_multi_line_note_is_kept_verbatim():
    note = "Watch the retry budget\nand page me if it trips twice"
    entry = _entry("note_sent", record_ref="n1", actor=_actor(), task_id="T1", text=note,
                   consequence={"kind": "not_consumed", "task_ids": [], "ref": ""})
    sentence = ownership_sentence(entry, titles=TITLES)
    assert sentence == (
        "You sent a note to task T1 (Task One): “" + note + "”. "
        "The task has not taken it in."
    )


def test_a_known_title_is_shown_beside_the_id():
    entry = _entry("task_resumed", record_ref="r1", actor=_actor(), task_id="T1")
    assert ownership_sentence(entry, titles=TITLES) == "You resumed task T1 (Task One)."


def test_an_unknown_title_shows_the_bare_id():
    entry = _entry("task_resumed", record_ref="r2", actor=_actor(), task_id="T-unknown")
    assert ownership_sentence(entry, titles=TITLES) == "You resumed task T-unknown."


def test_an_id_equal_to_its_own_title_shows_no_parenthetical():
    entry = _entry("task_resumed", record_ref="r3", actor=_actor(), task_id="T1")
    assert ownership_sentence(entry, titles={"T1": "T1"}) == "You resumed task T1."


def test_an_unknown_action_raises_ownershiperror():
    entry = _entry("teleported_the_task", record_ref="x1", actor=_actor(), task_id="T1")
    with pytest.raises(OwnershipError):
        ownership_sentence(entry, titles=TITLES)


# ---------------------------------------------------------------------------
# S1 — the plain-verb plan edits (round 4)
# ---------------------------------------------------------------------------


def test_plan_edit_task_reads_changed_t_in_the_plan():
    entry = _entry("plan_edited", record_ref="pe1", actor=_actor(), task_id="T1",
                   consequence={"kind": "plan_version", "task_ids": ["T1"], "ref": "v9"},
                   detail={"command": "plan_edit_task"})
    assert (ownership_sentence(entry, titles=TITLES)
            == "You changed task T1 (Task One) in the plan; the plan is now at version 9.")


def test_plan_edit_acceptance_reads_changed_the_acceptance_checks_of_t():
    entry = _entry("plan_edited", record_ref="pe2", actor=_actor(), task_id="T2",
                   consequence={"kind": "plan_version", "task_ids": ["T2"], "ref": "v10"},
                   detail={"command": "plan_edit_acceptance"})
    assert (ownership_sentence(entry, titles=TITLES)
            == "You changed the acceptance checks of task T2 (Task Two); "
               "the plan is now at version 10.")


def test_plan_delete_task_reads_deleted_t_from_the_plan():
    entry = _entry("plan_edited", record_ref="pe3", actor=_actor(), task_id="T3",
                   consequence={"kind": "plan_version", "task_ids": ["T3"], "ref": "v11"},
                   detail={"command": "plan_delete_task"})
    assert (ownership_sentence(entry, titles=TITLES)
            == "You deleted task T3 (Task Three) from the plan; the plan is now at version 11.")


def test_plan_split_task_reads_split_t_in_the_plan():
    entry = _entry("plan_edited", record_ref="pe4", actor=_actor(), task_id="T4",
                   consequence={"kind": "plan_version", "task_ids": ["T4"], "ref": "v12"},
                   detail={"command": "plan_split_task"})
    assert (ownership_sentence(entry, titles=TITLES)
            == "You split task T4 (Task Four) in the plan; the plan is now at version 12.")


def test_plan_merge_tasks_reads_merged_tasks_in_the_plan():
    entry = _entry("plan_edited", record_ref="pe5", actor=_actor(),
                   consequence={"kind": "plan_version", "task_ids": [], "ref": "v13"},
                   detail={"command": "plan_merge_tasks"})
    assert (ownership_sentence(entry, titles=TITLES)
            == "You merged tasks in the plan; the plan is now at version 13.")


def test_plan_reorder_reads_reordered_the_plans_tasks():
    entry = _entry("plan_edited", record_ref="pe6", actor=_actor(),
                   consequence={"kind": "plan_version", "task_ids": [], "ref": "v14"},
                   detail={"command": "plan_reorder"})
    assert (ownership_sentence(entry, titles=TITLES)
            == "You reordered the plan's tasks; the plan is now at version 14.")


def test_an_unknown_plan_edit_command_falls_back_and_names_itself():
    """The fallback the block orders: unrecognised `detail["command"]` values still read as
    a sentence, naming the command verbatim, and `version 7` for ref `v7` shows `V`'s leading
    `v` stripped."""
    entry = _entry("plan_edited", record_ref="pe7", actor=_actor(), task_id="T2",
                   consequence={"kind": "plan_version", "task_ids": ["T2"], "ref": "v7"},
                   detail={"command": "task edit T2 --acceptance add"})
    assert (ownership_sentence(entry, titles=TITLES)
            == "You edited the plan (task edit T2 --acceptance add) for task T2 (Task Two); "
               "the plan is now at version 7.")


def test_an_unknown_plan_edit_command_with_no_task_id_omits_the_for_clause():
    entry = _entry("plan_edited", record_ref="pe8", actor=_actor(),
                   consequence={"kind": "plan_version", "task_ids": [], "ref": "v15"},
                   detail={"command": "plan_rename"})
    assert (ownership_sentence(entry, titles=TITLES)
            == "You edited the plan (plan_rename); the plan is now at version 15.")


def test_a_task_edited_entry_drops_the_command_from_the_sentence():
    entry = _entry("task_edited", record_ref="te1", actor=_actor(), task_id="T3",
                   consequence={"kind": "plan_version", "task_ids": ["T3"], "ref": "v8"},
                   detail={"command": "task edit T3 --files add src/x.py"})
    assert (ownership_sentence(entry, titles=TITLES)
            == "You edited task T3 (Task Three) while the job ran; the plan is now at version 8.")


# ---------------------------------------------------------------------------
# S2 — `ownership_view`
# ---------------------------------------------------------------------------


class _StubTask:
    def __init__(self, task_id: str, title: str) -> None:
        self.task_id = task_id
        self.title = title


class _StubJob:
    def __init__(self, job_id: str, tasks: list[_StubTask]) -> None:
        self.job_id = job_id
        self.tasks = tasks


def test_ownership_view_carries_a_sentence_on_every_entry(monkeypatch):
    ledger = _golden_ledger()
    monkeypatch.setattr(
        "packages.orchestration.ownership.build_ownership_ledger", lambda job: ledger)
    job = _StubJob("job-1", [_StubTask(tid, title) for tid, title in TITLES.items()])

    view = ownership_view(job)

    assert view["schema"] == "remedy.ownership.v1"
    assert view["job_id"] == "job-1"
    assert view["error"] == ""
    assert len(view["entries"]) == len(ledger["entries"])
    for raw, rendered in zip(ledger["entries"], view["entries"], strict=True):
        assert rendered["sentence"] == ownership_sentence(raw, titles=TITLES)
        assert rendered["record_ref"] == raw["record_ref"]


def test_ownership_views_error_form(monkeypatch):
    def _raise(_job):
        raise OwnershipError("boom")

    monkeypatch.setattr("packages.orchestration.ownership.build_ownership_ledger", _raise)
    job = _StubJob("job-2", [])

    view = ownership_view(job)

    assert view == {
        "schema": "remedy.ownership.v1",
        "job_id": "job-2",
        "entries": [],
        "error": "The ownership ledger could not be read: boom",
    }
