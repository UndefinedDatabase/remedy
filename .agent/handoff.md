# Handoff — F288, round 6

## Session

SESSION 1 of feature F288 · round 6 · rounds so far 6. Context remaining at
handback: comfortable — the round's own derivations (the render harness's
five files, the drive.mjs CDP sequencing, and the mutation tool's seven
FROM/TO edits across three runners) used a moderate share of the session's
budget; a full context window remains for the next round.

## Range

Review of `cb022003`..`HEAD` (`HEAD` is this handback's own commit, `F288 R6
C6`, on `feature/f288-event-stream-completeness`).

## Commits

### 0247fc9b8 F288 R6 C1: copy round 6 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f288-r6-block.md | 250/0 | copy of this round's block |
| .agent/authored/f288-r6-plan.md | 29/0 | copy of the plan payload |
| .agent/authored/f288-r6-records.diff | 58/0 | copy of the records payload |

Measured insertions: 337 (block's own line count 250 + 87), matching the
block's expectation exactly (and under the 500-line cap).

### 7ccc3cb96 F288 R6 C2: book round 5's PASS, record D6 and the round 6 plan
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 40/0 | DECISION F288 D6 |
| .agent/live_review.md | 2/0 | round 5's Gate entry (VERDICT PASS) |
| .agent/plan.md | 9/9 | round 6's plan (payload rewrite) |

Matches the block's expected numstat (40/0, 2/0, 9/9) exactly.

### e57bc7f2e F288 R6 C3: let the keyboard reach the live picture's prompts through a parallel list
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/graph/BrainGraphStage.tsx | 7/2 | `promptEntries` memo, `<PromptNodeList>` mounted after `<ZoomBreadcrumbs>` in the live branch (S3) |
| apps/ui/src/components/graph/PromptNodeList.module.css | 70/0 | new style module: 1x1 clipped nav, `:focus-within` reveal, no `display: none`/`visibility: hidden` (S2) |
| apps/ui/src/components/graph/PromptNodeList.tsx | 37/0 | new component: `nav`/`ul`/`li`/`button`, `aria-pressed`, `onSelect(entry.promptId)`, no `aria-hidden` (S2) |
| apps/ui/src/components/graph/brainView.test.ts | 51/3 | new `describe("promptListEntries")` block: model order, filtered-out synapse, non-synapse absence, `in_progress`→`current` mapping |
| apps/ui/src/components/graph/brainView.ts | 42/1 | new `PromptListEntry`, `PROMPT_LIST_STATE_WORDS`, `promptListEntries` (S1) |
| tests/ui_contracts/test_brain_stage_mount.py | 54/0 | new `TestPromptNodeListMountsInTheLiveBranchOnly` and `TestPromptNodeListIsTheAccessibleSurfaceForTheCanvassSynapses` classes (S5) |

No insertion count was expected by the block for C3; measured 261 total (6
deletions), under the 500-line cap. One self-review correction folded in
before commit: the first drafts of `PromptNodeList.tsx`'s and its style
module's own header comments spelled out the literal strings `aria-hidden`,
`display: none` and `visibility: hidden` in prose, which tripped the very
S5 tests written to forbid those strings in the PRODUCT files; reworded
both comments to describe the same facts without the literal substrings,
re-ran `pytest` and `ruff` clean, then committed (not a deviation from the
block — no test or product line changed after the reword, only comment
prose, before this commit existed).

### 07de6c6a0 F288 R6 C4a: add the harness's five files for the prompt list's headless-Chrome proof
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f288-r6-render_drive.mjs | 182/0 | CDP driver: C-a through C-f, two screenshots (S4) |
| .agent/authored/f288-r6-render_index.html | 11/0 | harness page shell |
| .agent/authored/f288-r6-render_main.tsx | 85/0 | the stage's live wiring without the stage: demo recording, four-item prompt trace, `buildBrainLayout`, semantic zoom, `<ForceBrainGraph>`/`<PromptNodeList>` |
| .agent/authored/f288-r6-render_measure.py | 191/0 | harness runner, adapted from `f020-r5-conformance_measure.py` (ports 8993/9363, work dir `f288-render-run`) |
| .agent/authored/f288-r6-render_vite.config.mjs | 28/0 | scratch vite config, `fs.allow` reaching `apps/ui/src` |

Insertions: 497 (the five harness files alone). **DEVIATION (declared,
constraint 2):** staging all six C4 files together (the five harness files
plus `f288-r6-render.txt`) measured 527 insertions — over the 500-line cap
— so C4 was split into lettered parts before either was committed: C4a (the
five harness files, 497 insertions) and C4b (the reading, 30 insertions).
Neither part alone reaches the cap; this is the only oversize-avoidance
split in the round and the only such split in this feature's session.

### 53bdf90e6 F288 R6 C4b: record the harness's reading
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f288-r6-render.txt | 30/0 | the harness's own committed output (S4), reproduced byte-for-byte by the G5 re-run below |

### b6802cbc1 F288 R6 C3b: add a test_run coverage case to promptListEntries's vitest suite
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/graph/brainView.test.ts | 11/0 | one new `it`: a hand-built `test_run`-kind node stays absent from `promptListEntries`'s output even when visible |

**DEVIATION (declared):** added after C3 and before building the mutation
tool, anticipating G5's m3 (a `test_run` node wrongly listed) — C3's own
tests proved only that a `task` node stays excluded, which a mutation
widening the kind check to `synapse` OR `test_run` would not have reddened,
since no existing fixture ever placed a `test_run`-kind node in the model.
This is exactly the block's own G5 instruction ("you then say whether a
check can see it, add the one that can, and re-run"), applied before the
first tool run rather than after, to avoid a false first reading.

### 6441ce671 F288 R6 C5: add the mutation tool for the round's red proofs
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f288-r6-mutations.py | 395/0 | route proof + seven ordered mutations across three runners (vitest, pytest, the harness itself) |

No insertion count was expected by the block for C5; measured 395, under
the 500-line cap.

### F288 R6 C6: rewrite handoff for round 6 (this commit — a handoff cannot table the commit that writes it, R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback |

## External actions

- `git worktree add --detach .remedy-wt/f288-r6-mut 6441ce671` — succeeded
  (the official G5 worktree, at C5).
- `python3 .agent/authored/f288-r6-mutations.py
  /home/decodeux/Repos/remedy/.remedy-wt/f288-r6-mut` — the official G5
  run, reported whole in this round's reply; real outcome `ALL MUTATIONS
  CAUGHT AND RESTORED CLEANLY: True`.
- `git worktree remove .remedy-wt/f288-r6-mut --force` then `git worktree
  prune` — succeeded; count returned to 72, matching step 4's reading.
- `git push -u origin feature/f288-event-stream-completeness` — reported
  under G6 in this round's reply (run after this file is committed).
- No `gh pr create`, no `gh pr merge`, no branch deletion, no force-push, no
  `git stash`, no `git checkout`/`git switch` in the primary checkout.

## Verification

### G1 — TRANSPORT
Payload readings (measured before use, against the PAYLOADS table):
- `records.diff`: 58 lines, 13383 bytes, sha256
  `64934cead79ba357bc85d8154391f1d79c88e81ca7c9a6e4a8d5ea28ba06ec25` — MATCH.
- `plan.md`: 29 lines, 1044 bytes, sha256
  `6035ae3a5c0ae1fd5fca6caf2359c612d454d51cab1e7d9f2d273fded3a771c6` — MATCH.
- Block: 250 lines, sha256
  `937863b2a920840faf38bb0bc93fcb6ff11cea4a66640924a9ff55097e550e53` — MATCH.

Each `.agent/authored/f288-r6-*` copy, read back with `git show
0247fc9b8:<path>`, compared byte-for-byte (sha256, both sides) with its
source — all three identical: block copy vs `.remedy-wt/f288-r6/block.md`;
`records.diff` copy vs `.remedy-wt/f288-r6-payloads/records.diff`;
`plan.md` copy vs `.remedy-wt/f288-r6-payloads/plan.md`.

### G2 — THE BOOKING
`git show 7ccc3cb96:<path>`, bytes and sha256, each MATCHING the reviewer's
reading exactly:
```
.agent/decisions.md    bytes=2243664  2420243c48efc1c62bab7d474ad6719fa2b0cad1b3098690186b5a527b9ce670
.agent/live_review.md  bytes=318731   d1188613998e89bf48a901b411142b95972db5929d88d50c76c6c22dd5bc5cf8
.agent/plan.md         bytes=1044     6035ae3a5c0ae1fd5fca6caf2359c612d454d51cab1e7d9f2d273fded3a771c6
```
Open set (`open_finding_ids` from `scripts/rotate_live_review.py` over
`.agent/live_review.md`'s text at `7ccc3cb96`): `[]` — empty.

### G3 — THE CODE
```
$ python3 -m ruff check tests/ui_contracts/test_brain_stage_mount.py .agent/authored/f288-r6-render_measure.py
All checks passed!
REAL_EXIT=0
```
(Run at `HEAD`/C5 tip.)

Quoted from the diff, in full — reported in this round's reply per the
block's WHAT TO REPORT (`promptListEntries`, `PromptNodeList.tsx`, its
style module, and the stage's `promptEntries`/`<PromptNodeList` lines).

### G4 — THE TESTS
```
$ python3 -m pytest -q -p no:cacheprovider -rs <the ordered selection>
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:441: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:484: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543: D3 quarantine (F252) ...
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252) ...
1837 passed, 5 skipped in 110.17s (0:01:50)
REAL_EXIT=0
```
Same five skips as the reviewer's `cb022003` baseline (1828 passed, 5
skipped). Difference: +9 passed. `--collect-only -q` on
`tests/ui_contracts/test_brain_stage_mount.py`: 22 nodes at `cb022003`, 31
at `HEAD` — the nine new tests across
`TestPromptNodeListMountsInTheLiveBranchOnly` (2) and
`TestPromptNodeListIsTheAccessibleSurfaceForTheCanvassSynapses` (7) —
accounts for the difference exactly.

```
$ (cd apps/ui && node_modules/.bin/vitest run)
Test Files  75 passed | 1 skipped (76)
     Tests  1459 passed | 5 skipped (1464)
