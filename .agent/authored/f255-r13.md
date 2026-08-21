── STEP R13 — F255 Teacher role ───────────────────────────────
Goal:        Rule how a teacher question is billed, amend the ledger module's own
             text so the ruling and the module agree on disk, and build the ONE
             writer that records the row. This round calls NO model: the model
             call is R14, over this seam.

Bundle:      C0a save this block · C0b mirror it · C1 the plan, FIRST · C2 record
             the R12 verdict · C3 DECISION F255 D7 · C4 the ledger docstring pair
             · C5 the spend writer and its test · C6 the handback, then push.

Change:      Exactly these paths, in this order, one commit each.
             C0a `.agent/authored/f255-r13.md`
             C0b `.agent/last_block.md`
             C1  `.agent/plan.md`
             C2  `.agent/live_review.md`
             C3  `.agent/decisions.md`
             C4  `packages/orchestration/token_ledger.py`
             C5  `packages/orchestration/teacher_spend.py` (new) AND
                 `tests/orchestration/test_teacher_spend.py` (new) — ONE commit,
                 because a guard and the code it pins must not land apart.
             C6  `.agent/handoff.md`
             Nothing else is created, modified, deleted or staged. These paths are
             PRESENT at the base `8d8e7a5c` and must stay untouched:
             `packages/orchestration/teacher_qa.py`,
             `packages/orchestration/teacher_narration.py`,
             `apps/cli/commands/teach_cmd.py`, `apps/cli/command_catalog.py`.

Constraints:
1. NO SLICE IS EDITED. Every text between the SLICE and END markers is applied
   byte for byte. A slice you believe is wrong is applied anyway and DECLARED in
   the handback; you never repair it silently. Marker lines never reach a target.
2. TRANSPORT. `.remedy-wt/f255-r13.md` is this block on disk. C0a copies that
   FILE to `.agent/authored/f255-r13.md` — copy it, never retype it — and C0b
   copies the same file to `.agent/last_block.md`. Prove all three byte-EQUAL;
   the reviewer stated the expected digest when it delegated, and that digest
   cannot appear in this file because this file is what it digests.
3. THE PLAN COMES FIRST. Findings R-0377, R-0491 and R-0548 are OPEN and all rule
   that the `.agent/plan.md` update is the FIRST substantive commit of a round
   with substance to record.
4. THE ONE PAIR IS A REWRITE, classified by a containment test the reviewer ran
   on these final bytes rather than by eye (R-0508, R-0522). Its output was
   `TO contains FROM: false`, and REWRITE is derived from that output, so the
   FROM-zero count IS owed (§4.9). LEDGERFROM occurs exactly 1x in
   `packages/orchestration/token_ledger.py` at `8d8e7a5c`, a substring count the
   reviewer took over that blob.
5. THE CODE FILES C5 CREATES ARE CREATED, NOT EDITED, and ABSENT at `8d8e7a5c`.
   §4.9's per-line count binds PROSE only; for a CODE slice the obligation is
   ORDERED EQUALITY (R-0531), which G8 states.
6. THE APPENDS ARE BLANK-SEPARATED (R-0578): RECORDR12 at C2 and
   DECISION255D7 at C3 are each preceded by exactly one blank line. This round
   registers NO finding and resolves none — registered stays 181, resolved 3.
7. YOU NEVER WRITE A `Done:` OR A `Landed:` PARAGRAPH.
8. `.agent/STOP` is read from disk before C0a. If it exists, stop and write the
   handback instead.
9. `git status --porcelain` is EMPTY after every commit. Any destructive check
   runs ONLY inside a disposable worktree under the gitignored `.remedy-wt/`,
   removed before the handback; the primary checkout is never mutated to take a
   reading — use `git show <sha>:<path>`.
10. YOU DO NOT WAIT ON ANY CI RUN and you report no run's conclusion.

<<<SLICE PLAN255R13
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
R13: the BILLING half of T004. It rules how a teacher question is recorded
(DECISION F255 D7), amends `token_ledger`'s own module text so the ruling and the
module do not disagree on disk, and builds the one writer that records the row.
It calls NO model: the model call is R14, over this seam.

## Next Steps
1. R14 FINISHES T004, the model half of Stage 2: `remedy teach ask` on the CLI
   over `teacher_qa.build_teacher_context`, the teacher model call through
   `resolve_role_config("teacher")`, the honest refusal when no model is
   configured, and the spend row written through `teacher_spend`.
