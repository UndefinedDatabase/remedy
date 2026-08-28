# STEP T000 — F033 Hunk-level diff approval, round 1 — CLAIM AND INVENTORY

## Who you are and what binds you

You are the WORKER of a self-drive round (docs/agents/self_drive_protocol.md).
AGENTS.md is the highest authority and nothing here weakens it. You are the only
actor in this round that writes anything; the reviewer re-runs every gate itself
before issuing a verdict.

BASE. This round starts on `main`, at the merge commit your Open PR Gate creates
in step 1 below. Read `.agent/STOP` from disk before your first commit; if it
exists, write the handback and end without doing anything else. Read it again
before your last commit.

SESSION. Session 1 of feature F033, round 1. Carry
"SESSION 1 of feature F033 · round 1 · rounds so far 1" in the handback.

WHAT THIS ROUND IS. The feature claim and the source inventory. It merges F037's
pull request, cuts this branch, claims F033 in the ledger, resets the review
record's header carrying every finding forward, books the F037 R27 verdict the
reviewer issued this session, and puts the F033 source inventory on disk. NO
PRODUCTION CODE IS TOUCHED.

## Step 1 — the Open PR Gate, before any commit

Run these, in this order, and record every outcome in the handback:

    gh pr list --state open --json number,headRefName,baseRefName,isDraft
    gh pr merge 218 --merge --delete-branch
    git checkout main
    git pull --ff-only
    git rev-parse HEAD
    git checkout -b feature/f033-hunk-approval

The gate expects EXACTLY ONE open pull request, #218, from
`feature/f037-rendered-diff-viewer` into `main`, not a draft. If the list shows
anything else, STOP: write the handback naming what you saw and end the round.
The reviewer gated F037 R27 this session and watched that pull request's CI run
`33172259776` to completion — conclusion `success` in 25m31s, merge state
`CLEAN` — so the merge is authorised and is not a judgement you make again.

The `git rev-parse HEAD` reading taken AFTER the pull is THIS ROUND'S BASE.
Every range gate below is measured from it, and it is reported in the handback.

NEVER force-push and never rewrite history. The `--delete-branch` above is the
only branch deletion this round performs.

## Goal

Claim F033, cut its branch, carry the finding record across the reset, book the
F037 R27 verdict, and answer on disk the questions T001 cannot be planned
without.

## Bundle, in this commit order

- C0a — save this block verbatim to `.agent/authored/f033-r1.md`.
- C0b — mirror the same bytes into `.agent/last_block.md`.
- C1 — rewrite `.agent/plan.md` from the PLANF033R1 slice.
- C2 — apply the STATUSCLAIM pair to `docs/roadmap/STATUS.md`.
- C3 — apply the RECORDHEAD pair to `.agent/live_review.md` AND append
  GATEF037R27 to that same file, in ONE commit.
- C4 — write `.agent/f033_inventory.md`.
- C5 — rewrite `.agent/handoff.md`. It is the LAST commit of this round.
- Then push. No pull request is created this round.

## Change set — these paths and nothing else

- `.agent/authored/f033-r1.md` (C0a)
- `.agent/last_block.md` (C0b)
- `.agent/plan.md` (C1)
- `docs/roadmap/STATUS.md` (C2)
- `.agent/live_review.md` (C3)
- `.agent/f033_inventory.md` (C4)
- `.agent/handoff.md` (C5)

Nothing under `apps/`, `packages/` or `tests/` is touched, and no test is
edited, added, deleted or skipped. `docs/roadmap/features/T5_F033.md` is NOT
touched: this round proposes no amendment to it. `README.md` is NOT touched —
the reviewer measured at `1f0329f4` that no file under `tests/` reads the
README's `Next:` clause, and the only README figure `tests/docs/` pins is the
accepted count, which a `[ ]` to `[~]` claim does not move.

## Slice convention

The authored texts below are delimited by lines beginning `<<<SLICE ` and
`<<<END `, each naming its own label. Delimiter lines never reach a target file.
Apply each slice BYTE FOR BYTE including its trailing newline. The labels are
PLANF033R1, STATUSCLAIM, RECORDHEAD and GATEF037R27. STATUSCLAIM and RECORDHEAD
are not applied as whole texts: each CARRIES one FROM/TO pair, introduced by a
line beginning `[P`, and you apply the pair it names. The STATUSCLAIM pair and
the RECORDHEAD pair are each REWRITES — the reviewer ran the containment test on
each and each printed `TO contains FROM: false` — so each is proved by a
FROM-zero and a TO-one count after the edit, and neither carries an append
obligation.

