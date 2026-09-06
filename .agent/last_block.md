── STEP T002 (the state collapse, move two) — F272 ─
Goal:        Rename `JobPlan.status` to `JobPlan.state` at every site in ONE
             commit, with NO change of type, value, rendering or stored key, and
             pin the rename with a test; and rule the staging refinement this
             round is executing as DECISION F272 D6.
Bundle:      C0a save the block · C0b mirror · C1 the plan · C2 the round 8 gate
             entry and the D5 figure slip · C3 DECISION F272 D6 · C4 the rename ·
             C5 the test · C6 the handback.
Change:      EXACTLY the paths listed under "The change set" below and nothing
             else.
Handback:    completion report + rewrite `.agent/handoff.md`.
── end header. Per §3 item 37 every run of a repeated character in this block's
frame states its length: line 1 carries a run of 2 U+2500 then a run of 1, and
this line carries one run of 2. Both readings were measured, not recalled.

## What the reviewer MEASURED before ordering this (§3 item 34)

Round 8 PASSED, so `RunState` now covers every value `JobPlan.status` can hold.
D5 said the next move retypes and renames in one commit; the readings below split
it in two, and DECISION F272 D6 records why.

Every reading was taken at `c1c8f76d` by `ast` over the 1065 tracked `.py` files
enumerated from `git ls-files`, never by a name-regex over the text.

- THE RENAME IS 122 SITES ACROSS 20 FILES, not the 337 across 33 that DECISION
  F272 D5 states. D5's figure came from a grep that also counted every use of the
  six `JOB_*` constants, which this round does NOT touch. D5's RULING is
  unaffected and its cap claim holds with room to spare; the figure is refined
  here and recorded as a dated line in `.agent/prose_slips.md`, not as a finding,
  because nothing on disk is wrong.
- THE TYPE CHANGE CARRIES A HAZARD THE RENAME DOES NOT, and that is why D6 splits
  them. `RunState` is a `str, Enum`, and on this interpreter (Python 3.10.12)
  `str(RunState.PLANNED)` is `'RunState.PLANNED'` while an f-string, `format()`
  and `json.dumps` all give `'planned'`; every `JOB_*` constant is a plain `str`
  today whose `str()` IS its value. Retyping therefore changes what `str()` and
  `%s` render. Measured now: ZERO sites render a job status that way — but that
  is the RETYPE's gate, not this round's.
- THE SITES, each classified by reading it rather than by its receiver's name:
  86 `<job>.status` attribute reads and writes across 17 files, plus 36 `status=`
  keyword arguments in a `JobPlan(...)` call across 5 — 122 sites, 20 files.
- SEVEN SITES MATCHED THE SEARCH AND ARE NOT `JobPlan`. They must NOT be touched,
  and are named so the worker need not re-derive them. Four attribute sites:
  `tests/orchestration/test_autonomy.py:978`, `test_dogfood_run.py:164` and
  `:373`, `test_self_repair_proposal.py:414`. Three `replace(..., status=...)`
  calls: `packages/orchestration/mission_state.py:497`,
  `packages/orchestration/review_subject.py:1025`,
  `tests/orchestration/test_decision_evidence.py:1815`.
- NOTHING PINS `JobPlan`'s FIELD SET AS A CLOSED COLLECTION: no
  `__dataclass_fields__`, `fields(JobPlan)` or `set(asdict(` assertion in
  `tests/` reaches `JobPlan`, so the rename breaks exactly the sites that name
  the field and no guard beyond them.
- THE NAME `state` IS ALREADY TAKEN ELSEWHERE, and this is the round's main trap.
  The CLASSIC `Job` in `packages/core/models.py` has carried `state: RunState`
  all along, with 136 `<job>.state` sites across 50 files at `c1c8f76d`. ELEVEN
  of those sit INSIDE two files this round edits — 9 in
  `packages/orchestration/ui_server.py` and 2 in `apps/cli/commands/do_cmd.py` —
  so those two files will hold BOTH the classic `Job`'s `state` and, after C4,
  `JobPlan`'s. Renaming a `JobPlan` site there is correct; touching one of those
  eleven is not. G4(ii) is scoped and counted to make the difference visible.

## What the OPEN SET binds on this block (§3 item 34, last clause)