2. The INTEGRATION GATE round follows T004 — the full suite, per
   docs/agents/integration_gate.md — because T002 and T003 touch the CLI
   catalog, which the parser and the help renderer both read.
3. The CLOSURE round follows, per docs/roadmap/STATUS_closure_protocol.md:
   evidence job, fresh review zip, the STATUS line, and the pull request.

## Risks
- T004 WAS RESLICED INTO TWO ROUNDS by the reviewer at R13, because the billing
  ruling and the model call did not fit one block under the 490-line cap. The
  feature file's T004 is unchanged; only the round boundary moved.
- R14 IS WHERE THE COST STORY IS PROVEN OR LOST. R13 records a row from figures
  it is GIVEN; R14 must produce real ones from a real call, or D3 is unmet.
- THE READ-ONLY PROOF COVERS NARRATE ONLY; `teach ask` needs its own, and the
  ledger row R13 introduces is a WRITE that proof must exclude by name.
<<<END PLAN255R13
<<<SLICE RECORDR12
Gate: R13 — the R12 entry. R12 PASSED with NO finding against its work and none against its block. R12 was a RECORD round that built nothing, and every gate its block ordered was RE-EXECUTED by the reviewer over `da8c2e3f..8d8e7a5c` rather than read from the handback; every one holds and every number below is the reviewer's own. THE TRANSPORT HELD IN THE PRIMARY FORM: `.remedy-wt/f255-r12.md`, the committed `.agent/authored/f255-r12.md` at `fc3cd2e4` and the committed `.agent/last_block.md` at `cbb727d3` are byte-EQUAL at sha256 d7fa8558af635d879f9b540888d44aed37450fda5430babd16967eede99830bb over 17520 B and 176 lines, the digest stated at delegation. TWO SLICES, a count taken from the reviewer's own ordered extraction of the committed blob and agreeing with the worker's independent count: PLAN255R12 at sha256 8aca9b4c5f4a21cb1002abc1a1c3d7346b4bcf72c63d5501e91d458eb9f66f0e over 2380 B and 42 lines, and RECORDR11 at sha256 69d7956dffb82702a15c3e1ea2df48ad7f1578f7f4c77ad820e9213ae02b97f5 over 6106 B and 1 line, newline convention NEWLINE-INCLUDED. NEITHER slice is a FROM or a TO — the round contained no pair, so no containment reading and no FROM-zero count was ordered, owed or reported anywhere in it. THE PLAN LANDED FIRST AGAIN: `.agent/plan.md` at `938a861c` byte-equals PLAN255R12 at that same digest over 2380 B and 42 lines, under the 50-line cap, carrying `## Goal` once, `## Next Steps` once and the F-id F255, and it is the first commit after the two block-save commits. THE LEDGER APPEND IS PREFIX-CLEAN: the blob at `da8c2e3f` is a byte-exact prefix of the blob at `057146c4` with a 6107 B two-line remainder at sha256 0934102a3bd14ec22f985bf3d87ee9357c9fcc048c82d76f5d25ee507c30239a equal to one newline followed by RECORDR11, and the byte after that newline is not a newline, so the separator is exactly one blank line. An INDEPENDENT line-wise blank-line paragraph split of the `057146c4` blob yields 200 units whose LAST unit is RECORDR11 byte for byte, at newline-INCLUDED sha256 69d7956dffb82702a15c3e1ea2df48ad7f1578f7f4c77ad820e9213ae02b97f5 over 6106 B and newline-EXCLUDED sha256 7b61248f301a4149a9b1bd9da60f8370ca9cca59a5a8c2a3b71f0f02127440bf over 6105 B; a one-character mutant of the expected remainder is REJECTED by the prefix reading and by both paragraph readings, while the real blob is accepted by all three. THE SETS DID NOT MOVE, as a `Gate:` paragraph must not move them: 181 registered / 3 resolved / 178 open / 0 line-anchored `Landed:` at BOTH `da8c2e3f` and `057146c4`; `Gate: R12 — the R11 entry.` occurs 1x, sits last among the twelve lines beginning `Gate: R`, and all twelve header keys are distinct. THE ROUND GATE HOLDS, re-run serially by the reviewer in the primary checkout, never two pytest processes at once: the four state-reader files exit 0 at 160 passed and the canary exits 0 at 42 passed — the same 160 and 42 the R12 block stated. THE RANGE AND THE HISTORY HOLD: five paths over five single-parent commits, all five under `.agent/`; per-commit insertions 176, 72, 12, 2 and 25, every one under the 500 cap; each `+/-` cell of the handback's `## Commits` table is byte-identical to `git diff --numstat`; all four paths the block named untouched are PRESENT at `da8c2e3f` and ABSENT from the range; and zero lines beginning `<<<SLICE ` or `<<<END ` appear in any of the three written files. THE HANDBACK ITSELF MEASURES CLEAN: 60 lines at `8d8e7a5c`, exactly at the 60-line cap its five-commit table earns, with no trailing whitespace on any line and all seven mandated headings present in the order docs/agents/handback_template.md gives them. C3'S OWN REFLOG ENTRY IS MEASURED HERE, which is what R-0494 asks of the next gate and what R12 correctly declined to state for itself: at `8d8e7a5c` the round has made 5 commits and its reflog entries whose operation prefix reads exactly `commit` number 5, with 0 entries whose prefix contains amend, reset, rebase or cherry. THE PUSH LANDED: `origin/feature/f255-teacher-role` resolves to `8d8e7a5c`, the same commit the branch holds. FIVE OF RECORDR11'S OWN NUMBERS WERE SPOT-CHECKED RATHER THAN TRUSTED, because a `Gate:` paragraph is permanent and R12's whole value is that paragraph: `.agent/authored/f255-r11.md` at `153b78fd` and `.agent/last_block.md` at `b9b1ce9d` are byte-equal at sha256 d4e511dd4060b29e26f1331ee6eeb0c888abec01e04fe7f3681aea4fae07f5de over 31058 B and 490 lines; `.agent/plan.md` at `948f57de` is sha256 a8d22168cfc33e52a9f488082670cb24348bb203802b2aaef1fa84313057fda5 over 2350 B and 42 lines; `packages/orchestration/teacher_qa.py` and `tests/orchestration/test_teacher_qa.py` are both ABSENT at `c6c6fb08` and at `18083ea7` measure 151 lines at sha256 abe69cac625362f6067a2e491ced9b6a613cab7c293d2ce0831e905adc126d09 and 113 lines at sha256 208a9417619372ca27d1d07fa1aa0b034c99eb3ad87a15809f06f6c34c00f063; the R11 handback at `da8c2e3f` is 74 lines; and the sets read 181 / 3 / 178 / 0 at both `c6c6fb08` and `8271d828`. Every one of the five reproduces exactly, so the R11 entry directly above this one is sound as well as applied.
<<<END RECORDR12
<<<SLICE DECISION255D7
## DECISION F255 D7 — a teacher question is a ledger row with a NULL task_id (2026-08-21)