## Constraints

1. NEVER edit, reflow, reword, retitle, correct or shorten a slice. If you
   believe a slice is wrong, apply it as written and say so in the handback's
   deviations. Only the reviewer's text may change a slice.
2. Step 1's Open PR Gate runs BEFORE C0a. Every claim the GATEF037R27 slice
   makes about that merge is therefore true at the moment C3 writes it.
3. C1 is the first substantive commit, so `.agent/plan.md` is current before any
   other content commit — AGENTS.md's Commit Gate item 1.
4. Each commit's insertions stay under 500, counting the `+` column of
   `git diff --numstat` (AGENTS.md, DECISION F104 D1). If
   `.agent/f033_inventory.md` would exceed that, split C4 into two commits at a
   whole-section boundary and declare the split in the handback.
5. Run G7's two suites SERIALLY, one pytest process at a time, from the
   repository root of the primary checkout, capturing output in memory.
6. Every mutating or destructive verification runs ONLY inside a disposable
   `git worktree` under `.remedy-wt/`, removed before the handback
   (docs/agents/self_drive_protocol.md G5). The primary checkout satisfies
   `git status --porcelain` == empty after every commit.
7. Where this session's shell guard rejects a command's FORM, re-express it — a
   `python3` heredoc is accepted — and declare the re-expression in the
   handback. Never weaken a gate, and never skip one, to fit the guard.
8. `.remedy-wt/` never enters the index: `git ls-files .remedy-wt` prints 0
   lines.

## The inventory — what C4 must answer

`.agent/f033_inventory.md` answers each question below with FILE PATHS and
SYMBOL NAMES read from disk at this round's base, quoting the code it describes
rather than summarising it. Where the answer is "nothing in this repository does
this", say exactly that — a deliberate absence is an answer, and the feature
file's Design section is a PROPOSAL rather than a description of what exists.
Number the sections 1 through 9, in this order:

1. WHAT IDENTIFIES A HUNK TODAY. Read `packages/orchestration/diff_parser.py`
   and `packages/orchestration/diff_view_source.py`. Name the field the viewer
   JSON carries per hunk, where it is computed, and whether it survives an edit
   made elsewhere in the same file.
2. THE VIEWER JSON'S VERSION FIELD. Name it, its current value, the site that
   sets it, and every test that pins that value. Say whether this repository has
   a precedent for bumping it, and name the commit if it does.
3. THE HUNK LIBRARY `diff_repair` KEEPS TO ITSELF. Read
   `packages/orchestration/diff_repair.py` — `RepairHunk`, `RepairHunkSelection`
   and `select_repair_hunks` — and name every test file that guards them. The
   reviewer measured at `1f0329f4` that
   `tests/orchestration/test_diff_repair.py`,
   `tests/orchestration/test_diff_repair_apply.py`,
   `tests/orchestration/test_diff_repair_response.py`,
   `tests/orchestration/test_builder_repair_loop.py` and
   `tests/ui_server/test_command_channel.py` all name `diff_repair`; confirm
   that list yourself and say what each one actually asserts. This suite is
   T001's safety net.
4. THE APPLICATOR. Read `packages/orchestration/source_apply.py` and
   `packages/orchestration/patch_apply.py`. Name the entry point that lands a
   change, its atomicity contract, and what it does when ONE hunk of a set
   conflicts. The feature file's Do-not-touch list forbids changing applicator
   internals, so this section records what must be reused exactly as it stands.
5. THE WRITE CHANNEL. Read `UI_EXPOSED_COMMANDS` in
   `apps/cli/command_catalog.py` — the reviewer measured at `1f0329f4` that it
   holds exactly `job.stop` and `decision.resolve` — and the command door at
   `_handle_command_submission` in `packages/orchestration/ui_server.py`. Name
   every guard a NEW command must satisfy and the test file each guard lives in,
   including any import guard or walkable-path list in
   `tests/ui_server/test_command_channel.py`.
