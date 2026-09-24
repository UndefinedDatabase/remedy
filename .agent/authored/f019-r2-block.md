STEP F019 R2 — BOOK ROUND 1 AND LAND T002's PURE HALF: the layout of the reducer's model, the birth schedule and its tokens

GOAL
Book round 1's PASS, record DECISION F019 D2, and land the pure half of T002:
`buildBrainLayout` in `apps/ui/src/components/graph/buildForceBrainModel.ts` with its shapes in
`forceBrainTypes.ts`, the birth schedule in the new `brainMotion.ts`, the two birth-motion
tokens in `apps/ui/src/styles/tokens.css` and their guard
`tests/ui_contracts/test_brain_motion_tokens.py`, with vitest tests and red proofs.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f019-r2-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f019-r2/`           READ-ONLY. The reviewer's block, texts and builder.
  `.remedy-wt/f019-r2-sim/`, `.remedy-wt/f019-r2-proto/`  The reviewer's trees; do not touch.
  `.remedy-wt/f019-r2-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, `cd <dir> && git ...`, and multi-operation
one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe pytest.
Use `git -C <path>` rather than `cd`. Use `python3 - <<'PY'` for counting, hashing and
copying (`shutil.copyfile`). A heredoc containing a dollar-brace is refused: write such a
script to a file under your own directory and run the file. Never run npm or npx.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f019-live-node-materialization`, and `git log --oneline -1` must read `b6cc2690`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f019-r2/block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.

PAYLOADS — under `.remedy-wt/f019-r2-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 64 | 9957 | 54c531862bf89959ec01655f127d3d6ce748779b8ffcceb0e93ce91c4fad1d1a |
| plan.md | 36 | 1434 | 27b6456594fcfd7fc82af88d34c30f6da8c631ed1e85fd767910719d7b37d165 |
| product.diff | 325 | 14833 | 84ddd740553e117a298e7a3cc8a57399d0176aa91873e6fed5829c4bf15a8327 |
| tests.diff | 367 | 18134 | 4155efec6af89ab73ffb372b402c688d2f8e07d85d53a6afcb868ae4dfdb7db0 |
| mutations.py | 346 | 13825 | 5076fbef3eefdf16820ccc642a3d6c67c7346c21337826277b1ad2d36eef8c2e |

`plan.md` is a REWRITE of `.agent/plan.md`. The three `.diff` files go on with `git apply`; the
reviewer generated each with `git diff` from a tree at `b6cc2690` into which its builder copied
the reviewed prototype. `records.diff` appends the `Gate: F019 R1 — ` entry to
`.agent/live_review.md` and DECISION F019 D2 to `.agent/decisions.md`. `product.diff` edits
`forceBrainTypes.ts`, `buildForceBrainModel.ts` and `apps/ui/src/styles/tokens.css` and creates
`brainMotion.ts`. `tests.diff` edits `buildForceBrainModel.test.ts` and creates
`brainMotion.test.ts` and `tests/ui_contracts/test_brain_motion_tokens.py`. `mutations.py` is a
TOOL for G5: it is run, never applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C1c, C1d, C2, C3, C4 and C5, in this order.

C1a — `.agent/authored/f019-r2-block.md` := this block and `.agent/authored/f019-r2-plan.md` :=
  plan.md, by `shutil.copyfile`.
  Subject: `F019 R2 C1a: copy round 2 block and plan into .agent/authored/`
  Its insertions are this block's line count plus 36; STOP rather than commit if 500 or more.
C1b — `.agent/authored/f019-r2-records.diff` and `.agent/authored/f019-r2-product.diff`.
  Subject: `F019 R2 C1b: copy round 2 records and product diffs into .agent/authored/`
  Expected insertions: 389.
C1c — `.agent/authored/f019-r2-tests.diff`.
  Subject: `F019 R2 C1c: copy round 2 tests diff into .agent/authored/`
  Expected insertions: 367.
C1d — `.agent/authored/f019-r2-mutations.py`.
  Subject: `F019 R2 C1d: copy round 2 mutation tool into .agent/authored/`
  Expected insertions: 346.
C2 — THE BOOKING: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F019 R2 C2: book round 1's PASS, record DECISION F019 D2`
  Expected insertions by `git show --numstat`: 46 decisions.md, 2 live_review.md, 9 plan.md.
C3 — THE PRODUCT: `git apply` product.diff, then `git add` the new `brainMotion.ts`.
  Subject: `F019 R2 C3: lay out the reducer's model and schedule its births`
  Expected insertions: 60 brainMotion.ts, 171 buildForceBrainModel.ts, 46 forceBrainTypes.ts,
  5 tokens.css.
C4 — THE TESTS: `git apply` tests.diff, then `git add` the two new test files.
  Subject: `F019 R2 C4: pin the layout, the birth schedule and the motion tokens`
  Expected insertions: 83 brainMotion.test.ts, 195 buildForceBrainModel.test.ts, 62
  test_brain_motion_tokens.py.
C5 — THE HANDBACK: `.agent/handoff.md`, rewritten, its own commit, per
  `docs/agents/handback_template.md`. Subject: `F019 R2 C5: rewrite handoff for round 2`. Then
  `git push origin feature/f019-live-node-materialization` and report its real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading.
