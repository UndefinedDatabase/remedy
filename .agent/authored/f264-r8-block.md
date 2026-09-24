STEP F264 R8 — THE CLOSURE SEQUENCE'S FIRST HALF: BOOK ROUND 7, WRITE THE STEERING GUIDE AND THE BUILT STATE, CONSOLIDATE THE CHECKLIST, RECORD THE SELF-USE TRACK AND RUN THE ONE FULL SUITE

GOAL
Book round 7's PASS; add the operator guide `docs/guides/steering-user-guide-v1.md`, index it in
`docs/README.md`, and correct the sentence in `docs/system/operator-cockpit-v1.md` that says the
cockpit has no text input; append the Built State to `docs/roadmap/features/T5_F264.md`; run the
checklist consolidation pass, which joins nothing and keeps `docs/agents/planner_reviewer_prompt.md`
§3 at 34 items; record the self-use track's answer, NONE; and run this feature's ONE full suite,
committing its transcript.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. This round closes nothing: the evidence job, the review
package, the ledger rotation, the STATUS line and the pull request belong to later rounds.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f264-r8-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f264-r8-scratch/`   The reviewer's scripts; do not edit or delete them.
  `.remedy-wt/f264-r8-worker/`    YOURS for logs and scripts. All three are gitignored.

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
   must be empty, `git branch --show-current` must read `feature/f264-steering-channel`, and
   `git log --oneline -1` must read `d9bea4ba`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f264-r8-block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` as found.

PAYLOADS — under `.remedy-wt/f264-r8-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every reading.
Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 10 | 6182 | f8776d3849c7580a8fd56c13b71eb14fc242b652d92ba7b4ed5e3f7bc59661da |
| plan.md | 30 | 1096 | 3eff73a4b83aadd8abc5711a56f3e0e85f9d2abbe8f4ffc06b2f17d4cfd9356b |
| product.diff | 217 | 13496 | 07e876b88da2d4338d53af51f87ef9f7dd8cb2158204ce6cd3d38281ee25fc89 |
| selfuse_result.txt | 6 | 274 | d9c267009f86518e3be1dad28526b8ba5d6925b64bc3b8f20b9e92ce962b871b |

`plan.md` is a REWRITE of `.agent/plan.md`, copied whole. The `.diff` files go on with `git apply`;
the reviewer generated both from a tree at `d9bea4ba` and applied them, in the commit order below,
to a fresh worktree at `d9bea4ba` with `git apply --check` then `git apply`, each at real exit code
0. `records.diff` appends the `Gate: F264 R7 —` entry to `.agent/live_review.md`. `product.diff`
creates `docs/guides/steering-user-guide-v1.md` and edits `docs/README.md`,
`docs/agents/planner_reviewer_prompt.md`, `docs/roadmap/features/T5_F264.md` and
`docs/system/operator-cockpit-v1.md`. `selfuse_result.txt` becomes the NEW FILE
`.agent/selfuse_f264/result.txt`, copied only after C4's readings equal it.

BUNDLE — the commits are C1, C2, C3, C4 and C5, in this order.

C1 — copy this block and every payload: `.agent/authored/f264-r8-block.md` := this block, and one
  `.agent/authored/f264-r8-<name>` for each payload, keeping its own file name. All by
  `shutil.copyfile`.
  Subject: `F264 R8 C1: copy round 8 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 263. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C2 — THE RECORDS, in ONE commit (amend0917-throughput rule 4):
   1. `git apply` records.diff  → `.agent/live_review.md`
   2. rewrite `.agent/plan.md` := plan.md
  Subject: `F264 R8 C2: book round 7's PASS and advance the plan to the closure`
  Expected by `git show --numstat` (insertions/deletions): 2/0 live_review.md, 8/9 plan.md.

C3 — THE GUIDE, THE BUILT STATE AND THE CONSOLIDATION: `git apply` product.diff, then `git add`
  its five paths, the new guide included.
  Subject: `F264 R8 C3: add the steering guide, write the Built State and consolidate the checklist`
  Expected (insertions/deletions): 2/0 docs/README.md, 6/0 planner_reviewer_prompt.md,
  91/0 steering-user-guide-v1.md, 57/0 T5_F264.md, 5/2 operator-cockpit-v1.md.