6. THE VALIDATION PRECEDENT. Find the existing command that requires a REASON on
   a negative answer — the feature file calls this "the veto lesson". Name where
   that requirement is enforced and where it is tested.
7. THE SEAM A REJECTION RIDES INTO THE NEXT ROUND'S PROMPT. The feature file
   names "steering-style volatile injection". Find it, name its module and
   function, and name what already flows through it today.
8. WHERE A TASK'S CHANGE STATE IS RECORDED. Name the record, the field, and the
   vocabulary that field accepts today. Say whether any existing value already
   means PARTIAL, and if none does, say so.
9. THE THREE SURFACES A PARTIAL STATE MUST RENDER IN. Name the viewer component
   file, the node-glyph site and the report-line site, each by path and symbol.

Answer from the code, never from a summary and never from this block. A question
you cannot answer is reported as unanswered together with what you searched — an
honest gap is worth more than a guess, and the reviewer plans T001 against this
file.

## Done when — the gates

Run every gate yourself and record its REAL result, one line per gate, in the
handback. "Green" as a word is a finding. G1 through G8 all run at commits
strictly earlier than C5, so C5 can quote every one of them.

WHEREVER A GATE BELOW SAYS "the base blob" or "at the base", read those bytes
with `git show <base>:<path>` into memory, or into a scratch file under
`.remedy-wt/`. NEVER obtain them by writing over the tracked file and restoring
it afterwards: that mutates the primary checkout, which
docs/agents/self_drive_protocol.md guardrail G5 forbids outright.

G1 HYGIENE. Read `.agent/STOP` from disk with `os.path.exists` before C0a and
again before C5, and report both answers. Report `git branch --show-current`,
which must be `feature/f033-hunk-approval`. Report
`git status --porcelain | wc -l` after each of C0a, C0b, C1, C2, C3, C4 and C5
— one reading per commit, each of which must be 0.

G2 TRANSPORT. ONE digest comparison. Compute sha256 over the committed
`.agent/authored/f033-r1.md` blob, read with
`git show <C0a>:.agent/authored/f033-r1.md` into memory, and compare it with
sha256 over the reviewer's own original at `.remedy-wt/f033-r1.md`, reporting
the byte comparison itself as well as both digests. That original existed before
you did and was not written by you, so this reading covers the emission and not
merely your own self-consistency. Report the byte count and the line count.
Additionally report that `git rev-parse <C0b>:.agent/authored/f033-r1.md` and
`git rev-parse <C0b>:.agent/last_block.md` print ONE blob id.

G3 THE PLAN AT C1. Re-extract PLANF033R1 from the COMMITTED C0a blob, never from
this prompt, and compare it with `.agent/plan.md` at C1: it must be BYTE EQUAL
including the trailing newline. NEGATIVE CONTROL: the same comparison with the
trailing newline dropped must report `False`. Report `wc -l`, which must be
under 50, and the counts of lines exactly `## Goal` and exactly `## Next Steps`,
each of which must be 1.

G4 THE RECORD AT C3, BOTH READERS. Re-extract RECORDHEAD and GATEF037R27 from
the COMMITTED C0a blob. (a) Take the base blob of `.agent/live_review.md`,
replace its single RECORDHEAD FROM occurrence with the TO, append one newline
and then GATEF037R27, and require the result EQUAL to the C3 blob. NEGATIVE
CONTROL: flip one byte at an offset your script has CONFIRMED lies inside the
FIRST paragraph of GATEF037R27, and require the equality to become `False`;
report both the offset you used and the offset at which that first paragraph
ends. (b) Split the C3 blob on blank lines. Let N be the number of
blank-line-separated units in GATEF037R27, COUNTED BY YOUR SCRIPT from the slice
itself and never taken from this block; require the LAST N units of the file to
equal those N paragraphs IN ORDER, unit by unit, and report N. NO WHOLE-FILE
PREFIX CHECK IS ORDERED and none is meetable, because RECORDHEAD rewrites the
file's head. Report instead that the base blob's bytes AFTER its RECORDHEAD FROM
are a byte-exact prefix of the C3 blob's bytes after the RECORDHEAD TO.