CONTEXT. F255's acceptance requires Stage 2 to record exactly one ledger call
attributed to role `teacher`, and DECISION F255 D3 rules that teacher spend is
REPORTED through the `role` column the F103 ledger already carries. But
`packages/orchestration/token_ledger.py` states two invariants that such a write
breaks as written, both read at `8d8e7a5c`: a row is ONE FINALIZED TASK RUN keyed
`"<job_id>:<task_id>"` (DECISION D16), and the module has exactly ONE call site,
`pingpong_evidence.write_evidence_bundle`, because it never parses provider
output itself. A teacher question is neither a task nor a run, and it has no
`task_runs/<task_id>/provider_evidence.json`.

CHOSEN. Widen the row's identity by exactly one class rather than fabricate a
task run: a teacher question is a row whose `task_id` is NULL, and that NULL is
what MARKS the class. The schema already permits it — `job_id` and `task_id` are
both nullable and `call_id` alone is the primary key — so no migration is needed.
`packages/orchestration/teacher_spend.py` is the one writer, it takes no
`task_id` parameter at all, and it parses no provider output: it records figures
its caller was given. The `token_ledger` docstring is amended at C4 of the same
round, so the ruling and the module never disagree on disk.

ALTERNATIVES CONSIDERED and rejected. Giving the question a synthetic
`<job_id>:<task_id>` identity so the existing seam takes it unchanged — rejected
because it invents exactly the ids and the evidence file the actuals path exists
to refuse, and it would make a question indistinguishable from a task run in
every later query. Giving teacher spend its own table — rejected because D3
already rules that the separation IS the `role` column, and `query_cost(by=
"role")` would then answer a question that omits the teacher entirely.