REAL_EXIT=0
```
The 1 skipped file/5 skipped tests are `scrubLive.test.ts`'s own five
tests, pre-existing and untouched by this round. Difference from the
reviewer's `cb022003` reading (75 files, 1455 passed): +4 tests, 0 new
files. `git diff cb022003..HEAD -- apps/ui/src/components/graph/brainView.test.ts`
shows exactly 4 added `it(` lines (3 in C3's own
`describe("promptListEntries")`, 1 in C3b) — accounts for the difference
exactly.

```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "fail_count": 0, "ok": true, "passed": true, ...}
```
All six checks `pass`, `fail_count` 0.

### G5 — THE PROOFS
Harness (`python3 .agent/authored/f288-r6-render_measure.py
/home/decodeux/Repos/remedy`, run fresh at `HEAD`): whole output reported in
this round's reply, identical text to the C4-committed
`.agent/authored/f288-r6-render.txt` (byte counts included) except the
process pids, which are never part of that file's own content; all six
checks `PASS`, real exit code 0, two PNGs saved and reported with their
byte counts.

Mutation tool, run against `git worktree add --detach .remedy-wt/f288-r6-mut
6441ce671`: reported whole in this round's reply. Summary: the route proof
(brainView.ts broken at its own syntax) turned the worktree's
`brainView.test.ts` red with a transform/resolution failure, proving the
scratch vitest config reads the worktree's own sources; restored
byte-identical. TypeScript runner: control green, m1-m3 each red (1-2
failing tests apiece, matching the mutation's own defect), control green
again. Python runner: control green, m4-m6 each red (1-2 failing tests
apiece), control green again. Harness runner: control green (exit 0, 6/6
checks), m7 red (exit 1, C-e and C-f both failing, as ordered — the harness,
run against a worktree whose `PromptNodeList.tsx` calls
`onSelect(entry.nodeId)`), control green again. `ALL MUTATIONS CAUGHT AND
RESTORED CLEANLY: True`. Every file restored byte-identical after every
mutation; the worktree's `apps/ui/node_modules` symlink created before the
harness runner's block and deleted after it. Worktree removed, pruned;
`git worktree list | wc -l` back to 72, matching step 4's reading.
`git status --porcelain` empty afterward.

## Authored-text proofs

- Block copy (`.agent/authored/f288-r6-block.md`, at `0247fc9b8`) vs
  `.remedy-wt/f288-r6/block.md`: byte-identical (sha256 comparison).
- `records.diff` copy vs `.remedy-wt/f288-r6-payloads/records.diff`:
  byte-identical.
- `plan.md` copy vs `.remedy-wt/f288-r6-payloads/plan.md`: byte-identical.
- `records.diff` applied via `git apply`: `--check` and the real apply both
  exit 0; the payload was never edited or retyped.
- `.agent/plan.md` after the payload rewrite: sha256
  `6035ae3a5c0ae1fd5fca6caf2359c612d454d51cab1e7d9f2d273fded3a771c6`,
  matching the payload's own reading exactly.
- `.agent/authored/f288-r6-render.txt` (C4b) vs the harness's fresh re-run
  at `HEAD`: identical text (checks, screenshot byte counts, exit codes);
  only the server/chrome pids differ, which are process-specific and not
  part of the harness's own pass/fail content.

## Deviations & assumptions

1. **C4 split into C4a/C4b (declared under constraint 2).** Staging the
   five harness files together with `f288-r6-render.txt` measured 527
   insertions, over the 500-line cap. Split before either was committed:
   C4a (497 insertions, the five harness files) and C4b (30 insertions,
   the reading). Neither exceeds the cap; this is the only oversize split
   in the round.
2. **C3b added (declared, anticipating G5's m3).** A vitest test proving a
   `test_run`-kind node never lists, added between C3 and the mutation
   tool's authoring, because C3's own tests only proved a `task` node stays
   excluded — insufficient to catch a mutation that widens the kind check
   to admit `test_run`. Added before the first tool run, per the block's
   own G5 instruction to add the check that can see a mutation.
3. **Two comment rewrites inside C3, before that commit existed.** The
   first drafts of `PromptNodeList.tsx` and its style module named the
   literal strings `aria-hidden`, `display: none` and `visibility: hidden`
   in prose comments, which tripped the S5 python tests forbidding those
   substrings in the product files. Reworded both comments to state the
   same facts without the literal substrings; re-ran `pytest`/`ruff` clean
   before committing. No test or requirement changed — only comment
   wording, caught by self-review before C3 was ever committed.
4. Every other reading in this handback is real and measured, not
   expected.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round 6 with
the reviewer's reading of the two screenshots, then the closure sequence.
Open findings: 0. Operator questions: 0.

## Reviewer verdict on round 6, and the end of session 1

Written by the planner and reviewer of F288's first session after the worker's C6 above, and
appended to this handback by a delegated worker as the session's last commit. It is the durable
carrier of round 6's verdict (amend0827 rule 1): the first commit of the next round books the
paragraph between the two marker lines below, verbatim, as the last entry of
`.agent/live_review.md`, with one blank line before it.

----- BEGIN GATE ENTRY -----
Gate: F288 R6 — the F288 round 6 entry: the booking of round 5, DECISION F288 D6, and the second half of T003 — the keyboard's parallel list of the live picture's prompt nodes, hidden until it holds focus, and a headless browser's proof of the list, the keys and the drawn synapses. VERDICT PASS. Re-derived over `cb022003`..`b184775e` by the planner and reviewer of F288's first session, whose own readings are every one below. THE RANGE IS 8 COMMITS, at `0247fc9b` 337, `7ccc3cb9` 51, `e57bc7f2` 261, `07de6c6a` 497, `53bdf90e` 30, `b6802cbc` 11, `6441ce67` 395 and `b184775e` 179 insertions by `git show --numstat`, each under the 500-line cap, each single-parent and each ending with the ordered trailer. THE WORKER DECLARED THREE DEVIATIONS, and each stands: the block's C4 landed as C4a, the harness's five files, and C4b, its reading, under constraint 2's split clause; C3b added a vitest case proving a `test_run` node never lists, so that m3 had a test to turn red, as G5 orders; and two comments of the round's own new files were reworded before their commit because they named the very strings the round's contract test forbids in those files. THE TRANSPORT PROOF: the block copy and the two payload copies, read at `0247fc9b`, equal the reviewer's originals byte for byte, and at `7ccc3cb9` the ledger, the decisions and the plan equal the reviewer's simulation tree byte for byte, the open set reading empty. THE CODE, read in the diff: `promptListEntries` answers, in model order, one entry per synapse the visible layout holds, with the prompt id, the node id, `<role> r<round>` and the state words D6 (1) names; `PromptNodeList` renders a `nav` labelled "Prompts in the live graph" of native buttons whose `aria-pressed` follows the selection and whose click selects the prompt item; its style module clips it to one pixel until `:focus-within` and then shows it over the stage's top-left corner, and every one of the ten `var(--remedy-*)` names it uses is defined in `apps/ui/src/styles/tokens.css`; the stage renders it inside the live branch only, directly after the breadcrumbs; and `ForceBrainGraph`'s container keeps `aria-hidden="true"`. THE RENDER: the reviewer ran the committed harness `.agent/authored/f288-r6-render_measure.py` itself at `b184775e` and read all six checks `PASS`, Chrome and the server stopped by pid and the work dir removed, and read the worker's two screenshots: before focus the list is invisible and each task shows its runs and two faint synapses at graph_spec §4's radius of 2; after focus the list stands at the stage's top-left with its second button pressed, and the canvas rings that button's synapse. The four labels read `builder r1` and `reviewer r1` twice, without the task's name, exactly as the simple view's dots are labelled; that mirrors the view the list stands in for and is an observation, not a finding. THE TESTS: the reviewer's own serial run of the round's selection in the primary checkout at `b184775e` read 1837 passed and 5 skipped at real exit code 0, the base 1828 plus the 9 contract nodes the round adds, and the vitest suite there read 75 files and 1459 tests passed, 5 skipped, none failed; all six `integrity check` checks read `pass`. THE RED PROOFS: the worker's committed tool, re-run by the reviewer in a disposable worktree at `b184775e`, turned its route proof and all seven ordered mutations red — m7 being the harness itself, run on a worktree whose list selects the node id, failing C-e and C-f — with every runner's control green before and after, every file restored byte-identical, and the `node_modules` symlink it made removed. The worktree was removed.
----- END GATE ENTRY -----

WHY THE SESSION ENDS HERE. Session 1 ran six delegated rounds, which meets the target of six to
eight: rounds 1, 2, 4, 5 and 6 passed and round 3 failed on one gate, repaired by round 4. T001,
T002 and T003 are built. What remains is the closure sequence alone, which needs a fresh reading of
`docs/roadmap/STATUS_closure_protocol.md` and the evidence recipe, and this session wrote two lines
to `.agent/prose_slips.md` and caused round 3's failure by a path set that missed four readers —
the signal the protocol names for ending a session rather than authoring a closure. Context
remaining at this point: enough to write this, not enough to author a closure comfortably.

THE STATE FOR THE NEXT SESSION. Feature F288, session 2 next, rounds so far 6. Branch
`feature/f288-event-stream-completeness`, pushed, its last reviewed commit `b184775e`, forked from
`main` at `db691093`. Open findings: 0 (R-1075 registered and resolved in this session). Operator
questions open: 0. No pull request is open. Leftover reviewer worktrees under `.remedy-wt/` named
`f288-r1-dry` to `f288-r6-dry` and `f288-r1-sim` to `f288-r6-sim` are the reviewer's own and may be
removed by the next reviewer once it no longer needs them.

NEXT, AFTER THIS VERDICT:

1. Phase 1 rule 1: read `.agent/STOP` from disk.
2. The Open PR Gate: none is expected to be open.
3. The closure sequence of `docs/roadmap/STATUS_closure_protocol.md`, whose first round books round
   6's gate entry above into `.agent/live_review.md` in its first commit, then runs the one full
   suite of amend0917 rule 1, writes the Built State of `docs/roadmap/features/T5_F288.md`, and
   continues through the evidence bundle, the review package, the self-use item and the STATUS
   acceptance with the pull request.
