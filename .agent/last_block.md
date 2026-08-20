── STEP R10 — F255 Teacher role ───────────────────────────────
Goal:        Record the R9 verdict and finish T002 AND T003: `remedy teach
             narrate <job_id>` reads a job's run log through the production
             reader and prints Stage 1 narration, its catalog entry declares
             `action_class="read_only"`, and a behavioural proof shows every
             byte under the data root unchanged across the call.

Bundle:      C0a save this block · C0b mirror it · C1 the plan, FIRST · C2
             record the R9 verdict · C3 the catalog, the handler wiring, the
             command and its tests, together · C4 the handback, then push.

Change:      Exactly these paths, in this order, one commit each.
             C0a `.agent/authored/f255-r10.md`
             C0b `.agent/last_block.md`
             C1  `.agent/plan.md`
             C2  `.agent/live_review.md`
             C3  `apps/cli/command_catalog.py` AND
                 `apps/cli/commands/__init__.py` AND
                 `apps/cli/commands/teach_cmd.py` (CREATED) AND
                 `tests/cli/test_teach_cmd.py` (CREATED) — ONE commit, four
                 files. The catalog BUILDS the parser and the handler table is
                 keyed by its command ids, so any subset declares a command that
                 cannot run or wires a handler nothing dispatches to (R-0151).
             C4  `.agent/handoff.md`
             Nothing else is created, modified, deleted or staged. These paths
             are PRESENT at the base `de0f666b` and must stay untouched:
             `packages/orchestration/teacher_narration.py`,
             `packages/orchestration/timeline.py`,
             `packages/orchestration/run_log.py`,
             `packages/orchestration/data_paths.py`,
             `packages/orchestration/role_config.py`,
             `packages/orchestration/config.py`, `apps/cli/grouped.py`,
             `docs/agents/teacher_conventions.md`,
             `docs/roadmap/features/T5_F255.md`, `.agent/decisions.md`,
             `.agent/context.md`, `AGENTS.md`.

Constraints:
1. NO SLICE IS EDITED. Every text between `<<<SLICE x` and `<<<END x` is applied
   byte for byte. A slice you believe is wrong is applied anyway and DECLARED in
   the handback; you never repair it silently. Marker lines never reach a target.
2. TRANSPORT. `.remedy-wt/f255-r10.md` is this block on disk. C0a copies that
   FILE to `.agent/authored/f255-r10.md` — copy it, never retype it — and C0b
   copies the same file to `.agent/last_block.md`. Prove all three byte-EQUAL;
   the reviewer stated the expected digest when it delegated, and that digest
   cannot appear in this file because this file is what it digests.
3. THE PLAN COMES FIRST. Findings R-0377, R-0491 and R-0548 are OPEN and all
   rule that the `.agent/plan.md` update is the FIRST substantive commit of a
   round with substance to record.
4. FOUR PAIRS, AND THEIR SHAPES DIFFER. The reviewer ran the containment test
   over each before emission and quotes each result as the test printed it.
   GROUPFROM→GROUPTO: `TO contains FROM: True` — APPEND-shaped.
   ENTRYFROM→ENTRYTO: `True` — APPEND-shaped. IMPORTFROM→IMPORTTO: `False` —
   REWRITE. MERGEFROM→MERGETO: `False` — REWRITE. G7 orders the FROM-zero count
   for the two REWRITES ONLY, and never for the two appends, whose FROM the
   applied file necessarily still carries (§4.9, R-0207).
5. EVERY FROM IS UNIQUE IN ITS TARGET. The reviewer measured each of the four
   FROM texts at exactly 1 occurrence in its file at the base. Apply each by a
   count-checked replacement: assert the FROM occurs exactly once BEFORE
   replacing, and stop if it does not.
6. THE TWO CREATED FILES MUST NOT EXIST AT THE BASE. Report both as ABSENT at
   `de0f666b` before C3 and PRESENT after; if either exists already, stop.
