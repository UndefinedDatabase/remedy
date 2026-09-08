STEP — F274 ROUND 12 — a REPAIR ROUND: the three stale prose mentions the `feature` deletion left behind

Goal: correct the three places on disk that still name the `feature` command round 11 deleted — two
lines of `docs/system/development-artifact-boundary-v0.md` and the module docstring of
`tests/cli/test_progress_feature_runtime.py`. Book round 11's PASS verdict, book a RECURRENCE of
R-0819 for four wrong derived numerals in the round 11 block, register the stale prose as R-0835 and
RESOLVE it in this same round. NO EDGE AND NO CLUSTER MODULE MOVES — the deletion map is byte-
unchanged across this round and gate G7 proves it.

Base commit for every reading in this block: `5c7b856b2f3bb35e623e1d1cebd6fc9bf7fbf527`.

WHY THIS ROUND EXISTS, stated plainly because two of the three sites are the reviewer's own damage.
The round 11 block ordered a sweep of five exact strings, all of which correctly total zero; these
three sites name the command in PROSE, as the bare word `feature`, which no sweep can reach because
that word occurs legitimately throughout the repository. One of the three is not stale text at all
but a plural sentence the round 11 block's own ordered rewrite left standing over a one-item list.
The ROUND 11 WORKER found all three and declared them rather than editing outside its change set,
which is the behaviour the block asked for.

FRAME CONVENTION. No line of this block is a run of a single repeated character. Every slice is
delimited by a line reading `BEGIN <NAME> sha256=<hex> bytes=<n>` and a line reading `END <NAME>`,
and the slice is the bytes BETWEEN those two lines, the leading newline of an appended slice
included. Marker lines are never written to any file.


## Bundle — the commits of this round, in this order

C0a  Save this block verbatim as `.agent/authored/f274-r12.md`.
C0b  Mirror the same bytes into `.agent/last_block.md`.
C1   Replace `.agent/plan.md` with the PLAN12 slice.
C2   Append the RECORD12 slice to `.agent/live_review.md` — books round 11's PASS verdict, books the
     R-0819 RECURRENCE, and REGISTERS R-0835.
C3   Append the SLIPS12 slice to `.agent/prose_slips.md`.
C4   THE FIX: the three whole-line rewrites of the PAIRS12 slice.
C5   Append the RESOLVE12 slice to `.agent/live_review.md` — the authored `Done: R-0835`.
C6   The handback: rewrite `.agent/handoff.md`, then push.

C1 is the first substantive commit because this round touches the finding ledger and the plan must be
current before every commit (docs/agents/planner_reviewer_prompt.md §3 item 23). FINDINGS PERSIST
FIRST: C2 registers R-0835 before C4 repairs anything, per §4 item 4.


## Change set — these paths and nothing else

  .agent/authored/f274-r12.md
  .agent/last_block.md
  .agent/plan.md
  .agent/live_review.md
  .agent/prose_slips.md
  .agent/handoff.md
  docs/system/development-artifact-boundary-v0.md
  tests/cli/test_progress_feature_runtime.py


## C4 — the fix, three whole-line rewrites

The PAIRS12 slice below carries them in a fixed line format. For each tag P1, P2 and P3 it gives
three lines: `<tag> FILE ` then the repo-relative path, `<tag> FROM ` then the whole line as it
stands at the base, and `<tag> TO ` then the whole line that replaces it. In every case the content
begins immediately after a SINGLE space following the label, and runs to the end of that line —
there is no alignment padding to strip and no trailing whitespace anywhere in the slice.

ALL THREE ARE REWRITES, NOT APPENDS, AND THE READING IS MECHANICAL RATHER THAN BY EYE. The reviewer
ran the containment test on each pair at the base commit named above and it printed
`TO contains FROM: false` for P1, for P2 and for P3, so each is a REWRITE and each therefore owes
the FROM-zero proof that gate G5 orders. At that same commit each FROM occurs EXACTLY ONCE in its
file and each TO occurs ZERO times; the reviewer measured all six figures.

Replace the whole line, keeping its line ending. Every pair is one line in and one line out, so
NEITHER FILE CHANGES ITS LINE COUNT: the doc stays at 85 lines and the test file at 73.

