STEP F265 R4 — T003: THE COMMANDS MODE, the commands a task's diff touched, from the shipped catalog

GOAL
Book round 3's PASS, record DECISION F265 D4, and land T003: every row of the job's lessons
index carries the CLI commands its task's stored diff touched — a command whose handler module
the diff changed, or whose catalog line it changed — each with its invocation and the
catalog's shipped description, computed whenever the index is read; and the overlay gains a
Lesson and Commands switch that shows them. With this round T001 to T003 are built.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge.

WHY THIS IS NEXT
T5_F265.md's Orchestrator brief: T003 is small and independent of T002, and its Design says the
mode explains the SHIPPED description, never a remembered one. DECISION F265 D4 (in records.diff)
fixes what "touched" means and why the list is computed at read time and never stored. The
closure sequence follows.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f265-r4-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f265-r4-scratch/`   The reviewer's scripts; do not edit or delete them.
  `.remedy-wt/f265-r4-worker/`    YOURS for logs and scripts. All three are gitignored.
  `mutations.py` writes its vitest config and cache under `.remedy-wt/f265-r4-mutcfg/`.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, `cd <dir> && git ...`, and multi-operation
one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe pytest.
Use `git -C <path>` rather than `cd`. Use `python3 - <<'PY'` for counting, hashing and
copying (`shutil.copyfile`). A heredoc containing a dollar-brace is refused: write such a
script to a file under your own directory and run the file. Do NOT run `npm` or `npx`
yourself: the UI's lint, type check and vitest reach you through the pytest nodes G4 names
and through `mutations.py`.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f265-teacher-learning-ui`, and `git log --oneline -1` must read `b8ecbb3b`. Report
   all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f265-r4-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f265-r4-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 55 | 10652 | afe1f1e8a84d5963a4c587dac9c62ef4d53c94fe6b23efee32ba273b96cc5a50 |
| plan.md | 33 | 1327 | bb61f8ce265df0fde7463250e47f0897179d519ad3f2601db3fb84cad939f308 |
| product.diff | 303 | 14964 | 3e7e67c232c858e9a7edb53553b0dd5ee014e73d872f3954ae6efd139f259436 |
| tests.diff | 136 | 6378 | 868976df7aa3e48005eaaa4c26f8df9834f3e754e6e5dd7c8b90b9e75066f36f |
| mutations.py | 87 | 4553 | 7e1e3f56f15f10aa5999e3fa93341b3e780f6830117ed302430189de3fcf5a48 |

`plan.md` is a REWRITE of `.agent/plan.md`. The `.diff` files go on with `git apply`; the
reviewer generated each from a tree at `b8ecbb3b` and applied them, in the commit order below, to
a fresh worktree at `b8ecbb3b` with `git apply --check` then `git apply`, every one at real exit
code 0. `records.diff` appends the round 3 gate entry to `.agent/live_review.md` and DECISION
F265 D4 to `.agent/decisions.md`. `product.diff` edits `packages/orchestration/lessons.py`,
`apps/ui/src/api/lessons.ts`, `apps/ui/src/components/lessons/LessonsOverlay.tsx` and
`apps/ui/src/components/lessons/LessonsOverlay.module.css`. `tests.diff` edits
`tests/orchestration/test_lessons.py`, `apps/ui/src/api/lessons.test.ts` and
`tests/ui_contracts/test_lessons_overlay_contract.py`. `mutations.py` is a TOOL for G5: it is
run, never applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C1c, C2, C3, C4 and C5, in this order.

C1a — copy this block and the record payloads
  `.agent/authored/f265-r4-block.md` := this block, and `.agent/authored/f265-r4-plan.md` and
  `.agent/authored/f265-r4-records.diff` := plan.md and records.diff. All by `shutil.copyfile`.
  Subject: `F265 R4 C1a: copy round 4 block and record payloads into .agent/authored/`
  Its insertions are this block's line count plus 88. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C1b — copy the product diff and the mutation tool
  `.agent/authored/f265-r4-<name>` for each of product.diff and mutations.py.
  Subject: `F265 R4 C1b: copy round 4 product diff and mutation tool into .agent/authored/`
  Expected insertions: 390.