7. THE LEDGER APPEND IS BLANK-SEPARATED. RECORDR9 at C2 is appended preceded by
   exactly one blank line (R-0578). This round registers NO finding and resolves
   none: the registered count stays 181 and the resolved count stays 3. The
   `resolved` reading is the count of LINE-ANCHORED `Done:` paragraphs — named
   here because R9 had to derive it, and constraint 8 forbids you writing one.
8. YOU NEVER WRITE A `Done:` OR A `Landed:` PARAGRAPH.
9. NOTHING ELSE IS BUILT. No Stage 2, no `remedy teach ask`, no level dial, no
   grounding-source labelling, no ledger reader. Those are T004's.
10. `.agent/STOP` is read from disk before C0a. If it exists, stop and write the
   handback instead.
11. `git status --porcelain` is EMPTY after every commit. No worktree is created
   this round: the reviewer already ran every destructive control G9 reports.
12. YOU DO NOT WAIT ON ANY CI RUN and you report no run's conclusion.

<<<SLICE PLAN255R10
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
R10: record the R9 verdict and finish T002 and T003 — `remedy teach narrate`
over a real run log, its catalog entry declaring `action_class="read_only"`, and
the behavioural proof that the command changes no byte under the data root.

## Next Steps
1. R11 BUILDS T004, Stage 2 Q&A: `remedy teach ask`, the small context, the
   three grounding sources labelled per answer, the level dial, and spend
   recorded under the role name `teacher`. It is the round that gives
   `teacher.model` its first reader.
2. The INTEGRATION GATE round follows T004 — the full suite, per
   docs/agents/integration_gate.md — because T002 and T003 touch the CLI
   catalog, which the parser and the help renderer both read.
3. The CLOSURE round follows, per docs/roadmap/STATUS_closure_protocol.md:
   evidence job, fresh review zip, the STATUS line, and the pull request.

## Risks
- STAGE 2 IS THE ROUND THAT CAN BREAK THE COST STORY. Stage 1 spends nothing
  because it calls no model; T004 introduces the first teacher model call, and
  its spend must land under the role name `teacher` in the F103 ledger or
  DECISION F255 D3 is unmet.
- THE READ-ONLY PROOF COVERS THE NARRATE PATH ONLY. `remedy teach ask` is a new
  path and needs its own proof; a proof of one command is not a proof of a role.
- THE CATALOG IS SHARED GROUND. `teach` is a new command group the parser and
  the help renderer both build from, so a later round changing its shape re-runs
  their suites, not only the teacher's own.
<<<END PLAN255R10

