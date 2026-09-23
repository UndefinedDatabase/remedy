STEP F279 R4 — T001, THE READER HALF: every typed REMEDY_ read goes through one registry reader

GOAL
Book round 3's PASS, record DECISION F279 D4 with the feature file's note and one prose-slip
line, and land T001's reader half: `env_value` in `packages/orchestration/config.py` reads a
registered variable from the live environment as its declared type, the eleven typed reads move
onto it, and a guard keeps every typed read on it. Each new behaviour carries a red proof.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

WHAT CHANGES FOR A USER (DECISION F279 D4, the decisions.diff payload)
The UI flags and the strict event-name flag now read yes for 1, true or yes, the words the
configuration already honours, instead of for "1" alone. A whole-number or number variable that
does not parse now fails naming the variable and its type, an EMPTY value included: an empty
`REMEDY_RUNTIME_LOG_MAX` used to mean no cap and now fails the supervisor's log pump loudly.
The Claude planner's timeout default, 300 seconds, now lives in the variable's spec alone, and
the provider's private copy of it is deleted. Text reads, the standalone scripts under
`scripts/` and the two runtime port reads keep their own, the ports named in the guard with
their reason.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f279-r4-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f279-r4-scratch/`   YOURS for logs and scripts. Each is gitignored; create
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
   `0a529d69`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f279-r4-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `git stash list | head -1` as found.

PAYLOADS — under `.remedy-wt/f279-r4-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| claude_planner.diff | 36 | 1716 | c25383469ce6c105a374309b9995089cbbf38d420e380107c108a7df76c79e0d |
| config.diff | 47 | 2367 | 48e630d4ac3c4a98ff14c695302a3d2ac8aac0147a323e0073eae9c9160a0127 |
| decisions.diff | 43 | 3307 | 1ba8b5597e3719396187f04a2346baa2dbf1b96ceca6152dc74d7737ea2c2d5f |
| feature.diff | 15 | 1022 | 825ad48a9d0e852c4fdb8272c4b3ec1b0e9aee1da7749e3d3996f4f94216c025 |
| ledger.diff | 10 | 6964 | f0a999bdc734140734ddff7bd682804ea1c0844c1eae1e27607c8d7509e7c19d |
| mutations.py | 62 | 2701 | 4290c666b360759f3326f31b1ad7365047c8a5cf1dfb3473a8f245901480b114 |
| ollama_builder.diff | 47 | 2049 | c407d11691c15f9882c61d19b88615dc569bb81fb76fa8e9e972a46d290581ad |
| ollama_planner.diff | 45 | 1970 | 2618c9dddd20ad151b8f63c7d5b60036ce54ca4e31c21412c01442ec13aeb5e7 |
| plan.md | 32 | 1322 | 33556ec308a6cdc914adefec8236a42e5ffbfc1f7cc6391c362c7d6446c15abe |
| run_log.diff | 28 | 949 | 528a344828e61a00e77fbcf3d9ff3b9aaf3075d6121ada7b5eeb266f2f7475f6 |
| runtime_supervisor.diff | 21 | 1056 | 7a627d2f1f3cd943accb4258168f3e07b2d078df402970fba9409d3951f6ff91 |
| slips.diff | 9 | 1635 | 146e3b400665c5a2fa001becc102652f071a2a30cee3863d58a49b1799335212 |
| test_env_registry.diff | 122 | 6073 | e074be00ccacc38ae7980b3117c9fabc2713fff7267b3fe080b82aba7f5e1730 |
| ui_server.diff | 55 | 2430 | cd203efb96c84f949bd9cab2426ba95461bbcbe2b4c83ef7fb00ddec02efaf61 |

`plan.md` is a REWRITE of `.agent/plan.md`. Every `.diff` goes on with `git apply`; the
reviewer generated each from a tree at `0a529d69` and applied all of them, in the commit order
below, to a fresh worktree at `0a529d69` with `git apply --check` then `git apply`, every one
at real exit code 0. `ledger.diff` appends round 3's `Gate:` entry to `.agent/live_review.md`,
`decisions.diff` appends DECISION F279 D4, and `slips.diff` appends one line to
`.agent/prose_slips.md`. `mutations.py` is a TOOL for G5: it is run, never applied.

BUNDLE — the commits are C1a, C1b, C2, C3 and C4, in this order. The copies are two commits
because together with this block they exceed the 500-line cap.

