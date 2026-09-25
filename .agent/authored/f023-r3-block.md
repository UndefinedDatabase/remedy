STEP F023 R3 — THE NAMED PREREQUISITE OF THE L2 RUN DETAIL: a read route serving each round of a task's latest run

GOAL
Book round 2's PASS, record DECISION F023 D3, and land the route the L2 run popover reads:
`GET /api/jobs/<job>/task-runs/<task_id>/rounds`, built by the new
`packages/orchestration/run_rounds_view.py` from the run report the job's task record points at,
keeping only numbers, vocabulary words and timestamps; its client path and decoder
`apps/ui/src/api/taskRunRounds.ts` and the `loadTaskRunRounds` door in `remedyApi.ts`; the
route's line in `_walkable_paths` and the module's line in the import-reachability allowlist;
and the guards `tests/ui_server/test_task_run_rounds.py` and
`tests/ui_contracts/test_task_run_rounds_door.py`, with red proofs.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f023-r3-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f023-r3/`           READ-ONLY. The reviewer's block and scripts.
  `.remedy-wt/f023-r3-sim/`       The reviewer's simulated tree; do not touch it.
  `.remedy-wt/f023-r3-dry/`       The reviewer's authoring tree; do not touch it.
  `.remedy-wt/f023-r3-worker/`    YOURS for logs and scripts; create it if absent. All five are
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
   `feature/f023-semantic-zoom-l0-l3`, and `git log --oneline -1` must read `90669900`. Report
   all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f023-r3/block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f023-r3-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.diff | 62 | 9512 | 5dd08c4d43ec39517d476a99326f8aef368bf5d4db37436f56253175edcd03e3 |
| mutations.py | 175 | 8615 | 37b0a92862189878e06bd4acde44e22f233c857227b4d3c50e08983d26d9d2f9 |
| plan.md | 37 | 1407 | 3e8346ed19d0f65d237b2cd310794860000d2f94bc4e2c6e835ecac28c25fccb |
| product.diff | 93 | 5087 | ecae9d0f944407dd05a533ae437ff40e10af0ca90067b2b176c076f64626c7c7 |
| run_rounds_view.py | 152 | 5977 | 4b76b54f9b431bc9dc8237f3d0eabd7f669ec0c294ac3d7239de9f71f0301dda |
| taskRunRounds.test.ts | 98 | 4427 | 5e835b1d7595f370f420601dafe6d7bf5aaafd09e2bfc15a645e59d67456a359 |
| taskRunRounds.ts | 94 | 3940 | 39897a8ef3360159ed36dee99d71dd71446f5eb5ce75502213bcfbddc31dc5e9 |
| test_task_run_rounds.py | 217 | 9770 | 5e8d5455b6d62336e177cf366e64e3097d59911decdccc8c22e66117586cc9b6 |
| test_task_run_rounds_door.py | 70 | 3470 | ee0341193d00555ba2b8c0a182f4cc4c256c1848b89720928d12ca779f31a432 |
| tests.diff | 12 | 566 | 8fd4321ae04d9c71ea1cc715a33e20abd46ad2bbf331e631db517f30da5ba4b2 |

`plan.md` is a REWRITE of `.agent/plan.md`. Each of the five others is copied whole:
`run_rounds_view.py` is a NEW FILE at `packages/orchestration/run_rounds_view.py`,
`taskRunRounds.ts` a NEW FILE at `apps/ui/src/api/taskRunRounds.ts`, `taskRunRounds.test.ts` a
NEW FILE at `apps/ui/src/api/taskRunRounds.test.ts`, `test_task_run_rounds.py` a NEW FILE at
`tests/ui_server/test_task_run_rounds.py`, and `test_task_run_rounds_door.py` a NEW FILE at
`tests/ui_contracts/test_task_run_rounds_door.py`.
The three diffs go on with `git apply`; the reviewer generated each with `git diff HEAD` from a
tree at `90669900` into which it wrote the edits. `ledger.diff` appends round 2's gate entry to
`.agent/live_review.md` and DECISION F023 D3 to `.agent/decisions.md`. `product.diff` edits
`apps/ui/src/api/remedyApi.ts`, `packages/orchestration/ui_server.py` and
`tests/orchestration/import_reachability_allowlist.txt`, which must land with the module it
lists or the reachability test is red at that commit. `tests.diff` edits
`tests/ui_server/test_command_channel.py`. `mutations.py` is a TOOL for G5: it is run, never
applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C1c, C1d, C1e, C2, C3, C4 and C5, in this order.

C1a — copy this block and the plan payload
  `.agent/authored/f023-r3-block.md` := this block, and `.agent/authored/f023-r3-plan.md` :=
  plan.md. Both by `shutil.copyfile`.
  Subject: `F023 R3 C1a: copy round 3 block and plan payload into .agent/authored/`
  Expected insertions: 291. Report the number you measure and STOP rather than commit if it is
  500 or more.

C1b — copy the three diffs
  `.agent/authored/f023-r3-ledger.diff`, `-product.diff` and `-tests.diff`, each prefixed
  `f023-r3-` like the others.
  Subject: `F023 R3 C1b: copy round 3 ledger, product and test diffs into .agent/authored/`
  Expected insertions: 167.

C1c — copy the mutation tool
  `.agent/authored/f023-r3-mutations.py` := mutations.py.
  Subject: `F023 R3 C1c: copy round 3 mutation tool into .agent/authored/`
  Expected insertions: 175.

C1d — copy the product payloads
  `.agent/authored/f023-r3-run_rounds_view.py` and `.agent/authored/f023-r3-taskRunRounds.ts`.
  Subject: `F023 R3 C1d: copy round 3 product modules into .agent/authored/`
  Expected insertions: 246.

C1e — copy the test payloads
  `.agent/authored/f023-r3-taskRunRounds.test.ts`, `-test_task_run_rounds.py` and
  `-test_task_run_rounds_door.py`, each prefixed `f023-r3-` like the others.
  Subject: `F023 R3 C1e: copy round 3 test payloads into .agent/authored/`
  Expected insertions: 385.

C2 — THE RECORDS, in this order: `git apply` ledger.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F023 R3 C2: book round 2's PASS, record D3, advance the plan`
  Expected by `git show --numstat` (insertions and deletions): 44/0 decisions.md, 2/0 live_review.md, 12/12 plan.md.

