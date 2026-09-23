STEP F279 R6 — T004, THE REPORT HALF: `remedy doctor toolchain`, and the two-Python matrix held

GOAL
Book round 5's PASS, record DECISION F279 D6, and land T004's report half:
`packages/orchestration/toolchain.py` and the `doctor.toolchain` command, which show each pinned
tool's installed, pinned and newest version — the newest from the package index when allowed,
"unknown" otherwise and never a guessed number — and a test that holds the CI matrix to
exactly two Python versions, the first the floor. Each new behaviour carries a red proof.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

WHAT THE REVIEWER FOUND WHILE AUTHORING (DECISION F279 D6, the decisions.diff payload)
`remedy doctor core` promises no network, so the report is a new command beside it, with
`--offline` to skip the index. The new module joins the entry points' import closure, so the
allowlist gains its line (the allowlist.diff payload), and
`tests/cli/test_worker_facade_cmd.py` pins that module's handler set by equality, so its
expected set gains `doctor.toolchain` in the same commit (the test_worker_facade_cmd.diff
payload); without either, a guard goes red.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f279-r6-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f279-r6-scratch/`   YOURS for logs and scripts. Each is gitignored; create
      the scratch directory if it is absent.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, `cd <dir> && git ...`, and multi-operation
one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe pytest.
Use `git -C <path>` rather than `cd`. An inline heredoc with braces or a dollar sign is often
refused too: write any helper script to a file under your scratch directory and run the file.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f279-configuration-toolchain-truth`, and `git log --oneline -1` must read
   `86e12317`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f279-r6-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `git stash list | head -1` as found.

PAYLOADS — under `.remedy-wt/f279-r6-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| allowlist.diff | 12 | 586 | 4db2f64ccc9ae590addd89ea2a0d85fafb24f0cc6a5fe37c27f56d45c581c8e7 |
| command_catalog.diff | 27 | 1241 | 6d615f164d78f5b40ebe4906c83748d31ad32281b4664009f9109131b339a758 |
| decisions.diff | 36 | 2646 | cccc087f32ecc5e48f998157c19a8698020e55cdc158a9ab9b992da5760f7ab7 |
| ledger.diff | 10 | 6330 | 096065e335b5e710bdba9b1564d1b8ce0d726ab5d51035930879d1a51efed9c6 |
| mutations.py | 65 | 2754 | 755086939aa30f0edd1e152ae286102869461aaa6c60249985f894eab39b5af2 |
| plan.md | 31 | 1249 | d828e60c61c901f0cc720d709ef1bb819b17230c7136992b20242cb65d85e363 |
| test_ci_workflow.diff | 26 | 1326 | 2898e29ed4ea0cf75a436b5ae365b6ec1e35ff81b25e5df39175d3baaecffc11 |
| test_toolchain.py | 103 | 4309 | 72b7eee658dba5619d027147dfcbc7d46c1d4c74fdf36b1dfa6103852f8a585b |
| test_worker_facade_cmd.diff | 13 | 636 | 40ba79865b433e947a7478baecf16ba1b129ce55ec12c22d057f8f188f38ae2d |
| toolchain.py | 107 | 3992 | c854f24448029c004f73846619402e5f0ab10ed6453751b146807b2cdf2329a9 |
| worker_facade_cmd.diff | 40 | 1977 | 3b83c5407e62b6ccc25084458803798592bb5243cd83877d5cf8d486bd5226cf |

`plan.md` is a REWRITE of `.agent/plan.md`. `toolchain.py` is a NEW FILE at
`packages/orchestration/toolchain.py` and `test_toolchain.py` a NEW FILE at
`tests/orchestration/test_toolchain.py`, each copied whole. Every `.diff` goes on with
`git apply`; the reviewer generated each from a tree at `86e12317` and applied all of them, in
the commit order below, to a fresh worktree at `86e12317` with `git apply --check` then
`git apply`, every one at real exit code 0. `ledger.diff` appends round 5's `Gate:` entry and
`decisions.diff` appends DECISION F279 D6. `mutations.py` is a TOOL for G5, never applied.

BUNDLE — the commits are C1a, C1b, C2, C3 and C4, in this order. The copies are two commits
because together with this block they exceed the 500-line cap.

C1a — copy this block and the bookkeeping payloads
  `.agent/authored/f279-r6-block.md` := this block, and one `.agent/authored/f279-r6-<name>`
  for each of ledger.diff, plan.md and decisions.diff, keeping each payload's own file name.
  All by `shutil.copyfile`.
  Subject: `F279 R6 C1a: copy round 6 block and bookkeeping payloads into .agent/authored/`
  Its insertions are this block's line count plus 77. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C1b — copy the product payloads
  `.agent/authored/f279-r6-<name>` for each of toolchain.py, test_toolchain.py,
  worker_facade_cmd.diff, command_catalog.diff, allowlist.diff, test_ci_workflow.diff,
  test_worker_facade_cmd.diff and mutations.py, by `shutil.copyfile`.
  Subject: `F279 R6 C1b: copy round 6 product payloads into .agent/authored/`
  Expected insertions: 393.

C2 — THE BOOKKEEPING, one commit (amend0917-throughput rule 4), in this order:
   1. `git apply` ledger.diff     → `.agent/live_review.md`
   2. rewrite `.agent/plan.md` := plan.md
   3. `git apply` decisions.diff  → `.agent/decisions.md`
  Subject: `F279 R6 C2: book round 5's PASS and record DECISION F279 D6`
  Expected insertions by `git show --numstat`: 28 decisions.md, 2 live_review.md, 7 plan.md.

