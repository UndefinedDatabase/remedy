STEP F015 R5 — THE CLOSURE SEQUENCE'S FIRST HALF: BOOK ROUND 4, WRITE THE BUILT STATE, CONSOLIDATE THE CHECKLIST, RECORD THE SELF-USE TRACK AND RUN THE ONE FULL SUITE

GOAL
Book round 4's PASS; append the Built State to `docs/roadmap/features/T5_F015.md`; run the
checklist consolidation pass, which joins nothing and keeps `docs/agents/planner_reviewer_prompt.md`
§3 at 34 items; record the self-use track's answer, NONE; and run this feature's ONE full suite,
committing its transcript.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. This round closes nothing: the evidence job, the review
package, the ledger rotation, the STATUS line and the pull request belong to later rounds.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f015-r5-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f015-r5-scratch/`   The reviewer's scripts; do not edit or delete them.
  `.remedy-wt/f015-r5-worker/`    YOURS for logs and scripts; create it if it is absent. All
                                  three are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, `ln`, `npm ci`, `npm install`, process substitution,
`cd <dir> && git ...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`.
Capture real exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when
you pipe. Use `git -C <path>` rather than `cd`. Use `python3 - <<'PY'` for counting, hashing and
copying (`shutil.copyfile`). A heredoc containing a dollar-brace is refused: write such a script to a
file under your own directory and run the file. The `remedy` CLI may be denied: run
`python3 -m apps.cli.main ...`. Never use `git stash` in any form.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`: report `pwd` and use
   absolute paths or `git -C /home/decodeux/Repos/remedy` throughout. `git status --porcelain`
   must be empty, `git branch --show-current` must read `feature/f015-interactive-plan-editing`,
   and `git log --oneline -1` must read `4f010387`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f015-r5-block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f015-r5-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every reading.
Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 10 | 6733 | eb0df49ed893ed9f87e76386ae9833cd69cdadbd8cc169ab566c9a8b00534991 |
| product.diff | 101 | 7393 | 994ff0b544c9665b342a79365d700c4d855550e5d21c2cbc8f6c812f17fca0c3 |
| plan.md | 30 | 1103 | 2a865cc1bb7ebd19dfca7eb2960789de3a40ae4f7b4da2e842ed720e2e217b64 |
| selfuse_result.txt | 6 | 274 | 33f164f3e927c00ccd5d6573d0255ccdd9b78415a058d4f36c69351de7b334e0 |

`plan.md` is a REWRITE of `.agent/plan.md`, copied whole. The `.diff` files go on with `git apply`;
the reviewer generated both from a tree at `4f010387` and applied them, in the commit order below,
to a fresh detached worktree at `4f010387` with `git apply --check` then `git apply`, each at real
exit code 0. `records.diff` appends the `Gate: F015 R4 —` entry to `.agent/live_review.md`.
`product.diff` edits `docs/roadmap/features/T5_F015.md` (the Built State) and
`docs/agents/planner_reviewer_prompt.md` (the consolidation paragraph). `selfuse_result.txt` becomes
the NEW FILE `.agent/selfuse_f015/result.txt`, copied only after C4's readings equal it.

BUNDLE — the commits are C1, C2, C3, C4 and C5, in this order.

C1 — copy this block and every payload: `.agent/authored/f015-r5-block.md` := this block, and one
  `.agent/authored/f015-r5-<name>` for each payload, keeping its own file name. All by
  `shutil.copyfile`.
  Subject: `F015 R5 C1: copy round 5 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 147. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C2 — THE RECORDS, in ONE commit (amend0917-throughput rule 4):
   1. `git apply` records.diff  → `.agent/live_review.md`
   2. rewrite `.agent/plan.md` := plan.md
  Subject: `F015 R5 C2: book round 4's PASS and advance the plan to the closure`
  Expected insertions by `git show --numstat`: 2 live_review.md, 7 plan.md.