<<<SLICE RECORDR9
Gate: R10 — the R9 entry. R9 PASSED with NO finding against its work and none against its block. Every gate the R9 block ordered was RE-EXECUTED by the reviewer over `43dc5086..de0f666b` rather than read from the handback, and every one holds. THE TRANSPORT HELD IN THE PRIMARY FORM: `.remedy-wt/f255-r9.md`, the committed `.agent/authored/f255-r9.md` at `ab7e1ddc` and the committed `.agent/last_block.md` at `948a60a5` are byte-EQUAL at sha256 b94ed684d8ff88dba8713f704124a3e54e609d63fb24729cc3b52d2fc2e2c0c0 over 30330 B and 470 lines, the digest stated at delegation. FOUR SLICES, a count the reviewer took from its own ordered extraction of the committed blob, agreeing with the worker's independent count, and NO slice is a FROM or a TO: the round contained no pair, so no containment reading and no FROM-zero count was ordered, owed or reported anywhere in it. THE PLAN LANDED FIRST AGAIN: `.agent/plan.md` at `30bd554c` byte-equals PLAN255R9 at sha256 5ec4ef1ccc2c162eec00b263fd6336853e33cd0d085d9428c0a6728b73b3dd9e over 2795 B and 47 lines, under the 50-line cap, carrying `## Goal` once, `## Next Steps` once and the F-id F255, and `30bd554c` is the first commit after the two block-save commits. THE LEDGER APPEND IS PREFIX-CLEAN: the blob at `43dc5086` is a byte-exact prefix of the blob at `6dfc6dc7` with a 5001 B two-line remainder equal to one newline followed by RECORDR8, and an independent paragraph split of the `6dfc6dc7` blob yields 197 units whose LAST unit is RECORDR8 byte for byte. THE SETS DID NOT MOVE, as a `Gate:` paragraph must not move them: 181 registered / 3 resolved / 178 open / 0 line-anchored `Landed:` at BOTH `43dc5086` and `6dfc6dc7`; `Gate: R9 — the R8 entry.` occurs 1x, sits last among the nine lines beginning `Gate: R`, and all nine header keys are distinct. THE TWO FILES WERE CREATED, NOT EDITED, and each is the authored bytes: `packages/orchestration/teacher_narration.py` and `tests/orchestration/test_teacher_narration.py` are both ABSENT at `43dc5086` under `git ls-tree` and both PRESENT at `1990b8e6`, and each byte-EQUALS its slice — 93 lines and 128 lines, numstat 93/0 and 128/0. STAGE 1 NARRATES AND IT IS DETERMINISTIC, re-measured by the reviewer rather than read from the report: `python3 -m pytest tests/orchestration/test_teacher_narration.py -q -rf` exits 0 at 38 passed, scoped ruff over both created files exits 0 at `All checks passed!`, and narrating the three events `job_created`, `task_run_started` carrying `t7` and `weird_thing` in TWO SEPARATE PROCESSES produces byte-identical output, whose third sentence NAMES `weird_thing` rather than describing it — the honesty rule holding at the only place it can be observed. THE FOUR RED CONTROLS BEHIND G8 WERE RUN BY THE REVIEWER BEFORE DELEGATION, in a disposable worktree since removed: dropping one event from `NARRATED_EVENTS` gives 1 failed / 35 passed, making the unrecognised path raise gives 9 failed / 29 passed, adding a forbidden dependency to the module gives 1 failed / 37 passed, and pointing a template at a field no event carries gives 1 failed / 37 passed — so the enumeration, the honesty path, the zero-cost guard and the templates are each a real tripwire rather than an unfalsifiable assertion. THE NEIGHBOURS AND THE ROUND GATE HOLD, re-run serially in the primary checkout, never two pytest processes at once: the three T001 suites exit 0 at 131 passed, the four state-reader files exit 0 at 160 passed and the canary exits 0 at 42 passed. THE RANGE AND THE HISTORY HOLD: seven paths over six single-parent commits; per-commit insertions 470, 375, 23, 2, 221 and C4's own 33, every one under the 500 cap, with every `+/-` cell of the handback's `## Commits` table byte-identical to `git diff --numstat`; all eleven paths named untouched are PRESENT at the base and ABSENT from the range; zero marker lines in any written file; no trailing whitespace on any handback line; and the handback at `de0f666b` is 75 lines carrying all seven mandated headings in the template's order. THE R-0605 COUNTER-MEASURE HELD A SECOND TIME: the handback states no total for the round anywhere, measured with a pattern rather than by reading, and its reflog claim names `1990b8e6` as the commit the reading was taken at with five commits made at that moment and five prefix-`commit` entries. C4's own entry is recorded here, which is what R-0494 asks of the next gate. ONE DECLARED DEVIATION IS WORTH KEEPING: the R9 block stated the ledger sets as `registered / resolved / open / line-anchored Landed:` without naming the extractor for `resolved`, so the worker measured three candidate readings — 1 for "paragraph contains RESOLVED", 80 for "ends with OPEN.", and 3 for line-anchored `Done:` — chose the only one that reproduces the block's four numbers, and named it. That is the same class the R5 record already keeps as a declared deviation for the two readings of "header key", and it is handled the same way: measured, named, and re-measurable by a later reader. The R10 block names the extractor in its own text so the next worker measures nothing to find it.
<<<END RECORDR9

<<<SLICE GROUPFROM
    "memory": GroupDef("memory", "Memory", "Project memory."),
<<<END GROUPFROM

<<<SLICE GROUPTO
    "memory": GroupDef("memory", "Memory", "Project memory."),
    "teach": GroupDef("teach", "Teach", "Explain a run. Read-only, never steers it."),
<<<END GROUPTO