WHAT IS DELIBERATELY NOT DONE. The FILENAME `tests/cli/test_progress_feature_runtime.py` still names
a command it no longer covers. DECISION F274 D6 ruled in round 11 that it is not renamed here —
renaming breaks `git log --follow` on a file that round already touched, and F261 owns renames. Do
not rename it, and do not touch its surviving class `TestProgressChecklistRuntime`.


## Constraints

1. Apply every slice BYTE FOR BYTE. Do not reflow, retype or re-indent one. If something looks wrong,
   apply it as given and DECLARE the doubt in the handback.
2. RECORD12, SLIPS12 and RESOLVE12 are APPENDS: the target's existing bytes are a byte-exact PREFIX
   of the result and the slice is an exact SUFFIX. Each carries its OWN leading newline — ADD NO
   SEPARATOR of your own. PLAN12 replaces `.agent/plan.md` entirely. PAIRS12 is NOT appended to any
   file; it is a carrier for the three pairs and its own bytes never reach the work tree.
3. The path set of C0a through C5 is exactly the paths listed under "Change set" other than
   `.agent/handoff.md`, which C6 writes.
4. COMMIT ORDER IS LOAD-BEARING AND THIS CONSTRAINT IS WHAT MAKES THE RESOLUTION TRUE. C4, the fix,
   is committed BEFORE C5, the commit that writes `Done: R-0835`. The resolution paragraph asserts a
   fact about this round's own landed change, and under
   docs/agents/planner_reviewer_prompt.md §3 item 20 such a claim names the ordering constraint that
   fixes its commit rather than a SHA that cannot exist when the text is authored. This is that
   constraint.
5. Any destructive check runs ONLY inside a disposable `git worktree`, never in the primary checkout,
   which satisfies `git status --porcelain` == empty at every commit boundary. Remove and prune each
   worktree you create.
6. Do not write a `Done:` paragraph of your own. RESOLVE12 is the reviewer-authored resolution; apply
   it verbatim and add nothing.
7. Every gate below runs at a commit STRICTLY EARLIER than C6, so the handback can quote each.
8. RUN THE FULL SUITE IN THE PRIMARY CHECKOUT, never in a fresh worktree: `apps/ui/node_modules` and
   `apps/ui/dist` are gitignored, so a fresh worktree has neither and both the vitest foundation test
   and the npm-backed tests then fail on the missing build rather than on anything this round did.
9. READING A COMMITTED BLOB, since several gates below measure one. Use `git show <commit>:<path>`
   into memory or into a scratch file under the gitignored `.remedy-wt/`, or read it in a disposable
   worktree. NEVER write a blob over the tracked file and restore it afterwards.
10. THE KNOWN FLAKE, stated so you do not repair it. Finding R-0569 is OPEN and names the fixed port
    5273 under xdist, pinned at `tests/orchestration/test_product_smoke.py` line 90. The reviewer hit
    it once in its own round 11 gate run, at
    `tests/orchestration/test_product_smoke.py::TestAppStartsGreen::test_a_clean_app_passes`, and it
    passed serially and on an immediate re-run. If a server-backed file fails under `-n auto`, RE-RUN
    IT SERIALLY and report both results. Do NOT edit any file to make such a red go away.


## Done when — the gates, one line per gate in the handback

G1  TRANSPORT, at C0b. `sha256` of the committed `.agent/authored/f274-r12.md` equals `sha256` of the
    committed `.agent/last_block.md`, and both equal the digest the delegation message states. Report
    the digest you measured.