C1a — copy this block and the bookkeeping payloads
  `.agent/authored/f279-r4-block.md` := this block, and one `.agent/authored/f279-r4-<name>`
  for each of ledger.diff, plan.md, decisions.diff, feature.diff and slips.diff, keeping each
  payload's own file name. All by `shutil.copyfile`.
  Subject: `F279 R4 C1a: copy round 4 block and bookkeeping payloads into .agent/authored/`
  Its insertions are this block's line count plus 109. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C1b — copy the product payloads
  `.agent/authored/f279-r4-<name>` for each of config.diff, ollama_builder.diff,
  ollama_planner.diff, claude_planner.diff, ui_server.diff, run_log.diff,
  runtime_supervisor.diff, test_env_registry.diff and mutations.py, by `shutil.copyfile`.
  Subject: `F279 R4 C1b: copy round 4 product payloads into .agent/authored/`
  Expected insertions: 463.

C2 — THE BOOKKEEPING, one commit (amend0917-throughput rule 4), in this order:
   1. `git apply` ledger.diff     → `.agent/live_review.md`
   2. rewrite `.agent/plan.md` := plan.md
   3. `git apply` decisions.diff  → `.agent/decisions.md`
   4. `git apply` feature.diff    → `docs/roadmap/features/T2_F279.md`
   5. `git apply` slips.diff      → `.agent/prose_slips.md`
  Subject: `F279 R4 C2: book round 3's PASS and record DECISION F279 D4`
  Expected insertions by `git show --numstat`: 35 decisions.md, 2 live_review.md, 11 plan.md,
  1 prose_slips.md, 4 T2_F279.md.

C3 — THE READER, ITS ELEVEN CALLERS AND THEIR GUARD in one commit, because the reader and its
  callers change together and the tests are what verify them. `git apply`, in this order:
  config.diff, ollama_builder.diff, ollama_planner.diff, claude_planner.diff, ui_server.diff,
  run_log.diff, runtime_supervisor.diff, test_env_registry.diff.
  Subject: `F279 R4 C3: read every typed REMEDY_ variable through the registry reader`
  Expected insertions: 36 config.py, 2 run_log.py, 11 ui_server.py, 4 claude_planner
  provider.py, 5 ollama_builder provider.py, 5 ollama_planner provider.py,
  5 runtime_supervisor.py, 98 test_env_registry.py.

C4 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F279 R4 C4: rewrite handoff for round 4`
  Then `git push origin feature/f279-configuration-toolchain-truth`. Do NOT create a pull
  request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading. F279's one
   declared oversize commit was round 1's C5; there is no second.
3. The round's whole tracked path set is: the `.agent/authored/f279-r4-*` copies,
   `.agent/live_review.md`, `.agent/plan.md`, `.agent/decisions.md`, `.agent/prose_slips.md`,
   `docs/roadmap/features/T2_F279.md`, `packages/orchestration/config.py`,
   `packages/providers/ollama_builder/provider.py`,
   `packages/providers/ollama_planner/provider.py`,
   `packages/providers/claude_planner/provider.py`, `packages/orchestration/ui_server.py`,
   `packages/orchestration/run_log.py`, `packages/runtimes/runtime_supervisor.py`,
   `tests/orchestration/test_env_registry.py` and `.agent/handoff.md`. Report the list you
   measure with `git diff --name-only 0a529d69 HEAD` after C4. Do NOT touch
   `.agent/candidates.md`, `.agent/operator_questions.md`, `.agent/context.md`,
   `docs/guides/environment.md`, or any module or script not in that list.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash` — the stash list is shared by every
   worktree of this repository.
6. Leave `.remedy-wt/job-129b3ad7206d4f8d`, `.remedy-wt/job-e7268925db3a4831`, their branches
   and every existing stash alone. The worktree G5 adds goes under `.remedy-wt/`, is removed
   as that step's last action, and `git worktree list` is reported afterwards (R-0940).
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run
   and F279's belongs to its closure. Run G4 SERIALLY, never with `-n`: under `-n` the UI
   server tests fail in a fresh worktree at the base too, and a serial run is the reading.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C4 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f279-r4-*` copy byte for
 byte with its source (the block copy against `.remedy-wt/f279-r4-block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE BOOKKEEPING — at C2, the sha256 of each file below, read with `git show <C2>:<path>`,
 equals the reviewer's simulated reading:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 380746 | 85cb0df6d5996df33bb8f42c4976975e8e3e94197e060980667a4b544d87bebe |
 | .agent/plan.md | 1322 | 33556ec308a6cdc914adefec8236a42e5ffbfc1f7cc6391c362c7d6446c15abe |
 | .agent/decisions.md | 1867202 | 2c5cac8d0699fb617b1effbb04ef93f8812ae62bbc7e2998f60bf3462e2efc13 |
 | docs/roadmap/features/T2_F279.md | 8575 | 05493ada423526757ab668899782e7ef5c4461200a1c11c6c3dd28f804c00cf6 |
 | .agent/prose_slips.md | 364451 | 5a97f18d394d61a973e5373a69119172d4df3edc8784bda02a318f62ed6a5f97 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `0a529d69` and at C2, with the set
 difference in both directions (the reviewer read 26 and 26, both differences empty); the
 count of lines beginning `Gate: F279 R3 — ` at `0a529d69` and at C2 (the reviewer read 0 and
 1); and `git diff --name-only <C1b> <C2>`, which must name exactly the paths C2 lists.