- "BINDING ON THE NEXT BLOCK THAT ORDERS A HANDBACK" — APPLIED, same words, in
  the Handback section below.
- R-0819's "BINDING ON THE NEXT BLOCK ... THAT GATES THE SHADOW PROPERTY" —
  DECLINED AS NOT APPLICABLE: no `run_dir`/`runs_dir` gate here, so there is no
  wording to correct; still owed by T003 and T004. Its general clause — run a
  gate at its base before ordering it — APPLIES and WAS applied, and it caught a
  real error: G4(ii)'s `.state` base is 11, not the 0 first drafted.

## The change set

C3: `docs/roadmap/features/T2_F272.md`.
C4, the rename, these twenty files and no others — the count beside each is its
`<job>.status` site count at `c1c8f76d`, and they sum to the 86 of G4(ii):

    28 packages/orchestration/pingpong_job.py     9 apps/cli/commands/job_stop_cmd.py
     7 packages/orchestration/job_evidence.py     6 apps/cli/commands/do_cmd.py
     5 tests/cli/test_job_stop.py                 4 tests/orchestration/test_job_task_runner.py
     4 tests/orchestration/test_job_stop_integration.py
     4 tests/orchestration/test_f018_authority_integration.py
     3 packages/orchestration/job_promote.py      3 tests/orchestration/test_job_worktree_handoff.py
     3 tests/orchestration/test_job_worktree_integration.py
     3 tests/orchestration/test_job_worktree_integrity.py
     2 packages/orchestration/ui_server.py        2 tests/cli/test_job_rerun_manifest.py
     1 packages/orchestration/self_use_runner.py  1 tests/orchestration/test_failure_wiring.py
     1 tests/orchestration/test_episode_snapshot_lifecycle.py
     0 tests/orchestration/test_job_promote.py    0 tests/orchestration/test_budget_guard.py
     0 tests/orchestration/test_f018_package_pipeline_e2e.py

The last three are in the set for their `status=` arguments alone (23, 1, 3).
C5: `tests/orchestration/test_job_state_field.py` (NEW).
C0a/C0b/C1/C2/C6: `.agent/authored/f272-r9.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/live_review.md`, `.agent/prose_slips.md`,
`.agent/handoff.md`.

## C3 — the DECISION

APPEND the DECISIONR9 slice to the END of `docs/roadmap/features/T2_F272.md`,
whose `## DECISIONs` section is the file's last and D5's REVERSE paragraph its
last. Assert the pre-image's terminal byte is exactly one newline BEFORE writing.

## C4 — the rename, a SPEC and not a slice, and ONE commit

In `packages/orchestration/pingpong_job.py`, rename the `JobPlan` field
`status: str = JOB_PLANNED` to `state: str = JOB_PLANNED`. THE ANNOTATION STAYS
`str` AND THE DEFAULT STAYS `JOB_PLANNED`: retyping to `RunState` is D6's move
three and is not ordered here.

Then, in the twenty files above, every `<job>.status` attribute read or write
becomes `<job>.state`, and every `status=` keyword argument in a `JobPlan(...)`
call becomes `state=`.

TWO THINGS DO NOT MOVE, both being DECISION F272 D5's ruling:
  - THE STORED JSON KEY STAYS `"status"`: in `_export_job` the entry becomes
    `"status": job.state`, in `_import_job` the argument becomes
    `state=data.get("status", JOB_PLANNED)`, so every record on disk still loads
    — which is what G4(iii) measures.
  - THE SIX `JOB_*` CONSTANTS KEEP THEIR NAMES, THEIR VALUES AND THEIR TYPE.

Do NOT touch the seven non-`JobPlan` sites named above, the eleven classic-`Job`
`.state` lines in `ui_server.py` and `do_cmd.py`, or anything merely CONTAINING
`status` — `final_status`, `worktree_cleanup_status`, `job_status`, a `TaskPlan`'s
or a manifest's own. If you find a site this block does not name, do not guess:
change it only if the receiver is provably a `JobPlan`, and report it separately.

ONE commit, because it cannot be split: any intermediate commit leaves the old
name on some callers and the new on others, so the suite is red and no gate could
be honest.

## C5 — the test, a SPEC and not a slice

NEW FILE `tests/orchestration/test_job_state_field.py`, following the module
docstring convention of `test_job_administrative_fields.py`. It pins at minimum:

