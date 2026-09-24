STEP F282 R10 — THE CLOSURE SEQUENCE'S FIRST HALF: BOOK ROUND 9, CONSOLIDATE THE CHECKLIST, WRITE THE BUILT STATE, RECORD THE SELF-USE TRACK AND RUN THE ONE FULL SUITE

GOAL
Book round 9's PASS, R-1028's resolution and R-0950's partial one; record DECISION F282 D10; land
T019, the one checklist consolidation pass, which joins the counter-measures of R-0819 and R-0662 to
item 8 and that of R-0820 to item 12 of `docs/agents/planner_reviewer_prompt.md` §3 at 34 items;
append the feature file's Built State; record the self-use track's answer, NONE; and run this
feature's ONE full suite, committing its transcript.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. This round closes nothing: the evidence job, the review zip, the
ledger rotation, the STATUS line and the pull request belong to later rounds, and no commit of this
round may touch `docs/roadmap/STATUS.md`, `README.md` or `scripts/self_use_queue.json`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f282-r10-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f282-r10-scratch/`   The reviewer's scripts; do not edit or delete them.
  `.remedy-wt/f282-r10-worker/`    YOURS for logs and scripts. All three are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, `ln`, `npm ci`, `npm install`, process substitution,
`cd <dir> && git ...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`.
Capture real exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when
you pipe. Use `git -C <path>` rather than `cd`. Use `python3 - <<'PY'` for counting, hashing and
copying (`shutil.copyfile`). A heredoc containing a dollar-brace is refused: write such a script to a
file under your own directory and run the file. The `remedy` CLI is denied: run
`python3 -m apps.cli.main ...`. Never use `git stash` in any form.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f282-findings-paydown-v2`, and `git log --oneline -1` must read `ef2edb49`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f282-r10-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `git branch --list 'remedy/job-*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f282-r10-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.diff | 14 | 8554 | 5c4dc8a3f2dd34eff09d2935460c1f3f59306cee78155b5c172cd3365c79a0d0 |
| decisions.diff | 35 | 2839 | 631313297efe4232966eb91ec351fa9b8de2cf09557ddf3666aa51f7e5aee073 |
| plan.md | 32 | 1239 | 5606eec367b57df3f0dc3c3918855f8309ea99ce632f22a45ea09531288288a1 |
| product.diff | 89 | 6677 | 0b9eda1783ab1a5316601c869c38dd4d4f49e2cee73965f7928ebd84d32a254d |
| selfuse_result.txt | 6 | 274 | a0852bacb61c410112758dd449884c65a3f212b69afc092f3b515467a749571c |

`plan.md` is a REWRITE of `.agent/plan.md`, copied whole. The `.diff` files go on with
`git apply`; the reviewer generated every one from a tree at `ef2edb49` and applied all of
them, in the commit order below, to a fresh worktree at `ef2edb49` with `git apply --check`
then `git apply`, every one at real exit code 0. `ledger.diff` appends three paragraphs to
`.agent/live_review.md` — the `Gate: F282 R9` entry, the `Done:` line of R-1028 and R-0950's
partial resolution. `product.diff` edits `docs/agents/planner_reviewer_prompt.md` (items 8 and 12
of §3 and its consolidation paragraph) and appends the Built State to
`docs/roadmap/features/T2_F282.md`. `selfuse_result.txt` becomes the NEW FILE at
`.agent/selfuse_f282/result.txt`, copied only after C4's readings equal it.

BUNDLE — the commits are C1, C2, C3, C4 and C5, in this order.

C1 — copy this block and every payload: `.agent/authored/f282-r10-block.md` := this block, and one
  `.agent/authored/f282-r10-<name>` for each payload, keeping its own file name. All by
  `shutil.copyfile`.
  Subject: `F282 R10 C1: copy round 10 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 176. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C2 — THE BOOKKEEPING, in this order:
   1. `git apply` ledger.diff     → `.agent/live_review.md`
   2. `git apply` decisions.diff  → `.agent/decisions.md`
   3. rewrite `.agent/plan.md` := plan.md
  Subject: `F282 R10 C2: book round 9, resolve R-1028, partly resolve R-0950 and record DECISION F282 D10`
  Expected by `git show --numstat` (insertions/deletions): 27/0 decisions.md,
  6/0 live_review.md, 11/9 plan.md.

C3 — THE CONSOLIDATION AND THE BUILT STATE: `git apply` product.diff.
  Subject: `F282 R10 C3: consolidate the checklist for R-0662, R-0819 and R-0820 and write the Built State`
  Expected (insertions/deletions): 24/0 planner_reviewer_prompt.md, 32/0 T2_F282.md.

C4 — THE SELF-USE TRACK (closure precondition 6), from a scratch Python file you write under your
  directory and run in the primary checkout: print `next_self_use_item()` of
  `packages.orchestration.self_use_queue`, then `generate_and_append_if_empty()` of
  `packages.orchestration.self_use_generator` with no arguments, then `next_self_use_item()` again,
  then `git status --porcelain`. The reviewer read `None`, `None`, `None` and an empty status at the
  tree C3 builds. If all four readings are those, copy selfuse_result.txt to
  `.agent/selfuse_f282/result.txt` by `shutil.copyfile` and commit it. If ANY reading differs —
  the generator returns an item, or the queue file changes — STOP under constraint 4: commit
  nothing for C4, and report the readings verbatim.
  Subject: `F282 R10 C4: record the closure's self-use track, NONE`
  Expected insertions: 6.

