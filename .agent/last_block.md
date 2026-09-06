── STEP T002 (the state collapse, move one) — F272 ─
Goal:        Widen `RunState` with the two members `JobPlan`'s status vocabulary
             has and it lacks, pin the coverage with a test that is RED at its
             own base, and rule the whole `state`/`status` collapse as DECISION
             F272 D5 so the next round executes it mechanically.
Bundle:      C0a save the block · C0b mirror · C1 the plan · C2 the round 7 gate
             entry and the R-0819 recurrence · C3 the two DECISIONs into the
             feature file · C4 the two RunState members · C5 the coverage test ·
             C6 the handback.
Change:      EXACTLY the paths listed under "The change set" below and nothing
             else.
Handback:    completion report + rewrite `.agent/handoff.md`.
── end header. Per §3 item 37 every run of a repeated character in this block's
frame states its length: line 1 carries a run of 2 U+2500 then a run of 1, and
this line carries one run of 2. Both readings were measured, not recalled.

## Where this round stands

Round 7 PASSED and T002's eight pure-addition fields are on `JobPlan`. Of DECISION
F260 D1's three COLLIDING names, `id` is the 16-hex `job_id` and `name` is
`job_title` — both answered by naming — while `state` is a real type change and is
what this round prepares.

## What the reviewer read and MEASURED before ordering this (§3 item 34)

Every reading below was taken at `b5cde726` unless another commit is named, and
each is a fact this round depends on.

- The classic `Job` (`packages/core/models.py:222`) already spells the field
  `state: RunState = RunState.PENDING` at line 231, while `JobPlan`
  (`packages/orchestration/pingpong_job.py:305`) spells it `status: str =
  JOB_PLANNED`. The target spelling is not being invented here.
- THE VALUE SETS DIFFER IN BOTH DIRECTIONS, which is why a rename alone loses
  data. `JobPlan`'s six `JOB_*` constants are `planned`, `running`, `blocked`,
  `completed`, `paused`, `stopped`; `RunState`'s members are `pending`,
  `planned`, `running`, `paused`, `completed`, `failed`, `cancelled`. Running
  the coverage reading G4 orders, at `b5cde726`: `planned` True, `running` True,
  `blocked` FALSE, `completed` True, `paused` True, `stopped` FALSE. THE GATE IS
  THEREFORE MEASURED NON-VACUOUS AT ITS OWN BASE — the counter-measure R-0819's
  fix clause makes binding — and the C5 test needs no invented red control
  because it is red at the base by construction.
- WIDENING IS SAFE, measured rather than assumed. Over `packages/`, `apps/` and
  `tests/` there is NO `list(RunState)`, `len(RunState)`, `set(RunState)`,
  `tuple(RunState)`, no `for ... in RunState`, no `match`/`case RunState` and no
  dict entry keyed `RunState.<MEMBER>:`; the only `RunState.<MEMBER>` uses are
  six equality comparisons in `worker_recommend.py`, `autonomy_loop.py`,
  `task_runner.py` and `dag_schedule.py`. Nothing enumerates the enum.
- THE COLLAPSE ITSELF IS ROUND 9, NOT THIS ONE. `job.status` with the six `JOB_*`
  constants occurs 337 times across 33 files — one atomic commit's worth, under
  the DECISION F104 D1 cap of 500 insertions.

## What the OPEN SET binds on this block (§3 item 34, last clause)

The reviewer searched `.agent/live_review.md` for fix clauses labelled binding on
the next block. Both are answered here rather than left to be discovered:

- "BINDING ON THE NEXT BLOCK THAT ORDERS A HANDBACK" — APPLIED, in the same
  words, in the Handback section below.
- R-0819's "BINDING ON THE NEXT BLOCK ... THAT GATES THE SHADOW PROPERTY" —
  DECLINED AS NOT APPLICABLE: this block gates no `run_dir`/`runs_dir` shadow
  property, so there is no gate for that wording to correct, and it stays owed
  by T003 and T004. R-0819's OTHER clause — run a gate at its base before
  ordering it — is general, applies here, and WAS applied above.

## The change set

C3: `docs/roadmap/features/T2_F272.md`.
C4: `packages/core/models.py`.
C5: `tests/orchestration/test_run_state_covers_job_status.py` (NEW FILE).
C0a/C0b/C1/C2/C6: `.agent/authored/f272-r8.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/live_review.md`, `.agent/handoff.md`.

