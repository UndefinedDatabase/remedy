-- STEP R19 moot ids, dead residue, small repairs, D3 sentences -- F273 Findings paydown v1 --
Session 3 of F273 · round 19 · base `17c7f169` (the round 18 handoff, branch
`feature/f273-findings-paydown-v1`).

Goal: book round 18's verdict and three resolutions and the ids that are moot or met, land DECISION
F273 D19, and build the residue and repairs D19 names exactly as the reviewer's dry run built them.

Read first, completely: AGENTS.md; the payload `decisions.md` (DECISION F273 D19, this round's spec;
where this block is terser, it rules).

PAYLOADS: reviewer-authored, gitignored scratch. Verify each sha256 before use; any mismatch ->
stop and report. Apply byte-exact; never retype.
  `.remedy-wt/f273-r19/plan.md`        sha256 bf7253da371b8c5de9a4d15df345c2990e9da2da3bd1d7844298a34100de6957
  `.remedy-wt/f273-r19/ledger.md`      sha256 bb91f99bffd4f623cb1cd56159b5d2feac5c90088fa4b7548472ddac62c0ecaf
  `.remedy-wt/f273-r19/decisions.md`   sha256 1b81711711af72db93e81f6d2802d9c241444f002ecdf332b2f9996d34fb2a11
  `.remedy-wt/f273-r19/next.md`        sha256 97f9f07d0f666fb136d5df8c3f621c4e392e6f0c29599624437984a9ea4684db
  `.remedy-wt/f273-s3/r19_targets.txt` sha256 2a276ba1a4d6097a420b3a838497ce837fc47f3230c27b763101971fab9682ca
  `.remedy-wt/f273-r19/block.md`       this block (save it; report its sha256 and line count)
CODE: diffs the reviewer applied in this order at `17c7f169`, then ran and red-proved in its own
worktree. Apply with `git apply`; never edit a hunk:
  `.remedy-wt/f273-proto-g9a2.diff` sha256 9e13f8e517f05b54bb6635d07f2e8803cbdeabcb3b4dac04342cd81f2f991a34
  `.remedy-wt/f273-proto-g9b2.diff` sha256 2488836a2631a5d06897133da4cb915ac6229db7285c5c44c123de91370b0f78
  `.remedy-wt/f273-proto-g9c2.diff` sha256 0655371cda69637da8762992e5e8b8c261cbde275f99369d3cef7a1c2e55cfa4
Apply no other `.remedy-wt/*.diff` file (in particular not the older g9a, g9b and g9c).

Bundle (commit order):
C1 bookkeeping, one commit holding exactly:
   - byte copies of plan.md, ledger.md, decisions.md and block.md as `.agent/authored/f273-r19-<name>`;
   - `.agent/plan.md` := plan.md;
   - `.agent/live_review.md` and `.agent/decisions.md` := each one's `17c7f169` bytes + ledger.md and
     decisions.md respectively.
   Before this commit, compare the saved block copy's line count and sha256 with the block text you
   were given, and report both.
C2 R-0831, R-0832, R-0850, R-0941, R-0867, R-0863, R-0884: `git apply` g9a2.diff.
C3 R-0828, R-0826, R-0937: `git apply` g9b2.diff.
C4 R-0851, R-0852, R-0856, R-0860 (the command taxonomy): `git apply` g9c2.diff.
   Before each code commit run `git status --porcelain` and stage every path the apply touched,
   deletions included; nothing may be left untracked or unstaged.
C5 handoff: rewrite `.agent/handoff.md` per docs/agents/handback_template.md. Its Session section
   reads "SESSION 3 of feature F273 · round 19 · rounds so far 19", plus one sentence of context
   self-assessment. Include per-commit tables with `git show --numstat` counts for C1 to C4, every
   gate's real output, and open findings by distinct id (`count_open_findings`) on the committed
   ledger. Add one `Landed: R-xxxx` line naming its commit for each of R-0831, R-0832, R-0850,
   R-0941, R-0867, R-0863, R-0884, R-0828, R-0826, R-0937, R-0851, R-0852, R-0856 and R-0860, in the
   handoff only (for R-0851, R-0852, R-0856 and R-0860 name C1, which lands D19 (4), and C4); never
   write a `Done:` line of your own. Record under External actions that the branch
   `remedy/job-81ec65896729405c` still exists; a research helper's probe created it before round 16,
   and nobody may delete it without the operator. End with a `## Next` section whose body is next.md
   byte for byte, followed by the line "Operator questions open: <the count you read from the file>".
   Then `git push`. Open no pull request.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. No test may call a real provider or model. The shell denies `VAR=x cmd`, `cp`, loops, `$( )`,
   `$VAR` (including `$?`), heredocs and `cd` before git. Use `git -C <path>` and small python
   scripts under `.remedy-wt/f273-r19/`, with names prefixed `wk_` and an explicit `cwd=`. Copy a
   file with python, never with `cp`. Never use `git stash`.