1. **The field is `state` and `status` is gone.** `"state" in
   JobPlan.__dataclass_fields__` and `"status" not in`, the second being what
   makes the rename a replacement rather than an addition.
2. **The default is unchanged.** `JobPlan().state == JOB_PLANNED == "planned"`.
3. **The stored key did NOT move.** `_export_job` emits a `"status"` key carrying
   the state and NO `"state"` key; `_import_job` over an old record whose only
   lifecycle key is `"status"` returns a `JobPlan` whose `state` is that value.
4. **The round trip.** `_import_job(json.loads(json.dumps(_export_job(plan))))`
   preserves a non-default state, asserted for at least `JOB_BLOCKED`.
5. **The rendering is unchanged** — the guard D6 exists to protect: for a job
   whose state is `JOB_BLOCKED`, `f"{job.state}"` and the exported `"status"`
   value are both the plain string `"blocked"`. This is what goes red in move
   three if the retype lands without `.value` at the boundaries.

Every test carries a one-sentence docstring saying WHAT it pins and why that
could break.

## Constraints

1. NO SLICE IS EDITED — apply the authored texts byte for byte between their
   markers; if one looks wrong, apply it anyway and say so. C4 and C5 are a
   SPEC: write that code yourself.
2. The paths listed under "The change set" are the whole change set.
3. Commit order C0a, C0b, C1, C2, C3, C4, C5, C6, nothing reordered; C1 is the
   first substantive commit (§3 item 23).
4. APPEND CONVENTION for `.agent/live_review.md`, `.agent/prose_slips.md` and
   `docs/roadmap/features/T2_F272.md`: `post == pre + b"\n" + slice`, the slice
   being the marker-delimited lines each with its terminating newline, and the
   post-image ending in exactly one `\n`.
5. PLAN CONVENTION: `.agent/plan.md` is REPLACED by exactly the PLANF272R9 slice.
6. Behaviour changes: NONE. No value, type, rendering, stored key or `JOB_*`
   constant changes; this round renames one field.
7. Mint NO finding id of your own and write NO `Done:` paragraph of your own.
8. Destructive verification goes in a disposable `git worktree` under the
   gitignored `.remedy-wt/`, never the primary checkout (protocol G5); remove and
   prune it before the handback, BY EXACT PATH and never by glob.
9. Read `.agent/STOP` with `os.path.exists` before C0a, before C4 and before C6,
   and table all three; if it appears, finish only the half-written commit, then
   hand off (protocol G6).
10. `python3 -B` for every run; purge `__pycache__` in any worktree before a run;
    report each gate's REAL exit code, "green" as a word being a finding (G4).

## Gate list — DONE WHEN

**G1 TRANSPORT.** sha256 and byte length of the committed
`.agent/authored/f272-r9.md` and `.agent/last_block.md`; both equal each other and
the BLOCK_SHA and length the delegation names. Per §3 item 37 this covers the
saved copy and its mirror, not the bytes emitted into your prompt — say so.

**G2 THE RECORD, at C2.** Readers (a) to (d) over `.agent/live_review.md`, (a) and
(b) over `.agent/prose_slips.md`.
(a) BYTE: pre and post lengths; pre a byte-exact prefix; `post == pre + b"\n" +
slice`; pre's terminal byte asserted to be exactly one `\n` BEFORE writing; post
ends in exactly one `\n`.
(b) STRUCTURAL, computed independently of (a) by splitting the WHOLE image on
`\n{2,}`, with N COUNTED BY YOUR SCRIPT from the slice's own paragraphs and never
taken from this block: units before, after, delta; the last N units equal the
slice's paragraphs IN ORDER; the units before an unchanged prefix.
(c) NEGATIVE CONTROL in memory on a `bytes` object, never on disk: flip a byte
inside the FIRST appended paragraph, asserting the offset lies inside it first;
(a) and (b) must BOTH reject; restore and require both to accept and the restored
image to equal the disk image.
(d) COUNTS before → after C2: distinct `^- R-\d{4} — ` ids 303 → 303; distinct
`^Done: R-\d{4} — ` ids 247 → 247; open set BY DISTINCT ID 56 → 56; `^Gate: `
30 → 31; `^Gate: F272 R8 ` 0 → 1 — the first three unchanged because this round
mints no id.

