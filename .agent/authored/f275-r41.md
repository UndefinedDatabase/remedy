── STEP T003 (6 of n) — F275 ─────────────────────────────────
Goal:        WIDEN `TaskEntry` with the two fields DECISION F275 D22 names, in
             its own commit and green by construction, so the flip commit that
             follows loses nothing a caller could read and carries 427 fewer
             lines than it otherwise would.
Bundle:      C0a save this block · C0b mirror it · C1 the plan · C2 the round 40
             verdict and two prose slips · C3 the widen · C4 the handback.
Change:      exactly the paths listed here and nothing else —
             `.agent/authored/f275-r41.md`, `.agent/last_block.md`,
             `.agent/plan.md`, `.agent/live_review.md`,
             `.agent/prose_slips.md`,
             `packages/orchestration/pingpong_job.py`,
             `tests/orchestration/test_job_administrative_fields.py`,
             plus `.agent/handoff.md` at C4.
Constraints: the numbered list below.
Done when:   gates G1 to G8 below are RUN and their real exit codes recorded.
Handback:    completion report + rewrite `.agent/handoff.md`.
── end of frame; the single pure rule line below is exactly 62 `─` characters
──────────────────────────────────────────────────────────────

## Base

This round's base is `bbede92f`. THE WHOLE WIDEN WAS APPLIED, LINTED, RUN AND
RED-PROVED by the reviewer in a disposable worktree at that base before this block
was authored. Every numeral below is that run's, including the two mutation
readings and the file lengths.

## What this round is

DECISION F275 D22, recorded one round ago, measured that the flip carries a second
type pair — `Job.tasks` is `list[Task]` and `JobPlan.tasks` is `list[TaskEntry]` —
and ruled it landed by WIDENING `TaskEntry` first. This is that widen, and it is
the first production line this session moves.

WHAT MAKES IT GREEN BY CONSTRUCTION, which is the property the whole staging rests
on. Nothing reads the new fields yet; no classic consumer moves; the record on
disk gains keys rather than losing them, and a job file written before this round
loads with the defaults. The reviewer ran the whole orchestration suite with the
widen applied and read `11879 passed, 10 skipped` with ONE failure,
`tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes`
— which was measured to fail identically at the UNMODIFIED base in the same
worktree, so it is the known fresh-worktree artifact and not this change.

WHY THESE TWO FIELDS AND NOT THE THIRD. D22 rules it: `output_artifact_ids` is
read at 35 sites, 15 of them production, including the live task runner and the
cockpit's detail panel, so deleting it in the flip would be a user-observable
loss; the per-task `budget` would silently remove a limit rather than a display;
and `acceptance_checks` is deliberately excluded, its structured form to be
registered as a finding by the flip round instead.

WHY `budget` IS A DICT AND NOT A `Budget`. The same record already does this:
`JobPlan.budgets` is declared `dict | None` and exported verbatim, because
`_export_job` emits JSON and never a model object. The test that proves it is the
round trip THROUGH `json.dumps`, which is the half that would fail if a model had
been stored.

## Constraints

1. APPLY EVERY SLICE BYTE FOR BYTE. Extract each by its delimiter lines from the
   committed `.agent/authored/f275-r41.md` and apply with `shutil.copyfile`
   semantics — never by retyping, never reflowed. If anything does not fit,
   DECLARE it in the handback and apply the rest.
2. THE COMMIT ORDER IS C0a, C0b, C1, C2, C3, C4, exactly — six commits, no extra,
   none dropped, no reordering. C1 is the first substantive commit and makes
   `.agent/plan.md` current before any other change, per §3 item 23.
3. THE APPEND BASELINES for the record, read by the reviewer at the base:
   `.agent/live_review.md` is 851931 bytes and `.agent/prose_slips.md` is 233188
   bytes, each ending in a newline. An append is pre-blob, then ONE newline, then
   the slice as extracted.
4. C3 IS THE ONLY COMMIT THAT TOUCHES ANYTHING OUTSIDE `.agent/`, and it touches
   exactly two paths. No path under `apps/`, `docs/` or `scripts/` moves at all.