G5 THE LEDGER. Measure over the BASE blob and again over the C3 blob of
`.agent/live_review.md`, reporting both columns: the count of `^- R-\d+ — `,
whether those ids are all DISTINCT, the count of `^Done: R-\d+ — `, the count of
`^Landed: R-`, the count of `^Gate: F\d+ R\d+ — `, the maximum id, and the OPEN
SET computed AS A SET — the registered ids minus those carrying a `Done:` or a
`Landed:` line. The registrations, the `Done:` count, the `Landed:` count, the
maximum id and the open set must all be UNMOVED; the `^Gate: F\d+ R\d+ — ` count
must rise by EXACTLY ONE. Report how many times `Gate: F037 R27` occurs in the
C3 blob, which must be 1 — the reviewer measured 0 occurrences at the base.
Report `R-0714`'s registration, `Done:` and `Landed:` line counts separately.

G6 THE STATUS CLAIM AT C2. Before writing, verify that the STATUSCLAIM FROM
occurs exactly 1 time in `docs/roadmap/STATUS.md` at the base, and report that
count. Over the C2 content report the FROM count, which must be 0, and the TO
count, which must be 1, and report that the TO is present AS A WHOLE LINE
exactly once. Report the count of lines matching `^- \[~\]` at the base and at
C2, and the count matching `^- \[x\] F\d{3} — ` at the base and at C2.

G7 THE DOCS GATE AND THE CANARY, run after C4, serially:

    python3 -m pytest tests/docs/ -q
    python3 -m pytest tests/cli/test_golden_path.py -q

Report each command's REAL exit code, taken from the `returncode` of a
`subprocess.run` call with `capture_output=True` rather than from a pipeline,
and report its final summary line. Both must exit 0. The docs gate is required
because this round's change set includes `docs/roadmap/STATUS.md`
(docs/agents/planner_reviewer_prompt.md §3, docs-round gate); the canary is
required of every handback by the same section. The reviewer ran both at
`1f0329f4` and read exit 0 at `295 passed` and exit 0 at `42 passed`, and ran
`tests/docs/` once more inside a disposable worktree with the STATUSCLAIM pair
applied, reading exit 0 at `295 passed` — so this gate is known to be meetable
and is not a guess.

G8 STRUCTURE. `git diff --name-only <base>..<C5>` must return exactly the paths
of the change set above. Print BOTH residues — measured-minus-changeset
and changeset-minus-measured — and both must be EMPTY. `git diff --stat
<base>..<C5>` restricted to `apps/`, to `packages/`, to `tests/` and to
`docs/roadmap/features/` must print the empty string in all four cases. Report
the parent count of each of C0a, C0b, C1, C2, C3, C4 and C5; each must be 1.
Report the insertion count of each of C0a, C0b, C1, C2, C3 and C4 from
`git diff --numstat`, each under 500. C5's OWN insertion count is not reported
here and is not reported in the handback either: the reviewer measures it at the
next gate (docs/agents/planner_reviewer_prompt.md §3 checklist item 31). Report
`git ls-files .remedy-wt | wc -l`, which must be 0. After the push, report
`git rev-parse HEAD` and `git rev-parse origin/feature/f033-hunk-approval`;
the two must be equal.

## Handback

Rewrite `.agent/handoff.md` in C5, following docs/agents/handback_template.md.
It has NO length cap (AGENTS.md, amend0827 rule 3) and is valid when it carries
its mandated sections. It must carry: the SESSION line above; the review range
from this round's base; a per-commit changed-files table whose `+/-` cells come
from `git diff --numstat` — the same tool G8 reports from, so compare the two
readings cell by cell and state that they agree; step 1's external actions with
their real outcomes, INCLUDING the merge commit SHA and this round's base SHA;
one line per gate G1 through G8 carrying its real result; the deviations and
assumptions; the item-status table in which every ordered item appears exactly
once; the open-findings count; and the next expected action.

Then:

    git push -u origin feature/f033-hunk-approval

No pull request is created this round.

<<<SLICE PLANF033R1
# Plan — F033 Hunk-level diff approval

Branch: feature/f033-hunk-approval, cut from `main` at the merge of pull request
#218, which closed F037. `.agent/decisions.md` carries the F033 decisions.

