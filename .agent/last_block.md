STEP CLOSURE 2/4 — F272 — round 27 — the Built State section and the integration gate

Base commit for every reading in this block: `412ce673`, the round 26 handback commit.
Every separator line below is exactly twenty `=` characters.

====================
Goal
====================

Two closure preconditions, in one round. Precondition 4 of
`docs/roadmap/STATUS_closure_protocol.md` requires the feature file's Built State section
to be current, and `docs/roadmap/features/T2_F272.md` has NO such section — measured at
the base commit, `^## Built State` occurs zero times in it. Precondition 2 requires a
dedicated INTEGRATION-GATE round to have PASSed before closure, and F272 has never run
one: the ledger holds `Gate: F272 R1` through `Gate: F272 R26` and not one of them claims
the full suite.

THE BUILT STATE SECTION also discharges the recommendation round 26's worker made and the
reviewer upheld. F272's DECISIONs D1 through D15 live in this feature file; D16, the
split-and-close ruling, lives in `.agent/decisions.md`, because operator amendment
amend0905-throughput names that path and because the direct precedent is identical —
`### DECISION F260 D8`, F260's own split-and-close ruling, sits at
`.agent/decisions.md:10766` while F260's other rulings sit in its feature file. The
placement is right, but nothing in this file pointed at D16. BUILTSTATE carries that
pointer.

WHAT THE REVIEWER ALREADY MEASURED, so this round confirms rather than discovers. At
`412ce673`, in the primary checkout, `python3 -B -m pytest -n auto -q` reported
19786 passed, 23 skipped, 1 warning in 131.37s, with ZERO failures. A branch with no
failures at all has an EMPTY branch-only failure set by construction, which is the set the
integration gate exists to find. Report what YOU measure; if your branch run disagrees
with that reading, that disagreement is the round's finding and you stop.

====================
Bundle
====================

C0a  save this block verbatim to `.agent/authored/f272-r27.md`
C0b  mirror the same bytes to `.agent/last_block.md`
C1   `.agent/plan.md` replaced byte for byte with PLANF272R27
C2   `.agent/live_review.md` — append RECORDR27, the round 26 PASS gate entry
C3   `.agent/prose_slips.md` — append SLIPSR27, one dated line
C4   `docs/roadmap/features/T2_F272.md` — append BUILTSTATE
C5   the integration-gate evidence directory `.agent/gate_f272_r27/`
C6   `.agent/handoff.md` rewritten

====================
Change set — exactly these paths and nothing else
====================

    .agent/authored/f272-r27.md
    .agent/last_block.md
    .agent/plan.md
    .agent/live_review.md
    .agent/prose_slips.md
    docs/roadmap/features/T2_F272.md
    .agent/gate_f272_r27/                    (NEW DIRECTORY, created by C5)
    .agent/handoff.md

NOTHING under `packages/`, `apps/`, `tests/`, `scripts/` or `README.md` changes this
round, and no STATUS line is touched. No production line moves, so no red-proof is
ordered or possible. If a measurement forces a path outside this list, APPLY IT AND
DECLARE IT.

====================
Constraints
====================

1. This block is applied verbatim. If a slice is wrong, apply it as written and declare
   the disagreement; never silently correct it.
2. Every authored slice is extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f272-r27.md`, between its `<<<BEGIN NAME>>>` and `<<<END NAME>>>`
   lines, exclusive of both marker lines and INCLUSIVE of the newline ending its last
   content line. This round carries no FROM/TO pair, so round 26's second extraction
   convention does not arise. Never retype a slice.
3. C0a and C0b are `shutil.copyfile` of `.remedy-wt/f272-r27-block.md`.
4. BOTH APPENDS IN THIS ROUND ARE `post == pre + b"\n" + slice`. Each target ends in
   EXACTLY ONE newline at the base commit, measured per file rather than generalised:
   occurrences of three consecutive newlines at `412ce673` are 0 in
   `.agent/live_review.md`, 1 in `.agent/prose_slips.md` (offset 39213, pre-existing) and
   0 in `docs/roadmap/features/T2_F272.md`. None is load-bearing and none is repaired.
5. BUILTSTATE APPENDS A NEW SECTION AND EDITS NO LANDED TEXT. §3 item 20 forbids
   overwriting a landed ruling, so the fifteen `### DECISION F272 D` sections are left
   byte-unchanged and the count stays 15 after the append, not 16 — BUILTSTATE contains
   no DECISION heading.