Those are the paths of this round and there are no others. Nothing under `apps/`,
nothing else under `packages/`, no other file under `docs/`.

## C3 — the two DECISIONs

APPEND the DECISIONR8 slice to the END of `docs/roadmap/features/T2_F272.md`. Its
`## DECISIONs` section is the file's last and D3's REVERSE paragraph its last, so
the append lands in that section with no heading to move. Assert the pre-image's
terminal byte is exactly one newline BEFORE writing.

## C4 — the two RunState members, a SPEC and not a slice

In `packages/core/models.py`, add two members to `RunState` (the class at line
38), placed at the END of the member list, after `CANCELLED`:

| member | value |
|---|---|
| `BLOCKED` | `"blocked"` |
| `STOPPED` | `"stopped"` |

Above them put a one-sentence WHY comment, in this repository's idiom (AGENTS.md,
Code Discoverability): these two come from `JobPlan`'s `JOB_*` vocabulary and
exist so DECISION F272 D5's collapse can rename `status` to `state` without
losing a state. Do not reorder, rename, revalue or delete any existing member —
the seven that are there keep their spelling and their order, and G4 measures
that. `RunState` is a `str, Enum`, so a member's value is the string every
existing comparison already uses and adding one changes no existing path.

## C5 — the coverage test, a SPEC and not a slice

NEW FILE `tests/orchestration/test_run_state_covers_job_status.py`, following the
module-docstring convention of `test_job_administrative_fields.py`. It imports
`RunState` from `packages.core.models` and the `JOB_*` constants from
`packages.orchestration.pingpong_job`, and pins at minimum:

1. **Every `JOB_*` value is a `RunState` value.** One assertion per constant, so
   a failure names the constant it lost. This is the test that is RED at
   `b5cde726` for `JOB_BLOCKED` and `JOB_STOPPED` and green after C4.
2. **The seven pre-existing members survive.** `pending`, `planned`, `running`,
   `paused`, `completed`, `failed`, `cancelled` are each still `RunState`
   values with those exact spellings. Breaks if C4's edit renames or revalues one
   while adding the two.
3. **`RunState(value)` round-trips for each of the six `JOB_*` values** — the
   lookup round 9's importer will perform on a record's stored string.
4. **A value that is not a state is rejected.** `RunState("no_such_state")`
   raises `ValueError` — the non-vacuity control, without which a membership
   test answering True for everything would pass items 1 to 3.

Every test carries a one-sentence docstring saying WHAT it pins and why that
could break, per this repository's convention.

## Constraints

1. NO SLICE IS EDITED. Apply the authored texts byte for byte between their
   markers. If one looks wrong, apply it anyway and say so in the handback.
   C4 and C5 are a SPEC, not slices: write the code yourself to the description.
2. The paths listed under "The change set" are the whole change set.
3. Commit order C0a, C0b, C1, C2, C3, C4, C5, C6, nothing reordered. C1 is the
   first substantive commit (§3 item 23).
4. APPEND CONVENTION for `.agent/live_review.md` and for
   `docs/roadmap/features/T2_F272.md`: `post == pre + b"\n" + slice`, the slice
   being the lines between the markers each carrying its own terminating
   newline, and the post-image ending in exactly one `\n`.
5. PLAN CONVENTION: `.agent/plan.md` is REPLACED by exactly the PLANF272R8 slice
   bytes and nothing else.
6. Behaviour changes: NONE. No existing `RunState` member is renamed, revalued,
   reordered or removed; no existing caller is touched; `JobPlan.status` is NOT
   changed this round.
7. Mint NO finding id of your own and write NO `Done:` paragraph of your own.
   The RECORDR8 slice is authored below and is applied verbatim.
8. Destructive verification goes in a disposable `git worktree` under the
   gitignored `.remedy-wt/`, never in the primary checkout (protocol G5).
   Remove and prune it before the handback, BY EXACT PATH and never by glob.
9. Read `.agent/STOP` with `os.path.exists` three times — before C0a, before C4
   and before C6 — and table all three. If it appears, finish only the
   half-written commit, then hand off (protocol G6).
10. `python3 -B` for every run; purge `__pycache__` in any worktree before a run;
    report each gate's REAL exit code, "green" as a word being a finding (G4).

## Gate list — DONE WHEN

