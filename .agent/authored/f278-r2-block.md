STEP F278 R2 — BOOK ROUND 1, LAND T002's GUARD AS A RATCHET, MIGRATE TWO HELPER GROUPS

GOAL
Book round 1's PASS and DECISION F278 D1, then land the first half of T002:
`tests/orchestration/test_durable_write_guard.py`, a ratchet that fails on any private
atomic-write helper outside `packages/common/` that it does not still list, and the first
migrations onto `durable_write` — `pingpong_job.atomic_write_text` with its three importers,
and `proposed_tasks._atomic_write` — each helper DELETED in the commit that moves its callers.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

WHY THE GUARD COMES FIRST
A migration deletes a copy that WORKED, so no behavioural test goes red when it is reverted.
The guard's `STILL_TO_MIGRATE` set is what pins each deletion: the commit that deletes a copy
removes its entry, and a revert of that commit turns the guard red. DECISION F278 D1, in this
round's `decisions.md` payload, states the whole survivor list and the order.

EVERY CALL SITE KEEPS ITS BYTES. The payload each site writes is unchanged; only the writer
changes. `pingpong_job._persist_job` gains an explicit `mkdir` because it was the one caller
relying on the deleted helper to create the directory. These tests change because the
migration forces them: `tests/orchestration/test_checkpoints.py` patched
`checkpoints._atomic_write`, which no longer exists, and now patches
`checkpoints.durable_write`; `tests/orchestration/test_task_execution.py`'s source guard
required the string `_atomic_write` in `proposed_tasks.py` and now requires `durable_write`.

TWO DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f278-r2-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f278-r2-scratch/`   The reviewer's scripts; do not edit or delete them. Put
      your own logs under `.remedy-wt/f278-r2-worker/`. All are gitignored.

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
2. `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f278-durable-writes-loud-failures`, and `git log --oneline -1` must read
   `41254292`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f278-r2-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `git branch --list 'remedy/job-*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f278-r2-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| decisions.md | 44 | 3424 | 166b63291be48f9ac98d0fed624bed585bf5366b775f5b7613daac5f8edd36bf |
| ledger.md | 2 | 3117 | c95711681a718833fd5e4ff47137c54008ba54d9e597c7a21668d1b5f734164c |
| pingpong.diff | 186 | 8741 | 07e9daa3ac7453020ebb34a27fa5f648f39254fe6031909d86c23b22df9381da |
| plan.md | 33 | 1380 | 5dcb97ba8679da99b017154cc4a3ed0a499e95dceb89058b00c5356296c88112 |
| proposed.diff | 79 | 3157 | 2bc86facd9e50cf58d334d235947c31b733a7998c5724081ab4a049697eb4376 |
| prose_slips.md | 1 | 299 | 439a26bbc8e90f0c09b193154b638d00d1c02216f243fcb5631f4cd163e8678f |
| revert_probes.py | 51 | 1981 | e16b1de085e08720c27c7c6d6a3c4da326173c852882f4f2026c1df20a7a2009 |
| test_durable_write_guard.py | 76 | 3563 | f879db26626a60097145fdc4927a7f80a90714ee542fa9edab6c9ea751554274 |

`ledger.md`, `decisions.md` and `prose_slips.md` are APPENDS by byte concatenation: the
ledger and decisions payloads begin with the single newline that separates records, and the third begins with
no newline because `.agent/prose_slips.md` already ends in one. `plan.md` is a REWRITE of
`.agent/plan.md`. `test_durable_write_guard.py` is a NEW FILE at
`tests/orchestration/test_durable_write_guard.py`, copied whole. `pingpong.diff` and
`proposed.diff` go on with `git apply` and EACH EDITS THE GUARD FILE, so each applies only
after C3: `git apply --check pingpong.diff` at `41254292` fails on the missing guard file by
design, and the reviewer checked each diff on the tree it is meant for. `revert_probes.py`
is a TOOL for G5: it is run, never applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C2, C3, C4, C5 and C6, in this order.

C1a — copy this block and the bookkeeping payloads
  `.agent/authored/f278-r2-block.md` := this block, and one
  `.agent/authored/f278-r2-<name>` for each of decisions.md, ledger.md, plan.md and
  prose_slips.md, keeping each payload's own file name. All by `shutil.copyfile`.
  Subject: `F278 R2 C1a: copy round 2 block and bookkeeping payloads into .agent/authored/`
  Its insertions are this block's line count plus 80. STOP rather than commit at 500 or more.