6. THIS ROUND MINTS NO FINDING ID. Round 26 PASSED. The one gap its verdict named is the
   reviewer's own block prose and reached no product state, so under amend0827 rule 2 it
   is a dated `.agent/prose_slips.md` line. `R-0826` must still be free when the round
   ends.
7. THE BASE COMMIT FOR THE BASE RUN IS THE FORK POINT `b18fad576252f7f2739a5807b6408031da8fcde6`
   AND NEVER `git merge-base`. This branch has merged `main` in, so the two differ, and
   the reviewer measured both at `412ce673`: at the fork point
   `git rev-list --ancestry-path <base>..HEAD` and `git rev-list <base>..HEAD` both return
   213; at the merge-base `148fbd0b` they return 184 and 205. That inequality is the exact
   shape that packaged F260's round 22 attempt as BLOCKED_EVIDENCE, and the same base is
   the one the closure round's review zip will use. Re-run BOTH counts at the fork point
   and report them.
8. DESTRUCTIVE AND BASE VERIFICATION IS ISOLATED. The base run happens ONLY in a
   disposable `git worktree` created ON A THROWAWAY BRANCH (`git worktree add -b
   tmp/f272-base-gate <path> <fork-point>`) — a DETACHED head fails the self-dogfood
   branch guard by design. Remove it, prune, delete the throwaway branch, and prove with
   `git worktree list`. The primary checkout satisfies `git status --porcelain` == empty
   at every commit boundary. `git worktree list` is 13 entries at the base and must be 13
   again at the end.
9. RUN LOGS ARE WRITTEN OUTSIDE THE REPO WHILE A SUITE RUNS — use `~/remedy-gate-scratch/`
   — and are copied into `.agent/gate_f272_r27/` only AFTER the run exits. A log growing
   inside the repo during a run changes the worktree digest mid-run and fails the
   manifest-identity ids as false positives (R-0176). Every evidence file is named `.txt`
   and NEVER `.log`: `.gitignore` drops `*.log` silently and the review-zip guard rejects
   any `\.log$` member (R-0169).
10. Read `.agent/STOP` with `os.path.exists` before C0a, before C5 and before C6, and
    report all three readings.

====================
Done when — the gates
====================

Run every gate with `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, no pipe between the command
and the echo. Report ONE LINE PER GATE with the transcripts below it. Every gate runs
before C6, the commit that writes the handback.

G1 TRANSPORT. One digest comparison: `.remedy-wt/f272-r27-block.md` as delivered against
   the committed `.agent/authored/f272-r27.md` and the committed `.agent/last_block.md`.
   Report sha256, byte length and line count for each of the three.

G2 THE FINDING RECORD, over the single append at C2, against its own pre-image.
   (a) BYTE: pre_len, pre_sha256, post_len, post_sha256, the terminal twelve bytes and
       trailing-newline run of each, `PRE_IS_BYTE_EXACT_PREFIX_OF_POST` and
       `POST_EQUALS_PRE_NL_SLICE`. At the base the pre-image is 1215841 bytes, 2133 lines,
       sha256 beginning `d371b0aa6ab99916`.
   (b) STRUCTURAL: strip the single terminal newline, split on blank lines, compare the
       LAST N units against the slice's paragraphs IN ORDER, where N is COUNTED BY YOUR
       SCRIPT from the slice and never taken from this block. Report N, units before,
       units after and `EVERYTHING_BEFORE_UNCHANGED`.
   (c) NEGATIVE CONTROL on the FIRST paragraph the append adds, in memory only, never on
       disk: flip one byte, require BOTH readers to reject it, then re-read the file and
       confirm it is byte-identical to the real post-image.
   (d) COUNTS, each measured, none adjusted to agree:
           ^- R-\d{4} distinct        309 -> 309
           ^Done: R-\d{4} distinct    252 -> 252
           open set BY DISTINCT ID     57 ->  57
           ^Gate:                      49 ->  50
           ^Gate: F272 R26              0 ->   1
           ^- R-0826                    0 ->   0
       Report OPEN FINDINGS BY DISTINCT ID with its arithmetic.

G3 THE TWO PROSE FILES. `.agent/plan.md` is byte-equal to PLANF272R27; report its bytes,
   its line count against the AGENTS.md cap of 50, and that `## Goal` and `## Next Steps`
   are both present. `.agent/prose_slips.md` gets the byte append check only — pre_len
   150774 and pre_lines 563 at the base, and `POST_EQUALS_PRE_NL_SLICE` for SLIPSR27.