C1c — copy the tests diff
  `.agent/authored/f265-r4-tests.diff` := tests.diff.
  Subject: `F265 R4 C1c: copy round 4 tests diff into .agent/authored/`
  Expected insertions: 136.

C2 — THE RECORDS, in this order:
   1. `git apply` records.diff
   2. rewrite `.agent/plan.md` := plan.md
  Subject: `F265 R4 C2: book round 3's PASS, record DECISION F265 D4`
  Expected insertions by `git show --numstat`: 37 decisions.md, 2 live_review.md, 9 plan.md.

C3 — THE PRODUCT: `git apply` product.diff and `git add` every path it edits.
  Subject: `F265 R4 C3: name the commands a task's change touched, from the shipped catalog`
  Expected insertions: 32 lessons.ts, 20 LessonsOverlay.module.css, 36 LessonsOverlay.tsx, 53 lessons.py.

C4 — THE TESTS: `git apply` tests.diff and `git add` every path it edits.
  Subject: `F265 R4 C4: test the Commands mode and pin it to the server`
  Expected insertions: 17 lessons.test.ts, 38 test_lessons.py, 15 test_lessons_overlay_contract.py.

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F265 R4 C5: rewrite handoff for round 4`
  Then `git push origin feature/f265-teacher-learning-ui`. Do NOT create a pull request.
  Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f265-r4-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, every path product.diff and
   tests.diff edit, and `.agent/handoff.md`. Report the list you measure with
   `git diff --name-only b8ecbb3b HEAD` after C5. Do NOT touch `.agent/context.md`,
   `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md`, `README.md`,
   `docs/roadmap/STATUS.md` or `docs/roadmap/features/T5_F265.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch
   deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees, their branches, the reviewer's worktrees
   `.remedy-wt/f265-r4-dry` and `.remedy-wt/f265-r4-sim`, and every existing stash alone. The
   worktree G5 adds goes under `.remedy-wt/`, is removed as that step's last action, and
   `git worktree list` is reported afterwards (finding R-0940).
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F265's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f265-r4-*` copy byte for byte
 with its source (the block copy against `.remedy-wt/f265-r4-block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, which its simulation printed from a tree it built by applying these
 payloads at `b8ecbb3b`:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 311835 | 4b92f17efab60f5d50f1744bb32f93f95f6449ae6f4f45de38872d4a632153ab |
 | .agent/decisions.md | 1970289 | 4a9d7ada2b4a43387db7f7a20459ca00382f6b2ba1222288e96b5cd1cc106889 |
 | .agent/plan.md | 1327 | bb61f8ce265df0fde7463250e47f0897179d519ad3f2601db3fb84cad939f308 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `b8ecbb3b` and at C2, with the set
 difference in both directions (the reviewer read 4 at both — R-0499, R-0950, R-1008 and
 R-1046 — both differences empty); the lines C2's diff adds to `.agent/live_review.md` that
 begin `Gate: F265 R3 — `, which must number 1; and `git diff --name-only <C1c> <C2>`, which
 must name exactly `.agent/decisions.md`, `.agent/live_review.md` and `.agent/plan.md`.

G3 THE PRODUCT AND THE TESTS — at C4, the sha256 of each file below, read with
 `git show <C4>:<path>`, equals the reviewer's simulated reading:
 | path | bytes | sha256 |
 |---|---|---|
 | packages/orchestration/lessons.py | 21462 | 600fbc92b561f321b1ed05c8332d50029262210e889e42a64e5126695b3dd2a3 |
 | apps/ui/src/api/lessons.ts | 8812 | c16b5a5407a507b65755e97f1cf1808b837e27a10c9361c499ea2c8855204a77 |
 | apps/ui/src/components/lessons/LessonsOverlay.tsx | 6979 | dbf8303e3783b56ae2324ac6d75348f01002f3adb08c98122a55bd058f398ca1 |
 | apps/ui/src/components/lessons/LessonsOverlay.module.css | 4904 | 637839358b42d661e2104c8ac3d04e35593f4375c65bb6d7085dbafc06feb1a7 |
 | tests/orchestration/test_lessons.py | 20382 | 98f512a2e8df94f41718b4fdf3d6b2a1df9067ade03ef220201b973bb78e0e72 |
 | apps/ui/src/api/lessons.test.ts | 6713 | 0d4f1d95207bd13307e42dd6aad617de8d26cc83e9af427083d3a7af1ee791c2 |
 | tests/ui_contracts/test_lessons_overlay_contract.py | 4630 | 4318bc9befaa5ecda836df4c7414679e1debea6852255718814a915b9f4318c9 |
 Also `git diff --name-only <C2> <C3>` and `<C3> <C4>`, which must name exactly the paths C3
 and C4 list.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash .remedy-wt/f265-r4-scratch/g4.sh /home/decodeux/Repos/remedy
```
 The script runs one pytest selection with `-rs` (all of `tests/ui_contracts/`, which holds the
 contract test and `test_ui_lint.py`'s eslint run; `tests/ui_server/test_dashboard_contract.py`,
 whose typescript node compiles `apps/ui`; `tests/orchestration/test_test_runner.py`, whose
 vitest node runs the whole UI suite; the lesson and lessons-route tests, `tests/docs/`, the
 state-file readers and `tests/cli/test_golden_path.py`), then `ruff check` over the touched
 Python files, then `python3 -m apps.cli.main integrity check --json`, each followed by its real
 exit code. The reviewer ran the same script inside its sim worktree carrying C1a to C4 and read
 `1476 passed, 10 skipped` at pytest exit 0, ruff at exit 0, and all six integrity checks
 `pass` at `fail_count` 0; the sim worktree has no `apps/ui/node_modules`, so its eslint,
 typescript and vitest nodes are among its skips, and the reviewer ran those three tools over
 the sim's `apps/ui` sources with the primary's toolchain instead, reading `tsc` exit 0, eslint
 exit 0 over the three changed TypeScript files, and vitest `21 passed` over the lessons test; in the primary checkout the eslint, typescript and vitest nodes must RUN, so report
 every SKIPPED line the `-rs` output prints and confirm none of those three nodes is among them.
 Report the pytest summary line and exit code, ruff's exit code, and whether all six integrity
 checks read `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f265-r4-mut <C4>`, then
 `python3 -B .remedy-wt/f265-r4-payloads/mutations.py .remedy-wt/f265-r4-mut` and report its
 whole output. For each mutation the script runs pytest over the worktree's lesson tests and
 contract test, and vitest over the worktree's `apps/ui/src/api/lessons.test.ts` from the
 primary `apps/ui`, restores the bytes, and runs an unmutated control first and last. The
 reviewer read, over the same script against its sim tree carrying C1a to C4:
 control_before pytest `44 passed` at exit 0 | vitest `21 passed` at exit 0;
 m1 (a changed handler module touches nothing) pytest 3 failed at exit 1;
 m2 (a changed catalog line touches nothing) pytest 1 failed at exit 1;
 m3 (a `command_id=` line in any file counts) pytest 1 failed at exit 1;
 m4 (the invocation drops the group) pytest 1 failed at exit 1;
 m5 (a row carries no commands) pytest 1 failed at exit 1;
 m6 (the decoder drops the commands) vitest 2 failed at exit 1;
 m7 (no line for a task without commands) vitest 1 failed at exit 1;
 m8 (the Commands switch hides its pressed state) pytest 1 failed at exit 1;
 in each of m1 to m8 the half not named reads its control count at exit 0;
 control_after as control_before; every `restored byte-identical` line True.
 Then `git worktree remove --force .remedy-wt/f265-r4-mut`, `git worktree prune`, report
 `git worktree list`, and report `git status --porcelain`, which must still be empty.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 8`, which must show C5, C4, C3, C2, C1c, C1b, C1a and `b8ecbb3b` in that
 order; `git worktree list`, which must show the primary checkout, the `.remedy-wt/job-*`
 worktrees and the reviewer's worktrees constraint 6 names, and nothing else; the push's real
 outcome; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which
 must be EMPTY. These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and
the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 1 of feature F265, round 4, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 4, then the closure sequence (docs/roadmap/STATUS_closure_protocol.md). State the
open-findings count, 4, and the operator-questions count, 1.
