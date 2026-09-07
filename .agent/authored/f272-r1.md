── STEP T001 (part 1) — F272 ─────────────────────────────────
Goal:        Claim F272 on a new branch, re-head the review record, and give the
             job record the PLURAL run list DECISION F260 D1 names and nothing
             on disk carries yet: `JobPlan.run_refs`, the ordered ids of the
             runs one job produced, persisted and populated where a task's run
             is recorded.
Bundle:      C0a save this block · C0b mirror it · C1 plan + context · C2 the
             record re-head · C3 the STATUS claim · C4 the `run_refs` field,
             its persistence and its population · C5 the tests · C6 the handback
(the rule line above is 61 copies of U+2500 followed by nothing, per §3 item 37;
every other rule line in this block is the same 61 copies)
─────────────────────────────────────────────────────────────

## Before anything: the branch

The Open PR Gate has ALREADY RUN in the reviewer's session. Pull request 242 was
merged with `gh pr merge 242 --merge --delete-branch`, the merge commit is
`b18fad576252f7f2739a5807b6408031da8fcde6`, `main` was pulled to it, and
`gh pr list --state open` returns an empty list. DO NOT re-run the gate and DO
NOT merge anything this round. F260's round 24 terminator verdict is on pull
request 242 and in `.agent/handoff.md` (§4 item 13); NO `Gate: R24` paragraph is
ever written to `.agent/live_review.md`.

Start on `main` at `b18fad57` with a clean tree, then:

    git checkout -b feature/f272-one-world-completion

Every commit of this round lands on that branch. Never work on `main` (G3).

## Change set — nothing outside this list

    .agent/authored/f272-r1.md              (new, C0a)
    .agent/last_block.md                    (C0b)
    .agent/plan.md                          (C1)
    .agent/context.md                       (C1)
    .agent/live_review.md                   (C2)
    docs/roadmap/STATUS.md                  (C3)
    packages/orchestration/pingpong_job.py  (C4)
    tests/orchestration/test_job_run_refs.py (new, C5)
    .agent/handoff.md                       (C6)

Scratch you may create freely under the gitignored `.remedy-wt/`; it must stay
untracked, and `git ls-files .remedy-wt` must return nothing at the end.

## The slices in this block

Each authored text below sits between `<<<BEGIN name>>>` and `<<<END name>>>` on
their own lines. Extract by EXACT-POSITION marker matching, asserting exactly one
BEGIN and one END per name; the marker lines never reach any file. The whole-file
texts are PLANF272R1 and CONTEXTF272; the FROM/TO pairs are HEAD1, STEPS, STATUS.

## C0a — save this block

This block is on disk at `.remedy-wt/f272-r1-block.md`. The prompt that
delegated this round states that file's sha256; call it BLOCK_SHA. A file cannot
carry its own digest, so BLOCK_SHA is named there and never here. VERIFY the
source file against BLOCK_SHA BEFORE executing anything else in this block.

COPY that file to `.agent/authored/f272-r1.md` with `shutil.copyfile` — never a
retype, never a text round-trip — and commit it alone.

## C0b — mirror

Copy the same bytes to `.agent/last_block.md` with `shutil.copyfile` and commit
it alone. This is one indivisible `.agent/**` state rewrite (AGENTS.md DECISION
F104 D1 exemption), so its insertion count is not split.

## C1 — plan and context

Write `.agent/plan.md` from the PLANF272R1 slice and `.agent/context.md` from
the CONTEXTF272 slice, each byte-for-byte plus exactly one trailing newline, and
commit the two together. This is the round's FIRST substantive commit, because a
round that touches `.agent/` state advances the plan first
(planner_reviewer_prompt.md §3 item 23).

## C2 — the record re-head

