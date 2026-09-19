-- STEP R17 attestation writer, worker queue -- F273 Findings paydown v1 --
Session 3 of F273 · round 17 · base `9e753ffc` (the round 16 handoff, branch
`feature/f273-findings-paydown-v1`).

Goal: book round 16's verdict and nine resolutions, register R-0992, land DECISION F273 D17, and
build R-0914, R-0927 and R-0928 exactly as the reviewer's dry run built them.

Read first, completely: AGENTS.md; the payload `decisions.md` (DECISION F273 D17, this round's spec;
where this block is terser, it rules).

PAYLOADS: reviewer-authored, gitignored scratch. Verify each sha256 before use; any mismatch ->
stop and report. Apply byte-exact; never retype.
  `.remedy-wt/f273-r17/plan.md`       sha256 5b6f35fbf7d78dcefa5c265cc16b84da584d96519ee640a5e379f602cd0b5e8c
  `.remedy-wt/f273-r17/ledger.md`     sha256 db381dba776307d4c77d220a5fd012176b985b8b517b0a60a4d95cdea6315003
  `.remedy-wt/f273-r17/decisions.md`  sha256 1c0deae5a0bd9ae49c1137c670f0451a878f15721017660c5a9dcb997d11c832
  `.remedy-wt/f273-r17/slips.md`      sha256 87369fb1be614791839d1d58f80d6868ea12dc0e8bd8f0b132531d832576f8ee
  `.remedy-wt/f273-r17/next.md`       sha256 7b8adee05c0656984bd48c65861416c54dd6603ffbc76a0d09b52fa203a76e47
  `.remedy-wt/f273-s3/r17_targets.txt` sha256 92cd45f21b58c0166170272e3d5b1c771275864926574d15441c1bb6a5b5e9ab
  `.remedy-wt/f273-r17/block.md`      this block (save it; report its sha256 and line count)
CODE: diffs the reviewer applied in this order at `9e753ffc`, then ran and red-proved in its own
worktree. Apply with `git apply`; never edit a hunk:
  `.remedy-wt/f273-proto-g7c2.diff` sha256 0ac403ff52ada744d5b978d77e476275ff80a13294ea1942a6e3d2e81b633dc8
  `.remedy-wt/f273-proto-g7b2.diff` sha256 cf432c2ffd29083acb3216a38b5aa27cbb60f92f0f00991260387cfcde658726
  `.remedy-wt/f273-s3/r17_docs.diff` sha256 e6894ea1e00138b0b74eeab8201b91e473c4e3ae34f248af0b7a242d158ca088
Apply no other `.remedy-wt/*.diff` file.

Bundle (commit order):
C1 bookkeeping, one commit holding exactly: byte copies of plan.md, ledger.md, decisions.md, slips.md
   and block.md as `.agent/authored/f273-r17-<name>`; `.agent/plan.md` := plan.md;
   `.agent/live_review.md`, `.agent/decisions.md` and `.agent/prose_slips.md` := each one's
   `9e753ffc` bytes + ledger.md, decisions.md and slips.md respectively. Before this commit, compare
   the saved block copy's line count and sha256 with the block text you were given, and report both.
C2 R-0914: `git apply` g7c2.diff.
C3 R-0927, R-0928: `git apply` g7b2.diff.
C4 R-0914's Acceptance line: `git apply` r17_docs.diff.
   Before each code commit run `git status --porcelain` and stage every path the apply touched,
   deletions included; nothing may be left untracked or unstaged.
C5 handoff: rewrite `.agent/handoff.md` per docs/agents/handback_template.md. Its Session section
   reads "SESSION 3 of feature F273 · round 17 · rounds so far 17", plus one sentence of context
   self-assessment. Include per-commit tables with `git show --numstat` counts for C1 to C4, every
   gate's real output, and open findings by distinct id (`count_open_findings`) on the committed
   ledger. Add one `Landed: R-xxxx` line naming its commit for each of R-0914, R-0927 and R-0928, in
   the handoff only; never write a `Done:` line of your own. Record under External actions that the
   branch `remedy/job-81ec65896729405c` still exists; a research helper's probe created it before
   round 16, and nobody may delete it without the operator. End with a `## Next` section whose body
   is next.md byte for byte, followed by the line "Operator questions open: <the count you read from
   the file>". Then `git push`. Open no pull request.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. No test may call a real provider or model. The shell denies `VAR=x cmd`, `cp`, loops, `$( )`,
   `$VAR` (including `$?`), heredocs and `cd` before git. Use `git -C <path>` and small python
   scripts under `.remedy-wt/f273-r17/`, with names prefixed `wk_` and an explicit `cwd=`. Never
   use `git stash`.