**G3 THE PLAN at C1, AND THE FEATURE FILE at C3.** The plan: `.agent/plan.md`
equals the PLANF272R9 slice bytes exactly; report the equality, both byte
lengths, the line count against the AGENTS.md cap of 50, and that `## Goal` and
`## Next Steps` are present.
The feature file: readers (a) and (b) of G2's wording, with no negative control
(gate budget); plus the count YOU measure of lines matching
`^### DECISION F272 D\d+ ` and the D-number each names, in order.

**G4 THE RENAME IS COMPLETE, EXACT, AND CHANGED NOTHING ELSE, at C4.** Measured
by IMPORTING the shipped module and by `ast` over the tracked `.py` files, never
from a text grep; print `packages.orchestration.pingpong_job.__file__` first.
(i) THE FIELD: `"state" in JobPlan.__dataclass_fields__` TRUE and `"status" in
JobPlan.__dataclass_fields__` FALSE. Base readings at `c1c8f76d`, which this
round inverts: `state` FALSE, `status` TRUE.
(ii) THE SWEEP, by `ast` over every tracked `.py` file from `git ls-files`,
counting attribute sites whose receiver is a bare `Name` in
(`job`, `plan`, `job_plan`, `jp`, `loaded`, `reloaded`, `j`, `resumed`). REPORT
FOUR NUMBERS, INSIDE the twenty files of the change set and OUTSIDE them, because
a repo-wide count cannot tell this field from the CLASSIC `Job`'s own
`state: RunState`, which already has sites everywhere:

| reading | base at `c1c8f76d` | required after C4 |
|---|---|---|
| INSIDE the twenty, `.status` | 86 | 0 |
| INSIDE the twenty, `.state` | 11 | 97 |
| OUTSIDE them, `.status` | 4 | 4 |
| OUTSIDE them, `.state` | 125 | 125 |

The INSIDE `.state` base is 11, not 0, because `ui_server.py` (9) and
`do_cmd.py` (2) ALREADY read the classic `Job`'s `state` in files that also carry
`JobPlan.status`. THOSE ELEVEN ARE NOT YOURS TO TOUCH; 11 + 86 = 97, and a
post-count of 97 over a base of 11 is what distinguishes a correct rename from
one that also rewrote a classic-`Job` line. The OUTSIDE `.status` survivors must
remain exactly the four named above, reported BY PATH AND LINE.
(iii) THE STORED KEY DID NOT MOVE: for a `JobPlan` with `state=JOB_BLOCKED`,
`_export_job` has key `"status"` with value `"blocked"` and has NO key `"state"`;
and `_import_job` over a dict carrying `job_id` and `"status": "blocked"` and no
`"state"` key returns a `JobPlan` whose `state` is `"blocked"`.
(iv) NOTHING WAS RETYPED: `type(JobPlan().state).__name__` is `str` and
`isinstance(JobPlan().state, RunState)` is FALSE — this round is the RENAME, and
move three is what makes that second reading True.

**G5 THE PIN CAN FAIL — MUTATION RED-PROOF, in a disposable worktree at the
commit C5 creates.** Purge `__pycache__` first and confirm `pingpong_job`
resolves from INSIDE the worktree by printing its `__file__`. FIRST the UNMUTATED
CONTROL, in that worktree and BEFORE any mutation:
`python3 -B -m pytest tests/orchestration/test_job_state_field.py -q
-p no:randomly` must be EXIT 0; report its summary line — a colour with no
baseline is not evidence (§3 item 33).
THEN three mutations of the worktree's own copy of
`packages/orchestration/pingpong_job.py`, each byte string counted in that file
first where the count must be 1 (§3 item 25), each followed by a restore and a
control re-run that must be EXIT 0 again:
  (1) rename the dataclass field `state` back to `status` — require EXIT 1;
  (2) change the exporter's key from `"status"` to `"state"` — require EXIT 1,
      which is the pin that the stored key did not move;
  (3) change the importer's read from `data.get("status", JOB_PLANNED)` to
      `data.get("state", JOB_PLANNED)` — require EXIT 1, the old-record path.
Report one exit code per mutation. A mutation that leaves the run GREEN is a test
that pins nothing and is a finding of this round.