C3 — THE BUILT STATE AND THE CONSOLIDATION: `git apply` product.diff, then `git add` its two paths.
  Subject: `F015 R5 C3: write the Built State and consolidate the checklist`
  Expected insertions: 5 planner_reviewer_prompt.md, 77 T5_F015.md.

C4 — THE SELF-USE TRACK (closure precondition 6): run
  `python3 .remedy-wt/f015-r5-scratch/selfuse.py /home/decodeux/Repos/remedy` in the primary
  checkout. It prints `next_self_use_item()`, then `generate_and_append_if_empty()`, then
  `next_self_use_item()` again, then `git status --porcelain`. The reviewer read `None`, `None`,
  `None` and `''` over its own tree built at `4f010387` with this round's C1 to C3. If all four
  readings are those, create `.agent/selfuse_f015/` and copy selfuse_result.txt to
  `.agent/selfuse_f015/result.txt` by `shutil.copyfile`, then commit it. If ANY reading differs —
  the generator returns an item, or the queue file changes — STOP under constraint 4: commit
  nothing for C4, and report the readings verbatim.
  Subject: `F015 R5 C4: record the closure's self-use track, NONE`
  Expected insertions: 6.

C5 — THE INTEGRATION GATE AND THE HANDBACK, in the PRIMARY checkout, after C4:
  (a) Build the UI first, because a cold or stale `apps/ui/dist` reddens `tests/ui_server/` under
      `-n`: `bash -c 'npm --prefix apps/ui run build 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'`.
      A refused or failing build is a STOP under constraint 4. Then `git status --porcelain`,
      which must still be empty.
  (b) `python3 -m pytest -n auto -q`, its log written to `.remedy-wt/f015-r5-worker/full-suite.log`.
      Write `.agent/authored/f015-closure-suite.txt` holding the command, the real exit code, the
      summary line and the FULL list of bad node ids (failed plus errors), or the literal `NONE`.
  (c) Rewrite `.agent/handoff.md` per `docs/agents/handback_template.md`, and commit it TOGETHER
      with the transcript.
  Subject: `F015 R5 C5: record the closure suite transcript and rewrite handoff for round 5`
  Then `git push origin feature/f015-interactive-plan-editing` and report its real outcome. Do
  NOT create a pull request.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1.
3. The round's whole tracked path set is: the `.agent/authored/f015-r5-*` copies,
   `.agent/live_review.md`, `.agent/plan.md`, `docs/agents/planner_reviewer_prompt.md`,
   `docs/roadmap/features/T5_F015.md`, `.agent/selfuse_f015/result.txt`,
   `.agent/authored/f015-closure-suite.txt` and `.agent/handoff.md`. Report the list you measure
   with `git diff --name-only 4f010387` over the range to C5. Nothing under `packages/`, `apps/`,
   `tests/` or `scripts/`, and no edit to `README.md`, `docs/roadmap/STATUS.md`,
   `scripts/self_use_queue.json`, `.agent/decisions.md`, `.agent/prose_slips.md`,
   `.agent/candidates.md` or `.agent/operator_questions.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. THE ONE
   EXCEPTION is the full suite in C5: a red suite is this feature's work and not a stop — commit
   its transcript exactly as measured, report every bad node id, and hand back. Never weaken an
   assertion, delete a test or mark anything xfail on your own initiative.
5. NOTHING IS MERGED, NOTHING IS CLOSED. No `gh pr merge`, no `gh pr create`, no checkout of
   `main`, no branch deletion, no force-push, no STATUS edit, no evidence job, no review package.
6. Leave the `.remedy-wt/job-*` worktrees, their branches, the reviewer's worktrees whose names
   begin `.remedy-wt/f015-`, the local branch `sim/f267-r1`, and every existing stash alone.
7. The full suite runs ONCE, in C5, and nowhere else this round (amend0917 rule 1).

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G4 run before C5 is written, and G5
is the suite C5 runs.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f015-r5-*` copy byte for byte with
 its source (the block copy against `.remedy-wt/f015-r5-block.md`), read back with
 `git show <C1>:<path>`. Report one reading per copy.

