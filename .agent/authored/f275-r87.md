── STEP T003 — F275 — ROUND 87 ──
Goal: Re-derive the flip's input and re-run its transform at `bd2a75d5`, classify with a
committed instrument the full-suite transcripts the reviewer took there, land that reading as an
artefact, correct the record on F275's spent oversize allowance, and file the operator question.

Base commit: `bd2a75d5`. Round type: SPLIT. NO PRODUCTION PATH CHANGES: nothing under
`packages/`, `apps/`, `tests/`, `docs/` or `scripts/`.

THE FRAME RULE, per item 37 of §3, stated as the property MEASURED over the final bytes: NO LINE
of this block is a run of a single repeated character, and every box-drawing rule inside the
STEP and SLICE header lines is exactly two characters long.

## Bundle — the ordered commit sequence

C0a `.agent/authored/f275-r87.md`             the block, saved verbatim
C0b `.agent/last_block.md`                    mirrored FROM THE COMMITTED C0a BLOB
C1  `.agent/plan.md`                          slice PLAN87, a full replacement
C2  `.agent/live_review.md`                   slice RECORD87 appended, the round 86 verdict
C3  `.agent/prose_slips.md`                   slice SLIPS87 appended
C4  `.agent/authored/f275-r87-residue.py.md`  SPEC I, the worker's instrument
C5  `.agent/f275_t003_flip_residue_r87.md`    SPEC A, the artefact
C6  `.agent/decisions.md`                     slice DEC87 appended
C7  `.agent/operator_questions.md`            slice OPQ87, a full replacement
C8  `.agent/handoff.md`                       the handback

C1 is the FIRST SUBSTANTIVE COMMIT, per item 23 of §3.

## Change — exactly these paths and no others

The Bundle's paths.

## The pinned inputs — taken by the reviewer, read by the worker, NEVER regenerated

Under `/home/decodeux/Repos/remedy/.remedy-wt/`. Check each sha256 before use; if one is missing
or differs, STOP and hand back without rebuilding it.

 `r87/suite_ctl.out`          sha256 5b0883648f5a96b760194861ae0d3d9919a880b6a05f589f5d3856a316659463
 `r87/suite_flip.out`         sha256 33d2cdaecb8d1ae86b306be999babf44311442df399c43920d0a807b9f32faa7
 `r87/suite_flip_short.out`   sha256 8f79bcdba6702f237b520c42f0319d870495bfe0e8ed1dae2ed63f3b023df96e
 `r77_corrected.json`         sha256 765b5ba99f2c92765349c3a013f4074c62ece893cb50b373450927af0290a512
 `r77_corrected_owners.json`  sha256 670c6e952667b7c52b6c5a9ffd832dcc9f096aedfba114b83bc28ca061591b44
 `r61_status.json`            sha256 a4c6cd631b6669ea9ef58418e09471258f433a76e46c79e1ae363cf3eaad1e38

The three transcripts are full-suite runs, `python3 -B -m pytest -q -p no:randomly
-p no:cacheprovider`, taken at `bd2a75d5` inside registered worktrees since removed: `suite_ctl.out`
unflipped with `--tb=line -rfE`; `suite_flip.out` flipped with `--tb=line -rfE`;
`suite_flip_short.out` flipped with `--tb=short -rfE`. The flipped tree's path prefix inside them
is `/home/decodeux/Repos/remedy/.remedy-wt/r87/wt_flip`. Nothing else under `.remedy-wt/r87/` is
opened.

## SPEC I — `.agent/authored/f275-r87-residue.py.md`, at C4