G4 THE FEATURE FILE, over the append at C4. Report pre_len, pre_sha256, post_len,
   post_sha256, `PRE_IS_BYTE_EXACT_PREFIX_OF_POST` and `POST_EQUALS_PRE_NL_SLICE`. At the
   base the pre-image is 62897 bytes and 768 lines, sha256 beginning `075e72d74c8a382a`.
   Then report `^### DECISION F272 D` headings before and after — 15 at the base and 15
   after, per constraint 5 — and `^## Built State` before and after, which is 0 then 1.

G5 THE INTEGRATION GATE, BRANCH RUN, per `docs/agents/integration_gate.md` step 1, in the
   PRIMARY checkout at C4:
       python3 -m pytest -n auto -q
   Record the raw tail, the FULL `FAILED` list, the real exit code and the wall time, and
   write the sorted FAILED lines to `branch_failed.txt`. The reviewer measured 19786
   passed, 23 skipped and ZERO failures in 131.37s at `412ce673`; REPORT WHAT YOU MEASURE.
   A non-zero failure count here is the round's finding: STOP and hand back with the full
   output rather than continuing to the base run.

G6 THE INTEGRATION GATE, BASE RUN, per `docs/agents/integration_gate.md` step 2, at the
   FORK POINT constraint 7 names, in the throwaway worktree constraint 8 requires.
   RESTORE ARTEFACT PARITY BEFORE THE RUN: copy `apps/ui/node_modules` (305 MB) and
   `apps/ui/dist` from the PRIMARY checkout into the base worktree with
   `shutil.copytree(src, dst, symlinks=True)` — THE `symlinks=True` ARGUMENT IS ORDERED,
   NOT THE FUNCTION: `copytree` defaults to `symlinks=False`, and that default
   dereferenced npm's bin shims and CAUSED base-only failures on a previous gate
   (R-0591). Set `REMEDY_UI_NO_AUTO_BUILD=1` for the base run but do NOT trust it alone.
   VERIFY THE NEUTRALISATION BY MEASURING THE EVENT, NOT THE OUTCOME (R-0444): record the
   mtime of every file under the base worktree's `apps/ui/dist` before and after the run
   and report the run window; ANY mtime falling inside that window VOIDS the parity claim
   and forces per-id attribution. Then the same command as G5, its raw tail, FULL FAILED
   list, real exit code and wall time, sorted into `base_failed.txt`.

G7 THE COMPARISON, per `docs/agents/integration_gate.md` step 3, over the two sorted
   files:
       comm -13 base_failed.txt branch_failed.txt      # BRANCH-ONLY — the gate's verdict
       comm -23 base_failed.txt branch_failed.txt      # base-only
   Report both lists IN FULL and never truncated. THE BRANCH-ONLY SET IS THE GATE'S
   VERDICT CRITERION and G5's reading makes it empty by construction: a branch with zero
   failures can have no branch-only failure. Any branch-only id is a BLOCKER — stop and
   hand back. For base-only ids, attribute EVERY one to the environment class BY DIRECT
   EVIDENCE, naming the missing or stale artefact per id; an unattributed base-only id
   counts as a genuine base failure and blocks the gate verdict. Expect this class to be
   populated: finding R-0445 records that this procedure manufactures false base failures
   on every run, and the copied-artefact mtime interaction with `git worktree add`'s own
   stamping has produced roughly a hundred of them before. Write every list, both suite
   tails and the attribution table into `.agent/gate_f272_r27/` as `.txt` files at C5.

