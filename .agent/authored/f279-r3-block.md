STEP F279 R3 — T001, THE DOCTOR AND DOCS HALF: unknown and unparsable variables, and the guide

GOAL
Book round 2's PASS, record DECISION F279 D3, and land T001's doctor and docs half: the
`REMEDY_` names the shell scripts expand and the two real-Ollama opt-ins are registered and
guarded; `remedy doctor core` warns about an unknown `REMEDY_` variable with its closest
registered name and about a registered one whose value does not read as its type; and
`docs/guides/environment.md` is GENERATED from the registry, indexed, and held by a drift test.
Each new behaviour carries a red proof.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

WHAT THE REVIEWER FOUND WHILE AUTHORING (DECISION F279 D3, the decisions.diff payload)
Measured at `cec312cb`: the shell scripts under `scripts/` expand seven `REMEDY_` names no spec
registers, `REMEDY_REVIEW_DIR` among them, which `tests/conftest.py` sets for every test; and
this machine's shell carries `REMEDY_` names that belong to another tool. So doctor's two
reports are ADVISORY warnings, never blockers, and never print a value; and
`tests/cli/test_worker_facade_cmd.py` gains an autouse fixture that removes foreign and
unparsable `REMEDY_` variables for its own tests, because a test asserting which warnings appear
must not depend on the shell it runs in. The new guide quotes the `model_routing` key's
description, whose word `promotion` `tests/docs/test_retired_promote_word.py` allows only by
file, so that file gains the guide's entry under the same sense `config.py` already carries.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f279-r3-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f279-r3-scratch/`   YOURS for logs and scripts. Each is gitignored; create
      the scratch directory if it is absent.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, process substitution, `cd <dir> && git ...`, and multi-operation
one-liners chained with `;` or `&&` outside a `bash -c`. Capture real exit codes as
`bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe pytest.
Use `git -C <path>` rather than `cd`. Use `python3 - <<'PY'` for counting, hashing and
copying (`shutil.copyfile`). A heredoc containing a dollar sign followed by a brace is refused
too: put such a script in a file under your scratch directory and run the file.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f279-configuration-toolchain-truth`, and `git log --oneline -1` must read
   `cec312cb`. Report all three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f279-r3-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `git stash list | head -1` as found.

