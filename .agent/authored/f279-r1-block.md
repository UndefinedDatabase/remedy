STEP F279 R1 — CLAIM F279 AND LAND T002: the hash-pinned toolchain

GOAL
Pull request 266 is merged; `main` is at `c9bc5c20` and F279 is the next unchecked line.
Cut its branch, claim it, re-head the live review record, record DECISION F279 D1 with the
feature file's T002 amendment, and land T002: upper bounds on `pydantic` and `psutil`, a
GENERATED hash-pinned `constraints.txt`, the two-step pinned install in CI, and the tests that
hold all of it, each guard with a red proof.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run
the self-review loop before every commit, keep the tree clean, push, and write the
handback. You never issue a verdict and you never merge.

WHY T002 IS FIRST, AND WHY IT IS RE-STATED
T2_F279.md's Orchestrator brief puts T002 first. The slice as registered was measured at
`a5bf8949`; at `c9bc5c20` its lint ceiling no longer exists, `ruff` is already pinned, and pip
refuses `pip install -e ... -c <hashed file>` because one hash turns on hash-checking mode for
the whole install, which cannot hash an editable project. DECISION F279 D1 (the
decisions.diff payload) rules the replacement: the hashed file installs alone with
`--require-hashes -r`, Remedy follows with `--no-deps -e .`, then `pip check`. The reviewer
measured each of those steps on Python 3.10 and 3.12 with pip 26.2.1, each at real exit code 0,
and a corrupted ruff hash failing the first step at exit code 1.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f279-r1-payloads/`  READ-ONLY. The reviewer's originals. Never write here.
  `.remedy-wt/f279-venv310/`      READ-ONLY. A scratch venv holding `uv` 0.12.18, the
      generator. Run its binary; never install into it or change it.
  `.remedy-wt/f279-r1-scratch/`   YOURS for logs and scripts. Each is gitignored. The
      reviewer left its own `sim.py` in scratch; do not edit or delete it.

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
   and `git log --oneline -1` must read `c9bc5c20`. Report all three. Then
   `git checkout -b feature/f279-configuration-toolchain-truth` and report the branch. Do
   NOT pull: the Open PR Gate ran before you and `main` is already at the merge commit.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f279-r1-block.md` and compare both with the two readings your delegation
   message states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list` and `git branch --list 'remedy/job-*' | wc -l` as found.

PAYLOADS — under `.remedy-wt/f279-r1-payloads/`, lines = newline count.
Verify each one's line count, byte count and sha256 BEFORE using it and report every
reading. Never retype a payload; never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| status.diff | 13 | 1973 | 32ae7209b1a6cc5c40247702db093e4a359f5ae05af910c7181bfd6e87d0a879 |
| rehead.diff | 51 | 5850 | 47101839a084e35999a66854d5c258a60f3ff51a43702c5d4a550c184683a4d0 |
| plan.md | 34 | 1456 | bc0ac652719ae19919021888e240bd2c7a3dc1f6779a6897c6727f04a27d1176 |
| context.md | 47 | 2229 | 235d0f3bb6b11e3b7d6b4150f407fb83dfba52373aba2bb85f2363f3ac520ee0 |
| decisions.diff | 48 | 3494 | 281fb6005f411f2fbf29a37657e5008840e25bc719f87f8656e3acee44b6d212 |
| feature.diff | 36 | 2564 | 51f30833db20ec0844a72526dcbb0bb5a7f97ed27d26c988d12af4b7302eb420 |
| pyproject.diff | 15 | 642 | 885e4b51ce6ae3a0cf77e88e483f21a0b236250d12ca4e2a5f348b37f49886db |
| ci.diff | 36 | 1822 | d5ec59246023d9a35f1ef8cdfa97c7435893f6dceb1564b38e497d35e903e20e |
| readme.diff | 19 | 483 | cb574849619994c5027ad38edadaf65334fb554364df41177f7ea7911ed3b05a |
| test_ci_workflow.diff | 28 | 1572 | b4cb8404dfe2172aa532765dc1fe26a82bd00e74d2613bdb801b06772096e003 |
| test_toolchain_pins.py | 113 | 5164 | e7d5112feb55ade8614b1a6eff6798644116da075cb6cde5431e70b8c6f381ad |
| mutations.py | 84 | 3097 | 9c5d4b8145d31b9bba9a76e4ce61935830c7bf79c5c068ccfbabea8938d4ced7 |

`plan.md` and `context.md` are REWRITES of `.agent/plan.md` and `.agent/context.md`.
`test_toolchain_pins.py` is a NEW FILE at `tests/orchestration/test_toolchain_pins.py`,
copied whole. The `.diff` files go on with `git apply`; the reviewer generated every one from
a tree at `c9bc5c20` and applied all of them, in the commit order below, to a fresh worktree
at `c9bc5c20` with `git apply --check` then `git apply`, every one at real exit code 0.
`mutations.py` is a TOOL for G5: it is run, never applied to a tracked file.

`constraints.txt` IS NOT A PAYLOAD. It is GENERATED in C5 by the command its own header
records, and the reviewer ran that command twice from two trees and read the same bytes.

BUNDLE — the commits are C1a, C1b, C2, C3, C4, C5, C6 and C7, in this order.

C1a — copy this block and the bookkeeping payloads
  `.agent/authored/f279-r1-block.md` := this block, and one
  `.agent/authored/f279-r1-<name>` for each of status.diff, rehead.diff, plan.md,
  context.md, decisions.diff and feature.diff, keeping each payload's own file name. All by
  `shutil.copyfile`.
  Subject: `F279 R1 C1a: copy round 1 block and bookkeeping payloads into .agent/authored/`
  Its insertions are this block's line count plus 229. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C1b — copy the product payloads
  `.agent/authored/f279-r1-<name>` for each of pyproject.diff, ci.diff, readme.diff,
  test_ci_workflow.diff, test_toolchain_pins.py and mutations.py, by `shutil.copyfile`.
  Subject: `F279 R1 C1b: copy round 1 product payloads into .agent/authored/`
  Expected insertions: 295.

C2 — THE CLAIM, in this order:
   1. `git apply` rehead.diff  → `.agent/live_review.md`
   2. `git apply` status.diff  → `docs/roadmap/STATUS.md`
   3. rewrite `.agent/plan.md` := plan.md
   4. rewrite `.agent/context.md` := context.md
  Subject: `F279 R1 C2: claim F279 and re-head the live review record`
  Expected insertions by `git show --numstat`: 17 context.md, 18 live_review.md, 21 plan.md,
  1 STATUS.md.

C3 — THE DECISION AND THE FEATURE-FILE AMENDMENT
  `git apply` decisions.diff → `.agent/decisions.md`, then feature.diff →
  `docs/roadmap/features/T2_F279.md`.
  Subject: `F279 R1 C3: record DECISION F279 D1 and amend T002 to the tree`
  Expected insertions: 40 decisions.md, 14 T2_F279.md.

C4 — THE UPPER BOUNDS
  `git apply` pyproject.diff → `pyproject.toml`.
  Subject: `F279 R1 C4: bound pydantic and psutil below their next major version`
  Expected insertions: 3.

C5 — THE GENERATED CONSTRAINTS FILE, alone in its commit. From the repository root, run
  EXACTLY this one command line and report its real exit code:
  ```
  bash -c '.remedy-wt/f279-venv310/bin/uv pip compile pyproject.toml --extra dev --extra ollama --universal --python-version 3.10 --generate-hashes --no-annotate --exclude-newer 2026-09-23T00:00:00Z -o constraints.txt -q; echo "REAL_EXIT=$?"'
  ```
  It needs the network to reach PyPI. If it exits non-zero, STOP under constraint 4.
  `git add constraints.txt`.
  Subject: `F279 R1 C5: add constraints.txt, the generated hash-pinned toolchain`
  Expected insertions: 652. THIS IS F279'S ONE DECLARED OVERSIZE COMMIT under the AGENTS.md
  size exception: declare it in the handback with this reason — "a generated lockfile is one
  indivisible artifact; splitting it would leave a commit whose pinned set pip refuses, and the
  file is reproduced byte for byte by the command in its own header (DECISION F279 D1)".

C6 — CI, README AND THE GUARDS in one commit, because the tests are what verify C4 to C6
  `git apply` ci.diff → `.github/workflows/ci.yml`, readme.diff → `README.md`,
  test_ci_workflow.diff → `tests/orchestration/test_ci_workflow.py`; then copy
  test_toolchain_pins.py to `tests/orchestration/test_toolchain_pins.py` and `git add` it —
  an untracked test file fails `integrity check`'s `relevant_untracked`.
  Subject: `F279 R1 C6: install the pinned toolchain in CI and guard it`
  Expected insertions: 16 ci.yml, 8 README.md, 20 test_ci_workflow.py,
  113 test_toolchain_pins.py.

C7 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F279 R1 C7: rewrite handoff for round 1`
  Then `git push -u origin feature/f279-configuration-toolchain-truth`. Do NOT create a pull
  request: the branch opens one at F279's closure. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code. Never edit `constraints.txt` by hand.