**G1 TRANSPORT.** sha256 and byte length of the committed
`.agent/authored/f272-r8.md` and `.agent/last_block.md`; both equal each other and
the BLOCK_SHA and length the delegation names. Per §3 item 37 this covers the
saved copy and its mirror, not the bytes emitted into your prompt — say so.

**G2 THE RECORD, at C2.** Four readers over `.agent/live_review.md`.
(a) BYTE: pre and post lengths; pre a byte-exact prefix; `post == pre + b"\n" +
slice`; pre's terminal byte asserted to be exactly one `\n` BEFORE writing; post
ends in exactly one `\n`.
(b) STRUCTURAL, computed independently of (a) by splitting the WHOLE image on
`\n{2,}`, with N COUNTED BY YOUR SCRIPT from the slice's own paragraphs and never
taken from this block: units before, after, delta; the last N units equal the
slice's paragraphs IN ORDER; the units before an unchanged prefix.
(c) NEGATIVE CONTROL in memory on a `bytes` object, never on disk: flip a byte
inside the FIRST appended paragraph, asserting the offset lies inside it before
flipping; readers (a) and (b) must BOTH reject; restore and require both to
accept and the restored image to equal the disk image.
(d) COUNTS before → after C2: distinct `^- R-\d{4} — ` ids 303 → 303; distinct
`^Done: R-\d{4} — ` ids 247 → 247; open set BY DISTINCT ID 56 → 56; `^Gate: `
29 → 30; `^Gate: F272 R7 ` 0 → 1; `^Recurrence: R-0819 ` 0 → 1. This round mints
no id, so the first three readings are deliberately unchanged.

**G3 THE PLAN at C1, AND THE FEATURE FILE at C3.**
The plan: `.agent/plan.md` equals the PLANF272R8 slice bytes exactly; report the
equality, both byte lengths, the line count against the AGENTS.md cap of 50, and
that `## Goal` and `## Next Steps` are both present.
The feature file: readers (a) and (b) of G2's wording over
`docs/roadmap/features/T2_F272.md`, with no negative control (gate budget); plus,
over the post-image, the count YOU measure of lines matching
`^### DECISION F272 D\d+ ` and the D-number each names, in order.

**G4 THE ENUM, at C4.** Measured by IMPORTING the shipped modules, never from
their source text; print `packages.core.models.__file__` first.
(i) The full ordered member list of `RunState`, name and value.
(ii) For each of the six `JOB_*` constants imported from
`packages.orchestration.pingpong_job`, report whether its value is a `RunState`
value — every one TRUE. The reviewer measured this same reading at `b5cde726`
and got `blocked` and `stopped` FALSE with the other four TRUE, so report your
own reading beside that base one.
(iii) NON-VACUITY CONTROL: report that `"no_such_state"` is NOT a `RunState`
value (must be FALSE), so the TRUEs above are not measuring a test that answers
TRUE for everything.
(iv) THE SEVEN SURVIVE: report, one per line, that `pending`, `planned`,
`running`, `paused`, `completed`, `failed` and `cancelled` are each still
`RunState` values, and that the member list's first seven entries are still those
in that order.

**G5 THE PIN CAN FAIL — MUTATION RED-PROOF, in a disposable worktree at the
commit C5 creates.** Purge `__pycache__` first and confirm `packages.core.models`
resolves from INSIDE the worktree by printing its `__file__`.
FIRST the UNMUTATED CONTROL, in that same worktree and BEFORE any mutation:
`python3 -B -m pytest tests/orchestration/test_run_state_covers_job_status.py -q
-p no:randomly` must be EXIT 0; report its summary line. A colour with no
baseline is not evidence (§3 item 33).
THEN, for the `BLOCKED` member and the `STOPPED` member separately, delete that
member's single line from `RunState` in the worktree's own copy of
`packages/core/models.py` — counting those exact bytes IN THAT FILE first, where
the count must be 1, and choosing a longer unique byte string if it is not (§3
item 25) — re-run the same command, require EXIT 1 with the failure naming that
member's value, then restore and confirm the control EXIT 0 before the next.
THEN A THIRD MUTATION IN THE OTHER DIRECTION, proving item 4 of C5 is not
decoration: without touching the test, ADD one member `NO_SUCH_STATE =
"no_such_state"` to `RunState` in the worktree's copy, require EXIT 1, remove it
and require EXIT 0. A member's deletion and an unexpected member's addition must
BOTH be visible, or the test pins one direction only. One exit code per mutation.

