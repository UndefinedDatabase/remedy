STEP F265 R3 — T002: THE LEARNING OVERLAY over the stored lessons

GOAL
Book round 2's PASS, record DECISION F265 D3, and land T002: a right-anchored dialog sheet the
right panel's "Lessons" button opens, with the index of the job's lessons on the left and the
chosen lesson on the right with previous and next; it reads the lessons route through one pure
module, reads it again only when the stream announces a lesson, and generates nothing. Vitest
covers the pure module, a contract test pins it to the server, and two assumption-log rows
record what the design reference does not settle.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge.

WHY THIS IS NEXT
T5_F265.md's Orchestrator brief: T002 is pure rendering over stored artifacts and is safe to
build once the artifact's shape is settled, which rounds 1 and 2 did. DECISION F265 D3 (in
records.diff) fixes the sheet, its entry point, its refresh and its pins. T003, the Commands
mode, is next round's work.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f265-r3-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f265-r3-scratch/`   The reviewer's scripts; do not edit or delete them.
  `.remedy-wt/f265-r3-worker/`    YOURS for logs and scripts. All three are gitignored.
  `mutations.py` writes its vitest config and cache under `.remedy-wt/f265-r3-mutcfg/`.

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
   `feature/f265-teacher-learning-ui`, and `git log --oneline -1` must read `b09b36f4`. Report
   all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f265-r3-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f265-r3-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 62 | 9243 | 1dd9793d5f78501bf1320a339025c07aed0f199992b17a8ddf733a7b40e6e0de |
| plan.md | 33 | 1312 | ba3cd55a666b49de0dcc18c956b3b7283b04bf22c8c530bf68d4b1efa6b1bc8b |
| api.diff | 39 | 2151 | 4168fc0f6f080899da7c409eadd80bcf9ef2bb545938de309bfbe0bbdb89c192 |
| shell.diff | 88 | 8184 | 0601554f9be7599e5081a839dc06a898fd361de2c592a96aa775266183b7e3db |
| lessons.ts | 163 | 7434 | 488bf40891731094a7c8dbd93935258c943fb55049d5f12ed3c76f600486bb02 |
| LessonsOverlay.tsx | 137 | 5707 | e66077da500cc0ad2a745a75a7f0c9cd573922534e0f89a91b89ad5b25cd4bef |
| LessonsOverlay.module.css | 97 | 3844 | 7d358546eb4f93ebcd8686df0e03f46c3b7c30ce2c028da57353bfb5cf2f424a |
| lessons.test.ts | 135 | 5960 | 09c8eafc5039bac9abb159162a4d4d5546f5ad5bc596fc299c859c4811bebea2 |
| test_lessons_overlay_contract.py | 95 | 4038 | 734dc96a1d0f5ec9a1c28b54b02a5f238b8aa40f75527968b7a8e723d383944c |
| mutations.py | 84 | 4296 | 871a259a3e65bf761a56588b5cd8076bde6dba302d83ea5daad8f591b89ff204 |

`plan.md` is a REWRITE of `.agent/plan.md`. The NEW FILES, each copied whole: `lessons.ts` to
`apps/ui/src/api/lessons.ts`, `LessonsOverlay.tsx` and `LessonsOverlay.module.css` to
`apps/ui/src/components/lessons/`, `lessons.test.ts` to `apps/ui/src/api/lessons.test.ts`, and
`test_lessons_overlay_contract.py` to `tests/ui_contracts/test_lessons_overlay_contract.py`. The
`.diff` files go on with `git apply`; the reviewer generated each from a tree at `b09b36f4` and
applied them, in the commit order below, to a fresh worktree at `b09b36f4` with
`git apply --check` then `git apply`, every one at real exit code 0. `records.diff` appends the
round 2 gate entry to `.agent/live_review.md` and DECISION F265 D3 to `.agent/decisions.md`.
`api.diff` edits `apps/ui/src/api/remedyApi.ts`. `shell.diff` edits
`apps/ui/src/components/shell/RemedyShell.tsx`,
`apps/ui/src/components/panels/RightLivePanel.tsx` and
`docs/ui/design_reference/assumption_log.md`. `mutations.py` is a TOOL for G5: it is run,
never applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C1c, C2, C3, C4 and C5, in this order.

C1a — copy this block and the record payloads
  `.agent/authored/f265-r3-block.md` := this block, and `.agent/authored/f265-r3-plan.md` and
  `.agent/authored/f265-r3-records.diff` := plan.md and records.diff. All by `shutil.copyfile`.
  Subject: `F265 R3 C1a: copy round 3 block and record payloads into .agent/authored/`
  Its insertions are this block's line count plus 95. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C1b — copy the two diffs, the pure module and the mutation tool
  `.agent/authored/f265-r3-<name>` for each of api.diff, shell.diff, lessons.ts and
  mutations.py.
  Subject: `F265 R3 C1b: copy round 3 diffs, pure module and mutation tool into .agent/authored/`
  Expected insertions: 374.

