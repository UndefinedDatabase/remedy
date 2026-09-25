STEP F023 R8 — THE CLOSURE SEQUENCE'S FIRST HALF: BOOK ROUND 7, WRITE THE BUILT STATE AND THE LAST ASSUMPTION ROW, CONSOLIDATE THE CHECKLIST, RECORD THE SELF-USE TRACK AND RUN THE ONE FULL SUITE

GOAL
Book round 7's PASS; append the Built State to `docs/roadmap/features/T5_F023.md` and F023's third
row to `docs/ui/design_reference/assumption_log.md`; run the checklist consolidation pass, which
joins nothing and keeps `docs/agents/planner_reviewer_prompt.md` §3 at 34 items; record the
self-use track's answer, NONE; and run this feature's ONE full suite, committing its transcript.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. This round closes nothing: the evidence job, the review
package, the ledger rotation, the STATUS line and the pull request belong to later rounds.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f023-r8-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f023-r8/`           READ-ONLY. The reviewer's block and scripts.
  `.remedy-wt/f023-r8-sim/`       The reviewer's simulated tree; do not touch.
  `.remedy-wt/f023-r8-dry/`       The reviewer's authoring tree; do not touch.
  `.remedy-wt/f023-r8-worker/`    YOURS for scripts; create it if it is absent. All are
                                  gitignored. The full suite's log goes OUTSIDE the repository,
                                  to `/home/decodeux/remedy-gate-scratch/f023-full-suite.txt`.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, `ln`, `npm ci`, `npm install`, process substitution, command
substitution, `cd <dir> && git ...`, and multi-operation one-liners chained with `;` or `&&`
outside a `bash -c`. Capture real exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read
`${PIPESTATUS[0]}` when you pipe. Use `git -C <path>` rather than `cd`. Use `python3 - <<'PY'` for
counting, hashing and copying (`shutil.copyfile`). A heredoc containing a dollar-brace or an
f-string brace is refused: write such a script to a file under your own directory and run the
file. The `remedy` CLI may be denied: run `python3 -m apps.cli.main ...`. Never use `git stash`
in any form. Never `pkill -f`.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`: report `pwd` and use
   absolute paths or `git -C /home/decodeux/Repos/remedy` throughout. `git status --porcelain`
   must be empty, `git branch --show-current` must read
   `feature/f023-semantic-zoom-l0-l3`, and `git log --oneline -1` must read `967fc710`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f023-r8/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f023-r8-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every reading.
Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| plan.md | 31 | 1090 | e57e067bbe147b03db8930469d98eb20ee270e1245b18d1fcb7016bb0d268a38 |
| product.diff | 105 | 9750 | 6d1b0dc42365f3266d563e7455eab2b86706c494708fa621b6c137768956f0ef |
| records.diff | 10 | 6762 | 26f6879985c7680ea3b5ece3a9ff3aa3070ec0e7186c2d126ca3c18fb5dbdb79 |
| selfuse.py | 16 | 755 | abcec8f8aa1c9b2add1c379d7a60bd9b935e205587bf55328f38332a64b28245 |
| selfuse_result.txt | 6 | 274 | 8fb9a4f9f881101afdc83b6e85af5f522040a4928ffb92522e914c448b3077bf |

`plan.md` is a REWRITE of `.agent/plan.md`, copied whole. The `.diff` files go on with `git apply`;
the reviewer generated both with `git diff HEAD` from a tree at `967fc710`. `records.diff` appends
the `Gate: F023 R7 —` entry to `.agent/live_review.md`. `product.diff` appends the Built State to
`docs/roadmap/features/T5_F023.md`, adds the consolidation paragraph to
`docs/agents/planner_reviewer_prompt.md`, and appends one row to
`docs/ui/design_reference/assumption_log.md`. `selfuse_result.txt` becomes the NEW FILE at
`.agent/selfuse_f023/result.txt`, copied only after C4's readings equal it. `selfuse.py` is a TOOL
for C4, run from the payload directory and never applied.

BUNDLE — the commits are C1, C2, C3, C4 and C5, in this order.