G3 THE READER — at C3, `git diff --name-only <C2> <C3>` names exactly the paths C3 lists, and
 the sha256 of each, read with `git show <C3>:<path>`, equals the reviewer's simulated reading:
 | path | bytes | sha256 |
 |---|---|---|
 | packages/orchestration/config.py | 62161 | cb2ad6ad59d6a41e7632da2c3b35ede8fbbea50e7bc76da94d1384ffff330d2a |
 | packages/providers/ollama_builder/provider.py | 11447 | 99e5b3082473abcd411112bfca12887f1532754bab9a943ce238be7ec3c31601 |
 | packages/providers/ollama_planner/provider.py | 7658 | c18029b6e963433716d596143ad8c7ba7ea800f3b572ab6c7f1a1dc3a8be6a2b |
 | packages/providers/claude_planner/provider.py | 13104 | 3c9a9bb79b621f7eb691a04ea8ed95666459c87a59120e4256cc0207a5c63979 |
 | packages/orchestration/ui_server.py | 147335 | e69cada6cdd133296b0e92133ca96e5a90d3f215425ae56f1ceaf06844f8f7db |
 | packages/orchestration/run_log.py | 6845 | 77da32cb0a4d88f8f1955f27cd1402b602a6c5b105736f9cc36b13377faf7783 |
 | packages/runtimes/runtime_supervisor.py | 25721 | 3d5c888554c073559f91d5c0e6106bfa31edae18380acf5d194568ae23c3bba8 |
 | tests/orchestration/test_env_registry.py | 11442 | 52f60d4bc124a76af970f13d4231cd2043e18bc42cd7e09489dd494b9cf8c07e |

G4 THE TESTS — in the primary checkout at C3, SERIALLY, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_env_registry.py tests/test_ollama_builder.py tests/test_ollama_provider.py tests/orchestration/test_claude_planner.py tests/orchestration/test_event_names.py tests/orchestration/test_config.py tests/ui_server/ tests/ui_contracts/ tests/orchestration/test_test_runner.py tests/runtimes/test_runtime_config.py tests/runtimes/test_runtime_state_machine.py tests/runtimes/test_runtime_lifecycle_safety.py tests/runtimes/test_runtime_cli_process_boundary.py tests/runtimes/test_supervisor_portability.py tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py tests/test_ble001_ratchet.py tests/docs/ tests/orchestration/test_roadmap_index.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/regression/test_resource_safety.py tests/orchestration/test_self_use_generator.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path inside a disposable worktree
 carrying C2 and C3 and read `2201 passed, 5 skipped` at real exit code 0; the primary
 checkout carries the UI toolchain a worktree lacks, so a skip may pass there. Report what
 you read. Then `python3 -m ruff check` over the Python paths C3 lists, real exit code 0,
 and `python3 -m apps.cli.main integrity check --json`, which must read every check `pass` at
 `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f279-r4-mut <C3>`, then
 `python3 -B .remedy-wt/f279-r4-payloads/mutations.py .remedy-wt/f279-r4-mut` and report its
 whole output. The script asserts each FROM occurs exactly once, applies it, runs the
 affected test files under `python3 -B`, restores the bytes, and runs an unmutated control
 first and last. The reviewer read, over the same script against its own tree carrying C2 and
 C3:
 control_before `57 passed` at exit 0;
 m1 (a boolean reads yes only for "1") 1 failed at exit 1, at
   `TestTheRegistryReader::test_a_boolean_reads_yes_only_for_the_registered_words`;
 m2 (an unset variable answers its default everywhere) 1 failed at exit 1, at
   `TestTheRegistryReader::test_an_unset_variable_remedy_toml_may_carry_answers_none`;
 m3 (a parse error names nothing) 3 failed at exit 1, at
   `TestTheRegistryReader::test_a_number_that_does_not_parse_names_the_variable_and_its_type`,
   `test_invalid_temperature_raises_with_var_name` and
   `test_invalid_num_predict_raises_with_var_name`;
 m4 (a typed read bypasses the reader) 1 failed at exit 1, at
   `test_a_typed_variable_is_read_through_the_registry_reader`;
 control_after `57 passed` at exit 0.
 Then `git worktree remove --force .remedy-wt/f279-r4-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C4: `git status --porcelain`, which must be empty;
 `git log --oneline -n 6`, which must show C4, C3, C2, C1b, C1a and `0a529d69` in that order;
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
section reads SESSION 1 of feature F279, round 4, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review
of round 4, then T003 — `remedy block lint`. State the open-findings count, 26, and the
operator-questions count, 0.