C3 — THE PRODUCT: `git apply` product.diff, then copy run_rounds_view.py into
  `packages/orchestration/` and taskRunRounds.ts into `apps/ui/src/api/`, then `git add` both —
  an untracked module fails `integrity check`'s `relevant_untracked`.
  Subject: `F023 R3 C3: serve each round of a task's latest run for the run detail`
  Expected by `git show --numstat`: 24/0 remedyApi.ts, 94/0 taskRunRounds.ts, 152/0 run_rounds_view.py, 21/0 ui_server.py, 1/0 import_reachability_allowlist.txt.

C4 — THE TESTS: `git apply` tests.diff, then copy taskRunRounds.test.ts into `apps/ui/src/api/`,
  test_task_run_rounds.py into `tests/ui_server/` and test_task_run_rounds_door.py into
  `tests/ui_contracts/`, and `git add` all three.
  Subject: `F023 R3 C4: pin the rounds route, its refusals and the client door`
  Expected by `git show --numstat`: 98/0 taskRunRounds.test.ts, 70/0 test_task_run_rounds_door.py, 1/0 test_command_channel.py, 217/0 test_task_run_rounds.py.

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F023 R3 C5: rewrite handoff for round 3`
  Then `git push origin feature/f023-semantic-zoom-l0-l3`. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f023-r3-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, the three paths
   `product.diff` edits, the one path `tests.diff` edits, the five new files the payloads name,
   and `.agent/handoff.md`. Report the list you measure with `git diff --name-only 90669900 HEAD`
   after C5. Do NOT touch `.agent/prose_slips.md`, `.agent/candidates.md`,
   `.agent/operator_questions.md`, `.agent/context.md`, `README.md`, `docs/roadmap/**` or any
   file under `apps/ui/src/components/`.
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
 against the PAYLOADS table. Then compare each `.agent/authored/f023-r3-*` copy byte for byte
 with its source (the block copy against `.remedy-wt/f023-r3/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, which its builder printed from the simulated tree:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 299362 | aade3e06c161b7c4f82ee18bb691e94a4b9181b8d1f6965d22f04921dc9a41b2 |
 | .agent/decisions.md | 2055884 | ad994610221cd48d79435133e0952a14215f06845b44c74bd2e6e773497cef79 |
 | .agent/plan.md | 1407 | 3e8346ed19d0f65d237b2cd310794860000d2f94bc4e2c6e835ecac28c25fccb |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `90669900` and at C2 (the reviewer
 read R-1008 alone at both); the ledger's last line at C2 begins `Gate: F023 R2 — `; and
 `git diff --name-only <C1e> <C2>`, which must name exactly the paths of the table above.

G3 THE PRODUCT AND THE TESTS — the sha256 of each file below, read with `git show` at the commit
 named, equals the reviewer's reading from the simulated tree:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C3 | apps/ui/src/api/remedyApi.ts | 39430 | dbf2466e1af1df138e8c83a5ada3998022c1ec5a74d07b915884dcc51741f2d2 |
 | C3 | packages/orchestration/ui_server.py | 161536 | 5955fab4eb8f444d8dc4950398c0cc15683fba44ae598b5f476b08722e29351a |
 | C3 | tests/orchestration/import_reachability_allowlist.txt | 10128 | dde14ea413e12589ef539d17d5f7d4231d01cfc492c651e8e2f290b8c7019533 |
 | C3 | packages/orchestration/run_rounds_view.py | 5977 | 4b76b54f9b431bc9dc8237f3d0eabd7f669ec0c294ac3d7239de9f71f0301dda |
 | C3 | apps/ui/src/api/taskRunRounds.ts | 3940 | 39897a8ef3360159ed36dee99d71dd71446f5eb5ce75502213bcfbddc31dc5e9 |
 | C4 | tests/ui_server/test_command_channel.py | 95219 | 64a1db61bbb06cd54e0f5fc4a0d5e35735427c08240b1648de7d8771f0d4b0a7 |
 | C4 | apps/ui/src/api/taskRunRounds.test.ts | 4427 | 5e835b1d7595f370f420601dafe6d7bf5aaafd09e2bfc15a645e59d67456a359 |
 | C4 | tests/ui_server/test_task_run_rounds.py | 9770 | 5e8d5455b6d62336e177cf366e64e3097d59911decdccc8c22e66117586cc9b6 |
 | C4 | tests/ui_contracts/test_task_run_rounds_door.py | 3470 | ee0341193d00555ba2b8c0a182f4cc4c256c1848b89720928d12ca779f31a432 |
 Also `git diff --name-only <C2> <C3>` and `<C3> <C4>`, which must name exactly the paths C3 and
 C4 list; and `python3 -m ruff check` at C4 over `packages/orchestration/run_rounds_view.py`,
 `packages/orchestration/ui_server.py`, `tests/ui_server/test_task_run_rounds.py`,
 `tests/ui_server/test_command_channel.py` and `tests/ui_contracts/test_task_run_rounds_door.py`.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_server/test_task_run_rounds.py tests/ui_server/test_command_channel.py tests/ui_server/test_diff_endpoint.py tests/ui_server/test_sse_stream.py tests/ui_server/test_dashboard_contract.py tests/ui_contracts tests/orchestration/test_import_reachability.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/orchestration/test_block_lint.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path, serially, inside its sim tree
 carrying C1a to C4 with this block's copy, and read `1666 passed, 6 skipped` at real exit code 0. FOUR of
 those skips are toolchain nodes a worktree cannot run and the primary checkout can, and each
 must PASS in your run, not skip: the two in `tests/ui_contracts/test_ui_lint.py` (eslint at
 zero warnings), the typescript node in `tests/ui_server/test_dashboard_contract.py`
 (`tsc --noEmit`) and the vitest node in `tests/orchestration/test_test_runner.py`, which runs
 the UI's whole unit suite and so the new test file. Report every `SKIPPED` line the `-rs`
 summary prints. Then `python3 -m apps.cli.main integrity check --json`, which must read all six
 checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f023-r3-mut <C4>`, then
 `python3 -B .remedy-wt/f023-r3-payloads/mutations.py
 /home/decodeux/Repos/remedy/.remedy-wt/f023-r3-mut` and report its whole output. For each
 mutation the tool runs vitest over the WORKTREE's `taskRunRounds.test.ts` from the primary
 `apps/ui` with a scratch config under `.remedy-wt/f023-r3-mutscratch/`, and pytest over the
 worktree's two guards; it asserts each FROM occurs exactly once, restores the bytes, and runs
 an unmutated control first and last. The reviewer read, over the same tool against its sim tree
 (v = vitest failed, g = guard failed, each red at exit 1 wherever its count is not 0):
 control first: vitest 8 passed at exit 0, guard 17 passed at exit 0;
 m1 (an uppercase run id is accepted) v0 g1;
 m2 (any non-empty run id becomes a path segment) v0 g3;
 m3 (the builder's summary prose is served) v0 g5;
 m4 (a finish before the start yields a negative duration) v0 g1;
 m5 (a boolean is counted as a number) v0 g1;
 m6 (an unknown task falls through to the run lookup) v0 g2;
 m7 (a truthy string reads as a parse retry) v0 g1;
 m8 (an unparseable start time is served raw) v0 g1;
 m9 (the server routes the path under another name) v0 g3;
 m10 (the client accepts an envelope of another version) v1 g1;
 m11 (the client keeps rounds of an unavailable envelope) v1 g0;
 m12 (the client reads the builder's tokens from the wrong key) v1 g1;
 m13 (the task id is put in the path unencoded) v1 g0;
 m14 (the door throws on a failed fetch) v1 g1;
 control last: vitest 8 passed at exit 0, guard 17 passed at exit 0;
 every `restored byte-identical` reading True, and the final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`.
 Then `git worktree remove --force .remedy-wt/f023-r3-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 10`, which must show C5, C4, C3, C2, C1e, C1d, C1c, C1b, C1a and
 `90669900` in that order; `git worktree list`, which must show the primary checkout and the
 worktrees constraint 6 names, and nothing else; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and
the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 1 of feature F023, round 3, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 3, then T002's second half — the L2 run popover anchored to its node, reading the rounds
door, with its buttons wired to real endpoints or honestly marked not yet. State the
open-findings count, 1, and the operator-questions count, 3.
