STEP F263 R4 — BOOK ROUND 3 AND LAND T002: `remedy absorb`

GOAL
Book round 3's PASS and DECISION F263 D4, then land T002: `remedy absorb`, its catalog entry,
its visible help slot after `runtime` and its bare form, over `human_change.absorb_job` — the
one path that certifies a hand edit and re-bases a job's last known state, and that T003's run
safe points will call too.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

WHAT THE COMMAND DOES (DECISION F263 D4, the decisions.md payload)
It selects every persisted job whose `repo_path` resolves to the repository it runs in and whose
state is neither `failed` nor `cancelled` (with `--job`, only that one), skips a job whose
worktree lock a live process holds, and for every other job certifies the change since the
job's last known state and moves that state — the checkpoint ref and `target_last_known` — to
the tree the human left. It writes no file in the repository. Three tests pin the visible group
set and change with it: `tests/test_command_catalog.py`, `tests/cli/test_cli_ux.py` (the group
count becomes 32) and a docstring in `tests/cli/test_golden_path.py`; the new CLI module joins
the import-reachability allowlist.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f263-r4-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f263-r4-scratch/`   The reviewer's scripts; do not edit or delete them.
  `.remedy-wt/f263-r4-worker/`    YOURS for logs and scripts. All three are gitignored.

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
2. `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f263-human-change-absorption`, and `git log --oneline -1` must read `d5fe145f`.
   Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f263-r4-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `git branch --list 'remedy/job-*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f263-r4-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| ledger.md | 2 | 2244 | fb234ec8604bfb69f5d41e4db8e0c56612640e4a7e4975c977c0d1a84172c16f |
| decisions.md | 41 | 3115 | ad92fce8e4f1cc22c1e84ae166178bedba96345f8211bd57100553e3839952eb |
| plan.md | 30 | 1163 | 11b32fa937b036ca348b8bd0472ea49a37cc522aac7ce3b832881750f9a4df7d |
| product.diff | 185 | 9570 | 7a275e2c24c5188e71f29a7c98e50087195bfb3e46d531ed8d09cd874c8bf130 |
| absorb_cmd.py | 98 | 4118 | a96e0f27501a0abe0a76537f07069dfb9f4b4bb28a8b5a7e3f12cbc5bf367bd1 |
| pins.diff | 65 | 3094 | 83bc668ecdfb6183d7d7dda97ce768bfffd1ca00019644aeb7c8c02b5a0fa47a |
| test_absorb_cmd.py | 167 | 6800 | 8ba2357b44e83fc8f122185300ad36dc576c08a7ade495ffc8039714dceab3b0 |
| mutations.py | 81 | 2936 | 09dcbd3a292b35c0e9a1d28cabfeafbeaee02aecb673e2bfe84265c5bfaf84ae |

`ledger.md` and `decisions.md` are APPENDS by byte concatenation: each begins with the single
newline that separates records, because `.agent/live_review.md` and `.agent/decisions.md` each
end in exactly one newline. `plan.md` is a REWRITE of `.agent/plan.md`. `absorb_cmd.py` is a
NEW FILE at `apps/cli/commands/absorb_cmd.py` and `test_absorb_cmd.py` a NEW FILE at
`tests/cli/test_absorb_cmd.py`, each copied whole. The `.diff` files go on with `git apply`; the
reviewer generated both from a tree at `d5fe145f` and applied them to a fresh worktree there,
every `git apply --check` and `git apply` at real exit code 0. `product.diff` edits
`packages/orchestration/human_change.py`, `packages/orchestration/worktrees.py`,
`apps/cli/command_catalog.py`, `apps/cli/grouped.py`, `apps/cli/commands/__init__.py` and
`tests/orchestration/import_reachability_allowlist.txt`; `pins.diff` edits
`tests/test_command_catalog.py`, `tests/cli/test_cli_ux.py` and `tests/cli/test_golden_path.py`.
`mutations.py` is a TOOL for G5: it is run, never applied to a tracked file.

BUNDLE — the commits are C1a, C1b, C1c, C2, C3 and C4, in this order.

C1a — copy this block and the bookkeeping payloads
  `.agent/authored/f263-r4-block.md` := this block, and one `.agent/authored/f263-r4-<name>`
  for each of ledger.md, decisions.md and plan.md. All by `shutil.copyfile`.
  Subject: `F263 R4 C1a: copy round 4 block and bookkeeping payloads into .agent/authored/`
  Its insertions are this block's line count plus 73. STOP rather than commit at 500 or more.

C1b — copy the product payloads: product.diff, absorb_cmd.py and pins.diff.
  Subject: `F263 R4 C1b: copy round 4 product payloads into .agent/authored/`
  Expected insertions: 348.