**G6 THE SUITES, at C5, run SERIALLY, each its own invocation.** The new file,
then `tests/orchestration/`, then `tests/docs/` (the change set includes
`docs/roadmap/**`, tier 5), then `tests/cli/`, then the canary
`tests/cli/test_golden_path.py`. Every one EXIT 0; report each exit code and
summary line verbatim. Measured at `c1c8f76d`: `tests/orchestration/` 12838
passed and 10 skipped, `tests/docs/` 303, `tests/cli/` 1537, canary 42. A LOWER
count anywhere is a finding; `tests/orchestration/` must RISE by C5's tests.

**G7 LINT AND INTEGRITY, at C5.** `python3 -m ruff check` over exactly the `.py`
files this round changed, in ONE invocation: EXIT 0; if red, report the codes and
fix nothing outside the change set. A repo-wide `ruff check .` is NOT ordered: it
is EXIT 1 on base under OPEN finding R-0468.
`python3 -m apps.cli.grouped integrity check --json`: EXIT 0, `"passed": true`,
`"fail_count": 0`.

**G8 THE TREE.** `git status --porcelain` EMPTY when C6 is staged;
`git ls-files .remedy-wt` EMPTY; `git worktree list` naming any worktree you
created and confirming its removal. Per commit C0a through C5 — NOT C6, which
cannot count its own insertions (§3 item 14) — the insertion count from `git diff
--numstat <parent> <commit>`, each single-parent and under the F104 D1 cap of
500; those same numbers fill the handback's `## Commits` `+/-` column, so report
both readings side by side and confirm each row cell by cell (§3 item 28).
Marker sweep: the number YOU measure of lines beginning `<<<BEGIN ` or `<<<END `
in every written non-block file, zero in each. The three `.agent/STOP` readings
of constraint 9, as a table.

## The slices

<<<BEGIN PLANF272R9>>>
# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 and 3 through 8 PASSED; round
2 FAILED on a premise DECISION F272 D2 has corrected. T001 is COMPLETE. T002 has
landed the eight administrative fields and widened `RunState` to cover every
value the job lifecycle field can hold.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the run
re-key, T002 the rest of the unified record, T003 the eleven consumers, T004 the
classic runner, T005 the reachability test and the cluster deletion.

## Current Step

The `state` collapse, move two of the three DECISION F272 D6 now stages. This
round renames `JobPlan.status` to `JobPlan.state` at all 122 sites in one commit,
changing NO type, value, rendering or stored key — the JSON key stays `"status"`
and the six `JOB_*` constants keep their names, values and type. A new test pins
the field, the unchanged key, the old-record path and the rendering.

## Next Steps

1. Move three: retype `JobPlan.state` to `RunState` and make the six `JOB_*`
   constants `RunState` members, with `.value` at every boundary leaving the
   record. `RunState`'s `str()` is `'RunState.X'` while its f-string is the
   value, so this round's rendering guard is what that move must keep green.
2. The Mission extension — the order, the contract, the mission plan and the
   ordered job references.
3. T003, the eleven consumers named under Design in `T2_F260.md`, one per commit
   where the diff allows, each with a test on a job created through the
   ping-pong path.
4. T004, the classic runner and the resolver collapse; then T005, the
   reachability test and the cluster deletion, which is never split.

## Risks

- The rename cannot be staged by caller: an intermediate commit leaves both
  names live and the suite red, so it is one commit or none.
- The classic `Job` also has a `state` field, with eleven sites inside two of
  the files this round edits; those eleven do not move.
<<<END PLANF272R9>>>

