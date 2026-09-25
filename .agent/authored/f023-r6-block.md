STEP F023 R6 — T003 SECOND PART: deep links that restore the zoom, cluster expansion at the focused task, and a camera that waits for the canvas

GOAL
Book round 5's PASS, record DECISION F023 D6, and land: `zoomDeepLink.ts` and
`useZoomDeepLink.ts`, which read `?focus=&level=&tab=` once, replay it through the machine as a
click and a tab when the graph holds its node, and then keep the URL in step with
`history.replaceState`; `clusterExpansion.ts`, which gives the focused task's '+N' chip back its
runs, through an optional second argument of `buildBrainLayout`; `BrainGraphStage.tsx` checking
focus against the unexpanded layout and rendering the expanded one; `ForceBrainGraph.tsx`'s camera
waiting for the canvas and its settled fit keeping the current level's camera; the vitest goldens,
the guard `tests/ui_contracts/test_zoom_deep_link_wiring.py` and the updated
`test_semantic_zoom_wiring.py`, with red proofs.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f023-r6-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f023-r6/`           READ-ONLY. The reviewer's block and scripts.
  `.remedy-wt/f023-r6-sim/`       The reviewer's simulated tree; do not touch it.
  `.remedy-wt/f023-r6-dry/`       The reviewer's authoring tree; do not touch it.
  `.remedy-wt/f023-r6-worker/`    YOURS for logs and scripts; create it if absent. All five are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, command substitution, `cd <dir> && git ...`,
and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit
codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`. Use `python3 - <<'PY'` for counting, hashing and
copying (`shutil.copyfile`). A heredoc containing a dollar-brace is refused: write such a
script to a file under your own directory and run the file. Never run npm or npx.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f023-semantic-zoom-l0-l3`, and `git log --oneline -1` must read `950c4f14`. Report
   all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f023-r6/block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f023-r6-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| clusterExpansion.test.ts | 56 | 2773 | 6938bd3dd044a5c2a9a13be7c52b704fcecac5ab7e1ab665034ba55e2041607f |
| clusterExpansion.ts | 28 | 1717 | 241edd65870e280312a42db7f45221fa256c959628521b5f17a5e53cb5b7bfc2 |
| ledger.diff | 63 | 10239 | 2f5fdc07812d357f8d6bac5cdd54f37343d6a1d9c2e785f1077618cdea624b23 |
| mutations.py | 174 | 8418 | db30945c2cbe6d29a842c1c0de61679e196f2f4c368e2920c71a0622dc2678ff |
| plan.md | 33 | 1240 | 56f2e1f1c6b9520d0390edb8bec5304de2acd5b214eb82e68043cc74f906f3dc |
| product.diff | 151 | 8511 | 3d19ab6efe54ebed6a75687425a789a0bcd8e67c6d0bfcb6c661a712904d4fe3 |
| test_zoom_deep_link_wiring.py | 70 | 3623 | 7f6df0e24c2333758e1479450f6baaa0168da96837f06cb724ba1b1424969c30 |
| useZoomDeepLink.ts | 33 | 1560 | 29f5cc94dca1153be7ac41bbe02810c16028ddf71a4707fa743293f8486400f9 |
| zoomDeepLink.test.ts | 69 | 3210 | 87bbc5555b4225e91dd44ee72ccf55f55ad7cd8bf01a9f00aec32e143d8219b3 |
| zoomDeepLink.ts | 53 | 2557 | 41fe0ef0112780bdc13dd1b52b9371f01fe9e335e92795998144fc456b4d8326 |

`plan.md` is a REWRITE of `.agent/plan.md`. Each of the six others is copied whole:
`clusterExpansion.ts` is a NEW FILE at `apps/ui/src/components/graph/clusterExpansion.ts`,
`zoomDeepLink.ts` a NEW FILE at `apps/ui/src/components/graph/zoomDeepLink.ts`,
`useZoomDeepLink.ts` a NEW FILE at `apps/ui/src/components/graph/useZoomDeepLink.ts`,
`clusterExpansion.test.ts` a NEW FILE at `apps/ui/src/components/graph/clusterExpansion.test.ts`,
`zoomDeepLink.test.ts` a NEW FILE at `apps/ui/src/components/graph/zoomDeepLink.test.ts`, and
`test_zoom_deep_link_wiring.py` a NEW FILE at `tests/ui_contracts/test_zoom_deep_link_wiring.py`.
`ledger.diff` and `product.diff` go on with `git apply`; the reviewer generated both with
`git diff HEAD` from a tree at `950c4f14` into which it wrote the edits. `ledger.diff` appends
round 5's gate entry to `.agent/live_review.md` and DECISION F023 D6 to `.agent/decisions.md`.
`product.diff` edits `apps/ui/src/components/graph/BrainGraphStage.tsx`, `ForceBrainGraph.tsx`,
`buildForceBrainModel.ts` and `tests/ui_contracts/test_semantic_zoom_wiring.py`, whose update
must land with the product change it follows or that commit is red. `mutations.py` is a TOOL for
G5: it is run, never applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C1c, C1d, C1e, C2, C3, C4 and C5, in this order.

C1a — copy this block and the plan payload
  `.agent/authored/f023-r6-block.md` := this block, and `.agent/authored/f023-r6-plan.md` :=
  plan.md. Both by `shutil.copyfile`.
  Subject: `F023 R6 C1a: copy round 6 block and plan payload into .agent/authored/`
  Expected insertions: 290. Report the number you measure and STOP rather than commit if it is
  500 or more.

C1b — copy the two diffs
  `.agent/authored/f023-r6-ledger.diff` := ledger.diff, `.agent/authored/f023-r6-product.diff` :=
  product.diff.
  Subject: `F023 R6 C1b: copy round 6 ledger and product diffs into .agent/authored/`
  Expected insertions: 214.

C1c — copy the mutation tool
  `.agent/authored/f023-r6-mutations.py` := mutations.py.
  Subject: `F023 R6 C1c: copy round 6 mutation tool into .agent/authored/`
  Expected insertions: 174.

C1d — copy the product payloads
  `.agent/authored/f023-r6-clusterExpansion.ts`, `-zoomDeepLink.ts` and `-useZoomDeepLink.ts`,
  each prefixed `f023-r6-` like the others.
  Subject: `F023 R6 C1d: copy round 6 product modules into .agent/authored/`
  Expected insertions: 114.

C1e — copy the test payloads
  `.agent/authored/f023-r6-clusterExpansion.test.ts`, `-zoomDeepLink.test.ts` and
  `-test_zoom_deep_link_wiring.py`, each prefixed `f023-r6-` like the others.
  Subject: `F023 R6 C1e: copy round 6 test payloads into .agent/authored/`
  Expected insertions: 195.

C2 — THE RECORDS, in this order: `git apply` ledger.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F023 R6 C2: book round 5's PASS, record D6, advance the plan`
  Expected by `git show --numstat` (insertions and deletions): 45/0 decisions.md, 2/0 live_review.md, 11/13 plan.md.