C1c — copy the component and the tests
  `.agent/authored/f265-r3-<name>` for each of LessonsOverlay.tsx, LessonsOverlay.module.css,
  lessons.test.ts and test_lessons_overlay_contract.py.
  Subject: `F265 R3 C1c: copy round 3 component and tests into .agent/authored/`
  Expected insertions: 464.

C2 — THE RECORDS, in this order:
   1. `git apply` records.diff
   2. rewrite `.agent/plan.md` := plan.md
  Subject: `F265 R3 C2: book round 2's PASS, record DECISION F265 D3`
  Expected insertions by `git show --numstat`: 44 decisions.md, 2 live_review.md, 11 plan.md.

C3 — THE OVERLAY: copy lessons.ts, LessonsOverlay.tsx and LessonsOverlay.module.css to their
  paths, `git apply` api.diff, `git apply` shell.diff, and `git add` every path this commit
  writes.
  Subject: `F265 R3 C3: the learning overlay over the job's stored lessons`
  Expected insertions: 163 lessons.ts, 24 remedyApi.ts, 97 LessonsOverlay.module.css, 137 LessonsOverlay.tsx, 8 RightLivePanel.tsx, 18 RemedyShell.tsx, 2 assumption_log.md.

C4 — THE TESTS: copy lessons.test.ts and test_lessons_overlay_contract.py to their paths and
  `git add` both.
  Subject: `F265 R3 C4: test the overlay's rules and pin it to the lessons route`
  Expected insertions: 135 lessons.test.ts, 95 test_lessons_overlay_contract.py.

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F265 R3 C5: rewrite handoff for round 3`
  Then `git push origin feature/f265-teacher-learning-ui`. Do NOT create a pull request.
  Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f265-r3-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, the new files listed under
   PAYLOADS, every path api.diff and shell.diff edit, and `.agent/handoff.md`. Report the list
   you measure with `git diff --name-only b09b36f4 HEAD` after C5. Do NOT touch
   `.agent/context.md`, `.agent/prose_slips.md`, `.agent/candidates.md`,
   `.agent/operator_questions.md`, `README.md`, `docs/roadmap/STATUS.md` or
   `docs/roadmap/features/T5_F265.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch
   deletion, no force-push, no `git stash`.
