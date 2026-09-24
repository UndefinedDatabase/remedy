STEP F019 R6 — BOOK ROUND 5 AND FINISH T003: a live fake job checked against the demo recording, and the performance fixture measured in headless Chrome

GOAL
Book round 5's PASS, record DECISION F019 D6, and finish T003: the committed performance fixture
`apps/ui/src/components/graph/brainPerfFixture.ts` with its vitest test, the end-to-end test
`tests/ui_server/test_brain_demo_recording_live.py`, one line in `docs/roadmap/features/T5_F044.md`
naming the fixture, red proofs, and the stage-1 frame budget measured on the fixture with the
reviewer's measurement tool, which is kept as evidence under `.agent/authored/`.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f019-r6-payloads/`  READ-ONLY. The reviewer's payloads, `perf/` included.
  `.remedy-wt/f019-r6/`           READ-ONLY. The reviewer's block, texts and builder.
  `.remedy-wt/f019-r6-sim/`, `.remedy-wt/f019-r6-proto/`, `.remedy-wt/f019-r6-helper/`
                                  The reviewer's trees and tools; do not touch.
  `.remedy-wt/f019-r6-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored. The measurement tool creates and removes its own
                                  work dir `.remedy-wt/f019-perf-run/`.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, `cd <dir> && git ...`, and multi-operation
one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe pytest.
Use `git -C <path>` rather than `cd`. Use `python3 - <<'PY'` for counting, hashing and
copying (`shutil.copyfile`). A heredoc containing a dollar-brace or an f-string brace is refused:
write such a script to a file under your own directory and run the file. Never run npm or npx.
Never `pkill -f` anything.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f019-live-node-materialization`, and `git log --oneline -1` must read `22f3fe99`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f019-r6/block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.

PAYLOADS — under `.remedy-wt/f019-r6-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 61 | 10720 | b04bb2ea3debc6bd2eb2f8ac31143492a5df80e23b26ee91c431985542cb5403 |
| plan.md | 34 | 1403 | a03a038cf49858201e514d2bc35fdd4d9b157db1e018f6fb3148415f07bbd4a8 |
| product.diff | 167 | 8473 | 137375662f2e0328acd402d454c3e5d12847304b2e52407137d268278285ec3e |
| tests.diff | 253 | 10283 | eb7e3c8ae58dba663f31b4ab6b8a81db5f54f47bc9b1a2961f8cc0fda0cf4456 |
| mutations.py | 295 | 11928 | a8eee80e81b94c7341874813a0739c342fda7d2e119c0308f60b321a7074644a |
| perf/measure.py | 191 | 6512 | b5f38fd7112f0ffb787424fc18d585d5db05e8e9290e06ec70191490e2a8e4f9 |
| perf/index.html | 14 | 351 | 36c417978e86247aa68b70efdad66f35d0cf22e8e10ec4aa2dcdd3830c95a6cc |
| perf/main.tsx | 119 | 3814 | 3a9721713b9daa476dbfd3515a4c5ed0ca0b56b96d1e1107ead9ead996dae1c4 |
| perf/vite.config.mjs | 28 | 766 | 82b2d0f857c6821f6136d323d41d43ad94e6e4993ff192f17ee5425f9a74c6a9 |
| perf/drive_chrome.mjs | 127 | 4459 | 6b8886d2b1f5367e9f2b9690234531ad2c6fa657475061902d760c74c09c7438 |

`plan.md` is a REWRITE of `.agent/plan.md`. The three `.diff` files go on with `git apply`; the
reviewer generated each with `git diff` from a tree at `22f3fe99` into which its builder copied
the reviewed prototype. `records.diff` appends the `Gate: F019 R5 — ` entry to
`.agent/live_review.md` and DECISION F019 D6 to `.agent/decisions.md`. `product.diff` creates
`brainPerfFixture.ts` and adds one bullet to `docs/roadmap/features/T5_F044.md`. `tests.diff`
creates `brainPerfFixture.test.ts` and `tests/ui_server/test_brain_demo_recording_live.py`.
`mutations.py` and the files under `perf/` are TOOLS for G5: they are run from the payload
directory, never applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C1c, C1d, C2, C3, C4 and C5, in this order.

C1a — `.agent/authored/f019-r6-block.md` := this block and `.agent/authored/f019-r6-plan.md` :=
  plan.md, by `shutil.copyfile`.
  Subject: `F019 R6 C1a: copy round 6 block and plan into .agent/authored/`
  Its insertions are this block's line count plus 34; STOP rather than commit if 500 or more.
C1b — `.agent/authored/f019-r6-records.diff`, `.agent/authored/f019-r6-product.diff` and
  `.agent/authored/f019-r6-tests.diff`.
  Subject: `F019 R6 C1b: copy round 6 records, product and tests diffs into .agent/authored/`
  Expected insertions: 481.
C1c — `.agent/authored/f019-r6-mutations.py`.
  Subject: `F019 R6 C1c: copy round 6 mutation tool into .agent/authored/`
  Expected insertions: 295.
C1d — each `perf/<name>` as `.agent/authored/f019-r6-perf-<name>` (five files, same names
  after the prefix).
  Subject: `F019 R6 C1d: copy round 6 frame-rate measurement tool into .agent/authored/`
  Expected insertions: 479.
C2 — THE BOOKING: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F019 R6 C2: book round 5's PASS, record DECISION F019 D6`
  Expected insertions by `git show --numstat`: 43 decisions.md, 2 live_review.md, 10 plan.md.