C3 — THE PRODUCT: `git apply` product.diff, then copy clusterExpansion.ts, zoomDeepLink.ts and
  useZoomDeepLink.ts into `apps/ui/src/components/graph/`, then `git add` all three — an
  untracked module fails `integrity check`'s `relevant_untracked`.
  Subject: `F023 R6 C3: restore the zoom from a deep link and expand the focused task's cluster`
  Expected by `git show --numstat`: 19/6 BrainGraphStage.tsx, 16/6 ForceBrainGraph.tsx, 8/3 buildForceBrainModel.ts, 28/0 clusterExpansion.ts, 33/0 useZoomDeepLink.ts, 53/0 zoomDeepLink.ts, 3/1 test_semantic_zoom_wiring.py.

C4 — THE TESTS: copy clusterExpansion.test.ts and zoomDeepLink.test.ts into
  `apps/ui/src/components/graph/` and test_zoom_deep_link_wiring.py into `tests/ui_contracts/`,
  and `git add` all three.
  Subject: `F023 R6 C4: golden the deep link and the expansion, and pin their wiring`
  Expected by `git show --numstat`: 56/0 clusterExpansion.test.ts, 69/0 zoomDeepLink.test.ts, 70/0 test_zoom_deep_link_wiring.py.

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F023 R6 C5: rewrite handoff for round 6`
  Then `git push origin feature/f023-semantic-zoom-l0-l3`. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f023-r6-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, the four paths
   `product.diff` edits, the six new files the payloads name, and `.agent/handoff.md`. Report the
   list you measure with `git diff --name-only 950c4f14 HEAD` after C5. Do NOT touch
   `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md`,
   `.agent/context.md`, `README.md`, `docs/**`, `apps/ui/src/api/**` or `packages/**`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch
   deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees and their branches, every reviewer worktree already
   listed at your step 4, and every existing stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that step's last action, and `git worktree list` is reported
   afterwards.
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F023's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f023-r6-*` copy byte for byte
 with its source (the block copy against `.remedy-wt/f023-r6/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, which its builder printed from the simulated tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 305105 | c7ed8995c1699767674f40a3bfe44a045d62a3535a660b404303ade3d3703dac |
 | .agent/decisions.md | 2067796 | a5cc5c7c79d05d15a84f74a7a3ba4561120bb2e11afb136e2d5ed9880f7d2525 |
 | .agent/plan.md | 1240 | 56f2e1f1c6b9520d0390edb8bec5304de2acd5b214eb82e68043cc74f906f3dc |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `950c4f14` and at C2 (the reviewer
 read R-1008 alone at both); the ledger's last line at C2 begins `Gate: F023 R5 — `; and
 `git diff --name-only <C1e> <C2>`, which must name exactly the paths of the table above.

G3 THE PRODUCT AND THE TESTS — the sha256 of each file below, read with `git show` at the commit
 named, equals the reviewer's reading from the simulated tree:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C3 | apps/ui/src/components/graph/BrainGraphStage.tsx | 6753 | 720907896e30e90fdfdc46a0a7506ec5f4f9ef630c4da42ec4c08d4f063d7dce |
 | C3 | apps/ui/src/components/graph/ForceBrainGraph.tsx | 20268 | b32deb83f40002eb78ff16a101f0ae38c5703fef4c7fb7d83b4e6dccdc032182 |
 | C3 | apps/ui/src/components/graph/buildForceBrainModel.ts | 8798 | 831d04050863db4e16c000fd787cce526310b740293858c687c91cd8e8526d71 |
 | C3 | tests/ui_contracts/test_semantic_zoom_wiring.py | 4720 | 611ecaa1131f243b67a4ca0b07a17d31ba4d5d379b8bd8f84a46dada057defd1 |
 | C3 | apps/ui/src/components/graph/clusterExpansion.ts | 1717 | 241edd65870e280312a42db7f45221fa256c959628521b5f17a5e53cb5b7bfc2 |
 | C3 | apps/ui/src/components/graph/zoomDeepLink.ts | 2557 | 41fe0ef0112780bdc13dd1b52b9371f01fe9e335e92795998144fc456b4d8326 |
 | C3 | apps/ui/src/components/graph/useZoomDeepLink.ts | 1560 | 29f5cc94dca1153be7ac41bbe02810c16028ddf71a4707fa743293f8486400f9 |
 | C4 | apps/ui/src/components/graph/clusterExpansion.test.ts | 2773 | 6938bd3dd044a5c2a9a13be7c52b704fcecac5ab7e1ab665034ba55e2041607f |
 | C4 | apps/ui/src/components/graph/zoomDeepLink.test.ts | 3210 | 87bbc5555b4225e91dd44ee72ccf55f55ad7cd8bf01a9f00aec32e143d8219b3 |
 | C4 | tests/ui_contracts/test_zoom_deep_link_wiring.py | 3623 | 7f6df0e24c2333758e1479450f6baaa0168da96837f06cb724ba1b1424969c30 |
 Also `git diff --name-only <C2> <C3>` and `<C3> <C4>`, which must name exactly the paths C3 and
 C4 list; and `python3 -m ruff check tests/ui_contracts/test_zoom_deep_link_wiring.py
 tests/ui_contracts/test_semantic_zoom_wiring.py` at C4.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/orchestration/test_block_lint.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path, serially, inside its sim tree
 carrying C1a to C4 with this block's copy, and read `1478 passed, 10 skipped` at real exit code 0. FOUR of
 those skips are toolchain nodes a worktree cannot run and the primary checkout can, and each
 must PASS in your run, not skip: the two in `tests/ui_contracts/test_ui_lint.py` (eslint at
 zero warnings), the typescript node in `tests/ui_server/test_dashboard_contract.py`
 (`tsc --noEmit`) and the vitest node in `tests/orchestration/test_test_runner.py`, which runs
 the UI's whole unit suite and so the new test file. Report every `SKIPPED` line the `-rs`
 summary prints. Then `python3 -m apps.cli.main integrity check --json`, which must read all six
 checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f023-r6-mut <C4>`, then
 `python3 -B .remedy-wt/f023-r6-payloads/mutations.py
 /home/decodeux/Repos/remedy/.remedy-wt/f023-r6-mut` and report its whole output. For each
 mutation the tool runs vitest over the WORKTREE's `clusterExpansion.test.ts` and
 `zoomDeepLink.test.ts` from the primary `apps/ui`
 with a scratch config under `.remedy-wt/f023-r6-mutscratch/`, and pytest over the worktree's
 two guards; it asserts each FROM occurs exactly once, restores the bytes, and runs an unmutated
 control first and last. The reviewer read, over the same tool against its sim tree
 (v = vitest failed, g = guard failed, each red at exit 1 wherever its count is not 0):
 control first: vitest 25 passed at exit 0, guard 13 passed at exit 0;
 m1 (the chip's link survives its expansion) v1 g0;
 m2 (runs already shown are added a second time) v3 g0;
 m3 (a task with no chip gets a new object) v1 g0;
 m4 (the layout never expands) v1 g0;
 m5 (a link below L3 reads a tab) v3 g0;
 m6 (an L3 link without a tab opens none) v2 g0;
 m7 (the URL records every level as 1) v3 g0;
 m8 (an L3 link replays no tab) v2 g0;
 m9 (every step adds a history entry) v0 g1;
 m10 (a link replays before its node exists) v0 g1;
 m11 (a reader moving first does not cancel the link) v0 g1;
 m12 (the stage expands the run's level instead of the task's) v0 g1;
 m13 (the stage no longer restores the link) v0 g1;
 m14 (the camera does not wait for the canvas) v0 g1;
 m15 (the settled fit forces the organism's camera) v0 g1;
 control last: vitest 25 passed at exit 0, guard 13 passed at exit 0;
 every `restored byte-identical` reading True, and the final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`.
 Then `git worktree remove --force .remedy-wt/f023-r6-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 10`, which must show C5, C4, C3, C2, C1e, C1d, C1c, C1b, C1a and
 `950c4f14` in that order; `git worktree list`, which must show the primary checkout and the
 worktrees constraint 6 names, and nothing else; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and
the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 1 of feature F023, round 6, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 6, then T003's last part — the 500-node performance fixture driven through every zoom level
with its numbers recorded, and the live end-to-end. State the open-findings count, 1, and the
operator-questions count, 3.