Apply the HEAD1 pair and the STEPS pair to `.agent/live_review.md` and commit.
Both are REWRITES — the containment readings are in constraint 3 — so each FROM
occurs exactly once before and zero times after, and each TO exactly once after.
NOTHING BELOW `## Findings` MAY CHANGE BY ONE BYTE. No finding is registered,
resolved or renumbered this round, and no `Gate:` paragraph is appended: F260's
terminator has none by construction, and this round's own verdict is written by
the NEXT round's first commit.

## C3 — the STATUS claim

Apply the STATUS pair to `docs/roadmap/STATUS.md` and commit it alone. `README.md`
is NOT touched: its counters count `[x]` lines, and a claim changes none of them.

## C4 — the plural run list

Three edits to `packages/orchestration/pingpong_job.py` and NO other file. Each
anchor below was counted by the reviewer in that file at `b18fad57` and occurs
EXACTLY ONCE. Read the surrounding function before editing, per AGENTS.md.

(a) THE FIELD. In the `JobPlan` dataclass, immediately AFTER the line

        tasks: list[TaskEntry] = field(default_factory=list)

insert these six lines, at that same indentation:

        # F272 T001, DECISION F260 D1: a Job has MANY runs. The ordered ids of
        # the runs this job produced, oldest first and each exactly once. F260
        # closed with a record that could name only the one run of each task;
        # this list is what makes a job able to name its runs at all, and it is
        # the prerequisite for re-keying the run directory by RUN id.
        run_refs: list[str] = field(default_factory=list)

(b) THE PERSISTENCE. In `_export_job`, insert `"run_refs": job.run_refs,` on its
own line immediately AFTER the line `        "budgets": job.budgets,`. In
`_import_job`, insert `run_refs=list(data.get("run_refs") or []),` on its own
line immediately AFTER the line `        budgets=data.get("budgets"),`, which is
a keyword argument of the `JobPlan(...)` construction there.

(c) THE POPULATION. In `run_job`, immediately AFTER the line

            task.run_id = result.run_id

insert exactly:

            if result.run_id and result.run_id not in job.run_refs:
                job.run_refs.append(result.run_id)

Commit C4 alone.

## C5 — the tests

Create `tests/orchestration/test_job_run_refs.py` and commit it alone. It holds
exactly these four tests, and nothing else:

1. `run_refs` defaults to an empty list, and two freshly constructed `JobPlan`
   objects do NOT share one list object — the `default_factory` property.
2. `_export_job` then `_import_job` round-trips a `JobPlan` whose `run_refs`
   holds two ids, and the imported list is EQUAL and IN THE SAME ORDER. Follow
   the shape `tests/orchestration/test_job_budgets.py` already uses for a
   persisted field.
3. A job record written with NO `run_refs` key imports as an empty list rather
   than raising — the defaulted-field reading, not a compatibility reader.
4. THE ONE THAT MATTERS. Drive the real grouped CLI end to end with the
   deterministic fake providers over a job file holding TWO tasks, then load the
   job back and assert that `run_refs` equals `[t.run_id for t in job.tasks]` —
   same ids, same order, length 2, no duplicates, every id 16 hex characters.
   Copy the harness shape from `TestJobFlowEndToEnd` in `tests/test_do_job_flow.py`:
   `REMEDY_DATA_DIR` monkeypatched to a `tmp_path` directory, a demo repo, a job
   file with `## Task 1` and `## Task 2` headings, and

       grouped_main(["do", "job-flow", "--job-file", <jf>, "--repo", <repo>,
                     "--builder", "fake", "--reviewer", "fake",
                     "--out", <evidence>, "--json"])

   reading `job_id` out of the JSON on stdout and `load_job_plan(job_id)` back.
   The reviewer ran exactly this harness at `b18fad57` in the primary checkout
   and in a fresh worktree: 2 tasks, two distinct 16-hex run ids, report status
   `completed`, 0.89s and 0.80s. THE TEST MUST WRITE NOWHERE BUT ITS `tmp_path`.