C4 — THE SELF-USE TRACK (closure precondition 6), from a scratch Python file you write under your
  directory and run in the primary checkout: print `next_self_use_item()` of
  `packages.orchestration.self_use_queue`, then `generate_and_append_if_empty()` of
  `packages.orchestration.self_use_generator` with no arguments, then `next_self_use_item()` again,
  then `git status --porcelain`. The reviewer read `None`, `None`, `None` and an empty status in its
  own tree built at `d9bea4ba` with this round's edits. If all four readings are those, copy
  selfuse_result.txt to `.agent/selfuse_f264/result.txt` by `shutil.copyfile` and commit it. If ANY
  reading differs — the generator returns an item, or the queue file changes — STOP under
  constraint 4: commit nothing for C4, and report the readings verbatim.
  Subject: `F264 R8 C4: record the closure's self-use track, NONE`
  Expected insertions: 6.

C5 — THE INTEGRATION GATE AND THE HANDBACK, in the PRIMARY checkout, after C4:
  (a) Build the UI first, because a cold or stale `apps/ui/dist` reddens `tests/ui_server/` under
      `-n`, and this feature changed the cockpit in rounds 3 and 7:
      `bash -c 'npm --prefix apps/ui run build 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'`.
      A refused or failing build is a STOP under constraint 4. Then `git status --porcelain`,
      which must still be empty.
  (b) `python3 -m pytest -n auto -q`, its log written to `.remedy-wt/f264-r8-worker/full-suite.log`.
      Write `.agent/authored/f264-closure-suite.txt` holding the summary line, the real exit code
      and the FULL list of bad node ids (failed plus errors), or the literal `NONE`.
  (c) Rewrite `.agent/handoff.md` per `docs/agents/handback_template.md`, and commit it TOGETHER
      with the transcript.
  Subject: `F264 R8 C5: record the closure suite transcript and rewrite handoff for round 8`
  Then `git push origin feature/f264-steering-channel` and report its real outcome. Do NOT
  create a pull request.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1.
3. The round's whole tracked path set is: the `.agent/authored/f264-r8-*` copies,
   `.agent/live_review.md`, `.agent/plan.md`, `docs/README.md`,
   `docs/agents/planner_reviewer_prompt.md`, `docs/guides/steering-user-guide-v1.md`,
   `docs/roadmap/features/T5_F264.md`, `docs/system/operator-cockpit-v1.md`,
   `.agent/selfuse_f264/result.txt`, `.agent/authored/f264-closure-suite.txt` and
   `.agent/handoff.md`. Report the list you measure with `git diff --name-only d9bea4ba HEAD` after
   C5. Nothing under `packages/`, `apps/`, `tests/` or `scripts/`, and no edit to `README.md`,
   `docs/roadmap/STATUS.md`, `scripts/self_use_queue.json`, `.agent/decisions.md`,
   `.agent/prose_slips.md`, `.agent/candidates.md` or `.agent/operator_questions.md`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. THE ONE
   EXCEPTION is the full suite in C5: a red suite is this feature's work and not a stop — commit
   its transcript exactly as measured, report every bad node id, and hand back. Never weaken an
   assertion, delete a test or mark anything xfail on your own initiative.
5. NOTHING IS MERGED, NOTHING IS CLOSED. No `gh pr merge`, no `gh pr create`, no checkout of
   `main`, no branch deletion, no force-push, no STATUS edit, no evidence job, no review package.
6. Leave the `.remedy-wt/job-*` worktrees, their branches, the reviewer's worktrees whose names
   begin `.remedy-wt/f264-`, and every existing stash alone.