C1c — copy the test payloads: test_absorb_cmd.py and mutations.py.
  Subject: `F263 R4 C1c: copy round 4 test payloads into .agent/authored/`
  Expected insertions: 248.

C2 — THE BOOKING, one commit: append ledger.md to `.agent/live_review.md`, append
  decisions.md to `.agent/decisions.md`, and rewrite `.agent/plan.md` := plan.md.
  Subject: `F263 R4 C2: book round 3's PASS and DECISION F263 D4`
  Expected insertions by `git show --numstat`: 41 decisions.md, 2 live_review.md, 8 plan.md.

C3 — THE COMMAND, one commit, because the product, the pinned tests it moves and the tests that
  verify it stand or fall together: `git apply --check` then `git apply` for product.diff and
  pins.diff in that order, then copy absorb_cmd.py to `apps/cli/commands/absorb_cmd.py` and
  test_absorb_cmd.py to `tests/cli/test_absorb_cmd.py`, and `git add` every path — an untracked
  module fails `integrity check`'s `relevant_untracked`.
  Subject: `F263 R4 C3: add remedy absorb over the one absorb path`
  Expected insertions: 20 command_catalog.py, 2 commands/__init__.py, 98 absorb_cmd.py,
  3 grouped.py, 39 human_change.py, 22 worktrees.py, 167 test_absorb_cmd.py, 6 test_cli_ux.py,
  2 test_golden_path.py, 1 import_reachability_allowlist.txt, 3 test_command_catalog.py.