A carrier holding exactly ONE ```python fence, extracted and never retyped, which embeds no
commit and no repository path; the three transcripts and the prefix arrive as arguments. Its
stdout carries no wall-clock value and every listing over a set is sorted, so two runs agree
byte for byte. It prints:
I1 for each transcript, pytest's final tally line with its ` in <seconds>s (<clock>)` suffix
removed, and the count of distinct node ids on lines matching `^(FAILED|ERROR) (\S+)`.
I2 the flip-only set (`suite_flip.out` minus `suite_ctl.out`) and the control-only set by count,
and the symmetric difference of the two flipped transcripts' sets listed by node id.
I3 over `suite_flip_short.out`, every section between the `= ERRORS =` or `= FAILURES =` heading,
whichever comes first, and the `short test summary info` line, split at lines matching
`^_+ (.+?) _+$`. A section's EXCEPTION CLASS is group 1 of its LAST line matching
`^E   (\S+?): (.*)$`, else `<none>`. Its DEEPEST IN-TREE FRAME is the last line matching
`^(\S+\.py):(\d+): in (\S+)$` whose path, with the prefix and one `/` stripped when present, does
not start with `/` and does not contain `site-packages`; a section with none is UNATTRIBUTABLE. A
frame is PRODUCTION when its relative path does not start with `tests/`.
I4 the section count; the count per exception class; the count per (frame path `::` function,
class) pair for every pair of count 3 or more; the count per production frame path; and the
totals of production, test and unattributable deepest frames.

## SPEC A — `.agent/f275_t003_flip_residue_r87.md`, at C5

Opens with a paragraph stating what the round did and did not do — no production line moved,
no suite was run by the worker, the transcripts are the reviewer's and pinned by digest — then
the generator readings and the transform readings of G4 as measured, then the instrument's
stdout VERBATIM, every stdout line indented by one space and in order. No wall-clock value.

## Constraints

1. NO SLICE IS EDITED. PLAN87, RECORD87, SLIPS87, DEC87 and OPQ87 land byte for byte; a
   discrepancy inside one is DECLARED, never repaired.
2. C4 and C5 are the worker's OWN text from SPEC I and SPEC A.
3. READ `.agent/STOP` before C0a and before C8, with real exit codes. If it appears, finish the
   commit in hand, write the handoff and end.
4. Every commit stages EXACTLY ONE path and stays under 500 insertions.
5. No `.py` file under `.agent/`; scratch under `.remedy-wt/r87w/`, uncommitted; every scratch
   output path absolute.
6. No landed record is rewritten: every `.agent/live_review.md`, `.agent/prose_slips.md` and
   `.agent/decisions.md` commit is an APPEND with a ZERO deletion column.
7. No `gh`, no `remedy`, no pull request, no branch created or deleted, no merge, NEVER a
   force-push, no history rewrite. NO FULL SUITE IS RUN: the transcripts are pinned.
8. G4's worktree is created with `git worktree add --detach` at `bd2a75d5` and REMOVED AND PRUNED
   before C4. The four generator trees are plain directories, never registered worktrees.
9. THE BLOCK'S OWN SIZE, measured on its final bytes: 300 lines TOTAL and 205 lines of
   PROSE, against the caps of 490 and 400.
10. GATE ORDER. G4 runs before C4; G5 and G6 run at C5; DEC87 at C6 quotes them, and item 31 of
    §3 requires that they run STRICTLY EARLIER. G1, G2, G3, G7 and G8 run at C7. No gate runs
    after C8; C8's own numbers are the reviewer's.

## Done when — the gates, each run for real and its exit code recorded

G1 TRANSPORT, BUDGET, SLICES. `.agent/authored/f275-r87.md` at C0a against the block as received,
by `cmp`; `.agent/last_block.md` at C0b byte-identical to the COMMITTED C0a blob. Extract the
slices by their markers, report how many were FOUND, check each against its BEGIN-marker
sha256, and re-measure TOTAL and PROSE against constraint 9.

G2 THE PLAN. `.agent/plan.md` at C1 byte-identical to PLAN87 from the COMMITTED C0a blob; at
most 50 lines; one `## Goal` and one `## Next Steps`.

G3 THE RECORD. For the appends at C2 into `.agent/live_review.md` and at C6 into
`.agent/decisions.md`, FULL FORENSICS: the pre-commit blob read with `git show` at the commit's
PARENT, its length printed — 1119826 and 1264216 — READER A with the arithmetic printed; READER B
over the file's LAST N blank-line units against the slice's N paragraphs IN ORDER, N counted by
the script; a letter flipped in the FIRST appended paragraph REJECTED by both readers; deletion
column 0. `.agent/prose_slips.md` at C3 equals its 296513-byte pre-commit blob followed by
exactly SLIPS87. `.agent/operator_questions.md` at C7 byte-identical to OPQ87. Derive the
ledger's `Gate:` header pattern from the file, report how many heads it matches, and that
RECORD87's header matches it and duplicates none.