7. The full suite runs ONCE, in C5, and nowhere else this round (amend0917 rule 1).

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G4 run before C5 is written, and G5
is the suite C5 runs.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f264-r8-*` copy byte for byte with
 its source (the block copy against `.remedy-wt/f264-r8-block.md`), read back with
 `git show <C1>:<path>`. Report one reading per copy.

G2 THE RECORDS, THE GUIDE, THE BUILT STATE AND THE CONSOLIDATION — the sha256 of each file below,
 read with `git show <commit>:<path>` at the commit named, equals the reviewer's reading, which its
 simulation printed from a tree it built by applying these payloads at `d9bea4ba`:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/live_review.md | 324554 | 72a8ee952607be794cc14da52f407569f697898280539ebbd0ddf47824ca9a7a |
 | C2 | .agent/plan.md | 1096 | 3eff73a4b83aadd8abc5711a56f3e0e85f9d2abbe8f4ffc06b2f17d4cfd9356b |
 | C3 | docs/README.md | 20192 | 0917fcb35c91ec1bf4046be556f797e02e6d10b9e3b2f3a33018a21772dcdc5f |
 | C3 | docs/agents/planner_reviewer_prompt.md | 99461 | 405748947bf0c7cc27c8976c4dbbb40bc76c3139d4c47ce8921ad524dffc5234 |
 | C3 | docs/guides/steering-user-guide-v1.md | 4680 | bce9c3fd463a2d864edb0828c2492f291598d1bb00cd553d900b61211a7e030e |
 | C3 | docs/roadmap/features/T5_F264.md | 8982 | 80b78d143d4c6237fa0f663e6cb3bb3bd107aca51fa46054c6b70e1890fc1fa6 |
 | C3 | docs/system/operator-cockpit-v1.md | 4408 | a9653a6c82db9abd3f2f57428a8a13b82287fc0d0c1cb0a3d7560834f73647f5 |
 | C4 | .agent/selfuse_f264/result.txt | 274 | d9c267009f86518e3be1dad28526b8ba5d6925b64bc3b8f20b9e92ce962b871b |
 Also: among the lines C2's diff ADDS to `.agent/live_review.md`, the count of those beginning
 `Gate: F264 R7 — ` (the reviewer's simulation read 1); the open set by distinct id, computed with
 `open_finding_ids` from `scripts/rotate_live_review.py` over the file's TEXT, at `d9bea4ba` and at
 C2, with the set difference in both directions (the reviewer read 3 and 3 — R-0499, R-0950 and
 R-1008 — both differences empty); the checklist's item numbers, computed with
 `live_checklist_items` of `packages/orchestration/block_lint.py` over
 `docs/agents/planner_reviewer_prompt.md` at `d9bea4ba` and at C3 (the reviewer read the same 34
 numbers at both); the count of lines of `docs/README.md` at C3 containing
 `steering-user-guide-v1.md` (the reviewer read 2, the quick-find row and the guides-table row);
 and `git diff --name-only` between consecutive commits from C1 to C4, which must name exactly the
 paths each commit lists.

G3 THE LINTER ON THIS BLOCK — at C4, in the primary checkout:
 `python3 -m apps.cli.main integrity block .remedy-wt/f264-r8-block.md`, real exit code 0,
 every item `[OK]`. Report the whole output.

G4 THE TESTS AND THE TREE — in the primary checkout at C4, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_advertised_commands.py tests/orchestration/test_block_lint.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/orchestration/test_self_use_generator.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same command, serially, inside its simulation tree at the C4 it built and
 read `504 passed, 1 skipped` at real exit code 0. `tests/cli/test_advertised_commands.py` is the
 guard over every `remedy chat` line the guide prints; the reviewer red-controlled it by changing
 one of those lines to a subcommand that does not exist and one to a flag the command does not
 declare, and each read `1 failed, 13 passed`. Then C4's four readings verbatim; then
 `python3 -m apps.cli.main integrity check --json`, all six checks `pass` at `fail_count` 0; and
 `git status --porcelain` empty with no untracked file (closure precondition 3).

G5 THE INTEGRATION GATE — the UI build's last line and real exit code, `git status --porcelain`
 after it, then the full suite's real exit code, its summary line and every bad node id, all of it
 in `.agent/authored/f264-closure-suite.txt`. Report whether
 `tests/orchestration/test_import_reachability.py` or `tests/test_no_orphan_modules.py` holds a
 bad node (closure precondition 7).

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 6`, which must show C5, C4, C3, C2, C1 and `d9bea4ba` in that order;
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
what you expected to find. Your Session section reads SESSION 2 of feature F264, round 8, and says
in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round
8, then the closure's second half — the booking of round 8, any repair the suite requires, the
evidence job and the review package — and then the closing round. State the open-findings count,
3, and the operator-questions count, 0.