G2  THE REGISTRATION APPEND, at C2, re-derived from the COMMITTED blobs.
    (a) BYTES: `.agent/live_review.md` 579917 -> 588670; pre-image a byte-exact PREFIX; post-image
        equal to pre plus the 8753-byte RECORD12 slice. The second of those two clauses is the BYTE
        reader gate (c) names; the prefix clause alone cannot see a flip inside the appended region.
    (b) STRUCTURE over the WHOLE appended region: a unit is a maximal run of consecutive non-empty
        lines; COUNT N from the slice itself; the file's last N units equal the slice's units IN
        ORDER and everything before them is unchanged. Units 229 -> 232.
    (c) NEGATIVE CONTROL: flip the byte at ZERO-INDEXED BYTE offset 579918 of the post-image — it is
        the `G` opening the FIRST appended paragraph — and confirm the BYTE reader of (a) and the
        STRUCTURAL reader of (b) each reject it.
    (d) COUNTS: registrations 68 -> 69, resolutions 5 -> 5, OPEN SET 63 -> 64 BY DISTINCT ID,
        `^Gate: ` 42 -> 43, `^Gate: F274 R11` 0 -> 1, `^- R-0835 — ` 0 -> 1, `^Landed: ` UNCHANGED at
        37 lines. The open set RISES here by design; G6 brings it back.

G3  THE PROSE STATE FILES. `.agent/plan.md` at C1 is BYTE-EQUAL to the PLAN12 slice, is 46 lines
    against the cap of 50, and carries both `## Goal` and `## Next Steps`. `.agent/prose_slips.md` at
    C3 goes 162264 -> 162746 with the pre-image a byte-exact prefix and the appended line once.

G4  THE FIX, at C4, measured against the COMMITTED blobs.
    (a) For EACH of P1, P2 and P3: the FROM line occurs ZERO times in its file and the TO line occurs
        EXACTLY ONCE. Report six numbers. This is the rewrite proof §4.9 owes for a pair whose TO
        does not contain its FROM.
    (b) LINE COUNTS UNCHANGED: `docs/system/development-artifact-boundary-v0.md` 85 -> 85 and
        `tests/cli/test_progress_feature_runtime.py` 73 -> 73, because each pair is one line in and
        one line out.
    (c) ZERO-GATE, scoped to the two touched files and to nothing else: the bare word `feature`
        totals ZERO across those two files, against three occurrences across them at the base. THE
        SCOPE IS DELIBERATE AND UNMEETABLE ANYWHERE WIDER — that word occurs legitimately throughout
        the repository, and this block itself names it many times, so a repo-wide zero would be a
        gate that cannot pass. Report the two per-file totals.
    (d) `tests/cli/test_progress_feature_runtime.py` still parses under `ast` and still holds exactly
        one class, `TestProgressChecklistRuntime`, and the file is NOT renamed.

G5  THE SUITES, at C4. Run each command ALONE and report its own number — that separation is the
    clause the R-0819 recurrence in RECORD12 adds, and it is why this gate lists three commands
    instead of one.
    (a) `python3 -B -m pytest tests/docs/ -q` EXIT 0. The reviewer measured 303 passed.
    (b) `python3 -B -m pytest tests/orchestration/test_development_artifact_boundary.py -q` EXIT 0.
        The reviewer measured 18 passed.
    (c) `python3 -B -m pytest tests/cli/test_progress_feature_runtime.py -q` EXIT 0. The reviewer
        measured 5 passed.
    (d) THE FULL SUITE green, in the PRIMARY CHECKOUT per constraint 8: `python3 -m pytest -q -n auto`.
        Report the exit code and the passed/failed/skipped counts. The reviewer measured 19765
        passed, 23 skipped, 0 failed at the BASE, and this round changes one docstring and two
        markdown lines, so the count must be IDENTICAL at C4. Constraint 10 governs a red in a
        server-backed file.
    (e) `python3 -m ruff check tests/cli/test_progress_feature_runtime.py` EXIT 0, and `ruff check .`
        REPORTS 26 ERRORS, unchanged, so DECISION F083 D5's frozen ceiling is untouched — that
        command EXITS 1 while reporting them, which is the gate passing, because the ceiling is 26
        rather than 0.

G6  THE RESOLUTION APPEND, at C5, re-derived from the COMMITTED blobs, and it runs at a commit later
    than C4 so the paragraph it lands is true when it lands.
    (a) BYTES: `.agent/live_review.md` 588670 -> 589620; prefix exact; post equal to pre plus the
        950-byte RESOLVE12 slice.
    (b) STRUCTURE, N counted from the slice: units 232 -> 233, last N units equal the slice's units
        IN ORDER, everything before unchanged.
    (c) NEGATIVE CONTROL at zero-indexed byte offset 588671 — the `D` opening the appended paragraph
        — rejected by both readers.
    (d) COUNTS: registrations 69 -> 69, resolutions 5 -> 6, OPEN SET 64 -> 63 BY DISTINCT ID,
        `^Done: R-0835 — ` 0 -> 1, `^Landed: ` UNCHANGED at 37. THE ROUND THEREFORE OPENS AND CLOSES
        AT 63 OPEN FINDINGS, having registered and resolved exactly one.

