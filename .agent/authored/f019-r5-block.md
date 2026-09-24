STEP F019 R5 — BOOK ROUND 4 AND WIRE THE GRAPH LIVE: the stage folds the complete prefix of a ledger merged from `events-since` pages and the live ring

GOAL
Book round 4's PASS, record DECISION F019 D5, and land T003's first half: the new pure module
`apps/ui/src/components/graph/brainLedger.ts` and its thin hook `useBrainLedger.ts`, the exported
path builder `eventsSincePath` in `brainStreamDeps.ts`, the shell handing the stage the live ring
and a page reader, and the stage rebuilding its model from the ledger's complete prefix, with
vitest tests, a source guard and red proofs.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f019-r5-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f019-r5/`           READ-ONLY. The reviewer's block, texts and builder.
  `.remedy-wt/f019-r5-sim/`, `.remedy-wt/f019-r5-proto/`, `.remedy-wt/f019-r5-helper/`
                                  The reviewer's trees and tools; do not touch.
  `.remedy-wt/f019-r5-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, `cd <dir> && git ...`, and multi-operation
one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe pytest.
Use `git -C <path>` rather than `cd`. Use `python3 - <<'PY'` for counting, hashing and
copying (`shutil.copyfile`). A heredoc containing a dollar-brace or an f-string brace is refused:
write such a script to a file under your own directory and run the file. Never run npm or npx.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f019-live-node-materialization`, and `git log --oneline -1` must read `238f2aa5`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f019-r5/block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.

PAYLOADS — under `.remedy-wt/f019-r5-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 57 | 10140 | 1900ffc087f94bc6e789b8f380ce0eaf4c1141fa030f406e7de5bf2bc802ae09 |
| plan.md | 34 | 1362 | bc1babf1c5bca2ddf7bf73bf9c24906da2dafbf3d63148c3e41ecac179377e77 |
| product.diff | 375 | 18748 | 27b555cfab0fb4b94efff4808d84e9ee7be214c61f5dfcfecfc61cea131aab8d |
| tests.diff | 365 | 15972 | 9da3e999e72390047363a72d0bcc074ecb44d35b1c5ecc4d02143ea92b675e43 |
| mutations.py | 351 | 14009 | 923127841b30d778a59403d84c35bf3bc665ffbb843f2d7c4550902a4e512864 |

`plan.md` is a REWRITE of `.agent/plan.md`. The three `.diff` files go on with `git apply`; the
reviewer generated each with `git diff` from a tree at `238f2aa5` into which its builder copied
the reviewed prototype. `records.diff` appends the `Gate: F019 R4 — ` entry to
`.agent/live_review.md` and DECISION F019 D5 to `.agent/decisions.md`. `product.diff` edits
`apps/ui/src/api/brainStreamDeps.ts`, `BrainGraphStage.tsx` and
`apps/ui/src/components/shell/RemedyShell.tsx`, and creates `brainLedger.ts` and
`useBrainLedger.ts`. `tests.diff` edits `apps/ui/src/api/brainStreamDeps.test.ts` and
`tests/ui_contracts/test_brain_stage_mount.py`, and creates `brainLedger.test.ts` and
`tests/ui_contracts/test_brain_live_wiring.py`. `mutations.py` is a TOOL for G5: it is run,
never applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C1c, C1d, C2, C3, C4 and C5, in this order.

C1a — `.agent/authored/f019-r5-block.md` := this block and `.agent/authored/f019-r5-plan.md` :=
  plan.md, by `shutil.copyfile`.
  Subject: `F019 R5 C1a: copy round 5 block and plan into .agent/authored/`
  Its insertions are this block's line count plus 34; STOP rather than commit if 500 or more.
C1b — `.agent/authored/f019-r5-records.diff` and `.agent/authored/f019-r5-product.diff`.
  Subject: `F019 R5 C1b: copy round 5 records and product diffs into .agent/authored/`
  Expected insertions: 432.
C1c — `.agent/authored/f019-r5-tests.diff`.
  Subject: `F019 R5 C1c: copy round 5 tests diff into .agent/authored/`
  Expected insertions: 365.
C1d — `.agent/authored/f019-r5-mutations.py`.
  Subject: `F019 R5 C1d: copy round 5 mutation tool into .agent/authored/`
  Expected insertions: 351.
C2 — THE BOOKING: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F019 R5 C2: book round 4's PASS, record DECISION F019 D5`
  Expected insertions by `git show --numstat`: 39 decisions.md, 2 live_review.md, 10 plan.md.
C3 — THE PRODUCT: `git apply` product.diff, then `git add` the new `brainLedger.ts` and
  `useBrainLedger.ts`.
  Subject: `F019 R5 C3: fold the ledger's complete prefix into the live graph`
  Expected insertions and deletions: brainStreamDeps.ts 9 and 1, brainLedger.ts 165 and 0,
  useBrainLedger.ts 72 and 0, BrainGraphStage.tsx 25 and 4, RemedyShell.tsx 12 and 3.
C4 — THE TESTS: `git apply` tests.diff, then `git add` the two new test files.
  Subject: `F019 R5 C4: pin the ledger, the gap fill and the live wiring`
  Expected insertions and deletions: brainStreamDeps.test.ts 7 and 1, brainLedger.test.ts 196 and
  0, test_brain_live_wiring.py 114 and 0, test_brain_stage_mount.py 5 and 2.
