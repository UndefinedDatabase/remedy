STEP F278 R1 — CLAIM F278 AND LAND T001: the one durable write

GOAL
Pull request 265 is merged; `main` is at `9817a927` and F278 is the next unchecked line.
Cut its branch, claim it, re-head the live review record, and land T001 alone:
`durable_write` and `durable_write_json` in `packages/common/secure_fs.py`, with a new test
file whose fsync test and concurrent-writer test are this slice's two red proofs.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

WHY T001 IS ALONE IN ITS ROUND
T2_F278.md's Orchestrator brief: every later slice migrates a private helper onto this one
and deletes the copy, so the helper has to be right first. `secure_fs.py` already holds
descriptor-anchored writers (`write_file_atomically`, `append_line_at`); they are a
different contract and this round does not touch them. The new helper is the PATH-based
one: `tempfile.mkstemp` in the destination directory, write every byte, fsync the file,
`os.replace`, fsync the parent directory, and unlink the temporary file on every failure.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f278-r1-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f278-r1-scratch/`   YOURS for logs and scripts. Both are gitignored. The
      reviewer left its own scripts in scratch; do not edit or delete them.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, `cd <dir> && git ...`, and multi-operation
one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe pytest.
Use `git -C <path>` rather than `cd`. Use `python3 - <<'PY'` for counting, hashing and
copying (`shutil.copyfile`).

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` must be empty, `git branch --show-current` must read `main`,
   and `git log --oneline -1` must read `9817a927`. Report all three. Then
   `git checkout -b feature/f278-durable-writes-loud-failures` and report the branch. Do
   NOT pull: the Open PR Gate ran before you and `main` is already at the merge commit.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f278-r1-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `git branch --list 'remedy/job-*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f278-r1-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| context.md | 50 | 2451 | 55be0a982026b146d5511ffee64a3d8cc46a730085e074fdf401cb64144dfd4b |
| plan.md | 35 | 1483 | ef79958425dd58e1c5873ea3b438afedf5ce13ed0addc62155502aa61ec41ad1 |
| rehead.diff | 63 | 6919 | 2f8faa9dc627c767c8553a11f1dff131f56ee167dfd309727bf982338ce035f6 |
| secure_fs.diff | 86 | 3878 | 0b468114b3e3d07de620822c6b0c958029a2dc2c7ffebf9755de2cf58b8f4efd |
| status.diff | 13 | 2027 | 267a5d89d3faebefeab7655cad32da57d4c74241bc37badf81b61351c49a0217 |
| test_secure_fs_durable_write.py | 173 | 6828 | e2de683d0958dce574051ec0c683fbde83e2eb330b43cc07567e4405e7c86f92 |
| mutations.py | 53 | 2169 | 0c52bced6b395d0876691d2f61c9e426510ba9fd4ead3438e5e6d5d15f647f00 |

`plan.md` and `context.md` are REWRITES of `.agent/plan.md` and `.agent/context.md`.
`test_secure_fs_durable_write.py` is a NEW FILE at
`tests/orchestration/test_secure_fs_durable_write.py`, copied whole. The `.diff` files
go on with `git apply`; the reviewer generated every one from a tree at `9817a927` and ran
`git apply --check` over each of them at `9817a927`, real exit code 0. `mutations.py` is a TOOL
for G5: it is run, never applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C2, C3 and C4, in this order. The copies are two
commits because together with this block they exceed the 500-line cap.

C1a — copy this block and the bookkeeping payloads
  `.agent/authored/f278-r1-block.md` := this block, and one
  `.agent/authored/f278-r1-<name>` for each of context.md, plan.md, rehead.diff and
  status.diff, keeping each payload's own file name. All by `shutil.copyfile`.
  Subject: `F278 R1 C1a: copy round 1 block and bookkeeping payloads into .agent/authored/`
  Its insertions are this block's line count plus 161. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C1b — copy the product payloads
  `.agent/authored/f278-r1-secure_fs.diff`,
  `.agent/authored/f278-r1-test_secure_fs_durable_write.py` and
  `.agent/authored/f278-r1-mutations.py`, by `shutil.copyfile`.
  Subject: `F278 R1 C1b: copy round 1 product payloads into .agent/authored/`
  Expected insertions: 312.

C2 — THE CLAIM, in this order:
   1. `git apply` rehead.diff  → `.agent/live_review.md`
   2. `git apply` status.diff  → `docs/roadmap/STATUS.md`
   3. rewrite `.agent/plan.md` := plan.md
   4. rewrite `.agent/context.md` := context.md
  Subject: `F278 R1 C2: claim F278 and re-head the live review record`
  Expected insertions: 67 by `git show --numstat` (22, 1, 22 and 22 in that order).

C3 — THE HELPER AND ITS TESTS in one commit, because the test is what verifies it
  `git apply` secure_fs.diff, then copy test_secure_fs_durable_write.py to
  `tests/orchestration/test_secure_fs_durable_write.py` and `git add` it — an untracked test
  file fails `integrity check`'s `relevant_untracked`.
  Subject: `F278 R1 C3: add durable_write, the one path-based durable write`
  Expected insertions: 237 — 64 for `secure_fs.py` and 173 for the new test file.

C4 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F278 R1 C4: rewrite handoff for round 1`
  Then `git push -u origin feature/f278-durable-writes-loud-failures`. Do NOT create a pull
  request: the branch opens one at F278's closure. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f278-r1-*` copies,
   `.agent/live_review.md`, `docs/roadmap/STATUS.md`, `.agent/plan.md`, `.agent/context.md`,
   `packages/common/secure_fs.py`, `tests/orchestration/test_secure_fs_durable_write.py`
   and `.agent/handoff.md`. Report the list you measure with
   `git diff --name-only 9817a927 HEAD` after C4. Do NOT touch `README.md`,
   `.agent/decisions.md`, `.agent/prose_slips.md`, `.agent/candidates.md`,
   `.agent/operator_questions.md`, `docs/roadmap/features/T2_F278.md`, or any module other
   than `secure_fs.py`. No private atomic-write helper is migrated this round.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main` after the
   branch is cut, no branch deletion, no force-push, no `git stash`.
6. Leave `.remedy-wt/job-129b3ad7206d4f8d`, its branch and every existing stash alone. The
   worktree G5 adds goes under `.remedy-wt/`, is removed as that step's last action, and
   `git worktree list` is reported afterwards (finding R-0940).
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run
   and F278's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C4 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f278-r1-*` copy byte for
 byte with its source (the block copy against `.remedy-wt/f278-r1-block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE CLAIM — at C2, the sha256 of each file below, read with `git show <C2>:<path>`,
 equals the reviewer's reading, which its dry run printed from the tree it built:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 424321 | c02956ae55c72f2f52e00dcfc4f8bfa1a16ea751fa0f9203b08567cfb89210ff |
 | docs/roadmap/STATUS.md | 46787 | e4171f9f665060d7e477661e86ee4d078b7f9691a81fd8bb371e4e4357e385cb |
 | .agent/plan.md | 1483 | ef79958425dd58e1c5873ea3b438afedf5ce13ed0addc62155502aa61ec41ad1 |
 | .agent/context.md | 2451 | 55be0a982026b146d5511ffee64a3d8cc46a730085e074fdf401cb64144dfd4b |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `9817a927` and at C2, with the set
 difference in both directions (the reviewer read 26 and 26, both differences empty);
 `.agent/plan.md`'s line count at C2, under 50; F278's STATUS line read back in full, which
 must begin `- [~] F278 — `; and `git diff --name-only <C1b> <C2>`, which must name exactly
 the paths C2 lists.

G3 THE HELPER — at C3, `git diff --name-only <C2> <C3>` names exactly
 `packages/common/secure_fs.py` and `tests/orchestration/test_secure_fs_durable_write.py`,
 and their sha256 read with `git show <C3>:<path>` equal:
 | path | bytes | sha256 |
 |---|---|---|
 | packages/common/secure_fs.py | 39941 | 5affd1a24a88d390bb6fec5e019012b0b122a42786e9e47919025ded70d0fae0 |
 | tests/orchestration/test_secure_fs_durable_write.py | 6828 | e2de683d0958dce574051ec0c683fbde83e2eb330b43cc07567e4405e7c86f92 |

G4 THE TESTS — in the primary checkout at C3, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_secure_fs_durable_write.py tests/orchestration/test_secure_fs.py tests/docs/ tests/orchestration/test_roadmap_index.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path inside a disposable worktree
 carrying C2 and C3, and read `541 passed, 2 skipped` at real exit code 0; the primary
 checkout carries the UI toolchain a worktree lacks, so a skip may pass there. Report what
 you read. The state-file readers are in the selection because C2 rewrites
 `.agent/plan.md`, `.agent/context.md` and `.agent/live_review.md`. Then
 `python3 -m ruff check packages/common/secure_fs.py tests/orchestration/test_secure_fs_durable_write.py`,
 real exit code 0, and `python3 -m apps.cli.main integrity check --json`, which must read
 all five checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f278-r1-mut <C3>`, then
 `python3 .remedy-wt/f278-r1-payloads/mutations.py .remedy-wt/f278-r1-mut` and report its
 whole output. The script asserts each FROM occurs exactly once, applies it, runs the new
 test file, restores the bytes, and runs an unmutated control first and last. The reviewer
 read, over the same script against its own tree carrying C3:
 control_before `11 passed` at exit 0;
 m1 (the file fsync removed) `2 failed, 9 passed` at exit 1, both in `TestBothFsyncsHappen`;
 m2 (the directory fsync removed) `1 failed, 10 passed` at exit 1, at
   `test_the_file_and_then_its_parent_directory_are_fsynced`;
 m3 (the fixed sibling `with_suffix(".tmp")`) `2 failed, 9 passed` at exit 1, at
   `test_eight_writers_leave_exactly_one_intact_payload_and_no_residue` and
   `test_a_multi_suffix_name_keeps_its_temporary_file_a_sibling_under_its_whole_name`;
 control_after `11 passed` at exit 0.
 Then `git worktree remove --force .remedy-wt/f278-r1-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C4: `git status --porcelain`, which must be empty;
 `git log --oneline -n 6`, which must show C4, C3, C2, C1b, C1a and `9817a927` in that
 order; `git worktree list`, which must show the primary checkout and
 `.remedy-wt/job-129b3ad7206d4f8d` and nothing else; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be
 EMPTY. These readings go in your reply, since C4 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: the state block, the per-commit
changed-files table with the insertion count you MEASURED beside the one this block
expected, every gate's real output and exit code, the item-status table, the deviations,
and the next expected action. Report what you ran, not what you expected to find. Your
Session section reads SESSION 1 of feature F278, round 1, and says in one sentence how
much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review
of round 1, then T002 — the migration of the surviving private atomic-write helpers onto
`durable_write`, re-derived from the tree, one module per commit. State the open-findings
count, 26, and the operator-questions count, 0.