PAYLOADS — under `.remedy-wt/f279-r3-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| config.diff | 246 | 9768 | 2b0e70c416f14773d073b92f9c06c5dbf2581d1955da2a2b72f0980cd874266e |
| decisions.diff | 45 | 3263 | 354bb3190fbbb6ccf724d373cf83bb3820adc1468156c901cdd7ca8ff95eb73f |
| docs_index.diff | 20 | 1586 | c187ffdd6ace3e5b2faba836574719e244c81a7a8eab63da3770e0c3e3bd8c33 |
| ledger.diff | 10 | 7184 | 2de45a20ee1a14571751bd1bf6be17f7d697c1d26b5c8d421147d85048d98028 |
| mutations.py | 70 | 3094 | 4750e1c4c8354d51b9ec1740dd6ab7726d85d681bb58a305ccbd25f7a5bc8ba1 |
| plan.md | 34 | 1452 | ba92c746279cd411cb0d91dafe33e2a35c5fb548585ba9fe4af83e44b3cd0bf4 |
| retired_word.diff | 14 | 640 | 184da4c72d61003517f5fb587a5cf12197054d623906aea4b5ab92135524dbd7 |
| test_env_registry.diff | 96 | 4520 | ee3d6e6dc3015b0aab58e639cc00a68281ab2b5a36ca5ee5395d0858bd0e062f |
| test_environment_guide.py | 38 | 1513 | 02dea8e49e47ffdfa145e9915df10a191ad4c2b4fa0222ec66bebc339c6dc7dc |
| test_worker_facade_cmd.diff | 75 | 3515 | 7c64c1f2c7c21e791618fe5fe85e94c1a832d56fe9c74dcfba37449ccb2cb4fa |
| worker_facade_cmd.diff | 46 | 2513 | d903b6094d9496ac5810fa2d5ad8a367f80ef9a279e796771376610dde096a67 |

`plan.md` is a REWRITE of `.agent/plan.md`. `test_environment_guide.py` is a NEW FILE at
`tests/docs/test_environment_guide.py`, copied whole. The `.diff` files go on with `git apply`;
the reviewer generated every one from a tree at `cec312cb` and applied all of them, in the
commit order below, to a fresh worktree at `cec312cb` with `git apply --check` then
`git apply`, every one at real exit code 0. `ledger.diff` appends round 2's `Gate:` entry to
`.agent/live_review.md`; `decisions.diff` appends DECISION F279 D3 to `.agent/decisions.md`.
`mutations.py` is a TOOL for G5: it is run, never applied to a tracked file.

`docs/guides/environment.md` IS NOT A PAYLOAD. It is GENERATED in C5 from the registry C3
lands, by the command in C5, and the reviewer's simulation read the bytes G3 states.

BUNDLE — the commits are C1a, C1b, C1c, C2, C3, C4, C5 and C6, in this order. The copies are
three commits because together with this block they exceed the 500-line cap.

C1a — copy this block and the bookkeeping payloads
  `.agent/authored/f279-r3-block.md` := this block, and one `.agent/authored/f279-r3-<name>`
  for each of ledger.diff, plan.md and decisions.diff, keeping each payload's own file name.
  All by `shutil.copyfile`.
  Subject: `F279 R3 C1a: copy round 3 block and bookkeeping payloads into .agent/authored/`
  Its insertions are this block's line count plus 89. Report the number you measure and STOP
  rather than commit if it is 500 or more.

C1b — copy the registry payloads
  `.agent/authored/f279-r3-<name>` for each of config.diff, test_env_registry.diff and
  mutations.py, by `shutil.copyfile`.
  Subject: `F279 R3 C1b: copy round 3 registry payloads into .agent/authored/`
  Expected insertions: 412.

C1c — copy the doctor and docs payloads
  `.agent/authored/f279-r3-<name>` for each of worker_facade_cmd.diff,
  test_worker_facade_cmd.diff, docs_index.diff, retired_word.diff and
  test_environment_guide.py, by `shutil.copyfile`.
  Subject: `F279 R3 C1c: copy round 3 doctor and docs payloads into .agent/authored/`
  Expected insertions: 193.

C2 — THE BOOKKEEPING, one commit (amend0917-throughput rule 4), in this order:
   1. `git apply` ledger.diff     → `.agent/live_review.md`
   2. rewrite `.agent/plan.md` := plan.md
   3. `git apply` decisions.diff  → `.agent/decisions.md`
  Subject: `F279 R3 C2: book round 2's PASS and record DECISION F279 D3`
  Expected insertions by `git show --numstat`: 37 decisions.md, 2 live_review.md, 11 plan.md.

C3 — THE REGISTRY: the new specs, the environment checks, the guide renderer, and their tests
  `git apply` config.diff → `packages/orchestration/config.py`, then test_env_registry.diff →
  `tests/orchestration/test_env_registry.py`.
  Subject: `F279 R3 C3: register the shell scripts' names and read the environment against the registry`
  Expected insertions: 220 config.py, 54 test_env_registry.py.

C4 — THE DOCTOR REPORT and its tests
  `git apply` worker_facade_cmd.diff → `apps/cli/commands/worker_facade_cmd.py`, then
  test_worker_facade_cmd.diff → `tests/cli/test_worker_facade_cmd.py`.
  Subject: `F279 R3 C4: remedy doctor core names unknown and unparsable REMEDY_ variables`
  Expected insertions: 35 worker_facade_cmd.py, 57 test_worker_facade_cmd.py.

C5 — THE GENERATED GUIDE, its index lines and its drift test. From the repository root run
  EXACTLY this one command line and report its real exit code:
  ```
  bash -c 'python3 -c "from packages.orchestration.config import write_environment_guide; write_environment_guide()"; echo "REAL_EXIT=$?"'
  ```
  Then `git apply` docs_index.diff → `docs/README.md` and retired_word.diff →
  `tests/docs/test_retired_promote_word.py`, copy test_environment_guide.py to
  `tests/docs/test_environment_guide.py`, and `git add` the guide and the new test — an
  untracked file fails `integrity check`'s `relevant_untracked`.
  Subject: `F279 R3 C5: generate docs/guides/environment.md from the registry and index it`
  Expected insertions: 2 README.md, 105 environment.md, 38 test_environment_guide.py,
  3 test_retired_promote_word.py.