G7  THE TREE AND THE SCOPE GUARD, at C5. `git status --porcelain` EMPTY; `git ls-files .remedy-wt`
    EMPTY; `git worktree list` the same count as before your first worktree and after your last
    prune; `git diff --name-only 5c7b856b2f3bb35e623e1d1cebd6fc9bf7fbf527..<C5>` naming exactly the
    paths of constraint 3 and nothing else; every commit C0a through C5 single-parent. Report the
    INSERTION count of each commit C0a through C5. AND THE SCOPE GUARD, which is what proves this
    round did not wander into the deletion work: `tests/orchestration/cluster_deletion_map.txt` is
    BYTE-IDENTICAL at the base and at C5 — report the sha256 you measured for both — and
    `packages/orchestration/` holds no changed file in the range at all. Do not report C6's own
    numbers; the reviewer measures them at the next gate.


## Handback — rewrite `.agent/handoff.md` at C6, then push

Carry the mandated sections of `docs/agents/handback_template.md`: the state block, the commits table
with its `+/-` column taken from `git diff --numstat`, the changed-files table, ONE LINE PER GATE G1
through G7 with its real result, the deviations, the open-findings count, and the next expected
action. No length cap. Name the SESSION NUMBER as SESSION 5 of feature F274 and the round as 12.
State the open-findings count as the number G6(d) MEASURED. Add the one sentence of context
self-assessment amend0905-throughput requires.

DECLARE, do not silently repair: if any gate goes red, or any slice does not apply as described,
report the real command, the real exit code and the real output and say what you did.


BEGIN PLAN12 sha256=b9d95144faedcb48892ec8ba10adc3233f5994c1f9d9aeb70edb30d821f198d5 bytes=2815
# Plan — F274 One world completion, part two

Branch: feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, with `main` merged back in at `f85200e4` to take
operator amendment amend0907-cluster-first.

## Goal

Finish what F272 could not reach inside its own limit: the prototype cluster deletion and the
classic-to-unified record flip DECISION F272 D15 measured as ATOMIC. DECISION
amend0907-cluster-first D1 reorders the slices so the deletion runs FIRST.

## Current Step

Round 12, a REPAIR ROUND: fix the three stale prose mentions round 11's `feature` command deletion
left on disk — two in `docs/system/development-artifact-boundary-v0.md` and the module docstring of
`tests/cli/test_progress_feature_runtime.py`. Book round 11's PASS verdict, register the stale
prose as R-0835 and resolve it in the same round, and book a RECURRENCE of R-0819 for four wrong
derived numerals in the round 11 block. No cluster module and no edge moves this round.

## Next Steps

1. `worker_recommend`'s three edges, in `agent_loop.py`, `autonomy_loop.py` and `dashboard.py`.
   These are LIVE RUNTIME CALLS rather than read-only views: the reviewer measured that they feed
   the `token_policy_applied` run-log event and `CycleDecision.selected_worker`, and that
   `selected_worker` is named in `packages/orchestration/event_schemas.py`, so a DECISION naming
   what inherits worker recommendation is authored before the cut and the ruled event vocabulary
   is part of the question.
2. The two carry-overs F260's Design names, each freeing a cockpit section held back so far:
   overnight readiness to `mission readiness`, and the route-policy knobs checked against F110's
   config keys. `mission report` waits for the commit that deletes its current holder, per
   DECISION F274 D2, and that holder is in `worker_facade_cmd.py`.
3. `orchestrator_brain.py`'s four edges, measured as live signal reads in `_scrub`,
   `_review_state`, `_gather_signals` and `consult_local_advisor_for_decision` — a surviving module
   reading cluster modules, so a behaviour change rather than a deletion.