CONSEQUENCE. `query_cost(by="role")` reports a `teacher` bucket beside the
mission roles with no change to that function. A NULL `task_id` now READS as
"not a task run"; every row that has one keeps its D16 meaning untouched.

Reverse this decision by deleting this section, deleting
`packages/orchestration/teacher_spend.py` and its test, and restoring the two
amended bullets of the `token_ledger` module docstring.
<<<END DECISION255D7
<<<SLICE LEDGERFROM
* Remedy deliberately does NOT add a second capture path. This module records
  what the existing actuals path already produced; it never parses a provider
  response itself: the usage counters come from ``token_truth``'s existing
  extractor rather than from a second parse of provider output. Its ONE call
  site is the seam where actuals are finalized
  (``pingpong_evidence.write_evidence_bundle``), where it is opt-in and stays
  inert until a caller names a ledger target.
* Remedy deliberately does NOT store one row per HTTP request. A ROW IS ONE
  FINALIZED TASK RUN, keyed ``"<job_id>:<task_id>"`` (DECISION D16, recorded on
  the feature file): ``task_runs/<task_id>/provider_evidence.json`` is the
  finest record the actuals feature puts on disk, and a per-request row would
  have to invent ids, timestamps and a usage split no file records. F115 D4 adds
  ``call_segments`` BESIDE it rather than widening it — one row per segment of
  one composed prompt, keyed by the row's ``call_id`` plus the trace line's
  position — so the per-call breakdown lives in its own table and ``calls``
  keeps its one-row-per-task-run identity untouched.
<<<END LEDGERFROM
<<<SLICE LEDGERTO
* Remedy deliberately does NOT add a second ACTUALS capture path. This module
  records what the existing actuals path already produced; it never parses a
  provider response itself: the usage counters come from ``token_truth``'s
  existing extractor rather than from a second parse of provider output. That
  seam is ``pingpong_evidence.write_evidence_bundle``, where it is opt-in and
  stays inert until a caller names a ledger target. DECISION F255 D7 adds the
  one OTHER writer, ``teacher_spend.record_teacher_question``, which is not an
  actuals path either: it records figures its caller was GIVEN and parses no
  provider output at all.
* Remedy deliberately does NOT store one row per HTTP request. A ROW IS ONE
  FINALIZED TASK RUN, keyed ``"<job_id>:<task_id>"`` (DECISION D16, recorded on
  the feature file): ``task_runs/<task_id>/provider_evidence.json`` is the
  finest record the actuals feature puts on disk, and a per-request row would
  have to invent ids, timestamps and a usage split no file records. F115 D4 adds
  ``call_segments`` BESIDE it rather than widening it — one row per segment of
  one composed prompt, keyed by the row's ``call_id`` plus the trace line's
  position — so the per-call breakdown lives in its own table and ``calls``
  keeps its one-row-per-task-run identity untouched. DECISION F255 D7 widens
  that identity by exactly ONE class: a teacher question is a row whose
  ``task_id`` is NULL, because it has no task run to name and inventing one is
  the fabrication the sentence above refuses. A NULL ``task_id`` therefore READS
  as "not a task run"; every row that has one keeps the D16 meaning untouched.