5. WITHIN C3 THE ORDER IS FIXED: pairs H, I and J against
   `packages/orchestration/pingpong_job.py`; then pair L against
   `tests/orchestration/test_job_administrative_fields.py`; then append K to that
   same file. K's ordered-equality proof runs against the state L leaves, and G5
   states it as ONE chained reconstruction from the committed base blob to the
   committed C3 blob so that no uncommitted intermediate has to be trusted.
6. PAIRS H, I AND J ARE APPEND-SHAPED, MEASURED, NOT REWRITES: for each,
   `TO contains FROM: true`. Order no "FROM 0x" count for any of them — that
   reading is unattainable by construction for an append-shaped pair, per §4.9 and
   §3 item 15. PAIR L is a REWRITE: `TO contains FROM: false`. APPEND K is a CODE
   append, so its obligation is ORDERED EQUALITY and never the per-line count that
   binds prose, per §4.9 as finding R-0531 narrowed it.
7. IDS REGISTERED THIS ROUND: none. IDS RESOLVED THIS ROUND: none. The open set is
   86 by distinct id at the base and must read 86 at C3.
8. THE ROUND GATE IS TIER 1: the scoped commands in G7 and the canary. The full
   suite is NOT run this round — the reviewer ran the orchestration suite at the
   base with the widen applied and its reading is in "What this round is" above.

## SLICE PLAN41 → whole-file replacement of `.agent/plan.md`

<<<PLAN41
# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared. T001 and T002 are DONE, and the classic runner's whole
command surface is gone as of round 34.

## Current Step

ROUND 41 performs the WIDEN DECISION F275 D22 ruled: `TaskEntry` gains `output_artifact_ids`
and a per-task `budget`, both carried symmetrically through `_export_job` and `_import_job`,
with a test class pinning the defaults, the round trip through `json.dumps`, the defaulted
read of a record written before this round, and the real writer and reader. It is green by
construction — nothing reads the new fields yet — and it takes 427 lines out of the flip.

## Next Steps

1. The flip itself, applied from the round 36 site enumeration, the round 38 seam list and
   the round 40 task-pair list, as the one declared-oversize commit AGENTS.md permits per
   feature, with the inseparability reason AND the real size stated in the handback BEFORE
   review. It registers `Task.acceptance_checks`'s structured form as a finding naming the
   feature that owns acceptance criteria, per amend0908-f275-finish rule 4.
2. The resolver collapse DECISION F260 D5 places in T003 — `resolve_any_job_id`, the "TWO
   job stores" paragraph, every which-store branch and the absence test — with the classic
   store, which is the same commit range by that decision's own terms.
3. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   ledger rotation, the STATUS line and the PR.

## Risks

- Step 1 is the largest single commit this repository will take, and each round that
  measures it has found it larger: DECISION F275 D17 sized it at 1766 changed lines, D21 at
  3771 across 263 files, and D22 added a type pair worth 427 more, which this round removes.
- The open set is 86 by distinct id at this round's base `bbede92f`. This round registers
  none and resolves none. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's,
  per DECISION F272 D12.
PLAN41

## SLICE RECORD41 → append to `.agent/live_review.md`, in C2

