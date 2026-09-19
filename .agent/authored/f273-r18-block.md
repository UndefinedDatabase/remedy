-- STEP R18 check bytecode, do milestones, memory candidates -- F273 Findings paydown v1 --
Session 3 of F273 · round 18 · base `f445a2c0` (the round 17 handoff, branch
`feature/f273-findings-paydown-v1`).

Goal: book round 17's verdict and three resolutions, register R-0993, land DECISION F273 D18 and the
third ruling of operator question Q4, and build R-0993, R-0977 and R-0992 exactly as the reviewer's
dry run built them.

Read first, completely: AGENTS.md; the payload `decisions.md` (DECISION F273 D18, this round's spec;
where this block is terser, it rules).

PAYLOADS: reviewer-authored, gitignored scratch. Verify each sha256 before use; any mismatch ->
stop and report. Apply byte-exact; never retype.
  `.remedy-wt/f273-r18/plan.md`               sha256 745fad92f74191b5fd24f7b2eafd0596e0fff45389d85ee5140f5fdf3e730d4c
  `.remedy-wt/f273-r18/ledger.md`             sha256 796c01c3e202e4f3fe368480b1f89744a53cf8d1fc5cc95e0e175d9a063c643b
  `.remedy-wt/f273-r18/decisions.md`          sha256 1a9751de60d0c18c9c149d123c3987ffdd6ae1946817bf7dad719093bfeb94bd
  `.remedy-wt/f273-r18/operator_questions.md` sha256 7485f840f6c197585ed7c6617220323098f9ba233850d2002a4c4f15ae4f43aa
  `.remedy-wt/f273-r18/next.md`               sha256 a167c17a4d39f12360fba0de7b748555ed6ace30fb63e40b5cfaaea1f53ea362
  `.remedy-wt/f273-s3/r18_targets.txt`        sha256 835b6f3a0352a49642ad302074fc81f6e60ca2d90fb74204a9f1a803c36f2be3
  `.remedy-wt/f273-r18/block.md`              this block (save it; report its sha256 and line count)
CODE: diffs the reviewer applied in this order on the tree of `f445a2c0`, then ran and red-proved in
its own worktree. Apply with `git apply`; never edit a hunk:
  `.remedy-wt/f273-proto-g8a.diff` sha256 3de53880e4559fd6a58869a4e5f91c2fe818957f216eae6a62b0dd4e8e8daf83
  `.remedy-wt/f273-proto-g8b.diff` sha256 9112a626feb494f47a80ebf6687988572afb7aa9d1a8a082a83ac1718ab34261
  `.remedy-wt/f273-proto-g8c.diff` sha256 cb6b854dead7ef5be4d500e6f0f8124568e75be4274568ccc04b5addb71b5ccc
Apply no other `.remedy-wt/*.diff` file (in particular not `f273-proto-g8.diff`, the combined copy).

Bundle (commit order):
C1 bookkeeping, one commit holding exactly:
   - byte copies of plan.md, ledger.md, decisions.md, operator_questions.md and block.md as
     `.agent/authored/f273-r18-<name>`;
   - `.agent/plan.md` := plan.md and `.agent/operator_questions.md` := operator_questions.md;
   - `.agent/live_review.md` and `.agent/decisions.md` := each one's `f445a2c0` bytes + ledger.md
     and decisions.md respectively.
   Before this commit, compare the saved block copy's line count and sha256 with the block text you
   were given, and report both.
C2 R-0993: `git apply` g8a.diff.
C3 R-0977: `git apply` g8b.diff.
C4 R-0992: `git apply` g8c.diff.
   Before each code commit run `git status --porcelain` and stage every path the apply touched,
   deletions included; nothing may be left untracked or unstaged.
C5 handoff: rewrite `.agent/handoff.md` per docs/agents/handback_template.md. Its Session section
   reads "SESSION 3 of feature F273 · round 18 · rounds so far 18", plus one sentence of context
   self-assessment. Include per-commit tables with `git show --numstat` counts for C1 to C4, every
   gate's real output, and open findings by distinct id (`count_open_findings`) on the committed
   ledger. Add one `Landed: R-xxxx` line naming its commit for each of R-0993, R-0977 and R-0992, in
   the handoff only; never write a `Done:` line of your own. Record under External actions that the
   branch `remedy/job-81ec65896729405c` still exists; a research helper's probe created it before
   round 16, and nobody may delete it without the operator. End with a `## Next` section whose body
   is next.md byte for byte, followed by the line "Operator questions open: <the count you read from
   the file>". Then `git push`. Open no pull request.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. No test may call a real provider or model. The shell denies `VAR=x cmd`, `cp`, loops, `$( )`,
   `$VAR` (including `$?`), heredocs and `cd` before git. Use `git -C <path>` and small python
   scripts under `.remedy-wt/f273-r18/`, with names prefixed `wk_` and an explicit `cwd=`. Copy a
   file with python, never with `cp`. Never use `git stash`.