C1b — copy the product payloads
  One `.agent/authored/f278-r2-<name>` for each of pingpong.diff, proposed.diff,
  test_durable_write_guard.py and revert_probes.py, by `shutil.copyfile`.
  Subject: `F278 R2 C1b: copy round 2 product payloads into .agent/authored/`
  Expected insertions: 392.

C2 — THE BOOKING, one commit: append ledger.md to `.agent/live_review.md`, append
  decisions.md to `.agent/decisions.md`, append prose_slips.md to `.agent/prose_slips.md`,
  and rewrite `.agent/plan.md` := plan.md.
  Subject: `F278 R2 C2: book round 1's PASS and DECISION F278 D1`
  Expected insertions: 58 (44 decisions, 2 live review, 11 plan, 1 prose slips).

C3 — THE GUARD: copy test_durable_write_guard.py to
  `tests/orchestration/test_durable_write_guard.py` and `git add` it.
  Subject: `F278 R2 C3: add the private atomic-write guard as a ratchet`
  Expected insertions: 76.

C4 — THE PINGPONG GROUP: `git apply --check` then `git apply` pingpong.diff. It deletes
  `atomic_write_text` from `packages/orchestration/pingpong_job.py`, moves
  `checkpoints.py`, `mission_compiler.py` and `mission_state.py` onto `durable_write`,
  updates `tests/orchestration/test_checkpoints.py`, and removes the helper's entry from the
  guard's set.
  Subject: `F278 R2 C4: move the job, checkpoint and mission records onto durable_write`
  Expected insertions: 13.

C5 — PROPOSED TASKS: `git apply --check` then `git apply` proposed.diff. It deletes
  `_atomic_write` from `packages/orchestration/proposed_tasks.py`, updates the source guard
  in `tests/orchestration/test_task_execution.py`, and removes the entry from the guard's set.
  Subject: `F278 R2 C5: move proposed tasks onto durable_write`
  Expected insertions: 3.

C6 — THE HANDBACK: `.agent/handoff.md`, rewritten, its own commit, per
  `docs/agents/handback_template.md`, WITH the item-status table AGENTS.md requires — one
  row per commit and per gate. Subject: `F278 R2 C6: rewrite handoff for round 2`
  Then `git push origin feature/f278-durable-writes-loud-failures` and report its outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Report every `git apply --check` exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading.
3. The round's whole tracked path set is: the `.agent/authored/f278-r2-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/prose_slips.md`, `.agent/plan.md`,
   `tests/orchestration/test_durable_write_guard.py`, `packages/orchestration/pingpong_job.py`,
   `packages/orchestration/checkpoints.py`, `packages/orchestration/mission_compiler.py`,
   `packages/orchestration/mission_state.py`, `packages/orchestration/proposed_tasks.py`,
   `tests/orchestration/test_checkpoints.py`, `tests/orchestration/test_task_execution.py`
   and `.agent/handoff.md`. Report the list `git diff --name-only 41254292 <C6>` gives.
   Nothing under `docs/`, no other module, no other helper migrated.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no branch deletion, no
   force-push, no `git stash`, no checkout of another branch.
6. Leave `.remedy-wt/job-129b3ad7206d4f8d`, its branch and every existing stash alone. The
   worktree G5 adds goes under `.remedy-wt/`, is removed as that step's last action, and
   `git worktree list` is reported afterwards (finding R-0940).
7. DO NOT run the full suite (amend0917 rule 1); F278's one run belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C6 is written.

G1 TRANSPORT — each payload's line count, byte count and sha256 against the PAYLOADS table;
 then each `.agent/authored/f278-r2-*` copy, read with `git show <commit>:<path>` from the
 commit that added it, compared byte for byte with its source (the block copy against
 `.remedy-wt/f278-r2-block.md`). One reading per copy.

G2 THE BOOKING — at C2: each appended file equals its `41254292` bytes plus its
 payload's bytes, by strict concatenation, and `.agent/plan.md` equals plan.md; then the
 sha256 read with `git show <C2>:<path>` equals the reviewer's dry-run reading:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 427438 | d00deba9917bd06a55316ca02b116353a2e02dcc197e40cbde2db8909c3f04ed |
 | .agent/decisions.md | 1842186 | c9a02a6f2d5f9b716877d564529a4d7bda2f88a3f8121eaadbe6204e61319e15 |
 | .agent/prose_slips.md | 363591 | 1bc24fe2fc5cf7e0273d78f56d136c55d190169985e2bcdf1993a2abc0c5231f |
 | .agent/plan.md | 1380 | 5dcb97ba8679da99b017154cc4a3ed0a499e95dceb89058b00c5356296c88112 |
 And the open set by distinct id with `open_finding_ids` from `scripts/rotate_live_review.py`
 at `41254292` and at C2, with both set differences (the reviewer read 26, 26, both empty).