4. The four `worker_facade_cmd.py` edges and `worker_registry`'s remaining pair.
5. Draft DECISION F260 D3, the deletion paragraph. R-0832's fix clause binds it.
6. The cluster deletion itself, one commit per module group, NEVER SPLIT ACROSS SESSIONS.
7. T001 — the `Job.id` flip. Then T002 — the classic runner and the resolver collapse.

## Risks

- The map was blind twice and is now fixed once: R-0834's file-type blindness is closed, R-0832's
  event-name coupling is OPEN. Treat every "zero edges" reading as a claim about the WALKER.
- The open High findings are R-0803, R-0804, R-0806 and R-0807, all F273's rather than this
  feature's, per DECISION F272 D12.
END PLAN12


BEGIN RECORD12 sha256=2ccb3fed55a327af7bdb0739cc080c4d90a700f77a771f72989cbe4652c76b74 bytes=8753

Gate: F274 R11 — the F274 round 11 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER ITSELF, in the primary checkout and in a disposable worktree, against the COMMITTED blobs. Range `fb0d56c419f7bc8441f461dac1a6ea1e44a044d7`..`5c7b856b2f3bb35e623e1d1cebd6fc9bf7fbf527`, eight commits, every one single-parent, in the ordered sequence C0a, C0b, C1, C2, C3, C4, C5, C6, with the path set over the range to C5 naming exactly the fifteen declared paths. G1 TRANSPORT covers the emitted bytes: the reviewer's scratch original `.remedy-wt/f274-r11-FINAL.md`, hashed BEFORE delegation, is BYTE-IDENTICAL to both committed copies, all three 32441 bytes at `47f17119d101c2246c23fa7a1a43804b9658031925f2e5d31058240d3d5a447f`. G2 THE RECORD APPEND at `87e5249d`: 574989 to 579917 bytes, prefix exact, post equal to pre plus the 4928-byte slice, N counted as 1, units 228 to 229, ordered equality true, the control at byte offset 574990 rejected by both readers; registrations 68 to 68, resolutions 5 to 5, OPEN SET 63 TO 63 BY DISTINCT ID, `^Gate: ` 41 to 42, `^Landed: ` unchanged at 37. G3 THE DECISION APPEND at `5c6a234b`: 899779 to 905078 bytes against the 5299-byte slice, N counted as 9, units 1977 to 1986, control at 899780 rejected by both readers, `^## DECISION F274 D6` zero to one. G4: `.agent/plan.md` byte-equal to its slice at 48 lines; `.agent/prose_slips.md` 161811 to 162264 with the appended line once. G5 THE MEASUREMENTS: import reachability EXIT 0 at 3 passed and `tests/docs/` EXIT 0 at 303 passed; THE FULL SUITE GREEN IN THE REVIEWER'S OWN RUN IN THE PRIMARY CHECKOUT at 19765 passed, 23 skipped, 0 failed; the five deleted strings TOTAL ZERO over the 1719 tracked files of `packages/`, `apps/`, `tests/`, `scripts/` and `docs/` with no file-type filter; `ruff check` EXIT 0 over the four surviving touched paths and the frozen ceiling unchanged at 26. THE COLLECTED SET WAS DIFFED AS A SET RATHER THAN AS A COUNT, which is the reading this round most needed: 19804 to 19788, EXACTLY 16 node ids disappear and ZERO appear, the sixteen being the eight tests of the two deleted runtime classes and eight `[feature]` parametrizations in `tests/test_grouped_cli.py`. G6 THE EDGE TRUTH AND THE RATCHET, in the reviewer's own disposable worktree: control EXIT 0 at 3 passed, measured equals recorded at 23 with APPEARED and DISAPPEARED both empty, the zero-edge modules exactly the twelve named, the non-`.py` consumers THE EMPTY LIST; the red proof appended `packages.orchestration.feature_planner <- apps/cli/commands/feature_cmd.py` — zero occurrences after C5 — and got EXIT 1 with `DISAPPEARED (1)` naming that exact edge, restoring to `cfdbbe8ecdf2727a526cf49083265201d4f1ab43aabad85fe2204c29cf980702` and EXIT 0. G7: `apps/cli/commands/feature_cmd.py` PRESENT at the base and ABSENT at C5; every touched `.py` file parses; `tests/cli/test_progress_feature_runtime.py` holds exactly one class, `TestProgressChecklistRuntime`; the catalog holds no `feature` group and no `feature.plan` or `feature.accept` entry. G8 THE TREE: porcelain empty, `git ls-files .remedy-wt` empty, worktrees 14 before and after, per-commit insertions 405, 253, 12, 2, 69, 2 and 2 for C0a through C5. THE FULL SUITE WENT RED ONCE IN THE REVIEWER'S OWN RUNS, at `tests/orchestration/test_product_smoke.py::TestAppStartsGreen::test_a_clean_app_passes`, and the reviewer attributed it rather than accepting it: that file is the one finding R-0569 names for the fixed port 5273 under xdist, it passed serially at 76 passed, and an immediate second `-n auto` run of the whole suite was green at 19765. FOUR DERIVED NUMERALS IN THE ROUND 11 BLOCK WERE WRONG AND THE WORKER CAUGHT EVERY ONE: gate G7(b) ordered `apps/cli/command_catalog.py` to 4918 lines where the block's own prose gives 4917, and `tests/cli/test_progress_feature_runtime.py` to 81 where the prose gives 73; gate G8 ordered C5 at minus 217 where it is minus 226, which is exactly the sum of the other two errors; and gate G5(a) ordered `tests/docs/` at 306 passed where it is 303 both at the base and at the head. THE WORKER APPLIED THE PROSE, WHICH WAS CORRECT, DECLARED EVERY GAP, AND CHANGED NOTHING TO MAKE A GATE GREEN — the landed state is the better one in both files, with no orphaned comment banner above a deleted class and no double blank line at the catalog seam, and the reviewer verified both seams by reading the committed blobs. That is a reviewer arithmetic defect, not a worker execution defect, and it is booked as the R-0819 recurrence below. ONE FINDING IS REGISTERED BY THIS GATE, R-0835, and it is resolved later in this same round.