<<<RECORD41
Gate: F275 R40 — the F275 round 40 entry. VERDICT PASS, written by the planner and reviewer of session 17 after reading the committed range `6537ece6`..`bbede92f` and RE-DERIVING EVERY GATE INDEPENDENTLY against the committed blobs; the worker's report was evidence for no line of it. Eight single-parent commits C0a `550546a1`, C0b `59bf95ca`, C1 `d5da71c7`, C2 `37af7420`, C3 `2181a292`, C4 `79a071bd`, C5 `2ab9ad3c` and C6 `bbede92f`, per-commit insertions 460, 393, 20, 6, 2, 284 and 75 for the seven before the handback, every one under the AGENTS.md DECISION F104 D1 cap of 500. G1: the reviewer's delegation source was written AND HASHED BEFORE delegation at `23a30e502609c1357d8442c7a4df1b1b4f954d85175df2588f8abd6122fb0283`, and both committed copies are 34779 bytes at that digest as ONE shared git blob; per §3 item 37 that chain covers three on-disk artefacts and claims nothing about bytes emitted into a prompt. G2: `.agent/plan.md` byte-identical to PLAN40 at 2488 bytes, 44 lines against the cap of 50, both mandated headings exactly once. G3 OVER ALL FOUR APPENDS, each re-derived by the reviewer as a reconstruction from one COMMITTED blob to the next, which this round's shape allows because no two of the four share both a commit and a file: `.agent/live_review.md` 844533 to 848253 at C2 and 848253 to 851931 at C3, `.agent/prose_slips.md` 231842 to 233188, `.agent/decisions.md` 1049788 to 1055728; every reconstruction byte-identical to the committed blob and every joining byte a newline; `^Gate: F275 R39 `, `^Done: R-0870 ` and `^## DECISION F275 D22 ` each exactly 1. G4 IS THE READING THIS ROUND EXISTS FOR: THE OPEN SET FALLS FROM 87 TO 86 BY DISTINCT ID, 103 registrations against 17 resolutions where the base held 16, `R-0870` is ABSENT from the open set at C5, and the ids resolved this round are exactly `['R-0870']` with none registered. G5: the resolution landed as authored bytes and CHANGED NOTHING ABOVE IT — the committed C3 blob equals the committed C2 blob followed by one newline and the DONE40 slice, so the entire prior ledger survives verbatim as a prefix, and the five `Landed: R-0870` lines read 5 at the base and 5 at C3. That is the property §3 item 20 protects, proved by prefix rather than by counting. G6: the canary and the event-name guard re-run by the reviewer together at 46 passed, exit 0; no production line moved this round so no wider suite was owed. G7: every figure of the committed `.agent/f275_t003_task_pair.md` reproduced when the reviewer re-ran its own instrument — 246 constructions, 142 imports and 40 annotations over 427 distinct changed lines in 111 files, 15 production and 96 test. G8: the change set is an EXACT set match over eight paths with MISSING and EXTRA both empty and ZERO paths outside `.agent/`, porcelain EMPTY, ONE worktree, `.agent/STOP` absent. THE WORKER'S FIVE DEVIATIONS ARE ALL SUSTAINED AND THE FIFTH CORRECTS THE REVIEWER. Its delegation message called this "the first round of this feature in which the reviewer resolves a finding", and the worker measured the record: `^Done: R-\d+ — RESOLVED at F275` reads FOUR at the base — R-0847 at round 27, R-0872 at round 29, R-0873 at round 30 and R-0874 at round 33 — so R-0870 is the fifth and the first since round 33. The claim appears in no slice and no committed byte carries it, which is why it costs a prose slip and not a correction round. The first four deviations are the worker's own self-review catching its own generated prose before the commit: three table cells escaping a literal pipe that would otherwise split a GFM row, and one pluralization. NO FINDING IS REGISTERED BY THIS GATE AND EXACTLY ONE IS RESOLVED.
RECORD41

## SLICE SLIPS41 → append to `.agent/prose_slips.md`, in C2

<<<SLIPS41
2026-09-10 · F275 R40 · The round 40 DELEGATION MESSAGE — not the block, and not any slice — told the worker that this was "the first round of this feature in which the reviewer resolves a finding". The worker measured the record instead of believing it and found four earlier F275 resolutions, R-0847, R-0872, R-0873 and R-0874, making R-0870 the fifth. No committed byte carries the claim, so nothing is owed but this line. The lesson is about WHERE the claim sat: every sentence in a block is checked against the record before emission, and the wrapper that carries the block is written in the same breath and checked by nothing. A wrapper states the delimiters, the digest and the rules; a claim about the record belongs in the block, where the checklist reaches it.

2026-09-10 · F275 R40 · The round 40 SPEC-TASK ordered a generated markdown TABLE whose cells carry Python type strings, and three of those types are unions — `bool | None`, `ApplyManifest | None`, `TaskProofSummary | None`. A literal pipe splits a GFM table row even inside backticks, so the generated file's 23-row table broke and the worker had to escape three cells, which it caught in its own self-review before committing. A generation spec that orders a table says how a cell containing the delimiter is escaped, because the tool producing it has no way to know and the reviewer specifying it already knows the population.
SLIPS41

## The widen — PAIRS H, I, J and L, and APPEND K

Every FROM occurs EXACTLY ONCE in its target, measured at the base. H, I and J are
APPEND-SHAPED (`TO contains FROM: true`); L is a REWRITE
(`TO contains FROM: false`). All were applied, linted and run by the reviewer
before emission.

## PAIR H → `packages/orchestration/pingpong_job.py`, the dataclass