C5 — THE HANDBACK: `.agent/handoff.md`, rewritten, its own commit, per
  `docs/agents/handback_template.md`. Subject: `F019 R5 C5: rewrite handoff for round 5`. Then
  `git push origin feature/f019-live-node-materialization` and report its real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading.
3. The round's whole tracked path set is: the `.agent/authored/f019-r5-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, the files the product and
   test diffs name, and `.agent/handoff.md`. Report `git diff --name-only 238f2aa5 HEAD` after C5.
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
 then each `.agent/authored/f019-r5-*` copy byte for byte against its source (the block copy
 against `.remedy-wt/f019-r5/block.md`), read back with `git show <commit>:<path>`.

G2 THE BOOKING — at C2, read with `git show <C2>:<path>`, each equals the reviewer's simulated
 reading:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2012239 | d489e9b2c5f8f2478723cff983b3e4f13f2d764cf2483f34f9b33b5f6f1517e2 |
 | .agent/live_review.md | 315698 | 06b91d40088f7bee6702f8b62c8facac9791251a46d0cf53ca5a2eb0a3fe75be |
 | .agent/plan.md | 1362 | bc1babf1c5bca2ddf7bf73bf9c24906da2dafbf3d63148c3e41ecac179377e77 |
 Then the count of lines C2 adds to the ledger beginning `Gate: F019 R4 — `, which must be 1,
 and `open_finding_ids` of `scripts/rotate_live_review.py` over the ledger's text at `238f2aa5`
 and at C2, which the reviewer read as R-0499, R-0950, R-1008 and R-1046 at both.

G3 THE PRODUCT AND TESTS — at C4, read with `git show <C4>:<path>`, each equals the reviewer's
 simulated reading:
 | path | bytes | sha256 |
 |---|---|---|
 | apps/ui/src/api/brainStreamDeps.ts | 7546 | 006982735aa9281dfa7c4262080cb656f5dcfd1eb4749e44b8d723b4cb55a8db |
 | apps/ui/src/components/graph/brainLedger.ts | 7527 | 25c798c79b025a1e6d0d3c9ddd29931cb000b925a9167f38d5afc7406d4d0ffd |
 | apps/ui/src/components/graph/useBrainLedger.ts | 2927 | 59f20564662bd2aee15dea0d37e0d7cf832be60f20197f5c8c683ee44aec7519 |
 | apps/ui/src/components/graph/BrainGraphStage.tsx | 3369 | 8582b09e4563caf277de15da5493485fd96faa5dbe5f832f9f07571e0499d47b |
 | apps/ui/src/components/shell/RemedyShell.tsx | 13113 | 9ce1a7cdc9886e9fcc9098a8ba448595d56dfa09cda3d93160ff7abaa1ea9093 |
 | apps/ui/src/api/brainStreamDeps.test.ts | 7110 | fea8a2904e6a0d6ce6778d5c273c5a93ee4b91eb03f2fb9bc96f0a27b7caf886 |
 | apps/ui/src/components/graph/brainLedger.test.ts | 8214 | fc7d1f1c82041ae7a8b159eee93b890e5bd49979cc72965dd8963b6c0dde647b |
 | tests/ui_contracts/test_brain_live_wiring.py | 4805 | 9cd35d428e11366a42295479cdf2c079c2acbf382b22ddf9aee16e0a9fee7701 |
 | tests/ui_contracts/test_brain_stage_mount.py | 4582 | 48a4fde3f8fa3f6145f1b5cd6e55ff07c9c82471e03596297c84ed11fa0fb731 |

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path inside its sim tree and read
 `1380 passed, 10 skipped` at exit 0. The two eslint nodes of `tests/ui_contracts/test_ui_lint.py`,
 the tsc node of `tests/ui_server/test_dashboard_contract.py` and the vitest node of
 `tests/orchestration/test_test_runner.py` skip in a worktree and must PASS in your run. Report
 every `SKIPPED` line. Then `python3 -m ruff check tests/ui_contracts/test_brain_live_wiring.py
 tests/ui_contracts/test_brain_stage_mount.py`, real exit 0, and
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass` at
 `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f019-r5-mut <C4>`, then
 `python3 -B .remedy-wt/f019-r5-payloads/mutations.py
 /home/decodeux/Repos/remedy/.remedy-wt/f019-r5-mut` and report its whole output. The reviewer
 read, over the same tool against its prototype tree, whose product and test files equal the
 G3 readings: vitest control `124 passed` and pytest control `32 passed`, both at exit 0, first
 and last; failed counts at exit 1 of L1 2, L2 4, L3 2, L4 7, L5 1, L6 1, L7 1, L8 5, W1 3,
 W2 1 and W3 1; every mutation restored byte-identical, and the final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`. Then
 `git worktree remove --force .remedy-wt/f019-r5-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty; `git log --oneline
 -n 9`, which must show C5, C4, C3, C2, C1d, C1c, C1b, C1a and `238f2aa5` in that order; the
 push's real outcome; and `git worktree list`. These readings go in your reply.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertions you MEASURED beside the ones this
block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and the
next expected action. Your Session section reads SESSION 2 of feature F019, round 5, and says in
one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 5, then the rest of T003 as DECISION F019 D5 (1) names it: the end-to-end run of a live fake
job compared against the demo recording, and the performance fixture's measurement. State the
open-findings count, 4, and the operator-questions count, 3.