G4 THE RE-DERIVATION, before C4. Build `tree_base` from `git archive ef75e213` and `tree_tip` from
`git archive bd2a75d5`, each followed by `git init -q` and `git add -A -f .` inside it;
`tree_shift` and `tree_delete` as copies of `tree_tip` made with `shutil.copytree(...,
symlinks=True)`, the first with three empty lines inserted after line 1 of
`packages/orchestration/brain_detail.py`, the second with that file's one line
`    job_id_str = str(job.id)` removed, its count in that file reported as 1 first, each
re-indexed with `git add -A -f .`. Extract the ONE fence of `.agent/authored/f275-r59-rekey.py.md`,
`.agent/authored/f275-r73-owner-stage.py.md` and `.agent/authored/f275-r82-input.py.md`, and the
two fences of `.agent/authored/f275-r69-transform-guarded.part1.py.md` and `.part2.py.md`
concatenated in that order; report each byte count and sha256 — the reviewer's read f56394e9…,
7be34374…, c50da973… and 075bc0dc…. Run the generator as its carrier's Usage line orders over
the four trees and the two pinned JSON files. The reviewer measured: 21 paths under
`packages/`, `apps/` or `tests/` differing between BASE and TIP; 2183 ruled sites, all 2183
recovered by the scope key at TIP, SHIFT and DELETE with 0 UNRESOLVED; the line-key control 2157
at TIP and 2148 at SHIFT and at DELETE; the owner check at TIP 1908 CONFIRMED, 275 REFUSED and 0
CONTRADICTED. Then run the transform over the worktree of constraint 8 with the TIP re-keyed set,
its owners file and `r61_status.json`. The reviewer measured: PRECONDITION 2183 resolving and 0
not; 264 files rewritten; 6097 total rewrites; 0 broken. In that worktree `git diff --numstat`:
264 files, 5252 insertions and 5079 deletions, 4177 insertions under `tests/` and 1075 elsewhere,
largest single-file insertion count 141. Then, with `ast` over `packages/` at `bd2a75d5`, every
`UUID(...)` call counted by the call it is a positional argument of: the reviewer measured 55,
29 of `load_job` and 4 of `load_job_safe`. Report every reading beside the reviewer's.

G5 THE RESIDUE, at C5. Verify the pinned digests, then run the committed C4 fence TWICE over the
three transcripts and the prefix; the two stdouts are byte-identical. The reviewer measured: the
tallies `1 failed, 18429 passed, 29 skipped, 1 warning`, `796 failed, 17603 passed, 29 skipped,
1 warning, 31 errors` and `795 failed, 17610 passed, 23 skipped, 1 warning, 31 errors`; distinct
bad nodes 1, 827 and 826; flip-only 826 and control-only 0; the flipped transcripts' symmetric
difference exactly
`tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes`;
826 sections; classes AssertionError 233, TypeError 142, AttributeError 114, ValueError 85,
`http.client.RemoteDisconnected` 80, `<none>` 74; deepest frames production 237, test 589,
unattributable 0; the pairs `packages/orchestration/data_paths.py::job_dir` TypeError 80,
`packages/orchestration/job_fulfillment.py::run_job_fulfill` ValueError 46,
`packages/orchestration/pingpong_job.py::_persist_job` TypeError 31 and
`packages/orchestration/flight_plan.py::map_flight_plan_to_tasks` TypeError 12. Report every
reading beside the reviewer's. At C5 every stdout line appears in the artefact, in order.

G6 THE INSTRUMENT CAN FAIL, at C5, over scratch COPIES only. (a) `suite_flip.out` with its one
line `FAILED tests/orchestration/test_job_fulfillment.py::TestApplyScope::test_staged_apply_has_staged_scope`
removed, that line's count reported as 1 first: flip-only must read 825. (b) `suite_ctl.out` with the line
`FAILED tests/test_data_paths.py::TestLookupJobId::test_a_non_hex_string_raises_invalid` appended
after its last `FAILED` line: control-only must read 1. (c) `suite_flip_short.out` with every line
ENDING `packages/orchestration/data_paths.py:201: in job_dir` removed, their count reported — the
reviewer's copy removed 80: the `job_dir` pair must be absent. Report each reading and exit code.