## C6 — the handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md and commit it
last. It carries the mandated sections, the item-status table for C0a to C6, one
line per gate with REAL exit codes, and the SESSION NUMBER line: this is
**SESSION 1 of feature F272**, round 1. It has NO length cap (amend0827 rule 3).
Do NOT state C6's own insertion count or the number of any commit after C5 — the
reviewer measures those at the gate (§3 items 14 and 31).

## Constraints

1. Every slice is applied BYTE FOR BYTE. Believing one wrong does not license
   editing it; apply it and declare it.
2. The change set above is exhaustive. Touch no other tracked file. In
   particular: `README.md`, `docs/roadmap/features/T2_F272.md` and
   `docs/roadmap/features/T2_F260.md` are NOT edited this round.
3. PAIR SHAPES, measured by the reviewer at `b18fad57` with a containment test
   and reported as that test's own output, one reading per pair:
   HEAD1 — `TO contains FROM: false` — REWRITE.
   STEPS — `TO contains FROM: false` — REWRITE.
   STATUS — `TO contains FROM: false` — REWRITE.
   Every pair is therefore proved with the FROM-zero reading, and none of them
   with the §4 item 9 append obligation.
4. NO FINDING ID IS MINTED, RESOLVED OR RENUMBERED. The open set is 298 BY
   DISTINCT ID at `b18fad57` and must be 298 after C2. The next free id is
   R-0818; this round does not spend it.
5. COMMIT ORDER IS C0a, C0b, C1, C2, C3, C4, C5, C6, each its own commit, each
   single-parent, nothing after C6.
6. Every gate below runs at a commit STRICTLY EARLIER than C6, so the handback
   can quote it (§3 item 31). Where a gate names a commit, that is the commit it
   runs at.
7. This session's shell guard refuses `python3 <script>` followed by
   `echo "EXIT=$?"`, and refuses shell loops and `$(...)`. Read every exit code
   from `subprocess.run(...).returncode` inside a Python file under
   `.remedy-wt/`, never from a shell word. Bare `ruff` is DENIED; the spelling
   that runs is `python3 -m ruff check <path>`.
8. DESTRUCTIVE VERIFICATION — the G7 red proof only — runs in a DISPOSABLE
   `git worktree` and never in the primary checkout, which satisfies
   `git status --porcelain` empty at the handback (self_drive_protocol.md G5).
   Remove and prune that worktree before C6.
9. NOTHING IS MERGED and no pull request is created this round. `gh pr merge` and
   `gh pr create` are not run at all.
10. Read `.agent/STOP` from disk with `os.path.exists` before C0a, before C4 and
    before C6, and report all three readings. If it exists at any of those
    points, finish the commit in flight, write the handback and stop.
11. THIS BLOCK'S OWN SIZE, measured by the reviewer on these final bytes:
    PROSE 314 lines against the 400-line cap of DECISION F105 D5, and TOTAL 488
    lines against the 490-line budget of DECISION F085 D6 (ruled figure 490, per
    its own correction). Re-measure BOTH from the committed
    `.agent/authored/f272-r1.md` and report both; a disagreement is drift.

## Done when — the gates

Run each gate and record its REAL exit code and REAL output. "Green" as a word
is a finding (self_drive_protocol.md G4).

**G1 TRANSPORT.** `.remedy-wt/f272-r1-block.md`, the committed
`.agent/authored/f272-r1.md` at C0a and the committed `.agent/last_block.md` at
C0b are byte-identical: report the one sha256 and the one byte length, and the
`filecmp.cmp(shallow=False)` reading for source-vs-saved and source-vs-mirror.
That digest must equal BLOCK_SHA from the delegating prompt.

