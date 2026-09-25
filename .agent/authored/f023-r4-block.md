STEP F023 R4 — T002 SECOND HALF: the L2 run detail, its words, its popover and its buttons

GOAL
Book round 3's PASS, record DECISION F023 D4, and land the L2 run detail: `runDetailModel.ts`,
the words for a run's verdict, round, tokens, duration and retries, each a real value or a plain
sentence saying why it is missing; `RunDetailPopover.tsx` and its stylesheet, reading the rounds
door, with Open diff, Why and a disabled Rerun whose reason is visible; `BrainGraphStage.tsx`
mounting it for the focused run, `RemedyShell.tsx` handing the stage the token and the diff
panel's opener, and `ForceBrainGraph.tsx` no longer opening the task's popover on a run click;
their vitest goldens and the guard `tests/ui_contracts/test_run_detail_wiring.py`, with red
proofs.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f023-r4-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f023-r4/`           READ-ONLY. The reviewer's block and scripts.
  `.remedy-wt/f023-r4-sim/`       The reviewer's simulated tree; do not touch it.
  `.remedy-wt/f023-r4-dry/`       The reviewer's authoring tree; do not touch it.
  `.remedy-wt/f023-r4-worker/`    YOURS for logs and scripts; create it if absent. All five are
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
   `feature/f023-semantic-zoom-l0-l3`, and `git log --oneline -1` must read `12275971`. Report
   all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f023-r4/block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f023-r4-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| RunDetailPopover.module.css | 98 | 2008 | f74ec09058c7982e7ee511ca23a63419f3fe13ea384b9291fd008735f69bcf84 |
| RunDetailPopover.tsx | 89 | 4111 | a5519df21bcbe2660d0ab340fb5ea40d5f1b56bfffb799b79f51ef55d4df424a |
| canvas.diff | 92 | 4934 | f3fc5fdfacdf955ac4e6f9c2dbe7e876ef89aa2a11abfcdd3831b3eb947f7f17 |
| ledger.diff | 66 | 10297 | c349bd0042f9ec35d524b6eefb6f8de51e17eb0159b70ec8da8cfbb91c9289e7 |
| mutations.py | 178 | 9141 | 4bc82dd21deeadcbef4474eca81670a6102cb880cd07a9f4e56c84a5266c6e9f |
| plan.md | 36 | 1332 | cc718e99296a0210193f4de7526ace6695b8c68c7dcc8522e3e0038c134f8da1 |
| runDetailModel.test.ts | 161 | 7826 | 46a97e1e1279681bc3823aa42ca5d739627d58c60d15c4482897dafde7bebe3a |
| runDetailModel.ts | 170 | 8019 | a0f3e15c091ca07bd03fe43e803224154b7c051456fbe093e2ede3c737ad127f |
| test_run_detail_wiring.py | 68 | 3505 | 6c48ca4ba0739e49f712f548fc49e426242476d0a3f342f8221329860f65d34a |

`plan.md` is a REWRITE of `.agent/plan.md`. Each of the five others is copied whole:
`runDetailModel.ts` is a NEW FILE at `apps/ui/src/components/graph/runDetailModel.ts`,
`RunDetailPopover.tsx` a NEW FILE at `apps/ui/src/components/graph/RunDetailPopover.tsx`,
`RunDetailPopover.module.css` a NEW FILE at
`apps/ui/src/components/graph/RunDetailPopover.module.css`, `runDetailModel.test.ts` a NEW FILE at
`apps/ui/src/components/graph/runDetailModel.test.ts`, and `test_run_detail_wiring.py` a NEW FILE
at `tests/ui_contracts/test_run_detail_wiring.py`. `ledger.diff` and `canvas.diff` go on with
`git apply`; the reviewer generated both with `git diff HEAD` from a tree at `12275971` into
which it wrote the edits. `ledger.diff` appends round 3's gate entry to `.agent/live_review.md`
and DECISION F023 D4 to `.agent/decisions.md`. `canvas.diff` edits
`apps/ui/src/components/graph/BrainGraphStage.tsx`, `ForceBrainGraph.tsx` and
`apps/ui/src/components/shell/RemedyShell.tsx`. `mutations.py` is a TOOL for G5: it is run, never
applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C1c, C1d, C1e, C2, C3, C4 and C5, in this order.

C1a — copy this block and the plan payload
  `.agent/authored/f023-r4-block.md` := this block, and `.agent/authored/f023-r4-plan.md` :=
  plan.md. Both by `shutil.copyfile`.
  Subject: `F023 R4 C1a: copy round 4 block and plan payload into .agent/authored/`
  Expected insertions: 285. Report the number you measure and STOP rather than commit if it is
  500 or more.

C1b — copy the two diffs
  `.agent/authored/f023-r4-ledger.diff` := ledger.diff, `.agent/authored/f023-r4-canvas.diff` :=
  canvas.diff.
  Subject: `F023 R4 C1b: copy round 4 ledger and canvas diffs into .agent/authored/`
  Expected insertions: 158.

C1c — copy the mutation tool
  `.agent/authored/f023-r4-mutations.py` := mutations.py.
  Subject: `F023 R4 C1c: copy round 4 mutation tool into .agent/authored/`
  Expected insertions: 178.

C1d — copy the product payloads
  `.agent/authored/f023-r4-runDetailModel.ts`, `-RunDetailPopover.tsx` and
  `-RunDetailPopover.module.css`, each prefixed `f023-r4-` like the others.
  Subject: `F023 R4 C1d: copy round 4 product modules into .agent/authored/`
  Expected insertions: 357.

C1e — copy the test payloads
  `.agent/authored/f023-r4-runDetailModel.test.ts` and `.agent/authored/f023-r4-test_run_detail_wiring.py`.
  Subject: `F023 R4 C1e: copy round 4 test payloads into .agent/authored/`
  Expected insertions: 229.

C2 — THE RECORDS, in this order: `git apply` ledger.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F023 R4 C2: book round 3's PASS, record D4, advance the plan`
  Expected by `git show --numstat` (insertions and deletions): 48/0 decisions.md, 2/0 live_review.md, 13/14 plan.md.