C1 — copy this block and every payload: `.agent/authored/f023-r8-block.md` := this block, and one
  `.agent/authored/f023-r8-<name>` for each payload, keeping its own file name. All by
  `shutil.copyfile`.
  Subject: `F023 R8 C1: copy round 8 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 168. Report the number you measure and STOP
  rather than commit if it is 500 or more.
C2 — THE RECORDS, in ONE commit (amend0917-throughput rule 4): `git apply` records.diff, then
  rewrite `.agent/plan.md` := plan.md.
  Subject: `F023 R8 C2: book round 7's PASS and advance the plan to the closure`
  Expected insertions by `git show --numstat`: 2 live_review.md, 9 plan.md.
C3 — THE BUILT STATE, THE ASSUMPTION ROWS AND THE CONSOLIDATION: `git apply` product.diff.
  Subject: `F023 R8 C3: write the Built State, log the last assumption, consolidate the checklist`
  Expected insertions: 3 planner_reviewer_prompt.md, 74 T5_F023.md, 1 assumption_log.md.
C4 — THE SELF-USE TRACK (closure precondition 6): run
  `python3 .remedy-wt/f023-r8-payloads/selfuse.py /home/decodeux/Repos/remedy` in the primary
  checkout. It prints `next_self_use_item()`, then `generate_and_append_if_empty()`, then
  `next_self_use_item()` again, then `git status --porcelain`. The reviewer read `None`, `None`,
  `None` and `''` over its simulated tree at C3. If all four readings are those, create
  `.agent/selfuse_f023/` and copy selfuse_result.txt to `.agent/selfuse_f023/result.txt` by
  `shutil.copyfile`, then commit it. If ANY reading differs — the generator returns an item, or the
  queue file changes — STOP under constraint 4: commit nothing for C4, and report the readings
  verbatim.
  Subject: `F023 R8 C4: record the closure's self-use track, NONE`
  Expected insertions: 6.
C5 — THE INTEGRATION GATE AND THE HANDBACK, in the PRIMARY checkout, after C4:
  (a) Build the UI first, because a cold or stale `apps/ui/dist` reddens `tests/ui_server/` under
      `-n`: `bash -c 'npm --prefix apps/ui run build 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'`.
      A refused or failing build is a STOP under constraint 4. Then `git status --porcelain`,
      which must still be empty.
  (b) `python3 -m pytest -n auto -q`, its output written to
      `/home/decodeux/remedy-gate-scratch/f023-full-suite.txt` while it runs, and its wall time
      measured. Write `.agent/authored/f023-closure-suite.txt` holding the command, the real exit
      code, the wall time, the summary line and the FULL list of bad node ids (failed plus errors),
      or the literal `NONE`.
  (c) Rewrite `.agent/handoff.md` per `docs/agents/handback_template.md`, and commit it TOGETHER
      with the transcript.
  Subject: `F023 R8 C5: record the closure suite transcript and rewrite handoff for round 8`
  Then `git push origin feature/f023-semantic-zoom-l0-l3` and report its real outcome.
  Do NOT create a pull request.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1.
3. The round's whole tracked path set is: the `.agent/authored/f023-r8-*` copies,
   `.agent/live_review.md`, `.agent/plan.md`, `docs/agents/planner_reviewer_prompt.md`,
   `docs/roadmap/features/T5_F023.md`, `docs/ui/design_reference/assumption_log.md`,
   `.agent/selfuse_f023/result.txt`, `.agent/authored/f023-closure-suite.txt` and
   `.agent/handoff.md`. Report the list you measure with `git diff --name-only 967fc710` over the
   range to C5. Nothing under `packages/`, `apps/`, `tests/` or `scripts/`, and no edit to
   `README.md`, `docs/roadmap/STATUS.md`, `scripts/self_use_queue.json`, `.agent/decisions.md`,
   `.agent/prose_slips.md`, `.agent/candidates.md` or `.agent/operator_questions.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. THE ONE
   EXCEPTION is the full suite in C5: a red suite is this feature's work and not a stop — commit
   its transcript exactly as measured, report every bad node id, and hand back. Never weaken an
   assertion, delete a test or mark anything xfail on your own initiative.
5. NOTHING IS MERGED, NOTHING IS CLOSED. No `gh pr merge`, no `gh pr create`, no checkout of
   `main`, no branch deletion, no force-push, no STATUS edit, no evidence job, no review package.
6. Leave the `.remedy-wt/job-*` worktrees, their branches, every reviewer worktree whose name
   begins `.remedy-wt/f015-`, `.remedy-wt/f020-`, `.remedy-wt/f023-` or `.remedy-wt/f284-`, every local branch, and
   every stash alone.
7. The full suite runs ONCE, in C5, and nowhere else this round (amend0917 rule 1).

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G4 run before C5 is written, and G5
is the suite C5 runs.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f023-r8-*` copy byte for byte with
 its source (the block copy against `.remedy-wt/f023-r8/block.md`), read back with
 `git show <C1>:<path>`. Report one reading per copy.