<<<SLICE ENTRYFROM
    CommandEntry(
        command_id="job.attach-repo",
<<<END ENTRYFROM

<<<SLICE ENTRYTO
    CommandEntry(
        command_id="teach.narrate",
        group_id="teach",
        subcommand="narrate",
        description="Narrate a job's run log in plain sentences (read-only).",
        action_class="read_only",
        args=(_JOB_ID, _JSON_OPT),
        supports_json=True,
        related=("job.show",),
    ),
    CommandEntry(
        command_id="job.attach-repo",
<<<END ENTRYTO

<<<SLICE IMPORTFROM
        status_cmd,
        test_cmds,
<<<END IMPORTFROM

<<<SLICE IMPORTTO
        status_cmd,
        teach_cmd,
        test_cmds,
<<<END IMPORTTO

<<<SLICE MERGEFROM
 bench_cmd, ci_cmd):
<<<END MERGEFROM

<<<SLICE MERGETO
 bench_cmd, ci_cmd, teach_cmd):
<<<END MERGETO

<<<SLICE TEACHCMD
"""`remedy teach narrate <job_id>` — Stage 1 of the teacher role (F255 T002/T003).

The FIRST caller of ``packages.orchestration.teacher_narration`` outside its own
tests. It reads ONE job's run log through the production reader
``packages.orchestration.timeline.load_run_events`` and prints one plain sentence
per event.

READ-ONLY by construction AND by test: this command opens the run log for
reading only, holds no lock, and writes nothing — no run-log entry, no job
record, no cache, no export. ``tests/cli/test_teach_cmd.py`` proves that
behaviourally, by hashing every file under the data root before and after the
call and comparing the two maps.

Remedy deliberately does NOT emit a run-log event for a teach command. A teacher
that logged its own observation would change what the next observer sees, which
is exactly the influence this role is forbidden
(docs/agents/teacher_conventions.md, "Stance").

Zero tokens: narration is a template lookup, so Stage 1 reaches no model and
spends nothing. The teacher's own model key (``teacher.model``) belongs to the
Stage 2 question path and is deliberately not read here.

Exit codes:
* 0 — narrated; an absent or empty run log narrates to nothing and is still 0;
* 1 or 2 — raised by ``resolve_job_id`` itself: an unusable id, or a short
  prefix matching more than one job. This command adds no exit path of its own,
  because a teacher that could fail a run in a new way would not be passive.
"""
from __future__ import annotations


def _cmd_teach_narrate(job_id_str: str, *, json_output: bool = False) -> None:
    """Narrate one job's run log. READ-ONLY: nothing on this path writes."""
    import json as _json

    from packages.orchestration.data_paths import resolve_data_root, resolve_job_id
    from packages.orchestration.teacher_narration import narrate_run_events
    from packages.orchestration.timeline import load_run_events

    job_id = resolve_job_id(job_id_str)
    events = load_run_events(resolve_data_root(), job_id)
    sentences = narrate_run_events(events)

    if json_output:
        print(_json.dumps({
            "job_id": str(job_id),
            "event_count": len(events),
            "narration": sentences,
        }, indent=2))
        return

    print(f"Teacher narration for job {str(job_id)[:8]} ({len(events)} events)")
    if not sentences:
        print("  no events yet")
    for sentence in sentences:
        print(f"  {sentence}")


COMMAND_HANDLERS = {
    "teach.narrate": lambda args: _cmd_teach_narrate(
        getattr(args, "job_id", "") or "",
        json_output=bool(getattr(args, "json", False)),
    ),
}
<<<END TEACHCMD