FROM 67 bytes sha256 `d76d8b990df61ef5…`; TO 762 bytes sha256 `4090a79a9f21a35c…`;
TO's longest line 87 characters against the `pyproject.toml` limit of 120.
`field` is already imported in this module — `run_refs` uses
`field(default_factory=list)` on the same dataclass — and `Budget` is already
imported too, though this pair does not use it, for the reason the block states.

<<<PAIRH_FROM
    task_attempt_state: str = ""      # "" | "active" | "complete"
PAIRH_FROM

<<<PAIRH_TO
    task_attempt_state: str = ""      # "" | "active" | "complete"
    # F275 T003, DECISION F275 D22: the two fields the classic `Task` carried and
    # `TaskEntry` had no counterpart for. They are widened in BEFORE the flip, so the
    # commit that moves consumers onto this record loses nothing a caller could read.
    # `output_artifact_ids` is read at 35 sites, 15 of them production, including the
    # live task runner and the cockpit's detail panel. `budget` is a serialized dict
    # rather than a `Budget`, which is the shape `JobPlan.budgets` already uses on this
    # same record for the same reason: the exporter emits JSON, never a model object.
    output_artifact_ids: list[str] = field(default_factory=list)
    budget: dict | None = None
PAIRH_TO

## PAIR I → `packages/orchestration/pingpong_job.py`, the task export

FROM 60 bytes sha256 `998e62f123c2856e…`; TO 158 bytes sha256
`9a0133e60bbcdea2…`.

<<<PAIRI_FROM
                "task_attempt_state": t.task_attempt_state,
PAIRI_FROM

<<<PAIRI_TO
                "task_attempt_state": t.task_attempt_state,
                "output_artifact_ids": t.output_artifact_ids,
                "budget": t.budget,
PAIRI_TO

## PAIR J → `packages/orchestration/pingpong_job.py`, the task import

FROM 64 bytes sha256 `8b6b6f21c7d6ac2f…`; TO 174 bytes sha256
`66053bbe27714841…`.

<<<PAIRJ_FROM
            task_attempt_state=t.get("task_attempt_state", ""),
PAIRJ_FROM

<<<PAIRJ_TO
            task_attempt_state=t.get("task_attempt_state", ""),
            output_artifact_ids=list(t.get("output_artifact_ids") or []),
            budget=t.get("budget"),
PAIRJ_TO

## PAIR L → `tests/orchestration/test_job_administrative_fields.py`, the import

FROM 137 bytes sha256 `151806bf94f6c9fb…`; TO 152 bytes sha256
`15c90d5db522173a…`. `TaskEntry` is not imported in this file at the base — the
reviewer read the file rather than assuming it, which is why this pair exists.

<<<PAIRL_FROM
from packages.orchestration.pingpong_job import (
    JobPlan,
    _export_job,
    _import_job,
    load_job_plan,
    save_job_plan,
)
PAIRL_FROM

<<<PAIRL_TO
from packages.orchestration.pingpong_job import (
    JobPlan,
    TaskEntry,
    _export_job,
    _import_job,
    load_job_plan,
    save_job_plan,
)
PAIRL_TO

## APPEND K → `tests/orchestration/test_job_administrative_fields.py`, at the END

3681 bytes sha256 `e1fe7a11a1db651a…`, longest line 85. It begins with TWO
newlines because the target ends in one and PEP 8 wants two blank lines before a
top-level class; `ruff` was run on the applied file and printed
`All checks passed!`. The class declares its OWN `isolate_data` fixture rather
than reaching for the one above it, which is class-scoped and therefore invisible
here — the reviewer read that rather than assuming a shared fixture.

<<<APPENDK