G2 THE RECORDS, THE BUILT STATE AND THE CONSOLIDATION — the sha256 of each file below, read with
 `git show <commit>:<path>` at the commit named, equals the reviewer's reading, which its builder
 printed from a tree it built by applying these payloads at `967fc710`:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/live_review.md | 309561 | b5667d1a35fe0c4e6f5419195a54219e82052e138ebb1f4ea7c1370d1eb9a25b |
 | C2 | .agent/plan.md | 1090 | e57e067bbe147b03db8930469d98eb20ee270e1245b18d1fcb7016bb0d268a38 |
 | C3 | docs/agents/planner_reviewer_prompt.md | 101681 | 0d4c9a0072d983bfadc4e173ed43b33392a0ed866d099179f3903733d642921a |
 | C3 | docs/roadmap/features/T5_F023.md | 11017 | 5e0b8983827aaf3863a9856bb3ccb26fa064b7246200248a79de34c7574b33af |
 | C3 | docs/ui/design_reference/assumption_log.md | 8405 | 08e60ca07b47eabf4577a708316b587c8ab800f06b1f9c7dda1cb9f50b63f44e |
 | C4 | .agent/selfuse_f023/result.txt | 274 | 8fb9a4f9f881101afdc83b6e85af5f522040a4928ffb92522e914c448b3077bf |
 Also: among the lines C2's diff ADDS to `.agent/live_review.md`, the count of those beginning
 `Gate: F023 R7 — ` (the reviewer's builder read 1); the open set by distinct id, computed with
 `open_finding_ids` from `scripts/rotate_live_review.py` over the file's TEXT, at `967fc710` and at
 C2 (the reviewer read R-1008 alone at both); and the checklist's item numbers, computed with
 `live_checklist_items` of `packages/orchestration/block_lint.py` over
 `docs/agents/planner_reviewer_prompt.md` at `967fc710` and at C3, which must be the same 34
 numbers at both.

G3 THE LINTER ON THIS BLOCK — at C4, in the primary checkout:
 `python3 -m apps.cli.main integrity block .remedy-wt/f023-r8/block.md`, real exit code 0, every
 item `[OK]`. Report the whole output.

G4 THE TESTS AND THE TREE — in the primary checkout at C4, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_advertised_commands.py tests/orchestration/test_block_lint.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_roadmap_index.py tests/ui_contracts tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same command WITHOUT the golden path, serially, inside its simulated tree at
 C3 and read `1399 passed, 8 skipped` at real exit code 0; your tree adds the golden path, and the
 primary checkout's toolchain runs the two eslint nodes of `tests/ui_contracts/test_ui_lint.py`
 that skip in a worktree. Then C4's four readings verbatim; then
 `python3 -m apps.cli.main integrity check --json`, all six checks `pass` at `fail_count` 0; and
 `git status --porcelain` empty with no untracked file (closure precondition 3).

G5 THE INTEGRATION GATE — the UI build's last line and real exit code, `git status --porcelain`
 after it, then the full suite's real exit code, its wall time, its summary line and every bad
 node id, all of it in `.agent/authored/f023-closure-suite.txt`. Report whether
 `tests/orchestration/test_import_reachability.py` or `tests/test_no_orphan_modules.py` holds a
 bad node (closure precondition 7).

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 6`, which must show C5, C4, C3, C2, C1 and `967fc710` in that order;
 `git worktree list`, which must show the primary checkout and only worktrees constraint 6 names;
 the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the insertion count you MEASURED beside the one this block
expected, every gate's real output and exit code, the self-use readings, the full suite's summary
line and bad node ids, the authored-text proofs, the item-status table AGENTS.md requires (one row
per commit and per gate), the deviations, and the next expected action. Report what you ran, not
what you expected to find. Your Session section reads SESSION 1 of feature F023, round 8, and says
in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round
8, then the closure's second half — the booking of round 8, any repair the suite requires, the
evidence job and the review package — and then the closing round. State the open-findings count,
1, and the operator-questions count, 3.