G2 THE RECORDS, THE BUILT STATE AND THE CONSOLIDATION — the sha256 of each file below, read with
 `git show <commit>:<path>` at the commit named, equals the reviewer's reading, which its
 simulation printed from a tree it built by applying these payloads at `4f010387`:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/live_review.md | 300463 | 93cd3f684d7f65b5d956f48199928c42f355aab541e9dde915638e3a287928e9 |
 | C2 | .agent/plan.md | 1103 | 2a865cc1bb7ebd19dfca7eb2960789de3a40ae4f7b4da2e842ed720e2e217b64 |
 | C3 | docs/agents/planner_reviewer_prompt.md | 100544 | 58dc1930bbee1944c4f178db99a610fa22b1bdead2ec66071686771c810f3d4e |
 | C3 | docs/roadmap/features/T5_F015.md | 10859 | aa4cba6c70e14f3db9cd3eab4d69e17665b70b6c97be7ce186908220ba6f469a |
 | C4 | .agent/selfuse_f015/result.txt | 274 | 33f164f3e927c00ccd5d6573d0255ccdd9b78415a058d4f36c69351de7b334e0 |
 Also: among the lines C2's diff ADDS to `.agent/live_review.md`, the count of those beginning
 `Gate: F015 R4 — ` (the reviewer's simulation read 1); the open set by distinct id, computed with
 `open_finding_ids` from `scripts/rotate_live_review.py` over the file's TEXT, at `4f010387` and at
 C2, with the set difference in both directions (the reviewer read 4 and 4 — R-0499, R-0950,
 R-1008 and R-1046 — both differences empty); the checklist's item numbers, computed with
 `live_checklist_items` of `packages/orchestration/block_lint.py` over
 `docs/agents/planner_reviewer_prompt.md` at `4f010387` and at C3 (the reviewer read the same 34
 numbers at both); and `git diff --name-only` between consecutive commits from C1 to C4, which must
 name exactly the paths each commit lists.

G3 THE LINTER ON THIS BLOCK — at C4, in the primary checkout:
 `python3 -m apps.cli.main integrity block .remedy-wt/f015-r5-block.md`, real exit code 0,
 every item `[OK]`. Report the whole output.

G4 THE TESTS AND THE TREE — in the primary checkout at C4, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_advertised_commands.py tests/orchestration/test_block_lint.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_roadmap_index.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same command, serially, inside its simulation tree at the C4 it built and
 read `534 passed, 1 skipped` at real exit code 0; your tree carries the block copy the simulation lacked,
 which a test parametrized over the saved blocks may count once more. Then C4's four readings
 verbatim; then `python3 -m apps.cli.main integrity check --json`, all six checks `pass` at
 `fail_count` 0; and `git status --porcelain` empty with no untracked file (closure
 precondition 3).

G5 THE INTEGRATION GATE — the UI build's last line and real exit code, `git status --porcelain`
 after it, then the full suite's real exit code, its summary line and every bad node id, all of it
 in `.agent/authored/f015-closure-suite.txt`. Report whether
 `tests/orchestration/test_import_reachability.py` or `tests/test_no_orphan_modules.py` holds a
 bad node (closure precondition 7).

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 6`, which must show C5, C4, C3, C2, C1 and `4f010387` in that order;
 `git worktree list`, which must show the primary checkout and exactly the worktrees constraint 6
 names; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state block,
the per-commit changed-files table with the insertion count you MEASURED beside the one this block
expected, every gate's real output and exit code, the self-use readings, the full suite's summary
line and bad node ids, the authored-text proofs, the item-status table AGENTS.md requires (one row
per commit and per gate), the deviations, and the next expected action. Report what you ran, not
what you expected to find. Your Session section reads SESSION 1 of feature F015, round 5, and says
in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round
5, then the closure's second half — the booking of round 5, any repair the suite requires, the
evidence job and the review package — and then the closing round. State the open-findings count,
4, and the operator-questions count, 1.