C3 — THE REPORT, ITS COMMAND AND ITS GUARDS in one commit, because the tests verify them
  Copy toolchain.py and test_toolchain.py to their paths and `git add` both — an untracked file
  fails `integrity check`'s `relevant_untracked` — then `git apply` worker_facade_cmd.diff,
  command_catalog.diff, allowlist.diff, test_ci_workflow.diff and test_worker_facade_cmd.diff.
  Subject: `F279 R6 C3: add remedy doctor toolchain and hold the CI matrix to two Pythons`
  Expected insertions: 16 command_catalog.py, 24 worker_facade_cmd.py, 107 toolchain.py,
  1 test_worker_facade_cmd.py, 1 import_reachability_allowlist.txt, 15 test_ci_workflow.py,
  103 test_toolchain.py.

C4 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F279 R6 C4: rewrite handoff for round 6`
  Then `git push origin feature/f279-configuration-toolchain-truth`. Do NOT create a pull
  request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading. F279's one
   declared oversize commit was round 1's C5; there is no second.
3. The round's whole tracked path set is: the `.agent/authored/f279-r6-*` copies,
   `.agent/live_review.md`, `.agent/plan.md`, `.agent/decisions.md`,
   `packages/orchestration/toolchain.py`, `tests/orchestration/test_toolchain.py`,
   `apps/cli/commands/worker_facade_cmd.py`, `apps/cli/command_catalog.py`,
   `tests/orchestration/import_reachability_allowlist.txt`,
   `tests/orchestration/test_ci_workflow.py`, `tests/cli/test_worker_facade_cmd.py` and
   `.agent/handoff.md`. Report the list you measure with `git diff --name-only 86e12317 HEAD`
   after C4. Do NOT touch `.agent/prose_slips.md`, `.agent/candidates.md`,
   `.agent/operator_questions.md`, `.agent/context.md`, `.github/workflows/ci.yml`,
   `docs/roadmap/**`, or any module not in that list.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash` — the stash list is shared by every
   worktree of this repository.
6. Leave `.remedy-wt/job-129b3ad7206d4f8d`, `.remedy-wt/job-e7268925db3a4831`, their branches
   and every existing stash alone. The worktree G5 adds goes under `.remedy-wt/`, is removed
   as that step's last action, and `git worktree list` is reported afterwards (R-0940).
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run
   and F279's belongs to its closure. Run G4 serially, never with `-n`.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C4 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f279-r6-*` copy byte for
 byte with its source (the block copy against `.remedy-wt/f279-r6-block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE BOOKKEEPING — at C2, the sha256 of each file below, read with `git show <C2>:<path>`,
 equals the reviewer's simulated reading:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 384675 | ee7a9ca8fcfb6fe4aeeb37d5199815cb3f4d7b09f7772c5691dab9378da353b0 |
 | .agent/plan.md | 1249 | d828e60c61c901f0cc720d709ef1bb819b17230c7136992b20242cb65d85e363 |
 | .agent/decisions.md | 1872202 | 59cdbf56cc3b5ea972f24a81370f0c32abbd2849acb4c127837d9dd058f8c12c |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `86e12317` and at C2, with the set
 difference in both directions (the reviewer read 26 and 26, both differences empty); the
 count of lines beginning `Gate: F279 R5 — ` at `86e12317` and at C2 (the reviewer read 0 and
 1); and `git diff --name-only <C1b> <C2>`, which must name exactly the paths C2 lists.

G3 THE REPORT — at C3, `git diff --name-only <C2> <C3>` names exactly the paths C3 lists, and
 the sha256 of each, read with `git show <C3>:<path>`, equals the reviewer's simulated reading:
 | path | bytes | sha256 |
 |---|---|---|
 | packages/orchestration/toolchain.py | 3992 | c854f24448029c004f73846619402e5f0ab10ed6453751b146807b2cdf2329a9 |
 | tests/orchestration/test_toolchain.py | 4309 | 72b7eee658dba5619d027147dfcbc7d46c1d4c74fdf36b1dfa6103852f8a585b |
 | apps/cli/commands/worker_facade_cmd.py | 21424 | fc1aafb6f048aa9c41c786208e15f783079a33d003b86e5f4627743f587551c2 |
 | apps/cli/command_catalog.py | 110896 | a34066026a9d44a7c88b4ad446fbf33e0544d9c32029c85b35d43846513f1631 |
 | tests/orchestration/import_reachability_allowlist.txt | 9867 | 56a7fd7d5cb82648b7917a304633efed53716a54929cc186484688de948a3f66 |
 | tests/orchestration/test_ci_workflow.py | 5019 | 2afefc40c7eeffdc045ac6aa3d02b218e2fc4865e1fa79d19666a847ef95a8e8 |
 | tests/cli/test_worker_facade_cmd.py | 33678 | 8047f6e8885340e1dd1ed16523fa4918fec4c8887b11aa877971c53329ed0bf1 |

G4 THE TESTS — in the primary checkout at C3, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_toolchain.py tests/orchestration/test_ci_workflow.py tests/orchestration/test_toolchain_pins.py tests/cli/test_worker_facade_cmd.py tests/test_command_catalog.py tests/cli/test_command_catalog.py tests/cli/test_cli_ux.py tests/cli/test_exit_codes.py tests/cli/test_advertised_commands.py tests/cli/test_json_contract.py tests/cli/test_job_refusal_envelope.py tests/test_grouped_cli.py tests/test_help_renderer.py tests/docs/ tests/ui_contracts/test_humanize_catalog.py tests/orchestration/test_dead_command_check.py tests/cli/test_product_spine.py tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py tests/orchestration/test_integrity_gate.py tests/test_ble001_ratchet.py tests/orchestration/test_live_review_rotation.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_self_use_generator.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path inside a disposable worktree
 carrying C2 and C3 and read `1718 passed, 2 skipped` at real exit code 0; the primary
 checkout carries the UI toolchain a worktree lacks, so a skip may pass there. Report what
 you read. Then `python3 -m ruff check` over the Python paths C3 lists, real exit code 0;
 `python3 -m apps.cli.main integrity check --json`, which must read every check `pass` at
 `fail_count` 0; `python3 -m apps.cli.main doctor toolchain --offline`, whose table you paste;
 and `python3 -m apps.cli.main integrity block .remedy-wt/f279-r6-block.md`, which the
 reviewer ran on this block before emitting it and read every item OK at exit 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f279-r6-mut <C3>`, then
 `python3 -B .remedy-wt/f279-r6-payloads/mutations.py .remedy-wt/f279-r6-mut` and report its
 whole output. The script asserts each FROM occurs exactly once, applies it, runs the affected
 test files under `python3 -B`, restores the bytes, and runs an unmutated control first and
 last. The reviewer read, over the same script against its own tree carrying C2 and C3:
 control_before `21 passed` at exit 0;
 m1 (offline reads "0") 2 failed at exit 1, at
   `test_offline_and_an_empty_answer_both_read_unknown_never_a_number` and
   `TestTheCommand::test_offline_json_names_every_tool_with_three_columns`;
 m2 (a failed fetch reads "0") 2 failed at exit 1, at both parameters of
   `TestTheIndexFetch::test_any_fetch_failure_reads_unknown`;
 m3 (the dev extra dropped) 4 failed at exit 1, at
   `test_the_report_covers_the_runtime_dependencies_and_the_dev_extra`,
   `test_the_three_columns_come_from_their_three_sources`,
   `TestTheCommand::test_offline_json_names_every_tool_with_three_columns` and
   `TestTheCommand::test_text_mode_prints_a_header_and_one_line_per_tool`;
 m4 (`--offline` ignored) 1 failed at exit 1, at
   `TestTheCommand::test_offline_json_names_every_tool_with_three_columns` — this one mutation
   lets the unpatched text-mode test reach the package index, which is the mutation's effect;
 m5 (a third Python in the matrix) 2 failed at exit 1, at
   `test_hosted_workflow_runs_the_floor_and_a_current_interpreter` and
   `test_hosted_workflow_matrix_names_exactly_the_floor_and_one_current_python`;
 control_after `21 passed` at exit 0.
 Then `git worktree remove --force .remedy-wt/f279-r6-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C4: `git status --porcelain`, which must be empty;
 `git log --oneline -n 6`, which must show C4, C3, C2, C1b, C1a and `86e12317` in that order;
 `git worktree list`, which must show the primary checkout and the `.remedy-wt/job-*`
 worktrees constraint 6 names, and nothing else; `git stash list | head -1`, unchanged from
 the reading item 4 took; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be
 EMPTY. These readings go in your reply, since C4 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and
the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 1 of feature F279, round 6, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review
of round 6, then T004's order half — `docs/orders/toolchain-refresh.md`, its docs test and the
self-use generator's fourteen-day tier. State the open-findings count, 26, and the
operator-questions count, 0.