G7 TREE, CANARY, LINT, PATH SET, OPEN SET, at C7. `git status --porcelain` prints `''`;
`git worktree list` one row; the canary `python3 -B -m pytest tests/cli/test_golden_path.py -q`
exit 0, 42 at `bd2a75d5`; `ruff check .` exit 1 with its rows cross-checked against its own
`Found <n> errors.` line, 26 at `bd2a75d5`; the count of `.py` files under `.agent/` on the
filesystem, 0. The changed-path set of `bd2a75d5`..C7 against the Bundle's paths MINUS
`.agent/handoff.md`, MISSING and EXTRA by name. The open set BY DISTINCT ID at `bd2a75d5` and at
C7: 88 at both with identical membership; `R-0809`, `R-0880` and `R-0883` open at both.

G8 THE INSERTION CAP over `bd2a75d5`..C7: one row per commit with insertions, deletions and
staged path count, and the number of commits reaching 500 insertions. Then over
`a5bf8949`..`bd2a75d5` every NON-MERGE commit above 500 insertions with its paths: the reviewer
measured eight, seven rewriting `.agent/handoff.md` alone and `78e5c18c` at 529.

Handback: `.agent/handoff.md` per `docs/agents/handback_template.md`, Session line
`SESSION 30 of feature F275 · round 87 · rounds so far 87`; the Commits table read from
`git show --numstat` and compared cell by cell against G8, C8's row carrying no numbers and
saying why; one Verification line per gate with its REAL exit code; External actions;
Authored-text proofs; Item-status; Deviations; `## Next` stating `Operator questions open: 1`.
NO SCOPE REPORT AND NO SESSION-LIMIT BANNER, by amendment amend0911-f275-to-scope.

── SLICE PLAN87 ── target `.agent/plan.md` ── FULL REPLACEMENT ──
BEGIN PLAN87 sha256=12dfff71d180b560b1aa305c0e092e6766b9dfe7f07e8838ab97804ae4b00e3c
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

ROUND 87 MEASURES THE FLIP AT ITS OWN BASE AFTER THE SEAM WORK, AND CORRECTS HOW IT CAN LAND.
The committed generator re-derives the flip's input at `bd2a75d5`, the guarded transform flips
a worktree, and a committed instrument classifies the full-suite transcripts the reviewer took
there into the failures the flip alone causes. The round records that F275's one declared
oversize commit was spent in round 73, rules that the flip lands as a series of commits each
under the cap, and asks the operator whether to allow one more oversized commit instead. It
books the round 86 verdict and its prose slips.

## Next Steps

1. THE `UUID(...)` PARSES UNDER `packages/` THAT FEED THE JOB STORE, counted by flow and each
   read for how its caller uses the raw value. The largest residue groups raise at the store's
   path join and at `run_job_fulfill`'s parse. Production code, so a SPLIT round with mutation
   red-proofs.
2. THE FLIP'S DRY RUN AGAIN, at the base that round leaves, read for the groups that remain.
3. THE FLIP, carrying DECISION F275 D48's obligations, as a series of commits each under the
   500-insertion cap inside one round, unless the operator allows one more oversized commit.
   The stale test double at `packages/orchestration/project_registry.py:856` moves with it.
4. Then the classic store, then the closure sequence.

## Risks

- THE LIMIT IS LIFTED, not reached: amendment amend0911-f275-to-scope withdraws the 20
  sessions and 60 rounds without a replacement, so this feature closes only at full scope.
- THE FLIP IS NOT CLOSE: at `bd2a75d5` it breaks 826 test nodes the unflipped tree passes.
- ONE ROUTED LOAD IS REACHED BY NO TEST until `R-0883` is repaired.
- THE INPUT SET IS REPRODUCIBLE ONLY FROM ROUND 77's TWO SCRATCH JSON FILES, and the re-key
  cannot see a deleted ruled site.
- The open set is 88 by distinct id at this round's base, with `R-0809`, `R-0880` and `R-0883`
  open. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