**G6 THE SUITES, at C5, run SERIALLY, each its own invocation.**
`tests/orchestration/test_run_state_covers_job_status.py`, then
`tests/orchestration/`, then `tests/docs/` (ordered because this round's change
set includes `docs/roadmap/**`, verification tier 5), then `tests/cli/`, then the
canary `tests/cli/test_golden_path.py`. Every one EXIT 0. Report each exit code
and each summary line verbatim. The reviewer measured at `b5cde726`:
`tests/orchestration/` 12817 passed and 10 skipped, `tests/docs/` 303 passed,
`tests/cli/` 1537 passed, canary 42 passed. A LOWER count anywhere is a finding,
not a rounding; `tests/orchestration/` must RISE by exactly the tests C5 adds.

**G7 LINT AND INTEGRITY, at C5.** `python3 -m ruff check` over exactly the two
changed `.py` files in ONE invocation: EXIT 0. If it goes red, report the codes
and do NOT fix anything outside the change set. A repo-wide `ruff check .` is NOT
ordered: it is EXIT 1 on base under OPEN finding R-0468.
`python3 -m apps.cli.grouped integrity check --json`: EXIT 0, `"passed": true`,
`"fail_count": 0`.

**G8 THE TREE.** `git status --porcelain` EMPTY when C6 is staged;
`git ls-files .remedy-wt` EMPTY; `git worktree list` naming any worktree you
created and confirming its removal, the twelve pre-existing `remedy/job-*`
entries being older than this round. Per commit C0a through C5 — NOT C6, which
cannot count its own insertions (§3 item 14) — the insertion count from `git diff
--numstat <parent> <commit>`, each single-parent and under the DECISION F104 D1
cap of 500; those same numbers fill the handback's `## Commits` `+/-` column, so
report both readings side by side and confirm each row cell by cell (§3 item 28),
`.agent/last_block.md` being the full-file rewrite where line counts and diff
columns diverge. Marker sweep: the number YOU measure of lines beginning
`<<<BEGIN ` or `<<<END ` in every written non-block file, zero in each. The three
`.agent/STOP` readings of constraint 9, as a table.

## The slices

<<<BEGIN PLANF272R8>>>
# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1, 3, 4, 5, 6 and 7 PASSED;
round 2 FAILED on a premise DECISION F272 D2 has corrected. T001 is COMPLETE, and
T002's eight pure-addition administrative fields landed in round 7.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the plural
run list and the run re-key, T002 the rest of the unified record, T003 the
eleven consumers, T004 the classic runner, T005 the reachability test and the
cluster deletion, which is never split.

## Current Step

The `state` collapse, move one. `JobPlan` spells the lifecycle field `status:
str` while the classic `Job` already spells it `state: RunState`, and the two
vocabularies differ in both directions: `blocked` and `stopped` have no `RunState`
member. This round widens `RunState` with those two, pins the coverage with a
test that is red at its own base, and rules the whole collapse as DECISION F272
D5 so the next round can execute it in one atomic move. It also records DECISION
F272 D4, which rules that `job_id` stays the one required key of a job record.

## Next Steps

1. The collapse itself: replace `JobPlan.status: str` with `state: RunState`
   across every call site in ONE commit, exporting `job.state.value` into the
   unchanged `"status"` JSON key so records already on disk load unchanged.
2. The Mission extension — the order, the contract, the mission plan and the
   ordered job references.
3. T003, the eleven consumers named under Design in `T2_F260.md`, one per commit
   where the diff allows, each with a test that proves it works on a job created
   through the ping-pong path.
4. T004, the classic runner and the resolver collapse; then T005, the
   reachability test and the cluster deletion, which is never split.

## Risks

- Widening an enum is safe only while nothing enumerates it; that was measured
  at `b5cde726` and must be re-measured before any further member is added.
- The collapse cannot be staged by caller: an intermediate commit would leave
  both spellings alive and the suite red, so it is one commit or none.
<<<END PLANF272R8>>>