G8 THE TREE. `git status --porcelain` EMPTY at every commit boundary with the real output
   each time. `git ls-files .remedy-wt` empty. `git worktree list` back to 13 entries with
   the throwaway branch deleted. Per-commit insertions from `git diff --numstat <parent>
   <commit>` for C0a through C5 — C6 excluded, because a commit cannot count its own
   insertions while it is being written — each under the DECISION F104 D1 cap of 500. If
   the gate evidence at C5 exceeds that cap it is ONE indivisible artefact: declare the
   overage WITH its inseparability reason in the handback BEFORE review, per AGENTS.md
   Commit Discipline, and say that it is this feature's only such commit. The three
   `.agent/STOP` readings.

====================
Handback
====================

Rewrite `.agent/handoff.md` completely: `SESSION 12 of feature F272 · round 27 · rounds
so far 27`; the soft-limit reading; one sentence of context self-assessment; the range; a
per-commit changed-files table whose `+/-` column comes from `git diff --numstat` and is
compared cell for cell against G8's figures; the item-status table for C0a through C6; one
line per gate with the transcripts below it; every deviation and assumption. It has no
length cap. Record the integration gate's two wall-clock times and the exact failure
counts, because the closure round's runtime-actuals section reads them from here.

<<<BEGIN PLANF272R27 target=.agent/plan.md>>>
# Plan — F272 One world completion

Branch: feature/f272-one-world-completion. Rounds 1 to 26 PASSED except round 2 (premise
corrected by DECISION F272 D2) and round 21 (R-0824, repaired by round 22). T001, T002 and
T003 are COMPLETE; T004 is part-done and its remainder plus T005 are F274's, registered in
round 26 by DECISION F272 D16.

## Goal

Close F272 at the self-consistent scope DECISION F272 D16 fixed. Session 12 reached the
soft limit of 12 sessions, so the remaining work is the closure sequence of
`docs/roadmap/STATUS_closure_protocol.md` and no further building.

## Current Step

Round 27, two closure preconditions in one round: the feature file's Built State section,
which precondition 4 requires and which does not exist yet, and the dedicated
integration-gate round precondition 2 requires and which F272 has never run.

## Next Steps

1. The self-use round precondition 6 requires: the queue holds no pending item, so call
   `generate_and_append_if_empty` first, then plan it, run it, and register every string
   `describe_self_use_run_defects` returns as a normal R-id finding.
2. The evidence job and a FRESH review zip. Its `base_commit` is the FORK POINT
   `b18fad57`, never `git merge-base`, which differs on this branch and packages
   BLOCKED_EVIDENCE.
3. Ledger rotation by `scripts/rotate_live_review.py`, as its own commit, after the
   verdict bookings and before the STATUS flip.
4. The closure commit: the STATUS `[x]` line with the README capability sync in the SAME
   commit, then the PR. The PR is NOT merged this session.

## Risks

- Four open findings are High — R-0803, R-0804, R-0806 and R-0807 — all four booked to
  F273's T001 by the 2026-09-06 triage. The close is PASS_WITH_RISKS and names them.
- A failing review-zip build is a closure BLOCKER; the round that hits one stops.
- The base run's environment-coupled failures are a known class (R-0445); every one is
  attributed by direct evidence or the gate verdict is blocked.
<<<END PLANF272R27>>>