<<<SLICE TEACHCMDTEST
"""Tests for `remedy teach narrate` — the teacher's Stage 1 surface (F255 T002/T003).

The load-bearing property is T003's: the command is READ-ONLY, proven
BEHAVIOURALLY rather than asserted — every file under the data root is hashed
before and after the call and the two maps must be identical.

Deliberately NOT re-asserted here: the sentences themselves, which
tests/orchestration/test_teacher_narration.py pins at module level, and the
parser wiring, which this round's own gate exercises by running the real
`remedy teach narrate` end to end over a run log.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from apps.cli.command_catalog import get_command, get_commands_for_group
from apps.cli.commands.teach_cmd import COMMAND_HANDLERS, _cmd_teach_narrate

_JOB_ID = "3f2b1a90-0000-4000-8000-000000000001"

_EVENTS = [
    {"event": "job_created", "timestamp": "2026-08-21T00:00:01Z"},
    {"event": "task_run_started", "task_id": "t7", "timestamp": "2026-08-21T00:00:02Z"},
    {"event": "some_unlisted_event", "timestamp": "2026-08-21T00:00:03Z"},
]


def _write_run_log(root: Path, job_id: str, events: list[dict]) -> Path:
    """A run log at the real relative path ``load_run_events`` reads."""
    runs = root / "runs" / job_id
    runs.mkdir(parents=True, exist_ok=True)
    log = runs / "run-1.jsonl"
    log.write_text(
        "\n".join(json.dumps(e, separators=(",", ":")) for e in events) + "\n",
        encoding="utf-8",
    )
    return log


def _hash_tree(root: Path) -> dict[str, str]:
    """Every file under ``root``, mapped to the sha256 of its bytes."""
    return {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


@pytest.fixture()
def data_root(tmp_path, monkeypatch):
    root = tmp_path / "data"
    root.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    return root


class TestTeachNarrateIsReadOnly:
    """T003: the run's files are byte-identical before and after the command."""

    def test_narrating_changes_no_byte_under_the_data_root(self, data_root, capsys):
        _write_run_log(data_root, _JOB_ID, _EVENTS)
        before = _hash_tree(data_root)
        assert before, "the fixture must put at least one file on disk"

        _cmd_teach_narrate(_JOB_ID)
        capsys.readouterr()

        assert _hash_tree(data_root) == before

    def test_narrating_creates_and_removes_no_file(self, data_root, capsys):
        _write_run_log(data_root, _JOB_ID, _EVENTS)
        before = sorted(p.relative_to(data_root) for p in data_root.rglob("*"))
        _cmd_teach_narrate(_JOB_ID)
        capsys.readouterr()
        assert sorted(p.relative_to(data_root) for p in data_root.rglob("*")) == before

    def test_narrating_appends_no_run_log_event(self, data_root, capsys):
        log = _write_run_log(data_root, _JOB_ID, _EVENTS)
        before = log.read_bytes()
        _cmd_teach_narrate(_JOB_ID)
        capsys.readouterr()
        assert log.read_bytes() == before

    def test_a_job_with_no_run_log_writes_nothing_and_says_so(self, data_root, capsys):
        _cmd_teach_narrate(_JOB_ID)
        out = capsys.readouterr().out
        assert "no events yet" in out and "(0 events)" in out
        assert _hash_tree(data_root) == {}


class TestTeachCatalogDeclaration:
    def test_the_command_is_declared_read_only(self):
        cmd = get_command("teach.narrate")
        # T003 declares the action class as well as proving the behaviour: the
        # catalog is what a permission layer reads, and the tests above are what
        # make the declaration true rather than merely stated.
        assert cmd.action_class == "read_only"
        assert cmd.may_mutate_repo is False
        assert cmd.may_execute_commands is False
        assert cmd.requires_permission is False

    def test_the_handler_table_covers_every_declared_teach_command(self):
        declared = {c.command_id for c in get_commands_for_group("teach")}
        assert declared == {"teach.narrate"} == set(COMMAND_HANDLERS)
<<<END TEACHCMDTEST

Done when:
G1 HYGIENE. `.agent/STOP` read from disk before C0a and reported absent or
   present; branch is feature/f255-teacher-role; `git status --porcelain` EMPTY
   after every commit and at the handback; `git worktree list` reports the
   primary checkout alone. No reading is taken by overwriting a file in the
   primary checkout — use `git show <sha>:<path>`.
G2 TRANSPORT. Report the sha256 and the byte and line counts of
   `.remedy-wt/f255-r10.md`, of `.agent/authored/f255-r10.md` at C0a and of
   `.agent/last_block.md` at C0b, and state whether all three are EQUAL.