<<<BEGIN RECORDR8>>>
Gate: F272 R7 — the F272 round 7 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER RATHER THAN READ. Range `df955058`..`b5cde726`, eight commits, every one single-parent, in exactly the bundle's ordered sequence C0a, C0b, C1, C2, C3, C4, C5, C6 with nothing added, dropped or reordered; `git diff --name-status` over the range lists exactly the eight paths the block's change set enumerates and no other. G1 TRANSPORT: `.agent/authored/f272-r7.md` and `.agent/last_block.md` are both 29940 bytes and both hash to `e2b406be6fcbcf7cc55d19c2f5dc42976c955df56c1ca7d0896f9b8a86e956a1`; per §3 item 37 that chain covers the saved copy and its mirror and is not a claim about the bytes emitted into a prompt. G2 THE RECORD reproduces byte for byte: `.agent/live_review.md` 1088550 to 1097162 and `.agent/prose_slips.md` 134816 to 135900, both with the pre-image a byte-exact prefix, `post == pre + NL + slice` TRUE, reader (b) accepting with N counted at 2 from each slice's own paragraphs and units 694 to 696 and 171 to 173; registrations 302 to 303, resolutions 247 unchanged, open set BY DISTINCT ID 55 to 56, `^Gate: ` 28 to 29 and `^Gate: F272 R6 ` 0 to 1. G3 THE PLAN is 2401 bytes byte-equal to its slice at 47 lines against the cap of 50. G4 THE FIELDS: importing the SHIPPED `packages.orchestration.pingpong_job` from `/home/decodeux/Repos/remedy/packages/orchestration/pingpong_job.py`, all eight of `mission`, `user_prompt`, `project_id`, `intake`, `flight_plan`, `artifacts`, `budget` and `fences` are in `JobPlan.__dataclass_fields__`, with the non-vacuity controls `run_refs` TRUE and `no_such_administrative_field` FALSE, and all eight survive `_import_job(json.loads(json.dumps(_export_job(plan))))` including the Pydantic-valued three. G5 THE MUTATION RED-PROOF REPRODUCED EXACTLY, in a disposable worktree at `7cb6652e`: unmutated control EXIT 0 at 8 passed, then each of the eight export lines deleted one at a time — every byte string occurring exactly once in that file — giving EXIT 1 for all eight, each naming its own field, at 3 failed and 5 passed for the five plain fields and 4 failed and 4 passed for the three model-valued ones, with the control EXIT 0 again after every restore and the file byte-identical at the end. THE REVIEWER ADDED A SPOT-CHECK OF ITS OWN CHOOSING (§4 item 3), BECAUSE G5 AS ORDERED MUTATED ONLY THE EXPORT HALF OF THE WIRING: deleting the IMPORT read for `mission`, for `artifacts` and for `budget` in the same worktree each gave EXIT 1 at 2 failed and 6 passed, naming the field, with the control EXIT 0 before and after — so both halves of the persist/resume path are pinned, not just the writer. G6 THE SUITES, re-run serially by the reviewer: the new file EXIT 0 at 8 passed, `tests/orchestration/` EXIT 0 at 12817 passed and 10 skipped in 745.77s, `tests/cli/` EXIT 0 at 1537 passed in 304.02s, and the canary EXIT 0 at 42 passed; against the reviewer's own `df955058` readings that is a rise of exactly 8 in `tests/orchestration/`, which is the eight tests C5 adds and nothing else, with skips unchanged at 10 and no count falling anywhere. G7 EXIT 0 at `All checks passed!` over the two changed files and EXIT 0 with `"passed": true` and `"fail_count": 0` over 5 checks. G8 THE TREE: `git status --porcelain` EMPTY, `git ls-files .remedy-wt` EMPTY, every commit single-parent, and the per-commit insertion counts 367, 272, 24, 8, 31, 23 and 210 each under the DECISION F104 D1 cap of 500 and each matching the handback's `## Commits` table cell for cell, including the full-file rewrite of `.agent/last_block.md` where the file's 367 lines and the diff's 272 correctly diverge. THE WORKER'S DEVIATION 1 IS UPHELD IN FULL AND IS AGAIN THE ROUND'S MOST VALUABLE OUTPUT. It declined to meet gate G4(iii) as literally worded, measured why, and reported both readings; the reviewer reproduced the measurement independently — `_import_job({})` raises `KeyError('job_id')` at `b5cde726`, and the base blob `df955058` carries the same required subscript `job_id=data["job_id"]` at its line 741 — so the gate could not have passed on any commit of this feature and no edit inside the round's change set could make it pass. The design question it raises is RULED, not left open, as DECISION F272 D4 in `docs/roadmap/features/T2_F272.md`: `job_id` stays the one required key. Deviation 2, the block's "the two mutable ones (`artifacts`)" standing over a list of one, is a reviewer-prose inaccuracy that left nothing wrong on disk and the worker applied the enumeration; it is the §3 item 16 class and spends no id. Deviations 3, 4, 5 and 6 are accepted as declared. ONE READING THE HANDBACK COULD NOT HAVE TAKEN, recorded here so it is not mistaken later for an undeclared worktree: at review time `git worktree list` additionally named `.remedy-wt/f272-r7-rev-g5` at `7cb6652e` and `.remedy-wt/f272-r8-proto` at `b5cde726`, both clean and both created at 21:22:43 on 2026-09-06, which is 34 minutes AFTER the handback commit `b5cde726` was written at 20:48:31 — so they are an interrupted REVIEWER session's scratch and not the worker's, the handback's G8 sentence was true when written, and the reviewer removed both by exact path and pruned before this verdict.