class TestTheTwoTaskFieldsWidenedInBeforeTheFlip:
    """F275 T003 — the two fields `TaskEntry` had no counterpart for.

    DECISION F275 D22 measured that the classic `Task` and the unified `TaskEntry`
    share two field names of seven and twenty-three, and that three `Task` fields
    have no counterpart of the same meaning. Two of those are widened in here,
    before the flip, so that the commit moving consumers onto the unified record
    loses nothing a caller could read; `acceptance_checks` is deliberately NOT
    among them and its structured form is registered as a finding instead.

    These pin the same three properties the eight job-level fields above pin, for
    the same reason: `_export_job` and `_import_job` are explicit field-by-field
    functions, so a field added to the dataclass and to neither of them vanishes
    on the first persist/resume cycle.
    """

    @pytest.fixture
    def isolate_data(self, tmp_path: Path, monkeypatch) -> Path:
        """Persist jobs under tmp_path, never the repo's configured data dir.

        Declared again rather than shared: the fixture above it is class-scoped,
        and a fixture reached from another class is a fixture nobody can move.
        """
        data_dir = tmp_path / "remedy_data"
        data_dir.mkdir()
        monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
        return data_dir

    def _task(self):
        return TaskEntry(
            task_id="t1",
            title="widened",
            output_artifact_ids=["a1", "a2"],
            budget={"max_usd": 1.5, "max_tokens": 200},
        )

    def test_both_default_to_empty_rather_than_to_none(self):
        """A task written before this round loads with an empty list, not `None`."""
        fresh = TaskEntry(task_id="t0")
        assert fresh.output_artifact_ids == []
        assert fresh.budget is None

    def test_both_survive_the_round_trip_through_json(self):
        """Export, `json.dumps`, `json.loads`, import — the cycle a persist performs.

        The `json.dumps` is the load-bearing half: it proves the exporter emitted
        JSON-serialisable data rather than a model object, which is why `budget` is
        a dict here and not a `Budget`.
        """
        plan = JobPlan(job_id="j1", job_title="widen")
        plan.tasks.append(self._task())

        revived = _import_job(json.loads(json.dumps(_export_job(plan))))

        assert len(revived.tasks) == 1
        assert revived.tasks[0].output_artifact_ids == ["a1", "a2"]
        assert revived.tasks[0].budget == {"max_usd": 1.5, "max_tokens": 200}

    def test_a_record_written_before_this_round_still_loads(self):
        """Neither key present — the defaulted read, which is what a resume does."""
        plan = JobPlan(job_id="j2", job_title="older")
        plan.tasks.append(TaskEntry(task_id="t9", title="older"))
        data = json.loads(json.dumps(_export_job(plan)))
        data["tasks"][0].pop("output_artifact_ids", None)
        data["tasks"][0].pop("budget", None)

        revived = _import_job(data)

        assert revived.tasks[0].output_artifact_ids == []
        assert revived.tasks[0].budget is None

    def test_both_survive_the_real_job_record_file(self, isolate_data):
        """The same two survive `save_job_plan` -> job.json -> `load_job_plan`."""
        plan = JobPlan(job_id="j3", job_title="on disk")
        plan.tasks.append(self._task())
        save_job_plan(plan)

        loaded = load_job_plan(plan.job_id)

        assert loaded is not None
        assert loaded.tasks[0].output_artifact_ids == ["a1", "a2"]
        assert loaded.tasks[0].budget == {"max_usd": 1.5, "max_tokens": 200}
APPENDK

## Done when — GATES G1 to G8

Run each as `bash -c '<cmd>; echo "REAL_EXIT=$?"'` and record the REAL exit code
and the real numbers. "Green" as a word is a finding. One line per gate in the
handback. Where a gate names both a COUNT and an EXIT CODE, report both.

**G1 TRANSPORT (at C0b).** The committed `.agent/authored/f275-r41.md` and
`.agent/last_block.md` have the SAME sha256 as the reviewer's delegation source,
and resolve to ONE shared git blob. `.agent/last_block.md` is written from
`git cat-file blob HEAD:.agent/authored/f275-r41.md`, never retyped. State that
the chain covers those on-disk artefacts and claims nothing about emitted bytes.

**G2 THE PLAN (at C1).** `.agent/plan.md` is BYTE-EQUAL to the PLAN41 slice as
extracted — same length, same sha256. Report its line count against the
AGENTS.md cap of 50, and `^## Goal$` and `^## Next Steps$` each exactly 1.

**G3 THE RECORD (at C2).** For RECORD41 and SLIPS41: post-blob equals pre-blob
then ONE newline then the slice, with constraint 3's baselines; the two go to
DIFFERENT files, so both pre-blobs and both post-blobs are committed blobs. READ
BACK the joining byte at each offset. Then an INDEPENDENT structural reader with N
COUNTED FROM EACH SLICE. Then one negative control per append, flipping a byte
INSIDE THE FIRST appended paragraph, which BOTH readers must REJECT.
`^Gate: F275 R40 ` exactly 1 at C2.