C4 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`,
  WITH the item-status table AGENTS.md requires — one row per commit and per gate.
  Subject: `F263 R4 C4: rewrite handoff for round 4`
  Then `git push origin feature/f263-human-change-absorption` and report its real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Report every `git apply --check` exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f263-r4-*` copies,
   `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, the six paths
   product.diff edits, the three paths pins.diff edits, `apps/cli/commands/absorb_cmd.py`,
   `tests/cli/test_absorb_cmd.py` and `.agent/handoff.md`. Report the list
   `git diff --name-only d5fe145f <C4>` gives. Nothing under `docs/`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no branch deletion, no
   force-push, no `git stash`, no checkout of another branch.
6. Leave `.remedy-wt/job-129b3ad7206d4f8d`, `.remedy-wt/job-e7268925db3a4831`,
   `.remedy-wt/job-e7a145761bf04f86`, their branches and every existing stash alone. The
   worktree G5 adds goes under `.remedy-wt/`, is removed as that step's last action, and
   `git worktree list` is reported afterwards (finding R-0940). Do NOT run `remedy absorb` in
   the primary checkout: its jobs are real, and absorbing into them is not this round's work.
7. DO NOT run the full suite (amend0917 rule 1); F263's one run belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C4 is written.

G1 TRANSPORT — each payload's line count, byte count and sha256 against the PAYLOADS table;
 then each `.agent/authored/f263-r4-*` copy, read with `git show <commit>:<path>` from the
 commit that added it, compared byte for byte with its source (the block copy against
 `.remedy-wt/f263-r4-block.md`). One reading per copy.

G2 THE BOOKING — at C2: each appended file equals its `d5fe145f` bytes plus its payload's
 bytes, by strict concatenation, and `.agent/plan.md` equals plan.md; then the sha256 read
 with `git show <C2>:<path>` equals the reviewer's simulated reading:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 379930 | 1a669d064f7c6b410289bb7d7ea9ff0f3b5759c5631b150d72b4340f35c8108c |
 | .agent/decisions.md | 1886102 | d2f6f01249ee5cf5a398c827a6aec7ab12678f025b15fdc5a482d69e80e50fd6 |
 | .agent/plan.md | 1163 | 11b32fa937b036ca348b8bd0472ea49a37cc522aac7ce3b832881750f9a4df7d |
 And the open set by distinct id with `open_finding_ids` from `scripts/rotate_live_review.py`
 at `d5fe145f` and at C2, with both set differences (the reviewer read 28, 28, both empty).

G3 THE PRODUCT BYTES — at C3, the sha256 of each file read with `git show <C3>:<path>`:
 | path | bytes | sha256 |
 |---|---|---|
 | packages/orchestration/human_change.py | 13476 | a8d2e52ad1f901981c79bbf35b4b65ac63f0bca4862b26d2a44c9a4050edb6f2 |
 | packages/orchestration/worktrees.py | 32486 | f60edc5e59e7544dce3faff9b91d835677587e51270d61880c90da61359141db |
 | apps/cli/command_catalog.py | 111748 | ab3cb70b386def9d8ed6ab4a0ebe9d84c397095f9ec4c5fd437a2d22d46f82fa |
 | apps/cli/grouped.py | 28934 | b6bcf7dde1158b31783af3c33e8ba693eb4a132380493875141d408a68dac329 |
 | apps/cli/commands/__init__.py | 2065 | ac8cfcb63b70b50850bcbcf2256078caa6d757c487b9637295c4db330ded8c5a |
 | tests/orchestration/import_reachability_allowlist.txt | 9932 | fcb6cdc1dc8c3b9c0ce2548aaa1ba2349ef6eaa8caa70c28129f6c05439266e3 |
 | tests/test_command_catalog.py | 22526 | 1f03949b66afe54dfc2a31a2a62f2333e68030e8a5acf8a759e04fffa4047e30 |
 | tests/cli/test_cli_ux.py | 39149 | a74a39b3fdd97e8841ed86c459cfd9b505f87fd096938d8097965628f8eb82fe |
 | tests/cli/test_golden_path.py | 34675 | 633a0384d1fa63d56960870de63e8f3d1657c17b2425db58576906fc9733673d |
 | apps/cli/commands/absorb_cmd.py | 4118 | a96e0f27501a0abe0a76537f07069dfb9f4b4bb28a8b5a7e3f12cbc5bf367bd1 |
 | tests/cli/test_absorb_cmd.py | 6800 | 8ba2357b44e83fc8f122185300ad36dc576c08a7ade495ffc8039714dceab3b0 |

G4 THE TESTS AND THE LINT — in the primary checkout at C3, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/cli/test_absorb_cmd.py tests/orchestration/test_human_change.py tests/orchestration/test_human_change_evidence.py tests/test_command_catalog.py tests/test_grouped_cli.py tests/test_help_renderer.py tests/cli/test_cli_ux.py tests/cli/test_json_contract.py tests/cli/test_exit_codes.py tests/cli/test_advertised_commands.py tests/cli/test_worker_facade_cmd.py tests/docs/ tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/orchestration/test_job_worktree_integrity.py tests/orchestration/test_worktrees.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/ui_server/test_command_channel.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection WITHOUT the golden path, serially, in a disposable worktree
 carrying C2 and C3 and read `1694 passed, 2 skipped` at real exit code 0; report what you
 read. Then `bash -c 'python3 -m ruff check .; echo "REAL_EXIT=$?"'` over the whole
 repository, which must read `All checks passed!` at exit 0, and
 `python3 -m apps.cli.main integrity check --json`, all five checks `pass` at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f263-r4-mut <C3>`, then
 `python3 -B .remedy-wt/f263-r4-payloads/mutations.py .remedy-wt/f263-r4-mut` and report its
 whole output. The script runs `tests/cli/test_absorb_cmd.py`. The reviewer read, against its
 own tree carrying C2 and C3:
 control_before `11 passed` at exit 0;
 m1 (a running job's record rewritten) 1 failed at exit 1;
 m2 (the lock probe never sees a holder) 2 failed at exit 1;
 m3 (the re-base leaves the checkpoint ref behind) 1 failed at exit 1;
 m4 (the re-base is never persisted) 2 failed at exit 1;
 m5 (every repository's jobs absorbed) 1 failed at exit 1;
 m6 (`--job` ignored) 1 failed at exit 1;
 m7 (failed and cancelled jobs absorbed) 1 failed at exit 1;
 m8 (a bare `remedy absorb` prints help instead of running) 1 failed at exit 1;
 control_after `11 passed` at exit 0, with every `restored byte-identical` line `True`.
 Then `git worktree remove --force .remedy-wt/f263-r4-mut`, `git worktree prune`, and
 report `git worktree list`.

G6 TREE AND PUSH — after C4, in your reply: `git status --porcelain`, empty;
 `git log --oneline -n 7`, showing C4, C3, C2, C1c, C1b, C1a and then `d5fe145f`;
 `git worktree list`, the primary checkout and the three `.remedy-wt/job-*` worktrees only;
 the push's real outcome; and `gh pr list --state open --json
 number,headRefName,baseRefName,isDraft`, EMPTY.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`: the state block, the per-commit
changed-files table with the insertion count you MEASURED beside the one this block
expected, every gate's real output and exit code, the authored-text proofs, the ITEM-STATUS
TABLE, the deviations, and the next expected action. Your Session section reads SESSION 1 of
feature F263, round 4, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review
of round 4, then T003 — absorption at every safe point of a run and before every apply,
deleting the drift error it replaces. State the open-findings count, 28, and the
operator-questions count, 0.