END PLAN87

── SLICE RECORD87 ── target `.agent/live_review.md` ── APPEND ──
BEGIN RECORD87 sha256=770e942105badf349aea56de206a5dc223f6de5f8ead80b60f4755e9c3ab148f

Gate: F275 R86 — the F275 round 86 entry. VERDICT PASS. Written by the planner and reviewer of session 30 after reading the committed range `b0ef6ab4`..`bd2a75d5` and RE-DERIVING EVERY GATE AND EVERY RED-PROOF INDEPENDENTLY; the worker's report and its transcripts were evidence for no line below. It is booked here by the FIRST SUBSTANTIVE COMMIT of round 87 that writes the record, per operator amendment amend0827-process-diet rule 1. The round changed production code and the reviewer ran its own thirteen mutations in its own worktree before writing this.

WHAT THE TRANSPORT PROOF COVERS, per item 37 of §3. The committed `.agent/authored/` blob was identical to the reviewer's own original at 27925 bytes, `.agent/last_block.md` equalled it, all five slices matched their BEGIN-marker digests, and the block re-measured at 291 lines TOTAL and 220 PROSE. `.agent/plan.md` equalled its slice at 41 lines. The four appends were exact under reader A — 1114453 plus 3351 and then plus 2022 into the review record, 295435 plus 1078 into the prose slips, and 1260475 plus 3741 into the decisions — with reader B holding at N counted from each slice as 4, 1, 2 and 8, and a letter flipped in each FIRST appended paragraph rejected by both readers. Every commit staged one path except C5, which staged the seven handler files, and the largest commit was 291 insertions.

THE PRODUCTION CHANGE HOLDS UNDER THE REVIEWER'S OWN RE-RUN. The seven handler files at C5 are byte-identical to the files the reviewer produced by applying SPEC F to `b0ef6ab4` in its own worktree before authoring, and no path under `apps/`, `packages/`, `docs/` or `scripts/` changes after C5. Read with `ast` at C6, the `UUID(...)` calls under `apps/cli/` fell from 21 — 12 into `load_job`, 8 naming a project, 1 other — to 9 with none into `load_job`, and `load_job(lookup_job_id(...))` calls rose from 0 to 10. In a worktree at `2129a67b` whose module the reviewer printed as resolving inside it, the 49-test selection passed unmutated. Restoring the parse at each of the eight user-argument sites failed only that site's parameter; at `readiness project` only the stored ping-pong test; at `attach-job`, for the parse and for the raw key alike, only the attach test; at `job stop`'s loader only the unhyphenated-id test; and at `dashboard project` nothing, as FIND86 predicted. The scoped suite in the primary checkout read 13272 passed, 10 skipped and 0 failed, the base's 13261 plus exactly the eleven new node ids; `ruff check .` rows compared as a multiset at `b0ef6ab4` and at C6 differ by nothing, at 26 each; the canary read 42; `dashboard project` through the real CLI at C6 exited 1 ending `ModuleNotFoundError: No module named 'packages.orchestration.project_store'`; and the open set went from 87 to 88 at C3 with `R-0883` the only id added, `R-0809` and `R-0880` open throughout.

ONE DEFINITION THE BLOCK LEFT UNSTATED, AND THE WORKER STATED IT. G4's census did not say whether an import alias is followed, which is the omission round 85's slip line had named one round earlier. The worker wrote the definition beside its counts and measured that the one alias of `load_job` under `apps/cli/`, in `patch.py`, hides no `UUID(...)` call, so the counts stand under either reading.
END RECORD87

── SLICE SLIPS87 ── target `.agent/prose_slips.md` ── APPEND ──
BEGIN SLIPS87 sha256=74e778bdb8e80c782a0abdbeeb816566ce67cde8f1f5f3f5fd8850ebbed39d86

2026-09-13 · F275 R86 · The round 86 block's G4 defined its census by what each `UUID(...)` value flows into and did not say whether an import alias is followed, one round after a slip line had recorded that exact omission; the worker stated the definition beside its counts. THE RULE THAT FOLLOWS: before a block leaves, the slip lines of the two rounds before it are read against it, because a lesson on an append-only list binds only the reviewer who reads it before writing.

