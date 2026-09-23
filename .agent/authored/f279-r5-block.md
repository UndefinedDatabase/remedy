STEP F279 R5 — T003: `remedy integrity block <path>`, the checklist's checkable items by machine

GOAL
Book round 4's PASS, record DECISION F279 D5 with the feature file's amendment, and land T003:
`packages/orchestration/block_lint.py` with a rule for each of items 1, 3, 10, 24, 30, 31 and 37
of the reviewer's checklist, the `integrity.block` command, and a guard that holds every rule
to a live item number and to a sentence that item really contains. Each rule and the guard
carry a red proof.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

WHY `integrity block` AND NOT `block lint` (DECISION F279 D5, the decisions.diff payload)
A `block` group would be the catalog's thirty-second, and `tests/cli/test_cli_ux.py` pins the
group partition DECISION amend0905-vocab D4 ruled; the self-build `integrity` group already
holds the pre-handoff check. The new module joins the entry points' import closure through the
command, so `tests/orchestration/import_reachability_allowlist.txt` gains its one line in the
same commit (the allowlist.diff payload), or the reachability test goes red.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f279-r5-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f279-r5-scratch/`   YOURS for logs and scripts. Each is gitignored; create
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
   `182e7ea0`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f279-r5-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `git stash list | head -1` as found.

PAYLOADS — under `.remedy-wt/f279-r5-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| allowlist.diff | 12 | 605 | 9adabb68e03dd3b3d390b611c809701994c79db29e8d51e50715783718dd4f97 |
| block_lint.py | 185 | 8440 | 70ca22a3d1d838c7d9fa4b8e650c945c8af21589ca85c8384ac56979d0b19ba3 |
| command_catalog.diff | 25 | 1013 | 1f90a3f79b6dfc31683adf7dca3bfd4fa943bebd7717fd2673c3775538b3bd0f |
| decisions.diff | 45 | 3456 | 103dfba3a745afd78e0350af8c2b0b4198f5657df72ebc6e130d99afe0d825f4 |
| feature.diff | 28 | 1854 | 23758d84c981ded2f636f8e7e3b92d68f82e9d3853762ea3a709ed448bb6b640 |
| integrity_cmd.diff | 41 | 1773 | d90d1b9b9f9f1bef24257afc7bbc00b86cc3783af7514317a54a41babae8ad3f |
| ledger.diff | 10 | 6568 | 2fc34e64df65192041960488ac6e840abd01c6ad8a73b4861ced5f7ac032a3d4 |
| mutations.py | 71 | 2608 | 02345b48fe9d404fdd6b926be7ca29f3fa743e6ed1367d49ec7ea2bf5ddffd3a |
| plan.md | 30 | 1193 | a7faa59d7b6283628ee25b006fd361f8ff13ded8c4a1e2d87cac6f0ba60748d3 |
| test_block_lint.py | 161 | 7326 | 739972a5d5b5f15780417fee48109b7b4a49705c27ce372679a6ce83670c29f3 |

`plan.md` is a REWRITE of `.agent/plan.md`. `block_lint.py` is a NEW FILE at
`packages/orchestration/block_lint.py` and `test_block_lint.py` a NEW FILE at
`tests/orchestration/test_block_lint.py`, each copied whole. Every `.diff` goes on with
`git apply`; the reviewer generated each from a tree at `182e7ea0` and applied all of them, in
the commit order below, to a fresh worktree at `182e7ea0` with `git apply --check` then
`git apply`, every one at real exit code 0. `ledger.diff` appends round 4's `Gate:` entry and
`decisions.diff` appends DECISION F279 D5. `mutations.py` is a TOOL for G5, never applied.

BUNDLE — the commits are C1a, C1b, C2, C3 and C4, in this order. The copies are two commits
because together with this block they exceed the 500-line cap.

C1a — copy this block and the bookkeeping payloads
  `.agent/authored/f279-r5-block.md` := this block, and one `.agent/authored/f279-r5-<name>`
  for each of ledger.diff, plan.md, decisions.diff and feature.diff, keeping each payload's own
  file name. All by `shutil.copyfile`.
  Subject: `F279 R5 C1a: copy round 5 block and bookkeeping payloads into .agent/authored/`
  Its insertions are this block's line count plus 113. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C1b — copy the product payloads
  `.agent/authored/f279-r5-<name>` for each of block_lint.py, test_block_lint.py,
  integrity_cmd.diff, command_catalog.diff, allowlist.diff and mutations.py, by
  `shutil.copyfile`.
  Subject: `F279 R5 C1b: copy round 5 product payloads into .agent/authored/`
  Expected insertions: 495.

