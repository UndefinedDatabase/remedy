── STEP R9 — F255 Teacher role ────────────────────────────────
Goal:        Record the R8 verdict and BUILD Stage 1 narration: the enumerated
             event set, the deterministic templates and the unrecognised-event
             path, as one new module with its own test file. Nothing here opens
             a file and nothing reaches a model. The `remedy teach` surface and
             T003's behavioural read-only proof are R10's, together, for the
             reason the plan slice states.

Bundle:      C0a save this block · C0b mirror it · C1 the plan, FIRST, ahead of
             the record and ahead of the work · C2 record the R8 verdict · C3
             the narration module and its tests, together · C4 the handback,
             then push.

Change:      Exactly these paths, in this order, one commit each.
             C0a `.agent/authored/f255-r9.md`
             C0b `.agent/last_block.md`
             C1  `.agent/plan.md`
             C2  `.agent/live_review.md`
             C3  `packages/orchestration/teacher_narration.py` (CREATED) AND
                 `tests/orchestration/test_teacher_narration.py` (CREATED) —
                 ONE commit, both files, because a module whose test file
                 arrives in a later commit is a module that was unguarded in
                 the history (R-0151).
             C4  `.agent/handoff.md`
             Nothing else is created, modified, deleted or staged. These paths
             are PRESENT at the base `43dc5086` and must stay untouched:
             `packages/orchestration/role_config.py`,
             `packages/orchestration/role_conventions.py`,
             `packages/orchestration/config.py`,
             `packages/orchestration/timeline.py`,
             `packages/orchestration/run_log.py`,
             `docs/agents/teacher_conventions.md`, `docs/README.md`,
             `docs/roadmap/features/T5_F255.md`, `.agent/decisions.md`,
             `.agent/context.md`, `AGENTS.md`.

Constraints:
1. NO SLICE IS EDITED. Every text between `<<<SLICE x` and `<<<END x` is applied
   byte for byte. A slice you believe is wrong is applied anyway and DECLARED in
   the handback; you never repair it silently. Marker lines never reach a target.
2. TRANSPORT. `.remedy-wt/f255-r9.md` is this block on disk. C0a copies that
   FILE to `.agent/authored/f255-r9.md` — copy it, never retype it — and C0b
   copies the same file to `.agent/last_block.md`. Prove all three byte-EQUAL;
   the reviewer stated the expected digest when it delegated, and that digest
   cannot appear in this file because this file is what it digests.
3. THE PLAN COMES FIRST. Findings R-0377, R-0491 and R-0548 are OPEN and all
   rule that the `.agent/plan.md` update is the FIRST substantive commit of a
   round with substance to record.
4. THERE ARE NO FROM/TO PAIRS THIS ROUND. Every slice is a WHOLE-FILE write or
   an APPEND: PLAN255R9 replaces `.agent/plan.md` entirely, RECORDR8 is appended
   after exactly one blank line, and NARRATION and NARRATIONTEST create two
   files that do not exist at the base. No containment test, no FROM count and
   no FROM-zero reading is ordered or owed anywhere in this block, because no
   pair exists to owe one (§4.9).
5. THE MODULE AND ITS TESTS LAND IN ONE COMMIT (R-0151). C3 creates both files
   at once.
6. THE TWO CREATED FILES MUST NOT EXIST AT THE BASE. Report both as ABSENT at
   `43dc5086` before C3 and PRESENT after; if either already exists, stop.
7. THE LEDGER APPEND IS BLANK-SEPARATED. RECORDR8 at C2 is appended preceded by
   exactly one blank line (R-0578). This round registers NO finding and resolves
   none: the registered count stays 181 and the resolved count stays 3.
8. YOU NEVER WRITE A `Done:` OR A `Landed:` PARAGRAPH.
9. NOTHING ELSE IS BUILT. No CLI command, no `remedy teach` surface, no command
   catalog entry, no read-only behavioural proof, no call to any reader. Those
   are R10's, and the plan slice records why the proof travels with the surface
   rather than with this module.
10. `.agent/STOP` is read from disk before C0a. If it exists, stop and write the
   handback instead.
11. `git status --porcelain` is EMPTY after every commit. No worktree is created
   this round: the reviewer already ran every destructive control G8 reports.