2026-09-13 · F275 R82 · DECISION F275 D56 and every plan since round 82 treat F275's one declared-oversize allowance as still free for the flip, while round 73's ledger entry had recorded it spent by an `.agent/authored/` carrier of 529 insertions, and no block since has re-measured it. THE RULE THAT FOLLOWS: an allowance that can be spent once is re-measured over the commit range, by command, before any sentence relies on it being unspent.

2026-09-13 · F275 R87 · While preparing round 87 the reviewer's gate runner wrote a transcript named by a relative path into the primary checkout's root, because the runner resolved the path against its own working directory rather than the command's; `git status --porcelain` showed the file and it was moved into scratch before any commit. THE RULE THAT FOLLOWS: a scratch runner is given absolute output paths only.
END SLIPS87

── SLICE DEC87 ── target `.agent/decisions.md` ── APPEND ──
BEGIN DEC87 sha256=435031a68f9b24c9392e857e234b1e30d10f570428821c101537efcc409421cf

## DECISION F275 D61 (2026-09-13, F275 round 87) — the flip's dry run at its own base after the seam work breaks 826 test nodes; F275's one declared-oversize commit was spent in round 73, so the flip lands as a series of commits under the cap unless the operator allows another

CONTEXT. `.agent/plan.md` since round 82 names the flip as the next step and DECISION F275 D56 fixed its input with a committed generator to be re-derived at the flip's own base. Rounds 83 to 86 then changed the job-id seam in production, so the last dry run, round 77's, describes a tree that no longer exists. Before this round was authored the reviewer re-derived the input at `bd2a75d5`, flipped a worktree with the guarded transform of DECISION F275 D43, ran the full suite in that worktree and in an unflipped one at the same commit, and classified the difference. The readings below are the reviewer's at `bd2a75d5`; the gates constraint 10 of round 87's block runs before the commit that lands this paragraph reproduce them.

THE MEASUREMENT. Twenty-one paths under `packages/`, `apps/` and `tests/` differ between `ef75e213` and `bd2a75d5`, and the committed generator still recovers all 2183 ruled sites by their scope key with none unresolved, where the line-key control recovers 2157; the shipped owner check reads 1908 confirmed, 275 refused and none contradicted. The transform resolves all 2183 keys, rewrites 264 files by 6097 rewrites and breaks none, and the flipped tree differs from its base by 5252 insertions and 5079 deletions, 4177 of those insertions under `tests/` and 1075 elsewhere, with no single file above 141. The unflipped full suite fails one node, `tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes`, which needs the `apps/ui/node_modules` a worktree lacks. The flipped suite has 796 failures and 31 errors, and 826 of those nodes are bad only under the flip. A second flipped run with short tracebacks names the same 826.

WHERE THEY RAISE. By the deepest frame inside the tree, the method of DECISION F275 D53, 237 of the 826 end in production code and 589 in test code. The largest production groups are a `TypeError` joining a `UUID` object onto a path in `data_paths.job_dir`, 80; a `ValueError` from `UUID(...)` of a sixteen-hex id in `job_fulfillment.run_job_fulfill`, 46; a `UUID` that `pingpong_job._persist_job` cannot serialise, 31; and a keyword `TaskEntry` does not accept in `flight_plan.map_flight_plan_to_tasks`, 12. The ui server tests lose their connection 80 times because the request thread dies: the server-side traceback each captures ends in `'_JobPlanAdapter' object has no attribute 'job_id'` 73 times — a read the transform renames on the which-store adapter `ui_server.py` keeps to make a `JobPlan` look like a `Job` — and in the same path join 7 times. At `bd2a75d5` there are 55 `UUID(...)` calls under `packages/`, 29 of them an argument of `load_job` and 4 of `load_job_safe`: the handler seam rounds 84 to 86 closed under `apps/cli/`, reached by the store's other door.

CHOSEN, FIRST: THE NEXT PRODUCTION ROUND IS THAT SEAM UNDER `packages/`, and the flip is not attempted before it. ALTERNATIVE: repair the residue inside the flip's own commits, rejected because 826 failures in a commit series that cannot end a round red is a round no worker can finish, and because a pre-flip change to a parse is behaviour-neutral in today's store and provable by a red-proof, which a repair inside the flip is not.