6. Leave the `.remedy-wt/job-*` worktrees, their branches, the reviewer's worktrees
   `.remedy-wt/f265-r3-dry` and `.remedy-wt/f265-r3-sim`, and every existing stash alone. The
   worktree G5 adds goes under `.remedy-wt/`, is removed as that step's last action, and
   `git worktree list` is reported afterwards (finding R-0940).
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F265's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f265-r3-*` copy byte for byte
 with its source (the block copy against `.remedy-wt/f265-r3-block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE RECORDS — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, which its simulation printed from a tree it built by applying these
 payloads at `b09b36f4`:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 309498 | 81378a6dc695c5fa2d06d4e3105d7fae40422e954c338b14c129705f16890381 |
 | .agent/decisions.md | 1967387 | ec27976fa9d78a55ca667ec6dc8fb1d19a6f43322481cac8457c1c6ee544df2a |
 | .agent/plan.md | 1312 | ba3cd55a666b49de0dcc18c956b3b7283b04bf22c8c530bf68d4b1efa6b1bc8b |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `b09b36f4` and at C2, with the set
 difference in both directions (the reviewer read 4 at both — R-0499, R-0950, R-1008 and
 R-1046 — both differences empty); the lines C2's diff adds to `.agent/live_review.md` that
 begin `Gate: F265 R2 — `, which must number 1; and `git diff --name-only <C1c> <C2>`, which
 must name exactly `.agent/decisions.md`, `.agent/live_review.md` and `.agent/plan.md`.

G3 THE OVERLAY AND THE TESTS — at C4, the sha256 of each file below, read with
 `git show <C4>:<path>`, equals the reviewer's simulated reading:
 | path | bytes | sha256 |
 |---|---|---|
 | apps/ui/src/api/lessons.ts | 7434 | 488bf40891731094a7c8dbd93935258c943fb55049d5f12ed3c76f600486bb02 |
 | apps/ui/src/components/lessons/LessonsOverlay.tsx | 5707 | e66077da500cc0ad2a745a75a7f0c9cd573922534e0f89a91b89ad5b25cd4bef |
 | apps/ui/src/components/lessons/LessonsOverlay.module.css | 3844 | 7d358546eb4f93ebcd8686df0e03f46c3b7c30ce2c028da57353bfb5cf2f424a |
 | apps/ui/src/api/remedyApi.ts | 38219 | 0f7e995df6eafda042bd021816b1270557e722f9cf24c26fe0704bbcfb523b67 |
 | apps/ui/src/components/shell/RemedyShell.tsx | 12509 | ccc350153e795fb0a8e4b4fe3555d8b9fe5b4737c2eb50378e8fac6181c0f666 |
 | apps/ui/src/components/panels/RightLivePanel.tsx | 3294 | 2ddf248a7790752f3948e9edf2075340e737c093abc4c54bcf46321e771230dd |
 | docs/ui/design_reference/assumption_log.md | 4079 | 276f3a2a7dac5ee608083addfa60be6db166d836efc3afd528e2794b2807c428 |
 | apps/ui/src/api/lessons.test.ts | 5960 | 09c8eafc5039bac9abb159162a4d4d5546f5ad5bc596fc299c859c4811bebea2 |
 | tests/ui_contracts/test_lessons_overlay_contract.py | 4038 | 734dc96a1d0f5ec9a1c28b54b02a5f238b8aa40f75527968b7a8e723d383944c |
 Also `git diff --name-only <C2> <C3>` and `<C3> <C4>`, which must name exactly the paths C3
 and C4 write.

G4 THE TESTS — in the primary checkout at C4, SERIALLY, with real exit codes:
```
bash .remedy-wt/f265-r3-scratch/g4.sh /home/decodeux/Repos/remedy
```
 The script runs one pytest selection with `-rs` (all of `tests/ui_contracts/`, which holds the
 new contract test and `test_ui_lint.py`'s eslint run; `tests/ui_server/test_dashboard_contract.py`,
 whose typescript node compiles `apps/ui`; `tests/orchestration/test_test_runner.py`, whose
 vitest node runs the whole UI suite; the lesson tests, `tests/docs/`, the state-file readers
 and `tests/cli/test_golden_path.py`), then `ruff check` over the new Python test, then
 `python3 -m apps.cli.main integrity check --json`, each followed by its real exit code. The
 reviewer ran the same script inside its sim worktree carrying C1a to C4 and read `1471 passed, 10 skipped` at pytest exit 0, ruff at exit 0, and all six integrity checks
 `pass` at `fail_count` 0; the sim worktree has no `apps/ui/node_modules`, so its eslint,
 typescript and vitest nodes are among its skips, and the reviewer ran those three tools over
 the sim's `apps/ui` sources with the primary's toolchain instead, reading `tsc` exit 0, eslint
 exit 0 over the six changed TypeScript files, and vitest `19 passed` over the new test file;
 in the primary checkout the eslint, typescript and vitest nodes must RUN, so report every
 SKIPPED line the `-rs` output prints and confirm none of those three nodes is among them.
 Report the pytest summary line and exit code, ruff's exit code, and whether all six
 integrity checks read `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f265-r3-mut <C4>`, then
 `python3 -B .remedy-wt/f265-r3-payloads/mutations.py .remedy-wt/f265-r3-mut` and report its
 whole output. For each mutation the script runs vitest over the worktree's
 `apps/ui/src/api/lessons.test.ts` from the primary `apps/ui` and pytest over the worktree's
 contract test, restores the bytes, and runs an unmutated control first and last. The reviewer
 read, over the same script against its sim tree carrying C1a to C4:
 control_before vitest `19 passed` at exit 0 | contract `8 passed` at exit 0;
 m1 (a bad row is dropped instead of refusing the index) vitest 3 failed at exit 1;
 m2 (the overlay opens on the first task) vitest 2 failed at exit 1;
 m3 (next runs past the last lesson) vitest 1 failed at exit 1;
 m4 (any frame refreshes the index) vitest 1 failed at exit 1;
 m5 (the empty line ignores the off switch) vitest 1 failed at exit 1;
 m6 (the door drops the token) vitest 1 failed at exit 1;
 m7 (the decoder reads a key the server never writes) vitest 1 failed at exit 1 | contract
   1 failed at exit 1;
 m8 (a stale answer is painted) vitest 19 passed at exit 0 | contract 1 failed at exit 1;
 m9 (Escape does not close) vitest 19 passed at exit 0 | contract 1 failed at exit 1;
 the half each of m1 to m6 does not name reads `8 passed` at exit 0, the vitest half being the
 one that reaches the pure module's rules;
 control_after as control_before; every `restored byte-identical` line True.
 Then `git worktree remove --force .remedy-wt/f265-r3-mut`, `git worktree prune`, report
 `git worktree list`, and report `git status --porcelain`, which must still be empty.

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 8`, which must show C5, C4, C3, C2, C1c, C1b, C1a and `b09b36f4` in that
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
section reads SESSION 1 of feature F265, round 3, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 3, then T003 — the Commands mode over the catalog entries of the commands the task's diff
touched. State the open-findings count, 4, and the operator-questions count, 1.