12. YOU DO NOT WAIT ON ANY CI RUN and you report no run's conclusion.

<<<SLICE PLAN255R9
# Plan — F255 Teacher role

Branch: feature/f255-teacher-role, cut from `main` at b35d350b, the merge commit
of pull request #207. No pull request is open for this branch; on this project
the PR is created by the closure round.
`.agent/live_review.md` is the source of truth for the open set, for the next
free finding id and for the round map; this file repeats none of them.

## Goal
A fourth configured role, `teacher`, that narrates a running mission and answers
operator questions about the operator's own code, and never influences the run.
DONE when passive narration keyed to an enumerated set of ledger events (Stage 1,
deterministic templates, zero tokens) and on-demand Q&A (Stage 2, through the
teacher role's own model) both work, the three grounding sources are never mixed
silently, teacher spend is reported as its own role in the F103 ledger, and the
read-only invariant is proven behaviourally.

## Current Step
R9: record the R8 verdict and build Stage 1 narration — the enumerated event
set, the deterministic templates and the unrecognised-event path — as one new
module with its own tests. T001 is complete as of R8.

## Next Steps
1. R10 BUILDS THE SURFACE AND THE PROOF TOGETHER: `remedy teach` printing the
   narration over a real run log through `timeline.load_run_events`, its
   command-catalog entry declaring `action_class="read_only"`, and T003's
   BEHAVIOURAL proof over that command — bytes on disk unchanged across the
   call. T002 and T003 were planned as one round; they are two because the
   module and its tests alone measure 221 lines, and a block carrying the CLI
   surface as well cannot fit the 490-line cap of DECISION F085 D6. The proof
   travels with the SURFACE because the module opens nothing and takes no path,
   so proving it read-only would prove the half that was never at risk.
2. T004, Stage 2 Q&A, follows: the small context, the source labelling, the
   level dial, and spend recorded under the role name `teacher`. It is also the
   round that gives `teacher.model` its first reader.
3. The integration gate and the closure round follow T004, per
   docs/roadmap/STATUS_closure_protocol.md.

## Risks
- STAGE 1 IS ZERO-TOKEN ONLY WHILE NOTHING CALLS A MODEL FROM IT. The module
  built here imports no provider and opens no file, and a test asserts both; if
  a later round routes narration through a model, that test is the tripwire.
- THE READ-ONLY INVARIANT IS NOT YET PROVEN BEHAVIOURALLY. Nothing an operator
  can invoke exists until R10, and this branch's pull request is created by the
  closure round, so no narration reaches an operator before its proof lands.
- NARRATION IS UNDOCUMENTED IN `docs/` UNTIL R10, deliberately: documenting a
  module nobody can call would describe a capability that does not exist.
<<<END PLAN255R9

<<<SLICE RECORDR8
Gate: R9 — the R8 entry. R8 PASSED with NO finding against its work and none against its block. Every gate the R8 block ordered was RE-EXECUTED by the reviewer over `3812d625..43dc5086` rather than read from the handback, and every one holds. THE TRANSPORT HELD IN THE PRIMARY FORM: `.remedy-wt/f255-r8.md`, the committed `.agent/authored/f255-r8.md` at `edbe5081` and the committed `.agent/last_block.md` at `92ae84fd` are byte-EQUAL at sha256 10568c5540165120f2b96d9cf875c99ef1fd9b0a454a4f7701775c3655ee8e12 over 26977 B and 304 lines, the digest stated at delegation. SEVEN SLICES, a count the reviewer took from its own ordered extraction of the committed blob, agreeing with the worker's independent count. THE PLAN LANDED FIRST AGAIN: `.agent/plan.md` at `5970a477` byte-equals PLAN255R8 at sha256 a1d16420f454a4fd98f0e7701e6f943d0269a6c1a77d96f8991dd62a7aaebe55 over 2240 B and 41 lines, under the 50-line cap, carrying `## Goal` once, `## Next Steps` once and the F-id F255, and `5970a477` is the first commit after the two block-save commits. THE TWO LEDGER APPENDS ARE PREFIX-CLEAN: the blob at `3812d625` is a byte-exact prefix of the blob at `7b76bdd4` with a 3597 B two-line remainder equal to one newline followed by R0605, and that blob is a byte-exact prefix of the blob at `2aeec2b0` with a 5380 B two-line remainder equal to one newline followed by RECORDR7; an independent paragraph split of the `2aeec2b0` blob yields 196 units whose LAST unit is RECORDR7 byte for byte. THE SETS MOVED EXACTLY AS ORDERED: 180 registered / 3 resolved / 177 open / 0 line-anchored `Landed:` at `3812d625`, and 181 / 3 / 178 / 0 at both `7b76bdd4` and `2aeec2b0`; `- R-0605 — ` occurs 1x, no id is registered twice, and `Gate: R8 — the R7 entry.` occurs 1x, sits last among the eight lines beginning `Gate: R`, and repeats no header key. THE SOURCE COMMIT WAS RECONSTRUCTED RATHER THAN READ, in the shape G7 ordered after the reviewer had measured that neither a whole-file prefix reading nor an ordered line-by-line reading can hold for a mid-file code append: for BOTH files C4 touches, the blob at `47288467` byte-EQUALS the blob at the base with that file's single FROM occurrence replaced once by its TO — `packages/orchestration/config.py` at sha256 59fd1f2baa09da7fcae0bf44a98ae6a09a01171bbef7ff3767ce0690e5b03988 and `tests/orchestration/test_config.py` at sha256 946ea4a02da52d47d0aa060ebde0a5abc1f1e2c0c232a4d57f32e13fd4551569 — which fixes position and multiplicity together and is independent of how git attributes a hunk. The APPEND-shaped PINFROM→PINTO reads FROM 1x at BOTH ends and no FROM-zero count was ordered or reported for it; the REWRITE CFGFROM→CFGTO reads FROM 1x then 0x and TO 0x then 1x; the numstat is 14/0 and 9/0. THE KEY IS DECLARED AND ITS PIN IS A TRIPWIRE: `python3 -m pytest tests/orchestration/test_config.py -q -rf` exits 0 at 63 passed where the base measured 62, `get_key_spec("teacher.model")` returns a spec whose `.env_var`, `.value_type` and `.default` read `REMEDY_TEACHER_MODEL`, `str` and `None`, and the reviewer's three pre-delegation controls each turned that one pin RED — deleting the spec, renaming the env var, and giving the key a non-None default — at lines 78, 79 and 81 of the test file. THE SUITES WERE RE-RUN SERIALLY BY THE REVIEWER IN THE PRIMARY CHECKOUT, never two pytest processes at once: scoped ruff over both C4 files exits 0 at `All checks passed!`, the T001 neighbours exit 0 at 68 passed, the four state-reader files exit 0 at 160 passed, the canary exits 0 at 42 passed and `tests/docs/` exits 0 at 295 passed. THE RANGE AND THE HISTORY HOLD: seven paths over seven single-parent commits; per-commit insertions 304, 219, 15, 2, 2, 23 and C5's own 36, every one under the 500 cap, with every `+/-` cell of the handback's `## Commits` table byte-identical to `git diff --numstat`; all nine paths named untouched are PRESENT at the base and ABSENT from the range; zero marker lines in any written file; no trailing whitespace on any handback line; and the handback at `43dc5086` is 81 lines carrying all seven mandated headings in the template's order. R-0605'S COUNTER-MEASURE WORKED ON ITS FIRST OUTING, which is worth recording because the round that REGISTERED R-0605 was also the first round bound by it: its G12 ordered the reflog count together with the commit it was taken at and forbade any total for the round, and the handback states no round total anywhere — measured by the reviewer with a pattern over the file rather than by reading it. Re-measured at `43dc5086`, the eight most recent reflog entries all read `commit` in the operation prefix and none contains amend, reset, rebase or cherry, so C5's own entry — the one no round can count for itself — is recorded here, which is what R-0494 asks of the next gate. T001 IS COMPLETE: the teacher has a role name in `KNOWN_ROLES`, a reviewed conventions document loaded as a capped prompt segment, and its own `teacher.model` routing surface.
<<<END RECORDR8

<<<SLICE NARRATION
"""
Teacher narration — Stage 1 of the teacher role (F255 T002).

Turns run-log events into plain sentences an operator can read while a mission
runs. DETERMINISTIC and ZERO-TOKEN by construction: narrating an event is a
lookup in ``NARRATED_EVENTS`` followed by string formatting, so two passes over
the same run log produce byte-identical output and the token ledger records no
call for either.

Remedy deliberately does NOT invent a description for an event outside
``NARRATED_EVENTS``. Run-log event names are free strings and no stable event
vocabulary exists (DECISION F255 D2), so an unrecognised name is narrated AS
unrecognised rather than guessed at — the honesty rule of
docs/agents/teacher_conventions.md applied to this module's own blind spot.

Remedy deliberately opens no file here and provides no writer. The caller
supplies events already read by the production reader
``packages.orchestration.timeline.load_run_events``, which is read-only and
already drops a malformed line rather than repairing it (DECISION F255 D5).
Keeping the read out of this module is what makes the read-only invariant a
property of the whole teacher path rather than a claim about part of it.

Public API::

    NARRATED_EVENTS      — the enumerated Stage 1 set: event name -> template
    UNKNOWN_FIELD        — what an absent template field renders as
    narrate_run_event(event) -> str
    narrate_run_events(events) -> list[str]
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

#: What an absent template field renders as. A narration that RAISED on a
#: missing field could stop a run the teacher is forbidden to touch, and one
#: that invented a value would break the honesty rule; both are worse than a
#: sentence that says plainly which part it does not know.
UNKNOWN_FIELD = "unknown"

#: The enumerated Stage 1 event set, in the order a job lives through them.
#: Each value is a template over the TOP-LEVEL fields of a run-log event
#: (packages/orchestration/run_log.py ``RunEvent``). Adding an entry here is
#: the only way to narrate a new event: that is the point of the enumeration.
NARRATED_EVENTS: dict[str, str] = {
    "job_created": "The job was created.",
    "planning_started": "Planning started.",
    "planning_completed": "Planning finished and produced a task list.",
    "planning_failed": "Planning failed: {message}",
    "workspace_materialized": "The workspace was prepared for this run.",
    "task_run_started": "A task started: {task_id}",
    "task_run_completed": "A task finished: {task_id} (outcome: {outcome})",
    "task_run_failed": "A task failed: {task_id} (outcome: {outcome})",
    "task_run_noop": "A task ran and changed nothing: {task_id}",
    "verification_passed": "Verification passed.",
    "verification_failed": "Verification failed: {message}",
}

#: How an event outside NARRATED_EVENTS is narrated. It names the event rather
#: than describing it, because describing it would be inventing.
UNRECOGNISED_TEMPLATE = "An event this teacher has no narration for: {event}"


class _FieldsWithUnknown(dict):
    """Formatting map that yields :data:`UNKNOWN_FIELD` for absent fields."""

    def __missing__(self, key: str) -> str:
        return UNKNOWN_FIELD


def narrate_run_event(event: Mapping[str, Any]) -> str:
    """Narrate ONE run-log event as a single plain sentence.

    Never raises and never calls a model. An event whose name is missing, is
    not a string, or is absent from :data:`NARRATED_EVENTS` is narrated as
    unrecognised.
    """
    fields = _FieldsWithUnknown(event)
    name = event.get("event")
    if not isinstance(name, str) or name not in NARRATED_EVENTS:
        return UNRECOGNISED_TEMPLATE.format_map(fields)
    return NARRATED_EVENTS[name].format_map(fields)


def narrate_run_events(events: list[Mapping[str, Any]]) -> list[str]:
    """Narrate a run log, one sentence per event, in the order given.

    The caller's order is preserved rather than re-sorted: ``load_run_events``
    already sorts by timestamp, and re-sorting here would silently disagree
    with the reader when a timestamp is missing.
    """
    return [narrate_run_event(event) for event in events]
<<<END NARRATION

<<<SLICE NARRATIONTEST
"""Tests for teacher narration — Stage 1 of the teacher role (F255 T002).

The load-bearing properties are DETERMINISM (two passes are byte-identical),
ZERO COST (no model, no network, no writer) and HONESTY (an event outside the
enumerated set is narrated as unrecognised, never invented and never raised).
"""
from __future__ import annotations

from pathlib import Path

import pytest

from packages.orchestration import teacher_narration
from packages.orchestration.teacher_narration import (
    NARRATED_EVENTS,
    UNKNOWN_FIELD,
    UNRECOGNISED_TEMPLATE,
    narrate_run_event,
    narrate_run_events,
)


def _event(name: str, **fields: object) -> dict[str, object]:
    base: dict[str, object] = {
        "event": name,
        "job_id": "job-1",
        "run_id": "run-1",
        "timestamp": "2026-08-21T00:00:00Z",
    }
    base.update(fields)
    return base


class TestEnumeratedSet:
    @pytest.mark.parametrize("name", sorted(NARRATED_EVENTS))
    def test_every_enumerated_event_narrates_without_the_unrecognised_text(self, name):
        sentence = narrate_run_event(_event(name, task_id="t1", outcome="changed",
                                            message="because"))
        assert sentence
        assert "no narration for" not in sentence

    @pytest.mark.parametrize("name", sorted(NARRATED_EVENTS))
    def test_no_template_leaves_an_unfilled_placeholder(self, name):
        sentence = narrate_run_event(_event(name))
        assert "{" not in sentence and "}" not in sentence

    def test_the_set_holds_the_events_a_job_lives_through(self):
        # Pinned by EXPECTED LITERAL: a test that reads the mapping it is meant
        # to freeze can never fail, however wrong that mapping becomes.
        assert sorted(NARRATED_EVENTS) == [
            "job_created",
            "planning_completed",
            "planning_failed",
            "planning_started",
            "task_run_completed",
            "task_run_failed",
            "task_run_noop",
            "task_run_started",
            "verification_failed",
            "verification_passed",
            "workspace_materialized",
        ]


class TestUnrecognisedEvents:
    @pytest.mark.parametrize("name", ["nope", "builder_completed", ""])
    def test_an_event_outside_the_set_is_narrated_as_unrecognised(self, name):
        assert narrate_run_event(_event(name)) == UNRECOGNISED_TEMPLATE.format(event=name)

    def test_an_unrecognised_event_invents_no_description(self):
        sentence = narrate_run_event(_event("mystery_event"))
        assert "mystery_event" in sentence
        assert sentence == UNRECOGNISED_TEMPLATE.format(event="mystery_event")

    @pytest.mark.parametrize("broken", [{}, {"event": None}, {"event": 7},
                                        {"event": ["not", "a", "string"]}])
    def test_a_malformed_event_never_raises(self, broken):
        assert isinstance(narrate_run_event(broken), str)


class TestMissingFields:
    def test_an_absent_template_field_renders_as_unknown(self):
        sentence = narrate_run_event(_event("task_run_started"))
        assert UNKNOWN_FIELD in sentence

    def test_a_present_field_is_used_verbatim(self):
        sentence = narrate_run_event(_event("task_run_started", task_id="task-42"))
        assert "task-42" in sentence
        assert UNKNOWN_FIELD not in sentence


class TestDeterminism:
    def test_two_passes_over_one_run_log_are_byte_identical(self):
        events = [_event(name, task_id="t1", outcome="changed", message="m")
                  for name in sorted(NARRATED_EVENTS)] + [_event("unlisted")]
        first = narrate_run_events(events)
        second = narrate_run_events(events)
        assert first == second
        assert "\n".join(first).encode() == "\n".join(second).encode()

    def test_the_callers_order_is_preserved(self):
        events = [_event("verification_passed"), _event("job_created")]
        assert narrate_run_events(events) == [
            NARRATED_EVENTS["verification_passed"],
            NARRATED_EVENTS["job_created"],
        ]

    def test_an_empty_run_log_narrates_to_nothing(self):
        assert narrate_run_events([]) == []


class TestZeroCostGuards:
    def test_the_module_reaches_no_model_network_or_writer(self):
        source = Path(teacher_narration.__file__).read_text(encoding="utf-8")
        body = "\n".join(line for line in source.split("\n")
                         if not line.lstrip().startswith("#"))
        for banned in ("requests", "httpx", "socket", "subprocess", "openai",
                       "ollama", "RunLogWriter", "open(", "write_text"):
            assert banned not in body, banned

    def test_narration_needs_no_data_dir_and_opens_nothing(self):
        # The module takes events, never a path: the read stays with the
        # production reader, which is what keeps the teacher read-only.
        import inspect

        for fn in (narrate_run_event, narrate_run_events):
            params = list(inspect.signature(fn).parameters)
            assert params in (["event"], ["events"]), params
<<<END NARRATIONTEST

Done when:
G1 HYGIENE. `.agent/STOP` read from disk before C0a and reported absent or
   present; branch is feature/f255-teacher-role; `git status --porcelain` EMPTY
   after every commit and at the handback; `git worktree list` reports the
   primary checkout alone. No reading is taken by overwriting a file in the
   primary checkout — use `git show <sha>:<path>`.
G2 TRANSPORT. Report the sha256 and the byte and line counts of
   `.remedy-wt/f255-r9.md`, of `.agent/authored/f255-r9.md` at C0a and of
   `.agent/last_block.md` at C0b, and state whether all three are EQUAL.
G3 SLICES EXTRACTED, NEVER RETYPED. Extract each slice from the COMMITTED
   `.agent/authored/f255-r9.md` by its markers and report, for EACH slice the
   block contains, its name, sha256, byte count and line count, naming the
   newline convention used (R-0600). Report the number of slices you found as a
   COUNT YOU TOOK FROM THAT LISTING; this block deliberately states no numeral
   of its own for it (R-0604, checklist item 11).
G4 THE PLAN, FIRST. `.agent/plan.md` at C1 byte-equals PLAN255R9; report its
   sha256, byte and line counts, that the line count is under 50, and that
   `## Goal`, `## Next Steps` and a roadmap F-id all occur in it. Report also
   that C1 is the FIRST commit of this round other than C0a and C0b.
G5 THE R8 VERDICT RECORDED. C2 appends RECORDR8 preceded by exactly one blank
   line. Report the PREFIX property, the remainder's sha256, byte and line
   counts, and that the separator is present. Report a SECOND, independent
   paragraph-level split whose LAST unit is RECORDR8, giving that unit's sha256
   under BOTH newline conventions with the byte count of each, and run a
   negative control — one character of the expected remainder mutated — showing
   BOTH readings reject it. Report registered / resolved / open / line-anchored
   `Landed:` at the base and at C2: the reviewer measured 181 / 3 / 178 / 0 at
   `43dc5086`, and C2 owes the same four, because a `Gate:` paragraph adds
   neither kind of line. Report that `Gate: R9 — the R8 entry.` occurs 1x, is
   the LAST line beginning `Gate: R`, and repeats no header key.
G6 THE TWO FILES ARE CREATED, NOT EDITED. Report, with `git ls-tree`, that
   `packages/orchestration/teacher_narration.py` and
   `tests/orchestration/test_teacher_narration.py` are BOTH ABSENT at
   `43dc5086` and BOTH PRESENT at C3, and that each byte-equals its slice —
   NARRATION and NARRATIONTEST respectively — giving each file's sha256, byte
   count and line count.
G7 NO PAIR PROOF IS OWED. State plainly that this block contains no FROM/TO
   pair, so no containment reading, no FROM count and no FROM-zero count is
   reported for any slice (constraint 4). Report `git diff --numstat` for both
   files at C3.
G8 STAGE 1 NARRATES, DETERMINISTICALLY AND WITHOUT A MODEL. Report the exact
   command, exit code and tail of
     `python3 -m pytest tests/orchestration/test_teacher_narration.py -q -rf`
   at C3. The reviewer measured exit 0 at 38 passed. Report ALSO, from a short
   `python3 -c` you run yourself and run TWICE as two separate processes, the
   narration of three events — `job_created`, `task_run_started` carrying
   `task_id` `t7`, and `weird_thing` — and state whether the two processes'
   output is byte-identical. The reviewer measured it identical, with the third
   sentence NAMING `weird_thing` rather than describing it. Do NOT run a
   mutation red-proof: the reviewer already ran four in a disposable worktree
   before emitting this block — dropping one event from `NARRATED_EVENTS` gives
   1 failed / 35 passed, making the unrecognised path raise gives 9 failed /
   29 passed, adding a forbidden dependency to the module gives 1 failed /
   37 passed, and pointing a template at a field no event carries gives 1 failed
   / 37 passed against `test_the_callers_order_is_preserved` — and constraint 11
   forbids you creating a worktree.
G9 RUFF, SCOPED TO THE TWO CREATED FILES. Report the exact command, exit code
   and output of
     `python3 -m ruff check packages/orchestration/teacher_narration.py tests/orchestration/test_teacher_narration.py`
   at C3. The reviewer measured `All checks passed!` with these bytes. No base
   reading is ordered for these two paths and none is owed: both are ABSENT at
   `43dc5086`, so `ruff` there would exit on a missing file and evaluate no rule
   at all (checklist item 21).
G10 THE NEIGHBOURS T001 BUILT STAY GREEN. Report the exact command, exit code
   and tail of
     `python3 -m pytest tests/orchestration/test_role_config.py tests/orchestration/test_role_conventions.py tests/orchestration/test_config.py -q -rf`
   at C3. The reviewer measured exit 0 at 131 passed with these bytes.
G11 THE ROUND GATE, serially in the PRIMARY checkout, never two pytest processes
   at once. This round rewrites `.agent/` state, so the four state-reader files
   gate alongside the canary. Report the exact command, exit code and tail of
   each:
     `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
     `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
   The reviewer measured exit 0 at 160 passed and exit 0 at 42 passed, both at
   `43dc5086` in the primary checkout.
G12 CHANGE SET, HISTORY AND CAPS. Report `git diff --name-only 43dc5086..HEAD`
   and state that it equals the Change list with no path on either side alone.
   Report that each of the eleven paths the Change section names as untouched is
   PRESENT at the base and absent from the range; that every commit in the range
   has one parent; and each commit's insertion column from `git diff --numstat`,
   every one under 500, with the same `+/-` cells appearing byte-identically in
   the handback's `## Commits` table (checklist item 28). C4's own cell and the
   complete change set belong to the round report.
   THE REFLOG IS REPORTED AS TWO MEASURED CLAIMS, NOT ONE UNIVERSAL (R-0601),
   AND NEITHER IS A TOTAL FOR THE ROUND (R-0605): report the count of this
   round's reflog entries whose OPERATION PREFIX — the text before the first
   colon of `git reflog --format=%gs` — reads exactly `commit`, TOGETHER WITH
   the commit that count was taken at and the number of commits the round has
   made AT THAT MOMENT, and state that those two numbers are equal. Do NOT
   state a total for the round: C4 is not written when this text is composed, so
   its own entry cannot be counted here, and the reviewer measures it at the
   next gate (R-0494). Report also the count whose prefix contains `amend`,
   `reset`, `rebase` or `cherry`, which must be 0.
G13 NO MARKER LEAKED. Report the count of LINES beginning `<<<SLICE ` or
   `<<<END ` in `.agent/plan.md` at C1, `.agent/live_review.md` at C2, both
   created files at C3, and `.agent/handoff.md` at C4. Every count must be 0.
G14 THE PUSH. After C4, `git push` and report its real output. Do NOT create a
   pull request and do NOT wait on the CI run the push starts (constraint 12).

Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
             all seven mandated headings in the template's order, the
             item-status table for the C0a..C4 bundle, the `## Commits` table
             G12 pins, and one LINE per gate rather than its transcript
             (R-0582). The LINE cap your commit count earns is the bound. Its
             `## Next` section names the next session's FIRST action as Phase 1
             rule 1, the `.agent/STOP` re-read, and its SECOND as R10 — the
             `remedy teach` surface, its command-catalog `action_class` entry
             and T003's behavioural read-only proof, together — and states that
             R9 awaits review. There is no open pull request. The full
             transcripts go in the round report you return, never in the file.
             The handback also carries this Fortschritt line verbatim, because
             with no relay you never see the operator brief that would otherwise
             state it (R-0418):
             Fortschritt: ~45 % (T001 COMPLETE · Stage 1 narration BUILT:
             eleven enumerated events, deterministic templates, an honest
             unrecognised path · the CLI surface and the read-only proof are
             R10 · T004 open) — Schätzung
──────────────────────────────────────────────────────────────