RECURRENCE of R-0819 at F274 round 11, measured by the reviewer at `5c7b856b2f3bb35e623e1d1cebd6fc9bf7fbf527`. NO NEW ID IS SPENT: docs/agents/planner_reviewer_prompt.md §3 item 30 requires the open set to be searched for the DEFECT before an id is minted, and R-0819 is OPEN and its headline states this class — a gate ordering a value that cannot be met. The round 11 block ordered four such values, listed in the entry above. THE CAUSE IS NEW AND IS WHAT THIS RECURRENCE ADDS, because it is not the cause R-0819 already names. R-0819's own fix clause requires a gate to be RUN AT THE BASE BEFORE BEING ORDERED, and this time it was: the reviewer applied the whole cut in a disposable worktree and measured every file. The defect is that THE DRY-RUN SCRIPT AND THE BLOCK PROSE DESCRIBED DIFFERENT EDITS. The script kept the blank line after the deleted catalog run and kept the comment banner above each deleted test class; the prose ordered both removed. The reviewer then took the NUMERALS from the script and the INSTRUCTIONS from the prose, so every derived line count was one edit behind the order it stood beside, and the three counts compounded into a fourth in the deletion total. A fifth numeral failed the same way for a different reason: `tests/docs/` was measured in a command that also ran `test_import_reachability.py`, and the combined 306 was recorded as the docs figure alone. THE ADDITION THIS RECURRENCE MAKES TO R-0819's FIX, binding on every later block of this feature that orders a line count or a diff total: the numerals a block states are read out of the SAME applied dry run whose result the block's prose describes, by re-measuring the tree after that application rather than from the script that produced it; and a numeral for one command is measured by running THAT COMMAND ALONE. Where the two cannot be reconciled before emission, the block orders the WORKER to report the number it measured and states no numeral itself, which docs/agents/planner_reviewer_prompt.md §3 item 16 already permits for a count the block cannot fix.

