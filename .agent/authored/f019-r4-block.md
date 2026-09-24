STEP F019 R4 — BOOK ROUND 3 AND FINISH T002: the old decorative builder removed with its pins, and the demo recording with its golden

GOAL
Book round 3's PASS, record DECISION F019 D4, remove the old decorative `buildForceBrainModel()`
with its six types and the source pins that held them, and commit the demo recording
`apps/ui/src/components/graph/brainDemoRecording.ts`, a captured fake-provider job, with its
hand-derived golden in `brainDemoRecording.test.ts`, and red proofs.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f019-r4-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f019-r4/`           READ-ONLY. The reviewer's block, texts and builder.
  `.remedy-wt/f019-r4-sim/`, `.remedy-wt/f019-r4-proto/`, `.remedy-wt/f019-r4-helper/`,
  `.remedy-wt/f019-r4-research/`  The reviewer's trees and tools; do not touch.
  `.remedy-wt/f019-r4-worker/`    YOURS for logs and scripts; create it if absent. All are
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
   `feature/f019-live-node-materialization`, and `git log --oneline -1` must read `4b513511`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f019-r4/block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.

PAYLOADS — under `.remedy-wt/f019-r4-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 63 | 10710 | 0a309187242068ace3d01a9498dfc6d44b2e186cca600b705335c818d05f30ce |
| plan.md | 34 | 1319 | 00a4280d10c26e8b39bb1e3749af15c345b2499798f9f99174c07fbf96648132 |
| product.diff | 319 | 14553 | a8eb07d3e66f84add33e3a8519e9a382bc0b6ae503b2a9f377e17aefcbea7fed |
| tests.diff | 254 | 12612 | 1d45048824625bed1d2baa9cd64560dbeb619e4d329e53c706547da964456a60 |
| mutations.py | 307 | 12712 | d3a2bbff5a7628f3baa5dd47dcdd05cc991f338346c9acb6eb85b1c9eedc6be6 |

`plan.md` is a REWRITE of `.agent/plan.md`. The three `.diff` files go on with `git apply`; the
reviewer generated each with `git diff` from a tree at `4b513511` into which its builder copied
the reviewed prototype. `records.diff` appends the `Gate: F019 R3 — ` entry to
`.agent/live_review.md` and DECISION F019 D4 to `.agent/decisions.md`. `product.diff` edits
`buildForceBrainModel.ts` and `forceBrainTypes.ts` and creates `brainDemoRecording.ts`.
`tests.diff` edits `buildForceBrainModel.test.ts`, `tests/ui_server/test_dashboard_contract.py` and
`tests/ui_contracts/test_graph_architecture.py`, and creates `brainDemoRecording.test.ts`.
`mutations.py` is a TOOL for G5: it is run, never applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C1c, C1d, C2, C3, C4 and C5, in this order.

C1a — `.agent/authored/f019-r4-block.md` := this block and `.agent/authored/f019-r4-plan.md` :=
  plan.md, by `shutil.copyfile`.
  Subject: `F019 R4 C1a: copy round 4 block and plan into .agent/authored/`
  Its insertions are this block's line count plus 34; STOP rather than commit if 500 or more.
C1b — `.agent/authored/f019-r4-records.diff` and `.agent/authored/f019-r4-product.diff`.
  Subject: `F019 R4 C1b: copy round 4 records and product diffs into .agent/authored/`
  Expected insertions: 382.
C1c — `.agent/authored/f019-r4-tests.diff`.
  Subject: `F019 R4 C1c: copy round 4 tests diff into .agent/authored/`
  Expected insertions: 254.
C1d — `.agent/authored/f019-r4-mutations.py`.
  Subject: `F019 R4 C1d: copy round 4 mutation tool into .agent/authored/`
  Expected insertions: 307.
C2 — THE BOOKING: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F019 R4 C2: book round 3's PASS, record DECISION F019 D4`
  Expected insertions by `git show --numstat`: 45 decisions.md, 2 live_review.md, 8 plan.md.
C3 — THE PRODUCT: `git apply` product.diff, then `git add` the new `brainDemoRecording.ts`.
  Subject: `F019 R4 C3: remove the decorative dashboard builder, add the demo recording`
  Expected insertions and deletions: buildForceBrainModel.ts 8 and 143, forceBrainTypes.ts 9 and
  51, brainDemoRecording.ts 72 and 0.
C4 — THE TESTS: `git apply` tests.diff, then `git add` the new `brainDemoRecording.test.ts`.
  Subject: `F019 R4 C4: pin the recording's golden and the graph's truth contract`
  Expected insertions and deletions: brainDemoRecording.test.ts 116 and 0,
  buildForceBrainModel.test.ts 1 and 45, test_dashboard_contract.py 10 and 31,
  test_graph_architecture.py 1 and 1.
C5 — THE HANDBACK: `.agent/handoff.md`, rewritten, its own commit, per
  `docs/agents/handback_template.md`. Subject: `F019 R4 C5: rewrite handoff for round 4`. Then
  `git push origin feature/f019-live-node-materialization` and report its real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading.
