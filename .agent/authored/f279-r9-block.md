STEP F279 R9 — the first closure repair round: two guard tests, and the one full suite on the repaired tree

GOAL
Book round 8's PASS, record the self-use run as a recurrence of R-1007, register R-1040 and R-1041,
repair
the two guard tests the closure suite found red, and run the feature's one full suite again on
the repaired tree (operator amendment amend0917-throughput rule 2, the shrinking rule; amendment
amend0921-operator-feedback rule 1, the run belongs to the shipped tree).

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You never
issue a verdict and you never merge. The reviewer authors every payload; you apply them byte for
byte. This round closes nothing: no `docs/roadmap/STATUS.md`, no `README.md`, no
`scripts/self_use_queue.json`, no evidence job, no review zip, no pull request.

WHAT THE REVIEWER FOUND (both bad nodes are this feature's own; the ledger payload records why)
`test_no_new_product_dependency` counts `live_review.md` across `packages/` and `apps/`, and
round 5's `packages/orchestration/block_lint.py` names the ledger by design; the repair adds it to
that test's `_ALLOWED_LEGACY` with its reason. `test_the_env_var_is_read_in_exactly_one_module`
counts `REMEDY_REVIEW_BASE` across the same trees, and round 2's registry spells it once in
`packages/orchestration/config.py`; the repair accepts that one key spec and adds two assertions
that keep the test's property — `config.py` spells it exactly once, as `env_var=`, and no module
outside `config.py` asks for the key `review.base`.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f279-r9-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f279-r9-scratch/`   YOURS for logs, captures and scripts, EXCEPT every file the
      reviewer put there before C1 (`review_r8.py`, `sim.py`), which is read-only to you.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, heredocs written with `cat >`, process substitution, `$?` or
`${...}` outside a `bash -c`, `cd <dir> && git ...`, shell `for` loops, brace expansion, `awk`,
`xxd`, `bc`, a `grep` pattern holding `$`, and multi-operation one-liners chained with `;`, `&&`
or `|` outside a `bash -c`; put multi-step code in a scratch Python file. Capture real exit codes
as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`. Use `git -C <dir>` for a worktree. The `remedy` CLI is
denied: run `python3 -m apps.cli.main ...`. Nothing under `.data/` is readable to you. NEVER USE
`git stash` IN ANY FORM, and never check out another commit in the primary checkout.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` empty, `git branch --show-current` reads
   `feature/f279-configuration-toolchain-truth`, `git log --oneline -1` reads `2ecc2a90`.
3. Verify this block's own bytes (R-0954): line count and sha256 of `.remedy-wt/f279-r9-block.md`
   against the two readings your delegation message states. Report both beside both, and stop if
   either differs.
4. Record `git worktree list` and the first line of `git stash list`.

PAYLOADS — under `.remedy-wt/f279-r9-payloads/`, printed by the reviewer's simulation
(lines = newline count):

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.md | 8 | 7293 | ddee474e9fcb283231e6f14e92522e0bdc135ca4fc1f64f3a692ee2957e75a10 |
| mutations.py | 56 | 2217 | 7ee44c5f32bf817b03ddc7e6fa29c9fd99282807fec33841926633b429c58122 |
| plan.md | 31 | 1264 | b5c638cf0eb10beb9b2164be84c02d13d14a210ac63889f551540fbe3deb1827 |
| prose_slips.md | 1 | 597 | 3ec5d9375b0ebd463210c3079b73e779bdf7715f9b76b38cb18fa1cda16c51db |
| test_development_artifact_boundary.diff | 16 | 948 | c1ad5633ef22bdaf81cf288fdcc59f02cd2fba5d4e7702075cd4550f4f8e2247 |
| test_review_subject_resolution.diff | 25 | 1627 | 6b66ccb0a227aa9e30e85a71c6764b60dad59921688f5bff130e76c144336849 |

`ledger.md` is an APPEND beginning with the single newline that separates records: round 8's
`Gate:` entry, a `Recurrence: R-1007` paragraph and the `- R-1040` and `- R-1041` registrations.
`prose_slips.md` is an APPEND of one dated line. Appends are strict byte concatenation onto the
file as it stands at `2ecc2a90`. `plan.md` is a REWRITE. Each `.diff` goes on with `git apply
--check` then `git apply`; the reviewer generated both from a tree at `2ecc2a90` and applied them
to a fresh worktree there at real exit code 0. `mutations.py` is a TOOL for G4, never applied.
Never retype or edit a payload.

BUNDLE — commits C1 to C4, in this order.

C1 — `.agent/authored/f279-r9-block.md` := this block; `.agent/authored/f279-r9-<name>` for each
  payload, keeping its file name. Byte for byte, with `shutil.copyfile`.
  Subject: `F279 R9 C1: copy round 9 block and payloads into .agent/authored/`
  Its insertions are this block's line count plus 137. Report the number you measure.

C2 — `.agent/live_review.md` += ledger.md · `.agent/prose_slips.md` += prose_slips.md ·
  `.agent/plan.md` := plan.md.
  Subject: `F279 R9 C2: book round 8's PASS, record R-1007's recurrence, register R-1040 and R-1041`
  Expected insertions by `git show --numstat`: 8 live_review.md, 9 plan.md, 1 prose_slips.md.

C3 — `git apply` test_development_artifact_boundary.diff and test_review_subject_resolution.diff.
  Subject: `F279 R9 C3: hold the two guard tests to what F279 added, without widening them`
  Expected insertions: 5 test_development_artifact_boundary.py, 13
  test_review_subject_resolution.py.

C4 — THE INTEGRATION GATE AGAIN and THE HANDBACK, one commit: the new transcript REPLACES
  `.agent/authored/f279-closure-suite.txt` at the same path (round 8's stays in git history), and
  `.agent/handoff.md` is rewritten per `docs/agents/handback_template.md`.
  Subject: `F279 R9 C4: record the repaired closure suite and rewrite handoff for round 9`
  Then `git push origin feature/f279-configuration-toolchain-truth`. Do NOT create a PR.

CONSTRAINTS
1. Never edit or retype a payload. Run `git apply --check` before each real `git apply` and report
   its exit code.
2. Every commit stays under 500 insertions by `git show --numstat`.
3. The round's tracked path set is EXACTLY: the `.agent/authored/f279-r9-*` copies C1 makes,
   `.agent/live_review.md`, `.agent/prose_slips.md`, `.agent/plan.md`,
   `tests/orchestration/test_development_artifact_boundary.py`,
   `tests/orchestration/test_review_subject_resolution.py`,
   `.agent/authored/f279-closure-suite.txt` and `.agent/handoff.md`. Report the set you measure
   with `git diff --name-only 2ecc2a90` after C4. Nothing under `packages/` or `apps/`.
4. THE SHRINKING RULE: round 8's bad set is the two node ids of
   `.agent/authored/f279-closure-suite.txt` at `2ecc2a90`. This round's suite must list neither
   of them and no node that set does not hold. If it lists ANY bad node, commit the transcript
   exactly as measured, report every bad node id, and hand back; never weaken an assertion,
   delete a test or mark anything xfail.
5. If any other gate goes red, STOP: commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back.
6. NOTHING IS MERGED, NOTHING IS CLOSED. No `gh pr merge`, no `gh pr create`, no checkout of
   `main`, no branch deletion, no force-push.
7. Leave every `.remedy-wt/job-*` worktree and every `remedy/job-*` branch alone. The worktree G4
   adds goes under `.remedy-wt/`, is removed as that step's last action, and `git worktree list`
   is reported afterwards (R-0940).
8. A statement in the handback about what a job or a run did quotes the field that says so; a
   reading you did not take is reported as not taken.

DONE-WHEN — THE GATES, every one executed, every reading reported with its real exit code.
"Green" as a word is a finding (guardrail G4). G1 to G5 run BEFORE C4 is written; G5's suite run
is the last of them.

G1 TRANSPORT — each payload's lines, bytes and sha256 against the PAYLOADS table; then each
 committed `.agent/authored/f279-r9-*` blob, read with `git show <C1>:<path>`, compared byte for
 byte with its source (the block copy against `.remedy-wt/f279-r9-block.md`). One reading per
 file, all equal.

G2 THE BOOKING — read with `git show <C2>:<path>`, each equal to the reviewer's simulation:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 395859 | 1f48a2809f92c5d77eac14bfbcd023a8c907812a31be014d2e45f85b2d2f4708 |
 | .agent/prose_slips.md | 365048 | 26e20e0188ab78d31f98273ad8bbbde291eae3572daa7c152aea0c15a4beb4f5 |
 | .agent/plan.md | 1264 | b5c638cf0eb10beb9b2164be84c02d13d14a210ac63889f551540fbe3deb1827 |
 Also: lines beginning `Gate: F279 R8 — `, `Recurrence: R-1007 — `, `- R-1040 — ` and
 `- R-1041 — ` at C2, each 1; and the open set by distinct id via `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT at `2ecc2a90` and at C2 — the reviewer's
 simulation REMOVED none and ADDED exactly `R-1040` and `R-1041`; report both sizes you measure.

G3 THE REPAIR — at C3, read with `git show <C3>:<path>`, each equal to the reviewer's simulation:
 | path | bytes | sha256 |
 |---|---|---|
 | tests/orchestration/test_development_artifact_boundary.py | 6518 | 1d9fbb42ea438c6dd8c2c4989e8ebdd997080eeae3b6be3262872054473e6ec5 |
 | tests/orchestration/test_review_subject_resolution.py | 14557 | c3f864dea68dd48ff4767b5b2399ce4f76bfff430edd32339613831cee494561 |
 Then, SERIALLY in the primary checkout at C3:
 `bash -c 'python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_development_artifact_boundary.py tests/orchestration/test_review_subject_resolution.py tests/docs/ tests/orchestration/test_integrity_gate.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_block_lint.py tests/orchestration/test_env_registry.py tests/cli/test_golden_path.py 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'`
 — the reviewer ran the same selection without the golden path in its simulated tree and read
 `429 passed` at exit 0 — and `python3 -m ruff check` over the two test files, exit 0.

G4 THE RED PROOFS — `git worktree add --detach .remedy-wt/f279-r9-mut <C3>`, then
 `python3 -B .remedy-wt/f279-r9-payloads/mutations.py .remedy-wt/f279-r9-mut` and report its whole
 output. Each mutation PLANTS a violation in a production module of the worktree and restores it.
 The reviewer read, over the same script against its simulated tree:
 control_before `32 passed` at exit 0;
 m1 (a second module names the ledger) 1 failed at exit 1, at
   `TestWhitelistBoundary::test_no_new_product_dependency`;
 m2 (`config.py` spells the base twice) 1 failed at exit 1, and
 m3 (a module asks for the key `review.base`) 1 failed at exit 1, each at
   `TestProductionIsTheOnlyImplementation::test_the_env_var_is_read_in_exactly_one_module`;
 control_after `32 passed` at exit 0.
 Then `git worktree remove --force .remedy-wt/f279-r9-mut`, `git worktree prune`, and report
 `git worktree list`.

G5 THE INTEGRATION GATE — in the PRIMARY checkout at C3, in this order: (a) `python3 -m
 apps.cli.main integrity check --json`, all five checks `pass` at `fail_count` 0, and `git status
 --porcelain` empty with no untracked file; (b) `bash -c 'npm --prefix apps/ui run build 2>&1 |
 tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'` — never `npm install` — and `git status --porcelain`
 still empty; (c) `python3 -m pytest -n auto -q`, its log written outside the repository
 (`~/remedy-gate-scratch/` is writable): its real exit code, its summary line and every bad node
 id go into `.agent/authored/f279-closure-suite.txt`, together with the shrinking comparison
 against round 8's two ids, and a statement of whether
 `tests/orchestration/test_import_reachability.py` or `tests/test_no_orphan_modules.py` holds a
 bad node (closure precondition 7).

G6 TREE AND PUSH — after C4: `git status --porcelain` empty; `git log --oneline -n 5`, showing C4
 to C1 and `2ecc2a90`; `git worktree list`; `git stash list`'s first line unchanged from its reading
 before C1; the push's real outcome; `gh pr list --state open --json
 number,headRefName,baseRefName,isDraft`, EMPTY. These go in your final reply, not the handback —
 the push ships the handback.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, and AGENTS.md's
item-status table with one row per commit and per gate: state block, the per-commit
changed-files table with the insertions git MEASURED beside the ones this block expected, every
gate's real output and exit code, the full suite's summary line and bad node ids with the
shrinking comparison, the deviations, and the next action. Your Session section reads SESSION 2
of feature F279, round 9, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of round
9, then the closure sequence's evidence job and review package, and then the closing round: the
ledger rotation, the STATUS line with the README counters in the same commit, and the pull
request. State the open findings after this round as the 26 open at `2ecc2a90` plus `R-1040` and
`R-1041`, and the operator-questions count, 0.