C3 — THE PRODUCT: `git apply` product.diff, then `git add` the new `brainPerfFixture.ts`.
  Subject: `F019 R6 C3: add the frame-budget fixture and name it in F044's file`
  Expected insertions: 144 brainPerfFixture.ts, 6 T5_F044.md.
C4 — THE TESTS: `git apply` tests.diff, then `git add` the two new test files.
  Subject: `F019 R6 C4: check a live fake job against the demo recording, pin the fixture`
  Expected insertions: 65 brainPerfFixture.test.ts, 176 test_brain_demo_recording_live.py.
C5 — THE HANDBACK: `.agent/handoff.md`, rewritten, its own commit, per
  `docs/agents/handback_template.md`. Subject: `F019 R6 C5: rewrite handoff for round 6`. Then
  `git push origin feature/f019-live-node-materialization` and report its real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading.
3. The round's whole tracked path set is: the `.agent/authored/f019-r6-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, the files the product and
   test diffs name, and `.agent/handoff.md`. Report `git diff --name-only 22f3fe99 HEAD` after C5.
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
 then each `.agent/authored/f019-r6-*` copy byte for byte against its source (the block copy
 against `.remedy-wt/f019-r6/block.md`), read back with `git show <commit>:<path>`.

G2 THE BOOKING — at C2, read with `git show <C2>:<path>`, each equals the reviewer's simulated
 reading:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/decisions.md | 2015857 | a0b68b8aadc2a67353828c72f736943cefc5966c9448215ae1a8aa3de32a1fdd |
 | .agent/live_review.md | 317737 | cb0f8c063c8305f17320069dbafdc1160f28100d64d136544ca630c50a43da73 |
 | .agent/plan.md | 1403 | a03a038cf49858201e514d2bc35fdd4d9b157db1e018f6fb3148415f07bbd4a8 |
 Then the count of lines C2 adds to the ledger beginning `Gate: F019 R5 — `, which must be 1,
 and `open_finding_ids` of `scripts/rotate_live_review.py` over the ledger's text at `22f3fe99`
 and at C2, which the reviewer read as R-0499, R-0950, R-1008 and R-1046 at both.