Recurrence: R-0819 — SECOND INSTANCE, inside the very block that registered the first. The defect is the REVIEWER'S. R-0819 records a gate over production code ordered without being run at its base, and its fix clause names the general counter-measure in as many words: "RUN IT AT THE BASE BEFORE ORDERING IT ... §3 item 12 and finding R-0364 already require a gate to be executed at its base before it is ordered, and this block did not do it for G4(iii)." The F272 round 7 block, which is the block that authored and applied that very sentence at its own C2, then ordered its OWN gate G4(iii) — "`_import_job({})` returns without raising and its fields from that table equal a bare `JobPlan()`'s" — without running it at `df955058` first, and item 3 of its C5 spec carried the same unmeetable clause. MEASURED INDEPENDENTLY BY THE REVIEWER: `_import_job({})` raises `KeyError('job_id')` at `b5cde726`, and the base blob at `df955058` carries `job_id=data["job_id"]` at line 741, so the reading was identical before this round's code existed and the gate was unmeetable on every commit of the feature. NO NEW ID IS MINTED, per §3 item 30: the reviewer searched the open set for the DEFECT rather than for an id, found R-0819 describing it in as many words, and a second id would give one defect two things to resolve, two things to carry forward and two chances to fix it half-way. WHAT THIS INSTANCE ADDS, and it is the reason it is worth a paragraph rather than a prose slip: the first instance was a rule that had not yet been written down, and this one is a rule the SAME BLOCK was writing down while breaking it, which is the rule-in-a-finding-body class of R-0548 and R-0694 arriving at its sharpest — a fix clause labelled binding on the next block bound nothing even against the block that authored it, because the clause was written into the record at C2 and the gates it should have governed were written into the same file above it. THE COUNTER-MEASURE IS THEREFORE STRENGTHENED FROM A CLAUSE TO A SEQUENCE, and this block is the first to perform it: the reviewer runs every gate of the block at the base commit BEFORE the block is emitted, and writes the base reading INTO the gate beside the expected one, so a gate that cannot discriminate is visible on the page rather than discoverable only by a worker who declines to comply. This block's G4 carries its `b5cde726` base reading — `blocked` and `stopped` FALSE, the other four TRUE — for exactly that reason. R-0819 STAYS OPEN; this recurrence does not resolve it, and its original text is not rewritten.
<<<END RECORDR8>>>

<<<BEGIN DECISIONR8>>>
### DECISION F272 D4 (2026-09-06, F272 round 7) — `job_id` stays the ONE required key of a job record, and the round 7 gate that said otherwise was the thing that was wrong

CONTEXT. F272 round 7's gate G4(iii), and item 3 of the same block's C5 spec,
ordered `_import_job({})` to return a `JobPlan` and not raise. It raises
`KeyError('job_id')`, because `_import_job`'s first argument is
`job_id=data["job_id"]` — a required subscript and not a `.get`. Measured at
`b5cde726` and at the base blob `df955058`, where the same line stands at line
741: the reading is identical before and after the round, so no edit inside that
round's change set could have satisfied the gate.

CHOSEN. `job_id` REMAINS A REQUIRED KEY. A job record without an id is not
addressable: `load_job_plan(job_id)` is keyed by it and the record's own
directory is named by it, so a record that loads without one is a job detached
from its own file. The eight administrative fields of round 7 all default,
because they are FIELDS; `job_id` is the KEY, and a key with a default is not a
key. `tests/orchestration/test_job_administrative_fields.py::test_job_id_stays_the_one_required_key`
pins this and goes red if it ever becomes optional.