3. Never weaken an assertion, and never delete a test except where the diffs carry that change. A
   red gate, or an ambiguity D18 does not settle -> stop, commit nothing half-done, and report.
4. Build every edited `.agent/` file from `git show f445a2c0:<path>` bytes.
5. Commit messages read "F273 R18 C<n>: <summary>", then a blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Never list, read or write any `.data/`. Never run `scripts/remedy_smoke.sh` or
   `scripts/make_review_zip.sh` yourself. Never run the `remedy` CLI, `run_job` against this
   repository, `npm install` or the self-use runner. Create no branch and delete no branch.

Done when (G1 to G5 run at C4, before C5; report literal output and the real exit code):
G1 transport + state + path sets: every payload and diff digest matched. A python check prints True
   for each of these:
   - `.agent/plan.md` and `.agent/operator_questions.md` equal their payloads;
   - `.agent/live_review.md` and `.agent/decisions.md` each equal their `f445a2c0` bytes +
     ledger.md and decisions.md;
   - each `.agent/authored/f273-r18-*` copy equals its payload;
   - `git show --name-only --format=` of each of C2, C3 and C4 lists exactly the paths
     `git apply --numstat` reads from its diff.
G2 code transport: `git rev-parse` of `<C4>:tests`, `<C4>:packages`, `<C4>:apps`, `<C4>:docs` and
   `<C4>:scripts` prints exactly a52f51b4dd93071e87afe8d23dc04a9bff425d99,
   9754f8efaa0572938f7ca34549d377a1c3912407, 606b88b001ea70d32e9fa6d41e2fc2d64e95a426,
   f10debd13cab12e3de9e9289f6280395cae8e590 and 9dfa0d7d9f2824f65dbf9cc094ec2e1047b93e18 (the
   reviewer's dry-run objects).
G3 in the primary checkout, serial (no `-n`): `python3 -m pytest -q -p no:cacheprovider` over every
   path in `.remedy-wt/f273-s3/r18_targets.txt` (one per line; read it, never edit it), through a
   script whose `env=` drops `PYTHONDONTWRITEBYTECODE` -> summary line, 0 failed, exit 0, and no
   `R-0803:` line in the output.
G4 `python3 -m ruff check . --output-format concise` from the primary checkout's root ->
   "All checks passed!", exit 0; and `bash -n scripts/remedy_smoke.sh` -> exit 0.
G5 mutation red-proofs in ONE disposable worktree at `.remedy-wt/f273-r18-g5` (detached at C4).
   - Run from its root with `python3 -m pytest -q -p no:cacheprovider` and an env carrying
     `REMEDY_OLLAMA_HOST=http://127.0.0.1:9` and `OLLAMA_HOST=http://127.0.0.1:9`, with
     `PYTHONDONTWRITEBYTECODE` removed (through the script's `env=`).
   - Purge `__pycache__` before each run.
   - First print the imported `packages.orchestration.do_sequence` path, to prove it resolves
     inside the worktree.
   - Run the UNMUTATED control first over the three test files named below; it must exit 0.
   - Then run each mutation below. Before each, count its FROM line (with its newline) in the named
     file; the count must be 1. Revert each file from its saved bytes before the next mutation.
     Name the failing ids.
   The test files: D = tests/cli/test_do_sequence_cli.py; R = tests/orchestration/test_dod_runners.py;
   F = tests/cli/test_do_commit_flags.py.
   (a) `packages/orchestration/exec_guard.py`:
   `        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},` -> `        env=None,` -> D and R
   fail;
   (b) `packages/orchestration/dod_runners.py`:
   `    return [PYTEST_PYTHON, "-m", "pytest", "-p", "no:cacheprovider", str(spec["selector"]),` ->
   `    return [PYTEST_PYTHON, "-m", "pytest", str(spec["selector"]),` -> R fails;
   (c) `packages/orchestration/do_sequence.py`: `            record_job_milestone(job_id, milestone_id)`
   -> `            pass` -> D fails;
   (d) `packages/orchestration/mission_contract.py`:
   `                                                 and hold_on_milestone)})` ->
   `                                                 )})` -> D and F fail.
   Report exit codes and failing ids (the first eight per mutation are enough, plus the count). If a
   mutation stays green, report it as green. Then remove the worktree as this step's last action and
   show `git worktree list`.
G6 after the push: `git status --porcelain` is empty, the local tip equals origin, and
   `git branch --list "remedy/job-*"` still counts 37. Report this in your final message only, since
   the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput).
-- end of block --