**G2 THE RECORD**, at C2. (a) BYTE: the post-image equals the pre-image with the
HEAD1_FROM span replaced by HEAD1_TO and the STEPS_FROM span replaced by
STEPS_TO and nothing else — prove it by reconstructing the file INDEPENDENTLY
from the pre-image with only those two replacements applied and comparing the
reconstruction to the committed bytes. Report bytes before and after, and that
the file ends in exactly one newline. (b) THE CARRIED REGION: the bytes from and
including the line `## Findings` to end of file hash to
`147ce009557d42bc81def2249853ed1a8fccd60676077a08e9532aea0bc0f8dc` and are
`953408` bytes long BOTH before and after — that is the reviewer's reading at
`b18fad57` and it must be unchanged. (c) COUNTS before → after: distinct ids
matching `^- R-\d{4} — ` 301 → 301, distinct ids matching `^Done: R-\d{4} — `
3 → 3, open set BY DISTINCT ID 298 → 298, and `^Gate: ` 23 → 23. (d) NEGATIVE
CONTROL, in memory on a `bytes` object and NEVER on disk: flip one byte inside
the FIRST replaced span (HEAD1_TO) and report that reader (a) REJECTS it, then
restore and report that it ACCEPTS again and the restored image equals the disk
image.

**G3 THE PLAN AND THE CONTEXT**, at C1. `.agent/plan.md` equals PLANF272R1 plus
exactly one trailing newline, and `.agent/context.md` equals CONTEXTF272 plus
exactly one trailing newline — report both byte lengths and both equalities.
`.agent/plan.md` line count is under the AGENTS.md cap of 50, and it carries
`## Goal` and `## Next Steps`. Then the four state readers, run SERIALLY:
`python3 -m pytest tests/ui_server/ -q -p no:randomly` (515 passed at the base),
and `python3 -m pytest tests/orchestration/test_test_runner.py
tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
-q -p no:randomly` (89 passed at the base). Both exit 0.

**G4 THE STATUS CLAIM**, at C3. `^- \[~\] F272 — ` occurs exactly 1 time and
`^- \[ \] F272 — ` exactly 0 times; `^- \[x\] F\d{3} — ` is still 74 and
`^- \[[ x~!]\] F\d{3} — ` is still 272; `^- \[~\] F\d{3} — ` over the whole file
is exactly 1, which is the at-most-one-claim invariant
`tests/docs/test_docs_consistency.py` pins. `git diff --name-only` over C3 is
exactly `docs/roadmap/STATUS.md`. Then
`python3 -m pytest tests/docs/ -q -p no:randomly` (303 passed at the base) and
`python3 -m pytest tests/orchestration/test_roadmap_index.py -q -p no:randomly`
(30 passed at the base), both exit 0.

**G5 THE CODE**, at C4. `python3 -m ruff check
packages/orchestration/pingpong_job.py` exits 0 — it did at the base. Read the
SHIPPED dataclass rather than the source text: construct two `JobPlan()` objects
and report that `run_refs` is `[]` on both and that they are NOT the same list
object. Report the number of occurrences of the string `run_refs` in the file,
which was 0 at `b18fad57` and must now be at least 4. `git diff --name-only`
over C4 is exactly `packages/orchestration/pingpong_job.py`.

**G6 THE NEW TESTS**, at C5. `python3 -m pytest
tests/orchestration/test_job_run_refs.py -q -p no:randomly` exits 0; report the
passed count, which must be 4. Then the two suites this change is most likely to
disturb, run SERIALLY: `python3 -m pytest tests/test_do_job_flow.py -q
-p no:randomly` (178 passed at the base) and `python3 -m pytest
tests/orchestration/test_job_budgets.py -q -p no:randomly` (135 passed at the
base), both exit 0 and both at their base counts or higher.

**G7 THE RED PROOF**, run ONLY inside a disposable worktree created at C5's
commit, never in the primary checkout. Report, in this order: (i) the UNMUTATED
CONTROL — `python3 -m pytest tests/orchestration/test_job_run_refs.py -q
-p no:randomly` inside that worktree, exit 0 with its passed count, because a
colour with no baseline is not evidence; (ii) THE MUTATION — delete the two
lines C4(c) inserted, which are the only occurrence of `job.run_refs.append` in
that file, and re-run the same command; report the exit code, the failed count
and the NAME of each failing test. The end-to-end test of C5 item 4 must be
among them. (iii) `git -C <worktree> diff --name-only` after the deletion, to
show exactly which file was mutated. Then `git worktree remove --force` it and
`git worktree prune`, and report `git worktree list` afterwards. If the CONTROL
is not exit 0, the proof is VOID: report that instead of a colour and do not
mutate anything.