3. The round's whole tracked path set is: the `.agent/authored/f019-r4-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, the files the product and
   test diffs name, and `.agent/handoff.md`. Report `git diff --name-only 4b513511 HEAD` after C5.
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
 then each `.agent/authored/f019-r4-*` copy byte for byte against its source (the block copy
 against `.remedy-wt/f019-r4/block.md`), read back with `git show <commit>:<path>`.

G2 THE BOOKING — at C2, read with `git show <C2>:<path>`, each equals the reviewer's simulated
 reading:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2008978 | 5b3ef727c084fdde10ea377df14d38ee8cf8b43ea16b94af4dc6147ebcf00b22 |
 | .agent/live_review.md | 313478 | 7cd05b719fd2f803a3f8b4faf40803892c11b8194c855af3ccafe266c1ada853 |
 | .agent/plan.md | 1319 | 00a4280d10c26e8b39bb1e3749af15c345b2499798f9f99174c07fbf96648132 |
 Then the count of lines C2 adds to the ledger beginning `Gate: F019 R3 — `, which must be 1,
 and `open_finding_ids` of `scripts/rotate_live_review.py` over the ledger's text at `4b513511`
 and at C2, which the reviewer read as R-0499, R-0950, R-1008 and R-1046 at both.

G3 THE PRODUCT AND TESTS — at C4, read with `git show <C4>:<path>`, each equals the reviewer's
 simulated reading:
 | path | bytes | sha256 |
 |---|---|---|
 | apps/ui/src/components/graph/buildForceBrainModel.ts | 8068 | f75ab0d238bd8fe6565422049eab10496e29a946358403ac3072ecaaea55f3c8 |
 | apps/ui/src/components/graph/forceBrainTypes.ts | 1469 | 7ff324a5c9fb11df808bdc24387b001aaf0491ff94aa0bdab7b4a1233917c561 |
 | apps/ui/src/components/graph/brainDemoRecording.ts | 4021 | 00c3f0c99689ef5b9af368e8669a4917c611f5ae3483a2ccef878228b58da274 |
 | apps/ui/src/components/graph/buildForceBrainModel.test.ts | 9929 | 2a4310ac377bd4287157d1fa3041d818ef0dbce2381f2bc55f6e5166dfa36131 |
 | apps/ui/src/components/graph/brainDemoRecording.test.ts | 5938 | 79b057272a1f6398592a5185353da030ae76d64ebb2eae9c9fd6d73c4f1a8f9d |
 | tests/ui_server/test_dashboard_contract.py | 28533 | d2661b635d3d876bf64bca620948103f3501f133c2b41210eae7cac5ba66abb7 |
 | tests/ui_contracts/test_graph_architecture.py | 36438 | 4c01e73938a4b0da50cf5be87affa37b63be00415ac347c79dc8367cf039d695 |

G4 THE TESTS AND THE REMOVAL — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path inside its sim tree and read
 `1367 passed, 10 skipped` at exit 0. The two eslint nodes of `tests/ui_contracts/test_ui_lint.py`,
 the tsc node of `tests/ui_server/test_dashboard_contract.py` and the vitest node of
 `tests/orchestration/test_test_runner.py` skip in a worktree and must PASS in your run. Report
 every `SKIPPED` line. Then `python3 -m ruff check tests/ui_server/test_dashboard_contract.py
 tests/ui_contracts/test_graph_architecture.py`, real exit 0, and
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass` at
 `fail_count` 0. Then the removal search, which must print no match line and `GREP_EXIT=1`
 (the reviewer read 36 matching lines across five files with `git grep -c` and the same pattern
 and paths at `4b513511`):
```
bash -c 'git grep -n -E "buildForceBrainModel\(|ForceBrainNode|ForceBrainLink|ForceBrainGraphData|BrainSourceKind|BrainNodeKind|BrainNodeState" -- apps packages tests scripts docs; echo "GREP_EXIT=$?"'
```

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f019-r4-mut <C4>`, then
 `python3 -B .remedy-wt/f019-r4-payloads/mutations.py
 /home/decodeux/Repos/remedy/.remedy-wt/f019-r4-mut` and report its whole output. The reviewer
 read, over the same tool against its prototype tree, whose product and test files equal the
 G3 readings: vitest control `89 passed` and pytest control `11 passed`, both at exit 0, first
 and last; failed counts at exit 1 of D1 8, D2 2, D3 1, D4 2, P1 1, P2 1 and P3 1; every
 mutation restored byte-identical, and the final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`. Then
 `git worktree remove --force .remedy-wt/f019-r4-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty; `git log --oneline
 -n 9`, which must show C5, C4, C3, C2, C1d, C1c, C1b, C1a and `4b513511` in that order; the
 push's real outcome; and `git worktree list`. These readings go in your reply.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertions you MEASURED beside the ones this
block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and the
next expected action. Your Session section reads SESSION 2 of feature F019, round 4, and says in
one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 4, then T003: the live wiring from the stream hook through the reducer to the renderer, gap
and snapshot recovery by paging `events-since`, the performance fixture, and the end-to-end run on
a live fake job compared against the demo recording. State the open-findings count, 4, and the
operator-questions count, 3.