- R-0835 — Low — STALE PROSE LEFT BEHIND BY THE `feature` COMMAND DELETION. Registered at F274 round 12, measured by the reviewer at `5c7b856b2f3bb35e623e1d1cebd6fc9bf7fbf527`, and found by the ROUND 11 WORKER rather than by the reviewer, which is recorded because the round 11 block's own sweep could not reach it: gate G5(c) swept five exact strings — `feature_cmd`, `_cmd_feature_plan`, `_cmd_feature_accept`, `feature.plan` and `feature.accept` — and all five correctly total zero, while these three sites name the command in PROSE, as the bare word `feature`, which is unsweepable because the word occurs legitimately hundreds of times across the repository. THE THREE SITES. First, `docs/system/development-artifact-boundary-v0.md` line 60 reads `2. Development commands (`feature`, `progress`) may continue reading `.agent/` files` and names a command that no longer exists. Second, line 55 of the same file reads `These are classified as development commands, not core product operator commands.` and is plural about a list the round 11 block itself narrowed to one entry — so this half is damage the reviewer's own ordered rewrite caused. Third, the module docstring of `tests/cli/test_progress_feature_runtime.py` announces the file as covering `remedy progress` and `remedy feature` when its only surviving class is `TestProgressChecklistRuntime`. THE FIX, applied in this same round: three whole-line rewrites, one per site. DELIBERATELY OUT OF SCOPE AND NOT A GAP: the FILENAME `test_progress_feature_runtime.py` still names a command it no longer covers, and DECISION F274 D6 already ruled that it is not renamed here — renaming breaks `git log --follow` on a file the deletion round already touched, and F261 owns renames. THE GENERAL LESSON THIS FINDING CARRIES, binding on every later command deletion in this feature: an exact-string sweep proves the SYMBOLS are gone and proves nothing about the PROSE, so a round that deletes a user-facing command reads the docs and docstrings that named it rather than sweeping for them.
END RECORD12


BEGIN PAIRS12 sha256=4b5994cd191a0e24ae8e95524831a46b78c406b75d690d675e856859635a4747 bytes=669

P1 FILE docs/system/development-artifact-boundary-v0.md
P1 FROM These are classified as development commands, not core product operator commands.
P1 TO It is classified as a development command, not a core product operator command.
P2 FILE docs/system/development-artifact-boundary-v0.md
P2 FROM 2. Development commands (`feature`, `progress`) may continue reading `.agent/` files
P2 TO 2. The development command `progress` may continue reading `.agent/` files
P3 FILE tests/cli/test_progress_feature_runtime.py
P3 FROM """Runtime subprocess tests for ``remedy progress`` and ``remedy feature`` CLI.
P3 TO """Runtime subprocess tests for the ``remedy progress`` CLI.
END PAIRS12


BEGIN SLIPS12 sha256=9f9505bc7b10756b9cf86f65ee36f16992642d0d573d627a851725e955cbafb3 bytes=482

2026-09-08 · F274 R11 · The round 11 block's gate G5(a) stated `tests/docs/` at 306 passed when it is 303; the reviewer had measured it in a command that also ran `test_import_reachability.py` at 3 passed and recorded the combined total as the docs figure, and the worker re-measured both at the base and reported the real number. Not load-bearing — the gate's property is EXIT 0 and that held — and the substantive half of the same class is booked as the R-0819 recurrence.
END SLIPS12


BEGIN RESOLVE12 sha256=a71ec6ae364d7c42221cc692dce142c11c049a84c1046e8aa356d15107530368 bytes=950

Done: R-0835 — RESOLVED in F274 round 12, in the commit this round's own constraint fixes immediately before the commit that writes this paragraph. All three stale prose sites are corrected by whole-line rewrite, and the correction is verified by a zero-gate rather than by inspection: the bare word `feature` now totals ZERO in both touched files, `docs/system/development-artifact-boundary-v0.md` and `tests/cli/test_progress_feature_runtime.py`, against three occurrences across them before. Neither file changed its line count, because every pair replaces one line with one line. `tests/docs/` is 303 passed, `tests/orchestration/test_development_artifact_boundary.py` 18 passed and `tests/cli/test_progress_feature_runtime.py` 5 passed, each measured by running that command alone — which is the clause the R-0819 recurrence in this same round adds. The FILENAME is untouched by design, per DECISION F274 D6 and as the registration states.
END RESOLVE12