## Goal
Surgical consent over changes. Hunks get STABLE content-hash ids, an
`approve_hunks` command applies the approved set atomically to the job branch,
and rejected hunks become precise repair feedback quoted verbatim in the next
round — every partial state rendered truthfully in the viewer, on the node and
in the report. `docs/roadmap/features/T5_F033.md` holds Goal & Done, the task
slicing, the acceptance criteria and the Do-not-touch list.

## Current Step
R1 is the CLAIM AND INVENTORY round. It merges F037's pull request at the Open
PR Gate, cuts this branch, flips F033 to `[~]`, resets this record's header
carrying every finding forward, books the F037 R27 verdict, and puts the F033
source inventory on disk. No production code is touched.

| Item | Status | Reason |
|------|--------|--------|
| C0a and C0b save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the STATUS claim | ordered | `[ ]` becomes `[~]` |
| C3 the record header and the F037 R27 gate | ordered | record before work |
| C4 the source inventory | ordered | the questions, answered from code |
| C5 the handback | ordered | last commit of the round |

## Next Steps
1. Book the R1 verdict and plan T001 against the inventory.
2. T001 stable-id hashing, the stability property tests, the viewer JSON
   version bump and the shared-helper consolidation with `diff_repair`.
3. T002 the `approve_hunks` command, its validation, subset-apply atomicity
   and the hunk ledger.
4. T003 rejection-to-repair injection, the verbatim-quote trace proof and
   partial-state rendering across viewer, node and report.

## Risks
- T001 moves hunk identity out of `diff_repair`; that module's regression suite
  is the safety net the feature file names in its Orchestrator brief.
- `R-0714` stays open as a documented Medium risk inherited across the reset.
<<<END PLANF033R1

<<<SLICE STATUSCLAIM
[P1] docs/roadmap/STATUS.md · REWRITE · TO contains FROM: false · FROM occurs 1x
[P1-FROM]
- [ ] F033 — Hunk-level diff approval
[P1-TO]
- [~] F033 — Hunk-level diff approval
<<<END STATUSCLAIM

<<<SLICE RECORDHEAD
[P1] .agent/live_review.md · REWRITE · TO contains FROM: false · FROM occurs 1x
[P1-FROM]
# Live Review — F037 Rendered diff viewer

> Round-by-round review record for the F037 branch, reset at the feature claim.
> The F032 record closed with pull request #217, merged into `main` as
> `9dde5495`, this branch's point. F032's LAST round, R19, is the round whose
> own bundle CREATED that pull request, so it is a branch terminator under
> `docs/agents/planner_reviewer_prompt.md` §4 item 13 and owes this record no
> entry. Its verdict is nevertheless the first `Gate:` paragraph below, because
> the finding record carries across the reset and an entry therefore costs this
> round nothing — the disposition F031's own R1 chose for F022 R19. Finding ids
> continue the monotonic R-XXXX series across the reset, and every finding
> record F032 carried is carried forward unchanged: measured at `9dde5495`,
> 275 findings, 24 resolved, 251 open, the maximum id `R-0714`.

## Steps

R1 claim F037 in the roadmap ledger, cut the branch, reset this record carrying
every finding record forward, gate F032 R19, and put the F037 source inventory
on disk — the unified-diff readers that already exist and what each discards,
the file-status vocabulary and whether it names `binary`, where a diff is
produced and whether one is kept per attempt, the server route table and the
guards over it, what identifies an attempt, the client entry point the design
reference names, the fetch seam and the bundle budget, and the guards a new
parser must satisfy → R2 book the R1 verdict and plan T001 against that
inventory → T001 the parser, its corpus and the read endpoint → T002 the
rendering core, the binding CSS and the goldens → T003 sidebar, virtual
scrolling, lazy languages and the L3 tab.
[P1-TO]
# Live Review — F033 Hunk-level diff approval

> Round-by-round review record for the F033 branch, reset at the feature claim.
> The F037 record closed with pull request #218, merged into `main` at this
> round's Open PR Gate, and that merge commit is this branch's point. F037's
> LAST round, R27, is the round whose own bundle CREATED that pull request, so
> it is a branch terminator under `docs/agents/planner_reviewer_prompt.md` §4
> item 13 and owes its own record no entry. Its verdict is the first `Gate:`
> paragraph below, because the finding record carries across the reset and an
> entry therefore costs this round nothing — the disposition F037's own R1 chose
> for F032 R19. Finding ids continue the monotonic R-XXXX series across the
> reset, and every finding record F037 carried is carried forward unchanged:
> measured by the reviewer at `1f0329f4`, 292 registered ids, all distinct, 43
> `Done:` lines, 11 `Landed:` lines, an open set of 251 computed as a set, and
> the maximum id `R-0731`.