3. Never weaken an assertion, and never delete a test except where the diffs carry that change. A
   red gate, or an ambiguity D19 does not settle -> stop, commit nothing half-done, and report.
4. Build every edited `.agent/` file from `git show 17c7f169:<path>` bytes.
5. Commit messages read "F273 R19 C<n>: <summary>", then a blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Never list, read or write any `.data/`. Never run `scripts/remedy_smoke.sh` or
   `scripts/make_review_zip.sh` yourself. Never run the `remedy` CLI, `run_job` against this
   repository, `npm install` or the self-use runner. Create no branch and delete no branch.

Done when (G1 to G5 run at C4, before C5; report literal output and the real exit code):
G1 transport + state + path sets: every payload and diff digest matched. A python check prints True
   for each of these:
   - `.agent/plan.md` equals its payload;
   - `.agent/live_review.md` and `.agent/decisions.md` each equal their `17c7f169` bytes + ledger.md
     and decisions.md;
   - each `.agent/authored/f273-r19-*` copy equals its payload;
   - `git show --name-only --format=` of each of C2, C3 and C4 lists exactly the paths
     `git apply --numstat` reads from its diff.
G2 code transport: `git rev-parse` of `<C4>:tests`, `<C4>:packages`, `<C4>:apps`, `<C4>:docs` and
   `<C4>:scripts` prints exactly 9e0972ba882e0f07dee9d883474344ccf27eca05,
   519a486b77948a2eabf0f3a45248265e56eaf712, 39a6be279a37193ae0ebcf00d97cadb542da960f,
   562fdc1bab1c8ed3e18aaa6f6de27116dce0cb86 and 866c1b06bafcedd6f4cca87b588dccae60d37531 (the
   reviewer's dry-run objects).
G3 in the primary checkout, serial (no `-n`): `python3 -m pytest -q -p no:cacheprovider` over every
   path in `.remedy-wt/f273-s3/r19_targets.txt` (one per line; read it, never edit it), through a
   script whose `env=` drops `REMEDY_OLLAMA_HOST` and `OLLAMA_HOST` -> summary line, 0 failed,
   exit 0, and no `R-0803:` line in the output.
G4 `python3 -m ruff check . --output-format concise` from the primary checkout's root ->
   "All checks passed!", exit 0; and `bash -n scripts/remedy_smoke.sh` -> exit 0.
G5 mutation red-proofs in ONE disposable worktree at `.remedy-wt/f273-r19-g5` (detached at C4).
   - Run from its root with `python3 -m pytest -q -p no:cacheprovider` and an env carrying
     `REMEDY_OLLAMA_HOST=http://127.0.0.1:9` and `OLLAMA_HOST=http://127.0.0.1:9` (through the
     script's `env=`).
   - Purge `__pycache__` before each run.
   - First print the imported `packages.orchestration.pingpong_job` path, to prove it resolves
     inside the worktree.
   - Run the UNMUTATED control first over the three test files named below; it must exit 0.
   - Then run each mutation below. Before each, count its FROM line (with its newline) in the named
     file; the count must be 1. Revert each file from its saved bytes before the next mutation.
     Name the failing ids.
   The test files: B = tests/orchestration/test_predictive_budget.py;
   S = tests/orchestration/test_self_use_findings.py; E = tests/orchestration/test_event_name_coupling.py.
   (a) `packages/orchestration/pingpong_job.py`: delete the line
   `    job.finished_at = datetime.now(timezone.utc).isoformat()   # R-0828` -> B fails;
   (b) `packages/orchestration/self_use_findings.py`: `    if result.run_manifest_error.strip():` ->
   `    if result.run_manifest_error.strip() and False:` -> S fails;
   (c) E itself: `KNOWN_DEAD_EVENT_COUPLINGS: tuple[str, ...] = ()` ->
   `KNOWN_DEAD_EVENT_COUPLINGS: tuple[str, ...] = ("context_budget_optimized",)` -> E fails.
   Report exit codes and failing ids. If a mutation stays green, report it as green. Then remove the
   worktree as this step's last action and show `git worktree list`.
G6 after the push: `git status --porcelain` is empty, the local tip equals origin, and
   `git branch --list "remedy/job-*"` still counts 37. Report this in your final message only, since
   the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput).
-- end of block --