2. Every commit other than C5 stays under 500 insertions by the `git show --numstat`
   reading; see C1a.
3. The round's whole tracked path set is: the `.agent/authored/f279-r1-*` copies,
   `.agent/live_review.md`, `docs/roadmap/STATUS.md`, `.agent/plan.md`, `.agent/context.md`,
   `.agent/decisions.md`, `docs/roadmap/features/T2_F279.md`, `pyproject.toml`,
   `constraints.txt`, `.github/workflows/ci.yml`, `README.md`,
   `tests/orchestration/test_ci_workflow.py`, `tests/orchestration/test_toolchain_pins.py`
   and `.agent/handoff.md`. Report the list you measure with
   `git diff --name-only c9bc5c20 HEAD` after C7. Do NOT touch `.agent/prose_slips.md`,
   `.agent/candidates.md`, `.agent/operator_questions.md`, anything under `packages/` or
   `apps/`, or `.github/workflows/release.yml`.
4. If a gate goes red, STOP, commit and push what is verified, write an honest handoff
   under AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads.
5. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main` after the
   branch is cut, no branch deletion, no force-push, no `git stash`.
6. Leave `.remedy-wt/job-129b3ad7206d4f8d`, `.remedy-wt/job-e7268925db3a4831`, their branches
   and every existing stash alone. Install NOTHING into the primary checkout's Python: this
   round pins what CI installs, not the developer's environment (DECISION F279 D1 (5)). The
   worktree G5 adds goes under `.remedy-wt/`, is removed as that step's last action, and
   `git worktree list` is reported afterwards (finding R-0940).
7. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run
   and F279's belongs to its closure.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G5 run before C7 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f279-r1-*` copy byte for
 byte with its source (the block copy against `.remedy-wt/f279-r1-block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE BOOKKEEPING — the sha256 of each file below, read with `git show <commit>:<path>` at
 the commit named, equals the reviewer's reading, which its simulation printed from a tree it
 built by applying these payloads at `c9bc5c20`:
 | commit | path | bytes | sha256 |
 |---|---|---|---|
 | C2 | .agent/live_review.md | 374034 | 67d2b5d02211b7b37453260a860e563ff986f8cc31eb8697f50d3e35dadb1820 |
 | C2 | docs/roadmap/STATUS.md | 47144 | 913d3124e94e6b6f5b1090a48a8c635bb2b8909c264a78c3444a24a2774955ee |
 | C2 | .agent/plan.md | 1456 | bc0ac652719ae19919021888e240bd2c7a3dc1f6779a6897c6727f04a27d1176 |
 | C2 | .agent/context.md | 2229 | 235d0f3bb6b11e3b7d6b4150f407fb83dfba52373aba2bb85f2363f3ac520ee0 |
 | C3 | .agent/decisions.md | 1859397 | d2ae7ef5d5835d05e1321a2cc1cb6f46b129ccaaf4c5ad9c0771dbf5c2614c1c |
 | C3 | docs/roadmap/features/T2_F279.md | 7780 | 4724aa541ce75eb609f899a611157a6ad4fc11af28edf31c3d6cbb9bb5c6ee9e |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT, at `c9bc5c20` and at C2, with the set
 difference in both directions (the reviewer read 26 and 26, both differences empty); F279's
 STATUS line at C2 read back in full, which must begin `- [~] F279 — `; and
 `git diff --name-only <C1b> <C2>` and `git diff --name-only <C2> <C3>`, which must name
 exactly the paths C2 and C3 list.

G3 THE PRODUCT — at C6, the sha256 of each file below, read with `git show <C6>:<path>`,
 equals the reviewer's simulated reading:
 | path | bytes | sha256 |
 |---|---|---|
 | pyproject.toml | 5766 | 4817c168fc2dbaac617478d9eb86552bc7dfb8a443388440433d648061063e4c |
 | constraints.txt | 53521 | 7e6649c616a2c9facccb9241ad1385126094f388c203c7f7023bd148e7e92dbb |
 | .github/workflows/ci.yml | 4606 | e53a3e1580aa130d0c00690e9bded09bef0acc5cf451b2cdc4dc1f7e5037f5a4 |
 | README.md | 23594 | 6bf8b865dbc1f93e484d2f431587f074b1e7ff1cb4e279e7a8eb1388e6af7870 |
 | tests/orchestration/test_ci_workflow.py | 4244 | 7b016456ea223acc78db4baba0b18621b67a4e66d5664ff0edbe73b602238abb |
 | tests/orchestration/test_toolchain_pins.py | 5164 | e7d5112feb55ade8614b1a6eff6798644116da075cb6cde5431e70b8c6f381ad |
 A `constraints.txt` digest that differs means PyPI answered differently from the reviewer's
 run: report both digests and `git diff --no-index` of the two files' pin lines, and STOP.
 Also `git diff --name-only <C3> <C4>`, `<C4> <C5>` and `<C5> <C6>`, which must name exactly
 the paths C4, C5 and C6 list.

G4 THE TESTS — in the primary checkout at C6, with real exit codes:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_toolchain_pins.py tests/orchestration/test_ci_workflow.py tests/docs/ tests/orchestration/test_roadmap_index.py tests/orchestration/test_ci_budgets.py tests/orchestration/test_ci_stages.py tests/orchestration/test_ci_stage_selection.py tests/test_install_smoke.py tests/test_packaging_smoke.py tests/test_ble001_ratchet.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/regression/test_resource_safety.py tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_review_archive_authority.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the same selection WITHOUT the golden path inside a disposable worktree
 carrying C2 to C6 and read `620 passed, 3 skipped` at real exit code 0; the primary
 checkout carries the UI toolchain a worktree lacks, so a skip may pass there. Report what
 you read. Then `python3 -m ruff check tests/orchestration/test_toolchain_pins.py
 tests/orchestration/test_ci_workflow.py`, real exit code 0, and
 `python3 -m apps.cli.main integrity check --json`, which must read all five checks `pass`
 at `fail_count` 0.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f279-r1-mut <C6>`, then
 `python3 -B .remedy-wt/f279-r1-payloads/mutations.py .remedy-wt/f279-r1-mut` and report its
 whole output. The script asserts each FROM occurs exactly once, applies it, runs the
 guard files under `python3 -B`, restores the bytes, and runs an unmutated control first and
 last. The reviewer read, over the same script against its own tree carrying C2 to C6:
 control_before `15 passed` at exit 0;
 m1 (`--require-hashes` dropped from the install) 1 failed at exit 1, at
   `test_hosted_workflow_installs_the_hash_pinned_toolchain_before_remedy`;
 m2 (the pip cache key dropped) 1 failed at exit 1, at
   `test_hosted_workflow_keys_its_pip_cache_on_the_pinned_set`;
 m3 (the pyproject ruff pin moved) 2 failed at exit 1, at
   `test_every_declared_dependency_is_pinned_inside_its_declared_range` and
   `test_the_pinned_ruff_is_the_ruff_the_lint_gate_is_pinned_to`;
 m4 (psutil's upper bound removed) 1 failed at exit 1, at
   `test_the_runtime_dependencies_carry_an_upper_bound`;
 m5 (every ruff hash stripped) 1 failed at exit 1, at
   `test_every_pin_is_exact_and_carries_a_hash`;
 m6 (the psutil pin removed) 1 failed at exit 1, at
   `test_every_declared_dependency_is_pinned_inside_its_declared_range`;
 control_after `15 passed` at exit 0.
 Then `git worktree remove --force .remedy-wt/f279-r1-mut`, `git worktree prune`, and report
 `git worktree list`.

G6 TREE AND PUSH — after C7: `git status --porcelain`, which must be empty;
 `git log --oneline -n 9`, which must show C7, C6, C5, C4, C3, C2, C1b, C1a and `c9bc5c20` in
 that order; `git worktree list`, which must show the primary checkout and the
 `.remedy-wt/job-*` worktrees constraint 6 names, and nothing else; the push's real outcome; and
 `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be
 EMPTY. These readings go in your reply, since C7 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates: the state
block, the per-commit changed-files table with the insertion count you MEASURED beside the one
this block expected, every gate's real output and exit code, the authored-text proofs, the
item-status table AGENTS.md requires (one row per commit and per gate), the deviations —
including the C5 oversize declaration — and the next expected action. Report what you ran,
not what you expected to find. Your Session section reads SESSION 1 of feature F279, round 1,
and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review
of round 1, then T001 — the environment-variable registry, re-derived from the tree. State
the open-findings count, 26, and the operator-questions count, 0.
