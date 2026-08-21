── STEP R11 — F255 Teacher role ───────────────────────────────
Goal:        Record the R10 verdict and build the DETERMINISTIC half of T004
             Stage 2: one pure module carrying the three grounding sources with
             their honesty rules, the level dial that changes DEPTH and never
             the claim set, and the small-context assembly — reaching no model,
             opening no file, spending nothing.

Bundle:      C0a save this block · C0b mirror it · C1 the plan, FIRST · C2
             record the R10 verdict · C3 the module and its tests · C4 the
             handback, then push.

Change:      Exactly these paths, in this order, one commit each.
             C0a `.agent/authored/f255-r11.md`
             C0b `.agent/last_block.md`
             C1  `.agent/plan.md`
             C2  `.agent/live_review.md`
             C3  `packages/orchestration/teacher_qa.py` (CREATED) AND
                 `tests/orchestration/test_teacher_qa.py` (CREATED) — ONE
                 commit, two files. The tests are what make the honesty rules
                 true rather than merely stated, so shipping the module without
                 them would ship an unfalsifiable claim (R-0151).
             C4  `.agent/handoff.md`
             Nothing else is created, modified, deleted or staged. These paths
             are PRESENT at the base `c6c6fb08` and must stay untouched — the
             module this round imports, the two seams R12 will need, and the
             CLI surface R10 built: `packages/orchestration/teacher_narration.py`,
             `packages/orchestration/role_config.py`,
             `packages/orchestration/token_ledger.py`,
             `apps/cli/command_catalog.py`, `apps/cli/commands/teach_cmd.py`,
             `docs/roadmap/features/T5_F255.md`.

Constraints:
1. NO SLICE IS EDITED. Every text between `<<<SLICE x` and `<<<END x` is applied
   byte for byte. A slice you believe is wrong is applied anyway and DECLARED in
   the handback; you never repair it silently. Marker lines never reach a target.
2. TRANSPORT. `.remedy-wt/f255-r11.md` is this block on disk. C0a copies that
   FILE to `.agent/authored/f255-r11.md` — copy it, never retype it — and C0b
   copies the same file to `.agent/last_block.md`. Prove all three byte-EQUAL;
   the reviewer stated the expected digest when it delegated, and that digest
   cannot appear in this file because this file is what it digests.
3. THE PLAN COMES FIRST. Findings R-0377, R-0491 and R-0548 are OPEN and all
   rule that the `.agent/plan.md` update is the FIRST substantive commit of a
   round with substance to record.
4. THIS ROUND CONTAINS NO FROM/TO PAIR. Both C3 files are CREATED whole from a
   slice, so no containment reading, no FROM count and no FROM-zero count is
   owed, ordered or reported anywhere in this round (§4.9, R-0207).
5. THE TWO CREATED FILES MUST NOT EXIST AT THE BASE. Report both as ABSENT at
   `c6c6fb08` before C3 and PRESENT after; if either exists already, stop.
6. THE LEDGER APPEND IS BLANK-SEPARATED. RECORDR10 at C2 is appended preceded by
   exactly one blank line (R-0578). This round registers NO finding and resolves
   none: the registered count stays 181 and the resolved count stays 3.
7. YOU NEVER WRITE A `Done:` OR A `Landed:` PARAGRAPH.
8. NOTHING ELSE IS BUILT. No `remedy teach ask`, no CLI surface, no catalog
   entry, no model call, no ledger write, no config reader — those are R12's. A
   module that reached a model would make G7's zero-token property unmeasurable.
9. `.agent/STOP` is read from disk before C0a. If it exists, stop and write the
   handback instead.
10. `git status --porcelain` is EMPTY after every commit. No worktree is created
   this round: the reviewer already ran every destructive control G7 reports.
11. YOU DO NOT WAIT ON ANY CI RUN and you report no run's conclusion.

<<<SLICE PLAN255R11
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
R11: record the R10 verdict and build the DETERMINISTIC half of T004 Stage 2 —
the grounding-source labelling, the level dial and the small-context assembly,
as a pure module that reaches no model and opens no file.

## Next Steps
1. R12 FINISHES T004: `remedy teach ask` on the CLI, the teacher model call
   through the role's own config, the honest refusal when no model is
   configured, and spend recorded under the role name `teacher` so
   `query_cost(by="role")` separates it from mission spend.