C5 — THE INTEGRATION GATE AND THE HANDBACK, in the PRIMARY checkout, after C4:
  (a) Build the UI first, because a cold `apps/ui/dist` reddens `tests/ui_server/` under `-n`, and
      the dist on disk predates round 7's change to `RemedyShell.tsx`:
      `bash -c 'npm --prefix apps/ui run build 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'`.
      A refused or failing build is a STOP under constraint 4. Then `git status --porcelain`,
      which must still be empty.
  (b) `python3 -m pytest -n auto -q`, its log written to `.remedy-wt/f282-r10-worker/full-suite.log`.
      Write `.agent/authored/f282-closure-suite.txt` holding the summary line, the real exit code
      and the FULL list of bad node ids (failed plus errors), or the literal `NONE`.
  (c) Rewrite `.agent/handoff.md` per `docs/agents/handback_template.md`, and commit it TOGETHER
      with the transcript.
  Subject: `F282 R10 C5: record the closure suite transcript and rewrite handoff for round 10`
  Then `git push origin feature/f282-findings-paydown-v2` and report its real outcome. Do NOT
  create a pull request.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1.
3. The round's whole tracked path set is: the `.agent/authored/f282-r10-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `docs/agents/planner_reviewer_prompt.md`, `docs/roadmap/features/T2_F282.md`,
   `.agent/selfuse_f282/result.txt`, `.agent/authored/f282-closure-suite.txt` and
   `.agent/handoff.md`. Report the list you measure with `git diff --name-only ef2edb49 HEAD`
   after C5. Nothing under `packages/`, `apps/`, `tests/` or `scripts/`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. THE ONE
   EXCEPTION is the full suite in C5: a red suite is this feature's work and not a stop — commit
   its transcript exactly as measured, report every bad node id, and hand back. Never weaken an
   assertion, delete a test or mark anything xfail on your own initiative.
5. NOTHING IS MERGED, NOTHING IS CLOSED. No `gh pr merge`, no `gh pr create`, no checkout of
   `main`, no branch deletion, no force-push, no STATUS edit, no evidence job, no review zip.
6. Leave `.remedy-wt/job-129b3ad7206d4f8d`, `.remedy-wt/job-6a38b3203cca4928`,
   `.remedy-wt/job-e7268925db3a4831`, `.remedy-wt/job-e7a145761bf04f86`, the reviewer's
   `.remedy-wt/f282-r10-dry` and `.remedy-wt/f282-r10-sim`, their branches and every existing
   stash alone.
7. The full suite runs ONCE, in C5, and nowhere else this round (amend0917 rule 1).

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G4 run before C5 is written, and G5
is the suite C5 runs.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f282-r10-*` copy byte for
 byte with its source (the block copy against `.remedy-wt/f282-r10-block.md`), read back with
 `git show <C1>:<path>`. Report one reading per copy.

G2 THE BOOKKEEPING, THE CONSOLIDATION AND THE BUILT STATE — the sha256 of each file below, read
 with `git show <commit>:<path>` at the commit named, equals the reviewer's reading, which its
 simulation printed from a tree it built by applying these payloads at `ef2edb49`:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/live_review.md | 430187 | 1790c3fd3147227dcc5ce774789a5b1b2a5d0c955e07685513e8a5cc61094339 |
 | C2 | .agent/decisions.md | 1934593 | 04e57b3c33dcfa06184645d85cdd4d4d50e3121860f091e528a28877dc090563 |
 | C2 | .agent/plan.md | 1239 | 5606eec367b57df3f0dc3c3918855f8309ea99ce632f22a45ea09531288288a1 |
 | C3 | docs/agents/planner_reviewer_prompt.md | 98974 | f22a0f52d75be4f5301a58e206502aca98164480ef697bde0939322c4ea2d46a |
 | C3 | docs/roadmap/features/T2_F282.md | 9441 | fc442e15f8fae4ae4a1a66e8c89514fac6289deb7b24f25b9b9c7df346457cb2 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `ef2edb49` and at C2, with the set
 difference in both directions (the reviewer read 7 and 6, R-1028 leaving and none arriving);
 the checklist's item numbers, computed with `live_checklist_items` of
 `packages/orchestration/block_lint.py` over `docs/agents/planner_reviewer_prompt.md` at
 `ef2edb49` and at C3 — the reviewer read the same 34 numbers at both; and `git diff --name-only`
 between consecutive commits from C1 to C4, which must name exactly the paths each commit lists.

G3 THE LINTER ON THIS BLOCK — at C4, in the primary checkout:
 `python3 -m apps.cli.main integrity block .remedy-wt/f282-r10-block.md`, real exit code 0,
 every item `[OK]`. Report the whole output.

G4 THE TESTS AND THE TREE — in the primary checkout at C4:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/orchestration/test_block_lint.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/orchestration/test_self_use_generator.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection under `-n 8` inside its simulation tree at the C3 it built
 and read `490 passed, 1 skipped` at real exit code 0. Then C4's four readings verbatim; then
 `python3 -m apps.cli.main integrity check --json`, all six checks `pass` at `fail_count` 0; and
 `git status --porcelain` empty with no untracked file (closure precondition 3).

G5 THE INTEGRATION GATE — the UI build's last line and real exit code, `git status --porcelain`
 after it, then the full suite's real exit code, its summary line and every bad node id, all of it
 in `.agent/authored/f282-closure-suite.txt`. Report whether
 `tests/orchestration/test_import_reachability.py` or `tests/test_no_orphan_modules.py` holds a
 bad node (closure precondition 7).

G6 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 6`, which must show C5, C4, C3, C2, C1 and `ef2edb49` in that order;
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
what you expected to find. Your Session section reads SESSION 2 of feature F282, round 10, and says
in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round
10, then the closure's second half — the booking of round 10 and T019's resolutions, any repair the
suite requires, the evidence job and the review package — and then the closing round. State the
open-findings count, 6, and the operator-questions count, 0.