G3 THE PRODUCT BYTES — at C5, the sha256 of each file read with `git show <C5>:<path>`:
 | path | bytes | sha256 |
 |---|---|---|
 | tests/orchestration/test_durable_write_guard.py | 3427 | 72cab2e7073a81380d1626f48c50eb6397a376e32f85d658724e420f19c9ba57 |
 | packages/orchestration/pingpong_job.py | 193002 | b67a13c58a8069ef80030dd567a151fe0a3c67e2727c2d7f0a9cf8d934e8f194 |
 | packages/orchestration/checkpoints.py | 22340 | 49b896b169d21a5021713f51d20a8fbb69e82b49c57d785242e0548a715a57a3 |
 | packages/orchestration/mission_compiler.py | 33617 | b817772e0d825074aed3c7fc446026f9607d6af4383576fd651c695be1f1548c |
 | packages/orchestration/mission_state.py | 47639 | 30e64304b59cea9bea53fb4b6c52aae0d43ec4fd1817c52c2213884a7bdb7f25 |
 | packages/orchestration/proposed_tasks.py | 19964 | d49887a87083215ab8ecaea98e2f41a3380179e0e8382b726174cca558c27042 |
 | tests/orchestration/test_checkpoints.py | 16950 | 5548d4cabf427645d81ef086ea0449e2a68a0744ade1aa96f43d18da7cfbd995 |
 | tests/orchestration/test_task_execution.py | 708 | d29e60164a46d6cd57e09b9dfafb58c72ab2c89b0d386b1e68d101fd92635452 |

G4 THE TESTS — in the primary checkout at C5, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_durable_write_guard.py tests/orchestration/test_checkpoints.py tests/orchestration/test_task_execution.py tests/orchestration/test_mission_compiler.py tests/orchestration/test_mission_state.py tests/orchestration/test_proposed_tasks.py tests/orchestration/test_pingpong.py tests/orchestration/test_pingpong_integration.py tests/orchestration/test_resume_kill.py tests/orchestration/test_mission_e2e.py tests/storage/test_persistence.py tests/cli/test_job_commands.py tests/test_imports.py tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py tests/orchestration/test_secure_fs_durable_write.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection WITHOUT the golden path in a disposable worktree carrying
 C2 to C5 and read `559 passed, 1 skipped` at real exit code 0; report what you read. Then
 `python3 -m ruff check` over every Python path of the G3 table, real exit code 0, and
 `python3 -m apps.cli.main integrity check --json`, all five checks `pass` at `fail_count` 0.

G5 THE REVERT PROBES — `git worktree add --detach .remedy-wt/f278-r2-probe <C5>`, then
 `python3 .remedy-wt/f278-r2-payloads/revert_probes.py .remedy-wt/f278-r2-probe 41254292`
 and report its whole output. Each probe restores production files from `41254292` while
 the tests stay at C5. The reviewer read, over the same script against its own tree:
 control_before `42 passed` at exit 0;
 p1 (`pingpong_job.py` alone) `1 failed, 41 passed` at exit 1, the guard's
   `test_no_private_atomic_write_helper_outside_packages_common`;
 p2 (the pingpong group) `4 failed, 38 passed` at exit 1, that guard test and three in
   `tests/orchestration/test_checkpoints.py`;
 p3 (`proposed_tasks.py`) `2 failed, 40 passed` at exit 1, that guard test and
   `TestModularArchitectureGuards::test_storage_access_through_helpers`;
 control_after `42 passed` at exit 0, with every `restored clean` line `True`.
 Then `git worktree remove --force .remedy-wt/f278-r2-probe`, `git worktree prune`, and
 report `git worktree list`.

G6 TREE AND PUSH — after C6, in your reply: `git status --porcelain`, empty;
 `git log --oneline -n 8`, showing C6 back to C1a and then `41254292`; `git worktree list`,
 the primary checkout and `.remedy-wt/job-129b3ad7206d4f8d` only; the push's real outcome;
 and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: the state block, the per-commit
changed-files table with the insertion count you MEASURED beside the one this block
expected, every gate's real output and exit code, the ITEM-STATUS TABLE, the deviations,
and the next expected action. Your Session section reads SESSION 1 of feature F278,
round 2, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review
of round 2, then T002's boolean helpers in `real_test_execution`, `self_dogfood_execution`
and `token_economy`. State the open-findings count, 26, and the operator-questions count, 0.