CHOSEN, SECOND, AND IT IS A CORRECTION: THE DECLARED-OVERSIZE ROUTE IS NOT AVAILABLE. Over `a5bf8949`..`bd2a75d5` the reviewer found eight non-merge commits above 500 insertions. Seven rewrite `.agent/handoff.md` alone, which DECISION F104 D1 exempts. The eighth is `78e5c18c`, round 73's 529-insertion `.agent/authored/` carrier, which that round's ledger entry recorded as spending the one oversize commit AGENTS.md's Commit Discipline allows a feature. DECISION F275 D17 chose that route, DECISION F275 D21 sized it, and DECISION F275 D56 says the allowance must be kept for the flip; the last sentence has been false since round 73. Those paragraphs stay as landed and this one corrects them.

CHOSEN, THIRD: THE FLIP LANDS AS A SERIES OF COMMITS, EACH UNDER THE CAP, INSIDE ONE ROUND. At 5252 insertions with no file above 141 that is at least eleven commits, grouped by file. The commits inside the series need not pass the suite; the round's gates are taken at its last commit, and the handback declares the series and its reason before review. AGENTS.md says a diff over 500 lines is split before committing, and that is the rule left once the exception is spent. D17 objected that no rule permits a red intermediate commit, but AGENTS.md states no rule that every commit passes the suite, and the branch reaches `main` through a merge commit, so no intermediate commit is ever a first-parent commit of `main`. ALTERNATIVES: a second declared-oversize commit, rejected because AGENTS.md makes it a finding by construction; a reader that accepts both records so that every commit stays green, rejected by AGENTS.md Scope Control by name; an operator amendment allowing one more oversized commit, not rejected, because it is the operator's to grant — it is the question this round files, and this ruling is what happens if the operator says nothing.

CONSEQUENCE. The flip moves behind one more production round and a repeat of this dry run. `R-0809`, `R-0880` and `R-0883` stay open, and no finding is registered or resolved: the false sentence is reviewer prose and damaged nothing under `packages/`, `apps/`, `tests/` or `docs/`.

HOW TO REVERSE. Delete this paragraph block and the operator question it filed. The flip then returns to DECISION F275 D17's single-commit route, which needs a second oversize commit AGENTS.md does not allow.
END DEC87

── SLICE OPQ87 ── target `.agent/operator_questions.md` ── FULL REPLACEMENT ──
BEGIN OPQ87 sha256=f009f1512642ce5d5950a08032e1bd58595b022ba071178ec8caa231c887b762
# Operator questions — what the loop needs decodeux to know or decide

> Written per `docs/agents/self_drive_protocol.md`, operator amendment
> amend0911-feedback rule C (2026-09-11). Read by `remedy-decisions` on the
> operator's machine and by the orchestrator at every relay. Every entry's body
> stands alone in plain sentences; the heading carries the technical reference.
> Soft cap five; entries leave only by the operator's answer, recorded as a dated
> DECISION by the operator's next amendment, which deletes the entry.

### Q1 — How the big rename lands (2026-09-13, F275, round 87)

What needs deciding. The last large step of the current feature renames how every job record is read and written, across about two hundred and sixty files and roughly five thousand added lines. The project allows one commit of more than five hundred added lines per feature, and this feature already used that allowance earlier, on a tooling file. I have decided that the rename will land as a series of smaller commits inside one working round, where the commits in the middle of the series do not pass the test suite on their own and only the last one does. You can overrule that by allowing one more oversized commit for this feature, so the rename lands as a single commit.

Why it matters. A single commit keeps every commit on the branch in a working state, which helps anyone who later searches the history one commit at a time for the moment something broke. The series keeps the size rule intact but leaves around ten commits on the branch that do not work on their own. The main branch receives the finished work as one merge either way.

My recommendation. Keep the series of smaller commits. The size rule exists so that each change stays reviewable, and a mechanical rename split into groups of files is easier to check than one very large commit.

What happens if you say nothing. The rename lands as the series of smaller commits once it is ready. That is several working rounds away: about eight hundred tests still fail against the renamed code, and those failures are removed first.
END OPQ87