**G8 THE CANARY, INTEGRITY AND THE TREE**, run in the primary checkout after C5
and BEFORE C6 is staged. `python3 -m pytest tests/cli/test_golden_path.py -q
-p no:randomly` exits 0 at 42 passed. `python3 -m apps.cli.grouped integrity
check --json` exits 0 with `"passed": true` and `"fail_count": 0`.
`git status --porcelain` is EMPTY and `git ls-files .remedy-wt` returns nothing.
Report, per commit and for C0a through C5 ONLY, the `git diff --numstat
<parent> <commit>` INSERTION count — the column AGENTS.md DECISION F104 D1 caps
at 500, never insertions plus deletions — and that each commit is single-parent.
Report the count of lines beginning with the BEGIN or END marker prefix in each
of `.agent/plan.md`, `.agent/context.md`, `.agent/live_review.md`,
`docs/roadmap/STATUS.md`, `packages/orchestration/pingpong_job.py` and
`tests/orchestration/test_job_run_refs.py`; each must be 0.

<<<BEGIN PLANF272R1>>>
# Plan — F272 One world completion

Branch: feature/f272-one-world-completion, cut from `main` at
`b18fad576252f7f2739a5807b6408031da8fcde6`, the merge commit of pull request
242. F260 is accepted; this feature carries the scope DECISION F260 D8 split
off it, and its Acceptance list IS F260's, unchanged.

## Goal

Finish what F260 began: a Job that carries MANY runs, every consumer on the
unified model, and the classic runner, its resolver and the prototype cluster
deleted. Task slicing per `docs/roadmap/features/T2_F272.md` — T001 the plural
run list and the run re-key, T002 the rest of the unified record, T003 the
eleven consumers, T004 the classic runner, T005 the reachability test and the
cluster deletion, which is never split.

## Current Step

Round 1 claims F272 in the roadmap ledger, cuts the branch, re-points this file
and `.agent/context.md`, re-heads `.agent/live_review.md`, and lands the FIRST
half of T001: `JobPlan.run_refs`, the ordered ids of the runs one job produced,
persisted through the job record and populated where a task's run is recorded,
with the tests that prove it on a job created through the ping-pong path.

## Next Steps

1. The run re-key: `run_log_dir` and `pingpong_run_dir` collapse onto the one
   `run_dir` keyed by RUN id, together with the test-side spelling sweep
   DECISION F260 D6 declined and this feature inherits. `run_refs` lands first
   because a reader needs a job able to name its runs before the directory
   stops being keyed by the job.
2. The rest of the unified record: the eleven administrative fields and the
   Mission extension (T002).
3. The eleven consumers named under Design in `T2_F260.md`, one per commit
   where the diff allows (T003).

## Risks

- The re-key consumes its own observer: the tests that hand-spell the old path
  are the only reason such a round can go red at all, so the sweep needs its
  pre-sweep and post-sweep pair rather than one commit.
- `<data_root>/runs/` is occupied today by the job-keyed run log, so both
  function bodies must move together or two directories merge under one key.
<<<END PLANF272R1>>>
<<<BEGIN CONTEXTF272>>>
# Context — F272 One world completion

## Active Branch
feature/f272-one-world-completion, cut from `main` at
`b18fad576252f7f2739a5807b6408031da8fcde6`, the merge commit of pull request 242.

## Scope
F272 (Tier 2; depends on F259's binding vocabulary page and on the record F260
closed at; blocks F261, F266, F268, F269, F270, F271 and F263): the scope
DECISION F260 D8 split off F260 at the seven-session soft limit. Task slicing
per `docs/roadmap/features/T2_F272.md`: T001 the plural run list and the run
re-key, T002 the rest of the unified record, T003 the eleven consumers, T004 the
classic runner and the resolver collapse, T005 the reachability test and the
prototype cluster deletion.