C6 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F279 R3 C6: rewrite handoff for round 3`
  Then `git push origin feature/f279-configuration-toolchain-truth`. Do NOT create a pull
  request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code. Never edit `docs/guides/environment.md` by hand.
2. Every commit stays under 500 insertions by the `git show --numstat` reading. F279's one
   declared oversize commit was round 1's C5; there is no second.
3. The round's whole tracked path set is: the `.agent/authored/f279-r3-*` copies,
   `.agent/live_review.md`, `.agent/plan.md`, `.agent/decisions.md`,
   `packages/orchestration/config.py`, `tests/orchestration/test_env_registry.py`,
   `apps/cli/commands/worker_facade_cmd.py`, `tests/cli/test_worker_facade_cmd.py`,
   `docs/guides/environment.md`, `docs/README.md`, `tests/docs/test_environment_guide.py`,
   `tests/docs/test_retired_promote_word.py` and `.agent/handoff.md`. Report the list you
   measure with `git diff --name-only cec312cb HEAD` after C6. Do NOT touch
   `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md`,
   `.agent/context.md`, `docs/roadmap/**`, or any module or script not in that list.
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
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C6 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f279-r3-*` copy byte for
 byte with its source (the block copy against `.remedy-wt/f279-r3-block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE BOOKKEEPING — at C2, the sha256 of each file below, read with `git show <C2>:<path>`,
 equals the reviewer's simulated reading:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/live_review.md | 378596 | 52b760cbbd67ae04a5cc830fd8591c83533958ef0a568e2e5657bd5e905f545a |
 | .agent/plan.md | 1452 | ba92c746279cd411cb0d91dafe33e2a35c5fb548585ba9fe4af83e44b3cd0bf4 |
 | .agent/decisions.md | 1864432 | cb58b4387777ac00ed6d332bb08f5ea4ce37bfc2756b68326b3d3b2721b669bb |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `cec312cb` and at C2, with the set
 difference in both directions (the reviewer read 26 and 26, both differences empty); the
 count of lines beginning `Gate: F279 R2 — ` at `cec312cb` and at C2 (the reviewer read 0 and
 1); and `git diff --name-only <C1c> <C2>`, which must name exactly the paths C2 lists.

G3 THE PRODUCT — the sha256 of each file below, read with `git show <commit>:<path>` at the
 commit named, equals the reviewer's simulated reading:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C3 | packages/orchestration/config.py | 60320 | acb63eee44e93d2e91e9394e5a3af8f8b37bd7e043d74d010c4ad61c2ef2e325 |
 | C3 | tests/orchestration/test_env_registry.py | 6431 | 1edb95a729edb68aa58efeeb75ecda55a2a3eef9b5a940e65336500c8a20f381 |
 | C4 | apps/cli/commands/worker_facade_cmd.py | 20196 | 4a87ea41e3fd465cc057ffae414ed95974856fba3bc45ad0e9c091cdc26fbeb5 |
 | C4 | tests/cli/test_worker_facade_cmd.py | 33658 | 36b6686bd8440663b36b48e3edf336c86b541b79c74f5136dac9eb1b90098ff7 |
 | C5 | docs/guides/environment.md | 20564 | e5ec241bb89127d3f6ccdfba8bd735f60573766e1da6de0720734ddac8338098 |
 | C5 | docs/README.md | 18076 | 39a1472d22277eeaf18feba7bd0458ae0a66ccefa49e828cec6ad545fa88d704 |
 | C5 | tests/docs/test_environment_guide.py | 1513 | 02dea8e49e47ffdfa145e9915df10a191ad4c2b4fa0222ec66bebc339c6dc7dc |
 | C5 | tests/docs/test_retired_promote_word.py | 15876 | 5243991590e688faff6428cc53001beee70b395799795e42babf294c17e46774 |
 A guide digest that differs means the generator and the registry disagree with the
 reviewer's tree: report both digests and `git diff --no-index` of the two files, and STOP.
 Also `git diff --name-only <C2> <C3>`, `<C3> <C4>` and `<C4> <C5>`, which must name exactly
 the paths C3, C4 and C5 list.

G4 THE TESTS — in the primary checkout at C5, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_env_registry.py tests/docs/test_environment_guide.py tests/cli/test_worker_facade_cmd.py tests/orchestration/test_config.py tests/cli/test_config_cmd.py tests/orchestration/test_disk_floor.py tests/orchestration/test_dead_model_list.py tests/orchestration/test_run_manifest.py tests/orchestration/test_self_dogfood.py tests/cli/test_product_spine.py tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py tests/test_ble001_ratchet.py tests/docs/ tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_self_use_generator.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path inside a disposable worktree
 carrying C2 to C5 and read `853 passed, 2 skipped` at real exit code 0; the primary
 checkout carries the UI toolchain a worktree lacks, so a skip may pass there. Report what
 you read. Then `python3 -m ruff check packages/orchestration/config.py
 apps/cli/commands/worker_facade_cmd.py tests/orchestration/test_env_registry.py
 tests/cli/test_worker_facade_cmd.py tests/docs/test_environment_guide.py
 tests/docs/test_retired_promote_word.py`, real exit code 0, and
 `python3 -m apps.cli.main integrity check --json`, which must read every check `pass` at
 `fail_count` 0. Finally run `python3 -m apps.cli.main doctor core` once and paste its
 warnings section: this machine's shell carries foreign `REMEDY_` names, so seeing them named
 there is the feature working, and READY must still be read.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f279-r3-mut <C5>`, then
 `python3 -B .remedy-wt/f279-r3-payloads/mutations.py .remedy-wt/f279-r3-mut` and report its
 whole output. The script asserts each FROM occurs exactly once, applies it, runs the three
 affected test files under `python3 -B`, restores the bytes, and runs an unmutated control
 first and last. It takes about seven minutes. The reviewer read, over the same script
 against its own tree carrying C2 to C5:
 control_before `61 passed` at exit 0;
 m1 (registered names called unknown) 1 failed at exit 1, at
   `TestTheEnvironmentAgainstTheRegistry::test_registered_names_and_other_prefixes_are_not_unknown`;
 m2 (every boolean word accepted) 1 failed at exit 1, at
   `TestTheEnvironmentAgainstTheRegistry::test_a_value_that_does_not_read_as_its_type_is_named`;
 m3 (doctor drops the unparsable warning) 1 failed at exit 1, at
   `TestDoctorCoreEnvironment::test_a_registered_variable_that_does_not_parse_is_named_without_its_value`;
 m4 (doctor drops the closest match) 1 failed at exit 1, at
   `TestDoctorCoreEnvironment::test_an_unknown_variable_is_named_with_its_closest_registered_match`;
 m5 (a spec description changed without the guide) 1 failed at exit 1, at
   `test_the_committed_guide_is_the_registry_rendered`;
 m6 (an unregistered shell expansion) 1 failed at exit 1, at
   `test_every_remedy_name_a_shell_script_expands_is_registered`;
 control_after `61 passed` at exit 0.
 Then `git worktree remove --force .remedy-wt/f279-r3-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C6: `git status --porcelain`, which must be empty;
 `git log --oneline -n 9`, which must show C6, C5, C4, C3, C2, C1c, C1b, C1a and `cec312cb` in
 that order; `git worktree list`, which must show the primary checkout and the
 `.remedy-wt/job-*` worktrees constraint 6 names, and nothing else; `git stash list | head -1`,
 unchanged from the reading item 4 took; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be
 EMPTY. These readings go in your reply, since C6 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations, and
the next expected action. Report what you ran, not what you expected to find. Your Session
section reads SESSION 1 of feature F279, round 3, and says in one sentence how much context
you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review
of round 3, then T001's reader half — the direct `REMEDY_` reads moved onto one registry
reader. State the open-findings count, 26, and the operator-questions count, 0.