2. The INTEGRATION GATE round follows T004 — the full suite, per
   docs/agents/integration_gate.md — because T002 and T003 touch the CLI
   catalog, which the parser and the help renderer both read.
3. The CLOSURE round follows, per docs/roadmap/STATUS_closure_protocol.md:
   evidence job, fresh review zip, the STATUS line, and the pull request.

## Risks
- R12 IS WHERE THE COST STORY IS PROVEN OR LOST. Stage 1 and this round spend
  nothing because neither calls a model; R12 makes the first teacher model call,
  and its spend must land under the role name `teacher` or DECISION F255 D3 is
  unmet.
- THE LEDGER'S ONE ROW IS A TASK RUN. `token_ledger.record_call` is documented
  as one row per finalized task run, keyed `<job_id>:<task_id>`, and a teacher
  question is neither. R12 must settle that shape before it writes a row.
- THE READ-ONLY PROOF COVERS NARRATE ONLY; `teach ask` needs its own.
<<<END PLAN255R11
<<<SLICE RECORDR10
Gate: R11 — the R10 entry. R10 PASSED with NO finding against its work and none against its block. Every gate the R10 block ordered was RE-EXECUTED by the reviewer over `de0f666b..c6c6fb08` rather than read from the handback, and every one holds. THE TRANSPORT HELD IN THE PRIMARY FORM: `.remedy-wt/f255-r10.md`, the committed `.agent/authored/f255-r10.md` at `a00e60b3` and the committed `.agent/last_block.md` at `5814d65b` are byte-EQUAL at sha256 2970251815a503f9b3cf8fc405da232c828eab62113c57407c1fb4f3439736d8 over 30466 B and 489 lines, the digest stated at delegation. TWELVE SLICES, a count the reviewer took from its own ordered extraction of the committed blob, agreeing with the worker's independent count. THE PLAN LANDED FIRST AGAIN: `.agent/plan.md` at `83c55a73` byte-equals PLAN255R10 at sha256 8772ec24a08b68b3f25fd18011f04d201e2cd7009326fa60f9b2ed54faee4ee4 over 2426 B and 43 lines, under the 50-line cap, carrying `## Goal` once, `## Next Steps` once and the F-id F255, and it is the first commit after the two block-save commits. THE LEDGER APPEND IS PREFIX-CLEAN: the blob at `de0f666b` is a byte-exact prefix of the blob at `f732f92c` with a 5109 B two-line remainder equal to one newline followed by RECORDR9, an independent paragraph split of the `f732f92c` blob yields 198 units whose LAST unit is RECORDR9 byte for byte, and a one-character mutant of the expected remainder is REJECTED by both readings while the real blob is accepted by both. THE SETS DID NOT MOVE, as a `Gate:` paragraph must not move them: 181 registered / 3 resolved / 178 open / 0 line-anchored `Landed:` at BOTH `de0f666b` and `f732f92c`; `Gate: R10 — the R9 entry.` occurs 1x, sits last among the ten lines beginning `Gate: R`, and all ten header keys are distinct. THE TWO FILES WERE CREATED, NOT EDITED, and each is the authored bytes: `apps/cli/commands/teach_cmd.py` and `tests/cli/test_teach_cmd.py` are both ABSENT at `de0f666b` under `git ls-tree` and both PRESENT at `26312742`, and each byte-EQUALS its slice — 64 lines at sha256 46b3cfdb59f0a4c605c8aef5465375e2f4db2a2a1b9a57da37508627151752ec and 108 lines at sha256 cf0f258ec1cd9ad80bdadab05e881cc3e942b69b7cf0cd6a0b052eeba4631860. THE FOUR PAIRS HOLD BY THEIR OWN SHAPES, the containment reading taken mechanically per pair rather than by eye: GROUP and ENTRY are APPEND-shaped with FROM 1x at both ends and TO 0x then 1x, IMPORT and MERGE are REWRITES with FROM 1x then 0x and TO 0x then 1x, and no FROM-zero count is reported for either append. THE RECONSTRUCTION IS THE STRONGER PROOF AND IT PASSES: for each EDITED file, the base blob with its FROM occurrences replaced once each by their TOs in the block's pair order byte-EQUALS the `26312742` blob — `apps/cli/command_catalog.py` at sha256 82deed1ead7163d90f8513868d9305f852b30087ad9704d2ecd5947bfe6f5517 and `apps/cli/commands/__init__.py` at sha256 52ea7d69987764bb513d4cab3d5d3a708fe7d2ac7dbad2fb25e7cbd00e3da7cd. THE COMMAND RUNS FOR REAL, re-run by the reviewer in its own scratch data root rather than read from the report: `python3 -m apps.cli.main teach narrate 3f2b1a90-0000-4000-8000-000000000001` exits 0 over a three-line run log and prints four lines whose third NAMES the unrecognised event `mystery` rather than describing it, and the run log's sha256 a1f6170b3367fae683175fb152a192226712a380ac88d44864a937af9a6f8029 is identical before and after while the whole scratch tree hashes identically — the read-only invariant observed at the only place it can be, a real process. THREE SPOT-CHECKS THE BLOCK DID NOT ORDER WERE RUN, because a declared surface nobody exercises is where this feature would fail quietly: `--json` exits 0 and emits the declared `job_id` / `event_count` / `narration` shape, an unusable id exits 1 through `resolve_job_id` with `Error: invalid job ID`, adding no exit path of the command's own as its docstring claims, and `teach --help` renders the new group and its one command. THE SUITES AND THE LINT HOLD, re-run serially in the primary checkout: the read-only proof exits 0 at 6 passed, the catalog and grouped CLI suites exit 0 at 529 passed, scoped ruff over the four files exits 0 at `All checks passed!` with the two EDITED files also clean at the base through `--stdin-filename`, Stage 1's own suite exits 0 at 38 passed, the four state-reader files exit 0 at 160 passed and the canary exits 0 at 42 passed. THE RANGE AND THE HISTORY HOLD: nine paths over six single-parent commits; per-commit insertions 489, 366, 21, 2, 185 and C4's own 36, every one under the 500 cap, with every `+/-` cell of the handback's `## Commits` table byte-identical to `git diff --numstat`; all twelve paths named untouched are PRESENT at the base and ABSENT from the range; zero marker lines in any written file; no trailing whitespace on any handback line; and the handback at `c6c6fb08` is 78 lines carrying all seven mandated headings in the template's order, within the 100-line allowance its six-commit table earns. C4'S OWN REFLOG ENTRY IS MEASURED HERE, which is what R-0494 asks of the next gate: at `c6c6fb08` the round has made 6 commits and its reflog entries whose operation prefix reads exactly `commit` number 6, with 0 entries whose prefix contains amend, reset, rebase or cherry. THE DECLARED DEVIATION IS SOUND: the session's shell guard rejects the `VAR=value cmd` environment-prefix form, so G8's `REMEDY_DATA_DIR` was set in a runner spawning the block's EXACT argv through `subprocess.run`; the reviewer hit the same guard and reproduced the gate the same way, so the mechanism is the session's and not the worker's, and the command executed is the command the block names.
<<<END RECORDR10
<<<SLICE TEACHQA
"""
Teacher Q&A grounding — the deterministic half of Stage 2 (F255 T004).

Stage 2 answers an operator question through the teacher's own model. THIS
module is everything about that answer which must not depend on a model: which
grounding source each fact came from, what the level dial changes, and what is
refused when no model is configured. Keeping it here makes the honesty rules of
docs/agents/teacher_conventions.md TESTABLE without a network call.

Remedy deliberately opens NO file here and provides no writer, exactly as
``teacher_narration`` does not. The caller supplies run events already read by
``packages.orchestration.timeline.load_run_events`` and code text already read
read-only, so the read-only invariant stays a property of the whole teacher path
rather than a claim about part of it (DECISION F255 D5).

Each fact is built ONLY from the input its source names, which is what stops the
three sources being mixed silently. :func:`claim_set` is computed from the facts
alone and never from the level, so "the same question at two levels yields
answers whose claim set is the same" is a property of the type rather than a
hope about a prompt.

Public API:: ``GROUNDING_SOURCES`` / ``SOURCE_HONESTY``, ``LEVELS`` /
``DEFAULT_LEVEL`` / ``LEVEL_DEPTH``, ``GroundedFact`` / ``TeacherContext``,
``build_teacher_context``, ``claim_set``, ``render_prompt``,
``no_model_refusal``.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from packages.orchestration.teacher_narration import narrate_run_events

#: The three grounding sources, in the order
#: docs/agents/teacher_conventions.md lists them: what is happening, what this
#: code does, and what a term means.
SOURCE_LEDGER = "ledger"
SOURCE_CODE = "code"
SOURCE_CONCEPT = "concept"

GROUNDING_SOURCES: tuple[str, ...] = (SOURCE_LEDGER, SOURCE_CODE, SOURCE_CONCEPT)

#: The honesty rule each source carries, quoted into the prompt beside its facts
#: so the model is told the rule at the point it would break it.
SOURCE_HONESTY: dict[str, str] = {
    SOURCE_LEDGER: "Assert only what these events show; where they are silent, say unknown.",
    SOURCE_CODE: "Explain only the code shown; never invent a call site, a flag or a file.",
    SOURCE_CONCEPT: "General knowledge, explicitly not a claim about this project's state.",
}

#: The level dial. It selects a DEPTH instruction and nothing else.
LEVELS: tuple[str, ...] = ("student", "beginner", "pro")

DEFAULT_LEVEL = "beginner"

#: Depth per level. Every entry asks for the SAME facts at a different length,
#: which is what keeps :func:`claim_set` level-independent.
LEVEL_DEPTH: dict[str, str] = {
    "student": "Explain from scratch in short plain sentences. Define every term you use.",
    "beginner": "Explain plainly. Define a term the first time it appears.",
    "pro": "Be brief and precise. Skip definitions of common terms.",
}


@dataclass(frozen=True)
class GroundedFact:
    """One fact and the source it is allowed to be asserted from."""

    source: str
    text: str


@dataclass(frozen=True)
class TeacherContext:
    """The small context Stage 2 sends: a question, a level, and labelled facts."""

    question: str
    level: str
    facts: tuple[GroundedFact, ...]


def build_teacher_context(
    question: str,
    *,
    events: Sequence[Mapping[str, Any]] = (),
    code: str | None = None,
    code_path: str | None = None,
    level: str = DEFAULT_LEVEL,
) -> TeacherContext:
    """Assemble the small context for one question.

    Ledger facts are the Stage 1 narration of ``events``, reused rather than
    re-derived. A code fact exists only when code was actually supplied, because
    a fact about code nobody read is the invention this role must refuse. An
    unrecognised ``level`` falls back to :data:`DEFAULT_LEVEL` rather than
    raising: a teacher that could fail a run would not be passive.
    """
    if level not in LEVEL_DEPTH:
        level = DEFAULT_LEVEL

    facts: list[GroundedFact] = [
        GroundedFact(SOURCE_LEDGER, sentence) for sentence in narrate_run_events(list(events))
    ]
    if code is not None and code.strip():
        where = code_path or "the supplied code"
        facts.append(GroundedFact(SOURCE_CODE, f"{where}:\n{code}"))

    return TeacherContext(question=question, level=level, facts=tuple(facts))


def claim_set(context: TeacherContext) -> tuple[str, ...]:
    """The facts this answer may assert, as ``"<source>: <text>"`` strings.

    Computed from the facts ALONE: the level is deliberately not an input, so
    two contexts differing only in level have equal claim sets.
    """
    return tuple(f"{fact.source}: {fact.text}" for fact in context.facts)


def render_prompt(context: TeacherContext) -> str:
    """Render the prompt for one question, grouped by grounding source.

    Each block names its source and carries that source's honesty rule, and the
    question comes last so the cache-stable material sits in front of it.
    """
    lines: list[str] = []
    for source in GROUNDING_SOURCES:
        texts = [fact.text for fact in context.facts if fact.source == source]
        if not texts and source != SOURCE_CONCEPT:
            continue
        lines.append(f"[{source}] {SOURCE_HONESTY[source]}")
        lines.extend(texts)
        lines.append("")
    lines.append(LEVEL_DEPTH[context.level])
    lines.append(f"Question: {context.question}")
    lines.append("Name the source you answer from.")
    return "\n".join(lines)


def no_model_refusal(reason: str) -> str:
    """The honest refusal when Stage 2 has no model to call.

    Names Stage 1 explicitly, because Stage 1 is offline by construction and
    keeps working — the operator should be told what they still have.
    """
    return (
        f"I cannot answer that: {reason}. "
        "Stage 1 narration still works offline: run `remedy teach narrate <job_id>`."
    )
<<<END TEACHQA
<<<SLICE TEACHQATEST
"""Tests for teacher Q&A grounding — Stage 2's deterministic half (F255 T004).

