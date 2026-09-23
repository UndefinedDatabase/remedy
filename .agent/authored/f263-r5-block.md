STEP F263 R5 — BOOK ROUND 4 AND LAND T003's RUN HALF: a git job absorbs at every safe point

GOAL
Book round 4's PASS and DECISION F263 D5, then land the run half of T003: a git job absorbs a
hand edit at every safe point — the episode start, before each task, inside the task's own run,
where the pre-apply guard stood and after each applied task — and keeps running; the two drift
blocks are deleted for it; every check is counted and timed; and the demo case of T2_F263.md
runs end to end. A non-git copy job keeps its guard.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

THE OLD BEHAVIOUR IS SHOWN FIRST
T2_F263.md's Orchestrator brief: T003 deletes an existing error path, so its red proof must
show the OLD behaviour — the drift error — before the new one. G5's first probe puts
`packages/orchestration/pingpong_job.py` back to its bytes at `a2361d9a` and runs the new demo
tests against it; the reviewer read them fail with `target_repo_mutated_during_job`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f263-r5-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f263-r5-scratch/`   The reviewer's scripts; do not edit or delete them.
  `.remedy-wt/f263-r5-worker/`    YOURS for logs and scripts. All three are gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, `cd <dir> && git ...`, and multi-operation
one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe pytest.
Use `git -C <path>` rather than `cd`. Use `python3 - <<'PY'` for counting, hashing and
copying (`shutil.copyfile`). A heredoc containing a dollar-brace or a brace beside a quote is
refused: write such a script to a file under your own directory and run the file.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f263-human-change-absorption`, and `git log --oneline -1` must read `a2361d9a`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f263-r5-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `git branch --list 'remedy/job-*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f263-r5-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.md | 2 | 2015 | 6b63c46798164379eb28e56983a60b6c728ea22ea96f10ad7f7b0463f23c15e6 |
| decisions.md | 37 | 2897 | ba95a41c812aa49260003ae30eb3957109fc6795ad44b30fbbc89b60f456e81a |
| plan.md | 30 | 1163 | 9e262b13c87c1e2c7d7cfbd3b785344dc18a3ebb14124c74d8ea2c7e22a12a35 |
| mutations.py | 86 | 3318 | c194687b356af4af8128840a3d41650babab47af70cb781f6f89bb1612cace09 |
| product.diff | 218 | 10604 | d2704c8ef7e84a16f1e7f2c8d1ed7927260d990ab03bd8d1af54934f43f75a25 |
| test_human_change_in_run.py | 175 | 7082 | 22b6d8e9ebac1af5e89a39009401e8333902544abf37b1bb02d159846af19adf |

`ledger.md` and `decisions.md` are APPENDS by byte concatenation: each begins with the single
newline that separates records, because `.agent/live_review.md` and `.agent/decisions.md` each
end in exactly one newline. `plan.md` is a REWRITE of `.agent/plan.md`.
`test_human_change_in_run.py` is a NEW FILE at `tests/orchestration/test_human_change_in_run.py`,
copied whole. `product.diff` edits `packages/orchestration/pingpong_job.py` alone and goes on
with `git apply`; the reviewer generated it from a tree at `a2361d9a` and applied it to a fresh
worktree there, `git apply --check` and `git apply` at real exit code 0. `mutations.py` is a TOOL
for G5: it is run, never applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C2, C3 and C4, in this order.

C1a — copy this block and the bookkeeping payloads with the tool
  `.agent/authored/f263-r5-block.md` := this block, and one `.agent/authored/f263-r5-<name>`
  for each of ledger.md, decisions.md, plan.md and mutations.py. All by `shutil.copyfile`.
  Subject: `F263 R5 C1a: copy round 5 block, bookkeeping payloads and red-proof tool`
  Its insertions are this block's line count plus 155. STOP rather than commit at 500 or more.

C1b — copy the product payloads: product.diff and test_human_change_in_run.py.
  Subject: `F263 R5 C1b: copy round 5 product payloads into .agent/authored/`
  Expected insertions: 393.

C2 — THE BOOKING, one commit: append ledger.md to `.agent/live_review.md`, append
  decisions.md to `.agent/decisions.md`, and rewrite `.agent/plan.md` := plan.md.
  Subject: `F263 R5 C2: book round 4's PASS and DECISION F263 D5`
  Expected insertions by `git show --numstat`: 37 decisions.md, 2 live_review.md, 9 plan.md.

C3 — THE RUN HALF, one commit: `git apply --check` then `git apply` product.diff, copy
  test_human_change_in_run.py to `tests/orchestration/test_human_change_in_run.py`, and
  `git add` both paths.
  Subject: `F263 R5 C3: absorb human changes at every safe point of a git job's run`
  Expected insertions: 115 pingpong_job.py (25 deletions), 175 test_human_change_in_run.py.

C4 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`,
  WITH the item-status table AGENTS.md requires — one row per commit and per gate.
  Subject: `F263 R5 C4: rewrite handoff for round 5`
  Then `git push origin feature/f263-human-change-absorption` and report its real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Report the `git apply --check` exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f263-r5-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`,
   `packages/orchestration/pingpong_job.py`, `tests/orchestration/test_human_change_in_run.py`
   and `.agent/handoff.md`. Report the list `git diff --name-only a2361d9a <C4>` gives.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no branch deletion, no
   force-push, no `git stash`, no checkout of another branch.
