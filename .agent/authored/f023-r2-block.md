STEP F023 R2 — T002 FIRST HALF: the zoom's render effects on the live canvas, the camera per level, Escape and the breadcrumbs

GOAL
Book round 1's PASS, record DECISION F023 D2, and land T002's first half: `zoomView.ts`, the
render effects of a zoom state as plain data (sibling dimming to 25%, the focused task's label
and ring, the branch glow, the camera per level); `useSemanticZoom.ts`, the hook that holds the
state, walks back on Escape and reconciles on every graph change; `ZoomBreadcrumbs.tsx`, the chip
top-left of the stage; `ForceBrainGraph.tsx` painting the effects, sending clicks and wheel
crossings to the machine and moving its camera under a lock; `BrainGraphStage.tsx` wiring them;
their vitest goldens and the guard `tests/ui_contracts/test_semantic_zoom_wiring.py`, with red
proofs.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f023-r2-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f023-r2/`           READ-ONLY. The reviewer's block and scripts.
  `.remedy-wt/f023-r2-sim/`       The reviewer's simulated tree; do not touch it.
  `.remedy-wt/f023-r2-dry/`       The reviewer's authoring tree; do not touch it.
  `.remedy-wt/f023-r2-worker/`    YOURS for logs and scripts; create it if absent. All five are
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
   `feature/f023-semantic-zoom-l0-l3`, and `git log --oneline -1` must read `835930ee`. Report
   all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f023-r2/block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f023-r2-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| ZoomBreadcrumbs.module.css | 53 | 1075 | 0fd44b18466607dfe6e0c62585acc9f9845121109b2249f4bd3eac7dc7578b64 |
| ZoomBreadcrumbs.tsx | 37 | 1357 | 42355a5d577a6ed11ba9381a8c80432575a2b11e8f6ad8c11908cf6c60581f5f |
| canvas.diff | 248 | 12249 | 9e740efdd998d45fa9ffdb05e8829957add657c66b1823031b7b5b5f08dfbeab |
| ledger.diff | 68 | 9636 | c8fb842ddc215bc055f8f8ae6e0042eee0f1c2b74a1a6b6a39bacaec8879be3a |
| mutations.py | 171 | 8519 | 650d79bb9c01d0a49684d82adfe961d70ca95b81287e5a7b673a6d41bce2dc34 |
| plan.md | 37 | 1421 | 3253df702147a2d718f9f43a3414f7eb08f56655b10712ed7f596501488f5bfa |
| test_semantic_zoom_wiring.py | 94 | 4576 | ec8e1a460f1ff0ede4208e0f47df40d1b3f29e29a2abc0e0878001cd8b1eb99d |
| useSemanticZoom.ts | 51 | 2151 | 81546075b3e588fe6bad62b3fd2d33912ffbad63423a8415e58f957cfa6ddd88 |
| zoomView.test.ts | 139 | 6435 | 6b459d60877d76ade30a12294a4708f80082f4d3b618fc7d74d1ff93265a9043 |
| zoomView.ts | 105 | 4953 | 6a847845a4f6d7423d5e45ddac1be9d3758a630e0749c72af01353fb34ab397a |

`plan.md` is a REWRITE of `.agent/plan.md`. `zoomView.ts`, `useSemanticZoom.ts`,
`ZoomBreadcrumbs.tsx`, `ZoomBreadcrumbs.module.css` and `zoomView.test.ts` are NEW FILES under
`apps/ui/src/components/graph/`, and `test_semantic_zoom_wiring.py` is a NEW FILE under
`tests/ui_contracts/`, each copied whole. `ledger.diff` and `canvas.diff` go on with
`git apply`; the reviewer generated both with `git diff HEAD` from a tree at `835930ee` into
which it wrote the edits. `ledger.diff` appends round 1's gate entry to `.agent/live_review.md`
and DECISION F023 D2 to `.agent/decisions.md`. `canvas.diff` edits
`apps/ui/src/components/graph/BrainGraphStage.tsx`, `ForceBrainGraph.tsx` and
`apps/ui/src/types/react-force-graph-2d.d.ts`. `mutations.py` is a TOOL for G5: it is run, never
applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C1c, C1d, C1e, C2, C3, C4 and C5, in this order.

C1a — copy this block and the plan payload
  `.agent/authored/f023-r2-block.md` := this block, and `.agent/authored/f023-r2-plan.md` :=
  plan.md. Both by `shutil.copyfile`.
  Subject: `F023 R2 C1a: copy round 2 block and plan payload into .agent/authored/`
  Expected insertions: 285. Report the number you measure and STOP rather than commit if it is
  500 or more.

C1b — copy the two diffs
  `.agent/authored/f023-r2-ledger.diff` := ledger.diff, `.agent/authored/f023-r2-canvas.diff` :=
  canvas.diff.
  Subject: `F023 R2 C1b: copy round 2 ledger and canvas diffs into .agent/authored/`
  Expected insertions: 316.

C1c — copy the mutation tool
  `.agent/authored/f023-r2-mutations.py` := mutations.py.
  Subject: `F023 R2 C1c: copy round 2 mutation tool into .agent/authored/`
  Expected insertions: 171.

C1d — copy the product payloads
  `.agent/authored/f023-r2-zoomView.ts`, `-useSemanticZoom.ts`, `-ZoomBreadcrumbs.tsx` and
  `-ZoomBreadcrumbs.module.css`, each prefixed `f023-r2-` like the others.
  Subject: `F023 R2 C1d: copy round 2 product modules into .agent/authored/`
  Expected insertions: 246.

C1e — copy the test payloads
  `.agent/authored/f023-r2-zoomView.test.ts` and `.agent/authored/f023-r2-test_semantic_zoom_wiring.py`.
  Subject: `F023 R2 C1e: copy round 2 test payloads into .agent/authored/`
  Expected insertions: 233.

C2 — THE RECORDS, in this order: `git apply` ledger.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F023 R2 C2: book round 1's PASS, record D2, advance the plan`
  Expected by `git show --numstat` (insertions and deletions): 50/0 decisions.md, 2/0 live_review.md, 12/11 plan.md.