<<<BEGIN RECORDR27 target=.agent/live_review.md mode=append>>>
Gate: F272 R26 — the F272 round 26 entry. VERDICT PASS, AND EVERY GATE WAS RE-RUN BY THE REVIEWER RATHER THAN READ, in the primary checkout at `412ce673`. THIS IS THE ROUND THAT EXECUTED THE SPLIT HALF OF THE amend0905-throughput SPLIT-AND-CLOSE DEFAULT, session 12 having reached the soft limit operator amendment amend0906-triage-throughput rule 2 set for this feature by name at 12 sessions and 40 rounds. Range `9f99f286`..`412ce673`, eight commits, every one single-parent, in exactly the ordered sequence C0a, C0b, C1, C2, C3, C4, C5, C6, with `git diff --stat` naming exactly the seventeen declared paths and nothing under `packages/`, `apps/` or `scripts/`; the ONE file under `tests/` is `tests/docs/test_docs_consistency.py`, whose only change is the ledger pin and its comment. G1 TRANSPORT IS A REAL CHAIN: the reviewer's own scratch original `.remedy-wt/f272-r26-block.md`, written and hashed BEFORE delegation, and the committed `.agent/authored/f272-r26.md` and `.agent/last_block.md` are all 37396 bytes at 490 lines and all hash to `9d2dbe2ee13e0fd9cab718a6d604ba9aa063d147a5f51d9ee85e6527996d7b02`; per §3 item 37 that chain covers those artefacts and is not a claim about the bytes emitted into a prompt. G2 THE RECORD: 1212690 to 1215841 bytes with the pre-image a byte-exact prefix and `POST_EQUALS_PRE_NL_SLICE` true; the reviewer re-ran the structural reader at N counted from the slice as 1, units 731 to 732, and flipped a byte inside the FIRST appended paragraph, which BOTH readers rejected while both accepted the real post-image; registrations 309 unchanged, resolutions BY DISTINCT ID 252 unchanged, open set 57 unchanged, `^Gate: ` 48 to 49, `^Gate: F272 R25 ` 0 to 1, `^- R-0826 ` 0 to 0. G3 THE DECISION RECORD: 860210 to 865296 bytes, byte-exact prefix, `## DECISION F272 D16` heading exactly one section. G4 THE PROSE FILES: the plan is 1990 bytes at 40 lines against the cap of 50 and byte-equal to its slice; `.agent/prose_slips.md` gained six lines by the ordered relation. G5 THE REGISTRATION COMMIT IS THE ONE THIS ROUND COULD NOT GET WRONG AND IT IS EXACT: `git diff --name-only 1a04f5a6 8912bfec` lists precisely ten paths; `docs/roadmap/features/T2_F274.md` is 8056 bytes at 116 lines hashing to `c880e0e119e6c3c9d3df21b5fabe16215a611b62b1e485dd876d338290d60312` and byte-equal to the F274FILE slice; the F274 STATUS line sits IMMEDIATELY below F272's under a heading beginning `## Tier 2 —`, which is what makes Rule A5 propose F274 next and what keeps `test_the_filename_tier_matches_the_status_tier` green; `TOTAL_FEATURES = 274` occurs once and `= 273` zero times; each of the six dependency files carries `F274 (` exactly once; `README.md` carries `74 of 274 registered items accepted.` and the Tier 2 row at Done 17, Total 27; and F272 is still `[~]`, the `[x]` flip belonging to the closure round. G6 THE DOCS GATE AND LINT, all four RE-RUN BY THE REVIEWER at `412ce673`: `tests/docs/` exit 0 at 303 passed, `tests/orchestration/test_roadmap_index.py` exit 0 at 30 passed, `tests/cli/test_golden_path.py` exit 0 at 42 passed, and `ruff check tests/docs/test_docs_consistency.py` exit 0 at "All checks passed!". G7 THE TREE: porcelain empty, `git ls-files .remedy-wt` empty, worktrees 13 to 13, per-commit insertions 490, 424, 26, 2, 6, 131, 16 and 460, every one under the DECISION F104 D1 cap of 500. BOTH OF THE WORKER'S DECLARED DISAGREEMENTS ARE UPHELD AND BOTH ARE THE REVIEWER'S. FIRST, constraint 7 asserted that RECORDR26 "adds no occurrence of it at all" for `R-0826`, and the slice contains that string once, inside a backticked gate name, so the file goes 2 to 3 occurrences as prose; the load-bearing property was gated separately and held, `^- R-0826 ` reading 0 before and 0 after, so the id is still free and this is reviewer prose that reached no product state — one dated `.agent/prose_slips.md` line under amend0827 rule 2, no id, no correction round. SECOND, the worker measured that `.agent/decisions.md` held ZERO `^## DECISION F272 D` lines before this round, so G3's count reads 0 to 1 rather than 15 to 16, F272's D1 through D15 being sections of `docs/roadmap/features/T2_F272.md`; the gate asserted no expected value, so nothing false landed, and the reviewer confirms the PLACEMENT is correct rather than the numbering being broken — operator amendment amend0905-throughput names `.agent/decisions.md` by path for the split ruling, and the direct precedent is identical, `### DECISION F260 D8` sitting at `.agent/decisions.md:10766` while F260's other rulings sit in its feature file. The pointer the worker asked for already exists where that precedent puts it, at line 4 of `docs/roadmap/features/T2_F274.md`, and the reviewer additionally takes the recommendation into round 27's Built State section, which touches the parent file anyway. No id is minted for either.
<<<END RECORDR27>>>