<<<BEGIN RECORDR9>>>
Gate: F272 R8 — the F272 round 8 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER RATHER THAN READ. Range `b5cde726`..`c1c8f76d`, eight commits, every one single-parent, in exactly the bundle's ordered sequence C0a, C0b, C1, C2, C3, C4, C5, C6 with nothing added, dropped or reordered; `git diff --name-status` over the range lists exactly the eight paths the block's change set enumerates and no other. G1 TRANSPORT IS A REAL CHAIN AND NOT MERELY SELF-CONSISTENT: the reviewer's own scratch original `.remedy-wt/f272-r8-block.md` survived, and it, the committed `.agent/authored/f272-r8.md` and the committed `.agent/last_block.md` are all 31197 bytes and all hash to `eb35a3437340e705d700ffe0ef406c6feb7ef8253af81ce7173c7d485f7bbcf0`; per §3 item 37 that chain covers those three artefacts and is not a claim about the bytes emitted into a prompt. G2 THE RECORD reproduces byte for byte: `.agent/live_review.md` 1097162 to 1104989, pre-image a byte-exact prefix, `post == pre + NL + slice` TRUE, reader (b) accepting with N counted at 2 from the slice's own paragraphs and units 696 to 698; registrations 303 unchanged, resolutions 247 unchanged, open set BY DISTINCT ID 56 unchanged, `^Gate: ` 29 to 30, `^Gate: F272 R7 ` 0 to 1 and `^Recurrence: R-0819 ` 0 to 1 — exactly the counts the block ordered, and the unchanged first three are correct because the round deliberately minted no id. G3 THE PLAN is 2279 bytes byte-equal to its slice at 44 lines against the cap of 50, and THE FEATURE FILE appended 19325 to 24461 with reader (b) accepting at N counted 13 and units 37 to 50, its `^### DECISION F272 D\d+ ` headings reading D1 D2 D3 D4 D5 in order. G4 THE ENUM, measured by importing the SHIPPED `/home/decodeux/Repos/remedy/packages/core/models.py`: the ordered members are PENDING PLANNED RUNNING PAUSED COMPLETED FAILED CANCELLED BLOCKED STOPPED, all six `JOB_*` values are now `RunState` values where at the base `b5cde726` `blocked` and `stopped` were NOT — the two the round adds and no others — the non-vacuity control `no_such_state` reads FALSE, and the seven pre-existing members both survive and remain the first seven IN ORDER. G5 THE MUTATION RED-PROOF REPRODUCED EXACTLY, in a disposable worktree at `a6567261` with the module confirmed resolving from inside it: unmutated control EXIT 0 at 21 passed; deleting the `BLOCKED` line EXIT 1 at 2 failed and 19 passed naming `blocked`; deleting the `STOPPED` line EXIT 1 at 2 failed and 19 passed naming `stopped`; ADDING a `NO_SUCH_STATE` member EXIT 1 at 1 failed and 20 passed; the control EXIT 0 at 21 passed after every restore and the file byte-identical at the end. THE ADDITION HALF MATTERS AS MUCH AS THE DELETION HALF: a coverage test that only notices removals would pass an enum that had silently grown, and this one notices both. G6 THE SUITES, re-run serially by the reviewer: `tests/orchestration/` EXIT 0 at 12838 passed and 10 skipped in 739.74s, `tests/docs/` EXIT 0 at 303 passed, `tests/cli/` EXIT 0 at 1537 passed in 305.96s, and the canary EXIT 0 at 42 passed; against the reviewer's own `b5cde726` readings that is a rise of EXACTLY 21 in `tests/orchestration/`, which is the 21 tests C5 adds and nothing else, with skips unchanged at 10 and no count falling anywhere. G7 EXIT 0 at `All checks passed!` over the two changed files and EXIT 0 with `"passed": true` and `"fail_count": 0` over 5 checks. G8 THE TREE: `git status --porcelain` EMPTY, `git ls-files .remedy-wt` EMPTY, the worktree removed by exact path with only the twelve pre-existing `remedy/job-*` entries remaining, the marker sweep 0 in all five written non-block files, and the per-commit insertion counts 400, 301, 17, 4, 80, 4 and 108 each single-parent, each under the DECISION F104 D1 cap of 500, and each matching the handback's `## Commits` table cell for cell. THE WORKER'S DEVIATION 4 IS UPHELD AND IS THE ROUND'S BEST JUDGEMENT CALL: the block specified four properties for C5 and said "at minimum", and the worker shipped 21 tests rather than four assertions by parametrizing items 1 to 3 so a failure names the constant it lost, and by adding one test pinning that the seven pre-existing members are the enum's FIRST SEVEN IN ORDER — a property G4(iv) measures but which no test otherwise enforced, so leaving it to the gate alone would have left a gate reading something nothing pinned. That is the correct reading of a minimum, and the suite rose by exactly 21 as a result. Deviations 1, 2, 3 and 5 through 8 are accepted as declared; deviation 5, that C0a and C0b land while the plan still describes the previous round, is the block's own ordered sequence under constraint 3 and not a departure from it.
<<<END RECORDR9>>>