3. Never weaken an assertion, and never delete a test except where the diffs carry that change. A
   red gate, or an ambiguity D17 does not settle -> stop, commit nothing half-done, and report.
4. Build every edited `.agent/` file from `git show 9e753ffc:<path>` bytes.
5. Commit messages read "F273 R17 C<n>: <summary>", then a blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Never list, read or write any `.data/`. Never run `scripts/remedy_smoke.sh` or
   `scripts/make_review_zip.sh` yourself (tests that call it redirect it through
   `tests/conftest.py`). Never run the `remedy` CLI, `run_job` against this repository,
   `npm install` or the self-use runner. Create no branch and delete no branch.

Done when (G1 to G5 run at C4, before C5; report literal output and the real exit code):
G1 transport + state + path sets: every payload and diff digest matched. A python check prints True
   for each of these:
   - `.agent/plan.md` equals its payload;
   - `.agent/live_review.md`, `.agent/decisions.md` and `.agent/prose_slips.md` each equal their
     `9e753ffc` bytes + ledger.md, decisions.md and slips.md;
   - each `.agent/authored/f273-r17-*` copy equals its payload;
   - `git show --name-only --format=` of each of C2, C3 and C4 lists exactly the paths
     `git apply --numstat` reads from its diff.
G2 code transport: `git rev-parse <C4>:tests <C4>:packages <C4>:apps <C4>:docs` prints exactly
   85eed96929750b60a5d3d74261c991cc2e3dc191, c4e15508a4fae8d1e0d0f143552c4679612a813a,
   448e1225c49f39fed56da7cf75587294e9652908 and e80ecf9e6339fffef23603f9ac12405a02371023 (the
   reviewer's dry-run objects).
G3 in the primary checkout, serial (no `-n`): `python3 -m pytest -q -p no:cacheprovider` over every
   path in `.remedy-wt/f273-s3/r17_targets.txt` (one per line; read it, never edit it) -> summary
   line, 0 failed, exit 0, and no `R-0803:` line in the output.
G4 `python3 -m ruff check . --output-format concise` from the primary checkout's root ->
   "All checks passed!", exit 0.
G5 mutation red-proofs in ONE disposable worktree at `.remedy-wt/f273-r17-g5` (detached at C4).
   - Run from its root with `python3 -B -m pytest -q -p no:cacheprovider` and an env carrying
     `REMEDY_OLLAMA_HOST=http://127.0.0.1:9` and `OLLAMA_HOST=http://127.0.0.1:9` (through the
     script's `env=`).
   - Purge `__pycache__` before each run.
   - First print the imported `packages.orchestration.ui_server` path, to prove it resolves inside
     the worktree.
   - Run the UNMUTATED control first over the five test files named below; it must exit 0.
   - Then run each mutation below. Before each, count its FROM line (with its newline) in the named
     file; the count must be 1. Revert each file from its saved bytes before the next mutation.
     Name the failing ids.
   The test files: T = tests/orchestration/test_test_runner.py;
   P = tests/ui_server/test_pipeline_contract.py; C = tests/orchestration/test_proof_chain.py;
   U = tests/ui_contracts/test_humanize_catalog.py;
   E = tests/orchestration/test_event_name_coupling.py.
   (a) `packages/orchestration/hunk_apply.py`: delete the line `        job=job,` -> T fails;
   (b) `packages/orchestration/ui_server.py`: `        model_confidence = "low"` ->
   `        model_confidence = "high"` -> P fails;
   (c) the same file: `        "source_context": {"injected": False},` ->
   `        "source_context": {"injected": True},` -> P fails;
   (d) `packages/orchestration/proof_chain.py`:
   `        if ename in ("test_run_completed", "test_run_timed_out"):` ->
   `        if ename in ("test_run_timed_out",):` -> C fails;
   (e) `apps/ui/src/api/humanizeCatalog.ts`: delete the line
   `  "revert_completed": "Reverting the apply finished.",` -> U fails;
   (f) E itself: `        return {node.value}` -> `        return set()` -> E fails.
   Report exit codes and failing ids. If a mutation stays green, report it as green. Then remove the
   worktree as this step's last action and show `git worktree list`.
G6 after the push: `git status --porcelain` is empty and the local tip equals origin. Report this in
   your final message only, since the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput).
-- end of block --