C3 — THE PRODUCT: `git apply` canvas.diff, then copy zoomView.ts, useSemanticZoom.ts,
  ZoomBreadcrumbs.tsx and ZoomBreadcrumbs.module.css into `apps/ui/src/components/graph/`, then
  `git add` all four — an untracked module fails `integrity check`'s `relevant_untracked`.
  Subject: `F023 R2 C3: paint the zoom's render effects and move the camera per level`
  Expected by `git show --numstat`: 34/10 BrainGraphStage.tsx, 74/9 ForceBrainGraph.tsx, 53/0 ZoomBreadcrumbs.module.css, 37/0 ZoomBreadcrumbs.tsx, 51/0 useSemanticZoom.ts, 105/0 zoomView.ts, 4/0 react-force-graph-2d.d.ts.

C4 — THE TESTS: copy zoomView.test.ts into `apps/ui/src/components/graph/` and
  test_semantic_zoom_wiring.py into `tests/ui_contracts/`, and `git add` both.
  Subject: `F023 R2 C4: golden the render effects and pin the canvas wiring`
  Expected insertions: 233.

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F023 R2 C5: rewrite handoff for round 2`
  Then `git push origin feature/f023-semantic-zoom-l0-l3`. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f023-r2-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, the three paths
   `canvas.diff` edits, the five new files under `apps/ui/src/components/graph/` that the
   payloads name, `tests/ui_contracts/test_semantic_zoom_wiring.py`, and `.agent/handoff.md`.
   Report the list you measure with `git diff --name-only 835930ee HEAD` after C5. Do NOT touch
   `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md`,
   `.agent/context.md`, `README.md`, `docs/roadmap/**` or `semanticZoom.ts`.
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
 against the PAYLOADS table. Then compare each `.agent/authored/f023-r2-*` copy byte for byte
 with its source (the block copy against `.remedy-wt/f023-r2/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, which its builder printed from the simulated tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 297366 | 2fe0fb99b9eab14e0b49c516014a11babb823ec5de396d1a121128ef842944fa |
 | .agent/decisions.md | 2052300 | f3ab6aed4c096928fe20a2d326351064fa788f476be3a4dfdaa2cb0741d01798 |
 | .agent/plan.md | 1421 | 3253df702147a2d718f9f43a3414f7eb08f56655b10712ed7f596501488f5bfa |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `835930ee` and at C2 (the reviewer
 read R-1008 alone at both); the ledger's last line at C2 begins `Gate: F023 R1 — `; and
 `git diff --name-only <C1e> <C2>`, which must name exactly the paths of the table above.

G3 THE PRODUCT AND THE TESTS — the sha256 of each file below, read with `git show` at the commit
 named, equals the reviewer's reading from the simulated tree:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C3 | apps/ui/src/components/graph/BrainGraphStage.tsx | 4656 | 1860e92754412d3f0199bc6723fcc4dceca7d7d7725cf80e34c0f04f060ec8d6 |
 | C3 | apps/ui/src/components/graph/ForceBrainGraph.tsx | 19453 | d732c9b00dc5fec2c59409ff97cf43d7485ca21fed6daf29a3ca0054368c761f |
 | C3 | apps/ui/src/types/react-force-graph-2d.d.ts | 3029 | 8c7459020e2f3a9c3a517e497b770849798c9df4a639375610b5c487b109670c |
 | C3 | apps/ui/src/components/graph/zoomView.ts | 4953 | 6a847845a4f6d7423d5e45ddac1be9d3758a630e0749c72af01353fb34ab397a |
 | C3 | apps/ui/src/components/graph/useSemanticZoom.ts | 2151 | 81546075b3e588fe6bad62b3fd2d33912ffbad63423a8415e58f957cfa6ddd88 |
 | C3 | apps/ui/src/components/graph/ZoomBreadcrumbs.tsx | 1357 | 42355a5d577a6ed11ba9381a8c80432575a2b11e8f6ad8c11908cf6c60581f5f |
 | C3 | apps/ui/src/components/graph/ZoomBreadcrumbs.module.css | 1075 | 0fd44b18466607dfe6e0c62585acc9f9845121109b2249f4bd3eac7dc7578b64 |
 | C4 | apps/ui/src/components/graph/zoomView.test.ts | 6435 | 6b459d60877d76ade30a12294a4708f80082f4d3b618fc7d74d1ff93265a9043 |
 | C4 | tests/ui_contracts/test_semantic_zoom_wiring.py | 4576 | ec8e1a460f1ff0ede4208e0f47df40d1b3f29e29a2abc0e0878001cd8b1eb99d |
 Also `git diff --name-only <C2> <C3>` and `<C3> <C4>`, which must name exactly the paths C3 and
 C4 list; and `python3 -m ruff check tests/ui_contracts/test_semantic_zoom_wiring.py` at C4.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/orchestration/test_block_lint.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path, serially, inside its sim tree
 carrying C1a to C4 with this block's copy, and read `1458 passed, 10 skipped` at real exit code 0. FOUR of
 those skips are toolchain nodes a worktree cannot run and the primary checkout can, and each
 must PASS in your run, not skip: the two in `tests/ui_contracts/test_ui_lint.py` (eslint at
 zero warnings), the typescript node in `tests/ui_server/test_dashboard_contract.py`
 (`tsc --noEmit`) and the vitest node in `tests/orchestration/test_test_runner.py`, which runs
 the UI's whole unit suite and so the new test file. Report every `SKIPPED` line the `-rs`
 summary prints. Then `python3 -m apps.cli.main integrity check --json`, which must read all six
 checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f023-r2-mut <C4>`, then
 `python3 -B .remedy-wt/f023-r2-payloads/mutations.py
 /home/decodeux/Repos/remedy/.remedy-wt/f023-r2-mut` and report its whole output. For each
 mutation the tool runs vitest over the WORKTREE's `zoomView.test.ts` from the primary `apps/ui`
 with a scratch config under `.remedy-wt/f023-r2-mutscratch/`, and pytest over the worktree's
 guard; it asserts each FROM occurs exactly once, restores the bytes, and runs an unmutated
 control first and last. The reviewer read, over the same tool against its sim tree
 (v = vitest failed, g = guard failed, each red at exit 1 wherever its count is not 0):
 control first: vitest 14 passed at exit 0, guard 8 passed at exit 0;
 m1 (siblings dim to 40%, not 25%) v1 g0;
 m2 (the core dims with the siblings) v3 g0;
 m3 (every active branch glows at L1 too) v1 g0;
 m4 (the ring stays on the task at L2) v1 g0;
 m5 (a click lands L1's camera inside the wheel's dead band) v2 g0;
 m6 (a focus hidden by a filter still dims the graph) v1 g0;
 m7 (Escape in a text field walks the zoom back) v1 g0;
 m8 (the camera move drifts off --remedy-dur-slow) v1 g1;
 m9 (the canvas reads its own camera move as a wheel) v0 g1;
 m10 (the camera move sets no lock) v0 g1;
 m11 (a click no longer reaches the machine) v0 g1;
 m12 (a dimmed task's label is drawn at full strength) v0 g1;
 m13 (the stage checks focus against the view alone) v0 g1;
 m14 (Escape walks back under an open dialog) v0 g1;
 m15 (the focus is no longer reconciled when the graph changes) v0 g1;
 control last: vitest 14 passed at exit 0, guard 8 passed at exit 0;
 every `restored byte-identical` reading True, and the final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`.
 Then `git worktree remove --force .remedy-wt/f023-r2-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 10`, which must show C5, C4, C3, C2, C1e, C1d, C1c, C1b, C1a and
 `835930ee` in that order; `git worktree list`, which must show the primary checkout and the
 worktrees constraint 6 names, and nothing else; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and
the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 1 of feature F023, round 2, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 2, then T002's second half — the L2 run popover anchored to its node, with its buttons
wired to real endpoints or honestly marked not yet. State the open-findings count, 1, and the
operator-questions count, 3.