## Do not touch
Everything `T2_F260.md`'s "Do not touch" section names, unchanged: the
scope-fence builtin deny list (F017), the approval gate, STATUS semantics. No
command is RENAMED here — F261 owns renames. No module outside F260's Design
lists is deleted, and a module that turns out to be reachable is reported with
its import chain, never deleted.

## Assumptions
- Cleanliness before compatibility (DECISION D-A): no migration shim, no
  compatibility reader, no alias. Old `.data` content is deleted by the
  developer, not converted.
- F260's rulings D-A, D0, D1, D2, D4, D5, D6 and D7 stay binding here and are
  NOT restated; `docs/roadmap/features/T2_F260.md` keeps its Goal, Design,
  T-slice and Acceptance sections unedited for exactly that purpose.
- NEVER SPLIT INSIDE T005. A session reaching its own limit splits between T003
  and T004, or before T005, and never within it.

## Constraints
The bullets in this first group are STANDING project constraints, carried
forward from the context this file replaces.

- A round touching `docs/roadmap/**` also gates
  `tests/orchestration/test_roadmap_index.py` beside `tests/docs/`.
- A round rewriting `.agent/` state gates the four state readers:
  `tests/ui_server/`, `tests/orchestration/test_test_runner.py`,
  `tests/regression/test_resource_safety.py` and
  `tests/orchestration/test_integrity_gate.py`.
- THE FOUR STATE READERS ARE RUN AS FOUR, NOT AS THREE.
- Every handback runs the canary `pytest tests/cli/test_golden_path.py`.
- Destructive verification runs only inside a disposable git worktree, never in
  the primary checkout, which satisfies `git status --porcelain` empty at every
  verdict.
- Bare `ruff` is DENIED to this session's shell; `python3 -m ruff check <path>`
  runs and exited 0 over `packages/orchestration/pingpong_job.py` when the
  reviewer measured it at `b18fad57`. That spelling is the one every gate of
  this feature orders.
- `remedy` (the built CLI) is DENIED to this session's reviewer session-wide,
  subagents included; a round needing it delegates the run to the worker and
  reports the exact output.
- This session's shell guard refuses some command FORMS outright — shell loops,
  `$(...)` substitution, and `$?` inside a compound command — so checks of that
  shape are re-expressed in Python and the re-expression is reported.

This feature is NOT UI work — no design-reference binding applies.

## Steps
The item-status table for each round lives in that round's handback,
`.agent/handoff.md`, which AGENTS.md's "Completion Report — Item-Status Table"
section requires of every completion report. This file deliberately does not
restate it.
<<<END CONTEXTF272>>>
<<<BEGIN HEAD1_FROM>>>
# Live Review — F260 One world: mission → job → run

> Round-by-round review record, re-headed at the F260 claim per
> docs/agents/planner_reviewer_prompt.md §1. The heading this replaces named
> F259, which is accepted: its STATUS line went `[x]` at `1e7ecf90` and its pull
> request 240 merged at `b5cd6c20`. Only the heading and this paragraph are
> rewritten. Every finding record below `## Findings` is carried forward
> BYTE-IDENTICAL — the block that ordered this re-head gates that region's
> sha256 equal before and after the edit, as its gate G2(d) — and finding ids
> continue the monotonic R-XXXX series across the re-head. Measured by the
> reviewer at `b5cd6c20`, the branch point: 298 lines matching `^- R-\d{4} — `
> against 4 matching `^Done: R-\d{4} — `, so 294 findings are open, and the
> maximum id in use is R-0813 — the next id this feature mints is R-0814.
> Records belonging to features already marked `[x]` in docs/roadmap/STATUS.md
> are not here at all: `scripts/rotate_live_review.py` moves them byte-verbatim
> into the append-only `.agent/live_review_archive.md` in every closure
> sequence, under operator amendment amend0905-throughput, and that archive is
> read on demand by id, never at session start.
<<<END HEAD1_FROM>>>
<<<BEGIN HEAD1_TO>>>
# Live Review — F272 One world completion