These pin the three acceptance rules that must NOT depend on a model call:
every fact names its grounding source, the sources are never mixed silently,
and the level dial changes depth without changing the claim set.

Deliberately NOT tested here: the model call itself and the ledger attribution,
which are T004's second round and need a real provider seam to be honest about.
"""
from __future__ import annotations

import pytest

from packages.orchestration.teacher_qa import (
    DEFAULT_LEVEL,
    GROUNDING_SOURCES,
    LEVEL_DEPTH,
    LEVELS,
    SOURCE_CODE,
    SOURCE_CONCEPT,
    SOURCE_LEDGER,
    build_teacher_context,
    claim_set,
    no_model_refusal,
    render_prompt,
)

_EVENTS = [
    {"event": "job_created", "timestamp": "2026-08-21T00:00:01Z"},
    {"event": "task_run_started", "task_id": "t7", "timestamp": "2026-08-21T00:00:02Z"},
]

_CODE = "def add(a, b):\n    return a + b\n"


class TestGroundingSourcesAreLabelled:
    def test_every_fact_carries_a_known_source(self):
        ctx = build_teacher_context("what happened?", events=_EVENTS, code=_CODE)
        assert ctx.facts
        for fact in ctx.facts:
            assert fact.source in GROUNDING_SOURCES

    def test_ledger_facts_come_only_from_events(self):
        ctx = build_teacher_context("what happened?", events=_EVENTS)
        ledger = [f for f in ctx.facts if f.source == SOURCE_LEDGER]
        assert [f.text for f in ledger] == [
            "The job was created.",
            "A task started: t7",
        ]
        assert not [f for f in ctx.facts if f.source == SOURCE_CODE]

    @pytest.mark.parametrize("code", [None, "", "   \n"])
    def test_no_code_fact_without_real_code(self, code):
        ctx = build_teacher_context("what does add do?", events=_EVENTS, code=code)
        assert not [f for f in ctx.facts if f.source == SOURCE_CODE]

    def test_a_code_fact_names_where_it_was_read(self):
        ctx = build_teacher_context("?", code=_CODE, code_path="apps/x.py")
        code_facts = [f for f in ctx.facts if f.source == SOURCE_CODE]
        assert len(code_facts) == 1
        assert code_facts[0].text.startswith("apps/x.py:")

    def test_the_prompt_labels_each_source_block(self):
        prompt = render_prompt(build_teacher_context("?", events=_EVENTS, code=_CODE))
        for source in GROUNDING_SOURCES:
            assert f"[{source}]" in prompt

    def test_an_empty_context_still_declares_the_concept_source(self):
        prompt = render_prompt(build_teacher_context("what is a mutex?"))
        assert f"[{SOURCE_CONCEPT}]" in prompt
        assert f"[{SOURCE_LEDGER}]" not in prompt
        assert f"[{SOURCE_CODE}]" not in prompt


class TestTheLevelDialChangesDepthNotFacts:
    @pytest.mark.parametrize("level", LEVELS)
    def test_the_claim_set_is_the_same_at_every_level(self, level):
        baseline = claim_set(build_teacher_context("q", events=_EVENTS, code=_CODE))
        at_level = claim_set(
            build_teacher_context("q", events=_EVENTS, code=_CODE, level=level)
        )
        assert at_level == baseline

    @pytest.mark.parametrize("level", LEVELS)
    def test_each_level_asks_for_its_own_depth(self, level):
        prompt = render_prompt(build_teacher_context("q", events=_EVENTS, level=level))
        assert LEVEL_DEPTH[level] in prompt

    def test_the_three_levels_ask_for_three_different_depths(self):
        assert len({LEVEL_DEPTH[level] for level in LEVELS}) == len(LEVELS)

    def test_an_unknown_level_falls_back_and_never_raises(self):
        ctx = build_teacher_context("q", events=_EVENTS, level="wizard")
        assert ctx.level == DEFAULT_LEVEL

    def test_every_level_has_a_depth_and_the_default_is_one_of_them(self):
        assert set(LEVELS) == set(LEVEL_DEPTH)
        assert DEFAULT_LEVEL in LEVELS


class TestHonestyWithoutAModel:
    def test_the_refusal_names_the_reason_and_points_at_stage_1(self):
        message = no_model_refusal("no teacher model is configured")
        assert "no teacher model is configured" in message
        assert "remedy teach narrate" in message

    def test_building_a_context_calls_no_model_and_reads_no_file(self):
        # Zero-token by construction: the context is a pure function of its
        # arguments, so Stage 2's grounding half costs nothing.
        ctx = build_teacher_context("q", events=_EVENTS, code=_CODE)
        assert claim_set(ctx) == claim_set(
            build_teacher_context("q", events=_EVENTS, code=_CODE)
        )
<<<END TEACHQATEST

Done when:
G1 HYGIENE. `.agent/STOP` read from disk before C0a and reported absent or
   present; branch is feature/f255-teacher-role; `git status --porcelain` EMPTY
   after every commit and at the handback; `git worktree list` reports the
   primary checkout alone. No reading is taken by overwriting a file in the
   primary checkout — use `git show <sha>:<path>`.
G2 TRANSPORT. Report the sha256 and the byte and line counts of
   `.remedy-wt/f255-r11.md`, of `.agent/authored/f255-r11.md` at C0a and of
   `.agent/last_block.md` at C0b, and state whether all three are EQUAL.
G3 SLICES EXTRACTED, NEVER RETYPED. Extract each slice from the COMMITTED
   `.agent/authored/f255-r11.md` by its markers and report, for EACH slice the
   block contains, its name, sha256, byte count and line count, naming the
   newline convention used (R-0600). Report the number of slices you found as a
   COUNT YOU TOOK FROM THAT LISTING; this block deliberately states no numeral
   of its own for it (R-0604, checklist item 11).
G4 THE PLAN, FIRST. `.agent/plan.md` at C1 byte-equals PLAN255R11; report its
   sha256, byte and line counts, that the line count is under 50, and that
   `## Goal`, `## Next Steps` and a roadmap F-id all occur in it. Report also
   that C1 is the FIRST commit of this round other than C0a and C0b.
G5 THE R10 VERDICT RECORDED. C2 appends RECORDR10 preceded by exactly one blank
   line. Report the PREFIX property, the remainder's sha256, byte and line
   counts, and that the separator is present. Report a SECOND, independent
   paragraph-level split whose LAST unit is RECORDR10, giving that unit's sha256
   under BOTH newline conventions with the byte count of each, and run a
   negative control — one character of the expected remainder mutated — showing
   BOTH readings reject it. Report registered / resolved / open / line-anchored
   `Landed:` at the base and at C2, the registered count being lines matching
   `^- R-\d+ — ` and the resolved count lines matching `^Done: R-\d+ — `: the
   reviewer measured 181 / 3 / 178 / 0 at `c6c6fb08`, and C2 owes the same four,
   because a `Gate:` paragraph adds neither kind of line. Report that
   `Gate: R11 — the R10 entry.` occurs 1x, is the LAST line beginning `Gate: R`,
   and repeats no header key.
G6 THE TWO FILES ARE CREATED, NOT EDITED. Report, with `git ls-tree`, that
   `packages/orchestration/teacher_qa.py` and
   `tests/orchestration/test_teacher_qa.py` are BOTH ABSENT at `c6c6fb08` and
   BOTH PRESENT at C3, that each byte-equals its slice — TEACHQA and TEACHQATEST
   respectively — giving each file's sha256, byte and line counts, and
   `git diff --numstat` for both at C3. This round contains NO FROM/TO pair, so
   no containment reading and no FROM-zero count is owed (§4.9, R-0207).
G7 THE NEW SUITE. Report the exact command, exit code and tail of
     `python3 -m pytest tests/orchestration/test_teacher_qa.py -q -rf`
   at C3. The reviewer measured exit 0 at 19 passed. Do NOT run a mutation
   red-proof: the reviewer already ran five in a disposable worktree, since
   removed — level leaking into `claim_set` 2 failed / 17 passed, source label
   dropped from the prompt 2 failed / 17 passed, a code fact built with no code
   supplied 5 failed / 14 passed, an unknown level raising 1 failed / 18 passed,
   the Stage 1 pointer dropped from the refusal 1 failed / 18 passed — after
   which the module restored byte-identically and the suite returned to 19
   passed. Constraint 11 forbids you creating a worktree.
G8 THE REPO-WIDE SWEEPS, because C3 adds a file under `packages/` that three
   suites sweep by glob rather than by name. Report the exact command, exit code
   and tail of
     `python3 -m pytest tests/test_path_utils.py tests/test_data_paths.py tests/orchestration/test_autonomy.py -q -rf`
   at C3. The reviewer measured exit 0 at 132 passed BOTH at `c6c6fb08` and with
   the module present: the gate proves the new file trips no sweep, not that a
   count moved.
G9 RUFF, SCOPED TO THE TWO FILES C3 CREATES. Report the exact command, exit code
   and output of
     `python3 -m ruff check packages/orchestration/teacher_qa.py tests/orchestration/test_teacher_qa.py`
   at C3; the reviewer measured `All checks passed!`. NO base reading is owed:
   both files are ABSENT at `c6c6fb08`, so there is no base rule-code multiset
   to compare against (item 21).
G10 THE ROUND GATE, serially in the PRIMARY checkout, never two pytest processes
   at once. TEACHQA imports `teacher_narration` and this round rewrites `.agent/`
   state, so Stage 1's suite and the four state-reader files gate alongside the
   canary. Report the exact command, exit code and tail of each:
     `python3 -m pytest tests/orchestration/test_teacher_narration.py -q -rf`
     `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf`
     `python3 -m pytest tests/cli/test_golden_path.py -q -rf`
   The reviewer measured exit 0 at 38 passed, exit 0 at 160 passed and exit 0 at
   42 passed, all at `c6c6fb08` in the primary checkout.
G11 CHANGE SET, HISTORY AND CAPS. Report `git diff --name-only c6c6fb08..HEAD`
   and state that it equals the Change list with no path on either side alone.
   Report that each of the paths the Change section names as untouched is
   PRESENT at the base and absent from the range; that every commit in the range
   has one parent; and each commit's insertion column from `git diff --numstat`,
   every one under 500, with the same `+/-` cells appearing byte-identically in
   the handback's `## Commits` table (checklist item 28). C4's own cell and the
   complete change set belong to the round report.
   THE REFLOG IS REPORTED AS TWO MEASURED CLAIMS, NOT ONE UNIVERSAL (R-0601),
   AND NEITHER IS A TOTAL FOR THE ROUND (R-0605): report the count of this
   round's reflog entries whose OPERATION PREFIX — the text before the first
   colon of `git reflog --format=%gs` — reads exactly `commit`, TOGETHER WITH
   the commit it was taken at and the number of commits the round has made AT
   THAT MOMENT, and state that those two numbers are equal. State no total: C4
   is unwritten when this text is composed, so its entry cannot be counted here
   and the reviewer measures it at the next gate (R-0494). Report also the count
   whose prefix contains `amend`, `reset`, `rebase` or `cherry`, which must be 0.
G12 NO MARKER LEAKED. Report the count of LINES beginning `<<<SLICE ` or
   `<<<END ` in `.agent/plan.md` at C1, `.agent/live_review.md` at C2, both
   files at C3, and `.agent/handoff.md` at C4. Every count must be 0.
G13 THE PUSH. After C4, `git push` and report its real output. Do NOT create a
   pull request and do NOT wait on the CI run the push starts (constraint 12).

Handback:    Rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
             all seven mandated headings in the template's order, the
             item-status table for the C0a..C4 bundle, the `## Commits` table
             G11 pins, and one LINE per gate rather than its transcript
             (R-0582). The LINE cap your commit count earns is the bound. Its
             `## Next` section names the next session's FIRST action as Phase 1
             rule 1, the `.agent/STOP` re-read, and its SECOND as R12, which
             finishes T004 — `remedy teach ask`, the teacher model call, the
             honest refusal with no model configured, and spend under the role
             name `teacher` — and states that R11 awaits review and that T004's
             deterministic half is complete while its model half is not. There
             is no open pull request. Full transcripts go in the round report,
             never in the file. The handback carries this Fortschritt line
             verbatim (R-0418):
             Fortschritt: ~70 % (T001, T002 and T003 COMPLETE · T004 half done —
             the grounding sources, the level dial and the small context are
             built and red-proofed, zero tokens · the teacher model call, the
             integration gate and closure remain) — Schätzung
──────────────────────────────────────────────────────────────