<<<BEGIN SLIPSR9>>>
2026-09-07 · F272 R8 block and DECISION F272 D5 (reviewer) · D5's CONTEXT states that "`job.status` together with the six `JOB_*` constants occurs 337 times across 33 files", a figure taken from a grep whose alternation counted every use of the six constants alongside the attribute accesses. Re-measured by `ast` at `c1c8f76d`, the sites the rename actually moves are 122 across 20 files — 86 `<job>.status` attribute sites and 36 `status=` keyword arguments in `JobPlan(...)` calls — because the constants themselves do not move. The sentence is true of what it counts and overstates the work it describes, and D5's ruling and its under-the-500-cap claim are unaffected and hold with more room than stated. This is the §3 item 16 family reaching a DECISION's own CONTEXT paragraph: prefer naming the set to counting it, and where a count is load-bearing for a cap, count the thing that moves. Nothing on disk is wrong, so no id is spent and the landed text is corrected by the round 9 block's own measurement rather than rewritten.
<<<END SLIPSR9>>>

<<<BEGIN DECISIONR9>>>
### DECISION F272 D6 (2026-09-07, F272 round 9) — the `state` collapse is three moves, not two: the RENAME and the RETYPE are separated because only the retype can change what a state RENDERS as

CONTEXT. DECISION F272 D5 staged the collapse in two moves: widen `RunState`
(round 8, landed), then "replace `JobPlan.status: str` with `state: RunState`
across every call site in ONE commit". Preparing that second move, the reviewer
measured something at `c1c8f76d` that D5 could not have known. `RunState` is a
`str, Enum`, and on this interpreter (Python 3.10.12) `str(RunState.PLANNED)` is
`'RunState.PLANNED'`, while an f-string, `format()` and `json.dumps` all give
`'planned'`. Every `JOB_*` constant is a plain `str` today, whose `str()` IS its
value. So the RETYPE — and only the retype — can silently change what a job state
renders as, at any site using `str()` or the `%s` operator. The RENAME cannot: it
changes a name and touches no value. (D5's site figure is also refined, by the
dated line this round appends to `.agent/prose_slips.md`; the ruling stands.)

CHOSEN. THREE MOVES, NOT TWO. Move one widened `RunState` (round 8). MOVE TWO,
this round, renames the field to `state` at all 122 sites in one commit and
changes NO type, value, rendering or stored key. MOVE THREE, a later round,
retypes `state` to `RunState`, makes the six `JOB_*` constants `RunState` members,
and puts `.value` at every boundary where a state leaves the record — gated on the
rendering guard move two ships. Bundling them would have put a 122-site mechanical
edit and a subtle rendering change in one commit, where a red suite could not tell
which of the two caused it and a green one would have proved less than it seemed.

NOT CHANGED BY THIS RULING: D5 itself, its atomicity requirement — each move is
still one commit, because a half-renamed or half-retyped tree is red — and its
ruling that the stored JSON key stays `"status"`, which both remaining moves keep.

ALTERNATIVES CONSIDERED. Execute D5 as written, in one commit — rejected on the
measurement above: the two changes fail differently and deserve separate gates.
Retype first, rename second — rejected: the round that finds a rendering bug
would also be the round that moved 122 sites. Keep `status: str` — rejected:
D1 names the field `state` and AGENTS.md's Scope Control forbids leaving the
replaced spelling alive.

CONSEQUENCE. One extra round, and a rendering guard on disk that move three must
keep green. No behaviour changes in move two.

REVERSE by deleting this section, returning the collapse to D5's two-move
staging; the rename move two performs is not undone by that deletion.
<<<END DECISIONR9>>>

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md:
`SESSION 4 of feature F272 · round 9`, the one-sentence context self-assessment
amend0905-throughput requires, branch, the range, a per-commit changed-files
table with real `+/-`, the item-status table covering C0a through C6 with every
item present exactly once, one line per gate G1 to G8 with its real exit code,
G4's four scoped counts beside their base readings, the G5 exit codes, the
authored-text proof table, deviations and the next expected action. No length
cap. Per the fix clause OPEN in the record and binding on the next block that
orders a handback: any commit you make beyond the ordered sequence receives its
OWN `## Commits` row and its OWN item-status row, and the Deviations section says
so in those same words rather than beside a clause that denies it.