6. Leave `.remedy-wt/job-129b3ad7206d4f8d`, `.remedy-wt/job-e7268925db3a4831`,
   `.remedy-wt/job-e7a145761bf04f86`, their branches and every existing stash alone. The
   worktree G5 adds goes under `.remedy-wt/`, is removed as that step's last action, and
   `git worktree list` is reported afterwards (finding R-0940). Run no `remedy` job in the
   primary checkout.
7. DO NOT run the full suite (amend0917 rule 1); F263's one run belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C4 is written.

G1 TRANSPORT — each payload's line count, byte count and sha256 against the PAYLOADS table;
 then each `.agent/authored/f263-r5-*` copy, read with `git show <commit>:<path>` from the
 commit that added it, compared byte for byte with its source (the block copy against
 `.remedy-wt/f263-r5-block.md`). One reading per copy.

G2 THE BOOKING — at C2: each appended file equals its `a2361d9a` bytes plus its payload's
 bytes, by strict concatenation, and `.agent/plan.md` equals plan.md; then the sha256 read
 with `git show <C2>:<path>` equals the reviewer's simulated reading:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 381945 | aec166cabaf5e3f9b046977a764f3fa348a298cd9691d5e8746f24693ed24856 |
 | .agent/decisions.md | 1888999 | f7f52c3191ebe365bedeed1a0792903626dd3d3f84b3924318bb905ed099d21f |
 | .agent/plan.md | 1163 | 9e262b13c87c1e2c7d7cfbd3b785344dc18a3ebb14124c74d8ea2c7e22a12a35 |
 And the open set by distinct id with `open_finding_ids` from `scripts/rotate_live_review.py`
 at `a2361d9a` and at C2, with both set differences (the reviewer read 28, 28, both empty).

G3 THE PRODUCT BYTES — at C3, read with `git show <C3>:<path>`:
 | path | bytes | sha256 |
 |---|---|---|
 | packages/orchestration/pingpong_job.py | 199695 | 2e987b2f1c452d49a30091af22e0d96c9df2696384afa3d8014a03ebec7e9568 |
 | tests/orchestration/test_human_change_in_run.py | 7082 | 22b6d8e9ebac1af5e89a39009401e8333902544abf37b1bb02d159846af19adf |

G4 THE TESTS AND THE LINT — in the primary checkout at C3, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_human_change_in_run.py tests/orchestration/test_human_change.py tests/orchestration/test_human_change_evidence.py tests/cli/test_absorb_cmd.py tests/orchestration/test_job_task_runner.py tests/orchestration/test_job_worktree_integrity.py tests/orchestration/test_job_worktree_handoff.py tests/orchestration/test_job_worktree_integration.py tests/cli/test_do_evidence_package.py tests/orchestration/test_job_stop_integration.py tests/orchestration/test_job_budgets.py tests/orchestration/test_pingpong_job_dod_gate.py tests/orchestration/test_pingpong_job_hunk_ledger.py tests/orchestration/test_job_run_refs.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection WITHOUT the golden path, serially, in a disposable worktree
 carrying C2 and C3 and read `699 passed, 2 skipped` at real exit code 0; report what you
 read. Then `bash -c 'python3 -m ruff check .; echo "REAL_EXIT=$?"'` over the whole
 repository, which must read `All checks passed!` at exit 0, and
 `python3 -m apps.cli.main integrity check --json`, all five checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f263-r5-mut <C3>`, then
 `python3 -B .remedy-wt/f263-r5-payloads/mutations.py .remedy-wt/f263-r5-mut a2361d9a` and
 report its whole output. It runs `tests/orchestration/test_human_change_in_run.py` and
 `tests/cli/test_do_evidence_package.py`. The reviewer read, against its own tree carrying C2
 and C3:
 control_before `14 passed` at exit 0;
 old_runner (pingpong_job.py at `a2361d9a`) 5 failed at exit 1, its assertion lines naming
   `target_repo_mutated_during_job` — the OLD behaviour;
 m1 (the drift guard back for git jobs) 5 failed at exit 1;
 m2 (the run's own safe points do not check) 1 failed at exit 1;
 m3 (checks not counted) 1 failed at exit 1;
 m4 (a failed check does not block before the apply) 1 failed at exit 1;
 m5 (an old job gets no last known state) 1 failed at exit 1;
 m6 (no guard record for a git job) 1 failed at exit 1;
 control_after `14 passed` at exit 0, with every `restored byte-identical` line `True`.
 Then `git worktree remove --force .remedy-wt/f263-r5-mut`, `git worktree prune`, and
 report `git worktree list`.

G6 TREE AND PUSH — after C4, in your reply: `git status --porcelain`, empty;
 `git log --oneline -n 6`, showing C4, C3, C2, C1b, C1a and then `a2361d9a`;
 `git worktree list`, the primary checkout and the three `.remedy-wt/job-*` worktrees only;
 the push's real outcome; and `gh pr list --state open --json
 number,headRefName,baseRefName,isDraft`, EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: the state block, the per-commit
changed-files table with the insertion count you MEASURED beside the one this block
expected, every gate's real output and exit code, the authored-text proofs, the ITEM-STATUS
TABLE, the deviations, and the next expected action. Your Session section reads SESSION 1 of
feature F263, round 5, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review
of round 5, then T003's apply half — `job apply` and `do run --apply` absorbing before a
single file is copied. State the open-findings count, 28, and the operator-questions count, 0.
