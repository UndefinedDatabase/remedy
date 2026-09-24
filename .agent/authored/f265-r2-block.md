STEP F265 R2 — T001's REACH: the lesson announced on the stream, and the job's lessons route

GOAL
Book round 1's PASS, record DECISION F265 D2, and land T001's reach: a lesson the hook stores is
announced on the job's run log as `task_lesson_written`; a stream frame of that kind carries a
`lesson` field naming the Run and the status and nothing else; `GET /api/jobs/<job_id>/lessons`
lists every task's stored lesson or the reason it has none, reading and never writing; and the
hook names the job's mission, all with tests and red proofs.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge.

WHY THIS IS NEXT
T5_F265.md's Design: the overlay takes its data from the existing event stream, not from a
second polling path, and navigating the index is not re-generation. Round 1 stores lessons and
nothing yet announces or serves them. DECISION F265 D2 (in records.diff) fixes both halves. The
overlay itself, T002, is next round's work and reads exactly what this round serves.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f265-r2-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f265-r2-scratch/`   The reviewer's scripts; do not edit or delete them.
  `.remedy-wt/f265-r2-worker/`    YOURS for logs and scripts. All three are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, `cd <dir> && git ...`, and multi-operation
one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe pytest.
Use `git -C <path>` rather than `cd`. Use `python3 - <<'PY'` for counting, hashing and
copying (`shutil.copyfile`). A heredoc containing a dollar-brace is refused: write such a
script to a file under your own directory and run the file.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f265-teacher-learning-ui`, and `git log --oneline -1` must read `e7d1e080`. Report
   all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f265-r2-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f265-r2-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 59 | 8278 | 8adfcfc45448f7b22dc57d596347e4fda3f01fb54a88ae62e009ad182fb086cc |
| plan.md | 34 | 1367 | da7d4f209321b826b1da9e7c6b3b245e76c2376a07b60550c991af660951b564 |
| product.diff | 186 | 9625 | 3fb72088b9ef8be4863b5c73fd2dda161a40c4271566ab0fa3d1ea2441a53e62 |
| tests.diff | 66 | 3373 | e855e374cc1274de44df8fc3b4812409b0daca3824b9c2f87191bbf2cb26b613 |
| test_lessons_route.py | 123 | 5489 | b40bff157d2bc281b259676185d30811c2d46fcfa8f4a9494a68abb36106895c |
| mutations.py | 87 | 3242 | fca07fa92bf5ef4ea82ee8d8e75f61f18fd51c08a1a231ca612af30d96574d96 |

`plan.md` is a REWRITE of `.agent/plan.md`. `test_lessons_route.py` is a NEW FILE at
`tests/ui_server/test_lessons_route.py`, copied whole. The `.diff` files go on with
`git apply`; the reviewer generated each from a tree at `e7d1e080` and applied them, in the
commit order below, to a fresh worktree at `e7d1e080` with `git apply --check` then
`git apply`, every one at real exit code 0. `records.diff` appends the round 1 gate entry to
`.agent/live_review.md` and DECISION F265 D2 to `.agent/decisions.md`. `product.diff` edits
`packages/orchestration/lessons.py`, `packages/orchestration/pingpong_job.py`,
`packages/orchestration/ui_server.py`, `packages/orchestration/event_names.py` and
`apps/ui/src/api/humanizeCatalog.ts`. `tests.diff` edits `tests/orchestration/test_lessons.py`.
`mutations.py` is a TOOL for G5: it is run, never applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C2, C3, C4 and C5, in this order.

C1a — copy this block and the record payloads
  `.agent/authored/f265-r2-block.md` := this block, and `.agent/authored/f265-r2-plan.md` and
  `.agent/authored/f265-r2-records.diff` := plan.md and records.diff. All by `shutil.copyfile`.
  Subject: `F265 R2 C1a: copy round 2 block and record payloads into .agent/authored/`
  Its insertions are this block's line count plus 93. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C1b — copy the product and test payloads and the mutation tool
  `.agent/authored/f265-r2-<name>` for each of product.diff, tests.diff,
  test_lessons_route.py and mutations.py.
  Subject: `F265 R2 C1b: copy round 2 product, test payloads and mutation tool into .agent/authored/`
  Expected insertions: 462.

C2 — THE RECORDS, in this order:
   1. `git apply` records.diff
   2. rewrite `.agent/plan.md` := plan.md
  Subject: `F265 R2 C2: book round 1's PASS, record DECISION F265 D2`
  Expected insertions by `git show --numstat`: 41 decisions.md, 2 live_review.md, 13 plan.md.

C3 — THE PRODUCT: `git apply` product.diff and `git add` every path it edits.
  Subject: `F265 R2 C3: announce a stored lesson on the stream and serve the job's lessons`
  Expected insertions: 1 humanizeCatalog.ts, 1 event_names.py, 44 lessons.py, 13 pingpong_job.py, 27 ui_server.py.