3. The round's whole tracked path set is: the `.agent/authored/f019-r2-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, the seven files the two
   product and test diffs name, and `.agent/handoff.md`. Report `git diff --name-only b6cc2690
   HEAD` after C5.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr` command of any kind, no checkout of `main`, no branch
   deletion, no force-push, no `git stash`.
6. Leave every existing worktree, branch and stash alone. The worktree G5 adds goes under
   `.remedy-wt/`, is removed as that step's last action, and `git worktree list` is reported.
7. DO NOT run the full suite (amend0917 rule 1).

DONE-WHEN — every gate executed, every reading reported with its real exit code. "Green" as a
word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — each payload's line count, byte count and sha256 against the PAYLOADS table;
 then each `.agent/authored/f019-r2-*` copy byte for byte against its source (the block copy
 against `.remedy-wt/f019-r2/block.md`), read back with `git show <commit>:<path>`.

G2 THE BOOKING — at C2, read with `git show <C2>:<path>`: `.agent/live_review.md` 309572 bytes
 sha256 `cf732f8ecb9c05e5ba1fd5a0af8cad22f658e3de198944c2db410058d0cd3553`;
 `.agent/decisions.md` 2000583 bytes sha256
 `c7749033d278e777e12c9dfc5e6dcf6b5a5b463aff3832d8fe290f619c8513e6`; `.agent/plan.md` equal to
 plan.md. The count of lines C2 adds to the ledger beginning `Gate: F019 R1 — `, which must be
 1, and `open_finding_ids` of `scripts/rotate_live_review.py` over the ledger's text at
 `b6cc2690` and at C2, which the reviewer read as R-0499, R-0950, R-1008 and R-1046 at both.

G3 THE PRODUCT AND TESTS — at C4, read with `git show <C4>:<path>`, each equals the reviewer's
 simulated reading:
 | path | bytes | sha256 |
 |---|---|---|
 | apps/ui/src/components/graph/forceBrainTypes.ts | 2571 | 04f9f542e627dc92221a9b381feb740219b81b203d22605a3b613c11401be465 |
 | apps/ui/src/components/graph/buildForceBrainModel.ts | 13454 | e5d2e6c3425f782d8053e96c61cadfd1ff293019b3e37ad3499f63759cdf1dd4 |
 | apps/ui/src/components/graph/brainMotion.ts | 2766 | 28903dd8fc3ddd2fa443c47286352698a75c6a20a9cd7e13b676a14902dffc20 |
 | apps/ui/src/styles/tokens.css | 3911 | 416cc066450704c3487dccbf25332534a322feb2230d5be71d7b64f7e2153f34 |
 | apps/ui/src/components/graph/buildForceBrainModel.test.ts | 11980 | 52806a61551de42b88cae9abe18295e0159c2f9825b289389544a03bde8694fe |
 | apps/ui/src/components/graph/brainMotion.test.ts | 3895 | 3b317e9ad6ddde5b1afab166167fae53a6a6abe5100c996ba7f6df78704332c6 |
 | tests/ui_contracts/test_brain_motion_tokens.py | 2770 | 7710e34bbca6d151fbca2f4319c3ec1dcc7d24709c82f89cbb7e64e0b3710494 |

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path inside its sim tree and read
 `1351 passed, 10 skipped` at exit 0. The two eslint nodes of `tests/ui_contracts/test_ui_lint.py`,
 the tsc node of `tests/ui_server/test_dashboard_contract.py` and the vitest node of
 `tests/orchestration/test_test_runner.py` skip in a worktree and must PASS in your run. Report
 every `SKIPPED` line. Then `python3 -m ruff check tests/ui_contracts/test_brain_motion_tokens.py`,
 real exit 0, and `python3 -m apps.cli.main integrity check --json`, which must read all six
 checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f019-r2-mut <C4>`, then
 `python3 -B .remedy-wt/f019-r2-payloads/mutations.py
 /home/decodeux/Repos/remedy/.remedy-wt/f019-r2-mut` and report its whole output. The reviewer
 read, over the same tool against its sim tree: vitest control `64 passed` and pytest control
 `5 passed`, both at exit 0, first and last; failed counts at exit 1 of L1 2, L2 1, L3 2, L4 1,
 L5 1, L6 1, L7 1, L8 1, L9 1, B1 1, B2 1, B3 1, B4 4, P1 2 and P2 1; every mutation restored
 byte-identical, and the final line `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`. Then
 `git worktree remove --force .remedy-wt/f019-r2-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty; `git log --oneline
 -n 9`, which must show C5, C4, C3, C2, C1d, C1c, C1b, C1a and `b6cc2690` in that order; the
 push's real outcome; and `git worktree list`. These readings go in your reply.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertions you MEASURED beside the ones this
block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and the
next expected action. Your Session section reads SESSION 1 of feature F019, round 2, and says in
one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 2, then T002's painted half as DECISION F019 D2 (1) names it. State the open-findings
count, 4, and the operator-questions count, 2.