## Steps

R1 claim F033 in the roadmap ledger, merge F037's pull request at the Open PR
Gate, cut the branch, reset this record carrying every finding record forward,
gate F037 R27, and put the F033 source inventory on disk — what identifies a
hunk today and where that id is produced, the viewer JSON's version field and
its bump precedent, the hunk library `diff_repair` keeps to itself and the tests
that guard it, the applicator's entry point and its atomicity contract, the
write channel's command catalogue and the guards a new command must satisfy, the
validation precedent that already requires a reason, the seam a rejection would
ride into the next round's prompt, where a task's change state is recorded, and
the three surfaces a partial state must render truthfully in → R2 book the R1
verdict and plan T001 against that inventory → T001 stable ids, the stability
property and the shared-helper consolidation → T002 the command, its validation
and subset-apply atomicity → T003 rejection-to-repair injection and
partial-state rendering.
<<<END RECORDHEAD

<<<SLICE GATEF037R27
Gate: F037 R27 — the F037 closure round, and the entry F037's own record could not write. THE ROUND PASSED on every gate its block ordered, G1 through G8, and the reviewer re-ran all of them itself at `1f0329f4` before that branch's pull request was merged; because R27 created that pull request it is a branch terminator under `docs/agents/planner_reviewer_prompt.md` §4 item 13, so this paragraph is written by the next feature's first round rather than by a round of F037. TRANSPORT IS PROVED FROM A VALUE THAT EXISTED BEFORE THE WORKER DID: sha256 `c61bfc2eeeff1a450cd1d4d8c1e1640cc48154a423ebfc4b2c28f83869b5bc7c` over 20360 bytes and 286 lines is equal across the scratch original `.remedy-wt/f037-r27-block.md`, which an earlier session's reviewer wrote, and the committed `.agent/authored/f037-r27.md` blob at `314159ab`, and at `ae1b8b2c` that path and `.agent/last_block.md` are ONE git blob, `2b0101abe6cc702d70815e7d31936dcfdb32414e`. That chain covers the original, the saved copy and the mirror, and it claims NOTHING about the bytes of any prompt — the limit finding R-0705 requires to be stated rather than implied. THE PLAN IS BYTE-EQUAL to slice PLANF037R27 re-extracted from the committed C0a blob, with the trailing-newline negative control `False`, at 42 lines carrying one `## Goal` and one `## Next Steps`. THE APPEND INTO THE RECORD RECONSTRUCTS EXACTLY UNDER BOTH READERS: `.agent/live_review.md` at `7d84971b` equals its `6a32be79` blob plus one newline plus GATER26; a byte flipped at offset 50, which lies inside the FIRST appended paragraph, makes that equality `False`; the last 6 blank-line units of the file equal the slice's 6 paragraphs in order; and the pre-round blob is a byte PREFIX, 1329032 bytes growing to 1334200. THE LEDGER MOVED BY EXACTLY ONE GATE AND BY NOTHING ELSE, re-measured by this reviewer at both commits: 292 registrations all distinct, 43 `Done:` lines and 11 `Landed:` lines unmoved, the open set 251 unmoved, `^Gate: F\d+ R\d+ — ` rising 96 to 97, `Gate: F037 R26` occurring exactly once, and `R-0714` carrying one registration line, no `Done:` line and no `Landed:` line — so it closes F037 OPEN as the documented Medium risk closure precondition 1 admits. THE FOUR CLOSURE PAIRS HOLD IN THE SHAPE THE BLOCK ASSIGNED THEM, measured against `6a32be79`: every FROM occurred exactly 1x before the edit; P1, P2 and P3 are REWRITES and read FROM 0x and TO 1x after; P4 is the APPEND, its TO containing its FROM, and reads FROM 1x and TO 1x after. THE STATUS LINE IS PRESENT AS A WHOLE LINE EXACTLY ONCE at `1f0329f4`, the accepted count rising 59 to 60 and the in-progress count falling 1 to 0. THE CLOSURE PRECONDITIONS WERE RE-RUN BY THIS REVIEWER AT REAL EXIT CODES: `python3 -m pytest tests/docs/ -q` exit 0 at `295 passed`, `python3 -m pytest -n auto -q` exit 0 at `18119 passed, 20 skipped` in 159.2 seconds with the `^FAILED ` pattern matching 0 lines, and `run_integrity_checks()` reporting `passed=True` and `fail_count=0` across `handler_import`, `live_review_verdict`, `plan_consistency`, `relevant_untracked` and `high_blockers_open`. THE ONE FIGURE R27 COULD NOT MEASURE, THIS REVIEWER MEASURED: with `README.md` reverted to its `6a32be79` content inside a disposable worktree at `1f0329f4`, `tests/docs/` reads exit 1 at `2 failed, 293 passed`, the two failures being `test_the_readme_accepted_count_equals_the_status_count` and `test_the_readme_tier_table_done_column_matches_the_ledger` — so the R-0154 pin that forces STATUS and README into one commit demonstrably bites, and R27's quoted control is confirmed rather than inherited. THE README CAPABILITY PARAGRAPH IS TRUE AND NOT MERELY APPLIED, which is the reading the block's own gates did not order: the server parses a unified diff in `packages/orchestration/diff_parser.py`, which emits intraline spans through `_normalise_intraline_spans`, and serves the result at two routes — the per-job `diff` handler in the dispatch table of `packages/orchestration/ui_server.py` and the per-task-run `/api/jobs/<job_id>/task-runs/<task_id>/diff` structural route beside it; the file sidebar is `apps/ui/src/components/diff/DiffFileSidebar.tsx`; `DIFF_VIRTUAL_SCROLL_THRESHOLD_ROWS` in `apps/ui/src/api/diffViewModel.ts` is 2000 and the list is NOT virtualized at or below it, which is what "past two thousand rows" says; and highlighting is modelled by `DIFF_SUPPORTED_LANGUAGES`, `diffLanguageForPath` and `loadDiffLanguageBundle` in that same module while no `.tsx` file under `apps/ui/src` references any of the three, which is what "deliberately not wired" says. STRUCTURE HELD: `git diff --name-only 6a32be79..1f0329f4` returns exactly the block's seven paths with both residues empty, the four restricted stats over `apps/`, `packages/`, `tests/` and `docs/roadmap/features/T5_F037.md` all print the empty string, all five commits are single-parent at 286, 211, 21, 12 and 271 insertions, the transport markers count 0 in each of the four target files against 3 in the control, `git ls-files .remedy-wt` prints 0 lines, and the remote tip equalled the local tip at `1f0329f4877d16c9c13dec3b313f6b12ed062f24`. NO BLOCK CONDITION AROSE: nothing fabricated, no false green, no missing changed-files table, no unverified completion claim and no silent scope change.

WHAT THIS REVIEWER COULD NOT VERIFY IS STATED RATHER THAN IMPLIED, and it is the same limit the F032 R19 entry above records: the package filename `remedy-review-20260828-142213-READY_FOR_REVIEW.zip`, its SHA-256 and its archived path `/home/decodeux/Repos/remedy-history/zips` rest on R26's transcript and on R27's application of them, because that directory lies outside this session's allowed working directories, where `ls` and `sha256sum` are both refused; the STATUS line records all three on that basis and this sentence is their provenance. The `accepted HEAD` that line names, `5e557a1c2b4f7f9187f5388b18a3712d4a5c3d7e`, IS verifiable here and was verified: it is an ancestor of `1f0329f4` and is the commit `docs(roadmap): record F037's Built State on the feature file`. PULL REQUEST #218 WAS MERGED AT THE OPEN PR GATE AFTER THIS VERDICT AND BEFORE THIS PARAGRAPH WAS COMMITTED, which constraint 2 of the F033 R1 block fixes as that round's first action; its CI run `33172259776` was WATCHED TO COMPLETION rather than assumed, reporting conclusion `success` in 25m31s against a merge state of `CLEAN`, and the merge commit is this branch's point. F037 IS CLOSED.
<<<END GATEF037R27
