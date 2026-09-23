STEP F279 R2 — T001, THE REGISTRY HALF: every REMEDY_ name production code spells is registered

GOAL
Book round 1's PASS, record DECISION F279 D2 with the feature file's T001 amendment, and land
T001's registry half: the fifteen `REMEDY_` names production code spells without a spec are
registered as env-only keys in `packages/orchestration/config.py`, and a new
`tests/orchestration/test_env_registry.py` holds every such name to the registry, each guard
with a red proof.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

WHY THE REGISTRY IS config.py AND NOT A NEW MODULE
DECISION F279 D2 (the decisions.diff payload): `_CONFIG_KEY_SPECS` in
`packages/orchestration/config.py` already carries, per variable, a name, a type, a default, a
description and an `env_only` flag, so a second registry would be a second place to forget a
variable. The reviewer measured at `62c689e1` that 79 distinct whole `REMEDY_*` literals appear
under `packages/`, `apps/` and `scripts/` and 15 of them name no spec; with this round's specs
the count of unregistered names is zero, and without them the new guard names exactly the 15.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f279-r2-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f279-r2-scratch/`   YOURS for logs and scripts. Each is gitignored; create
      the scratch directory if it is absent.

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
   `feature/f279-configuration-toolchain-truth`, and `git log --oneline -1` must read
   `62c689e1`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f279-r2-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `git stash list | head -1` as found.

PAYLOADS — under `.remedy-wt/f279-r2-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| config.diff | 174 | 5717 | 386cc4f56ba8be5c70dd360c210b2ce3511fa58fc9700d6f914dd097d7efca44 |
| decisions.diff | 38 | 2697 | 1d7420e4765a2827c9d83be8c26910c502203faf67f81edeea75f841264b43f0 |
| feature.diff | 17 | 1046 | 6ae3410bd15a71431f18c44f8eb28891b5bbd85c422bdbb82883732dafb2a494 |
| ledger.diff | 10 | 7685 | c5d504286be531a09fe7650c2f9b2f5a4c8a65d04fd574fd099fe94039d78d96 |
| mutations.py | 67 | 2592 | 6a4db126d4a7dd162bf94ddc618842d1fecd2c15276086be9575f203c5d4ed83 |
| plan.md | 37 | 1599 | 87ef5e1b5d91202e4230e4e3dd0bd06ce5b8da37d593e1ca3fe9abbb84caf3b4 |
| test_env_registry.py | 93 | 3883 | 16ae49f0c403c5826131f239ae1947ef16a08ba9d9100b2ea70f07a25e2cb6f6 |

`plan.md` is a REWRITE of `.agent/plan.md`. `test_env_registry.py` is a NEW FILE at
`tests/orchestration/test_env_registry.py`, copied whole. The `.diff` files go on with
`git apply`; the reviewer generated every one from a tree at `62c689e1` and applied all of
them, in the commit order below, to a fresh worktree at `62c689e1` with `git apply --check`
then `git apply`, every one at real exit code 0. `ledger.diff` appends round 1's `Gate:` entry
to `.agent/live_review.md`; `decisions.diff` appends DECISION F279 D2 to
`.agent/decisions.md`. `mutations.py` is a TOOL for G5: it is run, never applied to a tracked
file.

BUNDLE — the commits are C1a, C1b, C2, C3 and C4, in this order. The copies are two commits
because together with this block they exceed the 500-line cap.

C1a — copy this block and the bookkeeping payloads
  `.agent/authored/f279-r2-block.md` := this block, and one `.agent/authored/f279-r2-<name>`
  for each of ledger.diff, plan.md, decisions.diff and feature.diff, keeping each payload's
  own file name. All by `shutil.copyfile`.
  Subject: `F279 R2 C1a: copy round 2 block and bookkeeping payloads into .agent/authored/`
  Its insertions are this block's line count plus 102. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C1b — copy the product payloads
  `.agent/authored/f279-r2-<name>` for each of config.diff, test_env_registry.py and
  mutations.py, by `shutil.copyfile`.
  Subject: `F279 R2 C1b: copy round 2 product payloads into .agent/authored/`
  Expected insertions: 334.

C2 — THE BOOKKEEPING, one commit (amend0917-throughput rule 4), in this order:
   1. `git apply` ledger.diff     → `.agent/live_review.md`
   2. rewrite `.agent/plan.md` := plan.md
   3. `git apply` decisions.diff  → `.agent/decisions.md`
   4. `git apply` feature.diff    → `docs/roadmap/features/T2_F279.md`
  Subject: `F279 R2 C2: book round 1's PASS, record DECISION F279 D2 and amend T001`
  Expected insertions by `git show --numstat`: 30 decisions.md, 2 live_review.md, 15 plan.md,
  6 T2_F279.md.

C3 — THE REGISTRY AND ITS GUARD in one commit, because the test is what verifies it
  `git apply` config.diff → `packages/orchestration/config.py`, then copy
  test_env_registry.py to `tests/orchestration/test_env_registry.py` and `git add` it — an
  untracked test file fails `integrity check`'s `relevant_untracked`.
  Subject: `F279 R2 C3: register every REMEDY_ name production code spells, and guard it`
  Expected insertions: 163 config.py, 93 test_env_registry.py.