<<<END LEDGERTO
<<<SLICE TEACHSPEND
"""
Teacher spend — the ledger row one answered teacher question produces (F255 T004).

Stage 2 calls a model, so Stage 2 costs money, and DECISION F255 D3 rules that
teacher spend is REPORTED through the ``role`` column the F103 ledger already
carries rather than capped by a new budget axis. This module is the one place
that builds such a row, so no caller assembles a ``CallRecord`` of its own.

WHY THIS IS NOT THE ACTUALS PATH: DECISION F255 D7, which states the argument in
full. In short, ``token_ledger`` documents a row as one FINALIZED TASK RUN keyed
``"<job_id>:<task_id>"``; a teacher question is neither, so D7 widens that
identity by one class — a NULL ``task_id`` MARKS the teacher row — rather than
invent the task id and the evidence file the actuals path exists to refuse.

Remedy deliberately records NULL counts rather than zeros when a reply reports no
usage, matching ``token_ledger``'s own rule: a fabricated zero is worse than an
honest unknown, because a zero sums and an unknown does not.

Public API:: ``TEACHER_ROLE``, ``TeacherUsage``, ``record_teacher_question``.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from packages.orchestration.token_ledger import (
    COST_BASIS_PROVIDER_REPORTED,
    COST_BASIS_UNKNOWN,
    CallRecord,
    record_call,
)

#: The role name teacher spend is attributed to. Spelled once here so the ledger
#: row, the query that reports it and the tests cannot drift apart.
TEACHER_ROLE = "teacher"


@dataclass(frozen=True)
class TeacherUsage:
    """What one teacher reply reported about its own cost.

    Every field is optional because a provider that reports nothing must land as
    NULL. There is no default of zero anywhere in this class.
    """

    tokens_in: int | None = None
    tokens_out: int | None = None
    cost_usd: float | None = None


def record_teacher_question(
    *,
    model: str,
    usage: TeacherUsage | None = None,
    job_id: str | None = None,
    path: Path | str | None = None,
    project_id: str | None = None,
    call_id: str | None = None,
    ts_utc: str | None = None,
) -> tuple[str, bool]:
    """Record ONE ledger row for ONE answered teacher question.

    Returns the row's ``call_id`` and whether it is durable. Never raises:
    ``record_call`` already absorbs every failure, and a teacher that could break
    a run by failing to bill itself would not be the passive role F255 specifies.

    ``task_id`` is deliberately NOT a parameter: it is always NULL, and making it
    settable would let a caller disguise a question as a task run (F255 D7).
    """
    reported = usage or TeacherUsage()
    record = CallRecord(
        call_id=call_id or f"teacher:{uuid.uuid4()}",
        job_id=job_id,
        task_id=None,
        role=TEACHER_ROLE,
        model=model,
        ts_utc=ts_utc or datetime.now(timezone.utc).isoformat(),
        tokens_in=reported.tokens_in,
        tokens_out=reported.tokens_out,
        cost_usd=reported.cost_usd,
        cost_basis=(
            COST_BASIS_PROVIDER_REPORTED
            if reported.cost_usd is not None
            else COST_BASIS_UNKNOWN
        ),
    )
    return record.call_id, record_call(record, project_id=project_id, path=path)
<<<END TEACHSPEND
<<<SLICE TEACHSPENDTEST
"""Teacher spend lands as ONE ledger row per question, attributed to the role.