G3 SLICES EXTRACTED, NEVER RETYPED. Extract each slice from the COMMITTED
   `.agent/authored/f255-r10.md` by its markers and report, for EACH slice the
   block contains, its name, sha256, byte count and line count, naming the
   newline convention used (R-0600). Report the number of slices you found as a
   COUNT YOU TOOK FROM THAT LISTING; this block deliberately states no numeral
   of its own for it (R-0604, checklist item 11).
G4 THE PLAN, FIRST. `.agent/plan.md` at C1 byte-equals PLAN255R10; report its
   sha256, byte and line counts, that the line count is under 50, and that
   `## Goal`, `## Next Steps` and a roadmap F-id all occur in it. Report also
   that C1 is the FIRST commit of this round other than C0a and C0b.
G5 THE R9 VERDICT RECORDED. C2 appends RECORDR9 preceded by exactly one blank
   line. Report the PREFIX property, the remainder's sha256, byte and line
   counts, and that the separator is present. Report a SECOND, independent
   paragraph-level split whose LAST unit is RECORDR9, giving that unit's sha256
   under BOTH newline conventions with the byte count of each, and run a
   negative control — one character of the expected remainder mutated — showing
   BOTH readings reject it. Report registered / resolved / open / line-anchored
   `Landed:` at the base and at C2, using constraint 7's extractors: the
   reviewer measured 181 / 3 / 178 / 0 at `de0f666b`, and C2 owes the same four,
   because a `Gate:` paragraph adds neither kind of line. Report that
   `Gate: R10 — the R9 entry.` occurs 1x, is the LAST line beginning `Gate: R`,
   and repeats no header key.
G6 THE FROM TEXTS WERE UNIQUE, AND THE TWO NEW FILES ARE CREATED. For each of
   the four FROM slices report its occurrence count in its target file at the
   base `de0f666b`; the reviewer measured each at exactly 1, and a count other
   than 1 stops the round. Report, with `git ls-tree`, that
   `apps/cli/commands/teach_cmd.py` and `tests/cli/test_teach_cmd.py` are BOTH
   ABSENT at `de0f666b` and BOTH PRESENT at C3, and that each byte-equals its
   slice — TEACHCMD and TEACHCMDTEST respectively — giving each file's sha256,
   byte count and line count.
G7 THE FOUR PAIRS, BY THEIR OWN SHAPES. For the two REWRITE pairs — IMPORT and
   MERGE — report FROM's count at the base and at C3 and TO's count at both
   ends; each owes FROM 0x and TO 1x after C3. For the two APPEND-shaped pairs —
   GROUP and ENTRY — report FROM 1x at BOTH ends and TO 0x then 1x, and do NOT
   report a FROM-zero count for either: that count is unreachable by
   construction (§4.9, R-0207). Report ALSO, for EACH of the two EDITED files,
   the RECONSTRUCTION: the blob at C3 byte-EQUALS the blob at the base with that
   file's FROM occurrences replaced once each by their TOs, in the block's own
   pair order. Report `git diff --numstat` for all four files at C3.
G8 THE COMMAND RUNS FOR REAL, END TO END — the gate that matters most, because
   docs/agents/reviewer_conventions.md rules that a spec naming a runtime route
   is not accepted until evidence shows that route EXECUTED. In a scratch dir
   under the gitignored `.remedy-wt/`, write a run log at
   `<scratch>/runs/3f2b1a90-0000-4000-8000-000000000001/run-1.jsonl` holding
   three compact JSON lines — `job_created`, `task_run_started` carrying
   `task_id` `t7`, and `mystery` — then with `REMEDY_DATA_DIR` set to that dir
   run
     `python3 -m apps.cli.main teach narrate 3f2b1a90-0000-4000-8000-000000000001`
   and report its exact command, exit code and full stdout. The reviewer
   measured exit 0 and four lines: a header naming 3 events, then
   `The job was created.`, `A task started: t7`, and a third sentence NAMING
   `mystery`. Report ALSO the scratch run log's sha256 unchanged across that
   invocation, and leave `git status --porcelain` empty.