> Round-by-round review record, re-headed at the F272 claim per
> docs/agents/planner_reviewer_prompt.md §1. The heading this replaces named
> F260, which is accepted: its STATUS line went `[x]` at `f5beb700` and its pull
> request 242 merged at `b18fad57`. Only the heading, this paragraph and the
> `## Steps` section below are rewritten. Every finding record below
> `## Findings` is carried forward BYTE-IDENTICAL — the block that ordered this
> re-head gates that region's sha256 equal before and after the edit, as its
> gate G2(b) — and finding ids continue the monotonic R-XXXX series across the
> re-head. Measured by the reviewer at `b18fad57`, the branch point: 301
> DISTINCT ids matching `^- R-\d{4} — ` against 3 DISTINCT ids matching
> `^Done: R-\d{4} — `, so 298 findings are open BY DISTINCT ID, and the maximum
> id in use is R-0817 — the next id this feature mints is R-0818.
> F260's LAST round has no entry here and never will:
> docs/agents/planner_reviewer_prompt.md §4 item 13 makes a branch
> terminator's verdict live in `.agent/handoff.md`, in the reviewer's
> completion report and in the pull request, where the reviewer wrote it before
> merging 242; that absence is the terminator and not a missing gate.
> Records belonging to features already marked `[x]` in docs/roadmap/STATUS.md
> are not here at all: `scripts/rotate_live_review.py` moves them byte-verbatim
> into the append-only `.agent/live_review_archive.md` in every closure
> sequence, under operator amendment amend0905-throughput, and that archive is
> read on demand by id, never at session start.
<<<END HEAD1_TO>>>
<<<BEGIN STEPS_FROM>>>
R1 claim F259 in the roadmap ledger, cut the branch, re-point `.agent/plan.md`
and `.agent/context.md`, re-head this record, book the reviewer's `Done: R-0797`
from the F262 branch, and put the T001 source inventory on disk — per word of
DECISION amend0905-vocab D1, the spelling the code really uses today, read from
the seven modules T2_F259.md names and from the shipped command catalog, with
every claim carrying the `path:line` it was read at → R2 the page's D1 table,
written from that inventory → R3 the do-not-confuse table, the Mermaid diagram
and its short description, completing T001 → R4 D2–D10 and F259 D1/D2 onto the
page, T002 → R5 `tests/docs/test_vocabulary.py` in planned mode with both red
proofs, T003 → R6 the README diagram and the docs index registration, T004 →
the integration gate → the closure sequence.
<<<END STEPS_FROM>>>
<<<BEGIN STEPS_TO>>>
R1 claim F272 in the roadmap ledger, cut the branch, re-point `.agent/plan.md`
and `.agent/context.md`, re-head this record, and land the first half of T001 —
`JobPlan.run_refs`, the ordered ids of the runs one job produced, persisted
through the job record and populated where a task's run is recorded → the run
re-key, `run_log_dir` and `pingpong_run_dir` collapsing onto the one `run_dir`
keyed by RUN id, with the test-side spelling sweep DECISION F260 D6 declined
and this feature inherits → the rest of the unified record, T002 → the eleven
consumers named under Design in T2_F260.md, T003 → the classic runner and the
resolver collapse, T004 → the reachability test, the two carry-overs, DECISION
F260 D3 and the prototype cluster deletion, T005, which is never split → the
integration gate → the closure sequence.
<<<END STEPS_TO>>>
<<<BEGIN STATUS_FROM>>>
- [ ] F272 — One world completion — the run re-key, the consumers, the classic runner and the cluster deletion
<<<END STATUS_FROM>>>
<<<BEGIN STATUS_TO>>>
- [~] F272 — One world completion — the run re-key, the consumers, the classic runner and the cluster deletion
<<<END STATUS_TO>>>