C3 — THE PRODUCT: `git apply` canvas.diff, then copy runDetailModel.ts, RunDetailPopover.tsx and
  RunDetailPopover.module.css into `apps/ui/src/components/graph/`, then `git add` all three — an
  untracked module fails `integrity check`'s `relevant_untracked`.
  Subject: `F023 R4 C3: show the L2 run detail beside the run the camera centred`
  Expected by `git show --numstat`: 20/0 BrainGraphStage.tsx, 3/0 ForceBrainGraph.tsx, 98/0 RunDetailPopover.module.css, 89/0 RunDetailPopover.tsx, 170/0 runDetailModel.ts, 1/1 RemedyShell.tsx.

C4 — THE TESTS: copy runDetailModel.test.ts into `apps/ui/src/components/graph/` and
  test_run_detail_wiring.py into `tests/ui_contracts/`, and `git add` both.
  Subject: `F023 R4 C4: golden the run detail's words and pin its wiring`
  Expected by `git show --numstat`: 161/0 runDetailModel.test.ts, 68/0 test_run_detail_wiring.py.

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F023 R4 C5: rewrite handoff for round 4`
  Then `git push origin feature/f023-semantic-zoom-l0-l3`. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f023-r4-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, the three paths
   `canvas.diff` edits, the five new files the payloads name, and `.agent/handoff.md`. Report the
   list you measure with `git diff --name-only 12275971 HEAD` after C5. Do NOT touch
   `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md`,
   `.agent/context.md`, `README.md`, `docs/roadmap/**`, `apps/ui/src/api/**` or
   `packages/**`.
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
 against the PAYLOADS table. Then compare each `.agent/authored/f023-r4-*` copy byte for byte
 with its source (the block copy against `.remedy-wt/f023-r4/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, which its builder printed from the simulated tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 301099 | 63485c3552ff84f3c79668d68aae45cdbdc1cd748011d92e26a69cd37c5c46d3 |
 | .agent/decisions.md | 2059971 | 6801f73ecbee7fbf09d10b12597f0f8a2f4ad9dbef7a21a282cd8f60e8c90d2c |
 | .agent/plan.md | 1332 | cc718e99296a0210193f4de7526ace6695b8c68c7dcc8522e3e0038c134f8da1 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `12275971` and at C2 (the reviewer
 read R-1008 alone at both); the ledger's last line at C2 begins `Gate: F023 R3 — `; and
 `git diff --name-only <C1e> <C2>`, which must name exactly the paths of the table above.

G3 THE PRODUCT AND THE TESTS — the sha256 of each file below, read with `git show` at the commit
 named, equals the reviewer's reading from the simulated tree:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C3 | apps/ui/src/components/graph/BrainGraphStage.tsx | 5503 | ec8bb7d68433b6c295b395ffe720c2eed8da0a346340deda41d45fe9acb4d2cc |
 | C3 | apps/ui/src/components/graph/ForceBrainGraph.tsx | 19621 | 005ac2ae2b45cb4102e7d1809a1db7dbeb15f733a2867dee5068a7856a2add11 |
 | C3 | apps/ui/src/components/shell/RemedyShell.tsx | 13170 | b1474134edb6ac902d534277e5f95fbc8e63927e46eee0b09348759374a4c685 |
 | C3 | apps/ui/src/components/graph/runDetailModel.ts | 8019 | a0f3e15c091ca07bd03fe43e803224154b7c051456fbe093e2ede3c737ad127f |
 | C3 | apps/ui/src/components/graph/RunDetailPopover.tsx | 4111 | a5519df21bcbe2660d0ab340fb5ea40d5f1b56bfffb799b79f51ef55d4df424a |
 | C3 | apps/ui/src/components/graph/RunDetailPopover.module.css | 2008 | f74ec09058c7982e7ee511ca23a63419f3fe13ea384b9291fd008735f69bcf84 |
 | C4 | apps/ui/src/components/graph/runDetailModel.test.ts | 7826 | 46a97e1e1279681bc3823aa42ca5d739627d58c60d15c4482897dafde7bebe3a |
 | C4 | tests/ui_contracts/test_run_detail_wiring.py | 3505 | 6c48ca4ba0739e49f712f548fc49e426242476d0a3f342f8221329860f65d34a |
 Also `git diff --name-only <C2> <C3>` and `<C3> <C4>`, which must name exactly the paths C3 and
 C4 list; and `python3 -m ruff check tests/ui_contracts/test_run_detail_wiring.py` at C4.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/orchestration/test_block_lint.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path, serially, inside its sim tree
 carrying C1a to C4 with this block's copy, and read `1466 passed, 10 skipped` at real exit code 0. FOUR of
 those skips are toolchain nodes a worktree cannot run and the primary checkout can, and each
 must PASS in your run, not skip: the two in `tests/ui_contracts/test_ui_lint.py` (eslint at
 zero warnings), the typescript node in `tests/ui_server/test_dashboard_contract.py`
 (`tsc --noEmit`) and the vitest node in `tests/orchestration/test_test_runner.py`, which runs
 the UI's whole unit suite and so the new test file. Report every `SKIPPED` line the `-rs`
 summary prints. Then `python3 -m apps.cli.main integrity check --json`, which must read all six
 checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f023-r4-mut <C4>`, then
 `python3 -B .remedy-wt/f023-r4-payloads/mutations.py
 /home/decodeux/Repos/remedy/.remedy-wt/f023-r4-mut` and report its whole output. For each
 mutation the tool runs vitest over the WORKTREE's `runDetailModel.test.ts` from the primary
 `apps/ui`
 with a scratch config under `.remedy-wt/f023-r4-mutscratch/`, and pytest over the worktree's
 guard; it asserts each FROM occurs exactly once, restores the bytes, and runs an unmutated
 control first and last. The reviewer read, over the same tool against its sim tree
 (v = vitest failed, g = guard failed, each red at exit 1 wherever its count is not 0):
 control first: vitest 13 passed at exit 0, guard 5 passed at exit 0;
 m1 (a round the ledger logged without a review is not counted) v3 g0;
 m2 (an earlier run is taken for the latest) v2 g0;
 m3 (the reviewer's tokens are filled from the builder's) v2 g0;
 m4 (a running run is described from the report) v1 g0;
 m5 (needs repair reads as failed) v1 g0;
 m6 (a test run claims a timing) v1 g0;
 m7 (Why opens a reviewer prompt of another round) v1 g0;
 m8 (a long duration is written in seconds only) v2 g0;
 m9 (a task with no run reads as an unreadable report) v1 g0;
 m10 (the detail shows a report read for another task) v0 g1;
 m11 (Rerun is enabled) v0 g1;
 m12 (the detail becomes a dialog Escape skips) v0 g1;
 m13 (the stage looks the run up in the filtered view) v0 g1;
 m14 (a run click opens its task's popover too) v0 g1;
 m15 (the shell hands the stage no token) v0 g1;
 control last: vitest 13 passed at exit 0, guard 5 passed at exit 0;
 every `restored byte-identical` reading True, and the final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`.
 Then `git worktree remove --force .remedy-wt/f023-r4-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 10`, which must show C5, C4, C3, C2, C1e, C1d, C1c, C1b, C1a and
 `12275971` in that order; `git worktree list`, which must show the primary checkout and the
 worktrees constraint 6 names, and nothing else; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and
the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 1 of feature F023, round 4, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 4, then T003 — the L3 evidence panel with its lazy tabs, Open diff and Why moved onto its
tabs, and the deep links. State the open-findings count, 1, and the operator-questions count, 3.