G9 THE READ-ONLY PROOF AND THE CATALOG. Report the exact command, exit code and
   tail of
     `python3 -m pytest tests/cli/test_teach_cmd.py -q -rf`
   at C3. The reviewer measured exit 0 at 6 passed. Do NOT run a mutation
   red-proof: the reviewer already ran three in a disposable worktree before
   emitting this block — making the command append a run-log event gives
   3 failed / 3 passed, making it create one unrelated file under the data root
   gives 3 failed / 3 passed, and changing the teach entry's `action_class` to
   `write_metadata` gives 1 failed against
   `test_the_command_is_declared_read_only` — and constraint 11 forbids you
   creating a worktree.
G10 THE CATALOG'S OWN SUITES, because C3 adds a GROUP and a command the parser
   and the help renderer both build from. Report the exact command, exit code
   and tail of
     `python3 -m pytest tests/test_command_catalog.py tests/test_grouped_cli.py -q -rf`
   at C3. The reviewer measured exit 0 at 529 passed with these bytes.
G11 RUFF, SCOPED TO THE FOUR FILES C3 TOUCHES. Report the exact command, exit
   code and output of
     `python3 -m ruff check apps/cli/command_catalog.py apps/cli/commands/__init__.py apps/cli/commands/teach_cmd.py tests/cli/test_teach_cmd.py`
   at C3; the reviewer measured `All checks passed!`. A base reading is owed for
   the two EDITED files ONLY, taken with no worktree and no overwrite via
   `git show de0f666b:<path> | python3 -m ruff check --stdin-filename <path> -`
   so the path's per-file-ignores resolve (item 29). The two CREATED files are
   ABSENT at the base, so none is owed for them (item 21).
G12 THE ROUND GATE, serially in the PRIMARY checkout, never two pytest processes
   at once. This round rewrites `.agent/` state, so the four state-reader files
   gate alongside the canary and Stage 1's own suite. Report the exact command,
   exit code and tail of each:
     `python3 -m pytest tests/orchestration/test_teacher_narration.py -q -rf`
     `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
     `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
   The reviewer measured exit 0 at 38 passed, exit 0 at 160 passed and exit 0 at
   42 passed, all at `de0f666b` in the primary checkout.
G13 CHANGE SET, HISTORY AND CAPS. Report `git diff --name-only de0f666b..HEAD`
   and state that it equals the Change list with no path on either side alone.
   Report that each of the twelve paths the Change section names as untouched is
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
G14 NO MARKER LEAKED. Report the count of LINES beginning `<<<SLICE ` or
   `<<<END ` in `.agent/plan.md` at C1, `.agent/live_review.md` at C2, all four
   files at C3, and `.agent/handoff.md` at C4. Every count must be 0.
G15 THE PUSH. After C4, `git push` and report its real output. Do NOT create a
   pull request and do NOT wait on the CI run the push starts (constraint 12).

Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
             all seven mandated headings in the template's order, the
             item-status table for the C0a..C4 bundle, the `## Commits` table
             G13 pins, and one LINE per gate rather than its transcript
             (R-0582). The LINE cap your commit count earns is the bound. Its
             `## Next` section names the next session's FIRST action as Phase 1
             rule 1, the `.agent/STOP` re-read, and its SECOND as R11, T004's
             Stage 2 Q&A — `remedy teach ask`, the small context, the three
             grounding sources labelled per answer, the level dial, and spend
             recorded under the role name `teacher` — and states that R10 awaits
             review and that T002 and T003 are complete. There is no open pull
             request. Full transcripts go in the round report, never in the
             file. The handback also carries this Fortschritt line verbatim
             (R-0418):
             Fortschritt: ~60 % (T001, T002 and T003 COMPLETE · `remedy teach
             narrate` runs end to end over a real run log, declared read_only
             and PROVEN read-only byte for byte · T004 Stage 2, the integration
             gate and closure remain) — Schätzung
──────────────────────────────────────────────────────────────