ALTERNATIVES CONSIDERED. Default it to a freshly minted id — rejected: the
record would be written to and read from a directory no caller can name, so a
corrupt record silently becomes a new and unreachable job. Default it to `""` —
rejected: every path built from it collapses onto the jobs root, which is worse
than raising. Make the whole import tolerant of an empty dict — rejected: that
is a different feature, it is not what D1 asks for, and it would hide exactly
the corruption this subscript surfaces.

CONSEQUENCE. The round 7 deviation that declined the gate is upheld; the gate
text was wrong and the code was right. No production line changes under this
decision.

REVERSE by deleting this section and the named test, at which point `job_id`'s
requiredness returns to being an undocumented property of one subscript.

### DECISION F272 D5 (2026-09-06, F272 round 8) — the `state` collapse widens `RunState` first, then replaces `status` in ONE atomic move

CONTEXT. DECISION F260 D1's eleventh administrative name is `state`. The classic
`Job` (`packages/core/models.py:222`) already spells it `state: RunState` at line
231; `JobPlan` (`packages/orchestration/pingpong_job.py:305`) spells it `status:
str = JOB_PLANNED`. Measured at `b5cde726`, the two vocabularies differ in both
directions: `JobPlan`'s six `JOB_*` values are `planned`, `running`, `blocked`,
`completed`, `paused` and `stopped`, while `RunState` carries `pending`,
`planned`, `running`, `paused`, `completed`, `failed` and `cancelled`. `blocked`
and `stopped` have no member, so a rename alone would lose two states.

CHOSEN, IN TWO ROUNDS. Round 8 widens `RunState` with `BLOCKED = "blocked"` and
`STOPPED = "stopped"` and pins the coverage with a test that is red at its own
base. That widening is a pure addition: measured at `b5cde726` over `packages/`,
`apps/` and `tests/`, nothing enumerates the enum — no `list`, `len`, `set` or
`tuple` of it, no iteration over it, no `match`/`case` on it and no dict keyed by
its members — so no exhaustive reader can break. Round 9 then replaces
`JobPlan.status: str` with `state: RunState` across every call site in ONE
commit; measured at `b5cde726`, `job.status` together with the six `JOB_*`
constants occurs 337 times across 33 files, which is inside the DECISION F104 D1
cap of 500 insertions for a single commit.

THE ON-DISK KEY DOES NOT MOVE. Round 9's `_export_job` writes `job.state.value`
into the existing `"status"` JSON key and `_import_job` reads `RunState` back out
of it, so every job record already written loads unchanged. This decision renames
a PYTHON FIELD, not a record format; changing the stored key as well would be a
migration and is deliberately not ordered.

ALTERNATIVES CONSIDERED. Map `blocked` and `stopped` onto the existing `FAILED`
and `CANCELLED` instead of widening — rejected: `blocked` is a recoverable state
that `job_promote` and the repair path both act on while `failed` is terminal,
and `stopped` is an operator action `apps/cli/commands/job_stop_cmd.py` exists to
record, so the map would erase two distinctions the code already makes. Keep
`status` and add `state` beside it — rejected outright by AGENTS.md's Scope
Control, "Replacing is deleting": two spellings for one concept is the exact
defect F272 exists to remove. Split round 9 by caller or by file — rejected:
every intermediate commit would leave both spellings alive and the suite red, so
no honest gate could be written for it; it is one commit or none.

CONSEQUENCE. `RunState` gains two members and nothing else changes in round 8.
Round 9 becomes a mechanical rename with a vocabulary that already covers every
value it must carry.

REVERSE by deleting this section, removing the two `RunState` members and
`tests/orchestration/test_run_state_covers_job_status.py`, at which point `state`
returns to D1's one-line description and `JobPlan` keeps `status: str`.
<<<END DECISIONR8>>>

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md:
`SESSION 4 of feature F272 · round 8`, the one-sentence context self-assessment
amend0905-throughput requires, branch, the range, a per-commit changed-files
table with real `+/-` from `git diff --numstat`, the item-status table covering
C0a through C6 with every item present exactly once, one line per gate G1 to G8
with its real exit code, the G4 readings beside the base readings this block
states, the G5 exit codes, the authored-text proof table, deviations and
assumptions, and the next expected action. There is no length cap. Per the fix
clause OPEN in the record and binding on the next block that orders a handback:
any commit you make beyond the ordered sequence receives its OWN `## Commits` row
and its OWN item-status row, and the Deviations section says so in those same
words rather than beside a clause that denies it.