G3 THE PRODUCT AND TESTS — at C4, read with `git show <C4>:<path>`, each equals the reviewer's
 simulated reading:
 | path | bytes | sha256 |
 |---|---|---|
 | apps/ui/src/components/graph/brainPerfFixture.ts | 7263 | f83198af2c1149df0a93f5ca755b42e524b61b4edb5e51f66bdb2cb73432b67c |
 | docs/roadmap/features/T5_F044.md | 5327 | 4d2fa890dd73e33e76ce1dbabc23d47cb0297e50b28c80266738e5f677af1e1a |
 | apps/ui/src/components/graph/brainPerfFixture.test.ts | 2691 | d5f413954a0e1db2dd087084bbb4c03ff4dffb9b0eb963681aacae2ec6db7bd9 |
 | tests/ui_server/test_brain_demo_recording_live.py | 6838 | 21535036b49fd59a9525150bdf742c579756ba355aecdfb9d6d6488e96c7ccf0 |

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/ui_server/test_brain_demo_recording_live.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The selection names the NEW FILE at `tests/ui_server/test_brain_demo_recording_live.py`, which C4
 creates. The reviewer ran the same selection WITHOUT the golden path inside its sim tree and read
 `1381 passed, 10 skipped` at exit 0. The two eslint nodes of `tests/ui_contracts/test_ui_lint.py`,
 the tsc node of `tests/ui_server/test_dashboard_contract.py` and the vitest node of
 `tests/orchestration/test_test_runner.py` skip in a worktree and must PASS in your run. Report
 every `SKIPPED` line. Then `python3 -m ruff check tests/ui_server/test_brain_demo_recording_live.py`,
 real exit 0, and `python3 -m apps.cli.main integrity check --json`, which must read all six
 checks `pass` at `fail_count` 0. Then `git status --porcelain`, which must still be empty.

G5 THE RED PROOFS AND THE MEASUREMENT — `git worktree add --detach .remedy-wt/f019-r6-mut <C4>`,
 then `python3 -B .remedy-wt/f019-r6-payloads/mutations.py
 /home/decodeux/Repos/remedy/.remedy-wt/f019-r6-mut` and report its whole output. The reviewer
 read, over the same tool against its prototype tree, whose product and test files equal the G3
 readings: controls `134 passed` for vitest and `1 passed` for pytest, both at exit 0, first and
 last; failed counts at exit 1 of F1 vitest 2, F2 vitest 6, F3 vitest 2, P1 vitest 2 and pytest 1,
 P2 vitest 2 and pytest 1; every mutation restored byte-identical, and the final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`. Then `git worktree remove --force
 .remedy-wt/f019-r6-mut` and `git worktree prune`. THEN THE MEASUREMENT, in the primary checkout
 at C4: `bash -c 'python3 .remedy-wt/f019-r6-payloads/perf/measure.py /home/decodeux/Repos/remedy;
 echo "REAL_EXIT=$?"'` and report its whole output. The reviewer read, with the same tool against
 its prototype tree: six runs, three at 200 nodes and three at 500 nodes, each with 481 frames,
 mean 60 fps, p50 16.7 ms and p95 at most 16.8 ms, the final line `BUDGET stage1 200 nodes: p95
 16.8 ms, mean 60 fps, PASS`, and `REAL_EXIT=0`. Your frame and millisecond readings may differ by
 a frame or a tenth of a millisecond; report them as measured, and the verdict line must read PASS.
 Then report `git worktree list` and `ls .remedy-wt/f019-perf-run`, which must say the directory
 does not exist.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty; `git log --oneline
 -n 9`, which must show C5, C4, C3, C2, C1d, C1c, C1b, C1a and `22f3fe99` in that order; the
 push's real outcome; and `git worktree list`. These readings go in your reply.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertions you MEASURED beside the ones this
block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and the
next expected action. Your Session section reads SESSION 2 of feature F019, round 6, and says in
one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 6, then F019's closure sequence per `docs/roadmap/STATUS_closure_protocol.md`, T001, T002
and T003 being built. State the open-findings count, 4, and the operator-questions count, 3.