C4 — THE TESTS: `git apply` tests.diff, copy test_lessons_route.py to
  `tests/ui_server/test_lessons_route.py`, and `git add` both.
  Subject: `F265 R2 C4: test the announcement, the stream field and the lessons route`
  Expected insertions: 50 test_lessons.py, 123 test_lessons_route.py.

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F265 R2 C5: rewrite handoff for round 2`
  Then `git push origin feature/f265-teacher-learning-ui`. Do NOT create a pull request.
  Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f265-r2-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, every path product.diff
   edits (listed under PAYLOADS), `tests/orchestration/test_lessons.py`,
   `tests/ui_server/test_lessons_route.py` and `.agent/handoff.md`. Report the list you measure
   with `git diff --name-only e7d1e080 HEAD` after C5. Do NOT touch `.agent/context.md`,
   `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md`, `README.md`,
   `docs/roadmap/STATUS.md` or `docs/roadmap/features/T5_F265.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch
   deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees, their branches, the reviewer's worktrees
   `.remedy-wt/f265-r2-dry` and `.remedy-wt/f265-r2-sim`, and every existing stash alone. The
   worktree G5 adds goes under `.remedy-wt/`, is removed as that step's last action, and
   `git worktree list` is reported afterwards (finding R-0940).
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F265's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f265-r2-*` copy byte for byte
 with its source (the block copy against `.remedy-wt/f265-r2-block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, which its simulation printed from a tree it built by applying these
 payloads at `e7d1e080`:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 307322 | e48a3398c51f5d60f43f8d68b8cf283ee7086bd3d50dbc04fde20730a1c42dec |
 | .agent/decisions.md | 1963597 | d275e94caa8eb3c30d8d5201f0fe396c3db734142e7c594c50b1cba8db12c958 |
 | .agent/plan.md | 1367 | da7d4f209321b826b1da9e7c6b3b245e76c2376a07b60550c991af660951b564 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `e7d1e080` and at C2, with the set
 difference in both directions (the reviewer read 4 at both — R-0499, R-0950, R-1008 and
 R-1046 — both differences empty); the lines C2's diff adds to `.agent/live_review.md` that
 begin `Gate: F265 R1 — `, which must number 1; and `git diff --name-only <C1b> <C2>`, which
 must name exactly `.agent/decisions.md`, `.agent/live_review.md` and `.agent/plan.md`.

G3 THE PRODUCT AND THE TESTS — at C4, the sha256 of each file below, read with
 `git show <C4>:<path>`, equals the reviewer's simulated reading:
 | path | bytes | sha256 |
 |---|---|---|
 | packages/orchestration/lessons.py | 19241 | e8bda9df8331bb95c0e5fb4cd65ee0468e8e52c9141da43a11d00b9e91d7d563 |
 | packages/orchestration/pingpong_job.py | 203409 | 067022fc47ed5ddc7e17c8ecef6eace6acbf48172ebddaa2895dff777259181a |
 | packages/orchestration/ui_server.py | 153608 | 1f78166ce14ae142c553ff6b7260329fed9f5adfe94588cb91e4cab2556a222d |
 | packages/orchestration/event_names.py | 8865 | 818868e1007391b44d84cd0e44635f98b90e09aca12d7f1a18734a4c11a7a64d |
 | apps/ui/src/api/humanizeCatalog.ts | 6830 | 230f14ff6d7835350bc1d07716853adb97b5731558235f54927d94e564492670 |
 | tests/orchestration/test_lessons.py | 18722 | b0a0a43de02fa1e77a065646d0b8a1d45af066bc2bf6c81789c5a9680bdaeb6a |
 | tests/ui_server/test_lessons_route.py | 5489 | b40bff157d2bc281b259676185d30811c2d46fcfa8f4a9494a68abb36106895c |
 Also `git diff --name-only <C2> <C3>` and `<C3> <C4>`, which must name exactly the paths C3
 and C4 list.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash .remedy-wt/f265-r2-scratch/g4.sh /home/decodeux/Repos/remedy
```
 The script runs one pytest selection (the lesson and lessons-route tests, the event-name and
 humanize-catalog guards, the stream, route-walk and command-channel tests, the teacher, ratchet,
 guard and reachability tests, the end-to-end job test, the mission test F264 wrote,
 `tests/docs/`, the state-file readers and `tests/cli/test_golden_path.py`), then `ruff check`
 over the touched Python files, then `python3 -m apps.cli.main integrity check --json`, each
 followed by its real exit code. The reviewer ran the same script inside its sim worktree
 carrying C1a to C4 and read `940 passed, 2 skipped` at pytest exit 0, ruff at exit 0, and all six integrity checks `pass` at
 `fail_count` 0 with `handlers=150`; the primary checkout carries the UI toolchain a
 worktree lacks, so a skip may pass there, and `tests/ui_server/test_dashboard_contract.py`
 then also compiles `apps/ui` with `tsc`. Report the three readings you get: the pytest
 summary line and exit code, ruff's exit code, and whether all six integrity checks read
 `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f265-r2-mut <C4>`, then
 `python3 -B .remedy-wt/f265-r2-payloads/mutations.py .remedy-wt/f265-r2-mut` and report its
 whole output. The script asserts each FROM occurs exactly once, applies it, runs
 `tests/orchestration/test_lessons.py` and `tests/ui_server/test_lessons_route.py` under
 `python3 -B`, restores the bytes, and runs an unmutated control first and last. The reviewer
 read, over the same script against its sim tree carrying C1a to C4:
 control_before `36 passed` at exit 0;
 m1 (a stored lesson is never announced) 1 failed at exit 1;
 m2 (a lesson the Run already had is announced again) 1 failed at exit 1;
 m3 (the hook drops the job's mission) 1 failed at exit 1;
 m4 (the stream carries no `lesson` field) 1 failed at exit 1;
 m5 (the stream passes any status through) 1 failed at exit 1;
 m6 (the lessons route is not served) 3 failed at exit 1;
 m7 (a tampered lesson breaks the index) 1 failed at exit 1;
 m8 (the index never says lessons are off) 1 failed at exit 1;
 m9 (a task that never ran is looked up) 1 failed at exit 1;
 control_after `36 passed` at exit 0; every `restored byte-identical` line True.
 Then `git worktree remove --force .remedy-wt/f265-r2-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 7`, which must show C5, C4, C3, C2, C1b, C1a and `e7d1e080` in that
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
section reads SESSION 1 of feature F265, round 2, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 2, then T002 — the overlay, an index on the left and the lesson with next and previous,
reading the lessons route when the stream announces one. State the open-findings count, 4, and
the operator-questions count, 1.