C4 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F279 R2 C4: rewrite handoff for round 2`
  Then `git push origin feature/f279-configuration-toolchain-truth`. Do NOT create a pull
  request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading. F279's one
   declared oversize commit was round 1's C5; there is no second.
3. The round's whole tracked path set is: the `.agent/authored/f279-r2-*` copies,
   `.agent/live_review.md`, `.agent/plan.md`, `.agent/decisions.md`,
   `docs/roadmap/features/T2_F279.md`, `packages/orchestration/config.py`,
   `tests/orchestration/test_env_registry.py` and `.agent/handoff.md`. Report the list you
   measure with `git diff --name-only 62c689e1 HEAD` after C4. Do NOT touch
   `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md`,
   `.agent/context.md`, or any module under `packages/`, `apps/` or `scripts/` other than
   `config.py`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of another branch, no
   branch deletion, no force-push, no `git stash` — the stash list is shared by every
   worktree of this repository.
6. Leave `.remedy-wt/job-129b3ad7206d4f8d`, `.remedy-wt/job-e7268925db3a4831`, their branches
   and every existing stash alone. The worktree G5 adds goes under `.remedy-wt/`, is removed
   as that step's last action, and `git worktree list` is reported afterwards (R-0940).
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run
   and F279's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C4 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f279-r2-*` copy byte for
 byte with its source (the block copy against `.remedy-wt/f279-r2-block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE BOOKKEEPING — at C2, the sha256 of each file below, read with `git show <C2>:<path>`,
 equals the reviewer's simulated reading:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 376430 | 01c7cc95b137b9ac6085c7ff2d0b457fc9baa87e0ab5f4eadec66426de59bf54 |
 | .agent/plan.md | 1599 | 87ef5e1b5d91202e4230e4e3dd0bd06ce5b8da37d593e1ca3fe9abbb84caf3b4 |
 | .agent/decisions.md | 1861590 | 87e7757e6b1c332f2593eae5259e1b80bf4b99df0fa054f936cb40c22b6a5d6f |
 | docs/roadmap/features/T2_F279.md | 8234 | 7eba8a4ca7349a9c98fd506d90a15a2bc12b5642a0278536d1e192e7a67a3a95 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `62c689e1` and at C2, with the set
 difference in both directions (the reviewer read 26 and 26, both differences empty); the
 count of lines beginning `Gate: F279 R1 — ` at `62c689e1` and at C2 (the reviewer read 0 and
 1); and `git diff --name-only <C1b> <C2>`, which must name exactly the paths C2 lists.

G3 THE REGISTRY — at C3, `git diff --name-only <C2> <C3>` names exactly
 `packages/orchestration/config.py` and `tests/orchestration/test_env_registry.py`, and their
 sha256 read with `git show <C3>:<path>` equal:
 | path | bytes | sha256 |
 |---|---|---|
 | packages/orchestration/config.py | 51844 | d69f3d331a2bd734aca42b40aa4c26ddaaa298acc37a47bb5bb9db268073032e |
 | tests/orchestration/test_env_registry.py | 3883 | 16ae49f0c403c5826131f239ae1947ef16a08ba9d9100b2ea70f07a25e2cb6f6 |

G4 THE TESTS — in the primary checkout at C3, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_env_registry.py tests/orchestration/test_config.py tests/cli/test_config_cmd.py tests/cli/test_worker_facade_cmd.py tests/orchestration/test_role_config.py tests/orchestration/test_dead_model_list.py tests/orchestration/test_run_manifest.py tests/orchestration/test_run_manifest_security.py tests/orchestration/test_run_manifest_export_allowlist.py tests/orchestration/test_self_dogfood.py tests/orchestration/test_model_aliases.py tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py tests/docs/ tests/orchestration/test_roadmap_index.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_self_use_generator.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path inside a disposable worktree
 carrying C2 and C3 and read `981 passed, 2 skipped` at real exit code 0; the primary
 checkout carries the UI toolchain a worktree lacks, so a skip may pass there. Report what
 you read. Then `python3 -m ruff check packages/orchestration/config.py
 tests/orchestration/test_env_registry.py`, real exit code 0, and
 `python3 -m apps.cli.main integrity check --json`, which must read every check `pass` at
 `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f279-r2-mut <C3>`, then
 `python3 -B .remedy-wt/f279-r2-payloads/mutations.py .remedy-wt/f279-r2-mut` and report its
 whole output. The script asserts each FROM occurs exactly once, applies it, runs the guard
 file under `python3 -B`, restores the bytes, and runs an unmutated control first and last.
 The reviewer read, over the same script against its own tree carrying C2 and C3:
 control_before `4 passed` at exit 0;
 m1 (an unregistered name read with a literal key) 2 failed at exit 1, at
   `test_every_literal_env_read_names_a_registered_variable` and
   `test_every_remedy_name_production_code_spells_is_registered`;
 m2 (an unregistered name kept in a constant) 1 failed at exit 1, at
   `test_every_remedy_name_production_code_spells_is_registered`;
 m3 (the `ui.demo_mode` spec renamed away) 2 failed at exit 1, at the same two tests as m1;
 m4 (one variable registered twice) 3 failed at exit 1, at the two tests of m1 and
   `test_every_registered_variable_is_a_remedy_name_and_registered_once`;
 control_after `4 passed` at exit 0.
 Then `git worktree remove --force .remedy-wt/f279-r2-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C4: `git status --porcelain`, which must be empty;
 `git log --oneline -n 6`, which must show C4, C3, C2, C1b, C1a and `62c689e1` in that order;
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
section reads SESSION 1 of feature F279, round 2, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review
of round 2, then T001's doctor and docs half — `remedy doctor core` naming unknown and
unparsable `REMEDY_*` variables, and the generated `docs/guides/environment.md` with its
drift test. State the open-findings count, 26, and the operator-questions count, 0.