C2 — THE BOOKKEEPING, one commit (amend0917-throughput rule 4), in this order:
   1. `git apply` ledger.diff     → `.agent/live_review.md`
   2. rewrite `.agent/plan.md` := plan.md
   3. `git apply` decisions.diff  → `.agent/decisions.md`
   4. `git apply` feature.diff    → `docs/roadmap/features/T2_F279.md`
  Subject: `F279 R5 C2: book round 4's PASS and record DECISION F279 D5`
  Expected insertions by `git show --numstat`: 37 decisions.md, 2 live_review.md, 8 plan.md,
  8 T2_F279.md.

C3 — THE LINTER, ITS COMMAND AND ITS GUARD in one commit, because the tests verify them
  Copy block_lint.py and test_block_lint.py to their paths and `git add` both — an untracked
  file fails `integrity check`'s `relevant_untracked` — then `git apply` integrity_cmd.diff,
  command_catalog.diff and allowlist.diff.
  Subject: `F279 R5 C3: add remedy integrity block, the checklist's checkable items by machine`
  Expected insertions: 14 command_catalog.py, 30 integrity_cmd.py, 185 block_lint.py,
  1 import_reachability_allowlist.txt, 161 test_block_lint.py.

C4 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F279 R5 C4: rewrite handoff for round 5`
  Then `git push origin feature/f279-configuration-toolchain-truth`. Do NOT create a pull
  request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading. F279's one
   declared oversize commit was round 1's C5; there is no second.
3. The round's whole tracked path set is: the `.agent/authored/f279-r5-*` copies,
   `.agent/live_review.md`, `.agent/plan.md`, `.agent/decisions.md`,
   `docs/roadmap/features/T2_F279.md`, `packages/orchestration/block_lint.py`,
   `tests/orchestration/test_block_lint.py`, `apps/cli/commands/integrity_cmd.py`,
   `apps/cli/command_catalog.py`, `tests/orchestration/import_reachability_allowlist.txt` and
   `.agent/handoff.md`. Report the list you measure with `git diff --name-only 182e7ea0 HEAD`
   after C4. Do NOT touch `.agent/prose_slips.md`, `.agent/candidates.md`,
   `.agent/operator_questions.md`, `.agent/context.md`, `docs/agents/**`, or any module not in
   that list.
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
 against the PAYLOADS table. Then compare each `.agent/authored/f279-r5-*` copy byte for
 byte with its source (the block copy against `.remedy-wt/f279-r5-block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE BOOKKEEPING — at C2, the sha256 of each file below, read with `git show <C2>:<path>`,
 equals the reviewer's simulated reading:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 382747 | 2e7b3abf8e0e33b2fa35014dc957a881781dd47b320ae7fbe6ae604cf50e83c0 |
 | .agent/plan.md | 1193 | a7faa59d7b6283628ee25b006fd361f8ff13ded8c4a1e2d87cac6f0ba60748d3 |
 | .agent/decisions.md | 1870110 | b8f76e9c8fc10739883505a8e6ac00a14bef7fdd062fe2d2fd29fa5f3c4aa90b |
 | docs/roadmap/features/T2_F279.md | 8970 | 116e7e92fbd15b2ada884d457f438efcdb5f8733534c8cd7db7d81b8f36e049d |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `182e7ea0` and at C2, with the set
 difference in both directions (the reviewer read 26 and 26, both differences empty); the
 count of lines beginning `Gate: F279 R4 — ` at `182e7ea0` and at C2 (the reviewer read 0 and
 1); and `git diff --name-only <C1b> <C2>`, which must name exactly the paths C2 lists.

G3 THE LINTER — at C3, `git diff --name-only <C2> <C3>` names exactly the paths C3 lists, and
 the sha256 of each, read with `git show <C3>:<path>`, equals the reviewer's simulated reading:
 | path | bytes | sha256 |
 |---|---|---|
 | packages/orchestration/block_lint.py | 8440 | 70ca22a3d1d838c7d9fa4b8e650c945c8af21589ca85c8384ac56979d0b19ba3 |
 | tests/orchestration/test_block_lint.py | 7326 | 739972a5d5b5f15780417fee48109b7b4a49705c27ce372679a6ce83670c29f3 |
 | apps/cli/commands/integrity_cmd.py | 2410 | ec1f2cc946e333f34a68cc0b526fc65b73bc4c369b5368060b39fa39c805ccd3 |
 | apps/cli/command_catalog.py | 110204 | 3d22af46395a89813cd5df12c71b41448324a94da5595566400b0ef013a9b30d |
 | tests/orchestration/import_reachability_allowlist.txt | 9834 | 8c65b73ddd3442277a34f8efcaaa15bce26f23329aa60626a75ee3fc81ff53f2 |

G4 THE TESTS — in the primary checkout at C3, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_block_lint.py tests/test_command_catalog.py tests/cli/test_command_catalog.py tests/cli/test_cli_ux.py tests/cli/test_exit_codes.py tests/cli/test_advertised_commands.py tests/cli/test_json_contract.py tests/cli/test_job_refusal_envelope.py tests/test_grouped_cli.py tests/test_help_renderer.py tests/docs/ tests/ui_contracts/test_humanize_catalog.py tests/orchestration/test_dead_command_check.py tests/cli/test_product_spine.py tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py tests/orchestration/test_integrity_gate.py tests/test_ble001_ratchet.py tests/orchestration/test_roadmap_index.py tests/orchestration/test_live_review_rotation.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_self_use_generator.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path inside a disposable worktree
 carrying C2 and C3 and read `1689 passed, 2 skipped` at real exit code 0. Your tree at C3 also
 carries this round's block copy, and `test_block_lint.py` checks every committed F279 block,
 so expect exactly one more test than the reviewer's tree ran; the primary checkout carries the
 UI toolchain a worktree lacks, so a skip may pass there. Report what you read. Then
 `python3 -m ruff check` over the Python paths C3 lists, real exit code 0;
 `python3 -m apps.cli.main integrity check --json`, which must read every check `pass` at
 `fail_count` 0; and `python3 -m apps.cli.main integrity block .remedy-wt/f279-r5-block.md`,
 which the reviewer ran on this block before emitting it and read every item OK at exit 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f279-r5-mut <C3>`, then
 `python3 -B .remedy-wt/f279-r5-payloads/mutations.py .remedy-wt/f279-r5-mut` and report its
 whole output. The script asserts each FROM occurs exactly once, applies it, runs the linter's
 test file under `python3 -B`, restores the bytes, and runs an unmutated control first and
 last. The reviewer read, over the same script against its own tree carrying C2 and C3, which
 lacks this round's block copy, so your counts are each one higher in the passed column:
 control_before `19 passed` at exit 0;
 m1 (a rule cites retired item 32) 3 failed at exit 1, at
   `test_no_rule_references_a_retired_item_number`,
   `test_every_rule_quotes_a_sentence_its_item_really_contains` and
   `test_a_run_of_one_repeated_character_is_refused_but_a_code_fence_is_not`;
 m2 (the size limit off by one) 1 failed at exit 1, at
   `test_size_counts_lines_against_four_hundred`;
 m3 (a declared new file not exempt) 1 failed at exit 1, at
   `test_a_path_a_command_names_must_resolve_unless_the_block_creates_it`;
 m4 (a code fence counted as a run) 1 failed at exit 1, at
   `test_a_run_of_one_repeated_character_is_refused_but_a_code_fence_is_not`;
 m5 (a wrong open count passes) 1 failed at exit 1, at
   `test_a_stated_open_count_is_recomputed_from_the_ledger`;
 m6 (a violation exits zero) 1 failed at exit 1, at
   `test_a_violation_exits_one_and_names_its_item`;
 control_after `19 passed` at exit 0.
 Then `git worktree remove --force .remedy-wt/f279-r5-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C4: `git status --porcelain`, which must be empty;
 `git log --oneline -n 6`, which must show C4, C3, C2, C1b, C1a and `182e7ea0` in that order;
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
section reads SESSION 1 of feature F279, round 5, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review
of round 5, then T004 — the toolchain refresh order and `remedy doctor toolchain`. State the
open-findings count, 26, and the operator-questions count, 0.