These pin DECISION F255 D7 — a teacher question is not a finalized task run, so
its row carries a NULL ``task_id`` and that NULL is the mark of the class — and
the acceptance criterion that ``query_cost(by="role")`` reports teacher spend
separately from mission spend. No network and no model: the writer records
figures it is GIVEN, so every property here is observable offline.
"""

from __future__ import annotations

import sqlite3

from packages.orchestration.teacher_spend import (
    TEACHER_ROLE,
    TeacherUsage,
    record_teacher_question,
)
from packages.orchestration.token_ledger import (
    COST_BASIS_PROVIDER_REPORTED,
    COST_BASIS_UNKNOWN,
    CallRecord,
    query_cost,
    record_call,
)


def _rows(ledger):
    """Every stored row, as dicts, read straight from SQLite."""
    conn = sqlite3.connect(ledger)
    try:
        conn.row_factory = sqlite3.Row
        return [dict(r) for r in conn.execute("SELECT * FROM calls ORDER BY call_id")]
    finally:
        conn.close()


def test_one_question_writes_one_row_with_a_null_task_id(tmp_path):
    ledger = tmp_path / "ledger.sqlite3"

    call_id, durable = record_teacher_question(
        model="teacher-model", job_id="job-1", path=ledger
    )

    assert durable is True
    rows = _rows(ledger)
    assert len(rows) == 1
    assert rows[0]["call_id"] == call_id
    assert rows[0]["role"] == TEACHER_ROLE
    assert rows[0]["job_id"] == "job-1"
    assert rows[0]["task_id"] is None


def test_unreported_usage_lands_as_null_never_zero(tmp_path):
    ledger = tmp_path / "ledger.sqlite3"

    record_teacher_question(model="teacher-model", path=ledger)

    row = _rows(ledger)[0]
    assert row["tokens_in"] is None
    assert row["tokens_out"] is None
    assert row["cost_usd"] is None
    assert row["cost_basis"] == COST_BASIS_UNKNOWN


def test_reported_cost_carries_the_provider_reported_basis(tmp_path):
    ledger = tmp_path / "ledger.sqlite3"

    record_teacher_question(
        model="teacher-model",
        usage=TeacherUsage(tokens_in=12, tokens_out=3, cost_usd=0.004),
        path=ledger,
    )

    row = _rows(ledger)[0]
    assert row["tokens_in"] == 12
    assert row["tokens_out"] == 3
    assert row["cost_usd"] == 0.004
    assert row["cost_basis"] == COST_BASIS_PROVIDER_REPORTED


def test_two_questions_are_two_rows(tmp_path):
    ledger = tmp_path / "ledger.sqlite3"

    first, _ = record_teacher_question(model="teacher-model", path=ledger)
    second, _ = record_teacher_question(model="teacher-model", path=ledger)

    assert first != second
    assert len(_rows(ledger)) == 2


def test_query_cost_by_role_reports_teacher_separately(tmp_path):
    ledger = tmp_path / "ledger.sqlite3"
    record_call(
        CallRecord(
            call_id="job-1:task-1",
            job_id="job-1",
            task_id="task-1",
            role="builder",
            model="mission-model",
            ts_utc="2026-08-21T00:00:00+00:00",
            tokens_in=100,
            cost_basis=COST_BASIS_UNKNOWN,
        ),
        path=ledger,
    )
    record_teacher_question(
        model="teacher-model", usage=TeacherUsage(tokens_in=12), path=ledger
    )

    buckets = {row.bucket: row for row in query_cost(path=ledger, by="role").rows}

    assert set(buckets) == {"builder", TEACHER_ROLE}
    assert buckets[TEACHER_ROLE].calls == 1
    assert buckets[TEACHER_ROLE].tokens_in == 12
    assert buckets["builder"].tokens_in == 100
<<<END TEACHSPENDTEST

Done when:
G1 HYGIENE. `.agent/STOP` read from disk before C0a and reported absent or
   present; branch is feature/f255-teacher-role; `git status --porcelain` EMPTY
   after every commit and at the handback; `git worktree list` reported.
G2 TRANSPORT. Report the sha256 and the byte and line counts of
   `.remedy-wt/f255-r13.md`, of `.agent/authored/f255-r13.md` at C0a and of
   `.agent/last_block.md` at C0b, and state whether all three are EQUAL.
G3 SLICES EXTRACTED, NEVER RETYPED. Extract each slice from the COMMITTED
   `.agent/authored/f255-r13.md` by its markers and report each slice's name,
   sha256, byte count and line count, naming the newline convention (R-0600).
   Report the number of slices as a COUNT YOU TOOK FROM THAT LISTING; this block
   states no numeral of its own for it (R-0604, checklist item 11).
G4 THE PLAN, FIRST. `.agent/plan.md` at C1 byte-equals PLAN255R13; report its
   sha256, byte and line counts, that the line count is under 50, and that
   `## Goal`, `## Next Steps` and a roadmap F-id all occur in it. Report also
   that C1 is the FIRST commit of this round other than C0a and C0b.
G5 THE R12 VERDICT RECORDED. Over `.agent/live_review.md`, report: the base blob
   at `8d8e7a5c` is a byte-exact PREFIX of the C2 blob; the remainder's sha256,
   byte and line counts; the byte after its leading newline is not a newline; a
   SECOND, INDEPENDENT paragraph split of the C2 blob whose LAST unit is
   RECORDR12, with that unit's sha256 under BOTH newline conventions and each
   byte count; and a negative control — one character of the expected remainder
   mutated — that BOTH readings reject. Report registered / resolved / open /
   line-anchored `Landed:` at the base and at C2: the reviewer measured
   181 / 3 / 178 / 0 at `8d8e7a5c` and C2 owes the same four, a `Gate:` paragraph
   adding neither kind of line. Report that `Gate: R13 — the R12 entry.` occurs
   1x, is the LAST line beginning `Gate: R`, and repeats no key.
G6 THE DECISION RECORDED. Report the SAME prefix, remainder and separator
   readings G5 names, over `.agent/decisions.md` at C3, and report that
   `## DECISION F255 D7` occurs 0x at `8d8e7a5c` and 1x at C3 with every line
   beginning `## DECISION ` in that file distinct.
G7 THE PAIR. In `packages/orchestration/token_ledger.py`: LEDGERFROM occurs 1x
   at `8d8e7a5c` and 0x at C4; LEDGERTO occurs 0x at `8d8e7a5c` and 1x at C4.
   Report the file's line count at both commits and its numstat for C4. This is
   the FROM-zero proof constraint 4 says is owed.
G8 THE CODE, BY ORDERED EQUALITY (R-0531). For EACH file C5 creates: report
   that `git ls-tree 8d8e7a5c -- <path>` is EMPTY; that the blob at C5
   byte-EQUALS its slice, with sha256, byte and line counts; and that the lines
   C5's diff ADDS for that path are exactly that slice's lines IN ORDER. Report
   each path's numstat cell.
G9 THE ROUND GATE. Run these serially in the PRIMARY checkout, never two pytest
   processes at once, and report the exact command, exit code and tail of each:
     `python3 -m pytest tests/orchestration/test_teacher_spend.py -q -rf`
     `python3 -m pytest tests/orchestration/test_token_ledger.py -q -rf`
     `python3 -m pytest tests/test_path_utils.py tests/test_data_paths.py tests/orchestration/test_autonomy.py -q -rf`
     `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
     `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
     `python3 -m ruff check packages/orchestration/token_ledger.py packages/orchestration/teacher_spend.py tests/orchestration/test_teacher_spend.py`
   At `8d8e7a5c` the reviewer measured 112, 132, 160 and 42 passed and ruff
   `All checks passed!` over the ruff paths that resolve there; the new test does
   NOT exist at the base, so G8's ls-tree emptiness is its base evidence.
G10 CHANGE SET, HISTORY AND CAPS. Report `git diff --name-only 8d8e7a5c..HEAD`
   and state that it equals the Change list with no path on either side alone.
   Report that each path the Change section names untouched is PRESENT at the
   base and absent from the range; that every commit in the range has one parent;
   and each commit's insertion column from `git diff --numstat`, every one under
   500, with the same `+/-` cells appearing byte-identically in the handback's
   `## Commits` table (checklist item 28). C6's own cell and the complete change
   set belong to the round report.
   THE REFLOG IS TWO MEASURED CLAIMS, NOT ONE UNIVERSAL (R-0601), AND NEITHER IS
   A TOTAL (R-0605): report the count of this round's reflog entries whose
   OPERATION PREFIX — the text before the first colon of
   `git reflog --format=%gs` — reads exactly `commit`, WITH the commit it was
   taken at and the number of commits the round has made AT THAT MOMENT, and
   state that the two are equal. State no total: C6 is unwritten as this is
   composed, so the reviewer measures its entry at the next gate (R-0494). Report
   also the count whose prefix contains `amend`, `reset`, `rebase` or `cherry`,
   which must be 0.
G11 NO MARKER LEAKED. Report the count of LINES beginning with the SLICE or END
   marker prefixes in every file this round writes other than
   `.agent/authored/f255-r13.md` and `.agent/last_block.md`. Every count is 0.
G12 THE PUSH. After C6, `git push` and report its real output. Do NOT create a
   pull request and do NOT wait on the CI run the push starts (constraint 10).

Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
             all seven mandated headings in the template's order, the item-status
             table for the C0a..C6 bundle, the `## Commits` table G10 pins, and
             one LINE per gate rather than its transcript (R-0582). Its `## Next`
             section names the next session's FIRST action as Phase 1 rule 1, the
             `.agent/STOP` re-read, and its SECOND as R14, which finishes T004 —
             `remedy teach ask` on the CLI, the teacher model call, the honest
             refusal with no model configured, and the spend row written through
             `teacher_spend`. It states that R12 PASSED and its verdict is now ON
             DISK at C2, that R13 awaits review, and that no pull request is
             open. Transcripts go in the round report. The handback carries this
             Fortschritt line verbatim (R-0418):
             Fortschritt: ~80 % (T001, T002 and T003 COMPLETE · T004 split in two
             by the reviewer at R13 — the billing ruling and the spend writer
             land here, the model call and the CLI at R14 · integration gate and
             closure remain) — Schätzung
──────────────────────────────────────────────────────────────