<<<BEGIN SLIPSR27 target=.agent/prose_slips.md mode=append>>>
2026-09-07, F272 round 26 — the block's constraint 7 asserted that the RECORDR26 slice "adds no occurrence of it at all" for `R-0826`, and the slice contains that string once, inside a backticked gate name in its own G2 summary, so the file went from two occurrences to three. The load-bearing property was gated separately and held. The lesson is the R-0584 class arriving from the other side: a claim that a slice does not USE a token must be measured over the slice's bytes INCLUDING its quotations, because the count a later reader takes will include them; state the property the gate actually measures — here `^- R-0826 ` registrations, which stayed 0 — rather than a whole-text absence the slice does not have.
<<<END SLIPSR27>>>

<<<BEGIN BUILTSTATE target=docs/roadmap/features/T2_F272.md mode=append>>>
## Built State (2026-09-07, rounds 1 to 27, ledger `Gate: F272 R1` to `Gate: F272 R26`)

WHAT THIS FEATURE BUILT. This is the scope its accepted STATUS line covers, and it is
smaller than the Goal & Done section above asks for — deliberately, and by DECISION F272
D16, which is recorded in `.agent/decisions.md` rather than in this file because operator
amendment amend0905-throughput names that path for a split-and-close ruling and because
the direct precedent, `### DECISION F260 D8`, sits there too.

**T001 — the plural run list and the run re-key: COMPLETE.** `Job.run_refs` exists and is
truthful, and `run_log_dir` and `pingpong_run_dir` collapsed onto one `run_dir` keyed by
RUN id, per DECISION F260 D1 as DECISION F272 D1 staged it. The test-side spelling sweep
DECISION F260 D6 declined was taken here, with the pre-sweep and post-sweep pair its own
red-proof needed.

**T002 — the rest of the unified record: COMPLETE.** The administrative fields and the
Mission extension. DECISION F272 D4 settled `job_id` as the ONE required key; D5, D6 and
D7 staged the `state` collapse as three moves — widen, rename, retype — with the rename
set determined by RUNTIME PROBE rather than by static classification, because `.status` is
polymorphic in this repository. D8 and D9 carried the cockpit half; D11 settled the
Mission contract's shape.

**T003 — move the consumer list: COMPLETE**, per DECISION F272 D12, which also ruled that
the five `tests.md` ids this file's Acceptance section names — R-0803, R-0804, R-0807,
R-0810 and R-0812 — are F273's and not this feature's.

**T004 — delete the classic runner: PART-DONE.** Rounds 20 to 22 deleted `job run-loop`,
its handler, its tests and its two prose advertisements, under DECISION F272 D13's rule
that a command's advertisements die in the same commit as the command.

## Which slices moved to F274

THE REMAINDER OF T004 AND THE WHOLE OF T005 ARE F274'S, by DECISION F272 D16 in
`.agent/decisions.md` — the ruling that closed this feature at the
amend0906-triage-throughput soft limit of 12 sessions and placed F274 directly after it
per amend0906-split-placement. A reader following this file's D1 to D15 should continue
there; D16 is the sixteenth in this series and the only one not kept in this file.

- **From T004:** `job.run --cycles`, `job.run-next` and its sixteen live rails, their
  handlers and tests, the DECISION F260 D5 resolver collapse, `resolve_any_job_id`, the
  "TWO job stores" paragraph, every which-store branch and the absence test — all of it
  behind the classic-to-unified record flip DECISION F272 D15 measured and ruled ATOMIC.
- **The whole of T005:** the D11c reachability test, the two carry-overs F260's Design
  section names, DECISION F260 D3's deletion paragraph, and the cluster deletion itself.
  It was never begun here, so this feature leaves NO half-performed deletion behind, which
  is the one state the Orchestrator brief above forbids.

WHAT IS THEREFORE STILL OPEN AGAINST THIS FILE'S OWN "Goal & Done": the Acceptance list it
inherits from `docs/roadmap/features/T2_F260.md` is NOT fully satisfied, and DECISION F260
D3 is NOT yet written. Both are F274's, and this feature closes saying so rather than
narrowing the contract to fit what it reached.
<<<END BUILTSTATE>>>