**G4 THE OPEN SET (at C3).** BY DISTINCT ID, every `^- R-\d+ — ` id minus every
`^Done: R-\d+ — ` id, read at THIS round's base `bbede92f` with
`git show bbede92f:.agent/live_review.md` into memory — never by writing over the
tracked file — and again at C3. The reviewer read 86 at the base and expects 86 at
C3. Ids registered and ids resolved this round must both be `[]`.

**G5 THE WIDEN IS THE AUTHORED BYTES (at C3).** For pairs H, I and J: each FROM
occurs EXACTLY 1x in `packages/orchestration/pingpong_job.py` before the edit and
each TO EXACTLY 1x after, and NO FROM-ZERO COUNT IS ORDERED because all three are
append-shaped. For pair L: FROM 1x before and 0x after, TO 1x after. For append K:
ORDERED EQUALITY — the state pair L leaves is a byte-exact PREFIX of the committed
C3 blob and K is an exact SUFFIX of it. Prove ALL FIVE as ONE CHAINED
RECONSTRUCTION per file: rebuild the committed C3 blob of each path from its
committed BASE blob by applying that path's slices in the constraint-5 order, and
compare sha256. The reviewer measured
`packages/orchestration/pingpong_job.py` at 164734 bytes before and 165637 after,
and `tests/orchestration/test_job_administrative_fields.py` at 8785 before and
12481 after. Then
`python3 -m ruff check packages/orchestration/pingpong_job.py tests/orchestration/test_job_administrative_fields.py`
— the reviewer read `All checks passed!` at exit 0.

**G6 THE WIDEN BITES — RED PROOF (at C3).** In a DISPOSABLE `git worktree` at C3,
`__pycache__` purged, every run under `python3 -B`, the selection scoped to
`tests/orchestration/test_job_administrative_fields.py`. CONTROL unmutated: the
reviewer read exit 0 at `12 passed`. Each mutation's anchor is counted in
`packages/orchestration/pingpong_job.py` and must read 1 before it is applied, and
each is reverted byte-exactly with sha256 re-read before the next.
  M1 — DELETE the whole line `                "output_artifact_ids": t.output_artifact_ids,`
  from the task export. The reviewer read exit 1 at `2 failed, 10 passed`, the
  named assertions being `…::test_both_survive_the_round_trip_through_json` and
  `…::test_both_survive_the_real_job_record_file`.
  M2 — DELETE the whole line `            output_artifact_ids=list(t.get("output_artifact_ids") or []),`
  from the task import. The reviewer read exit 1 at `2 failed, 10 passed`, the same
  two assertions.
Report the CONTROL AGAIN reading after both reverts, which the reviewer read at
exit 0 and `12 passed`.

**G7 THE SCOPED GATE (at C3).**
`python3 -B -m pytest tests/orchestration/test_job_administrative_fields.py tests/cli/test_golden_path.py -q`,
which the reviewer read at `54 passed` at exit 0 with the widen applied — the
target file's own tests plus the canary. Then the property measured through the
SHIPPED functions rather than by grep: import `TaskEntry` and
`dataclasses.fields`, and report that `output_artifact_ids` and `budget` are both
present, that a bare `TaskEntry(task_id="x")` reads `[]` and `None` for them, and
that `_export_job`'s task dict carries both keys.

**G8 NOTHING ELSE MOVED (at C3).** `.agent/STOP` read FROM DISK: report present
or absent. `git status --porcelain`: EMPTY. `git worktree list`: exactly ONE
entry. `git diff --name-only bbede92f..C3` is an EXACT SET MATCH against the
`Change:` list above minus `.agent/handoff.md` — report MISSING and EXTRA
explicitly, and report that ZERO paths under `apps/`, `docs/` or `scripts/` appear
in it. Per-commit insertions for C0a through C3, each under the DECISION F104 D1
cap of 500; the handback commit's own numbers are NOT ordered here, per §3 item 14.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md. It carries
SESSION 17 of F275 and round 41, the per-commit table with `git diff --numstat`
values in the `+/-` column, one line per gate G1 to G8 with real exit codes, the
item-status table, the open-findings count by distinct id, and the deviations.
Add the one sentence of context self-assessment amend0905-throughput requires. No
PR is created and nothing is merged: this round is not a closure sequence.
